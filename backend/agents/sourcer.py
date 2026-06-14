"""Video sourcing seam (ADR-001).

A `VideoSource` turns trip intent (destination + trip_type) into a ranked list of
candidate videos *before* the transcript pipeline runs. Manual URLs short-circuit
this node entirely (manual precedence, AC #5) — the seam only fires when the user
gave us no URLs of their own.

Implementations:
  - `StubVideoSource`     — fixed curated URLs for a few known destinations, with a
                            generic fallback. Used in dev / Milestone 1 so the intent
                            (workstream C) and frontend (workstream D) work can build
                            and test the zero-URL path end-to-end WITHOUT burning
                            YouTube quota.
  - `YouTubeSearchSource` — real YouTube Data API search + ranking (Milestone 3,
                            tasks B2/B3/B5/B6). Not built yet.

A future `InstagramSource` / blog source implements this same one-method contract
without touching the LangGraph graph.

The query modifier per trip type lives in `models.TRIP_TYPE_SEARCH_MODIFIERS`
(single source of truth, dev plan §2).
"""
from __future__ import annotations

import logging
import math
import os
from abc import ABC, abstractmethod
from datetime import datetime, timezone
from typing import TypedDict

import httpx

from .. import cache
from ..models import TripType, TRIP_TYPE_SEARCH_MODIFIERS

_log = logging.getLogger("ytinerary.sourcer")


class VideoCandidate(TypedDict):
    url: str
    title: str
    video_id: str
    score: float  # higher = better; ranking is the source's responsibility


class VideoSource(ABC):
    """Seam between trip intent and the transcript pipeline (ADR-001)."""

    @abstractmethod
    async def search(
        self, destination: str, trip_type: TripType = "balanced", limit: int = 8
    ) -> list[VideoCandidate]:
        """Return up to `limit` ranked candidate videos for the trip.

        Over-fetch is intentional (ADR-002): callers ask for ~8 and let
        `fetch_transcripts` be the real filter.

        MUST NOT raise. Return ``[]`` on any failure so the pipeline degrades to
        the paste fallback (NO_VIDEOS_FOUND) instead of returning a 500.
        """
        ...


# ── Stub implementation (Milestone 1) ────────────────────────────────────────


def _normalize(destination: str) -> str:
    """City/region key for curated lookup: lowercased, first comma-segment."""
    return destination.strip().lower().split(",")[0].strip()


# Curated, hand-picked travel-vlog URLs per destination. These are dev placeholders
# for the real YouTube search (M3) — they exist so the zero-URL flow reaches a real
# plan without API quota. Replace/extend freely; keys are normalized destinations.
_CURATED: dict[str, list[VideoCandidate]] = {
    "jaipur": [
        {"url": "https://www.youtube.com/watch?v=Yj4Dn4y8Ev0", "title": "Jaipur Travel Guide", "video_id": "Yj4Dn4y8Ev0", "score": 0.95},
        {"url": "https://www.youtube.com/watch?v=8aVa6CzGFsw", "title": "Top Things To Do in Jaipur", "video_id": "8aVa6CzGFsw", "score": 0.88},
        {"url": "https://www.youtube.com/watch?v=qz7Qk9p7r2A", "title": "Jaipur Food & Markets", "video_id": "qz7Qk9p7r2A", "score": 0.80},
    ],
    "tokyo": [
        {"url": "https://www.youtube.com/watch?v=8sJYRrqj4yM", "title": "Tokyo Travel Guide", "video_id": "8sJYRrqj4yM", "score": 0.95},
        {"url": "https://www.youtube.com/watch?v=kJ3S3I8m3hU", "title": "3 Days in Tokyo", "video_id": "kJ3S3I8m3hU", "score": 0.87},
    ],
    "paris": [
        {"url": "https://www.youtube.com/watch?v=AQ6GmpMu5L8", "title": "Paris Travel Guide", "video_id": "AQ6GmpMu5L8", "score": 0.94},
        {"url": "https://www.youtube.com/watch?v=tV8m6Xm6q4o", "title": "Paris in 4 Days", "video_id": "tV8m6Xm6q4o", "score": 0.86},
    ],
}

# Last-resort generic vlogs so any destination reaches the pipeline during dev.
_GENERIC: list[VideoCandidate] = [
    {"url": "https://www.youtube.com/watch?v=Yj4Dn4y8Ev0", "title": "Travel Vlog", "video_id": "Yj4Dn4y8Ev0", "score": 0.50},
]


class StubVideoSource(VideoSource):
    """Returns curated URLs for known destinations; generic fallback otherwise.

    Ignores `trip_type` beyond logging intent — ranking/personalization of sourced
    videos arrives with the real `YouTubeSearchSource` (M3). Never raises.
    """

    async def search(
        self, destination: str, trip_type: TripType = "balanced", limit: int = 8
    ) -> list[VideoCandidate]:
        try:
            candidates = _CURATED.get(_normalize(destination)) or _GENERIC
            ranked = sorted(candidates, key=lambda c: c["score"], reverse=True)
            return ranked[: max(0, limit)]
        except Exception:
            return []


# ── Real YouTube Data API source (Milestone 3) ───────────────────────────────


_SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"
_VIDEOS_URL = "https://www.googleapis.com/youtube/v3/videos"
_CACHE_TTL_SECONDS = 24 * 3600  # one search/day per (destination, trip_type) — B3

# Ranking weights (ADR-002): relevance dominates, recency and view-velocity refine,
# caption availability is a soft multiplier (never a hard gate).
_W_RELEVANCE = 3.0
_W_RECENCY = 1.0
_W_VELOCITY = 0.5
_CAPTION_BOOST = 1.15


