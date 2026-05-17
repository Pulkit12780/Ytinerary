# PRD — Ytinerary
*Created: 2026-05-17 | Based on: travel-planner-spec.md (CPO review, 2026-05-17)*

---

## 1. Summary

Ytinerary is an intelligent travel planning engine that turns YouTube travel videos and Google Maps links into a visual, route-optimized, day-by-day itinerary displayed on an interactive map. It is the only tool that takes the videos travelers are already watching and converts them into an actionable trip plan — not a content feed — in under 60 seconds. Version 1 targets pre-trip researchers and validates product-market fit before any monetization.

---

## 2. Contacts

| Name | Role | Notes |
|---|---|---|
| Pulkit | Product Owner / Builder | Sole decision-maker for v1 scope and build order |
| CPO Review | Product Advisor | Reviewed spec on 2026-05-17 (grilling session) |
| TBD | Early Beta Users | Target: 50 itineraries generated to unlock v2 |

---

## 3. Background

### Context

Travelers today plan trips by watching YouTube vlogs, saving Google Maps pins, and opening dozens of browser tabs. There is no tool that bridges the gap between the content they consume and a usable plan. Existing AI travel tools (Layla, Mindtrip) surface video content as inspiration lists — they do not extract specific places, geocode them, or build a route.

### Why now?

Three things became available at the same time:
1. **Transcript APIs** (`youtube-transcript-api`, `yt-dlp`) allow scraping YouTube subtitles without an official API key
2. **Fast, cheap LLMs** (Claude Haiku) can extract structured place data from unstructured video transcripts at near-zero cost
3. **Free mapping layers** (Leaflet.js + OpenStreetMap, Foursquare free tier) eliminate the largest variable cost in map-based products

Together these make a zero-infrastructure-cost v1 feasible. None of this was true 18 months ago.

### What has changed?

Creator-produced travel content has become the dominant trip-planning research channel — YouTube travel vlogs routinely reach millions of views per destination. The information is inside that content but trapped in an unstructured format. Ytinerary extracts, geocodes, clusters, and maps it.

---

## 4. Objective

### Goal

Enable any traveler to go from "I watched a travel video" to "I have a day-by-day map plan" in under 60 seconds, without copying anything manually.

### Why it matters

- **For users:** Replaces hours of tab management and manual pin-saving with a single URL submission
- **For the product:** Establishes a novel, defensible input moat (YouTube → structured itinerary) before larger players catch up
- **For the business:** Proves PMF before investing in infrastructure, auth, or monetization

### Key Results (v1 success threshold)

| # | Result | How measured |
|---|---|---|
| KR1 | 50 itineraries successfully generated | Server-side count of pipeline completions |
| KR2 | Place-extraction success rate > 70% | (places geocoded / places extracted) per itinerary |
| KR3 | ≥ 10 users share their URL with someone else | Shared-URL load events (URL parameter present on page load) |

KR3 is the primary PMF signal. If someone shows their output to another person, the output was good enough to be worth showing.

---

## 5. Market Segment(s)

### Primary segment — Pre-trip researcher

**Who:** A traveler who has chosen a destination but does not yet know specifically where to go. They are at home, not on the trip. They have already watched one or more YouTube travel vlogs about the destination and have 10+ browser tabs open.

**Behavior:** High intent. Willing to spend 30–60 minutes planning. Will copy YouTube links into a form if the output is clearly better than what they can build manually.

**Constraints:**
- Does not want to create an account to try the product
- Will abandon if the loading wait is not explained (pipeline takes 30–90 seconds)
- Trusts YouTube creators more than AI-generated lists

### Secondary segment — Place shortlist owners

**Who:** A traveler who has already saved individual Google Maps place page links (from friends, blogs, or their own past saves) and wants them organized into a day plan.

**Input difference:** Google Maps place links instead of YouTube URLs. Same pipeline output.

### Out of scope for v1

- On-trip users (mobile navigation)
- Group trip planners
- Users who have not yet chosen a destination

---

## 6. Value Propositions

### Jobs travelers are trying to do

1. **Turn video inspiration into a plan** — "I watched a 20-minute vlog; I don't want to re-watch it to write down every place"
2. **Stop managing tabs** — "I have 15 Google Maps pins saved across 4 lists; I want one map"
3. **Know where to go each day** — "I have 5 days; how do I group these places so I'm not crossing the city twice?"
4. **Trust the source** — "I want to know which creator recommended this place"

