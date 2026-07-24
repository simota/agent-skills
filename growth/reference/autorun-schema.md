# Growth — AUTORUN `_STEP_COMPLETE` Schema

See `_common/AUTORUN.md` for the protocol (`_AGENT_CONTEXT` input, mode semantics, error handling).

Growth-specific `_STEP_COMPLETE.Output` schema:

```yaml
_STEP_COMPLETE:
  Agent: Growth
  Status: SUCCESS | PARTIAL | BLOCKED | FAILED
  Output:
    deliverable: [artifact path or inline]
    artifact_type: "[SEO Meta | Heading Fix | OGP Setup | JSON-LD | Stacked Schema | Core Web Vitals Fix | GEO Optimization | E-E-A-T Signals | CRO Optimization | Form Optimization | Exit Prevention]"
    parameters:
      pillar: "[SEO | SMO | CRO]"
      target_metric: "[metric name]"
      expected_impact: "[description]"
      mobile_verified: "[yes | no]"
      lighthouse_score: "[before → after]"
    compliance: "[GDPR/CCPA notes if applicable]"
  Next: Experiment | Bolt | Pulse | Artisan | DONE
  Reason: [Why this next step]
```
