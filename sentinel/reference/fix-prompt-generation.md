# Sentinel LLM Fix Prompt Generation

**Purpose:** Sentinel-specific action verbs, suppression cases, template fields, and worked example for the `## LLM Fix Prompt` block when Sentinel hands off remediation to Builder rather than shipping the fix inline.
**Read when:** Sentinel has identified a finding but is NOT shipping the fix itself (size > 50 lines, breaking change, auth logic, or explicit review-only mode).

> Universal authoring rules and prompt structure: `_common/LLM_PROMPT_GENERATION.md`.
> This file documents only Sentinel-specific verbs, suppression cases, template fields, and an example.

## Contents

- When Sentinel emits a Fix Prompt vs ships inline
- Sentinel action verbs
- Verb selection heuristic
- Sentinel-specific suppression cases
- Per-finding fix prompt template (Sentinel-specific fields)
- Worked example

---

## When Sentinel Emits a Fix Prompt vs Ships Inline

Sentinel ships fixes inline (≤ 50 lines, no breaking change, no auth touch). The Fix Prompt is for the cases where Sentinel hands off:

| Situation | Action |
|-----------|--------|
| Fix fits in ≤ 50 lines, no breaking change, no auth touch | Ship inline. **Suppress Fix Prompt.** |
| Fix > 50 lines OR spans multiple modules | Hand off to Builder with `SECURE-FIX` prompt |
| Breaking change required (API shape, response code) | Hand off to Builder with `BREAKING-FIX` prompt |
| Auth logic touched (session, JWT, OAuth, MFA, password storage) | Hand off to Builder with `AUTH-FIX` prompt (Sentinel "Ask First" rule) |
| Hardcoded secret detected | Ship file removal inline if safe; emit `REVOKE-AND-ROTATE` prompt for the operator (revocation, not just deletion) |
| User explicitly requests review-only mode | Hand off to Builder with appropriate verb |
| Static-analysis inconclusive | Suppress Fix Prompt; escalate to Probe |

The `SENTINEL_TO_BUILDER` handoff carries a `fix_prompt` field; populate it whenever Sentinel does NOT ship the fix.

---

## Sentinel Action Verbs

Each fix prompt declares one verb at the top of `# Your task`.

| Verb | When to use | Receiving agent / LLM |
|------|-------------|----------------------|
| `SECURE-FIX` | HIGH/MEDIUM confidence, fix exceeds Sentinel's 50-line budget, no auth or breaking concern | Builder |
| `HARDEN` | ENHANCEMENT-class finding (defense-in-depth, audit logging, input limits) | Builder |
| `MITIGATE` | Compensating control while underlying fix is blocked (e.g., add WAF rule while patching upstream) | Builder + Beacon |
| `BREAKING-FIX` | Fix requires API shape change, response code change, or removes a public surface | Builder + Guardian + Launch |
| `AUTH-FIX` | Fix touches authentication / authorization / session / token logic | Builder + Guardian + Probe |
| `REVOKE-AND-ROTATE` | Hardcoded secret detected — file removal is insufficient; operator must revoke at the issuer and rotate | Operator (human) |
| `INVESTIGATE-FURTHER` | Static analysis inconclusive — receiving agent must verify exploitability before changing code | Probe (DAST), Breach (red team), or Sentinel re-entry |

---

## Verb Selection Heuristic

```
Severity == CRITICAL ─┬─ secret detected ───────────────→ REVOKE-AND-ROTATE
                      ├─ auth logic involved ────────────→ AUTH-FIX
                      ├─ breaking change required ──────→ BREAKING-FIX
                      └─ scoped fix > 50 lines ─────────→ SECURE-FIX

Severity == HIGH/MEDIUM ─┬─ scoped fix, no breakage ───→ SECURE-FIX (or ship inline if ≤50 lines)
                          └─ underlying blocked, need WAF/control ──→ MITIGATE

Severity == ENHANCEMENT ─→ HARDEN

Static-analysis inconclusive (need runtime exploit confirmation) ─→ INVESTIGATE-FURTHER (route to Probe)
```

Tiebreakers:
- `CRITICAL` + secret → always `REVOKE-AND-ROTATE`. Even if Sentinel deletes the file, the secret persists in git history; the operator must revoke at the issuer (cloud provider, API vendor, etc.). Per GitGuardian 2026, 64% of valid secrets from 2022 remained unrevoked in 2026.
- `AUTH-FIX` always cross-links to Probe for runtime verification — auth fixes that "look right" frequently fail real attacker testing.
- `BREAKING-FIX` always includes a Launch handoff — breaking changes need release coordination.

---

## Sentinel-Specific Suppression Cases

