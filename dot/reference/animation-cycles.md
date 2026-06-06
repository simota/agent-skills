# Sprite Animation Cycles Reference

Purpose: Author canonical sprite animation cycles for game characters and effects. Cover frame counts, timing curves, anticipation/squash-stretch principles, common cycle taxonomy (idle / walk / run / attack / hit / death), and JSON timing metadata for engines.

## Scope Boundary

- **dot `animation`**: Sprite animation authoring (this document).
- **dot `svg` / `canvas` / `phaser` (elsewhere)**: Static sprite output formats.
- **dot `tilesheet` (elsewhere)**: Tile-based world tiles, not character cycles.
- **Quest (elsewhere)**: Game design context (when an animation is needed).
- **Builder (elsewhere)**: Engine integration code.

## The Cycle Taxonomy

| Cycle | Frames | FPS | Loop | Purpose |
|-------|--------|-----|------|---------|
| `idle` | 4-12 | 4-6 | yes | Resting; subtle breathing or weight-shift |
| `idle_alt` | 4-8 | 4-6 | yes | Personality (yawn, look-around) |
| `walk` | 4-8 | 8 | yes | Locomotion at normal speed |
| `run` | 4-6 | 12 | yes | Locomotion at high speed |
| `jump_up` | 2-3 | n/a | no | Anticipation + ascent |
| `jump_apex` | 1 | n/a | hold | Hold at peak |
| `jump_down` | 2-3 | n/a | no | Descent |
| `land` | 2-4 | 12 | no | Squash + recovery |
| `attack` | 4-8 | 12-15 | no | Anticipation → strike → recovery |
| `attack_combo_2` | 4-6 | 15 | no | Continuation; chain into 3 if applicable |
| `hit` | 2-3 | 15 | no | Brief hitstun pose |
| `block` | 1-3 | 4 | hold | Defensive pose |
| `death` | 4-8 | 8 | no | Final pose; non-looping |
| `respawn` | 4-6 | 8 | no | Re-emergence |
| `interact` | 3-5 | 8 | no | Pick up / use / open |

Default cycle set for a platformer / action: idle / walk / run / jump (3-part) / attack / hit / death.

## Frame Count Heuristics

Rough rule: **fewer frames = stronger pose discipline**. NES sprites with 2-frame walks succeed because each pose tells a clear story. Don't pad.

```
2 frames: contrast pose (alternating; old-school NES idle)
3 frames: A-B-A loop (mirror-able; saves work)
4 frames: smooth basic
6 frames: cinematic-feel walk (Castlevania-era)
8 frames: full-quality character
12+ frames: hand-animated 60s+ smoothness (modern indies)
```

Pixel-art tradition: **2-4 frames** with strong key poses outperforms **8 frames** of mush.

## Frame Timing

| Style | FPS guideline |
|-------|---------------|
| NES / GB / 8-bit | 6-8 fps; even spacing |
| 16-bit (SNES / Mega Drive) | 8-12 fps; held + quick frames |
| Modern indie pixel | 8-15 fps; varied per frame |
| AAA hand-animated | 24fps with held frames acting as keys |

Per-frame timing (not just FPS) matters: an attack might be 4 frames at `[80ms, 60ms, 200ms, 120ms]` for anticipation→strike-hold→recovery.

```json
{
  "name": "attack_slash",
  "frames": [
    {"sprite": "atk_0", "duration_ms": 80,  "tag": "anticipate"},
    {"sprite": "atk_1", "duration_ms": 60,  "tag": "wind_up"},
    {"sprite": "atk_2", "duration_ms": 200, "tag": "strike", "hitbox": [12,8,18,4]},
    {"sprite": "atk_3", "duration_ms": 120, "tag": "recover"}
  ],
  "loop": false,
  "next": "idle"
}
```

## Animation Principles for Pixel Art

Adapted from Disney 12 principles for low-resolution work:

