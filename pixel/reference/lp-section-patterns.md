# LP Section Patterns

**Purpose:** HTML/CSS templates and identification heuristics for common LP (Landing Page) sections.
**Read when:** You need to identify or generate code for LP sections from a mockup image.

## Contents
- Section Identification Heuristics
- Hero Section
- Navigation
- Features Section
- Pricing Section
- Testimonials Section
- FAQ Section
- CTA Section
- Footer Section
- Section Composition Rules

---

## Section Identification Heuristics

When scanning a mockup, identify sections by these visual cues:

| Section | Primary Cues | Secondary Cues |
|---------|-------------|----------------|
| Hero | Full-width, largest text on page, prominent button | Background image/gradient, above fold |
| Navigation | Top-positioned bar, logo on left | Horizontal links, hamburger icon, sticky behavior |
| Features | Repeated item pattern (3-4 items) | Icons/images + text pairs, grid layout |
| Pricing | Cards with price numbers | Plan names, feature lists, highlighted "recommended" |
| Testimonials | Quoted text, avatar photos | Company logos, star ratings, carousel indicators |
| FAQ | Question-answer pairs | Accordion indicators (+/−/▼), alternating styling |
| CTA | Centered heading + button | Contrasting background color, urgency language |
| Footer | Bottom of page, multi-column | Small text, social icons, copyright line |

### Confidence Rules for Section Detection

- **HIGH**: 3+ primary cues match → proceed with identified pattern
- **MEDIUM**: 1-2 primary cues match → apply pattern but annotate uncertainty
- **LOW**: Only secondary cues → generate generic section, flag for review

---

## Hero Section

### Template (Vanilla HTML/CSS)

```html
<section class="hero">
  <div class="hero__background">
    <!-- Background: image, gradient, or solid color -->
    <img src="hero-bg.jpg" alt="" role="presentation" class="hero__bg-image" />
  </div>
  <div class="hero__content">
    <h1 class="hero__headline"><!-- Extracted headline text --></h1>
    <p class="hero__subline"><!-- Extracted subline text --></p>
    <div class="hero__actions">
      <a href="#" class="hero__cta-primary"><!-- Primary CTA text --></a>
      <!-- Optional secondary CTA -->
      <a href="#" class="hero__cta-secondary"><!-- Secondary CTA text --></a>
    </div>
  </div>
</section>
```

```css
.hero {
  position: relative;
  min-height: 80vh; /* MEDIUM: adjust based on mockup */
  display: flex;
  align-items: center;
  overflow: hidden;
}

.hero__background {
  position: absolute;
  inset: 0;
}

.hero__bg-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.hero__content {
  position: relative;
  z-index: 1;
  max-width: 48rem; /* MEDIUM: ~768px, adjust to mockup */
  margin: 0 auto;
  padding: 6rem 1.5rem;
  text-align: center;
}

.hero__headline {
  font-size: 3rem; /* MEDIUM: extract from mockup */
  font-weight: 700;
  line-height: 1.1;
  color: #ffffff; /* Extract from mockup */
}

.hero__subline {
  margin-top: 1rem;
  font-size: 1.25rem; /* MEDIUM: extract from mockup */
  color: rgba(255, 255, 255, 0.8);
  max-width: 36rem;
  margin-inline: auto;
}

.hero__actions {
  margin-top: 2rem;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
}

.hero__cta-primary {
  display: inline-block;
  padding: 0.75rem 1.5rem;
  border-radius: 0.5rem;
  font-weight: 600;
  text-decoration: none;
  transition: opacity 0.2s;
}

.hero__cta-secondary {
  text-decoration: underline;
  text-underline-offset: 4px;
  transition: opacity 0.2s;
}
```

### Variations

| Variant | Detection Cue | Modification |
|---------|---------------|-------------|
| Split hero | Image on one side, text on other | Use `display: grid; grid-template-columns: 1fr 1fr` |
| Video background | Play button or motion indicators | Replace `<img>` with `<video autoplay muted loop>` |
| Gradient overlay | Translucent color over image | Add `::after` pseudo-element with gradient |
| Text-only | No background image | Remove background layer, adjust typography |

