# Usage Examples

Purpose: Read this when Sketch needs must-keep trigger examples, mode-specific script shapes, collaboration handoffs, or reusable packaging patterns.

## Contents
- Basic requests
- Mode examples
- Collaboration examples
- Packaging patterns

Verified environment:
- `google-genai SDK v1.38.0`
- Google AI API
- `gemini-2.5-flash-image`

## Basic Requests

Keep these examples because they define common trigger shapes:

### Example 1: Simple text-to-image

**Request**: 「ランディングページ用のヒーロー画像を生成して」

Expected output:
- single Python script
- safe API-key lookup
- timestamped output path
- basic image save flow

### Example 2: Style-specified generation

**Request**: 「水彩風のイラストで、東京の街並みを描いて。9:16のストーリーサイズで」

Expected output:
- single Python script
- translated English prompt
- `9:16` prompt instruction or parameter
- style preset applied

## Mode Examples

### Example 3: Iterative refinement

**Request**: 「カフェの画像を生成して、段階的に調整したい」

Expected output:
- `ITERATIVE` mode
- chat/session-based edit script
- saved intermediate outputs

### Example 4: Batch generation

**Request**: 「プロダクトのアイコン候補を5パターン生成して」

Expected output:
- `BATCH` mode
- sequential generation
- batch-aware filenames
- rate-limit-safe pacing

### Example 5: Reference-based edit

**Request**: 「この写真の背景を変更して」

Expected output:
- `REFERENCE_BASED` mode
- reference image loading
- edited output plus metadata

## Collaboration Examples

### `VISION_TO_SKETCH`

Use when `Vision` provides creative direction.

Required fields:
- `creative_direction`
- `target_use`
- `requirements`
  - `aspect_ratio`
  - `style`
  - `constraints`
- `reference_images`

Typical Sketch response:
- hero + feature image generation scripts
- aligned prompt family
- asset-specific ratios

### `SKETCH_TO_MUSE`

Use when generated assets need design-system integration.

Required fields:
- `generated_images`
- `metadata`
- `prompt_used`
- `integration_notes`

Keep notes about:
- crop guidance
- color extraction
- SynthID disclosure

## Packaging Patterns

### Pattern A: CLI wrapper

Use when the user needs:
- a reusable command-line entry point
- prompt, ratio, and output-dir flags
- a single operator-friendly script

### Pattern B: API wrapper class

Use when the user needs:
- reusable image generation methods
- one abstraction over `generate`, `edit`, and `batch`
- shared retry and metadata logic

Both patterns must still preserve:
- environment-variable auth
- safe error handling
- deterministic file output
- metadata capture
