---
name: component-patterns
description: Established component patterns for Ytinerary v1 — accordion, rail, pin anatomy
metadata:
  type: project
---

## PlaceCard
Uses accordion expand/collapse via CSS `max-height` transition (0 → 600px). Collapsed height: 80px. Expanded: auto (image 160px + content). Transition: 320ms ease-out. No Framer Motion — pure CSS + vanilla JS `classList` toggle.

## Sidebar
Collapsible to 48px icon rail. Collapse button: floating pill at top of sidebar. When collapsed, only DaySectionHeader icons + day number visible. Expand/collapse: 250ms width transition, ease-out-smooth.

## Map Pins
HTML-based L.divIcon (not SVG file). Anatomy: outer wrapper div (.map-pin), inner dot (.map-pin__dot), number label (.map-pin__label). Hotel pin uses a building icon character instead of number. Tail (pointer) is a CSS triangle pseudo-element on .map-pin.

## URLInputRow
Each row is a flex container: URL input (flex-1) + remove button (32px icon button). "Add another URL" is a ghost `<button>` below the list. Rows animate in with a 200ms height + opacity CSS transition when added via vanilla JS `insertAdjacentHTML`.

## LoadingOverlay
Full-screen fixed overlay, z-index 50. Semi-transparent backdrop blur. Progress bar is a linear-gradient animated strip inside a fixed-height track (8px). Step label transitions with a 200ms fade + 4px upward slide between steps.

## DaySectionHeader
Sticky within sidebar scroll container. Contains: colored day badge pill (day token), day label text (Plus Jakarta Sans, semibold), place count chip. Click to filter map to that day only.

## MapTooltip
Leaflet popup with custom CSS override (.leaflet-popup-content-wrapper). Pill shape, shadow-lift, no default Leaflet triangle replaced with CSS triangle via ::after on wrapper. Shows: place name (semibold), category icon + text, star rating.

## ErrorBanner
Non-blocking, appears at top of sidebar (not full-page). Amber warning color. Dismissible with X button. Auto-dismisses after 8000ms.

## UnresolvedPlacePill
Small pill chip in sidebar below day sections. Gray background, italic place name, × remove button. NOT a full PlaceCard.
