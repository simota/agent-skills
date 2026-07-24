# Oath — AUTORUN `_STEP_COMPLETE` Schema

See `_common/AUTORUN.md` for the protocol (`_AGENT_CONTEXT` input, mode semantics, error handling).

Oath-specific `_STEP_COMPLETE.Output` schema:

```yaml
_STEP_COMPLETE:
  Agent: Oath
  Task_Type: ASSESS | AUDIT | DESIGN
  Status: SUCCESS | PARTIAL | BLOCKED | FAILED
  Output:
    deliverable: [artifact path or inline]
    artifact_type: "[Compliance Matrix | Gap Analysis | Audit Trail Design | Policy-as-Code | Remediation Roadmap]"
    parameters:
      frameworks: ["SOC2 | PCI-DSS | HIPAA | ISO 27001"]
      controls_assessed: "[count]"
      implemented: "[count]"
      partial: "[count]"
      missing: "[count]"
      critical_gaps: "[count]"
  Next: Builder | Beacon | Scribe | Gear | DONE
  Reason: [Why this next step]
```
