# Ytinerary — Website Design Specification
*Version 1.0 | 2026-05-17 | Desktop-first website (min 1280px)*

---

## 0. Design Principles

- **Calm precision** — no visual noise. Every element earns its place.
- **Trust through restraint** — muted palette, no gradients on data, no gamification.
- **Desktop-first** — primary user is a pre-trip researcher at a desk with multiple tabs open.
- **Map is the hero** — the results page exists to serve the map. Nothing competes with it.

---

## 1. Design Tokens

### 1.1 `tokens.json`

```json
{
  "color": {
    "background": "#F8F7F4",
    "surface": "#FFFFFF",
    "surface-elevated": "#FFFFFF",
    "border": "#E4E2DC",
    "border-subtle": "#EDECEA",

    "text-primary": "#1A1917",
    "text-secondary": "#5C5A55",
    "text-muted": "#9B9891",
    "text-inverse": "#FFFFFF",

    "accent": "#2563EB",
    "accent-hover": "#1D4ED8",
    "accent-subtle": "#EFF4FF",
    "accent-foreground": "#FFFFFF",

    "error": "#DC2626",
    "error-subtle": "#FEF2F2",
    "warning": "#D97706",
    "warning-subtle": "#FFFBEB",
    "success": "#16A34A",
    "success-subtle": "#F0FDF4",

    "day-1": "#2563EB",
    "day-2": "#16A34A",
    "day-3": "#D97706",
    "day-4": "#9333EA",
    "day-5": "#DB2777",
    "day-1-subtle": "#EFF4FF",
    "day-2-subtle": "#F0FDF4",
    "day-3-subtle": "#FFFBEB",
    "day-4-subtle": "#FAF5FF",
    "day-5-subtle": "#FDF2F8",

    "hotel": "#0F172A",
    "hotel-subtle": "#F1F5F9",

    "overlay": "rgba(15, 23, 42, 0.72)"
  },

  "font": {
    "family-heading": "'Inter', system-ui, sans-serif",
    "family-body": "'Inter', system-ui, sans-serif",
    "family-mono": "'JetBrains Mono', 'Fira Code', monospace"
  },

  "fontSize": {
    "xs": "11px",
    "sm": "13px",
    "base": "14px",
    "md": "15px",
    "lg": "17px",
    "xl": "20px",
    "2xl": "24px",
    "3xl": "30px",
    "4xl": "36px"
  },

  "fontWeight": {
    "regular": "400",
    "medium": "500",
    "semibold": "600",
    "bold": "700"
  },

  "lineHeight": {
    "tight": "1.2",
    "snug": "1.35",
    "normal": "1.5",
    "relaxed": "1.65"
  },

  "letterSpacing": {
    "tight": "-0.02em",
    "normal": "0em",
    "wide": "0.04em",
    "wider": "0.08em"
  },

  "spacing": {
    "1": "4px",
    "2": "8px",
    "3": "12px",
    "4": "16px",
    "5": "20px",
    "6": "24px",
    "8": "32px",
    "10": "40px",
    "12": "48px",
    "16": "64px",
    "20": "80px",
    "24": "96px"
  },

  "borderRadius": {
    "sm": "4px",
    "md": "8px",
    "lg": "12px",
    "xl": "16px",
    "2xl": "24px",
    "full": "9999px"
  },

  "shadow": {
    "sm": "0 1px 2px 0 rgba(0,0,0,0.05)",
    "md": "0 4px 6px -1px rgba(0,0,0,0.08), 0 2px 4px -2px rgba(0,0,0,0.05)",
    "lg": "0 10px 15px -3px rgba(0,0,0,0.08), 0 4px 6px -4px rgba(0,0,0,0.05)",
    "xl": "0 20px 25px -5px rgba(0,0,0,0.10), 0 8px 10px -6px rgba(0,0,0,0.05)",
    "tooltip": "0 4px 16px rgba(0,0,0,0.14)",
    "card-hover": "0 8px 24px rgba(0,0,0,0.10)"
  },

  "transition": {
    "fast": "120ms ease-out",
    "base": "200ms ease-out",
    "slow": "320ms ease-out",
    "spring": "400ms cubic-bezier(0.34, 1.56, 0.64, 1)"
  },

  "zIndex": {
    "sidebar": "10",
    "tooltip": "20",
    "overlay": "50",
    "toast": "60"
  }
}
```

