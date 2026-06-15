# Product Brief — Trip Intent & Auto-Sourcing

**Author:** CPO · **Date:** 2026-06-14 · **Status:** Shipped (2026-06-14)

---

## 1. The problem (sharpened)

Two complaints surfaced. They look separate but are the same root cause: **the user is doing the product's job, and the product isn't doing its own.**

### 1a. Every traveler gets the same plan
A couple on a honeymoon, a family with a 4-year-old, and a solo trekker all paste the same Jaipur video and get **byte-identical itineraries**. The pipeline has no concept of *who is traveling* or *what kind of trip this is*:

- `PlanRequest` (`backend/models.py:6`) carries `destination`, `youtube_urls`, `hotel`, dates. No traveler type. No vibe.
- The augmenter (`augmenter.py`) suggests "well-regarded sights" and "~3 restaurants/day" generically.
- The judge sequences by geography and meal slots only.

So the product's one job after extraction — *make this trip feel like it's for me* — never happens. A romantic plan should end days on sunsets and rooftop dinners; a family plan should be shorter, lower-walk, with nap windows; an adventure plan should pack in treks. Today they're all the same.

### 1b. The user has to source the videos
The `youtube_urls` field is **required** (`one_to_five_urls` validator, `models.py:23`). To use Ytinerary you must:
1. Already think in terms of YouTube,
2. Go to YouTube and hunt for good vlogs,
3. Judge which ones are any good,
4. Copy-paste 1–5 URLs back.

That's four steps of *our* work pushed onto the user — before they get any value. People who don't live on YouTube are simply excluded. People who do are doing tedious curation we could automate.

### Why this matters commercially
"Paste videos → get the same plan as everyone" is a **utility**, and a leaky one. Nobody pays for it — ChatGPT does a passable version for free. The thing worth paying for is: *"Tell us your trip; we'll build it from what real travel creators actually did there, tuned to your style."* The auto-sourcing removes the cost of entry; the personalization is what makes the output feel bespoke enough to convert. Both fixes are prerequisites to willingness-to-pay, not nice-to-haves.

---

## 2. The strategic reframe

> **The user expresses intent. The product does the sourcing and the personalization.**

The YouTube URL is an *implementation detail that has leaked into the UX.* Our wedge is still creator content — that's our differentiation vs. Google Maps / TripAdvisor / generic LLM plans — but **sourcing that content is our job, not the traveler's.**

New mental model of the input:

| Today (wrong) | Proposed (right) |
|---|---|
| Destination + **paste 1–5 URLs** (required) | Destination + dates + **"what kind of trip?"** |
| User finds & vets videos | **We search YouTube** and pick the best vlogs |
| Same plan for everyone | Plan **conditioned on intent** at 3 stages |

We keep the creator-content moat. We remove the part that was never the user's to do.

---

## 3. The decision

### 3a. Intent — add a single, lightweight "trip type" + free-text note

Add to `PlanRequest`:
- `trip_type`: one of a **small fixed preset set** (pick one, default "Balanced / first visit"):
  - **Romantic / couples**
  - **Family with kids**
  - **Adventure & outdoors**
  - **Nature & slow**
  - **Culture & heritage**
  - **Balanced / first visit** (default — current behavior)
- `notes` (optional free text): *"vegetarian, traveling with my parents who can't walk far, love coffee."*

Why presets over sliders/two-axis taxonomy: minimum cognitive load, no combinatorial explosion, and it's enough signal to differentiate output. The **free-text note is the high-leverage cheap lever** — it absorbs the infinite long tail (diet, mobility, budget, pace) without any UI complexity, and injects straight into prompts.

Intent then conditions **three stages**:
1. **Video search query** — "Jaipur honeymoon" / "Jaipur with toddlers" / "Jaipur trekking".
2. **Augmenter** — *what* to suggest (romantic → sunset points, rooftop dining; family → parks, low-walk, kid-friendly; adventure → treks, activities).
3. **Judge / plan** — *pace & shape* (family = fewer stops/day, lighter; romantic = end on a sunset/dinner beat; adventure = dense).

### 3b. Auto-sourcing — search YouTube for the user, keep manual as a fallback

- New default path: given `destination` + `trip_type`, call the **YouTube Data API `search.list`**, rank candidates by relevance + recency + view-velocity + **transcript availability**, take the top N (3–5), and feed them into the *existing, unchanged* pipeline.
- `youtube_urls` becomes **optional**. Keep a collapsed **"Have specific videos in mind? Paste them"** advanced affordance — it serves power users and is the graceful fallback when auto-search returns thin results.

This is deliberately **additive in front of the pipeline.** Everything from `extract_places` onward stays as-is. We're changing what fills `youtube_urls`, not how transcripts become plans.

---

## 4. Scope — what's IN, what's CUT

