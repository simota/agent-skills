# API Design Decision Tree

## Protocol Selection (2026-05)

| Requirement | REST (OpenAPI 3.2) | GraphQL (Sep 2025 spec) | gRPC / ConnectRPC | tRPC |
|-------------|------|---------|------|------|
| Public API | Recommended | Conditional | No (gRPC-Web/Connect for browser) | No (TypeScript-only) |
| Microservices | Acceptable | No | Recommended | No |
| Mobile apps | Yes | Recommended | Yes (gRPC over HTTP/3 in gRPC 1.67+ trims mobile latency 38-42% on 5G/4G) | No |
| Real-time | SSE (OpenAPI 3.2 `itemSchema`) / WebSocket | Subscription (graphql-ws or graphql-sse) | Server / bidi streaming | WebSocket |
| File transfer | Yes (multipart/mixed in OpenAPI 3.2) | No | Yes | No |
| Browser direct call | Yes | Yes | Connect protocol (Buf, CNCF graduated): same Protobuf, HTTP/1.1 or h2, JSON or binary — no gRPC-Web shim needed | Yes (TS only) |
| Internal TypeScript monorepo | Acceptable | Acceptable | Acceptable | Recommended (end-to-end type inference) |

**Connect protocol (ConnectRPC, [connectrpc.com](https://connectrpc.com/))** is the modern alternative to gRPC for browser-reachable Protobuf RPC. It supports all three protocols (gRPC, gRPC-Web, Connect) on a single handler — Bluesky, Dropbox, CrowdStrike, PlanetScale ship it in production. Default to Connect when you want gRPC ergonomics without HTTP/2 trailer requirements or grpc-web's translation proxy.

## Selection Flowchart

```
Q1: Who is the client?
├─ Browser/Mobile → Q2
├─ Internal services (polyglot) → gRPC or ConnectRPC
├─ Internal TS-only mono → tRPC or ConnectRPC-TS
└─ Third party / partner → REST (OpenAPI 3.2)

Q2: Data fetching pattern?
├─ Fixed fields / cacheable → REST + OpenAPI 3.2
├─ Flexible field selection / cross-domain → GraphQL (Federation 2.10+)
└─ Real-time updates → SSE (itemSchema) / WebSocket / GraphQL subscription
```

## GraphQL vs REST Decision Criteria

| GraphQL is better | REST is better |
|-------------------|----------------|
| Fetch multiple resources in one request | Simple CRUD operations |
| Mobile bandwidth is critical | Caching is important (CDN, HTTP semantics) |
| Frontend-driven development | API contract via OpenAPI is important |
| UI changes frequently | Stable API contract |
| Cross-team supergraph (Federation 2.10+) | Single owning team |
| AI agent consumes typed schema (Schema Coordinates stable IDs) | AI agent reads `llms.txt` + OpenAPI 3.2 |