---

### 1.2 Tailwind Config Extension

```js
// tailwind.config.js — theme.extend block
theme: {
  extend: {
    colors: {
      background: '#F8F7F4',
      surface: '#FFFFFF',
      border: {
        DEFAULT: '#E4E2DC',
        subtle: '#EDECEA',
      },
      text: {
        primary: '#1A1917',
        secondary: '#5C5A55',
        muted: '#9B9891',
        inverse: '#FFFFFF',
      },
      accent: {
        DEFAULT: '#2563EB',
        hover: '#1D4ED8',
        subtle: '#EFF4FF',
        foreground: '#FFFFFF',
      },
      day: {
        1: '#2563EB',
        2: '#16A34A',
        3: '#D97706',
        4: '#9333EA',
        5: '#DB2777',
        '1-subtle': '#EFF4FF',
        '2-subtle': '#F0FDF4',
        '3-subtle': '#FFFBEB',
        '4-subtle': '#FAF5FF',
        '5-subtle': '#FDF2F8',
      },
      hotel: {
        DEFAULT: '#0F172A',
        subtle: '#F1F5F9',
      },
    },
    fontFamily: {
      sans: ['Inter', 'system-ui', 'sans-serif'],
      mono: ['JetBrains Mono', 'Fira Code', 'monospace'],
    },
    fontSize: {
      xs: ['11px', { lineHeight: '1.5' }],
      sm: ['13px', { lineHeight: '1.5' }],
      base: ['14px', { lineHeight: '1.5' }],
      md: ['15px', { lineHeight: '1.5' }],
      lg: ['17px', { lineHeight: '1.35' }],
      xl: ['20px', { lineHeight: '1.35' }],
      '2xl': ['24px', { lineHeight: '1.2' }],
      '3xl': ['30px', { lineHeight: '1.2' }],
      '4xl': ['36px', { lineHeight: '1.1' }],
    },
    boxShadow: {
      sm: '0 1px 2px 0 rgba(0,0,0,0.05)',
      md: '0 4px 6px -1px rgba(0,0,0,0.08), 0 2px 4px -2px rgba(0,0,0,0.05)',
      lg: '0 10px 15px -3px rgba(0,0,0,0.08), 0 4px 6px -4px rgba(0,0,0,0.05)',
      xl: '0 20px 25px -5px rgba(0,0,0,0.10), 0 8px 10px -6px rgba(0,0,0,0.05)',
      tooltip: '0 4px 16px rgba(0,0,0,0.14)',
      'card-hover': '0 8px 24px rgba(0,0,0,0.10)',
    },
    borderRadius: {
      sm: '4px',
      md: '8px',
      lg: '12px',
      xl: '16px',
      '2xl': '24px',
    },
    transitionTimingFunction: {
      spring: 'cubic-bezier(0.34, 1.56, 0.64, 1)',
    },
  },
},
```

---

### 1.3 CSS Custom Properties

```css
:root {
  /* Colors */
  --color-background: #F8F7F4;
  --color-surface: #FFFFFF;
  --color-border: #E4E2DC;
  --color-border-subtle: #EDECEA;

  --color-text-primary: #1A1917;
  --color-text-secondary: #5C5A55;
  --color-text-muted: #9B9891;
  --color-text-inverse: #FFFFFF;

  --color-accent: #2563EB;
  --color-accent-hover: #1D4ED8;
  --color-accent-subtle: #EFF4FF;

  --color-error: #DC2626;
  --color-error-subtle: #FEF2F2;
  --color-warning: #D97706;
  --color-warning-subtle: #FFFBEB;
  --color-success: #16A34A;
  --color-success-subtle: #F0FDF4;

  --color-day-1: #2563EB;
  --color-day-2: #16A34A;
  --color-day-3: #D97706;
  --color-day-4: #9333EA;
  --color-day-5: #DB2777;
  --color-day-1-subtle: #EFF4FF;
  --color-day-2-subtle: #F0FDF4;
  --color-day-3-subtle: #FFFBEB;
  --color-day-4-subtle: #FAF5FF;
  --color-day-5-subtle: #FDF2F8;

  --color-hotel: #0F172A;
  --color-overlay: rgba(15, 23, 42, 0.72);

  /* Typography */
  --font-sans: 'Inter', system-ui, sans-serif;
  --font-mono: 'JetBrains Mono', 'Fira Code', monospace;

  /* Spacing */
  --spacing-1: 4px;
  --spacing-2: 8px;
  --spacing-3: 12px;
  --spacing-4: 16px;
  --spacing-5: 20px;
  --spacing-6: 24px;
  --spacing-8: 32px;
  --spacing-10: 40px;
  --spacing-12: 48px;
  --spacing-16: 64px;
  --spacing-20: 80px;

  /* Transitions */
  --transition-fast: 120ms ease-out;
  --transition-base: 200ms ease-out;
  --transition-slow: 320ms ease-out;
  --transition-spring: 400ms cubic-bezier(0.34, 1.56, 0.64, 1);
}
```

