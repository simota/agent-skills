# Atelier — AUTORUN `_STEP_COMPLETE` Schema

When atelier receives `_AGENT_CONTEXT`, parse `task_type`, `description`, `Constraints`, and any inbound `DESIGN_INTENT_HANDOFF`. Execute `ONBOARDING → INTAKE → PLAN → EXECUTE → HANDOFF → DELIVER` with verbose explanation suppressed. Return `_STEP_COMPLETE`.

### `_STEP_COMPLETE`

```yaml
_STEP_COMPLETE:
  Agent: atelier
  Status: SUCCESS | PARTIAL | BLOCKED | FAILED
  Output:
    deliverable: <primary artifact bundle>
    artifact_types: [prototype, production, deck, asset, export, story, diagram]
    Registry_Ref: .agents/design-system/<slug>.json
    delegates_used: [Frame, Muse, Forge, Artisan, Vitrine]
    parameters:
      Vision_Ref: <Vision direction or user-brief>
      operation_layers: [prompt, structured-comment, direct-edit, parametric-slider]
  Validations:
    onboarding: reused | refreshed | first-run
    a11y_check: passed | flagged | skipped
    token_drift: 0 | <count>
    fidelity: <percentage or n/a>
  Next: <recommended next agent or DONE>
  Reason: <why this next step>
```