---

## Navigation

```html
<header class="nav">
  <div class="nav__container">
    <a href="/" class="nav__logo">
      <img src="logo.svg" alt="Site Name" />
    </a>
    <nav class="nav__links" aria-label="Main navigation">
      <a href="#features" class="nav__link">Features</a>
      <a href="#pricing" class="nav__link">Pricing</a>
      <a href="#faq" class="nav__link">FAQ</a>
    </nav>
    <a href="#" class="nav__cta">Get Started</a>
  </div>
</header>
```

```css
.nav {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 50;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(8px);
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
}

.nav__container {
  max-width: 72rem;
  margin: 0 auto;
  padding: 0 1.5rem;
  height: 4rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.nav__links {
  display: flex;
  gap: 2rem;
}

.nav__link {
  font-size: 0.875rem;
  font-weight: 500;
  color: #374151;
  text-decoration: none;
  transition: color 0.2s;
}

.nav__link:hover {
  color: #111827;
}

.nav__cta {
  font-size: 0.875rem;
  font-weight: 600;
  padding: 0.5rem 1rem;
  border-radius: 0.375rem;
  text-decoration: none;
}
```

---

## Features Section

```html
<section class="features" id="features">
  <div class="features__container">
    <h2 class="features__heading"><!-- Section heading --></h2>
    <p class="features__description"><!-- Section description --></p>
    <div class="features__grid">
      <!-- Repeat for each feature -->
      <div class="features__item">
        <div class="features__icon"><!-- Icon or image --></div>
        <h3 class="features__item-title"><!-- Feature title --></h3>
        <p class="features__item-desc"><!-- Feature description --></p>
      </div>
    </div>
  </div>
</section>
```

```css
.features__container {
  max-width: 72rem;
  margin: 0 auto;
  padding: 5rem 1.5rem;
}

.features__heading {
  font-size: 2.25rem;
  font-weight: 700;
  text-align: center;
}

.features__description {
  margin-top: 1rem;
  font-size: 1.125rem;
  text-align: center;
  color: #6b7280;
  max-width: 36rem;
  margin-inline: auto;
}

.features__grid {
  margin-top: 3rem;
  display: grid;
  grid-template-columns: repeat(3, 1fr); /* Adjust column count from mockup */
  gap: 2rem;
}

.features__item {
  text-align: center;
}

.features__icon {
  width: 3rem;
  height: 3rem;
  margin: 0 auto 1rem;
}

.features__item-title {
  font-size: 1.25rem;
  font-weight: 600;
}

.features__item-desc {
  margin-top: 0.5rem;
  font-size: 0.9375rem;
  color: #6b7280;
  line-height: 1.6;
}
```

---

## Pricing Section

```html
<section class="pricing" id="pricing">
  <div class="pricing__container">
    <h2 class="pricing__heading"><!-- Pricing heading --></h2>
    <div class="pricing__grid">
      <!-- Repeat for each plan -->
      <div class="pricing__card pricing__card--featured">
        <div class="pricing__badge"><!-- e.g., "Most Popular" --></div>
        <h3 class="pricing__plan-name"><!-- Plan name --></h3>
        <div class="pricing__price">
          <span class="pricing__currency">$</span>
          <span class="pricing__amount">29</span>
          <span class="pricing__period">/mo</span>
        </div>
        <ul class="pricing__features">
          <li class="pricing__feature"><!-- Feature item --></li>
        </ul>
        <a href="#" class="pricing__cta"><!-- CTA text --></a>
      </div>
    </div>
  </div>
</section>
```

