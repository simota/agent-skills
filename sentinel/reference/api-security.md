# API Security & OWASP API Top 10

Purpose: Use this reference when auditing HTTP APIs, GraphQL services, OAuth flows, or API-specific authorization and SSRF risks.

---

## 1. OWASP API Security Top 10 (2023)

The 2023 edition remains the current version as of March 2026.

| Rank | Category | Severity | Key Signal |
|------|----------|----------|------------|
| `API1` | Broken Object Level Authorization (BOLA) | Critical | 40% of API attacks; ownership checks missing |
| `API2` | Broken Authentication | Critical | Weak credential handling |
| `API3` | Broken Object Property Level Authorization (BOPLA) | High | Mass assignment, field-level access missing |
| `API4` | Unrestricted Resource Consumption | High | No rate limiting on expensive queries |
| `API5` | Broken Function Level Authorization (BFLA) | Critical | Admin routes without authz middleware |
| `API6` | Unrestricted Access to Sensitive Business Flows | High | Abuse of legitimate workflows |
| `API7` | Server-Side Request Forgery (SSRF) | High | Internal network access via API |
| `API8` | Security Misconfiguration | Medium | CORS, debug mode, default credentials |
| `API9` | Improper Inventory Management | Medium | Shadow APIs, undocumented endpoints |
| `API10` | Unsafe API Consumption | Medium | Trusting third-party API responses |

2025 statistics: 99% of organizations experienced API security issues in the past year. 17% of all disclosed vulnerabilities (11,053 of 67,058) are API-related. 43% of CISA KEV additions are API-related. 97% of API vulnerabilities are exploitable with a single request.

---

## 2. Key Vulnerabilities

### API1: BOLA

Detection signals: object IDs in routes (`/orders/:id`), no server-side ownership check, predictable IDs.

```typescript
// Anti-pattern: no ownership check
app.get('/api/orders/:id', async (req, res) => {
  const order = await Order.findById(req.params.id);
  res.json(order);
});

// Pattern: ownership enforced
app.get('/api/orders/:id', async (req, res) => {
  const order = await Order.findOne({ _id: req.params.id, userId: req.user.id });
  if (!order) return res.status(404).json({ error: 'Not found' });
  res.json(order);
});
```

Mitigations: enforce ownership on every access, prefer UUIDs, use centralized authz or row-level security.

### API3: BOPLA (Mass Assignment)

Detection signals: `req.body` written directly to DB, missing field-level access, responses expose unnecessary fields.

```typescript
// Anti-pattern
await User.findByIdAndUpdate(req.params.id, req.body);

// Pattern: allowlist only
const { name, email, avatar } = req.body;
await User.findByIdAndUpdate(req.params.id, { name, email, avatar });
```

### API5: BFLA

Detection signals: admin routes without authz middleware, inconsistent method-level authz, `/admin` paths rely on UI hiding.

Mitigations: centralized policy-as-code, RBAC/ABAC on handlers and methods, deny by default.

---

## 3. API Security Checklist

### Authentication & Authorization

- [ ] Require authentication on every non-public endpoint
- [ ] Enforce ownership checks for object access (BOLA)
- [ ] Enforce function-level authorization (BFLA)
- [ ] Verify JWT signature and expiry
- [ ] Scope API keys
- [ ] Prefer OAuth Authorization Code + PKCE
- [ ] Keep session management strict

### Input & Output

- [ ] Validate request bodies and params (Zod / JSON Schema)
- [ ] Block mass assignment with allowlists
- [ ] Return DTOs, not raw models
- [ ] Paginate and rate limit expensive queries
- [ ] Constrain file type and size on uploads
- [ ] Validate path parameters (UUID, identifier format)

### Infrastructure & Configuration

- [ ] Forbid `CORS: *` for privileged APIs
- [ ] Force HTTPS
- [ ] Version APIs and retire stale endpoints
- [ ] Keep internal errors out of responses
- [ ] Disable public docs for sensitive internal endpoints

---

## 4. SSRF Prevention

```typescript
import { URL } from 'url';
import ipaddr from 'ipaddr.js';

function isAllowedUrl(urlString: string): boolean {
  const url = new URL(urlString);
  if (!['http:', 'https:'].includes(url.protocol)) return false;
  const addr = ipaddr.parse(url.hostname);
  if (addr.range() !== 'unicast') return false;
  const allowedDomains = ['api.example.com', 'cdn.example.com'];
  return allowedDomains.includes(url.hostname);
}
```

---

## 5. GraphQL Security

| Risk | Mitigation |
|------|-----------|
| Introspection exposure | Disable in production (`introspection: process.env.NODE_ENV !== 'production'`) |
| Depth/complexity attacks | `depthLimit(5)`, complexity analysis |
| Batch/alias abuse | Limit batch size, per-query rate limiting |
| BOLA at resolver level | Object-level authz in each resolver |
| CSRF | Accept only `POST` + `Content-Type: application/json` |

```typescript
import depthLimit from 'graphql-depth-limit';

const server = new ApolloServer({
  typeDefs, resolvers,
  validationRules: [depthLimit(5)],
  introspection: process.env.NODE_ENV !== 'production',
});
```

---

## 6. OAuth 2.1 / RFC 9700

OAuth 2.1 remains in draft (draft-ietf-oauth-v2-1-15), but RFC 9700 (OAuth 2.0 Security Best Current Practice, January 2025) codifies the key requirements:

| Requirement | Status |
|-------------|--------|
| Authorization Code + PKCE | **Mandatory** for public clients |
| Implicit Grant | **Deprecated** — detect and remove `response_type=token` |
| Resource Owner Password Credentials | **Deprecated** |
| Refresh token rotation | **Required** |
| Redirect URI exact matching | **Required** |

Sentinel checks:
- [ ] `code_verifier` / `code_challenge` present
- [ ] No `response_type=token` (Implicit Grant)
- [ ] Refresh-token rotation implemented
- [ ] Redirect URIs are exact-match validated

MCP adoption: Anthropic's Model Context Protocol uses OAuth 2.1 as its authorization foundation.

---

## 7. AI API Security (Emerging)

AI-related API threats grew 400% in 2025. MCP vulnerabilities increased 270% in Q2-Q3 2025.

Key risks:
- Prompt injection via API inputs
- Excessive agency (LLM with overprivileged tool calls)
- Unbounded consumption (Denial of Wallet attacks)
- MCP tool poisoning through API endpoints

**Source:** [OWASP API Security Top 10 2023](https://owasp.org/API-Security/editions/2023/en/0x11-t10/) · [Wallarm 2026 API ThreatStats](https://www.wallarm.com/reports/2026-wallarm-api-threatstats-report) · [RFC 9700](https://datatracker.ietf.org/doc/rfc9700/) · [Cloudflare BOLA Detection GA](https://developers.cloudflare.com/changelog/post/2025-11-12-bola-attack-detection/) · [OWASP GraphQL Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/GraphQL_Cheat_Sheet.html) · [Traceable 2025 State of API Security](https://www.traceable.ai/2025-state-of-api-security)
