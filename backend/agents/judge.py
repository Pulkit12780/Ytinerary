"""Realism judge: turn a flat list of geocoded places into a doable day-by-day plan.

This replaces the old naive k-means clusterer. The problem with pure k-means on lat/lng
is that nothing stops a single "day" from spanning tens of km, and it never reasons about
meals or ordering. Here we:

  1. Ground the model in real geography with haversine distances + a proximity pre-grouping,
     so it cannot hallucinate that far-apart places are "close".
  2. Let an LLM assemble realistic days: tight geographically, ordered sensibly, with
     breakfast/lunch/dinner interleaved, deferring outliers to "More to Explore".
  3. Apply a deterministic guardrail afterwards so we never blindly trust the model — any
     stop too far from its day's core is moved out with a warning.
"""
from __future__ import annotations
import json
import os
import math
import asyncio
from openai import OpenAI

_client: OpenAI | None = None
_MODEL = "gpt-4o-mini"

# A day's stops must sit within this radius of the day's geographic core. Tuned for
# city trips reachable on foot / short rides; truly far stops (day-trips 30-40km out)
# get deferred to "More to Explore".
MAX_DAY_RADIUS_KM = 12.0
_MAX_STOPS_PER_DAY = 7  # default cap (attractions + meals combined)

# Per-trip-type stop cap (dev plan C3). Lower for family/nature makes "fewer
# stops/day" a *structural* knob (AC #2), not just a prompt nudge. Also feeds the
# no-dates day-target heuristic so the same place count spreads over more days.
_TRIP_TYPE_MAX_STOPS: dict[str, int] = {
    "balanced": 7,
    "romantic": 6,
    "family": 5,
    "adventure": 7,
    "nature": 5,
    "culture": 6,
}

# Per-trip-type day *shape* guidance (dev plan §2). Injected into the planner prompt.
_TRIP_TYPE_SHAPE: dict[str, str] = {
    "balanced": "",
    "romantic": "Shape each day for a couple: keep an unhurried pace and end the day "
                "on a sunset viewpoint followed by an intimate dinner.",
    "family": "Shape each day for a family with kids: fewer stops, a relaxed "
              "low-intensity pace, and short hops between nearby stops. Don't overpack.",
    "adventure": "Shape each day to be activity-forward: lead with the main "
                 "trek/activity and keep momentum; the day can be dense.",
    "nature": "Shape each day around a relaxed, slow-travel pace with fewer stops "
              "and more time spent in nature.",
    "culture": "Shape each day around one coherent cultural cluster — group the "
               "museums, monuments and heritage of a single area together.",
}


def _max_stops_for(trip_type: str | None) -> int:
    return _TRIP_TYPE_MAX_STOPS.get(trip_type or "balanced", _MAX_STOPS_PER_DAY)


# ── Geometry ─────────────────────────────────────────────────────────────────


def _haversine(a: tuple[float, float], b: tuple[float, float]) -> float:
    """Great-circle distance in km between (lat, lng) pairs."""
    lat1, lng1, lat2, lng2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    dlat, dlng = lat2 - lat1, lng2 - lng1
    h = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlng / 2) ** 2
    return 2 * 6371.0 * math.asin(math.sqrt(h))


def _coord(p: dict) -> tuple[float, float]:
    return (float(p["lat"]), float(p["lng"]))


def _centroid(points: list[tuple[float, float]]) -> tuple[float, float]:
    n = len(points)
    return (sum(p[0] for p in points) / n, sum(p[1] for p in points) / n)


def _medoid(places: list[dict]) -> dict:
    """The place minimizing total distance to the others — the geographic core."""
    if len(places) == 1:
        return places[0]
    best, best_sum = places[0], float("inf")
    for cand in places:
        s = sum(_haversine(_coord(cand), _coord(o)) for o in places if o is not cand)
        if s < best_sum:
            best, best_sum = cand, s
    return best


def _pregroup(places: list[dict], radius_km: float) -> list[int]:
    """Greedy proximity grouping → a zone index per place (a hint for the LLM)."""
    zones: list[dict] = []  # {center, members}
    assignment: list[int] = []
    for p in places:
        c = _coord(p)
        best_z, best_d = -1, float("inf")
        for zi, z in enumerate(zones):
            d = _haversine(c, z["center"])
            if d < best_d:
                best_z, best_d = zi, d
        if best_z >= 0 and best_d <= radius_km:
            z = zones[best_z]
            z["members"].append(c)
            z["center"] = _centroid(z["members"])
            assignment.append(best_z)
        else:
            zones.append({"center": c, "members": [c]})
            assignment.append(len(zones) - 1)
    return assignment


