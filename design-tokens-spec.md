# Ytinerary — Design Tokens Specification
*v2.0 | Uber Design Language | Source: design-spec.md | For use by Frontend Engineer*

---

## Design Language Reference
Ytinerary's visual language is modeled after Uber's product design system: bold black-forward typography, clean white surfaces, green as the active/success signal, and zero visual decoration that doesn't serve function. No mesh gradients, no ambient orbs — typography and contrast do the work.

---

## 1. Color Tokens

| Token | Hex | CSS Var | Usage |
|---|---|---|---|
| background | `#FFFFFF` | `--color-background` | Page body, outer shell |
| background-secondary | `#F6F6F6` | `--color-background-secondary` | Section stripes, sidebar, alt surfaces |
| surface | `#FFFFFF` | `--color-surface` | Cards, inputs, modals |
| surface-elevated | `#FFFFFF` | `--color-surface-elevated` | Elevated overlays |
| border | `#E2E2E2` | `--color-border` | Default borders on all elements |
| border-subtle | `#F0F0F0` | `--color-border-subtle` | Section dividers inside cards |
| text-primary | `#000000` | `--color-text-primary` | Headings, labels, card titles, inputs |
| text-secondary | `#545454` | `--color-text-secondary` | Body copy, secondary info, subtitles |
| text-muted | `#8A8A8A` | `--color-text-muted` | Placeholders, meta, captions, footer |
| text-inverse | `#FFFFFF` | `--color-text-inverse` | Text on dark/primary backgrounds |
| primary | `#000000` | `--color-primary` | Primary CTA buttons, bold actions |
| primary-hover | `#1A1A1A` | `--color-primary-hover` | Primary button hover state |
| primary-subtle | `#F6F6F6` | `--color-primary-subtle` | Light background for primary-tinted surfaces |
| primary-foreground | `#FFFFFF` | `--color-primary-foreground` | Text/icons on primary background |
| accent | `#06C167` | `--color-accent` | Active states, success signals, Uber green |
| accent-hover | `#049C52` | `--color-accent-hover` | Accent on hover |
| accent-subtle | `#E6FAF0` | `--color-accent-subtle` | Accent tinted surface, valid input tint |
| accent-foreground | `#FFFFFF` | `--color-accent-foreground` | Text/icons on accent background |
| error | `#C7282D` | `--color-error` | Error text, invalid borders, required asterisk |
| error-subtle | `#FFF0F0` | `--color-error-subtle` | Error tinted input background |
| warning | `#F6A609` | `--color-warning` | Warning text, warning borders |
| warning-subtle | `#FFFBEB` | `--color-warning-subtle` | ErrorBanner background |
| success | `#05944F` | `--color-success` | Valid state, ✓ icons, copied state |
| success-subtle | `#E6FAF0` | `--color-success-subtle` | ShareButton copied background |
| hotel | `#000000` | `--color-hotel` | Hotel map pin fill |
| hotel-subtle | `#F6F6F6` | `--color-hotel-subtle` | Hotel tinted surface |
| overlay | `rgba(0,0,0,0.65)` | `--color-overlay` | Full-screen modal backdrop |
| sparkle | `#F6A609` | `--color-sparkle` | Sparkle burst (success moments only) |
| route-line | `rgba(39,110,241,0.6)` | `--color-route-line` | Day route polyline on map |

### Day Colors (map pins, sidebar accents, badges)

| Token | Hex | Subtle Hex | Usage |
|---|---|---|---|
| day-1 | `#276EF1` | `#EAF0FE` | Day 1 pins, headers, badges |
| day-2 | `#06C167` | `#E6FAF0` | Day 2 |
| day-3 | `#FF974A` | `#FFF3EB` | Day 3 |
| day-4 | `#7356BF` | `#F0ECFB` | Day 4 |
| day-5 | `#E85D99` | `#FEF0F7` | Day 5 |

CSS vars: `--color-day-N` and `--color-day-N-subtle` for N = 1–5.

