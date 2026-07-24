# Siege — AUTORUN `_STEP_COMPLETE` Schema

When invoked in Nexus AUTORUN mode, parse any `_AGENT_CONTEXT` block for mode hints, environment scope, success criteria, and upstream findings. Execute the normal workflow with concise delivery, then append `_STEP_COMPLETE:`.

### `_STEP_COMPLETE`

```yaml
_STEP_COMPLETE:
  Agent: Siege
  Status: SUCCESS | PARTIAL | BLOCKED | FAILED
  Output:
    mode: LOAD | CONTRACT | CHAOS | MUTATE | RESILIENCE
    artifacts: ["[test scripts]", "[reports]", "[contracts]"]
    findings: ["[metric or issue summary]"]
  Validations:
    thresholds_checked: "[pass/fail/partial]"
    cleanup_complete: "[yes/no]"
    rollback_ready: "[yes/no/not_applicable]"
  Next: Bolt | Radar | Builder | Triage | Beacon | DONE
  Reason: [Why this next step]
```
