# Travel Planning Engine — Product Spec
*Grilling session, 2026-05-17 | CPO review, 2026-05-17*

## One-line vision
An intelligent travel planning engine that converts YouTube videos and Google Maps links into an optimized, visual day-by-day itinerary displayed on an interactive map — "Google My Maps, but automated and smart."

## Differentiator
**Ytinerary is the only tool that takes YouTube videos you're already watching and turns them into a route-optimized, day-by-day map in under 60 seconds.**

Competitors (Layla, Mindtrip) surface video content as inspiration lists. Ytinerary extracts, geocodes, clusters, and maps the places — the output is an actionable day plan, not a content feed.

---

## The Problem
No product currently:
- Understands creator-generated travel content
- Extracts the places mentioned
- Converts them into a clean visual plan
- Auto-optimizes the route around the traveler's hotel
- Displays it all on a trusted, interactive map

---

## User Types

### Type 1 — Destination known, no idea where to go
- Input: YouTube video URLs
- System extracts places, enriches with Foursquare data
- Output: Visual clustered itinerary on map

### Type 2 — Has some places shortlisted
- Input: Individual Google Maps place page links
- System enriches and clusters those places
- Output: Same visual itinerary on map

### Type 3 — Wants more detail
- Uses the app's basic info (rating, hours, description)
- Clicks through to Google Maps / Foursquare for depth
- The app is the organization layer, not the replacement for Maps

**Primary user: Pre-trip researcher** — sitting at home before the trip, multiple browser tabs open, high intent, high tolerance for a multi-step workflow.

---

## v1 Input Form

| Field | Required? | Notes |
|---|---|---|
| Destination (city / region / country) | ✅ Required | |
| YouTube video URLs | ✅ Required (1 or more) | UI accepts multiple URLs; each is processed by the same pipeline and results are merged |
| Google Maps place page links | Optional | |
| Hotel name / address | Optional | Hotel pin shown on map only if provided |
| Travel dates | Optional | If provided, sets k directly in k-means (k = num_days) |

**Minimum viable submission:** Location + at least one YouTube URL.

---

## Core Architecture Decisions

### YouTube Extraction
- Fetch **transcript + video description** per URL (transcript-api, no YouTube Data API key needed)
- Feed each to **Claude Haiku** with a sentiment-aware prompt
- Extract places as structured JSON: `{name, sentiment, source_video_title, source_video_url}`
- **Multiple URLs:** run extraction in parallel per URL, merge results before enrichment
- Single LLM call per video — accept ~20% noise, sidebar lets users remove bad places
- Negative-sentiment places are **silently filtered out** before enrichment (not surfaced in UI)

**Transcript-api reliability:**
- `youtube-transcript-api` scrapes YouTube internal endpoints and can break without notice
- Wrap every transcript fetch in `try/except`; on failure return clean error (already in failure table)
- Add `yt-dlp` as a subtitle fallback if transcript-api fails
- Log every transcript failure with video URL — track real success rate from day one

**In-memory caching (same YouTube URL):**
- Cache `video_url → extracted_places_json` in a Python dict (or `functools.lru_cache`) per server process
- On cache hit: skip transcript fetch + Haiku call entirely
- Rationale: popular travel vlogs will be submitted by multiple users; re-processing is pure waste

### Place Enrichment & Geocoding

**Name → Foursquare ID matching (explicit algorithm):**
```
For each extracted place name:
  1. Derive destination_center (lat/lng) and destination_radius from user's destination field:
       city      → 30km radius
       region    → 150km radius
       country   → 400km radius
  2. Call Foursquare /places/search?query={name}&ll={destination_center}&radius={destination_radius}
  3. Take the highest-relevance result within radius
  4. If no result or relevance below threshold → mark as "Unresolved", skip enrichment
```

**Why this matters:** LLM-extracted names are colloquial ("the pink palace", "Amber Fort" vs "Amer Fort"). Bounding the search to the destination's radius and taking the top relevance result handles most variants automatically — same mechanism as deduplication by Foursquare place ID.

**Post-match enrichment:**
- Call `/places/{fsq_id}` for: coordinates, category, rating, opening hours, 1-line description, photo
- Deduplication: if two extracted places resolve to the same Foursquare place ID, merge into one (tracks all source videos)
- Foursquare call budget: ~40 calls/itinerary (1 search + 1 detail per place × ~20 places). Free tier = 100k/month → safe for v1 PMF target

