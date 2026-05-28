# Ytinerary — Landing Page & Loading Overlay Design Spec
*v2.0 | Uber Design Language | 2026-05-28 | Source: design-spec.md §2–3 | For Frontend Engineer*

---

## Design Language Notes
This page follows the Uber visual language: bold black typography on white surfaces, clean geometric layout, no ambient gradients or decorative orbs. The form card and hero section use high contrast and strong typographic hierarchy as the primary visual tool.

---

## Page 1: Landing Page (/)

### Full Layout — Desktop (1280px+)

```
┌──────────────────────────────────────────────────────────────────┐
│  TOPBAR  h=60px                                                  │
│  bg=#FFFFFF  border-bottom: 1px solid #E2E2E2                    │
│  padding-h: 32px                                                 │
│  [Y·tinerary logo]                                               │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  bg: #FFFFFF (pure white)                                        │
│  Subtle grid texture: repeating-linear-gradient @4% opacity     │
│                                                                  │
│  HERO SECTION  padding-top: 96px  padding-bottom: 64px          │
│  text-align: center  max-width: 900px  mx: auto                  │
│                                                                  │
│  "Turn YouTube travel videos"                                    │
│  "into a day-by-day itinerary."                                  │
│  Manrope Bold 56px  #000000  letter-spacing -0.04em             │
│                                                                  │
│  "Paste a YouTube URL. Get a route-optimized itinerary          │
│   in under 60 seconds — no account required."                  │
│  Manrope Regular 18px  #545454  mt:16px  max-width:540px         │
│                                                                  │
│  FORM CARD  max-width:640px  mx:auto  mt:40px  mb:80px          │
│  bg:#FFFFFF  border: 1px solid #E2E2E2  border-radius:16px      │
│  shadow:sm  padding:32px                                         │
│                                                                  │
│   [Destination field]                                            │
│   ── divider 1px #F0F0F0 ──                                      │
│   [YouTube URL rows]                                             │
│   [+ Add another video]                                          │
│   ── divider ──                                                  │
│   [Optional accordion]                                           │
│   ── divider ──                                                  │
│   [Submit button "Build My Itinerary →"]                        │
│                                                                  │
├──────────────────────────────────────────────────────────────────┤
│  FOOTER  h:48px  text-align:center                               │
│  "Free · No account required · Powered by YouTube + Foursquare" │
│  Manrope Regular 14px  #8A8A8A                                   │
└──────────────────────────────────────────────────────────────────┘
```

---

## 1.1 Topbar

### Dimensions & Layout
- Height: 60px
- Display: flex, align-items center, justify-content space-between
- Padding horizontal: 32px
- Position: sticky, top 0, z-index 200

### Background & Border
- Default: `background: #FFFFFF`
- Border-bottom: 1px solid #E2E2E2
- Shadow: none at rest

### Scroll Behavior
At `scrollY > 16px`:
- shadow → shadow-md
- Transition: 180ms ease-out

### Logo
- Text: **"Y·tinerary"**
- "Y": color #06C167 (Uber green accent)
- "·": color #06C167, wrapped in separate span
- "tinerary": color #000000
- Font: Manrope Bold (700) 18px, letter-spacing -0.02em
- No idle animations — Uber logos are static

---

## 1.2 Hero Section — Background

### Base (on `<body>` or outer wrapper)
- `background: #FFFFFF`
- Optional: very subtle grid texture overlay (`repeating-linear-gradient`) at 3–4% opacity using `#E2E2E2`. Creates a clean structured feel without distraction.

```css
.hero-bg {
  background-color: #FFFFFF;
  background-image:
    repeating-linear-gradient(0deg, transparent, transparent 39px, rgba(0,0,0,0.03) 39px, rgba(0,0,0,0.03) 40px),
    repeating-linear-gradient(90deg, transparent, transparent 39px, rgba(0,0,0,0.03) 39px, rgba(0,0,0,0.03) 40px);
}
```

> No ambient orbs. No mesh gradients. No blurred circles. Clean surface is the canvas.

---

## 1.3 Hero Section — Content

### Heading
- Text: "Turn YouTube travel videos into a day-by-day itinerary."
- Split across 2 lines for visual impact: "Turn YouTube travel videos" / "into a day-by-day itinerary."
- Font: Manrope Bold (700) 56px, color #000000, letter-spacing -0.04em, line-height 1.0
- `max-width: 820px`, `margin: 0 auto`

**Entrance choreography:**
Split heading into 2 lines, each with slide-up-fade:
1. Line 1 — delay 0ms, 280ms decelerate
2. Line 2 — delay 60ms, 280ms decelerate

