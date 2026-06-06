# Pixel Craft Reference

Purpose: load this when Dot must choose a palette, shape clusters, shading rules, or readability checks. It contains craft rules and anti-pattern guidance, not output-format templates.

## Contents

- [Color count theory](#color-count-theory)
- [Palette role system](#palette-role-system)
- [Famous palettes](#famous-palettes)
- [Color theory for pixel art](#color-theory-for-pixel-art)
- [Genre-specific palette recommendations](#genre-specific-palette-recommendations)
- [Dithering patterns](#dithering-patterns)
- [Outline techniques](#outline-techniques)
- [Shading and lighting](#shading-and-lighting)
- [Anti-patterns](#anti-patterns)
- [Anti-aliasing](#anti-aliasing)
- [Pixel cluster rules](#pixel-cluster-rules)
- [Sub-pixel animation](#sub-pixel-animation)
- [Readability](#readability)
- [Palette construction method](#palette-construction-method)
- [Design checklist](#design-checklist)

## Color Count Theory

| Colors | Bits | Historical Platform | Modern Use |
|--------|------|-------------------|------------|
| 2 | 1-bit | Mac 128K, ZX Spectrum | Stamps, silhouettes, minimalist icons |
| 4 | 2-bit | GameBoy, CGA (mode 4) | Retro-style, monochrome themes |
| 8 | 3-bit | CGA (full), early MSX | Simplified sprites, low-res icons |
| 16 | 4-bit | NES, SNES per-tile, EGA | Standard game sprites, most common |
| 32 | 5-bit | Custom | Rich scenes, detailed backgrounds |
| 256 | 8-bit | SNES full, GBA, DOS VGA | Full-color pixel scenes |

## Palette Role System

Every palette needs at minimum 4 functional roles:

| Role | Purpose | Selection Rule |
|------|---------|---------------|
| **Base** | Primary fill color | Mid-tone, defines character identity |
| **Highlight** | Light-facing surfaces | 1-2 steps lighter + slight warm hue shift |
| **Shadow** | Dark-facing surfaces | 1-2 steps darker + slight cool hue shift |
| **Outline** | Edge definition | Darkest value, near-black or darkest hue |

Extended roles (8+ colors): **Mid-tone** (transition), **Accent** (eye-catching detail), **Background** (scene fill), **Secondary** (supporting colors).

---

## Famous Palettes

### DB16 (DawnBringer 16)

```javascript
const DB16 = [
  "#140c1c", "#442434", "#30346d", "#4e4a4e",
  "#854c30", "#346524", "#d04648", "#757161",
  "#597dce", "#d27d2c", "#8595a1", "#6daa2c",
  "#d2aa99", "#6dc2ca", "#dad45e", "#deeed6"
];
```

**Best for:** General-purpose game sprites, balanced warm/cool

### DB32 (DawnBringer 32)

```javascript
const DB32 = [
  "#000000", "#222034", "#45283c", "#663931",
  "#8f563b", "#df7126", "#d9a066", "#eec39a",
  "#fbf236", "#99e550", "#6abe30", "#37946e",
  "#4b692f", "#524b24", "#323c39", "#3f3f74",
  "#306082", "#5b6ee1", "#639bff", "#5fcde4",
  "#cbdbfc", "#ffffff", "#9badb7", "#847e87",
  "#696a6a", "#595652", "#76428a", "#ac3232",
  "#d95763", "#d77bba", "#8f974a", "#8a6f30"
];
```

**Best for:** Detailed scenes, rich environments

### Sweetie 16

```javascript
const SWEETIE_16 = [
  "#1a1c2c", "#5d275d", "#b13e53", "#ef7d57",
  "#ffcd75", "#a7f070", "#38b764", "#257179",
  "#29366f", "#3b5dc9", "#41a6f6", "#73eff7",
  "#f4f4f4", "#94b0c2", "#566c86", "#333c57"
];
```

**Best for:** Modern pixel art, vibrant feel, UI/icons

### PICO-8

```javascript
const PICO8 = [
  "#000000", "#1d2b53", "#7e2553", "#008751",
  "#ab5236", "#5f574f", "#c2c3c7", "#fff1e8",
  "#ff004d", "#ffa300", "#ffec27", "#00e436",
  "#29adff", "#83769c", "#ff77a8", "#ffccaa"
];
// Secret palette (128-143):
const PICO8_SECRET = [
  "#291814", "#111d35", "#422136", "#125359",
  "#742f29", "#49333b", "#a28879", "#f3ef7d",
  "#be1250", "#ff6c24", "#a8e72e", "#00b543",
  "#065ab5", "#754665", "#ff6e59", "#ff9d81"
];
```

**Best for:** Fantasy console style, retro games, game jams

### Endesga 32

```javascript
const ENDESGA_32 = [
  "#be4a2f", "#d77643", "#ead4aa", "#e4a672",
  "#b86f50", "#733e39", "#3e2731", "#a22633",
  "#e43b44", "#f77622", "#feae34", "#fee761",
  "#63c74d", "#3e8948", "#265c42", "#193c3e",
  "#124e89", "#0099db", "#2ce8f5", "#ffffff",
  "#c0cbdc", "#8b9bb4", "#5a6988", "#3a4466",
  "#262b44", "#181425", "#ff0044", "#68386c",
  "#b55088", "#f6757a", "#e8b796", "#c28569"
];
```

**Best for:** Fantasy RPG, warm-toned games

### GameBoy

```javascript
const GAMEBOY = ["#0f380f", "#306230", "#8bac0f", "#9bbc0f"];
const GAMEBOY_ALT = ["#081820", "#346856", "#88c070", "#e0f8d0"];
const GB_POCKET = ["#000000", "#555555", "#aaaaaa", "#ffffff"];
```

### CGA (IBM PC)

```javascript
const CGA_16 = [
  "#000000", "#0000aa", "#00aa00", "#00aaaa",
  "#aa0000", "#aa00aa", "#aa5500", "#aaaaaa",
  "#555555", "#5555ff", "#55ff55", "#55ffff",
  "#ff5555", "#ff55ff", "#ffff55", "#ffffff"
];
const CGA_P1 = ["#000000", "#55ffff", "#ff55ff", "#ffffff"]; // Mode 4 Palette 1
const CGA_P0 = ["#000000", "#55ff55", "#ff5555", "#ffff55"]; // Mode 4 Palette 0
```

### Other Notable Palettes

```javascript
const NYX8 = [
  "#08141e", "#0f2a3f", "#20394f", "#f6d6bd",
  "#c3a38a", "#997577", "#816271", "#4e495f"
];
```

**NES:** 64-color system palette with 4 rows (dark/normal/light/tint). Use [Nestopia palette reference](https://www.nesdev.org/wiki/PPU_palettes) for exact values. Platform supports 25 simultaneous colors (4 BG palettes × 4 + 4 sprite palettes × 3 + 1 shared).

---

## Color Theory for Pixel Art

### Hue Shifting

The most important pixel art color technique. Shift hue (not just value) for shadows and highlights.

```
Shadow direction:    Hue toward cool (blue/purple), Saturation +, Value -
Base:                Original hue
Highlight direction: Hue toward warm (yellow/orange), Saturation -, Value +
```

**Standard increment:** +20° shift per swatch step. **Practical range:** 20°–40° total.

| Base Hue | Shadow Shift | Highlight Shift |
|----------|-------------|-----------------|
| Red | → Purple | → Orange |
| Green | → Teal/Blue | → Yellow |
| Blue | → Purple | → Cyan |
| Yellow | → Green | → White/Cream |
| Brown | → Dark Purple | → Orange/Gold |

### Color Ramp Construction (9-swatch)

```
Swatch 1 (darkest): H - 20°, S = 55%, V = 15%
Swatch 5 (mid):     H      , S = 80%, V = 65%  ← Saturation peak
Swatch 9 (lightest):H + 20°, S = 50%, V = 98%
```

### Saturation Ramps

```
Shadow:    S = 40-70%, V = 10-30%
Midtone:   S = 60-90%, V = 40-60%  ← Saturation peak
Highlight: S = 20-50%, V = 70-90%
```

### Value Stepping

| Palette Size | Steps per Hue |
|-------------|--------------|
| 2-color | 2 |
| 8-color | 3-4 |
| 16-color | 4-5 |
| 32-color | 5-7 |

Use **perceptual spacing** (not linear): `V = 96, 82, 64, 44, 26, 12` not `V = 100, 80, 60, 40, 20`.

### Color Temperature by Scene

| Scene | Shadow Color | Highlight Color |
|-------|-------------|----------------|
| Outdoor daylight | Cool blue-purple | Warm yellow |
| Indoor lantern/fire | Deep blue/teal | Orange/yellow |
| Night | Deep blue-purple | Cool white/blue |
| Underwater | Dark teal | Bright cyan-green |

---

## Genre-Specific Palette Recommendations

| Genre | Recommended Palette | Colors | Rationale |
|-------|-------------------|--------|-----------|
| RPG (Fantasy) | DB32, Endesga 32 | 16-32 | Wide range for characters, terrain, UI |
| Platformer | Sweetie 16, DB16 | 16 | Vibrant, readable at speed |
| Puzzle | PICO-8, Sweetie 16 | 16 | Clear color distinction |
| Horror | Custom dark | 8-16 | Low saturation, narrow value range |
| Sci-fi | Custom neon | 16 | High contrast, cyan/magenta accents |
| Mobile casual | Sweetie 16 | 16 | Friendly, modern feel |
| GameBoy homage | GAMEBOY | 4 | Authentic retro constraint |

---

## Dithering Patterns

### Ordered Dithering (Bayer Matrix)

```
2×2:              4×4:
┌───┬───┐         ┌────┬────┬────┬────┐
│ 0 │ 2 │         │  0 │  8 │  2 │ 10 │
├───┼───┤         ├────┼────┼────┼────┤
│ 3 │ 1 │         │ 12 │  4 │ 14 │  6 │
└───┴───┘         ├────┼────┼────┼────┤
                  │  3 │ 11 │  1 │  9 │
                  ├────┼────┼────┼────┤
                  │ 15 │  7 │ 13 │  5 │
                  └────┴────┴────┴────┘
```

### Implementation

```javascript
const BAYER_2x2 = [[0, 2], [3, 1]];
function ditherPixel(x, y, ratio, colorA, colorB) {
  const threshold = BAYER_2x2[y % 2][x % 2] / 4;
  return ratio > threshold ? colorB : colorA;
}
```

```python
BAYER_4x4 = [
    [0,  8,  2, 10],
    [12, 4, 14,  6],
    [3, 11,  1,  9],
    [15, 7, 13,  5],
]

def dither_region(img, x0, y0, w, h, color_a, color_b, ratio=0.5):
    for y in range(y0, y0 + h):
        for x in range(x0, x0 + w):
            threshold = BAYER_4x4[y % 4][x % 4] / 16
            color = color_b if ratio > threshold else color_a
            img.putpixel((x, y), color)
```

### Floyd-Steinberg (Error Diffusion)

Distributes quantization error to neighbors. More natural gradients than Bayer. **Not recommended for animation sprites** — causes flicker.

```
Error kernel:    [current]  7/16
          3/16    5/16      1/16
```

### Dithering Selection Guide

| Situation | Recommended |
|-----------|------------|
| Retro hardware emulation | Bayer (match hardware) |
| Photo palette reduction | Floyd-Steinberg |
| Simple gradient | Checkerboard or Bayer 2×2 |
| Animated sprites | Bayer only (no error diffusion) |
| Metal/stone texture | Sparse dithering |

### Pattern Types

| Pattern | Visual | Best For |
|---------|--------|----------|
| 50% checker | `XOXOXO` | Sharp transitions |
| 25% sparse | `X...X.` | Subtle gradients |
| Vertical lines | Column alternation | Fabric, rain |
| Diagonal | Staggered | Soft shadows |

---

## Outline Techniques

### Standard Outline (1px solid)

1px border in darkest palette color. Clear separation from any background.

### Selective Outline (Sel-out)

Outline color varies by adjacent fill and light direction:
- **Light-facing edge:** lighter outline or omit
- **Shadow-facing edge:** darkest outline
- Outline color = darkened version of adjacent fill (not pure black)

```javascript
// Sel-out examples:
// Red area:   base #cc2200 → outline #660011
// Yellow area: base #ffdd00 → outline #886600
// Skin area:   base #ffaa88 → outline #884422
```

### Double Outline

Two layers: inner (darkest fill) + outer (pure black). Use for boss characters, UI icons. **Warning:** Consumes 2px — not for small sprites.

### No Outline (Outlineless)

For backgrounds, very small sprites, soft/organic shapes, high-res (64×64+). Requires higher color contrast and 1px inner shadow for shape definition.

---

## Shading and Lighting

### Pillow Shading — ANTI-PATTERN

Center brightest, edges darken uniformly. Looks like internal illumination. **Fix:** Use directional light source.

### Light Source Convention

Standard: **top-left** (10 o'clock). Keep consistent across ALL sprites.

```
  ↘ Light direction
┌─────────┐
│ H H H . │  H = highlight
│ H B B S │  B = base
│ . B B S │  S = shadow
│ . S S S │
└─────────┘
```

### Cel Shading

Flat color planes with sharp boundaries. 3-5 steps: Highlight → Base → Shadow → Deep Shadow → (Rim Light).

**Rules:** Boundaries are 1px sharp lines, follow form contours, keep 1px gap from outline.

### Form Rendering by Size

| Size | Colors | Approach |
|------|--------|----------|
| 8×8 | 2-3 | Silhouette only, minimal shading |
| 16×16 | 3-4 | 1-level shadow + highlight |
| 32×32 | 4-6 | Full cel-shading, dithering for mid-tones |
| 64×64+ | 6-12 | Fine details, rim light, subsurface |

### Highlight Placement

| Surface | Highlight Position |
|---------|-------------------|
| Flat top | Top 1-2 rows |
| Curved | Top-left quadrant |
| Cylindrical | Left 1-2 columns |
| Metallic | Concentrated point |
| Matte | Diffused area |

---

## Anti-Patterns

### Orphan Pixels

Isolated single pixels without same-color neighbors. Causes noisy silhouette, flickers in animation.
**Fix:** Merge into 2+ pixel clusters or remove. **Exception:** Intentional sparkle/eye highlights.

### Jaggies

Staircase artifacts on diagonal lines. **Fix:** Keep line segment lengths consistent. For curves: vary progressively (3-2-1-1-2-3).

```
Bad (inconsistent):    Good (consistent 2:1):
. . X X                . . X X
. X . .                . X X .
X X . .                X X . .
```

### Banding

Shading forms parallel bands instead of following form. **Fix:** Make boundaries follow shape contours. Interlock clusters.

### Noise

Too much pixel variation. **Fix:** Ensure 2-3px minimum clusters. Prioritize silhouette over detail.

### Too Many Colors

**Fix:** Consolidate and reuse colors across parts. Limited palette forces cohesion.

---

## Anti-Aliasing

### Automated AA — FORBIDDEN

| Problem | Consequence |
|---------|------------|
| Blurry at 1x scale | Loses crispness |
| Halo at Nx scale | Grey fringe |
| Palette violation | Uncontrolled mid-tones |

Prevention: `image-rendering: pixelated` (CSS), `ctx.imageSmoothingEnabled = false` (Canvas), `shape-rendering="crispEdges"` (SVG).

### Manual AA — Selective Use Only

Place intermediate-value pixels at staircase ends on curves (32px+ sprites). Never on internal boundaries or small sprites.

---

## Pixel Cluster Rules

- **2×1 minimum** — avoid orphan pixels (except eyes/sparkle)
- **Staircase rule** — consistent step width for diagonals

## Sub-Pixel Animation

Movement smaller than 1 pixel via color alternation:
- **Value cycling:** ±1 palette step per frame (shimmer)
- **Edge add/remove:** +1px advancing side, -1px trailing → apparent 0.5px/frame

**Use for:** Idle breathing, floating, fire/water ripples.

---

## Readability

### Silhouette Test

Fill sprite with single color → can you identify it from shape alone? If not, redesign silhouette first.

### Size Design Rules

| Size | Colors | Key Rules |
|------|--------|-----------|
| 8×8 | 2-3 + transparent | Shape recognition = silhouette only |
| 16×16 | 4-6 + transparent | 1 shading level, face = eyes 2-4px + mouth 2px |
| 32×32+ | 8-16 | Full shading, internal detail |

### Contrast Requirements

| Comparison | Minimum Ratio |
|-----------|--------------|
| Sprite vs background | 4.5:1 |
| Outline vs background | 7:1 ideal |
| Highlight vs shadow | 3:1 |

### Character Proportions

| Size | Head Width | Proportion |
|------|-----------|------------|
| 8×8 | 4px max | Stick figure |
| 16×16 | 5-7px | Chibi 2:1 to 3:1 |
| 32×32 | 8-10px | Chibi to semi-real |
| 64×64 | 16-20px | Realistic 7:1 possible |

**Rule:** Realistic proportions below 48×48 don't work. Use chibi for small sprites.

---

## Palette Construction Method

1. **Choose color count** based on project scope
2. **Define value ramp** — perceptually even lightness
3. **Assign hue families** — typically 3-5 groups
4. **Apply hue shifting** — warm highlights, cool shadows
5. **Test readability** — distinguishable at 1x scale
6. **Validate contrast** — outline vs base ≥ 3:1

### Palette Templates

```javascript
const PALETTE = {
  name: "my-palette",
  colors: { outline: "#1a1c2c", shadow: "#5d275d", base: "#b13e53", highlight: "#ef7d57", accent: "#ffcd75" },
  array: ["#1a1c2c", "#5d275d", "#b13e53", "#ef7d57", "#ffcd75"],
};
```

```python
PALETTE = {
    "name": "my-palette",
    "colors": [
        (0x1a, 0x1c, 0x2c),  # outline
        (0x5d, 0x27, 0x5d),  # shadow
        (0xb1, 0x3e, 0x53),  # base
        (0xef, 0x7d, 0x57),  # highlight
        (0xff, 0xcd, 0x75),  # accent
    ],
}
```

---

## Design Checklist

### Palette
- [ ] Darkest/lightest contrast ≥ 4.5:1 (WCAG AA)
- [ ] Value steps perceptually even
- [ ] Hue shifting set (warm highlights, cool shadows)
- [ ] Accent colors ≤ 15% of total
- [ ] Skin tones 3+ steps minimum
- [ ] Color vision deficiency considered

### Technique
- [ ] No orphan pixels (except intentional)
- [ ] No jaggies (consistent staircase steps)
- [ ] No banding (form-following boundaries)
- [ ] No pillow shading (directional light source)
- [ ] Anti-aliasing disabled in all output
- [ ] Silhouette test passed

**Source:** [Lospec Palette List](https://lospec.com/palette-list) · [Pixel Art Tutorial by Cure](https://pixeljoint.com/forum/forum_posts.asp?TID=11299) · [Slynyrd Pixel Tutorials](https://www.slynyrd.com/blog/category/Pixel+Art) · [NES Dev Wiki Palettes](https://www.nesdev.org/wiki/PPU_palettes)
