# Ytinerary — Website Design Specification
*Version 2.0 | Uber Design Language | 2026-05-28 | Desktop-first website (min 1280px)*

---

## 0. Design Principles

- **Bold contrast** — Black on white. High-contrast at every level. `#000000` text on `#FFFFFF` surface. No warm intermediary tones carry meaning.
- **Typography does the work** — Large, heavy display text (56px hero, tight −0.04em tracking) makes the statement. Color is not decoration; hierarchy is typographic.
- **Black as the anchor** — Primary CTA is `#000000`. Nothing competes for the user's next action.
- **Green as signal** — `#06C167` (Uber green) marks active, success, and completion states only. Never used decoratively.
- **Clean surfaces** — No mesh gradients, no ambient orbs, no blurred circles. White is the canvas. Optional: subtle dot-grid texture at 3% opacity.
- **Map is the hero** — The results page exists to serve the map. The sidebar is a clean, functional tool.
- **Functional motion** — Animations confirm state changes. They do not entertain. Durations: 100ms hover, 180ms state, 280ms transition, 400ms page entrance. Nothing idles unless the form is complete.
- **Desktop-first** — Primary user is a pre-trip researcher at a desk. 1280px primary breakpoint.

---

## 1. Design Tokens

### 1.1 `tokens.json`

> Full token reference: see `design-tokens-spec.md`. Summary below.

