# Accord — AUTORUN `_STEP_COMPLETE` Schema

See `_common/AUTORUN.md` for the protocol (`_AGENT_CONTEXT` input, mode semantics, error handling).

Accord-specific `_STEP_COMPLETE.Output` schema:

```yaml
_STEP_COMPLETE:
  Agent: Accord
  Status: SUCCESS | PARTIAL | BLOCKED | FAILED
  Output:
    deliverable: [artifact path or inline]
    artifact_type: "[Full | Standard | Lite] Specification Package"
    parameters:
      scope: "[Full | Standard | Lite]"
      teams: ["Biz", "Dev", "Design"]
      requirement_count: "[number]"
      traceability_completeness: "[percentage]"
      bdd_scenario_count: "[number]"
  Handoff: "[target agent or N/A]"
  Next: Sherpa | Builder | Radar | Voyager | Canvas | Scribe | Lore | DONE
  Reason: [Why this next step]
```
