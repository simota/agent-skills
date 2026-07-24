# Breach — AUTORUN `_STEP_COMPLETE` Schema

See `_common/AUTORUN.md` for the protocol (`_AGENT_CONTEXT` input, mode semantics, error handling). On AUTORUN, run `SCOPE → MODEL → PLAN → EXECUTE → REPORT` and emit `_STEP_COMPLETE`. Breach-specific Constraints in `_AGENT_CONTEXT`: target scope, framework preference, authorization level.

Breach-specific `_STEP_COMPLETE.Output` schema:

```yaml
_STEP_COMPLETE:
  Agent: Breach
  Task_Type: threat_model | attack_scenario | ai_red_team | purple_team | full_assessment
  Status: SUCCESS | PARTIAL | BLOCKED | FAILED
  Output:
    findings: List[{id: "FIND-XXX", severity: Critical | High | Medium | Low, title}]
    threat_model: [Framework used and key threats]
    attack_scenarios: [Count and coverage]
    files_changed: List[{path, type, changes}]
  Handoff:
    Format: BREACH_TO_[NEXT]_HANDOFF
    Content: [Handoff content for next agent]
  Risks: [Untested attack surfaces, scope limitations]
  Next: [NextAgent] | VERIFY | DONE
  Reason: [Why this Status/Next; if BLOCKED/FAILED, what is needed to unblock]
```

---
