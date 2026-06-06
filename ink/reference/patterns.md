# Ink Design Patterns

## Icon Library Landscape (2026-05)

| Library | Version (2026-05) | Style | Grid | Stroke | License | Notes |
|---------|-------------------|-------|------|--------|---------|-------|
| Lucide | 1.16.x | outline | 24×24 | 2px | ISC | 1600+ icons, Feather fork, official React/Vue/Svelte/Solid/Preact/Angular/Flutter wrappers |
| Heroicons | 2.2.0 (2024-11) | outline / solid / mini / micro | 24/24/20/**16** | 1.5px outline | MIT | 4 styles incl. **Micro 16×16** (v2.1); React 19 support |
| Phosphor Icons | 2.1 | thin/light/regular/bold/fill/duotone | 256×256 | tunable | MIT | 6 weights; +268 icons in 2.1 |
| Tabler Icons | 3.44.x | outline + filled | 24×24 | 2px (1.5/1 variants) | MIT | 6,146 icons (2026-05) |
| Material Symbols | Variable Font | outlined/rounded/sharp × FILL/wght/GRAD/opsz | 20-48 | axis-controlled | Apache 2.0 | 4 axes (FILL 0-100, wght 100-700, GRAD -50 to 200, opsz 20-48) |
| Font Awesome | 7 (2025-07) | classic/sharp/duotone/sharp-duotone + new Jelly/Whiteboard/Notdog | 16×16 base | tunable | Free MIT + Pro | 4,500+ new icons in v7; Icon Wizard mix-and-match |
| Iconify | aggregator (2026) | unified API; SVG+CSS components for React/SolidJS/Svelte/Vue | varies | varies | per-source | ~300k icons, 200+ icon sets; CSS variable theming (2026-04) |
| Remix Icon | 4.x | outline + filled | 24×24 | 2px | Apache 2.0 | 3,000+ icons |

**Rule**: prefer Lucide or Heroicons for stroke consistency in product UI; Material Symbols Variable Font for axis-controlled responsive icons; Iconify for cross-library aggregation in dashboards. **Do not use icon fonts (glyph-based)** — they require extra ARIA work for accessibility and have been superseded by SVG sprite + `<symbol>` in all modern stacks (78% of major sites use SVG icons as of 2025). Source: [playground.halfaccessible.com](https://playground.halfaccessible.com/blog/svg-icons-guide-web-development) / [iconify.design/news/2026](https://iconify.design/news/2026.html)

## SVG Icon Construction

### Basic Icon Template (24x24)

```svg
<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"
     fill="none" stroke="currentColor" stroke-width="2"
     stroke-linecap="round" stroke-linejoin="round"
     role="img" aria-label="Icon description">
  <title>Icon Name</title>
  <!-- paths here -->
</svg>
```

### Grid System

```
┌──────────────────────┐
│  ┌──────────────────┐ │ ← 2px padding
│  │                  │ │
│  │   Drawing Area   │ │ ← 20x20 active area
│  │                  │ │
│  └──────────────────┘ │
└──────────────────────┘
         24x24 total
```

Rules:
- Keep strokes within the padding boundary
- Align to whole pixels (no sub-pixel rendering)
- Optical center may differ from geometric center

## Icon Style Patterns

### Outline Style

```svg
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
     stroke-linecap="round" stroke-linejoin="round">
  <circle cx="12" cy="12" r="10"/>
  <line x1="12" y1="8" x2="12" y2="16"/>
  <line x1="8" y1="12" x2="16" y2="12"/>
</svg>
```

### Filled Style

```svg
<svg viewBox="0 0 24 24" fill="currentColor">
  <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 15v-4H7l5-7v4h4l-5 7z"/>
</svg>
```

### Duotone Style

```svg
<svg viewBox="0 0 24 24">
  <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2z"
        fill="currentColor" opacity="0.2"/>
  <path d="M11 7v4H7l5 7v-4h4l-5-7z"
        fill="currentColor"/>
</svg>
```

## SVG Sprite System

### Symbol Definition

```svg
<svg xmlns="http://www.w3.org/2000/svg" style="display:none">
  <symbol id="icon-home" viewBox="0 0 24 24">
    <path d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-4 0a1 1 0 01-1-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 01-1 1"/>
  </symbol>
  <symbol id="icon-search" viewBox="0 0 24 24">
    <circle cx="11" cy="11" r="8"/>
    <line x1="21" y1="21" x2="16.65" y2="16.65"/>
  </symbol>
</svg>
```

### Symbol Usage

```html
<svg class="icon" width="24" height="24">
  <use href="#icon-home"/>
</svg>
```

## Optimization Rules (SVGO)

| Rule | Description |
|------|-------------|
| Remove editor metadata | Strip Illustrator/Figma metadata |
| Normalize viewBox | Ensure viewBox matches content bounds |
| Merge paths | Combine compatible paths |
| Round coordinates | Round to 2 decimal places |
| Remove empty groups | Clean up `<g>` wrappers |
| Remove hidden elements | Strip `display:none` elements |
| Convert shapes to paths | Optionally for smaller output |

```bash
# SVGO v4 (2024+): removeViewBox and removeTitle are disabled by default for
# scalability and accessibility. Node.js >= 16 required.
# Customize precision per use case: 1 for simple icons, 2-3 for complex illustrations.
npx svgo input.svg -o output.svg --config='{"plugins":[{"name":"preset-default","params":{"overrides":{"convertPathData":{"floatPrecision":1}}}}]}'
```

## Animated SVG Patterns

### CSS Animation

```svg
<svg viewBox="0 0 24 24">
  <style>
    .spin { animation: rotate 1s linear infinite; transform-origin: center; }
    @keyframes rotate { to { transform: rotate(360deg); } }
  </style>
  <circle class="spin" cx="12" cy="12" r="10" fill="none"
          stroke="currentColor" stroke-width="2"
          stroke-dasharray="50" stroke-dashoffset="10"/>
</svg>
```

### Hover Interaction

```css
.icon-button svg {
  transition: transform 0.2s ease, color 0.2s ease;
}
.icon-button:hover svg {
  transform: scale(1.1);
  color: var(--accent);
}
```

## Accessibility Checklist

| Requirement | Implementation |
|-------------|---------------|
| Screen reader label | `aria-label` or `<title>` element |
| Decorative icons | `aria-hidden="true"` |
| Focus indicators | Visible focus ring on interactive icons |
| Color contrast | 3:1 minimum against background |
| Touch target | 44x44px minimum for interactive icons |

## Variable Font Icons

Use Variable Fonts (e.g., Google Material Symbols) for responsive, themeable icons:

```css
.icon {
  font-family: 'Material Symbols Outlined';
  font-variation-settings:
    'FILL' 0,    /* 0=outlined, 1=filled */
    'wght' 400,  /* 100-700 */
    'GRAD' 0,    /* -25 to 200 */
    'opsz' 24;   /* 20, 24, 40, 48 */
  font-size: 1.5em; /* Scales with text */
}