**WCAG AA contrast check (on #FFFFFF):**
- day-1 `#276EF1`: 4.7:1 ✓ AA
- day-2 `#06C167`: 3.0:1 ⚠ use on white for large/bold text (≥18px or ≥14px bold); use day-2-subtle bg for small text
- day-3 `#FF974A`: 2.9:1 ⚠ use on white for large text only
- day-4 `#7356BF`: 5.3:1 ✓ AA
- day-5 `#E85D99`: 3.9:1 ⚠ use for large/bold text on white; use day-5-subtle for small text

---

## 2. Gradient Tokens

| Token | Definition | Used on |
|---|---|---|
| subtle-grid | `repeating-linear-gradient(0deg, transparent, transparent 39px, #F0F0F0 39px, #F0F0F0 40px), repeating-linear-gradient(90deg, transparent, transparent 39px, #F0F0F0 39px, #F0F0F0 40px)` | Landing page hero section — subtle grid texture, 4% opacity |
| card-sheen | `linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(255,255,255,0.7) 100%)` | Form card `::before` on focus (opacity 0.3) |
| shimmer | `linear-gradient(90deg, transparent 0%, rgba(255,255,255,0.80) 50%, transparent 100%)` | Skeleton loaders, progress bar shimmer |
| day-glow-1..5 | `radial-gradient(circle, rgba(N,N,N,0.18) 0%, transparent 65%)` | Behind active pins, 80×80px |

> No mesh gradients, warm orbs, or hero blurs. Clean surface is the canvas.

---

## 3. Typography Tokens

### Font Families
| Token | Value | Use |
|---|---|---|
| font-family-display | `'Uber Move', 'Manrope', -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif` | All headings, display text |
| font-family-body | `'Uber Move', 'Manrope', -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif` | All body text, UI |
| font-family-mono | `'JetBrains Mono', 'Fira Code', monospace` | Code snippets (if any) |

**Font load:** Uber Move is a proprietary typeface. Load `Manrope` via Google Fonts as the nearest equivalent:
`<link rel="preconnect" href="https://fonts.googleapis.com">`
`<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700&display=swap" rel="stylesheet">`

### Type Scale
| Token | px | rem | Line height | Letter spacing | Use |
|---|---|---|---|---|---|
| font-size-xs | 11px | 0.6875rem | 1.5 | 0 | Badges, micro labels |
| font-size-sm | 13px | 0.8125rem | 1.5 | 0 | Secondary text, captions |
| font-size-base | 16px | 1rem | 1.5 | 0 | Body text, inputs |
| font-size-md | 17px | 1.0625rem | 1.5 | 0 | Sidebar header, submit button |
| font-size-lg | 20px | 1.25rem | 1.35 | -0.01em | Section headings |
| font-size-xl | 24px | 1.5rem | 1.3 | -0.02em | Sub-headings |
| font-size-2xl | 32px | 2rem | 1.2 | -0.03em | Heading large |
| font-size-3xl | 40px | 2.5rem | 1.1 | -0.03em | Display medium |
| font-size-4xl | 56px | 3.5rem | 1.0 | -0.04em | Hero heading |
| font-size-display | 72px | 4.5rem | 1.0 | -0.05em | Super display (landing hero on wide screens) |

### Font Weights
| Token | Value | Use |
|---|---|---|
| font-weight-regular | 400 | Body, secondary, meta, placeholders |
| font-weight-medium | 500 | Labels, accordion triggers, badges |
| font-weight-semibold | 600 | Sub-headings, card titles, day labels |
| font-weight-bold | 700 | Hero headings, display text, CTAs |

### Line Heights
| Token | Value | Use |
|---|---|---|
| line-height-display | 1.0 | Hero heading (56px+) |
| line-height-tight | 1.1 | Large headings (40–56px) |
| line-height-snug | 1.2 | Medium headings (24–40px) |
| line-height-normal | 1.5 | Body text, inputs, form copy |
| line-height-relaxed | 1.65 | Description paragraphs in expanded PlaceCards |

### Letter Spacing
| Token | Value | Use |
|---|---|---|
| letter-spacing-display | -0.04em | Hero heading (56px) |
| letter-spacing-tight | -0.03em | Display medium, heading 2xl+ |
| letter-spacing-heading | -0.02em | xl headings |
| letter-spacing-normal | 0em | Default (all body text) |
| letter-spacing-wide | 0.04em | Badges, uppercase labels |
| letter-spacing-wider | 0.06em | Day section labels (uppercase) |

---

## 4. Spacing Tokens (8px base grid)

| Token | px | Use |
|---|---|---|
| space-1 | 4px | Icon gaps, chip internal spacing |
| space-2 | 8px | Row gaps, inline element gaps |
| space-3 | 12px | Compact card padding, small gaps |
| space-4 | 16px | Standard padding, card inner padding |
| space-5 | 20px | Section gaps (compact) |
| space-6 | 24px | Form field gap, standard card padding |
| space-8 | 32px | Form card padding, hero horizontal |
| space-10 | 40px | Loading card padding, section padding |
| space-12 | 48px | Large section gap, footer height |
| space-16 | 64px | Hero bottom padding |
| space-20 | 80px | Hero top padding, page section gap |
| space-24 | 96px | Landing page hero top (desktop) |
| space-32 | 128px | Extra-large section separation |

### Component-Specific Constants
| Constant | Value | Where |
|---|---|---|
| nav-height | 60px | Topbar height (all pages) — slightly taller, more Uber-like |
| sidebar-width | 400px | Results page sidebar width |
| form-card-max-width | 640px | Landing form card |
| form-card-padding | 32px | Form card internal padding |
| loading-card-width | 480px | Loading overlay card |
| loading-card-padding | 40px | Loading card internal |

---

## 5. Shadow Tokens

Uber uses minimal, functional shadows. Surfaces mostly rely on borders and whitespace.

| Token | Value | Use |
|---|---|---|
| shadow-none | `none` | Flat elements (nav, buttons in most states) |
| shadow-subtle | `0 1px 2px rgba(0,0,0,0.06)` | Cards at absolute rest |
| shadow-sm | `0 2px 4px rgba(0,0,0,0.08)` | Form card rest, toggles |
| shadow-md | `0 4px 12px rgba(0,0,0,0.08)` | Topbar on scroll, map controls |
| shadow-lg | `0 8px 24px rgba(0,0,0,0.10)` | Focused form card |
| shadow-xl | `0 16px 48px rgba(0,0,0,0.12)` | Loading overlay card |
| shadow-card-hover | `0 4px 16px rgba(0,0,0,0.12)` | PlaceCard hover |
| shadow-card-lift | `0 8px 32px rgba(0,0,0,0.14)` | Lifted/focused cards |
| shadow-glow-accent | `0 0 0 3px rgba(6,193,103,0.25)` | Input focus ring (green) |
| shadow-glow-primary | `0 0 0 3px rgba(0,0,0,0.12)` | Input focus ring (black) |
| shadow-glow-error | `0 0 0 3px rgba(199,40,45,0.20)` | Input error ring |
| shadow-pin-rest | `drop-shadow(0 2px 4px rgba(0,0,0,0.25))` | Map pin default |
| shadow-pin-active | `drop-shadow(0 6px 12px rgba(0,0,0,0.35))` | Map pin hover/selected |
| shadow-tooltip | `0 4px 16px rgba(0,0,0,0.14)` | Map tooltip |

---

## 6. Border Radius Tokens

| Token | px | Use |
|---|---|---|
| radius-xs | 2px | Tags, tight containers |
| radius-sm | 4px | Badges, thumbnails |
| radius-md | 8px | Inputs, buttons, small cards |
| radius-lg | 12px | Form card (mobile), place cards |
| radius-xl | 16px | Form card (desktop), modal |
| radius-2xl | 24px | Loading overlay card |
| radius-full | 9999px | Pills, badges, icon buttons, toggle |

---

## 7. Blur Tokens

| Token | Value | Use |
|---|---|---|
| blur-sm | `blur(4px)` | Subtle blur |
| blur-md | `blur(8px)` | Loading overlay backdrop |
| blur-backdrop | `blur(12px) saturate(180%)` | Topbar glassmorphism on scroll |

---

## 8. Motion Tokens

Motion is functional. It confirms state changes, guides attention, and communicates hierarchy. Nothing moves for decoration alone. Uber's motion is purposeful and direct — faster hover states, less spring.

### Easing Curves
| Token | Cubic-bezier | Role | Do NOT use for |
|---|---|---|---|
| ease-standard | `cubic-bezier(0.2, 0, 0, 1)` | General, simple state transitions | Long-distance motion |
| ease-decelerate | `cubic-bezier(0.05, 0.7, 0.1, 1)` | Elements ENTERING screen | Exits |
| ease-accelerate | `cubic-bezier(0.3, 0, 0.8, 0.15)` | Elements EXITING screen | Entrances |
| ease-spring-soft | `cubic-bezier(0.34, 1.40, 0.64, 1)` | Panel reveals, sidebar (subtle overshoot) | Buttons, text elements |
| ease-snap | `cubic-bezier(0.32, 0.72, 0, 1)` | Tab switches, segmented controls | Entrances/exits |

> Note: No spring-bouncy easing — Uber motion is direct. Pin drops use ease-decelerate.

### Composite Transitions
| Token | Value | When to use |
|---|---|---|
| transition-fast | `100ms ease-out` | Hover color/bg, focus ring |
| transition-base | `180ms ease-out` | Standard hover lifts, opacity |
| transition-snap | `140ms ease-snap` | Tab switches |
| transition-decelerate | `280ms ease-decelerate` | Elements entering screen |
| transition-accelerate | `180ms ease-accelerate` | Elements exiting screen |
| transition-spring-soft | `300ms ease-spring-soft` | Sidebar collapse, panel reveal |
| transition-slow | `400ms ease-out` | Page entrances |

### Duration Ladder
| Label | Duration | Feels like |
|---|---|---|
| Instant | 60–100ms | Direct response (hover, focus) |
| Quick | 140–200ms | Acknowledged action (click, toggle) |
| Smooth | 250–350ms | State transition (panel, expand) |
| Cinematic | 400–600ms | Page enter, sequence |
| Ambient | 2s+ | Idle loops |

### Animation Keyframes

**slide-up-fade** — `280ms ease-decelerate backwards`
- 0%: translateY(8px) opacity:0
- 100%: translateY(0) opacity:1
- Use: page entrances, cards, modals

**shimmer** — `1600ms linear infinite`
- 0%: background-position -200% 0
- 100%: background-position 200% 0
- Use: skeleton loaders, progress bar

**pin-drop** — `400ms ease-decelerate backwards` (no bounce — Uber-precise)
- 0%: translateY(-32px) scale(0.7) opacity:0
- 100%: translateY(0) scale(1) opacity:1
- Use: map pins on results page initial load

**pulse-ring** — `1600ms ease-out` (runs once per trigger)
- 0%: scale(0.8) opacity:0.5
- 100%: scale(2.0) opacity:0
- Use: pin landing ripple, active state confirmation

**route-draw** — `1000ms ease-out forwards`
- 0%: stroke-dashoffset 1000
- 100%: stroke-dashoffset 0
- Use: day route polyline

**check-draw** — `240ms ease-out forwards` (delay:60ms)
- 0%: stroke-dashoffset 24
- 100%: stroke-dashoffset 0
- Use: ShareButton check icon

**fade-in** — `200ms ease-out forwards`
- 0%: opacity 0
- 100%: opacity 1
- Use: loading states, overlays

**ripple-expand** — `300ms ease-decelerate forwards`
- 0%: scale(0) opacity:0.3
- 100%: scale(20) opacity:0
- Use: click feedback on buttons and headers

### Stagger Rules
- Default list stagger: **40ms** per child
- Map pin drops: **50ms** per pin
- Hero word groups: **60ms** per group
- Max staggered items: **8** — beyond that, single fade-in
- Total pin stagger cap: **1500ms** (remaining pins appear instantly)

---

## 9. Z-Index Scale

| Token | Value | Use |
|---|---|---|
| z-base | 0 | Default flow |
| z-raised | 10 | Sidebar panel, sticky headers |
| z-tooltip | 20 | Map tooltips, popovers |
| z-overlay | 50 | Loading overlay backdrop |
| z-toast | 60 | Error banners, toast notifications |

---

## 10. Breakpoints

| Token | px | Viewport |
|---|---|---|
| bp-mobile | 375px | Phone (minimum supported) |
| bp-tablet | 768px | Tablet portrait |
| bp-desktop | 1280px | **Primary target** (desktop-first) |
| bp-wide | 1440px | Widescreen |

### Responsive behavior summary
- **< 768px (mobile)**: Results page → full-map + bottom-sheet. Landing form → margin 0 16px, padding 24px. Hero heading: 40px.
- **768–1279px (tablet)**: Sidebar may narrow to 320px. Hero heading: 44px.
- **≥ 1280px (desktop)**: Full split layout, 400px sidebar, all animations at full fidelity. Hero: 56px.

---

## 11. CSS Custom Properties

```css
:root {
  /* Colors */
  --color-background: #FFFFFF;
  --color-background-secondary: #F6F6F6;
  --color-surface: #FFFFFF;
  --color-border: #E2E2E2;
  --color-border-subtle: #F0F0F0;

  --color-text-primary: #000000;
  --color-text-secondary: #545454;
  --color-text-muted: #8A8A8A;
  --color-text-inverse: #FFFFFF;

  --color-primary: #000000;
  --color-primary-hover: #1A1A1A;
  --color-primary-subtle: #F6F6F6;
  --color-primary-foreground: #FFFFFF;

  --color-accent: #06C167;
  --color-accent-hover: #049C52;
  --color-accent-subtle: #E6FAF0;
  --color-accent-foreground: #FFFFFF;

  --color-error: #C7282D;
  --color-error-subtle: #FFF0F0;
  --color-warning: #F6A609;
  --color-warning-subtle: #FFFBEB;
  --color-success: #05944F;
  --color-success-subtle: #E6FAF0;

  --color-day-1: #276EF1;
  --color-day-2: #06C167;
  --color-day-3: #FF974A;
  --color-day-4: #7356BF;
  --color-day-5: #E85D99;
  --color-day-1-subtle: #EAF0FE;
  --color-day-2-subtle: #E6FAF0;
  --color-day-3-subtle: #FFF3EB;
  --color-day-4-subtle: #F0ECFB;
  --color-day-5-subtle: #FEF0F7;

  --color-hotel: #000000;
  --color-hotel-subtle: #F6F6F6;
  --color-overlay: rgba(0, 0, 0, 0.65);
  --color-sparkle: #F6A609;
  --color-route-line: rgba(39, 110, 241, 0.60);

  /* Typography */
  --font-sans: 'Uber Move', 'Manrope', -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
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
  --spacing-24: 96px;

  /* Shadows */
  --shadow-none: none;
  --shadow-subtle: 0 1px 2px rgba(0,0,0,0.06);
  --shadow-sm: 0 2px 4px rgba(0,0,0,0.08);
  --shadow-md: 0 4px 12px rgba(0,0,0,0.08);
  --shadow-lg: 0 8px 24px rgba(0,0,0,0.10);
  --shadow-xl: 0 16px 48px rgba(0,0,0,0.12);
  --shadow-card-hover: 0 4px 16px rgba(0,0,0,0.12);
  --shadow-card-lift: 0 8px 32px rgba(0,0,0,0.14);
  --shadow-glow-accent: 0 0 0 3px rgba(6,193,103,0.25);
  --shadow-glow-primary: 0 0 0 3px rgba(0,0,0,0.12);
  --shadow-glow-error: 0 0 0 3px rgba(199,40,45,0.20);
  --shadow-tooltip: 0 4px 16px rgba(0,0,0,0.14);

  /* Border radius */
  --radius-xs: 2px;
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 12px;
  --radius-xl: 16px;
  --radius-2xl: 24px;
  --radius-full: 9999px;

  /* Easing */
  --ease-standard: cubic-bezier(0.2, 0, 0, 1);
  --ease-decelerate: cubic-bezier(0.05, 0.7, 0.1, 1);
  --ease-accelerate: cubic-bezier(0.3, 0, 0.8, 0.15);
  --ease-spring-soft: cubic-bezier(0.34, 1.40, 0.64, 1);
  --ease-snap: cubic-bezier(0.32, 0.72, 0, 1);

  /* Transitions */
  --transition-fast: 100ms ease-out;
  --transition-base: 180ms ease-out;
  --transition-slow: 280ms ease-out;
  --transition-slower: 400ms ease-out;
  --transition-snap: 140ms var(--ease-snap);
  --transition-spring-soft: 300ms var(--ease-spring-soft);
  --transition-decelerate: 280ms var(--ease-decelerate);
  --transition-accelerate: 180ms var(--ease-accelerate);
}

/* Global keyframes */
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
@keyframes fade-in {
  0%   { opacity: 0; }
  100% { opacity: 1; }
}

/* Reduced motion */
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

---

## 12. Tailwind Config Extension

```js
// tailwind.config.js — theme.extend block
theme: {
  extend: {
    colors: {
      background: '#FFFFFF',
      'background-secondary': '#F6F6F6',
      surface: '#FFFFFF',
      border: {
        DEFAULT: '#E2E2E2',
        subtle: '#F0F0F0',
      },
      text: {
        primary: '#000000',
        secondary: '#545454',
        muted: '#8A8A8A',
        inverse: '#FFFFFF',
      },
      primary: {
        DEFAULT: '#000000',
        hover: '#1A1A1A',
        subtle: '#F6F6F6',
        foreground: '#FFFFFF',
      },
      accent: {
        DEFAULT: '#06C167',
        hover: '#049C52',
        subtle: '#E6FAF0',
        foreground: '#FFFFFF',
      },
      day: {
        1: '#276EF1',
        2: '#06C167',
        3: '#FF974A',
        4: '#7356BF',
        5: '#E85D99',
        '1-subtle': '#EAF0FE',
        '2-subtle': '#E6FAF0',
        '3-subtle': '#FFF3EB',
        '4-subtle': '#F0ECFB',
        '5-subtle': '#FEF0F7',
      },
      hotel: {
        DEFAULT: '#000000',
        subtle: '#F6F6F6',
      },
    },
    fontFamily: {
      sans: ['Uber Move', 'Manrope', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Helvetica', 'Arial', 'sans-serif'],
      mono: ['JetBrains Mono', 'Fira Code', 'monospace'],
    },
    fontSize: {
      xs:      ['11px', { lineHeight: '1.5' }],
      sm:      ['13px', { lineHeight: '1.5' }],
      base:    ['16px', { lineHeight: '1.5' }],
      md:      ['17px', { lineHeight: '1.5' }],
      lg:      ['20px', { lineHeight: '1.35', letterSpacing: '-0.01em' }],
      xl:      ['24px', { lineHeight: '1.3',  letterSpacing: '-0.02em' }],
      '2xl':   ['32px', { lineHeight: '1.2',  letterSpacing: '-0.03em' }],
      '3xl':   ['40px', { lineHeight: '1.1',  letterSpacing: '-0.03em' }],
      '4xl':   ['56px', { lineHeight: '1.0',  letterSpacing: '-0.04em' }],
      display: ['72px', { lineHeight: '1.0',  letterSpacing: '-0.05em' }],
    },
    boxShadow: {
      none:        'none',
      subtle:      '0 1px 2px rgba(0,0,0,0.06)',
      sm:          '0 2px 4px rgba(0,0,0,0.08)',
      md:          '0 4px 12px rgba(0,0,0,0.08)',
      lg:          '0 8px 24px rgba(0,0,0,0.10)',
      xl:          '0 16px 48px rgba(0,0,0,0.12)',
      'card-hover':'0 4px 16px rgba(0,0,0,0.12)',
      'card-lift': '0 8px 32px rgba(0,0,0,0.14)',
      'glow-accent':'0 0 0 3px rgba(6,193,103,0.25)',
      'glow-primary':'0 0 0 3px rgba(0,0,0,0.12)',
      'glow-error': '0 0 0 3px rgba(199,40,45,0.20)',
      'tooltip':   '0 4px 16px rgba(0,0,0,0.14)',
    },
    borderRadius: {
      xs:   '2px',
      sm:   '4px',
      md:   '8px',
      lg:   '12px',
      xl:   '16px',
      '2xl':'24px',
      full: '9999px',
    },
  },
},
```

---

## 13. Idle Animation Budget (max 2 simultaneous per screen)

**Landing page:**
- Always on: topbar logo mark subtle pulse (opacity only)
- While form unfocused: nothing (no breathe animation — Uber is static at rest)
- After 4s idle on complete form: subtle arrow nudge in submit button (once every 8s)

**Results page:**
- When no pin selected: first pin of each day emits pulse-ring every 8s (staggered)
- Nothing else idles on results page

**Rule:** Never run > 2 idle animations simultaneously. Prefer 0 idle animations. Motion is reserved for user-triggered interactions.