Universal cases live in `_common/LLM_PROMPT_GENERATION.md`. Sentinel adds:

| Case | Reason | Note in report |
|------|--------|----------------|
| Sentinel ships the fix inline (≤ 50 lines, no breaking, no auth touch) | The fix IS the artifact | "Fix prompt N/A — fix shipped inline (see changed files: …)." |
| Static-analysis is inconclusive and Sentinel escalates to Probe (DAST) | Probe owns the dynamic remediation prompt after exploit confirmation | "Fix prompt suppressed — Probe owns remediation prompt after runtime verification." |
| Finding is suppressed as false positive | Not actionable | "Fix prompt withheld — finding suppressed as false positive (reason: …)." |
| Finding is `LOW` confidence (< 50%) and reported only on user request | Acting on low-confidence findings can introduce regressions | "Fix prompt withheld — confidence below 50% threshold." |

---

## Per-Finding Fix Prompt Template (Sentinel Fields)

Sentinel adds these Sentinel-specific blocks on top of the universal skeleton:

- `Vulnerability classification` — OWASP Top 10:2025 category, CWE ID, CVSS estimate
- `Evidence` — vulnerable code snippet, scanner output (if any), exploit pattern
- `Defensive controls` — recommended libraries, framework-native protections, configuration
- For `BREAKING-FIX` / `AUTH-FIX` — `User-facing impact` and `Rollback plan`
- For `REVOKE-AND-ROTATE` — `Revocation steps` (issuer-specific) and `Audit query` (was the secret used?)

````markdown
## LLM Fix Prompt

```text
# Your task
<VERB> the security finding described below.

# Finding context
- Title: [brief description]
- Severity: [CRITICAL | HIGH | MEDIUM | LOW | ENHANCEMENT]
- Confidence: [HIGH | MEDIUM | LOW] (Sentinel's static-analysis confidence)
- OWASP category: [e.g., A05:2025 – Security Misconfiguration]
- CWE: [e.g., CWE-89 SQL Injection]
- CVSS estimate: [e.g., 9.1 / Critical] (when applicable)

# Vulnerability
[What the vulnerability is and how it can be exploited]

Location: `<file>:<line>` in `<function>()`

# Evidence
Vulnerable code:
```
[verbatim code snippet]
```

Exploit pattern (illustrative — do NOT include in fix verification):
```
[example malicious input or attack vector]
```

Scanner output (if multi-engine consensus): [tools that flagged this finding]

# Recommended fix
Approach: [high-level fix strategy — defensive library, parameterization, etc.]
Files to modify: [list with expected change per file]
Defensive controls:
- [library name + version, e.g., `Zod 3.22+` for input validation]
- [framework-native control, e.g., Express `helmet()` for headers]
Constraints:
- [side effect / backward-compat note]
- [coupling with other modules]

# [BREAKING-FIX / AUTH-FIX only — User-facing impact]
- API shape change: [yes/no — describe]
- Client breaking change: [yes/no — describe]
- Migration steps for clients: [list]

# [BREAKING-FIX / AUTH-FIX only — Rollback plan]
- How to revert: [git revert SHA, feature flag toggle, etc.]
- Pre-deploy verification: [staging test, canary, etc.]
- Comms required: [release notes section, security advisory, etc.]

# Acceptance criteria
- [ ] Vulnerable code path no longer accepts the exploit pattern above
- [ ] Defensive controls listed above are wired in
- [ ] Regression test added covering the exploit pattern
- [ ] No new test failures
- [ ] [AUTH-FIX] Probe runtime verification scheduled

# Ruled-out alternatives (do not revisit)
- [alternative 1] — eliminated because [evidence, e.g., framework guarantee]
- [alternative 2] — eliminated because [evidence]

# What NOT to do
- Do not silence the symptom (catch-and-ignore, broad try/except, suppress scanner warning)
- Do not disable security controls "for build convenience"
- Do not commit secrets, even temporarily
- Do not bundle unrelated security changes into the same PR
- Do not expand scope beyond the cited files unless evidence demands it
- [domain-specific anti-action]
```
````

For `REVOKE-AND-ROTATE`, the prompt is addressed to the human operator, not a coding LLM:

````markdown
## LLM Fix Prompt

