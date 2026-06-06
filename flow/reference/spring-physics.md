# Spring Physics Reference

Purpose: Implement spring-based motion that feels natural and responsive by tuning stiffness/damping/mass instead of duration/easing curves. Replaces tweened animations where interruption, overshoot, or velocity continuation matter — drag releases, modal pop-ins, gesture-following toggles.

> **2026 platform context.** **Google Material 3 Expressive** (Android 16) ships **spring-based physics motion as the platform default** — every default transition in the system is already a spring, not a Bezier tween. **Apple Liquid Glass** (iOS 26) builds analogous depth + physics behaviour into native surfaces. Implications for spring authoring:
>
> - On native Android (Compose Material 3 Expressive), the platform's default spring is usually correct — additional spring layers added by the team need to clear a higher justification bar to avoid "competing physics" noise.
> - On the web, spring physics remains opt-in: pair the library presets below with `prefers-reduced-motion` fallbacks, *and* test against platforms where the user is already on a spring-default OS (Android 16+ webview, iOS 26 Safari). Stacking another team-authored spring on top of an already-springy platform reads as motion noise, not delight.

## Scope Boundary

- **flow `spring`**: physics-driven motion implementation. Tune stiffness/damping/mass; map to Motion v12 / react-spring / CSS `linear()` approximations.
- **flow `hover` / `transition` (sibling)**: tween-based duration+easing patterns. Use those when motion is short, deterministic, and never interrupted.
- **flow `gesture` (sibling)**: touch/drag handling. Spring is the *release* model after a gesture ends — gesture owns the input handler, spring owns the settle.
- **muse (elsewhere)**: motion token definitions including spring presets. Spring physics consumes muse-authored presets; it does not author the system.
- **palette (elsewhere)**: UX critique of whether spring is the right feel at all. Spring assumes the decision is made.
- **artisan (elsewhere)**: production wiring of the component. Spring delivers the motion config; artisan owns lifecycle and props.

## Workflow

```
SURVEY   → identify trigger (drag release, toggle, modal entry); confirm interruption likely
         → confirm framework (Motion v12 / react-spring / Vue / CSS-only)

PLAN     → choose preset (gentle/wobbly/stiff/slow) or tune stiffness/damping/mass
         → decide property (transform/opacity only — no layout-triggering props)
         → define reduced-motion fallback (instant or short tween)

VERIFY   → measure settle time (should be < 800ms for UI; longer for ambient)
         → confirm 60fps on mid-tier mobile; check no layout thrash
         → validate prefers-reduced-motion path

PRESENT  → ship config + reduced-motion branch + perf note
```

## Library Pattern Map

| Library | API surface | Default preset | Notes |
|---------|-------------|----------------|-------|
| Motion v12 (`motion/react`) | `transition={{ type: "spring", stiffness, damping, mass }}` | stiffness 100, damping 10, mass 1 | Hardware-accelerated; `layout` prop uses spring by default |
| react-spring | `useSpring({ to, config: { tension, friction, mass } })` | `config.default` (tension 170, friction 26) | `tension`≈stiffness; presets: `gentle`, `wobbly`, `stiff`, `slow`, `molasses` |
| Vue (@vueuse/motion) | `transition: { type: 'spring', stiffness, damping }` | matches Motion v12 | Same model as Motion |
| CSS `linear()` | `animation-timing-function: linear(0, 0.5, 0.9, 1.05, 0.99, 1)` | hand-authored stops | Approximates spring; Baseline 2024. Use [linear-easing-generator](https://linear-easing-generator.netlify.app/) |
| Web Animations API | `element.animate(keyframes, { easing: 'linear(...)' })` | n/a | Pair with `linear()` for JS-driven CSS spring |

## Spring Parameter Cheat Sheet

| Parameter | Range | Effect |
|-----------|-------|--------|
| `stiffness` (tension) | 50-400 | Higher = faster acceleration, snappier |
| `damping` (friction) | 5-40 | Higher = less oscillation; below ~10 wobbles |
| `mass` | 0.5-3 | Higher = slower settle, more inertia |
| `velocity` | inherited | Pass exit velocity from gesture for continuity |

| Preset | stiffness | damping | mass | Use case |
|--------|-----------|---------|------|----------|
| Gentle | 100 | 14 | 1 | Modal fade-in, content reveal |
| Wobbly | 180 | 12 | 1 | Playful toggle, success badge |
| Stiff | 300 | 30 | 1 | Tab indicator, snap-to-grid |
| Slow | 80 | 20 | 1 | Ambient background motion |
| Drag-release | 250 | 25 | 1 | Card flick settle, bottom-sheet |

## Performance Thresholds

- Target 60fps (16.7ms/frame). Animate `transform` and `opacity` only; layout props break compositor path.
- Spring durations are *emergent* — set settle threshold (`restDelta: 0.01`, `restSpeed: 0.01` in Motion). Without a rest threshold, springs run indefinitely and burn battery.
- Hard cap 800ms for UI feedback springs; 1500ms for ambient. Beyond that, the perceived feel becomes "broken," not "bouncy."
- GPU layer budget: `will-change: transform` on ≤2 elements per page. Never apply `will-change` permanently — toggle on gesture start, remove on rest.
- Avoid spring on `width`/`height`/`top`/`left` — use `transform: scale()` / `translate()`. Layout-triggering springs are top CLS contributors.
- Animating `font-size` or CSS custom properties forces main-thread; do not spring them.

## prefers-reduced-motion

```css
@media (prefers-reduced-motion: reduce) {
  /* Replace spring with instant or 150ms ease-out tween */
  .spring-target { transition: opacity 150ms ease-out; transform: none; }
}
```

```js
// Motion v12
const reduce = useReducedMotion();
const transition = reduce ? { duration: 0 } : { type: "spring", stiffness: 200, damping: 20 };
```

Reduced-motion path is mandatory: spring overshoot is exactly the kind of motion vestibular-sensitive users react to. Replace with instant state change or a 100-150ms ease-out tween — never just lower the stiffness.

## Anti-Patterns

- Tuning duration on a spring — there is no `duration` field. If you need exact duration, you want a tween, not a spring.
- Setting `damping: 0` for "extra bounce" — undamped springs oscillate forever and never trigger `onRest`. Minimum damping 5.
- Springing layout properties (`width`, `height`, `top`, `left`) — causes CLS and main-thread thrash. Use `transform` equivalents.
- Omitting `restDelta` / `restSpeed` thresholds — spring fires `onRest` with float-precision drift never reaching exact target; animation runs forever in the background.
- Reusing one spring config across micro-interactions (12px hover) and large transitions (full-screen modal) — same stiffness feels snappy on small distances and sluggish on large ones. Tune per scale.
- Ignoring exit velocity from gestures — without `velocity` passthrough, drag-release springs feel disconnected from the user's flick.
- No reduced-motion branch — spring overshoot is a documented vestibular trigger; shipping without a fallback violates WCAG 2.3.3 and EAA.
- Springing every element on a page for "liveliness" — violates the 2-3 motion types per view budget; creates visual chaos.

## Handoff

- **To Radar**: spring config + frame-budget verification request (60fps on mid-tier mobile, no CLS regression).
- **To Muse**: if spring presets vary across components, escalate to motion-token authoring.
- **To Palette**: if user testing shows the spring feel is wrong (too playful, too sluggish), Palette owns the feel decision and re-briefs Flow.
- **To Bolt**: if spring causes INP > 200ms or CLS > 0.1 in CWV reports, escalate for broader perf optimization.
