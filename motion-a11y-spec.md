# Ytinerary — Motion, Accessibility & Visual Richness Spec
*v2.0 | Uber Design Language | 2026-05-28 | Source: design-spec.md §6, §10, §11, §12 | For Frontend Engineer*

---

## Design Language Note
Motion in this system follows Uber's principle: **motion is functional, not decorative**. Animations exist to confirm state changes, guide attention, and communicate system feedback. Durations are slightly shorter than playful systems. Spring physics are reserved for structural movements (sidebar, panels) — not for individual UI elements. Nothing idles without purpose.

---

## 1. Motion Language

### 1.1 Easing Token Reference

| Token | Curve | Use for | Don't use for |
|---|---|---|---|
| `--transition-fast` (100ms ease-out) | ease-out | Hover color/bg, border changes, focus rings | Position changes |
| `--transition-base` (180ms ease-out) | ease-out | Standard state changes, opacity reveals | Long-distance motion |
| `--transition-decelerate` (280ms) | `cubic-bezier(0.05, 0.7, 0.1, 1)` | Elements entering screen | Exits |
| `--transition-accelerate` (180ms) | `cubic-bezier(0.3, 0, 0.8, 0.15)` | Elements exiting screen | Entrances |
| `--transition-snap` (140ms) | `cubic-bezier(0.32, 0.72, 0, 1)` | Tab switches, instant-but-not-jarring toggles | Lifts |
| `--transition-spring-soft` (300ms) | `cubic-bezier(0.34, 1.4, 0.64, 1)` | Sidebar collapse, panel reveals — subtle overshoot | Buttons, text |
| `--transition-slow` (400ms ease-out) | ease-out | Page entrances, complex reveals | Hover states |

> No `spring-bouncy` easing — too playful for this system. Pin drops use `ease-decelerate`.

### 1.2 Duration Ladder

| Speed | Duration | Feels like |
|---|---|---|
| Instant | 60–100ms | Direct response (hover, focus ring) |
| Quick | 140–200ms | Acknowledged action (click, toggle) |
| Smooth | 250–320ms | State transition (panel, expand) |
| Cinematic | 380–500ms | Page entrance, modal sequence |
| Ambient | 2s+ | Idle loops (only when meaningful) |

### 1.3 Stagger Rules
- Default list stagger: **40ms** per child
- Map pin drops: **50ms** per pin
- Hero word groups: **60ms** per group
- Cap stagger at **8 items** — beyond that, single group fade
- Total pin stagger cap: **1500ms** (remaining pins appear instantly)

---

## 2. Motion Master Table

