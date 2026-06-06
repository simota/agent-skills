# Smoke Test Deployment Gates Reference

Purpose: Use this file to design smoke / sanity suites that serve as the minimum viable deployment gate in Siege's `smoke` subcommand. A smoke suite answers a single binary question — "is this deployment obviously broken?" — within a tight time budget (≤3 min target). It is the narrowest check in the canary → smoke → regression hierarchy, and its value is speed and stability, not coverage.

## Scope Boundary

- **Siege `smoke`**: minimum-signal health suite for post-deploy verification, synthetic-check design, canary gate, and rollback trigger. Optimized for time-budget and flakiness tolerance.
- **Radar (elsewhere)**: unit-test authoring, edge-case coverage, flaky-test repair on the full suite. If the ask is "improve unit coverage," route to Radar.
- **Voyager (elsewhere)**: full E2E user journeys with Playwright/Cypress/WebdriverIO. Smoke is a tiny subset of E2E shaped for deploy gates, not a substitute for E2E coverage.
- **Attest (elsewhere)**: spec and AC compliance verification. Smoke checks only that deployment signal is green, not that every AC passes.
- **Beacon (elsewhere)**: SLO/SLI definitions, long-term observability, synthetic monitoring strategy. Smoke tests consume Beacon's SLOs and health signals but do not own them.
- **Mint (elsewhere)**: test-data factories. Smoke tests should use pre-baked, deterministic data — never generate data at smoke time.

If the ask is "deploy gate / post-deploy verification in <3 min" → `smoke`. If it is "validate the full checkout journey" → Voyager. If it is "ensure SLOs hold over a week" → Beacon.

## Test Hierarchy

| Layer | Runtime | When | Signal |
|-------|---------|------|--------|
| Canary | seconds | pre-deploy, on a single pod/region/user cohort | traffic-level regression |
| Smoke | ≤3 min | immediately post-deploy, every environment | deployment is not obviously broken |
| Regression | 10-60 min | pre-merge or nightly | feature-level correctness |
| Full E2E | 30 min - hours | nightly or release | full user-journey correctness |
| Load / Chaos | hours | scheduled | non-functional + resilience |

Rules:
- Each layer has a **distinct purpose**. Smoke is not "tiny E2E"; it is a binary up/down signal.
- If a smoke test failure cannot trigger rollback, it does not belong in the smoke suite.

## The Minimum Viable Signal Set

A smoke suite should cover only what, if broken, would make rollback clearly justified. Pick from:

| Signal | Example check | Why |
|--------|---------------|-----|
| Liveness | `GET /health` returns 200 | Process is running |
| Readiness | `GET /ready` returns 200 with DB + cache probes | Dependencies are reachable |
| Version | deployed SHA matches build artifact | Correct build landed |
| Auth | login flow returns valid session token | Auth path is not broken |
| Core write | create one canonical resource and delete it | DB write path works |
| Core read | fetch a known seed record | DB read path works |
| Critical third-party | stubbed or cached ping to payment / identity provider | External dep is reachable |
| Static asset | one JS bundle and one image return 200 | CDN / edge is healthy |

Cap the suite at **8-15 checks**. More than that and you are running regression, not smoke.

## Time Budget Discipline

Target: **≤3 min end-to-end**. If the suite exceeds budget, prune — do not parallelize your way out of a design problem.

| Check pattern | Wall-clock cost | Notes |
|---------------|-----------------|-------|
| Sequential HTTP health calls | ~50 ms each | Fine for liveness/readiness |
| Browser-based login check | 5-20 s | Use only if auth path must be exercised end-to-end |
| Full checkout journey | 30-120 s | Belongs in Voyager, not smoke |
| DB round-trip write+read | 100-500 ms | OK for core-write signal |
| Waits / polls for async | variable | Replace with direct status query; never `sleep(N)` |

Run smoke **serial** unless there is a concrete reason to parallelize. Parallel smoke hides ordering bugs and increases flakiness.

## Post-Deploy Verification Workflow

