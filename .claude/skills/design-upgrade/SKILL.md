Design Upgrade Skill
This skill upgrades basic HTML/CSS websites to award-winning quality by applying the design
principles, motion techniques, and visual strategies used on Awwwards-winning sites.
What the user provides

Their existing HTML/CSS/JS files (uploaded or pasted), OR
A description of what their site looks like / does, OR
A specific area they want improved (typography, layout, animations, etc.)

Your process
Step 1 — Understand the site
Read the existing code. Identify:

Purpose: Portfolio, agency, landing page, product, blog?
Current problems: Generic fonts, flat layout, no motion, boring colours, poor spacing?
Constraints: Must keep the same content? Specific brand colours? Framework restrictions?

If no code is provided, ask for it or for a clear description before proceeding.
Step 2 — Choose a design direction
Before writing a single line of code, commit to a bold aesthetic. Pick ONE direction:
DirectionGood forSignature traitsEditorial luxuryPortfolio, agency, fashionBlack/cream, oversized serif display, massive negative spaceBrutalist rawStudios, artists, techBold grid lines, system fonts used boldly, high contrastSoft organicWellness, food, lifestyleWarm off-whites, rounded forms, earthy palette, gentle motionDark cinematicGames, tech, SaaSNear-black bg, glowing accents, particle effects, depthPlayful boldConsumer apps, kids, foodBright palette, bouncy animation, chunky type, fun cursorsMinimal precisionFintech, tools, B2BGenerous whitespace, mono accents, data-forward, no decoration
State your chosen direction before writing code. Example: "I'm going for Editorial Luxury — oversized Playfair Display hero, cream background, lots of whitespace, subtle scroll reveals."
Step 3 — Apply the upgrade layers (in priority order)
Read /references/techniques.md for full implementation details on each layer.
Layer 1 — Typography (highest impact, easiest win)

Replace generic fonts (Roboto, Arial, system) with a distinctive pairing
Scale hero text to clamp(3rem, 10vw, 9rem) — go bigger than feels comfortable
Tighten letter-spacing: -0.02em to -0.05em on large display text
Loosen body line-height to 1.7–1.8

Layer 2 — Colour & atmosphere

Commit to a dominant background that isn't pure white or pure black (try #F5F0E8, #0D0D0D, #1A1A2E)
Add one strong accent colour used sparingly
Apply a subtle noise texture overlay (4% opacity SVG grain = instant depth)

Layer 3 — Spatial layout

Increase all section padding to at least 120px vertical
Break at least one element out of the center column — let it bleed to an edge
Use CSS Grid with named areas, not divs stacked in a column

Layer 4 — Motion & scroll

Add a load sequence: stagger hero elements with animation-delay
Add scroll-triggered fade/slide reveals using IntersectionObserver (no library needed for basic version) or GSAP ScrollTrigger (for advanced)
Add hover states to every interactive element — not just color changes, but scale, translate, or text reveal

Layer 5 — Details that judges notice

Custom cursor (if desktop-focused)
Smooth scroll via CSS scroll-behavior: smooth or Lenis.js
Image hover effects (scale, greyscale → colour, clip-path reveal)
Footer with proper typographic treatment

Step 4 — Deliver the output

Always output complete, working HTML/CSS/JS — never pseudocode or partial snippets
Preserve all original content (text, links, images)
Add inline comments explaining key techniques so the user can learn
Output as a single self-contained .html file unless the original was multi-file

Step 5 — Explain what changed
After the file, write a brief "What I changed and why" section covering:

Typography choices made
Colour rationale
Which animations were added and how they work
What library (if any) was added and why


Quality checklist
Before delivering, verify:

 No generic fonts (Roboto, Arial, system-ui used generically)
 Hero text is large — genuinely large, not just "a bit bigger"
 At least one scroll animation or page-load entrance
 Hover states on all buttons and links go beyond colour change
 Colour palette has a clear hierarchy (dominant / secondary / accent)
 Mobile responsive (test mentally at 375px)
 All original content preserved
 No broken references (images, fonts loaded via CDN)


Recommended CDN resources (always available, no install needed)
html<!-- Fonts — pick one pairing -->
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=Inter:wght@300;400&display=swap" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,300;9..144,700&family=Outfit:wght@300;400;500&display=swap" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;600&display=swap" rel="stylesheet">

<!-- GSAP (animation) -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/ScrollTrigger.min.js"></script>

<!-- Lenis (smooth scroll) -->
<script src="https://cdn.jsdelivr.net/npm/@studio-freight/lenis@1.0.42/dist/lenis.min.js"></script>

Reference files

references/techniques.md — Full code patterns for every technique (typography, animations, cursors, noise textures, scroll effects, page transitions)
references/palettes.md — Curated colour palettes by design direction with hex values

Read these when you need implementation specifics for a particular technique.