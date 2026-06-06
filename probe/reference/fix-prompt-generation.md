# Probe LLM Fix Prompt Generation

**Purpose:** Probe-specific action verbs, suppression cases, template fields, and worked example for the `## LLM Fix Prompt` block when Probe pairs a confirmed runtime exploit with a paste-ready prompt for downstream remediation.
**Read when:** Probe has confirmed a runtime exploit (or compensating control is needed) and is handing off remediation to Builder, Gear, Guardian, Beacon, or Sentinel.

> Universal authoring rules and prompt structure: `_common/LLM_PROMPT_GENERATION.md`.
> This file documents only Probe-specific verbs, suppression cases, template fields, and an example.

## Contents

- When Probe emits a Fix Prompt vs suppresses
- Probe action verbs
- Verb selection heuristic
- Probe-specific suppression cases
- Per-finding fix prompt template (Probe-specific fields)
- Worked example

---

## When Probe Emits a Fix Prompt vs Suppresses

Probe is a verification agent — it does not ship source-level fixes itself. The Fix Prompt is mandatory whenever Probe confirms a runtime exploit, and is suppressed when verification is incomplete or another agent owns the remediation prompt.

| Situation | Action |
|-----------|--------|
| Confirmed runtime exploit, scoped fix possible | Emit `EXPLOIT-FIX` prompt to Builder |
| Confirmed exploit, defense-in-depth recommended on top of source fix | Emit `HARDEN-RUNTIME` prompt to Builder + Gear |
| Underlying fix blocked or slow to deploy; need WAF/IP block/feature flag | Emit `MITIGATE` prompt to Builder + Beacon |
| Fix requires API shape or contract change | Emit `BREAKING-FIX` prompt to Builder + Guardian + Launch |
| Authentication / session / authorization bypass confirmed | Emit `AUTH-FIX` prompt to Builder + Guardian + Sentinel |
| Anomaly observed but exploit path unconfirmed | Emit `INVESTIGATE-FURTHER` prompt to Breach or Probe re-entry |
| Sentinel already owns the source-level remediation prompt | **Suppress** — Probe's report covers runtime confirmation only |
| Reconnaissance / scope-mapping only (no exploit attempt) | **Suppress** — no actionable finding |
| Probe escalates to Breach for adversarial validation | **Suppress** — Breach owns red-team remediation prompt |

The `PROBE_TO_BUILDER` (and parallel) handoffs carry a `fix_prompt` field; populate it whenever Probe confirms a runtime exploit and does NOT suppress per the table above.

---

## Probe Action Verbs

Each fix prompt declares one verb at the top of `# Your task`.

| Verb | When to use | Receiving agent / LLM |
|------|-------------|----------------------|
| `EXPLOIT-FIX` | Confirmed runtime exploit with reproducible attack chain, scoped fix possible | Builder |
| `HARDEN-RUNTIME` | Defense-in-depth based on observed attack surface (rate limit, WAF rule, header) | Builder + Gear |
| `MITIGATE` | WAF rule / IP block / feature flag while patching upstream | Builder + Beacon (alerting) |
| `BREAKING-FIX` | API or contract change required to close the vulnerability | Builder + Guardian + Launch |
| `AUTH-FIX` | Authentication / session / authorization bypass confirmed via runtime test | Builder + Guardian + Sentinel |
| `INVESTIGATE-FURTHER` | Anomaly observed but exploit path unconfirmed; need deeper red-team analysis | Breach (red team) or Probe re-entry |

---

## Verb Selection Heuristic

```
Exploit confirmed (reproducible attack chain) ─┬─ auth/session/authz bypass ─────→ AUTH-FIX
                                                ├─ requires API/contract change ──→ BREAKING-FIX
                                                ├─ underlying fix blocked ────────→ MITIGATE
                                                ├─ defense-in-depth on top ───────→ HARDEN-RUNTIME
                                                └─ scoped source fix possible ────→ EXPLOIT-FIX

Anomaly observed, exploit path unconfirmed ─────────────────────────────────────→ INVESTIGATE-FURTHER

Sentinel owns source-level remediation ─────────────────────────────────────────→ SUPPRESS
Reconnaissance / scope-mapping only ────────────────────────────────────────────→ SUPPRESS
Escalating to Breach for red-team validation ───────────────────────────────────→ SUPPRESS
```

