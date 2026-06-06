# Design Token System

Purpose: Use this reference when defining token categories, naming rules, typography and spacing scales, audit logic, or framework integration.

## 2026 Format Baseline: DTCG Stable + AI-Consumed Tokens

By 2026 the W3C **Design Tokens Community Group (DTCG) specification reached its first stable version** (announced 2025-10-28). Reference implementations now ship in **Style Dictionary**, **Tokens Studio**, **Terrazzo**, **Penpot**, **Figma**, **Sketch**, **Framer**, **Knapsack**, **Supernova**, and **zeroheight**. Two implications for new token systems:

1. **Default to the DTCG JSON format** for the source of truth — `$value`, `$type`, `$description`, `$extensions` keys with the `$`-prefix discipline. Migrate legacy bespoke token JSON to DTCG when the tool chain supports it; do not invent a fourth format.
2. **Tokens are now an AI-consumption surface.** Claude / Cursor / Copilot / Windsurf / Antigravity all write a meaningful share of frontend code in 2026, and they hallucinate brand colors / spacing / type choices unless given the token file. Treat the published token JSON as the source of truth that ships alongside `llms.txt` (see `quill/reference/readme-templates.md`) for AI agents — a stale or undocumented token file is the #1 reason AI-generated UI drifts from brand.

| Tool layer | Recommended in 2026 |
|------------|----------------------|
| Source of truth | DTCG JSON (committed to repo) |
| Figma authoring | **Figma Variables** for simple projects, **Tokens Studio** for GitHub sync / multi-platform export / CI integration |
| Transform pipeline | **Style Dictionary** (v4+ DTCG-native) or **Terrazzo** |
| Platform outputs | CSS custom properties, JS / TS constants, iOS / Android resources, plus the raw DTCG JSON for AI consumers |
| AI consumer surface | DTCG JSON + a short `tokens.md` describing intent (semantic layer naming, dark-mode mapping) for retrieval pipelines |

## Contents

- Token categories
- Naming convention
- Definition process
- File structure
- Typography scale
- Spacing system
- Design token audit
- Modern token integration
- Code standards

## Token Categories

| Layer     | Purpose                                | Examples                                       |
| --------- | -------------------------------------- | ---------------------------------------------- |
| Primitive | Raw values and neutral building blocks | `blue-500`, `gray-100`, `space-4`, `shadow-md` |
| Semantic  | Context-aware aliases                  | `bg-primary`, `text-secondary`, `border-focus` |
| Component | Component-specific composition         | `button-radius`, `card-shadow`, `input-border` |

Rules:

- Primitive tokens hold raw values only.
- Semantic tokens express purpose, not color names.
- Component tokens may depend on semantic tokens, not raw primitives.

## Naming Convention

| Layer           | Pattern                                     | Example                      |
| --------------- | ------------------------------------------- | ---------------------------- |
| Primitive color | `{family}-{scale}`                          | `blue-500`                   |
| Semantic color  | `{role}-{variant}`                          | `bg-primary`, `text-muted`   |
| Component token | `{component}-{property}`                    | `button-padding-x`           |
| CSS variable    | `--{category}-{property}-{variant}-{state}` | `--color-bg-primary-default` |

Rules:

- Prefer purpose-based naming over value-based naming.
- Keep names short enough to scan quickly.
- Reserve dark/light branching for tokens that visually change across modes.
- Attach lifecycle status comments when a token is not yet stable, for example `@status: propose|adopt|stable|deprecated|frozen`.

## Token Definition Process

1. Confirm the value belongs to a reusable system, not a one-off fix.
2. Choose the correct layer: primitive, semantic, or component.
3. Name it by intent.
4. Add it to token files and documentation.
5. Replace hardcoded references and verify light/dark behavior.

## Token File Structure

```text
tokens/
  primitives/
    colors.css
    spacing.css
    typography.css
    shadows.css
    radius.css
  semantic/
    colors.css
    surfaces.css
    feedback.css
  components/
    button.css
    card.css
    input.css
```

Rules:

- Keep primitives and semantic tokens globally available.
- Scope component tokens closer to the component when possible.
- Use the lifecycle status defined in [token-lifecycle.md](~/.claude/skills/muse/reference/token-lifecycle.md) for unstable or deprecated tokens.

## Typography Scale

Default ratio: Major Third (`1.25`)

```css
:root {
  --text-xs: 0.75rem; /* 12px */
  --text-sm: 0.875rem; /* 14px - secondary text, metadata */
  --text-base: 1rem; /* 16px - body */
  --text-lg: 1.125rem; /* 18px - lead paragraphs */
  --text-xl: 1.25rem; /* 20px - h5 */
  --text-2xl: 1.5rem; /* 24px - h4 */
  --text-3xl: 1.875rem; /* 30px - h3 */
  --text-4xl: 2.25rem; /* 36px - h2 */
  --text-5xl: 3rem; /* 48px - h1 */
}
```

