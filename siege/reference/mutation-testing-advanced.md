# Mutation Testing Advanced Strategies

Purpose: Use this file for equivalent-mutant handling, risk-based thresholds, CI tiering, and advanced mutation recommendations.

## Contents

- Equivalent mutants
- Modern detection approaches
- Performance optimization
- Risk-based thresholds
- Mutation anti-patterns
- Property-based testing synergy

## Equivalent Mutants

- Equivalent mutants change source code without changing behavior.
- They cannot be killed by tests and distort the denominator of the mutation score.
- Corrected score:

```text
Score = Killed / (Total - Equivalent) × 100
```

### Common Patterns

| Pattern | Example | Why it is equivalent |
| --- | --- | --- |
| Dead code mutation | unreachable branch change | path never executes |
| Redundant operation | `x = x + 0` -> `x = x - 0` | same outcome |
| Overflow guard | `>` -> `>=` | boundary value never occurs |
| Boolean tautology | mutate always-true logic | behavior unchanged |
| String constant | log message mutation | no runtime effect |
| Idempotent call | duplicate idempotent operation | result unchanged |

## Detection Approaches

| Method | Precision | Cost | Notes |
| --- | --- | --- | --- |
| Manual review | high | very high | accurate but unscalable |
| Compiler or bytecode comparison | medium | low | good first-pass suppression |
| Constraint solving | medium-high | medium | stronger proof but heavier |
| Program analysis | medium | medium | useful for repeated heuristics |
| ML classifiers | high | medium | recent research shows strong F1 |
| LLM-assisted review | mixed | medium | useful as triage, not sole authority |

## Performance Optimization

| Strategy | Typical gain | Use |
| --- | --- | --- |
| Incremental mutation | `60-90%` | mutate changed files only |
| Parallel execution | near-linear | run with `--threads=N` or equivalent |
| Coverage filtering | `30-50%` | skip uncovered code |
| Operator selection | `20-40%` | disable low-value operators |
| Early termination | `10-30%` | stop on first failing test |
| Result caching | `20-40%` | skip unaffected or repeated work |

## Tiered CI Integration

| Tier | Scope | Threshold style | Time budget |
| --- | --- | --- | --- |
| `Tier 1` PR/commit | changed files only | warn-only | `< 5 min` |
| `Tier 2` nightly/merge | changed module | module thresholds | `< 30 min` |
| `Tier 3` weekly/release | full codebase | project threshold | no strict limit |

## Risk-Based Thresholds

| Risk level | Example modules | Minimum | Recommended |
| --- | --- | --- | --- |
| `CRITICAL` | payment, auth, crypto | `85%` | `95%+` |
| `HIGH` | business logic, validation | `75%` | `85%+` |
| `MEDIUM` | API handlers, middleware | `65%` | `75%+` |
| `LOW` | utils, logging, config | `50%` | `65%+` |
| `MINIMAL` | UI components, tests | — | `50%+` |

### Heuristics

```text
CRITICAL: payment, billing, auth, crypto, security, or @critical
HIGH: service, domain, model, or external API access
MEDIUM: controller, handler, middleware
LOW: util, helper, config, logger
MINIMAL: component, view, test
```

## Mutation Anti-Patterns

| ID | Anti-pattern | Fix |
| --- | --- | --- |
| `MA-01` | Big Bang Mutation | use incremental and tiered execution |
| `MA-02` | Score Obsession | set realistic goals after excluding equivalent mutants |
| `MA-03` | Assertion Inflation | improve behavior coverage, not only assertion count |
| `MA-04` | Uniform Threshold | apply risk-based thresholds |
| `MA-05` | Mutation Without Coverage | reach about `80%+` coverage first |
| `MA-06` | Ignoring Survivors | classify every survivor |
| `MA-07` | Test-Only Mutation | also simplify design when survivors reveal structural issues |

## Property-Based Testing Synergy

```text
1. Mutation testing reveals weak tests.
2. Property-based testing improves invariant coverage.
3. Better invariants reduce the impact of equivalent-mutant noise.
```

## Routing Notes

- Hand survivor-driven test improvements to `Radar`.
- Keep Siege focused on classification, thresholding, and test-quality evidence.
