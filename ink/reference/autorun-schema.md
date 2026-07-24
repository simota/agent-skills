# Ink — AUTORUN `_STEP_COMPLETE` Schema

See `_common/AUTORUN.md` for the protocol (`_AGENT_CONTEXT` input, mode semantics, error handling).

Ink-specific `_STEP_COMPLETE.Output` schema:

```yaml
_STEP_COMPLETE:
  Agent: Ink
  Status: SUCCESS | PARTIAL | BLOCKED | FAILED
  Output:
    deliverable: [artifact path or inline]
    asset_type: "[icon | icon-set | illustration | sprite | animated]"
    parameters:
      grid_size: "[16x16 | 20x20 | 24x24 | 32x32 | 48x48]"
      stroke_width: "[1.5px | 2px | 2.5px]"
      icon_count: [N]
      style: "[outline | filled | duotone]"
      accessibility: "[complete | partial]"
    optimization: "[SVGO applied | manual]"
  Next: Artisan | Vitrine | DONE
  Reason: [Why this next step]
```
