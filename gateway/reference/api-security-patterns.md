# API Security Patterns

> **Scope**: This file covers authentication, authorization, CORS, input validation, and security review patterns. For rate-limit algorithms, headers (`RateLimit-*` / legacy `X-RateLimit-*`), 429 + `Retry-After` semantics, and distributed enforcement, see `rate-limit-patterns.md` (the canonical source).

## Authentication Methods

| Method | Use Case | Complexity |
|--------|----------|-----------|
| API Key | Server-to-server | Low |
| JWT Bearer | User auth | Medium |
| OAuth 2.0 | Third-party access | High |

## CORS Configuration

```typescript
const corsOptions = {
  origin: ['https://app.example.com'],
  methods: ['GET', 'POST', 'PUT', 'DELETE'],
  allowedHeaders: ['Content-Type', 'Authorization'],
  credentials: true,
  maxAge: 86400,
};
```

## Input Validation Checklist
- [ ] Validate Content-Type header
- [ ] Validate request body against schema
- [ ] Sanitize string inputs
- [ ] Limit request body size
- [ ] Validate path and query parameters

---

## Security Review Checklist

### Authentication
- [ ] Endpoints require authentication (unless public)
- [ ] Token validation documented
- [ ] Token expiration handled

### Authorization
- [ ] Resource ownership verified
- [ ] Role-based access defined
- [ ] Cross-tenant access prevented

### Input Validation
- [ ] All inputs validated
- [ ] Size limits defined
- [ ] Type coercion avoided
- [ ] SQL/NoSQL injection prevented
- [ ] Path traversal prevented

### Output Security
- [ ] Sensitive data excluded from responses
- [ ] Error messages don't leak internals
- [ ] CORS configured correctly
- [ ] Security headers present

### Rate Limiting
- [ ] Limits defined per endpoint
- [ ] Limits documented
- [ ] 429 response includes Retry-After

---

## API Security 2025

### OAuth 2.1 Consolidation

OAuth 2.1 consolidates OAuth 2.0 + best practices from Security BCP (RFC 9700) into a single spec.

| Change | OAuth 2.0 | OAuth 2.1 |
|--------|-----------|-----------|
| Implicit Flow | Allowed | Removed (use Auth Code + PKCE) |
| Resource Owner Password Credentials | Allowed | Removed |
| PKCE | Optional for public clients | Mandatory for all clients |
| Refresh Token rotation | Optional | Mandatory for public clients |
| `redirect_uri` exact match | Best practice | Required |

### DPoP (Demonstrating Proof of Possession)

DPoP (RFC 9449) binds access tokens to a client's key pair, preventing token replay attacks.

- Client generates an asymmetric key pair (ES256 / RS256) per session.
- Each request includes a `DPoP` header with a signed JWT proof containing the request method, URI, and timestamp.
- Server verifies proof and rejects tokens used without the matching key.

```http
Authorization: DPoP <access_token>
DPoP: eyJhbGciOiJFUzI1NiIsInR5cCI6ImRwb3Arand...
```

### API Key Best Practices

| Practice | Description |
|----------|-------------|
| Format | Prefix + random bytes: `sk_live_` + 32 bytes base62 |
| Storage | Hash (SHA-256) at rest; return plaintext only once at creation |
| Scope | Bind to specific permissions, not all-or-nothing |
| Rotation | Support multiple valid keys simultaneously for zero-downtime rotation |
| Transmission | Header only (`Authorization: Bearer` or custom `X-API-Key`); never in URL |
| Audit | Log key ID (not value) on every request for traceability |

### Rate Limiting Headers

See `rate-limit-patterns.md` for the IETF `RateLimit` / `RateLimit-Policy` draft header spec, legacy `X-RateLimit-*` headers, and 429 + `Retry-After` body conventions.

---

## API Gateway Patterns

### BFF (Backend for Frontend)

Each frontend type (web, mobile, third-party) gets a dedicated API gateway facade.

| BFF Type | Consumers | Optimizations |
|----------|-----------|---------------|
| Web BFF | Browser SPA | Larger payloads, session cookies, SSR data shapes |
| Mobile BFF | iOS/Android | Compressed payloads, offline-friendly schemas, push notification triggers |
| Partner BFF | External developers | Strict versioning, public OpenAPI spec, rate limiting |

**Rules:**
1. BFF owns aggregation logic — never expose raw microservice contracts to clients.
2. One BFF per client type (not per team) — avoid BFF proliferation.
3. BFF does not contain business logic — delegate to domain services.
4. Co-locate BFF code with the frontend team that owns it.

### Circuit Breaker

Prevents cascading failures when downstream services are degraded.

**State transitions:**
```
CLOSED → (failure threshold exceeded) → OPEN → (timeout elapsed) → HALF-OPEN → (probe success) → CLOSED
                                                                              → (probe failure) → OPEN
```

| Parameter | Typical Value | Description |
|-----------|---------------|-------------|
| Failure threshold | 50% over 10s | % of failures to trip to OPEN |
| Probe timeout | 30s | Time in OPEN before attempting HALF-OPEN |
| Probe count | 3 requests | Successful probes required to close |
| Slow call threshold | 2s | Latency that counts as failure |

### Retry Strategy

Exponential backoff with jitter prevents thundering herd after outages.

| Attempt | Base delay | With jitter (±25%) | Max delay |
|---------|-----------|---------------------|-----------|
| 1 | 100ms | 75–125ms | — |
| 2 | 200ms | 150–250ms | — |
| 3 | 400ms | 300–500ms | — |
| 4 | 800ms | 600–1000ms | — |
| 5 | 1600ms | 1200–2000ms | 30s cap |

**Rules:**
- Only retry on idempotent methods (GET, PUT, DELETE) or when `Idempotency-Key` is used.
- Never retry on 4xx errors except `429 Too Many Requests` (honor `Retry-After`).
- Include `Idempotency-Key` header on POST retries to prevent duplicate resource creation.

```http
POST /v1/payments
Idempotency-Key: 550e8400-e29b-41d4-a716-446655440000
Content-Type: application/json
```
