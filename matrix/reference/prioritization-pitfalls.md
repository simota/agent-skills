# Prioritization Pitfalls

Purpose: Use this file when the ranking looks biased, compressed, or too subjective.

## Contents

- Risk-matrix pitfalls
- Scoring pitfalls
- Domain-specific bias
- Priority health checks

## Risk-Matrix Pitfalls

| ID | Pitfall | Why it fails | Corrective action |
|---|---|---|---|
| `RP-01` | Range compression | materially different risks get the same label | use finer or normalized scales |
| `RP-02` | Priority inversion | lower quantitative risk gets a higher label | cross-check with data |
| `RP-03` | Subjective scoring | each evaluator interprets risk differently | define scoring anchors |
| `RP-04` | Everything is critical | real priorities disappear | keep `Critical <= 20%` |
| `RP-05` | Static ranking | the environment changes but the plan does not | reassess regularly |
| `RP-06` | False confidence | the matrix looks tidy but reality is not | treat it as a discussion starter |
| `RP-07` | Ignoring dependencies | chained risks remain hidden | model dependent scenarios |
| `RP-08` | No resource mapping | labels do not map to execution effort | pair ranking with cost or impact |

## Scoring Pitfalls

| Problem | Why it fails | Corrective action |
|---|---|---|
| arbitrary weights | the order is unjustified | base weights on domain data |
| naive linear scoring | extreme values dominate strangely | normalize or cap the scale |
| fixed value-risk tables | scores drift out of context | review periodically |
| skewed label thresholds | nearly everything becomes HIGH | use percentile or target distributions |

Useful percentile bands:

- `P90+` -> `Critical`
- `P70-89` -> `High`
- `P30-69` -> `Medium`
- `P0-29` -> `Low`

## Domain-Specific Bias

| Domain | Common bias | Guardrail |
|---|---|---|
| test | happy-path bias | keep at least `30%` abnormal or edge-oriented cases |
| risk | CVSS-only bias | add exposure and bypass ease |
| deploy | production-only bias | require staging coverage |
| experiment | novelty bias | keep measurement and segment realism |

## Priority Health Checks

- `Critical <= 20%`
- `Critical + High <= 30%`
- not every case lands in the same bucket
- the ranking rationale is explainable in one sentence per case