### Map Display
- **Leaflet.js + OpenStreetMap tiles** — fully free, no API key
- No Google Maps JS API — eliminates the largest billing item

### Clustering
- **k-means** on lat/lng coordinates (replaces DBSCAN)
- **Claude Haiku** labels each cluster meaningfully (e.g. "Day 1: Old City & Bazaars")
- **Max 5 places per day** — overflow goes to "More to Explore" section

**Why k-means over DBSCAN:**
DBSCAN requires an epsilon (ε) distance parameter that has no single correct value across destinations — ε that works for Paris (5km neighborhoods) produces 25 single-point clusters for a Rajasthan road trip (400km spread). DBSCAN's "auto-find cluster count" advantage was already being overridden by the fallback rules in the previous spec. k-means is deterministic, simpler, and the cluster count formula below replaces all fallback logic.

**k value formula:**
```
k = num_days                              if travel dates provided
k = min(5, ceil(num_places / 5))          if no dates provided
```
- num_places = count after enrichment + deduplication
- Max k = 5 (prevents single-place days on small itineraries)

### Day Labeling
- Travel dates provided → label as "Tuesday, May 20"
- No dates → label as "Day 1, Day 2, Day 3"

---

## LangGraph Pipeline

```
START
  → fetch_transcripts_and_descriptions    (parallel per URL; yt-dlp fallback if transcript-api fails)
  → check_extraction_cache                (return cached result if URL seen before)
  → extract_places_with_sentiment         (Claude Haiku, parallel per video)
  → write_extraction_cache                (store result keyed on video URL)
  → filter_negative_sentiment             (silent drop)
  → merge_all_places
  → fuzzy_match_to_foursquare             (search by name + destination_center + radius, parallel per place)
  → enrich_matched_places                 (Foursquare /places/{fsq_id}, parallel per place)
  → deduplicate_by_foursquare_id
  → cluster_geographically                (k-means, k from formula)
  → label_clusters                        (Claude Haiku)
END → return structured itinerary JSON
```

**SSE ↔ Pipeline wiring (asyncio.Queue pattern):**
```python
# Per-request queue created before pipeline starts
queue = asyncio.Queue()

# Pipeline nodes put progress strings to queue at key steps
await queue.put("Fetching video transcripts...")
await queue.put(f"Extracting places from {video_title}...")
await queue.put(f"Enriching {n} places with location data...")
await queue.put("Building your day-by-day plan...")
await queue.put("__done__")  # sentinel

# FastAPI SSE endpoint reads from queue
async def event_generator(queue):
    while True:
        msg = await queue.get()
        if msg == "__done__": break
        yield f"data: {msg}\n\n"
```
- Pipeline runs as `asyncio.create_task()` — continues if client disconnects
- Results discarded on disconnect (acceptable for v1; no database to save to)

**Progress events streamed to frontend:**
1. "Fetching video transcripts..."
2. "Extracting places from [Video Title]..."  *(one event per video)*
3. "Enriching [N] places with location data..."
4. "Building your day-by-day plan..."

---

## Output UI

### Loading State (required — pipeline takes 30–90s)
- Full-screen overlay shown immediately on form submit
- Animated progress bar with step label updating in real time:
  - "Fetching video transcripts..."
  - "Extracting places from [Video Title]..."
  - "Enriching [N] places with location data..."
  - "Building your day-by-day plan..."
- If a video has no transcript: inline warning below that URL, continue processing remaining URLs
- Pipeline errors surface as a non-blocking banner; partial results are shown if available

### Map (Leaflet)
- Day-colored pins (Day 1 = blue, Day 2 = green, etc.)
- Hotel pin (distinct marker, always visible) — only rendered if hotel was provided
- Clicking a pin → tooltip with place name, category, and rating
- Days light up when selected in sidebar

### Sidebar
- Collapsible, always accessible alongside the map
- Organized by day clusters
- **"More to Explore"** section at bottom — overflow places beyond the 5/day cap
- Negative-sentiment places are not shown anywhere in v1 (silently filtered at pipeline stage)

### Place Cards (minimalistic by default)
**Collapsed view:**
```
Amber Fort                    [Day 1]
Temple / Historic Site  ⭐ 4.7
📹 Mumbiker Nikhil's Jaipur Vlog
```

**Expanded view (on click):**
- Photo
- Opening hours
- Full description
- Source video link (opens YouTube)
- Remove button

### Provenance
- Every place card shows which YouTube video it came from
- If a place appears in multiple videos → all sources listed in the expanded card view
- Pin tooltips show place name, category, and rating (source video attribution is in the sidebar card, not the map tooltip)

