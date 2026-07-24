# Stream — AUTORUN `_STEP_COMPLETE` Schema

When input contains `_AGENT_CONTEXT`: parse `Step`, `Objective`, and `Constraints` to scope work.

When in Nexus AUTORUN mode: execute work, skip verbose explanations, and append:

```yaml
_STEP_COMPLETE:
  Agent: Stream
  Status: SUCCESS | PARTIAL | BLOCKED | FAILED
  Output: "<deliverable summary>"
  Next: "<suggested next agent or action>"
  Reason: "<why this status — blockers, assumptions, or completion notes>"
```
