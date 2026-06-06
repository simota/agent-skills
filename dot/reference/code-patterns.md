# Code Patterns Reference

Purpose: load this when implementing the selected output format. It keeps templates and optimization patterns for SVG, Canvas, Phaser 3, Pillow, and CSS in one place.

## Contents

- [Approach 1: SVG `<rect>` Grid](#approach-1-svg-rect-grid)
- [Approach 2: HTML Canvas](#approach-2-html-canvas)
- [Approach 3: Phaser 3 `generateTexture()`](#approach-3-phaser-3-generatetexture)
- [Approach 4: Python + Pillow](#approach-4-python--pillow)
- [Approach 5: CSS `box-shadow`](#approach-5-css-box-shadow)
- [Grid Data Format](#grid-data-format)
- [Approach Selection Guide](#approach-selection-guide)
- [Common Patterns](#common-patterns)

## Approach 1: SVG `<rect>` Grid

### Basic Template

```xml
<svg xmlns="http://www.w3.org/2000/svg"
     viewBox="0 0 {WIDTH} {HEIGHT}"
     width="{WIDTH * SCALE}" height="{HEIGHT * SCALE}"
     shape-rendering="crispEdges"
     style="image-rendering: pixelated;">
  <!-- Palette: {PALETTE_NAME} -->
  <!-- Row 0 -->
  <rect x="0" y="0" width="1" height="1" fill="#1a1c2c"/>
  <rect x="1" y="0" width="1" height="1" fill="#5d275d"/>
  <!-- ... -->
</svg>
```

### Generator Function (JavaScript)

```javascript
function generateSVG(grid, palette, scale = 4) {
  const h = grid.length;
  const w = grid[0].length;
  let svg = `<svg xmlns="http://www.w3.org/2000/svg" ` +
    `viewBox="0 0 ${w} ${h}" ` +
    `width="${w * scale}" height="${h * scale}" ` +
    `shape-rendering="crispEdges" ` +
    `style="image-rendering: pixelated;">\n`;

  // Palette comment
  svg += `  <!-- Palette: ${palette.map((c, i) => `${i}=${c}`).join(', ')} -->\n`;

  for (let y = 0; y < h; y++) {
    svg += `  <!-- Row ${y} -->\n`;
    for (let x = 0; x < w; x++) {
      const colorIndex = grid[y][x];
      if (colorIndex >= 0) { // -1 = transparent
        svg += `  <rect x="${x}" y="${y}" width="1" height="1" fill="${palette[colorIndex]}"/>\n`;
      }
    }
  }
  svg += `</svg>`;
  return svg;
}
```

### Optimization 1: Run-Length Encoding (Row Runs)

Merge consecutive same-color pixels into wider rects. Reduces element count by 40-70%.

```javascript
function generateSVGRunLength(grid, palette, scale = 4) {
  const h = grid.length;
  const w = grid[0].length;
  let rects = [];

  for (let y = 0; y < h; y++) {
    let x = 0;
    while (x < w) {
      const c = grid[y][x];
      if (c < 0) { x++; continue; }
      let run = 1;
      while (x + run < w && grid[y][x + run] === c) run++;
      rects.push(`  <rect x="${x}" y="${y}" width="${run}" height="1" fill="${palette[c]}"/>`);
      x += run;
    }
  }

  return `<svg xmlns="http://www.w3.org/2000/svg" ` +
    `viewBox="0 0 ${w} ${h}" width="${w * scale}" height="${h * scale}" ` +
    `shape-rendering="crispEdges" style="image-rendering: pixelated;">\n` +
    rects.join('\n') + `\n</svg>`;
}
```

### Optimization 2: Color Grouping

Group rects by color using `<g>` elements. Reduces `fill` attribute repetition.

```javascript
function generateSVGColorGrouped(grid, palette, scale = 4) {
  const h = grid.length;
  const w = grid[0].length;

  // Collect rects per color
  const colorGroups = {};
  for (let y = 0; y < h; y++) {
    let x = 0;
    while (x < w) {
      const c = grid[y][x];
      if (c < 0) { x++; continue; }
      let run = 1;
      while (x + run < w && grid[y][x + run] === c) run++;
      if (!colorGroups[c]) colorGroups[c] = [];
      colorGroups[c].push({ x, y, w: run });
      x += run;
    }
  }

  let svg = `<svg xmlns="http://www.w3.org/2000/svg" ` +
    `viewBox="0 0 ${w} ${h}" width="${w * scale}" height="${h * scale}" ` +
    `shape-rendering="crispEdges" style="image-rendering: pixelated;">\n`;

  for (const [colorIdx, rects] of Object.entries(colorGroups)) {
    svg += `  <g fill="${palette[colorIdx]}">\n`;
    for (const r of rects) {
      svg += `    <rect x="${r.x}" y="${r.y}" width="${r.w}" height="1"/>\n`;
    }
    svg += `  </g>\n`;
  }

  svg += `</svg>`;
  return svg;
}
```

### Optimization 3: 2D Rectangle Merging

Merge adjacent same-color rectangles both horizontally and vertically. Maximum compression.

```javascript
function generateSVG2DMerge(grid, palette, scale = 4) {
  const h = grid.length;
  const w = grid[0].length;
  const visited = Array.from({ length: h }, () => Array(w).fill(false));
  const rects = [];

  for (let y = 0; y < h; y++) {
    for (let x = 0; x < w; x++) {
      if (visited[y][x] || grid[y][x] < 0) continue;
      const c = grid[y][x];

      // Find max width of run
      let rw = 1;
      while (x + rw < w && grid[y][x + rw] === c && !visited[y][x + rw]) rw++;

      // Extend downward while full row matches
      let rh = 1;
      outer: while (y + rh < h) {
        for (let dx = 0; dx < rw; dx++) {
          if (grid[y + rh][x + dx] !== c || visited[y + rh][x + dx]) break outer;
        }
        rh++;
      }

      // Mark visited
      for (let dy = 0; dy < rh; dy++) {
        for (let dx = 0; dx < rw; dx++) {
          visited[y + dy][x + dx] = true;
        }
      }

      rects.push(`  <rect x="${x}" y="${y}" width="${rw}" height="${rh}" fill="${palette[c]}"/>`);
    }
  }

  return `<svg xmlns="http://www.w3.org/2000/svg" ` +
    `viewBox="0 0 ${w} ${h}" width="${w * scale}" height="${h * scale}" ` +
    `shape-rendering="crispEdges" style="image-rendering: pixelated;">\n` +
    rects.join('\n') + `\n</svg>`;
}
```

### SVG Animation (CSS Keyframes)

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" width="256" height="256"
     shape-rendering="crispEdges" style="image-rendering: pixelated;">
  <style>
    .blink { animation: blink-anim 2s steps(1) infinite; }
    @keyframes blink-anim {
      0%, 90% { opacity: 1; }
      95% { opacity: 0; }
    }
  </style>
  <!-- Static elements -->
  <rect x="4" y="3" width="1" height="1" fill="#1a1c2c"/>
  <!-- Blinking eyes -->
  <g class="blink">
    <rect x="5" y="5" width="1" height="1" fill="#e8d053"/>
    <rect x="8" y="5" width="1" height="1" fill="#e8d053"/>
  </g>
</svg>
```

### SVG Validation

```javascript
function validateSVG(svgString, expectedWidth, expectedHeight) {
  const errors = [];

  // Check required attributes
  if (!svgString.includes('shape-rendering="crispEdges"'))
    errors.push('Missing shape-rendering="crispEdges"');
  if (!svgString.includes('image-rendering: pixelated'))
    errors.push('Missing image-rendering: pixelated');

  // Check for sub-pixel coordinates
  const rectPattern = /<rect[^>]*x="([^"]*)"[^>]*y="([^"]*)"[^>]*/g;
  let match;
  while ((match = rectPattern.exec(svgString)) !== null) {
    const x = parseFloat(match[1]);
    const y = parseFloat(match[2]);
    if (x !== Math.floor(x) || y !== Math.floor(y))
      errors.push(`Sub-pixel coordinate: x=${x}, y=${y}`);
  }

  // Check viewBox
  const vb = svgString.match(/viewBox="0 0 (\d+) (\d+)"/);
  if (vb) {
    if (parseInt(vb[1]) !== expectedWidth || parseInt(vb[2]) !== expectedHeight)
      errors.push(`viewBox mismatch: expected ${expectedWidth}x${expectedHeight}`);
  } else {
    errors.push('Missing or malformed viewBox');
  }

  return { valid: errors.length === 0, errors };
}
```

---

## Approach 2: HTML Canvas

### Basic Template

```html
<!DOCTYPE html>
<html>
<head>
  <title>{SPRITE_NAME} - Pixel Art</title>
  <style>
    canvas {
      image-rendering: pixelated;
      image-rendering: crisp-edges;
      border: 1px solid #333;
    }
  </style>
</head>
<body>
  <canvas id="sprite" width="{WIDTH}" height="{HEIGHT}"></canvas>
  <script>
    const PALETTE = ["{COLOR_0}", "{COLOR_1}", /* ... */];
    const GRID = [
      [0, 1, 2, /* ... */],
      // ...
    ];
    const SCALE = 8;
    const canvas = document.getElementById('sprite');
    const ctx = canvas.getContext('2d');

    // Disable anti-aliasing
    ctx.imageSmoothingEnabled = false;

    // Scale canvas for display
    canvas.style.width = `${canvas.width * SCALE}px`;
    canvas.style.height = `${canvas.height * SCALE}px`;

    // Draw pixels
    GRID.forEach((row, y) => {
      row.forEach((colorIndex, x) => {
        if (colorIndex >= 0) {
          ctx.fillStyle = PALETTE[colorIndex];
          ctx.fillRect(x, y, 1, 1);
        }
      });
    });
  </script>
</body>
</html>
```

### ImageData Direct Manipulation (Faster)

For larger sprites, direct ImageData manipulation is significantly faster than fillRect.

```javascript
function drawGridFast(ctx, grid, palette, width, height) {
  const imageData = ctx.createImageData(width, height);
  const data = imageData.data;

  // Pre-parse palette to RGBA arrays
  const rgbPalette = palette.map(hex => {
    const h = hex.replace('#', '');
    return [
      parseInt(h.substring(0, 2), 16),
      parseInt(h.substring(2, 4), 16),
      parseInt(h.substring(4, 6), 16),
      255,
    ];
  });

  for (let y = 0; y < height; y++) {
    for (let x = 0; x < width; x++) {
      const ci = grid[y][x];
      if (ci >= 0) {
        const idx = (y * width + x) * 4;
        const [r, g, b, a] = rgbPalette[ci];
        data[idx] = r;
        data[idx + 1] = g;
        data[idx + 2] = b;
        data[idx + 3] = a;
      }
    }
  }

  ctx.putImageData(imageData, 0, 0);
}
```

### OffscreenCanvas (Web Worker Compatible)

For batch rendering or heavy pixel operations without blocking the main thread.

```javascript
// Main thread
const offscreen = new OffscreenCanvas(16, 16);
const ctx = offscreen.getContext('2d');
ctx.imageSmoothingEnabled = false;

// Draw using ImageData
drawGridFast(ctx, grid, palette, 16, 16);

// Convert to Blob for download
offscreen.convertToBlob({ type: 'image/png' }).then(blob => {
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = 'sprite.png';
  a.click();
  URL.revokeObjectURL(url);
});
```

### Canvas PNG Export

```javascript
function exportPNG(canvas, filename, scale = 1) {
  if (scale > 1) {
    // Create scaled canvas
    const scaled = document.createElement('canvas');
    scaled.width = canvas.width * scale;
    scaled.height = canvas.height * scale;
    const sCtx = scaled.getContext('2d');
    sCtx.imageSmoothingEnabled = false;
    sCtx.drawImage(canvas, 0, 0, scaled.width, scaled.height);
    canvas = scaled;
  }

  // Method 1: toDataURL
  const dataUrl = canvas.toDataURL('image/png');

  // Method 2: toBlob (recommended for large images)
  canvas.toBlob(blob => {
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    a.click();
    URL.revokeObjectURL(url);
  }, 'image/png');
}
```

### Canvas Animation (Spritesheet Playback)

```javascript
function animateSprite(ctx, spritesheet, frameWidth, frameHeight, frames, fps) {
  let currentFrame = 0;
  const interval = 1000 / fps;
  const cols = spritesheet.width / frameWidth;

  function render() {
    const frameIndex = frames[currentFrame];
    const sx = (frameIndex % cols) * frameWidth;
    const sy = Math.floor(frameIndex / cols) * frameHeight;

    ctx.clearRect(0, 0, frameWidth, frameHeight);
    ctx.drawImage(spritesheet, sx, sy, frameWidth, frameHeight, 0, 0, frameWidth, frameHeight);

    currentFrame = (currentFrame + 1) % frames.length;
  }

  setInterval(render, interval);
}
```

---

## Approach 3: Phaser 3 `generateTexture()`

### Basic Template

```javascript
function createPixelTexture(scene, key, grid, palette, scale = 1) {
  const h = grid.length;
  const w = grid[0].length;
  const graphics = scene.make.graphics({ x: 0, y: 0, add: false });

  grid.forEach((row, y) => {
    row.forEach((colorIndex, x) => {
      if (colorIndex >= 0) {
        const color = parseInt(palette[colorIndex].replace('#', ''), 16);
        graphics.fillStyle(color);
        graphics.fillRect(x * scale, y * scale, scale, scale);
      }
    });
  });

  graphics.generateTexture(key, w * scale, h * scale);
  graphics.destroy();
}

// Usage in scene.create()
const palette = ['#1a1c2c', '#5d275d', '#b13e53', '#ef7d57'];
const heroGrid = [
  [-1,  0,  0, -1],
  [ 0,  1,  2,  0],
  [ 0,  2,  3,  0],
  [-1,  0,  0, -1],
];
createPixelTexture(this, 'hero', heroGrid, palette);
const hero = this.add.sprite(100, 100, 'hero');
```

### Animated Sprite from Grid Frames

```javascript
function createSpritesheet(scene, key, frames, palette, frameWidth, frameHeight) {
  const cols = frames.length;
  const graphics = scene.make.graphics({ x: 0, y: 0, add: false });

  frames.forEach((grid, frameIndex) => {
    const offsetX = frameIndex * frameWidth;
    grid.forEach((row, y) => {
      row.forEach((colorIndex, x) => {
        if (colorIndex >= 0) {
          const color = parseInt(palette[colorIndex].replace('#', ''), 16);
          graphics.fillStyle(color);
          graphics.fillRect(offsetX + x, y, 1, 1);
        }
      });
    });
  });

  graphics.generateTexture(key, frameWidth * cols, frameHeight);
  graphics.destroy();

  // Add frames to texture
  const texture = scene.textures.get(key);
  for (let i = 0; i < cols; i++) {
    texture.add(i, 0, i * frameWidth, 0, frameWidth, frameHeight);
  }
}
```

### Phaser 3 Config for Pixel Art

```javascript
const config = {
  type: Phaser.AUTO,
  pixelArt: true,            // Disables anti-aliasing globally
  roundPixels: true,          // Snap to integer positions
  scale: {
    mode: Phaser.Scale.FIT,
    width: 320,               // Low-res game canvas
    height: 180,
    zoom: Phaser.Scale.MAX_ZOOM,
  },
  scene: { preload, create, update },
};
```

### Phaser 3 Palette Swap Shader

```javascript
// Fragment shader for palette swapping
const PALETTE_SWAP_FRAG = `
precision mediump float;
uniform sampler2D uMainSampler;
uniform vec3 originalColors[8];
uniform vec3 newColors[8];
uniform int colorCount;
varying vec2 outTexCoord;

void main() {
  vec4 color = texture2D(uMainSampler, outTexCoord);
  for (int i = 0; i < 8; i++) {
    if (i >= colorCount) break;
    if (distance(color.rgb, originalColors[i]) < 0.01) {
      gl_FragColor = vec4(newColors[i], color.a);
      return;
    }
  }
  gl_FragColor = color;
}
`;
```

---

## Approach 4: Python + Pillow

### Basic Template

```python
from PIL import Image

def hex_to_rgb(hex_color):
    """Convert '#RRGGBB' to (R, G, B) tuple."""
    h = hex_color.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def create_sprite(grid, palette, scale=1):
    """Generate a pixel art sprite from grid and palette."""
    h = len(grid)
    w = len(grid[0])
    img = Image.new('RGBA', (w, h), (0, 0, 0, 0))

    for y, row in enumerate(grid):
        for x, color_index in enumerate(row):
            if color_index >= 0:
                r, g, b = hex_to_rgb(palette[color_index])
                img.putpixel((x, y), (r, g, b, 255))

    if scale > 1:
        img = img.resize((w * scale, h * scale), Image.Resampling.NEAREST)

    return img
```

### Palette Mode (P Mode) -- Indexed Color

Use Pillow's P mode for true indexed-color images, matching retro hardware behavior.

```python
from PIL import Image

def create_indexed_sprite(grid, palette):
    """Create a palette-indexed (P mode) PNG."""
    h = len(grid)
    w = len(grid[0])
    img = Image.new('P', (w, h))

    # Build palette (flat RGB list: [R0, G0, B0, R1, G1, B1, ...])
    flat_palette = []
    for hex_color in palette:
        r, g, b = hex_to_rgb(hex_color)
        flat_palette.extend([r, g, b])
    # Pad to 256 colors (768 bytes total)
    flat_palette.extend([0] * (768 - len(flat_palette)))
    img.putpalette(flat_palette)

    # Set pixels (index values directly)
    for y, row in enumerate(grid):
        for x, color_index in enumerate(row):
            if color_index >= 0:
                img.putpixel((x, y), color_index)

    return img

# Usage
palette = ['#1a1c2c', '#5d275d', '#b13e53', '#ef7d57']
sprite = create_indexed_sprite(grid, palette)
sprite.save('sprite_indexed.png')
```

### Palette Remapping

Swap palettes on existing images -- useful for recoloring enemies, team colors, etc.

```python
from PIL import Image

def remap_palette(img, original_palette, new_palette):
    """Remap colors in an RGBA image from one palette to another."""
    pixels = img.load()
    w, h = img.size

    # Build color mapping
    color_map = {}
    for orig, new in zip(original_palette, new_palette):
        color_map[hex_to_rgb(orig)] = hex_to_rgb(new)

    for y in range(h):
        for x in range(w):
            r, g, b, a = pixels[x, y]
            if a > 0 and (r, g, b) in color_map:
                nr, ng, nb = color_map[(r, g, b)]
                pixels[x, y] = (nr, ng, nb, a)

    return img

# Usage: recolor goblin from green to blue
original = ['#2d5a1e', '#4a8c3f', '#7bc24e']
blue_variant = ['#1e3a5d', '#3f6a8c', '#4e9bc2']
recolored = remap_palette(goblin_img.copy(), original, blue_variant)
```

### Spritesheet Generation

```python
from PIL import Image

def create_spritesheet(frames, palette, frame_width, frame_height, cols=None, scale=1):
    """Pack multiple frames into a spritesheet."""
    if cols is None:
        cols = len(frames)
    rows = (len(frames) + cols - 1) // cols
    sheet = Image.new('RGBA', (frame_width * cols, frame_height * rows), (0, 0, 0, 0))

    for i, grid in enumerate(frames):
        frame = create_sprite(grid, palette)
        x = (i % cols) * frame_width
        y = (i // cols) * frame_height
        sheet.paste(frame, (x, y))

    if scale > 1:
        new_size = (sheet.width * scale, sheet.height * scale)
        sheet = sheet.resize(new_size, Image.NEAREST)

    return sheet
```

### GIF Animation

```python
from PIL import Image

def create_gif(frames, palette, fps=8, scale=4, output='animation.gif',
               transparent_color=None):
    """Create animated GIF from pixel art frames."""
    images = []
    for grid in frames:
        frame = create_sprite(grid, palette, scale=scale)
        # Convert RGBA to P mode for GIF with transparency
        if transparent_color is not None:
            frame = frame.convert('RGBA')
            bg = Image.new('RGBA', frame.size, transparent_color)
            bg.paste(frame, (0, 0), frame)
            frame = bg
        images.append(frame.convert('RGB'))

    duration = int(1000 / fps)
    images[0].save(
        output,
        save_all=True,
        append_images=images[1:],
        duration=duration,
        loop=0,
        disposal=2,  # clear frame before drawing next
    )
```

### APNG Animation (Better Quality)

```python
from PIL import Image

def create_apng(frames, palette, fps=8, scale=4, output='animation.png'):
    """Create animated PNG (APNG) -- supports transparency unlike GIF."""
    images = []
    for grid in frames:
        frame = create_sprite(grid, palette, scale=scale)
        images.append(frame)

    duration = int(1000 / fps)
    images[0].save(
        output,
        save_all=True,
        append_images=images[1:],
        duration=duration,
        loop=0,
    )
```

### Batch Export

```python
import json
from pathlib import Path

def batch_export(sprites, palette, output_dir, scale=4):
    """Export multiple sprites with metadata manifest."""
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)

    manifest = {"palette": palette, "scale": scale, "sprites": []}

    for name, grid in sprites.items():
        img = create_sprite(grid, palette, scale=scale)
        filepath = output / f"{name}.png"
        img.save(filepath)
        manifest["sprites"].append({
            "name": name,
            "file": f"{name}.png",
            "width": len(grid[0]),
            "height": len(grid),
        })

    with open(output / "manifest.json", "w") as f:
        json.dump(manifest, f, indent=2)
```

### Pillow Dithering

```python
from PIL import Image

def apply_ordered_dither(img, palette_img):
    """Apply ordered (Bayer) dithering to reduce colors."""
    return img.convert('RGB').quantize(
        palette=palette_img,
        dither=Image.Dither.NONE  # For clean pixel art
    )

def reduce_colors(img, num_colors, dither=False):
    """Reduce image to N colors with optional dithering."""
    method = Image.Dither.FLOYDSTEINBERG if dither else Image.Dither.NONE
    return img.convert('RGB').quantize(colors=num_colors, dither=method)
```

---

## Approach 5: CSS `box-shadow`

### Basic Template

```css
.pixel-sprite {
  width: 1px;
  height: 1px;
  transform: scale({SCALE});
  transform-origin: top left;
  box-shadow:
    /* x  y  color -- each pixel is a shadow */
    0px 0px #1a1c2c,
    1px 0px #5d275d,
    2px 0px #1a1c2c,
    0px 1px #b13e53,
    1px 1px #ef7d57,
    2px 1px #b13e53;
  /* ... */
}
```

### Generator Function

```javascript
function generateCSSSprite(grid, palette, scale = 8) {
  const shadows = [];

  grid.forEach((row, y) => {
    row.forEach((colorIndex, x) => {
      if (colorIndex >= 0) {
        shadows.push(`${x}px ${y}px ${palette[colorIndex]}`);
      }
    });
  });

  return `.pixel-sprite {
  width: 1px;
  height: 1px;
  transform: scale(${scale});
  transform-origin: top left;
  box-shadow:
    ${shadows.join(',\n    ')};
}`;
}
```

### CSS Grid Approach (Alternative)

For larger sprites, CSS Grid can be more performant than box-shadow.

```javascript
function generateCSSGrid(grid, palette, pixelSize = 4) {
  const h = grid.length;
  const w = grid[0].length;
  let cells = '';

  grid.forEach((row, y) => {
    row.forEach((colorIndex, x) => {
      if (colorIndex >= 0) {
        cells += `  .pixel-sprite > div:nth-child(${y * w + x + 1}) { background: ${palette[colorIndex]}; }\n`;
      }
    });
  });

  return `.pixel-sprite {
  display: grid;
  grid-template-columns: repeat(${w}, ${pixelSize}px);
  grid-template-rows: repeat(${h}, ${pixelSize}px);
  gap: 0;
  image-rendering: pixelated;
}
.pixel-sprite > div {
  width: ${pixelSize}px;
  height: ${pixelSize}px;
}
${cells}`;
}
```

### CSS Custom Properties for Palette

```css
:root {
  --pixel-outline: #1a1c2c;
  --pixel-base: #5d275d;
  --pixel-highlight: #b13e53;
  --pixel-accent: #ef7d57;
}

.pixel-sprite {
  box-shadow:
    0px 0px var(--pixel-outline),
    1px 0px var(--pixel-base),
    2px 0px var(--pixel-highlight);
}

/* Palette swap via custom properties */
.pixel-sprite.blue-variant {
  --pixel-base: #3b5dc9;
  --pixel-highlight: #41a6f6;
  --pixel-accent: #73eff7;
}
```

### CSS Animation (Multi-frame)

```css
.pixel-sprite-animated {
  width: 1px;
  height: 1px;
  transform: scale(8);
  transform-origin: top left;
  animation: sprite-anim 0.5s steps(1) infinite;
}

@keyframes sprite-anim {
  0%   { box-shadow: /* frame 0 shadows */; }
  33%  { box-shadow: /* frame 1 shadows */; }
  66%  { box-shadow: /* frame 2 shadows */; }
}
```

---

## Grid Data Format

All approaches share the same grid format:

```javascript
// 2D array: rows x columns
// Value = palette index, -1 = transparent
const grid = [
  [-1,  0,  0, -1],  // row 0
  [ 0,  1,  2,  0],  // row 1
  [ 0,  2,  3,  0],  // row 2
  [-1,  0,  0, -1],  // row 3
];
```

### Python equivalent

```python
grid = [
    [-1,  0,  0, -1],
    [ 0,  1,  2,  0],
    [ 0,  2,  3,  0],
    [-1,  0,  0, -1],
]
```

---

## Approach Selection Guide

| Criteria | SVG | Canvas | Phaser 3 | Pillow | CSS |
|----------|-----|--------|----------|--------|-----|
| Dependencies | None | None | CDN | pip | None |
| Scalability | Excellent | Good | Good | Excellent | Poor (>32x32) |
| Animation | CSS/SMIL | JS | Built-in | GIF/APNG | CSS |
| Interactivity | Limited | Full | Full | None | Limited |
| Export | Direct | PNG/Blob | In-engine | PNG/GIF | N/A |
| Batch processing | No | Limited | No | Excellent | No |
| Game integration | No | Possible | Native | Export only | No |
| Best sprite size | Any | Any | Any | Any | <=16x16 |
| File size | Small-Medium | HTML wrapping | JS wrapping | Script | Small |

### Decision Flowchart

```
Need game engine integration?
  Yes -> Phaser 3 / generateTexture()
  No ->
    Need batch export or GIF?
      Yes -> Python + Pillow
      No ->
        Need interactivity?
          Yes -> HTML Canvas
          No ->
            Sprite size > 16x16?
              Yes -> SVG
              No ->
                Prefer no-file solution?
                  Yes -> CSS box-shadow
                  No -> SVG
```

---

## Common Patterns

### Heart (8x8)

```javascript
const HEART = [
  [-1,  1,  1, -1, -1,  1,  1, -1],
  [ 1,  2,  3,  1,  1,  2,  3,  1],
  [ 1,  3,  3,  3,  3,  3,  3,  1],
  [ 1,  3,  3,  3,  3,  3,  3,  1],
  [-1,  1,  3,  3,  3,  3,  1, -1],
  [-1, -1,  1,  3,  3,  1, -1, -1],
  [-1, -1, -1,  1,  1, -1, -1, -1],
  [-1, -1, -1, -1, -1, -1, -1, -1],
];
// 0=unused, 1=outline(#1a1c2c), 2=highlight(#ef7d57), 3=base(#b13e53)
```

### Sword (8x16)

```javascript
const SWORD = [
  [-1, -1, -1, -1, -1, -1,  2, -1],
  [-1, -1, -1, -1, -1,  2,  1,  2],
  [-1, -1, -1, -1,  2,  1,  2, -1],
  [-1, -1, -1,  2,  1,  2, -1, -1],
  [-1, -1,  2,  1,  2, -1, -1, -1],
  [-1,  3,  0,  1,  0, -1, -1, -1],
  [-1, -1,  3,  0,  3, -1, -1, -1],
  [-1, -1,  3,  0,  3, -1, -1, -1],
];
// 0=metal(#9badb7), 1=edge(#ffffff), 2=glow(#41a6f6), 3=handle(#8f563b)
```

### Coin (8x8, 4 animation frames)

```javascript
const COIN_FRAMES = [
  // Frame 0: full face
  [[-1, 0, 0, 0, 0, 0, 0,-1],
   [ 0, 1, 1, 1, 1, 1, 1, 0],
   [ 0, 1, 2, 1, 1, 2, 1, 0],
   [ 0, 1, 1, 1, 1, 1, 1, 0],
   [ 0, 1, 1, 2, 2, 1, 1, 0],
   [ 0, 1, 1, 1, 1, 1, 1, 0],
   [ 0, 3, 3, 3, 3, 3, 3, 0],
   [-1, 0, 0, 0, 0, 0, 0,-1]],
  // Frame 1: 3/4 turn
  [[-1,-1, 0, 0, 0, 0,-1,-1],
   [-1, 0, 1, 1, 1, 1, 0,-1],
   [-1, 0, 1, 2, 1, 1, 0,-1],
   [-1, 0, 1, 1, 1, 1, 0,-1],
   [-1, 0, 1, 2, 2, 1, 0,-1],
   [-1, 0, 1, 1, 1, 1, 0,-1],
   [-1, 0, 3, 3, 3, 3, 0,-1],
   [-1,-1, 0, 0, 0, 0,-1,-1]],
  // Frame 2: edge
  [[-1,-1,-1, 0, 0,-1,-1,-1],
   [-1,-1,-1, 0, 0,-1,-1,-1],
   [-1,-1,-1, 0, 0,-1,-1,-1],
   [-1,-1,-1, 0, 0,-1,-1,-1],
   [-1,-1,-1, 0, 0,-1,-1,-1],
   [-1,-1,-1, 0, 0,-1,-1,-1],
   [-1,-1,-1, 0, 0,-1,-1,-1],
   [-1,-1,-1, 0, 0,-1,-1,-1]],
  // Frame 3: 3/4 reverse (same as frame 1)
];
// 0=outline(#1a1c2c), 1=gold(#e8d053), 2=highlight(#f4f4f4), 3=shadow(#a66940)
```
