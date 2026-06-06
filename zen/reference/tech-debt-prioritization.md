# Technical Debt Prioritization & Safe Refactoring Strategies

Purpose: Use this file when Zen must choose what to refactor first or needs a safe migration pattern for larger debt.

## Contents
- [Debt Types](#debt-types)
- [Hotspot Analysis](#hotspot-analysis)
- [Code Health and Zen Metrics](#code-health-and-zen-metrics)
- [Safe Migration Strategies](#safe-migration-strategies)
- [ROI Framing](#roi-framing)
- [Prioritization Guide](#prioritization-guide)

## Debt Types

| Type | Signal | How to detect |
|------|--------|---------------|
| **Complex Hot Code** | High complexity + high change frequency | Hotspot analysis |
| **Decaying Code** | Quality trends worsening over time | Code-health trend review |
| **Coordination Problems** | Team structure leaks into code churn | Developer-fragmentation analysis |
| **Excess Coupling** | Dense dependency graph | Dependency analysis |
| **Developer Fragmentation** | Too many occasional contributors in one area | Version-control history |

## Hotspot Analysis

Hotspot rule:

`hotspot = high change frequency x low code quality`

Use these as prioritization guidance, not as rigid gates:

- Hotspots often occupy only `2-3%` of a codebase.
- They can still absorb `11-16%` of all commits.
- `25-70%` of reported or fixed bugs may cluster there.

### Priority matrix

| Change frequency | Code quality | Priority |
|------------------|--------------|----------|
| High | Low | Refactor first |
| High | High | Maintain and protect |
| Low | Low | Monitor or schedule later |
| Low | High | Leave alone |

### Zen application

When Atlas sends a hotspot:

1. Take the highest-value hotspot first.
2. Limit execution to `1 hotspot = 1 Focused refactor`.
3. Verify improvement with Before/After metrics.

## Code Health and Zen Metrics

### Code-health interpretation

| Score | Meaning |
|-------|---------|
| `1-3` | Unhealthy; high defect and delivery drag |
| `4-6` | Warning zone; improve when touched |
| `7-10` | Healthy; keep stable |

### Zen's internal quality targets

Measure these before and after:

- Cyclomatic Complexity
- Cognitive Complexity
- Nesting Depth
- Function length
- Parameter count
- Code-duplication percentage

Target values:

- `CC: 15-25%` reduction
- `Cognitive: bring the target below the active threshold`
- `Nesting: <=3`
- `Function LOC: <=50`
- `Parameters: <=5`

## Safe Migration Strategies

Use these only when the task exceeds normal Focused refactoring.

### Strangler Fig Pattern

Use when replacing an entire legacy component gradually.

1. Pick a low-dependency, high-value entry point.
2. Add a routing or facade layer.
3. Start with a small non-critical component.
4. Validate old and new outputs side by side when possible.
5. Shift traffic gradually: `10% -> 50% -> 100%`.
6. Decommission the legacy path only after full validation.

### Branch by Abstraction

Use when old and new implementations must coexist behind one interface.

1. Add the abstraction first.
2. Route current callers through it.
3. Introduce the new implementation behind the same contract.
4. Switch with a feature flag when needed.
5. Remove the old implementation only after stability is proven.

### Parallel Change (Expand-Contract)

Use for public API renames or backward-compatible interface changes.

1. **Expand**: add the new interface while keeping the old one.
2. **Migrate**: move callers gradually.
3. **Contract**: remove the old interface after migration completes.

This is the preferred safety pattern for `Ask first` public API changes.

## ROI Framing

| Axis | Typical measure | Example |
|------|------------------|---------|
| **Technical** | Complexity, duplication, performance | `CC -20%` |
| **Business** | Delivery speed, defect rate, time-to-market | Deployment frequency `2x` |
| **Cost** | Maintenance effort, operational burden | Maintenance effort `-30%` |

Practical constraint: many teams spend `60-80%` of their IT budget maintaining existing systems. Zen should therefore focus on high-ROI debt, not "clean everything" cleanup.

## Prioritization Guide

1. Is this a hotspot?
   - Yes: refactor first.
2. Is the area already being changed soon?
   - Yes: apply the Boy Scout Rule during that work.
3. Is the area a recurring bug source?
   - Yes: prioritize targeted cleanup.
4. Otherwise:
   - Document it and leave it for a later cycle.

Rules:

- Do not chase perfection.
- Prefer high-ROI targets.
- Keep each execution pass inside the active scope tier.

**Source:** [CodeScene: Prioritize Technical Debt](https://codescene.com/blog/tech-debt-examples-prioritize-technical-debt-with-codescene) · [CodeScene: Code Health Metric](https://codescene.com/product/code-health) · [CodeScene: Behavioral Code Analysis](https://codescene.com/product/behavioral-code-analysis) · [Gocodeo: Strangler Fig Pattern](https://www.gocodeo.com/post/how-the-strangler-fig-pattern-enables-safe-and-gradual-refactoring) · [AWS: Branch by Abstraction](https://docs.aws.amazon.com/prescriptive-guidance/latest/modernization-decomposing-monoliths/branch-by-abstraction.html) · [Martin Fowler: Strangler Fig](https://martinfowler.com/bliki/StranglerFigApplication.html)