/* Responsive: heavier weight at small sizes */
@container (max-width: 320px) {
  .icon { font-variation-settings: 'wght' 500, 'opsz' 20; }
}
```

**Rule**: Prefer Variable Font icons for UI icon systems where dynamic weight/size is needed. Prefer custom SVG for brand-specific or illustrative icons.

## `color-mix()` Icon Theming

Derive icon states from semantic tokens without extra token definitions:

```css
.icon-button {
  color: var(--icon-primary);
}
.icon-button:hover {
  color: color-mix(in oklch, var(--icon-primary), white 20%);
}
.icon-button:disabled {
  color: color-mix(in oklch, var(--icon-primary), transparent 50%);
}
```

## SVG × Modern CSS Animation Integration

### View Transitions for Icon State Changes

```css
.icon-toggle {
  view-transition-name: icon-state;
}
::view-transition-old(icon-state) { animation: fade-out 0.2s; }
::view-transition-new(icon-state) { animation: fade-in 0.2s; }
```

### Scroll-Driven SVG Animation

```css
.hero-illustration path {
  animation: draw-path linear both;
  animation-timeline: view();
  animation-range: entry 0% cover 50%;
  stroke-dasharray: 1000;
  stroke-dashoffset: 1000;
}
@keyframes draw-path { to { stroke-dashoffset: 0; } }
```

### `@starting-style` for SVG Enter Animation

```css
.icon-appear {
  opacity: 1;
  transform: scale(1);
  transition: opacity 0.3s, transform 0.3s;
}
@starting-style {
  .icon-appear { opacity: 0; transform: scale(0.8); }
}
```

## Mesh Gradients & Noise Textures (SVG)

Generate organic textures using SVG filters — no image assets needed:

```html
<svg width="0" height="0">
  <filter id="grain">
    <feTurbulence type="fractalNoise" baseFrequency="0.65" numOctaves="3" stitchTiles="stitch"/>
    <feColorMatrix type="saturate" values="0"/>
  </filter>
