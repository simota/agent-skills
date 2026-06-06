# Circuit & Rate-Limit Remediation Reference

Purpose: Execute runtime interventions that contain a cascading failure or overload — trip a breaker, adjust a rate limit, shed load, isolate a bulkhead, or enable graceful degradation. These are operational state changes, not code changes. Every action is idempotent, auditable, and rollback-ready.

## Scope Boundary

- **Mend `circuit`**: runtime breaker / rate-limit / shed / bulkhead / degrade interventions during an incident.
- **Triage**: identifies *which* dependency is failing, *which* call path is cascading, and *what* the user-visible impact is. Triage decides that breaker is the right remediation; Mend trips it.
- **Builder**: permanent code-level fixes — retry policy, timeout, fallback response, hedged request, idempotency key. Circuit buys time; Builder lands the durable fix in a PR.
- **Beacon**: alert thresholds, SLO definitions, dependency-health dashboards. Beacon's dashboards are the evidence surface Mend reads.
- **Gear**: infra-level rate limits at the LB / API gateway / WAF. If the intervention requires IaC change, route to Gear.

Rule of thumb: if a dependency has failed twice this week and been contained by circuit twice, that's a Builder/Gear bet, not a Mend recurrence.

## Intervention Menu

| Intervention | Tier | Effect | Reversible |
|--------------|------|--------|-----------|
| Trip breaker open | T2 | Fail fast, stop hammering dep | Yes — close breaker |
| Tighten rate limit | T2 | Cap RPS into dep / from client | Yes — raise cap |
| Relax rate limit | T2 | Admit more traffic (post-recovery) | Yes — restore cap |
| Queue-based load shedding | T3 | Drop lowest-priority requests | Yes — re-enable intake |
| Bulkhead isolation | T2 | Partition pool / tenant / call-class | Yes — merge back |
| Graceful degradation | T3 | Serve stale cache / reduced feature | Yes — re-enable full path |

T3 applies when the intervention is visible to real users (shedding, degrading features). T2 is backend-only tuning.

## Workflow

```
PRE-CHECK      →  read Triage diagnosis: failing dep, error class, user impact
               →  read current breaker / rate-limit / bulkhead config
               →  read SLO burn rate (is this fast-burn >= 14.4x or slow?)
               →  classify tier: T2 internal-only vs T3 user-visible shed/degrade
               →  confirm fallback path exists (graceful degrade target is valid)

ACTION         →  trip breaker:   flip config flag / feature flag for dep-N
                                  → expect immediate error-fast for that call path
               →  tune rate:      update limiter config (per-route, per-client, per-tenant)
                                  → set new threshold; keep prior value for rollback
               →  shed:           enable priority-drop at intake (keep P0, drop P3)
               →  bulkhead:       separate connection pool / thread pool / tenant lane
               →  degrade:        switch handler to stale-cache / reduced-response mode
               →  each step is idempotent — re-running is a no-op if already in target state

STAGED VERIFY  →  Health Check:  dep error rate drops to ~0 (breaker open means calls
                                  short-circuit — look for CB state = OPEN, not 5xx)
               →  Smoke Test:   fallback path returns success;
                                priority P0 traffic still flows; degraded feature renders
               →  SLO Check:    user-facing SLO recovers (breaker is internal success);
                                fast-burn alert clears within 5-10 min
               →  Recovery Confirmed: no secondary cascade; upstream callers settle

ROLLBACK       →  trigger if: fallback path itself fails, P0 traffic starves,
                  degraded response breaks a contract (billing, auth, compliance),
                  dep recovers but breaker stays open past safe half-open window
               →  action:   close breaker → half-open → closed; restore rate-limit;
                  disable shed; merge bulkhead; re-enable full response
               →  verify:   Health → Smoke re-run; log rollback to timeline
```

## Breaker Tactics

- **Open immediately** (T2): when the dep is confirmed unhealthy (timeouts > threshold, error rate > 50%, connection reset storm). Opening early prevents pool exhaustion upstream.
- **Half-open probe** (T2): after cooldown, let 1-5% of traffic through. If success rate > 95% over N requests, close. Otherwise re-open.
- **Per-route / per-tenant breaker** (T2): scope the breaker narrowly when only one endpoint is failing. A global breaker kills healthy paths.
- **Never open a breaker on a critical path** (auth, payment, licensing) without a verified fallback. Route to T3 approval.

## Rate-Limit Tuning

- **Tighten at intake** (T2): drop the admission rate (e.g. 10k rps → 5k rps) to let the dep recover. Prefer per-client / per-tenant limits over global — avoids punishing healthy callers.
- **Queue with priority shedding** (T3): keep P0 traffic (checkout, auth), drop P3 (background sync, analytics). Requires a pre-existing priority classifier.
- **Token bucket vs leaky bucket**: token bucket for burst tolerance; leaky bucket for steady pacing. Don't swap algorithms during an incident — tune parameters only.
- **Relax after recovery**: step the limit back in increments (5k → 7k → 10k), verify each step holds for 5 min before the next. Full-send relax invites repeat saturation.

## Bulkhead Isolation

- **Connection-pool partition**: separate pools per downstream; one failing dep cannot exhaust the shared pool.
- **Tenant lane**: dedicated worker lane per major tenant so one noisy tenant cannot starve others. Useful when one tenant triggers the incident.
- **Call-class lane**: synchronous user requests in one lane, background / batch in another. Batch lane can be starved without user impact.

## Graceful Degradation Patterns

- **Stale cache serve**: return last-known-good with `X-Stale: true`. Verify TTL and staleness contract (minutes, not days).
- **Reduced response**: drop optional fields, disable recommendations, skip enrichment. Keep the contract compatible.
- **Read-only mode**: disable writes, keep reads. Common for DB primary incidents. T3 — user-visible, billing/audit impact.
- **Feature flag kill-switch**: flip off the non-critical feature that is cascading. Coordinate with product if user-visible.

## Anti-Patterns

- Tripping a breaker without a fallback. Fail-fast with no fallback is just faster 5xx.
- Tightening a global rate limit when one tenant is the abuser. Scope the intervention.
- Leaving the breaker open past the dep's recovery — false-positive outage.
- Shedding without priority classification — you drop the checkout and keep the health probe.
- Treating `degrade` as reversible by default — if it changes billing, audit, or compliance surface, it needs T3 approval both to enable and to disable.
- Stacking interventions (breaker + rate-limit + shed + degrade) simultaneously. You lose the ability to attribute recovery.

## Handoff

- **Triage ← Mend `circuit`**: if the intervention doesn't stabilize, diagnosis was wrong — the cascade origin is elsewhere.
- **Builder ← Mend `circuit`**: every successful circuit-trip is a Builder ticket — add a proper timeout / retry / fallback / hedged request in code so the breaker is a backup, not the primary defense.
- **Beacon ← Mend `circuit`**: post-incident, Beacon reviews whether dep-health SLO threshold fired in time and whether the breaker should be automated.
- **Gear ← Mend `circuit`**: if the rate-limit needs to live at LB / gateway / WAF layer, route to Gear for IaC change.
