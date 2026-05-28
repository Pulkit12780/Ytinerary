Techniques Reference
Full implementation patterns for the design-upgrade skill.

Typography upgrades
Variable font weight animation on scroll
css:root { --font-weight: 300; }

h1 {
  font-family: 'Fraunces', serif;
  font-variation-settings: 'wght' var(--font-weight);
  transition: font-variation-settings 0.3s;
  font-size: clamp(3.5rem, 12vw, 10rem);
  line-height: 0.9;
  letter-spacing: -0.04em;
}
Text split reveal (CSS only, no library)
html<h1 class="reveal-text">Hello World</h1>
css.reveal-text {
  overflow: hidden;
}
.reveal-text span {
  display: inline-block;
  transform: translateY(100%);
  animation: reveal 0.8s cubic-bezier(0.22, 1, 0.36, 1) forwards;
  animation-delay: calc(var(--i) * 0.08s);
}
@keyframes reveal {
  to { transform: translateY(0); }
}
js// Wrap each word in a span with --i custom property
document.querySelectorAll('.reveal-text').forEach(el => {
  el.innerHTML = el.textContent.split(' ').map((word, i) =>
    `<span style="--i:${i}">${word}&nbsp;</span>`
  ).join('');
});
Fluid type scale
css/* Never fixed px for display type */
.hero-title   { font-size: clamp(3rem,   10vw, 9rem);  }
.section-title { font-size: clamp(2rem,   5vw,  4rem);  }
.lead          { font-size: clamp(1.1rem, 2vw,  1.5rem); }
body           { font-size: clamp(1rem,   1.2vw, 1.125rem); }

Colour & atmosphere
Noise texture overlay (adds grain depth)
html<!-- Inline SVG noise — no external file needed -->
<style>
body::before {
  content: '';
  position: fixed;
  inset: 0;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
  opacity: 0.035;
  pointer-events: none;
  z-index: 9999;
}
</style>
Gradient mesh background
css.hero {
  background:
    radial-gradient(ellipse at 20% 50%, hsla(240, 80%, 60%, 0.15) 0%, transparent 60%),
    radial-gradient(ellipse at 80% 20%, hsla(320, 70%, 60%, 0.1) 0%, transparent 50%),
    #0a0a0f;
}
Colour palettes by direction
Editorial Luxury
css--bg:      #F7F3EC;
--text:    #1A1814;
--accent:  #C4A882;
--muted:   #8C8880;
Dark Cinematic
css--bg:      #080B0F;
--text:    #E8EDF2;
--accent:  #3B82F6;
--muted:   #4A5568;
Soft Organic
css--bg:      #FAF7F2;
--text:    #2D2926;
--accent:  #7C9A6E;
--muted:   #9B9289;
Brutalist Raw
css--bg:      #F0EDE8;
--text:    #000000;
--accent:  #FF3300;
--muted:   #666666;

Scroll animations
IntersectionObserver (no library — works everywhere)
css.fade-up {
  opacity: 0;
  transform: translateY(40px);
  transition: opacity 0.7s cubic-bezier(0.22, 1, 0.36, 1),
              transform 0.7s cubic-bezier(0.22, 1, 0.36, 1);
}
.fade-up.visible {
  opacity: 1;
  transform: translateY(0);
}
jsconst observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
      observer.unobserve(entry.target); // animate once
    }
  });
}, { threshold: 0.15 });

document.querySelectorAll('.fade-up').forEach(el => observer.observe(el));
Staggered children reveal
css.stagger-children > * {
  opacity: 0;
  transform: translateY(30px);
  transition: opacity 0.6s ease, transform 0.6s ease;
  transition-delay: calc(var(--i) * 0.1s);
}
.stagger-children.visible > * {
  opacity: 1;
  transform: none;
}
js// Assign --i to each child for stagger timing
document.querySelectorAll('.stagger-children').forEach(el => {
  [...el.children].forEach((child, i) => child.style.setProperty('--i', i));
});
GSAP ScrollTrigger (advanced — include GSAP CDN)
jsgsap.registerPlugin(ScrollTrigger);

// Pinned horizontal scroll section
gsap.to(".scroll-track", {
  x: () => -(document.querySelector(".scroll-track").scrollWidth - window.innerWidth),
  ease: "none",
  scrollTrigger: {
    trigger: ".horizontal-section",
    pin: true,
    scrub: 1,
    end: () => "+=" + document.querySelector(".scroll-track").scrollWidth,
  }
});

