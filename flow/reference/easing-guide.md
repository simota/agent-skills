# Easing Guide

Purpose: Use this file when you need to choose easing curves or spring presets that match interaction intent.

## Contents
- Canonical easing curves
- Selection rules
- Spring presets
- Minimal token examples

## Canonical Easing Curves

| Easing | CSS Value | Use For |
|--------|-----------|---------|
| ease-out | `cubic-bezier(0, 0, 0.2, 1)` | Entry, hover, click feedback, user-response motion |
| ease-in | `cubic-bezier(0.4, 0, 1, 1)` | Exit, dismiss, departure |
| ease-in-out | `cubic-bezier(0.4, 0, 0.2, 1)` | Toggles, state changes, route changes |
| linear | `linear` | Spinners, progress bars, scroll-bound motion |
| ease-out-back | `cubic-bezier(0.34, 1.56, 0.64, 1)` | Playful emphasis only |
| ease-in-back | `cubic-bezier(0.36, 0, 0.66, -0.56)` | Playful exit only |
| spring | JS only | Drag release, physics-like gestures |

## Selection Rules

- User action response: `ease-out`
- Element appearing: `ease-out`
- Element disappearing: `ease-in`
- Toggle or morphing state: `ease-in-out`
- Continuous progress: `linear`
- Playful emphasis: `ease-out-back`, used sparingly
- Drag release: spring in JS, not CSS bezier unless approximated intentionally

## Spring Presets

| Preset | Tension / Stiffness | Friction / Damping | Use When |
|--------|----------------------|--------------------|----------|
| Snappy | `300` | `20` | Buttons, toggles, tight interactive feedback |
| Gentle | `170` | `26` | Panels, drawers, modal content |
| Bouncy | `120` | `14` | Badges, playful UI, lightweight emphasis |
| Stiff | `400` | `30` | Drag release, crisp repositioning |

## Token Example

```css
:root {
  --ease-out: cubic-bezier(0, 0, 0.2, 1);
  --ease-in: cubic-bezier(0.4, 0, 1, 1);
  --ease-in-out: cubic-bezier(0.4, 0, 0.2, 1);
  --ease-out-back: cubic-bezier(0.34, 1.56, 0.64, 1);
}
```

## JS Example

```tsx
<motion.div
  animate={{ scale: 1 }}
  transition={{ type: "spring", stiffness: 300, damping: 20 }}
/>
```

## Spring-Based Physics Animations

The industry is shifting from fixed `cubic-bezier` to spring-based motion for more natural, responsive interaction feedback.

### CSS `linear()` Spring Approximation

```css
/* Underdamped spring — natural button press */
.spring-press {
  transition: transform 0.5s linear(
    0, 0.009, 0.035, 0.078, 0.141, 0.222, 0.324, 0.446,
    0.591, 0.757, 0.946, 1.069, 1.115, 1.097, 1.033,
    0.957, 0.9, 0.879, 0.899, 0.951, 1.009, 1.042, 1.032,
    0.999, 0.976, 0.98, 1.001, 1.007, 1
  );
}
```

### Library Spring Presets

| Library | API | Best For |
|---------|-----|----------|
| Motion v12 | `transition={{ type: "spring", stiffness: 300, damping: 20 }}` | React/Vue production |
| React Spring | `useSpring({ config: config.gentle })` | Complex orchestrated spring |
| CSS `linear()` | Pure CSS spring curve approximation | Simple transitions, no JS |

### Selection Rule

- Single transition → CSS `linear()` spring (zero JS)
- Orchestrated multi-element → Motion v12 spring presets
- Complex physics simulation → React Spring / GSAP

## Scroll-Driven Animation Easing

Scroll-driven animations should use `linear` as the base timing function to maintain 1:1 correspondence between scroll position and animation progress.

```css
.scroll-driven {
  animation-timeline: view();
  animation-timing-function: linear;
}
```

### CSS linear() Function for Custom Scroll Curves

```css
/* Custom ease-out curve via linear() (Chrome 113+) */
.scroll-driven-eased {
  animation-timing-function: linear(
    0, 0.004, 0.016, 0.035, 0.063, 0.098 13.6%,
    0.196 27.3%, 0.489 54.5%, 0.607, 0.697,
    0.772, 0.83, 0.875, 0.908 90.9%, 0.961 100%
  );
}
```
