# Optimization Algorithms

Purpose: Use this file when you must justify the chosen optimization method, budget tradeoffs, or coverage verification logic.

## Contents

- Method selection flow
- Pairwise generation
- Orthogonal array application
- Constraint-aware optimization
- Budgeted optimization
- Prioritization
- Coverage verification
- Performance guidance

## Method Selection Flow

| Condition | Default choice |
|---|---|
| `max_combinations` exists | budgeted optimization |
| invalid pairs `> 30%` | constrained pairwise |
| uniform value counts | orthogonal array |
| safety-critical requirement | `3-way+` CIT |
| axes `<= 2` | full enumeration |
| otherwise | pairwise |

## Pairwise Generation

Implementation expectation:

- expand the uncovered `2-way` tuple set
- greedily add rows that cover the most remaining tuples
- stop only when `2-way` coverage reaches `100%`

Use pairwise when:

- axes are numerous
- the domain is normal-risk
- constraints are manageable

## Orthogonal Arrays

Use OA when:

- value counts are uniform
- balanced distribution matters
- a known array such as `L9` or `L16` fits the matrix

Reference defaults:

| Levels | Factors | Array |
|---|---:|---|
| `2` | `2-3` | `L4` |
| `2` | `4-7` | `L8` |
| `3` | `2-4` | `L9` |
| `2` | `8-15` | `L16` |
| `4` | `4-5` | `L16` |

## Constraint-Aware Optimization

Apply constraints in this order:

1. remove invalid combinations
2. optimize the remaining space
3. enforce conditional rules
4. inject required cases

Escalate when:

- the valid space becomes empty
- constraints exceed the model’s explanatory power

## Budgeted Optimization

When `max_combinations` is smaller than the optimized set:

- keep the highest-coverage rows first
- report the achieved coverage rate
- list missing tuples explicitly
- do not claim the original coverage guarantee if the budget breaks it

## Prioritization

Rank after optimization, not before.

Useful strategies:

- weighted axis priority
- value-specific risk scores
- percentile bucketing for `Critical / High / Medium / Low`

Distribution guardrails:

- keep `Critical` around the top `10-20%`
- keep `Critical + High` around `<= 30%`
- warn when all rows collapse into one priority bucket

## Coverage Verification

Minimum verification fields:

- total tuples
- covered tuples
- coverage rate
- missing tuples

For pairwise:

```text
coverage_rate = covered_2_way_tuples / total_2_way_tuples
```

For higher-strength plans, verify the selected `t-way` explicitly.

## Performance Guidance

| Scale | Recommended approach | Typical runtime target |
|---|---|---|
| `2-5 axes`, `2-5 values` | Pairwise | `< 1s` |
| `6-10 axes`, `2-5 values` | Pairwise | `1-10s` |
| `10-15 axes`, `2-10 values` | Pairwise or OA | `10-60s` |
| very large or heavily constrained | specialized external tooling | context-dependent |

## High-Strength CCAG at Scale (2024–2025 Research)

For highly configurable systems with large parameter models where 3-way+ CIT was previously intractable:

**ScalableCA** (ISSTA 2024): Constrained Covering Array Generation algorithm introducing:
1. Fast invalidity detection — prunes impossible partial assignments early
2. Uncovering-guided sampling — biases random search toward uncovered tuples
3. Remainder-aware local search — repairs coverage without disrupting covered tuples

Results vs. prior SOTA: **38.9% smaller** 3-wise arrays, **1–2 orders of magnitude faster** construction on large-scale benchmarks.
Source: https://dl.acm.org/doi/10.1145/3650212.3680309

**ICSE 2025 CCAG** extends similar techniques to 4-wise and 5-wise on highly configurable software, making systematic escalation from 2-way to 4-way feasible for safety-critical configurable systems.
Source: https://dl.acm.org/doi/10.1109/ICSE55347.2025.00113

**Practical implication:** When axis count ≥ 20 or values are highly non-uniform and 3-way+ is required, recommend ScalableCA or ACTS 3-way mode rather than manual OA selection. Budget for 2–3x wall-clock time vs. pairwise, not the prior 10–100x penalty.
