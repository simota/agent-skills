# Cinematic Prompting

## Purpose

The difference between a flat AI-generated image and one that feels deliberate is cinematographic literacy. Camera, lens, lighting, depth of field, and composition vocabulary lets the prompt direct the image like a director, not a tourist with autoflash. This reference catalogs the vocabulary, the prompt patterns, and the verification criteria.

## Scope Boundary

- IN scope: shot-type vocabulary, camera / lens specification, lighting setups, depth of field, film stock and color science, composition rules, prompt-construction patterns, intent verification.
- OUT of scope: text-to-image API integration (`generate`), seed-locked variation (`batch`), style-transfer / character consistency (`style`), upscaling / inpainting (`upscale`), provenance / disclosure (`provenance`), content policy (`policy`).

## Core Concepts

### Why Cinematic Vocabulary Helps

Modern image models (Imagen 4, FLUX, SDXL Turbo, Nano Banana 2) have ingested decades of cinema and photography metadata. Calling a "Rembrandt-lit close-up shot on Kodak Portra 400 with shallow depth of field" gives the model a specific historical reference vector vastly stronger than "a portrait that looks nice".

| Generic prompt | Cinematic prompt |
|----------------|------------------|
| "A nice portrait of a woman" | "Medium close-up portrait, 85mm lens at f/1.8, Rembrandt lighting from camera-left, shallow depth of field, shot on Kodak Portra 400, golden hour" |
| "A landscape photo" | "Wide-angle landscape, 24mm lens at f/11, deep focus, Ansel Adams Zone System, low-angle morning light, large-format Velvia 50 emulation" |
| "An action shot" | "Mid-action tracking shot, 35mm anamorphic, slight motion blur, hard side-light, low-angle, color-graded Day-for-Night" |

### Shot Types

| Shot | Frame | Use |
|------|-------|-----|
| Extreme wide (EWS) | Subject tiny in vast environment | Establish setting; isolation |
| Wide (WS / LS) | Full body + environment | Context |
| Medium wide (MWS) | Knees up | Action with context |
| Medium (MS) | Waist up | Conversation default |
| Medium close-up (MCU) | Chest up | Interview |
| Close-up (CU) | Shoulders up | Emotion |
| Big close-up (BCU) | Face fills frame | Intensity |
| Extreme close-up (ECU / XCU) | Eyes / detail | Drama / detail emphasis |
| Macro | Subject magnified | Texture / object |

Combine with angle: low-angle (heroic), high-angle (vulnerable), Dutch tilt (unease), bird's-eye (observational), POV (immersion), worm's-eye, OTS (over-the-shoulder).

### Camera Format

| Format | Vocabulary | Effect |
|--------|-----------|--------|
| 35mm full-frame | "35mm full-frame" | Modern photographic default |
| Medium format | "Hasselblad medium format" / "Pentax 645" | Higher resolution, characteristic 6×6 / 6×7 ratio |
| Large format | "4x5 large format" / "8x10 view camera" | Sharp, Ansel Adams aesthetic |
| Super 35 | "Super 35 cinema" | Common cinema sensor |
| Anamorphic | "anamorphic 2.39:1" / "Panavision anamorphic" | Wide cinematic, oval bokeh, blue lens flares |
| 16mm | "16mm film grain" | Indie / documentary feel |
| 8mm / Super 8 | "Super 8 home-movie aesthetic" | Vintage / nostalgic |
| iPhone / smartphone | "shot on iPhone 15 Pro" | Modern casual realism |
| Polaroid | "Polaroid 600 instant film" | Square, soft, vintage |
| Drone / aerial | "drone shot, DJI Mavic 3" | High-angle scale |

### Lens Vocabulary

| Lens | Field of view | Use |
|------|--------------|-----|
| Ultra-wide 14mm | Very wide; distortion | Architecture, dramatic perspective |
| Wide 24mm | Wide environment | Landscape, environmental portrait |
| Wide-normal 35mm | Slight wide | Documentary, street |
| Normal 50mm | Eye-mimic | Reportage, casual portrait |
| Short tele 85mm | Compressed | Portrait classic |
| Tele 100-135mm | Compressed bg | Beauty / fashion portrait |
| Long tele 200-400mm | Heavy compression | Wildlife, sports, voyeuristic |
| Macro 100mm | 1:1 magnification | Detail / product |
| Tilt-shift | Selective focus plane | Architectural correction; miniature effect |
| Fisheye | Strong distortion | Skate / surreal |

