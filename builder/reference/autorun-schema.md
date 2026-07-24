# Builder — AUTORUN `_STEP_COMPLETE` Schema

See `_common/AUTORUN.md` for the protocol (`_AGENT_CONTEXT` input, mode semantics, error handling).

The `pair` recipe is INTERACTIVE and cannot run unattended — under AUTORUN, run SURVEY → PLAN, return the ordered increment plan, and set `Next: USER` (pair-ready) rather than implementing without confirmation.

Builder-specific `_STEP_COMPLETE.Output` schema:

```yaml
_STEP_COMPLETE:
  Agent: Builder
  Status: SUCCESS | PARTIAL | BLOCKED | FAILED
  Output: [Brief summary of implementation results]
  Validations:
    type_safety: [Complete | Partial | Needs Review]
    test_coverage: [Generated | Partial | Needs Radar]
    impact_scope:
      callers: [OK | Updated | N/A | NEEDS-REVIEW]
      tests: [OK | Updated | N/A | NEEDS-REVIEW]
      types: [OK | Updated | N/A | NEEDS-REVIEW]
      configs: [OK | Updated | N/A | NEEDS-REVIEW]
      docs: [OK | Updated | N/A | NEEDS-REVIEW]
      verdict: [Ready | Needs Ripple | Blocked]
  Next: [Radar | Guardian | Tuner | Sentinel | Ripple | USER | VERIFY | DONE]
  Reason: [Why this next step is recommended]
```
