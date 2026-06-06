# Fault Interaction Statistics

Purpose: Use this file when deciding whether `2-way`, `3-way`, `4-way`, or mixed-strength coverage is justified.

## Contents

- Interaction distributions
- Strength selection
- Escalation strategy
- Mixed strength
- Coverage targets

## Interaction Distributions

NIST-style evidence summary:

| Domain | `<=2-way` | `<=3-way` | `<=4-way` | `<=5-way` | `<=6-way` |
|---|---:|---:|---:|---:|---:|
| Medical devices | `97%` | `99%` | `100%` | - | - |
| Browsers | `70%` | `90%` | `95%` | `99%` | `100%` |
| Servers | `76%` | `95%` | `99%` | `100%` | - |
| General software | `70-95%` | `90-99%` | `97-100%` | - | - |

Operational takeaway:

- `2-way` is enough for many normal systems.
- `3-way+` is justified once history, regulation, or criticality says pairwise is insufficient.

## Strength Selection

| Strength | Typical detection | Relative cost | Use when |
|---|---:|---:|---|
| `2-way` | `70-95%` | baseline | normal applications |
| `3-way` | `90-99%` | `2-3x` | high-quality or interaction-heavy areas |
| `4-way` | `97-100%` | `3-5x` | safety-critical or regulated systems |
| `5-way+` | `99-100%` | very high | exceptional regulatory cases |

## Escalation Strategy

Use this escalation path:

1. start with `2-way`
2. if additional higher-order defects appear, move to `3-way`
3. if `3-way` still exposes meaningful new defects, move to `4-way`
4. stop escalating when the next step yields no meaningful new defects

## Mixed Strength

Use mixed strength when only part of the model is high risk.

Example:

- authentication x privilege x data sensitivity -> `3-way`
- browser x OS -> `2-way`
- locale or theme -> `1-way` sampling

This often delivers better cost efficiency than applying `3-way` to the entire matrix.

## Coverage Targets

| Domain | Minimum | Preferred |
|---|---|---|
| General web application | `2-way 100%` | `2-way 100%` |
| Finance | `2-way 100%` | `3-way 100%` |
| Medical or safety-critical | `3-way 100%` | `4-way 100%` |
| IoT / embedded | `2-way 100%` | `3-way 100%` |
| Security testing | `2-way 100%` | mixed strength with `3-way` for high-risk areas |

Quality gates:

- `2-way` coverage below `100%` -> warning
- safety-critical domain + `2-way` only -> escalate recommendation

## 2025–2026 Research Updates

### High-Strength CIT for Configurable Systems

The ISSTA 2024 paper *"Beyond Pairwise Testing: Advancing 3-wise Combinatorial Interaction Testing for Highly Configurable Systems"* (ACM SIGSOFT) introduces **ScalableCA**, a constrained covering array generator that produces 3-wise arrays **38.9% smaller** than prior SOTA while running **1–2 orders of magnitude faster**. Techniques: fast invalidity detection, uncovering-guided sampling, remainder-aware local search.
Source: https://dl.acm.org/doi/10.1145/3650212.3680309

The ICSE 2025 paper *"Towards High-Strength Combinatorial Interaction Testing for Highly Configurable Software Systems"* extends scalable CCAG to 4-wise and 5-wise for large parameter models where prior algorithms were intractable.
Source: https://dl.acm.org/doi/10.1109/ICSE55347.2025.00113

**Implication:** For highly configurable software (feature flags, plugin systems, product-line architectures), 3-way+ CIT is now computationally feasible at production scale — escalate from 2-way sooner when historical defect patterns or domain criticality justify it.

### Combinatorial Security Testing — 10 Years Later (2026)

Simos, Leithner, Kuhn, Garn, Kacker & Lei published a 2026 retrospective in *IEEE Security & Privacy* documenting a decade of combinatorial security testing (CST) in practice. Key updates:
- CST scope has expanded from input validation to cloud configurations, IoT firmware, and API security surfaces.
- Mixed-strength models (3-way for auth × privilege × data-sensitivity, 2-way elsewhere) remain the recommended practice.
- Constraint modeling quality is the dominant factor in CST effectiveness — over-constrained models produce false confidence.
Source: NIST CSRC project page — https://csrc.nist.gov/projects/automated-combinatorial-testing-for-software

### AI/ML Dataset Coverage (2025)

Kuhn, Raunak & Kacker, *"Measuring and Visualizing Dataset Coverage for Machine Learning"*, IEEE Computer vol 58 no 4, Mar 2025 — introduces visualization methods for feature-interaction frequency distributions in training data, making data skew detectable before model training.
Source: https://www.nist.gov/publications/combinatorial-testing-metrics-machine-learning

NIST CSRC Apr 2025, *"Data Frequency Coverage Impact on AI Performance"* — pilot study shows: (1) performance may increase or decrease with data skew; (2) feature importance methods do not predict skew impact; (3) adding more data does not reliably mitigate skew effects. Use combinatorial frequency coverage, not raw dataset size, as the quality gate for ML training sets.
Source: https://csrc.nist.gov/pubs/conference/2025/04/15/data-frequency-coverage-impact-on-ai-performance/final