Aperture controls depth of field:

| f-stop | DOF | Effect |
|--------|-----|--------|
| f/1.4 - f/2 | Razor thin | Subject isolated; bokeh dominant |
| f/2.8 - f/4 | Shallow | Portrait standard; some bg context |
| f/5.6 - f/8 | Medium | Both subject and bg readable |
| f/11 - f/16 | Deep | Landscape; everything sharp |
| f/22+ | Maximal | Diffraction softness; Zone System |

### Lighting Vocabulary

| Setup | Description | Mood |
|-------|------------|------|
| Rembrandt | Triangle of light on shadow-side cheek | Classical portrait |
| Butterfly / Paramount | Light from above-front; nose shadow under nose | Beauty / glamour |
| Loop | Slight side; small shadow off nose | Standard portrait |
| Split | Half face lit, half shadow | Drama / noir |
| Broad | Light hits the side closer to camera | Wider face |
| Short | Light hits the side further from camera | Slimmer face |
| Hard light | Direct sun, point source | High contrast, sharp shadows |
| Soft light | Diffused, large source | Wrap-around, gentle shadows |
| Backlight / rim | Behind subject | Halo, separation |
| Silhouette | Subject dark against bright bg | Iconography |
| Chiaroscuro | High contrast light/shadow | Dramatic, Caravaggio |
| Practical | In-frame light source (lamp, neon) | Naturalistic |
| Motivated | Off-frame source consistent with scene | Realistic |
| High-key | Bright, low-contrast | Commercial / fashion |
| Low-key | Dark, high-contrast | Noir / horror |
| Three-point | Key + fill + backlight | Standard professional |
| Available / natural | No artificial | Documentary |
| Golden hour | First / last hour of sun | Warm, long shadows |
| Blue hour | Twilight before sunrise / after sunset | Ethereal, cyan-magenta |
| Overcast | Diffuse cloud cover | Even, soft |
| Magic hour | Specific minutes of sunset | Cinematic mood |

### Color Science / Film Stock

| Stock / Look | Aesthetic |
|--------------|-----------|
| Kodak Portra 400 | Warm skin tones, slightly muted |
| Kodak Ektar 100 | High saturation, fine grain |
| Fuji Velvia 50 | Saturated greens / blues; landscape |
| Fuji Pro 400H | Cool, pastel, fashion |
| Cinestill 800T | Tungsten-balanced; halation around lights |
| Ilford HP5 / Tri-X | B&W, grainy, photojournalism |
| Polaroid 600 | Square, soft, vintage |
| Lomography | Cross-processed, vignetted |
| Teal-and-orange | Hollywood blockbuster look |
| Bleach bypass | Desaturated, silver retention |
| Day-for-night | Blue-graded daytime to imply night |
| Technicolor | Saturated, 3-strip era |
| Cool LUT / Warm LUT | Generic shifts |

### Composition Rules

| Rule | Description | Use |
|------|-------------|-----|
| Rule of thirds | Subject on third-line intersection | Default |
| Centered / symmetrical | Subject dead-center | Portrait, religious, Wes Anderson |
| Leading lines | Lines guide eye to subject | Landscape, architecture |
| Framing | Foreground frames subject | Depth, layered |
| Negative space | Empty area emphasizes subject | Minimalist |
| Diagonal | Strong diagonal element | Energy, tension |
| Triangle | 3-point composition | Stability |
| Repetition / pattern | Repeating elements | Graphic, design |
| Foreground-Mid-Background (FMB) | 3-layer depth | Cinematic |
| Golden ratio / spiral | Fibonacci composition | Classic art |
| Headroom / nose room | Space above head, in front of face | Portrait |
| Reflection / mirror | Subject + reflection | Doubled meaning |
| Rule of odds | 3 / 5 subjects (odd) | Visual interest |

### Style References

Adding director / photographer references invokes their entire visual signature:

