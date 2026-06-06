# Scroll-Triggered Animation Reference

Purpose: Implement entrance and reveal animations that fire when content crosses a scroll threshold. Distinguishes time-based triggers (animation plays at its own pace once activated) from scroll-driven scrubbing (progress tied to scroll position). Covers IntersectionObserver, CSS `animation-trigger` (Chrome 145+), and parallax-aware reveal coordination.

## Scope Boundary

- **flow `scroll`**: scroll-triggered entrance/reveal animations. Fire-once or fire-each-time patterns activated at offset thresholds.
- **flow `parallax` (sibling)**: depth-illusion via differential layer translation. Often co-located but a separate concern — parallax scrubs continuously; scroll-triggered fires discretely.
- **flow `transition` (sibling)**: route/modal transitions. Not scroll-coupled.
- **modern-css-animations.md (sibling reference)**: scroll-driven (`animation-timeline: scroll()`/`view()`) progress-scrubbing patterns. Use that when motion progress should track scroll position pixel-by-pixel.
- **palette (elsewhere)**: whether reveal-on-scroll is the right UX at all. Scroll-triggered assumes the decision is made.
- **muse (elsewhere)**: reveal-distance and stagger-timing tokens. Scroll-triggered consumes; muse authors.
- **artisan (elsewhere)**: production component that owns the wrapped content. Flow delivers the observer/trigger logic.

## Workflow

```
SURVEY   → confirm: fire-once vs fire-each-time, threshold (px or %), root margin
         → confirm framework, support targets (Chrome 145+ for animation-trigger?)

PLAN     → choose mechanism: IntersectionObserver (universal), animation-trigger (Chrome 145+),
           or scroll-driven view() timeline (Chrome 115+/Safari 26+)
         → define stagger interval if multiple children
         → reduced-motion fallback: instant visibility, no animation

VERIFY   → confirm 60fps; check observer disconnect on unmount
         → verify root margin handles sticky headers correctly
         → validate prefers-reduced-motion shows content immediately

PRESENT  → deliver observer + animation code + cleanup + reduced-motion branch
```

## Mechanism Map

| Mechanism | Browser support | When to use | Read |
|-----------|----------------|-------------|------|
| IntersectionObserver + class toggle | Universal (Baseline 2019) | Production-safe default; fire-once reveals | MDN IntersectionObserver |
| CSS `animation-trigger` | Chrome 145+ | Time-based animation triggered at scroll offset, no JS | reference/modern-css-animations.md |
| CSS `animation-timeline: view()` | Chrome 115+, Safari 26+ | Progress-tied scroll scrubbing (different model) | reference/modern-css-animations.md |
| Motion v12 `whileInView` | React/Vue | Declarative API wrapping IntersectionObserver | reference/framework-patterns.md |
| GSAP ScrollTrigger | All frameworks | Complex timelines, pin/scrub, callbacks | reference/framework-patterns.md |

## Code Pattern Table

| Pattern | Snippet |
|---------|---------|
| IntersectionObserver fire-once | `new IntersectionObserver((es) => es.forEach(e => e.isIntersecting && (e.target.classList.add('in'), io.unobserve(e.target))), { rootMargin: '0px 0px -10% 0px', threshold: 0.15 })` |
| Motion v12 viewport reveal | `<motion.div initial={{ opacity: 0, y: 24 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true, margin: "-10%" }} transition={{ duration: 0.5, ease: [0.16, 1, 0.3, 1] }} />` |
| CSS animation-trigger (Chrome 145+) | `animation: reveal 600ms cubic-bezier(.16,1,.3,1) both; animation-trigger: view() contain 0% cover 30%;` |
| GSAP ScrollTrigger | `gsap.from('.reveal', { y: 24, opacity: 0, duration: 0.6, scrollTrigger: { trigger: '.reveal', start: 'top 85%', toggleActions: 'play none none none' } })` |
| Stagger via stagger interval | Motion: `transition={{ staggerChildren: 0.08 }}`; GSAP: `stagger: 0.08` |

