# Pulse — AUTORUN `_STEP_COMPLETE` Schema

See `_common/AUTORUN.md` for the protocol (`_AGENT_CONTEXT` input, mode semantics, error handling).

Pulse-specific `_STEP_COMPLETE.Output` schema:

```yaml
_STEP_COMPLETE:
  Agent: Pulse
  Status: SUCCESS | PARTIAL | BLOCKED | FAILED
  Output:
    deliverable: [artifact path or inline]
    artifact_type: "[Metrics Framework | Event Schema | Funnel Analysis | Cohort Analysis | Dashboard Spec | Platform Integration | Privacy Review | Data Quality | Revenue Analytics | Alert Config]"
    parameters:
      metric_scope: "[North Star | KPI | Event | Funnel | Cohort | Dashboard | Revenue | Alert]"
      platform: "[GA4 | Amplitude | Mixpanel | Custom]"
      events_defined: "[count]"
      privacy_reviewed: "[yes | no]"
      data_quality_plan: "[yes | no]"
    Validations:
      completeness: "[complete | partial | blocked]"
      quality_check: "[passed | flagged | skipped]"
      privacy_reviewed: "[yes | no]"
  Next: Experiment | Growth | Canvas | Scout | Builder | DONE
  Reason: [Why this next step]
```
