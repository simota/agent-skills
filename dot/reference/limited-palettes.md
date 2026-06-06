# Limited Palettes Reference

Purpose: Author pixel art with deliberately constrained color palettes — emulating classic hardware (NES / Game Boy / PICO-8 / CGA / Apple II) and modern indie sub-palettes. Cover palette selection, per-sprite limits, dithering, color-cycling, and Lospec-aligned validation.

## Scope Boundary

- **dot `palette`**: Palette systems for pixel art (this document).
- **dot `animation` / `tilesheet` (elsewhere)**: Frames + tile layout assume a palette is chosen.
- **Muse (elsewhere)**: Modern design tokens (different domain).
- **Vision (elsewhere)**: Brand color direction.
- **Ink (elsewhere)**: SVG / vector color systems.

## Why Limit the Palette

- **Aesthetic identity**: NES looks like NES because the palette is tight.
- **Cognitive constraint**: Forces stronger value design over color crutches.
- **Memory budget**: Hardware-faithful retro projects need it.
- **Cohesion**: Shared palette across sprites = visual unity.
- **LLM / AI generation**: Constrained palette removes a degree of freedom = better consistency.

## Canonical Hardware Palettes

### NES (Nintendo Entertainment System)

- **System palette**: 54 visible colors (out of 64 in PPU index) — deeply researched FBX / Smooth / Wiki variants
- **Per-sprite limit**: 4 colors (1 transparent + 3 visible) selected from one of 4 sub-palettes
- **Background tile limit**: 4 colors per 16×16 attribute block
- **Total on screen**: up to 25 unique colors at once
- **Resolution**: 256×240
- **Famous palette**: FBX (most accurate emulation)

```
Sprite sub-palette example: (transparent, dark-skin, mid-skin, hair-black)
```

### Game Boy (DMG)

- **Palette**: 4 shades of grey / green-grey
  - `#0F380F` (darkest)
  - `#306230`
  - `#8BAC0F`
  - `#9BBC0F` (lightest)
- **Per-sprite**: 3 visible + 1 transparent
- **Resolution**: 160×144

Game Boy Color extended this to 32k color RGB but retained 4-shades-per-tile structure.

### PICO-8 (modern fantasy console)

- **Palette**: 16 fixed colors
  ```
  black, dark-blue, dark-purple, dark-green,
  brown, dark-grey, light-grey, white,
  red, orange, yellow, green, blue, lavender, pink, peach
  ```
- **Resolution**: 128×128
- **No per-sprite limit** within the 16
- Palette swap via `pal()` function for mood / damage / depth

### CGA (IBM PC, 1981)

- **Mode 4**: 4 colors per mode, 2 selectable palettes
  - Palette 0: black, green, red, brown
  - Palette 1: black, cyan, magenta, white (most-used)
- **Resolution**: 320×200
- Iconic ugly-beautiful aesthetic

### Apple II hi-res

- **6 colors**: black, white, green, violet, orange, blue
- Pixel position determines hue (interlace artifact)
- 280×192

### Atari 2600 / VCS

- **128-color** palette, **2 colors per sprite line** (per scanline manipulation expands this)
- Notorious "racing the beam" constraints

### EGA (1984)

- **64-color palette**, 16 simultaneous
- 320×200 / 640×350

### ZX Spectrum

- **15 colors** (2 brightness × 7 hues + black)
- **2 colors per 8×8 attribute block** — "attribute clash" iconic limitation
- 256×192

## Modern Designed Sub-Palettes

| Palette | Colors | Use case |
|---------|--------|----------|
| **DB16** | 16 | Dawnbringer's all-purpose; warm + cool balanced |
| **DB32** | 32 | Extended; richer skin / foliage |
| **PICO-8** | 16 | Fantasy console + community standard |
| **AAP-64** | 64 | Adigun Polack — broad scenic |
| **Endesga 32** | 32 | Punchy; modern indie |
| **Sweetie 16** | 16 | GrafxKid; pleasant pastel |
| **NA16** | 16 | Nauris Amatnieks; balanced earth |
| **Resurrect 64** | 64 | Kerrie Lake; warm + atmospheric |

