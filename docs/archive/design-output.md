# Ytinerary — Master Design Output
*v2.0 | Uber Design Language | 2026-05-28 | Single source of truth for Frontend Engineer*

This document is the assembled design output for Ytinerary. It reflects the Uber-inspired visual language: bold black typography, pure white surfaces, Uber green as the active/success signal, and Manrope (Uber Move substitute) as the typeface. All sections are implementation-ready.

---

## Document Map

| Section | Coverage | Source file |
|---|---|---|
| **1. Design Tokens** | Colors, typography, spacing, shadows, motion tokens, keyframes | `design-tokens-spec.md` |
| **2. Landing Page & Loading Overlay** | Full page layouts, form inputs, submit button, loading sequence | `landing-page-spec.md` |
| **3. Results Page** | Split-layout map+sidebar, sidebar collapse, cross-sync, mobile sheet | `results-page-spec.md` |
| **4. Components** | All interactive components with every state | `components-spec.md` |
| **5. Motion, A11y & Visual Richness** | Master timing table, principles, accessibility, performance | `motion-a11y-spec.md` |

---

## Design Language Summary

### Principles
1. **Bold contrast** — Black on white. High-contrast at every level. `#000000` text on `#FFFFFF` surface.
2. **Typography does the work** — Large, heavy display text (56px hero). Color is not decoration.
3. **Black as the anchor** — Primary CTA is black. Nothing competes for the user's attention.
4. **Green as signal** — `#06C167` (Uber green) marks active, success, and completion states.
5. **Clean surfaces** — No mesh gradients, no ambient orbs. White is the canvas.
6. **Map is the hero** — Results page: the map fills everything. Sidebar is a clean tool.
7. **Functional motion** — Shorter durations (100–280ms hover/state). Nothing moves for decoration.
8. **Desktop-first** — 1280px primary target. Mobile handled via bottom-sheet pattern.

---

## Section 1 — Design Tokens
*Source: design-tokens-spec.md*

### 1.1 Color Tokens

| Token | Hex | CSS Var | Usage |
|---|---|---|---|
| background | `#FFFFFF` | `--color-background` | Page body |
| background-secondary | `#F6F6F6` | `--color-background-secondary` | Sidebar, section alt surface |
| surface | `#FFFFFF` | `--color-surface` | Cards, inputs, modals |
| border | `#E2E2E2` | `--color-border` | All element borders |
| border-subtle | `#F0F0F0` | `--color-border-subtle` | Section dividers inside cards |
| text-primary | `#000000` | `--color-text-primary` | Headings, body, card titles |
| text-secondary | `#545454` | `--color-text-secondary` | Labels, secondary body |
| text-muted | `#8A8A8A` | `--color-text-muted` | Placeholders, meta, timestamps |
| text-inverse | `#FFFFFF` | `--color-text-inverse` | Text on dark/primary backgrounds |
| primary | `#000000` | `--color-primary` | CTA buttons, primary actions |
| primary-hover | `#1A1A1A` | `--color-primary-hover` | CTA hover |
| accent | `#06C167` | `--color-accent` | Active, success, Uber green |
| accent-hover | `#049C52` | `--color-accent-hover` | Accent hover |
| accent-subtle | `#E6FAF0` | `--color-accent-subtle` | Valid tint, focus accent bg |
| error | `#C7282D` | `--color-error` | Error states |
| error-subtle | `#FFF0F0` | `--color-error-subtle` | Error input background |
| warning | `#F6A609` | `--color-warning` | Warning states |
| success | `#05944F` | `--color-success` | Valid input, copied state |
| success-subtle | `#E6FAF0` | `--color-success-subtle` | Copied bg |

### Day Colors

| Token | Hex | Subtle | Use |
|---|---|---|---|
| day-1 | `#276EF1` | `#EAF0FE` | Day 1 pins, badges, accents |
| day-2 | `#06C167` | `#E6FAF0` | Day 2 |
| day-3 | `#FF974A` | `#FFF3EB` | Day 3 |
| day-4 | `#7356BF` | `#F0ECFB` | Day 4 |
| day-5 | `#E85D99` | `#FEF0F7` | Day 5 |

