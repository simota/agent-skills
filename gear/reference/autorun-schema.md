# Gear — AUTORUN `_STEP_COMPLETE` Schema

See `_common/AUTORUN.md` for the protocol (`_AGENT_CONTEXT` input, mode semantics, error handling).

Gear-specific `_STEP_COMPLETE.Output` schema:

```yaml
_STEP_COMPLETE:
  Agent: Gear
  Status: SUCCESS | PARTIAL | BLOCKED | FAILED
  Output:
    deliverable: [artifact path or inline]
    artifact_type: "[Dependency Update | CI Fix | Docker Config | Linter Setup | Env Config | Observability Setup | Monorepo Config | Build Fix]"
    parameters:
      area: "[dependencies | ci-cd | docker | linting | environment | observability | monorepo | build]"
      change_type: "[update | fix | config | setup]"
      risk_level: "[low | medium | high]"
      verification: "[build passes | tests pass | linter clean]"
    rollback: "[instructions if medium/high risk]"
  Next: Shift | Sentinel | Radar | Bolt | Launch | DONE
  Reason: [Why this next step]
```