Tiebreakers:
- `AUTH-FIX` always cross-links to Sentinel for static-rule refinement and Guardian for release gating — auth bypasses confirmed at runtime usually indicate missing static rules.
- `BREAKING-FIX` always includes a Launch handoff — breaking changes need release coordination and client-side migration windows.
- `MITIGATE` always includes a Beacon handoff — compensating controls (WAF rules, IP blocks) need monitoring so the team knows when the underlying patch must land.
- `INVESTIGATE-FURTHER` defaults to Breach when adversarial creativity is needed; defaults to Probe re-entry when more scan time / different tool / different identity tier resolves the gap.

---

## Probe-Specific Suppression Cases

Universal cases live in `_common/LLM_PROMPT_GENERATION.md`. Probe adds:

| Case | Reason | Note in report |
|------|--------|----------------|
| Exploit requires source-level fix that Sentinel should author | Sentinel owns source-level remediation; Probe's role is runtime confirmation | "Fix prompt suppressed — Sentinel owns source-level remediation prompt; this report covers runtime confirmation only." |
| Exploit is out of scope (third-party service, infrastructure) | Remediation lives outside the codebase | "Fix prompt withheld — exploit is in [3rd-party / infra]; coordinate via [responsible party]." |
| Probe escalates to Breach for adversarial validation | Breach owns the red-team remediation prompt after deeper attack-path analysis | "Fix prompt suppressed — Breach owns red-team validation prompt before remediation." |
| Test was reconnaissance / scope-mapping only | No exploit was attempted; no actionable finding | "Fix prompt N/A — reconnaissance only." |

---

## Per-Finding Fix Prompt Template (Probe Fields)

Probe adds these Probe-specific blocks on top of the universal skeleton:

- `Attack chain` — ordered steps that reproduce the exploit (curl/HTTP request sequence, ZAP attack ID, Nuclei template ID, Burp request reference)
- `Tool evidence` — tool name + scan ID + finding ID (ZAP / Burp / Nuclei output reference)
- `Affected endpoints` — URL paths, HTTP methods, parameters
- `Runtime observation` — what response/behavior confirms the exploit (status code, response content, side effect, timing)
- For `BREAKING-FIX` / `AUTH-FIX` — `User-facing impact` and `Rollback plan`
- For `MITIGATE` — `Underlying status` (why source fix is blocked) and `Compensating control lifetime`

````markdown
## LLM Fix Prompt

```text
# Your task
<VERB> the runtime exploit described below.

# Finding context
- Title: [brief description]
- Severity: [CRITICAL | HIGH | MEDIUM | LOW]
- Confidence: [HIGH | MEDIUM | LOW] (Probe's runtime-verification confidence)
- CVSS v4.0 vector: [e.g., CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N]
- CVSS v4.0 score: [e.g., 9.3 / Critical] (or v3.1 fallback)
- OWASP category: [e.g., A01:2025 – Broken Access Control]
- CWE: [e.g., CWE-639 IDOR, CWE-918 SSRF]

# Vulnerability
[What the vulnerability is and why the runtime test confirmed it is exploitable]

Affected endpoints:
- [METHOD] [URL path] — [parameter(s) under attack]

# Attack chain (reproducible)
1. [Step 1 — e.g., authenticate as user A, capture session token]
2. [Step 2 — e.g., issue request with user B's resource ID]
3. [Step 3 — e.g., observe successful response]

Verbatim exploit request:
```
[exact HTTP request — method, path, headers, body]
```

# Runtime observation (confirms exploit)
- Response status: [e.g., 200 OK instead of 403 Forbidden]
- Response body excerpt: [verbatim content proving data leak / state change]
- Side effect: [e.g., DB row modified, email sent, cache poisoned]
- Timing: [if blind/time-based — measured deltas]

# Tool evidence
- Tool: [ZAP / Burp / Nuclei / Autorize / schemathesis]
- Scan ID: [tool-specific scan/run identifier]
- Finding ID: [tool-specific finding identifier]
- Output reference: [path to raw output, screenshot, HAR file]

# Recommended fix
Approach: [high-level fix strategy — server-side authorization check, parameterization, allowlist, etc.]
Files to modify (best guess from runtime path; verify against source):
- [path/to/handler.ts] — [expected change]
- [path/to/middleware.ts] — [expected change]
Defensive controls:
- [framework-native control, e.g., Express middleware `requireOwnership(resourceId)`]
- [library, e.g., `casl` for ABAC enforcement]
Constraints:
- [side effect / backward-compat note]
- [coupling with other endpoints]

# [BREAKING-FIX / AUTH-FIX only — User-facing impact]
- API shape change: [yes/no — describe]
- Client breaking change: [yes/no — describe]
- Migration steps for clients: [list]

# [BREAKING-FIX / AUTH-FIX only — Rollback plan]
- How to revert: [git revert SHA, feature flag toggle, etc.]
- Pre-deploy verification: [staging Probe re-run, canary, etc.]
- Comms required: [release notes, security advisory, etc.]

# [MITIGATE only — Underlying status]
- Why source fix is blocked: [reason — e.g., upstream library, breaking change in flight]
- Target ETA for source fix: [date or release]
- Compensating control lifetime: [WAF rule expiry, feature flag sunset]

# Acceptance criteria
- [ ] Attack chain above no longer succeeds against the patched endpoint
- [ ] Defensive controls listed above are wired in
- [ ] Probe re-run reproduces "blocked" instead of "exploited"
- [ ] Regression test added (Radar handoff) covering the attack chain
- [ ] No new test failures
- [ ] [AUTH-FIX] Sentinel static-rule update scheduled

# Ruled-out alternatives (do not revisit)
- [alternative 1] — eliminated because [evidence, e.g., bypassed by URL encoding in Probe test #N]
- [alternative 2] — eliminated because [evidence]

# What NOT to do
- Do not silence the symptom (catch-and-ignore the auth exception, suppress the scanner alert)
- Do not rely on client-side validation as the fix — runtime test bypassed it
- Do not add a "trusted internal" bypass for the new check
- Do not disable the Probe scan or downgrade the finding to suppress the alert
- Do not commit attack payloads or PII captured during testing
- Do not bundle unrelated security changes into the same PR
- Do not expand scope beyond the cited endpoints unless evidence demands it
```
````

