# Gauge — AUTORUN `_STEP_COMPLETE` Schema

See `_common/AUTORUN.md` for the protocol (`_AGENT_CONTEXT` input, mode semantics, error handling).

Gauge-specific `_STEP_COMPLETE.Output` schema:

```yaml
_STEP_COMPLETE:
  Agent: Gauge
  Status: SUCCESS | PARTIAL | BLOCKED | FAILED
  Output:
    deliverable: [artifact path or inline]
    artifact_type: "[Compliance Report | Compliance Dashboard | Fix Plan | Evolution Log]"
    parameters:
      target_skills: ["[skill names or 'all']"]
      items_checked: 21
      total_pass: "[count]"
      total_partial: "[count]"
      total_fail: "[count]"
      health_score: "[percentage]"
      p0_violations: ["[list]"]
      sources_consulted: ["[URLs or references]"]
      source_tiers: ["[T1 | T2 | T3 | T4]"]
    evolution_applied: "[none | Level A: [changes] | Level B: [changes]]"
  Next: Architect | Darwin | Nexus | DONE
  Reason: [Why this next step]
```