---

## 2. Screen 1 — Landing / Input Form

### 2.1 Layout

```
┌─────────────────────────────────────────────────────────────────┐
│  TOPBAR  h=56px  bg=surface  border-b=border  shadow=sm         │
│  [Logo: Y·tinerary]                                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│               HERO SECTION  pt=80px pb=48px                     │
│    "Turn travel videos into a day-by-day map plan."             │
│    Subtitle: "Paste a YouTube URL. Get a route-optimized        │
│     itinerary in under 60 seconds."                             │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│               FORM CARD  max-w=640px  mx=auto                   │
│               bg=surface  rounded=xl  shadow=lg                 │
│               p=32px                                            │
│                                                                 │
│   [Destination field]                                           │
│   ─────────────────                                             │
│   [YouTube URLs  — multi-URL input]                             │
│   [+ Add another video]                                         │
│   ─────────────────                                             │
│   [Optional fields accordion: Hotel · Dates · Maps links]       │
│   ─────────────────                                             │
│   [Submit button: "Build My Itinerary →"]                       │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│  FOOTER  h=48px  text=muted  text-sm                            │
│  Free · No account required · Powered by YouTube + Foursquare  │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2 Topbar
- Height: 56px
- Background: `#FFFFFF`
- Border-bottom: 1px solid `#E4E2DC`
- Shadow: `shadow-sm`
- Logo: `Y·tinerary` — Inter Bold 17px, `#1A1917`
  - The "Y" renders in `#2563EB` (accent), the rest in `#1A1917`
- Padding horizontal: 32px

### 2.3 Hero Section
- `padding-top: 80px`, `padding-bottom: 48px`
- `text-align: center`
- Heading: "Turn travel videos into a day-by-day map plan." — Inter SemiBold 36px, `#1A1917`, letter-spacing `-0.02em`
- Subtitle: Inter Regular 17px, `#5C5A55`, `margin-top: 12px`, `max-width: 500px`, `mx: auto`

### 2.4 Form Card
- `max-width: 640px`, `margin: 0 auto`
- Background: `#FFFFFF`
- Border-radius: `16px`
- Shadow: `shadow-lg`
- Padding: `32px`
- `margin-bottom: 80px`

#### Field layout within card:
- Field gap: `24px` (vertical)
- Section dividers: `1px solid #EDECEA` between logical groups
- Label: Inter Medium 13px, `#1A1917`, `margin-bottom: 6px`
- Required marker: `*` in `#DC2626`, same font
- Helper text: Inter Regular 12px, `#9B9891`, `margin-top: 4px`

#### Input styling:
- Height: 40px (single-line), auto-height (multi-line)
- Border: 1px solid `#E4E2DC`
- Border-radius: `8px`
- Background: `#FFFFFF`
- Text: Inter Regular 14px, `#1A1917`
- Placeholder: `#9B9891`
- Padding: `0 12px`
- Focus: border-color `#2563EB`, `box-shadow: 0 0 0 3px rgba(37,99,235,0.12)`
- Transition: border-color 120ms, box-shadow 120ms

#### Submit Button
- Full-width: `width: 100%`
- Height: 44px
- Background: `#2563EB`
- Text: Inter SemiBold 15px, `#FFFFFF`
- Border-radius: `8px`
- Label: "Build My Itinerary →"
- Hover: background `#1D4ED8`, transition 120ms
- Active: background `#1E40AF`, scale `0.99`
- Disabled (form incomplete): background `#9B9891`, cursor `not-allowed`
- Loading (pipeline started): spinner icon left of label, background `#1D4ED8`

