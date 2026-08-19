# Canon — AUTORUN `_STEP_COMPLETE` Schema

See `_common/AUTORUN.md` for the protocol (`_AGENT_CONTEXT` input, mode semantics, error handling).

Canon-specific `_STEP_COMPLETE.Output` schema:

```yaml
_STEP_COMPLETE:
  Agent: Canon
  Task_Type: ASSESS | AUDIT | DESIGN
  Status: SUCCESS | PARTIAL | BLOCKED | FAILED
  Output:
    deliverable: [artifact path or inline]
    artifact_type: "[Security Compliance | A11y Compliance | API Compliance | Quality Compliance | Regulatory Control Matrix | Gap Analysis | Audit Trail Design | Policy-as-Code | Vendor Risk | Remediation Roadmap | Full Audit]"
    parameters:
      authorities: ["[OWASP | WCAG | OpenAPI | ISO 25010 | SOC2 | PCI-DSS | HIPAA | ISO 27001 | GDPR | EU AI Act | etc.]"]
      controls_assessed: "[number]"
      compliant_count: "[number]"
      partial_count: "[number]"
      non_compliant_count: "[number]"
      critical_findings: "[number]"
      evidence_tier: "[1 | 2 | 3 | 4 | 5 | mixed]"
  Next: Builder | Sentinel | Palette | Zen | Gateway | Scribe | Beacon | Gear | Crypt | Vigil | Cloak | DONE
  Reason: [Why this next step]
```
