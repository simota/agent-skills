# Theme & Token Reference

Purpose: Ship a single SVG asset that re-colors for light, dark, and brand themes without duplication. Use `currentColor` as the default; escalate to CSS custom properties when an icon needs more than one tunable color; coordinate multi-color tokens with Muse.

## Scope Boundary

- **ink `theme`**: `currentColor` strategy, CSS custom property injection into SVG paths, dark-mode variant authoring, multi-color icon token layering, sprite-symbol theme coordination.
- **Muse (elsewhere)**: the design-token source of truth — semantic names (`--icon-primary`, `--status-success`), palette scales, dark-mode mapping, cross-platform token output.
- **Palette (elsewhere)**: usability and contrast audit — flags when a chosen token pair fails WCAG.
- **Artisan (elsewhere)**: React/Vue theme provider that sets the CSS custom properties at runtime.

If the question is "what color value does `--icon-primary` resolve to?" → Muse. If it is "how does this SVG consume it?" → `theme`.

## Token-System Landscape (2026-05)

- **DTCG Design Tokens Format Module 2025.10** — first stable spec, published **2025-10-28** by the W3C Design Tokens Community Group. Vendor-neutral JSON, MIME `application/design-tokens+json`, extensions `.tokens` or `.tokens.json`. Supports color (with modern color spaces), dimension, duration, motion, gradient, border, shadow, typography token types and a new resolver module. Adopted by Figma, Penpot, Sketch, Framer, Knapsack, Supernova, zeroheight; reference impls in Style Dictionary, Tokens Studio, Terrazzo.
- **Style Dictionary v5** — DTCG 2025.10 alignment in progress (color/border/shadow done, gradient in progress; dimension token type accepts object value while remaining string-compatible).
- **Tokens Studio for Figma** — 2025 updates: auto-sync of scoping/syntax to Figma Variables, server-side token resolution for OAuth projects, gradient export as Figma styles.
- **CSS `color-mix()` + OKLCH** — Chrome 111+, Edge 111+, Firefox 113+, Safari 15.4+; ~95% global support per caniuse (2025-Q3). Safe to use as the default `color-mix` interpolation space in 2026.

## `currentColor` vs Hardcoded Fill

| Need | Approach |
|------|----------|
| Monochrome icon that follows text color | `fill="currentColor"` or `stroke="currentColor"` — parent sets `color:` |
| Two colors, both theme-dependent | CSS custom properties (`var(--icon-primary)`, `var(--icon-accent)`) |
| Brand-locked logo | Hardcoded hex — document that it is intentional |
| Decorative with gradient | `<linearGradient>` with stops bound to CSS vars |

Default every new icon to `currentColor` for fill or stroke. Only escalate when a second tunable color is needed.

## Workflow

1. **Count tunable colors** in the icon: 1 → `currentColor`; 2+ → CSS custom properties; 0 → hardcoded is fine.
2. **Name the tokens** with Muse's semantic vocabulary (`--icon-primary`, not `--blue-500`).
3. **Author** using inline SVG (external `.svg` via `<img>` cannot inherit CSS variables).
4. **Add dark-mode mapping** at the token layer, not the SVG layer.
5. **Test** by toggling `:root { color-scheme: light | dark }` and theme class.

## `currentColor` Pattern

```xml
<!-- Icon inherits parent's color. Single source of truth. -->
<svg viewBox="0 0 24 24" width="24" height="24" role="img" aria-label="Search">
  <path fill="none" stroke="currentColor" stroke-width="2"
        d="M11 4a7 7 0 1 0 0 14 7 7 0 0 0 0-14zM20 20l-4-4"/>
</svg>
```

```css
/* Consumer controls color through the cascade. */
.btn--primary   { color: var(--text-on-primary); }
.btn--secondary { color: var(--text-on-surface); }
```

One asset, many contexts, zero duplication.

## CSS Custom Property Injection

