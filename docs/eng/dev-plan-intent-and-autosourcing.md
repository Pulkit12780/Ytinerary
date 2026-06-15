# Development Plan — Trip Intent & Auto-Sourcing

**Author:** CTO · **Date:** 2026-06-14 · **Status:** Shipped — M1–M4 complete (2026-06-14)
**Source brief:** [`docs/product/brief-intent-and-autosourcing.md`](../product/brief-intent-and-autosourcing.md) (CPO, 2026-06-14)

---

## 0. TL;DR for the team

We're shipping the CPO's reframe — *"user expresses intent, product does the sourcing and personalization"* — as **one release**. The engineering shape is deliberately small because the pipeline doesn't change downstream of transcript fetch:

1. **Two new request fields** (`trip_type`, `notes`) and **`youtube_urls` becomes optional**.
2. **One new node in front of the graph** (`source_videos`) behind a `VideoSource` seam, with a YouTube Data API implementation.
3. **Prompt threading** of intent into the augmenter and the judge.
4. **Input UX reframe** on `index.html`.
5. **Ops/observability**: new API key, quota guard, graceful fallback, metric instrumentation.

The risk is concentrated in exactly one place — the **YouTube Data API dependency** (quota + transcript availability). We de-risk it by building behind an interface, caching aggressively, and letting transcript-fetch be the final filter rather than trusting the search ranking.

---

## 1. Architecture decisions

### ADR-001 — Auto-sourcing as a node behind a `VideoSource` interface

**Context.** The brief wants YouTube search to *populate* `youtube_urls` before the existing pipeline runs, and wants a seam so Instagram/TikTok/blogs can slot in later (CUT for now) without touching the graph.

**Decision.** Add a new first node `source_videos` to the LangGraph pipeline (before `fetch_transcripts`). It calls a `VideoSource` abstraction. Ship one implementation, `YouTubeSearchSource`. Manual URLs short-circuit it.

```
[NEW] source_videos ──> fetch_transcripts ──> extract_places ──> augment_places ──> geocode_places ──> judge_and_plan
        │
        ├─ if request.youtube_urls non-empty  → pass through unchanged (manual precedence)
        └─ else → VideoSource.search(destination, trip_type) → rank → populate youtube_urls
```

