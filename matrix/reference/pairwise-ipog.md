# Pairwise / All-Pairs Testing (IPOG) Reference

Purpose: Produce the smallest 2-way 100%-covering test suite using IPOG / IPOG-F (NIST ACTS) or Orthogonal Array Testing (OATS). Applies the empirically-validated rule that ≤ 2-way interactions trigger 93% of real-world faults (Kuhn, Wallace & Gallo 2004 / NIST SP 800-142).

## Scope Boundary

- **matrix `pairwise`**: IPOG / IPOG-F / OATS-specific 2-way coverage selection with explicit method rationale (this document).
- **matrix `cover` (elsewhere)**: Generic n-wise minimum coverage selection. Use when user does not specify pairwise.
- **matrix `combine` (elsewhere)**: Default — end-to-end explosion-control flow. Includes `pairwise` as the typical optimization step.
- **matrix `risk-cover` (elsewhere)**: RPN-weighted priority — complement to pairwise, not a replacement.
- **Radar / Voyager / Siege (elsewhere)**: Execution. Pairwise recipe emits a *plan*; these agents execute.

## Workflow

```
SCOPE      →  confirm 2-way is appropriate (not safety-critical / not regulated)
           →  enumerate axes, value counts, constraints

SELECT     →  IPOG (general-purpose, unequal value counts)
           →  IPOG-F (faster, memory-optimized for ≥ 10 axes)
           →  OATS (uniform value counts, balanced representation needed)

GENERATE   →  apply algorithm → minimum 2-way covering set
           →  verify 2-way coverage = 100% against all (v_i × v_j) pairs

VALIDATE   →  report reduction ratio vs exhaustive
           →  list uncovered ≥3-way tuples (expected — 2-way does not cover these)
           →  warn if any parameter value appears in < 10% of test cases

PRIORITIZE →  seed priority ordering (critical cases first)
           →  hand off to Radar / Voyager / Siege
```

## Method Selection Rubric

| Method | Use When | Strengths | Weaknesses |
|--------|----------|-----------|------------|
| IPOG | General case, unequal value counts | Flexible, proven (NIST ACTS reference) | Slower for ≥ 10 axes |
| IPOG-F | ≥ 10 axes, memory-constrained | Memory-efficient, parallelizable | Slightly larger output than IPOG |
| OATS | Value counts uniform across axes | Balanced representation, statistical elegance | Strict uniformity requirement limits applicability |
| AETG | Adaptive coverage with seeding | Handles complex constraints well | Non-deterministic (results vary across runs) |
| Manual Greedy | < 5 axes, teaching context | Pedagogical transparency | Not optimal for large matrices |

## IPOG Algorithm Walkthrough

Given parameters P_1...P_n with value sets V_1...V_n:

```
Step 1  Horizontal extension
        Start with a test set covering all 2-way pairs of (P_1, P_2)

Step 2  For each subsequent parameter P_i (i=3..n):
  a) For each existing test row t:
     Find the value v in V_i that covers the most uncovered 2-way pairs of (P_j, P_i) for j<i
     Extend t with v
  b) Vertical extension
     For remaining uncovered 2-way pairs, add new test rows that cover them
     (merge into existing rows where compatible)

Step 3  Output minimum 2-way covering test set
```

### Reduction Benchmarks (NIST)

| Exhaustive Size | Typical 2-way Pairwise Size | Reduction |
|-----------------|-----------------------------|-----------|
| 100 | ~10 | 10x |
| 1,000 | ~30 | 33x |
| 10,000 | ~60 | 167x |
| 100,000 | ~100 | 1000x |
| 1,000,000 | ~150 | 6667x |

## OATS (Orthogonal Array) Selection

Use when:
- All axes have same number of values (or close): e.g., all 2-level or all 3-level.
- Balanced representation matters (statistical analysis, DOE integration).
- User explicitly requests OA notation (L4, L8, L9, L16, L18, L27).

Example: **L9(3^4)** — 9 test cases cover 4 parameters each with 3 levels, 2-way balanced.

```
      P1   P2   P3   P4
TC1   1    1    1    1
TC2   1    2    2    2
TC3   1    3    3    3
TC4   2    1    2    3
TC5   2    2    3    1
TC6   2    3    1    2
TC7   3    1    3    2
TC8   3    2    1    3
TC9   3    3    2    1
```