class _QuotaExceeded(Exception):
    """Raised internally when YouTube returns a 403 quota/rate error (E2)."""


def _build_query(destination: str, trip_type: str) -> str:
    modifier = TRIP_TYPE_SEARCH_MODIFIERS.get(trip_type or "balanced", "")
    parts = [destination.strip(), modifier, "travel vlog"]
    return " ".join(p for p in parts if p)


def _age_days(published_at: str | None) -> float:
    if not published_at:
        return 3650.0
    try:
        dt = datetime.fromisoformat(published_at.replace("Z", "+00:00"))
        return max(0.0, (datetime.now(timezone.utc) - dt).total_seconds() / 86400.0)
    except Exception:
        return 3650.0


def _score(rank: int, published_at: str | None, views: int, has_caption: bool) -> float:
    relevance = 1.0 / (1 + rank)                      # earlier search rank = better
    age = _age_days(published_at)
    recency = 1.0 / (1 + age / 365.0)                 # decays over years
    velocity = math.log10(views / max(age, 1.0) + 1)  # views/day, log-compressed
    boost = _CAPTION_BOOST if has_caption else 1.0
    return boost * (_W_RELEVANCE * relevance + _W_RECENCY * recency + _W_VELOCITY * velocity)


def _raise_for_quota(resp: httpx.Response) -> None:
    if resp.status_code != 403:
        return
    try:
        reasons = {e.get("reason") for e in resp.json().get("error", {}).get("errors", [])}
    except Exception:
        reasons = set()
    # A 403 from this API is almost always quota/rate related; treat it as such.
    if not reasons or reasons & {"quotaExceeded", "dailyLimitExceeded", "rateLimitExceeded"}:
        raise _QuotaExceeded(", ".join(r for r in reasons if r) or "quotaExceeded")


class YouTubeSearchSource(VideoSource):
    """Real YouTube Data API v3 source via the REST endpoint (httpx, no extra dep).

    Reads `YOUTUBE_API_KEY` at call time. Over-fetches a ranked candidate set
    (ADR-002) and caches it 24h per (destination, trip_type) to conserve quota (B3).
    Never raises — quota or any API failure degrades to ``[]`` so the pipeline can
    surface the paste fallback (NO_VIDEOS_FOUND) instead of 500ing (E2).
    """

    def __init__(self, cache_ttl_seconds: float = _CACHE_TTL_SECONDS) -> None:
        self._cache_ttl = cache_ttl_seconds

    async def search(
        self, destination: str, trip_type: TripType = "balanced", limit: int = 8
    ) -> list[VideoCandidate]:
        api_key = os.getenv("YOUTUBE_API_KEY")
        if not api_key:
            _log.warning("YOUTUBE_API_KEY not set — skipping auto-sourcing")
            return []

        tt = trip_type or "balanced"
        cache_key = f"ytsearch:{_normalize(destination)}:{tt}"
        cached = cache.get_ttl(cache_key)
        if cached is not None:
            return list(cached)[: max(0, limit)]

        try:
            candidates = await self._search_uncached(api_key, destination, tt)
        except _QuotaExceeded as exc:
            _log.warning("YouTube quota exceeded (%s) — degrading to paste fallback", exc)
            return []
        except Exception as exc:
            _log.warning("YouTube search failed: %s", exc)
            return []

        if candidates:
            cache.set_ttl(cache_key, candidates, self._cache_ttl)
        return candidates[: max(0, limit)]

    async def _search_uncached(
        self, api_key: str, destination: str, trip_type: str
    ) -> list[VideoCandidate]:
        query = _build_query(destination, trip_type)
        async with httpx.AsyncClient(timeout=10.0) as client:
            # 1. search.list (100 units) — videoCaption is a soft preference (ADR-002).
            sr = await client.get(_SEARCH_URL, params={
                "key": api_key,
                "part": "snippet",
                "type": "video",
                "q": query,
                "relevanceLanguage": "en",
                "order": "relevance",
                "maxResults": 12,
                "videoCaption": "closedCaption",
            })
            _raise_for_quota(sr)
            sr.raise_for_status()

            snippets: dict[str, dict] = {}
            for rank, item in enumerate(sr.json().get("items", [])):
                vid = (item.get("id") or {}).get("videoId")
                if vid and vid not in snippets:
                    sn = item.get("snippet") or {}
                    snippets[vid] = {
                        "title": sn.get("title") or vid,
                        "published_at": sn.get("publishedAt"),
                        "rank": rank,
                    }
            if not snippets:
                return []

            # 2. videos.list (1 unit) — viewCount + caption flag for ranking.
            vr = await client.get(_VIDEOS_URL, params={
                "key": api_key,
                "part": "statistics,contentDetails",
                "id": ",".join(snippets.keys()),
            })
            _raise_for_quota(vr)
            vr.raise_for_status()

            stats: dict[str, dict] = {}
            for item in vr.json().get("items", []):
                vid = item.get("id")
                st = item.get("statistics") or {}
                cd = item.get("contentDetails") or {}
                stats[vid] = {
                    "views": int(st.get("viewCount") or 0),
                    "caption": cd.get("caption") == "true",
                }

        candidates: list[VideoCandidate] = []
        for vid, sn in snippets.items():
            stat = stats.get(vid, {})
            candidates.append({
                "url": f"https://www.youtube.com/watch?v={vid}",
                "title": sn["title"],
                "video_id": vid,
                "score": _score(sn["rank"], sn["published_at"],
                                stat.get("views", 0), stat.get("caption", False)),
            })
        candidates.sort(key=lambda c: c["score"], reverse=True)
        return candidates[:8]  # over-fetch ~8 (ADR-002); transcript-fetch is the real filter
