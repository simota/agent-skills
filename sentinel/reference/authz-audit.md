# Authorization Audit Reference

Purpose: Static review of access-control enforcement — RBAC/ABAC correctness, IDOR, BOLA/BFLA, horizontal and vertical privilege escalation. Maps to OWASP A01:2025 Broken Access Control (still the #1 category by incidence rate) and CWE-285, CWE-639, CWE-863.

## Scope Boundary

- **Sentinel `authz`**: static audit of access-control code — is the check present, correct, and applied at every protected resource path?
- **Probe (elsewhere)**: runtime exploit verification — actually fetching another tenant's record, escalating role via parameter tampering, replaying a privileged request as a low-privilege user.
- **`authn` (sibling)**: who the caller is. `authz` presumes identity is already established and asks "is this caller allowed to do this to this object?"

Rule of thumb: `authn` = identity assertion. `authz` = decision + enforcement. `Probe` = exploit confirmation.

## Workflow

```
SCAN       → enumerate protected resources: REST routes, GraphQL resolvers,
             RPC handlers, background jobs, admin consoles, file uploads
           → map roles / permissions / tenant scoping
           → list object-access points (anything that takes an ID from
             request and reads/writes a resource)

PRIORITIZE → CRITICAL: missing authz check entirely; admin action reachable
             by unauth or any-role caller
           → HIGH: IDOR / BOLA (object belongs to user A, reachable by
             user B), horizontal tenant leak via ORM query missing
             tenant_id filter, BFLA (function-level restriction absent)
           → MEDIUM: role check present but uses string compare instead
             of permission enum, client-side-only check
           → LOW: informational leaks (enumerable IDs without data
             exposure)

FILTER     → framework guarantees: trust only when the framework actually
             injects authz (e.g. Rails Pundit/CanCan explicit policy hit,
             tRPC `protectedProcedure` with role middleware); ignore
             comment-only "admin-only" claims

SECURE     → add permission check at the handler boundary
           → replace "check role string" with "check permission on object"
           → add tenant_id / owner_id predicate to query (ABAC)
           → centralize decision: one policy module, tested in isolation

VERIFY     → re-read diff; confirm the check fires before the side effect
           → unit-test the denial path (403, not silent skip)

PRESENT    → severity + confidence + OWASP A01:2025 + CWE + file:line
           → cross-link: Probe for runtime confirmation, Builder if
             fix > 50 lines or requires policy refactor
```

## High-Signal Patterns

| Area | Bad | Good |
|------|-----|------|
| IDOR | `db.order.find({ id: req.params.id })` | `db.order.find({ id: req.params.id, userId: req.user.id })` |
| BOLA | GraphQL resolver returns object if found | Resolver calls `can(user, 'read', object)` before return |
| BFLA | Admin route behind only UI hiding | Admin route asserts `user.permissions.includes('admin:write')` |
| Vertical | Role compared as string `user.role === 'admin'` | Permission enum: `hasPermission(user, P.USERS_DELETE)` |
| Horizontal | Shared-index query by id only | Scope with tenant_id in every query predicate |
| Mass-assign | `Object.assign(user, req.body)` | Allowlist of editable fields per role |
| Deny-by-default | `if (user.role === 'banned') reject; else allow` | `if (!hasPermission(...)) reject; else allow` |

## Anti-Patterns (fail the audit)

- Authorization logic only in the frontend (route guard, conditional render) — backend must re-check.
- "Admin" detected by email domain, IP, feature flag, or `isAdmin` column without audit trail.
- Using sequential integer IDs without scope filter (the canonical IDOR setup).
- JWT payload carries `role` claim that is trusted without re-checking against current DB state (stale role escalation after demotion).
- Policy scattered across handlers ("if-role-admin" repeated 40 times) — one drift away from a bypass.
- GraphQL field-level authz missing on nested relations (object itself is authz'd, but `object.owner.email` isn't).
- AI-generated code: correct handler in isolation, but router entry never wires the auth middleware (a dominant failure mode per Veracode Spring 2026). Always verify the router-to-middleware wiring, not just the handler.

## Handoff

| Target | When | Carry |
|--------|------|-------|
| `Probe` | High-confidence IDOR/BOLA where runtime PoC confirms severity | Endpoint, expected 403 vs observed, sample IDs |
| `Builder` | Fix requires centralized policy module or > 50 line refactor | Fix spec, policy table, migration plan |
| `Schema` | Missing `tenant_id` / `owner_id` columns at the storage layer | Table list, proposed column + index |
| `Radar` | Regression coverage missing for denial paths | Failing 403/404 test cases per role |
| `Canon` | Finding pattern is broad enough to map as an A01:2025 compliance gap | Findings inventory for mapping |

## Output Template

```
Finding: [short title]
Severity: CRITICAL | HIGH | MEDIUM | LOW
Confidence: HIGH | MEDIUM | LOW
OWASP: A01:2025 – Broken Access Control
CWE: [285 | 639 | 863 | ...]
File:Line: path/to/file.ts:NN
Evidence: [3-6 line code quote showing the missing/weak check]
Impact: [horizontal / vertical escalation, tenant leak, etc.]
Remediation: [concrete diff: add predicate, swap role→permission, etc.]
Verification: [denial-path test, or runtime probe plan]
Cross-link: [Probe / Builder / Schema if applicable]
```