Usage guide:

| Token         | Typical use                                       |
| ------------- | ------------------------------------------------- |
| `--text-sm`   | metadata, helper text                             |
| `--text-base` | default body, keep mobile body text at `min 16px` |
| `--text-lg`   | lead text                                         |
| `--text-2xl`  | section headers                                   |
| `--text-5xl`  | hero headlines                                    |

Responsive guidance:

- Mobile: compress the upper end of the scale.
- Desktop (`>= 1024px`): full scale is allowed.

## Spacing System

Base system: `8px` grid with `4px` support for tight pairings.

```css
:root {
  --space-1: 0.25rem; /* 4px */
  --space-2: 0.5rem; /* 8px */
  --space-3: 0.75rem; /* 12px */
  --space-4: 1rem; /* 16px */
  --space-5: 1.25rem; /* 20px */
  --space-6: 1.5rem; /* 24px */
  --space-8: 2rem; /* 32px */
  --space-10: 2.5rem; /* 40px */
  --space-12: 3rem; /* 48px */
  --space-16: 4rem; /* 64px */
}
```

Usage guide:

| Use case       | Range     | Tokens                |
| -------------- | --------- | --------------------- |
| Icon to text   | `4-8px`   | `space-1`, `space-2`  |
| Button padding | `8-16px`  | `space-2`, `space-4`  |
| Card padding   | `16-24px` | `space-4`, `space-6`  |
| Section gap    | `24-48px` | `space-6`, `space-12` |
| Page margins   | `16-64px` | `space-4`, `space-16` |

Responsive guidance:

- Mobile: page margin `16px`, section gap `24px`
- Tablet: page margin `24px`, section gap `32px`
- Desktop: page margin `32-64px`, section gap `48px`

Grid verification:

- Valid examples: `4px`, `8px`, `12px`, `16px`, `20px`, `24px`, `32px`, `40px`, `48px`, `64px`
- Suspicious values: `5px`, `7px`, `9px`, `10px`, `11px`, `13px`, `14px`, `15px`, `17px`, `18px`, `19px`
- Exceptions: `1px` borders and dividers, `2px` micro-adjustments only when visually necessary.

## Design Token Audit

### Detection Patterns

- Raw `HEX` or `RGB` values in components
- Primitive tokens used directly where semantic tokens should exist
- Spacing values outside the `4px/8px` system
- Shadow, radius, or z-index magic numbers
- Inconsistent dark-mode token mapping
- Single-use tokens and duplicated token values

### Audit Report Format

```md
### Design Token Audit Report: [Component/File]

- Coverage:
- Categories:
  - Hardcoded:
  - Tokenized:
  - Coverage:
- Critical Issues:
- Warnings:
- Off-grid spacing:
- Raw color usage:
- Dark mode status:
- Recommended token changes:
- Risks / follow-up:
```

Quick commands:

```sh
grep -r "var(--{old-token})" src/
git diff src/styles/tokens.css
```

## Modern Token Integration

### W3C DTCG Format

```json
{
  "color": {
    "bg-primary": {
      "$value": "{color.primitive.gray.100}",
      "$type": "color",
      "$description": "Primary application background"
    }
  }
}
```

### Tailwind v4

```css
@theme {
  --color-bg-primary: var(--color-neutral-0);
  --color-bg-secondary: var(--color-neutral-100);
  --spacing-4: var(--space-4);
}
```

### Panda CSS

```ts
semanticTokens: {
  colors: {
    bg: {
      value: { base: "{colors.white}", _dark: "{colors.gray.900}" }
    }
  }
}
```

### Open Props

- Use it as a baseline only if it aligns with the project vocabulary.
- Rename or wrap props with semantic aliases before product use.

### CSS-in-JS

- Prefer central token imports over ad hoc constants.
- Do not bypass tokens inside component files.

## Typography Selection Rules

When defining typography tokens, the display typeface must be intentionally chosen. See [typography-selection-guide.md](~/.claude/skills/muse/reference/typography-selection-guide.md) for the full selection process.

**Banned display fonts:** Inter, Roboto, Arial — these signal "generic AI template" and provide zero brand differentiation. System fonts are acceptable for body text only.

## Token Role Mapping

Map semantic color tokens to these standard roles for consistent cross-project usage:

