# Complexity Metrics & Technical Debt Measurement

Purpose: Use this file when complexity or technical debt should feed directly into Void scoring.

Contents:
- Cognitive-complexity scoring rules and thresholds
- Technical-debt metrics and cost multipliers
- Tooling and review gates
- Reduction strategies and how to map results into Void

## Cognitive Complexity

### Scoring Rules

```text
Base additions:
  +1 for control-flow branches
  +1 for loops
  +1 when logical operators switch type
  +1 for labeled jump flow
  +1 for recursion

Nesting penalty:
  +1 for each additional nesting level

Do not count:
  - simple null checks with early return
  - switch default
  - try/catch itself, though nested logic still counts
```

### Thresholds

| Cognitive complexity | Assessment | Action | Void mapping |
|----------------------|------------|--------|--------------|
| `<15` | maintainable | keep monitoring | `Cognitive Load: 0-3` |
| `15-25` | warning zone | simplify soon | `Cognitive Load: 4-6` |
| `>25` | dangerous | prioritize simplification | `Cognitive Load: 7-10` |

### Cognitive vs Cyclomatic Complexity

| Dimension | Cognitive complexity | Cyclomatic complexity |
|-----------|----------------------|------------------------|
| Measures | Human understandability | Number of execution paths |
| Nesting penalty | Yes | No |
| Switch handling | Constant treatment | Per case |
| Best use | Readability and maintainability | Test-path planning |

## Maintenance Cost Signals

Research-backed signals worth preserving:
- Complex code can cost `2.5-5x` more to maintain.
- Methods above `25` complexity can show roughly `3x` bug density.
- Teams may spend `60%+` of dev time understanding code before changing it.

## Technical Debt Metrics

| Metric | Target |
|--------|--------|
| Technical debt ratio | `<5%` |
| Debt growth per sprint | Downward trend |
| SQALE rating | `A-B` |

SQALE reference bands:
- `A`: `<5%`
- `B`: `6-10%`
- `C`: `11-20%`
- `D`: `21-50%`
- `E`: `>50%`

## Tooling

| Tool | Strength |
|------|----------|
| SonarQube | Cognitive complexity, debt, code smells |
| CodeClimate | Cognitive complexity and testability |
| ESLint `complexity` | JS/TS cyclomatic complexity |
| `radon` | Python complexity and maintainability |
| `gocyclo` | Go cyclomatic complexity |

## Review Gates

- New methods should stay below cognitive complexity `15`.
- Existing methods that increase complexity need explicit justification.
- Module average complexity should stay below `10`.
- Technical debt ratio above `10%` should trigger a debt-repayment plan.

## Reduction Strategies

| Pattern | Typical effect |
|---------|----------------|
| Early return | Removes deep nesting |
| Method extraction | Shrinks local branch density |
| Table-driven logic | Replaces long conditional chains |
| Polymorphism | Replaces oversized dispatch conditionals when justified |
| State pattern | Removes state x action conditional nesting when justified |

Priority:
1. Remove deep nesting first.
2. Split oversized methods next.
3. Simplify compound conditions.
4. Use structural redesign only when simpler moves are exhausted.

## Void Use

- During `WEIGH`, map cognitive complexity directly into the `Cognitive Load` dimension.
- Use debt ratio as a supporting signal, not a replacement for the 5-question investigation.
- During `SUBTRACT`, recommend simplification only when the abstraction cost is lower than the expected payoff.

Quality gates:
- complexity `>25` -> immediate `SIMPLIFY` candidate
- technical debt ratio `>10%` -> propose a repayment plan
- rising module-average complexity -> warn
- `60%+` of dev time spent on code comprehension -> process simplification candidate

Sources: [SonarSource: Cognitive Complexity](https://www.sonarsource.com/docs/CognitiveComplexity.pdf) · [Martin Fowler: Technical Debt Quadrant](https://martinfowler.com/bliki/TechnicalDebtQuadrant.html) · [SQALE](http://www.sqale.org/)
