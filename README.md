# Ytinerary

Turn travel intent — and optionally YouTube travel videos — into a visual, route-optimized, day-by-day itinerary on an interactive map. You tell it where you're going and what kind of trip it is; an AI travel curator builds the plan in under a minute.

> "Google My Maps, but automated and smart."

## How it works

1. **Intent first.** You enter a destination, pick a trip type (e.g. balanced, family, romantic, adventure), and optionally add notes. YouTube URLs are optional flavor, not required.
2. **Pipeline (FastAPI + LangGraph).** `source_videos → fetch_transcripts → extract_places → augment_places → geocode_places → judge_and_plan`. The **augmenter** acts as the travel-expert curator (the primary source of places); videos add flavor when present. The **judge** grounds an LLM plan against real geodistances and builds tight, ordered, meal-interleaved days.
3. **Results.** A Leaflet map with day-colored pins plus a day-by-day sidebar. Output streams to the browser over SSE.

## Stack

- **Frontend:** static `index.html` (landing + form + loading overlay) and `results.html` (Leaflet map + sidebar). Vanilla JS, no build step.
- **Backend:** Python 3.12, FastAPI, LangGraph, Pydantic.
- **LLM:** OpenAI `gpt-4o-mini` (extraction, curation, planning).
- **Geocoding:** OpenTripMap (optional key) with free Nominatim fallback.
- **Maps:** Leaflet.js + OpenStreetMap tiles (no key).
- **Transcripts:** `youtube-transcript-api` with `yt-dlp` fallback. *(Note: YouTube IP-blocks server-side transcript fetching — see `memory`/docs; videos are non-fatal by design.)*
- **Video sourcing:** YouTube Data API (`YOUTUBE_API_KEY`) when set, otherwise a curated stub.

## Running locally

This Mac requires Anaconda's ARM Python 3.12 (system Python is x86_64 and fails on some deps).

```bash
# Backend (from project root)
/opt/anaconda3/bin/pip install -r backend/requirements.txt
/opt/anaconda3/bin/uvicorn backend.main:app --reload
```

Create `backend/.env` from `backend/.env.example` and set at least `OPENAI_API_KEY` (optional: `OPENTRIPMAP_API_KEY`, `YOUTUBE_API_KEY`).

```bash
# Frontend — serve the static files, then open index.html
python3 -m http.server 5500   # then visit http://localhost:5500/index.html
```

`results.html?demo=1` renders mock Jaipur data with no backend call.

## Tests

```bash
/opt/anaconda3/bin/python3.12 -m pytest backend/tests/
```

## Endpoints

- `POST /plan` / `POST /plan/stream` — generate an itinerary (SSE for streaming).
- `GET /health` — liveness + whether keys are configured.
- `GET /metrics` — in-process run counters and rates.

## Docs

- [`PRD-Ytinerary.md`](PRD-Ytinerary.md) — product requirements
- [`travel-planner-spec.md`](travel-planner-spec.md) — original product spec / grilling session
- [`docs/product/brief-intent-and-autosourcing.md`](docs/product/brief-intent-and-autosourcing.md) + [`docs/eng/dev-plan-intent-and-autosourcing.md`](docs/eng/dev-plan-intent-and-autosourcing.md) — Trip Intent & Auto-Sourcing (Epic 4, shipped)
- [`docs/archive/`](docs/archive/) — superseded design specs & early dev plan (historical only)

The live visual design is implemented directly in `index.html` and `results.html` (warm editorial direction: Fraunces + Inter, clay accent, warm paper).