# ── LLM planning ───────────────────────────────────────────────────────────────


_SYSTEM = """\
You are a meticulous local trip planner. You are given a set of geocoded places (attractions \
and restaurants) for a destination, with real distances. Build a realistic day-by-day plan.

Return ONLY valid JSON — no prose, no markdown:
{
  "days": [
    {
      "theme": "short evocative label (3-6 words)",
      "notes": "one-sentence rationale for the day",
      "stops": [
        {"name": "Exact Place Name", "time_of_day": "Morning"|"Afternoon"|"Evening", "meal_type": "breakfast"|"lunch"|"dinner"|null}
      ]
    }
  ],
  "more_to_explore": ["Exact Place Name", ...],
  "warnings": ["short note about anything deferred or impractical"]
}

Hard rules:
- Each day must be geographically TIGHT: only group places that are realistically doable
  together in one day given the distances provided. Never put far-apart places (a long
  cross-town/out-of-town trip) in the same day. Defer such outliers to "more_to_explore".
- Respect the requested number of days. Spread the best attractions across them.
- Every day should include meals: a breakfast, a lunch and a dinner, chosen from the
  food places that are near that day's attractions. Tag them with the right meal_type.
- Order each day's stops as a sensible timeline: breakfast → nearby morning sights →
  lunch → afternoon sights → dinner. Set time_of_day accordingly.
- Use the EXACT place names provided. Do not invent places.
- Anything that doesn't fit a coherent day goes to "more_to_explore" (don't drop it).
- Respect the per-day stop cap and any trip-style shaping given in the request below.
"""


def _places_block(places: list[dict], zones: list[int], hotel: dict | None) -> str:
    lines = []
    hotel_coord = _coord(hotel) if hotel else None
    for i, p in enumerate(places):
        c = _coord(p)
        dist_h = f", {_haversine(c, hotel_coord):.1f}km from hotel" if hotel_coord else ""
        meal = p.get("meal_type")
        meal_s = f", meal={meal}" if meal else ""
        kind = "food" if (p.get("category") == "food" or meal) else (p.get("category") or "attraction")
        lines.append(
            f"- {p['name']} [zone {zones[i]}, {kind}, src={p.get('source', 'video')}{meal_s}{dist_h}]"
        )
    return "\n".join(lines)


def _zone_matrix(places: list[dict], zones: list[int]) -> str:
    """Compact zone centroid distance matrix so the LLM sees how far zones are apart."""
    nz = max(zones) + 1 if zones else 0
    centers = []
    for zi in range(nz):
        pts = [_coord(p) for i, p in enumerate(places) if zones[i] == zi]
        centers.append(_centroid(pts))
    rows = []
    for i in range(nz):
        cells = [f"{_haversine(centers[i], centers[j]):.0f}" for j in range(nz)]
        rows.append(f"zone {i}: " + " ".join(cells))
    return "\n".join(rows)


async def _llm_plan(
    places: list[dict],
    zones: list[int],
    hotel: dict | None,
    num_days: int,
    destination: str,
    trip_type: str = "balanced",
    notes: str | None = None,
) -> dict | None:
    global _client
    if _client is None:
        _client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    max_stops = _max_stops_for(trip_type)
    shape = _TRIP_TYPE_SHAPE.get(trip_type or "balanced", "")
    shape_line = f"{shape}\n" if shape else ""
    notes_line = f'Traveler notes (respect these): "{notes}"\n' if notes else ""

    prompt = (
        f"Destination: {destination}\n"
        f"Number of days: {num_days}\n"
        f"Hotel: {hotel['name'] if hotel else '(none)'}\n"
        f"Cap each day at about {max_stops} stops total including meals.\n"
        f"{shape_line}{notes_line}\n"
        f"Places:\n{_places_block(places, zones, hotel)}\n\n"
        f"Zone-to-zone distances (km):\n{_zone_matrix(places, zones)}\n\n"
        f"Build the {num_days}-day plan."
    )
    try:
        response = await asyncio.to_thread(
            _client.chat.completions.create,
            model=_MODEL,
            max_tokens=2048,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": _SYSTEM},
                {"role": "user", "content": prompt},
            ],
        )
        return json.loads(response.choices[0].message.content)
    except Exception:
        return None


# ── Assembly + guardrail ─────────────────────────────────────────────────────


