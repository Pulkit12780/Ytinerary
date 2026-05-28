from threading import Lock

_store: dict[str, dict] = {}
_lock = Lock()


def get(url: str) -> dict | None:
    with _lock:
        return _store.get(url)


def set(url: str, data: dict) -> None:
    with _lock:
        _store[url] = data


def clear() -> None:
    with _lock:
        _store.clear()
