"""LangGraph pipeline: transcript_fetch → place_extraction → geocoding → clustering → labeling."""
from __future__ import annotations
import asyncio
from datetime import date
from typing import Any, Optional
from typing_extensions import TypedDict

from langgraph.graph import StateGraph, END

from .models import (
    PlanRequest,
    PlanResponse,
    DayCluster,
    Place,
    HotelPin,
    SourceVideo,
)
from .agents import transcript as transcript_agent
from .agents import extractor as extractor_agent
from .agents import geocoder as geocoder_agent
from .agents import clusterer as clusterer_agent
from .agents import labeler as labeler_agent


# ── State ──────────────────────────────────────────────────────────────────


class PipelineState(TypedDict):
    request: dict                   # PlanRequest.model_dump()
    _queue: Any                     # asyncio.Queue | None — for SSE progress events
    transcripts: list               # [{url, video_id, title, transcript, error}]
    raw_places: list                # [{name, sentiment, context, source_videos}]
    enriched: list                  # [{name, lat, lng, ..., source_videos}]
    unresolved: list                # [place_name, ...]
    clusters: list                  # list of list of place dicts
    overflow: list                  # overflow places → "More to Explore"
    labels: list                    # theme label per cluster
    hotel: Optional[dict]           # {name, lat, lng} | None
    error: Optional[str]
    error_code: Optional[str]


# ── Helpers ────────────────────────────────────────────────────────────────


async def _emit(queue: Any, event: dict) -> None:
    if queue is not None:
        await queue.put(event)


def _num_days(req: dict) -> int | None:
    sd = req.get("start_date")
    ed = req.get("end_date")
    if sd and ed:
        try:
            delta = date.fromisoformat(ed) - date.fromisoformat(sd)
            return max(1, delta.days + 1)
        except ValueError:
            pass
    return None


# ── Nodes ──────────────────────────────────────────────────────────────────


async def fetch_transcripts(state: PipelineState) -> dict:
    req = state["request"]
    queue = state.get("_queue")

    await _emit(queue, {"type": "progress", "step": 1, "label": "Fetching video transcripts..."})

    results = await asyncio.gather(
        *[transcript_agent.fetch_transcript(url) for url in req["youtube_urls"]]
    )

    valid = [r for r in results if r.get("transcript")]
    if not valid:
        return {
            "transcripts": list(results),
            "error": "No transcripts found for the provided YouTube videos. "
                     "The videos may have captions disabled.",
            "error_code": "MISSING_TRANSCRIPT",
        }

    return {"transcripts": list(results)}


async def extract_places(state: PipelineState) -> dict:
    if state.get("error"):
        return {}

    req = state["request"]
    queue = state.get("_queue")
    valid_transcripts = [t for t in state["transcripts"] if t.get("transcript")]

    first_title = valid_transcripts[0].get("title", "video") if valid_transcripts else "video"
    await _emit(queue, {
        "type": "progress",
        "step": 2,
        "label": f"Extracting places from '{first_title}'...",
    })

    all_places: list[dict] = []

    # Process each transcript in parallel
    async def _extract_one(t: dict) -> list[dict]:
        places = await extractor_agent.extract_places(
            t["transcript"], req["destination"], t.get("title", "")
        )
        sv = {"url": t["url"], "title": t.get("title", t["url"])}
        for p in places:
            p["source_videos"] = [sv]
        return places

    nested = await asyncio.gather(*[_extract_one(t) for t in valid_transcripts])
    for batch in nested:
        all_places.extend(batch)

    # Drop clearly negative-sentiment places
    positive_places = [p for p in all_places if p.get("sentiment") != "negative"]

    if not positive_places:
        return {
            "raw_places": [],
            "error": "No places could be extracted from the video transcripts. "
                     "Try a travel-focused video with specific place names.",
            "error_code": "ZERO_PLACES",
        }

    return {"raw_places": positive_places}


async def geocode_places(state: PipelineState) -> dict:
    if state.get("error"):
        return {}

    req = state["request"]
    queue = state.get("_queue")
    raw = state.get("raw_places", [])

    await _emit(queue, {
        "type": "progress",
        "step": 3,
        "label": f"Enriching {len(raw)} places with location data...",
    })

    # Geocode places + hotel in parallel
    places_task = asyncio.create_task(
        geocoder_agent.geocode_places(raw, req["destination"])
    )

    hotel_task = None
    hotel_name = req.get("hotel") or ""
    if hotel_name and not hotel_name.startswith("http"):
        hotel_task = asyncio.create_task(
            geocoder_agent.geocode_hotel(hotel_name, req["destination"])
        )

    enriched, unresolved = await places_task
    hotel_result = (await hotel_task) if hotel_task else None

    if not enriched:
        return {
            "enriched": [],
            "unresolved": unresolved,
            "hotel": hotel_result,
            "error": "None of the extracted places could be located. "
                     "Try adding the destination country for better results.",
            "error_code": "ZERO_PLACES",
        }

    return {
        "enriched": enriched,
        "unresolved": unresolved,
        "hotel": hotel_result,
    }


