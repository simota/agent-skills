# Experiment — AUTORUN `_STEP_COMPLETE` Schema

See `_common/AUTORUN.md` for the protocol (`_AGENT_CONTEXT` input, mode semantics, error handling).

Experiment-specific `_STEP_COMPLETE.Output` schema:

```yaml
_STEP_COMPLETE:
  Agent: Experiment
  Status: SUCCESS | PARTIAL | BLOCKED | FAILED
  Output:
    deliverable: [artifact path or inline]
    artifact_type: "[Hypothesis Doc | Experiment Plan | Power Analysis | Feature Flag Setup | Experiment Report | Sequential Test Plan | SRM Diagnosis | Switchback Plan]"
    parameters:
      hypothesis: "[falsifiable hypothesis statement]"
      primary_metric: "[metric name]"
      sample_size: "[calculated N]"
      duration: "[estimated duration]"
      statistical_method: "[Z-test | Welch's t-test | Chi-square | Bayesian]"
      significance_level: "[alpha]"
      power: "[1-beta]"
      variance_reduction: "[CUPED | CUPAC | none]"
      srm_status: "[clean | detected: [details]]"
    guardrail_status: "[clean | flagged: [issues]]"
    recommendation: "[ship | iterate | discard | continue]"
  Next: Growth | Launch | Radar | Forge | DONE
  Reason: [Why this next step]
```
