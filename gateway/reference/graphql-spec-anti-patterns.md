# GraphQL & OpenAPI Specification Anti-Patterns

> Failure patterns in GraphQL schema design, OpenAPI spec structure, and API spec quality
>
> **2026-05 baseline**: The current reference is the GraphQL **September 2025 spec edition** ([spec.graphql.org/September2025](https://spec.graphql.org/September2025/), the first full spec revision in 4 years since October 2021). It adds Schema Coordinates, `@oneOf` input objects, executable-document descriptions, and full Unicode support. Apollo Federation **2.10** (2025-02) is the current minimum recommended version (requires explicit `@link` versioning, and is a prerequisite for `@connect`/`@source` Connectors). On the OpenAPI side, **3.2.0** (2025-09-23) is the current target, maintaining the JSON Schema Draft 2020-12 dialect.

## 1. The 7 Major GraphQL Schema Design Anti-Patterns

| # | Anti-Pattern | Problem | Symptoms | Countermeasure |
|---|-------------|------|------|------|
| **GQ-01** | **N+1 Query Problem** | Each item in a list triggers an individual child resolver DB call | Query execution time scales with item count, DB load spikes | Resolve field-boundary N+1 with DataLoader (batching + caching) |
| **GQ-02** | **No Depth Limiting** | Circular references allow unbounded-nesting queries | Malicious queries crash the server, DoS vulnerability | Limit nesting depth with `graphql-depth-limit`, query cost analysis |
| **GQ-03** | **Nullable by Default** | Every field can return null by default | Frontend is riddled with null checks, unexpected nulls break the UI | Mark required fields with `!`: `name: String!`; null should only be an explicit design decision |
| **GQ-04** | **No Pagination Default** | List queries can return all records with no limit set | Fetching millions of records crashes both client and server | Set a default limit at schema design time, Connection/Edges pattern recommended |
| **GQ-05** | **Lengthy Mutation Arguments** | A mutation enumerates many individual arguments | Adding arguments breaks the signature, reduces readability | Use an Input Object Type: `input CreateUserInput { name: String!, email: String! }` |
| **GQ-06** | **Insufficient Mutation Response** | A mutation returns only minimal data | Requires an additional query after an update, unnecessary network round trips | Have the mutation response return the changed data in full, for immediate client-side local state updates |
| **GQ-07** | **No Schema Documentation** | Types/fields have no description | GraphiQL/Playground auto-docs are empty, developers have to guess the meaning | Add a description string to every type/field, leverage auto-generated documentation |

---

## 2. GraphQL Performance Pitfalls

```
Performance failures:

  ❌ Over-Fetching at Resolver Level:
    → The resolver fetches more data from the DB than the client requested
    → Countermeasure: optimize field-level data fetching, check requested fields

  ❌ No Caching Strategy:
    → The resolver hits the DB every time, even for frequently accessed data
    → Countermeasure: in-memory/distributed caching, leverage DataLoader's built-in cache

  ❌ Query Complexity Ignorance:
    → No cost calculation for complex nested queries
    → Countermeasure: query cost analysis, complexity limits, timeout settings

  ❌ No Persisted Queries:
    → The full query string is sent every time
    → Countermeasure: use Persisted Queries / APQ (Automatic Persisted Queries) to send only a hash

  ❌ Schema Stitching Without Planning:
    → Combining microservice schemas without planning
    → Compatibility issues, name collisions, performance degradation
    → Countermeasure: planned integration via Federation (e.g. Apollo Federation)
```

---

## 3. OpenAPI Spec Anti-Patterns

| # | Anti-Pattern | Problem | Symptoms | Countermeasure |
|---|-------------|------|------|------|
| **OA-01** | **Post-Hoc Spec Generation** | Auto-generating the OpenAPI spec from code after implementation is complete | The spec is incomplete, examples are missing, design intent is lost | Design-First: spec → mock → review → implement → contract test |
| **OA-02** | **Internal Naming Leak** | Internal abbreviations/business logic names appear as-is in the spec | External developers can't understand `GET /api/txn_proc/{boid}` | Use clean naming for public consumption, separate internal/external APIs |
| **OA-03** | **No Security Scheme Context** | OAuth/API keys are declared but scope and granularity are unclear | Passes audits but access control fails to work in actual operation | Define scopes per endpoint, describe security requirements with context |
| **OA-04** | **Missing Examples** | Request/response examples are undefined | Mock servers return empty responses, developers have to guess API behavior | Provide request/response examples for every endpoint, including edge cases |
| **OA-05** | **Loose Validation** | `required`/`readOnly`/`writeOnly`/`pattern` unused | Any input passes through, errors surface only at runtime | Strictly define validation attributes such as min/max/pattern/enum/required |
| **OA-06** | **Monolithic Spec File** | A single OpenAPI file spans thousands of lines | Hard to review, frequent merge conflicts, hinders cross-team collaboration | Split into components/paths/schemas files, combine via `$ref` |

---

## 4. REST vs. GraphQL vs. gRPC Selection Pitfalls

```
Selection mistake patterns:

  ❌ GraphQL for Simple CRUD:
    → Introducing GraphQL's complexity for simple resource CRUD
    → Overhead of schema management and caching strategy
    → Countermeasure: simple CRUD → REST, complex data-fetching patterns → GraphQL

  ❌ REST for Real-Time:
    → Achieving pseudo-real-time via polling
    → Bandwidth waste, latency, server load
    → Countermeasure: real-time → WebSocket/SSE, bidirectional streaming → gRPC

  ❌ gRPC for Public APIs:
    → Not directly usable from a browser, requires a toolchain
    → Countermeasure: internal microservice-to-microservice → gRPC, public API → REST or GraphQL

  ❌ Mixing Without Gateway:
    → REST + GraphQL + gRPC coexist without a unified entry point
    → Countermeasure: unify the entry point via an API Gateway, with protocol translation
```

---

## 5. Custom Scalar & Enum Design

```
Type design failures:

  ❌ String for Everything:
    → Defining dates, emails, URLs, and monetary amounts all as String type
    → Validation depends on the resolver, no schema-level type safety
    → Countermeasure: define custom scalars (Date, Email, URL, Money)

  ❌ Boolean for Multi-State:
    → Using Boolean for something that may become a 3+ state field in the future
    → Countermeasure: use an Enum: `enum OrderStatus { PENDING, PROCESSING, SHIPPED, DELIVERED }`

  ❌ No Format Specification:
    → OpenAPI defines only `type: string`, with no `format` specified
    → Countermeasure: clarify with `format: date-time`, `format: email`, `format: uri`
```

---

## 6. Collaboration with Gateway

```
Usage within Gateway:
  1. SURVEY phase: screen schema/spec against GQ-01 through GQ-07 / OA-01 through OA-06
  2. PLAN phase: validate the GraphQL/REST/gRPC selection
  3. VERIFY phase: audit OpenAPI spec quality
  4. PRESENT phase: propose schema improvements

Quality gates:
  - No DataLoader used in GraphQL → propose resolving N+1 (prevents GQ-01)
  - No depth limit configured → introduce graphql-depth-limit (prevents GQ-02)
  - OpenAPI examples undefined → propose adding examples (prevents OA-04)
  - Spec generated after implementation → propose migrating to Design-First (prevents OA-01)
  - Validation attributes unused → add required/pattern/enum (prevents OA-05)
  - Single monolithic spec file → propose splitting + `$ref` structuring (prevents OA-06)
  - All fields typed as String → add custom scalars/format (prevents type-design issues)
```

---

## 7. Apollo Federation: v1 vs v2 vs v2.10+

| Feature | Federation v1 | Federation v2 | Federation v2.10+ (2025-02) |
|---------|--------------|--------------|---------------------------|
| Composition | `@apollo/gateway` only | `@apollo/composition` (standalone) | Rewritten composition engine — descriptive errors, composition hints for query planning |
| `@key` directive | Single subgraph owns entity | Multiple subgraphs can extend entity with `@key(resolvable: false)` | Same; required to be stable identifiers |
| `@extends` | Required for entity extension | Not needed — implicit extension | Not needed |
| `@shareable` | Not available | Fields shared across subgraphs must be marked `@shareable` | Same |
| `@override` | Not available | One subgraph can override another's field ownership | Same |
| `@inaccessible` | Not available | Mark fields hidden from supergraph consumers | Same |
| Link import | Not available | `@link` directive for importing external definitions | **MANDATORY** — every subgraph must declare `@link(url: "https://specs.apollo.dev/federation/v2.x")` |
| Connectors | Not available | Not available | **`@connect` / `@source`** — wrap REST endpoints / AI tools as subgraph fields (prerequisite: Federation 2.10) |

### When to Use Federation vs REST

| Criteria | Use GraphQL Federation | Use REST |
|----------|----------------------|---------|
| Data shape | Complex, nested, cross-service entities | Simple, flat resource per endpoint |
| Client variety | Many clients with different field needs | One or few clients with fixed shapes |
| Team structure | Multiple teams owning schema fragments | Single team or simple CRUD service |
| Caching | Willing to invest in query-level caching | HTTP response caching sufficient |
| Real-time | Subscriptions needed across subgraphs | Polling or WebSocket simpler |
| Operations maturity | Can invest in schema governance tooling | Standard HTTP monitoring sufficient |

### Subgraph Design Rules

1. **Single responsibility**: Each subgraph owns one domain (users, orders, catalog) — no cross-domain mutations.
2. **Entity key stability**: `@key` fields must be stable identifiers (avoid mutable fields like `email`).
3. **No circular dependencies**: Subgraph A should not require data from Subgraph B to resolve what Subgraph B also needs from A.
4. **Define entities at their source of truth**: Only the owning subgraph should define the full entity; others use `@key(resolvable: false)` references.
5. **Avoid schema sprawl**: Federation does not eliminate the need for schema review — all subgraph changes go through composition validation.

---

**Source:** [LogRocket: Anti-patterns in GraphQL Schema Design](https://blog.logrocket.com/anti-patterns-graphql-schema-design/) · [Composite Code: Top 10 GraphQL Anti-patterns](https://compositecode.blog/2023/08/02/top-10-graphql-anti-patterns-ime-the-horror/) · [Medium: GraphQL at Scale — 9 Anti-Patterns](https://medium.com/@connect.hashblock/graphql-at-scale-9-anti-patterns-faster-fixes-5146a1db9db8) · [Medium: Stop Shipping Fragile APIs — Advanced OpenAPI Best Practices](https://medium.com/@yasaswinitatikonda1/stop-shipping-fragile-apis-the-advanced-openapi-best-practices-every-engineer-should-know-de1fd311cf91) · [APIMatic: 14 Best Practices for OpenAPI](https://www.apimatic.io/blog/2022/11/14-best-practices-to-write-openapi-for-better-api-consumption) · [DEV.to: 10 OpenAPI Best Practices](https://dev.to/hsmall/10-openapi-best-practices-that-elevate-your-api-game-2hpj)
