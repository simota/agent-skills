# Prune — AUTORUN `_STEP_COMPLETE` Schema

See `_common/AUTORUN.md` for the protocol (`_AGENT_CONTEXT` input, mode semantics, error handling).

```yaml
_STEP_COMPLETE:
  Agent: Prune
  Task_Type: AUDIT | MERGE | SUNSET | PACK_IMPACT | FOLLOWUP
  Status: SUCCESS | PARTIAL | BLOCKED | FAILED  # approval pending (e.g. sunset) = BLOCKED + Pending Confirmations
  Output:
    audit_scope: full | pack=<name> | subset=[skill1, skill2, ...]
    skills_audited: <count>
    classification:
      KEEP: <count>
      MERGE: <count>
      SUNSET: <count>
      DEPRECATE: <count>
    proposals: [<proposal-id>, ...]
  Handoff: Architect (merge) | User (sunset approval) | Nexus (routing) | DONE
  Next: <follow-up action or DONE>
  Reason: <evidence summary>
```