#### Optional Fields Accordion
- Trigger: "Optional details" — Inter Medium 13px, `#5C5A55`, chevron right icon
- Expanded: chevron rotates 90°, transition 200ms
- Content: Hotel field, Dates date-range picker, Google Maps URLs input
- Gap inside: `16px`
- Use a custom HTML `<details>`/`<summary>` accordion styled with Tailwind + CSS transition on max-height

---

## 3. Screen 2 — Loading Overlay

### 3.1 Layout

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│                    FULL SCREEN OVERLAY                          │
│              bg=overlay (rgba(15,23,42,0.72))                   │
│              backdrop-filter: blur(4px)                         │
│                                                                 │
│         ┌─────────────────────────────────┐                     │
│         │  LOADING CARD  w=480px          │                     │
│         │  bg=surface  rounded=2xl        │                     │
│         │  shadow=xl  p=40px              │                     │
│         │                                 │                     │
│         │  [Logo mark — animated]         │                     │
│         │                                 │                     │
│         │  "Building your itinerary..."   │                     │
│         │                                 │                     │
│         │  [Step label — live SSE text]   │                     │
│         │                                 │                     │
│         │  [Progress bar]                 │                     │
│         │                                 │                     │
│         │  "This takes about 30–90        │                     │
│         │   seconds."                     │                     │
│         └─────────────────────────────────┘                     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 3.2 Card Spec
- Width: 480px, centered (translate-x -50%, translate-y -50%)
- Background: `#FFFFFF`
- Border-radius: `24px`
- Shadow: `shadow-xl`
- Padding: `40px`
- Text-align: `center`

### 3.3 Logo Mark Animation
- Display the "Y" letterform, size 40px, color `#2563EB`
- Animation: subtle pulse — `opacity: 1 → 0.5 → 1`, duration `1800ms`, `ease-in-out`, `infinite`

### 3.4 Typography
- Heading "Building your itinerary...": Inter SemiBold 20px, `#1A1917`, `margin-top: 20px`
- Step label: Inter Regular 14px, `#5C5A55`, `margin-top: 8px`, `min-height: 20px`
  - Transitions with `opacity: 0 → 1` on each new SSE message, 200ms ease-out
- Footer note "This takes about 30–90 seconds.": Inter Regular 13px, `#9B9891`, `margin-top: 24px`

### 3.5 Progress Bar
- Container: `height: 6px`, `border-radius: 9999px`, background `#E4E2DC`, `margin-top: 20px`
- Fill: `height: 6px`, `border-radius: 9999px`, background `#2563EB`
- 4 SSE steps → fill widths: 15%, 40%, 70%, 95%
- Width transition: `600ms ease-out` on each step update

### 3.6 Overlay Entrance Animation
- Overlay: `opacity: 0 → 1`, `200ms ease-out`
- Card: `opacity: 0, translateY: 12px → opacity: 1, translateY: 0`, `320ms ease-out`, `delay: 80ms`

---

## 4. Screen 3 — Results Page

### 4.1 Layout

```
┌─────────────────────────────────────────────────────────────────┐
│  TOPBAR  h=56px  (same as landing, adds: "← New Search" link)   │
├────────────────────────────────────┬────────────────────────────┤
│                                    │                            │
│        MAP PANEL                   │    SIDEBAR PANEL           │
│        flex: 1 (fills remaining)   │    width: 400px            │
│        height: calc(100vh - 56px)  │    height: calc(100vh-56px)│
│        position: sticky top=56px   │    overflow-y: scroll      │
│                                    │                            │
│        [Leaflet map]               │    [DaySection × N]        │
│                                    │    [PlaceCard × N]         │
│                                    │    [More to Explore]       │
│                                    │    [ShareButton]           │
│                                    │                            │
└────────────────────────────────────┴────────────────────────────┘
```

### 4.2 Map Panel
- `flex: 1` (takes all space left of sidebar)
- `height: calc(100vh - 56px)`
- `position: sticky; top: 56px` — map stays fixed as sidebar scrolls
- No padding, map tiles fill edge to edge

### 4.3 Sidebar Panel
- `width: 400px` — fixed, no flex shrink
- `height: calc(100vh - 56px)`
- `overflow-y: auto`
- Background: `#F8F7F4`
- Border-left: `1px solid #E4E2DC`
- Custom scrollbar: `width: 4px`, thumb `#E4E2DC`, track transparent
- Padding: `16px 16px 32px`

