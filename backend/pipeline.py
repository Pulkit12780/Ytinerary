"""LangGraph pipeline: transcript_fetch → place_extraction → augmentation → geocoding → judge/plan."""
from __future__ import annotations
import asyncio
import os
import time
from datetime import date
from typing import Any, Optional
from typing_extensions import TypedDict

from langgraph.graph import StateGraph, END

from . import metrics
from .models import (
    PlanRequest,
    PlanResponse,
    DayCluster,
    Place,
    HotelPin,
    SourceVideo,
)
from .agents import sourcer as sourcer_agent
from .agents import transcript as transcript_agent
from .agents import extractor as extractor_agent
from .agents import augmenter as augmenter_agent
from .agents import geocoder as geocoder_agent
from .agents import judge as judge_agent
from .agents import labeler as labeler_agent


# Active video source for auto-sourcing, resolved lazily so it can read
# YOUTUBE_API_KEY after dotenv loads: real YouTube search when a key is present,
# else the curated stub (dev / no quota). Tests may override this global directly.
_video_source: sourcer_agent.VideoSource | None = None


# How many transcript-yielding videos to keep from an auto-sourced over-fetch (B5).
_MAX_SOURCED_TRANSCRIPTS = 5


def _get_video_source() -> sourcer_agent.VideoSource:
    global _video_source
    if _video_source is None:
        _video_source = (
            sourcer_agent.YouTubeSearchSource()
            if os.getenv("YOUTUBE_API_KEY")
            else sourcer_agent.StubVideoSource()
        )
    return _video_source


# ── State ──────────────────────────────────────────────────────────────────


class PipelineState(TypedDict):
    request: dict                   # PlanRequest.model_dump()
    _queue: Any                     # asyncio.Queue | None — for SSE progress events
    transcripts: list               # [{url, video_id, title, transcript, error}]
    raw_places: list                # [{name, sentiment, category, source, source_videos}]
    enriched: list                  # [{name, lat, lng, ..., source_videos}]
    unresolved: list                # [place_name, ...]
    plan: Optional[dict]            # {days: [...], more_to_explore: [...], warnings: [...]}
    hotel: Optional[dict]           # {name, lat, lng} | None
    sourced: bool                   # True if youtube_urls were auto-sourced (not manual)
    error: Optional[str]
    error_code: Optional[str]


# ── Helpers ────────────────────────────────────────────────────────────────


async def _emit(queue: Any, event: dict) -> None:
    if queue is not None:
        await queue.put(event)


def _places_from_maps_links(links: list | None) -> list[dict]:
    """Parse place names out of Google Maps URLs the user explicitly added."""
    import re
    from urllib.parse import unquote_plus, urlparse, parse_qs

    out: list[dict] = []
    for link in links or []:
        name = None
        m = re.search(r"/maps/place/([^/@?]+)", link)
        if m:
            name = unquote_plus(m.group(1))
        else:
            qs = parse_qs(urlparse(link).query)
            q = (qs.get("q") or qs.get("query") or [None])[0]
            # Skip raw "lat,lng" queries — there's no name to geocode
            if q and not re.match(r"^-?\d+(\.\d+)?\s*,", q):
                name = q
        if name and name.strip():
            out.append({
                "name": name.strip(),
                "sentiment": "positive",
                "context": "added by you",
                "source": "video",
                "source_videos": [],
            })
    return out


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


def _hotel_hint(req: dict) -> str | None:
    name = req.get("hotel") or ""
    return name if name and not name.startswith("http") else None


def _to_place(p: dict) -> Place:
    return Place(
        name=p["name"],
        lat=p["lat"],
        lng=p["lng"],
        category=p.get("category"),
        rating=p.get("rating"),
        hours=p.get("hours"),
        description=p.get("description"),
        photo_url=p.get("photo_url"),
        place_id=p.get("place_id"),
        meal_type=p.get("meal_type"),
        source=p.get("source", "video"),
        time_of_day=p.get("time_of_day"),
        source_videos=[
            SourceVideo(url=sv["url"], title=sv["title"])
            for sv in p.get("source_videos", [])
        ],
    )


