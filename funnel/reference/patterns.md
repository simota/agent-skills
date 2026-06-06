# LP Design Patterns

**Purpose:** LP structure and layout patterns by LP type and section.
**Read when:** Selecting LP structure, choosing section-level design patterns.

> **Headline formulas** (PAS / BAB / 4U / 4Ps) referenced below are defined in `copy-lp-authoring.md` (sections "Headline Formulas" and "Formula Selection by Audience State"). This file specifies which formula fits each LP type and the section flow around it — not the formula mechanics.

---

## LP Type Patterns

### 1. SaaS Product LP

**Framework:** AIDA (first-time visitors) or PAS (problem-aware audience) — see `copy-lp-authoring.md#headline-formulas`
**Hero layout:** Pattern A (left text + right screenshot)
**CTA:** "Start free" / "14-day free trial"

**Section flow:**
1. Hero — product screenshot + value proposition
2. Pain Points — 3 key challenges
3. Solution — product intro + demo video
4. Benefits — 3–5 with icons
5. Social Proof — logo wall + testimonials
6. How It Works — 3-step process
7. Features — grid or tabs
8. Pricing — 3-tier comparison
9. FAQ — 5–7 objection handlers
10. Final CTA — free trial push

### 2. Lead Generation LP

**Framework:** PAS — see `copy-lp-authoring.md#pas--problem--agitate--solution`
**Hero layout:** Pattern D (split with form)
**CTA:** "Download free guide"
**Form:** 2–3 fields maximum

**Section flow:**
1. Hero — problem headline + inline form
2. Pain Amplification — data/statistics to concretize the problem
3. Solution Teaser — overview of what they'll get
4. What You Get — content preview (TOC, sample pages)
5. Author/Expert Proof — credentials, qualifications
6. Testimonials — from existing downloaders
7. Final CTA + Form — repeat form

### 3. Event / Webinar LP

**Framework:** 4Ps (Promise → Picture → Proof → Push) — 4Ps is event-LP-specific; for general formula selection see `copy-lp-authoring.md#formula-selection-by-audience-state`
**Urgency elements:** countdown timer + remaining seats
**CTA:** "Register free" / "Reserve your seat"

**Section flow:**
1. Hero — event name + date/time + registration CTA
2. What You'll Learn — 3–5 takeaways
3. Speaker Profiles — bios and credentials
4. Agenda — timeline
5. Past Event Proof — attendee testimonials + metrics
6. FAQ — logistics (how to join, recording availability)
7. Countdown + Final CTA

### 4. E-commerce Product LP

**Framework:** BAB — see `copy-lp-authoring.md#bab--before--after--bridge`
**Trust:** money-back guarantee badge required
**CTA:** "Buy now" / "Add to cart"

**Section flow:**
1. Hero — product image + price + purchase CTA
2. Problem/Before — life without the product
3. Product Benefits — life with the product
4. Product Demo — usage video/GIF
5. Social Proof — reviews + star ratings
6. Comparison — vs competitors table
7. Guarantee — refund/quality guarantee
8. Bundle/Upsell — set offers
9. Final CTA + Urgency

---

## Calm UI Landing Page Design

### Principles

| Principle | Do | Don't |
|-----------|-----|-------|
| Cognitive Clarity | Clear value proposition, generous whitespace, typographic hierarchy | Competing CTAs, information overload, visual noise |
| Trust Through Calm | Real testimonials, transparent pricing, honest copy | Fake urgency timers, "only 3 left" fabrications, hidden fees |
| Functional Minimalism | 1 primary CTA per viewport, restrained color palette | Rainbow gradients, auto-playing video, notification pop-ups |
| Progressive Information | Reveal detail on demand, scannable sections | Wall-of-text hero, collapsible FAQ hiding critical info |

### Calm UI vs Traditional LP

| Element | Traditional | Calm UI |
|---------|------------|---------|
| Hero CTA | "BUY NOW — 50% OFF ENDS TODAY!" | "Start your free trial" |
| Social proof | Animated counter, pop-up notifications | Static testimonials with names and roles |
| Urgency | Countdown timer, scarcity badges | "Join 2,000+ teams" — factual, not pressured |
| Form | 8+ fields with asterisks | 2-3 fields, progressive disclosure |

## View Transitions for LP Navigation

```css
/* Multi-step form transitions */
::view-transition-old(form-step) { animation: slide-out-left 0.3s ease; }
::view-transition-new(form-step) { animation: slide-in-right 0.3s ease; }

/* Section-to-section smooth scroll */
.lp-section { view-transition-name: lp-section; }
```

## Scroll-Driven LP Effects (CSS-Only)

```css
/* Reading progress bar */
.progress-bar {
  animation: grow-width linear both;
  animation-timeline: scroll(root);
}
@keyframes grow-width { from { width: 0; } to { width: 100%; } }

/* Section fade-in on scroll */
.reveal-section {
  animation: fade-up linear both;
  animation-timeline: view();
  animation-range: entry 0% entry 100%;
}
@keyframes fade-up { from { opacity: 0; translate: 0 30px; } }
```