async def cluster_and_label(state: PipelineState) -> dict:
    if state.get("error"):
        return {}

    req = state["request"]
    queue = state.get("_queue")
    enriched = state.get("enriched", [])

    await _emit(queue, {"type": "progress", "step": 4, "label": "Building your day-by-day plan..."})

    num_days = _num_days(req)
    cluster_result = clusterer_agent.cluster_places(enriched, num_days)
    main_clusters = cluster_result["clusters"]
    overflow = cluster_result["overflow"]

    labels = await labeler_agent.label_clusters(
        main_clusters, req["destination"], req.get("start_date")
    )

    return {"clusters": main_clusters, "overflow": overflow, "labels": labels}


# ── Routing ────────────────────────────────────────────────────────────────


def _route(state: PipelineState) -> str:
    return END if state.get("error") else "continue"


# ── Graph ──────────────────────────────────────────────────────────────────


def _build_graph() -> Any:
    builder = StateGraph(PipelineState)
    builder.add_node("fetch_transcripts", fetch_transcripts)
    builder.add_node("extract_places", extract_places)
    builder.add_node("geocode_places", geocode_places)
    builder.add_node("cluster_and_label", cluster_and_label)

    builder.set_entry_point("fetch_transcripts")
    builder.add_conditional_edges(
        "fetch_transcripts",
        _route,
        {"continue": "extract_places", END: END},
    )
    builder.add_conditional_edges(
        "extract_places",
        _route,
        {"continue": "geocode_places", END: END},
    )
    builder.add_conditional_edges(
        "geocode_places",
        _route,
        {"continue": "cluster_and_label", END: END},
    )
    builder.add_edge("cluster_and_label", END)

    return builder.compile()


_graph = _build_graph()


# ── Public API ─────────────────────────────────────────────────────────────


def _build_response(state: PipelineState) -> PlanResponse:
    req = state["request"]
    clusters: list[DayCluster] = []
    date_labels = labeler_agent.make_date_labels(
        len(state.get("clusters", [])), req.get("start_date")
    )

    for i, (cluster_places, theme) in enumerate(
        zip(state.get("clusters", []), state.get("labels", []))
    ):
        places = [
            Place(
                name=p["name"],
                lat=p["lat"],
                lng=p["lng"],
                category=p.get("category"),
                rating=p.get("rating"),
                hours=p.get("hours"),
                description=p.get("description"),
                photo_url=p.get("photo_url"),
                foursquare_id=p.get("foursquare_id"),
                source_videos=[
                    SourceVideo(url=sv["url"], title=sv["title"])
                    for sv in p.get("source_videos", [])
                ],
            )
            for p in cluster_places
        ]
        clusters.append(
            DayCluster(
                day_number=i + 1,
                date_label=date_labels[i] if i < len(date_labels) else f"Day {i + 1}",
                theme_label=theme,
                places=places,
            )
        )

    more_to_explore = [
        Place(
            name=p["name"],
            lat=p["lat"],
            lng=p["lng"],
            category=p.get("category"),
            rating=p.get("rating"),
            hours=p.get("hours"),
            description=p.get("description"),
            photo_url=p.get("photo_url"),
            foursquare_id=p.get("foursquare_id"),
            source_videos=[
                SourceVideo(url=sv["url"], title=sv["title"])
                for sv in p.get("source_videos", [])
            ],
        )
        for p in state.get("overflow", [])
    ]

    hotel_data = state.get("hotel")
    hotel = HotelPin(**hotel_data) if hotel_data else None

    video_titles = [
        t.get("title", t["url"])
        for t in state.get("transcripts", [])
        if t.get("transcript")
    ]

    total = sum(len(c.places) for c in clusters) + len(more_to_explore)

    return PlanResponse(
        destination=req["destination"],
        clusters=clusters,
        more_to_explore=more_to_explore,
        unresolved_places=state.get("unresolved", []),
        hotel=hotel,
        total_places=total,
        video_titles=video_titles,
    )


async def run(
    request: PlanRequest,
    progress_queue: asyncio.Queue | None = None,
) -> PlanResponse:
    """Run pipeline synchronously (no streaming). Raises ValueError on pipeline error."""
    initial: PipelineState = {
        "request": request.model_dump(),
        "_queue": progress_queue,
        "transcripts": [],
        "raw_places": [],
        "enriched": [],
        "unresolved": [],
        "clusters": [],
        "overflow": [],
        "labels": [],
        "hotel": None,
        "error": None,
        "error_code": None,
    }

    final_state = await _graph.ainvoke(initial)

    if final_state.get("error"):
        raise PipelineError(
            code=final_state["error_code"] or "PIPELINE_ERROR",
            message=final_state["error"],
        )

    return _build_response(final_state)


class PipelineError(Exception):
    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