| Element | Property | From | To | Duration | Easing |
|---|---|---|---|---|---|
| **Page transitions** | | | | | |
| Form → loading | opacity | 1 | 0.6 | 140ms | accelerate |
| Loading → results | opacity | 0 | 1 | 400ms | decelerate |
| **Landing — entrance** | | | | | |
| Hero line 1 | translateY, opacity | 8px, 0 | 0, 1 | 280ms | decelerate |
| Hero line 2 | translateY, opacity | 8px, 0 | 0, 1 | 280ms (delay 60ms) | decelerate |
| Subtitle | opacity | 0 | 1 | 200ms (delay 350ms) | ease-out |
| Form card entrance | translateY, opacity | 10px, 0 | 0, 1 | 400ms (delay 350ms) | decelerate |
| Topbar on-scroll | shadow | none | shadow-md | 180ms | ease-out |
| **Form fields** | | | | | |
| Input hover border | border-color | #E2E2E2 | #000000 | 100ms | ease-out |
| Input focus border | border-width, shadow | 1px | 2px + glow-primary | 100ms | ease-out |
| Input valid ✓ | translateX, opacity | 6px, 0 | 0, 1 | 180ms | ease-out |
| Input invalid shake | translateX | 0 | ±3px | 200ms | ease-out |
| Floating label | translate, font-size | 0, 16px | -20px, 11px | 160ms | ease-out |
| URLInputRow add | height, opacity, translateX | 0, 0, -6px | 48px, 1, 0 | 200ms | decelerate |
| URLInputRow remove | height, opacity, translateX | 48px, 1, 0 | 0, 0, 10px | 160ms | accelerate |
| URL valid → preview | height | 48px | 64px | 280ms | spring-soft |
| Thumbnail fade-in | opacity, scale | 0, 0.94 | 1, 1 | 200ms | ease-out |
| URL valid confirm flash | border-color | #E2E2E2 | #05944F → #E2E2E2 | 500ms | ease-out |
| Optional accordion open | max-height, opacity | 0, 0 | 300px, 1 | 280ms | decelerate |
| Optional accordion close | max-height, opacity | 300px, 1 | 0, 0 | 180ms | accelerate |
| Chevron rotate | rotate | 0° | 90° | 280ms | ease-out |
| **Submit button** | | | | | |
| Hover bg | background | #000000 | #1A1A1A | 100ms | ease-out |
| Arrow nudge (hover) | translateX | 0 | +3px | 100ms | ease-out |
| Press | scale | 1 | 0.98 | 80ms | ease-out |
| Click ripple | scale, opacity | 0, 0.3 | 20×, 0 | 300ms | decelerate |
| Idle arrow nudge | translateX | 0 | +4px → 0 | 800ms (every 6s) | ease-in-out |
| **Loading overlay** | | | | | |
| Backdrop fade-in | opacity | 0 | 1 | 180ms | ease-out |
| Backdrop blur-in | backdrop-filter | blur(0) | blur(8px) | 180ms | ease-out |
| Card enter | translateY, opacity | 10px, 0 | 0, 1 | 320ms (delay 60ms) | decelerate |
| Mini-map pin drop | translateY, opacity | -24px, 0 | 0, 1 | 400ms stagger 180ms | decelerate |
| Mini-map route draw | stroke-dashoffset | 1000 | 0 | 1000ms | ease-out |
| Step label swap out | translateY, opacity | 0, 1 | -6px, 0 | 140ms | accelerate |
| Step label swap in | translateY, opacity | 6px, 0 | 0, 1 | 180ms | decelerate |
| Progress fill | width | prev% | next% | 500ms | decelerate |
| Progress shimmer | bg-position | -200% | 200% | 1600ms loop | linear |
| Card exit | opacity, translateY | 1, 0 | 0, -6px | 280ms | accelerate |
| **Results — entrance** | | | | | |
| Sidebar entrance | translateX, opacity | 400px, 0 | 0, 1 | 400ms | decelerate |
| Map pin drop | translateY, opacity | -32px, 0 | 0, 1 | 400ms, 50ms stagger | decelerate |
| Pin landing ripple | scale, opacity | 0.8, 0.5 | 2.0, 0 | 1600ms once | ease-out |
| Sidebar card slide | translateY, opacity | 8px, 0 | 0, 1 | 280ms, 40ms stagger | decelerate |
| Day header enter | translateY, opacity | 8px, 0 | 0, 1 | 280ms | decelerate |
| **Results — interaction** | | | | | |
| PlaceCard hover | border-left, shadow | transparent, subtle | day-N, card-hover | 180ms | ease-out |
| PlaceCard press | scale | 1 | 0.99 | 80ms | ease-out |
| PlaceCard expand | max-height | 80px | 600px | 280ms | decelerate |
| PlaceCard collapse | max-height | 600px | 80px | 180ms | accelerate |
| PlaceCard photo zoom | scale | 1 | 1.02 | 360ms | ease-out |
| PlaceCard photo shimmer | bg-position | -200% | 200% | 1600ms loop | linear |
| Place removed | translateX, opacity | 0, 1 | 16px, 0 | 240ms | accelerate |
| Pin hover scale | scale | 1 | 1.12 | 180ms | ease-out |
| Pin selected scale | scale | 1 | 1.25 | 180ms | ease-out |
| Pin idle pulse-ring | scale, opacity | 0.8, 0.5 | 2.0, 0 | 1600ms (every 8s) | ease-out |
| Pin dim | opacity | 1 | 0.3 | 180ms | ease-out |
| Route polyline draw | stroke-dashoffset | len | 0 | 1000ms | ease-out |
| Route fade fallback | opacity | 0 | 0.80 | 280ms | ease-out |
| Route exit | opacity | 0.80 | 0 | 180ms | ease-out |
| DaySectionHeader active | background, accent | transparent, 3×16 | day-subtle, 4×20 | 180ms | ease-out |
| Header click ripple | scale, opacity | 0 | 640px, 0 | 300ms | decelerate |
| Sidebar collapse | width | 400px | 0 | 300ms | spring-soft |
| Sidebar expand | width | 0 | 400px | 300ms | spring-soft |
| Sidebar toggle hover | scale | 1 | 1.06 | 100ms | ease-out |
| Map panel flex | flex | — | — | 300ms | spring-soft |
| Auto-scroll to card | scroll-top | current | target | 300ms | ease-out |
| Map pan | latlng | current | target | 400ms | Leaflet default |
| **Misc** | | | | | |
| ShareButton hover | border | #E2E2E2 | #000000 | 100ms | ease-out |
| ShareButton copied | bg, border, color | default | success tints | 100ms | ease-out |
| ShareButton ✓ draw | stroke-dashoffset | 24 | 0 | 240ms (delay 60ms) | ease-out |
| ShareButton reset | all | success | default | 180ms (after 2000ms) | ease-out |
| ErrorBanner enter | translateY, opacity | -6px, 0 | 0, 1 | 180ms | decelerate |
| Skeleton shimmer | bg-position | -200% | 200% | 1600ms loop | linear |
| Tooltip show | opacity, translateY | 0, 3px | 1, 0 | 140ms | ease-out |
| Tooltip hide | opacity | 1 | 0 | 100ms | ease-in |

