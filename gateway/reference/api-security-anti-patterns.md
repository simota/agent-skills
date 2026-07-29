# API Security Anti-Patterns

> Failure patterns in authentication/authorization, rate limiting, CORS, data exposure, and the OWASP API Security Top 10
>
> **2026-05 baseline**: **OWASP API Security Top 10 2023** is still the latest edition (no 2025/2026 revision has been released). The newly published **OWASP Top 10 for Agentic Applications 2026** (published 2025-12, [genai.owasp.org](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/)) covers risks on the consuming side of agent/LLM APIs, with ASI01 Agent Goal Hijacking at #1. **RFC 9700 / BCP 240** (published 2025-01) formalized as the Best Current Practice for OAuth 2.0 security — mandatory PKCE, deprecation of the Implicit flow, and exact `redirect_uri` matching are now BCP-grade requirements.

## 1. The 7 Major API Security Anti-Patterns

| # | Anti-Pattern | Problem | Symptoms | Countermeasure |
|---|-------------|------|------|------|
| **AS-01** | **API Key Only Auth** | Using an API key as the sole authentication mechanism | Key leakage grants full access; rotation is difficult | Combine with OAuth 2.0 + mTLS, enforce strict expiry/rotation, IP restrictions/device fingerprinting |
| **AS-02** | **Broken Object Level Authorization (BOLA)** | Manipulating object IDs grants access to other users' data | #1 on the OWASP API Top 10; BOLA accounts for 40% of all API attacks | Authorization checks on every DB operation, unguessable GUIDs, object-level authorization testing |
| **AS-03** | **Wildcard CORS** | `Access-Control-Allow-Origin: *` allows all origins | Authenticated requests accepted from any domain | Allowlist trusted domains, restrict methods/headers, control credentialed requests |
| **AS-04** | **No Rate Limiting** | No request-count limits, vulnerable to DoS/brute force | Sudden traffic spikes take down the whole service | Request quotas, per-IP limits, exponential backoff, abnormal-traffic alerting |
| **AS-05** | **Excessive Data Exposure** | Responses include unnecessary internal data/sensitive info | DB structure, internal logs, and personal data leak into responses | Return only the minimum necessary data, schema validation, data masking, response auditing |
| **AS-06** | **Inconsistent Auth Standards** | Different authentication methods per team/service | Ad-hoc workarounds, emerging security gaps | Unified cross-service authentication/authorization standard, defined minimum security requirements |
| **AS-07** | **Poor Logging and Monitoring** | Auth attempts and anomalous access are not logged | Untraceable after an incident, no post-hoc analysis possible | Log auth attempts/excessive requests/anomalous patterns, integrate with an observability system |

---

## 2. OWASP API Security Top 10 (2023)

| Rank | Risk | Overview | Detection Pattern |
|------|--------|------|-------------|
| **API1** | Broken Object Level Authorization | Manipulating ID parameters grants access to others' data | Tampering the id in `GET /api/users/{id}` retrieves data |
| **API2** | Broken Authentication | Flaws in the authentication flow | Tokens never expire, weak password policy |
| **API3** | Broken Object Property Level Authorization | Insufficient authorization at the object property level | Mass assignment, returning unnecessary properties |
| **API4** | Unrestricted Resource Consumption | No limit on resource consumption | Unlimited page size, no rate limiting |
| **API5** | Broken Function Level Authorization | Insufficient authorization at the function level | Direct calls to admin APIs, privilege escalation via method changes |
| **API6** | Unrestricted Access to Sensitive Business Flows | Unrestricted access to sensitive business flows | Automated ticket hoarding, mass account creation |
| **API7** | Server-Side Request Forgery (SSRF) | Server-side request forgery | URL input parameters used to access internal services |
| **API8** | Security Misconfiguration | Security configuration mistakes | TLS not configured, debug mode enabled, verbose errors |
| **API9** | Improper Inventory Management | Poor API asset management | Old versions left running, Shadow APIs, undocumented endpoints |
| **API10** | Unsafe Consumption of APIs | Unsafe consumption of APIs | Third-party API responses not validated, redirects followed blindly |

---

## 3. Authentication/Authorization Pitfalls

```
Authentication design failures:

  ❌ Bearer Token Without Safeguards:
    → No protection against token leakage, no audience validation, weak session revocation
    → Countermeasure: short expiry, refresh token rotation, strict audience/issuer validation

  ❌ Implicit Flow in Production:
    → Using the OAuth 2.0 Implicit Flow in production
    → Tokens exposed in URL fragments, CSRF vulnerability
    → Countermeasure: use Authorization Code Flow + PKCE (even for SPAs)

  ❌ No Scope Granularity:
    → Only two scopes, `read` / `write`, cover all API access
    → Violates least privilege, grants excessive permissions
    → Countermeasure: fine-grained scopes designed per resource and per operation

  ❌ Missing Token Revocation:
    → Tokens remain valid after a user account is suspended
    → Former employees or compromised accounts retain ongoing access
    → Countermeasure: token blacklisting, short expiry + refresh token rotation

  ❌ Encryption Weakness:
    → Using HTTP, outdated TLS versions, weak cipher algorithms
    → Man-in-the-middle attacks, data interception
    → Countermeasure: enforce TLS 1.2+, AES-256, regular crypto audits
```

---

## 4. Defense-in-Depth Checklist

```
Defense layers:
  Layer 1 - Gateway: authentication, schema validation, rate limiting, CORS
  Layer 2 - Application: authorization, input validation, business logic verification
  Layer 3 - Data: output filtering, data masking, encryption
  Layer 4 - Network: network segmentation, WAF, DDoS protection
  Layer 5 - Monitoring: logging, anomaly detection, incident response

Key principles:
  - Do not rely on a single defense layer (any layer can be breached)
  - Authentication ≠ authorization (authorization checks are still required after authentication)
  - Validate input on the server side, not just the client side
  - Do not leak internal details in error responses
  - Regular CVE scanning of dependencies
```

---

## 5. Collaboration with Gateway

```
Usage within Gateway:
  1. SURVEY phase: security screening against AS-01 through AS-07
  2. PLAN phase: cross-check against the OWASP API Top 10
  3. VERIFY phase: confirm authentication/authorization/CORS configuration
  4. PRESENT phase: security improvement report

Quality gates:
  - API-key-only auth → propose OAuth 2.0 + PKCE (prevents AS-01)
  - Direct ID reference with no authorization check → detect BOLA, propose fix (prevents AS-02)
  - CORS `*` setting → propose trusted-domain allowlist (prevents AS-03)
  - Rate limiting not configured → propose 429 + Retry-After implementation (prevents AS-04)
  - Unnecessary fields in responses → design minimal data return (prevents AS-05)
  - Old API versions left running → deprecation + removal plan (prevents OWASP API9)
  - securitySchemes undefined in OpenAPI → add security definitions (prevents misconfiguration)
```

**Source:** [Nordic APIs: 9 Signs You're Doing API Security Wrong](https://nordicapis.com/9-signs-youre-doing-api-security-wrong/) · [Levo.ai: REST API Security Best Practices 2026](https://www.levo.ai/resources/blogs/rest-api-security-best-practices) · [OWASP: API Security Top 10 2023](https://owasp.org/API-Security/editions/2023/en/0xa1-broken-object-level-authorization/) · [CyCognito: API Security 2026 Guide](https://www.cycognito.com/learn/api-security/) · [Calmops: API Security Beyond JWT](https://calmops.com/programming/rust/api-security-beyond-jwt-oauth2-rate-limiting-cors/) · [Wiz: OWASP API Security Top 10](https://www.wiz.io/academy/api-security/owasp-api-security)