#### Sidebar header (sticky inside sidebar)
- `position: sticky; top: 0`
- Background: `#F8F7F4`
- `padding: 16px 0 12px`
- `border-bottom: 1px solid #E4E2DC`
- Destination name: Inter SemiBold 17px, `#1A1917`
- Place count: Inter Regular 13px, `#9B9891` — "14 places · 4 days"
- Share button: top-right of header

#### Sidebar collapse toggle
- Small button on the left edge of sidebar (overlapping the border)
- Icon: `ChevronRight` (pointing left when expanded, right when collapsed)
- Size: 28px × 28px, `border-radius: 9999px`
- Background: `#FFFFFF`, border: `1px solid #E4E2DC`, shadow: `shadow-sm`
- Collapsed sidebar: `width: 0`, map expands to fill

---

## 5. Component Specs

### 5.1 URLInputRow

Single URL text field with a remove button. Stacked vertically for multi-URL input.

```
┌─────────────────────────────────────────────────┐ [×]
│  https://youtube.com/watch?v=...                │
└─────────────────────────────────────────────────┘
[+ Add another video]
```

- Input: full-width, height 40px (standard input styling)
- Remove button `[×]`: 28px × 28px, `border-radius: 9999px`, bg transparent, hover bg `#EDECEA`, icon `#9B9891`
  - Only shown when more than 1 URL row exists
- Gap between rows: `8px`
- "Add" link: Inter Medium 13px, `#2563EB`, hover underline, `margin-top: 8px`
- Enter animation per new row: `height: 0 → 40px, opacity: 0 → 1`, `200ms ease-out`
- Remove animation: `height: 40px → 0, opacity: 1 → 0`, `160ms ease-out`

Use a standard `<input type="url">` styled with Tailwind utility classes per the input spec above.

---

### 5.2 InputForm

Full landing form. Uses `<form>` element with `onSubmit`.

- Sections in order:
  1. Destination — `Input`, placeholder "e.g. Jaipur, India"
  2. YouTube URLs — `URLInputRow` stack, starts with 1 row
  3. Optional accordion — Hotel text input, date range picker (shadcn `DatePickerWithRange`), Google Maps URLs stack
  4. Submit button
- Validation:
  - Destination: required, min 2 chars
  - YouTube URLs: at least 1 non-empty, valid URL pattern (`youtube.com/watch` or `youtu.be/`)
  - Inline error under the field: Inter Regular 12px, `#DC2626`, appears on blur

---

### 5.3 LoadingOverlay

Full-screen modal. Rendered above everything. Non-dismissable.

- `position: fixed; inset: 0; z-index: 50`
- Backdrop: `rgba(15,23,42,0.72)`, `backdrop-filter: blur(4px)`
- Card: centered (flexbox column, align-center justify-center)
- Receives SSE `stepMessage` and `stepIndex` (0–3) as props
- `stepIndex` drives progress bar width: `[15, 40, 70, 95][stepIndex]%`

---

### 5.4 MapContainer

Wrapper around the Leaflet map instance. Handles sizing only — Leaflet manages internal rendering.

- `width: 100%`, `height: 100%`
- `position: relative`
- Leaflet tile: OpenStreetMap — `https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png`
- Attribution: `© OpenStreetMap contributors` — bottom-right corner, small, styled to blend

---

### 5.5 MapPin (SVG Spec)

Custom Leaflet `DivIcon` rendered from an SVG string.

#### Day Pin

Shape: teardrop (circle with downward point)
- Width: 28px, Height: 36px
- Fill: `var(--color-day-N)` for selected, `rgba(day-color, 0.6)` for unselected/dimmed
- Stroke: `#FFFFFF`, stroke-width: `2px`
- Shadow: `drop-shadow(0 2px 4px rgba(0,0,0,0.25))`
- Number inside circle: `N` (day number), white, Inter Bold 11px, centered
- Selected state: scale `1.25`, shadow `drop-shadow(0 4px 8px rgba(0,0,0,0.35))`
- Transition: scale `200ms ease-out`

SVG template:
```svg
<svg width="28" height="36" viewBox="0 0 28 36" xmlns="http://www.w3.org/2000/svg">
  <path d="M14 0C6.268 0 0 6.268 0 14c0 9.333 14 22 14 22s14-12.667 14-22C28 6.268 21.732 0 14 0z"
        fill="{{DAY_COLOR}}" stroke="#FFFFFF" stroke-width="2"/>
  <text x="14" y="18" text-anchor="middle" dominant-baseline="central"
        fill="#FFFFFF" font-family="Inter,sans-serif" font-size="11" font-weight="700">
    {{DAY_NUMBER}}
  </text>
</svg>
```

