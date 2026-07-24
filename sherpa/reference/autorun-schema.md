# Sherpa — AUTORUN `_STEP_COMPLETE` Schema

When Sherpa receives `_AGENT_CONTEXT`, parse `task_type`, `description`, and `Constraints`, execute the standard workflow, and return `_STEP_COMPLETE`.

### `_STEP_COMPLETE`

```yaml
_STEP_COMPLETE:
  Agent: Sherpa
  Status: SUCCESS | PARTIAL | BLOCKED | FAILED
  Output:
    type: "[task_decomposition | progress_update | risk_assessment | replan]"
    summary: "[1-2 line summary of what was produced]"
    deliverable: [primary artifact]
    files_changed: [list of files if applicable, or "none"]
    parameters:
      task_type: "[task type]"
      scope: "[scope]"
      steps_total: [N]
      steps_completed: [M]
      weather: "[Clear | Cloudy | Stormy | Dangerous]"
  Validations:
    completeness: "[complete | partial | blocked]"
    quality_check: "[passed | flagged | skipped]"
  Handoff:
    Format: "[SHERPA_TO_*_HANDOFF format name]"
    Content: "[Full handoff block for next agent]"
  Next: [recommended next agent or DONE]
  Reason: [Why this next step]
```
