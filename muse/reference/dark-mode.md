# Dark Mode

Purpose: Use this reference when implementing dark mode, choosing a theme strategy, adapting colors and elevation, or verifying accessibility in dark surfaces.

## Contents

- Checklist
- Implementation strategies
- Color adaptation rules
- Theme toggle implementation
- Verification report format

## Dark Mode Checklist

### Colors

- Contrast meets WCAG AA: `4.5:1` for normal text, `3:1` for large text.
- Avoid pure `#000000`; prefer dark grays such as `#121212+`.
- Avoid pure white body text on dark surfaces and pure black body text on light surfaces unless explicitly justified and re-verified.
- Adjust accent colors if glare appears.
- Keep semantic roles stable across themes.

### Images And Icons

- Provide dark-appropriate logo or image treatment when light assets bloom.
- Ensure icons remain legible on dark surfaces.
- Avoid white-background imagery that glows excessively.

### Components

- Verify surfaces, borders, dividers, and overlays at each elevation.
- Ensure focus rings are visible in both themes.
- Verify empty, loading, error, success, and disabled states.

### Edge Cases

- Form controls
- Charts and data visualization
- Scrollbars, code blocks, syntax highlighting
- Modal backdrops and layered surfaces

## Dark Mode Implementation Strategies

### Strategy 1: CSS Custom Properties

Recommended for most projects.

```css
:root {
  --color-bg-surface: #ffffff;
  --color-text-primary: #111827;
}

[data-theme="dark"] {
  --color-bg-surface: #121212;
  --color-text-primary: #f3f4f6;
}
```

### Strategy 2: `prefers-color-scheme`

Best when the product follows the system setting without a custom toggle.

```css
@media (prefers-color-scheme: dark) {
  :root {
    --color-bg-surface: #121212;
    --color-text-primary: #f3f4f6;
  }
}
```

### Strategy 3: Tailwind Dark Mode

```html
<p class="text-gray-900 dark:text-gray-100">Content</p>
```

Use when the project already relies on Tailwind’s `dark:` variant.

### Strategy 4: `color-scheme`

Use to align browser-native controls with the active theme.

```css
html[data-theme="dark"] {
  color-scheme: dark;
}
```

## Color Adaptation Rules

### Lightness Inversion Table

| Light mode role | Dark mode counterpart | Notes |
|-----------------|----------------------|-------|
| Background | Dark surface | keep content readable first |
| Gray-100 surface | Gray-700+ surface | maintain hierarchy |
| Light border | Dark border | keep separation subtle |
| Muted text | Higher-lightness muted text | maintain contrast |

### Saturation And Glare

- If an accent color feels harsh on dark surfaces, reduce saturation by `10-20%` and raise lightness slightly.
- Preserve semantic meaning before visual novelty.

### Shadow Adaptation

- Shadows in dark mode often need lower opacity and stronger separation with surface layers.
- Use shadow tokens or surface elevation tokens, not hardcoded shadow values.

### Elevation In Dark Mode

- Express hierarchy through surface lightness progression, not through brighter shadows alone.
- Example: `Surface-0 (darkest) -> Surface-3 (lightest)` for layered components.

## Theme Toggle Implementation

Provide `System / Light / Dark` whenever the product allows explicit choice.

### React Example

```tsx
function ThemeToggle() {
  const setTheme = (theme: "system" | "light" | "dark") => {
    document.documentElement.dataset.theme = theme;
  };

  return null;
}
```

### System Preference Listener

```ts
window.matchMedia("(prefers-color-scheme: dark)");
```

Use it only if the selected mode is `system`.

## Dark Mode Verification Report Format

```md
### Dark Mode Verification: [Component]
- Status:
- Checklist passed:
- Strategy:
- Text contrast:
- Large text contrast:
- Focus visibility:
- Surface hierarchy:
- Image/icon adaptation:
- Edge cases checked:
- Issues:
- Recommendation:
```

## `light-dark()` for Dark Mode Tokens

The CSS `light-dark()` function (Baseline 2024) simplifies dark mode token definitions to a single declaration:

```css
:root {
  color-scheme: light dark;

  --bg-surface: light-dark(oklch(0.98 0.005 260), oklch(0.15 0.005 260));
  --bg-elevated: light-dark(oklch(1.0 0 0), oklch(0.2 0.005 260));
  --text-primary: light-dark(oklch(0.2 0.01 260), oklch(0.9 0.01 260));
  --text-secondary: light-dark(oklch(0.4 0.01 260), oklch(0.7 0.01 260));
  --border-default: light-dark(oklch(0.85 0.005 260), oklch(0.3 0.005 260));
}
```

### Rules

- Requires `color-scheme: light dark` on `:root` — without it, `light-dark()` always returns the light value.
- Use for **simple light/dark pairs**. For multi-theme systems (3+ themes, brand variants), use DTCG modes with `.resolver.json`.
- Combine with `color-mix()` for derived states: `color-mix(in oklch, light-dark(#333, #ccc), transparent 50%)`.
- **Migration path**: Replace `@media (prefers-color-scheme: dark)` duplication with `light-dark()` when supporting only light/dark.

## oklch Semantic Tokens for Dark Mode

oklch provides perceptually uniform lightness, making light/dark mode token pairs more predictable:

```css
:root {
  --color-bg-surface: oklch(0.98 0.005 260);
  --color-text-primary: oklch(0.2 0.01 260);
}

@media (prefers-color-scheme: dark) {
  :root {
    --color-bg-surface: oklch(0.15 0.01 260);
    --color-text-primary: oklch(0.95 0.005 260);
  }
}
```

Rules:
- Keep the same hue angle across light/dark pairs for brand consistency.
- Reduce chroma by 10-20% in dark mode to prevent glare on dark backgrounds.
- Lightness ≥ 0.8 guarantees readable black text; lightness ≤ 0.3 guarantees readable white text.
