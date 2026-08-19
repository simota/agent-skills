# Clause — AUTORUN `_STEP_COMPLETE` Schema

See `_common/AUTORUN.md` for the protocol (`_AGENT_CONTEXT` input, mode semantics, error handling). On AUTORUN, run `SCOPE → SCAN → ASSESS → REPORT → SUGGEST` and emit `_STEP_COMPLETE`.

Clause-specific `_STEP_COMPLETE.Output` schema:

```yaml
_STEP_COMPLETE:
  Agent: Clause
  Status: SUCCESS | PARTIAL | BLOCKED | FAILED
  Output:
    review_report:
      high_findings: [count]
      medium_findings: [count]
      low_findings: [count]
      missing_clauses: List[String]
    files_changed: List[{path, type, changes}]
  Handoff:
    Format: CLAUSE_TO_[NEXT]_HANDOFF
    Content: [Handoff content for next agent]
  Risks: [Summary of legal risks]
  Next: [NextAgent] | VERIFY | DONE
  Reason: [Why this Status/Next; if BLOCKED/FAILED, what is needed to unblock]
```

---
