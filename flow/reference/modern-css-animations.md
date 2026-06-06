# Modern CSS Animations

Purpose: Use this file when modern platform APIs can replace JavaScript or simplify animation architecture.

## Contents
- View Transitions API
- `@starting-style`
- Scroll-driven animations
- Scroll-triggered animations (Chrome 145+)
- `@property`
- Progressive enhancement rules

## Feature Gates (2026-05)

| Feature | Use For | Support |
|---------|---------|---------|
| View Transitions API (Level 1, same-document) | SPA route transitions, shared elements within one page | Baseline Newly Available — Chrome / Edge / Safari stable; Firefox in nightly |
| View Transitions Level 2 (MPA / cross-document) | Native MPA navigation without JS | Chrome `126+`, Safari `18.2+`, Firefox not yet — progressive enhancement only |
| `@starting-style` | Entry from `display: none`, popover / dialog open state | Baseline Newly Available |
| `interpolate-size` (`auto` → fixed transitions) | Animating to/from `height: auto`, `width: auto` | Chrome / Edge stable; Safari catching up — pair with `@starting-style` |
| Scroll-driven animations (`animation-timeline: view()` / `scroll()`) | Progress bars, reveal-on-scroll, parallax-lite | Chrome / Edge stable; Safari ships fragments; Firefox behind flag — feature-gate with `@supports` |
| `@property` | Animating custom properties, smooth gradient / shadow tweens | Baseline Widely Available |
| **Material 3 Expressive motion-physics** (spring-based) | Native Android transitions | Android 16 / Material 3 Expressive default |
| **Liquid Glass material** (iOS 26) | Translucent depth-aware surfaces that react to context / motion | iOS 26 SwiftUI / UIKit; CSS analogues are progressive enhancement only |

## Progressive Enhancement Rules

- Use `@supports` to gate modern features.
- Provide a CSS-only baseline before adding advanced behavior.
- Prefer View Transitions for context-preserving route changes, not every navigation.
- Avoid scroll-driven animation for essential content visibility.

## Minimal Examples

```js
document.startViewTransition(() => {
  updateDOM();
});
```

```css
::view-transition-old(root) {
  animation: fade-out 200ms ease-in;
}
::view-transition-new(root) {
  animation: fade-in 200ms ease-out;
}

dialog[open] {
  opacity: 1;
  transform: scale(1);
  transition: opacity 200ms ease-out, transform 200ms ease-out;

  @starting-style {
    opacity: 0;
    transform: scale(0.95);
  }
}

.reveal {
  opacity: 1;
  transform: none;
}

@supports (animation-timeline: view()) {
  .reveal {
    animation: fadeIn linear both;
    animation-timeline: view();
    animation-range: entry 0% entry 100%;
  }
}
```

## When Not To Use

- Do not require View Transitions on unsupported browsers.
- Do not use scroll-driven motion for key affordances.
- Do not use `@property` when a standard property animation is enough.

## View Transitions Level 2 (MPA Cross-Document)

Cross-document View Transitions enable page transitions without JavaScript in MPAs. Chrome 126+, Safari 18.2+. Firefox not yet supported.

### Basic MPA Transition

```css
/* Add to both source and destination pages */
@view-transition {
  navigation: auto;
}

/* Custom slide animation */
@keyframes slide-in-from-right {
  from { transform: translateX(100%); }
}
@keyframes slide-out-to-left {
  to { transform: translateX(-100%); }
}

::view-transition-new(root) {
  animation: slide-in-from-right 300ms ease-out;
}
::view-transition-old(root) {
  animation: slide-out-to-left 300ms ease-in;
}
```

### Shared Element Transition (MPA)

```css
/* Source page */
.hero-image {
  view-transition-name: hero-image;
}

/* Destination page — same view-transition-name */
.detail-image {
  view-transition-name: hero-image;
}
```

## @starting-style + transition-behavior

Pure CSS entry/exit animations for dialog and popover. Baseline achieved across all major browsers.

### Dialog Entry/Exit