### MVP (IN)
| Item | Rationale |
|---|---|
| `trip_type` presets + optional `notes` on `PlanRequest` | The personalization signal. Small surface, big payoff. |
| Intent injected into augmenter + judge prompts | Where "same plan for everyone" actually gets fixed. |
| YouTube auto-search node before `fetch_transcripts` | Removes the entry cost; opens product to non-YouTube users. |
| `youtube_urls` optional + collapsed "paste your own" fallback | Cheap to keep, serves power users, covers weak-search-result case. |
| New input UI: destination → dates → trip-type chooser → (advanced: paste) | The whole UX reframe the user is asking for. |

### CUT / LATER (with reason)
| Item | Why not now |
|---|---|
| Accounts, saved taste profiles, history | Not required to deliver a personalized plan once. Add when retention is the bottleneck, not before. |
| Multi-source ingestion (Instagram/TikTok/blogs) | YouTube is the moat and the proven path. Leave an interface seam in the sourcing layer; don't build it. |
| Two-axis taxonomy / sliders / per-stop preference tuning | Combinatorial UI cost with unproven incremental value. Presets + free-text covers ~90% at a fraction of the effort. |
| "Regenerate with a different vibe" / A-B itineraries | Real feature, but a fast-follow. Ship one good personalized plan first. |

---

## 5. User stories

1. *As a couple planning a honeymoon, I want to pick "Romantic" and get a plan that ends days on sunsets and intimate dinners, so the trip feels made for us — without me hunting for the right videos.*
   - **AC:** Selecting Romantic measurably changes suggested places and day endings vs. Balanced for the same destination.

2. *As a parent traveling with a toddler, I want a "Family" plan with fewer stops, less walking, and kid-friendly spots, so we're not dragging a tired child across a city.*
   - **AC:** Family plans have a lower stops/day count and flag/avoid high-intensity stops.

3. *As someone who doesn't use YouTube, I want to just enter where and when I'm going and get a plan, so I never have to find a video.*
   - **AC:** A valid plan is produced with **zero** URLs entered.

4. *As a vegetarian traveling with elderly parents, I want to type that in a notes box and have the plan respect it, so I don't get steak houses and 6-mile walking days.*
   - **AC:** Free-text notes demonstrably shift restaurant and pacing choices.

5. *As a power user who already found two great vlogs, I want to paste them, so my picks are used instead of (or alongside) auto-search.*
   - **AC:** The advanced paste path still works and takes precedence when provided.

---

## 6. User flow (critical path)

```
Landing
  → Destination  (Jaipur, India)
  → Dates        (optional)
  → "What kind of trip?"  [Romantic][Family][Adventure][Nature][Culture][Balanced]
  → (optional) "Anything we should know?"  free text
  → (advanced, collapsed) "Have videos in mind? Paste them"
  → Plan my trip
        ↓
  [NEW] Auto-source: YouTube search(destination + trip_type) → rank → top 3–5
        ↓
  fetch_transcripts → extract → augment(intent) → geocode → judge(intent)
        ↓
  Personalized day-by-day plan + map
```

Shortest path to value drops from *"go to YouTube, find videos, vet them, copy 5 URLs, come back"* to *"destination + one tap."*

---

## 7. Flags for CTO (feasibility)

- **YouTube Data API quota.** `search.list` costs **100 units/call**; default project quota is **10,000 units/day ≈ 100 searches/day**. Fine for MVP/validation; needs caching (cache top videos per destination+trip_type) and a quota-raise request before scale. **This is the main new dependency.**
- **Transcript availability is now our risk, not the user's.** When the user pasted URLs, a missing transcript was their bad pick. Now auto-search must **rank transcript-available videos up** and degrade gracefully (the `MISSING_TRANSCRIPT` path already exists). Recommend filtering for caption availability during ranking.
- **Prompt threading.** Personalization is mostly prompt-level: thread `trip_type` + `notes` into `augmenter.augment_places(...)` and `judge.plan_itinerary(...)`. Low structural risk; the pipeline shape is unchanged.
- **Sourcing seam.** Build auto-search as a node that *populates* `youtube_urls` before `fetch_transcripts`, behind a small `VideoSource` interface, so Instagram/TikTok/blogs can slot in later without touching the rest of the graph.

---

## 8. Success metrics

- **Activation:** % of sessions that reach a plan with **zero URLs pasted** (target: this becomes the dominant path).
- **Time-to-first-plan:** wall-clock from landing → plan (should drop sharply vs. the paste flow).
- **Personalization lift:** plans for the same destination across two trip types differ in ≥40% of stops (instrumented diff).
- **Perceived fit:** post-plan thumbs-up / "does this feel like your trip?" (the WTP proxy).
- **Fallback usage:** % using the advanced paste path (tells us how much auto-search is trusted).

---

## 9. Recommendation

Ship **3a + 3b together as one release.** They're two halves of the same reframe — auto-sourcing without personalization is still a generic plan; personalization without auto-sourcing still gates everyone behind URL-hunting. Done together, they turn Ytinerary from a *paste-to-plan utility* into *"tell us your trip, we build it from real creators, tuned to you"* — which is the version someone pays for.
