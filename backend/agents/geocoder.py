"""Geocode and enrich places via OpenTripMap API, with Nominatim fallback."""
from __future__ import annotations
import os
import re
import math
import asyncio
import httpx

_OTM_BASE = "https://api.opentripmap.com/0.1/en"
_NOMINATIM_SEARCH = "https://nominatim.openstreetmap.org/search"
_NOMINATIM_UA = "Ytinerary/1.0 (travel itinerary app)"

_otm_auth_failed = False
_dest_cache: dict[str, tuple[float, float]] = {}

# Geocoder "type"/"kinds" tokens that mean "this is NOT a place a traveler visits".
# These are exactly what produced "Administrative office" / "Ports" in the UI: the
# provider's raw classification was being shown as the place category. We now never
# *display* these, and — when a place has no trustworthy curated category of its own —
# treat a match that resolves only to one of these as a bad geocode (dropped).
_NON_TOURIST_TYPES: frozenset[str] = frozenset({
    "administrative", "administrative_area", "boundary", "postcode", "post_office",
    "government", "townhall", "town_hall", "courthouse", "office", "commercial",
    "industrial", "industrial_facilities", "construction", "company", "factory",
    "port", "ports", "harbour", "harbor", "ferry_terminal", "dock", "marina",
    "station", "bus_station", "bus_stop", "platform", "halt", "stop_position",
    "aerodrome", "airport", "terminal", "fuel", "parking", "parking_space",
    "toll_booth", "weighbridge", "depot", "yard", "warehouse", "wholesale",
    "hospital", "clinic", "doctors", "pharmacy", "police", "fire_station",
    "school", "university", "college", "kindergarten", "bank", "atm",
    "residential", "house", "apartments", "neighbourhood_block", "suburb_boundary",
    "locality", "hamlet", "isolated_dwelling", "unclassified", "yes",
})


def _parse_otm_rate(rate) -> int | None:
    """OTM popularity 'rate' → int 0-7. It arrives as 0-3 or strings like '3h'
    (h = has a Wikipedia article). Returns None when absent/unparseable."""
    if rate is None:
        return None
    try:
        return int(str(rate).rstrip("h") or 0)
    except (ValueError, TypeError):
        return None


def _clean_geo_category(geo_type: str | None) -> str | None:
    """Normalize a provider type/kinds token to a display label, or None if it's a
    non-tourist classification we should never surface as a place category."""
    if not geo_type:
        return None
    token = geo_type.strip().lower().replace(" ", "_")
    if token in _NON_TOURIST_TYPES:
        return None
    return geo_type.replace("_", " ").title()


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
        # Raw first kind — `geocode_places` decides whether it's a usable category.
        geo_type = kinds.split(",")[0] if kinds else None
        wiki = detail.get("wikipedia_extracts", {}).get("text")
        image = detail.get("image")

        return {
            "name": detail.get("name") or props.get("name", name),
            "lat": place_lat,
            "lng": place_lon,
            "geo_type": geo_type,
            # OTM "rate" is a 0-7 tourist-importance index (sometimes a string like
            # "3h"). Not a star rating — we use it only as a popularity hint, never
            # surface it as one.
            "geo_rate": _parse_otm_rate(props.get("rate") or detail.get("rate")),
            "rating": None,
            "hours": None,
            "description": wiki,
            "photo_url": image,
            "place_id": xid,
        }
    except Exception:
        return None


def _viewbox(dest_coords: tuple[float, float], half_deg: float = 0.5) -> str:
    """Nominatim viewbox (lon_min,lat_min,lon_max,lat_max) around the destination —
    ~55km half-side, enough to cover a city and its day-trip radius."""
    lat, lon = dest_coords
    return f"{lon - half_deg},{lat - half_deg},{lon + half_deg},{lat + half_deg}"


async def _nominatim_search(
    client: httpx.AsyncClient, params: dict
) -> list | None:
    try:
        resp = await client.get(
            _NOMINATIM_SEARCH,
            headers={"User-Agent": _NOMINATIM_UA, "Accept-Language": "en"},
            params={"format": "json", "limit": 1, "addressdetails": 0, **params},
            timeout=10.0,
        )
        resp.raise_for_status()
        return resp.json()
    except Exception:
        return None