---

## 3. Keyframe Registry

```css
@keyframes slide-up-fade {
  0%   { transform: translateY(8px); opacity: 0; }
  100% { transform: translateY(0); opacity: 1; }
}
@keyframes shimmer {
  0%   { background-position: -200% 0; }
  100% { background-position: 200% 0; }
}
@keyframes pin-drop {
  0%   { transform: translateY(-32px) scale(0.7); opacity: 0; }
  100% { transform: translateY(0) scale(1); opacity: 1; }
}
@keyframes pulse-ring {
  0%   { transform: scale(0.8); opacity: 0.5; }
  100% { transform: scale(2.0); opacity: 0; }
}
@keyframes route-draw {
  0%   { stroke-dashoffset: 1000; }
  100% { stroke-dashoffset: 0; }
}
@keyframes check-draw {
  0%   { stroke-dashoffset: 24; }
  100% { stroke-dashoffset: 0; }
}
@keyframes ripple-expand {
  0%   { transform: scale(0); opacity: 0.3; }
  100% { transform: scale(20); opacity: 0; }
}
@keyframes arrow-nudge {
  0%, 100% { transform: translateX(0); }
  50%       { transform: translateX(4px); }
}
@keyframes fade-in {
  0%   { opacity: 0; }
  100% { opacity: 1; }
}
```

### Animation Utility Classes

```css
.animate-slide-up-fade  { animation: slide-up-fade 280ms cubic-bezier(0.05,0.7,0.1,1) backwards; }
.animate-pin-drop       { animation: pin-drop 400ms cubic-bezier(0.05,0.7,0.1,1) backwards; }
.animate-shimmer        { animation: shimmer 1600ms linear infinite; }
.animate-pulse-ring     { animation: pulse-ring 1600ms ease-out; }
.animate-route-draw     { animation: route-draw 1000ms ease-out forwards; }
.animate-check-draw     { animation: check-draw 240ms ease-out 60ms forwards; }
.animate-fade-in        { animation: fade-in 200ms ease-out forwards; }
```

---

## 4. Interaction Design Principles Applied

These 8 principles replace the full Disney 12 in the Uber-influenced model. Uber's motion is purposeful — every animation serves a specific role.

| # | Principle | Where it lives in Ytinerary |
|---|---|---|
| 1 | **Directness** | Buttons do not lift on hover — they darken. Color change is more honest than spatial illusion. |
| 2 | **Anticipation** | Submit button arrow nudges forward on hover. "→" in label signals direction before the click. |
| 3 | **Staging** | Loading overlay dims everything. Active day filter dims all others to 0.5 opacity. One focus at a time. |
| 4 | **Follow Through** | Sidebar expand overshoots ~1.5% with spring-soft, then settles. Click ripples expand past the point. |
| 5 | **Slow In / Slow Out** | `ease-decelerate` for entrances, `ease-accelerate` for exits. Linear banned outside shimmer. |
| 6 | **Secondary Action** | PlaceCard hover reveals day-colored border-left. Pin hover causes sidebar card border to change. |
| 7 | **Timing precision** | 80ms (press) → 100ms (hover) → 180ms (state) → 280ms (transition) → 400ms (entrance). |
| 8 | **Non-redundancy** | Every state conveyed by motion ALSO has a non-motion indicator (color, text, shape). |

