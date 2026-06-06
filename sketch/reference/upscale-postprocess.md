# Upscale & Post-Process Reference

Purpose: Ship print-ready or retina-grade outputs from Gemini renders via upscaling, masked inpainting, outpainting, and final format selection. Invoke when the base generation is approved but the raster is too small, has a localized artifact, or needs canvas extension before handoff.

## Scope Boundary

- **sketch `upscale`**: upscaler choice, mask authoring, inpainting prompts, artifact detection heuristics, export format tradeoffs (WebP / AVIF / PNG / JPEG).
- **sketch `generate` / `batch` (siblings)**: produce the base raster. Do not upscale at generation time — render at native ceiling first (1K / 2K / 4K), then post-process if needed.
- **Artisan (elsewhere)**: picks the final format per surface (web / app / print) and wires it into components.
- **Muse (elsewhere)**: if the post-processed asset is a token (icon / hero), Muse registers it.

If the issue is "image is too small" → `upscale`. If "wrong subject" → re-run `generate` with a new prompt, not inpainting.

## Workflow

```
INSPECT    →  read base image: dimensions, artifact map, safe margins
           →  decide: upscale only / inpaint region / outpaint canvas / multi
           →  confirm color space (sRGB for web, Display P3 only if warranted)

CHOOSE     →  pick upscaler (see "Upscaler Choice")
           →  set target: 2x / 4x, target DPI for print (300 dpi)
           →  author mask if inpainting (see "Mask Authoring")

PROCESS    →  run upscaler; for inpainting, re-prompt Gemini with mask + source
           →  verify no new artifacts introduced (see "Artifact Detection")

EXPORT     →  pick format (see "Export Formats")
           →  strip EXIF unless provenance matters; preserve SynthID note
           →  write sidecar metadata.json with tool versions + params
```

## Upscaler Choice

| Tool | Strength | Cost | Use when |
|------|----------|------|----------|
| Real-ESRGAN (`RealESRGAN_x4plus`) | Free, local, general-purpose | GPU time | Default 2x–4x; illustrations and photos |
| Real-ESRGAN anime (`x4plus_anime_6B`) | Flat / cel styles | GPU time | Vector-like or anime outputs |
| Topaz Gigapixel / Photo AI | Highest quality for photos | Paid license | Print-ready photography, faces |
| Gemini native (regenerate @ 4K) | Same model, no seam | API cost (~$0.24 @ 4K) | Base render was 1K–2K; re-run is cheaper than post-process |
| SwinIR / HAT | Research-grade, sharper | GPU time | When Real-ESRGAN oversmooths detail |

Default: **regenerate at Nano Banana 2 / Pro 4K** if the base prompt is still valid — avoids upscaler hallucinations. Fall back to Real-ESRGAN when the base is fixed or regeneration is budget-blocked.

```python
# Real-ESRGAN CLI invocation (illustrative)
# pip install realesrgan
# realesrgan-ncnn-vulkan -i base.png -o out_4x.png -n realesrgan-x4plus -s 4
```

## Mask Authoring

Inpainting needs a mask that marks "change here, keep everything else". Three authoring paths:

1. **Alpha channel**: open in GIMP / Photoshop, paint transparent over the region, export PNG-RGBA. Transparent = editable.
2. **Separate grayscale PNG**: white = editable, black = keep. Same dimensions as source.
3. **SVG → raster**: author mask as SVG `<rect>` / `<path>`, rasterize at source resolution. Reproducible and versionable.

```python
# Example: SVG mask → PNG at source resolution
import cairosvg, pathlib

cairosvg.svg2png(
    url="mask.svg",
    write_to="mask.png",
    output_width=1024,
    output_height=1024,
)
```

Rule: feather the mask edge by 4–8 px. Hard edges produce visible seams after inpainting.

## Inpainting Prompt Strategy

Gemini-native inpainting via reference: send source + mask + targeted edit prompt. Keep the edit prompt narrow — describe only the region.

```
EDIT: within the masked region only, replace the coffee cup with a glass of water.
Preserve lighting direction, shadow falloff, and surrounding table texture.
Do not alter anything outside the mask.
```

Good prompts:
- name only the replacement subject
- repeat lighting / palette constraints
- explicitly forbid changes outside the mask

Bad prompts:
- full scene re-description (model re-renders everything)
- style pivots ("make it anime now") — that is a `generate` call, not `upscale`

## Outpainting (Canvas Extension)

When the canvas is too tight (hero needs 21:9 but base is 16:9):

1. Pad the source with transparent pixels to target ratio.
2. Use the transparent region as the inpaint mask.
3. Prompt: "extend the scene naturally into the transparent region, matching composition, palette, and lighting of the visible area."

Limit single-pass extension to 20–30% of the original canvas. Larger extensions produce repetition or seam artifacts — do it in 2–3 passes.

## Artifact Detection Heuristics

Quick pre-export checks:

| Artifact | Signal |
|----------|--------|
| Over-sharpening halo | bright 1–2 px rim around high-contrast edges |
| Upscaler smoothing | fine texture (fabric weave, skin pores) flattened |
| Mask seam | visible rectangular boundary at mask edge |
| Regenerated face drift | face identity changed after inpainting |
| Palette drift | hexes shifted outside STYLE_TOKEN range |

Quick gate: diff against base at 50% opacity in a viewer. Anomalies outside the intended mask region are artifacts.

## Export Formats

| Format | Use when | Avoid when |
|--------|----------|------------|
| WebP (q=85, lossy) | Web hero, blog, marketing — default | Print, archival |
| AVIF (q=60) | Web, max compression, modern browsers | IE / older Safari support matters |
| PNG-24 | Illustrations with hard edges, UI assets, transparency | Photo heroes (file size) |
| JPEG (q=88) | Photo hero, legacy pipelines | Transparency, flat art |
| TIFF / PNG-48 | Print workflow, 16-bit color | Web |

Rules:
- strip EXIF (`pillow: im.save(..., exif=b"")`) unless provenance is explicitly needed
- keep color profile: embed sRGB for web, Display P3 only for verified P3 surfaces
- preserve SynthID notice in the delivered sidecar — post-processing does not remove the watermark

## Anti-Patterns

- Upscale a 512 px base to 4K — upscaler invents detail; regenerate at native 4K instead.
- Inpaint a face and expect identity preservation — Gemini does not have face-lock; warn the user or route to a face-preserving pipeline.
- Use a hard-edged mask — seams show up at the exact rectangle. Feather 4–8 px minimum.
- Outpaint 2x the canvas in one pass — produces repetition. Stage it.
- Save the final as PNG-24 for a 4K photo hero on a marketing page — 8 MB asset; use WebP or AVIF.
- Strip the SynthID disclosure from the sidecar because "the watermark is invisible anyway" — the disclosure is the contract with the user, not the watermark itself.
- Run the upscaler before confirming the base is approved — wastes GPU minutes if the base is rejected.

## Handoff

- **To Artisan**: final assets + export table (which format for which surface) + dimensions / DPI note.
- **To Muse**: if the asset becomes a registered token, hand over the 1x and 2x exports plus color profile.
- **To Growth**: print-spec variant (300 DPI CMYK TIFF) only if marketing needs offset print; otherwise WebP hero.
- **To Showcase**: post-processed catalog entry with `upscaler`, `mask`, and `inpaint_prompt` recorded in sidecar metadata.
