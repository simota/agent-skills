# Cost Analysis Reference — Void

Purpose: Use this file to score keeping cost, score removal risk, and translate those numbers into a recommendation.

Contents:
- `Cost-of-Keeping Score (0-10)` formula and rubric
- `Removal Risk Score (0-10)` formula and dimensions
- `CoK x Removal Risk` decision matrix
- Reusable score-calculation template

## Cost-of-Keeping Score (0-10)

### Formula

```text
CoK Score = Σ (Dimension Score x Weight)

Dimensions:
  1. Upkeep          (0.25)
  2. Verification    (0.20)
  3. Cognitive Load  (0.25)
  4. Entanglement    (0.15)
  5. Replaceability  (0.15)
```

## 5 Dimensions

### 1. Upkeep (25%)

Frequency and cost of ongoing maintenance.

| Score | Label | Criteria |
|-------|-------|----------|
| `0-2` | `Stable` | 0-1 fixes or updates in the last 12 months |
| `3-4` | `Low` | 2-3 minor maintenance events per year |
| `5-6` | `Moderate` | Roughly monthly maintenance |
| `7-8` | `High` | Weekly maintenance or repeated breakage |
| `9-10` | `Critical` | Constant upkeep or fragile by default |

Evidence by domain:
- Code: bug frequency, ticket volume, on-call incidents
- Process: procedure changes, exception rate
- Document: staleness rate, review cycle
- Dependency: patch frequency, breaking-change frequency

### 2. Verification (20%)

Cost of proving it still works correctly.

| Score | Label | Criteria |
|-------|-------|----------|
| `0-2` | `Simple` | Fast and straightforward to verify |
| `3-4` | `Moderate` | Stable verification exists with some setup |
| `5-6` | `Complex` | Verification needs significant setup or external dependency |
| `7-8` | `Fragile` | Verification is noisy or inconsistent |
| `9-10` | `Unverifiable` | No reliable verification path |

Evidence by domain:
- Code: test runtime, flakiness, setup complexity
- Process: compliance or quality-check effort
- Document: reference-check effort and consistency burden
- Configuration: impact-testing difficulty

### 3. Cognitive Load (25%)

Understanding and operating cost.

| Score | Label | Criteria |
|-------|-------|----------|
| `0-2` | `Self-evident` | Immediate understanding |
| `3-4` | `Clear` | Some domain context needed |
| `5-6` | `Contextual` | Hidden assumptions and cross-context knowledge |
| `7-8` | `Complex` | Requires deep institutional knowledge |
| `9-10` | `Opaque` | Hard even for maintainers to explain |

Evidence by domain:
- Code: review time, onboarding friction
- Process: rule memorization, exception handling
- Document: contradictions, discoverability issues, terminology drift
- Design: user confusion, support volume

### 4. Entanglement (15%)

Coupling and blast radius complexity.

| Score | Label | Criteria |
|-------|-------|----------|
| `0-2` | `Isolated` | No meaningful downstream effect |
| `3-4` | `Loosely coupled` | Few clear interfaces |
| `5-6` | `Moderately coupled` | Multiple dependencies |
| `7-8` | `Tightly coupled` | Wide impact when changed |
| `9-10` | `Entangled` | Separation is difficult and side effects are hard to predict |

Evidence by domain:
- Code: dependency graph, change coupling
- Process: bottleneck frequency, process dependency chain
- Document: update cascades, reference sprawl
- Configuration: hidden option interactions

### 5. Replaceability (15%)

Inverse replaceability: higher score means harder to replace.

| Score | Label | Criteria |
|-------|-------|----------|
| `0-2` | `Trivially replaceable` | Standard replacement exists immediately |
| `3-4` | `Easily replaceable` | Low migration cost |
| `5-6` | `Replaceable with effort` | Days to a week of migration work |
| `7-8` | `Difficult to replace` | Requires custom work over weeks |
| `9-10` | `Irreplaceable` | No viable substitute without months of effort |

Evidence by domain:
- Code: library or implementation alternatives
- Process: alternative workflow or automation path
- Document: alternative source of truth
- Dependency: substitute maturity

## Score Interpretation

| CoK Score | Label | Recommendation |
|-----------|-------|----------------|
| `0.0-2.0` | `Low cost` | `KEEP` |
| `2.1-4.0` | `Moderate` | `KEEP-WITH-WARNING` |
| `4.1-6.0` | `Elevated` | `SIMPLIFY` candidate |
| `6.1-8.0` | `High` | strong `REMOVE` or `SIMPLIFY` candidate |
| `8.1-10.0` | `Critical` | highest-priority `REMOVE` candidate |

## Removal Risk Score (0-10)

### Formula

```text
Removal Risk = Σ (Risk Dimension x Weight)

Dimensions:
  1. User Impact      (0.30)
  2. Data Integrity   (0.25)
  3. System Stability (0.25)
  4. Reversibility    (0.20)
```

### Risk Dimensions

| Dimension | `0` low risk | `5` medium | `10` high risk |
|-----------|--------------|------------|----------------|
| `User Impact` | No users | Small internal group | Broad external audience |
| `Data Integrity` | No data effect | Manageable migration | Data-loss risk |
| `System Stability` | No stability effect | Partial impact | Outage or major instability |
| `Reversibility` | Immediate rollback | Hours to recover | Recovery is difficult or impossible |

## Decision Matrix: CoK x Removal Risk

```text
                Removal Risk
                Low(0-3)   Med(4-6)   High(7-10)
CoK High(7-10)  REMOVE     SIMPLIFY   DEFER+PLAN
CoK Med(4-6)    SIMPLIFY   DEFER      KEEP-WITH-WARNING
CoK Low(0-3)    KEEP       KEEP       KEEP
```

## Score Calculation Template

```yaml
cost_of_keeping:
  target: "<Target Name>"
  domain: "<DOMAIN>"
  dimensions:
    upkeep:          { score: X, evidence: "string", weight: 0.25 }
    verification:    { score: X, evidence: "string", weight: 0.20 }
    cognitive_load:  { score: X, evidence: "string", weight: 0.25 }
    entanglement:    { score: X, evidence: "string", weight: 0.15 }
    replaceability:  { score: X, evidence: "string", weight: 0.15 }
  total_score: "X.X"
  label: "LOW | MODERATE | ELEVATED | HIGH | CRITICAL"

removal_risk:
  dimensions:
    user_impact:      { score: X, evidence: "string", weight: 0.30 }
    data_integrity:   { score: X, evidence: "string", weight: 0.25 }
    system_stability: { score: X, evidence: "string", weight: 0.25 }
    reversibility:    { score: X, evidence: "string", weight: 0.20 }
  total_score: "X.X"

decision_matrix_result: "REMOVE | SIMPLIFY | DEFER | KEEP-WITH-WARNING | KEEP"
confidence: "X%"
next_phase: "-> SUBTRACT"
```