| Role | Token | Purpose |
|------|-------|---------|
| Background | `--color-bg-*` | Page and section backgrounds |
| Surface | `--color-surface-*` | Raised containers, cards, panels |
| Primary text | `--color-text-primary` | Headings, body text, high-emphasis content |
| Muted text | `--color-text-muted` | Secondary information, metadata, helper text |
| Accent | `--color-accent-*` | CTAs, links, active states, key focal points |

Rules:
- Every project must define all 5 roles before component work begins.
- Accent tokens should be used sparingly — only on interactive or focal elements.
- Surface tokens create visual hierarchy through subtle background shifts, not borders.
- Muted text must still meet WCAG AA contrast ratios (4.5:1 for normal text).

## Code Standards

### Good Muse Code

```css
.card {
  background: var(--color-bg-surface);
  color: var(--color-text-primary);
  padding: var(--space-6);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-md);
}
```

### Bad Muse Code

```css
.card {
  background: #ffffff;
  color: #111827;
  padding: 18px;
  border-radius: 7px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}
```

## DTCG 2025.10 Standard

The Design Tokens Community Group published the first stable specification (2025.10) with support from 20+ organizations (Adobe, Google, Microsoft, Figma, Shopify).

File extension: `.tokens` or `.tokens.json`
MIME type: `application/design-tokens+json`

### Token Types

Standard types: `color`, `dimension`, `font-family`, `font-weight`, `duration`, `cubic-bezier`, `number`.
Composite types: `shadow`, `border`, `transition`, `gradient`, `typography`.

### $value / $type / $description Notation

```json
{
  "color": {
    "$type": "color",
    "brand-primary": {
      "$value": {
        "colorSpace": "oklch",
        "components": [0.65, 0.2, 260]
      },
      "$description": "Brand primary color"
    }
  }
}
```

### Alias (Reference) Syntax

```json
{
  "semantic": {
    "bg-primary": {
      "$type": "color",
      "$value": "{color.brand-primary}"
    }
  }
}
```

## oklch Color Space for Design Tokens

Browser support: Chrome 111+, Safari 15.4+, Firefox 113+. Global coverage 92%+ (2025 Q2).

Primitive color tokens in oklch:
```css
:root {
  --color-blue-500: oklch(0.55 0.2 260);
  --color-blue-400: oklch(0.65 0.18 260);
  --color-blue-600: oklch(0.45 0.22 260);
}
```

Relative color syntax for hover states (CSS Colors 5):
```css
.button:hover {
  background: oklch(from var(--color-brand-primary) calc(l + 0.1) c h);
}
```

Wide-gamut (P3) support:
```css
@media (color-gamut: p3) {
  :root {
    --color-brand: oklch(0.65 0.28 260);
  }
}
```

## Container Queries and Token Integration

Container size queries enable responsive token switching at the component level:
```css
.card-container {
  container-type: inline-size;
  container-name: card;
}

@container card (min-width: 400px) {
  .card {
    --card-padding: var(--space-8);
    --card-font-size: var(--text-lg);
  }
}

@container card (max-width: 399px) {
  .card {
    --card-padding: var(--space-4);
    --card-font-size: var(--text-base);
  }
}
```

Browser support (2025): size queries fully supported; style queries in progress.

## CSS Functions for Token Systems

Modern CSS functions enable runtime token derivation — reducing static token definitions.

### `color-mix()` (Baseline 2023)

Derive hover, active, and disabled states from a single primitive:

```css
:root {
  --color-primary: oklch(0.55 0.2 260);
  --color-primary-hover: color-mix(in oklch, var(--color-primary), white 15%);
  --color-primary-active: color-mix(in oklch, var(--color-primary), black 10%);
  --color-primary-disabled: color-mix(in oklch, var(--color-primary), transparent 50%);
}
```

**Rule**: Define 1 primitive → derive states via `color-mix()`. Eliminates `*-hover`, `*-active`, `*-disabled` token bloat.

### `light-dark()` (Baseline 2024)

Single-line dark mode token switching:

```css
:root { color-scheme: light dark; }
:root {
  --text-primary: light-dark(oklch(0.2 0.01 260), oklch(0.9 0.01 260));
  --bg-surface: light-dark(oklch(0.98 0.005 260), oklch(0.15 0.005 260));
}
```

**Rule**: Use for simple light/dark pairs. For multi-theme (brand/density), stick with DTCG modes.

### Relative Color Syntax

Generate entire palettes from a single base:

```css
:root {
  --base: oklch(0.55 0.2 260);
  --lightest: oklch(from var(--base) 0.95 calc(c * 0.3) h);
  --light: oklch(from var(--base) 0.8 calc(c * 0.5) h);
  --dark: oklch(from var(--base) 0.35 calc(c * 0.8) h);
}
```