## IntersectionObserver Tuning

| Knob | Typical value | Effect |
|------|--------------|--------|
| `threshold` | 0.15 (15% visible) | Fires earlier with lower values; 0 fires at any pixel |
| `rootMargin` | `'0px 0px -10% 0px'` | Negative bottom margin delays fire until further into viewport |
| `root` | `null` (viewport) | Set to scroll container element for nested scrollers |
| Disconnect strategy | `unobserve` after fire-once | Required to prevent memory leak in long-lived pages |

## Performance Thresholds

- 60fps mandatory through reveal animation; 16.7ms frame budget.
- Animate `transform` and `opacity` only. `top`/`left`/`margin` reveals are top CLS offenders.
- IntersectionObserver itself is GPU-cheap; the cost is the animation it triggers. Limit to ≤8 simultaneous reveals per viewport.
- GPU layer (`will-change: transform`) toggled per-element on observe, removed in `transitionend`. Permanent `will-change` on dozens of below-fold elements is a documented memory bloat pattern.
- Stagger interval 60-120ms per child; below 60ms reads as simultaneous, above 150ms feels sluggish on 6+ children.
- Below-fold reveals must not cause CLS — reserve space (skeleton, fixed `min-height`) before the reveal fires. Reveal-from-collapsed (height: 0 → auto) is layout-triggering and breaks CWV.

## prefers-reduced-motion

```css
@media (prefers-reduced-motion: reduce) {
  .reveal { opacity: 1 !important; transform: none !important; transition: none; }
}
```

```js
const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
if (reduce) { element.classList.add('in'); return; }
// otherwise observe
```

Reduced-motion path is mandatory. Show content immediately at full opacity — never delay visibility behind a faded reveal, even a short one. WCAG 2.3.3 and EAA compliance.

## Parallax-Aware Reveal Coordination

When a section uses parallax (see `parallax-effects.md`) and reveals together, coordinate:

- Reveal fires **before** parallax depth becomes meaningful (parallax has 100% visible range; reveal has 15-30% threshold).
- Parallax must not depend on reveal having completed — they animate independent properties (parallax = `translateY` of layers; reveal = `opacity`/`translateY` of content).
- Disable parallax under `prefers-reduced-motion`; reveal still fires (instant visibility).

## Anti-Patterns

- Scroll listener instead of IntersectionObserver — `scroll` events fire 60+ times/second and force layout reads; use IntersectionObserver, which is async and compositor-aware.
- Forgetting `unobserve` after fire-once — leaks observers and DOM references on long-lived SPAs.
- Animating `height: 0 → auto` on reveal — layout-triggering, top CLS contributor. Use `transform: translateY()` + `opacity` and reserve space.
- Threshold `0` with `rootMargin: 0` — fires at the first pixel below the fold; users never see the reveal because it completes before scrolling brings the element into view. Use threshold 0.15 + negative bottom rootMargin.
- Reveal animations on every element in a long page (50+ items) — performance death by a thousand observers. Group reveals by section; observe the section, stagger children via CSS.
- No reduced-motion branch — reveals delay content for users who already opted out of motion. WCAG/EAA violation.
- Mixing scroll-driven (`animation-timeline: scroll()`) and scroll-triggered for the same element — they fight for the same animation slot. Pick one model per element.
- Using sticky headers without negative `rootMargin` — header overlaps the trigger zone, reveal fires when content is visually obscured.

## Handoff

- **To Radar**: scroll-trigger threshold + stagger interval verification on 3 viewport sizes (mobile/tablet/desktop) and with sticky header.
- **To Bolt**: if reveal causes CLS > 0.1, escalate. Reserve space and re-verify.
- **To Palette**: if research shows users miss CTA below long staggered reveals, Palette re-evaluates information density.
- **To Muse**: if reveal distance/stagger varies wildly across pages, escalate to token authoring.
- **To Canvas**: scroll-trigger choreography across multiple sections needs flow diagram.
