# Equivalence Class Partitioning + Boundary Value Analysis Reference

Purpose: Reduce input-domain test cases via Myers equivalence partitioning, then amplify defect-finding at partition edges via Boundary Value Analysis (BVA). Applies the one-defect-per-negative-case rule (NIST SP 800-142, Microsoft pairwise guidance) to avoid input masking.

## Scope Boundary

- **matrix `equiv-class`**: Input-domain equivalence partitioning + BVA for axes that are ranges/continuous/string-typed (this document).
- **matrix `pairwise` (elsewhere)**: Combinatorial 2-way pair coverage for enumerated axes.
- **matrix `cover` (elsewhere)**: Generic n-wise selection.
- **mint (elsewhere)**: Test data / fixture generation. `equiv-class` emits the *rules*; mint generates the *data*.
- **Radar / Builder / Probe (elsewhere)**: Execution. Radar=unit, Builder=validator, Probe=negative security.

## Workflow

```
PARTITION  →  identify valid classes and invalid classes per axis
           →  each class = set of inputs that should be treated equivalently
           →  representative input per class

BOUNDARIES →  at each class boundary: ON / OFF / IN / OUT points
           →  ON   = at the boundary (e.g., min, max)
           →  OFF  = just outside (min-1, max+1)
           →  IN   = inside the valid class (typical value)
           →  OUT  = outside (typical invalid value)

NEGATIVE   →  generate ONE invalid value per negative case
           →  never combine multiple invalid values in a single test case
           →  prevents input-masking defect escape

COMBINE    →  combine valid-class representatives with `pairwise` (if multi-axis)
           →  keep negative cases as *separate* targeted scenarios

HAND OFF   →  Radar (unit tests), Builder (input validator), Probe (negative security)
```

## Equivalence Partition Template

For each input axis, identify:

| Partition | Description | Representative | Expected Outcome |
|-----------|-------------|----------------|------------------|
| Valid 1 | [range/class] | [sample value] | Accept |
| Valid 2 | [another valid class] | [sample value] | Accept |
| Invalid 1 | [below range / wrong type] | [sample value] | Reject with error X |
| Invalid 2 | [above range / null / empty] | [sample value] | Reject with error Y |

## Boundary Value Analysis

For each partition boundary, generate:

```
VALID:        IN  ------- ON      OFF ------- OUT        :INVALID
            typical    min        min-1    typical
                        |          |
                        +-- boundary
```

### Numerical Input Example

```
Valid range: age 13-120

Partition          | Rep  | BVA points
-------------------|------|----------------
Invalid (too low)  | -5   | [min of partition], [max of partition]: e.g., 0, 12
ON / OFF boundary  |      | 12 (OFF low), 13 (ON low)
Valid              | 30   | [typical value]
ON / OFF boundary  |      | 120 (ON high), 121 (OFF high)
Invalid (too high) | 999  | [typical high]
Invalid (type)     | "abc"| [non-numeric]
Invalid (empty)    | null | [null / undefined / empty string]
```

Resulting test cases for one input:
- `age = 0` → reject (invalid low)
- `age = 12` → reject (OFF low, boundary)
- `age = 13` → accept (ON low, boundary)
- `age = 30` → accept (IN valid)
- `age = 120` → accept (ON high, boundary)
- `age = 121` → reject (OFF high, boundary)
- `age = 999` → reject (invalid high)
- `age = "abc"` → reject (invalid type)
- `age = null` → reject (invalid absence)

### String Input Example

```
Valid: non-empty string, length 1-255, matches ^[A-Za-z0-9._-]+$

Partition                    | Rep            | Rationale
-----------------------------|----------------|----------
Valid typical                | "user123"      | middle of valid
Valid boundary length 1      | "a"            | ON low length
Valid boundary length 255    | "a" × 255      | ON high length
Invalid length 0             | ""             | OFF low
Invalid length 256           | "a" × 256      | OFF high
Invalid character (space)    | "user 1"       | one invalid char
Invalid character (unicode)  | "user🙂"        | unicode outside pattern
Invalid null                 | null           | absence
Invalid SQL injection vector | "a'; DROP--"   | hostile (hand off to Probe)
```

## One-Defect-Per-Negative-Case Rule

**Why**: when multiple invalid values are combined, input validation often returns on the first failure. The remaining invalid values are never tested — real defects escape.

**Rule**: each negative test case must contain exactly one invalid value across all axes. All other axes stay at valid representatives.

```
Correct:
  TC-N1: age = -5     (invalid)  + name = "ok"    (valid)
  TC-N2: age = 30     (valid)    + name = ""      (invalid)
  TC-N3: age = 30     (valid)    + name = "a'SQL" (invalid)

Wrong (masking):
  TC-N-BAD: age = -5  (invalid)  + name = ""      (invalid)
           → validator returns on age; "" path untested
```

## Combining With Pairwise

For multi-axis input validation:

