# Dark Mode Derivation

Reference for Pixel's `dark` recipe. Derive a dark-mode variant from a light-mode mockup. Semantic tokens, contrast preservation, and elevation via brightness — not solid black.

> All dark-mode values derived from a light mockup are LOW confidence. Designer review required before production.

---

## 1. Token Architecture (Semantic Layer)

### Three-tier system
1. **Primitive tokens**: raw colors (`--neutral-50` through `--neutral-950`, `--brand-500`, etc.)
2. **Semantic tokens**: role-based (`--color-bg`, `--color-fg`, `--color-surface-1`, etc.)
3. **Component tokens**: per-component (`--card-bg`, `--input-border`)

Dark mode swaps **semantic tokens only**, never primitives. Component tokens reference semantic tokens, so they auto-update.

### Standard semantic token set
```css
:root {
  /* Backgrounds */
  --color-bg: #ffffff;              /* page background */
  --color-surface-1: #fafafa;       /* card, panel */
  --color-surface-2: #f5f5f5;       /* nested card, input */
  --color-surface-3: #ebebeb;       /* deepest nested */
  --color-overlay: rgba(0,0,0,0.5); /* modal backdrop */

  /* Foregrounds */
  --color-fg: #1a1a1a;              /* primary text */
  --color-fg-muted: #555555;        /* secondary text */
  --color-fg-subtle: #888888;       /* tertiary, captions */
  --color-fg-on-brand: #ffffff;     /* text on brand color */

  /* Borders */
  --color-border: #e5e5e5;
  --color-border-strong: #cccccc;

  /* Brand & semantic */
  --color-brand: #4f46e5;
  --color-brand-hover: #4338ca;
  --color-success: #16a34a;
  --color-warning: #d97706;
  --color-danger: #dc2626;
  --color-info: #0284c7;

  /* Elevation (shadows) */
  --shadow-1: 0 1px 2px rgba(0,0,0,0.05);
  --shadow-2: 0 4px 6px rgba(0,0,0,0.07);
  --shadow-3: 0 10px 15px rgba(0,0,0,0.10);
}

[data-theme="dark"] {
  --color-bg: #0d0d12;              /* never #000 */
  --color-surface-1: #16161c;
  --color-surface-2: #1f1f28;
  --color-surface-3: #2a2a36;
  --color-overlay: rgba(0,0,0,0.7);

  --color-fg: #f5f5f7;              /* never #fff */
  --color-fg-muted: #b0b0bb;
  --color-fg-subtle: #7d7d8a;
  --color-fg-on-brand: #ffffff;

  --color-border: #2e2e3a;
  --color-border-strong: #45455a;

  --color-brand: #6366f1;            /* lighten for contrast */
  --color-brand-hover: #818cf8;
  --color-success: #4ade80;
  --color-warning: #fbbf24;
  --color-danger: #f87171;
  --color-info: #38bdf8;

  /* Elevation: lighten background, not darker shadows */
  --shadow-1: 0 1px 2px rgba(0,0,0,0.5);
  --shadow-2: 0 4px 6px rgba(0,0,0,0.6);
  --shadow-3: 0 10px 15px rgba(0,0,0,0.7);
}
```

---

## 2. Why Not Pure Black

| Issue with `#000` background | Solution |
|---|---|
| OLED black means surface elevation is invisible (no shadow contrast) | Use `#0d0d12` base; surfaces lighten progressively |
| High eye strain at typical display brightness | Use `#0d0d12` to `#1a1a24` range |
| Loss of perceived depth (everything floats on void) | Layered surfaces: 1 lighter than bg, 2 lighter than 1, etc. |
| Poor anti-aliasing (fonts shimmer on pure black) | Slight blue/violet tint reduces shimmer |

### Recommended dark base palette
```css
--neutral-950: #0d0d12;  /* page bg */
--neutral-900: #16161c;  /* surface 1 */
--neutral-850: #1f1f28;  /* surface 2 */
--neutral-800: #2a2a36;  /* surface 3 */
--neutral-700: #3d3d4d;  /* border-strong */
--neutral-600: #585866;  /* placeholder text */
--neutral-500: #7d7d8a;  /* fg-subtle */
--neutral-400: #b0b0bb;  /* fg-muted */
--neutral-200: #e1e1e8;  /* alt fg */
--neutral-100: #f5f5f7;  /* fg primary */
```

---

## 3. Elevation via Brightness (Not Shadow)

In light mode: lower z = lower brightness (subtle shadow).
In dark mode: **higher z = higher brightness** (Material 3 elevation principle).

| Z-level | Light mode | Dark mode |
|---|---|---|
| 0 (page) | `#fff` | `#0d0d12` |
| 1 (card) | `#fff` + shadow-1 | `#16161c` (lighter than bg) |
| 2 (raised) | `#fff` + shadow-2 | `#1f1f28` |
| 3 (modal) | `#fff` + shadow-3 | `#2a2a36` + shadow |

Shadows still exist in dark mode but are darker (negative space) — main depth cue is the brightness step.

---

## 4. Contrast Preservation (WCAG)

### Requirements
- **WCAG AA Normal text**: ≥ 4.5:1
- **WCAG AA Large text** (≥ 18pt or 14pt bold): ≥ 3:1
- **WCAG AA Non-text** (UI components, icons): ≥ 3:1
- **WCAG AAA Normal text**: ≥ 7:1 (recommended for body)

