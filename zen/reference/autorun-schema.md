# Zen — AUTORUN `_STEP_COMPLETE` Schema

See `_common/AUTORUN.md` for the protocol (`_AGENT_CONTEXT` input, mode semantics, error handling).

Zen-specific `_STEP_COMPLETE.Output` schema:

```yaml
_STEP_COMPLETE:
  Agent: Zen
  Status: SUCCESS | PARTIAL | BLOCKED | FAILED
  Output:
    deliverable: [artifact path or inline]
    artifact_type: "[Refactoring Report | Code Review | Consistency Audit | Test Refactoring Report]"
    parameters:
      mode: "[Refactor | Review]"
      scope_tier: "[Focused | Module | Project-wide]"
      target: "[files or components]"
      smells_detected: ["[smell list]"]
      recipe_applied: "[recipe name or N/A]"
      complexity_before: "[metric or N/A]"
      complexity_after: "[metric or N/A]"
      tests_passed: "[yes | no | N/A]"
      coverage_delta: "[+X% | 0% | N/A]"
  Next: Radar | Judge | Guardian | Quill | Canvas | DONE
  Reason: [Why this next step]
```
