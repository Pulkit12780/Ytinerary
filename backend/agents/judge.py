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

Plan like a local expert who respects the traveler's limited time — not a clustering script.

Hard rules:
- Each day must be geographically TIGHT: only group places realistically doable together
  in one day given the distances provided. Never put far-apart places (a long cross-town
  or out-of-town trip) in the same day. Defer such outliers to "more_to_explore".
- If the places span multiple towns/areas (a regional trip), build the plan as BASES:
  spend consecutive days in one area before moving to the next, and never zig-zag between
  far-apart areas within a day. Each day's theme should name its area/base.
- PRIORITIZE by importance: every "must_see" should appear in the plan on its best-fit
  day. Fill remaining room with "recommended" and a hidden_gem or two for flavour. If you
  must leave things out to keep days realistic, defer "optional" ones FIRST.
- FIT the traveler: honour the audience and budget given in the request — pace and pick
  places (and restaurants) that suit them.
- Respect the requested number of days. Spread the best attractions across them; don't
  front-load everything into day one.
- Every day should include meals: a breakfast, a lunch and a dinner, chosen from the food
  places near that day's attractions. Tag them with the right meal_type.
- Order each day's stops as a sensible timeline: breakfast → nearby morning sights →
  lunch → afternoon sights → dinner (end on a sunset/viewpoint when one fits). Set
  time_of_day accordingly.
- Write each day's "notes" as a one-sentence rationale a real guide would give.
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
        # Expert signals the planner prioritizes on (only emit what's set).
        tags = []
        if p.get("importance"):
            tags.append(p["importance"])
        if p.get("area"):
            tags.append(f"area={p['area']}")
        if p.get("budget_tier"):
            tags.append(f"${p['budget_tier']}")
        if p.get("audience"):
            tags.append("for=" + "/".join(p["audience"]))
        if p.get("duration_hrs"):
            tags.append(f"~{p['duration_hrs']}h")
        tag_s = (", " + ", ".join(tags)) if tags else ""
        lines.append(
            f"- {p['name']} [zone {zones[i]}, {kind}, src={p.get('source', 'video')}{meal_s}{tag_s}{dist_h}]"
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
    budget: str = "any",
    audience: str | None = None,
    regional: bool = False,
) -> dict | None:
    global _client
    if _client is None:
        _client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    max_stops = _max_stops_for(trip_type)
    shape = _TRIP_TYPE_SHAPE.get(trip_type or "balanced", "")
    shape_line = f"{shape}\n" if shape else ""
    notes_line = f'Traveler notes (respect these): "{notes}"\n' if notes else ""
    aud_line = f"Travelling as: {audience}\n" if audience else ""
    budget_line = f"Budget: {budget}\n" if budget and budget != "any" else ""
    region_line = (
        "This is a REGIONAL trip: the places span multiple towns/areas. Build it as "
        "bases — group consecutive days by area and move between areas in a sensible "
        "order; never mix far-apart areas in one day.\n" if regional else ""
    )

    prompt = (
        f"Destination: {destination}\n"
        f"Number of days: {num_days}\n"
        f"Hotel: {hotel['name'] if hotel else '(none)'}\n"
        f"{aud_line}{budget_line}"
        f"Cap each day at about {max_stops} stops total including meals.\n"
        f"{region_line}{shape_line}{notes_line}\n"
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
    days: list[dict], more: list[dict], warnings: list[str],
    radius_km: float = MAX_DAY_RADIUS_KM,
) -> None:
    """Deterministic backstop: move any stop too far from its day's core to more_to_explore.
    `radius_km` widens for regional/multi-base trips where day-trips from a base are normal."""
    for day in days:
        stops = day["stops"]
        if len(stops) <= 2:
            continue
        core = _medoid(stops)
        keep, evicted = [], []
        for s in stops:
            if s is core or _haversine(_coord(s), _coord(core)) <= radius_km:
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


# Importance → sort rank (lower = keep first when a day hits its cap). Unknown/None
# sorts as "recommended" so curated must-sees always survive ahead of optional filler.
_IMPORTANCE_RANK = {"must_see": 0, "recommended": 1, "hidden_gem": 2, "optional": 3}


def _importance_key(p: dict) -> int:
    return _IMPORTANCE_RANK.get(p.get("importance") or "recommended", 1)


def _is_regional(places: list[dict]) -> bool:
    """True when places are spread far enough that one tight city plan can't hold them
    (a province/island/country trip) — switches the planner into multi-base mode."""
    coords = [_coord(p) for p in places]
    if len(coords) < 2:
        return False
    c = _centroid(coords)
    return max(_haversine(c, pt) for pt in coords) > 40.0


