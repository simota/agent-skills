# Architect — AUTORUN `_STEP_COMPLETE` Schema

See `_common/AUTORUN.md` for the protocol (`_AGENT_CONTEXT` input, mode semantics, error handling).

Architect-specific `_STEP_COMPLETE.Output` schema:

```yaml
_STEP_COMPLETE:
  Agent: Architect
  Task_Type: CREATE | IMPROVE | COMPRESS | AUDIT_VERBOSITY | EVOLVE
  Status: SUCCESS | PARTIAL | BLOCKED | FAILED
  Output: <summary of deliverables>
  Handoff: <next agent if applicable>
  Next: <suggested follow-up action>
  Reason: <why this outcome>
```
