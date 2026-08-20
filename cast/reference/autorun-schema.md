# Cast — AUTORUN `_STEP_COMPLETE` Schema

See `_common/AUTORUN.md` for the protocol (`_AGENT_CONTEXT` input, mode semantics, error handling).

Cast-specific `_STEP_COMPLETE.Output` schema:

```yaml
_STEP_COMPLETE:
  Agent: Cast
  Status: SUCCESS | PARTIAL | BLOCKED | FAILED
  Output:
    deliverable: [artifact path or inline]
    artifact_type: "[Persona Set | Evolution Report | Audit Report | Distribution Package | Voice Output]"
    parameters:
      mode: "[CONJURE | FUSE | EVOLVE | AUDIT | DISTRIBUTE | SPEAK]"
      persona_count: "[number]"
      confidence_range: "[low-high]"
      registry_changes: "[created | updated | unchanged]"
  Next: Echo | Spark | Growth | Compete | Scribe[unified] | DONE
  Reason: [Why this next step]
```
