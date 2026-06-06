# Animation Performance Anti-Patterns

Purpose: Use this file when motion work may affect frame time, Core Web Vitals, or rendering cost.

## Contents
- `AP-01` to `AP-07`
- Property cost tiers
- Frame budget
- Core Web Vitals impact
- `will-change` rules

## Anti-Patterns

| ID | Failure | Why It Fails | Safe Replacement |
|----|---------|--------------|------------------|
| `AP-01` | Animate layout properties | Forces layout on every frame | Replace with `transform` or `opacity` |
| `AP-02` | Layout thrashing in JS | Repeated read/write cycles force reflow | Batch reads, then writes, ideally in `requestAnimationFrame` |
| `AP-03` | `10+` simultaneous animated elements | CPU/GPU overload and frame drops | Stagger or limit viewport-visible motion |
| `AP-04` | Continuous `box-shadow` or heavy `filter` animation | Expensive paint workload | Prefer opacity or transform-based illusion |
| `AP-05` | Permanent `will-change` | Wastes memory and can hurt performance | Add just before animation and remove after |
| `AP-06` | Non-essential infinite loops | Persistent battery and GPU drain | Limit to loading indicators |
| `AP-07` | Main-thread-blocking animation logic | Jank and poor INP | Prefer CSS or WAAPI over heavy JS loops |

## Property Cost Tiers

| Tier | Properties | Guidance |
|------|------------|----------|
| `S` | `transform`, `opacity` | Preferred default |
| `A` | `filter`, `clip-path`, `color`, `background-color`, limited `box-shadow` | Use carefully and verify paint cost |
| `B` | `width`, `height`, `padding`, `margin`, `border-width` | Ask-first or redesign |
| `C` | `top`, `left`, `font-size`, `line-height` | Avoid for motion |

## Frame Budget

- `16.67ms` per frame at 60fps
- Browser overhead often consumes about `6ms`
- Keep JS + style + layout + paint within roughly `10ms`
- Treat `50ms+` long animation frames as a hard warning

## Core Web Vitals Impact

| Metric | Risk | Rule |
|--------|------|------|
| CLS | High | Do not animate layout-shifting properties |
| LCP | Medium | Do not delay critical content for showmanship |
| INP | High | Start feedback within `<200ms` and avoid heavy handler work |

## `will-change` Rules

- Use only on elements about to animate.
- Remove after the transition completes.
- Keep active `will-change` usage to `<=10` elements on a page.

## Review Checklist

- Composite-only by default
- No layout thrashing
- No excessive concurrency
- No non-essential infinite loops
- Reduced-motion path still works

## AP-08 / AP-09: Scroll-Driven Animation Performance

| ID | Failure | Why It Fails | Safe Replacement |
|----|---------|--------------|------------------|
| `AP-08` | Layout properties in scroll-driven animations | Layout thrashing on every scroll frame | Use `transform` / `opacity` only |
| `AP-09` | Scroll-driven animations on all sections | Simultaneous animation count explosion, GPU overload | Limit to viewport elements, max 5-10 elements |

### View Transitions Performance Notes

```css
/* Apply view-transition-name only to specific elements */
.hero-image {
  view-transition-name: hero-image;
}

/* NEVER do this — memory consumption explosion */
/* * { view-transition-name: auto; } */
```