```json
{
  "color": {
    "background": "#FFFFFF",
    "background-secondary": "#F6F6F6",
    "surface": "#FFFFFF",
    "surface-elevated": "#FFFFFF",
    "border": "#E2E2E2",
    "border-subtle": "#F0F0F0",

    "text-primary": "#000000",
    "text-secondary": "#545454",
    "text-muted": "#8A8A8A",
    "text-inverse": "#FFFFFF",

    "primary": "#000000",
    "primary-hover": "#1A1A1A",
    "primary-foreground": "#FFFFFF",

    "accent": "#06C167",
    "accent-hover": "#049C52",
    "accent-subtle": "#E6FAF0",
    "accent-foreground": "#FFFFFF",

    "error": "#C7282D",
    "error-subtle": "#FFF0F0",
    "warning": "#F6A609",
    "warning-subtle": "#FFFBEB",
    "success": "#05944F",
    "success-subtle": "#E6FAF0",

    "day-1": "#276EF1",
    "day-2": "#06C167",
    "day-3": "#FF974A",
    "day-4": "#7356BF",
    "day-5": "#E85D99",
    "day-1-subtle": "#EAF0FE",
    "day-2-subtle": "#E6FAF0",
    "day-3-subtle": "#FFF3EB",
    "day-4-subtle": "#F0ECFB",
    "day-5-subtle": "#FEF0F7",

    "hotel": "#000000",
    "hotel-subtle": "#F6F6F6",

    "overlay": "rgba(0, 0, 0, 0.65)",

    "sparkle": "#F6A609",
    "route-line": "rgba(39, 110, 241, 0.60)"
  },

  "gradient": {
    "subtle-grid": "repeating-linear-gradient(0deg, transparent, transparent 39px, rgba(0,0,0,0.03) 39px, rgba(0,0,0,0.03) 40px), repeating-linear-gradient(90deg, transparent, transparent 39px, rgba(0,0,0,0.03) 39px, rgba(0,0,0,0.03) 40px)",
    "card-sheen": "linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(255,255,255,0.70) 100%)",
    "day-glow-1": "radial-gradient(circle, rgba(39,110,241,0.18) 0%, transparent 65%)",
    "day-glow-2": "radial-gradient(circle, rgba(6,193,103,0.18) 0%, transparent 65%)",
    "day-glow-3": "radial-gradient(circle, rgba(255,151,74,0.18) 0%, transparent 65%)",
    "day-glow-4": "radial-gradient(circle, rgba(115,86,191,0.18) 0%, transparent 65%)",
    "day-glow-5": "radial-gradient(circle, rgba(232,93,153,0.18) 0%, transparent 65%)",
    "shimmer": "linear-gradient(90deg, transparent 0%, rgba(255,255,255,0.80) 50%, transparent 100%)"
  },

  "font": {
    "family-display": "'Uber Move', 'Manrope', -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif",
    "family-body": "'Uber Move', 'Manrope', -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif",
    "family-mono": "'JetBrains Mono', 'Fira Code', monospace"
  },

  "fontSize": {
    "xs": "11px",
    "sm": "13px",
    "base": "16px",
    "md": "17px",
    "lg": "20px",
    "xl": "24px",
    "2xl": "32px",
    "3xl": "40px",
    "4xl": "56px",
    "display": "72px"
  },

  "fontWeight": {
    "regular": "400",
    "medium": "500",
    "semibold": "600",
    "bold": "700"
  },

  "lineHeight": {
    "display": "1.0",
    "tight": "1.1",
    "snug": "1.2",
    "normal": "1.5",
    "relaxed": "1.65"
  },

  "letterSpacing": {
    "display": "-0.04em",
    "tight": "-0.03em",
    "heading": "-0.02em",
    "normal": "0em",
    "wide": "0.04em",
    "wider": "0.06em"
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
    "card-hover": "0 8px 24px rgba(0,0,0,0.10)",
    "card-lift": "0 16px 40px -8px rgba(15, 23, 42, 0.18), 0 4px 8px -2px rgba(15, 23, 42, 0.06)",
    "glow-accent": "0 0 0 4px rgba(37, 99, 235, 0.18), 0 8px 24px -8px rgba(37, 99, 235, 0.38)",
    "glow-success": "0 0 0 4px rgba(22, 163, 74, 0.18), 0 8px 24px -8px rgba(22, 163, 74, 0.38)",
    "glow-error": "0 0 0 4px rgba(220, 38, 38, 0.18)",
    "pin-rest": "0 2px 4px rgba(15, 23, 42, 0.25)",
    "pin-active": "0 8px 16px rgba(15, 23, 42, 0.35)",
    "inset-subtle": "inset 0 1px 0 0 rgba(255, 255, 255, 0.65)"
  },

  "blur": {
    "sm": "blur(2px)",
    "md": "blur(4px)",
    "lg": "blur(12px)",
    "backdrop": "blur(8px) saturate(140%)"
  },

  "transition": {
    "fast": "120ms ease-out",
    "base": "200ms ease-out",
    "slow": "320ms ease-out",
    "slower": "480ms ease-out",
    "spring-soft": "320ms cubic-bezier(0.34, 1.40, 0.64, 1)",
    "spring": "400ms cubic-bezier(0.34, 1.56, 0.64, 1)",
    "spring-bouncy": "520ms cubic-bezier(0.22, 1.61, 0.36, 1)",
    "snap": "160ms cubic-bezier(0.32, 0.72, 0, 1)",
    "decelerate": "320ms cubic-bezier(0.05, 0.7, 0.1, 1)",
    "accelerate": "200ms cubic-bezier(0.3, 0, 0.8, 0.15)"
  },

  "easing": {
    "standard": "cubic-bezier(0.2, 0, 0, 1)",
    "decelerate": "cubic-bezier(0.05, 0.7, 0.1, 1)",
    "accelerate": "cubic-bezier(0.3, 0, 0.8, 0.15)",
    "spring-soft": "cubic-bezier(0.34, 1.40, 0.64, 1)",
    "spring": "cubic-bezier(0.34, 1.56, 0.64, 1)",
    "spring-bouncy": "cubic-bezier(0.22, 1.61, 0.36, 1)",
    "snap": "cubic-bezier(0.32, 0.72, 0, 1)"
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
      ambient: {
        warm: '#FAF6EE',
        cool: '#EEF3F8',
        blush: '#FAF0F3',
      },
      sparkle: '#FCD34D',
    },
    backgroundImage: {
      'hero-mesh': 'radial-gradient(at 18% 22%, #EFF4FF 0%, transparent 42%), radial-gradient(at 82% 18%, #FAF0F3 0%, transparent 38%), radial-gradient(at 50% 88%, #F0FDF4 0%, transparent 45%)',
      'card-sheen': 'linear-gradient(135deg, rgba(255,255,255,0.9) 0%, rgba(255,255,255,0.6) 100%)',
      'accent-glow': 'radial-gradient(circle, rgba(37,99,235,0.18) 0%, transparent 70%)',
      'shimmer': 'linear-gradient(90deg, transparent 0%, rgba(255,255,255,0.65) 50%, transparent 100%)',
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
      'card-lift': '0 16px 40px -8px rgba(15, 23, 42, 0.18), 0 4px 8px -2px rgba(15, 23, 42, 0.06)',
      'glow-accent': '0 0 0 4px rgba(37, 99, 235, 0.18), 0 8px 24px -8px rgba(37, 99, 235, 0.38)',
      'glow-success': '0 0 0 4px rgba(22, 163, 74, 0.18), 0 8px 24px -8px rgba(22, 163, 74, 0.38)',
      'glow-error': '0 0 0 4px rgba(220, 38, 38, 0.18)',
      'pin-rest': '0 2px 4px rgba(15, 23, 42, 0.25)',
      'pin-active': '0 8px 16px rgba(15, 23, 42, 0.35)',
    },
    borderRadius: {
      sm: '4px',
      md: '8px',
      lg: '12px',
      xl: '16px',
      '2xl': '24px',
    },
    transitionTimingFunction: {
      standard: 'cubic-bezier(0.2, 0, 0, 1)',
      decelerate: 'cubic-bezier(0.05, 0.7, 0.1, 1)',
      accelerate: 'cubic-bezier(0.3, 0, 0.8, 0.15)',
      'spring-soft': 'cubic-bezier(0.34, 1.40, 0.64, 1)',
      spring: 'cubic-bezier(0.34, 1.56, 0.64, 1)',
      'spring-bouncy': 'cubic-bezier(0.22, 1.61, 0.36, 1)',
      snap: 'cubic-bezier(0.32, 0.72, 0, 1)',
    },
    keyframes: {
      'pulse-soft': {
        '0%, 100%': { opacity: '1' },
        '50%': { opacity: '0.55' },
      },
      'pulse-ring': {
        '0%': { transform: 'scale(0.8)', opacity: '0.6' },
        '100%': { transform: 'scale(2.2)', opacity: '0' },
      },
      'breathe': {
        '0%, 100%': { transform: 'scale(1)' },
        '50%': { transform: 'scale(1.04)' },
      },
      'shimmer': {
        '0%': { backgroundPosition: '-200% 0' },
        '100%': { backgroundPosition: '200% 0' },
      },
      'pin-drop': {
        '0%': { transform: 'translateY(-40px) scale(0.6)', opacity: '0' },
        '60%': { transform: 'translateY(4px) scale(1.05)', opacity: '1' },
        '100%': { transform: 'translateY(0) scale(1)', opacity: '1' },
      },
      'route-draw': {
        '0%': { strokeDashoffset: '1000' },
        '100%': { strokeDashoffset: '0' },
      },
      'sparkle': {
        '0%, 100%': { transform: 'scale(0) rotate(0deg)', opacity: '0' },
        '50%': { transform: 'scale(1) rotate(180deg)', opacity: '1' },
      },
      'ambient-drift': {
        '0%, 100%': { transform: 'translate(0, 0)' },
        '33%': { transform: 'translate(20px, -10px)' },
        '66%': { transform: 'translate(-15px, 8px)' },
      },
      'slide-up-fade': {
        '0%': { transform: 'translateY(12px)', opacity: '0' },
        '100%': { transform: 'translateY(0)', opacity: '1' },
      },
      'check-draw': {
        '0%': { strokeDashoffset: '24' },
        '100%': { strokeDashoffset: '0' },
      },
    },
    animation: {
      'pulse-soft': 'pulse-soft 1800ms ease-in-out infinite',
      'pulse-ring': 'pulse-ring 1800ms ease-out infinite',
      'breathe': 'breathe 4s ease-in-out infinite',
      'shimmer': 'shimmer 1600ms linear infinite',
      'pin-drop': 'pin-drop 520ms cubic-bezier(0.22, 1.61, 0.36, 1) backwards',
      'route-draw': 'route-draw 1200ms ease-out forwards',
      'sparkle': 'sparkle 800ms ease-out forwards',
      'ambient-drift': 'ambient-drift 18s ease-in-out infinite',
      'slide-up-fade': 'slide-up-fade 320ms cubic-bezier(0.05, 0.7, 0.1, 1) backwards',
      'check-draw': 'check-draw 280ms ease-out 80ms forwards',
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

  --color-ambient-warm: #FAF6EE;
  --color-ambient-cool: #EEF3F8;
  --color-ambient-blush: #FAF0F3;
  --color-sparkle: #FCD34D;
  --color-route-line: rgba(37, 99, 235, 0.55);

  /* Gradients */
  --gradient-hero-mesh: radial-gradient(at 18% 22%, #EFF4FF 0%, transparent 42%), radial-gradient(at 82% 18%, #FAF0F3 0%, transparent 38%), radial-gradient(at 50% 88%, #F0FDF4 0%, transparent 45%), #F8F7F4;
  --gradient-card-sheen: linear-gradient(135deg, rgba(255,255,255,0.9) 0%, rgba(255,255,255,0.6) 100%);
  --gradient-accent-glow: radial-gradient(circle, rgba(37,99,235,0.18) 0%, transparent 70%);
  --gradient-shimmer: linear-gradient(90deg, transparent 0%, rgba(255,255,255,0.65) 50%, transparent 100%);

  /* Shadows */
  --shadow-sm: 0 1px 2px 0 rgba(0,0,0,0.05);
  --shadow-md: 0 4px 6px -1px rgba(0,0,0,0.08), 0 2px 4px -2px rgba(0,0,0,0.05);
  --shadow-lg: 0 10px 15px -3px rgba(0,0,0,0.08), 0 4px 6px -4px rgba(0,0,0,0.05);
  --shadow-xl: 0 20px 25px -5px rgba(0,0,0,0.10), 0 8px 10px -6px rgba(0,0,0,0.05);
  --shadow-tooltip: 0 4px 16px rgba(0,0,0,0.14);
  --shadow-card-hover: 0 8px 24px rgba(0,0,0,0.10);
  --shadow-card-lift: 0 16px 40px -8px rgba(15, 23, 42, 0.18), 0 4px 8px -2px rgba(15, 23, 42, 0.06);
  --shadow-glow-accent: 0 0 0 4px rgba(37, 99, 235, 0.18), 0 8px 24px -8px rgba(37, 99, 235, 0.38);
  --shadow-glow-success: 0 0 0 4px rgba(22, 163, 74, 0.18), 0 8px 24px -8px rgba(22, 163, 74, 0.38);
  --shadow-glow-error: 0 0 0 4px rgba(220, 38, 38, 0.18);
  --shadow-pin-rest: 0 2px 4px rgba(15, 23, 42, 0.25);
  --shadow-pin-active: 0 8px 16px rgba(15, 23, 42, 0.35);

  /* Blur */
  --blur-sm: blur(2px);
  --blur-md: blur(4px);
  --blur-lg: blur(12px);
  --blur-backdrop: blur(8px) saturate(140%);

  /* Easing */
  --ease-standard: cubic-bezier(0.2, 0, 0, 1);
  --ease-decelerate: cubic-bezier(0.05, 0.7, 0.1, 1);
  --ease-accelerate: cubic-bezier(0.3, 0, 0.8, 0.15);
  --ease-spring-soft: cubic-bezier(0.34, 1.40, 0.64, 1);
  --ease-spring: cubic-bezier(0.34, 1.56, 0.64, 1);
  --ease-spring-bouncy: cubic-bezier(0.22, 1.61, 0.36, 1);
  --ease-snap: cubic-bezier(0.32, 0.72, 0, 1);

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
  --transition-slower: 480ms ease-out;
  --transition-spring-soft: 320ms var(--ease-spring-soft);
  --transition-spring: 400ms var(--ease-spring);
  --transition-spring-bouncy: 520ms var(--ease-spring-bouncy);
  --transition-snap: 160ms var(--ease-snap);
  --transition-decelerate: 320ms var(--ease-decelerate);
  --transition-accelerate: 200ms var(--ease-accelerate);
}

/* Global motion primitives — load once, reuse everywhere */
@keyframes pulse-soft {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.55; }
}
@keyframes pulse-ring {
  0%   { transform: scale(0.8); opacity: 0.6; }
  100% { transform: scale(2.2); opacity: 0; }
}
@keyframes breathe {
  0%, 100% { transform: scale(1); }
  50%      { transform: scale(1.04); }
}
@keyframes shimmer {
  0%   { background-position: -200% 0; }
  100% { background-position: 200% 0; }
}
@keyframes pin-drop {
  0%   { transform: translateY(-40px) scale(0.6); opacity: 0; }
  60%  { transform: translateY(4px) scale(1.05); opacity: 1; }
  100% { transform: translateY(0) scale(1); opacity: 1; }
}
@keyframes route-draw {
  0%   { stroke-dashoffset: 1000; }
  100% { stroke-dashoffset: 0; }
}
@keyframes sparkle {
  0%, 100% { transform: scale(0) rotate(0deg); opacity: 0; }
  50%      { transform: scale(1) rotate(180deg); opacity: 1; }
}
@keyframes ambient-drift {
  0%, 100% { transform: translate(0, 0); }
  33%      { transform: translate(20px, -10px); }
  66%      { transform: translate(-15px, 8px); }
}
@keyframes slide-up-fade {
  0%   { transform: translateY(12px); opacity: 0; }
  100% { transform: translateY(0); opacity: 1; }
}
@keyframes check-draw {
  0%   { stroke-dashoffset: 24; }
  100% { stroke-dashoffset: 0; }
}

/* Universal reduced-motion override (see Section 12) */
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

### 1.4 Motion Language

Motion is a vocabulary, not decoration. Each easing has a single, defined role. Don't invent new curves — pick from this table.

| Token | Curve | Use for | Don't use for |
|---|---|---|---|
| `--transition-fast` (120ms ease-out) | Linear-ish ease-out | Hover color/bg flips, focus rings, tooltip fades | Position changes, size changes |
| `--transition-base` (200ms ease-out) | ease-out | Standard hover lifts, opacity reveals, inline state | Long-distance motion |
| `--transition-decelerate` (320ms) | `cubic-bezier(0.05, 0.7, 0.1, 1)` | Element entering screen (cards, banners) | Exits |
| `--transition-accelerate` (200ms) | `cubic-bezier(0.3, 0, 0.8, 0.15)` | Element exiting screen | Entrances |
| `--transition-snap` (160ms) | `cubic-bezier(0.32, 0.72, 0, 1)` | Tab switches, segmented control, instant-but-not-jarring toggles | Lifts |
| `--transition-spring-soft` (320ms) | `cubic-bezier(0.34, 1.4, 0.64, 1)` | Sidebar collapse, panel reveals — overshoots subtly | Buttons |
| `--transition-spring` (400ms) | `cubic-bezier(0.34, 1.56, 0.64, 1)` | Day-pin selection, toggle thumbs, badge pops | Anything text-heavy |
| `--transition-spring-bouncy` (520ms) | `cubic-bezier(0.22, 1.61, 0.36, 1)` | Pin drops on results-page entrance, success confirmations | Hover states (too aggressive) |

**Duration ladder.** Anchor every choice to one of these:

| Speed | Duration | Feels like |
|---|---|---|
| Instant | 80–120ms | Direct response (hover, focus) |
| Quick | 160–200ms | Acknowledged action (click, toggle) |
| Smooth | 280–400ms | State transition (panel, expand) |
| Cinematic | 480–800ms | Page enter, hero choreography |
| Ambient | 1.8–4s loop | Idle breath (pulse, drift, shimmer) |

**Stagger rule.** When animating a list, delay each child by **40ms** (default). For pin drops on the map, **60ms** to give each one room. Never exceed 8 staggered items — past that, use a single fade.

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
- Height: 60px
- Background: `#FFFFFF` at rest
- Border-bottom: 1px solid `#E2E2E2`
- Shadow: none at rest
- On scroll past 16px: shadow upgrades to `shadow-md`. Transition `--transition-base`.
- Logo: `Y·tinerary` — Manrope Bold (700) 18px
  - The "Y" renders in `#06C167` (Uber green accent)
  - The "·" renders in `#06C167`
  - "tinerary" renders in `#000000`
  - Letter-spacing: `-0.02em`
  - No idle animations — static
