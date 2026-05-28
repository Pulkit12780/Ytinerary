# Ytinerary — Component Design Specifications
*v2.0 | Uber Design Language | 2026-05-28 | Source: design-spec.md | For Frontend Engineer*

---

## Reading this document

- All measurements in px unless noted
- `var(--color-day-N)` = actual day color hex (Day1=#276EF1, Day2=#06C167, Day3=#FF974A, Day4=#7356BF, Day5=#E85D99)
- Transition shorthand: `fast`=100ms ease-out, `base`=180ms ease-out, `spring-soft`=300ms cubic-bezier(0.34,1.40,0.64,1), `decelerate`=280ms cubic-bezier(0.05,0.7,0.1,1), `accelerate`=180ms cubic-bezier(0.3,0,0.8,0.15)
- Font: 'Uber Move', 'Manrope', -apple-system, system-ui, sans-serif (loaded as Manrope from Google Fonts)
- [COMPLEXITY: LOW/MEDIUM/HIGH] marks implementation effort

---

## 1. URLInputRow [COMPLEXITY: HIGH]

Single YouTube URL input that transforms into a video preview card on valid URL detection.

### Visual Structure — Empty State
```
┌─────────────────────────────────────────────┐ [×]
│  ▶  Paste a YouTube URL...                 │
└─────────────────────────────────────────────┘
[+ Add another video]
```

### Dimensions & Spacing
- Container: width 100%, position relative
- Input: height 48px, width 100%, border-radius 8px, padding 0 14px 0 40px
- Leading icon (▶): 14px, position absolute left 14px, vertically centered
- Remove [×] button: 28×28px, border-radius 9999px, right of row
- Row gap: 8px
- "Add another video" button: margin-top 8px

### Input States
| State | Border | Background | Icon color |
|---|---|---|---|
| Rest | 1px solid #E2E2E2 | #FFFFFF | #8A8A8A |
| Hover | 1px solid #000000 | #FFFFFF | #8A8A8A |
| Focus | 2px solid #000000 + glow-primary | #FFFFFF | #8A8A8A |
| Typing valid URL | 1px solid #E2E2E2 | #FFFFFF | #C7282D (YouTube red) |

Leading ▶ color: #8A8A8A → #C7282D when value contains "youtube" / "youtu.be". Transition: fast.

### Valid URL Detection Transform [KEY MOMENT]
Triggered on: `youtube.com/watch?v=` or `youtu.be/`.

```
┌──────────────────────────────────────────────────────┐ [×]
│  [thumb 64×36]  Mumbiker Nikhil's Jaipur Vlog        │
│                 12:34 · youtube.com/watch?v=...      │
└──────────────────────────────────────────────────────┘
```

**Sequence:**
1. Row height: 48px → 64px over spring-soft
2. Input: opacity 1→0 80ms, then display:none after preview animation
3. Preview div:
   - Thumbnail: 64×36px, border-radius 4px, object-fit cover
   - Source: `https://img.youtube.com/vi/{VIDEO_ID}/mqdefault.jpg`
   - Thumbnail entrance: opacity 0→1, scale 0.94→1, 200ms ease-out
   - Thumbnail skeleton: #E2E2E2 bg + shimmer while loading
   - Title: Manrope SemiBold 13px, #000000, single-line, ellipsis
   - Meta: Manrope Regular 11px, #8A8A8A
4. Border flashes: #E2E2E2 → #05944F for 500ms → back to #E2E2E2
5. Green ✓ at right edge: scale 0→1.1→1, 280ms spring-soft

### Row Animations
- Add: height 0→48px, opacity 0→1, translateX -6px→0, 200ms decelerate
- Remove: height 48px→0, opacity 1→0, translateX 0→10px, 160ms accelerate

### "Add another video" button
- Style: Manrope Medium (500) 14px, #000000, leading + icon, underline on hover
- Hover: underline + + icon rotates 90° over 280ms ease-out
- Click: adds new URLInputRow with enter animation

### Accessibility
- `aria-label="YouTube video URL [N]"` on each input
- Remove: `aria-label="Remove video [N]"`
- Add: `aria-label="Add another video URL"`

---

## 2. Map Pin — Day Pin [COMPLEXITY: MEDIUM]

Custom Leaflet DivIcon. SVG teardrop with day number.

### SVG Template
```svg
<svg width="28" height="36" viewBox="0 0 28 36" overflow="visible">
  <path d="M14 0C6.268 0 0 6.268 0 14c0 9.333 14 22 14 22s14-12.667 14-22C28 6.268 21.732 0 14 0z"
        fill="{{DAY_COLOR}}" stroke="#FFFFFF" stroke-width="2.5"/>
  <text x="14" y="18" text-anchor="middle" dominant-baseline="central"
        fill="#FFFFFF" font-family="Uber Move, Manrope, sans-serif" font-size="11" font-weight="700">
    {{DAY_NUMBER}}
  </text>
</svg>
```

### Leaflet Icon Config
```
iconSize:    [28, 36]
iconAnchor:  [14, 36]   ← bottom tip
popupAnchor: [0, -36]
```

### transform-origin
`transform-origin: 50% 100%` — all scale transforms pivot from bottom tip.

### States
| State | Scale | Fill opacity | SVG filter | Ring | Trigger |
|---|---|---|---|---|---|
| Rest | 1.0 | 1.0 | drop-shadow(0 2px 4px rgba(0,0,0,0.25)) | none | default |
| Hover | 1.12 | 1.0 | drop-shadow(0 4px 8px rgba(0,0,0,0.35)) | none | mouseover pin OR card sync |
| Active | 1.25 | 1.0 | drop-shadow(0 4px 8px rgba(0,0,0,0.35)) | 2px white, 4px outside | pin click or day filtered |
| Dimmed | 1.0 | 0.3 | none | none | another day filtered |
| Idle pulse | 1.0 | 1.0 | rest shadow | pulse-ring 8s | first pin/day, page at rest |

State transitions: scale 180ms ease-out, opacity 180ms ease-out, filter 180ms ease-out.

### Active White Ring
`box-shadow: 0 0 0 2px #FFFFFF, 0 0 0 5px rgba(255,255,255,0.25)` — appears 180ms ease-out.

### Day-Tinted Halo (active pins)
80×80px behind pin, centered: `radial-gradient(circle, rgba(DAY_RGB, 0.18) 0%, transparent 65%)`, opacity 0.5.

### Pin Drop Entrance
```
keyframe: pin-drop 400ms ease-decelerate backwards
delay: (dayIndex × 240ms) + (pinIndex × 50ms)
cap: delay > 1500ms → use 0ms
```
On landing: pin emits ONE pulse-ring (day color 40% opacity, 1600ms, once).

### Cross-sync
- Card hover → pin hover state + `map.panTo({animate:true, duration:0.4})` if near edge
- Pin hover → sidebar card: border-left 3px solid day-N, shadow-card-hover, auto-scroll 300ms

### Idle Pulse Ring
First pin of each day, every 8s, only when no day filtered:
```css
@keyframes pulse-ring-emit {
  0%   { box-shadow: 0 0 0 0px rgba(R,G,B,0.40); }
  100% { box-shadow: 0 0 0 18px rgba(R,G,B,0.00); opacity: 0; }
}
duration: 1600ms ease-out, runs once per 8s interval
```

---

## 3. Map Pin — Hotel Pin [COMPLEXITY: LOW]

### SVG Template
```svg
<svg width="32" height="32" viewBox="0 0 32 32" overflow="visible">
  <rect x="1" y="1" width="30" height="30" rx="6"
        fill="#000000" stroke="#FFFFFF" stroke-width="2.5"/>
  <text x="16" y="17" text-anchor="middle" dominant-baseline="central"
        fill="#FFFFFF" font-size="15">⌂</text>
</svg>
```

### Leaflet Icon Config
```
iconSize:    [32, 32]
iconAnchor:  [16, 16]   ← center
popupAnchor: [0, -20]
```

### Rules
- Always full opacity — never dimmed by day filter
- No entrance animation — simple opacity fade 0→1, 200ms
- Hover: scale 1.05, 100ms ease-out
- No selected state

---

## 4. Map Tooltip (Leaflet Popup) [COMPLEXITY: LOW]

### Visual
```
┌──────────────────────────────┐
│  ● Day 1  Amber Fort         │
│  Temple · ⭐ 4.7             │
└──────────────────────────────┘
```

### Spec
- Background: #FFFFFF
- Border: 1px solid #E2E2E2
- border-radius: 8px
- Shadow: 0 4px 16px rgba(0,0,0,0.14)
- Padding: 10px 14px
- No close button, no tip triangle

### Typography
- Place name: Manrope SemiBold (600) 14px, #000000
- Category + rating: Manrope Regular 13px, #545454, margin-top 2px
- Day dot: 8px circle, fill day-N color, margin-right 6px

### Leaflet CSS Overrides
```css
.leaflet-popup-content-wrapper {
  border-radius: 8px;
  padding: 0;
  box-shadow: 0 4px 16px rgba(0,0,0,0.14);
  border: 1px solid #E2E2E2;
}
.leaflet-popup-content { margin: 0; }
.leaflet-popup-tip-container { display: none; }
.leaflet-popup-close-button { display: none; }
```

### Animations
- Show: opacity 0→1, translateY 3px→0, 140ms ease-out
- Hide: opacity 1→0, 100ms ease-in

---

## 5. Day Route Polyline [COMPLEXITY: MEDIUM]

### Leaflet Options
```javascript
{
  color:       DAY_COLOR_HEX,
  weight:      2.5,
  opacity:     0.80,
  dashArray:   '4 6',
  lineCap:     'round',
  lineJoin:    'round',
  interactive: false
}
```

### Visibility Logic
| Condition | Action |
|---|---|
| Page load | Hidden |
| DaySectionHeader click (activate) | Add, animate entrance |
| DaySectionHeader click (deactivate) | Exit, removeLayer |
| Different day clicked | Remove old, draw new |
| Pin hovered >400ms | Draw preview at opacity 0.45 |

### Entrance
```javascript
const path = layer._path
const len = path.getTotalLength()
path.style.strokeDasharray = len
path.style.strokeDashoffset = len
requestAnimationFrame(() => {
  path.style.transition = 'stroke-dashoffset 1000ms ease-out'
  path.style.strokeDashoffset = '0'
})
```
Fallback: opacity 0→0.80, 280ms ease-out.

### Exit
opacity 0.80→0, 180ms ease-out, then removeLayer.

---

## 6. DaySectionHeader [COMPLEXITY: MEDIUM]

### Visual
```
┌─────────────────────────────────────────────────────────┐
│ ▌ DAY 1  ·  Old City & Bazaars              5 places    │
└─────────────────────────────────────────────────────────┘
```

### Container
- padding: 12px 12px 8px
- border-radius: 8px
- cursor: pointer
- position: relative; overflow: hidden (ripple)
- margin-bottom: 4px
- display: flex; align-items: center

Below: 1px solid #F0F0F0 separator.

### Left Accent Bar
- Width: 3px, Height: 16px
- Background: var(--color-day-N)
- border-radius: 9999px
- margin-right: 10px; flex-shrink: 0

### Typography
- "DAY 1": Manrope SemiBold (600) 13px, #000000, uppercase, letter-spacing 0.06em
- " · ": separator, #8A8A8A
- Cluster name: Manrope Regular 13px, #545454, flex:1, ellipsis
- "5 places": Manrope Regular 12px, #8A8A8A, margin-left auto

### States
| State | Background | Accent (W×H) | Day label color | Opacity |
|---|---|---|---|---|
| Rest | transparent | 3×16 | #000000 | 1.0 |
| Hover | #F0F0F0 | 3×18 | #000000 | 1.0 |
| Active | var(--color-day-N-subtle) | 4×20 | var(--color-day-N) | 1.0 |
| Sibling-dimmed | transparent | 3×16 | #000000 | 0.5 |

Transitions: background 180ms ease-out, opacity 180ms ease-out, accent bar: 280ms spring-soft.

### Click Ripple
Inject `<span>` at click coordinates. Expand 0→640px, day-N-subtle color, opacity 0.5→0, 300ms decelerate. Remove on animationend.

### Active Count Pill
Shows "5 stops" when active:
- border-radius 9999px, padding 2px 8px, bg day-N-subtle, Manrope Medium 11px day-N
- Entrance: translateX 6px→0, opacity 0→1, 180ms ease-out

### Entrance (page load)
slide-up-fade 280ms decelerate, 80ms after last card of prior day.

### Accessibility
`role="button"`, `tabIndex=0`, `aria-pressed`, Enter+Space activate. `focus-visible` ring.

---

## 7. PlaceCard — Collapsed [COMPLEXITY: MEDIUM]

### Visual
```
┌───────────────────────────────────────────────┐
│  Amber Fort                    [Day 1 badge]  │
│  Temple · Historic Site   ⭐ 4.7              │
│  📹 Mumbiker Nikhil's Jaipur Vlog             │
└───────────────────────────────────────────────┘
```

### Container
- element: `<article>`
- background: #FFFFFF
- border: 1px solid #E2E2E2
- border-left: 3px solid transparent → var(--color-day-N) on hover/sync
- border-radius: 10px
- padding: 12px 16px
- shadow: shadow-subtle
- margin-bottom: 8px; cursor: pointer
- position: relative; overflow: hidden

### Row 1 — Title + Badge
flex, justify-content space-between, align-items flex-start

- Place name: Manrope SemiBold (600) 14px, #000000, flex:1, padding-right 8px
- Day badge: border-radius 9999px, padding 2px 8px, bg day-N-subtle, Manrope Medium 11px day-N, letter-spacing 0.04em

### Row 2 — Category + Rating
flex, gap 4px, margin-top 3px

- Category: Manrope Regular 13px, #545454
- "·" separator: #8A8A8A
- "⭐ 4.7": Manrope Regular 13px, #545454

### Row 3 — Video Source
flex, margin-top 4px

- 📹: emoji at 13px
- Title: Manrope Regular 12px, #8A8A8A → #545454 on parent hover (120ms), ellipsis

### Expand caret
Lucide ChevronDown, 16px, #8A8A8A, position absolute top-right corner, padding 12px.
Rotates 0°→180° (280ms ease-out) on expand.

### States
| State | Border-left | Shadow | Transform |
|---|---|---|---|
| Rest | 3px transparent | shadow-subtle | none |
| Hover | 3px var(--color-day-N) | shadow-card-hover | none (no lift — Uber cards don't lift) |
| Pin-sync | 3px var(--color-day-N) | shadow-card-hover | none |
| Press | 3px var(--color-day-N) | shadow-subtle | scale(0.99) |

All transitions: 180ms ease-out. Press: 80ms.

> Note: No translateY(-2px) lift — Uber cards use border/shadow changes instead of vertical lift.

### Unresolved State
- Name: #8A8A8A, italic
- Row 2: "Location not found"
- Row 3: absent
- Border: 1px dashed #E2E2E2
- Hover: bg #FFFFFF→#F6F6F6, no border change

### Entrance
slide-up-fade, 40ms stagger within day group.

### Accessibility
`role="article"`, `aria-expanded`, `tabIndex=0`, Enter+Space expand.

---

## 8. PlaceCard — Expanded [COMPLEXITY: HIGH]

### Visual
```
┌───────────────────────────────────────────────────────┐
│  [Photo — 100% wide, 160px tall, cover crop]          │
├───────────────────────────────────────────────────────┤
│  Amber Fort                         [Day 1 badge]    │
│  Temple · Historic Site   ⭐ 4.7                     │
│  Mon–Sun   8:00–17:30                                │
│                                                       │
│  Spectacular hilltop fort...                         │
│                                                       │
│  📹 Mumbiker Nikhil's Jaipur Vlog          ↗        │
│  📹 Curly Tales Rajasthan                  ↗        │
│                                                       │
│  [Remove from itinerary]                              │
└───────────────────────────────────────────────────────┘
```

### Photo Area
- height 160px, width 100%, object-fit cover
- border-radius: 10px 10px 0 0
- Skeleton: #E2E2E2 + shimmer
- Photo entrance: opacity 0→1, 280ms decelerate
- Hover (expanded): photo scale 1→1.02, 360ms ease-out (overflow:hidden)

### Hours
- Manrope Regular 12px, #8A8A8A, each day on own line
- Today's row: bg #EAF0FE, padding 2px 6px, border-radius 4px, color #000000

### Description
- Manrope Regular 14px, #545454, line-height 1.5
- max 3 lines (-webkit-line-clamp: 3)

### Video Links
- Manrope Regular 13px, #000000 (underline on hover), target _blank
- Hover: underline + ↗ icon translate(+2px, -2px), 180ms ease-out

### Remove Button
- width 100%, height 40px, margin-top 12px
- border: 1px solid #E2E2E2, border-radius 8px
- Manrope Medium (500) 14px, #C7282D
- Hover: bg #FFF0F0, border-color #C7282D, 180ms ease-out

**Remove exit:**
1. Card: translateX 0→16px, opacity 1→0, 240ms accelerate
2. Pin: scale 1→0, opacity 1→0, 240ms ease-out
3. DOM removal

### Expand Animation
- max-height 80px → 600px, 280ms decelerate
- Content fades in 60ms after expand (photo 200ms, text 140ms)

### Collapse Animation
- max-height 600px → 80px, 180ms accelerate
- Content opacity 1→0 first (80ms), then container collapses

---

## 9. ShareButton [COMPLEXITY: MEDIUM]

### Layout
- height 36px, padding 0 14px
- bg #FFFFFF, border 1px solid #E2E2E2, border-radius 8px
- display inline-flex, align-items center, gap 6px

### Content
- Share2 icon (Lucide) 14px, #545454
- "Share itinerary" — Manrope Medium (500) 14px, #000000

### States
| State | Background | Border | Color |
|---|---|---|---|
| Rest | #FFFFFF | #E2E2E2 | #000000 |
| Hover | #F6F6F6 | #000000 | #000000 |
| Copied | #E6FAF0 | #05944F | #05944F |

Hover: border goes black (very Uber), 100ms ease-out.
Press: container scale 0.97, 80ms.

### Copied State Sequence (t=0 on clipboard success)
1. Background+border+color transition, 100ms ease-out
2. Label swaps: "Share itinerary" → "Link copied!"
3. Icon: Share2 → Check (Lucide), crossfade 80ms
4. Check stroke-draw: stroke-dashoffset 24→0, 240ms ease-out (delay 60ms)
5. Hold 2000ms → reset, 180ms fast

### Accessibility
`aria-live="polite"` on label. Focus ring.

---

## 10. ErrorBanner [COMPLEXITY: LOW]

### Layout
```
⚠  Some places couldn't be processed.   [×]
```
- bg #FFFBEB, border 1px solid #F6A609, border-radius 8px, padding 10px 14px
- display flex, align-items center, gap 8px
- position sticky, top 60px, z-index 11, margin-bottom 8px

### Content
- AlertTriangle (Lucide) 15px, #F6A609
- Manrope Regular 14px, #000000
- Dismiss [×]: 24×24px, `aria-label="Dismiss"`, hover bg rgba(246,166,9,0.1)

### Animations
- Enter: translateY(-6px)→0, opacity 0→1, 180ms ease-out
- Exit: translateY(0)→-6px, opacity 1→0, 140ms accelerate

### Variants
| Type | Background | Border | Text |
|---|---|---|---|
| Warning | #FFFBEB | #F6A609 | #000000 |
| Error | #FFF0F0 | #C7282D | #000000 |

Accessibility: `role="alert"` (error) or `role="status"` (warning).

---

## 11. UnresolvedPlacePill [COMPLEXITY: LOW]

```
[ Amber Fort  × ]
```

- display inline-flex, align-items center, height 28px, padding 0 10px
- bg #F6F6F6, border 1px dashed #E2E2E2, border-radius 9999px, gap 6px
- Text: Manrope Regular 13px, #8A8A8A
- Remove ×: 16×16px, color #8A8A8A → #C7282D on hover (100ms)

Container: `<details>` disclosure. Summary: "Unresolved places (N)" Manrope Medium 14px, #8A8A8A.
Pill removal: scale 1→0.8, opacity 1→0, 120ms ease-out.

---

## 12. Skeleton Loaders [COMPLEXITY: LOW]

### Universal Shimmer
```css
.skeleton {
  background-color: #F0F0F0;
  background-image: linear-gradient(90deg, transparent 0%, rgba(255,255,255,0.80) 50%, transparent 100%);
  background-size: 200% 100%;
  animation: shimmer 1600ms linear infinite;
}
```
All skeletons: `aria-hidden="true"`.

### Variants
| Name | Height | Width | border-radius |
|---|---|---|---|
| PlaceCard | 56px | 100% | 10px |
| Photo | 160px | 100% | 10px 10px 0 0 |
| Text line full | 12px | 100% | 4px |
| Text line medium | 12px | 75% | 4px |
| Text line short | 12px | 55% | 4px |
| Day section header | 40px | 100% | 8px |

---

## 13. Button System [COMPLEXITY: LOW]

### Primary (Black — Uber CTA)
height 48px, padding 0 24px, bg #000000, Manrope Bold (700) 16px, #FFFFFF, border-radius 8px.
Hover: bg #1A1A1A, 100ms ease-out.
Press: scale 0.98, 80ms.
Disabled: bg #E2E2E2, color #8A8A8A, cursor not-allowed.
Loading: white spinner 18px (border 2px rgba(255,255,255,0.3), border-top #FFFFFF, 600ms linear infinite).

### Secondary
height 40px, bg #FFFFFF, border 1px solid #E2E2E2, Manrope Medium (500) 14px, #000000, border-radius 8px.
Hover: border-color #000000, 100ms ease-out.
Destructive: color #C7282D, hover border-color #C7282D, bg #FFF0F0.

### Ghost
height 36px, bg transparent, no border, Manrope Regular 14px, #545454, border-radius 8px.
Hover: bg #F6F6F6, color #000000, 100ms.

### Icon-only
28–32px square, border-radius 9999px, bg transparent.
Hover: bg #F0F0F0. Always needs `aria-label`.

### Universal Rules
- `focus-visible`: `box-shadow: 0 0 0 3px rgba(0,0,0,0.12)`
- Min tap target: 28×28px
- Keyboard: Enter + Space
- Disabled: `aria-disabled="true"`, no transitions

---

## 14. Global Focus Ring

```css
:focus-visible {
  outline: none;
  box-shadow: 0 0 0 3px rgba(0, 0, 0, 0.12);
  border-radius: inherit;
}
```

For inputs (where border-black on hover is used), switch to:
```css
input:focus-visible {
  box-shadow: 0 0 0 3px rgba(6, 193, 103, 0.25);
}
```

---

## 15. Animation Keyframes Registry

```css
@keyframes pin-drop {
  0%   { transform: translateY(-32px) scale(0.7); opacity: 0; }
  100% { transform: translateY(0) scale(1); opacity: 1; }
}

@keyframes slide-up-fade {
  0%   { transform: translateY(8px); opacity: 0; }
  100% { transform: translateY(0); opacity: 1; }
}

@keyframes shimmer {
  0%   { background-position: -200% 0; }
  100% { background-position: 200% 0; }
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

---

*End of components-spec.md*
