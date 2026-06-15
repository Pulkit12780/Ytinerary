"""F3 — pipeline integration with all network-touching agents mocked.

Covers:
  - AC #3: a zero-URL request reaches a real plan (auto-sourced).
  - AC #5: pasted URLs take precedence over auto-sourcing.
  - ADR-002: an auto-sourced over-fetch keeps only transcript-available videos.
"""
import asyncio

import pytest

from backend import pipeline, metrics
from backend.models import PlanRequest


# ── Fakes ────────────────────────────────────────────────────────────────────


class _FakeSource:
    """Records calls and returns a fixed set of ranked candidates."""
    def __init__(self, n=8):
        self.calls = 0
        self._n = n

    async def search(self, destination, trip_type="balanced", limit=8):
        self.calls += 1
        return [
            {"url": f"https://www.youtube.com/watch?v=vid{i:08d}",
             "title": f"Video {i}", "video_id": f"vid{i:08d}", "score": float(8 - i)}
            for i in range(self._n)
        ][:limit]


def _install_fakes(monkeypatch, *, source, transcripts_without=()):
    """Patch every agent that would hit the network with deterministic stubs."""
    monkeypatch.setattr(pipeline, "_video_source", source)

    async def fake_fetch_transcript(url):
        vid = url.rsplit("=", 1)[-1].rsplit("/", 1)[-1]
        has = vid not in transcripts_without
        return {"url": url, "video_id": vid, "title": f"Title {vid}",
                "transcript": f"We visited Place {vid}." if has else None,
                "error": None if has else "no_transcript"}
    monkeypatch.setattr(pipeline.transcript_agent, "fetch_transcript", fake_fetch_transcript)

    async def fake_extract(transcript, destination, title=""):
        # one place per video, named after the transcript
        name = transcript.replace("We visited ", "").rstrip(".")
        return [{"name": name, "sentiment": "positive", "category": "attraction"}]
    monkeypatch.setattr(pipeline.extractor_agent, "extract_places", fake_extract)

    async def fake_augment(*a, **k):
        return {"attractions": [], "restaurants": []}
    monkeypatch.setattr(pipeline.augmenter_agent, "augment_places", fake_augment)

    async def fake_geocode(raw, destination):
        enriched = []
        for i, p in enumerate(raw):
            q = dict(p)
            q["lat"] = 26.91 + i * 0.001
            q["lng"] = 75.79 + i * 0.001
            enriched.append(q)
        return enriched, []
    monkeypatch.setattr(pipeline.geocoder_agent, "geocode_places", fake_geocode)

    # Force the judge's deterministic fallback (no LLM/network).
    async def fake_llm_plan(*a, **k):
        return None
    monkeypatch.setattr(pipeline.judge_agent, "_llm_plan", fake_llm_plan)


@pytest.fixture(autouse=True)
def _reset_metrics():
    metrics.reset()
    yield
    metrics.reset()


# ── Tests ────────────────────────────────────────────────────────────────────


def test_zero_url_request_reaches_a_plan(monkeypatch):
    src = _FakeSource(n=8)
    _install_fakes(monkeypatch, source=src)

    resp = asyncio.run(pipeline.run(PlanRequest(destination="Jaipur", trip_type="balanced")))

    assert src.calls == 1                     # auto-sourcing happened
    assert resp.total_places > 0              # a real plan came out
    assert resp.clusters                      # at least one day
    # metrics recorded a zero-URL, auto-sourced success
    snap = metrics.snapshot()
    assert snap["counters"]["zero_url_sessions"] == 1
    assert snap["counters"]["auto_sourced_ok"] == 1
    assert snap["counters"]["plans_succeeded"] == 1


def test_thin_manual_paste_is_topped_up_to_minimum(monkeypatch):
    # A single pasted URL is kept and PRIORITIZED, but topped up with auto-sourced
    # videos so the plan draws on at least _MIN_VIDEOS creators.
    src = _FakeSource(n=8)
    _install_fakes(monkeypatch, source=src)

    resp = asyncio.run(pipeline.run(PlanRequest(
        destination="Jaipur",
        youtube_urls=["https://www.youtube.com/watch?v=manual00001"],
    )))

    assert src.calls == 1                       # auto-sourcing ran to top up
    titles = " ".join(resp.video_titles)
    assert "manual00001" in titles              # the pasted link is kept
    assert len(resp.video_titles) == pipeline._MIN_VIDEOS  # topped up to the minimum
    # still a manual (not zero-URL) session
    assert metrics.snapshot()["counters"]["zero_url_sessions"] == 0


def test_rich_manual_paste_is_not_topped_up(monkeypatch):
    # Five+ pasted URLs are already rich — auto-sourcing is skipped entirely.
    src = _FakeSource(n=8)
    _install_fakes(monkeypatch, source=src)

    urls = [f"https://www.youtube.com/watch?v=manual{i:05d}" for i in range(5)]
    resp = asyncio.run(pipeline.run(PlanRequest(destination="Jaipur", youtube_urls=urls)))

    assert src.calls == 0                       # no top-up needed
    assert len(resp.video_titles) == 5


def test_overfetch_keeps_only_transcript_available(monkeypatch):
    # 8 sourced, 3 have no transcript → keep first 5 transcript-yielding (B5).
    src = _FakeSource(n=8)
    _install_fakes(
        monkeypatch, source=src,
        transcripts_without=("vid00000001", "vid00000003", "vid00000005"),
    )

    resp = asyncio.run(pipeline.run(PlanRequest(destination="Jaipur")))

    # 5 kept, all transcript-available; the 3 dead ones excluded.
    assert len(resp.video_titles) == 5
    for dead in ("vid00000001", "vid00000003", "vid00000005"):
        assert dead not in " ".join(resp.video_titles)


def test_no_videos_falls_through_to_curator(monkeypatch):
    """Videos are optional now: when auto-sourcing finds nothing, the travel-expert
    curator still produces a plan instead of the pipeline hard-failing."""
    class _Empty:
        async def search(self, *a, **k):
            return []
    _install_fakes(monkeypatch, source=_Empty())

    # Curator returns real places even with zero videos.
    async def curator_with_places(*a, **k):
        return {
            "attractions": [{"name": "Hawa Mahal", "category": "sight",
                             "importance": "must_see", "source": "suggested",
                             "source_videos": []}],
            "restaurants": [{"name": "LMB", "category": "food", "meal_type": "lunch",
                             "source": "suggested", "source_videos": []}],
        }
    monkeypatch.setattr(pipeline.augmenter_agent, "augment_places", curator_with_places)

    resp = asyncio.run(pipeline.run(PlanRequest(destination="Jaipur")))

    assert resp.total_places > 0          # a real plan from curated research alone
    assert not resp.video_titles          # built without any videos
    assert any("research" in w.lower() for w in resp.warnings)  # soft note surfaced
    assert metrics.snapshot()["counters"]["plans_succeeded"] == 1


def test_zero_places_when_nothing_found(monkeypatch):
    """No videos AND an empty curator → the only genuine dead end: ZERO_PLACES."""
    class _Empty:
        async def search(self, *a, **k):
            return []
    _install_fakes(monkeypatch, source=_Empty())  # _install_fakes' curator returns empty

    with pytest.raises(pipeline.PipelineError) as exc:
        asyncio.run(pipeline.run(PlanRequest(destination="Atlantis")))
    assert exc.value.code == "ZERO_PLACES"

    assert metrics.snapshot()["counters"]["plans_failed"] == 1
