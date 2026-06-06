# Responsive Design

**Purpose:** Canonical reference for Pixel's `responsive` recipe. Covers (a) mobile-first conversion patterns when reproducing a desktop mockup as multi-breakpoint HTML/CSS, and (b) derivation methodology when the mockup shows only a single viewport.
**Read when:** You need to convert a static mockup into responsive HTML/CSS, or derive breakpoint behavior from a single-viewport mockup.

> Derivation is inference, not extraction. Every breakpoint, fluid value, and reflow rule produced from a single mockup must be marked `/* LOW: derived from <source>, verify */` (or MEDIUM if conventional).

## Contents
- Breakpoint System (resolved canonical set)
- Mobile-First Philosophy
- Breakpoint Estimation from Content
- Fluid Typography (clamp)
- Derivation Methodology (mockup → breakpoint rules)
- Section Reflow Patterns (Hero / Nav / Grid / Footer / Card)
- Container Queries vs Media Queries
- Aspect Ratio & Image Handling
- Modern CSS for Faithful Reproduction (2025–2026)
- Common Pitfalls / Anti-patterns
- Decision Walkthrough Template

---

## Breakpoint System

> **Conflict resolution note (2026-05):** This file previously existed as two references with conflicting breakpoint sets — the older `responsive-derivation.md` used a 5-point set (0 / 768 / 1024 / 1440 / 1920), and the newer `responsive-strategies.md` (refreshed 2026-05) used a Tailwind-aligned 4-point set (0 / 640 / 1024 / 1280). The merged canonical set below adopts the Tailwind-default breakpoints (640 / 768 / 1024 / 1280 / 1536) because: (1) it matches the most widely used utility framework, (2) it appeared in the more recently refreshed source, and (3) it aligns with what most production designs ship today. The legacy 1440 / 1920 endpoints are retained only as optional verification widths, not as media-query targets.

### Canonical breakpoints

| Name | Min width | Tailwind | CSS (`em` / `rem`) | Typical device | Confidence |
|------|-----------|----------|--------------------|----------------|------------|
| Mobile (base) | 0 | (default) | Default styles | Phones | HIGH (convention) |
| Small | 640px | `sm:` | `@media (min-width: 40rem)` | Large phones / small tablets portrait | MEDIUM |
| Medium | 768px | `md:` | `@media (min-width: 48rem)` | Tablets | MEDIUM |
| Large | 1024px | `lg:` | `@media (min-width: 64rem)` | Laptops, small desktops | MEDIUM |
| XL | 1280px | `xl:` | `@media (min-width: 80rem)` | Standard desktops | HIGH (if mockup ~1280–1440px) |
| 2XL | 1536px | `2xl:` | `@media (min-width: 96rem)` | Wide monitors | LOW |

### Container max-widths (suggested)

| Breakpoint | Container max | Rationale |
|------------|---------------|-----------|
| Mobile | `100% - 32px` | Edge padding |
| 640 | 600px | Read-line ~65ch |
| 768 | 720px | 2-col grid comfortable |
| 1024 | 960px | 3-col grid |
| 1280 | 1200px | 4-col / standard hero |
| 1536 | 1440px | Wide hero / dashboard |

Use these unless the mockup explicitly demands custom breakpoints (e.g., dashboard with sidebar at 1180px).

### Verification widths

Test at: `320 / 375 / 640 / 768 / 1024 / 1280 / 1440 / 1920`. The legacy 1440 / 1920 widths remain useful as sanity checks even though they are not active media-query targets.

---

## Mobile-First Philosophy

When a mockup shows only a desktop viewport:
1. **Build mobile layout first** — single column, stacked elements.
2. **Add complexity at breakpoints** — multi-column, larger spacing, bigger type.
3. **Document assumptions** — since the mobile view is not in the mockup, all mobile decisions are MEDIUM confidence at best.

```css
/* Mobile first: default styles are mobile */
.features__grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1.5rem;
}

/* Medium: 2 columns */
@media (min-width: 48rem) {
  .features__grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

/* Large: match mockup */
@media (min-width: 64rem) {
  .features__grid {
    grid-template-columns: repeat(3, 1fr); /* HIGH: matches mockup */
  }
}
```

