# GraphQL Schema Design Reference

Purpose: Author a GraphQL SDL that is type-safe, performant under N+1 pressure, and evolvable across federated services. The contract is the schema and its operation limits — not the resolver code.

> **2026-05 baseline**: The **GraphQL September 2025 edition** of the specification ([spec.graphql.org/September2025](https://spec.graphql.org/September2025/), [announcement](https://graphql.org/blog/2025-09-08-september-edition/)) is the first full spec release since October 2021. It standardizes **Schema Coordinates** (stable IDs like `User.email` for diff/codegen/lint tooling), **OneOf input objects** (exactly-one-of input pattern via `@oneOf`), executable-document `description`s, full Unicode grammar, and clarified deprecation + execution semantics. **Apollo Federation 2.10** (2025-02, [docs](https://www.apollographql.com/docs/graphos/schema-design/federated-schemas/reference/versions)) mandates explicit `@link` versioning and is the prerequisite for the `@connect` / `@source` Connectors spec. `@defer` / `@stream` remain opt-in via `experimentalExecuteIncrementally` in graphql-js — they are spec-track but not yet GA in the September 2025 edition.

## Scope Boundary

- **Gateway `graphql`**: the SCHEMA/CONTRACT layer. Decides types, fields, nullability, Connection shape, complexity/depth limits, persisted-query policy, subscription transport, federation boundaries.
- **Builder `api`**: the IMPLEMENTATION layer. Writes resolvers, wires DataLoader, implements persisted-query storage, runs the WebSocket server. Receives the schema from Gateway via `GATEWAY_TO_BUILDER`.
- **Seek**: owns search retrieval architecture. If the schema exposes `search(query: String!): SearchConnection!`, Gateway `graphql` decides the Connection shape and nullability; Seek decides index, ranking, and vector fusion. Cross-link whenever a field returns search results.
- **vs Gateway `rest` / `openapi`**: mutually exclusive at the operation level. A single endpoint is either REST or GraphQL — do not mix in one contract. A product may expose both surfaces for different consumers.

If the question is "what does the schema look like?" → `graphql`. If it is "how do I implement the resolver?" → Builder `api`. If it is "how do I rank results inside `search`?" → Seek.

## Schema-First vs Code-First

| Approach | Pick when | Skip when |
|----------|-----------|-----------|
| Schema-first (SDL authored by hand, codegen for types) | Multiple languages consume the schema; design review is the bottleneck; federation is planned | Single-language team with fast iteration — SDL drifts from code |
| Code-first (types authored in TS/Python, SDL generated) | Single-language team, schema evolves with domain code | Cross-team contract review; SDL is the artifact humans review |

Default: **Schema-first** for public APIs and federated graphs. Code-first for internal monoliths.

## Type Design Principles

- Nullability is load-bearing — every `!` is a promise to never return null. Non-null a field only when the resolver truly cannot fail. Prefer null + error extension over partial schema collapse.
- Enums over free-form strings for bounded sets — enums are introspectable and codegen-friendly.
- `ID` scalar is opaque — do not assume UUID vs integer downstream.
- Input types are distinct from output types. Never reuse an object type as input.
- Use interfaces/unions for polymorphism (`SearchResult = Article | Product | User`). Clients can fragment on each.
- For exactly-one-of input shapes (e.g., `lookupBy: { id, email, phone }` where only one is set), use the **`@oneOf`** input object pattern standardized in the September 2025 spec edition. Pre-2025 codebases emulated this with manual resolver checks — the spec'd form is now enforced at the GraphQL layer.
- Refer to fields by **Schema Coordinates** (`User.email`, `Mutation.updateUser`, `User.email(format:)`) when emitting diffs, lint output, or registry annotations. Coordinates are now spec-stable, so tooling produces deterministic codegen and PR-comment anchors across schema versions.

## N+1 Prevention — DataLoader

The canonical GraphQL performance trap: a list of N parents each resolves a child with one DB query → N+1 queries.

Fix:
- Wrap every cross-boundary fetch in a `DataLoader` (or language equivalent) keyed by the parent's ID.
- DataLoader batches all keys collected within one event-loop tick into a single multi-get.
- DataLoader is **request-scoped** — never share a loader across requests (cache poisoning, stale data, user-data leaks across tenants).

Schema-side signals that Builder must add a loader:
- Any field that resolves from a different data source than its parent.
- Any list field whose items each have a nested object reference.

## Persisted Queries

Allow-list clients to only pre-registered query documents identified by a hash.

Benefits:
- Blocks arbitrary query execution from untrusted clients (compounds with depth/complexity limits).
- Query hash is GET-cacheable at the CDN — reduces origin load dramatically.
- Makes schema evolution visible — you can see exactly which queries are in production use.

Two modes:
- **Automatic Persisted Queries (APQ)** — client sends hash first, server asks for full query on miss, then caches.
- **Static persisted queries** — queries are extracted from client code at build time and registered. Stricter but requires client-build integration.

Recommend static for public APIs, APQ for first-party web clients.

## Query Depth and Complexity Limits

A single malicious query can ask for `user { friends { friends { friends { ... } } } }` and exhaust the server.

Enforce both:
- **Depth limit**: reject queries with selection depth > N (typical: 10).
- **Complexity limit**: assign each field a cost (scalars = 1, list multiplier = `first` or default 10), reject queries whose summed cost > budget.

Complexity is superior to depth alone — depth does not penalize a wide query like `users(first: 1000) { posts(first: 1000) { comments(first: 1000) } }`.

## Schema Stitching vs Federation

| Approach | Pick when | Skip when |
|----------|-----------|-----------|
| Monolithic schema | Single team, single service, no cross-domain graph | Multi-team product |
| Schema stitching (gateway merges independent schemas by name) | Legacy or quick aggregation across two existing GraphQL services | New architecture — federation is strictly superior |
| Apollo Federation v2.10+ (subgraphs declare ownership via `@key`/`@shareable`, explicit `@link` versioning required) | Multi-team, multi-service; each team owns a domain and its types | Single service — overhead without payoff |

Federation lets each subgraph own its types and extend others' types. The gateway composes a single supergraph. Boundary clarity at the `@key` directive. Federation 2.10 (2025-02) is the floor for new graphs in 2026 — every subgraph SDL must declare `@link(url: "https://specs.apollo.dev/federation/v2.x", ...)`. Federation 2.10 is also the prerequisite for the `@connect` / `@source` Connectors spec (REST/AI-tool wrapping inside the graph).

## Relay Spec — Connections, Cursors, Nodes

Relay standardizes list pagination and object identity:

```graphql
type ArticleConnection {
  edges: [ArticleEdge!]!
  pageInfo: PageInfo!
}
type ArticleEdge {
  node: Article!
  cursor: String!
}
type PageInfo {
  hasNextPage: Boolean!
  endCursor: String
}
```

- Cursor-based, not offset-based (same reasoning as REST `rest` recipe).
- Global `Node` interface with opaque `id: ID!` enables `node(id: $id)` refetch pattern.
- Adopt Relay for any list field with > 100 expected items, even if the client is not Relay.

## Subscriptions

- Transport: **graphql-ws** over WebSocket for bi-directional, or **graphql-sse** for one-way streams and simpler infra.
- Scope each subscription tightly — `orderUpdated(orderId: ID!)` not `allOrderUpdates`. Broad subscriptions fan out to every connection and exhaust the server.
- Authenticate at connection init, not per message. Revoke on auth token expiry.
- Hand off the subscription transport and scaling story (sticky sessions or Redis pub/sub) to Builder `api`.

## Anti-Patterns

- `String` fields that encode JSON — defeats the type system.
- `Query.everything: [Everything!]!` — unbounded list with no pagination.
- Circular non-null references that force a 500 on any missing relation.
- Mutations that return `Boolean` — return the affected object so clients can update their cache in one round-trip.
- Sharing a DataLoader across requests.
- Launching federation without `@key` discipline — subgraph ownership collapses into chaos.
- Subscriptions without depth/complexity limits — a subscription runs every resolver on every event.

## Handoff

- **→ Builder `api`**: SDL path, DataLoader plan (which fields batch), persisted-query policy (APQ vs static), depth/complexity limits, subscription transport and auth model.
- **→ Seek**: if the schema has search fields, hand over the Connection shape and field-level filter arguments. Seek designs the retrieval; `graphql` keeps the schema shape.
- **→ `openapi`**: not applicable — GraphQL does not emit OpenAPI. For hybrid surfaces, author two separate contracts.
