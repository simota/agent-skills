# Quill — AUTORUN `_STEP_COMPLETE` Schema

See `_common/AUTORUN.md` for the protocol (`_AGENT_CONTEXT` input, mode semantics, error handling).

Quill-specific `_STEP_COMPLETE.Output` schema:

```yaml
_STEP_COMPLETE:
  Agent: Quill
  Status: SUCCESS | PARTIAL | BLOCKED | FAILED
  Output:
    deliverable: [files changed or artifact produced]
    artifact_type: "[JSDoc/TSDoc | README | Type Improvement | Coverage Audit | API Docs | Code Comments | Changelog | Quality Report]"
    parameters:
      task_type: "[documentation | types | readme | api-docs | coverage-audit | comments | changelog]"
      files_changed: "[count]"
      coverage_delta: "[before → after]"
      any_types_removed: "[count]"
      quality_score: "[Completeness/Accuracy/Readability/Maintainability]"
    handoff: "[token or NONE]"
  Next: Canvas | Atlas | Gateway | Lore | DONE
  Reason: [Why this next step]
```
