# Multi-Engine Parallel Scan

> **Filename retained** as `tri-engine-scan.md` for backward compatibility. Covers both dual-engine baseline (Claude + Codex) and tri-engine optional (Claude + Codex + agy) modes.

Sentinel-specific implementation of the multi-engine concurrence pipeline for static security analysis (SAST). Run scans in parallel via subagents — one per AVAILABLE engine — integrate findings, ground single-engine candidates against the actual source and lockfiles, and ship **only security findings that warrant action**.

**Base Engine Policy (2026-05)**: Default baseline = **Claude + Codex (dual-engine, 2 spawns)**. agy adds a third axis (tri-engine, 3 spawns) when AVAILABLE at PREFLIGHT. For Sentinel the agy uplift adds Google OSS-Vulnerability + Wiz CVE corpus; dual-engine still covers GitHub Security Advisory (Codex) + Anthropic-curated security research (Claude). Pattern C scoring in dual-engine: CONFIRMED=2/2 (ship after spot-check), CANDIDATE=1/2 (strict grounding mandatory). LIKELY structurally unreachable — the bar for shipping a single-engine security finding is automatically higher. See `_common/MULTI_ENGINE_RECIPE.md §Base Engine Policy + §Engine Availability Modes`.

**Pattern**: C (Concurrence-primary). Read `_common/MULTI_ENGINE_RECIPE.md` first for canonical flow, PREFLIGHT probe, engine-attribution conventions, and engine-availability modes. This document records only the Sentinel-specific deltas.

**Why three engines for SAST**: Each engine carries a different CVE/CWE prior distribution and was trained on non-overlapping vulnerability corpora. Single-tool SAST misses 78% of confirmed vulnerabilities (Veracode 2026). Concurrence collapses false positives — engines rarely hallucinate the *same* fake CWE at the *same* file:line — while still surfacing genuine single-engine catches after grounding. Independent subagent contexts also eliminate the self-bias that compromises Claude-only review of potentially Claude-authored code.

---

## Flow (delta from `_common/MULTI_ENGINE_RECIPE.md`)

```
SCOPE → PREFLIGHT → FAN-OUT → NORMALIZE → CLUSTER → SCORE → GROUND → ARBITRATE → FILTER → REPORT
```

Only the Sentinel-specific steps are documented below. PREFLIGHT (binary probe + fallback paths + strict availability verdict) and FAN-OUT (parallel Agent calls in a single message, JSON output mandate, subscription auth only) are inherited from the common protocol.

---

## 1. SCOPE — security-specific

Set once for all three subagents:

- Target paths (changed files for delta, full tree for periodic full scan)
- Scan focus subset (default: full OWASP Top 10:2025 + secrets + dependencies; recipe-narrowed when invoked via `secrets` / `injection` / `deps` / `authn` / `authz` / `aisec` / `mobile`)
- Project context (framework, runtime, threat model, REVIEW.md / AGENTS.md / CLAUDE.md / SECURITY.md content if present)
- Severity floor (default MEDIUM; LOW only when user requests exhaustive)
- AI-code flag (heightened scrutiny path triggered when changes are AI-authored — CWE-80/117 prioritization, Plausible Hallucination check, slopsquat detection on every new import)
- Lockfile / SBOM paths (`package-lock.json`, `pnpm-lock.yaml`, `yarn.lock`, `Cargo.lock`, `go.sum`, `poetry.lock`, `requirements.txt`, `Gemfile.lock`) for the `deps` axis

---

## 2. FAN-OUT — security-focused subagent prompts

| Subagent | Engine | Baseline command |
|----------|--------|------------------|
| `scan-codex` | Codex CLI | `codex exec --full-auto "<security-focused prompt>"` |
| `scan-agy` | Antigravity CLI | `agy -p "<security-focused prompt>" --dangerously-skip-permissions --log-file <path>` (silent-failure detection mandatory — see `_common/MULTI_ENGINE_RECIPE.md §3.5 Engine Runtime Failure Detection`) |
| `scan-claude` | Claude Code CLI (subagent) | Agent tool with `subagent_type: general-purpose` |

**Loose prompt rule** — pass only Role + Target + Output schema + axis focus. Do NOT preload OWASP checklists, CWE catalogs, vulnerability-pattern references, or remediation snippets. Each engine should surface what its training-data priors flag — that diversity is the value.

**Axis focus** — when a recipe other than `scan` is active, narrow the prompt to that axis but keep the full JSON schema. The three engines are told the focus axis (e.g., "Focus: SQL injection + XSS + command injection. CWE-89/79/78"); they are NOT told what specific patterns to look for.

### Security-finding JSON schema (mandatory)

