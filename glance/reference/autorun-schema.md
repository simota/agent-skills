# Glance — AUTORUN `_STEP_COMPLETE` Schema

See `_common/AUTORUN.md` for the protocol (`_AGENT_CONTEXT` input, mode semantics, error handling). On AUTORUN, run `FRAME → INVENTORY → COMPOSE → NAVIGATE → VERIFY → HANDOFF` and emit `_STEP_COMPLETE`.

Glance-specific `_STEP_COMPLETE.Output` schema:

```yaml
_STEP_COMPLETE:
  Agent: Glance
  Status: SUCCESS | PARTIAL | BLOCKED | FAILED
  Output:
    ui_design: [wireframes, screen-state map, focus graph, a11y checklist]
    platform_input: [target platform + input model]
    files_changed: List[{path, type, changes}]
  Handoff:
    Format: GLANCE_TO_[NEXT]_HANDOFF
    Content: [Handoff content for next agent]
  Risks: [Glanceability risks, a11y gaps, nav dead-ends]
  Next: Tick | Artisan | Echo | VERIFY | DONE
  Reason: [Why this Status/Next; if BLOCKED/FAILED, what is needed to unblock]
```

---