Browse: lospec.com/palette-list

## Per-Sprite Limit Discipline

Even with 16-color global palettes, restrict to **4-6 colors per sprite** to maintain readability:

- 1 transparent
- 1 darkest (outline / shadow)
- 1-2 mid-tones (form)
- 1 highlight

This forces clear value structure. PICO-8 generation patterns work because most sprites use ≤6 of the 16.

## Dithering

Dithering creates intermediate values from limited colors via patterned mixing:

| Pattern | Density | Use |
|---------|---------|-----|
| Bayer 2×2 | 25 / 50 / 75% | Subtle gradients, sky |
| Bayer 4×4 | 6.25-93.75% | Smooth gradients |
| Checkerboard | 50% | Mid-tone surface |
| Stippling (random) | varies | Organic surfaces |
| Hatching | varies | Stylized surfaces |
| 1×1 alternating | 50% | Old-school flicker effect |

```
Dither only between adjacent palette steps (e.g., dark+mid, not dark+highlight).
Dither in the second-darkest band to avoid muddying highlights.
```

Modern pixel art uses dithering sparingly — over-dithering looks dated / muddy. Mark Ferrari / Daniel Linssen popularized "selective dither at the value-step boundaries."

## Color Cycling

Animate palette indices instead of pixels — water, lava, magic effects, day/night.

```javascript
// PICO-8 / Phaser color-cycle example
const waterPalette = [12, 1, 13, 12]; // cycle 4 indices
const cycleSpeed = 200; // ms per step
let frame = 0;
setInterval(() => {
  pal(12, waterPalette[frame % 4]);
  frame++;
}, cycleSpeed);
```

Mark Ferrari LucasArts adventures (Loom, Monkey Island) used this for waterfalls / candles. Free in 8-bit, fast in modern engines.

## Validation

```
Lospec import: validate that the palette exists / matches a known hardware constraint
Color count check: ≤ N globally, ≤ M per sprite
Value contrast: convert to greyscale; verify silhouette + form readable
WCAG contrast (UI use): if palette is for UI, check 4.5:1
NES check: each 4-color sub-palette has 1 shared "universal" entry (background)
```

## Workflow

```
SELECT       →  pick palette: hardware-faithful / curated / custom
             →  document constraint (size, per-sprite limit)

ALLOCATE     →  reserve sub-palettes for character / enemies / UI
             →  if NES-faithful: 4 sub-palettes, attribute blocks

VALUE PLAN   →  greyscale-first sketch
             →  assign palette colors to value steps

DITHER       →  selectively at boundary between value steps
             →  prefer Bayer 4×4 or stippling
             →  avoid more than 2 dither textures per scene

COLOR CYCLE  →  identify cycling targets (water, sky, magic)
             →  define cycle palette + speed

VALIDATE     →  Lospec / hardware spec
             →  greyscale silhouette test
             →  per-sprite color count

EXPORT       →  indexed PNG (palette in file metadata)
             →  Aseprite .ase / GIMP .gpl palette export
             →  per-engine palette config

HANDOFF      →  dot `animation`: animation cycles within palette
             →  dot `tilesheet`: tiles within palette
             →  Builder: engine palette swap code
             →  Realm: gameplay palette tints (damage flash, etc.)
```

## Output Template