| Reference | What it conveys |
|-----------|----------------|
| Roger Deakins cinematography | Subtle realism, controlled silhouettes |
| Wes Anderson aesthetic | Centered, pastel, symmetrical |
| Stanley Kubrick one-point perspective | Dread, vanishing point |
| Tarkovsky long take | Slow, melancholic |
| Annie Leibovitz portrait | Theatrical lighting, environmental |
| Henri Cartier-Bresson | Decisive moment, B&W reportage |
| Sebastião Salgado | Heroic B&W landscape, social documentary |
| Saul Leiter | Soft color, layered street |
| Daido Moriyama | Grainy, high-contrast Tokyo |
| Yasujirō Ozu tatami shot | Low-angle Japanese domestic |
| Hopper painting | Lonely Americana, hard light |
| Rembrandt painting | Dramatic chiaroscuro |
| Studio Ghibli backgrounds | Detailed naturalistic anime |
| Moebius / Jean Giraud | Sci-fi line art, surreal |

Use one or two; stacking five name-references muddies the signal.

### Prompt Construction Pattern

Effective cinematic prompts follow Subject + Style + Composition + Technical:

```
[Subject + action + emotion],
[Shot type] [Camera angle],
[Camera / lens / aperture],
[Lighting],
[Film stock / color grade],
[Composition rule + framing detail],
[Style reference if any],
[Aspect ratio / quality]
```

Example:

> Tired barista mid-yawn behind counter,
> Medium close-up, slight low angle,
> 35mm full-frame at f/2 with shallow depth of field,
> Window light from camera-right, warm tungsten practical,
> Cinestill 800T color grade with halation,
> Rule-of-thirds with negative space at right,
> Roger Deakins style,
> 16:9 cinematic widescreen.

This 60-word prompt outperforms a vague 5-word ask by an order of magnitude.

### Verification Criteria

After generation, check intent match:

| Criterion | Check |
|-----------|-------|
| Shot type matches | EWS prompt produced EWS, not CU |
| Lens / aperture honored | Shallow DoF if requested f/1.8 |
| Lighting setup recognizable | Rembrandt triangle visible |
| Color grade / film stock | Specific look present |
| Composition rule honored | Rule of thirds / centered as specified |
| Style reference recognizable | Deakins / Wes Anderson character preserved |
| Aspect ratio correct | 16:9, 2.39:1, 1:1, 4:5 etc. |

If 3+ criteria fail, restructure the prompt rather than re-roll seeds.

### Common Failure Patterns

| Failure | Cause | Fix |
|---------|-------|-----|
| Generic "professional photo" feel | Too vague | Add lens / lighting / film |
| Bokeh requested but not present | Aperture not specified | Add f/1.4 or f/1.8 |
| Wrong camera angle | Angle not specified | Add "low-angle" / "high-angle" |
| Style reference ignored | Too many references stacked | Cut to 1-2 |
| Wrong era / aesthetic | Modern keyword conflicts | Match film stock to era |
| Composition broken | No composition rule | Add "rule of thirds" / "centered" |
| Color cast off | No film stock / LUT | Specify Portra / Ektar / etc. |
| All faces look the same | No facial-specific prompt | Add age / ethnicity / expression |

### Genre Templates

Pre-built Subject + Style + Composition combinations:

| Genre | Template |
|-------|----------|
| Documentary portrait | "MS, 50mm at f/2.8, available natural light, slight reportage feel, Kodak Tri-X B&W, rule of thirds, Henri Cartier-Bresson tradition" |
| Editorial fashion | "MCU, 85mm at f/1.4, butterfly lighting + softbox fill, Fuji Pro 400H pastel grade, centered, Annie Leibovitz" |
| Landscape | "EWS, 24mm at f/11, deep focus, golden hour, Velvia 50 saturated, leading lines, Ansel Adams Zone System" |
| Sci-fi atmosphere | "WS, 35mm anamorphic 2.39:1, motivated practical lighting, teal-and-orange grade, FMB depth, Roger Deakins / Blade Runner 2049" |
| Indie film still | "MS, Super 35 at f/2, soft window light, slight 16mm grain, muted natural color, off-center composition, Sofia Coppola feel" |
| Beauty / cosmetics | "BCU, 100mm macro at f/4, butterfly + ring light, high-key fashion grade, centered symmetrical, glossy product feel" |
| Sports action | "MS tracking, 200mm at f/2.8, hard side-light, slight motion blur, saturated Velvia, diagonal composition" |
| Architectural | "Tilt-shift, 50mm equivalent at f/11, overcast diffuse, neutral grade, rule of thirds with leading lines, Iwan Baan style" |

Use as starting templates; tune Subject and 1-2 details.

## Workflow

