# Motion Accessibility Anti-Patterns

Purpose: Use this file when motion must respect WCAG, reduced-motion settings, and vestibular safety.

## Contents
- `MA-01` to `MA-07`
- Reduced-motion implementation model
- Animation-type fallback matrix

## Anti-Patterns

| ID | Failure | Required Fix |
|----|---------|--------------|
| `MA-01` | No `prefers-reduced-motion` support | Add reduced-motion handling to all non-trivial motion |
| `MA-02` | Autoplay animation longer than `5s` with no control | Provide pause, stop, or hide |
| `MA-03` | Flashing `>3` times per second | Reduce or remove immediately |
| `MA-04` | Motion-only state communication | Add text, color, icon, or structure |
| `MA-05` | Delete all motion in reduced mode | Keep functional feedback with gentler alternatives |
| `MA-06` | Rely only on OS-level preference | Support OS preference and optionally app-level control |
| `MA-07` | Force parallax or large scroll-coupled motion | Disable in reduced mode |

## Reduced-Motion Strategy

| Level | Behavior |
|-------|----------|
| `0` | No non-essential motion; instant state change |
| `1` | Minimal motion: fade only, usually `<=100ms` |
| `2` | Full motion for `no-preference` users |

Default to functional clarity. Motion is enhancement, not dependency.

## Animation-Type Fallbacks

| Animation Type | Reduced-Motion Fallback |
|----------------|-------------------------|
| Page transition slide | Fade or instant swap |
| Hover movement | Color or shadow change only |
| Loading spinner | Static progress or text if possible |
| Scroll reveal | Content visible without animation |
| Parallax | Disabled |
| Modal entry | Fade or instant display |
| Drag feedback | Keep if functionally required |
| Success / error feedback | Color + icon + text |

## Minimal Pattern

```css
.element {
  transition: none;
}

@media (prefers-reduced-motion: no-preference) {
  .element {
    transition: transform 200ms var(--ease-out), opacity 200ms var(--ease-out);
  }
}

@media (prefers-reduced-motion: reduce) {
  .element {
    transition: opacity 120ms ease-out;
  }
}

## MA-08: Scroll-Driven Animations Without Reduced-Motion

| ID | Failure | Required Fix |
|----|---------|--------------|
| `MA-08` | Scroll-driven animations without reduced-motion fallback | Wrap in `@supports` inside `@media (prefers-reduced-motion: no-preference)` |

### Safe Pattern

```css
/* Default: always visible */
.reveal { opacity: 1; }

@media (prefers-reduced-motion: no-preference) {
  @supports (animation-timeline: view()) {
    .reveal {
      opacity: 0;
      animation: fadeIn linear both;
      animation-timeline: view();
      animation-range: entry 0% entry 60%;
    }
  }
}
```
```