# ── Nodes ──────────────────────────────────────────────────────────────────


async def source_videos(state: PipelineState) -> dict:
    """Entry node (ADR-001): turn trip intent into `youtube_urls` to feed the pipeline.

    - Manual precedence (AC #5): if the user pasted URLs, pass through untouched.
    - Otherwise auto-source via the `VideoSource` seam and over-fetch (~8) so
      `fetch_transcripts` can be the real filter (ADR-002).
    - If nothing comes back, set NO_VIDEOS_FOUND so the UX nudges the paste fallback.
    """
    req = state["request"]
    queue = state.get("_queue")

    if req.get("youtube_urls"):
        return {}  # manual URLs win — skip auto-sourcing

    await _emit(queue, {
        "type": "progress",
        "step": 0,
        "label": "Finding the best travel videos for your trip...",
    })

    candidates = await _get_video_source().search(
        req["destination"], req.get("trip_type", "balanced"), limit=8
    )

    if not candidates:
        return {
            "error": "We couldn't find good videos for this trip — "
                     "paste a YouTube link or two and we'll build from those.",
            "error_code": "NO_VIDEOS_FOUND",
        }

    sourced_urls = [c["url"] for c in candidates]
    return {"request": {**req, "youtube_urls": sourced_urls}, "sourced": True}


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

    # Over-fetch filter (ADR-002, B5): when we auto-sourced ~8 candidates, keep only
    # the first few (ranked order) that actually yielded a transcript and drop the
    # rest. Manual URLs keep the current "use all" behavior.
    if state.get("sourced"):
        return {"transcripts": valid[:_MAX_SOURCED_TRANSCRIPTS]}

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
            p["source"] = "video"
        return places

    nested = await asyncio.gather(*[_extract_one(t) for t in valid_transcripts])
    for batch in nested:
        all_places.extend(batch)

    # Drop clearly negative-sentiment places
    positive_places = [p for p in all_places if p.get("sentiment") != "negative"]

    # Must-include places the user pasted as Google Maps links
    positive_places.extend(_places_from_maps_links(req.get("maps_links")))

    if not positive_places:
        return {
            "raw_places": [],
            "error": "No places could be extracted from the video transcripts. "
                     "Try a travel-focused video with specific place names.",
            "error_code": "ZERO_PLACES",
        }

    return {"raw_places": positive_places}


async def augment_places(state: PipelineState) -> dict:
    if state.get("error"):
        return {}

    req = state["request"]
    queue = state.get("_queue")
    raw = state.get("raw_places", [])

    await _emit(queue, {
        "type": "progress",
        "step": 3,
        "label": "Researching more places to visit & where to eat...",
    })

    existing = [p["name"] for p in raw]
    aug = await augmenter_agent.augment_places(
        req["destination"],
        existing,
        _num_days(req),
        _hotel_hint(req),
        req.get("start_date"),
        req.get("trip_type", "balanced"),
        req.get("notes"),
    )

    combined = list(raw) + aug.get("attractions", []) + aug.get("restaurants", [])
    return {"raw_places": combined}


async def geocode_places(state: PipelineState) -> dict:
    if state.get("error"):
        return {}

    req = state["request"]
    queue = state.get("_queue")
    raw = state.get("raw_places", [])

    await _emit(queue, {
        "type": "progress",
        "step": 4,
        "label": f"Locating {len(raw)} places on the map...",
    })

    # Geocode places + hotel in parallel
    places_task = asyncio.create_task(
        geocoder_agent.geocode_places(raw, req["destination"])
    )

    hotel_task = None
    hotel_name = _hotel_hint(req)
    if hotel_name:
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
            "error_code": "GEOCODING_FAILURE",
        }

    return {
        "enriched": enriched,
        "unresolved": unresolved,
        "hotel": hotel_result,
    }