### Subtitle
- Text: "Paste a YouTube URL. Get a route-optimized itinerary in under 60 seconds — no account required."
- Font: Manrope Regular (400) 18px, #545454, line-height 1.5
- margin-top: 16px, max-width: 540px, margin: 16px auto 0
- Entrance: opacity 0→1, 200ms ease-out, delay ~350ms from page load

### Social Proof Strip
- margin-top: 24px, text-align center
- 4 creator avatar circles: 28px diameter, white 2px ring, box-shadow shadow-subtle, overlapping -8px
- Avatars: bg #F6F6F6 placeholder
- Text: "Built from videos by Mumbiker Nikhil, Curly Tales, +28 more" — Manrope Regular 14px, #545454, margin-left 10px
- Clean, no hover animation — static display

---

## 1.4 Form Card

### Container
- max-width: 640px, width 100%, margin: 40px auto 80px
- background: #FFFFFF
- border: 1px solid #E2E2E2
- border-radius: 16px
- shadow: shadow-sm at rest → shadow-lg on any inner field focus (180ms ease-out)
- padding: 32px

### Entrance Animation
- From: opacity 0, translateY 10px
- To: opacity 1, translateY 0
- Duration: 400ms decelerate, delay ~350ms after subtitle appears

> No idle breathe animation. No parallax. The card is static at rest.

### Internal Layout
- Vertical gap between field sections: 24px
- Section dividers: 1px solid #F0F0F0
- Label style: Manrope Medium (500) 14px, #000000, margin-bottom 6px, display block
- Required asterisk: * in #C7282D, same font
- Helper text: Manrope Regular 13px, #8A8A8A, margin-top 4px

---

## 1.5 Input Fields — System States

### Dimensions
- Height: 48px (taller than before — more Uber)
- Auto height (textarea / multi-line)
- border-radius: 8px
- Font: Manrope Regular (400) 16px, #000000
- Placeholder: #8A8A8A
- Padding: 0 14px (left 40px if leading icon)

### State Table
| State | Border | Background | Shadow | Additional |
|---|---|---|---|---|
| Rest | 1px solid #E2E2E2 | #FFFFFF | none | — |
| Hover | 1px solid #000000 | #FFFFFF | none | 100ms ease-out — border goes black on hover (very Uber) |
| Focus | 2px solid #000000 | #FFFFFF | shadow-glow-primary | 100ms; border thickens to 2px |
| Valid | 1px solid #E2E2E2 | #FFFFFF | none | ✓ icon enters from right in #05944F |
| Invalid | 1px solid #C7282D | #FFF0F0 | shadow-glow-error | 3px shake + error message |

**Valid ✓ entrance:** translateX 6px→0, opacity 0→1, 180ms ease-out. Icon: 16px ✓ in #05944F, positioned absolute right 14px.

**Invalid shake:** translateX sequence: 0 → -3px → 3px → -2px → 2px → 0, duration 200ms ease-out, one-shot on blur.

**Inline error:** Manrope Regular 13px, #C7282D, margin-top 4px, opacity 0→1 (100ms ease-out).

### Floating Label (Destination field)
- Default: label text inside field, font-size 16px, color #8A8A8A
- Focus or filled: translateY -20px, font-size 11px, color #000000, bg #FFFFFF padding 0 4px
- Transition: transform 160ms ease-out, font-size 160ms ease-out, color 120ms ease-out

---

## 1.6 Destination Field
- Floating label: "Destination *" (required)
- Placeholder: "e.g. Jaipur, India"
- Validation: required, min 2 chars

---

## 1.7 YouTube URL Stack
See components-spec.md §1 (URLInputRow) for complete spec.

Stack behavior:
- Starts with 1 URLInputRow
- "+ Add another video" adds rows
- No hard cap in v1

---

## 1.8 Optional Fields Accordion