### Validation tool
- Check every fg/bg combination via `Lch` in CSS or contrast tools
- Common dark-mode trap: `#cccccc` text on `#1a1a1a` = 9.5:1 ✓
- Common dark-mode trap: `#888888` text on `#1a1a1a` = 4.4:1 ✗ (below AA)

### Programmatic check (Playwright + axe)
```js
import AxeBuilder from '@axe-core/playwright';
const results = await new AxeBuilder({ page })
  .withTags(['wcag2aa', 'wcag2aaa'])
  .analyze();
const colorContrast = results.violations.filter(v => v.id === 'color-contrast');
console.log(colorContrast);
```

### Brand color adjustment
Brand colors often need lightening in dark mode:
- Light: `--color-brand: #4f46e5` (indigo-600) on `#fff` → 7.4:1 ✓
- Dark: `--color-brand: #6366f1` (indigo-500) on `#0d0d12` → 6.8:1 ✓
- If lightening drops contrast on hover, lighten further or use lighter variant

---

## 5. Image & Media Handling

### Photographs
- Generally do not modify; reduce brightness slightly via `filter: brightness(0.85)` only if blinding
- Avoid `filter: invert()` — turns photos surreal

### Logos / Brand marks
- Provide both light + dark versions: `<img src="logo-dark.svg">` swapped via theme
- Or use `currentColor` SVG that inherits foreground

### Illustrations / Icons
- SVGs with `currentColor` auto-update with `--color-fg`
- Colored illustrations may need dark-mode variants

### Code blocks
- Always use a dark theme regardless of UI mode (or theme-matched)
- Light theme on dark UI is high contrast (acceptable but jarring)

---

## 6. System Toggle Pattern

### `prefers-color-scheme` media query (system follows OS)
```css
:root { /* light defaults */ }

@media (prefers-color-scheme: dark) {
  :root { /* dark overrides */ }
}
```

### Manual toggle with `[data-theme]` attribute
```css
:root { /* light defaults */ }

[data-theme="dark"] { /* dark overrides */ }
```

```html
<html data-theme="light">
  <button onclick="document.documentElement.dataset.theme = 'dark'">Dark</button>
</html>
```

### Combined: system + manual override
```css
:root { /* light defaults */ }

@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    /* dark overrides — applies if system is dark AND user hasn't forced light */
  }
}

[data-theme="dark"] {
  /* dark overrides — explicit user choice overrides system */
}
```

### Persistence (avoid FOUC)
```html
<!-- Inline script BEFORE first paint -->
<script>
  const saved = localStorage.getItem('theme');
  if (saved) document.documentElement.dataset.theme = saved;
</script>
```

### `color-scheme` for native form elements
```css
:root { color-scheme: light; }
[data-theme="dark"] { color-scheme: dark; }
```
This styles native scrollbars, form inputs, and date pickers correctly.

---

## 7. Common Pitfalls

| Pitfall | Avoidance |
|---|---|
| Pure `#000` bg destroys depth | Use `#0d0d12-#1a1a24` base |
| Pure `#fff` text strains eyes on dark bg | Use `#f5f5f7` (off-white) |
| Same brand color on dark — low contrast | Lighten brand by 1-2 shades for dark |
| Swapping primitives instead of semantic tokens | Only flip `--color-*` semantic vars |
| Missing `color-scheme` → ugly native form fields | Add `color-scheme: dark` |
| FOUC on initial load | Pre-paint inline script |
| Photos look washed out | Don't filter; trust the image |
| Forgetting hover state contrast | Validate hover, focus, active in dark too |
| Borders disappear (too dark on dark bg) | Use `--color-border` light enough (≥ 3:1 against surrounding) |
| No `prefers-color-scheme` support | Always query both system pref + manual override |
| Hardcoded shadow `rgba(0,0,0,0.1)` doesn't show on dark | Increase opacity to `0.5-0.7` for dark |

---

## 8. Decision Walkthrough Template

```
Source mockup: light mode (assumed)
Derivation source: light tokens

Token tier check:
  □ Semantic tokens defined (--color-bg, --color-fg, etc.)
  □ Component tokens reference semantic (not primitives)
  □ Primitive scale extends to dark range

Dark palette generation:
  Background: ____ (never #000)
  Surface 1-3 progression (lightening): ____ → ____ → ____
  Foreground: ____ (never #fff)
  Brand: ____ (lightened from light variant by ___ shades)

Contrast validation:
  □ All body text ≥ 4.5:1 AA
  □ All large text ≥ 3:1 AA
  □ All UI components ≥ 3:1 AA
  □ axe-core check passes

System integration:
  □ prefers-color-scheme media query
  □ [data-theme="dark"] manual override
  □ color-scheme CSS property set
  □ Pre-paint inline script (no FOUC)
  □ localStorage persistence

Asset handling:
  □ Logo: light + dark variants OR currentColor SVG
  □ Icons: currentColor SVG
  □ Photos: untouched (or minimal brightness filter)
  □ Code blocks: dark theme always or theme-matched

Designer review request:
  □ Surface progression brightness steps
  □ Brand color lightening
  □ Border visibility
  □ Hover/focus states in dark
```

---

## 9. References
- Material Design 3: Elevation in dark mode
- Apple HIG: Dark Mode (color philosophy)
- WCAG 2.1: 1.4.3 Contrast (Minimum), 1.4.6 Contrast (Enhanced), 1.4.11 Non-text Contrast
- web.dev: `color-scheme` and `prefers-color-scheme`
