# Prune — AUTORUN `_STEP_COMPLETE` Schema

See `_common/AUTORUN.md` for the protocol (`_AGENT_CONTEXT` input, mode semantics, error handling).

Prune-specific `_STEP_COMPLETE.Output` schema:

```yaml
_STEP_COMPLETE:
  Agent: Prune
  Task_Type: AUDIT | MERGE | SUNSET | PACK_IMPACT | FOLLOWUP
  Status: DONE | NEED_APPROVAL | BLOCKED
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