// Text line reveal on scroll
gsap.utils.toArray(".reveal-line").forEach(line => {
  gsap.from(line, {
    y: "100%",
    opacity: 0,
    duration: 1,
    ease: "power4.out",
    scrollTrigger: { trigger: line, start: "top 85%" }
  });
});
Parallax images
jsdocument.querySelectorAll('.parallax').forEach(el => {
  window.addEventListener('scroll', () => {
    const speed = el.dataset.speed || 0.3;
    const rect  = el.getBoundingClientRect();
    const offset = (window.innerHeight / 2 - rect.top - rect.height / 2) * speed;
    el.style.transform = `translateY(${offset}px)`;
  });
});

Load sequence (hero entrance)
css/* Elements start invisible */
.hero-eyebrow, .hero-title, .hero-subtitle, .hero-cta {
  opacity: 0;
  transform: translateY(24px);
  animation: enter 0.9s cubic-bezier(0.22, 1, 0.36, 1) forwards;
}
.hero-eyebrow  { animation-delay: 0.1s; }
.hero-title    { animation-delay: 0.25s; }
.hero-subtitle { animation-delay: 0.4s; }
.hero-cta      { animation-delay: 0.55s; }

@keyframes enter {
  to { opacity: 1; transform: translateY(0); }
}

Hover interactions
Magnetic button effect
jsdocument.querySelectorAll('.magnetic').forEach(btn => {
  btn.addEventListener('mousemove', e => {
    const rect = btn.getBoundingClientRect();
    const x = e.clientX - rect.left - rect.width / 2;
    const y = e.clientY - rect.top  - rect.height / 2;
    btn.style.transform = `translate(${x * 0.3}px, ${y * 0.3}px)`;
  });
  btn.addEventListener('mouseleave', () => {
    btn.style.transform = '';
    btn.style.transition = 'transform 0.5s cubic-bezier(0.22, 1, 0.36, 1)';
  });
});
Text fill on hover (underline grows)
css.hover-link {
  position: relative;
  text-decoration: none;
}
.hover-link::after {
  content: '';
  position: absolute;
  bottom: -2px;
  left: 0;
  width: 0;
  height: 1px;
  background: currentColor;
  transition: width 0.4s cubic-bezier(0.22, 1, 0.36, 1);
}
.hover-link:hover::after { width: 100%; }
Image reveal on hover (clip-path)
css.image-reveal {
  overflow: hidden;
}
.image-reveal img {
  transform: scale(1.08);
  filter: grayscale(30%);
  transition: transform 0.6s cubic-bezier(0.22, 1, 0.36, 1),
              filter 0.6s ease;
}
.image-reveal:hover img {
  transform: scale(1);
  filter: grayscale(0%);
}

Custom cursor
css*, *::before, *::after { cursor: none; }

.cursor {
  position: fixed;
  top: 0; left: 0;
  width: 10px; height: 10px;
  background: var(--accent);
  border-radius: 50%;
  pointer-events: none;
  z-index: 99999;
  transition: transform 0.1s ease;
}
.cursor-follower {
  position: fixed;
  top: 0; left: 0;
  width: 36px; height: 36px;
  border: 1px solid var(--accent);
  border-radius: 50%;
  pointer-events: none;
  z-index: 99998;
  transition: transform 0.25s ease, width 0.3s, height 0.3s, opacity 0.3s;
}
/* Expand follower on hover over links */
a:hover ~ .cursor-follower,
button:hover ~ .cursor-follower {
  width: 60px; height: 60px;
  opacity: 0.5;
}
jsconst cursor = document.querySelector('.cursor');
const follower = document.querySelector('.cursor-follower');
let mouseX = 0, mouseY = 0;
let followerX = 0, followerY = 0;

document.addEventListener('mousemove', e => {
  mouseX = e.clientX; mouseY = e.clientY;
  cursor.style.transform = `translate(${mouseX - 5}px, ${mouseY - 5}px)`;
});

function animateFollower() {
  followerX += (mouseX - followerX - 18) * 0.12;
  followerY += (mouseY - followerY - 18) * 0.12;
  follower.style.transform = `translate(${followerX}px, ${followerY}px)`;
  requestAnimationFrame(animateFollower);
}
animateFollower();

Smooth scroll (Lenis)
html<script src="https://cdn.jsdelivr.net/npm/@studio-freight/lenis@1.0.42/dist/lenis.min.js"></script>
<script>
const lenis = new Lenis({
  duration: 1.2,
  easing: t => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
  smooth: true,
});

function raf(time) {
  lenis.raf(time);
  requestAnimationFrame(raf);
}
requestAnimationFrame(raf);
</script>

