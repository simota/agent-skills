# Accessibility Patterns Reference

Purpose: Apply WCAG 2.1 AA interaction rules for semantics, keyboard access, screen readers, contrast, and motion reduction.

## Contents

- WCAG 2.1 AA quick reference
- Keyboard navigation
- Screen reader support
- Contrast and color
- Reduced motion
- Component patterns
- Testing

## WCAG 2.1 AA Quick Reference

| Area | Must-check rule |
|------|------------------|
| Non-text content | all meaningful images have alt text |
| Structure | semantic HTML conveys relationships |
| Contrast | text `4.5:1`, large text `3:1`, non-text UI `3:1` |
| Keyboard | all functionality works by keyboard |
| Focus | focus order is logical and visible |
| Error handling | errors are identified in text and suggest recovery |
| Status messages | dynamic updates use `aria-live` or equivalent semantics |

## Keyboard Navigation

Rules:

- DOM order should match visual order
- trap focus inside modals
- provide a visible focus ring
- include a skip link for repetitive navigation

Common keys:

| Key | Use |
|-----|-----|
| `Tab` / `Shift+Tab` | move focus |
| `Enter` / `Space` | activate controls |
| `Escape` | close modal or overlay |
| Arrow keys | move inside menus, tabs, or listbox-like controls |

## Screen Reader Support

- prefer native HTML over custom ARIA-heavy widgets
- use `aria-live="polite"` for non-urgent updates
- use assertive announcements only for urgent failures
- ensure accessible names match visible labels

## Contrast And Color

- never rely on color alone to convey status
- keep contrast at or above `4.5:1` for normal text
- validate error, focus, and disabled states, not just default text

## Reduced Motion

- respect `prefers-reduced-motion`
- pause auto-rotating content for reduced-motion users
- motion used only for decoration should be removable

## Component Patterns

Use native or accessible primitives for:

- accordion
- dropdown menu
- alerts and notifications
- skip link
- dialogs and sheets

## Dark Mode / Color Scheme Toggle

Support three options: Light, Dark, and System (default).

```css
:root {
  color-scheme: light dark;
}

@media (prefers-color-scheme: dark) {
  :root {
    --text-primary: #f1f1f1;
    --surface-1: #1a1a1a;
    --surface-2: #2a2a2a;
  }
}

[data-theme="dark"] {
  --text-primary: #f1f1f1;
  --surface-1: #1a1a1a;
  --surface-2: #2a2a2a;
}

[data-theme="light"] {
  --text-primary: #111111;
  --surface-1: #ffffff;
  --surface-2: #f5f5f5;
}
```

Dark palette rules:

- maintain contrast ratios at or above `4.5:1` in both schemes
- do not rely on color inversion alone — remap semantic tokens explicitly
- test focus rings and error states in both dark and light schemes
- persist the user's preference to `localStorage` and apply it before first paint to avoid flash

```typescript
const saved = localStorage.getItem('color-scheme') as 'light' | 'dark' | null;
const preferred = saved ?? (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
document.documentElement.dataset.theme = preferred;
```

## Testing

Run both:

- automated checks such as axe, linting, and snapshot-based audits
- manual checks for keyboard, focus, announcements, and zoom/reflow behavior
