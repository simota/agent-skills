# Beacon — AUTORUN `_STEP_COMPLETE` Schema

See `_common/AUTORUN.md` for the protocol (`_AGENT_CONTEXT` input, mode semantics, error handling).

Beacon-specific `_STEP_COMPLETE.Output` schema:

```yaml
_STEP_COMPLETE:
  Agent: Beacon
  Status: SUCCESS | PARTIAL | BLOCKED | FAILED
  Output:
    deliverable: [artifact path or inline]
    artifact_type: "[SLO Document | Alert Strategy | Dashboard Spec | Capacity Model | Tracing Spec | Toil Plan | Reliability Review]"
    parameters:
      mode: "[MEASURE | MODEL | DESIGN | SPECIFY]"
      slo_count: "[number or N/A]"
      alert_count: "[number or N/A]"
      cost_impact: "[Low | Medium | High]"
  Next: Gear | Builder | Triage | Scaffold | Bolt | DONE
  Reason: [Why this next step]
```