---

## 5. Component State Checklist

Every interactive element must define these 5 states:

```
┌─────────────┬───────────────────────────────────────────────────┐
│ State       │ Required behavior                                 │
├─────────────┼───────────────────────────────────────────────────┤
│ rest        │ idle visual; static (no ambient animation)        │
│ hover       │ border/bg change — no vertical lift               │
│ focus       │ focus ring: box-shadow 0 0 0 3px rgba(0,0,0,0.12) │
│ active      │ scale(0.98–0.99) on press                         │
│ disabled    │ bg #E2E2E2, color #8A8A8A, cursor not-allowed     │
└─────────────┴───────────────────────────────────────────────────┘
```

### Per-Component Coverage

| Component | Rest | Hover | Focus | Active | Disabled | Loading | Success | Error |
|---|---|---|---|---|---|---|---|---|
| DestinationInput | ✓ | ✓ border-black | ✓ ring | ✓ shake | ✓ | — | ✓ ✓ icon | ✓ shake |
| URLInputRow | ✓ | ✓ border | ✓ ring | — | ✓ | ✓ skeleton | ✓ green flash | — |
| SubmitButton | ✓ | ✓ darken | ✓ ring | ✓ scale | ✓ | ✓ 3-dot | — | — |
| DaySectionHeader | ✓ | ✓ bg-gray | ✓ ring | ✓ filter | — | — | — | — |
| PlaceCard | ✓ | ✓ border-day | ✓ ring | ✓ press | — | ✓ shimmer | — | — |
| ShareButton | ✓ | ✓ border-black | ✓ ring | ✓ scale | — | — | ✓ copied | — |
| MapPin | ✓ | ✓ scale 1.12 | — | ✓ scale 1.25 | — | — | — | — |
| SidebarToggle | ✓ | ✓ scale 1.06 | ✓ ring | ✓ scale | — | — | — | — |

---

## 6. Code Recipes

```css
/* Ripple */
.ripple {
  position: absolute;
  border-radius: 9999px;
  background: rgba(255,255,255,0.20);
  pointer-events: none;
  animation: ripple-expand 300ms var(--ease-decelerate) forwards;
}

/* Skeleton shimmer */
.skeleton {
  background:
    linear-gradient(90deg, transparent, rgba(255,255,255,0.80), transparent) 0 0 / 200% 100%,
    #F0F0F0;
  animation: shimmer 1600ms linear infinite;
  border-radius: 8px;
}

/* Idle arrow nudge — fires every 6s on complete form */
[data-idle="true"] .btn-arrow {
  animation: arrow-nudge 800ms ease-in-out infinite;
  animation-delay: 6s;
}
[data-idle="true"]:hover .btn-arrow {
  animation: none;
}

/* Focus ring — universal */
:focus-visible {
  outline: none;
  box-shadow: 0 0 0 3px rgba(0, 0, 0, 0.12);
  border-radius: inherit;
}

/* Uber-style press */
.press:active { transform: scale(0.98); transition: transform 80ms ease-out; }

/* Hover border — Uber-style (border goes black, no lift) */
.hover-border {
  border: 1px solid #E2E2E2;
  transition: border-color 100ms ease-out;
}
.hover-border:hover { border-color: #000000; }
```

---

## 7. Visual Language Spec

### 7.1 Surfaces

| Surface | Color | Border | Use |
|---|---|---|---|
| Page background | `#FFFFFF` | none | Landing page, outer shell |
| Alt surface | `#F6F6F6` | none | Sidebar, section stripes |
| Card | `#FFFFFF` | 1px solid #E2E2E2 | Form card, PlaceCards, modal |
| Input | `#FFFFFF` | 1px solid #E2E2E2 | All text inputs |
| Error input | `#FFF0F0` | 1px solid #C7282D | Invalid state |
| Active day section | day-N-subtle | — | DaySectionHeader active |