async def judge_and_plan(state: PipelineState) -> dict:
    if state.get("error"):
        return {}

    req = state["request"]
    queue = state.get("_queue")
    enriched = state.get("enriched", [])
    hotel = state.get("hotel")

    await _emit(queue, {
        "type": "progress",
        "step": 5,
        "label": "Sanity-checking distances & building your day-by-day plan...",
    })

    plan = await judge_agent.plan_itinerary(
        enriched, hotel, _num_days(req), req["destination"],
        req.get("trip_type", "balanced"), req.get("notes"),
    )
    return {"plan": plan}


# ── Routing ────────────────────────────────────────────────────────────────


def _route(state: PipelineState) -> str:
    return END if state.get("error") else "continue"


# ── Graph ──────────────────────────────────────────────────────────────────


def _build_graph() -> Any:
    builder = StateGraph(PipelineState)
    builder.add_node("source_videos", source_videos)
    builder.add_node("fetch_transcripts", fetch_transcripts)
    builder.add_node("extract_places", extract_places)
    builder.add_node("augment_places", augment_places)
    builder.add_node("geocode_places", geocode_places)
    builder.add_node("judge_and_plan", judge_and_plan)

    builder.set_entry_point("source_videos")
    builder.add_conditional_edges(
        "source_videos",
        _route,
        {"continue": "fetch_transcripts", END: END},
    )
    builder.add_conditional_edges(
        "fetch_transcripts",
        _route,
        {"continue": "extract_places", END: END},
    )
    builder.add_conditional_edges(
        "extract_places",
        _route,
        {"continue": "augment_places", END: END},
    )
    builder.add_conditional_edges(
        "augment_places",
        _route,
        {"continue": "geocode_places", END: END},
    )
    builder.add_conditional_edges(
        "geocode_places",
        _route,
        {"continue": "judge_and_plan", END: END},
    )
    builder.add_edge("judge_and_plan", END)

    return builder.compile()


_graph = _build_graph()


# ── Public API ─────────────────────────────────────────────────────────────


def _build_response(state: PipelineState) -> PlanResponse:
    req = state["request"]
    plan = state.get("plan") or {"days": [], "more_to_explore": [], "warnings": []}
    days = plan.get("days", [])

    date_labels = labeler_agent.make_date_labels(len(days), req.get("start_date"))

    clusters: list[DayCluster] = []
    for i, day in enumerate(days):
        places = [_to_place(p) for p in day.get("stops", [])]
        clusters.append(
            DayCluster(
                day_number=i + 1,
                date_label=date_labels[i] if i < len(date_labels) else f"Day {i + 1}",
                theme_label=day.get("theme") or f"Day {i + 1}",
                places=places,
                notes=day.get("notes"),
            )
        )

    more_to_explore = [_to_place(p) for p in plan.get("more_to_explore", [])]

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
        warnings=plan.get("warnings", []),
    )


async def run(
    request: PlanRequest,
    progress_queue: asyncio.Queue | None = None,
) -> PlanResponse:
    """Run pipeline synchronously (no streaming). Raises PipelineError on pipeline error."""
    initial: PipelineState = {
        "request": request.model_dump(),
        "_queue": progress_queue,
        "transcripts": [],
        "raw_places": [],
        "enriched": [],
        "unresolved": [],
        "plan": None,
        "hotel": None,
        "sourced": False,
        "error": None,
        "error_code": None,
    }

    zero_url = not bool(request.youtube_urls)
    start = time.perf_counter()
    final_state = await _graph.ainvoke(initial)
    duration = time.perf_counter() - start

    if final_state.get("error"):
        metrics.record_plan_run(
            zero_url=zero_url,
            sourced=bool(final_state.get("sourced")),
            outcome="error",
            error_code=final_state.get("error_code") or "PIPELINE_ERROR",
            duration_s=duration,
        )
        raise PipelineError(
            code=final_state["error_code"] or "PIPELINE_ERROR",
            message=final_state["error"],
        )

    metrics.record_plan_run(
        zero_url=zero_url,
        sourced=bool(final_state.get("sourced")),
        outcome="success",
        error_code=None,
        duration_s=duration,
    )
    return _build_response(final_state)


class PipelineError(Exception):
    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