**Rule**: CSS scroll-driven effects improve INP vs JS scroll listeners. Always provide `@supports` fallback.

## Modern CSS for LP

| Feature | LP Use Case |
|---------|-------------|
| `text-wrap: balance` | Headline auto-balancing (≤6 lines) |
| `color-mix()` | Button hover/active states from single color token |
| Popover API | FAQ expandable answers, feature tooltips |
| `@scope` | Section-isolated styles preventing bleed |

---

## Hero Section Visual Patterns (2025-2026)

### Gradient Mesh Hero Background

```css
.hero-bg {
  background:
    radial-gradient(at 40% 20%, hsla(228,100%,74%,1) 0px, transparent 50%),
    radial-gradient(at 80% 0%, hsla(189,100%,56%,1) 0px, transparent 50%),
    radial-gradient(at 0% 50%, hsla(355,85%,63%,1) 0px, transparent 50%);
  animation: meshMove 20s ease-in-out infinite alternate;
}
```

**Rule**: Hero only — never on repeated components. Slow animation (15-30s). Ensure text contrast with semi-transparent overlay. Products: Stripe, Vercel, Linear.

### Large Typography Hero

```css
.hero-headline {
  font-size: clamp(3rem, 8vw, 8rem);
  font-weight: 700;
  letter-spacing: -0.03em;
  line-height: 1.05;
}
```

Text-only hero (no image) with oversized headline. 37% higher reading completion. Pair with `text-wrap: balance` for clean line breaks.

### Dark Mode LP Default

Design LP dark-first: `#0C1120` background, single bright accent for CTAs, muted text for descriptions. 82% of mobile users prefer dark mode. Reduce visual fatigue, increase perceived premium quality.

### Pill Button CTA

```css
.cta-pill {
  border-radius: 999px;
  padding: 12px 32px;
  font-weight: 600;
  transition: transform 0.2s, box-shadow 0.2s;
}
.cta-pill:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0,0,0,0.15); }
```

---

## Bento Grid LP Layout

Use asymmetric Bento Grid for feature showcase sections as an alternative to card grids:

```css
.features-bento {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr;
  grid-template-areas: "main side1 side1" "main side2 side3";
  gap: 1rem;
}
@media (max-width: 768px) {
  .features-bento { grid-template-columns: 1fr; grid-template-areas: "main" "side1" "side2" "side3"; }
}
```

**Rule**: Largest cell = primary feature. CTR improves when visual hierarchy matches content priority. 67% of top SaaS sites now use Bento Grid.

## Scroll-Driven Storytelling for LP

Narrative-style LPs using CSS scroll-driven animations:

```css
/* Data-journalism style: number counter on scroll */
.stat-number {
  animation: count-up linear both;
  animation-timeline: view();
  animation-range: entry 20% cover 60%;
}

/* Sequential section reveal */
.story-section {
  animation: fade-slide-up linear both;
  animation-timeline: view();
  animation-range: entry 0% entry 80%;
}
@keyframes fade-slide-up {
  from { opacity: 0; transform: translateY(40px); }
  to { opacity: 1; transform: translateY(0); }
}
```

**Rule**: Scrollytelling converts 23% better than static LPs for complex products (data-heavy, multi-step). Keep each "scene" to 1 viewport height. Provide non-scroll fallback.

---

## Section-Level Patterns

### Pain Section

| Pattern | Structure | Best for |
|---------|-----------|----------|
| **Statistics-Driven** | Large number + supporting text (e.g., "73% of companies still use spreadsheets") | B2B, data-oriented audience |
| **Checklist** | ☑ list of pain points + transition CTA ("If any apply, we have a solution →") | Broad audience, quick scanning |

### Benefits Section

| Pattern | Structure | Best for |
|---------|-----------|----------|
| **Icon Grid** | 3–5 cards: icon + title + 1-line description | Most LPs |
| **Before/After** | Two-column comparison (❌ before vs ✅ after) | Transformation-focused products |

### How It Works

- Always 3 steps (cognitive simplicity).
- Structure: step number → title → 1-line description.
- Connect steps visually with arrows or a progress line.

### Pricing Section

- Highlight recommended plan visually (border, badge, background).
- Show annual billing toggle with discount percentage.
- CTA button on every plan.
- 3-tier is standard: Free / Pro (recommended) / Enterprise.

### FAQ Section

- Design as objection handlers, not generic Q&A.
- Map objections to FAQ format:
  - "Too expensive" → "Tell me about pricing plans" → respond with ROI.
  - "Seems hard" → "How long to set up?" → emphasize simplicity.
  - "Can I trust you?" → "Is it secure?" → certifications and track record.
  - "Not urgent" → "When should I start?" → frame opportunity cost.
