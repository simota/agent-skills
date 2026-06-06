# Engine Integration Reference

Purpose: load this when the asset must run in a browser, Phaser, Godot, Unity, PixiJS, or RPG Maker. It preserves pixel-perfect rendering rules, engine configuration, and troubleshooting guidance.

## Contents

- [Browser `image-rendering` compatibility](#browser-image-rendering-compatibility)
- [Rendering method comparison](#rendering-method-comparison)
- [Phaser 3 configuration](#phaser-3-configuration)
- [Godot 4 configuration](#godot-4-configuration)
- [Unity configuration](#unity-configuration)
- [PixiJS v8 configuration](#pixijs-v8-configuration-2024)
- [RPG Maker MV/MZ configuration](#rpg-maker-mvmz-configuration)
- [Common integration checklist](#common-integration-checklist)
- [Scaling matrix](#scaling-matrix)
- [Troubleshooting](#troubleshooting)

## Browser `image-rendering` Compatibility

### CSS Property

```css
/* Recommended: stack for cross-browser */
.pixel-art {
  image-rendering: pixelated;       /* Chrome, Edge, Opera */
  image-rendering: crisp-edges;     /* Firefox */
  -ms-interpolation-mode: nearest-neighbor; /* IE (legacy) */
}
```

### Browser Support Matrix

| Browser | `pixelated` | `crisp-edges` | Notes |
|---------|:-----------:|:-------------:|-------|
| Chrome 41+ | Yes | Partial | Use `pixelated` |
| Chrome 120+ | Yes | Yes | Both work |
| Firefox 65+ | Yes | Yes | Either works |
| Safari 10+ | Yes | Yes | Either works |
| Safari 17+ (iOS) | Yes | Yes | Stable |
| Edge 79+ | Yes | Partial | Chromium-based, use `pixelated` |
| Opera 28+ | Yes | Partial | Chromium-based |
| Samsung Internet 5+ | Yes | No | Use `pixelated` only |
| Android Chrome | Yes | Partial | Use `pixelated` |

**Recommendation:** Always use both `pixelated` and `crisp-edges` for maximum compatibility. Order matters: put `pixelated` first (most common), `crisp-edges` second (fallback).

### Canvas Context

```javascript
// Must set BEFORE any drawing operations
const ctx = canvas.getContext('2d');
ctx.imageSmoothingEnabled = false;

// Legacy vendor prefixes (for older browsers)
ctx.mozImageSmoothingEnabled = false;    // Firefox < 65
ctx.webkitImageSmoothingEnabled = false; // Safari < 15
ctx.msImageSmoothingEnabled = false;     // IE/Edge Legacy
```

**Important:** `imageSmoothingEnabled` resets when canvas is resized. Re-set it after any `canvas.width =` or `canvas.height =` assignment.

### SVG

```xml
<!-- On the SVG element -->
<svg shape-rendering="crispEdges"
     style="image-rendering: pixelated;" ...>

<!-- Or on individual elements -->
<rect shape-rendering="crispEdges" ... />
```

### WebGL

```javascript
// For WebGL-based renderers (Phaser, PixiJS, Three.js)
const gl = canvas.getContext('webgl2');
gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.NEAREST);
gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.NEAREST);
```

---

## Rendering Method Comparison

| Aspect | SVG | Canvas 2D | WebGL | CSS |
|--------|-----|-----------|-------|-----|
| **Scaling quality** | Excellent | Good | Excellent | Good |
| **Performance (static)** | Good | Excellent | Excellent | Fair |
| **Performance (animated)** | Fair | Good | Excellent | Poor |
| **Transparency** | Yes | Yes | Yes | Limited |
| **Max sprite size** | Unlimited | Browser limit | GPU limit | ~32x32 |
| **Pixel-perfect guarantee** | Yes (crispEdges) | Yes (smoothing off) | Yes (NEAREST) | Yes (transform) |
| **Export** | Direct SVG | PNG/Blob | PNG/Blob | N/A |
| **Interactivity** | DOM events | Hit detection | Shader-based | DOM events |
| **Browser support** | Universal | Universal | ~97% | Universal |

### When to Use Each

| Use Case | Best Method |
|----------|------------|
| Static icon/sprite display | SVG |
| Interactive preview | Canvas 2D |
| Game (many sprites, animation) | WebGL (via Phaser/PixiJS) |
| Small decorative element | CSS |
| Batch export/processing | Canvas (OffscreenCanvas) |
| Print/vector output | SVG |

---

## Phaser 3 Configuration

### Game Config (Complete Pixel Art Setup)

```javascript
const config = {
  type: Phaser.AUTO,        // Auto-select WebGL or Canvas
  pixelArt: true,            // Sets texture filtering to NEAREST
  roundPixels: true,          // Prevents sub-pixel rendering
  antialias: false,           // Explicit anti-alias disable
  scale: {
    mode: Phaser.Scale.FIT,
    autoCenter: Phaser.Scale.CENTER_BOTH,
    width: 320,               // Game resolution (low)
    height: 180,
    zoom: Phaser.Scale.MAX_ZOOM,
  },
  render: {
    pixelArt: true,           // Also set in render config
    antialias: false,
    roundPixels: true,
  },
  physics: {
    default: 'arcade',
    arcade: {
      gravity: { y: 0 },
      debug: false,
    },
  },
  scene: [GameScene],
};
```

### Key Settings Explained

| Setting | Value | Purpose |
|---------|-------|---------|
| `pixelArt` | `true` | Forces NEAREST filtering on all textures |
| `roundPixels` | `true` | Snaps sprite positions to integers |
| `antialias` | `false` | Disables WebGL anti-aliasing |
| `scale.width/height` | Low res (e.g., 320x180) | Native pixel resolution |
| `scale.zoom` | `MAX_ZOOM` | Scales up to fill screen |
| `scale.mode` | `FIT` | Maintains aspect ratio |

### Common Resolutions for Pixel Art Games

| Resolution | Aspect Ratio | Style | Scale to 1080p |
|-----------|-------------|-------|---------------|
| 160x144 | ~10:9 | GameBoy | 7x (1120x1008) |
| 256x224 | ~8:7 | NES | 4x (1024x896) |
| 256x240 | ~16:15 | NES (full) | 4x (1024x960) |
| 320x180 | 16:9 | Modern widescreen | 6x (1920x1080) |
| 320x240 | 4:3 | SNES-era | 4x (1280x960) |
| 384x216 | 16:9 | Modern widescreen | 5x (1920x1080) |
| 480x270 | 16:9 | HD pixel art | 4x (1920x1080) |
| 640x360 | 16:9 | Large pixel art | 3x (1920x1080) |

### Sprite Loading

```javascript
// Single sprite
this.load.image('item', 'item.png');

// Spritesheet (uniform grid)
this.load.spritesheet('hero', 'hero-sheet.png', {
  frameWidth: 16,
  frameHeight: 16,
  margin: 0,      // border around entire sheet
  spacing: 0,     // gap between frames
});

// Texture atlas (JSON hash -- variable frame sizes)
this.load.atlas('sprites', 'sprites.png', 'sprites.json');

// Aseprite native support (Phaser 3.60+)
this.load.aseprite('hero', 'hero.png', 'hero.json');
```

### Animation Creation

```javascript
// Basic animation
this.anims.create({
  key: 'walk',
  frames: this.anims.generateFrameNumbers('hero', { start: 0, end: 5 }),
  frameRate: 8,
  repeat: -1,     // loop forever
});

// Variable frame duration
this.anims.create({
  key: 'attack',
  frames: [
    { key: 'hero', frame: 10, duration: 150 },  // anticipation
    { key: 'hero', frame: 11, duration: 50 },   // swing
    { key: 'hero', frame: 12, duration: 50 },   // impact
    { key: 'hero', frame: 13, duration: 200 },  // follow-through
  ],
  repeat: 0,
});

// From Aseprite tags (Phaser 3.60+)
this.anims.createFromAseprite('hero');
// Automatically creates animations named by Aseprite frame tags
```

### Camera Configuration

```javascript
// In scene.create()
this.cameras.main.roundPixels = true;
this.cameras.main.setZoom(4);

// Follow player with pixel-perfect camera
this.cameras.main.startFollow(player, true, 1, 1);
this.cameras.main.setDeadzone(0, 0);

// Bounds (limit camera to map)
this.cameras.main.setBounds(0, 0, mapWidth, mapHeight);
```

### Generate Texture Pattern

```javascript
// Create texture from code (no external file needed)
function makeTexture(scene, key, pixelData, palette) {
  const gfx = scene.make.graphics({ add: false });

  pixelData.forEach((row, y) => {
    row.forEach((idx, x) => {
      if (idx >= 0) {
        gfx.fillStyle(parseInt(palette[idx].slice(1), 16));
        gfx.fillRect(x, y, 1, 1);
      }
    });
  });

  gfx.generateTexture(key, pixelData[0].length, pixelData.length);
  gfx.destroy();
}
```

### Phaser 3 Tilemap Setup

```javascript
// Load
this.load.image('tiles', 'tileset.png');
this.load.tilemapTiledJSON('map', 'map.json');

// Create
const map = this.make.tilemap({ key: 'map' });
const tileset = map.addTilesetImage('terrain', 'tiles', 16, 16, 0, 0);
const ground = map.createLayer('ground', tileset, 0, 0);
const objects = map.createLayer('objects', tileset, 0, 0);

// Collision
objects.setCollisionByProperty({ collides: true });

// Animated tiles (via plugin or manual)
// https://github.com/nkholski/phaser-animated-tiles
```

---

## Godot 4 Configuration

### Project Settings

```ini
# project.godot
[rendering]
textures/canvas_textures/default_texture_filter = 0  # Nearest
2d/snap/snap_2d_transforms_to_pixel = true
2d/snap/snap_2d_vertices_to_pixel = true

[display]
window/size/viewport_width = 320
window/size/viewport_height = 180
window/size/window_width_override = 1280
window/size/window_height_override = 720
window/stretch/mode = "viewport"
window/stretch/aspect = "keep"
```

### Import Settings (per texture)

```
Filter: Off (Nearest)
Repeat: Disabled (or Enabled for tilesets)
Mipmaps: Off
Fix Alpha Border: Off
Premultiplied Alpha: Off
```

### Sprite Setup (GDScript)

```gdscript
# Sprite2D node
var sprite = Sprite2D.new()
sprite.texture = load("res://sprites/hero.png")
sprite.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
sprite.centered = true

# Camera2D for pixel-perfect
var camera = Camera2D.new()
camera.zoom = Vector2(4, 4)
camera.position_smoothing_enabled = false
```

### Animated Sprite

```gdscript
# AnimatedSprite2D
var anim_sprite = AnimatedSprite2D.new()
var frames = SpriteFrames.new()

# Add animation
frames.add_animation("walk")
frames.set_animation_speed("walk", 8)  # FPS
frames.set_animation_loop("walk", true)

# Add frames
for i in range(6):
    var tex = load("res://sprites/hero_walk_%d.png" % i)
    frames.add_frame("walk", tex)

anim_sprite.sprite_frames = frames
anim_sprite.play("walk")
```

### Godot 4.3+ TileMapLayer (replaces TileMap)

Godot 4.3 deprecated the monolithic `TileMap` node. Use individual `TileMapLayer` nodes instead:

```gdscript
# Godot 4.3+: Use TileMapLayer nodes (one per layer)
# 1. Create TileMapLayer node (not TileMap)
# 2. Assign TileSet resource
# 3. Set tile size: 16x16
# 4. Configure terrains in TileSet editor

var ground_layer = $GroundLayer  # TileMapLayer node
var object_layer = $ObjectLayer  # TileMapLayer node

# Place tile programmatically
ground_layer.set_cell(Vector2i(5, 3), 0, Vector2i(0, 0))
# Args: coords, source_id, atlas_coords (no layer index needed)

# Godot 4.3+: integer scale mode for pixel-perfect rendering
# Project Settings → Display → Window → Stretch → Scale Mode = "integer"
```

**Migration from TileMap:** Replace single `TileMap` with multiple `TileMapLayer` children. Remove the layer index parameter from `set_cell()` calls.

---

## Unity Configuration

### Sprite Import Settings

| Setting | Value | Purpose |
|---------|-------|---------|
| Texture Type | Sprite (2D and UI) | Standard sprite |
| Sprite Mode | Single / Multiple | Single or atlas |
| Pixels Per Unit | 16 (match tile size) | World unit = 1 tile |
| Filter Mode | **Point (no filter)** | NEAREST neighbor |
| Compression | None | Preserve exact pixels |
| Max Size | Match source | No downscaling |
| Generate Mipmaps | Off | Prevent blurring at distance |
| sRGB (Color Texture) | On | Correct color space |

### Pixel Perfect Camera

```csharp
// Requires: com.unity.2d.pixel-perfect package
using UnityEngine.U2D;

var ppCam = Camera.main.gameObject.AddComponent<PixelPerfectCamera>();
ppCam.assetsPPU = 16;              // Match sprite Pixels Per Unit
ppCam.refResolutionX = 320;        // Reference resolution
ppCam.refResolutionY = 180;
ppCam.upscaleRT = true;            // Render at low res, upscale
ppCam.pixelSnapping = true;        // Snap to pixel grid
ppCam.cropFrame = PixelPerfectCamera.CropFrame.None;
```

### Sprite Renderer

```csharp
// Ensure point filtering at runtime
var sr = GetComponent<SpriteRenderer>();
sr.sprite.texture.filterMode = FilterMode.Point;

// Material: use "Sprites/Default" material
// Ensure material's texture is also set to Point filtering
```

### Unity Tilemap Setup

```csharp
// Grid component
var grid = gameObject.AddComponent<Grid>();
grid.cellSize = new Vector3(1, 1, 0);  // 1 unit = 1 tile

// Tilemap
var tilemap = gameObject.AddComponent<Tilemap>();
var renderer = gameObject.AddComponent<TilemapRenderer>();
renderer.sortingOrder = 0;

// For pixel art: ensure Grid Layout is "Rectangle"
// and cell swizzle is "XYZ"
```

### Unity Animator for Pixel Art

```csharp
// 1. Slice spritesheet in Sprite Editor (Multiple mode)
// 2. Select all frames in Project window
// 3. Drag into Scene -> Unity creates Animation + Animator automatically
// 4. Set Animator update mode to "Normal"
// 5. Ensure all sprites have same PPU and Point filtering

// Programmatic animation control
var animator = GetComponent<Animator>();
animator.Play("walk");

// For frame-perfect animations, use Animation component instead of Animator
var animation = gameObject.AddComponent<Animation>();
// Set sample rate to match your FPS (e.g., 8, 10, 12)
```

---

## PixiJS v8 Configuration (2024+)

PixiJS v8 rewrote the rendering pipeline. Key API changes for pixel art:

```javascript
// v8: Application is now async
const app = new PIXI.Application();
await app.init({
  width: 320,
  height: 180,
  resolution: 4,
  autoDensity: true,
  antialias: false,
  backgroundColor: 0x000000,
});

// v8: Set default scale mode for all textures
PIXI.TextureStyle.defaultOptions.scaleMode = 'nearest';

// Or per-texture
const texture = PIXI.Texture.from('hero.png');
texture.source.scaleMode = 'nearest';

// Sprite
const sprite = new PIXI.Sprite(texture);
sprite.roundPixels = true;  // Snap to integer positions

// Animated sprite from spritesheet
const sheet = await PIXI.Assets.load('hero.json');
const animSprite = new PIXI.AnimatedSprite(sheet.animations['walk']);
animSprite.animationSpeed = 0.15;  // 0-1 range, roughly FPS/60
animSprite.play();
```

### PixiJS v7 → v8 Migration (Pixel Art)

| v7 API | v8 API |
|--------|--------|
| `new PIXI.Application({ ... })` | `await new PIXI.Application().init({ ... })` |
| `PIXI.BaseTexture.defaultOptions.scaleMode = PIXI.SCALE_MODES.NEAREST` | `PIXI.TextureStyle.defaultOptions.scaleMode = 'nearest'` |
| `texture.baseTexture.scaleMode` | `texture.source.scaleMode` |
| `PIXI.SCALE_MODES.NEAREST` | `'nearest'` (string) |

---

## RPG Maker MV/MZ Configuration

### Character Sprite Format

```
Standard character sheet: 12 columns x 8 rows
  3 columns per direction x 4 directions
  2 rows per character x 4 characters per sheet

Walking pattern: [left-step] [center] [right-step]
Direction order: Down(0) Left(1) Right(2) Up(3)

Default frame size: 48x48 (MV/MZ)
                    32x32 (VX/VX Ace)
                    24x32 (XP)
```

### Tileset Format (A2 Autotile)

```
Each A2 autotile is 2 tiles wide x 3 tiles tall
Generates 48 patterns from 5 sub-tile combinations
Place in img/tilesets/ folder
```

---

## Common Integration Checklist

Before shipping pixel art to any engine:

- [ ] **Nearest-neighbor filtering** enabled on all sprites
- [ ] **No compression artifacts** (PNG only, no JPEG)
- [ ] **Integer scaling** (2x, 3x, 4x -- never 1.5x)
- [ ] **Camera pixel-snapping** enabled
- [ ] **Sub-pixel movement disabled** or handled properly
- [ ] **Consistent pixel density** across all assets
- [ ] **Transparent background** (RGBA, not white)
- [ ] **Power-of-two dimensions** for spritesheets (256, 512, 1024)
- [ ] **No anti-aliasing** on any sprite edge
- [ ] **Consistent light direction** across all sprites (top-left default)
- [ ] **Consistent palette** across all assets in same scene
- [ ] **No mipmap generation** on pixel art textures
- [ ] **Frame rate tested** at target device performance

## Scaling Matrix

| Source | 1x | 2x | 3x | 4x | 8x |
|--------|----|----|----|----|-----|
| 8x8 | 8px | 16px | 24px | 32px | 64px |
| 16x16 | 16px | 32px | 48px | 64px | 128px |
| 32x32 | 32px | 64px | 96px | 128px | 256px |
| 64x64 | 64px | 128px | 192px | 256px | 512px |
| 320x180 | 320px | 640px | 960px | 1280px | 2560px |

---

## Troubleshooting

### Common Rendering Issues

| Issue | Symptom | Fix |
|-------|---------|-----|
| **Blurry sprites** | Soft edges, no sharp pixels | Enable nearest-neighbor filtering |
| **Color bleeding** | Colors from adjacent tiles leak | Add 1px padding to spritesheet, or fix UV |
| **Sub-pixel jitter** | Sprites vibrate when moving | Enable roundPixels / pixel snapping |
| **Inconsistent size** | Some sprites look bigger/smaller | Ensure consistent PPU / pixels-per-unit |
| **Dark edges** | Black line around transparent sprites | Premultiply alpha or fix sprite import |
| **Seams in tilemap** | Gaps between tiles visible | Enable pixel snapping on camera + tilemap |
| **Wrong colors** | Colors shifted or different | Check sRGB setting, disable color management |
| **Mipmap blur** | Sprites blur at distance | Disable mipmap generation on all textures |
| **Scaling artifacts** | Asymmetric pixels, uneven scaling | Use integer scaling only (2x, 3x, not 2.5x) |

### Engine-Specific Gotchas

| Engine | Gotcha | Solution |
|--------|--------|----------|
| **Phaser 3** | `pixelArt: true` doesn't affect pre-loaded textures | Set config before any scene loads |
| **Phaser 3** | Camera zoom causes sub-pixel issues | Use `roundPixels: true` on camera |
| **Godot 4** | Import filter resets on reimport | Set project default to Nearest |
| **Godot 4** | Viewport scaling can introduce blur | Use "viewport" stretch mode |
| **Unity** | Sprite Editor resets filter on reimport | Create TextureImporter preset |
| **Unity** | Pixel Perfect Camera conflicts with cinemachine | Use PP Camera's own follow logic |
| **PixiJS v8** | `Application()` is now async, requires `await app.init()` | Use `await` pattern; set `TextureStyle.defaultOptions` early |
| **CSS** | `transform: scale()` can trigger anti-aliasing | Use `image-rendering: pixelated` on parent |
