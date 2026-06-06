"""Geocode and enrich places via OpenTripMap API, with Nominatim fallback."""
from __future__ import annotations
import os
import asyncio
import httpx

_OTM_BASE = "https://api.opentripmap.com/0.1/en"
_NOMINATIM_SEARCH = "https://nominatim.openstreetmap.org/search"
_NOMINATIM_UA = "Ytinerary/1.0 (travel itinerary app)"

_otm_auth_failed = False
_dest_cache: dict[str, tuple[float, float]] = {}


def _otm_key() -> str:
    return os.getenv("OPENTRIPMAP_API_KEY", "")


async def _geocode_city(destination: str, client: httpx.AsyncClient) -> tuple[float, float] | None:
    if destination in _dest_cache:
        return _dest_cache[destination]

    try:
        resp = await client.get(
            f"{_OTM_BASE}/places/geoname",
            params={"name": destination, "apikey": _otm_key()},
            timeout=10.0,
        )
        if resp.status_code == 200:
            data = resp.json()
            lat, lon = data.get("lat"), data.get("lon")
            if lat and lon:
                coords = (float(lat), float(lon))
                _dest_cache[destination] = coords
                return coords
    except Exception:
        pass

    try:
        resp = await client.get(
            _NOMINATIM_SEARCH,
            headers={"User-Agent": _NOMINATIM_UA, "Accept-Language": "en"},
            params={"q": destination, "format": "json", "limit": 1},
            timeout=10.0,
        )
        resp.raise_for_status()
        results = resp.json()
        if results:
            coords = (float(results[0]["lat"]), float(results[0]["lon"]))
            _dest_cache[destination] = coords
            return coords
    except Exception:
        pass

    return None


async def _geocode_one_otm(
    name: str,
    dest_coords: tuple[float, float],
    client: httpx.AsyncClient,
) -> dict | None:
    global _otm_auth_failed
    if _otm_auth_failed:
        return None

    lat, lon = dest_coords
    try:
        resp = await client.get(
            f"{_OTM_BASE}/places/radius",
            params={
                "radius": 20000,
                "lon": lon,
                "lat": lat,
                "name": name,
                "limit": 1,
                "apikey": _otm_key(),
            },
            timeout=10.0,
        )
        if resp.status_code == 401:
            _otm_auth_failed = True
            return None
        resp.raise_for_status()
        features = resp.json().get("features", [])
        if not features:
            return None

        feat = features[0]
        props = feat.get("properties", {})
        coords = feat.get("geometry", {}).get("coordinates", [])
        if not coords or len(coords) < 2:
            return None
        place_lon, place_lat = coords[0], coords[1]
        xid = props.get("xid")

        detail: dict = {}
        if xid:
            det_resp = await client.get(
                f"{_OTM_BASE}/places/xid/{xid}",
                params={"apikey": _otm_key()},
                timeout=10.0,
            )
            if det_resp.status_code == 200:
                detail = det_resp.json()

        kinds = detail.get("kinds") or props.get("kinds", "")
        category = kinds.split(",")[0].replace("_", " ").title() if kinds else None
        wiki = detail.get("wikipedia_extracts", {}).get("text")
        image = detail.get("image")

        return {
            "name": detail.get("name") or props.get("name", name),
            "lat": place_lat,
            "lng": place_lon,
            "category": category,
            "rating": props.get("rate"),
            "hours": None,
            "description": wiki,
            "photo_url": image,
            "place_id": xid,
        }
    except Exception:
        return None


async def _geocode_one_nominatim(
    name: str, destination: str, client: httpx.AsyncClient
) -> dict | None:
    """Fallback: Nominatim (OpenStreetMap). Free, no key needed, 1 req/sec limit."""
    params = {
        "q": f"{name}, {destination}",
        "format": "json",
        "limit": 1,
        "addressdetails": 0,
    }
    try:
        resp = await client.get(
            _NOMINATIM_SEARCH,
            headers={"User-Agent": _NOMINATIM_UA, "Accept-Language": "en"},
            params=params,
            timeout=10.0,
        )
        resp.raise_for_status()
        results = resp.json()
        if not results:
            return None
        r = results[0]
        lat = float(r.get("lat", 0) or 0)
        lng = float(r.get("lon", 0) or 0)
        if not lat and not lng:
            return None
        return {
            "name": name,
            "lat": lat,
            "lng": lng,
            "category": r.get("type", "").replace("_", " ").title() or None,
            "rating": None,
            "hours": None,
            "description": None,
            "photo_url": None,
            "place_id": None,
        }
    except Exception:
        return None


async def geocode_places(
    places: list[dict],
    destination: str,
) -> tuple[list[dict], list[str]]:
    """
    Deduplicates by name, geocodes each via OpenTripMap (parallel) with Nominatim fallback
    (sequential, 1 req/sec). Returns (enriched_places, unresolved_names).
    """
    seen: dict[str, dict] = {}
    for p in places:
        key = p["name"].strip().lower()
        if key not in seen:
            seen[key] = dict(p)
        else:
            existing_svs = seen[key].get("source_videos", [])
            new_svs = p.get("source_videos", [])
            merged = existing_svs + [sv for sv in new_svs if sv not in existing_svs]
            seen[key]["source_videos"] = merged

    deduped = list(seen.values())

    async with httpx.AsyncClient() as client:
        dest_coords = await _geocode_city(destination, client)

        if dest_coords is not None:
            otm_tasks = [_geocode_one_otm(p["name"], dest_coords, client) for p in deduped]
            otm_results = await asyncio.gather(*otm_tasks, return_exceptions=True)
        else:
            otm_results = [None] * len(deduped)

        final_results: list[dict | None] = []
        for place_input, geo in zip(deduped, otm_results):
            if isinstance(geo, Exception) or geo is None:
                nom = await _geocode_one_nominatim(place_input["name"], destination, client)
                final_results.append(nom)
                await asyncio.sleep(0.25)
            else:
                final_results.append(geo)

    enriched: list[dict] = []
    unresolved: list[str] = []

    for place_input, geo in zip(deduped, final_results):
        if geo is None:
            unresolved.append(place_input["name"])
        else:
            enriched.append({**geo, "source_videos": place_input.get("source_videos", [])})

    return enriched, unresolved


async def geocode_hotel(name: str, destination: str) -> dict | None:
    """Returns {name, lat, lng} or None."""
    async with httpx.AsyncClient() as client:
        dest_coords = await _geocode_city(destination, client)
        if dest_coords:
            result = await _geocode_one_otm(name, dest_coords, client)
            if result:
                return {"name": result["name"], "lat": result["lat"], "lng": result["lng"]}
        result = await _geocode_one_nominatim(name, destination, client)
    if result:
        return {"name": result["name"], "lat": result["lat"], "lng": result["lng"]}
    return None
