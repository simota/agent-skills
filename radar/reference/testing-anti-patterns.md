# Testing Anti-Patterns & Quality Metrics

Purpose: Detect weak tests before they create false confidence. Read this when auditing test quality or when a suite “passes” but still feels unsafe.

Contents:

- the 13 core anti-patterns
- pyramid mistakes
- quality metrics
- test smells and review checklist

## 13 Core Anti-Patterns

| Pattern | Symptom | Fix |
|---------|---------|-----|
| The Liar | Test passes but asserts nothing meaningful | Require behavior-level assertions |
| Excessive Setup | Setup is longer than the test intent | Use factories and smaller helpers |
| The Giant | One test checks too many behaviors | Split by behavior |
| The Mockery | Deep mock chains replace real behavior | Prefer integration at the right boundary |
| The Inspector | Test reaches into internals | Assert public behavior only |
| Generous Leftovers | Shared state leaks between tests | Reset state per test |
| The Local Hero | Works only on one machine | Reproduce in CI-like conditions |
| The Nitpicker | Tiny implementation changes break tests | Assert outputs, not incidental structure |
| The Secret Catcher | Exceptions are swallowed indirectly | Assert the intended failure path |
| The Dodger | Only easy code gets tested | Prioritize risky logic |
| The Slow Poke | Suite is too slow to trust | Use selection, caching, and faster layers |
| Chain Gang | Tests depend on order | Remove cross-test coupling |
| The Flickering Test | Nondeterministic pass/fail | Use the flaky guide immediately |

## Test Pyramid Anti-Patterns

| Shape | Problem | Better Move |
|------|---------|-------------|
| Ice Cream Cone | Too many manual and E2E tests | Push more checks down to unit and integration layers |
| Hourglass | Unit and E2E exist, integration is missing | Add boundary-focused integration tests |

Correct baseline:

| Layer | Share | Runtime |
|-------|-------|---------|
| Unit | `70%` | `< 10ms` |
| Integration | `20%` | `< 1s` |
| E2E | `10%` | `< 30s` |

## Quality Metrics

| Metric | Target |
|--------|--------|
| Line coverage | `80%+` |
| Branch coverage | `70%+` |
| Mutation score | `60%+`, or `80%+` for critical code |
| Assertion density | `1-3` meaningful assertions per test |
| Unit suite runtime | `< 5min` |
| Flaky rate | `< 1%` |
| MTTR | `< 1h` |

Coverage alone is not a quality verdict.

## Test Smell Checklist

Structural smells:

- `beforeEach` longer than `20` lines
- test file longer than `500` lines
- more than `5` assertions in one test
- numbered or vague test names

Logic smells:

- branches inside the test body
- loops where parameterized tests would be clearer
- copied production logic inside tests
- magic numbers with no intent

Dependency smells:

- three or more nested mock layers
- direct dependence on real time, randomness, filesystem, or network
- hidden order dependence

## Review Checklist

- test name explains the behavior
- AAA or an equally explicit structure is visible
- edge cases, nulls, empties, and error paths are covered where relevant
- behavior is asserted instead of internals
- data setup is concise and intention-revealing
- the test can fail for the right reason