```markdown
## Palette Pack: [Project / Style]

### Palette Choice
- Name: [DB16 / NES-FBX / PICO-8 / custom]
- Total colors: [N]
- Per-sprite limit: [M]
- Hardware target: [NES / GB / web / generic]

### Palette Definition
```
0: #000000 (transparent / outline)
1: #1d2b53 (dark blue)
...
15: #ffccaa (peach)
```
[full hex list + role assignment]

### Sub-Palette Allocation (if applicable)
| Sub | Use | Colors |
|-----|-----|--------|
| 0 | Player | bg, skin-dark, skin, hair |
| 1 | Enemy A | bg, dark, mid, light |
| 2 | UI | bg, frame, text-dim, text |
| 3 | Effects | bg, fire-1, fire-2, fire-3 |

### Dithering Strategy
- Where: [sky, water, smoke surfaces]
- Pattern: [Bayer 4×4]
- Boundaries dithered: [dark↔mid only]

### Color Cycling
| Target | Indices | Speed |
|--------|---------|-------|
| Water | [12, 1, 13, 12] | 200ms |
| Lava | [8, 9, 10, 9] | 100ms |

### Validation
- Lospec match: [URL]
- Greyscale silhouette test: [pass / fail per sprite]
- Per-sprite color count: [pass / fail]
- WCAG contrast (if UI): [ratio per pair]

### Export
- Aseprite .ase / .gpl
- Indexed PNG (palette embedded)
- Engine config snippet: [Phaser / Godot / Unity]

### Handoffs
- dot `animation`: cycles within palette
- dot `tilesheet`: tiles within palette
- Builder: palette swap code
- Realm: gameplay tints
```

## Anti-Patterns

| Anti-pattern | Fix |
|--------------|-----|
| Free-color palette ("pick whatever looks good") | Constrain; cohesion comes from limit |
| 8 colors per 16×16 sprite | Cap at 4-6 visible; force value discipline |
| Heavy dithering across all surfaces | Selective; only at value-step boundary |
| Palette swap that uses out-of-palette tints | Stay within indices; use hue-shift via index |
| Unmarked transparent index | Always reserve index 0 as transparent |
| Custom palette without name / source | Name + Lospec or document origin |
| Mixing photorealistic colors with retro palette | Pick a coherent era / style |
| Per-sprite color count varies wildly | Set a per-sprite cap and enforce |
| Outline color = pure black always | Outline can be deepest hue, not always black |
| Highlight = pure white always | Off-white retains palette warmth |
| Skipping greyscale value pass | Greyscale-first or values fail |
| Muddy mid-tones from too-similar values | Min ΔE between value steps; expand contrast |
| Color cycling at 60Hz strobe | Slow enough not to flicker (≥100ms/step) |
| Hardware-faithful palette without per-sprite limit | NES isn't NES without 4-color sprite rule |
| Hex codes captured but no role assignment | Each color has a role (outline / shadow / mid / light) |

## Deliverable Contract

When `palette` completes, emit:

- **Palette choice** with size + per-sprite limit + hardware target.
- **Palette definition** (hex + role per index).
- **Sub-palette allocation** if hardware-constrained.
- **Dithering strategy** with where/pattern/boundaries.
- **Color cycling** definitions if used.
- **Validation** against Lospec / hardware spec / value test.
- **Export** files (Aseprite .ase / .gpl / indexed PNG).
- **Handoffs**: dot animation, dot tilesheet, Builder, Realm.

## References

- Lospec — lospec.com (palette browser + Pixel Art tutorials)
- DawnBringer — DB16 / DB32 palette pages
- PICO-8 manual — pico-8.fandom.com
- NES Dev Wiki — wiki.nesdev.org/w/index.php/PPU_palettes
- FCEUX FBX palette — fceux.com
- *Pixel Logic* — Michael Azzi
- *Make Your Own Pixel Art* — Dawe + Humphries
- Mark Ferrari — color-cycling demos (effectgames.com / 8bitworkshop)
- Daniel Linssen — selective dithering essays
- Pedro Medeiros (Saint11) — pixel art tutorials
- Endesga 32 — github.com/Endesga
- AAP-64 — Adigun Polack palette
- *The Art of Pixel* — Brandon James Greer (YouTube)
- "Color in Game Art" — GDC talks (e.g., Mark Brown)
- Aseprite color and palette docs
- Tile-based: Tiled / LDtk palette imports
- Game Maker Studio palette swap example
