# Authentication Audit Reference

Purpose: Static review of authentication surfaces — session lifecycle, JWT handling, OAuth/OIDC flows, MFA enforcement, and password storage. Maps to OWASP A07:2025 Identification and Authentication Failures and CWE-287, CWE-384, CWE-521, CWE-798.

## Scope Boundary

- **Sentinel `authn`**: static audit of auth code — does the implementation correctly USE primitives, enforce flows, and fail safely?
- **Crypt (elsewhere)**: cryptographic algorithm and key-design ownership — how a JWT should be signed, which KDF fits, how keys rotate. `authn` consumes Crypt's decisions.
- **Probe (elsewhere)**: runtime exploitability — credential stuffing demos, live session-hijack, brute-force rate-limit bypass, token-replay PoCs.

Rule of thumb: if the finding is "the code path is missing / wrong" → `authn`. If it is "which algorithm should we pick?" → hand to `Crypt`. If it is "does this actually break at runtime?" → hand to `Probe`.

## Workflow

```
SCAN       → enumerate auth entrypoints (login, signup, refresh, logout,
             password-reset, email-verify, SSO callback, MFA challenge)
           → locate session store, JWT issuer/verifier, OAuth client config
           → list password-hash + MFA code paths

PRIORITIZE → CRITICAL: alg=none / alg-confusion, unsigned refresh, plain
             password storage, hardcoded JWT secret (CWE-798)
           → HIGH: missing PKCE, open redirect in OAuth callback, absent
             MFA on privileged ops, session fixation, weak password policy
           → MEDIUM: long session lifetime with no rotation, verbose auth
             error leaks, missing clock-skew tolerance
           → LOW: non-HttpOnly/Secure cookie flags on non-auth cookies

FILTER     → suppress framework-guaranteed paths (e.g. Devise bcrypt default,
             NextAuth PKCE-by-default) unless overridden in config

SECURE     → apply the minimal fix: pin JWT `alg`, add `aud`/`iss`/`exp`
             checks, enforce PKCE, rotate session on privilege change,
             move secret to env/KMS, raise bcrypt cost or migrate to argon2id

VERIFY     → re-read the diff; confirm no regression on logout/refresh
           → unit test the failure path (invalid token, expired, wrong aud)

PRESENT    → severity + confidence + OWASP A07:2025 + CWE + file:line
           → cross-link: Crypt (if algorithm choice), Probe (if runtime
             confirmation recommended)
```

## High-Signal Patterns

| Area | Bad | Good |
|------|-----|------|
| JWT verify | `jwt.verify(token, secret)` with no algorithms option | `jwt.verify(token, key, { algorithms: ['RS256'], audience, issuer })` |
| Session | Reusing session ID across login boundary | Rotate session ID on login, privilege change, and MFA completion |
| OAuth | No `state`/PKCE, wildcard redirect | `state` + PKCE (S256), strict redirect allowlist |
| Password | `md5`/`sha1`/`sha256(password)` | argon2id (default), bcrypt cost ≥ 12, per-user salt |
| MFA | MFA optional on admin endpoints | Enforce MFA on privileged routes; verify TOTP window ≤ ±1 |
| Reset flow | Token never expires, predictable | 15-min TTL, single-use, CSPRNG, bound to user+email |

## Anti-Patterns (fail the audit)

- Accepting `alg: "none"` or allowing HS256 verification with an RSA public key (alg-confusion, CVE class seen in 2015+ and still appearing).
- Storing refresh tokens in `localStorage` on browsers (XSS = total compromise).
- Hardcoded JWT signing secret in source (CWE-798) — route to `secrets` recipe for git-history scrub + revocation.
- Silent fallback: `if (!token) allow()` style middleware.
- Treating email-verify link as proof of MFA.
- Username enumeration via timing or differentiated error messages.
- Logging the full `Authorization` header or refresh token.
- Missing `kid` validation, or trusting `kid` path to fetch an arbitrary key.

## Handoff

| Target | When | Carry |
|--------|------|-------|
| `Crypt` | Algorithm / KDF / key-rotation decision is ambiguous | Current algo, threat model, compliance constraints |
| `Probe` | Finding is high-confidence and runtime confirmation adds value | Endpoint, auth flow, expected exploit path |
| `Builder` | Fix is > 50 lines or touches shared auth middleware | Fix spec, OWASP mapping, acceptance criteria |
| `Vigil` | Pattern is detectable at runtime (e.g. repeated 401s, alg-none attempts) | Rule seed: log pattern + threshold |
| `Radar` | Regression coverage missing on auth boundary | Failing-path test cases to add |

## Output Template

```
Finding: [short title]
Severity: CRITICAL | HIGH | MEDIUM | LOW
Confidence: HIGH | MEDIUM | LOW
OWASP: A07:2025 – Identification and Authentication Failures
CWE: [287 | 384 | 521 | 798 | ...]
File:Line: path/to/file.ts:NN
Evidence: [3-6 line code quote]
Impact: [attacker capability in 1 sentence]
Remediation: [concrete diff or library change]
Verification: [test or log to confirm fix]
Cross-link: [Crypt / Probe / Builder if applicable]
```
