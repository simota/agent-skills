# API Integration Reference

Purpose: Read this when Sketch needs canonical Gemini API integration rules, compatibility notes, error handling, rate guidance, or SynthID handling details.

## Contents
- SDK compatibility
- Authentication
- Request patterns
- Parameter rules
- Response handling
- Error handling
- Rate and cost guidance
- SynthID documentation

## SDK Compatibility

Verified baseline:
- `google-genai SDK v1.38.0`
- Google AI API with API-key auth
- default model: `gemini-3.1-flash-image`

| SDK version | Config pattern | Notes |
| --- | --- | --- |
| `v1.38+` | `GenerateContentConfig(response_modalities=["TEXT", "IMAGE"])` | simple config only; control ratio/style in the prompt |
| `v1.50+` | `GenerateContentConfig(image_generation_config=ImageGenerationConfig(...))` | supports `aspect_ratio` and `person_generation` as parameters |

Default guidance:
- keep docs and code `v1.38+` compatible unless the user explicitly targets `v1.50+`

## Authentication

```python
import os
from google import genai

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
```

Setup guidance:

```bash
pip install google-genai
export GEMINI_API_KEY="your-api-key-here"
```

Always include:

```bash
# .env
GEMINI_API_KEY=your-api-key-here

# .gitignore
.env
*.env
.env.*
```

## Model Rules

| Model | ID | API type | Speed | Cost | Use |
| --- | --- | --- | --- | --- | --- |
| Nano Banana 2 | `gemini-3.1-flash-image` | Gemini API | fast | verify current pricing | default generalist; 0.5K-4K output |
| Nano Banana Pro | `gemini-3-pro-image` | Gemini API | medium | verify current pricing | complex professional asset production |
| Nano Banana | `gemini-2.5-flash-image` | Gemini API | fast | verify current pricing | legacy; migrate to a Gemini 3 image model |

Rules:
- default to `gemini-3.1-flash-image`; use `gemini-3-pro-image` for the most demanding professional workflows
- `gemini-2.5-flash-image` is a legacy option, not the default
- Imagen 4 endpoints were shut down on 2026-08-17; migrate to Gemini 3 image models

## Request Patterns

### Text-to-image

```python
response = client.models.generate_content(
    model="gemini-3.1-flash-image",
    contents="A modern minimalist workspace, soft natural lighting, widescreen 16:9 composition",
    config=types.GenerateContentConfig(
        response_modalities=["IMAGE"],
    ),
)
```

### Text + image response

Use `response_modalities=["TEXT", "IMAGE"]` when the text explanation matters.

### Reference-based editing

Pass the reference image with `types.Part.from_bytes(...)` (Base64 inlineData) plus the edit instruction.

**Important:** Do not use the Files API (`fileData`) for reference/source images in editing workflows — it causes silent failures where the model returns text instead of an edited image. Always use `inlineData` (Base64-encoded).

### Iterative editing

Use `client.chats.create(...)` for multi-turn image refinement.

With Nano Banana 2, the model uses **Thought Signatures** to preserve visual context between conversation turns. This means you do not need to re-send the full image each turn — the model retains the visual state. Only re-send the base image if you are changing it entirely.

### Grounding with Google Image Search

Available for Nano Banana 2 (`gemini-3.1-flash-image`). Enable via `google_search` tool config to allow the model to reference real-world images during generation, improving accuracy for specific objects, styles, or scenes.

### Style transfer

Pass multiple reference images plus the transformation instruction.

## Parameter Rules

### `response_modalities`

| Value | Behavior | Use |
| --- | --- | --- |
| `["TEXT", "IMAGE"]` | text and image | **default — always use this** |
| `["IMAGE"]` | image only | **avoid — causes silent failure (HTTP 200, empty parts) on most models** |

### Prompt-based controls for `v1.38+`

| Control | Prompt instruction example |
| --- | --- |
| Aspect ratio | `"widescreen 16:9 composition"` |
| Style | `"photorealistic, DSLR quality"` |
| Quality | `"8K detail, professional photography"` |
| No people | `"no people, empty scene"` |
| Orientation | `"vertical portrait orientation"` |

### Aspect ratio guide

| Ratio | Prompt instruction | Use |
| --- | --- | --- |
| `1:1` | `"square format, 1:1 aspect ratio"` | social posts, icons, avatars |
| `3:2` | `"landscape 3:2 photography format"` | standard photography |
| `2:3` | `"portrait 2:3 vertical format"` | portrait/mobile |
| `16:9` | `"widescreen 16:9 composition"` | hero images, thumbnails |
| `9:16` | `"vertical 9:16 portrait orientation"` | stories, mobile vertical |
| `21:9` | `"ultra-wide 21:9 panoramic"` | banners |

