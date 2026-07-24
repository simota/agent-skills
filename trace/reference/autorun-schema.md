# Trace — AUTORUN `_STEP_COMPLETE` Schema

See `_common/AUTORUN.md` for the protocol (`_AGENT_CONTEXT` input, mode semantics, error handling).

Trace-specific `_STEP_COMPLETE.Output` schema:

```yaml
_STEP_COMPLETE:
  Agent: Trace
  Status: SUCCESS | PARTIAL | BLOCKED | FAILED
  Output:
    deliverable: [artifact path or inline]
    artifact_type: "[Session Analysis | Frustration Report | Persona Validation | Journey Narrative | A/B Behavior Report]"
    parameters:
      analysis_type: "[session | frustration | persona | journey | ab_test]"
      persona_count: "[number]"
      session_count: "[number]"
      frustration_score: "[low | medium | high]"
      significance: "[statistical significance level]"
  Validations:
    completeness: "[complete | partial | blocked]"
    quality_check: "[passed | flagged | skipped]"
    privacy_compliance: "[confirmed | needs_review]"
  Next: Field | Echo | Canvas | Palette | DONE
  Reason: [Why this next step]
```