- Padding horizontal: 32px

### 2.3 Hero Section

#### Background
- Page background: `#FFFFFF` (pure white)
- Optional subtle grid texture on hero section at 3% opacity:
  ```css
  background-image:
    repeating-linear-gradient(0deg, transparent, transparent 39px, rgba(0,0,0,0.03) 39px, rgba(0,0,0,0.03) 40px),
    repeating-linear-gradient(90deg, transparent, transparent 39px, rgba(0,0,0,0.03) 39px, rgba(0,0,0,0.03) 40px);
  ```
- No ambient orbs. No gradient mesh. Clean canvas.

#### Layout
- `padding-top: 96px`, `padding-bottom: 64px`
- `text-align: center`, `max-width: 900px`, `mx: auto`
- Heading: "Turn YouTube travel videos into a day-by-day itinerary."
  - Manrope Bold (700) 56px, `#000000`, letter-spacing `-0.04em`, line-height `1.0`
  - Split across 2 lines: "Turn YouTube travel videos" / "into a day-by-day itinerary."
  - **Entrance choreography**: each line `slide-up-fade` with 60ms stagger, 280ms decelerate
- Subtitle: Manrope Regular (400) 18px, `#545454`, `margin-top: 16px`, `max-width: 540px`, `mx: auto`
  - Fade-in opacity 0→1, 200ms, delay 350ms

#### Social proof strip
- Below subtitle, `margin-top: 24px`
- 4 creator avatar circles (28px, overlapping −8px, white 2px ring), followed by "Built from videos by Mumbiker Nikhil, Curly Tales, +28 more" in Manrope Regular 14px `#545454`
- Static display — no hover animation

### 2.4 Form Card
- `max-width: 640px`, `margin: 40px auto 80px`
- Background: `#FFFFFF`
- Border: `1px solid #E2E2E2`
- Border-radius: `16px`
- Shadow: `shadow-sm` at rest, `shadow-lg` when any field is focused (180ms ease-out)
- Padding: `32px`
- **Entrance**: `slide-up-fade`, opacity 0→1, translateY 10px→0, 400ms decelerate, delay 350ms after subtitle
- **No idle animation** — static at rest (no breathe, no parallax)

#### Field layout within card:
- Field gap: `24px` (vertical)
- Section dividers: `1px solid #EDECEA` between logical groups
- Label: Inter Medium 13px, `#1A1917`, `margin-bottom: 6px`
- Required marker: `*` in `#DC2626`, same font
- Helper text: Inter Regular 12px, `#9B9891`, `margin-top: 4px`

#### Input styling (rest → hover → focus → valid → invalid):

| State | Border | Background | Shadow | Note |
|---|---|---|---|---|
| Rest | `1px solid #E4E2DC` | `#FFFFFF` | — | — |
| Hover | `1px solid #C7C5BE` | `#FFFFFF` | — | Transition `--transition-fast` |
| Focus | `1px solid #2563EB` | `#FFFFFF` | `--shadow-glow-accent` | Transition 120ms border, 120ms shadow |
| Valid (after blur, value present) | `1px solid #E4E2DC` | `#FFFFFF` | — | Inline ✓ in `#16A34A` slides in from right (`translateX(8px → 0px)`, 200ms `--ease-spring-soft`) |
| Invalid (after blur) | `1px solid #DC2626` | `#FEF2F2` | `--shadow-glow-error` | 3px horizontal shake (`translateX: 0 → -3px → 3px → 0`, 200ms ease-out, runs once) |

- Height: 40px (single-line), auto-height (multi-line)
- Border-radius: `8px`
- Text: Inter Regular 14px, `#1A1917`
- Placeholder: `#9B9891`
- Padding: `0 12px` (left padding `36px` if a leading icon present)
- **Caret blink**: rely on browser default (do not animate)

#### Floating label variant (optional, used on Destination)
- Default state: label sits inside the field at 14px, `#9B9891`
- On focus or filled: label translates to `y: -22px` and shrinks to 11px, color `#5C5A55`, with a small `--color-surface` background pad behind it so it sits cleanly on the border. Transition: `transform 180ms --ease-spring-soft, font-size 180ms ease-out, color 180ms ease-out`

#### Submit Button
- Full-width: `width: 100%`
- Height: 48px
- Background: `#000000`
- Text: Manrope Bold (700) 16px, `#FFFFFF`
- Border-radius: `8px`
- Label: "Build My Itinerary →" — the → in its own `<span class="btn-arrow">`
- **Rest**: no shadow
- **Hover**: background `#1A1A1A`, arrow `translateX(+3px)`. 100ms ease-out. No vertical lift.
- **Active (press)**: `scale(0.98)`, 80ms ease-out.
- **Release**: returns to rest 150ms ease-out
- **Ripple on click**: inject `<span class="ripple">` at click point, `background: rgba(255,255,255,0.20)`, expands scale 0→20, opacity 0.3→0, 300ms decelerate. Remove on animationend.
- **Disabled**: background `#E2E2E2`, color `#8A8A8A`, cursor `not-allowed`. No transitions.
- **Loading**: label swaps to "Working..." with 3-dot wave (each dot opacity 0→1→0, delays 0/160/320ms). Background stays `#1A1A1A`. pointer-events: none.
- **Idle attention** (after 4s idle on complete form): arrow nudges `translateX 0→4px→0` every 6s via `arrow-nudge` keyframe. Stops on first hover.