### Reference-image limits

- maximum `14` reference images per request
- supported formats: PNG, JPEG, WebP, GIF first frame
- recommended maximum size: `4MB` per reference image

## Response Handling

Always:
- save images with timestamped filenames
- capture text responses when `TEXT` is requested
- write `metadata.json`

Suggested metadata fields:

```json
{
  "generated_at": "...",
  "prompt": "...",
  "model": "gemini-3.1-flash-image",
  "files": ["..."],
  "synthid": true
}
```

## Error Handling

Keep a comprehensive handler such as `generate_image_safe(...)` with retries.

| Error | Cause | Recovery |
| --- | --- | --- |
| `ResourceExhausted` | quota or rate limit | exponential backoff, quota check |
| `InvalidArgument` | bad prompt or parameters | fix prompt or params |
| `PermissionDenied` | invalid API key | verify `GEMINI_API_KEY` |
| `NotFound` | wrong or retired model ID | verify the lifecycle page and use `gemini-3.1-flash-image` by default |
| `ServiceUnavailable` | server issue | retry with backoff |
| empty response | content-policy block | simplify or adjust prompt |
| `DeadlineExceeded` | timeout | retry or simplify the request |

Common pitfalls:

| Pitfall | Symptom | Fix |
| --- | --- | --- |
| `ImageGenerationConfig` missing | `AttributeError` | on `< v1.50`, use simple config |
| retired Imagen 3/4 model ID | `NotFound` | migrate to `gemini-3.1-flash-image` |
| wrong Gemini model name | `NotFound` | keep the `-image` suffix |
| copy-pasted model names from tutorials | `NotFound` or unexpected behavior | Google naming is inconsistent across docs — always verify against Model Rules table. Common wrong names: `gemini-flash-image`, `gemini-3.1-flash-preview-image`, `agy-pro-image` |

## Rate Limits And Cost

Rate limits and image pricing vary by model, project, tier, resolution, and service changes. Read the live project quota and current official pricing page before production use; do not encode a static RPM/RPD table as a durable contract.

Rules:
- preview `1-3` images before large batches

## Batch Guidance

For batch generation:
- generate sequentially with delay and retries
- show progress
- keep output paths deterministic
- estimate total cost before the run

## SynthID

All Gemini-generated images contain an invisible `SynthID` watermark.

Document:
- that the image is AI-generated
- the model used
- the generation timestamp
- that SynthID is present

Suggested disclosure snippet:

```text
This image was generated using Google Gemini API.
It contains an invisible SynthID watermark for AI-generated content identification.
Model: gemini-3.1-flash-image
Generated: [timestamp]
```


---

## Model Landscape and SDK Constraints (SKILL.md excerpt)

| Topic | Rule |
|---|---|
| Model landscape 2026 | Nano Banana 2 (`gemini-3.1-flash-image`) is the default generalist; Nano Banana Pro (`gemini-3-pro-image`) is the premium option; `gemini-2.5-flash-image` is legacy. Preview image endpoints from the Gemini 3 launch are retired. [Source: ai.google.dev/gemini-api/docs/image-generation, 2026-08] |
| Retired Imagen endpoints | Imagen 4 endpoints shut down 2026-08-17; use `gemini-3.1-flash-image`. Imagen 3 endpoints are also retired. |
| SDK compatibility | `v1.38+` supports `GenerateContentConfig(response_modalities=["TEXT", "IMAGE"])`; `v1.50+` additionally supports `ImageGenerationConfig` and `person_generation` param |
| 4K latency | Nano Banana Pro 4K takes ~60-65s per image vs <10s at 1K. Factor into batch timeouts and Batch API preference; avoid 4K for interactive UX unless streaming is acceptable |


## Silent-Failure Diagnostic Sequence (SKILL.md excerpt)

- Classify silent failures into four states before diagnosing: (1) prompt-side blocking (safety filter rejects the input), (2) output-side image blocking (`IMAGE_SAFETY` or `blockReason`), (3) no image produced (text-only response), (4) non-policy failures (ambiguous prompt, request-shape mistake). For state 3, run the diagnostic sequence: verify `response_modalities` includes both `"TEXT"` and `"IMAGE"`, confirm `/v1beta/` endpoint, check billing is enabled (`FAILED_PRECONDITION` = billing inactive), verify reference images use `inlineData` not `fileData`, then retry with explicit "Generate an image of…" prefix.