For `INVESTIGATE-FURTHER`, replace `Recommended fix` with `Verification plan` and address the prompt to Breach or a re-entered Probe session:

````markdown
## LLM Fix Prompt

```text
# Your task
INVESTIGATE-FURTHER the runtime anomaly described below. The exploit path is
unconfirmed; do not change application code until exploitability is established.

# Anomaly context
- Title: [brief description]
- Severity (preliminary): [HIGH | MEDIUM | LOW]
- Confidence: LOW (anomaly observed, exploit unconfirmed)
- Suspected OWASP category: [e.g., A01:2025]

# Observed anomaly
[What was seen — unusual response, timing delta, error leak, etc.]

# Verification plan
1. [Hypothesis 1 to test — e.g., reissue request with second identity tier]
2. [Hypothesis 2 to test — e.g., fuzz parameter with schemathesis]
3. [Hypothesis 3 to test — e.g., manual Burp Repeater walkthrough]

# Evidence captured so far
- [Tool output reference]
- [HAR file path]
- [Response excerpt]

# What NOT to do
- Do not patch application code based on this report alone
- Do not file a CVE or security advisory until exploitability is confirmed
- Do not run destructive payloads in shared environments
- Do not expand scope beyond the cited endpoints
```
````

---

## Worked Example (EXPLOIT-FIX — IDOR)

**Scenario:** A REST endpoint serving user invoices accepts an `invoiceId` path parameter without verifying that the authenticated user owns the invoice. Probe confirmed the exploit by authenticating as user A and reading user B's invoice.

````markdown
## LLM Fix Prompt

