# Token Mapping (Figma Variables → W3C DTCG)

Reference for Frame's `tokens` recipe. Map Figma Variables to W3C Design Tokens Community Group (DTCG) format with mode/theme support, alias chains, and Display P3 / Oklch color preservation.

> Output target: W3C DTCG Module 2025.10 (stable). Aligns with Tokens Studio, Style Dictionary, and Figma Code Connect.

---

## 1. Discovery Workflow

```
search_design_system --includeVariables   → list Variable Collections
get_variable_defs                          → fetch Variable values, modes, aliases
```

Map Figma concepts:
- **Variable Collection** → DTCG token group (`color`, `spacing`, `typography`)
- **Mode** → DTCG `$value` mode (e.g., `light`, `dark`, `brand-a`)
- **Variable Reference** → DTCG alias (`{color.brand.primary}`)
- **Variable Scope** (Color / Number / Boolean / String) → DTCG `$type`

---

## 2. Three-Tier Token Architecture

### Primitive
Raw values, no semantics. Foundation layer.
```json
{
  "color": {
    "neutral": {
      "50":  { "$type": "color", "$value": "#fafafa" },
      "500": { "$type": "color", "$value": "#737373" },
      "950": { "$type": "color", "$value": "#0d0d12" }
    },
    "indigo": {
      "500": { "$type": "color", "$value": "#6366f1" }
    }
  }
}
```

### Semantic
Role-based, references primitives.
```json
{
  "color": {
    "bg": { "$type": "color", "$value": "{color.neutral.50}" },
    "fg": { "$type": "color", "$value": "{color.neutral.950}" },
    "brand": { "$type": "color", "$value": "{color.indigo.500}" }
  }
}
```

### Component
Per-component, references semantic.
```json
{
  "button": {
    "primary": {
      "background": { "$type": "color", "$value": "{color.brand}" },
      "foreground": { "$type": "color", "$value": "{color.fg-on-brand}" }
    }
  }
}
```

---

## 3. Mode / Theme Support

### Multi-mode in DTCG (proposed `$value` extension)
```json
{
  "color": {
    "bg": {
      "$type": "color",
      "$value": {
        "light": "{color.neutral.50}",
        "dark":  "{color.neutral.950}"
      }
    }
  }
}
```

### Multi-dimension (mode × brand)
```json
{
  "color": {
    "brand": {
      "$type": "color",
      "$value": {
        "brand-a-light": "#6366f1",
        "brand-a-dark":  "#818cf8",
        "brand-b-light": "#16a34a",
        "brand-b-dark":  "#4ade80"
      }
    }
  }
}
```

Map Figma Mode names to DTCG keys exactly. Document mode dimensions in collection-level metadata:
```json
{
  "$description": "Modes: { theme: light|dark, brand: a|b }"
}
```

---

## 4. Alias Resolution

### Alias chain
```
button.primary.background
  → color.brand
    → color.indigo.500
      → "#6366f1"
```

### Output: include both alias and resolved value
```json
{
  "button": {
    "primary": {
      "background": {
        "$type": "color",
        "$value": "{color.brand}",
        "$resolved": "#6366f1",
        "$resolvedChain": ["{color.brand}", "{color.indigo.500}", "#6366f1"]
      }
    }
  }
}
```

This allows downstream consumers (Style Dictionary, Code Connect) to use either reference or value.

---

## 5. Color Preservation (Display P3 / Oklch)

Figma supports wide-gamut colors via Display P3 since 2023.
DTCG `$type: color` accepts hex (sRGB) by default; for P3/Oklch, use:

```json
{
  "color": {
    "brand-vivid": {
      "$type": "color",
      "$value": {
        "colorSpace": "display-p3",
        "components": [0.45, 0.30, 0.95]
      }
    }
  }
}
```

CSS output:
```css
--color-brand-vivid: color(display-p3 0.45 0.30 0.95);
/* Fallback: */
--color-brand-vivid-fallback: #6240f0;
```

For Oklch (perceptually uniform):
```css
--color-brand-perceptual: oklch(60% 0.2 270);
```

Always provide sRGB fallback for browsers without P3 support (~5% of users).

---

## 6. Type Mapping

| Figma Variable Type | DTCG `$type` | Example value |
|---|---|---|
| Color | `color` | `"#6366f1"` or `{ colorSpace: "display-p3", components: [...] }` |
| Number (px) | `dimension` | `{ value: 16, unit: "px" }` |
| Number (rem) | `dimension` | `{ value: 1, unit: "rem" }` |
| Number (raw) | `number` | `1.5` |
| String | `string` | `"Inter, sans-serif"` |
| Boolean | `boolean` | `true` |
| Composite (typography) | `typography` | `{ fontFamily, fontSize, lineHeight, fontWeight }` |
| Composite (shadow) | `shadow` | `{ offsetX, offsetY, blur, spread, color }` |

---

## 7. Output Format

### File: `tokens.json` (single file or split per collection)
```json
{
  "$schema": "https://schemas.dtcg.org/tokens/2025-10/tokens.schema.json",
  "$metadata": {
    "tokenSetOrder": ["primitive", "semantic", "component"]
  },
  "primitive": { ... },
  "semantic": { ... },
  "component": { ... }
}
```

### Split-file alternative
- `tokens/primitive.json`
- `tokens/semantic.json`
- `tokens/component/button.json`
- `tokens/component/input.json`

Tokens Studio plugin and Style Dictionary both consume this layout.

---

## 8. Common Pitfalls

| Pitfall | Avoidance |
|---|---|
| Skipping primitive layer (semantic refs raw values) | Always extract primitive layer; semantic always aliases primitive |
| Mode names with spaces (`Light Mode`) | Normalize to kebab-case (`light`) |
| Display P3 colors flattened to sRGB | Detect P3 in Figma, preserve `colorSpace` field |
| Composite typography exported as separate tokens | Use DTCG `$type: typography` composite |
| Alias chain not resolved → consumer can't use raw value | Include `$resolved` in output |
| Mode dimensions not documented | `$description` at collection level |
| Variable not bound to any property → still exported | Filter by usage: only export bound variables (or mark as orphan) |
| Theme name collision across collections | Namespace by collection name |
| Forgetting fallback for Display P3 | Always emit sRGB fallback |
| Alpha channel in hex (`#rrggbbaa`) misread as 8-char hex | Detect alpha; emit as `rgba()` or DTCG color object |

---

## 9. Decision Walkthrough Template

```
File: ____________
Collections detected: ____
Modes per collection: ____ (e.g., {theme: light|dark})

Token tier mapping:
  Primitive count:  ____
  Semantic count:   ____
  Component count:  ____

Wide-gamut colors (P3/Oklch): ____ count
sRGB fallbacks: ✓ generated

Output:
  □ Single tokens.json
  □ Split per-collection files
  □ Alias chain resolved + included
  □ Mode dimensions documented in $description
  □ DTCG 2025.10 schema reference
  □ CSS custom property output (optional)
  □ Style Dictionary config (optional)

Handoff:
  □ Muse for token system maintenance
  □ Artisan for component implementation using tokens
```

---

## 10. References
- W3C DTCG 2025.10 spec
- Tokens Studio plugin documentation
- Style Dictionary documentation
- Figma Variables (Modes, Scopes, Aliases) docs
- CSS Color Module Level 4 (Display P3, Oklch)
