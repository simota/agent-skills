# Cloak — AUTORUN `_STEP_COMPLETE` Schema

See `_common/AUTORUN.md` for the protocol (`_AGENT_CONTEXT` input, mode semantics, error handling).

Cloak-specific `_STEP_COMPLETE.Output` schema:

```yaml
_STEP_COMPLETE:
  Agent: Cloak
  Status: SUCCESS | PARTIAL | BLOCKED | FAILED
  Output:
    deliverable: [artifact path or inline]
    artifact_type: "[PII Inventory | Compliance Audit | Consent Pattern | DSAR Handler | Data Flow Map | DPIA]"
    parameters:
      regulation: "[GDPR | CCPA | APPI | Multiple]"
      pii_findings: "[count by severity]"
      data_classification: "[tiers found]"
      remediation_status: "[complete | partial | blocked]"
  Validations:
    completeness: "[complete | partial | blocked]"
    quality_check: "[passed | flagged | skipped]"
  Next: Builder | Schema | Gateway | Beacon | Scribe | DONE
  Reason: [Why this next step]
```