Each subagent returns JSON matching this exact schema. Free-form Markdown forces a re-emit request.

```json
{
  "engine": "codex|agy|claude",
  "findings": [
    {
      "severity": "CRITICAL|HIGH|MEDIUM|LOW|ENHANCEMENT",
      "cwe": "CWE-XXX",
      "owasp": "A0X:2025 – Category Name | LLM0X (LLM Top 10 2025) | MASVS-XXX | none",
      "cve_id": "CVE-YYYY-NNNNN | none (only for dependency findings)",
      "file": "path/to/file.ts",
      "line": 42,
      "line_end": 47,
      "vuln_class": "secret|sql-injection|xss|command-injection|prompt-injection|ssrf|path-traversal|deserialization|missing-authn|missing-authz|idor|weak-crypto|insecure-storage|missing-validation|missing-header|dependency-cve|typosquat|slopsquat|hardcoded-credential|other",
      "title": "One-line description",
      "evidence": "Quoted code or lockfile line + brief mechanism explanation",
      "exploit_scenario": "Attacker action → outcome (one paragraph, concrete)",
      "remediation": "Concrete change (library, config, or code snippet) — keep < 50 lines if inline",
      "engine_notes": "Optional: training-data bias this engine knows it brings"
    }
  ],
  "scope_summary": { "files_scanned": 12, "loc_delta": 340, "deps_checked": 187 }
}
```

