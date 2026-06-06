# Animation Catalog

Purpose: Use this file when you need a concrete animation pattern, duration, easing choice, or reduced-motion fallback.

## Contents
- Entry and exit defaults
- Micro-interactions and state feedback
- Gesture patterns
- Scroll and page transitions
- Stagger guidance

## Entry Patterns

| Pattern | Duration | Easing | Use When | Reduced Motion |
|---------|----------|--------|----------|----------------|
| Fade in | `200ms` | ease-out | Default content appearance | Keep fade, shorten if needed |
| Slide up | `200-300ms` | ease-out | Cards, toasts, modals | Replace with fade |
| Scale in | `150-200ms` | ease-out | Popovers, menus, dropdowns | Replace with fade |
| Reveal / clip | `300ms` | ease-in-out | Hero media, image reveals | Prefer static reveal |

## Exit Patterns

| Pattern | Duration | Easing | Use When | Reduced Motion |
|---------|----------|--------|----------|----------------|
| Fade out | `150ms` | ease-in | Default exit | Keep fade |
| Slide down | `150-200ms` | ease-in | Toast and modal dismissal | Replace with fade |
| Scale out | `100-150ms` | ease-in | Popover close | Replace with fade |
| Collapse | `200ms` | ease-in-out | Accordions and expandable sections | Instant state change if needed |

Rule: exits are usually `60-80%` of entry duration.

## Micro-Interactions

| Pattern | Duration | Easing | Use When |
|---------|----------|--------|----------|
| Button press | `100ms` | ease-out | Click and tap confirmation |
| Toggle switch | `200ms` | ease-in-out | On/off state change |
| Ripple | `400ms` | ease-out | Material-style touch feedback |
| Pulse | `1000ms` | ease-in-out | Attention hint, not persistent CTA bait |
| Shake | `400ms` | ease-in-out | Error feedback only |
| Success state | `300ms` | ease-out | Completion feedback |
| Error state | `200ms` + shake | ease-out | Failed action feedback |
| Loading spinner | `1000ms` loop | linear | Active waiting state |
| Skeleton shimmer | `1500ms` loop | ease-in-out | Content placeholder |

## Gesture Patterns

| Pattern | Duration | Easing | Use When | Notes |
|---------|----------|--------|----------|-------|
| Drag feedback | continuous | spring | Reordering, drag surfaces | JS only |
| Swipe to dismiss | `200ms` | ease-out | Mobile notifications and rows | Dismiss threshold must be clear |
| Pull to refresh | `300ms` | ease-out | Mobile list refresh | Keep feedback functional |
| Long press | `400ms` hold | ease-in | Context menu trigger | Pair with non-motion affordance |
| Snap scroll | `300ms` | ease-out | Carousels, horizontal rails | Respect user control |

## Scroll and Page Patterns

| Pattern | Duration | Easing | Use When | Notes |
|---------|----------|--------|----------|-------|
| Scroll reveal | `400-600ms` | ease-out | Content entering viewport | Progressive enhancement only |
| Parallax | continuous | linear | Rare depth effect | Disable for reduced motion |
| Sticky header show/hide | `200ms` | ease-out | Scroll-aware chrome | Keep interaction stable |
| Crossfade page transition | `200-250ms` | ease-out | Route changes | Default page transition |
| Shared element transition | `300ms` | ease-in-out | Context-preserving route change | Use only when identity is clear |
| Slide lateral page transition | `200-250ms` | ease-out | Forward/back mental model | Direction must match navigation |

## Stagger Rules

- Use stagger only when sequential attention helps comprehension.
- Keep stagger intervals in the `30-80ms` range.
- Keep total stagger under `500ms`.
- `200ms * 10 items = 2s` is too slow.
- Prefer viewport-only stagger when long lists are involved.

## Minimal Examples

```css
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes slideUp {
  from { opacity: 0; transform: translateY(16px); }
  to { opacity: 1; transform: translateY(0); }
}

.card-enter {
  animation: slideUp 240ms var(--ease-out) both;
}

@media (prefers-reduced-motion: reduce) {
  .card-enter {
    animation: fadeIn 120ms ease-out both;
  }
}

## Modern CSS Patterns (2025)

| Pattern | Duration | Easing | Use When | Notes |
|---------|----------|--------|----------|-------|
| MPA cross-document fade | `200-250ms` | ease-out | Astro/MPA route changes | `@view-transition { navigation: auto }` only |
| Scroll-driven reveal | continuous | linear | ViewTimeline usage | `animation-range: entry 0% entry 60%` |
| Popover/dialog entry (pure CSS) | `150-200ms` | ease-out | `@starting-style` + `allow-discrete` | No JS required |
| Gradient hover transition | `300ms` | ease-out | `@property` gradient animation | Chrome/Safari only |
| Magnetic cursor pull | `300ms` | `cubic-bezier(0.33, 1, 0.68, 1)` | Creative/portfolio button hover | Wrapper padding creates detection zone |
| Aurora/holographic shift | `4-8s` | ease infinite | Premium card effects, hero backgrounds | `background-size: 200% 200%`, OKLCH gradient layers |
| Skeleton shimmer | `1.5-2s` | ease-in-out infinite | Content loading states | `background-size: 200% 100%`, linear-gradient animation |
| Liquid glass refraction | continuous | N/A | Overlay cards, iOS-style surfaces | SVG `feDisplacementMap` + `backdrop-filter: blur()` |
| Scroll-state sticky shadow | instant | N/A | Header shadow on stick | `@container scroll-state(stuck: top)`, CSS-only |
```

```tsx
<motion.ul variants={{ show: { transition: { staggerChildren: 0.05 } } }}>
  {items.map((item) => (
    <motion.li
      key={item.id}
      variants={{
        hidden: { opacity: 0, y: 16 },
        show: { opacity: 1, y: 0 },
      }}
    />
  ))}
</motion.ul>
```