| Principle | Pixel-art application |
|-----------|----------------------|
| **Squash & stretch** | Land = squash (1 wider + shorter frame); jump-up = stretch (1 taller frame) |
| **Anticipation** | 1 frame leaning back before forward attack |
| **Staging** | Silhouette readability; never silhouette-overlap key body parts |
| **Follow-through** | Cape / hair / tail trails by 1-2 frames |
| **Slow-in / slow-out** | Per-frame timing varies (not even FPS) |
| **Arcs** | Even at low res, weapon swings follow curve, not straight |
| **Secondary action** | Idle: separate breathing layer + weapon-bob |
| **Timing** | Heavy character = more frames slower; light = fewer faster |
| **Exaggeration** | One-pixel push beyond realistic sells the feel |

## Walk Cycle Anatomy (4-frame)

```
Frame 0: Contact      — front foot down, back foot up
Frame 1: Down/Pass    — front leg bears weight, body lowest
Frame 2: Up/Pass      — body highest, leg extending
Frame 3: Mirror of 0  — back foot down, front foot up
```

8-frame walk adds passing/extreme between each: contact → down → pass → up → contact'.

## Run Cycle Anatomy (4-frame)

```
Frame 0: Contact (extended stride)
Frame 1: Recoil (compressed)
Frame 2: Push-off (other leg extended)
Frame 3: Recoil-mirror
```

Run = walk with: longer stride, more vertical bob, body forward-leaning, hands clenched.

## Attack Cycle Anatomy (variable)

| Phase | Frames | Purpose |
|-------|--------|---------|
| Anticipation | 1-2 | Wind-up; sells weight |
| Strike | 1 (held) | Impact frame; longest duration |
| Active (hitbox) | 1-2 | Damage window; line up gameplay hitbox |
| Recovery | 1-2 | Return to neutral; vulnerability window |

Hitbox metadata travels in JSON next to the strike frame.

## Death / KO Cycle

Non-looping. Final frame held. Variants:

- Stagger → fall back (3-4 frames)
- Spirit-rise → vanish (sprite + particles)
- Disintegration (palette-cycle on the sprite while shrinking)

The held last frame is the one players see — invest in pose quality.

## Workflow

```
PLAN         →  identify cycle set (which cycles, priority)
             →  frame budget per cycle (start minimum, expand if mush)

REFERENCE    →  collect rotoscope refs (video at 30fps) or hand-key
             →  block out key poses (1, mid, end) before in-betweens

KEY POSES    →  draw extreme + middle frames first
             →  validate silhouette at icon size

INBETWEEN    →  fill in timing-driven frames
             →  prefer fewer + held over many + mushy

ANTICIPATE   →  add 1-frame anticipation for any abrupt action
             →  squash-and-stretch on jump / land

TIMING       →  per-frame durations, not uniform FPS
             →  hold strike frames; quick anticipate

PALETTE      →  per-frame palette stable; only swap for hit-flash
             →  hit-flash: 1 frame in white / monotone

EXPORT       →  spritesheet + JSON timing
             →  consistent frame size (pad smaller frames)
             →  pivot point per frame (for weapon positioning)

PREVIEW      →  loop check; should feel weighted
             →  silhouette check at 0.5x scale
             →  side-by-side: idle ↔ walk ↔ run continuity

HANDOFF      →  Builder: engine config (Phaser anim, Aseprite tags)
             →  Realm / Quest: gameplay timing tuning
             →  dot `phaser` / `pillow`: export pipeline
```

## Output Template

