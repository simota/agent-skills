# Hearth — AUTORUN `_STEP_COMPLETE` Schema

See `_common/AUTORUN.md` for the protocol (`_AGENT_CONTEXT` input, mode semantics, error handling).

Hearth-specific `_STEP_COMPLETE.Output` schema:

```yaml
_STEP_COMPLETE:
  Agent: Hearth
  Status: SUCCESS | PARTIAL | BLOCKED | FAILED
  Output:
    configs_generated: [list of files]
    backups_created: [list of backups]
    verification:
      - tool: [tool name]
        check: [syntax/startup_time/functional]
        result: [PASS/FAIL with details]
  Artifacts: [generated files]
  Risks: [potential issues]
  Next: [next agent]
  Reason: "[why next agent is needed]"
```