```text
# Your task
REVOKE-AND-ROTATE the secret described below. This is an operator action — file
deletion alone is insufficient because the secret persists in git history.

# Secret context
- Title: [secret type — e.g., AWS Access Key, GitHub PAT, Stripe API key]
- Severity: CRITICAL
- Detected in: `<file>:<line>` (commit <SHA> if git-history scan)
- Issuer: [cloud provider / vendor]

# Evidence
Detection pattern: [regex name + entropy score]
Verbatim secret prefix: `<first 4 chars only — never paste full secret>`

# Revocation steps
1. Log into [issuer console URL]
2. Navigate to [credentials/keys section]
3. Revoke the key with prefix `<first 4 chars>` and creation date `<YYYY-MM-DD>`
4. Generate a replacement and store it in [secrets manager — Vault, AWS Secrets Manager, etc.]
5. Update consuming services to use the new secret

# Audit query (was the secret used between leak and revocation?)
- [provider-specific audit log query, e.g., `aws cloudtrail lookup-events …`]
- [time range: from leak detection time to revocation time]

# Acceptance criteria
- [ ] Secret revoked at the issuer (verify in console)
- [ ] Replacement secret deployed to all consumers
- [ ] Audit log reviewed for unauthorized use
- [ ] git-secrets or pre-commit hook installed to prevent recurrence
- [ ] Incident logged in security tracking system

# What NOT to do
- Do not assume `git rm` or `git filter-branch` is sufficient — secrets persist
  in cached forks, GitHub event API, and clones
- Do not skip the audit log review even if revocation was fast
- Do not paste the revoked secret into chat, tickets, or PR descriptions
```
````

---

## Worked Example (SECURE-FIX)

**Scenario:** SQL injection in a search endpoint that builds a query via string concatenation.

````markdown
## LLM Fix Prompt

```text
# Your task
SECURE-FIX the security finding described below.

# Finding context
- Title: SQL injection in /api/search via unparameterized query
- Severity: CRITICAL
- Confidence: HIGH (multi-engine consensus: Semgrep + CodeQL + Sentinel)
- OWASP category: A03:2025 – Injection
- CWE: CWE-89 (SQL Injection)
- CVSS estimate: 9.1 / Critical

# Vulnerability
The search endpoint constructs the SQL query by concatenating the user-supplied
`q` query parameter directly into the WHERE clause. An attacker can inject SQL
to extract arbitrary data from the database, including the users table.

Location: `src/api/search.ts:42` in `searchHandler()`

# Evidence
Vulnerable code:
```
const results = await db.raw(
  `SELECT id, title FROM products WHERE name LIKE '%${req.query.q}%'`
);
```

Exploit pattern (illustrative — do NOT include in fix verification):
```
GET /api/search?q=%25%27%20UNION%20SELECT%20id%2C%20password%20FROM%20users--
```

Scanner output: Semgrep `tainted-sql-string` (HIGH), CodeQL `js/sql-injection`
(error), Sentinel pattern match.

# Recommended fix
Approach: Use parameterized query with the database driver's binding mechanism.
Replace the raw concatenation with a prepared statement and a bound parameter.
Add Zod validation on `q` to bound length and reject control characters.

Files to modify:
- src/api/search.ts — replace `db.raw(...)` with `db.select(...).where('name', 'LIKE', ...)`, add Zod schema
- src/api/search.test.ts — add test cases for injection patterns

Defensive controls:
- Knex query builder (already in use) — `.where('name', 'LIKE', `%${q}%`)` parameterizes the bound value
- Zod 3.22+ for input validation — `z.string().max(100).regex(/^[a-zA-Z0-9 .-]+$/)`
- Rate limiting via `express-rate-limit` (5 req/sec/ip) — already wired in middleware

Constraints:
- Public response shape must remain `{ id, title }[]` — do not include extra fields
- Pagination cursor format must remain backward-compatible

# Acceptance criteria
- [ ] Vulnerable concatenation removed from src/api/search.ts:42
- [ ] All queries use bound parameters (verified by `grep -r "db.raw" src/`)
- [ ] Zod schema rejects strings > 100 chars and control characters
- [ ] Regression test covers UNION SELECT, OR 1=1, and `--` comment patterns
- [ ] No new test failures in src/api/search.test.ts

# Ruled-out alternatives (do not revisit)
- WAF-only mitigation — eliminated: WAF rules are bypassed by encoding tricks
  and do not address the root cause
- Manual escaping (`q.replace("'", "''")`) — eliminated: manual escaping is
  fragile and CWE-89 explicitly warns against it
- Switching to NoSQL — eliminated: out of scope; the existing relational schema
  is correct, only the query construction is wrong

# What NOT to do
- Do not silence the symptom by removing the search feature
- Do not catch-and-ignore SQL exceptions — they are the only signal that the fix is wrong
- Do not commit any debug code that prints query strings (information disclosure)
- Do not add a "trusted internal" bypass for the validation
- Do not bundle unrelated changes (UI tweaks, copy edits) into this security PR
```
````

This prompt is self-contained: a coding LLM can act on it without seeing the rest of the Sentinel report.
