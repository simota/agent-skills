# Vigil — AUTORUN `_STEP_COMPLETE` Schema

See `_common/AUTORUN.md` for the protocol (`_AGENT_CONTEXT` input, mode semantics, error handling). On AUTORUN, run `ASSESS → DESIGN → BUILD → TEST → DEPLOY → HUNT` and emit `_STEP_COMPLETE`.

Vigil-specific `_STEP_COMPLETE.Output` schema:

```yaml
_STEP_COMPLETE:
  Agent: Vigil
  Task_Type: coverage_assessment | rule_design | threat_hunt | purple_team_blue | detection_pipeline
  Status: SUCCESS | PARTIAL | BLOCKED | FAILED
  Output:
    rules_created: List[{id: "DET-XXX", technique: "T-ID", format: "Sigma|YARA|KQL"}]
    coverage_delta: "+X techniques covered"
    hunting_hypotheses: [count]
    files_changed: List[{path, type, changes}]
  Handoff:
    Format: VIGIL_TO_[NEXT]_HANDOFF
    Content: [Handoff content for next agent]
  Risks: [Remaining coverage gaps, false positive concerns]
  Next: [NextAgent] | VERIFY | DONE
```

---
