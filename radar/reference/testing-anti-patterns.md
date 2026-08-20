# Testing Anti-Patterns & Quality Metrics
Purpose: Detect weak tests before they create false confidence. Read this when auditing test quality or when a suite “passes” but still feels unsafe.
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
## Test Smell Checklist
- `beforeEach` longer than `20` lines
- test file longer than `500` lines
- more than `5` assertions in one test
- numbered or vague test names
- branches inside the test body
- loops where parameterized tests would be clearer
- copied production logic inside tests
- magic numbers with no intent
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

## Canonical Tautology Patterns

Moved from `SKILL.md` § Core Contract 2026-08-20. A test matching any of these asserts nothing about behavior:

1. **field-exists-only** — asserts a key is present, never its value
2. **call-happened-only** — asserts a collaborator was invoked, never with what or to what effect
3. **no-throw-only** — asserts the call did not raise, never what it produced
4. **mirrors implementation's exact arithmetic** — recomputes the expression under test in the assertion
5. **length/count-only** — asserts collection size, never element identity
6. **snapshot-as-sole-oracle** — a snapshot is the only assertion, so any change is "expected"

The rule these serve: **≥1 behavioural assertion per public path.**
