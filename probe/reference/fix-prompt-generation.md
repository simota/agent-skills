# Probe LLM Fix Prompt Generation

**Purpose:** Probe-specific action verbs, suppression cases, template fields for the `## LLM Fix Prompt` block when Probe pairs a confirmed runtime exploit with a paste-ready prompt for downstream remediation.
**Read when:** Probe has confirmed a runtime exploit (or compensating control is needed) and is handing off remediation to Builder, Gear, Guardian, Beacon, or Sentinel.

> Universal authoring rules and prompt structure: `_common/LLM_PROMPT_GENERATION.md`.
> This file documents only Probe-specific verbs, suppression cases, template fields.

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

Each fix prompt declares one verb at the top of `# Your task`. See the Verb table in `SKILL.md` § LLM Fix Prompt Generation for the full verb → receiving-agent mapping (`EXPLOIT-FIX`, `HARDEN-RUNTIME`, `MITIGATE`, `BREAKING-FIX`, `AUTH-FIX`, `INVESTIGATE-FURTHER`).

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