### 1.2 Typography

**Font:** `'Uber Move', 'Manrope', -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif`
**Google Fonts load:** Manrope weights 400, 500, 600, 700

| Token | Size | Weight | Letter Spacing | Line Height | Use |
|---|---|---|---|---|---|
| display | 72px | 700 | -0.05em | 1.0 | Super hero (wide screens) |
| 4xl | 56px | 700 | -0.04em | 1.0 | Hero heading |
| 3xl | 40px | 700 | -0.03em | 1.1 | Display medium |
| 2xl | 32px | 600 | -0.03em | 1.2 | Large heading |
| xl | 24px | 600 | -0.02em | 1.3 | Section headings |
| lg | 20px | 600 | -0.01em | 1.35 | Card section titles |
| md | 17px | 500 | 0 | 1.5 | Sidebar header, CTA |
| base | 16px | 400 | 0 | 1.5 | Body text, inputs |
| sm | 13px | 400 | 0 | 1.5 | Secondary text, labels |
| xs | 11px | 500 | +0.04em | 1.5 | Badges, caps labels |

### 1.3 Spacing (8px base grid)

| Token | Value | Common use |
|---|---|---|
| 1 | 4px | Icon gap |
| 2 | 8px | Inline gap |
| 3 | 12px | Compact padding |
| 4 | 16px | Default padding |
| 6 | 24px | Card padding |
| 8 | 32px | Form card padding |
| 10 | 40px | Section spacing |
| 12 | 48px | Large gap |
| 16 | 64px | Hero bottom |
| 20 | 80px | Page section gap |
| 24 | 96px | Hero top (desktop) |

### 1.4 Shadows (minimal — Uber flat style)

| Token | Value | Use |
|---|---|---|
| subtle | `0 1px 2px rgba(0,0,0,0.06)` | Cards at rest |
| sm | `0 2px 4px rgba(0,0,0,0.08)` | Form card, toggles |
| md | `0 4px 12px rgba(0,0,0,0.08)` | On-scroll topbar, map controls |
| lg | `0 8px 24px rgba(0,0,0,0.10)` | Focused form card |
| xl | `0 16px 48px rgba(0,0,0,0.12)` | Loading overlay |
| card-hover | `0 4px 16px rgba(0,0,0,0.12)` | PlaceCard hover |
| glow-primary | `0 0 0 3px rgba(0,0,0,0.12)` | Input focus ring |
| glow-accent | `0 0 0 3px rgba(6,193,103,0.25)` | Input focus (accent) |
| glow-error | `0 0 0 3px rgba(199,40,45,0.20)` | Error ring |

### 1.5 Border Radius

| Token | px | Use |
|---|---|---|
| xs | 2px | Tight tags |
| sm | 4px | Badges, thumbnails |
| md | 8px | Inputs, buttons |
| lg | 12px | Cards (mobile), place cards |
| xl | 16px | Form card, modal |
| 2xl | 24px | Loading overlay card |
| full | 9999px | Pills, badges, icon buttons |

### 1.6 Motion Tokens

| Token | Value | Use |
|---|---|---|
| fast | `100ms ease-out` | Hover color/border |
| base | `180ms ease-out` | Standard state changes |
| decelerate | `280ms cubic-bezier(0.05,0.7,0.1,1)` | Entrances |
| accelerate | `180ms cubic-bezier(0.3,0,0.8,0.15)` | Exits |
| spring-soft | `300ms cubic-bezier(0.34,1.40,0.64,1)` | Sidebar, panels |
| snap | `140ms cubic-bezier(0.32,0.72,0,1)` | Tab switches |

---

## Section 2 — Landing Page & Loading Overlay
*Source: landing-page-spec.md*

