# Ledger — AUTORUN `_STEP_COMPLETE` Schema

See `_common/AUTORUN.md` for the protocol (`_AGENT_CONTEXT` input, mode semantics, error handling).

Ledger-specific `_STEP_COMPLETE.Output` schema:

```yaml
_STEP_COMPLETE:
  Agent: Ledger
  Task_Type: ESTIMATE | OPTIMIZE | GOVERN | REVIEW
  Status: SUCCESS | PARTIAL | BLOCKED | FAILED
  Output:
    deliverable: [artifact path or inline]
    artifact_type: "[Cost Estimate | Right-Sizing Report | RI/SP Recommendation | Budget Alert Config | Anomaly Detection Rules | Tag Strategy | Cost Dashboard Spec]"
    parameters:
      scope: "[single resource | service | account | organization]"
      estimated_savings: "[monthly amount or percentage]"
      confidence: "[high | medium | low]"
  Next: Scaffold | Beacon | Gear | Canvas | DONE
  Reason: [Why this next step]
```
