# Integration Testing Reference

Purpose: Design backend-service integration tests that exercise real component-to-component boundaries — service ↔ database, ↔ cache, ↔ message queue, ↔ downstream HTTP — without crossing into full user journeys. Testcontainers is the default for stateful dependencies; WireMock / MSW stubs everything at the HTTP boundary.

## Scope Boundary

- **Radar `integration`**: backend component-to-component tests. Service ↔ Postgres, ↔ Redis, ↔ Kafka, ↔ another HTTP service via stub. Playwright API mode is acceptable for backend HTTP assertions.
- **Radar `unit`**: single function / class in isolation. No I/O.
- **Radar `edge`**: adds cases to an existing integration or unit suite.
- **Voyager (E2E)**: browser-driven, user-to-system flows, multi-page navigation. Anything involving a real browser or a full user journey belongs to Voyager, NOT here.

Rule of thumb: if the test asks "does my HTTP handler correctly write to Postgres and emit to Kafka?", it is `integration`. If it asks "can a user check out?", it is Voyager.

## Stack Selection

| Stack | Primary tooling |
|-------|-----------------|
| TS / JS backend | Vitest + Testcontainers-node, MSW (HTTP boundary), `pg` / `ioredis` clients directly, supertest for HTTP |
| Python | pytest + testcontainers-python, respx or VCR for HTTP, `httpx.AsyncClient` for FastAPI |
| Go | `testing` + testcontainers-go, `httptest.Server` or WireMock for downstream |
| Java / Kotlin | JUnit 5 + Testcontainers-java, WireMock, REST Assured |
| Rust | `cargo test` + testcontainers-rs, `wiremock-rs`, `reqwest::Client` |

## Workflow

```
SCAN    →  identify boundary under test (DB, cache, queue, HTTP)
        →  check existing suite: unit-level leak? full E2E overreach?
        →  confirm Testcontainers is already in use OR ask first

LOCK    →  pick ONE boundary per test file
        →  choose DB fixture strategy (see below)
        →  pin container image tags (no `latest`)

PING    →  write tests that hit the real dependency via Testcontainers
        →  stub only what is outside the hexagon (downstream HTTP)
        →  keep per-test runtime < 1s; suite < 5min target

VERIFY  →  run full suite, assert cleanup (no dangling containers)
        →  measure flake rate over 10 runs; > 2% → diagnose before shipping
```

## DB Fixture Strategy

Pick exactly one per suite; do not mix without cause.

| Strategy | When to use | Cost | Trap |
|----------|-------------|------|------|
| Transaction rollback | Simple CRUD, no triggers, single connection | Fastest (~ms per test) | Breaks when code-under-test opens its own transaction |
| TRUNCATE between tests | Triggers / multi-connection code / complex FKs | Medium (~10-50ms) | Must respect FK order; disable/re-enable constraints |
| Per-test DB | Schema migrations under test, destructive ops | Slowest (~1-5s) | Pair with Testcontainers `withReuse(true)` at the container level, not the schema |
| Seed-and-assert | Read-only queries | Fast | Poisoning: a failing test leaves garbage for the next — prefer rollback |

Default for a fresh suite: **transaction rollback**. Escalate only when it fails.

## HTTP Boundary Stubbing

- **WireMock** (JVM, also WireMock-Standalone for any stack): declarative stub mappings, excellent for contract fixtures, supports record-and-playback against a real upstream.
- **MSW** (Node/browser): reuse the same handler set for dev, unit, and integration — single source of truth. Use `msw/node` in integration, `setupServer(...handlers)`.
- **respx / wiremock-rs / httptest.Server**: language-native equivalents.

Never let integration tests hit the real internet. Assert the stub was called with the exact expected payload, not just "called once".

## Contract-at-Boundary

Integration tests prove: *given a real DB and a stubbed downstream, the component behaves correctly under real I/O*. They do NOT prove the stub matches the real downstream. Pair with:

- `Siege` contract testing (Pact / Specmatic) to verify stub fidelity against the provider.
- Periodic smoke tests in a staging environment.

## Playwright API Mode

Playwright's `request` context can hit a real backend over HTTP for integration assertions (auth flow verification, API response schema). Acceptable here when:
- The test does not launch a browser.
- The scope is a single service boundary (not a full user flow).
Otherwise route to Voyager.

## Anti-Patterns

- Using Testcontainers for tests that could pass as pure unit tests — you've widened the blast radius and slowed CI.
- Reusing one Postgres container across a parallel test suite without schema-per-worker isolation — order-dependent failures.
- `docker-compose up` in CI instead of Testcontainers — hard to clean up, can't parallelize.
- Asserting on internal DB rows when an API response would do — coupling tests to the schema.
- Stubbing the database ("mock Postgres") — you've lost the point of integration tests.
- Letting containers leak between test runs — always `withReuse(false)` or explicit cleanup in CI.

## Handoff

- If the test actually requires a browser → `Voyager`.
- If container startup is the CI bottleneck → `Gear` (for shared test-container layer, CI caching).
- If the stubbed downstream drifts from reality → `Siege` (contract testing).
- If boundaries reveal schema design issues → `Schema`.
