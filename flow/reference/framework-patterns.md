# Framework Patterns

Purpose: Use this file when Flow work must match a specific frontend framework or motion library.

## Contents
- Framework defaults
- Reduced-motion hooks
- When to choose CSS vs JS

## Framework Defaults

| Framework | Preferred Approach | Use JS When | Reduced Motion Hook |
|-----------|--------------------|-------------|---------------------|
| Tailwind | `transition-*`, `animate-*`, custom keyframes | Gesture physics, orchestration, shared layout | `motion-safe:` / `motion-reduce:` |
| React | CSS first, then Motion (`motion/react`) | Gesture, layout transitions, drag, sequencing | `useReducedMotion()` from `motion/react` |
| Vue | `<Transition>` / `<TransitionGroup>` | JS hooks or WAAPI when CSS is insufficient | media query or app-level flag |
| Svelte | `transition:` / `in:` / `out:` / `animate:flip` | Custom gesture or timeline logic | media query or store-driven flag |
| Vanilla JS | CSS transitions or `element.animate()` | WAAPI control, imperative sequencing | `matchMedia('(prefers-reduced-motion: reduce)')` |
| Next.js | CSS or Motion; View Transitions if available | Shared layout, page choreography | same as React |
| Astro | CSS first, `<ViewTransitions />` when supported | Cross-page progressive enhancement | media query |

## Motion v12 (formerly Framer Motion)

Motion v12 changed the import path and added several features.

### Import Path Change

```tsx
// Before (framer-motion)
// import { motion } from 'framer-motion'

// After (motion v12+)
import { motion, AnimatePresence, useAnimate } from 'motion/react'
```

### New Features

```tsx
// oklch/oklab color space animation
<motion.div
  animate={{ color: 'oklch(0.7 0.15 220)' }}
  transition={{ duration: 0.3 }}
/>

// Axis-limited layout animation
<motion.div layout="y" />

// Layout anchor
<motion.div layout layoutAnchor="top" />
```

### WAAPI Integration

Motion v12 automatically switches between requestAnimationFrame and Web Animations API based on the animated properties. Hardware-accelerated properties (`transform`, `opacity`) use WAAPI for better performance.

## MPA View Transitions (Astro / Next.js)

### Astro

```css
/* Astro: use CSS instead of ViewTransitions component */
@view-transition {
  navigation: auto;
}
```

### Updated Framework Table

| Framework | Preferred Approach | Use JS When | Reduced Motion |
|-----------|--------------------|-------------|----------------|
| Tailwind | `transition-*`, `animate-*` | Gesture physics, orchestration | `motion-safe:` / `motion-reduce:` |
| React | CSS first, then Motion (`motion/react`) | Gesture, layout, drag, sequencing | `useReducedMotion()` from `motion/react` |
| Vue | `<Transition>` / `<TransitionGroup>` | JS hooks or WAAPI | media query or app-level flag |
| Svelte | `transition:` / `in:` / `out:` / `animate:flip` | Custom gesture/timeline | media query or store-driven flag |
| Vanilla | CSS transitions or `element.animate()` (WAAPI) | Imperative sequencing | `matchMedia('(prefers-reduced-motion)')` |
| Next.js | CSS or Motion; `@view-transition` for MPA | Shared layout, page choreography | same as React |
| Astro | CSS first, `@view-transition { navigation: auto }` | Cross-page progressive enhancement | media query |

## Implementation Rules

- Tailwind: keep motion inside utility scale or tokenized custom keyframes.
- React: avoid JS animation libs for simple hover and state changes.
- Vue: prefer CSS transitions before JS hooks.
- Svelte: use built-in transitions before custom functions.
- Vanilla: prefer WAAPI over ad hoc `setTimeout` choreography.
- Next.js and Astro: use View Transitions as progressive enhancement, not a hard dependency.

## Motion One (WAAPI-Based Lightweight Alternative)

Motion One uses the Web Animations API natively — smaller bundle, browser-level performance.

```js
import { animate } from "motion";

animate(".box", { transform: "translateX(100px)" }, { duration: 0.5, easing: "ease-out" });
```

| Aspect | Motion One | Motion v12 | GSAP |
|--------|-----------|------------|------|
| Bundle | ~3.8KB | ~18KB | ~28KB |
| Engine | WAAPI native | JS-driven | JS-driven |
| React integration | Vanilla / adapters | First-class | Plugin |
| Spring physics | Via `linear()` CSS | Built-in | CustomEase |
| Best for | Lightweight vanilla JS | React/Vue production | Complex timelines |

### Selection Rule

- Vanilla JS project, simple animations → Motion One
- React/Vue project, spring physics → Motion v12
- Complex timeline, scroll-triggered sequences → GSAP (all plugins free since Webflow acquisition 2024)

## Reduced Motion Example

```tsx
import { useReducedMotion } from "motion/react";

const shouldReduceMotion = useReducedMotion();

<motion.div
  initial={shouldReduceMotion ? { opacity: 0 } : { opacity: 0, y: 16 }}
  animate={shouldReduceMotion ? { opacity: 1 } : { opacity: 1, y: 0 }}
  transition={{ duration: shouldReduceMotion ? 0.12 : 0.24 }}
/>
```

```html
<div class="motion-safe:animate-slide-up motion-reduce:animate-none">
  Accessible animation
</div>
```