```css
dialog {
  opacity: 0;
  transform: scale(0.95) translateY(8px);
  transition: opacity 200ms ease-out,
              transform 200ms ease-out,
              display 200ms allow-discrete,
              overlay 200ms allow-discrete;

  @starting-style {
    opacity: 0;
    transform: scale(0.95) translateY(8px);
  }
}

dialog[open] {
  opacity: 1;
  transform: scale(1) translateY(0);
}
```

### Popover Entry/Exit

```css
[popover] {
  opacity: 0;
  transform: translateY(4px);
  transition: opacity 150ms ease-out,
              transform 150ms ease-out,
              display 150ms allow-discrete,
              overlay 150ms allow-discrete;

  @starting-style {
    opacity: 0;
    transform: translateY(4px);
  }
}

[popover]:popover-open {
  opacity: 1;
  transform: translateY(0);
}
```

## Scroll-Driven Animations (Practical Examples)

Chrome 115+, Safari 26+ (with threaded execution on ProMotion displays). Firefox behind flag. Always wrap in `@supports` and provide reduced-motion fallback.

### ViewTimeline: Reveal on Scroll

```css
@media (prefers-reduced-motion: no-preference) {
  @supports (animation-timeline: view()) {
    .reveal {
      opacity: 0;
      animation: fadeUp linear both;
      animation-timeline: view();
      animation-range: entry 0% entry 60%;
    }
  }
}

@keyframes fadeUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
```

### ScrollTimeline: Progress Bar

```css
@supports (animation-timeline: scroll()) {
  .progress-bar {
    transform-origin: left;
    animation: progress linear;
    animation-timeline: scroll(root block);
  }

  @keyframes progress {
    from { transform: scaleX(0); }
    to { transform: scaleX(1); }
  }
}
```

### animation-range Keywords

| Keyword | Meaning |
|---------|---------|
| `entry 0% entry 100%` | Element entering the scroll area |
| `contain` | Element fully within the scroll area |
| `exit 0% exit 100%` | Element leaving the scroll area |

## @property for Gradient Animation

```css
@property --color-start {
  syntax: '<color>';
  initial-value: #6366f1;
  inherits: false;
}
@property --color-end {
  syntax: '<color>';
  initial-value: #8b5cf6;
  inherits: false;
}

.gradient-btn {
  background: linear-gradient(135deg, var(--color-start), var(--color-end));
  transition: --color-start 300ms ease-out, --color-end 300ms ease-out;
}

.gradient-btn:hover {
  --color-start: #4f46e5;
  --color-end: #7c3aed;
}
```

## Container Scroll-State Queries

Detect scroll-related states (`stuck`, `snapped`, `scrolled`) via CSS container queries — no JS scroll listeners needed.

```css
.sticky-header {
  container-type: scroll-state;
}

@container scroll-state(stuck: top) {
  .sticky-header {
    box-shadow: 0 2px 8px oklch(0 0 0 / 0.15);
    backdrop-filter: blur(8px);
  }
}

@container scroll-state(snapped: x) {
  .carousel-item { opacity: 1; }
}
```

- **Support**: Chrome 133+, Edge 133+. Use `@supports` for progressive enhancement.
- **Use cases**: Sticky header shadow, carousel snap indicators, "back to top" visibility.
- **Rule**: Always provide a no-support fallback — JS `IntersectionObserver` or static styling.

## Intrinsic Size Animation

Animate to/from `height: auto` natively — eliminates FLIP, `ResizeObserver`, and max-height hacks.

```css
:root {
  interpolate-size: allow-keywords;
}

.accordion-body {
  height: 0;
  overflow: clip;
  transition: height 0.3s ease, opacity 0.3s ease;
}

.accordion[open] > .accordion-body {
  height: auto;
}
```

- **Support**: Chrome 129+, Edge 129+. Not yet in Safari/Firefox.
- **`calc-size()`**: For computed intrinsic values — `calc-size(auto, size - 20px)`.
- **Fallback**: Use `max-height` with generous value or `grid-template-rows: 0fr / 1fr` trick.
- **Rule**: Prefer `interpolate-size` global opt-in over per-element `calc-size()`.