---

## Sharing
- **URL encodes inputs only** — YouTube URLs + destination + hotel + dates (not the itinerary output)
- On shared-link load: re-run the pipeline (30–90s wait; acceptable for v1)
- No database required for v1
- Anyone with the link sees the same map (output may vary slightly if Foursquare data updates)

**Why not encode the full itinerary:**
A 20-place itinerary with names, coordinates, photos, and source URLs is 5–15KB raw. Even compressed, this routinely exceeds the 2,048-character URL limit enforced by many servers and older browsers. Encoding only the inputs (< 500 chars typically) is safe at any itinerary size.

- Upgrade to short IDs + database in v2

---

## Failure Handling
| Failure | User-facing message |
|---|---|
| No transcript available | "This video doesn't have captions. Try a different video." |
| Zero places extracted | "We coul
dn't find specific places in this video. Try a video with more destination coverage." |
| Foursquare geocoding fails | Place appears in sidebar as "Unresolved" — user can remove |

---

## Tech Stack

| Layer | Choice | Reason |
|---|---|---|
| Backend | Python + FastAPI | Fits existing skills, clean REST API |
| Pipeline | LangGraph | Multi-step agent graph, easy to debug |
| LLM (extraction + clustering) | Claude Haiku | Fast, cheap, good JSON output |
| Streaming | FastAPI SSE + asyncio.Queue | Push progress events to frontend during 30–90s pipeline |
| Transcript | youtube-transcript-api + yt-dlp fallback | yt-dlp covers videos where transcript-api fails |
| Clustering | scikit-learn k-means | Deterministic, no ε tuning, predictable cluster count |
| Place data | Foursquare Places API | Free tier, 100k calls/month; ~40 calls/itinerary |
| Map tiles | Leaflet.js + OpenStreetMap | Fully free, no API key (switch to Carto in v2 for reliability) |
| Frontend | React + Leaflet (react-leaflet) | Best Leaflet ecosystem support |
| Config | python-dotenv (.env file) | `ANTHROPIC_API_KEY`, `FOURSQUARE_API_KEY` — never hardcoded |
| Caching | In-memory dict (server process) | Skip re-processing same YouTube URL |
| Database | None for v1 | Sessions only, URL input encoding for sharing |

---

## Monetization
- **Free for v1** — validate product-market fit first
- **Natural v2 path:** Affiliate links to MakeMyTrip / Booking.com for hotel and activity bookings (revenue share per conversion — fits organically since hotel is already in the flow)

---

## Build Order (v1)

**0. CLI smoke test (before any UI work)**
   - Script: `python pipeline.py --url <youtube_url> --destination "Jaipur, India"`
   - Output: itinerary JSON printed to terminal
   - Validates the entire backend (transcript → extraction → Foursquare matching → k-means → labeling) before building a frontend around potentially broken assumptions
   - Exit criteria: at least 3 different destination + video combos produce sensible JSON

1. Input form (location, 1+ YouTube URLs, optional hotel/dates)

2. Full LangGraph pipeline + SSE streaming *(steps 2+3 from old order are one milestone — can't validate extraction without seeing geocoded results)*
   - Parallel transcript fetch (transcript-api + yt-dlp fallback)
   - In-memory cache check per URL
   - Claude Haiku extraction per video (parallel)
   - Foursquare name-matching (destination_center + radius strategy)
   - Foursquare enrichment + deduplication
   - FastAPI SSE endpoint with asyncio.Queue wiring
   - Frontend loading state consuming SSE events

3. k-means clustering + Claude Haiku cluster labeling

4. Leaflet map with day-colored pins + hotel pin (if provided)

5. Sidebar with place cards (source video attribution), "More to Explore" section

6. URL input encoding for sharing (encode inputs only, re-run pipeline on load)

---

## Success Metric (v1 → v2 trigger)
v1 is done when: **50 itineraries successfully generated** (place-extraction success rate > 70%) AND **at least 10 users share their URL with someone else.** The share signal is the strongest PMF indicator — it means the output was good enough to show another person.

---

## Decisions Explicitly Deferred to v2
- Filter places by video source in sidebar
- Negative sentiment "Places to Skip" section with creator reasoning
- Short-link sharing with database persistence
- Affiliate/hotel booking integration
- Vision/frame extraction from video (expensive, high-accuracy moat)
- User accounts and saved itineraries
- Mobile-first / on-trip navigation mode
