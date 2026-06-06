# Animation Extraction

Reference for Pixel's `animation` recipe. Extract micro-interactions from mockup signals (motion blur, ghost frames, multi-keyframe). Define interaction states, transition tokens, easing curves, reduced-motion fallback, and performance budget.

> Static mockups rarely encode motion. Most animation values are inferred from designer intent (signals like motion blur, ghost frames, hover-state mockups). Mark all derived motion values as LOW confidence.

---

## 1. Mockup Motion Signals

| Signal in mockup | Implies |
|---|---|
| Motion blur / streak lines | Translation animation, fast easing |
| Ghost frames (multiple semi-transparent copies) | Multi-keyframe animation, slow ease |
| Drop shadow with offset | Hover lift state |
| Two states side-by-side (default + hover) | Hover transition needed |
| Arc / curve overlay | Custom path animation |
| "Loading" placeholder bars / shimmer | Skeleton screen animation |
| Numbered annotations / state callouts | Multi-step interaction |
| Pulsing dot / ring | Attention-grabbing animation |
| Folded corner / page-turn imagery | Reveal / accordion animation |

---

## 2. Interaction State Matrix

For each interactive element, define all 5 states:

| State | Purpose | Visual change |
|---|---|---|
| `default` | Resting | Base styles |
| `hover` | Cursor over (pointer-fine only) | Subtle elevation, color shift |
| `focus` (`focus-visible`) | Keyboard focus | Visible outline (≥ 2px, ≥ 3:1 contrast) |
| `active` | Press (mousedown / touchstart) | Slight scale-down or color darken |
| `disabled` | Non-interactive | Reduced opacity, no pointer |

### Example: Button states
```css
.btn {
  background: var(--color-brand);
  color: var(--color-fg-on-brand);
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  transition: background-color var(--motion-fast) var(--ease-out),
              transform var(--motion-fast) var(--ease-out);
}

.btn:hover { background: var(--color-brand-hover); }

.btn:focus-visible {
  outline: 2px solid var(--color-brand);
  outline-offset: 2px;
}

.btn:active { transform: scale(0.97); }

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  pointer-events: none;
}
```

---

## 3. Motion Tokens

```css
:root {
  /* Durations */
  --motion-instant: 0ms;
  --motion-fast: 150ms;        /* hover, focus, small UI feedback */
  --motion-base: 250ms;        /* most transitions */
  --motion-slow: 400ms;        /* modals, drawers, layout changes */
  --motion-slower: 600ms;      /* page-level transitions */

  /* Easing — favor cubic-bezier over linear/ease */
  --ease-linear: linear;
  --ease-out: cubic-bezier(0.16, 1, 0.3, 1);     /* gentle exit */
  --ease-in: cubic-bezier(0.7, 0, 0.84, 0);      /* sharp entry */
  --ease-in-out: cubic-bezier(0.65, 0, 0.35, 1); /* smooth both */
  --ease-bounce: cubic-bezier(0.68, -0.55, 0.265, 1.55); /* playful overshoot */
}
```

### Easing intuition
- `ease-out`: starts fast, ends slow → exits, dismissals, "settling" motion
- `ease-in`: starts slow, ends fast → entrances, "ramping up" motion
- `ease-in-out`: smooth both ends → most reliable default
- `linear`: constant speed → loops, progress bars (avoid for transitions)
- `bounce`: overshoot → playful UI (sparingly)

---

## 4. Reduced-Motion Fallback (CRITICAL)

**`prefers-reduced-motion: reduce` must be honored.** Failure to do so is an a11y violation and triggers vestibular disorders.

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

### Targeted approach (preferred)
```css
.modal {
  transition: transform var(--motion-base) var(--ease-out);
}

@media (prefers-reduced-motion: no-preference) {
  .modal {
    transition: transform var(--motion-base) var(--ease-out),
                opacity var(--motion-base) var(--ease-out);
  }
}

@media (prefers-reduced-motion: reduce) {
  .modal { transition: opacity var(--motion-fast) var(--ease-linear); }
}
```

Critical: keep ESSENTIAL animations (loading spinners, progress) — they communicate state. Reduce DECORATIVE animations.

---

## 5. Performance Budget

### Composite-only animation (60fps guarantee)
Animate **ONLY**:
- `transform` (translate, scale, rotate)
- `opacity`
- `filter` (use sparingly — paint, not composite, on some GPUs)

**NEVER** animate:
- `width`, `height`, `top`, `left`, `right`, `bottom`, `margin`, `padding` → triggers layout
- `background-color`, `box-shadow`, `border-radius` → triggers paint
- `display`, `visibility` → discrete, can't transition smoothly

### Layout-trigger fallback
If you must change layout dimensions, use:
- `transform: scale()` instead of `width/height`
- `transform: translate()` instead of `top/left`
- `clip-path` / `mask` for reveal effects

