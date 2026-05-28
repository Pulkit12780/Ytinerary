Colour Palettes Reference
Curated palettes for each design direction. Use these as starting points — adjust to match brand.

Editorial Luxury
Warm, sophisticated, high-end magazines and luxury agencies.
css:root {
  --bg:          #F7F3EC;  /* warm cream */
  --bg-alt:      #EDE8DF;  /* slightly darker cream for sections */
  --text:        #1A1814;  /* near-black with warmth */
  --text-muted:  #8C8880;  /* warm mid-grey */
  --accent:      #C4A882;  /* warm gold */
  --accent-dark: #8A6F52;  /* darker gold for hover */
  --border:      #D8D2C8;  /* subtle divider */
}
Font pairing: Fraunces (display) + Outfit (body)
Mood: Slow, considered, unhurried

Dark Cinematic
Tech products, games, SaaS, creative agencies with a dark aesthetic.
css:root {
  --bg:          #080B0F;  /* near-black with blue undertone */
  --bg-alt:      #0F1419;  /* cards/sections */
  --text:        #E8EDF2;  /* cool off-white */
  --text-muted:  #6B7280;  /* medium grey */
  --accent:      #3B82F6;  /* electric blue */
  --accent-glow: rgba(59, 130, 246, 0.2); /* glow effect */
  --border:      #1F2937;  /* subtle dark border */
}
Font pairing: Space Grotesk (display) + Inter (body)
Mood: Intense, technical, dramatic

Soft Organic
Wellness, food, sustainable brands, lifestyle.
css:root {
  --bg:          #FAF7F2;  /* warm white */
  --bg-alt:      #F0EBE3;  /* light sand */
  --text:        #2D2926;  /* dark brown */
  --text-muted:  #9B9289;  /* warm grey */
  --accent:      #7C9A6E;  /* sage green */
  --accent-alt:  #C17F52;  /* terracotta */
  --border:      #E5DDD5;  /* light warm border */
}
Font pairing: Cormorant Garamond (display) + DM Sans (body)
Mood: Calm, natural, trustworthy

Brutalist Raw
Artist studios, experimental agencies, avant-garde brands.
css:root {
  --bg:          #F0EDE8;  /* dirty white */
  --bg-alt:      #E5E1DB;
  --text:        #000000;  /* pure black */
  --text-muted:  #555555;
  --accent:      #FF3300;  /* aggressive red */
  --accent-alt:  #FFE000;  /* electric yellow */
  --border:      #000000;  /* thick black borders */
}
Font pairing: Bebas Neue (display) + IBM Plex Mono (body/details)
Mood: Bold, confrontational, unforgettable

Playful Bold
Consumer apps, food delivery, kids products, social platforms.
css:root {
  --bg:          #FFFBF5;  /* warm white */
  --bg-alt:      #FFF0D6;  /* light yellow */
  --text:        #1A1006;  /* dark brown */
  --text-muted:  #7A6A50;
  --accent:      #FF5F1F;  /* bold orange */
  --accent-2:    #7B61FF;  /* electric purple */
  --accent-3:    #00C896;  /* mint green */
  --border:      #E8D5B0;
}
Font pairing: Nunito (display, rounded) + Nunito (body, lighter weight)
Mood: Energetic, friendly, approachable

Minimal Precision
Fintech, productivity tools, B2B SaaS, developer tools.
css:root {
  --bg:          #FFFFFF;
  --bg-alt:      #F8F9FA;  /* light grey */
  --text:        #111827;  /* near-black */
  --text-muted:  #6B7280;
  --accent:      #111827;  /* black as accent */
  --accent-alt:  #2563EB;  /* link blue */
  --border:      #E5E7EB;  /* clean grey */
  --mono:        'JetBrains Mono', monospace;  /* for code/data */
}
Font pairing: Syne (display) + Inter (body)
Mood: Precise, trustworthy, data-forward

Neon Underground
Clubs, music, nightlife, gaming, youth culture.
css:root {
  --bg:          #0A0A0A;  /* true black */
  --bg-alt:      #111111;
  --text:        #FFFFFF;
  --text-muted:  #666666;
  --accent:      #39FF14;  /* neon green */
  --accent-2:    #FF0080;  /* hot pink */
  --accent-3:    #00FFFF;  /* cyan */
  --border:      #222222;
  --glow-green:  0 0 20px rgba(57, 255, 20, 0.4);
  --glow-pink:   0 0 20px rgba(255, 0, 128, 0.4);
}
Font pairing: Bebas Neue (display) + JetBrains Mono (body)
Mood: Electric, underground, raw energy

Usage notes

Never mix warm and cool neutrals — if your background is warm cream, your greys should have a warm undertone too
Accent colour used sparingly — aim for max 10–15% of the visual area. If your accent is everywhere, it's not an accent
Test contrast — ensure text on background meets WCAG AA (4.5:1 ratio for body, 3:1 for large text)
Dark mode consideration — if building dark mode, use HSL values so you can rotate lightness cleanly