### Touch-first adjustments
- Buttons / interactive controls → minimum 44×44px recommended (WCAG 2.2 AA requires 24×24px).
- Form inputs → ≥ 44px height + 16px font (prevents iOS auto-zoom).
- Tap targets ≥ 8px spacing.
- Hover-only effects → provide tap-or-focus equivalents.

---

## Breakpoint Estimation from Content

When the mockup doesn't specify breakpoints, infer them from layout density:

| Content Pattern | Likely Break | Reason |
|-----------------|--------------|--------|
| 3-column grid | ~768px → 1 col, ~1024px → 3 col | 3 cols too narrow below 1024px |
| 4-column grid | ~640px → 1 col, ~768px → 2 col, ~1024px → 4 col | Needs progressive build-up |
| Side-by-side text+image | ~768px → stack | Text becomes too narrow below |
| Pricing cards (3) | ~768px → stack, ~1024px → 3 | Cards need ~300px minimum |
| Navigation | ~768px → hamburger | Standard mobile nav pattern |
| Sidebar + content | ~1024px → side-by-side | Below this, sidebar collapsed/below content |

---

## Fluid Typography (clamp)

### Formula
```css
font-size: clamp(MIN, BASE + VW-DELTA, MAX);
```

Where:
- MIN = mobile size (e.g., `1rem`)
- MAX = desktop size (e.g., `1.5rem`)
- VW-DELTA = `calc(MIN_REM + (MAX - MIN) * ((100vw - MIN_VW) / (MAX_VW - MIN_VW)))`

### Simple linear interpolation example
Desktop H1 = 48px, Mobile H1 = 32px, range 320–1440px:
```css
:root {
  --fs-h1: clamp(2rem, 1.71rem + 1.43vw, 3rem);
  /* min 32px @ 320px, max 48px @ 1440px */
}
```

### Quick scale (8-step type system)
```css
:root {
  --fs-xs:   clamp(0.75rem, 0.71rem + 0.18vw, 0.875rem);  /* 12-14 */
  --fs-sm:   clamp(0.875rem, 0.84rem + 0.18vw, 1rem);     /* 14-16 */
  --fs-base: clamp(1rem, 0.96rem + 0.18vw, 1.125rem);     /* 16-18 */
  --fs-lg:   clamp(1.125rem, 1.07rem + 0.27vw, 1.25rem);  /* 18-20 */
  --fs-xl:   clamp(1.25rem, 1.16rem + 0.45vw, 1.5rem);    /* 20-24 */
  --fs-2xl:  clamp(1.5rem, 1.34rem + 0.80vw, 2rem);       /* 24-32 */
  --fs-3xl:  clamp(2rem, 1.71rem + 1.43vw, 3rem);         /* 32-48 */
  --fs-4xl:  clamp(2.5rem, 2.05rem + 2.23vw, 4rem);       /* 40-64 */
}
```

### Fluid spacing
```css
:root {
  --space-section: clamp(3rem, 2.4rem + 3vw, 6rem);     /* 48-96 */
  --space-block:   clamp(1.5rem, 1.2rem + 1.5vw, 3rem); /* 24-48 */
  --gap-grid:      clamp(1rem, 0.8rem + 1vw, 2rem);     /* 16-32 */
}
```

### Breakpoint-step typography (alternative)

Use when you want full designer control rather than smooth interpolation:

| Element | Mobile | Medium | Large | Method |
|---------|--------|--------|-------|--------|
| Hero h1 | 2rem | 2.5rem | 3rem+ | Breakpoint steps |
| Section h2 | 1.5rem | 1.75rem | 2.25rem | Breakpoint steps |
| Body | 1rem | 1rem | 1rem | Fixed |
| Small | 0.875rem | 0.875rem | 0.875rem | Fixed |

**Note**: Clamp values are MEDIUM confidence when derived from a single-viewport mockup. Document the assumed mobile minimum.

