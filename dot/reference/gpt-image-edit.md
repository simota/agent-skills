# GPT Image Edit API Reference

Purpose: comprehensive reference for the OpenAI Image Edit API (`/v1/images/edits`). Covers parameters, model comparison, mask behavior, transparency, prompt engineering for edits, pixel art / spritesheet techniques, and known pitfalls.

## Contents

- [API Parameters](#api-parameters)
- [Model Comparison (Edit Capabilities)](#model-comparison-edit-capabilities)
- [Mask Usage](#mask-usage)
- [Transparent Background](#transparent-background)
- [Input Fidelity](#input-fidelity)
- [Prompt Engineering for Edits](#prompt-engineering-for-edits)
- [Pixel Art & Spritesheet Techniques](#pixel-art--spritesheet-techniques)
- [Common Pitfalls & Workarounds](#common-pitfalls--workarounds)
- [Quality / Cost / Latency Tradeoffs](#quality--cost--latency-tradeoffs)
- [Sources](#sources)

---

## API Parameters

### `images.edit()` — Full Parameter Reference

| Parameter | Type | Required | Values | Default | Notes |
|-----------|------|----------|--------|---------|-------|
| **image** | FileTypes \| FileTypes[] | Yes | PNG, WebP, JPG (<50 MB each) | — | Up to 16 images (GPT models); single square PNG <4 MB (DALL-E 2) |
| **prompt** | str | Yes | max 32,000 chars (GPT); 1,000 (DALL-E 2) | — | Text description of desired output |
| **model** | str | No | `gpt-image-1.5`, `gpt-image-1`, `gpt-image-1-mini`, `dall-e-2` | `gpt-image-1.5` | Edit capabilities differ by model |
| **mask** | FileTypes | No | PNG with alpha channel, same dims as image, <4 MB | — | Transparent areas = editable regions. Applied to first image only |
| **background** | str | No | `transparent`, `opaque`, `auto` | `auto` | GPT models only. Requires PNG or WebP output |
| **input_fidelity** | str | No | `high`, `low` | `low` | GPT models only. High preserves input details at higher token cost |
| **quality** | str | No | `low`, `medium`, `high`, `auto` | `auto` | Higher quality = more tokens = higher cost + latency |
| **size** | str | No | `1024x1024`, `1536x1024`, `1024x1536`, `auto` | `auto` | GPT models. DALL-E 2: `256x256`, `512x512`, `1024x1024` |
| **n** | int | No | 1–10 | 1 | Number of output images |
| **output_format** | str | No | `png`, `jpeg`, `webp` | `png` | GPT models only |
| **output_compression** | int | No | 0–100 | 100 | JPEG/WebP only |
| **partial_images** | int | No | 0–3 | 0 | Streaming partial renders |
| **user** | str | No | — | — | End-user ID for abuse monitoring |

### Basic Usage

```python
from openai import OpenAI
client = OpenAI()

result = client.images.edit(
    model="gpt-image-1",
    image=open("sprite.png", "rb"),
    prompt="Change the character's hat to red",
    input_fidelity="high",
    quality="high",
    background="transparent",
    output_format="png",
    size="1024x1024",
)
```

### Response Shape

```python
result.data[0].b64_json   # base64-encoded image (GPT models always return b64)
result.data[0].url         # URL (DALL-E 2 only, valid 60 min)
result.usage               # token usage (GPT models only)
```

---

## Model Comparison (Edit Capabilities)

| Feature | gpt-image-1.5 | gpt-image-1 | gpt-image-1-mini | dall-e-2 |
|---------|---------------|-------------|-------------------|----------|
| **Edit endpoint** | Yes | Yes | Yes | Yes |
| **Multi-image input** | Up to 16 | Up to 16 | Up to 16 | 1 only |
| **Mask support** | Yes (soft) | Yes (soft) | Yes (soft) | Yes (pixel-level) |
| **background param** | Yes | Yes | Yes | No |
| **input_fidelity** | Yes | Yes | No | No |
| **Consistency Locking** | Yes | Limited | Limited | No |
| **Semantic Locking** | Yes | No | No | No |
| **Grid Consistency** | Yes | Limited | Limited | No |
| **Max prompt** | 32,000 chars | 32,000 chars | 32,000 chars | 1,000 chars |
| **Output sizes** | 1024², 1536×1024, 1024×1536 | same | same | 256², 512², 1024² |
| **Text rendering** | Excellent | Good | Basic | Poor |
| **Speed** | ~4× faster | Baseline | Fast | Fast |

**Key distinction:** DALL-E 2 performs true pixel-level inpainting within masked areas. GPT Image models use a "soft mask" approach — they regenerate the full image while using the mask as guidance, which may cause unintended changes outside the mask.

---

## Mask Usage

### Specification

- **Format:** PNG with alpha channel
- **Size:** Must match input image dimensions exactly
- **Limit:** < 4 MB
- **Behavior:** Transparent regions (alpha = 0) indicate where the model may edit

### Creating a Mask in Python

```python
from PIL import Image
from io import BytesIO

# Load a black-and-white mask
mask_bw = Image.open("mask.png").convert("L")

# Convert to RGBA with alpha channel
mask_rgba = mask_bw.convert("RGBA")
mask_rgba.putalpha(mask_bw)  # white pixels → opaque (keep), black → transparent (edit)

buf = BytesIO()
mask_rgba.save(buf, format="PNG")
mask_bytes = buf.getvalue()
```

### Editing with Mask

```python
result = client.images.edit(
    model="gpt-image-1",
    image=open("input.png", "rb"),
    mask=mask_bytes,
    prompt="Replace the background with a forest scene",
    size="1024x1024",
)
```

### Known Limitation: Soft Mask Behavior

**Problem:** With GPT Image models (`gpt-image-1`, `gpt-image-1.5`), the mask does not perform pixel-level inpainting. Instead, the model performs a "soft mask" with total image recreation — it regenerates the entire image while using the mask as guidance.

**Impact:**
- Areas outside the mask may change unexpectedly
- Fine-grained spatial control at the pixel level is not available
- Contextual coherence issues (background, lighting, pose may shift)

**Mitigation:**
- Use `input_fidelity="high"` to better preserve unmasked regions
- Add explicit preservation language in the prompt: "Keep all areas outside the mask exactly unchanged"
- For true pixel-level inpainting, use `dall-e-2` (limited to 1024×1024, single image)
- Generate the full composition in one request rather than iterative masked edits

---

## Transparent Background

### Configuration

```python
result = client.images.edit(
    model="gpt-image-1",
    image=open("sprite.png", "rb"),
    prompt="Keep the character on a transparent background",
    background="transparent",
    output_format="png",   # required: png or webp
    quality="high",
)
```

### Requirements

| Requirement | Detail |
|-------------|--------|
| `background` | Must be `"transparent"` |
| `output_format` | Must be `"png"` or `"webp"` (JPEG does not support alpha) |
| `quality` | Use `"high"` for best edge quality |

### Known Issue: Transparency Loss in Edits

**Problem:** Early versions of the Edit endpoint lacked `background` parameter support. The source image should already have a transparent background for edits to preserve it reliably.

**Workaround:**
1. Generate the initial image with `background="transparent"` via the Generate endpoint
2. Use that transparent PNG as input for subsequent edits
3. Include transparency preservation language in the prompt
4. Always set `background="transparent"` explicitly in edit requests

---

## Input Fidelity

### High vs Low

| Setting | Behavior | Token Cost | Use When |
|---------|----------|-----------|----------|
| `"low"` (default) | Allows creative reinterpretation of input | Lower | Style transfer, creative edits, major changes |
| `"high"` | Preserves distinctive features and composition | Higher | Face preservation, logo consistency, subtle edits, spritesheet generation |

### Best Practices

- **Always use `"high"` for spritesheet editing** — preserves character identity across frames
- The **first image** in a multi-image request retains the finest detail
- Combine multiple reference elements into a single composite before sending

### Serial Edit Degradation

**Problem:** Consecutive edits (output → input → output → ...) cause progressive quality degradation. After several iterations, images become grainy and unusable, even with PNG format.

**Workarounds:**
- Minimize the number of edit iterations (prefer single-pass generation)
- Always use PNG format between iterations (never JPEG)
- Start new API sessions between edit chains
- Add "Do not modify the original figures or brightness" to prompts
- For animation strips, generate all frames in one request rather than iteratively

---

## Prompt Engineering for Edits

### Structure for Edit Prompts

```
[Intended use] → [Identity lock] → [Composition] → [Action/Change] → [Style] → [Constraints]
```

| Section | Purpose | Example |
|---------|---------|---------|
| **Intended use** | Anchors model to output mode | "production spritesheet for a 2D platformer" |
| **Identity lock** | Exhaustively list visual attributes to preserve | "same red bandana, same blue tunic, same proportions" |
| **Composition** | Canvas size, layout, transparency | "1024×1024 canvas, four 256×256 slots, centered" |
| **Action/Change** | What to modify | "frames 2-4 show a hurt recoil animation" |
| **Style** | Art style constraints | "16-bit pixel art, crisp clusters, stepped shading" |
| **Constraints** | Negative prompting | "no sword, no scenery, no blur, no glow" |

### Preserve vs Change

- State exclusions explicitly: "no watermark," "no extra text," "no extra characters"
- Use "change only X" + "keep everything else the same"
- Repeat preservation lists on each iteration to reduce drift
- Use labeled segments or line breaks for complex prompts

### Multi-Image Referencing

When providing multiple input images:
- Reference each by index: "Image 1: character reference… Image 2: pose reference…"
- Describe interactions: "apply Image 2's pose to Image 1's character"
- Match lighting, perspective, scale, and shadows

---

## Pixel Art & Spritesheet Techniques

### Consistency Locking (gpt-image-1.5)

The ability to maintain character identity and style across multiple generations. Lock:
- Face details, body proportions, color palette, silhouette
- Outfit details (armor, accessories, clothing)
- Art style (pixel density, shading technique)

### Grid Consistency (gpt-image-1.5)

Generate structured layouts where each cell contains a distinct frame without visual interference between cells. Request grids explicitly:

```
"Create a 4-column spritesheet on a 1024×1024 canvas.
Each column is one 256×256 frame slot.
Frame 1: idle pose. Frame 2: wind-up. Frame 3: attack. Frame 4: recovery.
Same character in every frame."
```

### Semantic Locking (gpt-image-1.5)

Localized modifications — adjust a specific element while keeping backgrounds and primary features static. Useful for:
- Changing only a weapon or accessory
- Modifying pose while preserving outfit
- Adjusting expression without altering body

### Spritesheet Generation Prompt Template

```
Intended use: production spritesheet for a 2D [genre] [animation-type] animation.

Edit the provided reference-canvas image into a single horizontal [N]-frame
[animation-type] spritesheet.

The existing sprite in the leftmost slot is the exact shipped [anchor-name]
starting frame: same [detailed attribute list].

Composition: keep transparent background, exactly one row of [N] equal
[slot-size] frame slots left to right across the [canvas-size] canvas,
centered vertically, no overlap, no labels, no UI.

Action: frame 1 stays as [starting pose], frames 2 through [N] show
[frame-by-frame description of animation].

Style: authentic [bit-depth] pixel art, crisp pixel clusters, stepped
shading, restrained palette, production game asset.

Constraints: no [unwanted elements], keep wide transparent empty space
outside frame slots.
```

### Recommended API Parameters for Spritesheets

| Parameter | Value | Reason |
|-----------|-------|--------|
| `model` | `gpt-image-1.5` or `gpt-image-1` | Best consistency features |
| `input_fidelity` | `"high"` | Preserve character identity from reference |
| `background` | `"transparent"` | Game-ready with alpha channel |
| `quality` | `"high"` | Best detail preservation for pixel art |
| `output_format` | `"png"` | Lossless + transparency support |
| `size` | `"1024x1024"` | Optimal for 4-slot spritesheet (256px per slot) |

---

## Common Pitfalls & Workarounds

| Pitfall | Symptom | Workaround |
|---------|---------|------------|
| **Mask ignored** | Entire image regenerated, not just masked area | Use `input_fidelity="high"`, add preservation language in prompt; for pixel-precise inpainting use `dall-e-2` |
| **Serial edit degradation** | Grainy, noisy output after 3+ consecutive edits | Generate all frames in one request; minimize edit chains; always use PNG |
| **Transparency loss** | White/opaque background instead of transparent | Set `background="transparent"` + `output_format="png"`; ensure input already has transparency |
| **Consistency drift** | Character changes between frames (proportions, colors) | Use `input_fidelity="high"`, exhaustive identity lock in prompt, generate full strip at once |
| **Frame overlap** | Sprites bleed into adjacent frame slots | Specify exact slot dimensions and "no overlap between frame slots" in prompt |
| **Style escalation** | Model adds detail beyond pixel art (smoothing, gradients) | Add "crisp pixel clusters, no anti-aliasing, no smooth shading, no gradients" |
| **Unwanted elements** | Extra characters, labels, UI elements, backgrounds | Explicit negative constraints: "no labels, no UI, no extra characters, no scenery" |
| **Size mismatch** | Output frames have inconsistent sizes | Post-process with normalization script; use one global scale factor |
| **Text in sprites** | Model adds text labels to frame slots | "no text, no labels, no numbers, no annotations" |

---

## Quality / Cost / Latency Tradeoffs

| quality | input_fidelity | Relative Cost | Latency | Best For |
|---------|---------------|---------------|---------|----------|
| `low` | `low` | Lowest | Fastest | Rapid prototyping, layout testing |
| `medium` | `low` | Low | Fast | Iteration, exploring compositions |
| `high` | `low` | Medium | Medium | Final output with creative freedom |
| `low` | `high` | Medium | Fast | Quick edits preserving identity |
| `high` | `high` | Highest | Slowest | Production spritesheets, face/logo preservation |

**Token cost note:** Both latency and cost are proportional to the number of tokens required to render an image. Larger sizes and higher quality settings consume more tokens.

---

## Sources

- [OpenAI Images API Reference — createEdit](https://platform.openai.com/docs/api-reference/images/createEdit)
- [OpenAI Image Generation Guide](https://developers.openai.com/api/docs/guides/image-generation/)
- [Generate Images with High Input Fidelity — OpenAI Cookbook](https://developers.openai.com/cookbook/examples/generate_images_with_high_input_fidelity/)
- [GPT Image 1.5 Prompting Guide — OpenAI Cookbook](https://developers.openai.com/cookbook/examples/multimodal/image-gen-1.5-prompting_guide)
- [GPT Image 1.5 Prompt Guide — fal.ai](https://fal.ai/learn/devs/gpt-image-1-5-prompt-guide)
- [GPT Image 1.5 — The Essentials — Scenario](https://help.scenario.com/en/articles/gpt-image-1-5-the-essentials/)
- [GPT Image API — OpenAI Help Center](https://help.openai.com/en/articles/11128753-gpt-image-api)
- [Mask Inpainting Limitation — OpenAI Community](https://community.openai.com/t/image-editing-inpainting-with-a-mask-for-gpt-image-1-replaces-the-entire-image/1244275)
- [Serial Edit Degradation — OpenAI Community](https://community.openai.com/t/multiple-gpt-image-1-high-fidelity-edits-lead-to-grainy-result/1320474)
- [Transparent Background — OpenAI Community](https://community.openai.com/t/gpt-image-1-transparent-background-edit-request/)
