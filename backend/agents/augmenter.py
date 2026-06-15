"""Travel-expert curator — the brain of the itinerary.

Given a destination and the traveler's intent (trip type, audience, budget, dates,
free-text notes), this produces a *curated, scored* set of real places: attractions
and restaurants tagged with how must-see they are, who they suit, their budget tier,
vibe, area and a one-line expert rationale. It uses OpenAI's Responses API
`web_search` tool so suggestions are real and current rather than hallucinated.

This replaces the old "fill the gaps the video missed" framing. Because server-side
transcripts are unreliable (YouTube IP-blocks them), this curator — not the video
extractor — is the primary source of places. Video/maps-link places are folded in as
*additional* candidates the curator's output is merged with downstream.

The output shape stays `{"attractions": [...], "restaurants": [...]}` so the pipeline
wiring is unchanged; each item just carries far richer signals now.
"""
from __future__ import annotations
import json
import os
import re
import asyncio
from openai import OpenAI

from ..models import TRIP_TYPE_AUDIENCE

_client: OpenAI | None = None
_MODEL = "gpt-4o-mini"

_SYSTEM = """\
You are a seasoned local travel expert building a trip for a specific traveler — not a \
generic list-maker. Think like someone who actually lives there and knows what's worth a \
visitor's limited time. Use web search so every place is real and currently operating.

Return ONLY a valid JSON object — no prose, no markdown fences:
{
  "attractions": [
    {
      "name": "Exact, searchable place name",
      "category": "sight"|"museum"|"temple"|"park"|"viewpoint"|"beach"|"market"|"neighbourhood"|"experience"|"nature",
      "importance": "must_see"|"recommended"|"hidden_gem"|"optional",
      "audience": ["couples"|"families"|"solo"|"groups"],
      "budget_tier": "budget"|"mid"|"luxury",
      "vibe": ["romantic"|"adventurous"|"cultural"|"relaxing"|"lively"|"scenic"],
      "area": "neighbourhood or sub-area name",
      "ideal_time": "morning"|"afternoon"|"evening"|"sunset"|"night"|"any",
      "duration_hrs": 1.5,
      "why": "one short expert sentence on why it's worth it"
    }
  ],
  "restaurants": [
    {
      "name": "Exact Restaurant Name",
      "meal_type": "breakfast"|"lunch"|"dinner",
      "cuisine": "short",
      "budget_tier": "budget"|"mid"|"luxury",
      "area": "neighbourhood or sub-area name",
      "vibe": ["romantic"|"casual"|"lively"|"fine-dining"],
      "why": "one short expert sentence"
    }
  ]
}

How an expert curates (follow this — it's what separates a real itinerary from a scraper):
- COMMON SENSE FIRST. Only suggest places a traveler actually goes to enjoy: sights,
  nature, food, culture, experiences. NEVER include airports, ports/harbours, bus or
  train stations, government/administrative offices, hospitals, banks, business parks,
  residential areas, or an entire city/town as if it were a single stop.
- BALANCE THE MIX. Lead with the genuine must-sees so a first-timer isn't disappointed,
  then layer in 1-2 hidden gems a local would recommend. Don't pad with filler.
- FIT THE TRAVELER. Honour the trip style, audience and budget given below: e.g. couples
  → atmospheric, scenic, intimate dining; families → kid-friendly, low-intensity, easy
  walking; luxury → refined spots, skip the backpacker joints; budget → great-value local
  picks, skip the splurges. Set `audience`/`budget_tier` honestly per place.
- USE EXACT, GEOCODABLE NAMES. Include the area in the name only to disambiguate.
- Do NOT repeat anything in the traveler's "already have" list.
- Suggest roughly enough attractions to support the trip length (a few per day), and about
  3 restaurants per day spread across breakfast/lunch/dinner, favouring authentic local
  spots over chains.
- Group by `area` so nearby places can form a coherent day. If the destination is a whole
  region/country, treat each `area` as a base town/city.
- Never invent a place. If unsure it exists, omit it.
"""

# Per-trip-type curation bias (dev plan §2). Appended to the user prompt so the *kind*
# of places we surface matches the traveler's intent. "balanced" = no bias.
_TRIP_TYPE_BIAS: dict[str, str] = {
    "balanced": "",
    "romantic": "Trip style: romantic / couples. Favour sunset viewpoints, scenic and "
                "atmospheric spots, and intimate or rooftop dining. Avoid crowded, "
                "kid-oriented or backpacker-party places.",
    "family": "Trip style: family with kids. Favour parks, interactive/hands-on sights, "
              "easy low-walking attractions and casual, welcoming restaurants. Avoid "
              "strenuous treks, late-night venues and anything unsafe for children.",
    "adventure": "Trip style: adventure & outdoors. Favour treks, hikes, water/air "
                 "activities and hearty post-activity eats. Hidden, effort-rewarding "
                 "spots are welcome.",
    "nature": "Trip style: nature & slow travel. Favour scenic/natural spots, gardens, "
              "lakes, viewpoints and unhurried experiences over dense urban sights.",
    "culture": "Trip style: culture & heritage. Favour museums, monuments, historic "
               "quarters, craft/artisan spots and traditional local restaurants.",
}


