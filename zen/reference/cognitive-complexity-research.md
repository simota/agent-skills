# Cognitive Complexity Research & Metrics

Purpose: Use this file when readability problems are driven by control flow, nesting, or test-specific complexity.

## Contents
- [Metric Comparison](#metric-comparison)
- [Operational Thresholds](#operational-thresholds)
- [Test-Aware Complexity (CCTR)](#test-aware-complexity-cctr)
- [Complexity Drivers](#complexity-drivers)
- [Zen Workflow](#zen-workflow)
- [Tool Configuration](#tool-configuration)

## Metric Comparison

| Dimension | Cognitive Complexity | Cyclomatic Complexity |
|-----------|----------------------|-----------------------|
| Focus | Human readability and comprehension effort | Number of execution paths and test burden |
| Nesting sensitivity | Yes | No |
| Best use | Prioritize readability cleanup | Estimate path complexity and test surface |
| Limitation | Not a full predictor of maintainability | Misses nested readability pain |

Research remains clear on one point: cognitive complexity is useful for prioritization, but it is not a substitute for domain understanding.

## Operational Thresholds

### Primary metrics

| Metric | Thresholds | Tool examples |
|--------|------------|---------------|
| **Cognitive Complexity** | `0-5 low`, `6-10 medium`, `11-15 high`, `16+ critical` | SonarQube, ESLint |
| **Cyclomatic Complexity** | `1-10 low`, `11-20 medium`, `21-50 high`, `50+ critical` | SonarQube, ESLint, PMD |
| **Maintainability Index** | `0-9 high risk`, `10-19 medium`, `20-100 healthy` | VS Code analysis, SonarQube |
| **Nesting Depth** | `1-2 low`, `3 medium`, `4 high`, `5+ critical` | ESLint `max-depth` |

### Supporting metrics

| Metric | Target |
|--------|--------|
| Code churn rate | `<=3` quick rewrites per area |
| PR size | `200-400 LOC` |
| Change failure rate | `<15%` |
| Review time | `<24-48 hours` |

## Test-Aware Complexity (CCTR)

CCTR matters when test code looks simple to traditional tools but is still hard to understand.

- Standard cognitive-complexity tools often under-score generated or annotation-heavy tests.
- CCTR adds test-specific signals such as assertion density, test-structure patterns, and semantic roles.
- Use CCTR as a secondary aid when refactoring tests; keep `test-refactoring.md` as the primary operational guide.

## Complexity Drivers

| Driver | Typical signal | Preferred response |
|--------|----------------|--------------------|
| Too many conditionals | Large `if/else` or `switch` chains | Guard clauses, strategy pattern |
| Deep nesting | `4+` levels of indentation | Early return, extract method |
| Poor naming | Ambiguous identifiers | Rename, explaining variables |
| Tight coupling | Components know too much about each other | Interface split, dependency inversion |
| Large functions or classes | Hundreds of lines, overloaded responsibilities | Extract method/class, SRP |
| Inconsistent conventions | Mixed naming and patterns | Consistency audit |
| Essential complexity | The domain itself is hard | Clarify abstractions without over-abstracting |
| Unfamiliar codebase | Readers lack context | Improve naming and documentation anchors |

## Zen Workflow

1. Measure `Before` with the same toolset you will use for `After`.
2. Identify the main driver, not just the loudest symptom.
3. Pick one recipe at a time.
4. Apply the change inside the active scope tier.
5. Re-measure and verify that the improvement is real.

Preferred target for focused cleanup: reduce cyclomatic complexity by `15-25%` without changing behavior.

## Tool Configuration

### ESLint

```json
{
  "rules": {
    "complexity": ["warn", 15],
    "max-depth": ["warn", 4],
    "max-lines-per-function": ["warn", 50],
    "max-params": ["warn", 5]
  }
}
```

### SonarQube

```properties
sonar.cognitive_complexity.threshold=15
sonar.complexity.threshold=20
```

### Python (Radon)

```bash
radon cc src/ -a -nc
radon mi src/ -s
radon hal src/
```

**Source:** [ScienceDirect: Cognitive Complexity as Predictor](https://www.sciencedirect.com/science/article/abs/pii/S0164121222002370) · [Arxiv: Rethinking Cognitive Complexity for Unit Tests (CCTR)](https://www.arxiv.org/abs/2506.06764) · [Axify: Cognitive Complexity Explained](https://axify.io/blog/cognitive-complexity) · [DX: Cognitive Complexity in Engineering](https://getdx.com/blog/cognitive-complexity/) · [Arxiv: How Developers Improve Code Readability](https://arxiv.org/pdf/2309.02594)
