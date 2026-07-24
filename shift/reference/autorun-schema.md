# Shift — AUTORUN `_STEP_COMPLETE` Schema

See `_common/AUTORUN.md` for the protocol (`_AGENT_CONTEXT` input, mode semantics, error handling).

Shift-specific `_STEP_COMPLETE.Output` schema:

```yaml
_STEP_COMPLETE:
  Agent: Shift
  Status: SUCCESS | PARTIAL | BLOCKED | FAILED
  Output:
    deliverable: [artifact path or inline]
    artifact_type: "[Migration Plan | Codemod | DB Migration | API Migration | Verification Plan]"
    parameters:
      migration_type: "[Framework | Library | Language | API | Database | Infrastructure]"
      strategy: "[Strangler Fig | Branch by Abstraction | Parallel Run | Big Bang | Expand-Contract]"
      scope: "[file count / module count]"
      phases: "[phase count]"
      rollback: "[available | partial | manual]"
  Validations:
    completeness: "[complete | partial | blocked]"
    quality_check: "[passed | flagged | skipped]"
  Next: Builder | Radar | Schema | Launch | Gear | DONE
  Reason: [Why this next step]
```
