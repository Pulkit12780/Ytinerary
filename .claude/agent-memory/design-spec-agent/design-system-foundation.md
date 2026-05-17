---
name: design-system-foundation
description: Core Ytinerary design token conventions, palette rationale, and aesthetic decisions established in the v1 spec
metadata:
  type: project
---

## Aesthetic Direction
Calm, precise, trustworthy. Notion/Linear meets travel magazine. NOT gamified or loud. Desktop-first (1280px min). Neutral off-white base with a single indigo/slate accent — NOT coral (coral was agent system prompt default; product owner spec overrides to indigo for "smart tool" feel).

## Token Conventions
- All colors in OKLCH format
- Token names: kebab-case
- Day palette: day-1 (indigo) through day-5 (rose) — warm, distinguishable, accessible on OSM map tiles AND white sidebar simultaneously
- Shadow tokens: shadow-soft (resting), shadow-lift (hover), shadow-pin (map markers), shadow-overlay (loading overlay)
- Spacing: 4px base grid (Tailwind default)
- Border radius: cards = rounded-2xl (16px), pills = rounded-full, inputs = rounded-xl (12px)

## Stack
Plain HTML + Tailwind CSS (loaded via CDN `<script>`) + vanilla JavaScript. No React, no Next.js, no build step. Leaflet.js also loaded via CDN. Output is static `.html` files served by FastAPI's `StaticFiles`.

## Typography
- Heading: "Plus Jakarta Sans" (Google Fonts) — geometric, confident, friendly
- Body: "Inter" (Google Fonts) — maximum readability
- Both loaded via `<link>` tag in `<head>` of `index.html`

## Day Palette Rationale
- day-1: Indigo — confident, first-day anchor color
- day-2: Teal — fresh, spatial separation from indigo
- day-3: Amber — warm midpoint, evokes afternoon/sunset
- day-4: Rose — distinct from amber, warm but different hue family
- day-5: Violet — closing day, distinct from indigo (lighter/more purple)
All chosen to be visually distinct on OSM tile backgrounds (pale gray/beige street map).

## Key Aesthetic Decisions
- Background: oklch(0.98 0.004 85) — warm off-white, not pure white
- Primary accent: oklch(0.55 0.18 264) — indigo, not coral (overrides agent default)
- Cards: 16px border radius, shadow-soft at rest, shadow-lift on hover
- No loud gradients; subtle surface variation only
- Map container: no chrome — full bleed to viewport edge on left panel
