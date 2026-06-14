import time
from threading import Lock

# Per-URL transcript cache — no expiry (a video's transcript doesn't change).
_store: dict[str, dict] = {}
_lock = Lock()

# Namespaced cache with TTL — used to conserve YouTube search quota (B3): one
# search/day per (destination, trip_type). Values are arbitrary objects.
_ttl_store: dict[str, tuple[float, object]] = {}
_ttl_lock = Lock()


def get(url: str) -> dict | None:
    with _lock:
        return _store.get(url)


def set(url: str, data: dict) -> None:
    with _lock:
        _store[url] = data


def get_ttl(key: str) -> object | None:
    """Return the cached value for `key` if present and unexpired, else None."""
    now = time.time()
    with _ttl_lock:
        entry = _ttl_store.get(key)
        if entry is None:
            return None
        expires_at, value = entry
        if expires_at < now:
            _ttl_store.pop(key, None)
            return None
        return value


def set_ttl(key: str, value: object, ttl_seconds: float) -> None:
    """Cache `value` under `key` for `ttl_seconds`."""
    with _ttl_lock:
        _ttl_store[key] = (time.time() + ttl_seconds, value)


def clear() -> None:
    with _lock:
        _store.clear()
    with _ttl_lock:
        _ttl_store.clear()