> No mesh gradients, ambient orbs, or warm color washes. Contrast is achieved through black/white/gray hierarchy.

### 7.2 Hero Background Texture
Optional grid texture at 3–4% opacity using `rgba(0,0,0,0.03)`. Creates structured-space feel without competing with content.

```css
.hero-section {
  background-color: #FFFFFF;
  background-image:
    repeating-linear-gradient(0deg, transparent, transparent 39px, rgba(0,0,0,0.03) 39px, rgba(0,0,0,0.03) 40px),
    repeating-linear-gradient(90deg, transparent, transparent 39px, rgba(0,0,0,0.03) 39px, rgba(0,0,0,0.03) 40px);
}
```

### 7.3 Skeleton Colors
- Skeleton background: `#F0F0F0`
- Shimmer: `rgba(255,255,255,0.80)` layer, 200% wide, moves left-to-right

### 7.4 Idle Animation Budget (maximum 1 per screen)

**Landing page:**
- Nothing idles at rest — Uber interfaces are static
- Only exception: subtle arrow nudge on submit button after 4s idle on complete form (every 6s)

**Results page:**
- First pin of each day: pulse-ring every 8s when no filter is active

**Rule:** Zero ambient idle animations unless form is complete. Uber keeps the UI still.

---

## 8. Accessibility Specification

### 8.1 ARIA Map

| Element | ARIA |
|---|---|
| Page main | `role="main"` |
| Map panel | `role="application"` `aria-label="Interactive trip map"` |
| Sidebar | `role="complementary"` `aria-label="Trip itinerary"` |
| Sidebar toggle | `aria-label="Collapse sidebar"` / `"Expand sidebar"` |
| Loading overlay | `role="status"` `aria-live="polite"` |
| Step label | `aria-live="polite"` |
| Day filter | `aria-live="polite"` |
| Place removal | `aria-live="polite"` |
| Mobile sheet | `role="dialog"` `aria-label="Trip itinerary"` |
| Icon-only buttons | All: `aria-label` required |
| Error banner | `role="alert"` (auto-announces) |
| Optional accordion | `<details>`/`<summary>` — native semantics |

### 8.2 Focus Management
- All focus rings: `box-shadow: 0 0 0 3px rgba(0,0,0,0.12)`. Never removed.
- Tab order: Topbar → Form fields (top to bottom) → Submit → Optional accordion → Footer
- Loading overlay: focus moves to card on mount; returns to Submit on close
- Sidebar toggle collapse: focus moves to first map control; expand: focus to first PlaceCard

### 8.3 WCAG AA Contrast

| Color | Hex | On White | Status |
|---|---|---|---|
| text-primary | `#000000` | 21:1 | ✓ AAA |
| text-secondary | `#545454` | 7.6:1 | ✓ AA |
| text-muted | `#8A8A8A` | 3.5:1 | use 16px+ body |
| primary / CTA | `#000000` | 21:1 | ✓ AAA |
| accent green | `#06C167` | 3.0:1 | use for large/bold text; not small text |
| day-1 `#276EF1` | — | 4.7:1 | ✓ AA |
| day-4 `#7356BF` | — | 5.3:1 | ✓ AA |
| error | `#C7282D` | 5.1:1 | ✓ AA |

### 8.4 Non-Color Redundancy

| State | Color indicator | Non-color indicator |
|---|---|---|
| Selected map pin | Color saturation | Scale 1.25, elevation shadow |
| Valid input | Green border | ✓ checkmark icon |
| Error input | Red border + bg | Error message text + shake |
| Copied state | Green tint | "Link copied!" text |
| Active day filter | Day color highlight | Increased border weight (3→4px) |

### 8.5 Touch Targets

Minimum: **28×28px** for all interactive elements.

| Element | Size | Status |
|---|---|---|
| Sidebar toggle | 28×28 | ✓ exact minimum |
| Remove × PlaceCard | 24×24 | ⚠ needs 4px invisible padding |
| Pill remove × | 16×16 | ⚠ needs 6px invisible padding |
| Map pins | 28×36 | ✓ |
| DaySectionHeader | 40px height | ✓ |
| All buttons | 36–48px height | ✓ |