#### Optional Fields Accordion
- Trigger: "Optional details" — Inter Medium 13px, `#5C5A55`, chevron right icon (Lucide `ChevronRight`)
- **Trigger hover**: text color `#1A1917`, chevron `translateX(+2px)`, both 120ms ease-out
- **Expanded**: chevron rotates 90° (`transform: rotate(90deg)`, `--transition-spring-soft`)
- **Expand content**: `max-height: 0 → 280px`, `opacity: 0 → 1`, both `--transition-decelerate`. Inner fields stagger-fade-in with `slide-up-fade` 40ms delay each.
- **Collapse**: `max-height: 280px → 0`, `opacity: 1 → 0`, `--transition-accelerate` (faster going away)
- Content: Hotel field, Dates date-range picker, Google Maps URLs input
- Gap inside: `16px`
- Use a custom HTML `<details>`/`<summary>` accordion styled with Tailwind + CSS transition on max-height

#### Hotel field (optional, inside accordion)
- Standard input + a small `🏨` glyph fades in to the right of the field when the value is valid (`opacity: 0 → 1`, `translateY(4px → 0)`, 200ms `--ease-spring-soft`)

#### Date range picker
- Two `<input type="date">` side-by-side with a `→` arrow between them
- When **both** dates are valid, the arrow pulses once (`scale: 1 → 1.2 → 1` over 320ms, `--ease-spring`) and the inferred day count appears below in Inter Regular 12px `#5C5A55`: "_5 days · clustered into 5 days_" — fades in `slide-up-fade`

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
- A faint radial `--gradient-accent-glow` sits behind the card at `z-index: -1`, scaled to 1.4× the card, with `breathe` animation — turns the modal into a quiet halo on the dim backdrop.

### 3.3 Logo Mark + Mini-Map Animation (the storytelling moment)

This is the loading overlay's hero element. It replaces a generic spinner with a tiny narrative — a route being assembled.

#### Visual
- An 80×80 SVG canvas sits at the top of the card
- Inside it:
  - 5 small day-pin circles (8px) appear one at a time as the pipeline progresses
  - A dotted path (`stroke-dasharray: 3 4`) draws progressively from pin to pin
  - The accent "Y" letterform sits centered behind the pins at 24% opacity

#### Animation sequence (tied to SSE step index 0–3)
| Step | What happens |
|---|---|
| 0 (Fetching transcripts) | "Y" letterform fades up. Background mesh dot grid (10×10, 2px dots in `#E4E2DC`) draws in left-to-right over 800ms. |
| 1 (Extracting places) | Pin 1 drops in at top-left (`pin-drop` animation). Then pin 2 drops 200ms later. Each pin emits one `pulse-ring` on arrival. |
| 2 (Enriching with location) | Pins 3 and 4 drop, also 200ms apart. The first dotted line draws from pin 1 → pin 2 → pin 3 over 1200ms with `route-draw`. |
| 3 (Building day plan) | Final pin drops. The remaining route lines draw, connecting all 5. The full path then flashes a single brighter pulse (stroke-width 1.5 → 2.5 → 1.5 over 320ms). |

If step 4 (results ready) arrives, the whole SVG scales 1 → 1.08 → 1 over 400ms `--ease-spring-bouncy` as a "done" gesture, then the overlay begins exiting.

### 3.4 Typography
- Heading "Building your itinerary...": Inter SemiBold 20px, `#1A1917`, `margin-top: 20px`
- **Step label**: Inter Regular 14px, `#5C5A55`, `margin-top: 8px`, `min-height: 20px`
  - On each new SSE message, the *outgoing* label slides up + fades (`translateY: 0 → -8px, opacity: 1 → 0`, 160ms `--ease-accelerate`), then the *incoming* label slides up from below (`translateY: 8px → 0, opacity: 0 → 1`, 200ms `--ease-decelerate`). Use a wrapper with `overflow: hidden`.
- Footer note "This takes about 30–90 seconds.": Inter Regular 13px, `#9B9891`, `margin-top: 24px`
  - After 60s elapsed, gently swap to "Almost there — finishing up..." (same slide-fade swap). After 90s, swap to "Taking a little longer than usual..." in `#D97706`.

### 3.5 Progress Bar
- Container: `height: 6px`, `border-radius: 9999px`, background `#E4E2DC`, `margin-top: 20px`, `overflow: hidden`
- Fill: `height: 6px`, `border-radius: 9999px`, background `#2563EB`
- 4 SSE steps → fill widths: 15%, 40%, 70%, 95%. On completion: 100%.
- Width transition: `600ms --ease-decelerate` on each step update
- **Shimmer overlay**: a 60px wide gradient (`--gradient-shimmer`) loops left-to-right over the *filled* portion only, 1600ms linear infinite — communicates "actively working" even when the width is stable between steps
- On step change, the fill briefly brightens (`filter: brightness(1.15)` for 200ms) — a subtle "tick" of progress

### 3.6 Overlay Entrance + Exit Animation

#### Entrance
- Overlay: `opacity: 0 → 1`, 200ms `--ease-decelerate`
- Card: `opacity: 0, translateY: 12px, scale: 0.96 → opacity: 1, translateY: 0, scale: 1`, 400ms `--ease-spring-soft`, delay 80ms

#### Exit (when pipeline completes successfully)
- Card: `scale: 1 → 1.04 → 0.92, opacity: 1 → 0`, 400ms — a tiny "lift off, then dive into the results" gesture
- Overlay: `opacity: 1 → 0`, 280ms `--ease-accelerate`, starting 80ms into card exit
- The results page underneath fades in (`opacity: 0 → 1`, 480ms `--ease-decelerate`) so the cut isn't visible
- During the handoff, the mini-map pins from the loading overlay can "teleport" to their real positions on the actual map — implement only if time allows; skip if it complicates the routing

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
- **Hover**: shadow `shadow-md`, `transform: scale(1.08)`, 120ms ease-out
- **Press**: `scale: 0.95`, 80ms
- **On toggle**: chevron rotates 180° over `--transition-spring-soft`. The button briefly leaves a `pulse-ring` ripple behind it in `--color-accent-subtle`.
- Collapsed sidebar: `width: 0`, map expands to fill via flex; both transition `--transition-spring-soft` (sidebar overshoots subtly when expanding back).
- When sidebar is collapsed, the toggle floats free against the map — give it `shadow-md` to read against the map tiles.

---

## 5. Component Specs

### 5.1 URLInputRow

Single URL text field that **transforms into a video preview card** the moment a valid YouTube URL is detected. Stacked vertically for multi-URL input.

#### Empty / invalid state
```
┌─────────────────────────────────────────────────┐ [×]
│  ▶  Paste a YouTube URL...                     │
└─────────────────────────────────────────────────┘
[+ Add another video]
```

- Input: full-width, height 40px (standard input styling)
- Leading icon: small ▶ play glyph in `#9B9891`, fades to `#DC2626` (YouTube red) when a valid URL is being typed
- Remove button `[×]`: 28px × 28px, `border-radius: 9999px`, bg transparent, hover bg `#EDECEA`, icon `#9B9891`
  - Only shown when more than 1 URL row exists
- Gap between rows: `8px`
- "Add another video" button: Inter Medium 13px, `#2563EB`, leading `+` icon, hover underline + `+ icon rotates 90deg` (becomes ×-like indicator of "adding"), `margin-top: 8px`. `--transition-spring`.

#### Valid URL state (auto-transition — most important moment of the form)

When a valid YouTube URL is detected (`youtube.com/watch?v=` or `youtu.be/`), the row morphs in place:

```
┌─────────────────────────────────────────────────────────────┐ [×]
│  [thumb 64×36]  Mumbiker Nikhil's Jaipur Vlog              │
│                 12:34 · youtube.com/watch?v=...            │
└─────────────────────────────────────────────────────────────┘
```

- Height grows: `40px → 56px` over `--transition-spring-soft`
- Thumbnail fetched from `https://img.youtube.com/vi/{VIDEO_ID}/mqdefault.jpg` (no API key needed). 64×36, `border-radius: 4px`, `object-fit: cover`. Fades in with `opacity: 0 → 1, scale: 0.92 → 1` over 200ms `--ease-spring-soft`.
- Title row: Inter SemiBold 13px `#1A1917`, single-line truncated. **Fetched optionally via `oembed`** (`https://www.youtube.com/oembed?url={URL}&format=json`) — if unavailable, fall back to "_YouTube video_".
- Meta row: Inter Regular 11px `#9B9891`, "duration · short domain"
- Border-color shifts to `#16A34A` for 600ms then settles back to `#E4E2DC` — a tiny "got it" confirmation. Implement as a `valid-confirm` class that auto-removes after the animation.
- A small green ✓ check pops at the right edge: `scale: 0 → 1.15 → 1` over 320ms `--ease-spring`. Stays as long as the URL is valid.