---

## Derivation Methodology

When the mockup shows only one viewport (typically desktop), follow this derivation procedure:

1. **Identify the source viewport.** From the mockup canvas size (e.g., 1440 × 900), assume this represents the Large or XL breakpoint.
2. **Mark all derived values LOW confidence.** Every breakpoint, fluid range, and reflow rule needs `/* LOW: derived from <source>, verify */` so reviewers can see what is inferred vs. measured.
3. **Apply mobile-first reflow rules** (see Section Reflow Patterns below) to determine the mobile structure from the desktop layout.
4. **Choose a typography strategy**: 8-step fluid `clamp` (default for marketing/LP) vs. breakpoint-step (default for dashboards / dense data).
5. **Choose spacing strategy**: fluid tokens vs. static `rem` with `@media` overrides. Fluid wins for prose-heavy pages; static wins for grid-heavy dashboards.
6. **Decide media query vs. container query per component** (see decision table below).
7. **Hand off with a Decision Walkthrough** (template at the bottom of this file) so the designer can confirm or override every derived rule.

---

## Section Reflow Patterns

### Hero: Desktop → Mobile
```css
/* Mobile */
.hero {
  min-height: 100vh; /* Full screen on mobile */
  min-height: 100svh; /* Safe area viewport */
  padding: 4rem 1.5rem;
  text-align: center;
}
.hero__headline { font-size: 2rem; }
.hero__subline  { font-size: 1rem; }
.hero__actions  { flex-direction: column; gap: 0.75rem; }

/* Large */
@media (min-width: 64rem) {
  .hero {
    min-height: 80vh;
    padding: 6rem 1.5rem;
  }
  .hero__headline { font-size: 3rem; } /* MEDIUM: match mockup */
  .hero__subline  { font-size: 1.25rem; }
  .hero__actions  { flex-direction: row; }
}
```

### Hero grid (alternative — symmetric reflow)
```css
.hero {
  display: grid;
  gap: var(--space-block);
  grid-template-columns: 1fr;  /* mobile */
}

@media (min-width: 48rem) {
  .hero {
    grid-template-columns: 1fr 1fr;  /* medium+ */
    align-items: center;
  }
}
```

### Navigation: Desktop → Mobile
```css
/* Mobile: hamburger (hide links) */
.nav__links { display: none; }
.nav__hamburger { display: block; }

/* Medium: show links */
@media (min-width: 48rem) {
  .nav__links     { display: flex; gap: var(--gap-grid); }
  .nav__hamburger { display: none; }
}
```

### Grid Sections: Desktop → Mobile (Pricing)
```css
/* Mobile: single column */
.pricing__grid {
  grid-template-columns: 1fr;
  gap: 1.5rem;
}
.pricing__card--featured { transform: none; }

/* Large: match mockup */
@media (min-width: 64rem) {
  .pricing__grid { grid-template-columns: repeat(3, 1fr); }
  .pricing__card--featured { transform: scale(1.05); }
}
```

### Card grid (container-aware)
```css
.card-grid {
  container-type: inline-size;
  display: grid;
  gap: var(--gap-grid);
  grid-template-columns: repeat(auto-fill, minmax(min(100%, 280px), 1fr));
}
/* Auto-reflows: 1col < 280, 2col < 580, 3col < 880, etc. */
```

### Footer: Desktop → Mobile
```css
/* Mobile: stacked */
.footer__grid  { grid-template-columns: 1fr; gap: 2rem; }
.footer__bottom { flex-direction: column; gap: 1rem; text-align: center; }

/* Medium: multi-column */
@media (min-width: 48rem) {
  .footer__grid   { grid-template-columns: 2fr repeat(3, 1fr); }
  .footer__bottom { flex-direction: row; text-align: left; }
}
```

### Common desktop → mobile reflow patterns (cheat sheet)

| Desktop | Mobile reflow |
|---------|---------------|
| Horizontal nav | Hamburger menu + drawer |
| 3-column hero (image + text + form) | Stack: text → image → form |
| Sidebar + content | Content full-width, sidebar collapsed/below |
| Multi-column footer | Stacked sections, accordion if dense |
| Inline form fields | Stacked fields, full-width inputs |
| Hover-revealed nav | Tap-toggle dropdown |

