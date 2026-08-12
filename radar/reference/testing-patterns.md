# Testing Patterns

Purpose: Core TS/JS testing defaults for Radar. Read this when adding unit or integration tests in JavaScript or TypeScript repositories.

Contents:

- AAA and naming rules
- React Testing Library defaults
- MSW and test-data strategy
- Integration test patterns
- Coverage and mock decisions

## Arrange-Act-Assert (AAA)

Use explicit phases. If the test is too small for comments, keep the logical separation anyway.

```typescript
test('adds an item to the cart', () => {
  // Arrange
  const cart = new Cart();
  const item = { id: '1', price: 100 };

  // Act
  cart.add(item);

  // Assert
  expect(cart.items).toHaveLength(1);
  expect(cart.total).toBe(100);
});
```

## Naming Rules

Prefer names that explain behavior, trigger, and outcome.

```typescript
test('GIVEN an empty cart WHEN checkout is clicked THEN it shows an empty warning', () => {
  // ...
});

test('calculateDiscount throws for a negative percentage', () => {
  expect(() => calculateDiscount(100, -5)).toThrow('Invalid percentage');
});
```

Avoid vague names such as `should work`.

## React Testing Library Defaults

### Query Priority

Use the highest semantic query available.

| Priority | Query | Typical Use |
|----------|-------|-------------|
| 1 | `getByRole` | Buttons, links, headings, form controls |
| 2 | `getByLabelText` | Form fields |
| 3 | `getByPlaceholderText` | Input fallback |
| 4 | `getByText` | Static copy |
| 5 | `getByTestId` | Last resort |

### Async Pattern

```typescript
test('shows loading, then data', async () => {
  render(<UserList />);

  expect(screen.getByText('Loading...')).toBeInTheDocument();
  expect(await screen.findByText('John Doe')).toBeInTheDocument();
  expect(screen.queryByText('Loading...')).not.toBeInTheDocument();
});
```

### Provider Wrapper

Use a shared `renderWithProviders` helper when components need router, query client, or store context.

```typescript
function renderWithProviders(ui: React.ReactElement) {
  const queryClient = new QueryClient({
    defaultOptions: { queries: { retry: false } },
  });
  return render(
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>{ui}</BrowserRouter>
    </QueryClientProvider>
  );
}
```

## MSW Defaults

Use MSW for network boundaries in component and integration tests.

```typescript
const server = setupServer(
  http.get('/api/users', () => HttpResponse.json([{ id: 1, name: 'Test User' }])),
);

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());
```

Add dedicated error handlers for `500`, timeout, and malformed payload scenarios.

## Test Data Strategy

| Pattern | Use When | Notes |
|--------|----------|-------|
| Factory | Most tests | Best default; override only relevant fields |
| Fixture object | Small stable datasets | Keep local and readable |
| DB seed | Integration tests with real persistence | Reset state between tests |

Prefer factories over giant fixtures when a suite keeps growing.

## Integration Test Patterns

### API Boundary

```typescript
test('POST /api/orders returns 201 and the created order', async () => {
  const response = await request(app)
    .post('/api/orders')
    .send({ productId: '123', quantity: 2 })
    .expect(201);

  expect(response.body).toMatchObject({
    id: expect.any(String),
    status: 'pending',
  });
});
```

### Database Integration

Use Testcontainers only when realism matters more than setup cost:

- repository and transaction behavior
- migration-sensitive flows
- query correctness against a real engine

If setup cost is high and the repo has no container pattern yet, ask first.

## Coverage Commands

| Goal | Vitest 4.x | Jest 30 |
|------|-----------|---------|
| Full coverage | `pnpm test --coverage` | `pnpm jest --coverage` |
| Specific file | `pnpm test src/foo.test.ts --coverage` | `pnpm jest src/foo.test.ts --coverage` |
| HTML report | `pnpm test --coverage --coverage.reporter=html` | `pnpm jest --coverage --coverageReporters=html` |
| Changed-files only | `pnpm test --coverage --coverage.changed` (Vitest 4.1+) | N/A |

