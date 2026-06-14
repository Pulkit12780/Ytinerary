"""Lightweight in-process metric instrumentation (dev plan E3 / brief §8).

Tracks the success metrics the brief cares about without pulling in a metrics
backend: zero-URL session share, time-to-first-plan, fallback-path usage, and the
NO_VIDEOS_FOUND rate. Each plan run emits one structured log line and bumps
in-memory counters exposed at GET /metrics.

This is process-local and resets on restart — enough to validate the launch
hypothesis; swap for a real metrics sink (StatsD/Prometheus) when scaling.
"""
from __future__ import annotations

import json
import logging
from threading import Lock

_log = logging.getLogger("ytinerary.metrics")
_lock = Lock()

_counters: dict[str, int] = {
    "plans_total": 0,          # every /plan(/stream) invocation that reached the pipeline
    "plans_succeeded": 0,
    "plans_failed": 0,
    "zero_url_sessions": 0,    # requests with no manual URLs (intent-only)
    "auto_sourced_ok": 0,      # zero-URL requests where auto-sourcing yielded videos
    "no_videos_found": 0,      # ended in NO_VIDEOS_FOUND (paste fallback surfaced)
    "missing_transcript": 0,   # ended in MISSING_TRANSCRIPT
}
# Time-to-first-plan, successful runs only (seconds).
_durations: list[float] = []
_DURATIONS_CAP = 1000  # keep memory bounded


def record_plan_run(
    *,
    zero_url: bool,
    sourced: bool,
    outcome: str,            # "success" | "error"
    error_code: str | None,
    duration_s: float,
) -> None:
    with _lock:
        _counters["plans_total"] += 1
        if zero_url:
            _counters["zero_url_sessions"] += 1
            if sourced:
                _counters["auto_sourced_ok"] += 1
        if outcome == "success":
            _counters["plans_succeeded"] += 1
            _durations.append(duration_s)
            if len(_durations) > _DURATIONS_CAP:
                del _durations[0]
        else:
            _counters["plans_failed"] += 1
            if error_code == "NO_VIDEOS_FOUND":
                _counters["no_videos_found"] += 1
            elif error_code == "MISSING_TRANSCRIPT":
                _counters["missing_transcript"] += 1

    _log.info(
        "plan_run %s",
        json.dumps({
            "outcome": outcome,
            "error_code": error_code,
            "zero_url": zero_url,
            "sourced": sourced,
            "duration_s": round(duration_s, 2),
        }),
    )


def _percentile(values: list[float], pct: float) -> float | None:
    if not values:
        return None
    s = sorted(values)
    k = max(0, min(len(s) - 1, round((pct / 100.0) * (len(s) - 1))))
    return round(s[k], 2)


def snapshot() -> dict:
    """Current counters + derived rates, safe to expose at /metrics."""
    with _lock:
        c = dict(_counters)
        durs = list(_durations)

    total = c["plans_total"] or 1  # avoid div/0 in rates
    zero = c["zero_url_sessions"] or 1
    return {
        "counters": c,
        "rates": {
            "zero_url_share": round(c["zero_url_sessions"] / total, 3),
            "auto_source_success_rate": round(c["auto_sourced_ok"] / zero, 3),
            "no_videos_found_rate": round(c["no_videos_found"] / total, 3),
            "success_rate": round(c["plans_succeeded"] / total, 3),
        },
        "time_to_first_plan_s": {
            "count": len(durs),
            "p50": _percentile(durs, 50),
            "p90": _percentile(durs, 90),
        },
    }


def reset() -> None:
    """Test helper — clear all counters."""
    with _lock:
        for k in _counters:
            _counters[k] = 0
        _durations.clear()
