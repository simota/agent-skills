# Bazaar — AUTORUN `_STEP_COMPLETE` Schema

See `_common/AUTORUN.md` for the protocol (`_AGENT_CONTEXT` input, mode semantics, error handling).

`bazaar`-specific `_STEP_COMPLETE.Output` schema:

```yaml
_STEP_COMPLETE:
  Agent: Bazaar
  Task_Type: PREMIUM | LEAD_GEN | SAAS | ECOM | EVENT | MAGNET | AUDIT
  Status: DONE | BLOCKED | NEED_INFO
  Recipe: <recipe id>
  Stage_Reached: <last completed stage>
  Output: <summary of deliverables and artifacts paths>
  Quality_Gates: <pass/fail per stage>
  Handoff: <next agent if applicable>
  Next: <suggested follow-up action>
  Reason: <why this outcome>
```
