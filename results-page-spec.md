# Ytinerary — Results Page Design Spec
*v2.0 | Uber Design Language | 2026-05-28 | Source: design-spec.md §4 | For Frontend Engineer*

---

## Page Layout — Desktop (1280px+)

```
┌──────────────────────────────────────────────────────────────────────────┐
│  TOPBAR  h=60px  bg=#FFFFFF  border-bottom 1px solid #E2E2E2             │
│  [← New Search]  [Y·tinerary logo]                                       │
├─────────────────────────────────────────────┬────────────────────────────┤
│                                             │                            │
│  MAP PANEL                                  │  SIDEBAR PANEL             │
│  flex: 1                                    │  width: 400px (fixed)      │
│  height: calc(100vh - 60px)                 │  height: calc(100vh - 60px)│
│  position: sticky; top: 60px               │  overflow-y: auto          │
│  overflow: hidden                           │  background: #F6F6F6       │
│                                             │  border-left:1px solid     │
│  Leaflet map fills 100% × 100%              │  #E2E2E2                   │
│  No padding. Tiles touch all edges.         │                            │
│                                             │  ┌──────────────────────┐  │
│  [Sidebar collapse toggle]                  │  │ STICKY HEADER  top:0 │  │
│  28×28px circle, overlaps left border       │  │ bg:#F6F6F6           │  │
│  position: absolute left:-14px              │  │ [Destination name]   │  │
│  top: 50vh                                  │  │ [14 places · 4 days] │  │
│  z-index: 10                                │  │ [ShareButton]  →     │  │
│                                             │  └──────────────────────┘  │
│  [Map legend — bottom-left]                 │                            │
│  [Zoom controls — top-right]                │  [DaySectionHeader Day 1]  │
│                                             │  [PlaceCard × up to 5]     │
│                                             │  [DaySectionHeader Day 2]  │
│                                             │  [PlaceCard × up to 4]     │
│                                             │  ...                       │
│                                             │  [More to Explore]         │
│                                             │  [Unresolved places]       │
│                                             │  [32px bottom padding]     │
│                                             │                            │
└─────────────────────────────────────────────┴────────────────────────────┘
```

---

## 1. Topbar — Results Variant

### Same as landing topbar PLUS:
- "← New Search" link, left of logo
  - Font: Manrope Medium (500) 14px, #545454
  - Content: ← arrow + "New Search"
  - Hover: color #545454→#000000, arrow translateX -2px, 100ms ease-out
  - Links to `/`

---

## 2. Map Panel

### CSS Properties
```
flex: 1
height: calc(100vh - 60px)
position: sticky
top: 60px
overflow: hidden
```

### Leaflet Map
- Tile URL: `https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png`
- On load: `map.fitBounds(allCoordinates, {padding: [48, 48]})`
- maxZoom: 18, minZoom: 3
- Attribution: bottom-right, opacity 0.6, font-size 11px

### Map Controls (Zoom buttons)
- Position: top-right of map panel
- Style: background #FFFFFF, border-radius 8px, shadow-md, border 1px solid #E2E2E2
- Text: Manrope Regular 14px, #000000

### Map Legend
- Position: bottom-left corner (absolute)
- Container: bg #FFFFFF, border-radius 8px, shadow-sm, border 1px solid #E2E2E2, padding 8px 14px
- Contents: one row per day — 8px filled circle + "Day N" label
- Text: Manrope Regular 13px, #545454
- Row gap: 6px

---

## 3. Sidebar Panel

### CSS Properties
```
width: 400px
flex-shrink: 0
height: calc(100vh - 60px)
overflow-y: auto
background: #F6F6F6
border-left: 1px solid #E2E2E2
```

### Scrollbar Styling
```css
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-thumb { background: #E2E2E2; border-radius: 2px; }
::-webkit-scrollbar-track { background: transparent; }
```

### Padding
- padding: 16px 16px 32px

### Accessibility
`role="complementary"`, `aria-label="Trip itinerary"`

---

## 4. Sidebar Sticky Header

```
position: sticky
top: 0
z-index: 10
background: #F6F6F6
padding: 16px 0 12px
border-bottom: 1px solid #E2E2E2
display: flex
align-items: center
```

### Content
- Left column (flex):
  - Destination name: Manrope SemiBold (600) 17px, #000000
  - Place count: Manrope Regular 14px, #8A8A8A — "14 places · 4 days"
- Right: ShareButton (see components-spec.md §9)

---

## 5. Sidebar Collapse Toggle

### Position & Visual
- Position: absolute, left -14px, top 50vh
- Visual: 28×28px circle
- Background: #FFFFFF
- Border: 1px solid #E2E2E2
- Shadow: shadow-sm
- z-index: 10

