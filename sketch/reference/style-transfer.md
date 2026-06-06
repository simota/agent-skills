# Style Transfer Reference

Purpose: Match an existing brand or illustration style when generating new images — either by referencing a source image, extracting reusable style tokens, or pinning style weight against content. Invoke when cross-asset cohesion must follow an already-shipped look (brand illustrations, a licensed style guide, a sibling product's art direction) rather than a freshly invented one.

## Scope Boundary

- **sketch `style`**: reference-image prompts for Gemini, style-token extraction, weight / negative-prompt controls, comparison notes for SDXL / Flux when Gemini is not the right tool.
- **sketch `batch` (sibling)**: consumes the locked style anchor to fan out N assets. Run `style` first.
- **Vision (elsewhere)**: creative direction and mood boards. If the ask is "what style?" → Vision, not `style`.
- **Muse (elsewhere)**: converts final palette / typography / spacing into design tokens after style is locked.

If the user hands over a PNG and says "match this" → `style`. If they say "decide on a style" → Vision first.

## Workflow

```
INTAKE     →  collect style sources: reference images, brand guide PDF,
              existing asset URLs, palette hex list
           →  confirm licensing: can we use this style? (see Anti-Patterns)
           →  decide: Gemini-native vs external (SDXL / Flux) — see "Model Choice"

EXTRACT    →  derive style tokens: palette, line weight, shading mode,
              lens / lighting / mood, grain / noise signature
           →  write a reusable STYLE_TOKEN string (≤ 40 words)

APPLY      →  build prompt: Subject + STYLE_TOKEN + Composition + Technical
           →  attach 2–4 reference images via inlineData (never fileData)
           →  add negative prompt against known leakage patterns

VERIFY     →  render 3 A/B pairs against the reference, eyeball cohesion,
              pHash reference vs output (expect distance 20–35 — too close
              = plagiarism risk, too far = style drift)
```

## Reference-Image Prompt Patterns

Gemini accepts up to 14 reference images per request; keep each under 4 MB.

```python
from google import genai
from google.genai import types
import base64, pathlib

def ref(path: str) -> types.Part:
    data = pathlib.Path(path).read_bytes()
    return types.Part.from_bytes(
        data=data, mime_type="image/png"
    )  # inlineData, never fileData for style refs

parts = [
    types.Part.from_text(text=(
        "Generate a new illustration that matches the visual style of "
        "the attached references. Subject: a fox reading a letter. "
        "STYLE: flat vector, 4-color limited palette (#0B3954 #087E8B #BFD7EA #FF5A5F), "
        "1.5px outline, slight paper grain, soft ambient shadow. "
        "Do not copy the references' subjects."
    )),
    ref("refs/brand_hero.png"),
    ref("refs/brand_secondary.png"),
]
```

Rule: always tell the model to match *style* and not *subject*, otherwise it reconstructs the reference content.

## Style Token Extraction

A good STYLE_TOKEN is a short, dense, reusable string that composes with any subject.

| Axis | Example tokens |
|------|----------------|
| Medium | flat vector / gouache wash / 3D clay render / pencil / cel-shaded |
| Palette | "4-color limited, #hex #hex #hex #hex" or named ("Scandinavian muted") |
| Line | "1.5px outline, rounded caps" or "no outline" |
| Shading | "single soft shadow below subject, no highlights" |
| Texture | "slight paper grain, 8% noise" |
| Lens / mood | "isometric, calm, editorial" |

Target length: 20–40 words. Pin the token in `metadata.json` so `batch` can reuse it verbatim.

## Style Strength Controls

Gemini does not expose a numeric style weight. Simulate it with prompt + references:

| Desired strength | Pattern |
|------------------|---------|
| Hard-pin | 3–4 refs, STYLE_TOKEN at the front of the prompt, explicit palette hexes |
| Medium | 2 refs, STYLE_TOKEN mid-prompt |
| Light | 1 ref, STYLE_TOKEN mentioned without hexes |

For SDXL / Flux workflows (out of Sketch scope), you would use IP-Adapter or LoRA weight (`0.4–0.9`). If the user needs numeric control, that is the hand-off signal — see "Model Choice" below.

## Negative Prompts for Style Leakage

Common leakage modes and their counter-prompts:

```
--- leakage: reference subject bleeds into output ---
negative: "copying reference subject, same composition as reference"

--- leakage: photorealism sneaks into flat illustration ---
negative: "photographic, realistic skin, bokeh, depth of field"

--- leakage: extra colors outside palette ---
negative: "colors outside the stated palette, gradient, neon"

--- leakage: wrong outline ---
negative: "sketchy lines, variable line weight, crosshatch"
```

Gemini supports negative phrasing inside the main prompt — no dedicated `negative_prompt` field. Wrap them with "Avoid: …".

## Model Choice: Gemini vs Dedicated Style Models

| Need | Pick | Why |
|------|------|-----|
| One-shot style match, user controls via prompt | Gemini (Nano Banana / NB2) | Fastest integration, no infra |
| Numeric style weight, LoRA control | SDXL / Flux (out of scope) | Native IP-Adapter / LoRA weights |
| High fidelity to a single artist's oeuvre | External, with licensed dataset | Licensing + reproducibility |
| Brand illustration at batch scale | Gemini + locked STYLE_TOKEN | Good enough cohesion, 90% cheaper |

If the user brings LoRA weights or IP-Adapter config, Sketch stops — route to an external pipeline (not an in-repo agent). Sketch still delivers the Gemini-native version if the brief tolerates it.

## Anti-Patterns

- Upload a copyrighted reference ("make it like Ghibli") — policy risk and likely content-filter rejection. Ask the user to confirm licensing.
- Use `fileData` URL for reference images — model silently returns text-only, no image. Always `inlineData` Base64.
- Pack 10+ references of the same shot — model averages to mud. 2–4 diverse angles of the same style outperform.
- Include the STYLE_TOKEN once then vary it across the batch — cohesion collapses. Pin it verbatim.
- Ask Gemini for numeric style weight (`style_weight=0.7`) — no such parameter exists; that signals "wrong model".
- Skip the A/B against reference — style drift is invisible without side-by-side.
- Match style so closely the output is a near-duplicate of the reference (pHash hamming < 10) — that is plagiarism, not style transfer.

## Handoff

- **To `batch`**: `STYLE_TOKEN` string + reference image paths + recommended seed stride. `batch` fans out.
- **To Muse**: finalized palette hex list and typography hints if the style will become design tokens.
- **To Vision**: if the reference style is unclear or inconsistent, bounce back — creative direction must land before `style` is useful.
- **To Growth**: one hero render plus STYLE_TOKEN so marketing asset requests stay on-brand.