def _assemble(plan: dict, places: list[dict], num_days: int) -> tuple[list[dict], list[dict]]:
    """Map LLM name references back to full place dicts. Unplaced places fall through to
    more_to_explore so nothing is silently dropped."""
    by_name = {p["name"].strip().lower(): p for p in places}
    used: set[str] = set()
    days: list[dict] = []

    for d in plan.get("days", [])[:num_days]:
        stops: list[dict] = []
        for s in d.get("stops", []) or []:
            key = (s.get("name") or "").strip().lower()
            p = by_name.get(key)
            if not p or key in used:
                continue
            used.add(key)
            merged = dict(p)
            if s.get("meal_type") in ("breakfast", "lunch", "dinner"):
                merged["meal_type"] = s["meal_type"]
            if s.get("time_of_day"):
                merged["time_of_day"] = s["time_of_day"]
            stops.append(merged)
        if stops:
            days.append({
                "theme": d.get("theme") or "Exploring",
                "notes": d.get("notes"),
                "stops": stops,
            })

    more: list[dict] = []
    for name in plan.get("more_to_explore", []) or []:
        key = (name or "").strip().lower()
        p = by_name.get(key)
        if p and key not in used:
            used.add(key)
            more.append(dict(p))
    # Anything the model forgot entirely
    for key, p in by_name.items():
        if key not in used:
            more.append(dict(p))

    return days, more


def _apply_guardrail(
    days: list[dict], more: list[dict], warnings: list[str]
) -> None:
    """Deterministic backstop: move any stop too far from its day's core to more_to_explore."""
    for day in days:
        stops = day["stops"]
        if len(stops) <= 2:
            continue
        core = _medoid(stops)
        keep, evicted = [], []
        for s in stops:
            if s is core or _haversine(_coord(s), _coord(core)) <= MAX_DAY_RADIUS_KM:
                keep.append(s)
            else:
                evicted.append(s)
        if evicted:
            day["stops"] = keep
            for s in evicted:
                more.append(s)
                warnings.append(
                    f"{s['name']} is too far from the rest of {day['theme']} — moved to More to Explore."
                )


def _fallback(places: list[dict], num_days: int, max_stops: int) -> dict:
    """Deterministic plan if the LLM is unavailable: proximity zones → days, meals kept."""
    zones = _pregroup(places, MAX_DAY_RADIUS_KM)
    nz = max(zones) + 1 if zones else 0
    buckets: list[list[dict]] = [[] for _ in range(nz)]
    for i, p in enumerate(places):
        buckets[zones[i]].append(p)
    buckets.sort(key=len, reverse=True)
    buckets = [b for b in buckets if b]

    days: list[dict] = []
    overflow: list[dict] = []
    for b in buckets[:num_days]:
        days.append({"theme": "Exploring the area", "notes": None, "stops": b[:max_stops]})
        overflow.extend(b[max_stops:])
    for b in buckets[num_days:]:
        overflow.extend(b)
    return {"days": days, "more_to_explore": overflow, "warnings": []}


async def plan_itinerary(
    places: list[dict],
    hotel: dict | None,
    num_days: int | None,
    destination: str,
    trip_type: str = "balanced",
    notes: str | None = None,
) -> dict:
    """
    Returns {"days": [{theme, notes, stops:[place...]}], "more_to_explore": [place...],
    "warnings": [str]}. Never raises.

    `trip_type` controls pace/shape and the per-day stop cap (§2, C3); `notes` is the
    traveler's verbatim free text. Both default so existing callers are unaffected.
    """
    if not places:
        return {"days": [], "more_to_explore": [], "warnings": []}

    max_stops = _max_stops_for(trip_type)
    # No-dates heuristic: fewer stops/day → spread the same places over more days.
    days_target = num_days or max(1, min(5, (len(places) + max_stops - 1) // max_stops))
    zones = _pregroup(places, MAX_DAY_RADIUS_KM)

    plan = await _llm_plan(places, zones, hotel, days_target, destination, trip_type, notes)
    if not plan or not plan.get("days"):
        plan = _fallback(places, days_target, max_stops)
        days, more = plan["days"], plan["more_to_explore"]
        warnings = plan["warnings"]
    else:
        days, more = _assemble(plan, places, days_target)
        warnings = [w for w in (plan.get("warnings") or []) if isinstance(w, str)]

    _apply_guardrail(days, more, warnings)
    return {"days": days, "more_to_explore": more, "warnings": warnings}
