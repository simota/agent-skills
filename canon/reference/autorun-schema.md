# Canon — AUTORUN `_STEP_COMPLETE` Schema

See `_common/AUTORUN.md` for the protocol (`_AGENT_CONTEXT` input, mode semantics, error handling).

Canon-specific `_STEP_COMPLETE.Output` schema:

```yaml
_STEP_COMPLETE:
  Agent: Canon
  Status: SUCCESS | PARTIAL | BLOCKED | FAILED
  Output:
    deliverable: [artifact path or inline]
    artifact_type: "[Security Compliance | A11y Compliance | API Compliance | Quality Compliance | Full Audit]"
    parameters:
      standards: ["[OWASP | WCAG | OpenAPI | ISO 25010 | etc.]"]
      compliant_count: "[number]"
      partial_count: "[number]"
      non_compliant_count: "[number]"
      critical_findings: "[number]"
  Next: Builder | Sentinel | Palette | Zen | Gateway | Scribe | DONE
  Reason: [Why this next step]
```
