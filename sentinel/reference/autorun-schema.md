# AUTORUN `_STEP_COMPLETE` Schema (Sentinel)

Sentinel-specific output schema for AUTORUN mode. See `_common/AUTORUN.md` for the cross-skill protocol.

```yaml
_STEP_COMPLETE:
  Agent: Sentinel
  Status: SUCCESS | PARTIAL | BLOCKED | FAILED
  Output:
    deliverable: [primary artifact or inline report]
    artifact_type: "[Security Report | CVE Report | Fix Specification | Multi-Engine Report | SARIF Report]"
    parameters:
      task_type: "[secret_detection | injection | headers | dependency | auth | ai_code | api_security | tri_engine_scan]"
      scope: "[file path(s) or component]"
      finding_severity: "[CRITICAL | HIGH | MEDIUM | LOW | ENHANCEMENT | none]"
      finding_confidence: "[HIGH | MEDIUM | LOW]"
      owasp_category: "[e.g., A05:2025 – Injection | none]"
      fix_applied: "[true | false | partial]"
      lines_changed: "[count or 0]"
      false_positive_note: "[reason if downgraded | none]"
    tri_engine:
      activated: "[true | false]"
      engines_run: "[codex, agy, claude]"
      engines_failed: "[list or none]"
      concurrence: "[CONFIRMED: N, LIKELY: N, VERIFIED: N (1/3-grounded)]"
      findings_shipped: "[count after FILTER]"
      rejected: "[count + top categories: hallucinated_sink | upstream_mitigated | framework_guaranteed | test_file_only | unreachable_dep | wrong_cwe_mapping | style_only]"
      ai_authored_flag: "[true | false]"
      plausible_hallucination_rejects: "[count or 0]"
      slopsquat_rejects: "[count or 0]"
  Validations:
    - "[lint/tests pass after fix]"
    - "[issue confirmed closed or suppressed with rationale]"
    - "[no regressions introduced]"
    - "[no secrets or sensitive data in output]"
  Next: Builder | Probe | Radar | Triage | Guardian | DONE
  Reason: [Why this next step]
```
