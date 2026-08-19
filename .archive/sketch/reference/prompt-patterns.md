# Prompt Patterns Reference

Purpose: Read this when Sketch needs canonical prompt architecture, prompt-quality thresholds, JP -> EN translation rules, policy-safe rewriting, or `v1.50+` prompt controls.

## Contents
- Prompt architecture
- Style preset library
- Domain templates
- JP -> EN translation rules
- Policy-safe prompting
- Quality checklist
- Negative patterns
- SDK v1.50+ controls

## Prompt Architecture

Build prompts in this order:

```
[Subject] + [Style] + [Composition] + [Technical]
```

| Layer | Role | Weight | Rule |
| --- | --- | --- | --- |
| Subject | what to depict | `40%` | put it first |
| Style | mood and expression | `30%` | keep style internally consistent |
| Composition | framing and camera | `20%` | choose ratio and perspective deliberately |
| Technical | quality directives | `10%` | keep this last and concise |

Construction rules:
1. subject first
2. style immediately after the subject
3. composition before technical polish
4. technical keywords last

## Style Preset Library

### Photorealistic

`photorealistic, natural lighting, detailed textures, DSLR quality, sharp focus, high dynamic range`

### Digital Illustration

`digital illustration, clean lines, vibrant colors, flat design, modern graphic style`

### 3D Render

`3D render, isometric view, clean geometry, soft shadows, ambient occlusion, PBR`

### Watercolor

`watercolor painting, soft edges, translucent layers, paper texture, bleeding colors`

### Abstract

`abstract composition, geometric shapes, bold color palette, minimalist design, conceptual art`

Additional styles:
- oil painting
- anime/manga
- vintage/retro
- cyberpunk
- art nouveau
- minimalist

## Domain Templates

### Marketing / hero image

`[Product/Scene], professional commercial photography, hero image composition, brand-appropriate lighting`

Recommended ratios:
- `16:9`
- `21:9`

### Product photography

`[Product] on [surface/background], studio product photography, soft box lighting, clean minimal composition`

Recommended ratios:
- `1:1`
- `4:3`

### UI / UX assets

`[UI element/icon/illustration], flat design, UI-ready, consistent line weight, transparent-ready`

Recommended ratio:
- `1:1`

### Documentation / technical

`[Concept visualization], clean infographic style, explanatory illustration, clear visual hierarchy`

Recommended ratios:
- `16:9`
- `4:3`

### Social media

| Platform | Ratio |
| --- | --- |
| Instagram Post | `1:1` |
| Instagram Story | `9:16` |
| Twitter/X | `16:9` |
| LinkedIn | `4:3` |
| YouTube Thumbnail | `16:9` |

## JP -> EN Translation Rules

Rules:
1. restore omitted subjects
2. replace vague adjectives with concrete English keywords
3. expand mood words into recognizable visual descriptors
4. keep technical terms in English

Common mappings:

| Japanese | English keywords |
| --- | --- |
| かわいい | cute, adorable, charming, kawaii-style |
| かっこいい | cool, stylish, sleek, dynamic |
| おしゃれ | fashionable, trendy, chic, sophisticated |
| あたたかい（雰囲気） | warm, cozy, inviting, golden tones |
| クール | cool tones, blue palette, modern, minimal |
| レトロ | vintage, retro, nostalgic, film-like |
| ナチュラル | natural, organic, earthy, authentic |
| シンプル | minimalist, clean, simple, uncluttered |
| ダイナミック | dynamic, energetic, motion blur, bold angles |
| 幻想的 | ethereal, dreamy, fantasy, soft glow |
| 荘厳 | majestic, grand, imposing, awe-inspiring |
| 繊細 | delicate, intricate, fine detail, subtle |

Keep this must-keep example:

**Input (日本語)**:
> やわらかい光のなかで、木のテーブルの上にコーヒーとノートパソコンがある、おしゃれなワークスペース

**Output (English prompt)**:
> A stylish modern workspace with a laptop and coffee cup on a wooden table, soft diffused natural lighting, cozy atmosphere, shallow depth of field, warm tones, lifestyle photography, 8K detail

## Policy-Safe Prompting

Safe patterns:
- use generic people descriptions instead of named real people
- use generic workplaces instead of branded offices
- use descriptive traits instead of copyrighted character names

Fallback sequence when a prompt is risky:
1. remove sensitive keywords
2. replace specific references with generic descriptions
3. reframe with positive keywords
4. simplify the prompt
5. suggest an alternative concept if still blocked

## Prompt Quality Checklist

- subject is specific
- style keywords do not conflict
- aspect ratio matches the use case
- no copyrighted character or brand reference unless explicitly required
- person-generation policy is checked
- prompt is in English
- technical keywords are present
- prompt length stays in the `50-200` word range

## Negative Patterns

### Style conflicts

| Bad prompt | Problem | Fix |
| --- | --- | --- |
| `photorealistic watercolor painting` | photorealism and watercolor conflict | choose one direction |
| `minimalist detailed ornamental` | minimalist and ornamental conflict | simplify or decorate, not both |
| `bright dark moody cheerful` | tonal conflict | choose one lighting and mood direction |

### Prompt length

| Length | Result | Rule |
| --- | --- | --- |
| `< 20` words | generic, vague results | aim for at least `50` |
| `50-200` words | best control and quality | preferred range |
| `> 200` words | blurred subject, lower quality | cut by importance |
| `> 500` words | keywords start losing force | reduce aggressively |

### Ineffective patterns

| Pattern | Why it fails | Better approach |
| --- | --- | --- |
| `NOT a photo of...` | negative instructions are weak | use positive framing |
| `Don't include people` | negation may be ignored | `empty scene, no figures, landscape only` |
| `ultra mega super high quality` | redundant modifiers cancel out | use `8K detail, sharp focus` |
| `like the Mona Lisa` | copyright risk and vagueness | describe the actual traits |
| `beautiful amazing stunning` | subjective and weak | use concrete technical instructions |

Quality-keyword rule:
- choose `3-5` strong quality keywords, not a long stack

## SDK v1.50+ Controls

If `v1.50+` is available, use:

```python
image_generation_config=types.ImageGenerationConfig(
    aspect_ratio="16:9",
    person_generation="DONT_ALLOW",
)
```

Available parameters:

| Parameter | Values | Default |
| --- | --- | --- |
| `aspect_ratio` | `"1:1"`, `"3:2"`, `"2:3"`, `"16:9"`, `"9:16"`, `"21:9"` | model default |
| `person_generation` | `"DONT_ALLOW"`, `"ALLOW_ADULT"` | `"DONT_ALLOW"` |

Version guidance:
- `v1.38+`: control ratio and people via the prompt
- `v1.50+`: prefer parameters for ratio and person generation, and keep the prompt focused on subject and style
