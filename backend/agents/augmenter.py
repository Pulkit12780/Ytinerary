"""Augment video-extracted places with web-searched attractions + restaurants.

Uses OpenAI's Responses API `web_search` tool so suggestions reflect real, current
places (and meal spots) rather than the model's stale training data. The video
transcripts are often thin or skip food entirely — this fills those gaps so the judge
has enough material to build a realistic day-by-day plan with breakfast/lunch/dinner.
"""
from __future__ import annotations
import json
import os
import re
import asyncio
from openai import OpenAI

_client: OpenAI | None = None
_MODEL = "gpt-4o-mini"

_SYSTEM = """\
You are a local travel researcher. Using web search, suggest real, currently-operating \
places for a trip. Return ONLY a valid JSON object — no prose, no markdown fences:
{
  "attractions": [
    {"name": "Exact Place Name", "category": "attraction"|"market"|"viewpoint"|"museum"|"temple"|"beach"|"neighbourhood"|"park", "why": "one short phrase"}
  ],
  "restaurants": [
    {"name": "Exact Restaurant Name", "meal_type": "breakfast"|"lunch"|"dinner", "cuisine": "short", "why": "one short phrase"}
  ]
}

Rules:
- Use the EXACT, searchable name of each place (so it can be geocoded). Include the
  neighbourhood/area in the name only if needed to disambiguate.
- attractions: suggest well-regarded sights that fill gaps the traveler hasn't already
  listed. Do NOT repeat places that are already in the provided "already have" list.
  Suggest roughly enough to support the trip length, fewer if the list is already rich.
- restaurants: suggest real, well-reviewed eateries spread across breakfast, lunch and
  dinner — aim for about 3 per day of the trip. Favor local/authentic spots over chains.
- Prefer places reasonably close to the traveler's hotel/area when one is given.
- Never invent names. If unsure a place exists, omit it.
"""

# Per-trip-type suggestion bias (dev plan §2). Appended to the user prompt so the
# *kind* of places we surface matches the traveler's intent. "balanced" = no bias.
_TRIP_TYPE_BIAS: dict[str, str] = {
    "balanced": "",
    "romantic": "Trip style: romantic / couples. Bias toward sunset viewpoints, "
                "scenic spots, and intimate or rooftop dining. Favor atmospheric, "
                "couples-friendly places.",
    "family": "Trip style: family with kids. Bias toward parks, easy low-walking "
              "attractions, and kid-friendly activities and casual, welcoming "
              "restaurants. Avoid strenuous or late-night spots.",
    "adventure": "Trip style: adventure & outdoors. Bias toward treks, hikes, "
                 "outdoor activities, and hearty post-activity eats.",
    "nature": "Trip style: nature & slow travel. Bias toward scenic/natural spots, "
              "gardens, lakes and viewpoints over dense urban sights.",
    "culture": "Trip style: culture & heritage. Bias toward museums, monuments, "
               "historic old-town quarters, and traditional/local restaurants.",
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


async def augment_places(
    destination: str,
    existing_names: list[str],
    num_days: int | None,
    hotel: str | None = None,
    start_date: str | None = None,
    trip_type: str = "balanced",
    notes: str | None = None,
) -> dict:
    """
    Returns {"attractions": [...], "restaurants": [...]} with each item carrying
    source="suggested". Never raises — returns empty lists on any failure so the
    pipeline degrades gracefully to video-only places.

    `trip_type` biases *what* we suggest (§2); `notes` is the traveler's free text,
    injected verbatim and treated as untrusted (it's already length-capped upstream).
    """
    global _client
    if _client is None:
        _client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    days = num_days or 3
    have = ", ".join(existing_names[:60]) or "(none provided)"
    hotel_line = f"Staying near: {hotel}\n" if hotel else ""
    when_line = f"Travel dates start: {start_date}\n" if start_date else ""
    bias = _TRIP_TYPE_BIAS.get(trip_type or "balanced", "")
    bias_line = f"{bias}\n" if bias else ""
    notes_line = f'Traveler notes (respect these): "{notes}"\n' if notes else ""

    prompt = (
        f"Destination: {destination}\n"
        f"Trip length: {days} day(s)\n"
        f"{hotel_line}{when_line}{bias_line}{notes_line}"
        f"Places the traveler already has: {have}\n\n"
        f"Suggest additional attractions and a spread of restaurants "
        f"(breakfast/lunch/dinner) for this trip."
    )

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
        attractions.append({
            "name": name,
            "category": a.get("category") or "attraction",
            "description": a.get("why"),
            "source": "suggested",
            "source_videos": [],
        })

    restaurants = []
    valid_meals = {"breakfast", "lunch", "dinner"}
    for r in data.get("restaurants", []) or []:
        name = (r.get("name") or "").strip()
        if not name:
            continue
        meal = (r.get("meal_type") or "").strip().lower()
        restaurants.append({
            "name": name,
            "category": "food",
            "meal_type": meal if meal in valid_meals else None,
            "description": r.get("why") or r.get("cuisine"),
            "source": "suggested",
            "source_videos": [],
        })

    return {"attractions": attractions, "restaurants": restaurants}