**Consequences.**
- Everything from `fetch_transcripts` onward is **untouched** (the brief's "additive in front" principle).
- The seam is a 3-method protocol; a future `InstagramSource` implements the same contract. We do **not** build it now — we only leave the interface.
- Failure mode `NO_VIDEOS_FOUND` is new and must be handled end-to-end (see §6).

### ADR-002 — Transcript availability is enforced by *over-fetching*, not by trusting the caption flag

**Context.** With manual URLs, a missing transcript was the user's bad pick. Now it's our risk. The YouTube `contentDetails.caption` flag only reflects **manually-uploaded** captions — it says nothing about auto-generated (ASR) captions, which our transcript agent happily uses and translates.

**Decision.** Use the caption flag only as a **ranking boost**, never a hard filter. Source **more candidates than we need** (rank top ~8), then let `fetch_transcripts` be the real filter: keep the first 3–5 that actually yield a transcript. Only if *zero* candidates yield a transcript do we return `NO_VIDEOS_FOUND`.

**Consequences.** Slightly more transcript-fetch work (already parallel + cached, cheap). Dramatically lower chance of a dead-end plan. The existing `MISSING_TRANSCRIPT` degrade path stays as the backstop.

### ADR-003 — Personalization is prompt-level, not structural

**Context.** "Same plan for everyone" is fixed by conditioning the augmenter (*what* to suggest) and the judge (*pace & shape*) on intent.

**Decision.** Thread `trip_type` + `notes` as parameters into `augment_places(...)` and `plan_itinerary(...)`. Add a small per-trip-type guidance block to each system/user prompt and inject `notes` verbatim (length-bounded, treated as untrusted text). Vary one structural knob in the judge — stops-per-day — by trip type, since "family = fewer stops" is a hard AC, not a soft prompt nudge.

**Consequences.** Low structural risk; the data model of a plan is unchanged. The only non-prompt change is making `_MAX_STOPS_PER_DAY` and the day-target heuristic trip-type-aware.

---

## 2. The `trip_type` taxonomy (single source of truth)

Define once, shared by frontend chips, request validation, query builder, and prompts.

| `trip_type` value | Label (UI) | Search modifier | Augmenter bias | Judge shape |
|---|---|---|---|---|
| `balanced` *(default)* | Balanced / first visit | *(none)* `travel vlog` | current behavior | current (6–7 stops/day) |
| `romantic` | Romantic / couples | `honeymoon couples` | sunset points, rooftop/intimate dining | end day on sunset→dinner beat |
| `family` | Family with kids | `with kids family` | parks, low-walk, kid-friendly | **fewer stops/day (~4–5), lower intensity** |
| `adventure` | Adventure & outdoors | `trekking adventure` | treks, activities, outdoors | dense, activity-forward |
| `nature` | Nature & slow | `nature slow travel` | scenic/nature, fewer urban | relaxed pace, fewer stops |
| `culture` | Culture & heritage | `heritage culture history` | museums, monuments, old town | culture-clustered days |

`notes` is free text, **capped at 500 chars**, injected verbatim into both prompts as "Traveler notes (respect these): …".

---

## 3. Workstreams & tasks

Tasks are file-scoped and ordered so they can be parallelized after Milestone 1. Estimates are eng-days for one engineer; **S ≤ 0.5d, M ≈ 1d, L ≈ 2d**.

### Workstream A — Contract & data model  *(blocks everything; do first)*
**Files:** `backend/models.py`

- **A1 (S)** Add `trip_type: TripType = "balanced"` using a `Literal`/enum of the six values; default `balanced` preserves current behavior.
- **A2 (S)** Add `notes: Optional[str] = None` with a validator capping length at 500 and stripping.
- **A3 (S)** Make `youtube_urls: list[str] = []` (default empty). **Replace** the `one_to_five_urls` validator: drop the "at least one required" rule, **keep** the max-5 cap. Empty is now valid.
- **A4 (S)** Add `NO_VIDEOS_FOUND` to the `ErrorResponse.code` doc enum.

### Workstream B — Sourcing seam + YouTube auto-search  *(the only real new dependency)*
**Files:** `backend/agents/sourcer.py` *(new)*, `backend/pipeline.py`, `backend/cache.py`, `backend/main.py`, `backend/requirements.txt`, `backend/.env.example`

- **B1 (S)** Define `VideoSource` protocol/ABC in `sourcer.py`: `async search(destination, trip_type, limit) -> list[{url, title, video_id, score}]`. Document the seam (ADR-001).
- **B2 (L)** Implement `YouTubeSearchSource`:
  - `search.list` (cost **100 units**) — `part=snippet`, `type=video`, `q=<destination> <modifier> travel vlog`, `relevanceLanguage=en`, `order=relevance`, `maxResults=12`, `videoCaption=closedCaption` *(soft preference — see ADR-002, we do not rely on it)*.
  - Batched `videos.list` (cost **1 unit**) — `part=statistics,contentDetails` for viewCount + caption flag.
  - **Rank** = weighted (relevance rank · recency · view-velocity = views/age · caption-flag boost). Return top ~8 candidates (over-fetch per ADR-002).
  - **Never raises** — return `[]` on any API error (mirrors augmenter's degrade-gracefully contract).
- **B3 (M)** Caching to conserve quota: add **TTL support** to `cache.py` (namespaced keys, e.g. `ytsearch:{normalized_destination}:{trip_type}`, TTL 24h). One search/day per (destination, trip_type) instead of per request. Keep existing per-URL transcript cache untouched.
- **B4 (M)** New pipeline node `source_videos` (entry point, before `fetch_transcripts`):
  - If `request.youtube_urls` non-empty → pass through (manual precedence; AC #5).
  - Else → `VideoSource.search(...)`, take ranked candidates, write into `state.request["youtube_urls"]` (capped ~8 for transcript over-fetch; final keep happens after fetch).
  - If search returns `[]` → set `error=NO_VIDEOS_FOUND`.
  - Wire `_route` so the new node short-circuits to `END` on error, like the others.
- **B5 (S)** In `fetch_transcripts`, when sourced (not manual), keep the **first 3–5** that yield a transcript and drop the rest (the over-fetch filter). Manual path keeps current "use all" behavior.
- **B6 (S)** `requirements.txt`: add `google-api-python-client` (or call the REST endpoint with the existing `httpx` — preferred, one fewer dep). `.env.example`: add blank `YOUTUBE_API_KEY=`.

### Workstream C — Intent threading  *(parallel after A)*
**Files:** `backend/agents/augmenter.py`, `backend/agents/judge.py`, `backend/pipeline.py`

- **C1 (M)** `augment_places(...)` gains `trip_type`, `notes`. Add the per-trip-type bias block (§2) + verbatim notes to the prompt. `pipeline.augment_places` passes `req["trip_type"], req["notes"]`.
- **C2 (M)** `plan_itinerary(...)` / `_llm_plan(...)` gain `trip_type`, `notes`. Add per-trip-type **shape** instructions to `_SYSTEM`/prompt (romantic end-of-day beat, etc.) + verbatim notes.
- **C3 (S)** Make stops-per-day trip-type-aware: `family`/`nature` lower `_MAX_STOPS_PER_DAY` (~4–5) and the day-target heuristic. This is what makes AC #2 ("lower stops/day") *measurable*, not just prompted.
- **C4 (S)** `pipeline.judge_and_plan` threads the two fields through.

### Workstream D — Input UX reframe  *(parallel after A)*
**Files:** `index.html`

- **D1 (M)** Add a **trip-type chooser** (6 chips/radio, `balanced` preselected) between destination and the advanced section. Matches the flow in brief §6.
- **D2 (S)** Add a **notes** free-text box ("Anything we should know?").
- **D3 (M)** Move YouTube URL inputs **into** the existing collapsed `#optional-details` ("Have videos in mind? Paste them"). They're no longer primary.
- **D4 (S)** `isFormComplete()` → require **only** `destination.length >= 2`. Remove the `hasYtUrl` requirement.
- **D5 (S)** Submit payload: add `trip_type`, `notes`; `youtube_urls` now optional (omit/empty when none).
- **D6 (S)** Handle `NO_VIDEOS_FOUND` in the SSE error branch with a friendly message that nudges toward the paste fallback.

### Workstream E — Ops, config & observability
**Files:** `backend/main.py`, `backend/agents/sourcer.py`, `backend/.env.example`, `.gitignore`

- **E1 (S)** `/health` reports `youtube_key_set`.
- **E2 (S)** **Quota guard:** on `403 quotaExceeded` from YouTube, log + degrade to "no auto videos" (which surfaces the paste fallback) rather than 500. Treat quota as expected, not exceptional.
- **E3 (S)** Lightweight **metric instrumentation** (structured logs/counters) for the brief's §8 success metrics: zero-URL session flag, time-to-first-plan, fallback-path usage, `NO_VIDEOS_FOUND` rate.
- **E4 (S)** **Secret hygiene:** `backend/.env.example` currently contains a real-looking `OPENAI_API_KEY` — blank it out, confirm `.env.example` is the template (committed) and `.env` is git-ignored. **Rotate the exposed OpenAI key.** (See §7.)

### Workstream F — Tests & validation
**Files:** `backend/tests/…` *(new)*

- **F1 (M)** Unit: model validation (optional/empty URLs, max-5 cap, notes 500-char cap, `trip_type` default).
- **F2 (M)** Unit: `sourcer` ranking + query builder per trip type, with a **mocked** YouTube API (no quota in CI). Cache TTL behavior.
- **F3 (M)** Integration: zero-URL run (mocked source) reaches a plan (AC #3); manual URLs take precedence (AC #5); over-fetch keeps transcript-available ones (ADR-002).
- **F4 (M)** **Personalization diff harness** — same destination, two trip types → assert ≥40% stop difference (brief §8 metric + ACs #1/#2/#4). Doubles as the metric instrument.

---

## 4. Sequencing & milestones

```
M1  Foundation        A1–A4 (models)  +  B1 (interface)  +  B4 node wired to a STUB source
    → unblocks C and D in parallel WITHOUT burning YouTube quota
M2  Parallel build    C (intent threading)  ‖  D (frontend UX)   — both build against the stub
M3  Real source       B2,B3,B5,B6 (YouTubeSearchSource + ranking + cache + over-fetch filter)
                      E1,E2 (health, quota guard)
M4  Harden & verify   F1–F4 (tests + diff harness)  +  E3 (metrics)  +  E4 (secret hygiene)
```

The **stub source** in M1 (returns a fixed curated set of URLs for a known destination) is the key unlock: it lets the intent and frontend work proceed and be tested end-to-end before the real API integration exists, and keeps quota untouched during development.

**Rough size:** ~10–13 eng-days total. With the stub enabling parallelism, ~1 week of wall-clock with two engineers (one on B/E, one on C/D), F shared.

---

## 5. The one diagram that matters (intent + sourcing flow)

```
PlanRequest{ destination, dates, trip_type, notes, youtube_urls? }
        │
        ▼
 source_videos ── manual urls? ──► (pass through)
        │ no
        ▼
 YouTubeSearchSource.search(destination + trip_type modifier)
   search.list(100u) → videos.list(1u) → rank → top ~8 candidates
        │            (cached 24h per destination+trip_type)
        ▼
 fetch_transcripts ── keep first 3–5 with a real transcript ──► (else NO_VIDEOS_FOUND)
        ▼
 extract_places  →  augment_places(trip_type, notes)  →  geocode_places  →  judge_and_plan(trip_type, notes)
                         ▲ what to suggest                                      ▲ pace & shape + stops/day
        ▼
 Personalized day-by-day plan + map
```

---

## 6. Error handling matrix (new + changed paths)

| Code | When | Status | UX |
|---|---|---|---|
| `NO_VIDEOS_FOUND` *(new)* | Auto-search returns nothing **or** quota-degraded with no candidates | 404 | "We couldn't find good videos for this trip — paste your own?" → opens paste fallback |
| `MISSING_TRANSCRIPT` *(now also auto-path)* | All sourced candidates lack transcripts | 404 | Same friendly nudge; backstop after over-fetch |
| Quota exceeded | YouTube `403 quotaExceeded` | → degrades to `NO_VIDEOS_FOUND`, not 500 | Logged for ops; user sees fallback |
| Existing `ZERO_PLACES` / `GEOCODING_FAILURE` | unchanged | unchanged | unchanged |

---

## 7. Risks & mitigations

| Risk | Severity | Mitigation |
|---|---|---|
| **YouTube quota** — `search.list` = 100u, default 10k/day ≈ 100 searches/day | High at scale, fine for MVP | 24h cache per (destination, trip_type) → repeat searches are free; stub source during dev; quota-raise request before any scale; quota guard degrades gracefully (E2) |
| **Transcript availability now ours** | High | ADR-002 over-fetch: rank ~8, let transcript-fetch filter, keep 3–5; caption flag as boost not gate |
| **Sourced video quality / relevance** | Medium | Rank on relevance+recency+view-velocity; instrument fallback-usage (§8) as the trust signal; paste path always available |
| **Personalization not actually differentiating** | Medium | C3 makes stops/day a *structural* knob (not just prompt); F4 diff harness enforces ≥40% as a test, surfacing regressions |
| **`notes` is untrusted free text injected into prompts** | Low | 500-char cap; injected as clearly-delimited "traveler notes"; single-user planning context, low blast radius |
| **Exposed OpenAI key in `.env.example`** | High (security) | E4: blank the template, rotate the key, confirm `.env` git-ignored |
| New API key in CI/CD | Low | Tests mock YouTube (F2); no live key needed in CI |

---

## 8. Definition of done (maps to brief §5 ACs + §8 metrics)

- [ ] A valid plan is produced with **zero URLs entered** (AC #3) — covered by F3.
- [ ] Selecting `romantic` vs `balanced` for the same destination changes places/day-endings (AC #1) — F4.
- [ ] `family` plans have **lower stops/day** (AC #2) — enforced by C3, asserted by F4.
- [ ] Free-text `notes` demonstrably shift restaurant/pacing choices (AC #4) — F4.
- [ ] Pasted URLs still work and **take precedence** (AC #5) — F3.
- [ ] Metrics instrumented: zero-URL %, time-to-first-plan, fallback usage, `NO_VIDEOS_FOUND` rate (§8) — E3/F4.
- [ ] `OPENAI_API_KEY` rotated; `.env.example` blanked; quota guard verified (E2/E4).

---

## 9. Open questions for CPO/founder (non-blocking)

1. **Quota ceiling for launch.** 100 searches/day caps concurrent unique (destination, trip_type) pairs before cache warms. Acceptable for validation? If we expect a launch spike, file the quota-raise now (lead time).
2. **Default trip type wording.** Brief says "Balanced / first visit" is default and = current behavior. Confirm chip copy.
3. **How many sourced videos to *show* the user.** We fetch ~8, keep 3–5 — do we surface which videos a plan was built from (we already render `video_titles`)? Recommend yes — it reinforces the creator-content moat.
```