Version notes:
- **Vitest 4.x** (4.0 Oct 2025 / 4.1 Mar 2026): requires Vite ≥6 and Node ≥20; `coverage.changed` limits reporting to changed files; adds custom test tags with `timeout`/`retry` config. Source: [vitest.dev/blog/vitest-4](https://vitest.dev/blog/vitest-4), [vitest.dev/blog/vitest-4-1.html](https://vitest.dev/blog/vitest-4-1.html)
- **Jest 30** (Jun 2025): drops Node 14/16/19/21 support; jsdom upgraded to v26; native TypeScript config support; faster module resolution via `unrs-resolver`. Minimum TypeScript: 5.4. Source: [jestjs.io/blog/2025/06/04/jest-30](https://jestjs.io/blog/2025/06/04/jest-30)

## Mock Strategy Decision Tree

| Dependency | Default | Escalate To |
|-----------|---------|-------------|
| Pure function / local module | No mock | Direct call |
| HTTP API | MSW | Contract test if schema drift matters |
| Database | Fake or repository stub | Testcontainers when SQL behavior matters |
| Time / randomness | Fake timers / fixed seed | Never use real time in flaky-sensitive tests |
| Browser / DOM-only E2E concern | Hand off | Voyager |

## Quick Rules

- Prefer one behavior per test.
- Prefer explicit edge cases over snapshot sprawl.
- Prefer helpers that clarify intent, not helpers that hide assertions.
- Prefer integration tests over deep mock trees once behavior crosses a meaningful boundary.


---

## Recipe Behavior Detail (SKILL.md excerpt)

| Recipe | Behavior |
|---|---|
| Unit Test Design | `unit` | | Design unit test architecture from scratch (AAA, test doubles, boundary isolation) across Jest/Vitest, pytest, Go testing, cargo-test | Design unit test architecture from scratch or restructure an existing suite. Enforce AAA (Arrange-Act-Assert), pick the right test double (fake > stub > mock > spy in that preference order), isolate at the unit boundary, and keep tests deterministic (no clock, network, or filesystem without injection). Multi-language: Vitest 4.x / Jest 30 for TS/JS, pytest 8.x for Python, Go `testing`, `cargo test` / cargo-nextest for Rust, JUnit 5.12+ / JUnit 6 for Java. Use `coverage` instead when the goal is filling gaps in an existing suite, not redesigning it. | `reference/unit-testing.md` |
| Integration Test Design | `integration` | | Design backend-integration test architecture with Testcontainers, WireMock/MSW, DB fixture strategy | Design backend-service integration tests (component-to-component: service ↔ DB / cache / queue / downstream HTTP). Prefer Testcontainers for ephemeral Postgres/MySQL/Redis/Kafka, WireMock or MSW for HTTP stubbing at the boundary, and pick a DB fixture strategy (transaction rollback fastest, truncate if triggers matter, per-test DB only when schema migrations are under test). Playwright API mode is acceptable for backend HTTP assertions. Route to `Voyager` for browser-level E2E and full user journeys — this recipe does NOT cover user-to-system flows. Use `edge` instead when extending an existing integration suite with edge cases. | `reference/integration-testing.md` |
| Mutation Testing | `mutation` | | Run Stryker/PIT/mutmut/cargo-mutants, analyze survivors, triage equivalent mutants, enforce CI mutation-score threshold | Run a mutation testing tool against an existing suite to measure test-suite effectiveness. StrykerJS 7.0+ for JS/TS (supports Vitest, Jest, Node Tap; `npx stryker run`), PIT for Java/Kotlin, mutmut (or cosmic-ray) for Python, cargo-mutants for Rust. Analyze survived mutants as weak assertions, triage equivalent mutants (functionally identical — accept the survivor), and wire a mutation-score threshold into CI (critical modules ≥85%, project-wide ≥60% per Siege baselines). Scope: author-side code-quality mutation (strengthening unit-test assertions day-to-day). Route to `Siege` for program-level mutation strategy, tiered CI (PR/nightly/release) design, operator selection at scale, and mutation as a non-functional resilience verification — Siege owns the broader mutation testing program and Radar `mutation` complements it at the individual-developer layer. | `reference/mutation-testing.md` |


## Collaboration Handoffs (SKILL.md excerpt)

Radar receives bug reports, implementation changes, review findings, coverage gaps, and refactoring safety requests. Radar returns test infrastructure needs, quality metrics, E2E escalations, coverage reports, CI optimization handoffs, and story alignment updates.

| Direction | Handoff | Purpose |
|-----------|---------|---------|
| Scout → Radar | `SCOUT_TO_RADAR_HANDOFF` | Bug report with repro needs regression safety net |
| Builder → Radar | `BUILDER_TO_RADAR_HANDOFF` | New feature or API needs test coverage |
| Judge → Radar | `JUDGE_TO_RADAR_HANDOFF` | Review findings identify weak tests or missing assertions |
| Guardian → Radar | `GUARDIAN_TO_RADAR_HANDOFF` | Coverage gaps require targeted tests |
| Zen → Radar | `ZEN_TO_RADAR_HANDOFF` | Refactored code needs pre/post safety coverage |
| Flow → Radar | `FLOW_TO_RADAR_HANDOFF` | Timing-sensitive UI changes need stability coverage |
| Vitrine → Radar | `SHOWCASE_TO_RADAR_HANDOFF` | Component coverage gaps need test follow-up |
| Oracle → Radar | `ORACLE_TO_RADAR_HANDOFF` | AI-assisted test generation strategy and evaluation patterns |
| Sentinel → Radar | `SENTINEL_TO_RADAR_HANDOFF` | Security-critical code paths requiring thorough coverage |
| Radar → Voyager | `RADAR_TO_VOYAGER_HANDOFF` | Browser-level flow should be validated end to end |
| Radar → Gear | `RADAR_TO_GEAR_HANDOFF` | CI selection, caching, sharding, or runner config is the bottleneck |
| Radar → Builder | `RADAR_TO_BUILDER_HANDOFF` | Test infrastructure or fixture needs implementation support |
| Radar → Judge | `RADAR_TO_JUDGE_HANDOFF` | Tests need adversarial review or quality scoring |
| Radar → Zen | `RADAR_TO_ZEN_HANDOFF` | Test code needs readability refactoring after behavior is secured |
| Radar → Vitrine | `RADAR_TO_SHOWCASE_HANDOFF` | Component behavior is covered and stories should be aligned |
| Radar → Guardian | `RADAR_TO_GUARDIAN_HANDOFF` | Coverage reports for governance tracking |
| Radar → Oracle | `RADAR_TO_ORACLE_HANDOFF` | AI/LLM-specific testing and evaluation strategy delegation |

### Overlap Boundaries

| Pair | Radar Owns | Partner Owns | Escalation |
|------|-----------|--------------|------------|
| Radar / Voyager | Unit and integration tests, component-level assertions | Browser-level E2E, full user journey flows | Radar hands off when test requires browser context or multi-page navigation |
| Radar / Judge | Test implementation and coverage improvement | Code review findings, quality scoring, bug detection | Judge identifies weak tests → Radar implements fixes |
| Radar / Builder | Test code, fixtures, mocks | Production code, business logic, API endpoints | Radar requests test infrastructure support from Builder when needed |
| Radar / Guardian | Test execution and coverage measurement | Git/PR governance, commit strategy, coverage policy | Guardian sets coverage thresholds → Radar meets them |
| Radar / Gear | Test selection strategy, skip conditions | CI runner config, caching, sharding, Docker builds | Radar proposes selection → Gear implements CI pipeline changes |
| Radar / Oracle | Traditional software test coverage and mutation testing | AI/LLM evaluation, prompt testing, model quality assessment | Radar tests deterministic code; Oracle handles probabilistic AI evaluation |
| Radar / Sentinel | Test coverage for security-critical paths | SAST scanning, vulnerability detection, security policy | Sentinel identifies critical paths → Radar ensures 100% coverage |

