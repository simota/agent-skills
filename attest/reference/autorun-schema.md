# Attest — AUTORUN `_STEP_COMPLETE` Schema

See `_common/AUTORUN.md` for the protocol (`_AGENT_CONTEXT` input, mode semantics, error handling). Attest-specific Constraints in `_AGENT_CONTEXT`: operating mode (FULL | EXTRACT | AUDIT | ADVERSARIAL), scope (ALL | CRITICAL_ONLY | DIFF_ONLY).

Attest-specific `_STEP_COMPLETE.Output` schema:

```yaml
_STEP_COMPLETE:
  Agent: Attest
  Status: SUCCESS | PARTIAL | BLOCKED | FAILED
  Output:
    verdict: CERTIFIED | CONDITIONAL | REJECTED
    criteria_summary: {pass, partial, fail, not_tested, ambiguous}
    critical_findings: List[String]
    files_analyzed: List[{path, criteria_covered: List[AC_ID]}]
  Handoff:
    Format: ATTEST_TO_[NEXT]_HANDOFF
    Content: [Full compliance report]
  Risks: [Compliance gaps, ambiguity concerns]
  Next: Builder | Radar | DONE
  Reason: [Why this Status/Next; if BLOCKED/FAILED, what is needed to unblock]
```