def _parse_json(text: str) -> dict:
    """Extract the JSON object from a model response that may be fenced or prefixed."""
    if not text:
        return {}
    fence = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    candidate = fence.group(1) if fence else None
    if candidate is None:
        brace = re.search(r"\{.*\}", text, re.DOTALL)
        candidate = brace.group(0) if brace else text
    try:
        return json.loads(candidate)
    except json.JSONDecodeError:
        return {}


_VALID_IMPORTANCE = {"must_see", "recommended", "hidden_gem", "optional"}
_VALID_BUDGET = {"budget", "mid", "luxury"}
_VALID_MEALS = {"breakfast", "lunch", "dinner"}


def _str_list(v) -> list[str]:
    """Coerce a model field to a clean list[str] (it may send a string or list)."""
    if isinstance(v, str):
        return [v.strip()] if v.strip() else []
    if isinstance(v, list):
        return [str(x).strip() for x in v if str(x).strip()]
    return []


def _duration(v) -> float | None:
    try:
        d = float(v)
        return d if 0 < d <= 12 else None
    except (TypeError, ValueError):
        return None


async def augment_places(
    destination: str,
    existing_names: list[str],
    num_days: int | None,
    hotel: str | None = None,
    start_date: str | None = None,
    trip_type: str = "balanced",
    notes: str | None = None,
    budget: str = "any",
    audience: str | None = None,
) -> dict:
    """
    Returns {"attractions": [...], "restaurants": [...]}, each item carrying
    source="suggested" plus expert signals (importance, audience, budget_tier, vibe,
    area, ideal_time→time_of_day, duration_hrs, why). Never raises — returns empty
    lists on any failure so the pipeline degrades gracefully.

    `trip_type`/`audience`/`budget` shape *what* we surface; `notes` is the traveler's
    verbatim free text, injected as untrusted (already length-capped upstream).
    """
    global _client
    if _client is None:
        _client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    days = num_days or 3
    have = ", ".join(existing_names[:60]) or "(none provided)"
    aud = audience or TRIP_TYPE_AUDIENCE.get(trip_type or "balanced", "general")

    lines = [
        f"Destination: {destination}",
        f"Trip length: {days} day(s)",
        f"Travelling as: {aud}",
    ]
    if budget and budget != "any":
        lines.append(f"Budget: {budget}")
    if hotel:
        lines.append(f"Staying near: {hotel}")
    if start_date:
        lines.append(f"Travel dates start: {start_date}")
    bias = _TRIP_TYPE_BIAS.get(trip_type or "balanced", "")
    if bias:
        lines.append(bias)
    if notes:
        lines.append(f'Traveler notes (respect these): "{notes}"')
    lines.append(f"Places the traveler already has: {have}")
    lines.append("")
    lines.append("Curate attractions and a spread of restaurants for this exact trip.")
    prompt = "\n".join(lines)

    try:
        response = await asyncio.to_thread(
            _client.responses.create,
            model=_MODEL,
            tools=[{"type": "web_search_preview"}],
            input=[
                {"role": "system", "content": _SYSTEM},
                {"role": "user", "content": prompt},
            ],
        )
        data = _parse_json(response.output_text)
    except Exception:
        return {"attractions": [], "restaurants": []}

    attractions = []
    for a in data.get("attractions", []) or []:
        name = (a.get("name") or "").strip()
        if not name:
            continue
        imp = (a.get("importance") or "").strip().lower()
        bt = (a.get("budget_tier") or "").strip().lower()
        ideal = (a.get("ideal_time") or "").strip().lower()
        tod = {"morning": "Morning", "afternoon": "Afternoon", "evening": "Evening",
               "sunset": "Evening", "night": "Evening"}.get(ideal)
        attractions.append({
            "name": name,
            "category": a.get("category") or "sight",
            "importance": imp if imp in _VALID_IMPORTANCE else "recommended",
            "audience": _str_list(a.get("audience")),
            "budget_tier": bt if bt in _VALID_BUDGET else None,
            "vibe": _str_list(a.get("vibe")),
            "area": (a.get("area") or "").strip() or None,
            "time_of_day": tod,
            "duration_hrs": _duration(a.get("duration_hrs")),
            "description": a.get("why"),
            "why": a.get("why"),
            "source": "suggested",
            "source_videos": [],
        })

    restaurants = []
    for r in data.get("restaurants", []) or []:
        name = (r.get("name") or "").strip()
        if not name:
            continue
        meal = (r.get("meal_type") or "").strip().lower()
        bt = (r.get("budget_tier") or "").strip().lower()
        restaurants.append({
            "name": name,
            "category": "food",
            "meal_type": meal if meal in _VALID_MEALS else None,
            "budget_tier": bt if bt in _VALID_BUDGET else None,
            "vibe": _str_list(r.get("vibe")),
            "area": (r.get("area") or "").strip() or None,
            "description": r.get("why") or r.get("cuisine"),
            "why": r.get("why"),
            "source": "suggested",
            "source_videos": [],
        })

    return {"attractions": attractions, "restaurants": restaurants}
