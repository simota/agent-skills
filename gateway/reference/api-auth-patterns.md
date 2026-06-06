# API Auth Patterns Reference

Purpose: Choose and design the API authentication contract. Cover OAuth 2.1 (with PKCE), OpenID Connect (OIDC), JWT bearer, mTLS, and API keys. Define scope taxonomy, audience claims, token lifetime, refresh strategy, and IdP integration.

> **2026-05 baseline**: **RFC 9700 / BCP 240** "Best Current Practice for OAuth 2.0 Security" was published **2025-01** ([datatracker](https://datatracker.ietf.org/doc/rfc9700/)) and is the floor — it is now BCP-grade (not just informational). **OAuth 2.1** itself remains an IETF draft (latest `draft-ietf-oauth-v2-1-15` as of 2025; [oauth.net/2.1](https://oauth.net/2.1/)) — it rolls in RFC 9700 + PKCE (RFC 7636) + browser-based apps guidance and removes Implicit + Resource Owner Password Credentials. For new APIs in 2026, design against OAuth 2.1 + RFC 9700 even before the final RFC ships. **Passkeys / WebAuthn L3** (FIDO Alliance, 2024) are the recommended user-facing replacement for password-based factors; FIDO2 = WebAuthn (browser API) + CTAP2 (authenticator protocol). For MCP / agent endpoints, use **OAuth 2.0 Authorization Server Metadata (RFC 8414)** for discovery — OpenAPI 3.2's `oauth2MetadataUrl` plugs straight into this.

## Scope Boundary

- **gateway `auth`**: API auth contract design (this document).
- **Builder (elsewhere)**: Verification middleware implementation.
- **Crypt (elsewhere)**: Key management depth (KMS, rotation, HSM).
- **Sentinel (elsewhere)**: Static security analysis of auth code.
- **Probe (elsewhere)**: Runtime testing of auth flows.
- **Cloak (elsewhere)**: Token-level PII / consent rules.

## Choosing the Right Auth

| Scenario | Choose | Notes |
|----------|--------|-------|
| 1st-party SPA | OAuth 2.1 + PKCE + httpOnly cookie | No client secret in browser |
| 1st-party mobile | OAuth 2.1 + PKCE + system browser | App-Auth pattern |
| 1st-party server-side web | OAuth 2.1 Authorization Code + client secret | Standard confidential client |
| B2B service-to-service | OAuth 2.1 Client Credentials | Optionally JWT bearer with assertion |
| Partner / 3rd-party developer | OAuth 2.1 + scopes per app | Like Stripe / GitHub |
| Internal platform | mTLS or signed JWT | High trust, fixed clients |
| Public read-only | API key + scope | Low value, easy onboarding |
| Federated identity (SSO) | OIDC over OAuth 2.1 | id_token + userinfo |
| Webhook callback signing | HMAC-SHA256 | Not auth per se; provider-side |

OAuth 2.1 (IETF draft `draft-ietf-oauth-v2-1-15`, supersedes 2.0) makes PKCE mandatory and removes implicit flow + password grant. RFC 9700 / BCP 240 (2025-01) already enforces these as Best Current Practice — default to it for new APIs even while OAuth 2.1 is in draft.

## OAuth 2.1 Grants Summary

| Grant | Use case | Token in browser? |
|-------|----------|-------------------|
| Authorization Code + PKCE | SPA, mobile, web | No (sessions/cookies) |
| Client Credentials | Service-to-service | N/A |
| Refresh Token | Token renewal | Yes (rotated) |
| Device Code | TVs, IoT, CLI | Out-of-band |
| Token Exchange (RFC 8693) | Identity propagation | N/A |

Removed in 2.1: Implicit, Resource Owner Password Credentials.

## Token Shapes

### Access token (JWT vs opaque)

| Type | Pros | Cons |
|------|------|------|
| JWT (signed) | Stateless verification at any service | Cannot revoke without revocation list / short TTL |
| Opaque (random) | Server can revoke instantly via lookup | Introspection round-trip per request |
| JWT + cache | Verify signature, cache a short revocation TTL | Hybrid; tune carefully |

JWT default for distributed systems; opaque for high-assurance (banking).

### JWT claims (RFC 7519 + per-API extensions)

```
iss: https://auth.example.com
sub: user-id
aud: api.example.com         # critical: validate
exp: NumericDate
iat, nbf, jti
scope: "read:invoices write:invoices"
azp: client-id              # OIDC: authorized party
tenant_id: tenant-42        # custom
roles: ["admin"]            # custom
```

Validate `aud` always. Audience-confused tokens are a classic vulnerability.

### Token lifetime

| Token | Typical TTL |
|-------|-------------|
| Access token | 5-60 min (15 min default) |
| ID token (OIDC) | 5-60 min |
| Refresh token | 7-90 days, rotated on use |
| API key | indefinite (rotate manually) |
| Service-to-service token | minutes; renewed via client credentials |

Long-lived bearer tokens are a foot-gun. Use refresh + short access tokens.

## Scope Taxonomy

Design scopes per *resource* + *action*:

```
read:invoices
write:invoices
delete:invoices
admin:invoices
```

Or hierarchical:

```
billing.read
billing.write
billing.admin
```

Anti-patterns:
- One mega-scope (`api`) — no granularity.
- Scope per endpoint — too fine, unmanageable.
- Conflating role and scope — scope is *capability*, role is *who*.

## mTLS (mutual TLS)

When client identity comes from certificate, not bearer.

- Internal service mesh (Istio, Linkerd, Consul Connect).
- Bank / fintech partner integrations.
- High-security IoT device fleet.

Cert rotation cadence: 30-90 days; SPIFFE / SPIRE for identity.

## API Key

Simple but inflexible. Best practices:
- Treat as bearer secret (use Authorization header, not URL).
- Per-environment + per-app scoping.
- Hash at rest (don't store plaintext).
- Reveal once at creation; let users rotate.
- Display last 4 chars in UI for identification.
- Optional IP allowlist per key.
- Optional scope per key.

Never use API keys for end-user auth. They're for app-level access only.

## Workflow

```
INVENTORY    →  identify caller types (1st-party / 3rd-party / service / internal)
             →  per-caller security posture

CHOOSE       →  matrix above → grant + token type
             →  token TTL + refresh policy

SCOPES       →  define resource × action taxonomy
             →  document granularity rules

CLAIMS       →  required: iss, sub, aud, exp, iat, scope
             →  custom: tenant_id, roles, ...
             →  audience validation MANDATORY

KEYS         →  signing key strategy (asymmetric: RS256/ES256/EdDSA)
             →  rotation cadence (90d default)
             →  KMS / HSM for production
             →  JWKS endpoint for verification

IDP          →  build (Keycloak, Authentik) vs buy (Auth0, Okta, Cognito)
             →  user provisioning (SCIM 2.0)
             →  social / SAML federation if needed

CLIENT-SIDE  →  SPA: BFF (Backend-for-Frontend) recommended; cookie-based
             →  mobile: AppAuth pattern
             →  CLI: device code flow

REVOCATION   →  refresh token rotation + family revocation on reuse
             →  API key revocation list
             →  session forced-logout

SIGNALS      →  401 vs 403 semantics
             →  WWW-Authenticate header
             →  rate-limit interplay (separate response space)

HANDOFF      →  Builder: middleware
             →  Crypt: key mgmt depth
             →  Sentinel: static analysis
             →  Probe: runtime tests
             →  Vigil: detection (token theft, anomalous auth)
             →  Comply: regulated context (PCI / HIPAA implications)
```

## Output Template

```markdown
## API Auth Design: [API / Surface]

### Caller Inventory
| Caller type | Auth | Token type | TTL | Notes |
|-------------|------|-----------|-----|-------|
| SPA (1st party) | OAuth 2.1 + PKCE | JWT | 15m | BFF cookie |
| Mobile | OAuth 2.1 + PKCE | JWT | 15m | AppAuth |
| Service-to-service | Client Credentials | JWT | 5m | tenant-bound |
| Partner | OAuth 2.1 | JWT | 30m | per-app scopes |

### Token Specification
- **Algorithm**: [RS256 / ES256 / EdDSA]
- **JWKS**: [URL]
- **Required claims**: iss, sub, aud, exp, iat, jti, scope
- **Custom claims**: [tenant_id, roles, ...]
- **Audience**: [string; mandatory validation]

### Scope Taxonomy
| Scope | Capability |
|-------|-----------|
| read:X | ... |
| write:X | ... |
| admin:X | ... |

### Lifetime + Refresh
- Access: [TTL]
- Refresh: [TTL, rotation on use]
- Refresh family revocation on token reuse: yes

### Key Management
- Signing: [KMS / HSM]
- Rotation: [cadence]
- Old-key grace period: [days]

### IdP
- Provider: [Auth0 / Okta / Cognito / Keycloak / Authentik]
- SCIM provisioning: [yes/no]
- Federation: [SAML / Social / OIDC upstream]

### Error Semantics
- 401: missing/invalid token
- 403: token valid but lacks scope
- WWW-Authenticate: Bearer realm="api", error="..."

### Client Patterns
- SPA: BFF + httpOnly cookie
- Mobile: AppAuth
- CLI: device code

### Handoffs
- Builder: middleware impl
- Crypt: key mgmt
- Sentinel: static analysis
- Probe: runtime tests
- Vigil: detection rules
- Comply: regulated mapping
```

## Anti-Patterns

| Anti-pattern | Fix |
|--------------|-----|
| Resource Owner Password Credentials grant | Removed in OAuth 2.1; use Authorization Code |
| Implicit flow | Removed in 2.1; use PKCE |
| API key in URL query | Use Authorization header; URL leaks via logs/referer |
| Long-lived JWT (1+ day) | Short TTL + refresh rotation |
| Skipping `aud` validation | Audience confusion attack |
| One global scope | Granular scopes per resource × action |
| Symmetric HS256 in distributed system | Asymmetric (RS256/ES256/EdDSA) for verification at edge |
| Storing API keys plaintext | Hash + display last 4 |
| Refresh token without rotation | Theft = permanent access |
| OAuth state param missing | CSRF on auth flow |
| PKCE optional for public clients | Mandatory in 2.1 |
| Self-rolled JWT verification | Use library; constant-time signature, claim validation |
| Conflating role and scope | Scope = capability; role = identity attribute |

## Deliverable Contract

When `auth` completes, emit:

- **Caller inventory** with auth + token + TTL.
- **Token spec** (alg, JWKS, required + custom claims).
- **Scope taxonomy** per resource × action.
- **Lifetime + refresh policy** with rotation.
- **Key management** plan.
- **IdP choice** + provisioning + federation.
- **Error semantics** (401 vs 403, WWW-Authenticate).
- **Client patterns** per caller type.
- **Handoffs**: Builder, Crypt, Sentinel, Probe, Vigil, Comply.

## References

- OAuth 2.1 — `draft-ietf-oauth-v2-1-15` (2025) — [datatracker](https://datatracker.ietf.org/doc/draft-ietf-oauth-v2-1/)
- OAuth 2.0 (RFC 6749, RFC 6750)
- PKCE (RFC 7636) — mandatory in OAuth 2.1 + RFC 9700
- OpenID Connect Core 1.0
- JWT (RFC 7519); JWS (RFC 7515); JWE (RFC 7516); JWK (RFC 7517)
- **OAuth 2.0 Security Best Current Practice — RFC 9700 / BCP 240 (2025-01)** — [datatracker](https://datatracker.ietf.org/doc/rfc9700/)
- OAuth 2.0 Authorization Server Metadata (RFC 8414) — discovery for OpenAPI 3.2 `oauth2MetadataUrl`
- Token Exchange (RFC 8693)
- WebAuthn Level 3 + FIDO2 / Passkeys (FIDO Alliance, 2024)
- AppAuth pattern (Mobile OAuth) — OpenID Foundation
- BFF pattern — Phil Calçado, Thoughtworks
- SPIFFE / SPIRE — workload identity
- Auth0 / Okta / Cognito / Keycloak / Authentik documentation
- OWASP API Security Top 10 (2023 — still current; 2026 edition not yet released)
- OWASP Top 10 for Agentic Applications (2026, peer-reviewed release 2025-12)
- IETF OAuth Working Group — current drafts