```text
# Your task
EXPLOIT-FIX the runtime exploit described below.

# Finding context
- Title: IDOR on GET /api/invoices/:invoiceId — cross-tenant invoice read
- Severity: HIGH
- Confidence: HIGH (reproduced 5/5 attempts across 2 identity pairs)
- CVSS v4.0 vector: CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N
- CVSS v4.0 score: 7.1 / High
- OWASP category: A01:2025 – Broken Access Control
- CWE: CWE-639 (Authorization Bypass Through User-Controlled Key)

# Vulnerability
The invoice retrieval handler loads the invoice by ID but does not verify that
the authenticated user owns it. Any authenticated user can read any invoice by
guessing or enumerating IDs. Sequential integer IDs make enumeration trivial.

Affected endpoints:
- GET /api/invoices/:invoiceId — `invoiceId` path parameter under attack

# Attack chain (reproducible)
1. Authenticate as user A (tenant 1) and capture session cookie `sid=AAA`.
2. Authenticate as user B (tenant 2) in a separate session; create invoice via
   POST /api/invoices and note the returned `invoiceId=10042`.
3. Reuse user A's session cookie to GET /api/invoices/10042.
4. Observe HTTP 200 with user B's invoice payload (PII + amount + line items).

Verbatim exploit request:
```
GET /api/invoices/10042 HTTP/1.1
Host: staging.example.com
Cookie: sid=AAA
Accept: application/json
```

# Runtime observation (confirms exploit)
- Response status: 200 OK (expected: 403 Forbidden or 404 Not Found)
- Response body excerpt:
  `{"invoiceId":10042,"tenantId":2,"customerEmail":"userB@example.com","amount":4500,...}`
- Side effect: none (read-only), but full PII + financial data exposure
- Timing: response time matches owner-access baseline (no auth check on path)

# Tool evidence
- Tool: Burp Suite Professional (Autorize extension)
- Scan ID: probe-2026-05-01-staging-invoices-001
- Finding ID: AUTORIZE-IDOR-0042
- Output reference: .agents/probe/runs/2026-05-01/autorize-idor-0042.har

# Recommended fix
Approach: Add server-side ownership check in the invoice handler. Reject the
request with 404 (not 403) when the invoice's `tenantId` does not match the
authenticated user's `tenantId` — using 404 prevents existence oracle leakage.

Files to modify (best guess from runtime path; verify against source):
- src/api/invoices/[invoiceId].ts — add `requireOwnership(invoice, req.user)` before serializing
- src/auth/ownership.ts (new or existing) — implement `requireOwnership` helper that throws 404 on mismatch
- src/api/invoices/__tests__/access.test.ts — add cross-tenant read test

Defensive controls:
- Existing session middleware (`requireAuth`) — already wired in; this is an
  authorization gap, not authentication
- `casl` ABAC library (already in dependencies) — define `Invoice` ability with
  `tenantId === user.tenantId` rule and call `ability.can('read', invoice)`
- Switch IDs from sequential integers to ULIDs in a follow-up PR (not blocking;
  defense-in-depth — see HARDEN-RUNTIME below)

Constraints:
- Public response shape must remain unchanged for owner reads
- Do not return 403 — 404 prevents enumeration of existing invoice IDs
- Audit log entries for cross-tenant attempts must be added (Beacon will alert)

# Acceptance criteria
- [ ] Attack chain above returns 404 for cross-tenant requests on the patched endpoint
- [ ] `requireOwnership` (or `casl` equivalent) wired into the handler at src/api/invoices/[invoiceId].ts
- [ ] Probe re-run on staging reproduces "blocked" (404) instead of "exploited" (200)
- [ ] Regression test added covering: owner read 200, cross-tenant read 404, unauthenticated 401
- [ ] No new test failures in src/api/invoices/__tests__/
- [ ] Audit log entry emitted on every cross-tenant attempt (consumed by Beacon)

# Ruled-out alternatives (do not revisit)
- WAF rule blocking enumeration patterns — eliminated: WAF cannot distinguish
  legitimate from malicious access by URL alone; root cause is missing authz
- Switching IDs to UUIDs without adding the authz check — eliminated: Probe
  attempted enumeration with valid IDs captured from a second account; UUIDs
  alone do not stop the attack once an attacker holds a valid ID
- Returning 403 instead of 404 — eliminated: 403 leaks existence of the resource
  and enables enumeration via response-code differential (CWE-204)

# What NOT to do
- Do not silence the symptom by removing the invoice endpoint or hiding it behind
  a feature flag — the data remains accessible to anyone with the URL
- Do not catch-and-ignore the new authorization exception — let it propagate to
  the audit log so Beacon can detect attack patterns
- Do not add a "trusted internal" bypass (`if (req.headers['x-internal']) return invoice`)
  — internal headers are spoofable
- Do not disable the Burp Autorize check or downgrade the finding to suppress the alert
- Do not commit any captured invoice payload, customer email, or financial data
  into tests, fixtures, or PR descriptions — use synthetic data
- Do not bundle ULID migration into this PR — ship the authz fix first; ULIDs
  are tracked separately as HARDEN-RUNTIME defense-in-depth
- Do not expand scope beyond src/api/invoices/[invoiceId].ts unless other handlers
  show the same pattern in source review (escalate to Sentinel for sweep)
```
````

This prompt is self-contained: a coding LLM (or Builder) can act on it without seeing the rest of the Probe report. After remediation, Probe re-runs the attack chain and updates the report with the new "blocked" status.
