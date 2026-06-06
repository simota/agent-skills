# Unit Testing Reference

Purpose: Design unit test architecture from scratch or restructure an existing suite so every test has a clear Arrange/Act/Assert shape, the right kind of test double, a single behavioral intent, and deterministic setup. Multi-language: Jest / Vitest, pytest, Go `testing`, `cargo test`.

## Scope Boundary

- **Radar `unit`**: designs unit test *architecture* — AAA discipline, test-double choice, boundary isolation, naming, determinism.
- **Radar `coverage`**: extends an existing suite to fill measured coverage gaps. Uses patterns already established by `unit`.
- **Radar `edge`**: adds boundary / error-branch cases into an existing suite. Does not restructure.
- **Siege / Voyager**: resilience / browser-level scope — out of scope here.

Use `unit` when the suite does not exist yet, is inconsistent across files, or test smells (`arrange >> act`, ambiguous mocks, shared state) are blocking further coverage work.

## AAA Structure

Every unit test is three contiguous blocks, visually separated:

```ts
test('refund exceeding order total is rejected', () => {
  // Arrange
  const order = makeOrder({ total: 1000 });
  const refund = makeRefund({ amount: 1500 });

  // Act
  const result = applyRefund(order, refund);

  // Assert
  expect(result.ok).toBe(false);
  expect(result.reason).toBe('REFUND_EXCEEDS_TOTAL');
});
```

Anti-patterns: assertions mixed into arrange, multiple Act steps per test, Act that mutates shared fixtures.

## Test Double Selection

Pick the weakest double that still proves the behavior. Order of preference:

| Double | Use when | Avoid when |
|--------|----------|------------|
| Fake | An in-memory implementation can replace the collaborator (in-memory repo, fake clock) | The real thing is already fast and deterministic — use it |
| Stub | You need to force a specific return value for a branch | You actually care whether the call happened |
| Mock | You must verify an interaction (side effect on a collaborator) | You only want to shape state — use a stub |
| Spy | You need to assert on a real implementation's calls without replacing it | You don't care about call arguments — drop it |

Rule of thumb: **mock roles, not objects**. Don't mock value types or private internals; replace collaborators at the unit boundary.

## Boundary Isolation

A unit test must not cross its boundary:
- No network, no real clock, no real filesystem, no real DB.
- Inject collaborators (`clock`, `uuid`, `logger`, `repository`) through the constructor or function arguments.
- If the code reaches global state, that's a design signal — surface it in the COOL phase handoff to Zen.

## Naming Conventions

Test names are executable documentation. Prefer `subject_scenario_expected`:

- `applyRefund_whenAmountExceedsTotal_rejects`
- `test_cart_removes_item_when_quantity_reaches_zero`
- `TestUserService_WhenEmailTaken_ReturnsConflict`

Avoid: `test1`, `it_works`, `handles edge case`.

## Determinism Checklist

- Freeze the clock (`vi.useFakeTimers()`, `freezegun`, `clockwork.Mock`, `mockall::mock!`).
- Seed any RNG; assert against the seed.
- Do not rely on map/dict iteration order (Go, Rust HashMap).
- No `sleep`, no real timers, no `Date.now()` unmocked.
- One assertion focus per test — if the Act produces 4 observable effects, write 4 tests unless they share the exact same setup and intent.

## Multi-Language Notes

| Stack | Framework | Doubles | Notes |
|-------|-----------|---------|-------|
| TS / JS | Vitest (preferred) or Jest | `vi.fn()` / `jest.fn()`, MSW for boundary HTTP | Prefer Vitest for Vite projects; Jest for CRA / legacy |
| Python | pytest + pytest-mock | `unittest.mock.Mock`, `pytest-mock.mocker` | Use `freezegun` for clock, `pytest.fixture(scope=...)` carefully |
| Go | `testing` + testify | `gomock` / `mockery` (generated) | Prefer table-driven tests; keep subtests named `TestX/case` |
| Rust | `cargo test` + `mockall` | `mockall::automock`, `#[cfg(test)]` modules | Use `assert2` or `pretty_assertions` for readable diffs |
| Java / Kotlin | JUnit 5 + Mockito | `@Mock`, `@InjectMocks` | Avoid PowerMock — it enables anti-patterns |

## Anti-Patterns

- Testing private methods directly — behavior is observable only at the public boundary.
- `expect(spy).toHaveBeenCalled()` with no argument assertions — a weak mock kill target.
- Shared mutable fixtures at module scope — breaks test isolation (Radar Always: every test isolates setup).
- One mega-test with 20 assertions — split along Act steps.
- `any` in TypeScript test doubles — type the mock to catch drift.

## Handoff

- If test redesign surfaces production-code smells (globals, hard-coded clocks, mixed concerns), hand off to `Zen` with the list of seams needed.
- If the designed suite passes but survives mutants, escalate to `mutation` recipe.
- If boundary isolation requires a real DB / Redis / Kafka to prove value, the test actually belongs in `integration` — move it.