```css
.pricing__container {
  max-width: 72rem;
  margin: 0 auto;
  padding: 5rem 1.5rem;
}

.pricing__heading {
  font-size: 2.25rem;
  font-weight: 700;
  text-align: center;
}

.pricing__grid {
  margin-top: 3rem;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
  align-items: start;
}

.pricing__card {
  border: 1px solid #e5e7eb;
  border-radius: 1rem;
  padding: 2rem;
  text-align: center;
}

.pricing__card--featured {
  border-color: transparent;
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.1);
  transform: scale(1.05);
}

.pricing__badge {
  display: inline-block;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  margin-bottom: 1rem;
}

.pricing__amount {
  font-size: 3rem;
  font-weight: 700;
  line-height: 1;
}

.pricing__period {
  font-size: 1rem;
  color: #6b7280;
}

.pricing__features {
  list-style: none;
  padding: 0;
  margin: 1.5rem 0;
  text-align: left;
}

.pricing__feature {
  padding: 0.5rem 0;
  border-bottom: 1px solid #f3f4f6;
  font-size: 0.9375rem;
}

.pricing__cta {
  display: block;
  padding: 0.75rem 1.5rem;
  border-radius: 0.5rem;
  font-weight: 600;
  text-decoration: none;
  text-align: center;
}
```

---

## FAQ Section

```html
<section class="faq" id="faq">
  <div class="faq__container">
    <h2 class="faq__heading"><!-- FAQ heading --></h2>
    <div class="faq__list">
      <!-- Repeat for each Q&A -->
      <details class="faq__item">
        <summary class="faq__question"><!-- Question text --></summary>
        <div class="faq__answer">
          <p><!-- Answer text --></p>
        </div>
      </details>
    </div>
  </div>
</section>
```

```css
.faq__container {
  max-width: 48rem;
  margin: 0 auto;
  padding: 5rem 1.5rem;
}

.faq__heading {
  font-size: 2.25rem;
  font-weight: 700;
  text-align: center;
  margin-bottom: 3rem;
}

.faq__item {
  border-bottom: 1px solid #e5e7eb;
}

.faq__question {
  padding: 1.25rem 0;
  font-size: 1.0625rem;
  font-weight: 500;
  cursor: pointer;
  list-style: none;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.faq__question::after {
  content: '+';
  font-size: 1.5rem;
  font-weight: 300;
  color: #9ca3af;
  transition: transform 0.2s;
}

.faq__item[open] .faq__question::after {
  content: '−';
}

.faq__answer {
  padding-bottom: 1.25rem;
  font-size: 0.9375rem;
  color: #6b7280;
  line-height: 1.7;
}
```

---

## CTA Section

```html
<section class="cta">
  <div class="cta__container">
    <h2 class="cta__heading"><!-- CTA heading --></h2>
    <p class="cta__description"><!-- CTA description --></p>
    <a href="#" class="cta__button"><!-- CTA button text --></a>
  </div>
</section>
```

```css
.cta {
  padding: 5rem 1.5rem;
  text-align: center;
}

.cta__container {
  max-width: 36rem;
  margin: 0 auto;
}

.cta__heading {
  font-size: 2.25rem;
  font-weight: 700;
}

.cta__description {
  margin-top: 1rem;
  font-size: 1.125rem;
  color: #6b7280;
}

.cta__button {
  display: inline-block;
  margin-top: 2rem;
  padding: 1rem 2rem;
  border-radius: 0.5rem;
  font-size: 1.0625rem;
  font-weight: 600;
  text-decoration: none;
  transition: opacity 0.2s;
}
```

---

## Footer Section

```html
<footer class="footer">
  <div class="footer__container">
    <div class="footer__grid">
      <div class="footer__brand">
        <img src="logo.svg" alt="Site Name" class="footer__logo" />
        <p class="footer__tagline"><!-- Brand tagline --></p>
      </div>
      <!-- Repeat for each link group -->
      <div class="footer__group">
        <h4 class="footer__group-title"><!-- Group title --></h4>
        <ul class="footer__links">
          <li><a href="#" class="footer__link"><!-- Link text --></a></li>
        </ul>
      </div>
    </div>
    <div class="footer__bottom">
      <p class="footer__copyright">&copy; 2025 Company Name. All rights reserved.</p>
      <div class="footer__social">
        <!-- Social icons -->
      </div>
    </div>
  </div>
</footer>
```

