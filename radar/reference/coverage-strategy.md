# Coverage Strategy

Purpose: Choose the right coverage signal, enforce safe thresholds, and separate real risk from vanity metrics. Read this when Radar runs in `AUDIT` mode or when a team wants stronger coverage gates.

Contents:

- coverage type selection
- code-type thresholds
- diff coverage and ratchets
- dead code triage
- anti-patterns

## Coverage Types Decision Matrix

| Type | What It Measures | Blind Spot |
|------|------------------|------------|
| Line | Whether a line executed | Misses branch combinations |
| Branch | Whether each branch executed | May still miss condition permutations |
| Function | Whether each function ran | Does not prove meaningful assertions |
| Statement | Whether each statement ran | Similar limits to line coverage |
| Condition | Whether boolean conditions hit both outcomes | Tooling support is inconsistent |

## Recommended Metrics By Code Type

| Code Type | Primary | Secondary | Target | Notes |
|----------|---------|-----------|--------|-------|
| Business logic | Branch | Line | `85%+` | Default high-value target |
| API handlers | Line | Function | `80%+` | Endpoint breadth matters |
| Utilities / helpers | Branch | Line | `90%+` | Reused code deserves stronger gates |
| UI components | Function | Line | `70%+` | Rendering and interaction are the main concern |
| Generated code | Exclude | — | Exclude | Do not game the metric |
| Config / constants | Exclude | — | Exclude | No logic to test |

## Judge Integration

If coverage must feed Judge's UQS, keep the composite weighting intact:

```text
radar_score = (line × 0.4) + (branch × 0.4) + (function × 0.2)
```

That weighting makes branch improvements the highest-leverage change when line coverage is already acceptable.

## Diff Coverage

Use diff coverage to stop new code from lowering quality.

```bash
pip install diff-cover
npx vitest run --coverage
diff-cover coverage/lcov.info --compare-branch=main --fail-under=80
```

Default rule:

- new or changed lines should stay at `80%+`
- do not accept lower diff coverage just because global coverage is high

## Framework Coverage Config

### Vitest

```typescript
export default defineConfig({
  test: {
    coverage: {
      provider: 'v8',
      reporter: ['text', 'lcov', 'json-summary'],
      thresholds: {
        lines: 80,
        branches: 80,
        functions: 75,
        statements: 80,
      },
    },
  },
});
```

### Jest

```javascript
module.exports = {
  coverageDirectory: 'coverage',
  coverageReporters: ['text', 'lcov', 'json-summary'],
  coverageThreshold: {
    global: {
      lines: 80,
      branches: 80,
      functions: 75,
      statements: 80,
    },
  },
};
```

### pytest / Go / Java

```bash
pytest --cov=src --cov-report=term-missing --cov-report=lcov:coverage/lcov.info
go test ./... -coverprofile=coverage.out -covermode=atomic
go tool cover -func=coverage.out
```

Use JaCoCo bundle rules with `0.80` line coverage as the default floor unless the repo already uses a stricter gate.

## Coverage Ratchet Strategy

Ratchet upward instead of chasing an arbitrary global number.

### Rules

- PR coverage must be `>=` the default branch coverage
- changed modules should not regress below their current baseline
- weak modules should improve incrementally, not be exempt forever

### Per-Module Example

| Module | Current | Minimum For PR | Target |
|--------|---------|----------------|--------|
| core | `88%` | `88%` | `90%` |
| api | `75%` | `75%` | `80%` |
| utils | `92%` | `92%` | `90%` |

## Dead Code vs Untested Code

| Case | Meaning | Action |
|------|---------|--------|
| Untested reachable code | Real behavior with no safety net | Add tests or accept explicit risk |
| Dead code | Behavior no caller can reach | Confirm with static analysis, then route to Sweep or Void if cleanup is intended |

Do not raise coverage by testing code that should be deleted.

## Multi-Module Coverage

Useful patterns:

- merge `lcov.info` files for monorepos
- use Codecov flags per package
- keep one combined HTML report for local triage

Example:

```bash
npx lcov-result-merger 'packages/*/coverage/lcov.info' merged.lcov
genhtml merged.lcov --output-directory combined-coverage
```

## Anti-Patterns

| Anti-Pattern | Why It Fails | Better Rule |
|--------------|--------------|-------------|
| `100%` target everywhere | Diminishing returns and test-maintenance waste | Use code-type targets plus mutation score |
| Assertion-free tests | Inflates line coverage without safety | Review assertion quality with Judge |
| Covering generated code | Numbers rise, signal does not | Exclude generated and config files |
| Coverage gaming | Adds meaningless tests | Tie coverage to behavior and review |
| Global-only threshold | Hides weak hotspots | Add diff and per-module gates |
| Ignoring branch coverage | Misses decision logic gaps | Track branch coverage on logic-heavy code |
| Coverage without review | Metric replaces engineering judgment | Pair with flaky, mutation, and smell checks |

## Quick Reference

| Metric | Good Default | Stretch Target | Tooling |
|--------|--------------|----------------|---------|
| Line | `80%+` | Ratchet upward | v8 / istanbul / coverage.py / JaCoCo |
| Branch | `80%+` for logic-heavy modules | `85%+` on core logic | Same |
| Function | `75%+` | Context-specific | Same |
| Diff | `80%+` | Ratchet upward | diff-cover |
| Mutation Score | `75%+` | `90%+` critical code | Stryker / mutmut / cargo-mutants |