Sentinel-specific schema requirements (beyond Judge's):

- `cwe` — mandatory; pinpoints the weakness class for clustering
- `owasp` — mandatory; maps to A0X:2025 / LLM0X / MASVS-XXX / "none" (where Sentinel still ships the finding but flags it as outside the standard mapping)
- `cve_id` — only for `deps` axis findings; null/"none" elsewhere
- `vuln_class` — controlled vocabulary; drives CLUSTER identity
- `exploit_scenario` — required for ≥ HIGH severity; forces engines to demonstrate the bug is exploitable, not theoretical

---

## 3. CLUSTER — Sentinel identity rules

Two findings collapse into one cluster when **all four** hold:

1. Same `vuln_class` OR same `cwe` (CWE is normative; `vuln_class` is the engine-friendly label)
2. Same `file` (exact path match; symlink-resolved)
3. Line range overlap within `±5 lines` (wider than Judge's `±3` because SAST engines often anchor to different points in the same sink — argument vs call site vs assignment)
4. Same OWASP/MASVS category bucket (different sub-categories of A03 are NOT merged; e.g., `A05:2025 Security Misconfiguration → Missing CSP` and `A05:2025 → Permissive CORS` stay separate even if on the same file)

**Dependency-finding clustering** (deps axis):

- Cluster by `(package_name, version_range_affected)` — NOT by file. A CVE in `lodash@4.17.20` reported by three engines is one cluster regardless of how many `package.json` files reference it.
- Slopsquat / typosquat findings cluster by `(package_name, registry)` since the bug *is* the package itself.

**Secret-finding clustering** (secrets axis):

- Cluster by `(file, line, secret_class)` where `secret_class` ∈ `{aws_access_key, openai_api_key, github_token, generic_high_entropy, ...}`. Engines that anchor on the variable name vs the value still cluster if within ±2 lines.

Record the set of engines flagging each cluster.

---

## 4. SCORE — Pattern C concurrence rubric

| Engines flagging | Label | Action |
|------------------|-------|--------|
| 3 / 3 | `CONFIRMED` | Ship after a lightweight spot-check (first CONFIRMED only, to detect shared hallucination) |
| 2 / 3 | `LIKELY` | Ship with concurrence tag; light GROUND (existence + not-already-mitigated) |
| 1 / 3 | `CANDIDATE` | MUST pass strict GROUND to ship; drop if rejected |

Severity is NOT averaged across engines — see ARBITRATE for resolution.

---

## 5. GROUND — Sentinel-strict verification (main context, never delegated)

Sentinel's grounding is stricter than Judge's because **a false-positive security finding has a higher trust cost** (developers learn to ignore Sentinel) **and a false-negative is catastrophic** (the CRITICAL ships). Every CANDIDATE and LIKELY cluster gets explicit grounding; every CONFIRMED gets a one-finding spot-check.

For each finding, answer in order:

### 5.1 Existence (Plausible Hallucination check)

Read the cited `file:line` range with the Read tool. Then verify:

- **Does the cited code exist?** Engines hallucinate plausible-looking sinks. If the function/method/import named in `evidence` is not at that location, REJECT.
- **Does the cited import resolve?** For slopsquat / typosquat findings, query the registry (PyPI JSON API / npm registry / crates.io / RubyGems / Go module proxy / packagist) for existence, publish date, and download count. If the engine flagged a typo but the package is the legitimate one (Levenshtein distance ≥ 3 from a popular package OR > 1M downloads OR > 1 year publish age) → REJECT.
- **Does the cited CVE exist?** For dependency findings, cross-reference NVD or the registry's own advisory feed. If the CVE ID is fabricated or the affected version range doesn't include the project's pinned version → REJECT.

### 5.2 Lockfile / dependency reality check (deps axis)

For every `deps` finding, read the actual lockfile (NOT just `package.json`) and confirm:

- Pinned version falls inside the vulnerable range
- Transitive dependency path is reachable (not behind an unused optional dep)
- No `overrides` / `resolutions` / `pin` already mitigates

Reject CVE findings against versions the project does not actually install.

### 5.3 Upstream mitigation

- Input validation already exists earlier in the call chain (Zod / Joi / pydantic / Bean Validation / framework-native binder)
- Output context already escapes (React's auto-escape, Django auto-escape, framework-templating)
- Framework guarantee already covers (Express's `req.query` type-coerces to string, Django's ORM parameterizes by default, Spring's `@PreAuthorize` enforces)
- Type system rules out the bug (TypeScript `strictNullChecks`, Rust's borrow checker)

If mitigated → REJECT with reason recorded for the ledger.

### 5.4 Fix coherence

- Does the proposed `remediation` actually address the stated `vuln_class`? Engines sometimes suggest a fix unrelated to the bug (e.g., adding a CSP header for an SQL injection finding) — treat as unverified.
- Is the remediation a known anti-pattern (raising blanket `except`, broadening `allowedHosts: ['*']`, disabling CSRF, `eval` workarounds)? REJECT.

### 5.5 Severity sanity

- If `severity: CRITICAL` but `vuln_class` is hygiene-level (missing header, verbose error message) → downgrade per ARBITRATE.
- If `severity: LOW` but the sink is on a production endpoint with no upstream mitigation → upgrade per ARBITRATE.

### 5.6 Verdict

Mark each cluster as `VERIFIED` / `LIKELY-VERIFIED` (keep), `REJECTED` (drop with category), or `NEEDS-INFO` (escalate — flag for user or route to Probe for runtime check).

For CONFIRMED, run sections 5.1 and 5.3 on the first finding only as a sanity check. Skip further grounding unless the spot-check rejects.

---

## 6. ARBITRATE — Sentinel-specific severity rules

Default to the max severity any engine assigned, then apply Sentinel overrides:

| Condition | Override |
|-----------|----------|
| Hardcoded secret confirmed | Force `CRITICAL` regardless of engine label |
| Dependency CVE with CVSS ≥ 9.0 AND reachable code path | Force `CRITICAL` |
| Dependency CVE with CVSS ≥ 9.0 AND unreachable code path | Downgrade to `MEDIUM` (still report; not blocking) |
| Slopsquat / typosquat CONFIRMED | Force `CRITICAL` (supply chain compromise pre-condition) |
| Missing CSRF on a session-cookie endpoint | Force `HIGH` minimum |
| Missing CSP on a public HTML response | `MEDIUM` (not `HIGH`) unless the response embeds user content |
| AI-generated code + CWE-80/117/918/798 | Boost one tier (these CWEs have 86%/88%/high failure rates in AI code per Veracode Spring 2026) |
| Framework guarantee covers the sink | Drop two tiers OR REJECT per GROUND |
| Test file / mock / fixture | Drop to `LOW` or REJECT if not exploitable |

**Remediation routing** (Sentinel-specific):

| Finding shape | Receiving agent |
|---------------|-----------------|
| Fix ≤ 50 lines, no breaking, no auth touch | Ship inline; suppress LLM Fix Prompt |
| Fix > 50 lines OR breaking | Builder + LLM Fix Prompt (`SECURE-FIX` or `BREAKING-FIX`) |
| Auth/authz/session/token touch | Builder + Guardian + Probe (`AUTH-FIX`) |
| Hardcoded secret | Inline file deletion (if safe) + `REVOKE-AND-ROTATE` prompt addressed to the human operator |
| SAST inconclusive but signal is strong | Probe (DAST, `INVESTIGATE-FURTHER`) |
| Dependency CVE | Gear (lockfile update) + Sentinel re-scan |
| Detection-rule opportunity | Vigil (Sigma/YARA from pattern) |

---

## 7. FILTER — actionable-only rule

A finding ships ONLY when ALL of these hold:

- `VERIFIED`, `LIKELY-VERIFIED`, or `CONFIRMED` (no REJECTED)
- Severity ≥ MEDIUM (or user explicitly requested LOW/ENHANCEMENT)
- Has concrete `remediation` (code, config, library, version pin)
- Has concrete `exploit_scenario` for ≥ HIGH (theoretical bugs without a path drop one tier)
- Not already mitigated upstream
- Not style/hygiene-only (those belong to Zen / Guardian)

Goal: every shipped finding is something an operator should fix today.

---

## 8. SYNTHESIZE — Sentinel security report

Output structure (Sentinel-specific augmentation of the standard report):

- **Header**: engines run, engines failed/unavailable, scope summary, concurrence distribution (`CONFIRMED: N, LIKELY: N, VERIFIED: N`)
- **Findings table**, sorted by severity then by concurrence (CONFIRMED → LIKELY → VERIFIED):
  - ID
  - Severity + Confidence (HIGH/MEDIUM/LOW per Sentinel's confidence rules)
  - CWE / OWASP-2025 (or LLM Top 10 / MASVS) mapping
  - file:line range
  - Vuln class + one-line title
  - Engine concurrence tag (`[codex+agy+claude]` / `[codex+agy]` / `[claude-verified]`)
  - Exploit scenario
  - Remediation (inline OR pointer to LLM Fix Prompt block)
  - Receiving agent (Builder / Probe / Gear / Vigil / Triage / operator)
- **LLM Fix Prompt blocks** per `reference/fix-prompt-generation.md` — one per finding that isn't shipped inline
- **Rejection ledger** (condensed): counts by category — `hallucinated_sink`, `upstream_mitigated`, `framework_guaranteed`, `test_file_only`, `unreachable_dep`, `wrong_cwe_mapping`, `style_only`. Preserves SNR transparency without re-introducing noise.
- **AI-code section** (when AI-authored changes detected): summary of CWE-80/117/918/798 hits, slopsquat detector output, integration-point auth wiring check, Plausible Hallucination rejects.
- **Verdict**: `APPROVE` / `REQUEST CHANGES` / `BLOCK`. `BLOCK` is mandatory when any CRITICAL ships.

---

## 9. Subagent prompt skeleton (Sentinel)

```
You are the {engine} scan subagent for Sentinel.

# Role
Static security auditor. You are one of three engines scanning independently — do not
try to be exhaustive; surface what your training-data priors flag as highest-risk.
You will NOT modify code; this is detection-only.

# Target
Files: {file list or path glob}
Project context: {framework, runtime, brief threat model}
Focus axis: {full OWASP 2025 | secrets | injection | deps | headers | authn | authz | aisec | mobile}
AI-authored flag: {true|false} — if true, apply heightened scrutiny to CWE-80 (XSS),
CWE-117 (Log Injection), CWE-918 (SSRF), CWE-798 (hardcoded credentials), CWE-22
(path traversal), and verify every import resolves (Plausible Hallucination check).

# Output format
Return ONLY JSON matching this exact schema (no commentary outside the JSON):

{security-finding JSON schema — see §2 above}

# Constraints
- Do not paraphrase or invent file paths, function names, imports, CVE IDs, or
  package names. If you cite a sink, quote the actual line.
- Map every finding to a CWE and an OWASP-2025 / LLM-2025 / MASVS category.
- For ≥ HIGH severity, include a concrete exploit_scenario (attacker action →
  outcome). Theoretical bugs without an exploit path are MEDIUM at most.
- Do not flag style/hygiene unless explicitly requested.
- Open with the deliverable JSON (no completion preamble).
```

Engine-specific invocation matches the canonical `_common/MULTI_ENGINE_RECIPE.md` block — subscription auth only, default model, structured JSON output mandatory.

---

## 10. Cross-References

- `_common/MULTI_ENGINE_RECIPE.md` — canonical flow, PREFLIGHT, engine-attribution tags, degraded modes
- `_common/SUBAGENT.md` §MULTI_ENGINE — base engine dispatch mechanics
- `judge/reference/tri-engine-review.md` — canonical Pattern C implementation (Sentinel is the security specialization)
- `reference/vulnerability-patterns.md` — detection heuristics consulted during GROUND
- `reference/owasp-2025-checklist.md` — OWASP-2025 mapping used in NORMALIZE/SYNTHESIZE
- `reference/supply-chain-security.md` — registry probe checklist used in 5.1/5.2 for slopsquat/typosquat
- `reference/ai-code-security.md` — heightened-scrutiny axis used when AI-authored flag is set
- `reference/fix-prompt-generation.md` — verb selection (SECURE-FIX / HARDEN / MITIGATE / BREAKING-FIX / AUTH-FIX / REVOKE-AND-ROTATE / INVESTIGATE-FURTHER) for the LLM Fix Prompt block