```css
.footer {
  background: #111827;
  color: #d1d5db;
  padding: 4rem 1.5rem 2rem;
}

.footer__container {
  max-width: 72rem;
  margin: 0 auto;
}

.footer__grid {
  display: grid;
  grid-template-columns: 2fr repeat(3, 1fr); /* Adjust from mockup */
  gap: 2rem;
}

.footer__tagline {
  margin-top: 0.75rem;
  font-size: 0.875rem;
  color: #9ca3af;
}

.footer__group-title {
  font-size: 0.875rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: #f9fafb;
  margin-bottom: 1rem;
}

.footer__links {
  list-style: none;
  padding: 0;
}

.footer__link {
  display: block;
  padding: 0.25rem 0;
  font-size: 0.875rem;
  color: #9ca3af;
  text-decoration: none;
  transition: color 0.2s;
}

.footer__link:hover {
  color: #f9fafb;
}

.footer__bottom {
  margin-top: 3rem;
  padding-top: 1.5rem;
  border-top: 1px solid #374151;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.footer__copyright {
  font-size: 0.8125rem;
  color: #6b7280;
}
```

---

## 2025 Emerging LP Section Patterns

### Interactive Demo Section

Increasingly common in SaaS LPs — embed a product walkthrough directly on the page:

```html
<section class="demo" id="demo">
  <div class="demo__container">
    <h2 class="demo__heading">See it in action</h2>
    <div class="demo__embed">
      <!-- Interactive demo embed (Navattic, Storylane, or custom) -->
      <iframe src="..." title="Product demo" loading="lazy"></iframe>
    </div>
  </div>
</section>
```

### ROI Calculator Section

SaaS LPs with slider/form to calculate concrete savings:

```html
<section class="roi" id="roi">
  <div class="roi__container">
    <h2 class="roi__heading">Calculate your savings</h2>
    <div class="roi__calculator">
      <label for="team-size">Team size</label>
      <input type="range" id="team-size" min="1" max="100" value="10" />
      <div class="roi__result">
        <span class="roi__amount">$2,400</span>
        <span class="roi__period">saved per year</span>
      </div>
    </div>
  </div>
</section>
```

### Comparison Section

Direct competitor comparison table — effective for SEO and decision-making:

```html
<section class="compare" id="compare">
  <div class="compare__container">
    <h2 class="compare__heading">How we compare</h2>
    <table class="compare__table">
      <thead>
        <tr>
          <th>Feature</th>
          <th class="compare__us">Our Product</th>
          <th>Competitor A</th>
          <th>Competitor B</th>
        </tr>
      </thead>
      <!-- Feature rows -->
    </table>
  </div>
</section>
```

---

## CTA Placement Strategy (2025 Best Practice)

CTAs should appear in at least **5 locations** throughout the LP:

1. **Hero section** — primary CTA
2. **After social proof** — reinforcement
3. **After features/benefits** — when value is understood
4. **After pricing** — decision point
5. **Final CTA section** — last chance, before footer

### Micro-copy Under CTAs

Always include anxiety-reducing text below the CTA button:

```html
<a href="#" class="cta-button">Start free trial</a>
<p class="cta-microcopy">No credit card required · Cancel anytime</p>
```

### Sticky Mobile CTA

```css
.sticky-cta {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  z-index: 40;
  padding: 0.75rem 1rem;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(8px);
  border-top: 1px solid rgba(0, 0, 0, 0.05);
  /* Must not cover >30% of viewport (Google Better Ads Standards) */
}

/* Ensure sticky CTA doesn't obscure focused elements (WCAG 2.4.11) */
html {
  scroll-padding-bottom: 4rem;
}
```

