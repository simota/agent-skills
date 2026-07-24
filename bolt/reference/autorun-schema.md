# Bolt — AUTORUN `_STEP_COMPLETE` Schema

See `_common/AUTORUN.md` for the protocol (`_AGENT_CONTEXT` input, mode semantics, error handling).

Bolt-specific `_STEP_COMPLETE.Output` schema:

```yaml
_STEP_COMPLETE:
  Agent: Bolt
  Status: SUCCESS | PARTIAL | BLOCKED | FAILED
  Output:
    deliverable: [artifact path or inline]
    artifact_type: "[Frontend Optimization | Backend Optimization | Bundle Optimization | CWV Improvement | Index Optimization | Caching Implementation]"
    parameters:
      domain: "[frontend | backend | network | infrastructure]"
      baseline: "[before metric]"
      result: "[after metric]"
      improvement: "[percentage]"
  Validations:
    - "[lint + test passed]"
    - "[baseline metric documented]"
    - "[optimization rationale documented]"
    - "[no regression introduced]"
  Next: Tuner | Radar | Growth | Shift | Gear | Canvas | DONE
  Reason: [Why this next step]
```
