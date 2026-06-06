# REST API Design Reference

Purpose: Author a REST contract that is predictable, cache-friendly, and evolvable. The contract is HTTP-idiom focused — resource shape, URI design, status-code taxonomy, conditional requests, pagination, and error format. The contract typically becomes an OpenAPI 3.1/3.2 spec downstream.

> **2026-05 baseline**: OpenAPI 3.2.0 shipped 2025-09-23 ([OAI announcement](https://www.openapis.org/blog/2025/09/23/announcing-openapi-v3-2)) and adds the **HTTP `QUERY` method** as a first-class operation. The QUERY method itself was approved as a Proposed Standard by the IESG on 2025-11-20 ([draft-ietf-httpbis-safe-method-w-body-14](https://datatracker.ietf.org/doc/draft-ietf-httpbis-safe-method-w-body/)) — RFC publication pending in 2026. For new REST contracts, prefer `QUERY /v1/search` (idempotent, body-bearing, cacheable) over `POST /v1/search`. RFC 9457 (Problem Details) was published **2023-07** and obsoletes RFC 7807 — adopt the new `type`/`title`/`status`/`detail`/`instance` shape and the multi-error extension on every new endpoint.

## Scope Boundary

- **Gateway `rest`**: the SPEC/CONTRACT layer. Decides resources, URIs, methods, status codes, pagination style, ETag strategy, RFC 9457 error shape.
- **Gateway `openapi`**: the spec-format layer. Translates `rest` decisions into YAML with schemas, examples, security.
- **Builder `api`**: the IMPLEMENTATION layer. Writes the handler, serializes the resource, computes the ETag, paginates against the DB. Receives the contract from Gateway via `GATEWAY_TO_BUILDER`.
- **Seek**: owns search retrieval (inverted index, ranking, vector search). If a REST endpoint exposes search (`GET /v1/articles?q=...`), `rest` owns URI/status/pagination shape; Seek owns the query semantics and ranking behavior.

If the question is "what should the URL, status, and body look like?" → `rest`. If it is "how do I implement this handler?" → Builder `api`. If it is "how do I rank results?" → Seek.

## Richardson Maturity Model

| Level | What | When to stop |
|-------|------|--------------|
| 0 | Single URI, POST only (RPC over HTTP) | Never acceptable for a public API |
| 1 | Resources (URIs per entity) | Internal-only with tight client coupling |
| 2 | Resources + correct HTTP verbs + status codes | **Target for 95% of APIs** |
| 3 | + HATEOAS (hypermedia links) | Only when clients are browsers or agents that benefit from discovery (e.g. LLM agents, admin UIs) |

Default target: **Level 2**. Escalate to Level 3 only when runtime discoverability pays off.

## Resource Modeling

- Nouns, plural, lowercase-kebab: `/v1/payment-intents`, not `/v1/getPaymentIntent` or `/v1/paymentIntent`.
- Collection + item pairing: `GET /v1/orders` (list), `GET /v1/orders/{id}` (item).
- Nest only when the child cannot exist without the parent: `/v1/orders/{id}/line-items`. Do NOT nest more than 2 levels — flatten with filter query params instead (`/v1/line-items?orderId=...`).
- Actions that do not fit CRUD become a sub-resource POST: `POST /v1/orders/{id}/cancel` (not `POST /v1/cancel-order`).

## HTTP Method Selection (RFC 9110)

| Method | Safe | Idempotent | Use for |
|--------|------|------------|---------|
| GET | yes | yes | Read a resource or collection |
| HEAD | yes | yes | Read headers only (existence / ETag probe) |
| QUERY | yes | yes | Complex/large read whose criteria exceed URL length limits — body is the query, response is the result. IESG-approved 2025-11-20 (Proposed Standard pending RFC); OpenAPI 3.2 models it natively |
| PUT | no | yes | Full replace of a known-URI resource |
| PATCH | no | no (by default) | Partial update — require `Idempotency-Key` header |
| POST | no | no | Create, or action that does not map to PUT/PATCH |
| DELETE | no | yes | Remove a resource |

Never use POST for reads. Never use GET for state-changing operations (CSRF risk, leaks into logs/caches). When a search/filter payload outgrows `?q=...` (typical limit ~8 KB across proxies), reach for `QUERY` instead of `POST /search` — caches and observability tooling can now treat it as safe+idempotent.

## Status Code Taxonomy

- **2xx success** — `200 OK` (read/update with body), `201 Created` (with `Location` header to the new resource), `202 Accepted` (async queued), `204 No Content` (successful delete or update with no body).
- **3xx redirect** — `301` permanent URI change, `304 Not Modified` (conditional GET with matching ETag), `307/308` preserve method on redirect.
- **4xx client error** — `400` malformed request, `401` missing/invalid auth, `403` authenticated but forbidden (BFLA), `404` resource missing or hidden (BOLA mask), `409` conflict (version mismatch, duplicate), `410` permanently gone, `412 Precondition Failed` (If-Match/If-Unmodified-Since failed), `422` semantic validation error, `429` rate limited.
- **5xx server error** — `500` unexpected, `502/503/504` dependency failure — never leak stack traces.

Map each endpoint to its full status set in the spec. Reviewers should be able to see every status the client must handle.

## Conditional Requests (ETag / If-None-Match / If-Match)

- On every cacheable GET, return a strong or weak `ETag` header.
- Clients send `If-None-Match: "<etag>"` on re-fetch — server returns `304 Not Modified` with empty body if unchanged.
- On PUT/PATCH/DELETE, require `If-Match: "<etag>"` for optimistic concurrency. Mismatch → `412 Precondition Failed`. Prevents lost-update races without a separate version field.
- ETag derivation: hash of the serialized resource, or a monotonic `updatedAt` + `id`. Document the derivation in the spec.

## Pagination

| Style | When | Why |
|-------|------|-----|
| Cursor (opaque token) | **Default** for any collection expected to grow | Stable under concurrent inserts, O(1) lookup, no deep-page perf cliff |
| Offset / limit | Only for small, bounded admin lists | Skips/duplicates under concurrent writes, O(offset) DB cost |
| Page number | Never for new APIs | Same failure modes as offset plus human-editable URLs encourage scraping |

Cursor response shape:

```json
{
  "data": [ ... ],
  "pagination": {
    "nextCursor": "eyJpZCI6Li4ufQ==",
    "hasMore": true
  }
}
```

Cursor is opaque (base64 of `{id, sortKey}`). Never expose raw DB offsets. Max `limit` default 100, hard ceiling 1000.

## Error Format — RFC 9457 Problem Details

RFC 9457 (published 2023-07, [datatracker](https://datatracker.ietf.org/doc/html/rfc9457)) obsoletes RFC 7807. `Content-Type: application/problem+json`.

```json
{
  "type": "https://api.example.com/problems/insufficient-funds",
  "title": "Insufficient funds",
  "status": 402,
  "detail": "Wallet balance 12.50 USD is below required 25.00 USD.",
  "instance": "/v1/payments/pay_01HXYZ",
  "walletId": "wal_42"
}
```

- `type` is a stable URI that documents the error class (not a random string).
- Use the multiple-problem extension when returning multiple validation errors in one response — clients can surface every field-level error at once instead of playing whack-a-mole.

## HATEOAS — When Useful

Skip for typed SDK consumers. Add links when:
- The API is consumed by LLM agents that benefit from runtime discovery.
- State transitions are complex (e.g. `cancel` is only valid in some states — return a `cancel` link only when it is).
- Admin UIs that should not hard-code URI templates.

Format: `application/hal+json` or JSON:API `links` — pick one and keep it consistent.

## Anti-Patterns

- Verbs in URIs (`/v1/getOrders`, `/v1/create-user`). Use resources + methods.
- 200 OK with `{ "error": "..." }` body. Use the correct 4xx/5xx and RFC 9457.
- Mixing camelCase and snake_case across endpoints in the same API.
- Exposing DB primary keys as sequential integers — leaks volume, enables enumeration.
- Page-number pagination on unbounded collections.
- Missing `Location` on 201 Created.
- Returning stack traces in 5xx responses.

## Handoff

- **→ `openapi`**: produce the YAML spec from the `rest` decisions. Include `ETag`/`If-Match` headers, cursor pagination schema, RFC 9457 error component, and the full status set per operation.
- **→ Builder `api`**: attach the spec path, ETag derivation rule, cursor encoding, and RFC 9457 `type` URI catalog. Builder implements the handler.
- **→ Seek**: if the endpoint is a search endpoint, hand the URI/status/pagination shape to Seek so it can design query semantics and ranking against that shape.