async def _geocode_one_nominatim(
    name: str,
    destination: str,
    client: httpx.AsyncClient,
    dest_coords: tuple[float, float] | None = None,
) -> dict | None:
    """Fallback: Nominatim (OpenStreetMap). Free, no key needed, 1 req/sec limit.

    Tries "<name>, <destination>" first, then — if that's empty and we know the
    destination's coordinates — the bare name bounded to a viewbox around the city.
    The second pass is what saves awkwardly-typed destinations like "Ireland, Dublin",
    where the comma order ("<name>, Ireland, Dublin") confuses Nominatim's parser.
    """
    results = await _nominatim_search(client, {"q": f"{name}, {destination}"})
    if not results and dest_coords is not None:
        results = await _nominatim_search(
            client, {"q": name, "viewbox": _viewbox(dest_coords), "bounded": 1}
        )
    if not results:
        return None
    try:
        r = results[0]
        lat = float(r.get("lat", 0) or 0)
        lng = float(r.get("lon", 0) or 0)
        if not lat and not lng:
            return None
        return {
            "name": name,
            "lat": lat,
            "lng": lng,
            # Raw OSM type (e.g. "administrative", "port", "attraction") — kept raw so
            # `geocode_places` can reject non-tourist matches instead of displaying them.
            "geo_type": r.get("type") or r.get("class"),
            "geo_rate": None,
            "rating": None,
            "hours": None,
            "description": None,
            "photo_url": None,
            "place_id": None,
        }
    except Exception:
        return None


# Importance ranking so a merge keeps the better label ("Sigiriya Rock" over "Sigiriya").
_IMPORTANCE_ORDER = {"must_see": 0, "recommended": 1, "hidden_gem": 2, "optional": 3}
_GENERIC_TOKENS = frozenset({
    "the", "of", "fort", "fortress", "temple", "palace", "park", "beach", "lake",
    "national", "garden", "gardens", "old", "city", "town", "rock", "hill", "point",
})


def _name_tokens(name: str) -> set[str]:
    toks = re.findall(r"[a-z0-9]+", (name or "").lower())
    sig = {t for t in toks if t not in _GENERIC_TOKENS}
    return sig or set(toks)  # fall back to all tokens if everything was generic


def _same_place(a: dict, b: dict) -> bool:
    """Two geocoded entries that are really the same spot — so we never list a place
    on multiple days (or twice in one) under slightly different names."""
    d = _meters_between((a["lat"], a["lng"]), (b["lat"], b["lng"]))
    if d <= 120:                       # within ~120m → same location, merge outright
        return True
    if d > 400:                        # clearly different places
        return False
    ta, tb = _name_tokens(a["name"]), _name_tokens(b["name"])
    if not ta or not tb:
        return False
    overlap = len(ta & tb) / min(len(ta), len(tb))
    return overlap >= 0.5              # nearby AND name overlap → same place


def _meters_between(a: tuple[float, float], b: tuple[float, float]) -> float:
    lat1, lng1, lat2, lng2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    dlat, dlng = lat2 - lat1, lng2 - lng1
    h = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlng / 2) ** 2
    return 2 * 6371000.0 * math.asin(math.sqrt(h))


def _merge_near_duplicates(enriched: list[dict]) -> list[dict]:
    """Collapse entries that resolve to the same physical place. Keeps the richer record
    (curated source / stronger importance / has description) and unions source_videos."""
    kept: list[dict] = []
    for p in enriched:
        match = next((k for k in kept if _same_place(k, p)), None)
        if match is None:
            kept.append(p)
            continue
        # Decide which record is the keeper, then fold the other's signal into it.
        better, worse = (p, match) if _richer(p, match) else (match, p)
        if better is not match:
            kept[kept.index(match)] = better
        svs = better.get("source_videos", []) + [
            sv for sv in worse.get("source_videos", []) if sv not in better.get("source_videos", [])
        ]
        better["source_videos"] = svs
        for k in ("description", "photo_url", "importance", "why", "area",
                  "budget_tier", "meal_type", "duration_hrs"):
            if not better.get(k) and worse.get(k):
                better[k] = worse[k]
        if better.get("source") != "video" or worse.get("source") != "video":
            better["source"] = "video" if "video" in (better.get("source"), worse.get("source")) else better.get("source")
    return kept


