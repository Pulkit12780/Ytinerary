"""Geocode and enrich places via Foursquare Places API v3."""
from __future__ import annotations
import os
import asyncio
import httpx

_FSQ_SEARCH = "https://api.foursquare.com/v3/places/search"
_FSQ_FIELDS = "fsq_id,name,geocodes,categories,rating,hours,description,photos"


def _fsq_headers() -> dict[str, str]:
    return {
        "Authorization": os.getenv("FOURSQUARE_API_KEY", ""),
        "Accept": "application/json",
    }


def _parse_result(r: dict, fallback_name: str) -> dict | None:
    geo = r.get("geocodes", {}).get("main", {})
    lat = geo.get("latitude")
    lng = geo.get("longitude")
    if lat is None or lng is None:
        return None

    cats = r.get("categories", [])
    category = cats[0]["name"] if cats else None

    photos = r.get("photos", [])
    photo_url = None
    if photos:
        p = photos[0]
        photo_url = f"{p.get('prefix', '')}300x300{p.get('suffix', '')}"

    hours_obj = r.get("hours", {})
    hours_str = hours_obj.get("display") or None

    return {
        "name": r.get("name", fallback_name),
        "lat": lat,
        "lng": lng,
        "category": category,
        "rating": r.get("rating"),
        "hours": hours_str,
        "description": r.get("description"),
        "photo_url": photo_url,
        "foursquare_id": r.get("fsq_id"),
    }


async def _geocode_one(
    name: str, destination: str, client: httpx.AsyncClient
) -> dict | None:
    params = {
        "query": name,
        "near": destination,
        "limit": 1,
        "fields": _FSQ_FIELDS,
    }
    try:
        resp = await client.get(
            _FSQ_SEARCH, headers=_fsq_headers(), params=params, timeout=10.0
        )
        resp.raise_for_status()
        results = resp.json().get("results", [])
        if not results:
            return None
        return _parse_result(results[0], name)
    except Exception:
        return None


async def geocode_places(
    places: list[dict],
    destination: str,
) -> tuple[list[dict], list[str]]:
    """
    Deduplicates by name, geocodes each via Foursquare.
    Returns (enriched_places, unresolved_names).
    Each enriched place carries its source_videos list from the input.
    """
    # Deduplicate by lower-case name; merge source_videos on collision
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
        tasks = [_geocode_one(p["name"], destination, client) for p in deduped]
        results = await asyncio.gather(*tasks, return_exceptions=True)

    enriched: list[dict] = []
    unresolved: list[str] = []

    for place_input, geo in zip(deduped, results):
        if isinstance(geo, Exception) or geo is None:
            unresolved.append(place_input["name"])
        else:
            enriched.append({**geo, "source_videos": place_input.get("source_videos", [])})

    return enriched, unresolved


async def geocode_hotel(name: str, destination: str) -> dict | None:
    """Returns {name, lat, lng} or None."""
    async with httpx.AsyncClient() as client:
        result = await _geocode_one(name, destination, client)
    if result:
        return {"name": result["name"], "lat": result["lat"], "lng": result["lng"]}
    return None
