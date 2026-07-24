# Dot — AUTORUN `_STEP_COMPLETE` Schema

See `_common/AUTORUN.md` for the protocol (`_AGENT_CONTEXT` input, mode semantics, error handling).

Dot-specific `_STEP_COMPLETE.Output` schema:

```yaml
_STEP_COMPLETE:
  Agent: Dot
  Status: SUCCESS | PARTIAL | BLOCKED | FAILED
  Output:
    deliverable: [artifact path or inline]
    artifact_type: "[SVG | Canvas HTML | Phaser 3 JS | Pillow Script | CSS | Spritesheet | Tileset | Gemini SVG]"
    parameters:
      grid_size: "[WxH]"
      palette_tier: "[1-bit | 2-bit | 8-color | 16-color | 32-color]"
      palette_hex: ["#hex1", "#hex2"]
      target_engine: "[Browser | Phaser 3 | Godot | Unity | PixiJS | RPG Maker | None]"
      frame_count: [N]
      animation_states: ["[idle | walk | attack | ...]"]
      gemini_delegated: [true | false]
    metadata_json: "[path or inline]"
    rendering_mode: "[pixelated | crispEdges | nearest]"
  Next: Realm | Forge | Artisan | DONE
  Reason: [Why this next step]
```
