# Relay — AUTORUN `_STEP_COMPLETE` Schema

When input contains `_AGENT_CONTEXT`, parse it for task parameters and constraints.

When called in Nexus AUTORUN mode: execute normal work, skip verbose explanations, append completion block:

```yaml
_STEP_COMPLETE:
  Agent: Relay
  Status: SUCCESS | PARTIAL | BLOCKED | FAILED
  Output: "<deliverable summary>"
  Next: "<recommended next agent or action>"
  Reason: "<why this status>"
```
