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