```xml
<!-- Multi-color icon: primary stroke + accent fill, both themed. -->
<svg viewBox="0 0 24 24" class="icon-status-ok" role="img" aria-label="Success">
  <circle cx="12" cy="12" r="10" fill="var(--icon-bg, currentColor)"/>
  <path d="M7 12l3 3 7-7" fill="none" stroke="var(--icon-fg, #fff)"
        stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
</svg>
```

```css
:root {
  --icon-bg: var(--status-success);
  --icon-fg: var(--text-on-success);
}
```

Always provide a fallback in `var(--x, fallback)` — guarantees the icon renders even outside the theme provider (e.g., in Storybook isolation or email).

## Dark-Mode Variants

Two routes:

```css
/* A. Token-level (preferred) — Muse owns the mapping, SVG stays identical */
:root            { --icon-primary: #111; }
[data-theme=dark]{ --icon-primary: #eee; }
@media (prefers-color-scheme: dark) {
  :root:not([data-theme]) { --icon-primary: #eee; }
}

/* B. Media-query inside <style> inline in the SVG (for standalone <img src>) */
```

```xml
<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
  <style>
    path { fill: #111; }
    @media (prefers-color-scheme: dark) { path { fill: #eee; } }
  </style>
  <path d="M12 2l10 18H2z"/>
</svg>
```

Route B only for icons shipped as portable standalone `.svg` files. Inside an app, always prefer route A.

## Multi-Color Icon Token Layering

Layer tokens by role, not hex:

| Layer | Token example | When |
|-------|--------------|------|
| Background | `--icon-bg` | Badge backdrop, filled shapes |
| Foreground | `--icon-fg` | Primary path, glyph |
| Accent | `--icon-accent` | Highlights, dots, state markers |
| Outline | `--icon-outline` | Border stroke distinct from fg |

Keep layer count ≤ 3 per icon. More than three color roles usually means the icon is an illustration — use `illustration` Recipe instead and lean on `<linearGradient>` plus tokens.

## Sprite-Theme Coordination

When an icon set ships as a `<symbol>` sprite and uses CSS variables, each `<use>` instance inherits the caller's context:

```html
<svg style="display:none"><symbol id="i-ok" viewBox="0 0 24 24">
  <circle cx="12" cy="12" r="10" fill="var(--icon-bg)"/>
  <path d="M7 12l3 3 7-7" stroke="var(--icon-fg)"/>
</symbol></svg>

<!-- Different themes, same symbol. -->
<span style="--icon-bg:green; --icon-fg:white"><svg><use href="#i-ok"/></svg></span>
<span style="--icon-bg:red;   --icon-fg:white"><svg><use href="#i-ok"/></svg></span>
```

Avoid `fill="currentColor"` inside a `<symbol>` if the surrounding context toggles `color` for text — it will drift. Name a dedicated token.

## Anti-Patterns

- Hardcoding hex values in a generic UI icon — makes dark-mode support impossible without re-exporting.
- Inventing new token names inside the SVG that do not exist in Muse's token registry — breaks hand-off and theme consistency.
- Applying dark-mode via a second duplicate SVG file — doubles the bundle and drifts over time.
- Using `color-scheme: light dark` without also providing the variable mappings — the icon renders in an indeterminate state.
- Setting fill on the root `<svg>` when paths override it individually — unreachable style, confusing diff.
- Relying on `currentColor` for a multi-color icon — the second color will collide with text color.

## Handoff

**From Muse:** token names, semantic meaning, light/dark/high-contrast values, contrast-ratio target per pairing. Prefer **DTCG 2025.10** JSON format (`*.tokens.json`) for cross-tool exchange.
**To Artisan:** which CSS variables the component must set, default fallbacks, theme switching contract (class or `data-*`). Note Style Dictionary v5 + Tokens Studio output paths.
**To Palette:** color-pairing list for WCAG 1.4.11 non-text-contrast audit (≥ 3:1 for meaningful icons).
**To Showcase:** light + dark + high-contrast story variants per icon so visual regression catches theme drift.