def _is_meal(s: dict) -> bool:
    return bool(s.get("meal_type") or s.get("category") == "food")


def _keep_key(s: dict) -> tuple[int, int]:
    """Sort key for trimming a fat day — best-to-keep first. Meals and must-sees stay;
    low-importance attractions are the first to be moved out."""
    return (_importance_key(s), 0 if _is_meal(s) else 1)


def _timeline_key(s: dict) -> float:
    """Order a day's stops as a real timeline: breakfast → morning → lunch → afternoon
    → evening sight → dinner. Stable, so same-slot order is preserved."""
    meal = s.get("meal_type")
    if meal == "breakfast":
        return 0.0
    if meal == "lunch":
        return 2.0
    if meal == "dinner":
        return 5.0
    return {"Morning": 1.0, "Afternoon": 3.0, "Evening": 4.0}.get(s.get("time_of_day"), 3.0)


def _rebalance(days: list[dict], more: list[dict], max_stops: int, regional: bool) -> None:
    """Even out stops across days so we never ship a 1-stop day next to an 8-stop one.
    Trims over-full days and refills thin ones from geographically compatible places
    (other days' overflow + More to Explore). Mutates `days` and `more` in place."""
    if not days:
        return
    radius = 25.0 if regional else MAX_DAY_RADIUS_KM
    scheduled = sum(len(d["stops"]) for d in days)
    target = max(2, min(max_stops, round(scheduled / len(days)) or 2))

    # 1. Trim fat days down to target, keeping meals + the most important stops.
    pool: list[dict] = []
    for d in days:
        if len(d["stops"]) > target:
            ranked = sorted(d["stops"], key=_keep_key)
            d["stops"] = ranked[:target]
            pool.extend(ranked[target:])

    # 2. Fill thin days from the pool, then from More to Explore — only with places
    #    that actually sit near that day's core (so we don't recreate impossible days).
    sources = pool + list(more)
    used: set[int] = set()
    for d in days:
        if not d["stops"]:
            continue
        core = _medoid(d["stops"])
        for cand in sources:
            if len(d["stops"]) >= target:
                break
            if id(cand) in used:
                continue
            if _haversine(_coord(cand), _coord(core)) <= radius:
                d["stops"].append(cand)
                used.add(id(cand))

    # 3. Order each day as a sensible timeline (meals interleaved), and rebuild More.
    for d in days:
        d["stops"].sort(key=_timeline_key)
    more[:] = [c for c in sources if id(c) not in used]


def _fallback(places: list[dict], num_days: int, max_stops: int) -> dict:
    """Deterministic plan if the LLM is unavailable: proximity zones → days, meals kept.
    Within a day we keep the most important places first so the per-day cap never drops a
    must-see in favour of optional filler."""
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
        ordered = sorted(b, key=_importance_key)  # stable: equal importance keeps input order
        days.append({"theme": "Exploring the area", "notes": None, "stops": ordered[:max_stops]})
        overflow.extend(ordered[max_stops:])
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
    budget: str = "any",
    audience: str | None = None,
) -> dict:
    """
    Returns {"days": [{theme, notes, stops:[place...]}], "more_to_explore": [place...],
    "warnings": [str]}. Never raises.

    `trip_type` controls pace/shape and the per-day stop cap (§2, C3); `budget`/`audience`
    bias which places the planner keeps; `notes` is the traveler's verbatim free text. All
    default so existing callers are unaffected. Regional spreads switch to multi-base mode.
    """
    if not places:
        return {"days": [], "more_to_explore": [], "warnings": []}

    max_stops = _max_stops_for(trip_type)
    # No-dates heuristic: fewer stops/day → spread the same places over more days.
    days_target = num_days or max(1, min(5, (len(places) + max_stops - 1) // max_stops))
    zones = _pregroup(places, MAX_DAY_RADIUS_KM)
    regional = _is_regional(places)

    plan = await _llm_plan(places, zones, hotel, days_target, destination, trip_type,
                           notes, budget, audience, regional)
    if not plan or not plan.get("days"):
        plan = _fallback(places, days_target, max_stops)
        days, more = plan["days"], plan["more_to_explore"]
        warnings = plan["warnings"]
    else:
        days, more = _assemble(plan, places, days_target)
        warnings = [w for w in (plan.get("warnings") or []) if isinstance(w, str)]

    _apply_guardrail(days, more, warnings, 25.0 if regional else MAX_DAY_RADIUS_KM)
    _rebalance(days, more, max_stops, regional)
    return {"days": days, "more_to_explore": more, "warnings": warnings}
