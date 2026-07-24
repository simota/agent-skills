# Forge — AUTORUN `_STEP_COMPLETE` Schema

See `_common/AUTORUN.md` for the protocol (`_AGENT_CONTEXT` input, mode semantics, error handling).

Forge-specific `_STEP_COMPLETE.Output` schema:

```yaml
_STEP_COMPLETE:
  Agent: Forge
  Status: SUCCESS | PARTIAL | BLOCKED | FAILED
  Output:
    deliverable: [artifact path or inline]
    artifact_type: "[UI Component | Page Flow | API Mock | Backend PoC | Full-Stack Slice | Builder Handoff]"
    parameters:
      hypothesis: "[what was tested]"
      strategy: "[Throwaway | Evolutionary]"
      mock_strategy: "[inline | MSW | json-server | Express]"
      quality_level: "[L0 | L1 | L2 | L3]"
      prototype_status: "[concept | structured | demoable | builder-ready]"
    decision: "[ADOPT | ITERATE | DISCARD]"
    known_debt: ["[debt items]"]
  Validations:
    - "[build compiles / renders without error]"
    - "[happy path is demoable]"
    - "[mock assumptions documented]"
    - "[prototype status declared]"
  Next: Builder | Artisan | Vitrine | Muse | DONE
  Reason: [Why this next step]
```