---

## 9. `prefers-reduced-motion` Strategy

```css
@media (prefers-reduced-motion: reduce) {
  /* Kill all durations first */
  *, *::before, *::after {
    transition-duration: 0.01ms !important;
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    scroll-behavior: auto !important;
  }

  /* Re-enable opacity fades that aid comprehension */
  .step-label,
  .toast,
  .place-card-photo {
    transition-duration: 200ms !important;
    transition-property: opacity !important;
  }
}
```

**State fallbacks:**
- Pin drop: pins appear instantly, stagger via JS opacity (no transform)
- Valid input: ✓ icon appears without scale animation
- Progress bar: fill advances without shimmer
- Loading card: appears immediately, no translate entrance

---

## 10. Performance Budget

### 10.1 Compositor Rules

Target **60fps** for all hover, scroll, click interactions.

**Animate only via compositor:**
- `transform` (translate, scale, rotate)
- `opacity`
- `filter` — only blur and brightness, sparingly

**Never animate:**
- `width` on pins — use `transform: scale`
- `height` on cards > 200px — use `max-height` with cap
- `top`/`left` — use `transform: translate`
- `background-color` on paint-every-scroll elements

### 10.2 `will-change` Policy

```css
.place-card:hover { will-change: transform; }
element.addEventListener('transitionend', () => {
  element.style.willChange = 'auto';
});
```

Apply only on hover-in. Remove on hover-out or animationend.

### 10.3 Pin Count Limits
- Pins beyond **30**: no ripple/pulse ambient
- Only viewport-visible pins receive idle animations (use Leaflet `getBounds()` + `IntersectionObserver`)

### 10.4 Implementation Hints

**JS-driven stagger** (pin drops, sidebar cards):
```js
cards.forEach((card, i) => {
  card.animate(
    [{ transform: 'translateY(8px)', opacity: 0 },
     { transform: 'translateY(0)',    opacity: 1 }],
    { duration: 280, delay: i * 40,
      easing: 'cubic-bezier(0.05,0.7,0.1,1)', fill: 'backwards' }
  );
});
```

**Route polyline draw:**
```js
const path = polylineLayer._path;
const len = path.getTotalLength();
path.style.strokeDasharray = len;
path.style.strokeDashoffset = len;
requestAnimationFrame(() => {
  path.style.transition = 'stroke-dashoffset 1000ms ease-out';
  path.style.strokeDashoffset = '0';
});
```

**Thumbnail fetch:** debounce input event 200ms before firing YouTube oembed fetch.

---

## 11. HTML Element Map

This project is **plain HTML + Tailwind CSS (CDN) + vanilla JavaScript**. No React, no framework.

| UI Element | HTML Implementation |
|---|---|
| Text inputs | `<input type="text">` / `<input type="url">` — Tailwind classes per components-spec.md |
| Submit button | `<button type="submit">` — Tailwind classes per components-spec.md |
| Remove buttons | `<button type="button" aria-label="...">` — SVG icon inside |
| Optional accordion | `<details>`/`<summary>` with CSS `max-height` transition on inner `<div>` |
| Date range | Two `<input type="date">` side-by-side |
| Loading overlay | `<div position:fixed inset:0>` toggled via JS classList |
| Error banner | `<div role="alert">` — dismissed via JS |
| Sidebar toggle | `<button type="button" aria-label="Toggle sidebar">` |
| Share copied feedback | JS: button text/style swap, setTimeout 2000ms reset |
| Unresolved places | `<details>`/`<summary>` |
| Hero background texture | `<div class="hero-bg">` — pure CSS grid pattern |
| URL → video preview | JS: input event, regex YouTube URL, swap children to `<div class="video-preview">` |
| Map pin idle pulse rings | `<div class="pin-pulse">` as Leaflet DivIcon sibling, CSS pulse-ring, removed after loop |
| Day route polyline | Leaflet `L.polyline`, JS `strokeDashoffset` animation via rAF |
| Ripples | JS `mousedown` → inject `<span class="ripple">` at click coords, remove on animationend |
| Skeleton loaders | `<div class="skeleton">` blocks while SSE loads |

---

*End of motion-a11y-spec.md*
*Everything moves with intention. Nothing moves without a reason.*
