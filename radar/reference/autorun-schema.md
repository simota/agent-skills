# Radar — AUTORUN `_STEP_COMPLETE` Schema

See `_common/AUTORUN.md` for the protocol (`_AGENT_CONTEXT` input, mode semantics, error handling).

Radar-specific `_STEP_COMPLETE.Output` schema:

```yaml
_STEP_COMPLETE:
  Agent: Radar
  Status: SUCCESS | PARTIAL | BLOCKED | FAILED
  Output:
    artifact_type: "test_suite | coverage_report | flaky_fix | selection_strategy"
    deliverable: [primary artifact]
    parameters:
      task_type: "[task type]"
      mode: "[Default | FLAKY | AUDIT | SELECT]"
      scope: "[scope]"
      tests_added: [number of new tests]
      tests_modified: [number of modified tests]
      coverage_delta: "[+X.X% or N/A]"
      flaky_fixed: [number of flaky tests fixed or 0]
  Validations:
    completeness: "[complete | partial | blocked]"
    quality_check: "[passed | flagged | skipped]"
    tests_passing: "[all | partial | none]"
  Next: [recommended next agent or DONE]
  Reason: [Why this next step]
```