### Trigger
- Content: "Optional details" — Manrope Medium (500) 14px, #545454
- ChevronRight icon (Lucide 14px, #8A8A8A), right of text
- Native `<details>`/`<summary>` element
- Trigger hover: text color →#000000, chevron translateX +2px, 100ms ease-out

### Expand Animation
- Chevron: rotate 0°→90°, 280ms ease-out
- Content div: max-height 0→300px, opacity 0→1, 280ms decelerate
- Inner fields: slide-up-fade stagger 40ms each

### Collapse Animation
- Chevron: rotate 90°→0°, ease-out
- max-height 300px→0, opacity 1→0, 180ms accelerate

### Content (gap: 16px)

**Hotel field:**
- Label: "Hotel (optional)"
- Placeholder: "e.g. Rambagh Palace"
- On valid value: green ✓ fades in right of field (same as other valid state)

**Date range:**
- Two `<input type="date">` side by side
- Between them: "→" in Manrope Regular 14px, #8A8A8A
- When both dates valid: day count appears below — Manrope Regular 13px, #545454, slide-up-fade

**Google Maps URLs:**
- Label: "Google Maps links (optional)"
- Placeholder: "Paste maps.google.com links"

---

## 1.9 Submit Button

The primary CTA follows Uber's bold black button pattern.

### Dimensions & Base
- width: 100%, height: 48px
- background: #000000, border-radius: 8px
- Font: Manrope Bold (700) 16px, #FFFFFF
- Label: "Build My Itinerary →" — the → in its own `<span class="btn-arrow">`
- position: relative, overflow: hidden (for ripple)
- margin-top: 24px

### State Table
| State | Background | Transform | Shadow | Arrow |
|---|---|---|---|---|
| Rest | #000000 | none | none | default |
| Hover | #1A1A1A | none | none | translateX +3px |
| Press | #333333 | scale(0.98) | none | default |
| Release | #1A1A1A | none | none | snap back |
| Disabled | #8A8A8A | none | none | — |
| Loading | #1A1A1A | none | none | replaced by dots |

Hover transition: 100ms ease-out. Press: 80ms. Release: 150ms ease-out.

> No translateY lift on hover — Uber buttons don't lift. Background darkens slightly. Arrow slides forward.

### Click Ripple
On mousedown, inject `<span class="ripple">` at click coordinates:
- background rgba(255,255,255,0.20)
- animation: ripple-expand 300ms ease-decelerate forwards
- Remove on animationend

### Loading State (3-dot wave)
Label swaps to "Working..." + 3 dots:
- Each: •, animation opacity 0→1→0, 1400ms ease-in-out infinite
- Delays: 0ms / 160ms / 320ms
- pointer-events: none

### Idle Attention (after 4s, form complete)
A subtle right-arrow pulse: the → arrow in the label nudges +3px and returns every 6s.
Implemented as `@keyframes arrow-nudge { 0%,100% { transform:translateX(0) } 50% { transform:translateX(4px) } }` on `[data-idle="true"] .btn-arrow`.

### Disabled State
- background #E2E2E2, color #8A8A8A, cursor not-allowed
- No transitions, no ripple

---

## 1.10 Footer
- height: 48px, margin-top auto
- text-align center, display flex, align-items center, justify-content center
- Text: "Free · No account required · Powered by YouTube + Foursquare"
- Font: Manrope Regular 14px, #8A8A8A

---

## 1.11 Mobile Adaptations (< 768px)

| Element | Desktop | Mobile |
|---|---|---|
| Hero heading | 56px | 40px |
| Hero heading line-height | 1.0 | 1.05 |
| Subtitle font-size | 18px | 16px |
| Form card margin | 40px auto | 24px 16px |
| Form card border-radius | 16px | 12px |
| Form card padding | 32px | 24px |
| Topbar padding-h | 32px | 16px |
| Input height | 48px | 48px (unchanged) |
| Submit button | unchanged | unchanged (full-width) |
| Background grid | subtle | hidden |

---

## Page 2: Loading Overlay (Full-screen Modal)

Rendered above everything after form submit. Non-dismissable. `position: fixed; inset: 0; z-index: 50`.

### Layout
```
┌──────────────────────────────────────────────────────────────────┐
│  BACKDROP                                                        │
│  bg: rgba(0,0,0,0.65)  backdrop-filter: blur(8px)               │
│  display: flex  align-items: center  justify-content: center    │
│                                                                  │
│      ┌─────────────────────────────────────────────┐            │
│      │  CARD  w:480px                              │            │
│      │  bg:#FFFFFF  rounded:24px  shadow:xl        │            │
│      │  border: 1px solid #E2E2E2                  │            │
│      │  padding:40px  text-align:center            │            │
│      │                                             │            │
│      │  [MINI-MAP SVG  80×80px]                    │            │
│      │                                             │            │
│      │  "Building your itinerary."                 │            │
│      │  Manrope Bold 20px  #000000  mt:20px        │            │
│      │                                             │            │
│      │  [Step label]                               │            │
│      │  Manrope Regular 15px  #545454  mt:8px      │            │
│      │                                             │            │
│      │  [Progress bar  h:4px  rounded]             │            │
│      │  mt:24px                                    │            │
│      │                                             │            │
│      │  "This takes about 30–90 seconds."          │            │
│      │  Manrope Regular 14px  #8A8A8A  mt:20px     │            │
│      └─────────────────────────────────────────────┘            │
└──────────────────────────────────────────────────────────────────┘
```

---

## 2.1 Card Spec
- Width: 480px (mobile: calc(100% - 32px), max-width 480px)
- Background: #FFFFFF
- border: 1px solid #E2E2E2
- border-radius: 24px
- Shadow: shadow-xl
- Padding: 40px
- text-align: center
- No ambient glow or breathe animation behind card — clean modal on dark backdrop

---

## 2.2 Overlay Entrance Animation
1. Backdrop: opacity 0→1 over 180ms ease-out + blur(0)→blur(8px) simultaneously
2. Card: opacity 0, translateY 10px → opacity 1, translateY 0 — 320ms ease-decelerate, delay 60ms

---

## 2.3 Mini-Map SVG (80×80px)

Canvas: 80×80px, centered in card.

**Static elements:**
- "Y" letterform: Manrope Bold ~28px, #06C167 (Uber green), 20% opacity, centered behind everything
- 10×10 dot grid: 2px circles, #E2E2E2, 8px spacing — initially hidden

**5 day-pin circles:** 8px diameter, day colors, initially opacity 0.

**Dotted path:** stroke-dasharray: 3 4, stroke: #276EF1 at 50% opacity. Drawn via stroke-dashoffset.

### Animation sequence (keyed to SSE step index 0–3)

**Step 0 — Fetching transcripts:**
- "Y" letterform: opacity 0→0.20, 280ms ease-out
- Dot grid: draws left-to-right over 600ms

**Step 1 — Extracting places:**
- Pin 1 drops in (pin-drop 400ms): opacity 0→1, translateY -24px→0
- Pin 2 drops 180ms later

**Step 2 — Enriching with location data:**
- Pins 3 and 4 drop, 180ms apart
- Route path draws pin1→pin2→pin3: route-draw 1000ms

**Step 3 — Building day plan:**
- Pin 5 drops
- Remaining route segments draw
- Full path pulses once: stroke-opacity 0.5→0.9→0.5, 280ms ease-out

**Step 4 — Complete:**
- Entire SVG: scale 1→1.04→1 over 320ms spring-soft — clean success confirmation
- Overlay begins exit sequence

---

## 2.4 Step Label

Container: min-height 20px, overflow hidden.

**Swap animation (on new SSE message):**
- Outgoing: translateY 0→-6px, opacity 1→0, 140ms accelerate
- Incoming: translateY 6px→0, opacity 0→1, 180ms decelerate

**Step text:**
- Step 0: "Fetching video transcripts..."
- Step 1: "Extracting places..."
- Step 2: "Enriching places with location data..."
- Step 3: "Building your day-by-day plan..."

**Footer note copy changes:**
- Default: "This takes about 30–90 seconds."
- After 60s: "Almost there — finishing up..."
- After 90s: "Taking a little longer than usual..." (color: #F6A609)

---

## 2.5 Progress Bar

**Container:** height 4px (thinner, more Uber), border-radius 9999px, background #E2E2E2, margin-top 24px, overflow hidden.

**Fill div:** height 4px, border-radius 9999px, background #000000 (pure black progress fill).

**Step → width mapping:**
| SSE step | Fill width |
|---|---|
| 0 (start) | 15% |
| 1 | 40% |
| 2 | 70% |
| 3 | 95% |
| 4 (complete) | 100% |

Width transition: 500ms decelerate.

**Shimmer overlay:** gradient left-to-right over filled portion, 1600ms linear infinite.

---

## 2.6 Overlay Exit Animation

1. Card: opacity 1→0, translateY 0→-6px, 280ms accelerate
2. Backdrop: opacity 1→0, 200ms accelerate — starts 40ms into card exit
3. Results page: opacity 0→1, 400ms decelerate — starts simultaneously

---

## 2.7 Mobile (< 768px)
- Card: width calc(100% - 32px), max-width 480px, padding 28px
- Mini-map SVG: scale to 64×64px

---

## 2.8 Accessibility
- Overlay: `role="status"` `aria-live="polite"` `aria-label="Building your itinerary"`
- Step label: live region announces each step text change
- Progress bar: `role="progressbar"` `aria-valuenow={percent}` `aria-valuemin="0"` `aria-valuemax="100"`
- Focus management: set `tabIndex=-1` on card, programmatically focus on mount
- Non-dismissable: no close button, no Escape handler
- `prefers-reduced-motion`: pin animations instant, route draw instant, card entrance instant

---

*End of landing-page-spec.md*
