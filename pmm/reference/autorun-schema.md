# PMM — AUTORUN `_STEP_COMPLETE` Schema

See `_common/AUTORUN.md` for the protocol (`_AGENT_CONTEXT` input, mode semantics, error handling).

PMM-specific `_STEP_COMPLETE.Output` schema:

```yaml
_STEP_COMPLETE:
  Agent: PMM
  Status: SUCCESS | PARTIAL | BLOCKED | FAILED
  Output:
    deliverable: [report path or inline]
    artifact_type: "[Positioning Statement | Messaging House | GTM Plan | Launch Plan | Enablement Asset | Advisor Answer]"
    parameters:
      goal: "[marketing goal]"
      segment: "[target ICP/persona]"
      product_truth_source: "[PDM status / Lens survey / specs]"
      competitive_frame: "[Compete input / stated absence]"
      proof_grounding: "[grounded | partial | unsubstantiated claims flagged]"
      confidence: "[High | Medium | Low]"
      ungrounded: "[claims that couldn't be grounded]"
  Handoff: Saga | Funnel | Prose | Compete | Launch | Stage | Canvas
  Next: Saga | Funnel | Launch | VERIFY | DONE
  Reason: [Why this next step]
```