---

## Container Queries vs Media Queries

| Use case | Choose | Why |
|----------|--------|-----|
| Page-level layout (header / sidebar / footer) | `@media` | Tied to viewport |
| Component used in multiple slots (card, sidebar widget) | `@container` | Responds to parent width |
| User preferences (`prefers-color-scheme`, `prefers-reduced-motion`) | `@media` | Only available there |
| Print | `@media print` | Only available there |
| Modal / dialog responsive content | `@container` | Modal width varies by trigger |

### Container query example
```css
.card-wrapper {
  container-type: inline-size;
  container-name: card;
}

.card {
  display: grid;
  grid-template-columns: 1fr;
}

@container card (min-width: 400px) { .card { grid-template-columns: 1fr 2fr; } }
@container card (min-width: 600px) { .card { grid-template-columns: auto 1fr auto; } }
```

### When NOT to use container queries
- Page-level layout that depends on viewport.
- More than 3 levels of nested containers (browser overhead).
- When an unnamed query would match the wrong ancestor — always assign `container-name`.

---

## Aspect Ratio & Image Handling

### Modern aspect-ratio
```css
.hero-image {
  width: 100%;
  aspect-ratio: 16 / 9;
  object-fit: cover;
}

@media (min-width: 48rem) {
  .hero-image { aspect-ratio: 21 / 9; } /* wider on medium+ */
}
```

### Art-direction with `<picture>`
```html
<picture>
  <source media="(min-width: 64rem)" srcset="hero-wide.webp">
  <source media="(min-width: 48rem)" srcset="hero-tablet.webp">
  <img src="hero-mobile.webp" alt="..." loading="eager">
</picture>
```

### Responsive images via srcset
```html
<img
  src="card-400.webp"
  srcset="card-400.webp 400w, card-800.webp 800w, card-1200.webp 1200w"
  sizes="(min-width: 64rem) 33vw, (min-width: 48rem) 50vw, 100vw"
  alt="..."
  loading="lazy"
>
```

### Defaults
```css
img { max-width: 100%; height: auto; }

.split__image {
  width: 100%;
  aspect-ratio: 4/3;
  object-fit: cover;
}
@media (min-width: 48rem) {
  .split__image { aspect-ratio: auto; }
}
```

---

## Spacing Reduction on Mobile
```css
.section { padding: 3rem 1rem; }

@media (min-width: 48rem) { .section { padding: 4rem 1.5rem; } }
@media (min-width: 64rem) { .section { padding: 5rem 1.5rem; } } /* Match mockup */
```

---

## Touch Targets (WCAG 2.2 — 2.5.8 Target Size)

WCAG 2.2 AA requires minimum 24×24 CSS px; 44×44px is recommended for mobile:

```css
.nav__link,
.faq__question,
.footer__link {
  min-height: 2.75rem; /* 44px */
  display: flex;
  align-items: center;
}

.cta-button {
  min-height: 2.75rem;
  min-width: 2.75rem;
  padding: 0.75rem 1.5rem;
}
```

---

## Hidden / Shown Elements
```css
.desktop-only { display: none; }
.mobile-only  { display: block; }

@media (min-width: 48rem) {
  .desktop-only { display: block; }
  .mobile-only  { display: none; }
}
```

Prefer restructuring over `display: none` when content matters for SEO / a11y. If hiding for layout purposes only, this pattern is fine. If hiding because the content is irrelevant on that breakpoint, use `hidden` attribute or remove it from the DOM via SSR/CSR.

---

## Modern CSS for Faithful Reproduction (2025–2026)

Browser-support summary (as of 2026-05):