### CSS `if()` (Emerging — Chrome Canary)

Conditional token resolution based on custom properties:

```css
.component {
  padding: if(style(--density: compact): 4px 8px; else: 8px 16px);
  font-size: if(style(--density: compact): 0.8125rem; else: 1rem);
}
```

**Rule**: Progressive enhancement only. Always provide a non-`if()` fallback via `@supports`.

## AI-Readable Token Architecture

Tokens evolve from storing **values** to storing **intent** — enabling AI agents to generate, adapt, and validate UI:

```json
{
  "$type": "color",
  "$value": "#3B82F6",
  "$intent": "trust-building action color",
  "$usage": ["primary CTA", "navigation highlights"],
  "$constraints": {
    "contrast": "WCAG AA on white",
    "never-on": ["warning surfaces", "destructive actions"]
  }
}
```

**Rule**: Add `$intent`, `$usage`, `$constraints` fields to semantic tokens. AI tools (Figma Make, v0, Stitch) consume these to generate design-system-compliant output. Keep primitive tokens value-only.

## COLRv1 Color Fonts

Modern color font format with gradients, compositing, and variable font axis compatibility:

```css
.brand-heading {
  font-family: 'Plakato Color', sans-serif;
  font-palette: --brand-palette;
}
@font-palette-values --brand-palette {
  font-family: 'Plakato Color';
  override-colors: 0 var(--color-primary), 1 var(--color-secondary);
}
```

- **Rule**: Use `font-palette` for runtime color switching. Token-driven palette overrides via `override-colors`.
- Supported in all major browsers. Compact and crisp vs SVG-in-OpenType.

## Variable Everything: Unified Responsive Token System

The convergence of Variable Fonts + Relative Color Syntax + `clamp()` + `@property` eliminates breakpoint-based design steps:

### `@property` for Animatable Custom Properties

```css
@property --hue {
  syntax: '<angle>';
  initial-value: 240deg;
  inherits: true;
}
:root {
  --brand: oklch(0.65 0.2 var(--hue));
  --brand-light: oklch(from var(--brand) calc(l + 0.2) c h);
  --space-unit: clamp(0.5rem, 1vw, 1rem);
}
```

- `@property` makes custom properties animatable (gradients, hues, positions).
- Combined with `clamp()`, spacing and typography become continuous rather than stepped.
- **Rule**: Define `@property` for any token that needs animation or interpolation.

### Generative Token Architecture

Tokens that derive themselves through rules rather than static definitions:

| Strategy | Formula | Example |
|----------|---------|---------|
| Typographic scale | `base × ratio^level` | 1rem × 1.25^3 = 1.953rem |
| Color palette | `base hue + rotation` | `oklch(0.7 0.15 calc(var(--hue) + 120))` |
| Spacing scale | `base × fibonacci` | 4 → 8 → 12 → 16 → 24 → 32 → 48 |
| Shadow depth | `elevation × multiplier` | `calc(var(--elevation) * 4px) blur, calc(var(--elevation) * 0.05) opacity` |

**Rule**: Prefer generative formulas over exhaustive static token lists. One formula replaces dozens of static values.

### Sustainability-Aware Token Mode

```json
{
  "mode": "eco",
  "rules": {
    "background": "prefer darkest variant (OLED 42% energy reduction)",
    "animation": "prefers-reduced-motion: reduce",
    "images": "WebP/AVIF only, max 200KB",
    "fonts": "system font stack, zero transfer cost"
  }
}
```

## Multi-Brand Token Architecture

| Dimension | Examples |
|-----------|----------|
| Theme | light / dark |
| Brand | brand-a / brand-b |
| Platform | web / ios / android |
| Density | compact / default / comfortable |
| Accessibility | standard / high-contrast |

Directory structure:
```
tokens/
  core/                    # shared primitives
    colors.tokens.json
    spacing.tokens.json
  brands/
    brand-a/
      primitives.tokens.json
      semantic.tokens.json
    brand-b/
      primitives.tokens.json
      semantic.tokens.json
  themes/
    light.tokens.json
    dark.tokens.json
  components/
```

Style Dictionary multi-brand build:
```js
const brands = ['brand-a', 'brand-b'];
for (const brand of brands) {
  const sd = new StyleDictionary({
    source: [
      'tokens/core/**/*.tokens.json',
      `tokens/brands/${brand}/**/*.tokens.json`,
    ],
    platforms: {
      css: {
        transformGroup: 'css',
        buildPath: `dist/${brand}/`,
        files: [{ destination: 'tokens.css', format: 'css/variables' }]
      }
    }
  });
  await sd.buildAllPlatforms();
}
```
