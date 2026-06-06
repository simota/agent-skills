# API DAST Reference

Purpose: Dynamically attack a running REST, GraphQL, or WebSocket API to confirm OWASP API Security Top 10 2023 flaws with reproducible evidence. Static review (source code, OpenAPI spec lint) is out of scope — cross-link to Sentinel and Gateway for those layers.

> **Currency note (2026-05)**:
> - **OWASP API Top 10 2023** is still the active list — no 2026 update yet (`owasp.org/API-Security/`). Threat-stat refresh from Wallarm *2026 API ThreatStats Report* (2026-02-17): **43% of 2025 CISA KEV additions were API-related (106 / 245)**, **97% exploitable in a single request**, **52% of disclosed API breaches were broken-auth**, and **36% of AI vulnerabilities overlap with API vulnerabilities**.
> - **Burp AI** (PortSwigger, announced 2025-03-31): AI-generated login-sequence handling, automated issue validation with AI-generated PoCs, AI insights in Repeater. Burp Scanner natively parses OpenAPI, SOAP WSDL, Postman Collection, and GraphQL definitions.
> - **Akto** (open-source, MIT, `github.com/akto-api-security/akto`): 1,000+ pre-built tests including BOLA / Broken Auth / SSRF / mass assignment; integrates with Burp, AWS, Postman, GCP traffic sources for low-FP discovery. Useful as a complement to Burp Autorize for CI-driven BOLA sweeps.
> - **MCP-specific attack surface (2025-2026)**: Wallarm tracked **315 MCP-related vulnerabilities** in 2025 with 270% Q2→Q3 growth — when the API exposes an MCP server, test for tool-name shadowing, tool-description injection, and unauthenticated `tools/list` enumeration.

## Scope Boundary

- **Probe `api`**: runtime attacks against a deployed API. Confirms exploitability, produces request/response evidence, CVSS v4.0 scores, and remediation SLA.
- **Sentinel**: static source/config audit — hardcoded secrets, unsafe ORM usage, missing auth decorators. Probe `api` validates Sentinel findings at runtime.
- **Gateway**: API design — OpenAPI spec, versioning, breaking-change detection. Probe `api` attacks the deployed implementation to confirm the spec actually enforces what it claims.
- **Breach**: full red-team engagement chaining API flaws into business impact. Probe `api` is the DAST slice inside that engagement.

If the question is "does the spec say X?" → Gateway. "Does the code say X?" → Sentinel. "Does the running API actually enforce X under attack?" → `api`.

**AUTHORIZATION**: Written scope authorization is mandatory before any active testing. Passive inspection (schema download, public docs) only, unless the target, environment, and attack classes are explicitly named in a signed scope document. Production active testing requires separate written approval. Unauthorized API testing is illegal regardless of intent.

## OWASP API Top 10 2023 Coverage

| API# | Risk | Primary dynamic check |
|------|------|-----------------------|
| API1 | BOLA (Broken Object-Level Auth) | Swap object IDs across authenticated identities; ~40% of API attacks (Wallarm Q2 2025) |
| API2 | Broken Authentication | JWT alg=none, weak secret, expired-token accept, refresh-token abuse |
| API3 | Broken Object Property-Level Auth / Excessive Data Exposure | Compare API response to documented DTO; diff for hidden fields |
| API4 | Unrestricted Resource Consumption | Rate limit, payload size, nested depth, compression bombs |
| API5 | BFLA (Broken Function-Level Auth) | Call admin endpoints as standard user; method override (`X-HTTP-Method-Override`) |
| API6 | Mass Assignment | POST unexpected fields (`isAdmin`, `role`, `verified`) and check persistence |
| API7 | SSRF | Submit internal URLs (`169.254.169.254`, `localhost`, `file://`) to URL parameters |
| API8 | Security Misconfiguration | Default creds, verbose errors, CORS wildcard, missing headers |
| API9 | Improper Inventory | Shadow / zombie endpoints, `/v1` alongside `/v2`, staging leaked to prod |
| API10 | Unsafe Consumption of APIs | Server-to-server trust without validation |

## Tooling