| Feature | Baseline | Ship to production? |
|---------|----------|---------------------|
| `subgrid` | Baseline Widely Available (2026-03-15, all stable engines) | Yes — first-class tool, no `@supports` needed |
| `:has()` parent selector | Baseline Widely Available | Yes |
| Container Queries (`@container`, `cqw/cqh`) | Baseline Widely Available, ~78% production adoption | Yes |
| Dynamic Viewport Units (`dvh/svh/lvh`) | Baseline Widely Available | Yes |
| Cascade Layers (`@layer`) | Baseline Widely Available | Yes |
| Native Nesting | Baseline Widely Available | Yes |
| `text-wrap: balance` / `pretty` | Baseline Widely Available | Yes |
| Anchor Positioning (`anchor-name`, `position-anchor`, `position-try-fallbacks`) | Baseline Newly Available — Chrome/Edge stable; Safari TP / Firefox partial | Progressive enhancement only; require JS fallback for popover/tooltip placement |
| `@scope` | Baseline Newly Available — Chrome/Edge stable; Safari/Firefox catching up | Progressive enhancement; nice-to-have, not load-bearing |
| Native CSS Masonry / Grid Lanes (`grid-template-rows: masonry`) | NOT Baseline — Safari TP only; Chrome competing `display: masonry` proposal; Firefox behind a flag | Do not ship without a JS or Grid fallback |
| `@starting-style` + `interpolate-size` (entry/exit transitions) | Baseline Newly Available — Chrome/Edge stable | Progressive enhancement for entrance animations |

### CSS Subgrid — Card Content Alignment

Subgrid is now Baseline Widely Available. Use it as the default for any mockup that shows horizontally-aligned card content (title row / description row / CTA row across all cards).

```css
.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 24px;
}
.card {
  display: grid;
  grid-template-rows: subgrid;
  grid-row: span 3; /* title + description + CTA */
}
```

**Rule**: Eliminates fixed-height hacks and the legacy "auto-flow + min-content" workarounds. No `@supports` gate required as of 2026-05.

### Anchor Positioning — Tooltip / Dropdown Reproduction

```css
.tooltip-trigger { anchor-name: --tip; }
.tooltip {
  position: fixed;
  position-anchor: --tip;
  position-area: top;
  position-try-fallbacks: bottom, right, left;
}
```

**Rule**: Use for mockups showing positioned overlays. Browser support is still uneven (Chrome/Edge stable, Safari/Firefox partial), so pair with a JS positioning fallback (Floating UI or manual `position: absolute`) when shipping cross-browser.

### `@scope` — Section Style Isolation

```css
@scope (.hero-section) {
  h1 { font-size: 3rem; }
  p  { font-size: 1.25rem; }
}
@scope (.features-section) {
  h2 { font-size: 2rem; }
  p  { font-size: 1rem; }
}
```

**Rule**: Use when mockup sections have different typography scales. Prevents style bleed. Still progressive enhancement in 2026-05 — pair with explicit class selectors so the layout still works on engines without `@scope` support.

### Native CSS Masonry — Pinterest Layout

```css
.masonry {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  grid-template-rows: masonry;
}
```

**Rule**: As of 2026-05, native Masonry is NOT Baseline. Safari TP has the most complete implementation; Chrome tabled a competing `display: masonry` proposal; Firefox keeps it behind a flag. Ship with `@supports (grid-template-rows: masonry)` and a Grid- or JS-based fallback (e.g., CSS multi-column or Masonry.js). Do not promise native masonry to designers as a faithful reproduction tool yet.

### Dynamic Viewport Units

Use `dvh` for mobile-accurate full-screen hero sections (accounts for address bar):

```css
.hero { min-height: 100dvh; }
```

| Unit | Behavior |
|------|----------|
| `svh` | Small viewport (address bar visible) |
| `lvh` | Large viewport (address bar hidden) |
| `dvh` | Dynamic — changes with browser chrome |

### CSS Nesting (Native)

```css
.pricing__card {
  border: 1px solid #e5e7eb;
  border-radius: 1rem;
  padding: 2rem;

  &--featured {
    border-color: transparent;
    box-shadow: 0 4px 24px rgba(0, 0, 0, 0.1);
    transform: scale(1.05);
  }

  @media (max-width: 64rem) {
    &--featured { transform: none; }
  }
}
```

