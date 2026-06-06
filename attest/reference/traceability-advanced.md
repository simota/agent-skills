# Advanced Traceability Techniques

Purpose: Read this when running `AUDIT`, building `BIDIRECTIONAL_TRACEABILITY`, classifying traceability gaps, or evaluating L1/L2/L3 coverage.

## Contents

- [Bidirectional traceability](#bidirectional-traceability)
- [Gap analysis](#gap-analysis)
- [Coverage levels](#coverage-levels)
- [Automation patterns](#automation-patterns)
- [Audit and regulatory use](#audit-and-regulatory-use)
- [Anti-patterns](#anti-patterns)

## Bidirectional Traceability

Bidirectional traceability checks both directions:

```text
Forward traceability:
  Requirements -> Implementation -> Tests
  "Was every requirement implemented and tested?"

Backward traceability:
  Tests / Implementation -> Requirements
  "Does every artifact have a requirement justification?"
```

### Mapping Types

| Direction | Mapping | Main issue detected |
|-----------|---------|---------------------|
| Forward | `AC-ID -> implementation -> test` | Unimplemented or untested criteria |
| Backward | `implementation -> AC-ID` | Gold plating or undocumented behavior |
| Test forward | `AC-ID -> test` | Missing test coverage |
| Test backward | `test -> AC-ID` | Orphan tests |

### Output Format

```yaml
BIDIRECTIONAL_TRACEABILITY:
  forward:
    total_criteria: 12
    mapped_to_implementation: 10
    mapped_to_tests: 8
    gaps:
      - criterion_id: AC-LOGIN-007
        type: FORWARD_GAP
        description: "No implementation mapping"
      - criterion_id: AC-LOGIN-003
        type: TEST_GAP
        description: "Implementation exists, no tests"
  backward:
    orphan_implementations:
      - file: src/utils/legacyAuth.ts
        description: "Implementation not mapped to any criterion"
    orphan_tests:
      - file: test/deprecated.test.ts
        description: "Test not mapped to any criterion"
  coverage:
    implementation: 83%
    test: 67%
    full_chain: 67%
```

## Gap Analysis

### Gap Types

| Gap type | Definition | Risk | Detection method |
|----------|------------|------|------------------|
| `Implementation Gap` | Criterion has no implementation mapping | High | Forward trace |
| `Test Gap` | Implementation exists but no mapped test | Medium-High | Forward trace |
| `Specification Gap` | Implementation exists but no mapped criterion | Medium | Backward trace |
| `Coverage Gap` | Tests exist but do not cover the full criterion intent | Medium | Coverage analysis |

### Gap Priority Matrix

```text
Criterion exists + implementation missing -> Implementation Gap
Criterion exists + implementation present + tests missing -> Test Gap
Implementation present + criterion missing -> Specification Gap
Implementation and tests present but incomplete -> Coverage Gap
```

### AUDIT-Mode Sequence

1. Build forward mapping: criteria -> implementation.
2. Build forward mapping: implementation -> tests.
3. Build backward mapping: tests -> criteria.
4. Classify each discovered gap.
5. Calculate L1, L2, and L3 coverage.
6. Report orphan artifacts and remediation priorities.

## Coverage Levels

| Level | Definition | Formula |
|-------|------------|---------|
| `L1` | Requirements coverage | Criteria with implementation / Total criteria |
| `L2` | Test coverage | Criteria with tests / Total criteria |
| `L3` | Full-chain coverage | Criteria with implementation and tests / Total criteria |
| `L4` | Result coverage | Passing criteria / Total criteria |

### Coverage Thresholds

| Level | `CERTIFIED` tendency | `CONDITIONAL` tendency | `REJECTED` tendency |
|-------|----------------------|------------------------|---------------------|
| `L1` | `>= 90%` | `>= 70%` | `< 70%` |
| `L2` | `>= 80%` | `>= 60%` | `< 60%` |
| `L3` | `>= 70%` | `>= 50%` | `< 50%` |

Use `L3` for release confidence when the environment requires full-chain evidence.

## Automation Patterns

### Mapping Techniques

| Technique | Strength | Use when |
|-----------|----------|----------|
| Naming convention | High accuracy | Files or tests include `AC-*` IDs |
| Comment or tag mapping | High accuracy | `@requirement` or `@covers` tags are enforced |
| Pattern matching | Medium accuracy | Route or handler names match criterion language |
| Code search | Medium-Low accuracy | Used as fallback when tags are absent |
| LLM inference | Medium accuracy | Only after deterministic methods are exhausted |

### Recommended Tags

```text
Code:
  // @requirement AC-LOGIN-001
  // @covers AC-LOGIN-001, AC-LOGIN-002

Tests:
  describe('AC-LOGIN-001: Valid credentials grant access', () => { ... })
  // @criterion AC-LOGIN-001

Gherkin:
  @AC-LOGIN-001
  Scenario: Successful login with valid credentials
```

## Audit and Regulatory Use

- Use `AUDIT` mode when the goal is gap analysis, not just verdict issuance.
- Regulated environments often require bidirectional traceability and full-chain coverage.
- For regulated releases, treat `L3` as a release gate and preserve orphan-artifact reporting.

## Anti-Patterns

| Anti-pattern | Symptom | Mitigation |
|-------------|---------|------------|
| Manual-only RTM | Spreadsheet goes stale | Prefer tag-based or generated mapping |
| One-way traceability | Only forward gaps are visible | Require backward mapping too |
| Snapshot RTM | Matrix updated only once | Re-run `AUDIT` continuously |
| Over-granular mapping | Line-by-line trace noise | Keep mapping at criterion level |
| Orphan tolerance | Unmapped code or tests accepted silently | Report as `MEDIUM` or above |