Leaflet icon anchor: `[14, 36]` (tip of teardrop)

#### Hotel Pin

Shape: solid square with rounded corners and a roof peak (house silhouette)
- Width: 32px, Height: 32px
- Fill: `#0F172A`
- Icon inside: `🏨` emoji or a house SVG glyph in `#FFFFFF`, 14px
- Stroke: `#FFFFFF`, stroke-width: `2px`
- Shadow: `drop-shadow(0 2px 6px rgba(0,0,0,0.35))`
- Always full opacity (not dimmed when a day is selected)

SVG template:
```svg
<svg width="32" height="32" viewBox="0 0 32 32" xmlns="http://www.w3.org/2000/svg">
  <rect x="2" y="2" width="28" height="28" rx="6" ry="6"
        fill="#0F172A" stroke="#FFFFFF" stroke-width="2"/>
  <text x="16" y="20" text-anchor="middle" dominant-baseline="central"
        fill="#FFFFFF" font-family="Inter,sans-serif" font-size="15">
    ⌂
  </text>
</svg>
```

Leaflet icon anchor: `[16, 16]` (center)

---

### 5.6 MapTooltip

Leaflet `Popup` with custom styling. Appears on pin click.

```
┌──────────────────────────────┐
│  [Day 1 dot] Amber Fort      │
│  Temple · ⭐ 4.7             │
└──────────────────────────────┘
```

- Background: `#FFFFFF`
- Border-radius: `8px`
- Shadow: `shadow-tooltip`
- Padding: `10px 14px`
- Border: none (override Leaflet default)
- No close button (closes on click-away)

Place name: Inter SemiBold 14px, `#1A1917`
Category + rating row: Inter Regular 12px, `#5C5A55`, `margin-top: 2px`
Day indicator dot: 8px circle, filled with `var(--color-day-N)`, `margin-right: 6px`, vertical-align middle

Leaflet CSS overrides:
```css
.leaflet-popup-content-wrapper {
  border-radius: 8px;
  padding: 0;
  box-shadow: 0 4px 16px rgba(0,0,0,0.14);
}
.leaflet-popup-content { margin: 0; }
.leaflet-popup-tip-container { display: none; }
```

---

### 5.7 SidebarPanel

Right panel container.

- `width: 400px`
- `height: calc(100vh - 56px)`
- `overflow-y: auto`
- Background: `#F8F7F4`
- Border-left: `1px solid #E4E2DC`
- Contains: sticky header, list of `DaySectionHeader` + `PlaceCard`, "More to Explore" section, footer with `ShareButton`

Collapse behavior:
- Collapsed: `width: 0`, `overflow: hidden`, transition `width 320ms ease-out`
- Map panel: `transition: flex 320ms ease-out`
- Toggle button remains visible at the left edge of the sidebar at all times

---

### 5.8 DaySectionHeader

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ● Day 1 · Old City & Bazaars        5 places
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

- Padding: `12px 0 8px`
- Left accent: 3px × 16px vertical bar, color `var(--color-day-N)`, `border-radius: 9999px`, `margin-right: 10px`
- Day label: Inter SemiBold 13px, `#1A1917`, uppercase, letter-spacing `0.08em`
- Cluster name: Inter Regular 13px, `#5C5A55`  — separated from day label by ` · `
- Place count: Inter Regular 12px, `#9B9891`, pushed right (`margin-left: auto`)
- Separator line below: `1px solid #EDECEA`

Interaction: clicking a `DaySectionHeader` highlights that day's pins on the map.
- Active state: background `var(--color-day-N-subtle)`, transition `background 200ms ease-out`

---

### 5.9 PlaceCard

#### Collapsed State

```
┌──────────────────────────────────────────┐
│  Amber Fort               [Day 1 badge]  │
│  Temple · Historic Site  ⭐ 4.7          │
│  📹 Mumbiker Nikhil's Jaipur Vlog        │
└──────────────────────────────────────────┘
```

- Background: `#FFFFFF`
- Border: `1px solid #E4E2DC`
- Border-radius: `10px`
- Padding: `12px 14px`
- Shadow: `shadow-sm`
- `margin-bottom: 8px`
- Hover: `box-shadow: shadow-card-hover`, border-color `#C7C5BE`, transition `200ms ease-out`
- Cursor: `pointer`