**Key specs:**
- Hero: Manrope Bold 56px, #000000, letter-spacing -0.04em, pure white background
- Optional subtle grid texture (repeating-linear-gradient @3% opacity) on hero
- No ambient orbs, no mesh gradient
- Form card: white, 1px solid #E2E2E2, border-radius 16px, shadow-sm
- Input height: 48px, border goes black (1px→2px solid #000000) on hover/focus
- Submit button: full-width, bg #000000, 48px, Manrope Bold 16px white, arrow nudges +3px on hover
- Loading overlay: dark backdrop rgba(0,0,0,0.65), white card, 4px progress bar (black fill)

---

## Section 3 — Results Page
*Source: results-page-spec.md*

**Key specs:**
- Topbar: 60px, pure white, border-bottom #E2E2E2
- Map panel: flex:1, sticky top:60px
- Sidebar: 400px fixed, bg #F6F6F6, border-left #E2E2E2
- Sidebar sticky header: destination Manrope 600 17px #000000, count 14px #8A8A8A
- Split-view + mobile bottom-sheet (peek 120px / half 50vh / full 90vh)
- Entrance sequence: sidebar translateX 400→0 at t=0ms, pins drop at t=400ms

---

## Section 4 — Components
*Source: components-spec.md*

| # | Component | Key visual change from v1 |
|---|---|---|
| 1 | URLInputRow | Border goes black on hover/focus (no blue); valid flash = green (#05944F) |
| 2 | Day Pin (Map) | Same shape, new day colors (day-1=#276EF1, day-2=#06C167, etc.) |
| 3 | Hotel Pin | Fill: #000000 (was #0F172A) |
| 4 | Map Tooltip | White card with #E2E2E2 border |
| 5 | Day Route Polyline | Same, day colors updated |
| 6 | DaySectionHeader | Hover: bg #F0F0F0 (neutral gray, not warm) |
| 7 | PlaceCard (collapsed) | No vertical lift on hover — border-left reveals, shadow upgrades |
| 8 | PlaceCard (expanded) | White card, #E2E2E2 border |
| 9 | ShareButton | Hover: border goes black; copied: green (#05944F) |
| 10 | SubmitButton | Black bg, height 48px, arrow nudge on hover (no lift) |
| 11 | ErrorBanner | #000000 text on colored warning bg |
| 12 | Skeleton | bg #F0F0F0 shimmer |

---

## Section 5 — Motion, Accessibility & Visual Richness
*Source: motion-a11y-spec.md*

**Key changes from v1:**
- Duration ladder shortened: hover 100ms (was 120ms), state 180ms (was 200ms), entrance 280ms (was 320ms)
- No spring-bouncy easing — pins use ease-decelerate instead
- No ambient orbs, breathe animations, or sparkle bursts
- Idle animation: only subtle arrow nudge on submit (1 per screen max)
- Focus ring: `rgba(0,0,0,0.12)` (black-based, not blue)
- Contrast ratios all verified for WCAG AA

---

## Quick Reference: Key Numbers

| Specification | Value |
|---|---|
| Topbar height | 60px |
| Sidebar width (desktop) | 400px |
| Form card max-width | 640px |
| Form card padding | 32px |
| Hero heading | 56px, weight 700, tracking -0.04em |
| Input height | 48px |
| Submit button height | 48px |
| Submit button bg | #000000 |
| Accent green | #06C167 |
| Map pin anchor | [14, 36] (bottom tip) |
| Hotel pin anchor | [16, 16] (center) |
| Focus ring | `0 0 0 3px rgba(0,0,0,0.12)` |
| Min touch target | 28×28px |
| Stagger default | 40ms |
| Pin stagger | 50ms (cap 1500ms) |
| Idle motion budget | Max 1 simultaneous per screen |
| Mobile sheet peek | ~120px |
| Mobile sheet half | ~50vh |
| Mobile sheet full | ~90vh |
| Sidebar entrance delay | 0ms (400ms duration, decelerate) |
| Pin drop start delay | 400ms (after sidebar) |

---

*End of design-output.md — Master design package for Ytinerary v2.0*
*Frontend Engineer: implement from this document. All five source spec files are authoritative for their sections.*