1. **Define Subject** — what + action + emotion in one phrase.
2. **Choose shot type** — EWS to ECU based on intent.
3. **Pick camera + lens + aperture** — match to mood (shallow vs deep DoF).
4. **Design lighting** — Rembrandt / butterfly / hard / soft / golden hour / blue hour.
5. **Select film stock or color grade** — era + mood + saturation.
6. **Apply composition rule** — thirds / centered / leading lines / negative space.
7. **Add 1-2 style references** if needed (don't stack 5).
8. **Specify aspect ratio + quality**.
9. **Construct prompt** in Subject → Style → Composition → Technical order.
10. **Generate + verify** against the 7-criteria checklist.
11. **Iterate prompt** (not just seeds) when 3+ criteria fail.

## Output Template

```yaml
cinematic_prompt:
  subject: "Tired barista mid-yawn behind counter"
  shot_type: medium_close_up
  camera_angle: slight_low
  camera: 35mm_full_frame
  lens: 35mm
  aperture: f/2
  depth_of_field: shallow
  lighting:
    key: window_light_camera_right
    practical: warm_tungsten_in_frame
    setup: motivated_natural
  color_grade: cinestill_800t_with_halation
  composition:
    rule: rule_of_thirds
    negative_space_at: right
  style_reference: roger_deakins
  aspect_ratio: 16:9
  prompt_text: |
    Tired barista mid-yawn behind counter,
    medium close-up at slight low angle,
    35mm full-frame at f/2 with shallow depth of field,
    window light from camera-right with warm tungsten practical,
    Cinestill 800T color grade with halation,
    rule-of-thirds composition with negative space right,
    Roger Deakins cinematography style,
    16:9 cinematic widescreen.
  verification:
    shot_type_match: PASS
    aperture_honored: PASS
    lighting_recognizable: PASS
    color_grade: PASS
    composition: PASS
    style_reference: PASS
    aspect_ratio: PASS
```

## Anti-Patterns

- Generic "professional photo" with no cinematic vocabulary — flat output.
- Stacking 5 style references — model loses signal.
- Conflicting era cues (Cinestill 800T + 1920s sepia) — incoherent.
- Aperture requested but DoF wrong — model didn't honor; restructure prompt.
- "Bokeh" without aperture spec — vague.
- "Beautiful" / "stunning" / "amazing" — meaningless to the model.
- "Hyperdetailed, 8K, masterpiece" filler — 2022-era prompts; modern models don't need this.
- Ignoring composition rule — center-default everywhere.
- Mismatched lens to subject (200mm tele for landscape EWS) — wrong tool.
- Lighting setup unspecified for portrait — uncontrolled.
- Color grade unspecified — model defaults to bland.
- Aspect ratio missing — square default may not match intent.
- Re-rolling seeds when prompt is the problem — wastes API calls.
- Director name without directorial signature in mind — name-dropping noise.
- Mixing photo + painting + 3D references — pick one medium.

## Deliverable Contract

A cinematic prompt design is complete when:

- Subject articulated in one phrase.
- Shot type + angle specified.
- Camera + lens + aperture + DoF specified.
- Lighting setup named.
- Film stock / color grade named.
- Composition rule applied.
- Style reference (≤ 2) chosen if needed.
- Aspect ratio specified.
- Prompt text follows Subject → Style → Composition → Technical order.
- Verification criteria checked post-generation.

## References

- David Bordwell & Kristin Thompson, *Film Art: An Introduction* (12th ed., 2019).
- Roger Deakins, *Byways* (2021) photo book — visual reference.
- Vittorio Storaro, *Writing with Light* — color theory in cinema.
- Ansel Adams, *The Negative* / *The Print* — Zone System.
- Henri Cartier-Bresson, *The Decisive Moment* (1952).
- Annie Leibovitz, *At Work* (2008).
- Wes Anderson, *Accidentally Wes Anderson* (community visual reference).
- Ed Lachman, Christopher Doyle, Hoyte van Hoytema — cinematography interviews.
- *American Cinematographer* magazine — current cinematography techniques.
- Cinestill, Kodak, Fuji film stock documentation — accurate color science.
- Imagen 4 / FLUX / SDXL prompt-engineering community guides (2024–2026).
- Ari Folman, "How to Direct an AI" — practical cinematic-prompt tutorials.
- Karen Cheng (visual essays) — composition / framing breakdowns.
