# Hone — AUTORUN `_STEP_COMPLETE` Schema

When Hone receives `_AGENT_CONTEXT`, parse `scope`, `concerns`, and `Constraints`, run FETCH→AUDIT→PROPOSE, and return `_STEP_COMPLETE`.

### `_STEP_COMPLETE`

```yaml
_STEP_COMPLETE:
  Agent: Hone
  Status: SUCCESS | PARTIAL | BLOCKED | FAILED
  Output:
    deliverable: [artifact path or inline]
    artifact_type: "[Audit Report | Focused Audit | Proposal Set]"
    parameters:
      target_cli: "[codex | agy | antigravity | claude-code | all]"
      scope: "[full | model | trust | features | mcp | rules | agents | instructions | safety | extensions | permissions | commands | hooks]"
      items_checked: "[count]"
      total_pass: "[count]"
      total_warn: "[count]"
      total_fail: "[count]"
      proposals_generated: "[count]"
      p0_proposals: ["[list]"]
      sources_consulted: ["[URLs]"]
      source_tiers: ["[T1 | T2 | T3 | T4]"]
  Next: Builder | Judge | Nexus | DONE
  Reason: [Why this next step]
```