### Gains Ytinerary delivers

- One-click conversion from YouTube URL to day-by-day route plan
- Places automatically clustered by geography into days
- Hotel shown on the same map (spatial anchoring)
- Creator attribution on every place card — retains the trust of the original recommendation
- Shareable link with no account required

### Pains Ytinerary removes

- Re-watching videos to find place names mentioned briefly
- Manual copying of place names into Google Maps
- Figuring out route order by hand
- Losing saved pins across multiple Google Maps lists
- Paying for travel itinerary SaaS tools before knowing if they're useful

### Competitive advantage

| Capability | Ytinerary | Layla / Mindtrip |
|---|---|---|
| Extracts places from YouTube video | ✅ | ❌ (surfaces video as inspiration) |
| Geocodes extracted places | ✅ | ❌ |
| Route-optimizes by geography | ✅ | ❌ |
| Outputs actionable day plan | ✅ | ❌ |
| Shows creator provenance | ✅ | ❌ |
| Free to use | ✅ | Freemium / paid |

---

## 7. Solution

### 7.1 User Flow

```
User opens Ytinerary
  → Fills in: Destination (required), YouTube URL(s) (required),
              Google Maps links (optional), Hotel (optional), Dates (optional)
  → Submits form
  → Full-screen loading overlay appears with live progress:
      "Fetching video transcripts..."
      "Extracting places from [Video Title]..."
      "Enriching [N] places with location data..."
      "Building your day-by-day plan..."
  → Results page: Interactive map (left) + Sidebar (right)
      → Map: Day-colored pins + hotel pin
      → Sidebar: Place cards organized by day cluster
      → Each card: Place name, category, rating, source video
      → Expanded card: Photo, hours, description, source link, Remove button
  → User can share via URL (encodes inputs only; pipeline re-runs on load)
```

### 7.2 Key Features

#### F1 — YouTube-to-Places Extraction
- User submits one or more YouTube video URLs
- System fetches transcript + video description (via `youtube-transcript-api`; fallback to `yt-dlp`)
- Claude Haiku extracts place names with sentiment, outputting structured JSON
- Negative-sentiment places are silently dropped before display
- Multiple videos processed in parallel; results merged before geocoding
- Same YouTube URL within a session hits an in-memory cache (skips re-processing)

#### F2 — Place Geocoding via Foursquare
- Each extracted place name is matched to a Foursquare place ID using the user's destination as a bounding region
- Radius scales by destination type: city (30km), region (150km), country (400km)
- Places that fail to match are shown as "Unresolved" in sidebar; user can remove them
- Matched places are enriched with: coordinates, category, rating, hours, 1-line description, photo
- Duplicate places (same Foursquare ID from multiple videos) are merged; all source videos tracked

#### F3 — Day Clustering
- k-means clustering on lat/lng of enriched places
- k = number of travel days (if dates provided) or min(5, ceil(num_places / 5))
- Maximum 5 places per day cluster; overflow goes to "More to Explore" section
- Claude Haiku labels each cluster with a descriptive name (e.g., "Day 1: Old City & Bazaars")
- If dates are provided, clusters are labeled with actual day names ("Tuesday, May 20")

#### F4 — Interactive Map
- Leaflet.js + OpenStreetMap tiles (fully free, no API key)
- Each day's places shown in a distinct color (Day 1 = blue, Day 2 = green, etc.)
- Hotel shown as a distinct marker if hotel was provided by user
- Pin click → tooltip with place name, category, rating
- Clicking a day in the sidebar highlights that day's pins on the map

#### F5 — Sidebar with Place Cards
- Collapsible sidebar; always accessible alongside map
- Collapsed card: place name, day label, category, rating, source video title
- Expanded card (on click): photo, opening hours, description, source video link (opens YouTube), Remove button
- Places appearing in multiple videos show all source videos in expanded view
- "More to Explore" section at bottom for places beyond the 5/day cap

#### F6 — Sharing via URL
- Share button encodes inputs only (YouTube URLs, destination, hotel, dates) into the URL
- Recipient opens link → pipeline re-runs (~30–90 second wait)
- No database or account required for v1
- URL stays under 500 characters for single-video itineraries; safe for all platforms

