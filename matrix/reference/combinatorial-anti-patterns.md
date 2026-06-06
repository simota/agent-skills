# Combinatorial Testing Anti-Patterns

Purpose: Use this file when parameter modeling, constraint design, or pairwise assumptions look suspicious.

## Contents

- Parameter modeling failures
- Constraint failures
- Coverage misconceptions
- Process failures

## Parameter Modeling Failures

| ID | Anti-pattern | Why it fails | Corrective action |
|---|---|---|---|
| `CT-01` | Over-parameterization | Noise creates a needlessly huge set | Keep only behaviorally meaningful differences |
| `CT-02` | Mismatched granularity | Values are too fine or too coarse | Use representative values |
| `CT-03` | Missing parameters | Hidden environmental inputs go unmodeled | Add user-facing and behavior-changing factors |
| `CT-04` | Static models | The matrix drifts from the product | Regenerate whenever the model changes |

## Constraint Failures

| ID | Anti-pattern | Why it fails | Corrective action |
|---|---|---|---|
| `CT-05` | Over-constraint | Useful coverage disappears | Review once exclusion rate exceeds `30%` |
| `CT-06` | Contradictory constraints | No valid space remains | detect conflicts and escalate |
| `CT-07` | Unvalidated constraints | Assumptions hide real cases | confirm with product or engineering owners |
| `CT-08` | Undocumented constraints | No one can maintain the model | record rule, rationale, and example |

Constraint health:

- `< 30%` excluded: healthy
- `30-40%`: suspicious, review
- `> 40%`: redesign recommended

## Coverage Misconceptions

| ID | Anti-pattern | Why it fails | Corrective action |
|---|---|---|---|
| `CT-09` | Pairwise equals full coverage | `2-way 100%` is not system coverage `100%` | state the guarantee precisely |
| `CT-10` | Pairwise is always enough | some domains need `3-way+` | escalate strength for safety-critical or higher-order evidence |
| `CT-11` | Sequence is ignored | order-dependent defects survive | pair Matrix with sequence-oriented specialists |

Do not rely on pairwise alone when:

- the main risk is sequencing
- regulation requires exhaustive or stronger coverage
- known defects are `3-way+`

## Process Failures

| ID | Anti-pattern | Why it fails | Corrective action |
|---|---|---|---|
| `CT-12` | Manual maintenance | generated cases drift from reality | regenerate instead of patching manually |
| `CT-13` | Multiple invalid values per case | input masking — the first detected invalid value prevents testing of subsequent invalid values, hiding real defects | generate separate negative test cases with only one invalid value each (NIST SP 800-142; Microsoft pairwise testing guidance) |

Quality gates:

- exclusion rate `> 30%` -> warning
- safety-critical + `2-way` only -> recommend `3-way+`
- parameter model changed -> regenerate the plan