---

## Modern CSS Techniques for LP Sections

### Subgrid for Aligned Pricing Cards

```css
.pricing__grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
}

.pricing__card {
  display: grid;
  grid-template-rows: subgrid;
  grid-row: span 4; /* plan-name, price, features, CTA — all aligned across cards */
}
```

### Scroll-Driven Section Animations

```css
@keyframes section-reveal {
  from { opacity: 0; transform: translateY(2rem); }
  to   { opacity: 1; transform: translateY(0); }
}

.section {
  animation: section-reveal linear both;
  animation-timeline: view();
  animation-range: entry 0% entry 100%;
}

/* Respect reduced motion preference */
@media (prefers-reduced-motion: reduce) {
  .section {
    animation: none;
    opacity: 1;
  }
}
```

### FAQ with @starting-style (no JS)

```css
.faq__answer {
  opacity: 1;
  max-height: 500px;
  transition: opacity 0.3s, max-height 0.3s;

  @starting-style {
    opacity: 0;
    max-height: 0;
  }
}
```

### content-visibility for Below-Fold Performance

```css
.below-fold-section {
  content-visibility: auto;
  contain-intrinsic-size: auto 600px; /* Estimated height */
}
```

---

## LP Performance Checklist

### Hero Image (LCP Target ≤ 2.5s)

```html
<!-- AVIF with fallback, explicit dimensions, high priority -->
<picture>
  <source srcset="hero.avif" type="image/avif">
  <source srcset="hero.webp" type="image/webp">
  <img
    src="hero.jpg"
    alt="Product showcase"
    width="1440" height="720"
    fetchpriority="high"
    decoding="async"
  >
</picture>
```

**Critical rules:**
- `fetchpriority="high"` on hero image
- NO `loading="lazy"` on above-fold images (worsens LCP)
- Explicit `width` and `height` to prevent CLS
- AVIF format: 50% smaller than JPEG at equivalent quality
- Inline critical CSS for hero section in `<style>` tag

### Below-Fold Images

```html
<img src="feature.avif" alt="..." width="600" height="400" loading="lazy" decoding="async">
```

---

## LP Accessibility Requirements (WCAG 2.2)

### Key Requirements for LP

| Criterion | Level | LP Impact |
|-----------|-------|-----------|
| 2.4.11 Focus Not Obscured | AA | Sticky header/CTA must not cover focused elements |
| 2.5.8 Target Size (Min) | AA | All buttons/links ≥ 24x24px (44x44px recommended) |
| 3.3.7 Redundant Entry | A | Multi-step forms must pre-fill previously entered data |
| 3.3.8 Accessible Auth | AA | Avoid CAPTCHA; use reCAPTCHA v3 (invisible) |

### Contrast on Hero Images

```css
/* Ensure text over hero images meets 4.5:1 contrast */
.hero__overlay {
  background: linear-gradient(
    to bottom,
    rgba(0, 0, 0, 0.6),
    rgba(0, 0, 0, 0.3)
  );
}
```

### Focus Styles

```css
:focus-visible {
  outline: 3px solid #005fcc;
  outline-offset: 3px;
  border-radius: 2px;
}
```

### Reduced Motion

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

---

## Section Composition Rules

1. **Order matters**: Sections should follow the mockup's vertical order exactly.
2. **Background alternation**: Alternate between base and raised backgrounds as seen in mockup.
3. **Spacing consistency**: Use the same section padding throughout unless the mockup clearly differs.
4. **ID anchors**: Add `id` attributes to sections for navigation link targets.
5. **One purpose per section**: Each `<section>` should serve a single clearly identifiable purpose.
6. **CTA repetition**: Place CTAs in at least 5 locations throughout the page.
7. **Performance layering**: Use `content-visibility: auto` on below-fold sections.
8. **Semantic landmarks**: Use `<header>`, `<nav>`, `<main>`, `<section>`, `<footer>` for accessibility.
