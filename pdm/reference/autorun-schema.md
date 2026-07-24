# PDM — AUTORUN `_STEP_COMPLETE` Schema

See `_common/AUTORUN.md` for the protocol (`_AGENT_CONTEXT` input, mode semantics, error handling).

PDM-specific `_STEP_COMPLETE.Output` schema:

```yaml
_STEP_COMPLETE:
  Agent: PDM
  Status: SUCCESS | PARTIAL | BLOCKED | FAILED
  Output:
    deliverable: [report path or inline]
    artifact_type: "[Status Matrix | Feature Inventory | Gap List | Roadmap View | WBS Tree | Navigator Answer | Drift Report]"
    parameters:
      scope_sources: "[specs/issues/roadmap/code areas located]"
      features_total: "[count]"
      status_breakdown: "[Done/In-Progress/Not-Started/Undocumented counts]"
      confidence: "[High | Medium | Low]"
      drift_flags: "[count]"
      unreconciled: "[what couldn't be reconciled]"
  Handoff: Rank | Sherpa | Orbit | Scribe | Spark | Canvas
  Next: Rank | Sherpa | Orbit | Scribe | VERIFY | DONE
  Reason: [Why this next step]
```