## CSS `linear()` Easing Function

Define complex easing curves (bounce, elastic, spring) in pure CSS — no JS libraries.

```css
/* Bounce easing */
.bounce {
  transition: transform 0.6s linear(
    0, 0.004, 0.016, 0.035, 0.063, 0.098, 0.141, 0.191,
    0.25, 0.316, 0.391, 0.472, 0.562, 0.66, 0.765, 0.878,
    1, 0.916, 0.844, 0.784, 0.735, 0.699, 0.675, 0.663,
    0.663, 0.675, 0.699, 0.735, 0.784, 0.844, 0.916, 1
  );
}

/* Spring easing */
.spring {
  transition: transform 0.5s linear(
    0, 0.009, 0.035, 0.078, 0.141, 0.222, 0.324, 0.446,
    0.591, 0.757, 0.946, 1.069, 1.115, 1.097, 1.033,
    0.957, 0.9, 0.879, 0.899, 0.951, 1.009, 1.042, 1.032,
    0.999, 0.976, 0.98, 1.001, 1.007, 1
  );
}
```

- **Support**: Baseline 2024 — all major browsers.
- **Tooling**: Use CSS `linear()` generator tools to convert spring/bounce parameters.
- **Rule**: Prefer `linear()` over JS-based easing for transitions; keep GSAP/Motion for orchestrated sequences.

## Scroll-Triggered Animations (Chrome 145+)

Time-based animations that fire when crossing a scroll offset — unlike scroll-driven animations which scrub with scroll progress. Replaces many `IntersectionObserver` + `element.classList.add()` patterns with declarative CSS.

### Basic Usage

```css
@supports (animation-trigger: --reveal) {
  @scroll-trigger --reveal {
    trigger-scope: root;
    trigger-range: entry 0% entry 50%;
  }

  .card {
    animation: fadeUp 400ms ease-out both;
    animation-trigger: --reveal play-forwards;
  }
}

@keyframes fadeUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
```

### Key Differences from Scroll-Driven

| Aspect | Scroll-Driven | Scroll-Triggered |
|--------|---------------|------------------|
| Timeline | Scroll position controls progress | Time-based (plays at own pace) |
| Reversibility | Reverses when scrolling back | Configurable via `play-backwards` |
| Use case | Progress bars, parallax | Entrance reveals, count-ups |
| API | `animation-timeline: scroll()/view()` | `animation-trigger` + `@scroll-trigger` |

- **Support**: Chrome 145+ only. Use `@supports (animation-trigger: ...)` for progressive enhancement.
- **Fallback**: `IntersectionObserver` + class toggle for unsupported browsers.
- **Rule**: Prefer scroll-triggered for entrance animations; prefer scroll-driven for progress-linked motion.

## Updated Feature Gate Table

| Feature | Use For | Support |
|---------|---------|---------|
| View Transitions Level 1 | SPA transitions, shared elements | Chrome 111+, Safari 18+, Firefox 133+ (**Baseline**) |
| View Transitions Level 2 | MPA/cross-document transitions | Chrome 126+, Safari 18.2+ (Firefox not supported) |
| `@starting-style` | Entry from display:none, popover/dialog | Chrome 117+, Safari 17.4+, Firefox 129+ (**Baseline**) |
| `transition-behavior: allow-discrete` | Bidirectional display:none animation | All major browsers (**Baseline**) |
| Scroll-driven animations | Progress bars, reveal-on-scroll | Chrome 115+, Safari 26+ (Firefox behind flag; `@supports` required) |
| Scroll-triggered animations | Entrance reveals, time-based on scroll | Chrome 145+ (`@supports` required) |
| Container Scroll-State | Sticky shadow, snap indicators | Chrome 133+ (`@supports` required) |
| `interpolate-size` | Height:auto animation, accordion | Chrome 129+ (progressive enhancement) |
| `linear()` easing | Bounce, elastic, spring CSS-only | All major browsers (**Baseline 2024**) |
| `@property` | Animating custom properties, gradients | Chrome 85+, Safari 15.4+ (Firefox not yet) |
