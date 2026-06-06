# LP Section Structure Reference

**Purpose:** Quick reference for LP section composition during the BUILD phase.
**Read when:** Building LP sections and need structure guidance (not code).

---

## LP Section Checklist

Every LP should verify these elements are present:

### Hero Section
- Headline: benefit-driven, specific (include numbers when possible)
- Sub-headline: supports headline with detail or proof
- Primary CTA button (min-height 48px, contrast ≥ 4.5:1)
- Trust element inline ("1,200+ companies use us")
- Hero image/visual with `fetchpriority="high"`, explicit width/height

### Pain Section
- 2–3 pain points maximum (avoid overwhelming)
- Use statistics or checklist format
- Transition CTA linking pain to solution

### Benefits Section
- 3–5 benefits (not features)
- Icon + title + 1-line description per card
- Second CTA after benefits block

### Social Proof Section
- Use highest available proof type (see hierarchy in SKILL.md)
- Testimonials: Result → Challenge → Solution structure
- Named, with photo + company + title when possible
- Third CTA after social proof

### How It Works
- Exactly 3 steps (cognitive simplicity)
- Step number + title + 1-line description
- Visual connector between steps

### FAQ Section
- 5–7 items
- Each item handles a specific objection
- Use `<details>` / `<summary>` for accessible accordion
- Include FAQPage JSON-LD structured data

### Final CTA Section
- Urgency or scarcity message
- Risk reversal ("30-day money-back guarantee")
- Large CTA button

---

## Responsive Priorities

| Element | Desktop | Mobile |
|---------|---------|--------|
| Hero image | Full display | Hidden or reduced; text priority |
| CTA | Standard placement | Consider sticky bottom bar (CV +15–25%) |
| Multi-column | 3–4 columns | Single-column stack |
| Testimonials | Grid | Single card or carousel |
| Navigation | Minimal or none | None (LP has one purpose — no exits) |
| Form | Sidebar | Full-width, large inputs |

---

## Performance Checklist

- [ ] Hero image: `preload` + `fetchpriority="high"` + WebP with JPEG fallback
- [ ] Below-fold images: `loading="lazy"` + explicit width/height
- [ ] Fonts: ≤ 2 families, `font-display: swap`, preload critical weights
- [ ] Critical CSS: inline above-fold styles
- [ ] Non-critical CSS: defer via `media="print"` pattern
- [ ] Scripts: all non-essential deferred; analytics after `onload`
- [ ] CLS prevention: explicit dimensions on all media, `size-adjust` font fallback
- [ ] Third-party: `preconnect` for external origins, lazy-load widgets
- [ ] Targets: LCP ≤ 2.5s, INP < 200ms, CLS < 0.1, TTFB < 800ms

---

## Scroll Depth Tracking

Use `IntersectionObserver` to track section visibility. Fire analytics event when each section enters viewport (threshold 0.5). Implementation is straightforward — no code template needed.

## Sticky Mobile CTA

On viewports ≤ 768px, use `position: fixed; bottom: 0` CTA bar. Add `padding-bottom` to body to prevent content overlap. Keep bar height minimal (~72px).
