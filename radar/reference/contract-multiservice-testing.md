# Contract & Multi-Service Testing

Purpose: Use this when Radar must verify service boundaries, schema compatibility, or real dependency interactions without escalating into full user-journey E2E testing.

Contents:

- Agent boundary
- REST and Pact
- gRPC and `buf`
- GraphQL contracts
- Event-driven schemas
- Testcontainers and stubs
- Multi-service decision rules

## Agent Boundary

| Scope | Owner |
|-------|-------|
| Unit-level service contracts | `Radar` |
| Service integration with real dependencies | `Radar` |
| Full stack or browser-wide end-to-end validation | `Voyager` |

## REST API Contract Testing (Pact)

Use Pact when a consumer and provider must evolve independently.

Core steps:

1. Define consumer expectations.
2. Verify the provider against the pact file.
3. Publish or compare contracts in CI if multiple teams are involved.

## gRPC Contract Testing

### Must-Keep Commands

```bash
buf lint
buf breaking --against '.git#branch=main'
buf generate
```

### Compatibility Matrix

| Check | Tool | When |
|-------|------|------|
| Wire compatibility | `buf breaking` | Every PR |
| Linting | `buf lint` | Every PR |
| Code generation | `buf generate` | On proto change |
| Mock generation | `nice-grpc` / `grpcmock` | Test setup |

## GraphQL Contract Testing

Use schema-first validation when queries, mutations, or federation boundaries are shared.

### Must-Keep Commands

```bash
npm install -D @graphql-inspector/cli
npx graphql-inspector diff schema-main.graphql schema-pr.graphql
npx graphql-inspector validate './src/**/*.graphql' schema.graphql
```

## Event-Driven Contract Testing

Use AsyncAPI plus schema validation when the boundary is a message rather than a request-response API.

Recommended stack:

- AsyncAPI document for the channel contract
- `Ajv` for schema validation
- Kafka integration tests only when broker behavior matters

## Testcontainers Deep Patterns

### Reuse Strategy

| Strategy | Use case | Tradeoff |
|----------|----------|----------|
| Per-test | Maximum isolation | Slow |
| Per-suite | Reasonable default | State leak risk |
| Per-run | Maximum speed | Cleanup discipline required |
| Reusable | Local development only | Manual cleanup risk |

Use LocalStack when AWS behavior matters but a real AWS account would add cost or instability.

## Multi-Service Integration Patterns

| Pattern | Tool | Use when |
|---------|------|----------|
| Service stub | WireMock / MSW | One boundary should stay fake |
| Real service dependency | Testcontainers | DB, broker, cache, or AWS-emulator semantics matter |
| Saga test | Orchestrated integration test | Compensation and sequence logic matter |

## Decision Rule

| Boundary | Preferred approach |
|----------|--------------------|
| REST | Pact or OpenAPI diff |
| gRPC | `buf breaking` plus targeted mocks |
| GraphQL | Schema diff plus operation validation |
| Event bus | AsyncAPI plus payload validation |
| Real dependency behavior | Testcontainers |
| Full multi-service flow | Hand off to `Voyager` if it becomes an end-to-end user journey |
