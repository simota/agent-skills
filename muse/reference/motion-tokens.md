# Motion Tokens Reference

Purpose: Define motion design tokens (duration, easing, spring) as a system-level vocabulary so animations stay consistent across components and platforms. Motion tokens encode *intent* (e.g. "fast UI feedback", "expressive enter") rather than literal `200ms` values, enabling theme-level retuning, reduced-motion fallbacks, and platform-specific output via Style Dictionary v5 / DTCG v2025.10.

## Scope Boundary

- **muse `motion`**: defines `duration.*`, `easing.*`, `spring.*`, and `motion-reduce.*` tokens. Authors DTCG-compliant token specs and reduced-motion fallback strategy. No animation code.
- **flow (elsewhere)**: implements animations using these tokens — keyframes, choreography, sequencing, performance tuning.
- **vision (elsewhere)**: sets motion *direction* and brand expressiveness (calm vs. energetic) before tokens are defined.
- **palette (elsewhere)**: fixes interaction-level usability (hit targets, perceived feedback) — not motion token definitions.
- **muse `theme` / `tokens`**: covers color, surface, and core token system; route here only for motion.

## Workflow

```
SURVEY    →  inventory current animations: hardcoded ms / ease values, reduced-motion gaps,
              cross-component drift (e.g. modal 250ms, dropdown 180ms, toast 320ms)

DEFINE    →  pick a duration scale (e.g. base 50ms, stops 100/150/200/300/500/700/1000)
              choose 4-6 easing curves (standard, decelerate, accelerate, emphasized, bounce)
              spring presets (gentle / wobbly / stiff / slow) for physics-based motion
              decide motion-reduce mapping: fade-only or instant-cut

VALIDATE  →  W3C DTCG v2025.10 compliance ($value/$type/$description)
              prefers-reduced-motion: every motion token has a reduce variant or fallback
              cross-platform: durations in ms (web), seconds (iOS Core Animation), float (Android)

PRESENT   →  token table, naming map, reduce-motion strategy, platform output samples
              handoff to Flow with semantic-to-component mapping
```

## Duration Scale

| Token | Value | Use |
|-------|-------|-----|
| `duration.0` | `0ms` | Instant — for reduced-motion fallback or skip animation |
| `duration.100` | `100ms` | Micro feedback — hover, focus ring, small state flips |
| `duration.150` | `150ms` | Fast UI — button press, checkbox tick, color transitions |
| `duration.200` | `200ms` | Standard UI — dropdown open, tooltip appear (default) |
| `duration.300` | `300ms` | Moderate — modal enter, drawer slide, tab switch |
| `duration.500` | `500ms` | Expressive — page transition, hero reveal |
| `duration.700` | `700ms` | Slow / dramatic — onboarding, success celebration |
| `duration.1000` | `1000ms` | Cinematic — splash, marketing reveal (use sparingly) |

Anchor point: `duration.200` is the default for generic UI transitions. Material 3 motion durations cluster `100/200/300/500ms`; align with that to ease cross-platform reasoning.

## Easing Tokens

| Token | Cubic-bezier | Use |
|-------|--------------|-----|
| `easing.linear` | `linear` | Progress bars, infinite loops |
| `easing.standard` | `cubic-bezier(0.2, 0, 0, 1)` | Default UI — Material 3 standard easing |
| `easing.decelerate` | `cubic-bezier(0, 0, 0, 1)` | Enter — element comes to rest |
| `easing.accelerate` | `cubic-bezier(0.3, 0, 1, 1)` | Exit — element leaves screen |
| `easing.emphasized` | `cubic-bezier(0.2, 0, 0, 1)` (with longer duration) | Hero / spotlight transitions |
| `easing.bounce` | `cubic-bezier(0.34, 1.56, 0.64, 1)` | Playful overshoot — toasts, success ticks |

## Spring Presets

For physics-based animation (Framer Motion, React Spring, SwiftUI, Jetpack Compose):

| Token | Stiffness | Damping | Use |
|-------|-----------|---------|-----|
| `spring.gentle` | `120` | `14` | Soft transitions, ambient motion |
| `spring.default` | `170` | `26` | Standard component motion |
| `spring.wobbly` | `180` | `12` | Playful, brand-expressive |
| `spring.stiff` | `210` | `20` | Snappy, immediate feedback |
| `spring.slow` | `280` | `60` | Slow, deliberate emphasis |

## Reduced-Motion Strategy

W3C `prefers-reduced-motion: reduce` should map **every** motion token to a safe variant. Two viable strategies:

| Strategy | Mapping | When to use |
|----------|---------|-------------|
| **Fade-only** | All transforms → opacity-only at `duration.150` | Default for product UI |
| **Instant-cut** | All durations → `duration.0` | Marketing pages with parallax / large transforms |

DTCG example:

```jsonc
{
  "duration": {
    "200": { "$value": "200ms", "$type": "duration" },
    "200-reduce": { "$value": "0ms", "$type": "duration" }
  }
}
```

Resolver document (`.resolver.json`) can swap full token sets when `prefers-reduced-motion` is active, avoiding per-component conditionals.

## Naming Conventions

- Numeric duration scale: `duration.{step}` where step = ms (e.g. `duration.200`).
- Semantic aliases optional: `duration.fast` → `{duration.150}`, `duration.moderate` → `{duration.300}`.
- Easing: descriptive intent (`standard` / `decelerate` / `emphasized`) — not curve coordinates.
- Spring: physical descriptor (`gentle` / `wobbly` / `stiff`) — not raw stiffness numbers.
- Reduce variant suffix: `-reduce` (e.g. `duration.300-reduce`).

## Anti-Patterns

- Hardcoding `transition: all 0.3s ease` in components — locks animation policy at the component level; theme retunes break everywhere.
- One mega-easing-token (`easing.default`) used for enter, exit, and loops — directional motion needs decelerate (in) vs accelerate (out); collapsing them makes UI feel sluggish.
- Skipping `prefers-reduced-motion` — vestibular-disorder users see large transforms as nauseating; legal exposure under WCAG 2.2 SC 2.3.3.
- Defining durations as raw numbers (`200`) without `$type: duration` — DTCG v2025.10 rejects unit-less duration; Style Dictionary v5 emits incorrect platform output.
- Naming durations by use-case (`duration.modal`, `duration.toast`) — couples scale to specific components; reuse breaks when modal animation needs to slow down.
- Spring stiffness/damping copied across libraries without mapping — Framer Motion's `170/26` is not the same feel as SwiftUI's `0.5 response`; document the cross-platform mapping table.
- Ignoring iOS `UIAccessibility.isReduceMotionEnabled` and Android `Settings.Global.TRANSITION_ANIMATION_SCALE` — web `prefers-reduced-motion` covers browsers only; native apps need platform tokens.

## Handoff

- **To Flow**: motion-token spec with semantic mapping (`modal-enter` → `duration.300` + `easing.decelerate`), reduced-motion variants, and component-level guidance.
- **To Artisan**: token references for `transition`/`animation` properties in component CSS or styled-components.
- **To Showcase**: motion token catalog page with live examples and reduced-motion preview toggle.
- **To Palette**: when motion choices affect perceived responsiveness (>300ms feels laggy for primary CTAs), bring back to Palette for usability call.
- **To Polyglot**: directional motion tokens for RTL — slide-in-from-start vs slide-in-from-left.