```markdown
## Animation Pack: [Character / Effect]

### Cycle Inventory
| Cycle | Frames | FPS | Loop | Notes |
|-------|--------|-----|------|-------|
| idle | 6 | 5 | yes | breathing + blink at f4 |
| walk | 4 | 8 | yes | classic 4-frame |
| run | 4 | 12 | yes | exaggerated lean |
| attack | 5 | varied | no | per-frame timing |
| hit | 2 | 15 | no | white-flash on f0 |
| death | 6 | 8 | no | hold last |

### Frame Sheet
- Path: assets/sprites/hero.png
- Frame size: 16×24
- Frames per row: 8
- Layout: by cycle (idle row 0, walk row 1, ...)
- Pivot per frame: (8, 22) default; override list for attack frames

### Timing JSON
```json
{
  "hero": {
    "idle": {"frames": [...], "loop": true, "fps": 5},
    "walk": {"frames": [...], "loop": true, "fps": 8},
    "attack": {
      "frames": [
        {"frame": 0, "duration_ms": 80, "tag": "anticipate"},
        {"frame": 1, "duration_ms": 60, "tag": "wind"},
        {"frame": 2, "duration_ms": 200, "tag": "strike",
         "hitbox": [12, 8, 18, 4]},
        {"frame": 3, "duration_ms": 120, "tag": "recover"}
      ],
      "loop": false, "next": "idle"
    }
  }
}
```

### Validation
- Silhouette readable at 0.5x: [pass / fail per cycle]
- Weight feels right (drop a frame test): [yes / no]
- Hit-flash present: [yes / no]
- Held key poses on attack: [yes / no]
- Held last frame on death: [yes / no]

### Engine Hint
- Aseprite tags: idle:0-5, walk:6-9, attack:10-14, hit:15-16, death:17-22
- Phaser config: [code snippet]
- Godot animation: [.tres outline]

### Handoffs
- Builder: integration code
- Realm: gameplay tuning + hitbox sync
- dot `phaser` / `pillow`: export pipeline
```

## Anti-Patterns

| Anti-pattern | Fix |
|--------------|-----|
| Uniform FPS for all frames in attack | Per-frame timing; hold strike frame |
| 8-frame walk where 4 would do | Fewer frames + key poses; pad with held |
| Mirroring left/right by sprite-flip then re-drawing eyes | Decide one or other; mirroring loses asymmetric details |
| Loop on death | Non-looping; hold last |
| No anticipation on abrupt motion | Add 1-frame anticipation; sells weight |
| Even silhouette in walk extremes | Contrast extreme poses; A-B-A doesn't work without contrast |
| Hit-flash on every frame instead of 1 | 1-frame white flash; multi-frame loses impact |
| Per-frame palette drift | Stable palette; swap only for intentional flash |
| Pivot point fixed across frames | Pivot may shift on attack swing; specify per-frame |
| Idle that's just one frame | Add subtle breathing; still poses look broken |
| 60fps run that "looks smoother" | 12fps with right poses beats 60fps mush at low res |
| Hitbox metadata not aligned to active frame | Hitbox lives on strike frame; align in JSON |
| Forgetting `image-rendering: pixelated` on web | Add CSS / engine flag |
| Exporting frames without consistent canvas size | Pad to max bounds; engines expect uniform |
| Tail / cape moves at same time as body | Lag tail by 1-2 frames (follow-through) |
| Death has same frame count as idle | Death needs distinct timing + held last |

## Deliverable Contract

When `animation` completes, emit:

- **Cycle inventory** with frames, FPS, loop, notes per cycle.
- **Frame sheet** layout (path, frame size, layout, pivots).
- **Timing JSON** with per-frame durations + tags + hitboxes.
- **Validation** checklist (silhouette, weight, key poses, hit-flash).
- **Engine hint** (Aseprite tags, Phaser / Godot config).
- **Handoffs**: Builder, Realm, dot export.

## References

- Frank Thomas + Ollie Johnston — *The Illusion of Life* (12 principles)
- Richard Williams — *The Animator's Survival Kit* (timing, walks, runs)
- Aseprite documentation — aseprite.org/docs (tags, timing per frame)
- Pedro Medeiros — pixel art animation tutorials (saint11.org)
- Lospec animation guide — lospec.com/articles
- Brandon James Greer — pixel-art YouTube series
- *Pixel Logic* — Michael Azzi (pixel art principles)
- *Make Your Own Pixel Art* — Jennifer Dawe + Matthew Humphries
- Adam Saltsman — "Pixel Art Animations" (Canabalt postmortem)
- Tim Soret — Last Night animation case study
- *Game Feel* — Steve Swink (timing & weight)
- Dead Cells animation pipeline (Motion Twin GDC talks)
- Hyper Light Drifter / Heart Forth, Alicia case studies
- Rick Brewster — Aseprite animation tagging conventions
- Phaser 3 Animation Manager docs — phaser.io/docs
- Godot AnimationPlayer / SpriteFrames docs
- Unity SpriteAtlas + Animator workflow
