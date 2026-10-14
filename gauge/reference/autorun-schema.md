# Gauge — AUTORUN `_STEP_COMPLETE` Schema

See `_common/AUTORUN.md` for the protocol (`_AGENT_CONTEXT` input, mode semantics, error handling).

```yaml
_STEP_COMPLETE:
  Agent: Gauge
  Status: SUCCESS | PARTIAL | BLOCKED | FAILED
  Output:
    deliverable: [artifact path or inline]
    artifact_type: "[Compliance Report | Compliance Dashboard | Fix Plan | Evolution Log]"
    parameters:
      target_skills: ["[skill names or 'all']"]
      items_checked: 21
      coverage_by_severity:  # per-severity counts — never a composite grade (reference/report-templates.md § Coverage figures)
        P0: { pass: "[count]", partial: "[count]", fail: "[count]", not_run: "[count]" }
        P1: { pass: "[count]", partial: "[count]", fail: "[count]", not_run: "[count]" }
        P2: { pass: "[count]", partial: "[count]", fail: "[count]", not_run: "[count]" }
        P3: { pass: "[count]", partial: "[count]", fail: "[count]", not_run: "[count]" }
      blocked_skills: "[count]"
      p0_violations: ["[list]"]
      sources_consulted: ["[URLs or references]"]
      source_tiers: ["[T1 | T2 | T3 | T4]"]
    evolution_applied: "[none | Level A: [changes] | Level B: [changes]]"
  Next: Architect | Darwin | Nexus | Sigil | Chain | DONE
  Reason: [Why this next step]
```
