"""F2 — sourcer ranking, query builder, quota guard, and cache TTL.

All YouTube calls are mocked (httpx swapped) so no quota is spent in CI.
"""
import asyncio

import httpx
import pytest

from backend import cache
from backend.agents import sourcer


# ── Query builder per trip type ──────────────────────────────────────────────


@pytest.mark.parametrize("trip_type,expected", [
    ("balanced", "Jaipur travel vlog"),
    ("family", "Jaipur with kids family travel vlog"),
    ("romantic", "Jaipur honeymoon couples travel vlog"),
    ("culture", "Jaipur heritage culture history travel vlog"),
])
def test_build_query_per_trip_type(trip_type, expected):
    assert sourcer._build_query("Jaipur", trip_type) == expected


def test_build_query_strips_and_handles_unknown():
    assert sourcer._build_query("  Tokyo  ", "balanced") == "Tokyo travel vlog"


# ── Ranking ──────────────────────────────────────────────────────────────────


def test_score_prefers_relevance_recency_views_and_captions():
    top = sourcer._score(0, "2024-01-01T00:00:00Z", 1_000_000, True)
    low = sourcer._score(9, "2010-01-01T00:00:00Z", 100, False)
    assert top > low


def test_caption_flag_is_a_boost_not_a_gate():
    with_cap = sourcer._score(0, "2024-01-01T00:00:00Z", 1000, True)
    without = sourcer._score(0, "2024-01-01T00:00:00Z", 1000, False)
    assert with_cap > without  # boosts, but a no-caption video still scores > 0
    assert without > 0


# ── Quota guard (E2) ─────────────────────────────────────────────────────────


class _Resp:
    def __init__(self, status, payload):
        self.status_code = status
        self._payload = payload

    def json(self):
        return self._payload

    def raise_for_status(self):
        if self.status_code >= 400:
            raise httpx.HTTPStatusError("err", request=None, response=None)


def test_raise_for_quota_on_403():
    with pytest.raises(sourcer._QuotaExceeded):
        sourcer._raise_for_quota(_Resp(403, {"error": {"errors": [{"reason": "quotaExceeded"}]}}))
    # bare 403 with no parseable reason is still treated as quota
    with pytest.raises(sourcer._QuotaExceeded):
        sourcer._raise_for_quota(_Resp(403, {}))
    # non-403 passes through
    sourcer._raise_for_quota(_Resp(200, {}))


# ── End-to-end search with mocked httpx ──────────────────────────────────────


class _FakeClient:
    """Mock httpx.AsyncClient returning a fixed search + videos response."""
    instances = 0

    def __init__(self, *a, **k):
        _FakeClient.instances += 1

    async def __aenter__(self):
        return self

    async def __aexit__(self, *a):
        return False

    async def get(self, url, params=None):
        if "search" in url:
            return _Resp(200, {"items": [
                {"id": {"videoId": "AAAAAAAAAAA"},
                 "snippet": {"title": "Best Jaipur Vlog", "publishedAt": "2024-01-01T00:00:00Z"}},
                {"id": {"videoId": "BBBBBBBBBBB"},
                 "snippet": {"title": "Old Jaipur", "publishedAt": "2012-01-01T00:00:00Z"}},
            ]})
        return _Resp(200, {"items": [
            {"id": "AAAAAAAAAAA", "statistics": {"viewCount": "900000"},
             "contentDetails": {"caption": "true"}},
            {"id": "BBBBBBBBBBB", "statistics": {"viewCount": "500"},
             "contentDetails": {"caption": "false"}},
        ]})


@pytest.fixture(autouse=True)
def _clean(monkeypatch):
    cache.clear()
    _FakeClient.instances = 0
    monkeypatch.delenv("YOUTUBE_API_KEY", raising=False)
    yield
    cache.clear()


def test_search_returns_ranked_candidates(monkeypatch):
    monkeypatch.setenv("YOUTUBE_API_KEY", "test")
    monkeypatch.setattr(httpx, "AsyncClient", _FakeClient)
    res = asyncio.run(sourcer.YouTubeSearchSource().search("Jaipur", "balanced", limit=8))
    assert [c["video_id"] for c in res] == ["AAAAAAAAAAA", "BBBBBBBBBBB"]
    assert res[0]["url"] == "https://www.youtube.com/watch?v=AAAAAAAAAAA"
    assert all(c["score"] > 0 for c in res)


def test_search_without_key_returns_empty(monkeypatch):
    monkeypatch.setattr(httpx, "AsyncClient", _FakeClient)
    res = asyncio.run(sourcer.YouTubeSearchSource().search("Jaipur"))
    assert res == []
    assert _FakeClient.instances == 0  # never hit the network


def test_search_caches_per_destination_trip_type(monkeypatch):
    monkeypatch.setenv("YOUTUBE_API_KEY", "test")
    monkeypatch.setattr(httpx, "AsyncClient", _FakeClient)
    src = sourcer.YouTubeSearchSource()
    first = asyncio.run(src.search("Jaipur", "balanced"))
    after_first = _FakeClient.instances
    second = asyncio.run(src.search("Jaipur", "balanced"))
    assert second == first
    assert _FakeClient.instances == after_first  # served from cache, no new client


def test_cache_ttl_expiry():
    cache.set_ttl("k", [1, 2], ttl_seconds=100)
    assert cache.get_ttl("k") == [1, 2]
    cache.set_ttl("expired", "v", ttl_seconds=-1)
    assert cache.get_ttl("expired") is None
    assert cache.get_ttl("missing") is None


def test_quota_degrades_to_empty(monkeypatch):
    monkeypatch.setenv("YOUTUBE_API_KEY", "test")

    class _QuotaClient(_FakeClient):
        async def get(self, url, params=None):
            return _Resp(403, {"error": {"errors": [{"reason": "quotaExceeded"}]}})

    monkeypatch.setattr(httpx, "AsyncClient", _QuotaClient)
    res = asyncio.run(sourcer.YouTubeSearchSource().search("Jaipur"))
    assert res == []  # never raises — surfaces NO_VIDEOS_FOUND downstream


def test_stub_source_returns_candidates():
    res = asyncio.run(sourcer.StubVideoSource().search("Jaipur, India", "romantic"))
    assert res and all({"url", "title", "video_id", "score"} <= set(c) for c in res)
    # unknown destination still yields the generic fallback (dev convenience)
    assert asyncio.run(sourcer.StubVideoSource().search("Nowhereville"))