#### Row enter / exit
- Enter animation per new row: `height: 0 → 40px, opacity: 0 → 1, translateX: -8px → 0`, 200ms `--ease-decelerate`
- Remove animation: `height: 40px → 0, opacity: 1 → 0, translateX: 0 → 12px`, 160ms `--ease-accelerate`
- New rows scroll into view smoothly if outside the visible card area

Use a standard `<input type="url">` styled with Tailwind utility classes per the input spec above. The thumbnail/title block is a sibling `<div>` rendered conditionally by JS; the input itself fades to `display: none` only after the preview has finished entering, so layout never jumps.

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

Custom Leaflet `DivIcon` rendered from an SVG string. Pins are the most-touched interactive element on the results page — every state matters.

#### Day Pin

Shape: teardrop (circle with downward point)
- Width: 28px, Height: 36px
- Fill: `var(--color-day-N)` for selected, `rgba(day-color, 0.6)` for unselected/dimmed
- Stroke: `#FFFFFF`, stroke-width: `2px`
- Shadow: `drop-shadow(0 2px 4px rgba(0,0,0,0.25))` (rest), `drop-shadow(0 4px 8px rgba(0,0,0,0.35))` (active/hover)
- Number inside circle: `N` (day number), white, Inter Bold 11px, centered

#### Pin states

| State | Visuals | Trigger |
|---|---|---|
| **Rest** | base color, scale 1, no ring | default |
| **Hover** | scale 1.12, shadow upgrade, `cursor: pointer` | mouse over pin OR mouse over its linked sidebar card |
| **Active (selected)** | scale 1.25, full day color (no opacity), shadow upgrade, a static 1.5px white ring sits 4px outside the pin | clicked, or its day is currently filtered |
| **Idle attention pulse** | a single `pulse-ring` ripple emits every 6s on the *first* pin of each day on page load (staggered between days) | passive idle, only when the page is at rest |
| **Dimmed** | scale 1, opacity 0.3, no shadow | a different day is filtered |

Transitions:
- `transform 200ms --ease-spring`
- `opacity 200ms ease-out`
- `filter` (drop-shadow) 200ms ease-out

#### Pin drop entrance (results page first load)
- All pins enter with the `pin-drop` keyframe (520ms `--ease-spring-bouncy`)
- Staggered by day group, then by order within day: `animation-delay: (dayIndex * 280ms) + (pinIndex * 60ms)`
- Cap total stagger at 1800ms — anything beyond that, snap in instantly
- Each pin emits one `pulse-ring` ripple as it lands (matches the day color at 50% opacity)

#### Hover-from-sidebar sync
When user hovers a `PlaceCard` in the sidebar:
- The matching map pin enters hover state (scale 1.12, ring)
- The map *gently* pans to keep that pin in view if it's near the edge (use `map.panTo({ animate: true, duration: 0.4 })`)
- *Reverse* sync: when user hovers a pin on the map, the matching sidebar card gets `--shadow-card-hover` and a faint `var(--color-day-N-subtle)` left-border (3px). Sidebar auto-scrolls to bring it into view if outside the viewport — smooth scroll, 320ms.

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

### 5.5.1 Day Route Line (new)

A dashed polyline connecting the pins of the *currently filtered day*, in their route-optimized order.

- Use Leaflet `L.polyline` with these options:
  - `color: var(--color-day-N)`
  - `weight: 2.5`
  - `opacity: 0.85`
  - `dashArray: '4 6'`
  - `lineCap: 'round'`