Every pair (P_i, P_j) covers all 9 value combinations exactly once → 2-way balanced.

## Pairwise Is Not Enough When

Stop at pairwise is **wrong** when:

- **Safety-critical**: medical devices, avionics, automotive — use `3-way+` per NIST fault data.
- **Security-sensitive**: auth bypass, injection — combine with Sentinel/Breach attack matrices.
- **Known fault history shows ≥ 3-way interactions**: historical incidents triggered by 3+ parameters.
- **Regulated domains** (FDA, FAA, ISO 26262): regulatory expectation is ≥ 3-way for SIL/ASIL applicable systems.
- **Concurrency / timing bugs**: linear pairwise does not capture race conditions — use siege concurrency + targeted sequences.

Matrix defaults to pairwise for general business logic; switch to `High-Strength` mode or variable-strength when any of these apply.

## Constraint Handling

Constraints (invalid pairs, requires, excludes) reduce the effective space. IPOG accepts hard constraints; verify:

1. **Constraint exclusion rate** must be < 30%. Above 30%, warn. Above 40%, recommend redesign.
2. **Every parameter value** must appear in ≥ 10% of the final test suite (anti-skew rule).
3. **No single test case** should combine multiple invalid values — one defect per negative case.

## Output Template

```markdown
## Pairwise Coverage Plan

### Matrix Definition
- **Domain**: [test / deploy / compat / etc.]
- **Axes**: [P1(v_1), P2(v_2), ..., Pn(v_n)]
- **Exhaustive space**: [N total combinations]
- **Constraints**: [list of invalid pairs / requires]
- **Exclusion rate**: [X%]

### Method
- **Algorithm**: [IPOG / IPOG-F / OATS (L_k)]
- **Rationale**: [why this method]
- **Coverage guarantee**: 2-way 100%
- **Tool reference**: NIST ACTS, PICT, Allpairs, pairwise.rb

### Optimized Set
- **Size**: [M test cases]
- **Reduction**: [N → M, X-fold reduction]
- **Parameter-value appearance check**: [pass / flagged values]

### Test Case Table
| TC | P1 | P2 | ... | Pn | Priority |
|----|----|----|----|----|---------|
| 1 | ... | ... | ... | ... | Critical |
| ... | ... | ... | ... | ... | ... |

### Uncovered Higher-Order Tuples (expected for 2-way)
- [3-way tuple count, sampled examples — expected non-coverage at pairwise]
- [Caveat: if any of these are safety-critical, escalate to `High-Strength`]

### Warnings
- [List: constraint rate, parameter skew, domain mismatch, etc.]

### Handoff
- **Next agent**: [Radar / Voyager / Siege / Scaffold]
- **Execution note**: [any priority seeding, environment prep]
```

## Common Pitfalls

| Pitfall | Fix |
|---------|-----|
| Claiming pairwise = full coverage | Always state "2-way 100%, not end-to-end" |
| Applying pairwise to safety-critical | Switch to 3-way+ or mixed-strength |
| Ignoring constraints | Always declare invalid pairs explicitly |
| Over-constraining to shrink output | Warn at 30%, redesign at 40% |
| Masking multiple invalid values | One invalid value per negative case |
| Uniform priority (everything Critical) | Use `prioritize` recipe; cap Critical at 20% |

## Deliverable Contract

When `pairwise` completes, emit:

- **Method chosen** (IPOG / IPOG-F / OATS) with rationale.
- **Test case table** (2-way 100% covering).
- **Reduction ratio** vs exhaustive.
- **Parameter-value appearance audit** (no value < 10%).
- **Uncovered ≥3-way tuple note** (expected for 2-way; escalate if critical).
- **Warnings** (constraint rate, domain mismatch, skew).
- **Handoff target** (Radar / Voyager / Siege / Scaffold).

## References

- Kuhn, Wallace, Gallo (2004) — "Software Fault Interactions and Implications for Software Testing"
- NIST SP 800-142 — Practical Combinatorial Testing
- NIST IR 7878 — Combinatorial Coverage Measurement
- NIST ACTS (Automated Combinatorial Testing Tools)
- Microsoft PICT (Pairwise Independent Combinatorial Testing)
- Cohen et al. — AETG: Automatic Efficient Test Generator
- Taguchi — Orthogonal Array design of experiments
