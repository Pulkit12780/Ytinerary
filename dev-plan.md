# Ytinerary — Dev Plan

## Epic Breakdown

### Epic 1 — Landing Page + Loading Overlay (Frontend, no backend)
**Files:** `index.html`
**Milestone:** PRD milestone 1 — Input form
- Topbar with Y·tinerary logo (glassmorphism, scroll-aware)
- Hero section with ambient mesh gradient + 3 orbs + SVG route doodle
- Form card: destination field (floating label), YouTube URL stack (URLInputRow with preview transform), optional accordion (hotel, dates, Maps links), submit button
- Loading overlay: mini-map SVG animation keyed to SSE steps, progress bar, step labels
- All design tokens from design-tokens-spec.md as CSS custom properties
- All animations from components-spec.md §15 keyframe registry
- Responsive: mobile < 768px adaptations
- Accessibility: ARIA roles, reduced-motion, focus rings

### Epic 2 — Backend Pipeline (Python + FastAPI)
**Files:** `backend/main.py`, `backend/pipeline.py`, `backend/agents/`, `backend/.env.example`
**Milestone:** PRD milestone 2 — Full pipeline + SSE streaming
- FastAPI app with `/plan` POST endpoint + SSE `/plan/stream` endpoint
- LangGraph pipeline nodes: transcript_fetch → place_extraction → geocoding → clustering → labeling
- youtube-transcript-api + yt-dlp fallback for transcript fetch
- Claude Haiku (claude-haiku-4-5) for place extraction + cluster labeling
- Foursquare Places API for geocoding + place enrichment
- scikit-learn k-means for day clustering
- In-memory cache per YouTube URL
- SSE pushes 4 step events during pipeline run
- Error shapes: zero places, missing transcript, geocoding failure, invalid destination

### Epic 3 — Results Page (Frontend)
**Files:** `results.html`
**Milestone:** PRD milestones 3–5 — Map, sidebar, place cards
- Split layout: sticky Leaflet map (left) + scrollable sidebar (right, 400px)
- Leaflet.js + OpenStreetMap tiles
- Custom SVG day pins (DivIcon) with pin-drop entrance + pulse-ring
- Hotel pin (dark square icon)
- Map tooltip on pin click
- Day route polyline (drawn on DaySectionHeader click)
- Sidebar sticky header: destination + place count + ShareButton
- DaySectionHeader with ripple + day filter mode
- PlaceCard collapsed + expanded states
- More to Explore section + UnresolvedPlacePill
- Sidebar collapse toggle (overlaps map border)
- Cross-sync: card hover ↔ pin hover
- Mobile: full-map + bottom-sheet layout

### Epic 4 — URL Sharing + Integration
**Files:** `js/share.js`, updates to both HTML files
**Milestone:** PRD milestone 6 — URL input encoding for sharing
- Share button encodes destination + YouTube URLs + hotel + dates into URL params
- On page load: read params → auto-submit form → pipeline re-runs
- URL stays under 500 chars for single-video itineraries

---

## Build Order
1. ✅ Epic 1 — Landing page (no backend needed)
2. ✅ Epic 2 — Backend pipeline (validate with CLI smoke test first)
3. Epic 3 — Results page (wire to backend)
4. Epic 4 — URL sharing

## Tech Stack
- Frontend: HTML + Tailwind CSS (CDN) + vanilla JS + Leaflet.js (CDN)
- Backend: Python 3.12 (Anaconda ARM) + FastAPI + LangGraph + scikit-learn
- Run backend: `cd backend && /opt/anaconda3/bin/uvicorn main:app --reload` (from project root: `cd backend && /opt/anaconda3/bin/python3.12 -m uvicorn backend.main:app --reload`)
- LLM: claude-haiku-4-5 via Anthropic SDK
- Maps: Leaflet.js + OpenStreetMap (free, no API key)
- Places: Foursquare Places API (free tier)
- Transcripts: youtube-transcript-api + yt-dlp fallback
