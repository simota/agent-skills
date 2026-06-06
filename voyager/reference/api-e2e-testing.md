# API E2E Testing Reference

Purpose: Validate a user journey that is expressed as a chain of HTTP calls rather than browser interactions. The assertion set spans HTTP response, persisted state, and downstream-API effects — it is not a single-endpoint unit test.

## Scope Boundary

- **Voyager `api`**: user-journey E2E through the API-only interface. HTTP → state → downstream-API is the unit of validation. No browser.
- **Radar `integration`**: service-to-service backend internals (DB, cache, queue, message bus). Runs inside the service process, not over HTTP.
- **Probe `api`**: security DAST (OWASP ZAP / Burp) — looks for vulnerabilities, not functional correctness.
- **Gateway**: authors the OpenAPI spec and contract. Voyager `api` consumes that spec and verifies observable conformance.
- **Siege**: load / chaos over the same surface. Voyager measures correctness first; Siege stresses it after.

If the question is "does POST /orders → GET /orders/:id → GET /inventory stay consistent?" → `api`. If it is "is SELECT ... FOR UPDATE correct?" → Radar `integration`.

## When to Pick `api` Over `playwright`

- The journey has no UI (B2B API, webhook callback, server-to-server integration).
- The UI variant is covered by `playwright` and duplicating it at API level costs more than it finds.
- The team needs a smoke tag that runs in under 60 seconds (Playwright browser boot is too expensive).
- A schema change is landing and a contract check must gate the merge.

## Stack Selection

| Tool | Pick when | Skip when |
|------|-----------|-----------|
| Playwright `APIRequestContext` | Already using Playwright; want one runner for UI + API; need shared fixtures, trace, and reporter | Team has no Node.js toolchain |
| supertest + vitest/jest | Backend-only repo (Node); tests colocated with services | Need cross-language / cross-repo runs |
| REST Assured (Java) | JVM backend; contract + functional in one harness | JS-centric org |
| Bruno / Hurl | Human-authored `.http` suites checked into git; low-code contributors | Complex chained state logic |
| Pact | Consumer-driven contract verification | Functional correctness is the only goal |

Default: **Playwright APIRequestContext** when the project already runs Playwright for UI. It reuses `storageState`, fixtures, and reporter — no second toolchain.

## Workflow

```
PLAN       → list journeys (signup → first-order → refund chain, not single endpoints)
           → choose mock-vs-real backend toggle (env: API_BACKEND=mock|real)
           → pin real backend for @critical smoke tag
           → identify cross-endpoint invariants (order total == sum(line_items))

AUTOMATE   → create APIRequestContext fixture with base URL + auth
           → chain calls; store IDs returned from POST into test scope
           → assert response shape AND state (GET back the resource)
           → assert downstream side effect (inventory decremented, event emitted)

STABILIZE  → isolate test data per run (tenant/account prefix, cleanup after)
           → retry on transient 5xx only, never on 4xx
           → record request/response trace on failure

SCALE      → shard by journey, not by endpoint
           → publish contract-test follow-up: handoff to Gateway when schema drifts
```

## Chained Validation Pattern

```ts
import { test, expect } from '@playwright/test';

test('order → inventory → refund chain', async ({ request }) => {
  // 1. HTTP call
  const createRes = await request.post('/orders', {
    data: { sku: 'WIDGET-1', qty: 2 },
  });
  expect(createRes.status()).toBe(201);
  const order = await createRes.json();

  // 2. State validation via different endpoint
  const fetchRes = await request.get(`/orders/${order.id}`);
  expect(fetchRes.ok()).toBeTruthy();
  expect(await fetchRes.json()).toMatchObject({
    id: order.id,
    status: 'CONFIRMED',
    total: 2 * order.line_items[0].unit_price,
  });

  // 3. Downstream-API side effect
  const invRes = await request.get('/inventory/WIDGET-1');
  const inv = await invRes.json();
  expect(inv.available).toBe(inv.initial - 2);

  // 4. Reverse path
  const refundRes = await request.post(`/orders/${order.id}/refund`);
  expect(refundRes.status()).toBe(200);

  const postRefundInv = await (await request.get('/inventory/WIDGET-1')).json();
  expect(postRefundInv.available).toBe(inv.initial);
});
```

At least one cross-endpoint invariant per test — otherwise the test collapses into a Radar unit.

## Mock vs Real Backend Toggle

```ts
// playwright.config.ts
export default defineConfig({
  use: {
    baseURL: process.env.API_BACKEND === 'mock'
      ? 'http://localhost:4010'  // Prism / MSW / WireMock
      : process.env.API_URL,
  },
  projects: [
    { name: 'api-smoke',     grep: /@critical/, use: { baseURL: process.env.API_URL } }, // real only
    { name: 'api-regression', grep: /@regression/ },                                      // either
  ],
});
```

- **Mock (Prism from OpenAPI / MSW / WireMock)**: fast PR checks, schema-shape validation, no env dependency.
- **Real**: critical-path smoke, staging gates, release candidates.
- Never run `@critical` against mocks — mock drift silently passes broken code.

## Contract-Test Follow-Up

When a journey asserts a specific response shape, promote that shape to a contract:

1. Capture the actual response during a green CI run.
2. Diff against the OpenAPI spec (`schemathesis`, `dredd`, or Spectral).
3. If drift is detected, open a Gateway handoff — do not silently relax the Voyager assertion.

## Anti-Patterns

- Single-endpoint tests dressed up as E2E — that is a Radar unit, route it back.
- Hardcoded IDs from a seeded DB — makes tests order-dependent and parallel-hostile.
- Assertions only on HTTP status — a 200 with a broken body passes. Always validate body shape + state.
- `sleep(N)` between calls — replace with a polling `expect.poll(() => request.get(...))` against the state endpoint.
- Leaving test data behind — cleanup in `afterEach` or use disposable tenants.
- Running security checks here — route to Probe `api`.

## Handoff

- To **Gateway**: schema drift or missing contract.
- To **Radar**: a failure that reproduces at integration level (single service, no HTTP).
- To **Probe**: an endpoint that needs authz / injection / rate-limit validation.
- To **Siege**: the journey works but needs throughput / failure-mode verification.
