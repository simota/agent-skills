# Mend — AUTORUN `_STEP_COMPLETE` Schema

See `_common/AUTORUN.md` for the protocol (`_AGENT_CONTEXT` input, mode semantics, error handling).

Mend-specific `_STEP_COMPLETE.Output` schema:

```yaml
_STEP_COMPLETE:
  Agent: Mend
  Status: SUCCESS | PARTIAL | BLOCKED | FAILED
  Output:
    deliverable: [report path or inline]
    artifact_type: "[Remediation Report | Auto-fix Report | Escalation Report | Rollback Report | Verification Report | Catalog Update]"
    parameters:
      safety_tier: "[T1 | T2 | T3 | T4]"
      pattern_confidence: "[percentage]"
      autonomy_mode: "[AUTO-REMEDIATE | GUIDED-REMEDIATE | INVESTIGATE | ESCALATE]"
      verification_stage: "[Health Check | Smoke Test | SLO Check | Recovery Confirmed]"
      rollback_triggered: "[yes | no]"
    Validations:
      completeness: "[complete | partial | blocked]"
      quality_check: "[passed | flagged | skipped]"
      safety_compliance: "[confirmed | needs_review]"
  Next: Radar | Builder | Beacon | Gear | Triage | DONE
  Reason: [Why this next step]
```