```
DEFINE    →  rollback-worthy signals only (8-15 checks)
          →  per-check success criteria + timeout (assert explicit, not "eventually")
          →  environment scope (staging / prod-canary / prod-full)

PREPARE   →  pre-bake test data (seeded accounts, fixed product IDs)
          →  wire smoke credentials (read-only where possible, rotated per env)
          →  store known-good baseline response shape (JSON schema / version string)

EXECUTE   →  run serial by default, ≤3 min total
          →  collect per-check latency, not just pass/fail
          →  emit structured log (envelope with deploy SHA, env, start/end, verdict)

ANALYZE   →  on fail: classify as infra / regression / test-bug within minutes
          →  track flake rate per check; any check >1% flake goes to quarantine

REPORT    →  verdict: PROMOTE / HOLD / ROLLBACK
          →  deploy SHA + env + failed check list + runtime
          →  handoff: Triage for rollback, Builder for bug, Radar for test-fix
```

## Synthetic Check Design

Smoke checks that run **continuously** post-deploy (every N minutes from outside the cluster) become synthetic monitors. Rules:

- Probe from the same perspective as real users (geographic region, TLS stack, DNS resolver).
- Use a dedicated **synthetic user account** — never a real user, never a shared test account.
- Alert on **3 consecutive failures**, not 1 — single-failure alerting flood is worse than slight detection lag.
- Tag every probe with the deploy SHA so synthetic failure maps cleanly to "this deploy broke X."
- Expire and rotate synthetic credentials; treat them as real secrets.

## Flakiness Tolerance

Smoke flakes are deployment-blocker false alarms. Tolerance:

| Flake rate | Action |
|------------|--------|
| 0-0.5% | Acceptable — keep monitoring |
| 0.5-1% | Investigate before next sprint |
| >1% | Quarantine or delete the check — it is no longer a reliable gate |
| >5% | Engineering is ignoring the gate; rebuild the check from scratch |

**Never retry a failing smoke check silently to mask flake.** Either the check is deterministic (keep it strict) or it is flaky (remove or rewrite it). Silent retry turns smoke into noise.

## Anti-Patterns

- Smoke suite that takes 10 min — by the time it fails, rollback window has closed.
- Smoke checks writing real user data to production — create and delete the same canonical row, never leave residue.
- Smoke reusing the regression test suite with a subset tag — regression is for correctness; smoke is for "obviously broken." They need different assertions.
- Smoke asserting exact response JSON bodies — changes in non-breaking fields create false rollbacks. Assert on status code + a few stable fields only.
- Sleeping or polling for async completion inside smoke — replace with status endpoint or skip the check entirely.
- Testing multiple features per smoke check — one check, one signal. When it fails, the cause must be obvious.
- Treating smoke as a coverage metric ("smoke covers 40% of code") — smoke is a gate, not coverage.
- Running smoke only in staging — production deploys need their own smoke run against the production endpoint.
- Hardcoded production credentials in smoke scripts — rotate via secret manager; read-only scope where possible.
- Silent retry loops (`retry: 3` with no logging) — if a check needs retry, log every attempt and surface flake rate.

## Handoff

**To Triage:**
- Failed smoke verdict with deploy SHA + failed check list — Triage decides rollback vs roll-forward.
- Repeated smoke flake patterns that indicate infra degradation, not code regression.

**To Builder:**
- Genuine regressions smoke caught — minimized reproducer, failed check output, suspected module.

**To Radar:**
- Smoke flakes traced to test brittleness — Radar repairs the check.
- Signals missing from smoke that a past incident exposed — Radar adds the regression test at the right level (unit / E2E / smoke).

**To Beacon:**
- Synthetic-check frequency, alert thresholds, and multi-region probe topology proposals.
- Smoke SLO ("95% of deploys pass smoke on first try") as a release-health metric.

**To Voyager:**
- Journey-level coverage that was attempted in smoke but belongs in full E2E.

**Escape hatches / follow-ups:**
- `#TODO(agent): quarantine flaky check` when flake rate exceeds 1%.
- `#TODO(agent): prune smoke suite` when runtime exceeds 3 min budget.
- `#TODO(agent): add synthetic monitor` when a smoke check would also be useful as a continuous probe.
