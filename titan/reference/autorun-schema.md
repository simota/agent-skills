# Titan — AUTORUN `_STEP_COMPLETE` Schema

See `_common/AUTORUN.md` for the protocol (`_AGENT_CONTEXT` input, mode semantics, error handling).

Titan-specific `_STEP_COMPLETE.Output` schema:

```yaml
_STEP_COMPLETE:
  Agent: Titan
  Status: SUCCESS | PARTIAL | BLOCKED | FAILED
  Output:
    deliverable: [primary artifact]
    parameters:
      task_type: "[task type]"
      scope: "[scope]"
  Validations:
    completeness: "[complete | partial | blocked]"
    quality_check: "[passed | flagged | skipped]"
  Next: [recommended next agent or DONE]
  Reason: [Why this next step]
```