Layout patterns
Asymmetric hero grid
css.hero-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  grid-template-rows: auto auto;
  gap: 0;
  min-height: 100vh;
  align-items: end;
  padding: 120px 60px 80px;
}
.hero-title  { grid-column: 1 / 3; } /* bleeds full width */
.hero-body   { grid-column: 2 / 3; margin-top: 40px; max-width: 420px; justify-self: end; }
.hero-scroll { grid-column: 1 / 2; align-self: end; }
Full-bleed section with inset content
css.full-bleed {
  width: 100vw;
  margin-left: calc(50% - 50vw);
  padding: 120px calc(50vw - 600px);
}
Overlapping image + text
css.overlap-block {
  position: relative;
  display: grid;
  grid-template-columns: 1fr 1fr;
}
.overlap-block .image { grid-column: 1 / 3; grid-row: 1; }
.overlap-block .text  { grid-column: 2 / 3; grid-row: 1; align-self: end; z-index: 1;
                         background: var(--bg); padding: 48px; margin-top: 160px; }

Page transitions (Barba.js pattern)
html<script src="https://unpkg.com/@barba/core"></script>
js// Curtain reveal transition
barba.init({
  transitions: [{
    name: 'curtain',
    leave(data) {
      return gsap.to(data.current.container, { opacity: 0, y: -20, duration: 0.4 });
    },
    enter(data) {
      return gsap.from(data.next.container, { opacity: 0, y: 20, duration: 0.5, delay: 0.1 });
    }
  }]
});

Complete minimal template (starting point)
html<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Site</title>
  <link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,300;9..144,700&family=Outfit:wght@300;400;500&display=swap" rel="stylesheet">
  <style>
    *, *::before, *::after { margin: 0; padding: 0; box-sizing: border-box; }

    :root {
      --bg:     #F7F3EC;
      --text:   #1A1814;
      --accent: #C4A882;
      --muted:  #8C8880;
      --display: 'Fraunces', serif;
      --body:   'Outfit', sans-serif;
    }

    html { scroll-behavior: smooth; }
    body {
      background: var(--bg);
      color: var(--text);
      font-family: var(--body);
      font-size: clamp(1rem, 1.2vw, 1.125rem);
      line-height: 1.7;
      overflow-x: hidden;
    }

    /* Noise overlay */
    body::before {
      content: '';
      position: fixed; inset: 0;
      background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
      opacity: 0.035;
      pointer-events: none;
      z-index: 9999;
    }

    /* Hero */
    .hero {
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      justify-content: flex-end;
      padding: 120px 60px 80px;
    }

    .hero h1 {
      font-family: var(--display);
      font-size: clamp(4rem, 12vw, 10rem);
      font-weight: 700;
      line-height: 0.92;
      letter-spacing: -0.04em;
      opacity: 0;
      transform: translateY(40px);
      animation: enter 1s cubic-bezier(0.22, 1, 0.36, 1) 0.2s forwards;
    }

    .hero p {
      max-width: 480px;
      color: var(--muted);
      margin-top: 32px;
      opacity: 0;
      animation: enter 0.9s cubic-bezier(0.22, 1, 0.36, 1) 0.45s forwards;
    }

    @keyframes enter {
      to { opacity: 1; transform: translateY(0); }
    }

    /* Sections */
    section {
      padding: 120px 60px;
    }

    /* Fade-up on scroll */
    .fade-up {
      opacity: 0;
      transform: translateY(40px);
      transition: opacity 0.8s cubic-bezier(0.22, 1, 0.36, 1),
                  transform 0.8s cubic-bezier(0.22, 1, 0.36, 1);
    }
    .fade-up.visible { opacity: 1; transform: none; }
  </style>
</head>
<body>

  <main>
    <section class="hero">
      <h1>Your headline<br>goes here</h1>
      <p>A concise description of what you do, who you do it for, and why it matters.</p>
    </section>

    <section>
      <h2 class="fade-up" style="font-family: var(--display); font-size: clamp(2rem, 5vw, 4rem); letter-spacing: -0.03em;">Section title</h2>
      <p class="fade-up" style="max-width: 600px; color: var(--muted); margin-top: 24px;">Content here.</p>
    </section>
  </main>

  <script>
    // Scroll reveal
    const observer = new IntersectionObserver(entries => {
      entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('visible'); observer.unobserve(e.target); } });
    }, { threshold: 0.15 });
    document.querySelectorAll('.fade-up').forEach(el => observer.observe(el));
  </script>
</body>
</html>