</svg>
```

```css
.grainy-gradient {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  position: relative;
}
.grainy-gradient::after {
  content: '';
  position: absolute;
  inset: 0;
  filter: url(#grain);
  opacity: 0.15;
  mix-blend-mode: overlay;
}
```

**Tooling**: fffuel.co (gggrain/nnnoise) for Figma/SVG export. Adds analog/print-like texture to flat digital gradients.

## Aurora / Holographic SVG Effects

Iridescent color shifts using layered OKLCH gradients:

```css
.holo-card {
  background: linear-gradient(125deg,
    oklch(0.8 0.2 0) 0%, oklch(0.7 0.2 90) 25%,
    oklch(0.8 0.2 180) 50%, oklch(0.7 0.2 270) 75%,
    oklch(0.8 0.2 360) 100%);
  background-size: 200% 200%;
  animation: holo-shift 6s ease infinite;
}
@keyframes holo-shift {
  0%, 100% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
}
```

**Use**: Premium card effects, NFT displays, portfolio hero backgrounds. Combine with `mix-blend-mode: screen` for light refraction.

## CSS Paint API (Generative Patterns)

Houdini Paint Worklets for procedural SVG-like patterns — no assets, CSS-customizable:

```js
// register: CSS.paintWorklet.addModule('dots.js')
class Dots {
  static get inputProperties() { return ['--dot-color', '--dot-count']; }
  paint(ctx, geom, props) {
    ctx.fillStyle = props.get('--dot-color').toString();
    for (let i = 0; i < parseInt(props.get('--dot-count')); i++) {
      ctx.beginPath();
      ctx.arc(Math.random() * geom.width, Math.random() * geom.height, 3, 0, Math.PI * 2);
      ctx.fill();
    }
  }
}
registerPaint('dots', Dots);
```

```css
.generative-bg { --dot-color: #6366f1; --dot-count: 50; background: paint(dots); }
```

**Rule**: Chromium-only. Progressive enhancement — fallback to static gradient. Ideal for decorative backgrounds.

## React Component Pattern

```tsx
interface IconProps extends React.SVGProps<SVGSVGElement> {
  size?: number;
  label?: string;
}

export const IconHome: React.FC<IconProps> = ({
  size = 24,
  label = "Home",
  ...props
}) => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    width={size}
    height={size}
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    strokeWidth={2}
    strokeLinecap="round"
    strokeLinejoin="round"
    role="img"
    aria-label={label}
    {...props}
  >
    <title>{label}</title>
    <path d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-4 0a1 1 0 01-1-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 01-1 1"/>
  </svg>
);
```