1. **Positive cases**: apply pairwise across valid class representatives of all axes (2-way covering).
2. **Boundary cases**: one test per ON/OFF boundary per axis (keep others at valid IN).
3. **Negative cases**: one test per invalid partition per axis (keep others at valid IN).
4. **Integration**: positive + boundary + negative sets are distinct; do not merge.

```
Total = pairwise_positive_size
      + Σ (boundary_count_axis_i)
      + Σ (invalid_partition_count_axis_i)
```

## Common Pitfalls

| Pitfall | Why it breaks | Fix |
|---------|--------------|-----|
| Skipping OFF boundary | Off-by-one bugs escape | Always include (min-1, max+1) per boundary |
| One giant negative case | Input masking hides defects | One invalid value per negative case |
| Testing typical only (no BVA) | Defects cluster at boundaries | ON/OFF points are mandatory |
| Partition too coarse | Real defects need finer grain | Refine when defects correlate with sub-ranges |
| Merging boundary with pairwise | Dilutes boundary signal | Keep boundary tests separate |
| Ignoring null/undefined | Absence is a common defect path | Always include null/empty as invalid partition |
| Treating overflow as impossible | Integer overflow is common | Include type-max + 1 as boundary |

## Coverage Metrics

| Metric | Definition | Target |
|--------|-----------|--------|
| Partition coverage | % of partitions with ≥ 1 representative | 100% |
| Boundary coverage | % of boundaries with ON + OFF points | 100% |
| Negative coverage | % of invalid partitions with isolated test | 100% |
| Type coverage | % of type variants tested (null, empty, wrong-type, overflow) | 100% |
| Pairwise coverage (valid only) | 2-way across valid representatives | 100% |

## Output Template

```markdown
## Equivalence Partitioning + BVA Plan

### Input Analysis
- **Axes**: [count] input parameters
- **Per-axis partitions**: [table below]

| Axis | Type | Valid partitions | Invalid partitions | Boundaries |
|------|------|------------------|---------------------|------------|
| age | int | {13-120} | {<13}, {>120}, {type}, {null} | 12/13, 120/121 |
| name | str | {1-255 chars, regex valid} | {empty}, {>255}, {invalid char}, {null} | 0/1, 255/256 |

### Test Case Set

#### Positive (pairwise 2-way across valid representatives)
| TC | age | name | Expected |
|----|-----|------|----------|
| P-1 | 30 | "user123" | accept |
| P-2 | 13 | "a" × 255 | accept |
| ... | ... | ... | ... |

#### Boundary (one per ON/OFF, others at valid IN)
| TC | age | name | Boundary | Expected |
|----|-----|------|----------|----------|
| B-1 | 12 | "user123" | age OFF low | reject |
| B-2 | 13 | "user123" | age ON low | accept |
| B-3 | 120 | "user123" | age ON high | accept |
| B-4 | 121 | "user123" | age OFF high | reject |
| B-5 | 30 | "" | name OFF low | reject |
| B-6 | 30 | "a" | name ON low | accept |
| ... | ... | ... | ... | ... |

#### Negative (one invalid per case, others valid)
| TC | age | name | Invalid axis | Expected |
|----|-----|------|--------------|----------|
| N-1 | -5 | "user123" | age low | reject with error X |
| N-2 | 999 | "user123" | age high | reject with error X |
| N-3 | "abc" | "user123" | age type | reject with error Y |
| N-4 | null | "user123" | age null | reject with error Z |
| N-5 | 30 | "user 1" | name charset | reject with error W |
| N-6 | 30 | null | name null | reject with error Z |
| ... | ... | ... | ... | ... |

### Coverage Summary
- **Partition coverage**: 100%
- **Boundary coverage**: 100%
- **Negative coverage**: 100%
- **Pairwise valid coverage**: 100%
- **Total TC count**: [positive + boundary + negative]

### Handoff
- **Next agents**: Radar (unit tests), Builder (input validator), Probe (security-sensitive cases)
- **Execution note**: negative cases must each isolate a single invalid axis
```

## Deliverable Contract

When `equiv-class` completes, emit:

- **Per-axis partition table** (valid / invalid / rationale).
- **Boundary specification** (ON/OFF per boundary).
- **Positive test set** (pairwise 2-way across valid representatives).
- **Boundary test set** (one per ON/OFF, others valid IN).
- **Negative test set** (one invalid per case, others valid IN).
- **Coverage metrics** (partition, boundary, negative, pairwise).
- **Handoff targets**: Radar, Builder, Probe (for hostile inputs).

## References

- Glenford Myers — "The Art of Software Testing" (ch. on equivalence partitioning, BVA)
- ISTQB Foundation Level Syllabus — equivalence partitioning + BVA
- NIST SP 800-142 — Practical Combinatorial Testing (one-defect-per-case rule)
- Microsoft PICT documentation — pairwise + equivalence integration
- Boris Beizer — "Software Testing Techniques" (on input domain coverage)
