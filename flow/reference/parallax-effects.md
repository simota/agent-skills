# Parallax Effects Reference

Purpose: Implement depth-illusion via differential layer translation tied to scroll position. Covers multi-layer composition, performance budget for compositor-only execution, and mandatory `prefers-reduced-motion` handling — parallax is a documented vestibular trigger and is the most-abused motion pattern on the web.

## Scope Boundary

- **flow `parallax`**: continuous-scrub depth-illusion via translate offsets. Layers move at different rates relative to scroll.
- **flow `scroll` (sibling)**: discrete reveal triggers. Fires once/each-time at thresholds; not continuous scrubbing.
- **flow `transition` (sibling)**: route/modal motion. Unrelated to scroll position.
- **modern-css-animations.md (sibling reference)**: `animation-timeline: scroll()`/`view()` API — the modern, compositor-safe parallax mechanism.
- **palette (elsewhere)**: UX critique of whether parallax serves the user. Parallax often hurts content comprehension; Palette owns the "should we?" decision.
- **vision (elsewhere)**: creative direction calling for depth/atmosphere. Vision authors the brief; Flow scopes implementation.
- **artisan (elsewhere)**: production component owning layer markup. Flow wires the scroll coupling.

## Workflow

```
SURVEY   → confirm intent (atmospheric depth, hero only, not full-page)
         → confirm layer count (2-4 max), max translate range, viewport scope
         → confirm reduced-motion fallback (static, no parallax)

PLAN     → choose mechanism: scroll-driven CSS (preferred, Chrome 115+/Safari 26+)
           or rAF-throttled JS (universal fallback)
         → define rate per layer (background slowest, foreground fastest)
         → cap max translate offset to prevent layer escaping bounds

VERIFY   → confirm 60fps with DevTools Performance panel; check no layout/paint
         → verify prefers-reduced-motion disables parallax entirely
         → measure CLS — parallax-induced CLS is a common shipping blocker

PRESENT  → deliver code + reduced-motion branch + perf measurement
```

## Mechanism Map

| Mechanism | Browser support | Tradeoff |
|-----------|----------------|----------|
| CSS `animation-timeline: scroll()` | Chrome 115+, Safari 26+, Firefox flag | Compositor-only, no JS; preferred when support permits |
| CSS `animation-timeline: view()` | Chrome 115+, Safari 26+ | Per-element ranges; better for scoped parallax |
| `transform: translate3d()` on `scroll` rAF | Universal | Compatibility; requires careful throttling |
| GSAP ScrollTrigger `scrub` | All frameworks | Battle-tested, smooth scrub interpolation |
| Motion v12 `useScroll` + `useTransform` | React/Vue | Declarative; built-in scroll progress |

## Code Pattern Table

| Pattern | Snippet |
|---------|---------|
| CSS scroll-driven (modern) | `@keyframes drift { to { transform: translateY(-80px); } } .layer-bg { animation: drift linear; animation-timeline: scroll(root block); animation-duration: 1ms; }` |
| CSS view() scoped | `animation-timeline: view(); animation-range: cover 0% cover 100%;` |
| Motion v12 useScroll | `const { scrollYProgress } = useScroll(); const y = useTransform(scrollYProgress, [0,1], [0,-80]); <motion.div style={{ y }} />` |
| GSAP ScrollTrigger scrub | `gsap.to('.layer-bg', { yPercent: -30, ease: 'none', scrollTrigger: { trigger: '.section', start: 'top bottom', end: 'bottom top', scrub: true } })` |
| rAF-throttled vanilla | Cache `scrollY` in `scroll` listener (passive); apply via `requestAnimationFrame` to `transform: translate3d(0, Y, 0)` |

## Layer Rate Cheat Sheet

| Layer | Translate rate | Use |
|-------|---------------|-----|
| Background | 0.2-0.3× scroll | Sky, distant mountains, gradient atmosphere |
| Midground | 0.5-0.7× scroll | Decorative shapes, secondary visuals |
| Foreground | 0.9-1.1× scroll (near 1) | Primary content, slight lift only |
| Text content | 1.0× (none) | Never parallax body copy — comprehension breaks |

Rule: **content layers stay still, decoration moves**. Parallaxing text or primary CTAs is an accessibility regression.

## Performance Budget

| Budget | Threshold |
|--------|-----------|
| FPS during scroll | 60fps minimum, no drops below 50fps |
| Frame budget | 16.7ms; parallax should consume < 4ms |
| GPU layers (`will-change: transform`) | ≤2 elements per page (matches Flow Core Contract) |
| Layer count | 2-4 max; beyond 4, depth becomes noise |
| Max translate offset | ≤120px (or 15vh) — beyond this, layers escape natural bounds |
| Properties allowed | `transform: translate3d()` only. NO `top`/`left`/`margin`/`background-position` |
| Scroll handler | Must be `passive: true`; rAF-throttled if JS-driven |
| Compositor check | DevTools Layers panel — every parallax layer must show as a separate compositor layer with no paint flashing |

## prefers-reduced-motion

Parallax is one of the highest-priority motion patterns to disable under reduced-motion — it is a documented vestibular trigger that causes nausea and dizziness in sensitive users.

```css
@media (prefers-reduced-motion: reduce) {
  .parallax-layer {
    animation: none !important;
    transform: none !important;
  }
}
```

```js
const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
if (reduce) return; // skip useScroll/scrollTrigger entirely
```

This is non-negotiable: WCAG 2.3.3 (Animation from Interactions) and the EU Accessibility Act (effective June 2025) treat parallax disable under reduced-motion as a baseline requirement. Do not "soften" parallax for reduced-motion users — disable it completely.

## Anti-Patterns

- Parallaxing primary content — breaks reading flow, hurts comprehension, is the #1 reason "parallax sites" rank low in usability studies.
- Animating `background-position` for parallax — forces paint on every frame; 30fps at best on mid-tier mobile. Use `transform: translate3d()` on a layer.
- Scroll listener without `passive: true` — blocks scroll, causes jank. `addEventListener('scroll', fn, { passive: true })` always.
- Scroll listener without rAF throttling — fires 60+ times/second, recalculates layout each time, creates main-thread bottleneck.
- More than 4 parallax layers — perceptual depth caps at 3-4; additional layers just consume GPU memory and cause jitter.
- Parallax over the entire page height — full-page parallax is a top abandonment driver. Scope to hero or one feature section.
- No reduced-motion branch — parallax is *the* canonical vestibular trigger; shipping without disable violates WCAG 2.3.3.
- Animating layout-triggering properties (`top`, `margin-top`, `height`) — top CLS contributor; breaks Core Web Vitals immediately.
- Coupling parallax to `wheel` events instead of `scroll` — breaks touch, breaks keyboard scroll, breaks accessibility.
- Parallax inside a sticky/fixed container without `view()` ranges — layers escape bounds and float across unrelated sections.

## Handoff

- **To Radar**: parallax FPS verification on mid-tier mobile (target device: ~$250 Android, throttled CPU 4× in DevTools); CLS regression check.
- **To Bolt**: if parallax causes CLS > 0.1 or INP > 200ms, escalate. Compositor refactor or section scope reduction may be needed.
- **To Palette**: if user research shows confusion or nausea reports, Palette re-evaluates whether parallax should exist at all — Flow does not own the "should we?" decision.
- **To Vision**: if parallax direction conflicts across pages, escalate for unified depth-system direction.
- **To Canvas**: multi-section parallax choreography needs depth-layer diagram.