### will-change (use surgically)
```css
.menu-panel { will-change: transform; }
/* Promotes to own layer; remove after animation */
```
Don't blanket-apply — wastes GPU memory.

### Hardware acceleration trick
```css
.element { transform: translateZ(0); }  /* forces GPU layer */
```

---

## 6. Common Micro-Interactions

### Hover lift
```css
.card {
  transition: transform var(--motion-fast) var(--ease-out),
              box-shadow var(--motion-fast) var(--ease-out);
}
.card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-3);
}
```

### Loading skeleton (shimmer)
```css
.skeleton {
  background: linear-gradient(
    90deg,
    var(--color-surface-2) 25%,
    var(--color-surface-3) 50%,
    var(--color-surface-2) 75%
  );
  background-size: 200% 100%;
  animation: shimmer 1.5s linear infinite;
}

@keyframes shimmer {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

@media (prefers-reduced-motion: reduce) {
  .skeleton { animation: none; background: var(--color-surface-2); }
}
```

### Modal entrance
```css
.modal {
  opacity: 0;
  transform: translateY(20px) scale(0.96);
  transition: opacity var(--motion-base) var(--ease-out),
              transform var(--motion-base) var(--ease-out);
}
.modal[data-state="open"] {
  opacity: 1;
  transform: translateY(0) scale(1);
}
```

### Accordion toggle
```css
.accordion-content {
  display: grid;
  grid-template-rows: 0fr;
  transition: grid-template-rows var(--motion-base) var(--ease-out);
}
.accordion-content > div { overflow: hidden; }
.accordion[data-state="open"] .accordion-content {
  grid-template-rows: 1fr;
}
/* Modern grid-template-rows trick — animates height without JS measurement */
```

### Toast slide-in
```css
.toast {
  transform: translateX(120%);
  transition: transform var(--motion-base) var(--ease-out);
}
.toast[data-state="show"] {
  transform: translateX(0);
}
```

### Pulse / attention
```css
@keyframes pulse {
  0%, 100% { transform: scale(1); opacity: 1; }
  50% { transform: scale(1.1); opacity: 0.7; }
}
.notification-dot { animation: pulse 2s ease-in-out infinite; }
```

---

## 7. Common Pitfalls

| Pitfall | Avoidance |
|---|---|
| Animating `width: 0 → 200px` causes layout thrash | Use `transform: scaleX()` or grid trick |
| `transition: all` slow + brittle | Specify exact properties |
| No reduced-motion fallback | Always add `@media (prefers-reduced-motion)` |
| 1-second transitions feel laggy | Stay under 400ms unless dramatic |
| `linear` easing for transitions feels mechanical | Use `ease-out` as default |
| `display: none → block` can't transition | Toggle `opacity` + `visibility`, or animate `height` via grid trick |
| Hover effects on touch devices stick | Wrap hover in `@media (hover: hover) and (pointer: fine)` |
| Multiple `will-change` properties → GPU memory waste | Apply only during active animation |
| Animating `box-shadow` is paint-heavy | Use `transform` to fake elevation, or limit shadow animation |
| No focus-visible state | Always pair `:hover` with `:focus-visible` |
| Bouncing animation on essential UI (e.g., navigation) | Reserve bounce for delight moments only |

---

## 8. Decision Walkthrough Template

```
Element: ____________________
Mockup signals: motion blur / ghost frames / hover-state shown / state callouts / N/A

State matrix:
  □ default  styles: ____
  □ hover    transition: ____  delta: ____
  □ focus    outline: ____
  □ active   transform: ____
  □ disabled opacity: ____

Motion tokens used:
  Duration: instant / fast / base / slow / slower
  Easing: out / in / in-out / bounce / linear

Composite-safe properties only?
  □ transform (translate/scale/rotate)
  □ opacity
  □ filter (verify GPU support)
  Layout-trigger properties avoided?
  □ Yes / No (justify)

Reduced-motion fallback:
  □ Animation disabled OR
  □ Reduced to opacity-only fade OR
  □ Essential animation kept (state communication)

Performance budget:
  Estimated frame cost: ____ ms (target ≤ 16ms for 60fps)
  will-change applied: only during animation / never / always (FIX)

Accessibility:
  □ focus-visible state present
  □ hover wrapped in @media (hover: hover)
  □ Sufficient contrast in all states

Confidence: LOW (derived from static mockup) — designer review needed
```

---

## 9. References
- web.dev: Animations and Performance (Paul Lewis)
- WCAG 2.1: 2.3.3 Animation from Interactions (AAA)
- MDN: `prefers-reduced-motion`, `cubic-bezier()`
- CSS Triggers (csstriggers.com) — paint/composite/layout reference
- Material Design 3: Motion principles (duration tokens, easing curves)
