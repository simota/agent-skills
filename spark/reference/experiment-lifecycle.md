# Spark Experiment Lifecycle Reference

Purpose: decide what Spark should do after an experiment, including ship, pivot, extend, or kill decisions.

## Contents
- Verdict matrix
- Iteration packets
- Inconclusive flow
- Pivot patterns
- Sample-size recalculation
- Guardrail violations
- Iteration metrics

## Result To Decision Matrix

| Verdict | Primary metric | Guardrail | Decision | Next action |
| --- | --- | --- | --- | --- |
| `VALIDATED` | significant positive | no regression | `SHIP` | proceed to implementation |
| `INVALIDATED` | significant negative or no effect | n/a | `KILL` or `PIVOT` | archive or restate the hypothesis |
| `INCONCLUSIVE` | not significant | n/a | `EXTEND` or `ITERATE` | gather more data or redesign |
| `GUARDRAIL_VIOLATED` | positive | significant negative | `KILL` | do not ship without a new approach |

Detailed verdict rules:
- `VALIDATED`
  - primary metric improved with `p < 0.05`
  - effect size meets the MDE
  - no guardrail metric regressed materially
- `INVALIDATED`
  - primary metric regressed, or
  - no meaningful change after adequate sample and duration
- `INCONCLUSIVE`
  - significance was not reached
  - sample, duration, or variance likely blocked interpretation
- `GUARDRAIL_VIOLATED`
  - the main metric improved, but a guardrail regression makes release unsafe

## Iteration Packets

### `## EXPERIMENT_TO_SPARK_ITERATION`

Required fields:
- `Hypothesis ID`
- `Test Name`
- `Duration`
- `Sample Size`
- `Results Summary`
- `Statistical Confidence` (`90% / 95% / 99%`)
- `Experiment Verdict`

### `## SPARK_ITERATION_RESPONSE`

Required fields:
- `Hypothesis ID`
- `Original Proposal`
- `Experiment Verdict`
- `Decision` (`SHIP / ITERATE / PIVOT / KILL / EXTEND`)
- `Rationale`
- `Next Steps`

## Inconclusive Handling

### `## Inconclusive Result Analysis`

Check:
- actual vs required sample size
- actual vs planned duration
- traffic allocation
- effect size vs expected MDE
- variance and implementation quality
- seasonal or external noise

Decision rules:
- if the trend matches the hypothesis and more data is achievable in `2 weeks`, `EXTEND`
- if the trend matches but the sample requirement is unrealistic, either `KILL` for tiny effects or `ITERATE` for strategically important ideas
- if there is no clear trend, inspect instrumentation and redesign before retesting

## Pivot Patterns

| Pivot type | Use when | Example |
| --- | --- | --- |
| `Scope Pivot` | the idea is too broad or too narrow | all users -> power users only |
| `Mechanism Pivot` | the problem is right but the solution is wrong | modal -> inline notification |
| `Metric Pivot` | the success metric was weak | clicks -> time on page |
| `Timing Pivot` | the touchpoint is wrong | homepage -> post-signup |
| `Channel Pivot` | the delivery surface is wrong | in-app -> email |

### `## HYPOTHESIS_PIVOT`

Required fields:
- `Original Hypothesis`
- `New Hypothesis`
- `Pivot Type`
- `Original Statement`
- `Learnings from Test`
- `What Changes Next`

## Sample Size Recalculation

Recalculate when:
- observed effect is smaller than expected
- variance is higher than planned
- confidence requirements changed
- prior results were inconclusive

### `## Sample Size Recalculation`

Required fields:
- `Original Assumptions`
- `Observed Reality`
- `Recalculated Requirements`

Quick reference:

```
n = (Zα/2 + Zβ)² × 2 × p × (1-p) / δ²
```

Where:
- `Zα/2 = 1.96` for `95%` confidence
- `Zβ = 0.84` for `80%` power

## Guardrail Violations

| Guardrail type | Severity | Typical action |
| --- | --- | --- |
| Revenue | Critical | always kill |
| User experience (`NPS`, `CSAT`) | High | kill unless a strategic exception is justified |
| Performance (latency, errors) | High | kill or fix before ship |
| Engagement (secondary) | Medium | evaluate tradeoff |
| Operational (cost, support) | Medium | evaluate tradeoff |

### `## GUARDRAIL_VIOLATION_ANALYSIS`

Required fields:
- `Hypothesis`
- `Violated Guardrail`
- `Primary Metric Result`
- `Violation Details`
  - control
  - treatment
  - change
  - p-value
  - threshold
- `Impact Assessment`

## Iteration Tracking

### `## Hypothesis Evolution: [Feature Area]`

Track:
- original hypothesis
- changed version such as `H-001-v2`
- result per cycle
- learning per cycle

Velocity targets:

| Metric | Definition | Target |
| --- | --- | --- |
| Iterations to validation | test cycles to a clear outcome | `< 3` |
| Time to decision | first test to final decision | `< 30 days` |
| Learning quality | actionable insights per iteration | `> 2` |
| Pivot success rate | pivots that later validate | `> 30%` |

## Integration Rules

| Result | Related pattern | Integration |
| --- | --- | --- |
| `VALIDATED` | implementation handoff | proceed to `SPARK_TO_SHERPA_HANDOFF` |
| `INVALIDATED` | competitive review | check whether competitors solved the problem better |
| `INCONCLUSIVE` | persona validation | request qualitative input from `Echo` |
| `GUARDRAIL_VIOLATED` | security review | inspect whether `Sentinel` concerns are driving the failure |

### `## POST_EXPERIMENT_HANDOFF`

Required fields:
- `Hypothesis`
- `Final Verdict` (`SHIP / KILL / PIVOT`)
- implementation path if shipping
- archival path and learnings if killing
