# Resilience Anti-Patterns & SLO-Based Testing

Purpose: Use this file for resilience failure modes, error-budget policy, and SLO-based validation in `RESILIENCE` mode.

## Contents

- `AP-01` to `AP-07`
- Error budget rules
- SLO-based test strategy
- Recommended pattern chain
- Verification matrix

## Resilience Anti-Patterns

| ID | Anti-pattern | Symptom | Primary fix |
| --- | --- | --- | --- |
| `AP-01` | Retry Storm | traffic spikes `2-10x` during failure | cap retry budget to `10-20%`, add backoff and breaker |
| `AP-02` | Thundering Herd | recovered service fails again immediately | add jitter, stagger recovery, rate limit retries |
| `AP-03` | Timeout Cascade | slow downstream causes chain-wide slowdown | set upstream timeout > downstream timeout + work time |
| `AP-04` | Bulkhead Bypass | one dependency starves all callers | isolate pools and quotas per dependency |
| `AP-05` | Fallback Avalanche | fallback path also overloads the system | use independent resources and lightweight fallback |
| `AP-06` | Health Check Lie | readiness says healthy while service is unusable | use deep readiness checks |
| `AP-07` | Configuration Drift | staging passes, production fails | centralize resilience config and test it |

## Key Numeric Rules

- Retry budget: keep retry overhead within `10-20%` of normal traffic.
- Deep readiness examples:
  - DB pool active `< max × 80%`
  - Redis latency `< 100ms`
  - disk free `> 10%`
- Timeout cascade example:
  - bad: all services `30s`
  - better: upstream `10s` -> mid-tier `5s` -> downstream `2s`

## Error Budget Policy

```text
Error Budget = 1 - SLO

Example:
SLO 99.9% -> Error Budget 0.1%
1,000,000 monthly requests -> 1,000 errors allowed
43,200 minutes/month -> 43.2 minutes downtime allowed
```

### Budget Burn Actions

| Burn state | Action |
| --- | --- |
| `0-50%` consumed | keep normal release speed |
| `50-75%` consumed | incident review and performance investigation |
| `75-100%` consumed | slow releases and prioritize stability |
| `>100%` consumed | freeze releases and focus on reliability |

If one incident burns `>20%`, require a postmortem and `P0` action items.

## SLO-Based Test Strategy

| Test type | What it proves | Timing |
| --- | --- | --- |
| SLO validation | target RPS still meets SLO | pre-release gate |
| Error-budget stress | budget burn under high load | monthly or quarterly |
| Degradation test | graceful degradation during SLO violation | pre-release |
| Recovery test | MTTR after violation | Game Day |
| Budget burn rate | burn speed during fault scenarios | chaos experiment |

## SLI / SLO / SLA Stack

| Level | Meaning |
| --- | --- |
| `SLI` | measured metric |
| `SLO` | internal objective |
| `SLA` | external contractual commitment |

Siege validates `SLI -> SLO -> error-budget impact`.

## Recommended Pattern Chain

```text
Rate Limiter
-> Timeout
-> Retry + Backoff + Jitter
-> Circuit Breaker
-> Bulkhead
-> Fallback
```

### Combination Rules

1. Put retries inside the circuit-breaker boundary.
2. Count retries toward the circuit-breaker threshold.
3. Bound the total call time, not only each retry.
4. Isolate bulkheads per dependency.
5. Keep fallback as the outermost last-resort behavior.

## Verification Matrix

| Pattern | Normal | Temporary fault | Persistent fault | Recovery |
| --- | --- | --- | --- | --- |
| Retry | inactive | retries to success | stops at budget/limit | returns to normal |
| Circuit Breaker | CLOSED | stays CLOSED below threshold | OPEN -> HALF-OPEN | CLOSES after healthy probes |
| Bulkhead | normal pool usage | only affected pool degrades | affected pool rejects | pool recovers independently |
| Timeout | inside limit | fires between retries | falls back quickly | resumes normal latency |
| Fallback | inactive | usually inactive | serves degraded response | deactivates |

## Routing Notes

- Hand SLO and error-budget policy ownership to `Beacon`.
- Hand implementation gaps to `Builder`.
