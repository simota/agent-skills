# Mutation Testing Guide

Purpose: Use this file for baseline mutation workflows, tool setup, survivor analysis, CI wiring, and default score thresholds in `MUTATE` mode.

## Contents

- Mutation workflow
- Tool configuration
- Survivor analysis
- CI integration
- Baseline thresholds

## Mutation Workflow

```text
1. Parse source code
2. Apply small mutations
3. Run tests against each mutant
4. Classify outcomes:
   - Killed
   - Survived
   - Timed out
   - No coverage

Mutation Score = Killed / (Total - No Coverage) × 100
```

## Common Mutation Operators

| Category | Mutation | Example |
| --- | --- | --- |
| Arithmetic | replace operator | `a + b` -> `a - b` |
| Conditional | negate condition | `a > b` -> `a <= b` |
| Boundary | off-by-one | `a > 0` -> `a >= 0` |
| Return value | change return | `true` -> `false` |
| Remove call | delete function call | `validate(input)` -> removed |
| String | empty string | `"error"` -> `""` |
| Assignment | change value | `x = 1` -> `x = 0` |

## Tool Configuration

### Stryker

```json
{
  "mutate": ["src/**/*.ts", "!src/**/*.test.ts", "!src/**/*.d.ts"],
  "testRunner": "jest",
  "reporters": ["html", "clear-text", "progress"],
  "coverageAnalysis": "perTest",
  "thresholds": {
    "high": 80,
    "low": 60,
    "break": 50
  },
  "timeoutMS": 10000,
  "concurrency": 4
}
```

```bash
npx stryker run
npx stryker run --mutate "src/utils/validation.ts"
```

### mutmut

```ini
[mutmut]
paths_to_mutate=src/
tests_dir=tests/
runner=pytest -x --tb=no -q
```

```bash
mutmut run
mutmut run --paths-to-mutate src/validation.py
mutmut results
mutmut show 42
```

### cargo-mutants

```bash
cargo mutants
cargo mutants --file src/validation.rs
cargo mutants -j 4
cargo mutants --timeout 30
```

## Survivor Analysis

| Pattern | Why it survives | Fix |
| --- | --- | --- |
| Missing boundary test | `>` vs `>=` not exercised | add boundary-value tests |
| Missing negative test | only happy path exists | add error and edge-case tests |
| Weak assertion | only presence is checked | assert exact values |
| Dead code | path is unreachable | remove dead code |
| Equivalent mutant | behavior is unchanged | mark as ignored or escalate to advanced review |

### Workflow

```markdown
1. Run mutation testing
2. Sort survivors by file or module
3. Classify each survivor:
   a. equivalent mutant
   b. dead code
   c. missing test
4. Re-run to confirm improvement
5. Track score over time
```

## CI Integration

```yaml
mutation-test:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-node@v4
    - run: npm ci
    - run: npx stryker run
```

### Incremental Mode

```bash
CHANGED_FILES=$(git diff --name-only HEAD~1 -- 'src/**/*.ts' | tr '\n' ',')
npx stryker run --mutate "$CHANGED_FILES"
```

## Baseline Thresholds

| Context | Minimum | Recommended |
| --- | --- | --- |
| Critical business logic | `80%` | `90%+` |
| Utility functions | `70%` | `80%+` |
| API handlers | `60%` | `70%+` |
| UI components | `50%` | `60%+` |
| Overall project | `60%` | `75%+` |