Anatomy:
- **Row 1:** Place name (Inter SemiBold 14px, `#1A1917`) + Day badge right-aligned
- **Day badge:** `border-radius: 9999px`, `padding: 2px 8px`, background `var(--color-day-N-subtle)`, text Inter Medium 11px `var(--color-day-N)`, letter-spacing `0.04em`
- **Row 2:** Category (Inter Regular 12px, `#5C5A55`) · Rating (⭐ + number, same style)
- **Row 3:** Source video — `📹` + video title (Inter Regular 12px, `#9B9891`, truncated with ellipsis, max-width fits card)

"Unresolved" state: place name in `#9B9891`, italic. Row 2: "Location not found". No video row. Border `1px dashed #E4E2DC`.

#### Expanded State (on click, replaces collapsed)

```
┌──────────────────────────────────────────┐
│  [Photo — 100% wide, 160px tall]         │
│  [object-fit: cover, rounded top]        │
├──────────────────────────────────────────┤
│  Amber Fort               [Day 1 badge]  │
│  Temple · Historic Site  ⭐ 4.7          │
│  Mon–Sun 8:00–17:30                      │
│                                          │
│  Spectacular hilltop fort overlooking    │
│  the Maota Lake, a UNESCO World          │
│  Heritage Site.                          │
│                                          │
│  📹 Mumbiker Nikhil's Jaipur Vlog ↗     │
│  📹 Curly Tales Rajasthan ↗              │
│                                          │
│  [Remove from itinerary]                 │
└──────────────────────────────────────────┘
```

- Photo: `height: 160px`, `width: 100%`, `object-fit: cover`, `border-radius: 10px 10px 0 0`
- Description text: Inter Regular 13px, `#5C5A55`, line-height `1.5`, `margin-top: 8px`
- Hours: Inter Regular 12px, `#9B9891`, `margin-top: 4px`
- Source video links: each on its own line, Inter Regular 12px, `#2563EB`, hover underline, opens YouTube in new tab
- Remove button: full-width, height 36px, border `1px solid #E4E2DC`, border-radius `8px`, text Inter Medium 13px `#DC2626`, hover bg `#FEF2F2`, `margin-top: 12px`

Expand animation: `height: auto` via `max-height: 0 → 600px`, `overflow: hidden`, `320ms ease-out`

---

### 5.10 ShareButton

```
[↗ Share itinerary]
```

- Position: top-right of sidebar sticky header
- Height: 32px, `padding: 0 12px`
- Background: `#FFFFFF`
- Border: `1px solid #E4E2DC`
- Border-radius: `8px`
- Text: Inter Medium 13px, `#1A1917`
- Icon: `Share2` (Lucide), 14px, left of label, `margin-right: 6px`
- Hover: background `#F8F7F4`, border-color `#C7C5BE`
- Copied state (after click): background `#F0FDF4`, border-color `#16A34A`, text `#16A34A`, label "Link copied!", duration 2000ms then resets

---

### 5.11 ErrorBanner

Non-blocking. Appears at the top of the sidebar or as a toast.

```
⚠ Some places couldn't be processed. Showing partial results.   [×]
```

- Background: `#FFFBEB`
- Border: `1px solid #D97706`
- Border-radius: `8px`
- Padding: `10px 14px`
- Icon: `AlertTriangle`, 15px, `#D97706`, `margin-right: 8px`
- Text: Inter Regular 13px, `#92400E`
- Dismiss `[×]`: 24px × 24px, icon button, right-aligned
- Entrance: `translateY(-8px) → translateY(0)`, `200ms ease-out`

---

### 5.12 UnresolvedPlacePill

Shown in sidebar within a collapsed "Unresolved places (3)" disclosure below "More to Explore".

```
[ Amber Fort  × ]
```

- `display: inline-flex; align-items: center`
- Height: 28px, `padding: 0 10px`
- Background: `#F8F7F4`
- Border: `1px dashed #E4E2DC`
- Border-radius: `9999px`
- Text: Inter Regular 13px, `#9B9891`
- Remove `×`: 16px × 16px, icon button, `margin-left: 6px`, hover color `#DC2626`

---

## 6. Motion Rules

All animations use CSS transitions or `framer-motion` (if already in the stack).

