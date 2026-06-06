# API Standards Reference

## OpenAPI Specification 3.1.x / 3.2

[Source: https://spec.openapis.org/oas/] — Current stable versions: **3.1.2** (patch, Sep 2025) and **3.2.0** (minor, Sep 2025). 3.1.1 was released Oct 2024. All 3.1.x share the same structure; tooling that supports 3.1.0 works on 3.1.2 without changes. For new projects, target 3.1.2 or 3.2.0. OpenAPI 3.2 adds streaming media types, new Tag Object structure (summary, parent, kind), and expanded HTTP method support. OpenAPI 4.0 ("Moonwalk") is in exploratory design with no planned release date [Source: https://www.openapis.org/blog/2025/02/05/moonwalk-2025-update].

**Deprecation notice:** OpenAPI 2.0 (Swagger 2.0) is obsolete. Assess only against OpenAPI 3.1.x or 3.2 — never 2.0.

### Specification Structure

```yaml
openapi: 3.1.2
info:
  title: API Title
  version: 1.0.0
  description: API Description

servers:
  - url: https://api.example.com/v1
    description: Production

paths:
  /resource:
    get:
      summary: Get resources
      responses:
# ...
```

### OpenAPI Compliance Checklist

#### Required Elements
- [ ] `openapi` version string
- [ ] `info` object with `title` and `version`
- [ ] At least one path OR `webhooks` OR `components`

#### Best Practices (Recommended)
- [ ] All operations have `operationId`
- [ ] All operations have `summary` and/or `description`
- [ ] All parameters documented with `description`
- [ ] All responses have `description`
- [ ] Schemas use appropriate `type` and constraints
- [ ] Examples provided for requests and responses
- [ ] Security schemes defined and applied
- [ ] Consistent naming (camelCase or snake_case)

### Schema Definition Standards

#### Data Types

| Type | Format | Example |
|------|--------|---------|
| string | - | `"hello"` |
| string | date | `"2024-01-15"` |
| string | date-time | `"2024-01-15T10:30:00Z"` |
| string | email | `"user@example.com"` |
| string | uri | `"https://example.com"` |
| string | uuid | `"123e4567-e89b-12d3-a456-426614174000"` |
| string | password | (write-only) |
| integer | int32 | `42` |
| integer | int64 | `9223372036854775807` |
| number | float | `3.14` |
| number | double | `3.141592653589793` |
| boolean | - | `true` |
| array | - | `[1, 2, 3]` |
| object | - | `{"key": "value"}` |

#### Schema Constraints

```yaml
# String constraints
type: string
minLength: 1
maxLength: 100
pattern: '^[a-zA-Z0-9]+$'

# Number constraints
type: integer
minimum: 0
maximum: 100
exclusiveMinimum: true
multipleOf: 5

# Array constraints
type: array
# ...
```

### Response Standards

#### Success Responses

| Status | Usage | Response Body |
|--------|-------|---------------|
| 200 OK | GET success, PUT/PATCH success | Resource or collection |
| 201 Created | POST success | Created resource + Location header |
| 204 No Content | DELETE success, PUT with no response | Empty |

#### Error Responses

| Status | Usage | When |
|--------|-------|------|
| 400 Bad Request | Invalid input | Validation failure, malformed request |
| 401 Unauthorized | Auth required | Missing or invalid credentials |
| 403 Forbidden | Access denied | Authenticated but not authorized |
| 404 Not Found | Resource missing | Resource doesn't exist |
| 409 Conflict | State conflict | Duplicate, version conflict |
| 422 Unprocessable Entity | Semantic error | Business logic violation |
| 429 Too Many Requests | Rate limited | Include Retry-After header |
| 500 Internal Server Error | Server error | Unexpected failure |

#### Standard Error Schema

```yaml
components:
  schemas:
    Error:
      type: object
      required:
        - code
        - message
      properties:
        code:
          type: string
          description: Machine-readable error code
          example: VALIDATION_ERROR
        message:
          type: string
          description: Human-readable message
# ...
```

---

## RFC 9110 - HTTP Semantics (supersedes RFC 7231)

[Source: https://www.rfc-editor.org/rfc/rfc9110] — RFC 9110 was published June 2022 and supersedes RFC 7231, RFC 7232, RFC 7233, RFC 7235. Always cite RFC 9110 for HTTP semantics assessments; RFC 7231 is obsolete.

### HTTP Methods

| Method | Safe | Idempotent | Cacheable | Request Body | Response Body |
|--------|------|------------|-----------|--------------|---------------|
| GET | Yes | Yes | Yes | No | Yes |
| HEAD | Yes | Yes | Yes | No | No |
| POST | No | No | Only if explicit | Yes | Yes |
| PUT | No | Yes | No | Yes | Yes |
| PATCH | No | No | No | Yes | Yes |
| DELETE | No | Yes | No | May have | May have |
| OPTIONS | Yes | Yes | No | No | Yes |

### Method Semantics

#### GET
- Retrieve representation of target resource
- Must not have side effects
- Response can be cached

**Non-Compliant:**
```
GET /api/users/123/delete  # Side effect via GET
```

**Compliant:**
```
DELETE /api/users/123
```

#### POST
- Process enclosed entity according to resource semantics
- Not idempotent (multiple requests may create multiple resources)
- Use for creating subordinate resources

#### PUT
- Replace all current representations of target resource
- Idempotent (multiple identical requests have same effect)
- Complete replacement, not partial update

**Non-Compliant:**
```
PUT /api/users/123
{"name": "John"}  # Missing other fields = deletion
```

**Compliant:**
```
PUT /api/users/123
{"id": "123", "name": "John", "email": "john@example.com", "status": "active"}
```

#### PATCH
- Apply partial modifications
- Not necessarily idempotent
- Use JSON Patch (RFC 6902) or JSON Merge Patch (RFC 7396)

```json
// JSON Merge Patch
PATCH /api/users/123
Content-Type: application/merge-patch+json
{"name": "John Updated"}

// JSON Patch
PATCH /api/users/123
Content-Type: application/json-patch+json
[{"op": "replace", "path": "/name", "value": "John Updated"}]
```

#### DELETE
- Remove target resource
- Idempotent (deleting non-existent resource is success)
- May return 200 (with body) or 204 (no body)

### Status Code Usage

#### 2xx Success
- **200 OK:** Request succeeded, response has content
- **201 Created:** Resource created, include Location header
- **202 Accepted:** Request accepted for processing (async)
- **204 No Content:** Success with no response body

#### 3xx Redirection
- **301 Moved Permanently:** Resource moved, update bookmarks
- **302 Found:** Temporary redirect (often misused)
- **303 See Other:** Redirect to GET another resource
- **304 Not Modified:** Cache validation success
- **307 Temporary Redirect:** Preserve method
- **308 Permanent Redirect:** Preserve method, permanent

#### 4xx Client Error
- **400 Bad Request:** Malformed syntax
- **401 Unauthorized:** Authentication required
- **403 Forbidden:** Authenticated but not authorized
- **404 Not Found:** Resource doesn't exist
- **405 Method Not Allowed:** Method not supported
- **406 Not Acceptable:** Cannot satisfy Accept header
- **409 Conflict:** Request conflicts with current state
- **410 Gone:** Resource permanently gone
- **415 Unsupported Media Type:** Content-Type not supported
- **422 Unprocessable Entity:** Semantic errors (WebDAV, widely adopted)
- **429 Too Many Requests:** Rate limited

#### 5xx Server Error
- **500 Internal Server Error:** Generic server error
- **501 Not Implemented:** Server doesn't support functionality
- **502 Bad Gateway:** Invalid upstream response
- **503 Service Unavailable:** Server overloaded or down
- **504 Gateway Timeout:** Upstream timeout

### Content Negotiation

#### Request Headers
```http
Accept: application/json, application/xml;q=0.9, */*;q=0.1
Accept-Language: ja, en;q=0.8
Accept-Encoding: gzip, deflate, br
```

#### Response Headers
```http
Content-Type: application/json; charset=utf-8
Content-Language: ja
Content-Encoding: gzip
```

---

## RFC 7807 - Problem Details for HTTP APIs

### Standard Error Format

```json
{
  "type": "https://example.com/probs/out-of-credit",
  "title": "You do not have enough credit.",
  "status": 403,
  "detail": "Your current balance is 30, but the cost is 50.",
  "instance": "/account/12345/transactions/abc"
}
```

### Required Members

| Member | Type | Description |
|--------|------|-------------|
| `type` | URI | Reference to problem type definition |
| `title` | string | Short, human-readable summary |

### Optional Members

| Member | Type | Description |
|--------|------|-------------|
| `status` | integer | HTTP status code |
| `detail` | string | Human-readable explanation specific to this occurrence |
| `instance` | URI | URI reference identifying specific occurrence |

### Content-Type

```http
Content-Type: application/problem+json
```

---

## JSON Schema

### Schema Keywords

#### Type Validation
```json
{
  "type": "object",
  "properties": {
    "name": {"type": "string"},
    "age": {"type": "integer"},
    "active": {"type": "boolean"},
    "tags": {"type": "array", "items": {"type": "string"}},
    "metadata": {"type": "object"}
  }
}
```

#### String Validation
```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 100,
  "pattern": "^[a-z]+$",
  "format": "email"
}
```

#### Numeric Validation
```json
{
  "type": "number",
  "minimum": 0,
  "maximum": 100,
  "exclusiveMinimum": true,
  "multipleOf": 0.01
}
```

#### Array Validation
```json
{
  "type": "array",
  "items": {"type": "string"},
  "minItems": 1,
  "maxItems": 10,
  "uniqueItems": true
}
```

#### Object Validation
```json
{
  "type": "object",
  "properties": {...},
  "required": ["id", "name"],
  "additionalProperties": false,
  "minProperties": 1,
  "maxProperties": 10
}
```

#### Composition
```json
{
  "oneOf": [{...}, {...}],
  "anyOf": [{...}, {...}],
  "allOf": [{...}, {...}],
  "not": {...}
}
```

---

## GraphQL Specification

### Schema Definition

```graphql
type Query {
  user(id: ID!): User
  users(filter: UserFilter, first: Int, after: String): UserConnection!
}

type Mutation {
  createUser(input: CreateUserInput!): CreateUserPayload!
  updateUser(id: ID!, input: UpdateUserInput!): UpdateUserPayload!
  deleteUser(id: ID!): DeleteUserPayload!
}

type User {
  id: ID!
  name: String!
  email: String!
// ...
```

### Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Types | PascalCase | `User`, `OrderItem` |
| Fields | camelCase | `createdAt`, `orderItems` |
| Arguments | camelCase | `userId`, `includeDeleted` |
| Enums | SCREAMING_SNAKE_CASE | `PENDING`, `IN_PROGRESS` |
| Input types | PascalCase + Input suffix | `CreateUserInput` |
| Payload types | PascalCase + Payload suffix | `CreateUserPayload` |

### Relay Pagination (Connections)

```graphql
type UserConnection {
  edges: [UserEdge!]!
  pageInfo: PageInfo!
  totalCount: Int!
}

type UserEdge {
  node: User!
  cursor: String!
}

type PageInfo {
  hasNextPage: Boolean!
  hasPreviousPage: Boolean!
  startCursor: String
// ...
```

### Error Handling

```graphql
type CreateUserPayload {
  user: User
  errors: [UserError!]!
}

type UserError {
  field: String
  message: String!
  code: ErrorCode!
}

enum ErrorCode {
  VALIDATION_ERROR
  NOT_FOUND
  UNAUTHORIZED
// ...
```

### Compliance Checklist

- [ ] Use nullable fields by default, non-null (!) when truly required
- [ ] Implement pagination for list queries (Connections)
- [ ] Return structured errors in mutation payloads
- [ ] Use Input types for mutation arguments
- [ ] Version via schema evolution, not URL versioning
- [ ] Implement DataLoader for N+1 prevention
- [ ] Set query depth and complexity limits
- [ ] Disable introspection in production (optional)

---

## REST API Design Standards

### URL Design Rules

| Rule | Good | Bad |
|------|------|-----|
| Use nouns, not verbs | `/users` | `/getUsers` |
| Use plural for collections | `/users` | `/user` |
| Use lowercase | `/user-profiles` | `/UserProfiles` |
| Use hyphens for readability | `/user-profiles` | `/user_profiles` |
| Hierarchical structure | `/users/123/orders` | `/get-orders-for-user?id=123` |
| Query params for filtering | `/users?status=active` | `/users/active` |

### Resource Naming

```
# Collection
GET /api/v1/users

# Single resource
GET /api/v1/users/{userId}

# Sub-collection
GET /api/v1/users/{userId}/orders

# Sub-resource
GET /api/v1/users/{userId}/orders/{orderId}

# Actions (only when CRUD doesn't fit)
POST /api/v1/users/{userId}/activate
POST /api/v1/orders/{orderId}/cancel
```

### Versioning Standards

| Strategy | Example | Pros | Cons |
|----------|---------|------|------|
| URL path | `/api/v1/users` | Clear, cacheable | URL changes |
| Query param | `/api/users?version=1` | Same URL | Less discoverable |
| Header | `Accept: application/vnd.api.v1+json` | Clean URLs | Hidden |

**Recommendation:** URL path versioning for simplicity.

### Pagination Standards

#### Offset-Based
```
GET /api/v1/users?limit=10&offset=20

{
  "data": [...],
  "meta": {
    "total": 100,
    "limit": 10,
    "offset": 20
  }
}
```

#### Cursor-Based (Recommended for large datasets)
```
GET /api/v1/users?limit=10&cursor=abc123

{
  "data": [...],
  "meta": {
    "nextCursor": "def456",
    "hasMore": true
  }
}
```

### HATEOAS (Hypermedia)

```json
{
  "id": "123",
  "name": "John Doe",
  "_links": {
    "self": {"href": "/api/v1/users/123"},
    "orders": {"href": "/api/v1/users/123/orders"},
    "update": {"href": "/api/v1/users/123", "method": "PUT"},
    "delete": {"href": "/api/v1/users/123", "method": "DELETE"}
  }
}
```

---

## API Security Standards

### Authentication

| Method | Use Case | Standard |
|--------|----------|----------|
| API Key | Service-to-service | Header: `X-API-Key` |
| Bearer Token | User authentication | Header: `Authorization: Bearer <token>` |
| OAuth 2.0 | Third-party access | RFC 6749 |
| OIDC | Identity + OAuth | OpenID Connect Core |

### Security Headers

```http
# CORS
Access-Control-Allow-Origin: https://example.com
Access-Control-Allow-Methods: GET, POST, PUT, DELETE
Access-Control-Allow-Headers: Authorization, Content-Type
Access-Control-Max-Age: 86400

# Security
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
Content-Security-Policy: default-src 'self'
```

### Rate Limiting Headers

```http
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 99
X-RateLimit-Reset: 1640995200
Retry-After: 60
```

---

## Compliance Validation Tools

### OpenAPI Linting

```bash
# Spectral (recommended)
npx @stoplight/spectral-cli lint openapi.yaml

# OpenAPI Generator validation
npx @openapitools/openapi-generator-cli validate -i openapi.yaml

# Redocly CLI
npx @redocly/cli lint openapi.yaml
```

### Common Spectral Rules

```yaml
# .spectral.yaml
extends: ["spectral:oas", "spectral:asyncapi"]

rules:
  operation-operationId: error
  operation-description: warn
  oas3-api-servers: error
  info-contact: warn
  info-description: error
```

### JSON Schema Validation

```bash
# ajv-cli
npx ajv validate -s schema.json -d data.json

# json-schema-to-typescript
npx json-schema-to-typescript schema.json > types.ts
```
