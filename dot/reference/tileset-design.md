# Tileset Design Reference

Purpose: engine-agnostic tile **fundamentals** — sizes, bitmask math, terrain overlay strategy, seamless tile algorithm, palette-cycling animation, common tile categories. Read this when Dot must design tilesets, autotiles, terrain transitions, or tilemap metadata.

> Engine-specific recipe workflow (Tiled `.tsx` XML, LDtk auto-rules, Phaser/Godot/Unity emission, atlas packing, deliverable contract, anti-patterns) is in `reference/tilesheet-design.md`.

## Contents

- [Standard tile sizes](#standard-tile-sizes)
- [Basic tileset layout](#basic-tileset-layout)
- [Auto-tiling systems](#auto-tiling-systems)
- [Wang tiles](#wang-tiles)
- [Terrain transitions](#terrain-transitions)
- [Animated tiles](#animated-tiles)
- [Seamless tiling patterns](#seamless-tiling-patterns)
- [Common tile categories](#common-tile-categories)
- [Engine-specific auto-tile formats](#engine-specific-auto-tile-formats)
- [Tilemap metadata JSON](#tilemap-metadata-json)
- [Design checklist](#design-checklist)

## Standard Tile Sizes

| Size | Use Case | Engines |
|------|----------|---------|
| 8x8 | Micro tiles, NES-style | Custom, PICO-8 |
| 16x16 | Standard RPG/platformer | Phaser 3, Godot, RPG Maker, Unity |
| 24x24 | RPG Maker default | RPG Maker MV/MZ |
| 32x32 | Detailed tiles | Phaser 3, Godot, Unity |
| 48x48 | Large detail tiles | RPG Maker (scaled) |
| 64x64 | High-res pixel art | Unity, Godot |

**Default recommendation:** 16x16 -- widest engine support, good detail-to-effort ratio.

### Size Selection by Project

| Game Type | Recommended | Reason |
|-----------|------------|--------|
| NES retro | 8x8 or 16x16 | Hardware authenticity |
| SNES retro | 16x16 | Standard for the era |
| Modern indie | 16x16 or 32x32 | Balance detail vs. effort |
| Detailed RPG | 32x32 or 48x48 | Rich environments |
| Strategy/Tactics | 16x16 or 32x32 | Many tiles visible at once |

---

## Basic Tileset Layout

### Minimal Terrain Set (15 tiles)

```
+----+----+----+
| TL | TM | TR |  Top-left, Top-mid, Top-right
+----+----+----+
| ML | MM | MR |  Mid-left, Mid (fill), Mid-right
+----+----+----+
| BL | BM | BR |  Bot-left, Bot-mid, Bot-right
+----+----+----+
Plus: inner corners (4) + single tile + horizontal pipe + vertical pipe
```

### Complete Terrain Set Categories

| Category | Tiles | Purpose |
|----------|-------|---------|
| **Outer edges** | 8 (4 sides + 4 corners) | Where terrain meets another terrain |
| **Inner corners** | 4 | Concave corners (terrain wraps around) |
| **Fill** | 1+ | Interior with possible variations |
| **Isolated** | 1 | Single-tile island |
| **Pipes** | 2 | 1-tile wide horizontal and vertical strips |
| **Caps** | 4 | End pieces for pipes |
| **Total (4-bit)** | 16 | Minimum complete set |
| **Total (8-bit)** | 47 | All diagonal combinations |

---

## Auto-Tiling Systems

### 4-bit (Simple) -- 16 tiles

Check 4 cardinal neighbors: Up, Down, Left, Right.

```
Bitmask:
  Up    = 1
  Right = 2
  Down  = 4
  Left  = 8

Index = (up ? 1 : 0) + (right ? 2 : 0) + (down ? 4 : 0) + (left ? 8 : 0)
```

| Index | Binary | Neighbors | Tile Type |
|-------|--------|-----------|-----------|
| 0 | 0000 | None | Isolated |
| 1 | 0001 | U | Bottom cap |
| 2 | 0010 | R | Left cap |
| 3 | 0011 | U+R | Bottom-left corner |
| 4 | 0100 | D | Top cap |
| 5 | 0101 | U+D | Vertical pipe |
| 6 | 0110 | R+D | Top-left corner |
| 7 | 0111 | U+R+D | Left edge |
| 8 | 1000 | L | Right cap |
| 9 | 1001 | U+L | Bottom-right corner |
| 10 | 1010 | R+L | Horizontal pipe |
| 11 | 1011 | U+R+L | Bottom edge |
| 12 | 1100 | D+L | Top-right corner |
| 13 | 1101 | U+D+L | Right edge |
| 14 | 1110 | R+D+L | Top edge |
| 15 | 1111 | All | Center fill |

### 8-bit (Blob) -- 47 tiles

Check 8 neighbors (including diagonals). **Critical rule:** Corners only count if both adjacent edges are filled.

```javascript
// Bitmask calculation with corner masking
function calcBitmask(x, y, map) {
  const n  = get(x, y-1);    // 1
  const ne = get(x+1, y-1);  // 2
  const e  = get(x+1, y);    // 4
  const se = get(x+1, y+1);  // 8
  const s  = get(x, y+1);    // 16
  const sw = get(x-1, y+1);  // 32
  const w  = get(x-1, y);    // 64
  const nw = get(x-1, y-1);  // 128

  let mask = 0;
  if (n)            mask |= 1;
  if (ne && n && e) mask |= 2;   // corner needs both edges
  if (e)            mask |= 4;
  if (se && s && e) mask |= 8;   // corner needs both edges
  if (s)            mask |= 16;
  if (sw && s && w) mask |= 32;  // corner needs both edges
  if (w)            mask |= 64;
  if (nw && n && w) mask |= 128; // corner needs both edges

  return mask;
}
```

#### Why 47 Tiles, Not 256?

8-bit bitmask produces 256 values (2^8), but corner masking reduces unique visual configurations:
- Corners only matter when **both** adjacent edges exist
- When an edge is missing, adjacent corners don't change appearance
- This collapses 256 values into **47 unique visual tiles**

#### 47-Tile Visual Reference

```
Category breakdown:
  4 outer corners    (L-shaped outer edge)
  4 outer edges      (straight edge)
  4 inner corners    (single pixel concave notch)
  4 T-junctions      (3 edges filled, 1 open)
  4 end caps         (pipe terminator)
  2 pipes            (horizontal, vertical)
  1 isolated         (all sides open)
  1 center fill      (all sides filled)
  4 peninsula        (one corner notched from fill)
  2 channel          (opposite sides open)
  8 irregular        (various 2-corner combinations)
  9 complex          (3-corner and mixed patterns)
  ---
  47 total unique tiles
```

### Bitmask to Tile Index Lookup

```javascript
// Map 256 bitmask values to 47 tile indices
// This lookup table maps each valid bitmask to a tile index (0-46)
const BITMASK_TO_TILE = {
  0: 0,     // isolated
  1: 1,     // N only
  2: 1,     // NE only (ignored, no adjacent edges)
  4: 2,     // E only
  5: 3,     // N+E
  // ... (full table has 256 entries mapping to 47 tiles)
};

// Simplified approach: use a minimal lookup
function bitmaskToTileIndex(mask) {
  // Normalize: strip corners without adjacent edges
  const normalized = normalizeCorners(mask);
  return TILE_LOOKUP[normalized] || 0;
}
```

---

## Wang Tiles

Wang tiles use colored edges instead of bitmasks. Each tile has 4 edges, each with a color code.

### 2-Color Wang Tile Set

```
Edge colors: A (terrain) and B (empty)
Each tile has: [North, East, South, West] edge colors

With 2 colors and 4 edges: 2^4 = 16 unique tiles
```

| Tile | N | E | S | W | Description |
|------|---|---|---|---|-------------|
| 0 | B | B | B | B | Empty |
| 1 | A | B | B | B | North edge |
| 2 | B | A | B | B | East edge |
| 3 | A | A | B | B | NE corner |
| ... | | | | | |
| 15 | A | A | A | A | Full fill |

### Wang Tiles vs Bitmask

| Aspect | Wang Tiles | Bitmask |
|--------|-----------|---------|
| Concept | Edge color matching | Neighbor presence check |
| Tile count (simple) | 16 | 16 |
| Tile count (complex) | 16-48 | 47 |
| Randomization | Natural; multiple tiles per edge combo | Requires variant tiles |
| Tool support | Tiled, Godot | Godot, RPG Maker, Unity |
| Best for | Organic terrain, varied landscapes | Structured tiles, walls |

### Wang Tile Advantage: Variation

Multiple tiles can share the same edge configuration, enabling randomized placement:

```
All with edges [A, A, A, A] (center fill):
  Tile 15a: grass with no detail
  Tile 15b: grass with small flower
  Tile 15c: grass with stone
  -> Engine randomly picks one, breaking visible repetition
```

---

## Terrain Transitions

### Single Terrain (A on empty)

Standard 16 or 47 tile approach as described above.

### Two-Terrain Transition (A meets B)

When two terrain types meet (e.g., grass meets dirt), you need transition tiles:

```
                Dirt
           +---------+
           |  grass  |  <- transition tile: grass top, dirt bottom
           |  dirt   |
           +---------+
                Grass
```

**Tile count for 2-terrain transitions:**

| Method | Tiles per Pair | Notes |
|--------|---------------|-------|
| 4-bit overlay | 16 | Transparent overlay tiles on base |
| 8-bit overlay | 47 | Full blob set as overlay |
| Separate tiles | 16-47 per pair | Dedicated transition tiles |

### Multi-Terrain Strategy

For N terrains, dedicated transition tiles grow as O(N^2). Use overlay strategy instead:

```
Layer 0 (base):   Fill terrain (dirt, stone, etc.)
Layer 1 (overlay): Transparent-bordered terrain on top (grass edges)
Layer 2 (overlay): Additional overlay (path, water edges)
```

**Benefit:** Each new terrain adds only 16/47 overlay tiles, not N new transition sets.

### Cliff / Height Transitions

For top-down RPGs with elevation:

```
+------+------+------+
| cliff| cliff| cliff|  <- cliff face (2-3 tiles tall)
| face | face | face |
+------+------+------+
| cliff| cliff| cliff|  <- cliff base / shadow
| base | base | base |
+------+------+------+
| low  | low  | low  |  <- lower terrain
| terr | terr | terr |
+------+------+------+
```

---

## Animated Tiles

### Water Animation (Common)

```
Frame 0: Base water pattern
Frame 1: Shifted 1-2px (or palette rotation)
Frame 2: Shifted 2-4px
Frame 3: (optional) return cycle

FPS: 3-4 (slow, ambient)
```

**Palette cycling trick:** Instead of different tile graphics, cycle 2-3 blue shades in the palette. All water tiles animate simultaneously with zero additional tile data.

```python
# Palette cycling for water
water_palettes = [
    ['#2a5db0', '#3d7edb', '#63a2f4'],  # Frame 0
    ['#63a2f4', '#2a5db0', '#3d7edb'],  # Frame 1 (rotated)
    ['#3d7edb', '#63a2f4', '#2a5db0'],  # Frame 2 (rotated)
]
```

### Other Animated Tiles

| Tile | Frames | FPS | Technique |
|------|--------|-----|-----------|
| Water | 3-4 | 3-4 | Palette cycle or pixel shift |
| Lava | 3-4 | 2-3 | Palette cycle (warm tones) |
| Torches/Fire | 3-5 | 6-8 | Frame swap |
| Flowers/Grass | 2-3 | 2-3 | Subtle pixel shift (wind) |
| Waterfall | 3-4 | 6-8 | Vertical pixel shift |
| Sparkle | 3-4 | 4-6 | Highlight pixel on/off |

---

## Seamless Tiling Patterns

### Rules for Seamless Tiles

1. **Edge matching** -- pixels on left edge must flow into right edge
2. **Corner consistency** -- all 4 corners must be compatible when tiled
3. **Pattern variation** -- avoid obvious 2x2 repetition
4. **Noise distribution** -- scatter details to break grid visibility

### Creating Seamless Tiles (Method)

```
Step 1: Draw the full tile
Step 2: Cut into 4 quadrants and swap diagonally:
  [A][B]  ->  [D][C]
  [C][D]  ->  [B][A]
Step 3: Fix the center seams (where cuts meet)
Step 4: Test by tiling 3x3 and checking for visible seams
```

### Seamless Tile Verification

```python
from PIL import Image

def verify_seamless(tile_path, grid=3):
    """Check if a tile tiles seamlessly by creating a grid."""
    tile = Image.open(tile_path)
    w, h = tile.size
    test = Image.new('RGBA', (w * grid, h * grid))
    for row in range(grid):
        for col in range(grid):
            test.paste(tile, (col * w, row * h))
    test.save('seamless_test.png')
    return test

def create_seamless_from_texture(source, tile_size):
    """Create a seamless tile from a larger texture using the offset method."""
    # Crop to tile_size
    tile = source.crop((0, 0, tile_size, tile_size))
    half = tile_size // 2

    # Split into 4 quadrants and swap diagonally
    tl = tile.crop((0, 0, half, half))
    tr = tile.crop((half, 0, tile_size, half))
    bl = tile.crop((0, half, half, tile_size))
    br = tile.crop((half, half, tile_size, tile_size))

    seamless = Image.new('RGBA', (tile_size, tile_size))
    seamless.paste(br, (0, 0))
    seamless.paste(bl, (half, 0))
    seamless.paste(tr, (0, half))
    seamless.paste(tl, (half, half))
    # Note: center seams need manual pixel editing after this
    return seamless
```

### Breaking Repetition

| Technique | Description |
|-----------|-------------|
| **Tile variants** | Create 2-4 versions of fill tile; randomly pick |
| **Detail overlays** | Scatter small objects (stones, flowers) on separate layer |
| **Large-tile composition** | Compose 2x2 or 3x3 macro-tiles for complex patterns |
| **Dithering at edges** | Use dither patterns at tile boundaries for organic feel |

---

## Common Tile Categories

### Terrain Tiles

| Category | Tiles Needed | Notes |
|----------|-------------|-------|
| Grass | 1 fill + 15 edge variants | Most common base terrain |
| Water | 1 fill + 15 edges + 3 animation frames | Animated fill |
| Dirt/Path | 1 fill + 15 edges | Walkable surface |
| Stone/Brick | 1 fill + 15 edges | Walls, floors |
| Sand | 1 fill + 15 edges | Beach, desert |
| Snow | 1 fill + 15 edges | Winter theme |

### Object Tiles

| Category | Size | Notes |
|----------|------|-------|
| Trees | 2x2 or 2x3 | Multi-tile, top layer over terrain |
| Buildings | 3x3 to 5x5 | Multi-tile with door position |
| Furniture | 1x1 or 2x1 | Interior decoration |
| Props | 1x1 | Signs, barrels, crates |
| Doors | 1x2 | With open/closed states |
| Stairs | 1x2 or 2x2 | Elevation change markers |

### Decoration Layer

Props and decorations should be on a **separate layer** above terrain:

```
Layer 2: Objects  (trees, buildings — collision)
Layer 1: Overlay  (grass tufts, flowers — no collision)
Layer 0: Terrain  (ground tiles — base layer)
```

---

## Engine-Specific Auto-Tile Formats

| Engine | System | Tile Count | Layout |
|--------|--------|-----------|--------|
| RPG Maker MV/MZ | A2 autotile | 48 variants from 5 sub-tiles | 2x3 source -> 48 combos |
| Godot 3/4 | TileSet bitmask | 47 (blob) or 16 (simple) | Configure in editor |
| Unity (Rule Tile) | Custom rules | Variable | Scriptable object |
| Phaser 3 | Manual / plugin | 16 or 47 | Index array |
| Tiled (editor) | Wang tiles | 16 or 47 | Terrain brush |

### RPG Maker A2 Autotile (Sub-Tile Method)

RPG Maker generates 48 tile variants from a **2x3 mini-tileset** (5 sub-tiles):

```
Source layout (2x3):
+----+----+
| A1 | A2 |  <- inner parts
+----+----+
| A3 | A4 |  <- outer corners
+----+----+
| A5 |    |  <- center fill
+----+----+

Each output tile is composed of 4 quarter-sub-tiles
arranged from these 5 sources -> 48 combinations
```

### Godot 4.3+ TileSet Setup (TileMapLayer)

Godot 4.3 deprecated `TileMap` in favor of individual `TileMapLayer` nodes:

```gdscript
# In editor:
# 1. Create TileSet resource
# 2. Add atlas texture (your tileset image)
# 3. Set tile size (16x16)
# 4. Configure terrain sets:
#    - Terrain Set 0: Match Corners and Sides (8-bit / 47 tiles)
#    - Terrain Set 0: Match Sides (4-bit / 16 tiles)
# 5. Paint terrain bits on each tile in the atlas

# In code (Godot 4.3+: use TileMapLayer, not TileMap):
var ground = $GroundLayer   # TileMapLayer node
var objects = $ObjectLayer  # TileMapLayer node
ground.set_cell(Vector2i(x, y), source_id, atlas_coords)
# Note: no layer index parameter — each TileMapLayer is a separate node
```

---

## Tileset Code Template (Phaser 3)

> Engine emission templates (Phaser, Tiled `.tsx`, LDtk rules, Godot, Unity) live in `reference/tilesheet-design.md` under "Engine Integration". This document keeps only metadata structure (next section).

---

## Tilemap Metadata JSON

```json
{
  "name": "forest-tileset",
  "tileWidth": 16,
  "tileHeight": 16,
  "columns": 16,
  "tileCount": 256,
  "terrains": [
    {
      "name": "grass",
      "firstGid": 0,
      "autotile": "4bit",
      "tileCount": 16,
      "variants": 2
    },
    {
      "name": "water",
      "firstGid": 16,
      "autotile": "4bit",
      "tileCount": 16,
      "animated": true,
      "animFrames": 3,
      "animFps": 4
    },
    {
      "name": "stone",
      "firstGid": 64,
      "autotile": "8bit",
      "tileCount": 47
    }
  ],
  "layers": [
    { "name": "ground", "type": "terrain" },
    { "name": "overlay", "type": "decoration" },
    { "name": "objects", "type": "collision" }
  ]
}
```

---

## Design Checklist

- [ ] Tile size matches target engine standards
- [ ] All terrain types have complete edge sets (16 or 47)
- [ ] Corner masking implemented correctly (8-bit)
- [ ] Fill tiles have 2+ variants to break repetition
- [ ] Animated tiles have consistent frame counts and FPS
- [ ] Seamless tiling verified with 3x3 grid test
- [ ] Decorations on separate layer from terrain
- [ ] Object tiles have consistent size and anchor point
- [ ] Palette consistent with sprite assets
- [ ] Tileset image is power-of-two dimensions
- [ ] No anti-aliasing on any tile edge
- [ ] Consistent light direction matches sprite assets