### `:has()` Selector

```css
.form-group:has(:invalid) { border-color: #ef4444; }

.form-group:has(input:not(:placeholder-shown)) .label {
  transform: translateY(-1.5rem);
  font-size: 0.75rem;
}
```

### text-wrap: balance / pretty

```css
h1, h2, h3 { text-wrap: balance; }
p          { text-wrap: pretty; }
```

### Cascade Layers

```css
@layer reset, base, components, utilities;

@layer reset {
  *, *::before, *::after { box-sizing: border-box; margin: 0; }
}
@layer base {
  body { font-family: system-ui, sans-serif; line-height: 1.6; }
}
@layer components {
  .hero { /* ... */ }
  .pricing { /* ... */ }
}
```

### Subpixel Rendering Best Practices

```css
body {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

.thin-border {
  box-shadow: inset 0 0 0 0.5px rgba(0, 0, 0, 0.1);
}

.precise-element { transform: translateZ(0); }
```

---

## Common Pitfalls / Anti-patterns

| Pitfall | Avoidance |
|---------|-----------|
| Designing only at desktop, scaling down | Mobile-first: start CSS without media queries |
| Fixed `px` font sizes | Use `rem` + `clamp` for fluid scaling |
| Single-breakpoint thinking (just `@media (min-width: 768px)`) | Test all standard breakpoints + intermediate widths |
| Hover-only interactions | Provide tap or focus alternative |
| `100vh` on iOS bounces with URL bar | Use `100dvh` |
| Sub-44px tap targets on touch devices | Enforce minimum size in mobile breakpoint |
| Container query without named container in nested layout | Always assign `container-name` |
| Hiding content via `display: none` instead of restructuring | Hidden content still loads but is unreachable to screen readers if `hidden` not used |
| Pixel values for fluid spacing | Use `clamp()` or `vw` units |
| Assuming 1440px is the widest viewport | Test 1920px+ for ultrawide users |

---

## Decision Walkthrough Template

```
Mockup viewport: ___ x ___
Assumed source breakpoint: □ Large (1024+) □ XL (1280+) □ 2XL (1536+)

Implied derived breakpoints (LOW confidence):
  Mobile:   0-639
  Small:    640-767
  Medium:   768-1023
  Large:    1024-1279
  XL:       1280-1535
  2XL:      1536+

Type scale strategy:
  □ 8-step fluid (xs/sm/base/lg/xl/2xl/3xl/4xl with clamp)
  □ Breakpoint-step (per-element sizes at md / lg / xl)
  □ Custom — list per-element clamps

Spacing strategy:
  □ Fluid section/block/gap tokens
  □ Static rem with @media overrides

Container queries (component-level):
  □ Cards
  □ Sidebar widgets
  □ Modal contents
  □ N/A

Per-component reflow:
  □ Hero (1-col → 2-col @ 768)
  □ Nav (hamburger ↔ inline @ 768)
  □ Card grid (auto-fill minmax)
  □ Sidebar (stacked → side @ 1024)
  □ Form (stacked → inline @ 768)

Image strategy:
  □ aspect-ratio + object-fit
  □ <picture> art direction
  □ srcset + sizes
  □ loading="lazy" below fold

Verification:
  □ Test at 320 / 375 / 640 / 768 / 1024 / 1280 / 1440 / 1920
  □ Touch target check at mobile widths
  □ All derived values marked LOW confidence
  □ Designer review for derived breakpoints
```

---

## References
- MDN: CSS Container Queries, `clamp()`, `aspect-ratio`, `:has()`, `@scope`, `@layer`
- WCAG 2.2 — 2.5.8 Target Size (AA: 24×24; recommended 44×44)
- web.dev: Modern Responsive Design (Una Kravets)
- caniuse.com: `container-type`, `dvh`, `aspect-ratio`, `subgrid` (all Baseline as of 2026-05)
- Tailwind CSS docs: default breakpoints (`sm` 640 / `md` 768 / `lg` 1024 / `xl` 1280 / `2xl` 1536)