### Icon
- ChevronLeft (Lucide, 14px, #8A8A8A) when expanded
- ChevronRight when collapsed

### States
| State | Shadow | Transform |
|---|---|---|
| Rest | shadow-sm | none |
| Hover | shadow-md | scale(1.06) |
| Press | shadow-subtle | scale(0.96) |

Hover: 100ms ease-out. Press: 80ms.

### On Click
1. Icon rotates 180° over 280ms ease-out
2. Sidebar panel: width 400px→0, overflow hidden, transition 300ms spring-soft
3. Map panel grows via flex, transition 300ms spring-soft

**Expanding back:** width 0→400px, spring-soft with subtle ~1.5% overshoot.

**Collapsed:** toggle floats against map tiles — keep shadow-md so it reads.

---

## 6. Sidebar Content Order

1. **For each day cluster (Day 1 → Day N):**
   - `DaySectionHeader`
   - Up to 5 `PlaceCard` components

2. **"More to Explore" section** (overflow places):
   - Heading: "More to Explore" — Manrope SemiBold 14px, #000000
   - Sub-heading: "These places didn't make the main plan" — Manrope Regular 13px, #8A8A8A
   - PlaceCards with no day badge

3. **Unresolved places** (geocoding failures):
   - `<details>` disclosure
   - Summary: "Unresolved places (N)"

4. **32px bottom padding**

---

## 7. Map + Sidebar Cross-Sync

### Card hover → Pin sync
When a PlaceCard is hovered:
1. Matching map pin enters hover state (scale 1.12, elevated shadow)
2. If near map edge: `map.panTo(pinLatLng, {animate: true, duration: 0.4})`

### Pin hover → Card sync
When a map pin is hovered:
1. Matching PlaceCard: border-left 3px solid var(--color-day-N), shadow-card-hover (180ms ease-out)
2. If out of viewport: `card.scrollIntoView({behavior: 'smooth', block: 'nearest'})`

### Day filter mode (DaySectionHeader click)
Toggle — click to activate, click again to deactivate.

**Activate:**
- All other day pins: opacity 0.3 (180ms ease-out)
- All other DaySectionHeaders + cards: opacity 0.5 (180ms)
- Active day pins: scale 1.25
- Day route polyline: draws for this day
- Announce via `aria-live="polite"`: "Showing Day N: [cluster name]. N places."

**Deactivate:**
- All pins and sections return to normal (180ms ease-out)
- Route polyline: exit, removeLayer

---

## 8. Results Page Entrance Sequence

| t= | Event |
|---|---|
| 0ms | Topbar already visible |
| 0ms | Sidebar slides in: translateX 400px→0, opacity 0→1, 400ms decelerate |
| 0ms | Map tiles begin loading. #F0F0F0 skeleton shows behind tiles. |
| 400ms | Map pins begin dropping: delay = dayIndex×240ms + pinIndex×50ms |
| 400ms+ | Sidebar cards: slide-up-fade, 40ms stagger within each day group |
| per pin | Each pin emits one pulse-ring on landing |
| all pins down | Idle: first pin of each day begins 8s pulse-ring cycle |

---

## 9. Mobile Layout (< 768px)

```
┌──────────────────────────────────────────┐
│  TOPBAR  h=60px                          │
├──────────────────────────────────────────┤
│                                          │
│  MAP — fills remaining viewport          │
│  (minus bottom-sheet peek ~120px)        │
│                                          │
├──────────────────────────────────────────┤
│  BOTTOM SHEET                            │
│  ▬ handle bar (32×4px, #E2E2E2 centered)│
│  bg: #F6F6F6                             │
│  border-radius: 16px 16px 0 0            │
│  shadow: shadow-xl (top edge)            │
└──────────────────────────────────────────┘
```

### Bottom Sheet Snap Points
| State | Height visible | Map visible |
|---|---|---|
| Peek | ~120px | Fully visible |
| Half | ~50vh | Partially visible |
| Full | ~90vh | Mostly hidden |

Transitions: 300ms spring-soft. Momentum-based snap on drag.

### Sheet Behavior
- Handle tap/drag: cycles snap points
- Pin tap in Peek: sheet snaps to Half, scrolls to matching card
- `role="dialog"` `aria-label="Trip itinerary"`

---

## 10. Accessibility

| Element | ARIA |
|---|---|
| Main content | `role="main"` |
| Map | `role="application"` `aria-label="Interactive trip map"` |
| Sidebar | `role="complementary"` `aria-label="Trip itinerary"` |
| Sidebar toggle | `aria-label="Collapse sidebar"` / `"Expand sidebar"` (dynamic) |
| Day filter | `aria-live="polite"` announces active day |
| Place removal | `aria-live="polite"` announces removal |
| Mobile sheet | `role="dialog"` `aria-label="Trip itinerary"` |

---

*End of results-page-spec.md*
