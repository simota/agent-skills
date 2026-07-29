# API Versioning Strategies

## Comparison

| Strategy | Pros | Cons | Example |
|----------|------|------|---------|
| URL Path | Simple, visible | URL pollution | `/v1/users` |
| Header | Clean URLs | Hidden version | `Accept: application/vnd.api.v1+json` |
| Query Param | Easy testing | Caching issues | `/users?version=1` |
| Content Negotiation | Standard-based | Client complexity | `Accept: application/json; version=1` |

**Recommendation:** URL Path versioning for simplicity and clarity.

## Deprecation Timeline

1. Announce deprecation (6 months before)
2. Add `Deprecation` header to responses
3. Add `Sunset` header with date
4. Monitor usage of deprecated version
5. Remove after sunset date

## Breaking vs Non-Breaking Changes

| Change | Breaking? |
|--------|-----------|
| Add optional field | No |
| Add new endpoint | No |
| New HTTP methods on existing endpoints | No |
| More permissive validation | No |
| Remove field | Yes |
| Rename field | Yes |
| Change field type | Yes |
| Add required field | Yes |
| Change URL structure | Yes |
| Stricter validation | Yes |
| Change authentication method | Yes |
| Change error response format | Yes |

## Version Migration Strategy

```markdown
## Version Migration Plan: v1 → v2

### Timeline
| Phase | Duration | Action |
|-------|----------|--------|
| Announcement | Week 1 | Notify consumers of v2 release |
| Parallel Operation | Weeks 2-12 | Both v1 and v2 available |
| Deprecation Notice | Week 8 | Add deprecation headers to v1 |
| v1 Sunset | Week 13 | v1 returns 410 Gone |

### Deprecation Headers
```http
Deprecation: true
Sunset: Sat, 01 Mar 2025 00:00:00 GMT
Link: </api/v2/users>; rel="successor-version"
```
```

---

## 2025 Versioning Best Practices

### Strategy Comparison

| Strategy | Best For | Caching | Client Complexity | Example |
|----------|----------|---------|-------------------|---------|
| URL Path (`/v1/`) | Public APIs, stable contracts | Excellent (path-based CDN) | Low | `/api/v2/users` |
| Date-Based (`2024-01-01`) | SaaS products, continuous delivery | Good | Medium | `Stripe-Version: 2024-06-20` |
| Header (`Accept-Version`) | Internal APIs, microservices | Moderate (Vary header needed) | Medium | `Accept-Version: 2` |
| Query Param (`?version=1`) | Testing, backwards compat tooling | Poor (cache busting risk) | Low | `/users?version=1` |
| Content Negotiation | Standards-based, hypermedia APIs | Moderate | High | `Accept: application/vnd.myapi.v2+json` |

**2025 Recommendation:** URL path for public APIs; date-based for SaaS with rolling deployments.

---

## Date-Based Versioning (Stripe Model)

Stripe popularized date-based versioning where each client pins to a specific API date snapshot. As of the 2024-09-30.`acacia` release Stripe shifted to a **monthly cadence with twice-yearly named breaking releases** ([Stripe versioning policy](https://docs.stripe.com/sdks/versioning)). Current GA version as of 2026-05 is `2026-04-22.dahlia`.

**Rules:**
1. Each release date represents a stable API snapshot — clients that specify a date get that behavior forever.
2. New fields and backwards-compatible additions are transparent to all clients.
3. Breaking changes ship in the twice-yearly named release (e.g., `acacia`, `dahlia`); intermediate monthly versions are additive-only. SDKs cut a new minor each month and a new major every named release.
4. Default version (no header) = latest — only safe for internal or test clients.
5. Store the client's pinned version server-side; return `Stripe-Version` in every response for auditability.

```http
# Request with pinned version
GET /v1/charges
Stripe-Version: 2026-04-22.dahlia

# Response confirms active version
HTTP/1.1 200 OK
Stripe-Version: 2026-04-22.dahlia
```

---

## Sunset Header (RFC 8594)

For the full `Sunset` (RFC 8594) / `Deprecation` (RFC 9745) header contract, signaling rules, and timeline standards, see `reference/deprecation-policy.md` — the canonical source for deprecation signaling (`deprecation` recipe owns the SIGNAL/POLICY layer; `versioning` owns the URL/strategy layer).