def _richer(a: dict, b: dict) -> bool:
    """True if a is the better record to keep over b."""
    ia = _IMPORTANCE_ORDER.get(a.get("importance") or "optional", 3)
    ib = _IMPORTANCE_ORDER.get(b.get("importance") or "optional", 3)
    if ia != ib:
        return ia < ib
    # Prefer the one with a description, then the longer (more specific) name.
    if bool(a.get("description")) != bool(b.get("description")):
        return bool(a.get("description"))
    return len(a.get("name", "")) >= len(b.get("name", ""))


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
                nom = await _geocode_one_nominatim(
                    place_input["name"], destination, client, dest_coords
                )
                final_results.append(nom)
                await asyncio.sleep(1.1)  # Nominatim usage policy: max 1 req/sec
            else:
                final_results.append(geo)

    enriched: list[dict] = []
    unresolved: list[str] = []

    # Curated tags we want to preserve verbatim across geocoding (the geocoder only
    # contributes coordinates + optional photo/description, never these).
    _carry = ("importance", "why", "audience", "vibe", "budget_tier",
              "area", "duration_hrs", "meal_type")

    for place_input, geo in zip(deduped, final_results):
        if geo is None:
            unresolved.append(place_input["name"])
            continue

        in_cat = place_input.get("category")
        geo_cat = _clean_geo_category(geo.get("geo_type"))

        # The curated/extracted category is authoritative — it's clean controlled
        # vocab the planner relies on. The provider's classification is only a
        # fallback, and only when it's tourist-relevant (`_clean_geo_category`
        # returns None for admin/transport/etc.). This is what stops "Administrative
        # office" / "Ports" from ever reaching the UI.
        category = in_cat or geo_cat

        # Drop a match that resolved *only* to a non-tourist feature and that we have
        # no trusted category for: it's almost certainly the wrong pin (an admin
        # boundary or transport node), not the place the traveler meant.
        if category is None and geo.get("geo_type") and geo_cat is None:
            unresolved.append(place_input["name"])
            continue

        # OTM popularity (0-7) backfills an importance hint when the curator didn't
        # set one, so even video/maps-link places get prioritized sensibly.
        importance = place_input.get("importance")
        if not importance and isinstance(geo.get("geo_rate"), int):
            importance = "must_see" if geo["geo_rate"] >= 5 else (
                "recommended" if geo["geo_rate"] >= 3 else "optional")

        merged = {
            "name": geo["name"],
            "lat": geo["lat"],
            "lng": geo["lng"],
            "category": category,
            "rating": geo.get("rating"),
            "hours": geo.get("hours"),
            "description": geo.get("description") or place_input.get("description"),
            "photo_url": geo.get("photo_url"),
            "place_id": geo.get("place_id"),
            "importance": importance,
            "source": place_input.get("source", "video"),
            "source_videos": place_input.get("source_videos", []),
        }
        for k in _carry:
            if place_input.get(k) is not None and k not in ("importance",):
                merged[k] = place_input[k]
        enriched.append(merged)

    # Final pass: collapse entries that geocoded to the same physical spot under
    # different names, so a place can never appear on two days (or twice in one).
    enriched = _merge_near_duplicates(enriched)

    return enriched, unresolved


async def geocode_hotel(name: str, destination: str) -> dict | None:
    """Returns {name, lat, lng} or None."""
    async with httpx.AsyncClient() as client:
        dest_coords = await _geocode_city(destination, client)
        if dest_coords:
            result = await _geocode_one_otm(name, dest_coords, client)
            if result:
                return {"name": result["name"], "lat": result["lat"], "lng": result["lng"]}
        result = await _geocode_one_nominatim(name, destination, client, dest_coords)
    if result:
        return {"name": result["name"], "lat": result["lat"], "lng": result["lng"]}
    return None
