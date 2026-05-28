---
name: project-ytinerary
description: Core context for the Ytinerary travel planning app — what it is, what's been built, and design system conventions established
metadata:
  type: project
---

Ytinerary is a travel planning app that converts YouTube travel video URLs into route-optimized, day-by-day itineraries. The product is in early portfolio/MVP stage.

**Why:** The core value proposition is zero friction — paste a YouTube URL, get a structured itinerary in under 60 seconds. Powered by YouTube transcript extraction + Foursquare place data. No account required.

**How to apply:** All frontend decisions should prioritize simplicity, delight, and trust. The form is the entire landing page — it must feel polished and responsive. Every micro-interaction serves to build confidence that the AI pipeline is working.

## What's been built

- `index.html` — Full landing page (single-file: HTML + Tailwind CDN + vanilla JS). Located at `/Users/pulkit/Documents/Product Portfolio/Ytinerary/index.html`.

## Design system conventions

- **CSS custom properties** defined in `:root` — always use these, never hardcode hex values inline.
- **Primary accent:** `#2563EB` (--color-accent) — used for CTA, focus rings, Day 1 pins, logo.
- **Background:** `#F8F7F4` (--color-background) — warm off-white, not pure white.
- **Text primary:** `#1A1917` — slightly warm black.
- **Tailwind CDN** used for utility classes — no build step.
- **Lucide Icons** via CDN (`https://unpkg.com/lucide@latest/dist/umd/lucide.js`), initialized with `lucide.createIcons()` after DOMContentLoaded.
- **Inter font** via Google Fonts (weights 400, 500, 600, 700).

## Class naming convention

BEM-inspired, descriptive kebab-case. Examples: `.form-card`, `.url-row`, `.ambient-orb`, `.hero-heading`, `.loading-overlay`.

## Breakpoints

- Mobile: max-width 767px
- Desktop primary target: 1280px+

## Z-index scale

- Overlay: 50, topbar: 200, toast: 60

## Backend integration stubs (not yet wired)

- Form submits to `/api/plan` (POST)
- SSE stream expected at `/api/plan/stream?dest=...&urls=...`
- Each SSE message: `{ step: 0|1|2|3|4 }` — step 4 signals completion
- `simulateProgress()` in `index.html` handles demo mode until backend is ready

## Animation system

All animations wrapped in `@media (prefers-reduced-motion: no-preference)` blocks. Keyframes include: pulse-soft, ambient-drift, slide-up-fade, breathe, shimmer, sparkle, shake, pin-drop-mini, route-draw, progress-shimmer, ripple-expand.
