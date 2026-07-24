# Flow — AUTORUN `_STEP_COMPLETE` Schema

See `_common/AUTORUN.md` for the protocol (`_AGENT_CONTEXT` input, mode semantics, error handling).

Flow-specific `_STEP_COMPLETE.Output` schema:

```yaml
_STEP_COMPLETE:
  Agent: Flow
  Status: SUCCESS | PARTIAL | BLOCKED | FAILED
  Output:
    deliverable: [artifact path or inline]
    artifact_type: "[Micro Animation | Page Transition | Gesture Handler | Motion System | Modern CSS | Accessible Motion]"
    parameters:
      work_mode: "[micro | page | gesture | system | modern-css]"
      framework: "[React | Vue | Svelte | Vanilla | CSS-only]"
      duration: "[Xms]"
      easing: "[curve name]"
      properties: ["[transform | opacity | etc.]"]
      reduced_motion: "[approach]"
    performance_notes: "[fps target, browser support]"
    browser_gates: ["[API: browser versions]"]
  Next: Radar | Canvas | Vitrine | Palette | DONE
  Reason: [Why this next step]
```
