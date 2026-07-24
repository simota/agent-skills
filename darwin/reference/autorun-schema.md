# Darwin — AUTORUN `_STEP_COMPLETE` Schema

See `_common/AUTORUN.md` for the protocol (`_AGENT_CONTEXT` input, mode semantics, error handling).

Darwin-specific `_STEP_COMPLETE.Output` schema:

```yaml
_STEP_COMPLETE:
  Agent: Darwin
  Status: SUCCESS | PARTIAL | BLOCKED | FAILED
  Output:
    deliverable: [artifact path or inline]
    artifact_type: "[EFS Dashboard | RS Table | Lifecycle Report | Evolution Proposal | Sunset Report | Journal Synthesis]"
    parameters:
      lifecycle_phase: "[GENESIS | ACTIVE_BUILD | STABILIZATION | PRODUCTION | MAINTENANCE | SCALING | SUNSET]"
      confidence: "[0.0-1.0]"
      efs_score: "[0-100]"
      efs_grade: "[S | A | B | C | D | F]"
      triggers_fired: ["[ET-01 | ET-02 | ... | ET-08]"]
    evolution_actions: ["[action descriptions]"]
    risks: ["[risk descriptions]"]
  Next: Architect | Nexus | Void | Canvas | DONE
  Reason: [Why this next step]
```
