"""Quality guards for the 2026-06-15 fixes: near-duplicate collapse + day balancing."""
from backend.agents import geocoder, judge


# ── Near-duplicate place collapse (geocoder) ─────────────────────────────────


def test_near_duplicates_are_merged_keeping_richer_record():
    enriched = [
        {"name": "Sigiriya Rock", "lat": 7.9570, "lng": 80.7603,
         "importance": "must_see", "description": "Ancient rock fortress.",
         "source": "suggested", "source_videos": [{"url": "u1", "title": "t1"}]},
        {"name": "Sigiriya", "lat": 7.9572, "lng": 80.7601,   # ~25m away
         "importance": None, "description": None,
         "source": "video", "source_videos": [{"url": "u2", "title": "t2"}]},
    ]
    merged = geocoder._merge_near_duplicates(enriched)

    assert len(merged) == 1                       # collapsed into one place
    assert merged[0]["name"] == "Sigiriya Rock"   # the richer (must_see) record won
    urls = {sv["url"] for sv in merged[0]["source_videos"]}
    assert urls == {"u1", "u2"}                   # both videos credited


def test_distinct_nearby_places_are_not_merged():
    enriched = [
        {"name": "Galle Lighthouse", "lat": 6.0269, "lng": 80.2170,
         "source": "suggested", "source_videos": []},
        {"name": "Dutch Reformed Church", "lat": 6.0286, "lng": 80.2156,  # ~250m, no name overlap
         "source": "suggested", "source_videos": []},
    ]
    assert len(geocoder._merge_near_duplicates(enriched)) == 2


# ── Day balancing (judge) ────────────────────────────────────────────────────


def _stop(name, i):
    # All clustered within ~1km so geography permits moving stops between days.
    return {"name": name, "lat": 26.9124 + i * 0.001, "lng": 75.7873 + i * 0.001,
            "category": "attraction", "source": "video"}


def test_rebalance_evens_out_a_lopsided_plan():
    fat = {"theme": "Packed", "notes": None, "stops": [_stop(f"A{i}", i) for i in range(8)]}
    thin = {"theme": "Empty", "notes": None, "stops": [_stop("B0", 8)]}
    days = [fat, thin]
    more: list = []

    judge._rebalance(days, more, max_stops=6, regional=False)

    counts = [len(d["stops"]) for d in days]
    assert max(counts) - min(counts) <= 1         # no more 8-vs-1 imbalance
    assert min(counts) >= 2                        # no near-empty days
    # Nothing is lost: every original stop is still somewhere.
    placed = {s["name"] for d in days for s in d["stops"]} | {p["name"] for p in more}
    assert placed == {f"A{i}" for i in range(8)} | {"B0"}


def test_rebalance_respects_the_per_day_cap():
    fat = {"theme": "Packed", "notes": None, "stops": [_stop(f"A{i}", i) for i in range(10)]}
    days = [fat]
    more: list = []

    judge._rebalance(days, more, max_stops=5, regional=False)

    assert len(days[0]["stops"]) <= 5             # never exceeds the cap
