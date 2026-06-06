# Multi-Engine Mode (Sentinel)

Pattern type: **C — Concurrence-primary**. Different LLM engines carry non-overlapping CVE / CWE / framework-specific training-data priors. Concurrence collapses false positives; the 78% single-tool miss rate (Veracode 2026) is the cost of skipping fan-out on high-assurance scans.

## Base Engine Policy (2026-05)

Default baseline = **Claude + Codex (dual-engine, 2 spawns)**. agy adds a third axis (tri-engine, 3 spawns) when AVAILABLE at PREFLIGHT.

- Codex carries GitHub Security Advisory + npm/PyPI registry advisories prominently
- Antigravity (agy) carries Google's OSS-Vulnerability database + Wiz / Google-product CVE corpus prominently
- Claude carries Anthropic-curated security research + general OWASP/CWE training prominently

Dual-engine still covers GitHub Security Advisory + npm/PyPI (Codex) + Anthropic-curated + general OWASP/CWE (Claude). See `_common/MULTI_ENGINE_RECIPE.md §Base Engine Policy + §Engine Availability Modes`.

## Trigger

Activate when any of these hold:

- User invokes `multi` subcommand, or says `multi-engine`, `tri-engine`, `parallel SAST`, `cross-engine`, or `high-assurance` scan
- Nexus routes a security task with concurrence-required signal
- Target is AI-authored code (heightened scrutiny — single engine misses absent-defense patterns)
- Target touches auth, payments, PII, secret handling, or other security-critical surface
- A prior single-engine scan returned an ambiguous result and the user requests cross-validation

## Flow

`SCOPE → PREFLIGHT → FAN-OUT → NORMALIZE → CLUSTER → SCORE → GROUND → ARBITRATE → FILTER → REPORT` per `reference/tri-engine-scan.md`. PREFLIGHT runs in Sentinel main context only — never delegated to subagents, whose inherited PATH is narrower than the user's interactive shell.

## Loose prompt rule

Dispatch each engine with minimal context: role (one line), target code, axis focus, AI-authored flag, output JSON schema. Do NOT preload OWASP checklists, CWE catalogs, vulnerability-pattern references, or remediation snippets. The point of fan-out is to let each engine's training-data priors drive independent output; preloaded frameworks collapse that diversity. Frameworks apply at SYNTHESIZE.

## Plausible Hallucination check (Sentinel-strict)

For every CANDIDATE finding, read the cited sink with the Read tool and verify the cited code, import, function name, CVE ID, and package name actually exist. Engines hallucinate plausible-looking sinks at non-trivial rates; for dependency findings, also confirm the lockfile pins a version inside the affected range (NOT just `package.json`). For slopsquat/typosquat findings, query the registry's JSON API for existence, publish date, and download count before shipping.

## Concurrence + arbitration

- **Tri-engine** (Claude + Codex + agy): 3/3 `CONFIRMED` → ship after one-finding spot-check; 2/3 `LIKELY` → ship with light grounding (existence + not-mitigated); 1/3 `CANDIDATE` → MUST pass strict grounding, drop if rejected.
- **Dual-engine** (Claude + Codex, default baseline): 2/2 `CONFIRMED` → ship after one-finding spot-check; 1/2 `CANDIDATE` → MUST pass strict grounding, drop if rejected. `LIKELY` is structurally unreachable with 2 engines, so the bar for shipping a single-engine security finding is automatically higher than in tri-engine mode.
- **Severity arbitration overrides**: hardcoded secret → CRITICAL; CVSS≥9 reachable → CRITICAL; CVSS≥9 unreachable → MEDIUM; missing CSRF on session endpoint → HIGH; framework guarantee covers sink → drop two tiers or REJECT; AI-generated code + CWE-80/117/918/798 → boost one tier (per Veracode Spring 2026 failure rates).

## Filter aggressively

Every shipped finding must carry: VERIFIED/LIKELY/CONFIRMED status, severity ≥ MEDIUM (or explicitly requested LOW), concrete `remediation`, concrete `exploit_scenario` for ≥ HIGH, no upstream mitigation, no style-only content. Goal: zero noise from Sentinel reports.

## Degraded modes

- 1 engine missing → run other two, treat CANDIDATEs more strictly
- 2 engines missing → single-engine, all findings CANDIDATE, ground all
- All 3 fail → abort multi mode and fall back to default `scan` Recipe with reduced-confidence flag

## Required reading order before fan-out

1. `_common/MULTI_ENGINE_RECIPE.md` — cross-skill canonical flow
2. `reference/tri-engine-scan.md` — Sentinel JSON schema, CLUSTER identity rules, SCORE rubric, GROUND checks, SYNTHESIZE merge, subagent prompt skeleton
3. `_common/SUBAGENT.md` §MULTI_ENGINE — base engine dispatch mechanics