| Tool | Role | Notes |
|------|------|-------|
| `schemathesis` | Property-based fuzzing from OpenAPI / GraphQL schema | Strong for API3/API4/API6; generates counterexamples |
| `restler-fuzzer` (MS) | Stateful REST fuzzing, dependency inference | Best-in-class for sequence-dependent bugs |
| `graphql-cop` | GraphQL audit (introspection, field suggestions, batching) | Non-intrusive; run first on GraphQL |
| `clairvoyance` | GraphQL schema recovery when introspection is off | Field-name brute force — coordinate with scope |
| `ws-harness` / ZAP WebSocket add-on | WebSocket frame fuzzing, replay | Watch for state poisoning in pub/sub |
| ZAP (authenticated) | Session-aware passive + active scan | Use Zest scripts for multi-step login; v2.16.0 (ZAP by Checkmarx) is current |
| Burp Suite Pro + Burp AI | BOLA/BFLA via dual-session diffing; AI login recording + auto-validation | Autorize remains the standard BOLA verifier; Burp AI adds AI-generated PoC for triage |
| Akto (OSS) | API discovery + 1,000+ tests for OWASP API Top 10 / HackerOne Top 10 | Low-FP via traffic-pattern learning; useful for CI sweeps |
| Nuclei API templates | Known-CVE checks, default-creds, exposed admin panels | Pin `>= 3.8.0` (CVE-2024-43405, GHSA-29rg-wmcw-hpf4, GHSA-jm34-66cf-qpvr) |
| Garak (NVIDIA) | LLM-backed endpoint scanning (prompt injection, jailbreaks, data leakage) | v0.14.0 (2026-02) — 37+ probe modules |
| PyRIT (Microsoft) | Multi-turn / multi-modal LLM red teaming (crescendo, TAP) | Integrates with Azure AI Foundry; pairs with Burp for hybrid API + LLM tests |

## Workflow

```
PLAN      →  confirm written scope, target list, environments, excluded endpoints
          →  obtain auth artifacts: 2+ identities at different privilege tiers
          →  acquire OpenAPI / GraphQL schema; if unavailable, negotiate discovery budget
          →  declare attack classes in-scope (BOLA? mass assignment? SSRF?)

SCAN      →  passive: schema analysis, introspection (GraphQL), header review
          →  stateful fuzz: restler / schemathesis with 2 identities
          →  BOLA sweep: Autorize or scripted dual-session diff on every object-ID path
          →  BFLA sweep: call role-restricted endpoints with low-privilege token
          →  mass assignment: inject out-of-schema fields (`isAdmin`, `role`, `owner_id`)
          →  GraphQL: introspection exposure, query depth > 10, alias batching, field suggestions
          →  WebSocket: origin check, auth at upgrade, message-level authz, replay

VALIDATE  →  reproduce each finding with minimal curl / HTTPie payload
          →  label Confirmed vs Unconfirmed; FP rate target < 30%
          →  CVSS v4.0 per finding; fall back to v3.1 if tooling limits
          →  cross-check against Sentinel static findings (if provided) for correlation

REPORT    →  per-finding: repro, evidence, CVSS, SLA, remediation
          →  handoff: Builder (fix), Gateway (spec tightening), Sentinel (static rule)
```

## BOLA Testing Pattern

Traditional DAST cannot dynamically substitute credentials — you must configure the tool for two identities.

```
Identity A (user_a, owns object_id=101)
Identity B (user_b, owns object_id=202)

For every endpoint matching /resource/{id}:
  1. Call as A against A's object → expect 2xx (baseline)
  2. Call as A against B's object → expect 403/404
  3. Call as B against A's object → expect 403/404
  4. Unauthenticated call → expect 401

Any 2xx in steps 2-4 = Confirmed BOLA.
```

Burp Autorize automates this. ZAP requires Zest scripts or the API Access Control add-on.

## GraphQL-Specific Checks

- Introspection on in production → API8 / information disclosure.
- Query depth / alias / batch limit: send `{ a:user{friends{friends{...}}} }` nested ≥ 10 and aliased 100x — if no limit, API4.
- Field-level authz: `graphql-cop` + manual per-field probe with low-privilege token.
- Batching abuse: `[{query:...},{query:...}]` x 1000 to bypass rate limits measured per-request.
- Mutations without CSRF / origin checks.

## Anti-Patterns

- Running unauthenticated scan only — misses API1, API3, API5 entirely.
- Using one identity for "auth testing" — cannot detect BOLA.
- Accepting "200 OK with empty array" as authz enforcement — often it's silent failure.
- Trusting OpenAPI spec as ground truth — the whole point of `api` is the implementation drifted from the spec.
- Fuzzing production without isolation — rate-limit the fuzzer (`-rl 30` for Nuclei on prod-adjacent).
- Skipping WebSocket auth review — upgrade handshake often trusted blindly post-connect.

## Handoff

- **→ Builder**: confirmed finding + minimal repro + remediation pattern + SLA.
- **→ Gateway**: when flaw is spec-level (missing `security:`, no rate-limit extension, overpermissive CORS) — spec needs tightening.
- **→ Sentinel**: confirmed runtime flaw with probable source location — refine static rules.
- **→ Triage**: any CVSS ≥ 9.0 (auth bypass, mass assignment on admin role, SSRF to cloud metadata).
- **→ Radar**: confirmed pattern → regression test.
- **→ Vigil**: exploit signature → Sigma/YARA detection rule.