#### F7 — Live Progress Streaming
- SSE (Server-Sent Events) pushes 4 progress steps to the frontend during the pipeline run
- Full-screen loading overlay updates in real time with step label and progress bar
- If a video has no transcript: inline warning below that URL; pipeline continues with remaining URLs
- On pipeline error: non-blocking banner; partial results shown if any places were successfully processed

### 7.3 Technology

| Layer | Choice | Reason |
|---|---|---|
| Backend | Python + FastAPI | Fits existing skills; clean async API |
| Pipeline orchestration | LangGraph | Multi-step agent graph; easy to debug node by node |
| LLM | Claude Haiku | Fast, cheap, reliable JSON output |
| Streaming | FastAPI SSE + asyncio.Queue | Push progress during 30–90s pipeline without long-polling |
| Transcript | youtube-transcript-api + yt-dlp fallback | Covers most videos without an official YouTube API key |
| Clustering | scikit-learn k-means | Deterministic; no ε tuning required |
| Place data | Foursquare Places API (free tier) | 100k calls/month; ~40 calls per itinerary |
| Map | Leaflet.js + OpenStreetMap | Fully free; no API key; switch to Carto in v2 |
| Frontend | HTML + Tailwind CSS (CDN) + vanilla JS | Zero build tooling; Leaflet.js loads directly via CDN; no React required |
| Caching | In-memory dict per server process | Skip re-processing same YouTube URL |
| Database | None (v1) | No persistence needed; URL encodes inputs for sharing |
| Secrets | python-dotenv (.env) | `ANTHROPIC_API_KEY`, `FOURSQUARE_API_KEY` — never hardcoded |

### 7.4 Assumptions

| # | Assumption | Risk if wrong |
|---|---|---|
| A1 | `youtube-transcript-api` is reliable enough for most popular travel vlogs | Low success rate → user frustration; mitigated by yt-dlp fallback |
| A2 | Claude Haiku extracts places with ~80% precision (accepting ~20% noise) | Too many "Unresolved" cards degrades trust; user can remove bad places |
| A3 | Foursquare free tier (100k calls/month) is sufficient for v1 volume | At 40 calls/itinerary, the cap is hit at 2,500 itineraries/month — well above v1 PMF target |
| A4 | Users are willing to wait 30–90 seconds if progress is clearly communicated | Drop-off before results load; mitigated by live SSE progress overlay |
| A5 | URL-encoded sharing (re-runs pipeline on load) is acceptable without persistence | Shared links feel slow; acceptable for v1, upgrade to DB in v2 |
| A6 | k-means with k-cap of 5 days produces geographically sensible day plans | Poor clustering for road-trip-style destinations (large spread); observable from v1 usage data |

---

## 8. Release

### v1 — PMF (current focus)

**Goal:** Prove the core loop works and that people want to share the output.

**What's in:**
- Input form (destination, YouTube URLs, optional hotel/dates/Maps links)
- Full LangGraph pipeline (transcript → extraction → geocoding → clustering → labeling)
- Leaflet map with day-colored pins and hotel pin
- Sidebar with place cards and provenance attribution
- SSE progress streaming with loading overlay
- URL-input sharing (no database)
- Basic failure handling (transcript missing, zero places, geocoding fail)

**Build order (milestone sequence):**
0. CLI smoke test — validate pipeline end-to-end before any frontend
1. Input form
2. Full pipeline + SSE streaming (transcript fetch, extraction, Foursquare, SSE endpoint, loading overlay)
3. k-means clustering + Haiku cluster labeling
4. Leaflet map with pins
5. Sidebar with place cards
6. URL input encoding for sharing

**Estimated effort:** 1–2 weeks solo, building in the milestone order above.

**v1 → v2 trigger:** 50 itineraries generated (>70% extraction success) AND ≥ 10 URL shares.

### v2 — Growth (deferred)

The following are explicitly deferred and will only be scoped after v1 PMF criteria are met:

- Short-link sharing with database persistence
- Affiliate links (MakeMyTrip / Booking.com) for hotel and activity bookings
- Filter places by video source in sidebar
- "Places to Skip" section for negative-sentiment places (with creator reasoning)
- Vision/frame extraction from video (expensive, high-accuracy moat)
- User accounts and saved itineraries
- Mobile-first / on-trip navigation mode
- OpenStreetMap → Carto upgrade for improved tile reliability

---

*This PRD was generated from `travel-planner-spec.md` on 2026-05-17. It is the authoritative product specification for Ytinerary v1.*