| Element | Property | From | To | Duration | Easing |
|---|---|---|---|---|---|
| LoadingOverlay backdrop | opacity | 0 | 1 | 200ms | ease-out |
| LoadingOverlay card | opacity, translateY | 0, 12px | 1, 0 | 320ms | ease-out |
| Progress bar fill | width | prev% | next% | 600ms | ease-out |
| Step label | opacity | 0 | 1 | 200ms | ease-out |
| URLInputRow add | height, opacity | 0, 0 | 40px, 1 | 200ms | ease-out |
| URLInputRow remove | height, opacity | 40px, 1 | 0, 0 | 160ms | ease-out |
| PlaceCard expand | max-height | 0 | 600px | 320ms | ease-out |
| PlaceCard collapse | max-height | 600px | 0 | 200ms | ease-out |
| Sidebar collapse | width | 400px | 0 | 320ms | ease-out |
| Sidebar expand | width | 0 | 400px | 320ms | ease-out |
| Map panel | flex-grow | — | — | 320ms | ease-out |
| DaySectionHeader active | background | transparent | day-subtle | 200ms | ease-out |
| Day pins highlight | opacity | 1 | 0.3 (non-selected) | 200ms | ease-out |
| Day pin selected | scale | 1 | 1.25 | 200ms | ease-out |
| ShareButton copied | background, color | default | success | 120ms | ease-out |
| ShareButton reset | background, color | success | default | 200ms | ease-out (after 2000ms delay) |
| ErrorBanner entrance | translateY | -8px | 0 | 200ms | ease-out |
| Page: form → loading | opacity | 1 | 0.6 | 160ms | ease-out |
| Page: loading → results | opacity | 0 | 1 | 320ms | ease-out |

---

## 7. Typography Hierarchy Summary

| Role | Font | Size | Weight | Color |
|---|---|---|---|---|
| Page heading | Inter | 36px | 600 | `#1A1917` |
| Section heading | Inter | 20px | 600 | `#1A1917` |
| Card title | Inter | 14px | 600 | `#1A1917` |
| Day section label | Inter | 13px | 600 | `#1A1917` |
| Body text | Inter | 14px | 400 | `#1A1917` |
| Secondary text | Inter | 13px | 400 | `#5C5A55` |
| Meta / label | Inter | 12px | 400 | `#9B9891` |
| Badge | Inter | 11px | 500 | day color |
| Button | Inter | 14–15px | 600 | `#FFFFFF` / `#1A1917` |
| Link | Inter | 13px | 400 | `#2563EB` |
| Error | Inter | 12px | 400 | `#DC2626` |

---

## 8. Accessibility

- All interactive elements have `focus-visible` ring: `0 0 0 3px rgba(37,99,235,0.25)`
- Day colors all pass WCAG AA on white (`#FFFFFF`) and on their subtle backgrounds
- Map pins use both color and number label — not color-only
- All icon-only buttons have `aria-label`
- Loading overlay has `role="status"` and `aria-live="polite"` for screen readers
- Minimum touch / click target: 28px × 28px

---

## 9. HTML Element Map

This project is a **plain HTML + Tailwind CSS (CDN) + vanilla JavaScript** website. No React, no component library, no build step.

| UI Element | HTML Implementation |
|---|---|
| Text inputs | `<input type="text">` / `<input type="url">` — Tailwind-styled per §2.4 input spec |
| Submit button | `<button type="submit">` — Tailwind-styled per §2.4 submit spec |
| Remove / icon buttons | `<button type="button" aria-label="...">` — SVG icon inside, Tailwind ghost style |
| Optional fields accordion | `<details>`/`<summary>` with CSS `max-height` transition on the inner content `<div>` |
| Date range picker | Two `<input type="date">` fields (start / end) side-by-side |
| Loading overlay | `<div>` with `position: fixed; inset: 0` toggled via JS `classList.add/remove('hidden')` |
| Error banner | `<div role="alert">` with warning styles — dismissed via JS |
| Sidebar toggle | `<button type="button" aria-label="Toggle sidebar">` — SVG chevron icon |
| Share copied feedback | Inline JS: button text/style swapped on click, reset after 2000 ms via `setTimeout` |
| Unresolved disclosure | `<details>`/`<summary>` pattern, same as optional fields accordion |

---

*End of Ytinerary Website Design Specification v1.0*
