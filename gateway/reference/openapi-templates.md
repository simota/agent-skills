# OpenAPI Templates

> **2026-05 baseline — OpenAPI 3.2.0** shipped on 2025-09-23 ([OAI announcement](https://www.openapis.org/blog/2025/09/23/announcing-openapi-v3-2), [spec](https://spec.openapis.org/oas/v3.2.0.html)). The JSON Schema dialect is now anchored at `https://spec.openapis.org/oas/3.2/dialect/2025-09-17` (still JSON Schema Draft 2020-12 underneath). 3.2 is **strictly backward-compatible with 3.0 and 3.1** — existing specs keep validating. For new APIs in 2026, default to 3.2 to unlock the streaming + QUERY + OAuth metadata features described below.

| 3.2 capability | What it unlocks |
|----------------|-----------------|
| `itemSchema` on `text/event-stream`, `application/jsonl`, `application/json-seq`, `multipart/mixed` | First-class streaming contracts (SSE / JSON Lines / multipart feeds) without prose disclaimers |
| `query` operation + `additionalOperations` | Native HTTP `QUERY` method (IESG-approved 2025-11-20) plus a defined slot for non-standard methods |
| `querystring` | Whole query string as a Schema Object — clean validation when arbitrary query keys are not enumerable |
| Hierarchical Tags (`summary`, `parent`, `kind`) | Real taxonomy; tooling can filter sections deterministically |
| OAuth 2.0 Device Code + `oauth2MetadataUrl` | Smart-TV / CLI / kiosk flows + automatic discovery of OAuth 2.0 AS metadata (RFC 8414) |
| Improved `multipart/form-data` per-part schema | Mixed file + JSON upload contracts without ad hoc encoding rules |

## Minimal OpenAPI 3.0 Template

```yaml
openapi: '3.0.3'
info:
  title: API Name
  version: '1.0.0'
  description: API description
servers:
  - url: https://api.example.com/v1
paths:
  /resources:
    get:
      summary: List resources
      parameters:
        - $ref: '#/components/parameters/PageParam'
        - $ref: '#/components/parameters/LimitParam'
      responses:
# ...
```

## Error Response (RFC 9457 Problem Details — obsoletes RFC 7807, published 2023-07)

```yaml
ErrorResponse:
  type: object
  properties:
    type: { type: string, format: uri }
    title: { type: string }
    status: { type: integer }
    detail: { type: string }
    instance: { type: string, format: uri }
```

---

## Full OpenAPI 3.1 Structure

```yaml
openapi: 3.1.0
info:
  title: [API Name]
  description: |
    [API description with key features]
  version: 1.0.0
  contact:
    name: API Support
    email: api-support@example.com
  license:
    name: MIT
    url: https://opensource.org/licenses/MIT

servers:
  - url: https://api.example.com/v1
# ...
```

## Endpoint Definition Template

```yaml
paths:
  /users:
    get:
      tags:
        - Users
      summary: List all users
      description: |
        Retrieve a paginated list of users.
        Supports filtering by status and sorting.
      operationId: listUsers
      parameters:
        - $ref: '#/components/parameters/limitParam'
        - $ref: '#/components/parameters/offsetParam'
        - name: status
          in: query
# ...
```

## Schema Definition Template

```yaml
components:
  schemas:
    User:
      type: object
      required:
        - id
        - name
        - email
        - status
        - createdAt
      properties:
        id:
          type: string
          description: Unique user identifier
          example: "usr_123abc"
# ...
```

## Common Components Template

```yaml
components:
  parameters:
    limitParam:
      name: limit
      in: query
      description: Maximum number of items to return
      schema:
        type: integer
        minimum: 1
        maximum: 100
        default: 10

    offsetParam:
      name: offset
      in: query
# ...
```

---

## OpenAPI 3.1+ Breaking Changes from 3.0

OpenAPI 3.1 aligns fully with JSON Schema 2020-12. The following changes are breaking or behaviorally different:

| Topic | OpenAPI 3.0 | OpenAPI 3.1 |
|-------|-------------|-------------|
| `nullable` | `nullable: true` (vendor extension) | Use `type: ["string", "null"]` or `oneOf` with `{type: null}` |
| `exclusiveMinimum` / `exclusiveMaximum` | Boolean flag alongside `minimum`/`maximum` | Numeric value: `exclusiveMinimum: 5` replaces `minimum: 5, exclusiveMinimum: true` |
| Webhooks | Not supported natively | Top-level `webhooks` object (parallel to `paths`) |
| `$ref` siblings | Ignored (siblings were silently discarded) | Allowed and merged — `$ref` with `description` override works |
| `const` | Not supported | Supported: `const: "active"` instead of `enum: ["active"]` |
| `if` / `then` / `else` | Not supported | Full conditional validation supported |
| `prefixItems` | Not supported (`items` only) | `prefixItems` for tuple validation; `items` becomes boolean or schema for additional |

### Migration Checklist: 3.0 → 3.1

- [ ] Replace all `nullable: true` with `type: ["T", "null"]`
- [ ] Convert boolean `exclusiveMinimum`/`exclusiveMaximum` to numeric form
- [ ] Move webhook definitions to top-level `webhooks` block
- [ ] Audit `$ref` siblings — they now take effect (may change validation behavior)
- [ ] Replace single-value `enum` with `const` where intent is a constant
- [ ] Update tooling (validators, code generators) to JSON Schema 2020-12 compatible versions
- [ ] Change `openapi: 3.0.x` → `openapi: 3.1.0` in info block

---

## JSON Schema 2020-12 Features in OpenAPI 3.1

OpenAPI 3.1 adopts JSON Schema 2020-12 as its schema dialect. Key new capabilities:

| Feature | Description | Example |
|---------|-------------|---------|
| `$dynamicRef` / `$dynamicAnchor` | Recursive schemas with late-binding anchors (replaces `$recursiveRef`) | `$dynamicRef: "#items"` for tree structures |
| `prefixItems` | Per-index validation for tuple arrays | `prefixItems: [{type: string}, {type: integer}]` |
| `$vocabulary` | Declare which JSON Schema vocabularies a metaschema uses | Used in custom metaschemas for strict validation |
| `contentMediaType` / `contentEncoding` | Annotate encoded string content | `contentMediaType: "application/json"`, `contentEncoding: "base64"` |
| `unevaluatedItems` / `unevaluatedProperties` | Stricter additional items/properties control | Catches items not covered by `prefixItems` |
| Multiple `type` as array | `type: ["string", "null"]` natively | Replaces `nullable: true` from 3.0 |
