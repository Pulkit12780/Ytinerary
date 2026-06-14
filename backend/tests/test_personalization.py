"""F4 — personalization diff harness (ACs #1/#2/#4, brief §8 metric).

Two layers:
  - Deterministic (CI): proves the C3 structural knob — `family` produces a
    materially lighter plan than `balanced` on identical inputs (no LLM/network).
    This is the regression guard and the per-day-intensity metric instrument.
  - Live (opt-in): runs the real augmenter + judge for two trip types on the same
    destination and asserts the *scheduled place set* differs by >= 40%. Enabled
    only with YTINERARY_RUN_LIVE=1 and an OPENAI key, so CI spends no quota.
"""
import asyncio
import os

import pytest

from backend.agents import judge
from backend.models import PlanRequest


def _cluster(n):
    """n attractions packed within one walkable zone (so geography isn't the variable)."""
    return [
        {"name": f"Place {i}", "lat": 26.9124 + i * 0.0008, "lng": 75.7873 + i * 0.0008,
         "category": "attraction", "source": "video"}
        for i in range(n)
    ]


def _scheduled(plan):
    return [s["name"] for day in plan["days"] for s in day["stops"]]


def _max_day(plan):
    return max((len(day["stops"]) for day in plan["days"]), default=0)


# ── Deterministic structural harness ─────────────────────────────────────────


def test_family_plan_is_structurally_lighter_than_balanced(monkeypatch):
    # Force the deterministic fallback so the only variable is trip_type (C3).
    async def no_llm(*a, **k):
        return None
    monkeypatch.setattr(judge, "_llm_plan", no_llm)

    places = _cluster(14)
    balanced = asyncio.run(judge.plan_itinerary(places, None, 1, "Jaipur", "balanced"))
    family = asyncio.run(judge.plan_itinerary(places, None, 1, "Jaipur", "family"))

    bal_max, fam_max = _max_day(balanced), _max_day(family)
    assert bal_max == 7 and fam_max == 5            # caps from _TRIP_TYPE_MAX_STOPS

    # AC #2 as a measurable number: balanced packs >= 40% more stops/day than family.
    intensity_ratio = bal_max / fam_max
    assert intensity_ratio >= 1.4, intensity_ratio

    # The scheduled sets genuinely diverge (family defers stops to More to Explore).
    bal_set, fam_set = set(_scheduled(balanced)), set(_scheduled(family))
    assert fam_set < bal_set                         # family is a strict subset here
    assert len(bal_set) > len(fam_set)


def test_stops_per_day_helper_matches_taxonomy():
    assert judge._max_stops_for("family") == 5
    assert judge._max_stops_for("nature") == 5
    assert judge._max_stops_for("balanced") == 7
    assert judge._max_stops_for(None) == 7
    assert judge._max_stops_for("unknown") == 7      # safe default


def test_no_dates_heuristic_spreads_family_over_more_days(monkeypatch):
    async def no_llm(*a, **k):
        return None
    monkeypatch.setattr(judge, "_llm_plan", no_llm)

    places = _cluster(14)
    # No num_days → fewer stops/day means more days for the same place count.
    balanced = asyncio.run(judge.plan_itinerary(places, None, None, "Jaipur", "balanced"))
    family = asyncio.run(judge.plan_itinerary(places, None, None, "Jaipur", "family"))
    assert len(family["days"]) >= len(balanced["days"])


# ── Live diff harness (opt-in; doubles as the §8 metric instrument) ──────────


_LIVE = os.getenv("YTINERARY_RUN_LIVE") == "1" and bool(os.getenv("OPENAI_API_KEY"))


@pytest.mark.skipif(not _LIVE, reason="set YTINERARY_RUN_LIVE=1 + OPENAI_API_KEY")
def test_live_personalization_diff_at_least_40pct():
    from backend import pipeline

    urls = ["https://www.youtube.com/watch?v=Yj4Dn4y8Ev0"]  # one known travel vlog
    base = dict(destination="Jaipur", youtube_urls=urls,
                start_date="2026-07-01", end_date="2026-07-03")

    bal = asyncio.run(pipeline.run(PlanRequest(**base, trip_type="balanced")))
    rom = asyncio.run(pipeline.run(PlanRequest(**base, trip_type="romantic")))

    def names(resp):
        return {p.name for c in resp.clusters for p in c.places}

    a, b = names(bal), names(rom)
    diff = len(a ^ b) / max(1, len(a | b))
    print(f"\n[F4] balanced vs romantic scheduled-place diff = {diff:.0%}")
    assert diff >= 0.40, f"personalization diff {diff:.0%} < 40%"