- Hidden by default (no day filtered). Shown when:
  - A `DaySectionHeader` is clicked (active state)
  - A pin is hovered for >400ms (preview of that day's route)
- Entrance: animate the dash via JS — set `lineDashOffset` from `200 → 0` over 1200ms (`route-draw` style). Leaflet doesn't animate this natively; use a `requestAnimationFrame` loop or fall back to fading the polyline in (`opacity 0 → 0.85`, 320ms).
- Exit: opacity 0.85 → 0 over 200ms, then `removeLayer`.

Order: use the order returned by the clustering step (already TSP-ish per the PRD's route optimization). If the API doesn't expose order, fall back to nearest-neighbor from the hotel pin or the cluster centroid.

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

- Padding: `12px 12px 8px`
- Border-radius: `8px` (so the active background shows nicely)
- Cursor: `pointer`
- Left accent: 3px × 16px vertical bar, color `var(--color-day-N)`, `border-radius: 9999px`, `margin-right: 10px`. On active, accent grows to `5px × 20px` with `--transition-spring`.
- Day label: Inter SemiBold 13px, `#1A1917`, uppercase, letter-spacing `0.08em`
- Cluster name: Inter Regular 13px, `#5C5A55`  — separated from day label by ` · `
- Place count: Inter Regular 12px, `#9B9891`, pushed right (`margin-left: auto`)
- Separator line below: `1px solid #EDECEA`

#### Interaction states

| State | Visuals | Trigger |
|---|---|---|
| Rest | as above | default |
| Hover | background `#EDECEA`, accent bar slightly taller (`16px → 18px`) | mouse over |
| Active (filtered) | background `var(--color-day-N-subtle)`, accent bar grown to `5px × 20px`, day label color shifts to `var(--color-day-N)` | clicked, toggles |
| Sibling-dimmed | opacity 0.55 | another day is currently active |

- Transition: `background 200ms ease-out`, `opacity 200ms ease-out`, accent bar `--transition-spring`
- **Click feedback**: a single ripple originates from click point in `var(--color-day-N-subtle)`, expands to 320px, fades out over `--transition-decelerate`. Same pattern as the Submit Button ripple.
- **Pinned-count badge**: when active, a tiny day-color filled pill ("5 stops") slides in from the right (`translateX: 8px → 0, opacity: 0 → 1`, 200ms `--ease-spring-soft`)
- **Entrance** (on results page first load): each `DaySectionHeader` enters with `slide-up-fade`, staggered 80ms after the preceding day group's last card has entered

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
- Border-left: `3px solid transparent` — becomes `var(--color-day-N)` on hover or when its pin is hovered (sync). 200ms ease-out.
- Border-radius: `10px`
- Padding: `12px 14px`
- Shadow: `shadow-sm`
- `margin-bottom: 8px`
- **Hover**: `shadow-card-hover`, border-color `#C7C5BE`, `transform: translateY(-2px)`, transition `200ms ease-out`. Also triggers map pin sync (see §5.5).
- **Pressed**: `transform: translateY(0) scale(0.99)`, 80ms ease-out (squash & stretch)
- Cursor: `pointer`
- **Entrance** (on results page load): `slide-up-fade`, staggered 40ms within a day group

Anatomy:
- **Row 1:** Place name (Inter SemiBold 14px, `#1A1917`) + Day badge right-aligned
- **Day badge:** `border-radius: 9999px`, `padding: 2px 8px`, background `var(--color-day-N-subtle)`, text Inter Medium 11px `var(--color-day-N)`, letter-spacing `0.04em`
  - On its parent card hover, badge briefly scales `1 → 1.08 → 1` over 320ms `--ease-spring` (secondary action — the badge "answers" the parent's hover)
- **Row 2:** Category (Inter Regular 12px, `#5C5A55`) · Rating (⭐ + number, same style)
  - ⭐ glyph gets a 1.5px text-shadow in `--color-sparkle` for a subtle warm glint
- **Row 3:** Source video — `📹` + video title (Inter Regular 12px, `#9B9891`, truncated with ellipsis, max-width fits card)
  - On card hover: video title color transitions to `#5C5A55` and `📹` gains a tiny 200ms wobble (`rotate: 0 → -8deg → 8deg → 0`) — playful but contained

"Unresolved" state: place name in `#9B9891`, italic. Row 2: "Location not found". No video row. Border `1px dashed #E4E2DC`. No hover lift (since there's no pin to sync with) — only a faint background change to `#FFFFFF → #FAF6EE`.

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
  - **Skeleton state** while loading: background `#EDECEA` with a `shimmer` overlay (1600ms loop). Photo fades in (`opacity: 0 → 1`, 320ms `--ease-decelerate`) when loaded.
  - On card hover (when expanded): photo subtly zooms (`scale: 1 → 1.03`, 400ms `--ease-decelerate`) within its overflow-hidden frame
- Description text: Inter Regular 13px, `#5C5A55`, line-height `1.5`, `margin-top: 8px`
- Hours: Inter Regular 12px, `#9B9891`, `margin-top: 4px`. Each weekday on its own line with a subtle `today` highlight (background `--color-day-1-subtle`, padding `2px 6px`, border-radius 4px) on the row matching the user's actual day.
- Source video links: each on its own line, Inter Regular 12px, `#2563EB`, hover underline + a tiny `↗` icon translates `+3px x, -3px y` on hover (200ms ease-out), opens YouTube in new tab
- Remove button: full-width, height 36px, border `1px solid #E4E2DC`, border-radius `8px`, text Inter Medium 13px `#DC2626`, hover bg `#FEF2F2`, `margin-top: 12px`
  - On click: card *collapses then drops away* — `transform: translateX(0) → translateX(20px) scale(0.96), opacity: 1 → 0` over 280ms `--ease-accelerate`, then DOM removed. Matching pin shrinks `scale: 1 → 0, opacity: 1 → 0` simultaneously.

#### Expand / collapse animation
- Expand: `max-height: 80px → 600px` (or measured natural height) over 320ms `--ease-decelerate`, `overflow: hidden`. Day badge stays anchored visually (use a flex layout that doesn't reflow).
- Collapse: `max-height: 600px → 80px` over 200ms `--ease-accelerate`.
- Caret indicator (16px chevron, `#9B9891`) at the top-right of the collapsed row rotates `0deg → 180deg` over `--transition-spring-soft` to match.
- Photo and inner content fade in 80ms *after* the expand starts (so the chrome moves first, then content) — a small staging principle

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
- **Hover**: background `#F8F7F4`, border-color `#C7C5BE`, icon `translateY(-1px)` (anticipation), 120ms ease-out
- **Press**: `scale: 0.97` 80ms ease-out
- **Copied state** (after click): background `#F0FDF4`, border-color `#16A34A`, text `#16A34A`, label swaps from "Share itinerary" to "Link copied!"
  - Icon morph: `Share2` cross-fades into a `Check` icon (both 14px), with the `Check` drawing in via `stroke-dashoffset: 24 → 0` (`check-draw` keyframe, 280ms ease-out)
  - **Sparkle burst**: 4 tiny SVG sparkles (`✦`, 8px) emit from the button center, traveling outward to ±18px with `sparkle` keyframe (800ms each, 40ms stagger). Color: `--color-sparkle`. They fade out and remove themselves on completion.
  - Subtle confetti is intentionally *not* used — too playful for this audience; sparkles communicate "success" without being childish.
  - Resets after 2000ms with a 200ms `--transition-fast` back to rest state

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

All animations use CSS transitions, CSS keyframes from §1.3, or vanilla JS for SVG-attribute animations (stroke-dashoffset, leaflet polylines). No external animation library required.

### 6.1 Master timing table

| Element | Property | From | To | Duration | Easing |
|---|---|---|---|---|---|
| **Page transitions** | | | | | |
| Page: form → loading | opacity | 1 | 0.6 | 160ms | accelerate |
| Page: loading → results | opacity | 0 | 1 | 480ms | decelerate |
| **Landing — ambient** | | | | | |
| Ambient mesh orb drift | translate | — | ±20px | 18s loop | ease-in-out |
| Hero word group stagger | translateY, opacity | 12px, 0 | 0, 1 | 320ms ea, 80ms stagger | decelerate |
| Hero "videos" underline | width | 0 | 100% | 480ms (delay 320ms) | decelerate |
| Form card entrance | translateY, opacity, scale | 12px, 0, 0.98 | 0, 1, 1 | 480ms (delay 200ms) | decelerate |
| Form card breathe (idle) | scale | 1 | 1.005 | 4s loop | ease-in-out |
| Topbar logo · dot pulse | opacity | 1 | 0.3 | 2400ms loop | ease-in-out |
| Topbar on-scroll | background, shadow | translucent, sm | white, md | 200ms | ease-out |
| **Form fields** | | | | | |
| Input focus glow | box-shadow | — | glow-accent | 120ms | ease-out |
| Input valid ✓ | translateX, opacity | 8px, 0 | 0, 1 | 200ms | spring-soft |
| Input invalid shake | translateX | 0 | ±3px | 200ms | ease-out |
| Invalid bg flash | background | white | error-subtle | 120ms | ease-out |
| Floating label | translate, font-size | 0, 14px | -22px, 11px | 180ms | spring-soft |
| URLInputRow add | height, opacity, translateX | 0, 0, -8px | 40px, 1, 0 | 200ms | decelerate |
| URLInputRow remove | height, opacity, translateX | 40px, 1, 0 | 0, 0, 12px | 160ms | accelerate |
| URL valid → preview swap | height | 40px | 56px | 320ms | spring-soft |
| Thumbnail fade-in | opacity, scale | 0, 0.92 | 1, 1 | 200ms | spring-soft |
| URL valid confirm-flash | border-color | E4E2DC | 16A34A → E4E2DC | 600ms | ease-out |
| URL valid ✓ pop | scale | 0 | 1.15 → 1 | 320ms | spring |
| Optional accordion expand | max-height, opacity | 0, 0 | 280px, 1 | 320ms | decelerate |
| Optional accordion collapse | max-height, opacity | 280px, 1 | 0, 0 | 200ms | accelerate |
| Chevron rotate | rotate | 0deg | 90deg | 320ms | spring-soft |
| Date arrow pulse on valid | scale | 1 | 1.2 → 1 | 320ms | spring |
| **Submit button** | | | | | |
| Hover lift | translateY, shadow | 0, sm | -1px, card-hover | 120ms | ease-out |
| Press squash | scaleY | 1 | 0.96 | 80ms | ease-out |
| Click ripple | radius, opacity | 0, 0.35 | 200px, 0 | 320ms | decelerate |
| Idle attention sparkle | scale, rotate, opacity | 0, 0deg, 0 | 1, 180deg, 1 | 800ms (every 8s) | sparkle keyframe |
| **Loading overlay** | | | | | |
| Backdrop fade-in | opacity | 0 | 1 | 200ms | decelerate |
| Backdrop blur-in | backdrop-filter | blur(0) | blur(8px) | 200ms | decelerate |
| Card enter | translateY, scale, opacity | 12px, 0.96, 0 | 0, 1, 1 | 400ms (delay 80ms) | spring-soft |
| Mini-map pin drop | translateY, scale, opacity | -40px, 0.6, 0 | 0, 1, 1 | 520ms, 200ms stagger | spring-bouncy |
| Mini-map route draw | stroke-dashoffset | 1000 | 0 | 1200ms | ease-out |
| Step label swap (out) | translateY, opacity | 0, 1 | -8px, 0 | 160ms | accelerate |
| Step label swap (in) | translateY, opacity | 8px, 0 | 0, 1 | 200ms | decelerate |
| Progress fill width | width | prev% | next% | 600ms | decelerate |
| Progress fill brighten tick | filter brightness | 1 | 1.15 → 1 | 200ms | ease-out |
| Progress shimmer | background-position | -200% | 200% | 1600ms loop | linear |
| Card exit (success) | scale, opacity | 1 | 0.92, 0 | 400ms | accelerate |
| **Results — entrance** | | | | | |
| Map pin drop | translateY, scale, opacity | -40px, 0.6, 0 | 0, 1, 1 | 520ms, 60ms stagger | spring-bouncy |
| Pin landing ripple | scale, opacity | 0.8, 0.6 | 2.2, 0 | 1800ms once | ease-out |
| Sidebar card slide-in | translateY, opacity | 12px, 0 | 0, 1 | 320ms, 40ms stagger | decelerate |
| Day section header enter | translateY, opacity | 12px, 0 | 0, 1 | 320ms | decelerate |
| **Results — interaction** | | | | | |
| PlaceCard hover lift | translateY, shadow | 0, sm | -2px, card-hover | 200ms | ease-out |
| PlaceCard press squash | scale, translateY | 1, -2px | 0.99, 0 | 80ms | ease-out |
| PlaceCard expand | max-height | 80px | 600px | 320ms | decelerate |
| PlaceCard collapse | max-height | 600px | 80px | 200ms | accelerate |
| PlaceCard photo zoom | scale | 1 | 1.03 | 400ms | decelerate |
| PlaceCard photo shimmer | bg-position | -200% | 200% | 1600ms loop | linear |
| Day badge bounce (parent hover) | scale | 1 | 1.08 → 1 | 320ms | spring |
| 📹 wobble (parent hover) | rotate | 0 | -8° → 8° → 0 | 200ms | ease-out |
| Place removed exit | translateX, scale, opacity | 0, 1, 1 | 20px, 0.96, 0 | 280ms | accelerate |
| Pin hover scale | scale | 1 | 1.12 | 200ms | spring |
| Pin selected scale | scale | 1 | 1.25 | 200ms | spring |
| Pin idle pulse-ring (first of each day) | scale, opacity | 0.8, 0.6 | 2.2, 0 | 1800ms (every 6s) | ease-out |
| Pin dim (non-selected day) | opacity | 1 | 0.3 | 200ms | ease-out |
| Day route polyline draw | line-dash-offset | 200 | 0 | 1200ms | ease-out |
| Day route fade-in fallback | opacity | 0 | 0.85 | 320ms | ease-out |
| Day route exit | opacity | 0.85 | 0 | 200ms | ease-out |
| DaySectionHeader active | background, accent | transparent, 3×16 | day-subtle, 5×20 | 200ms / spring | varies |
| DaySectionHeader click ripple | radius, opacity | 0 | 320px, 0 | 320ms | decelerate |
| Pinned-count pill slide | translateX, opacity | 8px, 0 | 0, 1 | 200ms | spring-soft |
| Sidebar collapse | width | 400px | 0 | 320ms | spring-soft |
| Sidebar expand | width | 0 | 400px | 320ms | spring-soft (overshoots) |
| Sidebar toggle hover | scale, shadow | 1, sm | 1.08, md | 120ms | ease-out |
| Sidebar toggle ripple | scale, opacity | 0.8, 0.6 | 2.2, 0 | 1800ms once | ease-out |
| Map panel flex | flex-grow | — | — | 320ms | spring-soft |
| Auto-scroll to card | scroll-top | current | target | 320ms | ease-out |
| Map gentle pan to pin | latlng | current | target | 400ms | leaflet default |
| **Misc** | | | | | |
| ShareButton copied confirm | bg, border, color | default | success tints | 120ms | ease-out |
| ShareButton ✓ draw | stroke-dashoffset | 24 | 0 | 280ms (delay 80ms) | ease-out |
| ShareButton sparkles | scale, opacity | 0, 0 | 1, 1 → 0 | 800ms, 40ms stagger | sparkle keyframe |
| ShareButton reset | bg, border, color | success | default | 200ms (after 2000ms hold) | ease-out |
| ErrorBanner entrance | translateY, opacity | -8px, 0 | 0, 1 | 200ms | decelerate |
| Generic skeleton shimmer | bg-position | -200% | 200% | 1600ms loop | linear |
| Tooltip show | opacity, translateY | 0, 4px | 1, 0 | 150ms | ease-out |
| Tooltip hide | opacity | 1 | 0 | 100ms | ease-in |

---

## 7. Typography Hierarchy Summary

Font family: `'Uber Move', 'Manrope', -apple-system, system-ui, sans-serif`
Load via Google Fonts: `Manrope` weights 400, 500, 600, 700

| Role | Size | Weight | Letter-spacing | Color |
|---|---|---|---|---|
| Hero heading | 56px | 700 | -0.04em | `#000000` |
| Display heading | 40px | 700 | -0.03em | `#000000` |
| Section heading | 24px | 600 | -0.02em | `#000000` |
| Card section title | 20px | 600 | -0.01em | `#000000` |
| Card title | 14px | 600 | 0 | `#000000` |
| Day section label | 13px | 600 | +0.06em | `#000000` |
| Body text | 16px | 400 | 0 | `#000000` |
| Secondary text | 14px | 400 | 0 | `#545454` |
| Meta / label | 13px | 400 | 0 | `#8A8A8A` |
| Badge | 11px | 500 | +0.04em | day color |
| Button (primary) | 16px | 700 | 0 | `#FFFFFF` |
| Button (secondary) | 14px | 500 | 0 | `#000000` |
| Link | 14px | 400 | 0 | `#000000` (underline) |
| Error | 13px | 400 | 0 | `#C7282D` |

---

## 8. Accessibility

- All interactive elements have `focus-visible` ring: `0 0 0 3px rgba(0,0,0,0.12)` (black-based, WCAG 3:1 contrast)
- Day-1 (#276EF1), Day-4 (#7356BF): pass AA. Day-2 (#06C167), Day-3 (#FF974A), Day-5 (#E85D99): use large/bold text only on white; always use on subtle backgrounds for small text.
- Map pins use both color AND number label — never color-only
- All icon-only buttons have `aria-label`
- Loading overlay has `role="status"` and `aria-live="polite"` for screen readers
- Minimum touch / click target: 28px × 28px
- Primary button (#000000): 21:1 contrast on white — AAA

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
| Ambient mesh background | `<div class="ambient-bg">` with 3 absolutely-positioned `<div class="orb">` children, animated via the `ambient-drift` keyframe |
| URL → video preview transform | JS-driven: `input` event listener regex-matches valid YouTube URLs, swaps the row's children to a `<div class="video-preview">` containing `<img>` + title meta. Original input kept `display: none` until preview animation completes. |
| Map pin idle pulse rings | `<div class="pin-pulse">` injected as a Leaflet `DivIcon` sibling, CSS-animated with `pulse-ring`, removed after one loop |
| Day route polyline | Leaflet `L.polyline` with `dashArray`; JS manipulates `_path.strokeDashoffset` per frame |
| Submit ripple / DaySection ripple | JS `mousedown` handler injects a `<span class="ripple">` at click coords; auto-removes on `animationend` |
| Share copied sparkles | 4 pre-pooled `<span class="sparkle">` elements absolute-positioned over the button, re-triggered with class toggle on copy |
| Skeleton loaders | `<div class="skeleton skeleton--card">` blocks rendered while SSE pipeline is in flight |

---

---

## 10. Micro-Interactions Playbook (Disney's 12 Principles, Applied)

This is the heart of "alive but quiet." Every interactive element on Ytinerary must reach at least 3 of the 12 principles. Buttons, pins, and the loading overlay should reach all 12 between them.

### 10.1 Principle-by-principle application

| # | Principle | Where it lives in Ytinerary |
|---|---|---|
| 1 | **Squash & Stretch** | Submit button `scaleY: 0.96` on press. PlaceCard `scale: 0.99` on press. Toggle thumbs squash subtly when reaching bound. |
| 2 | **Anticipation** | Submit button `translateY(-1px)` on hover *before* the click. The arrow inside the button slides `+4px` on hover, hinting at forward motion. Sidebar toggle scales 1.08 on hover. URL preview thumbnail scales `0.92 → 1` so it "arrives". |
| 3 | **Staging** | The Loading Overlay dims everything else with `backdrop-filter: blur(8px)`. The active DaySectionHeader filters all other days down to opacity 0.55. Focused inputs get the only glow on the page. *One spotlight at a time.* |
| 4 | **Straight Ahead vs Pose to Pose** | Progress shimmer (straight ahead) layered with stepped progress fills (pose to pose). Idle pin pulse rings (straight ahead) with discrete selected-state snaps (pose to pose). |
| 5 | **Follow Through & Overlapping** | Submit ripple expands *past* the click point. Toggle/sidebar expansion uses `spring-soft` so the panel overshoots by ~2% then settles. The map pin lands then emits one ripple after settling. Successive pins drop in stagger. |
| 6 | **Slow In / Slow Out** | Default easing is `--ease-decelerate` for entrances, `--ease-accelerate` for exits. Linear is banned outside ambient shimmers. |
| 7 | **Arc** | The chevron icons rotate through a 90°/180° arc, not just snap. The "+ Add another video" `+` rotates 45° on hover. The sparkle burst from ShareButton travels in slight outward arcs (varied x/y end-points, not pure radial). |
| 8 | **Secondary Action** | When PlaceCard hovers, the day badge inside it bounces. When the parent's pin is hovered, the sidebar card's left-border lights up. The 📹 icon wobbles. *Children answer their parent's state.* |
| 9 | **Timing** | Strict scale: 80ms (press) → 120ms (hover) → 200ms (state) → 320ms (transition) → 480ms (entrance) → 1800ms+ (idle loop). Document every deviation. |
| 10 | **Exaggeration** | Pin selected scales `1.25` (noticeable, not silly). Spring overshoots are subtle: <1.1× for most, never over `1.25×`. Error shake is 3px not 15px. Sparkles are 8px, not 20px. |
| 11 | **Solid Drawing** | Transform-origin discipline: pins scale from their *anchor point* (bottom tip of teardrop = `transform-origin: 50% 100%`). Cards scale from center. Tooltips scale from their pin's anchor. Day badge scales from its baseline center. |
| 12 | **Appeal** | The cumulative effect: orbs drift behind the form, the logo dot breathes, the Submit button periodically sparkles, the form card breathes, URL pastes get a green confirm flash. None individually loud — together, *alive*. |

### 10.2 Component checklist — interaction states

Every interactive element MUST define these 5 states. If a state is absent, the element is incomplete.

```
┌─────────────┬───────────────────────────────────────────────────┐
│ State       │ Required behavior                                 │
├─────────────┼───────────────────────────────────────────────────┤
│ rest        │ idle visual; may include ambient pulse / breathe  │
│ hover       │ anticipation cue (lift, glow, scale 1.02–1.12)    │
│ focus       │ visible ring `--shadow-glow-accent`               │
│ active      │ squash on press (scale 0.95–0.99) or state-toggle │
│ disabled    │ opacity 0.5, cursor not-allowed, NO transitions   │
└─────────────┴───────────────────────────────────────────────────┘
```

Plus where applicable:
- **loading** (skeleton shimmer or inline spinner)
- **success** (one-shot scale-up + color shift + optional sparkle)
- **error** (3px shake + error-tint background)
- **empty** (illustrative SVG + subtle one-line copy)

### 10.3 Code recipes (drop-in CSS)

```css
/* Ripple — append to any button via JS on mousedown */
.ripple {
  position: absolute;
  border-radius: 9999px;
  background: rgba(255, 255, 255, 0.35);
  pointer-events: none;
  animation: ripple-expand 320ms var(--ease-decelerate) forwards;
}
@keyframes ripple-expand {
  0%   { transform: scale(0); opacity: 0.35; }
  100% { transform: scale(20); opacity: 0; }
}

/* Skeleton shimmer — apply to any block awaiting content */
.skeleton {
  background:
    linear-gradient(90deg, transparent, rgba(255,255,255,0.65), transparent) 0 0 / 200% 100%,
    #EDECEA;
  animation: shimmer 1600ms linear infinite;
  border-radius: 8px;
}

/* Idle attention sparkle — applies once every 8s on `data-idle="true"` */
@keyframes sparkle-flash {
  0%, 90%, 100% { opacity: 0; transform: scale(0) rotate(0deg); }
  92%, 96%      { opacity: 1; transform: scale(1) rotate(180deg); }
}
[data-idle="true"]::after {
  content: '✦';
  position: absolute;
  top: -4px; right: -4px;
  color: var(--color-sparkle);
  font-size: 10px;
  animation: sparkle-flash 8s infinite;
  pointer-events: none;
}

/* Universal focus ring */
:focus-visible {
  outline: none;
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.25);
  border-radius: inherit;
}

/* Press squash — apply via Tailwind active: variant */
.press-squash:active { transform: scale(0.98); }
.press-squash-y:active { transform: scaleY(0.96); }

/* Hover lift */
.hover-lift {
  transition: transform 120ms ease-out, box-shadow 120ms ease-out;
}
.hover-lift:hover { transform: translateY(-1px); box-shadow: var(--shadow-card-hover); }
```

---

## 11. Visual Richness Layer

A taxonomy of "extra" visual elements that make pages feel composed rather than generic. Apply sparingly — each is opt-in per page.

### 11.1 Surfaces & Backgrounds

| Layer | Use on | Spec |
|---|---|---|
| **Pure white** | All pages | `#FFFFFF` on `<body>` — primary surface |
| **Light gray** | Sidebar, section stripes | `#F6F6F6` |
| **Subtle grid texture** | Hero section (optional) | `repeating-linear-gradient` at 3% opacity `rgba(0,0,0,0.03)` — structured, not decorative |
| **Mesh dot grid** | Loading overlay mini-map | 10×10 grid of 2px `#E2E2E2` circles, 8px spacing |
| **Day-tinted halo** | Around active map pins only | `--gradient-day-glow-N`, 80×80, behind pin, opacity 0.5 |

> No mesh gradients, warm orbs, or blurred circles on any page surface.

### 11.2 Decorative SVG elements

- **Route doodle** — hand-drawn-looking dashed line, used as ambient decoration. Stored as inline SVG with `stroke-dasharray: 4 6` and `stroke-linecap: round`.
- **Pin cluster motif** — 3 small overlapping teardrops in the Topbar logo's `·` separator (replaces the dot on hover). 80ms staggered fade.
- **Compass rose** — tiny 12px compass at the bottom of the loading overlay card, rotating slowly (`animation: spin 12s linear infinite`). Only visible when the network is slow.
- **Skeleton shapes** — generic placeholder rectangles for PlaceCard while photo loads.

### 11.3 Sparkle / confetti governance

Sparkles communicate success quietly. **Rules:**

1. Max 4 sparkles per burst, max one burst per user action.
2. Color: always `--color-sparkle` (`#FCD34D`). Never the accent blue (would compete with day-1).
3. Allowed contexts: **only** ShareButton "Link copied", Submit button "idle attention", and the loading overlay "complete" gesture.
4. Never on hover or input focus — sparkles must mark a *completed transaction*, not a passive state.
5. Each sparkle's `transform-origin` is its own center, so it scales cleanly without clipping.

### 11.4 Skeleton & loading shapes

- All async-loaded content uses `.skeleton` blocks (see §10.3) — never blank white space.
- Sidebar cards: 4 skeleton cards visible during the SSE pipeline before first real result. Each skeleton: 56px tall, full width, `margin-bottom: 8px`.
- Map: a faint `--color-border-subtle` cross-hatch SVG (10% opacity) shows behind tiles while they load.

### 11.5 Idle attention budget

The interface is static when not in use. Allowed idle motions, strictly limited:

1. **Submit button arrow nudge** — landing only, only when form is complete and no interaction for 4s+. Repeats every 6s. Stops on hover.
2. **First pin of each day pulse-ring** — results page only, when no day is filtered.

Max **1** simultaneous idle motion per screen. Uber interfaces are still at rest.

---

## 12. Reduced Motion + Performance

### 12.1 `prefers-reduced-motion` strategy

The CSS in §1.3 strips all durations and animations to ~0 globally. But that flat-killing fallback is brutal — we want a *graceful* reduced mode, not a no-mode.

**Layered approach:**

```css
@media (prefers-reduced-motion: reduce) {
  /* 1) Kill ambient loops (drift, breathe, shimmer, idle pulse) */
  .ambient-orb,
  .form-card,
  .logo-dot,
  .progress-shimmer,
  .pin-idle-pulse,
  .skeleton {
    animation: none !important;
  }

  /* 2) Allow opacity transitions to remain (they don't trigger vestibular issues) */
  *, *::before, *::after {
    transition-duration: 0.01ms !important;
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
  }

  /* 3) Re-enable specific opacity-only fades that aid comprehension */
  .step-label,
  .toast,
  .place-card-photo {
    transition-duration: 200ms !important;
    transition-property: opacity !important;
  }

  /* 4) Pin drops become instant — but pins still appear in stagger via JS-controlled opacity */
}
```

### 12.2 Performance budget

- Target **60fps** for all hover, scroll, and click interactions on a 5-year-old laptop.
- All transforms must run on the compositor: only `transform` and `opacity` (and `filter` sparingly).
- **Never animate**: `width` on map pins (use `transform: scale` and adjust the wrapper), `height` on cards larger than 200px (use `max-height` with a known cap), `top/left` on absolute elements (use `transform: translate`).
- Use `will-change: transform` only on elements about to animate (e.g. `.place-card:hover { will-change: transform; }`), and remove it after.
- Map pin count: pins beyond 30 should *not* receive ripple/pulse ambient animations — only the visible-in-viewport ones (use Leaflet's `bounds` + an IntersectionObserver on the icon DOM).
- Loading overlay's mini-map SVG runs on the main thread but is fewer than 10 nodes — safe.

### 12.3 Accessibility cross-checks

- Every animation that conveys state must have a non-animated equivalent (e.g. selected pin uses both scale *and* color saturation; valid input uses both ✓ icon *and* border color).
- `aria-live="polite"` on the Loading overlay's step label so screen readers announce each step transition.
- Focus rings (`--shadow-glow-accent`) must never be removed in any state.
- All idle-attention animations must be suppressible via reduced-motion (see §12.1).

### 12.4 Implementation hints

- For JS-driven stagger (pin drops, sidebar cards), use `Element.animate()` API with `delay: index * stagger` rather than `setTimeout` — keeps the timing on the compositor.
- For the route polyline draw, manipulate the Leaflet layer's `_path.style.strokeDashoffset` directly in a `requestAnimationFrame` loop. Roughly 20 lines of JS.
- For thumbnail fetch on URL paste, debounce input by 200ms before firing the fetch.
- For sparkle bursts, generate `<span>` elements once at page-load (pooled), absolute-positioned, and just replay the keyframe — avoids GC churn.

---

*End of Ytinerary Website Design Specification v1.1*
*Visually rich. Always responding. Never loud.*
