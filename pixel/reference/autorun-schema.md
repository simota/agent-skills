# Pixel — AUTORUN `_STEP_COMPLETE` Schema

See `_common/AUTORUN.md` for the protocol (`_AGENT_CONTEXT` input, mode semantics, error handling). On AUTORUN, run `SCAN → EXTRACT → COMPOSE → VERIFY → REFINE` and emit `_STEP_COMPLETE`. Pixel-specific Constraints in `_AGENT_CONTEXT`: framework preference, scope (full page | single section), fidelity target percentage.

Pixel-specific `_STEP_COMPLETE.Output` schema:

```yaml
_STEP_COMPLETE:
  Agent: Pixel
  Status: SUCCESS | PARTIAL | BLOCKED | FAILED
  Output:
    deliverable: [artifact path or inline]
    artifact_type: HTML/CSS Reproduction
    parameters:
      framework: Vanilla | React | Vue 3 | Svelte 5
      fidelity_score: [percentage]
      iterations_used: 1-3
      confidence_breakdown: {high_values, medium_values, low_values}
    files_changed: List[{path, type, changes}]
  Handoff:
    Format: PIXEL_TO_[NEXT]_HANDOFF
    Content: [Handoff content for next agent]
  Risks: [Low-confidence values needing manual verification; responsive assumptions]
  Next: Artisan | Muse | Growth | Voyager | Canon | Judge | DONE
```

---
