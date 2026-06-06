# Scale Remediation Reference

Purpose: Execute incident-time capacity remediation for a service that is saturating or forecast to saturate. Scale is a reactive operational action — not a capacity plan, not a code fix. Every scale action is idempotent (check current state, apply only the delta), auditable, and rollback-ready.

## Scope Boundary

- **Mend `scale`**: reactive, incident-time horizontal / vertical capacity delta. HPA / KEDA tuning, pre-warm, drain-before-resize for stateful tiers.
- **Triage**: first-response diagnosis — *what* is saturating, *who* is affected, *which* signal (CPU / memory / RPS / queue depth / DB connections) is the leading indicator. Triage decides whether scale is the right move; Mend does the move.
- **Beacon**: preventive capacity planning, SLO design, headroom models, load forecasts. Beacon owns the *target* and *budget*; Mend burns capacity against that target during an incident.
- **Builder**: permanent code-level fix (N+1, memory leak, missing index, inefficient algorithm). Scale buys time; Builder removes the cause. Always open a Builder follow-up if the same scale action recurs.

Rule of thumb: if this is the second time you are scaling the same service for the same reason, you are masking a Builder problem.

## Direction Decision: Horizontal vs Vertical

| Signal | Prefer horizontal | Prefer vertical |
|--------|-------------------|-----------------|
| Stateless service, request-bound | Yes | No |
| CPU-bound per-request work | Yes | Sometimes |
| Memory-pressure per-instance (heap growth, ML model size) | No | Yes |
| Connection pool saturation (DB / upstream) | Careful — adds fan-out | Sometimes |
| Stateful (DB primary, cache shard, stateful queue) | Requires resharding → T3 | Requires failover / restart → T3 |
| Cold-start cost is high (JVM, large ML model) | Pre-warm required | Faster to vertical |

Default: horizontal for stateless workers / web / API. Vertical only when memory-bound or when fan-out would pressure a shared downstream.

## Workflow

```
PRE-CHECK      →  read current replicas / limits / HPA config
               →  read Triage diagnosis; confirm scale is the right remediation
               →  load current SLO burn rate and error-budget state from Beacon
               →  classify safety tier (T2 stateless / T3 stateful)
               →  for stateful: confirm connection-drain and stickiness plan

ACTION         →  stateless:    kubectl scale / HPA min-replicas bump / KEDA trigger adjust
               →  pre-warm:     warm N replicas before the forecast spike window
               →  stateful:     drain → quiesce → resize → rejoin (one node at a time)
               →  each step is idempotent (check current, apply delta only)

STAGED VERIFY  →  Health Check:  pods Ready, no CrashLoop, liveness/readiness green
               →  Smoke Test:   synthetic probe hits the new capacity path
               →  SLO Check:    fast-burn (>= 2% budget / 1h, 14.4x) settles;
                                error rate < 0.1% steady; p95 within SLO for 10m
               →  Recovery Confirmed: burn rate normalizes, no secondary alert

ROLLBACK       →  trigger if: crash loop on new replicas, connection-pool exhaustion
                  downstream, p95 regression > 2x post-scale, stateful rebalance stalls
               →  action:   revert replica count / instance size / HPA config to
                  previous values (recorded in PRE-CHECK)
               →  verify:   Health → Smoke re-run; log rollback to timeline
```

## HPA / KEDA Tuning Patterns

- **HPA min-replicas bump** (T2): fastest lever during an incident. Raise `minReplicas` to current steady-state + forecast delta; let `maxReplicas` stay generous. Do not lower `maxReplicas` during an incident.
- **HPA target utilization** (T2): drop CPU target from e.g. 70% → 50% to scale more aggressively. Expect faster scale-out but higher cost.
- **KEDA trigger tune** (T2): for queue-depth or event-lag scaling, lower the threshold (e.g. SQS depth 100 → 50) so replicas spin up earlier. Keep cooldown unchanged unless thrash is observed.
- **Scale-down lockout** (T2): during incident, suspend scale-down (HPA behavior `scaleDown.stabilizationWindowSeconds` high, or remove HPA temporarily) to prevent flap.

## Pre-Warm for Expected Load

When load is forecastable (flash sale, scheduled job, cohort rollout, regional time-of-day):
- Pre-warm = raise `minReplicas` *before* the window. Do not rely on HPA reactive path alone — cold-start latency + HPA polling delay compounds and breaks SLO at the spike edge.
- Pre-warm 15-30 min ahead for JVM / .NET. 1-5 min ahead for Go / Rust / small Node. For ML inference services with large model weights, pre-warm 30-60 min.
- Record the pre-warm end time; schedule scale-down only after burn rate confirms recovery.

## Stateful Service Gotchas

Stateful scaling is T3 (approval-gated). These are *not* stateless replica bumps.

- **Connection drain**: close accept listener, let in-flight requests finish, wait for pool drain before terminating the instance. Respect `terminationGracePeriodSeconds` and set it explicitly.
- **Session stickiness**: if sessions are sticky (sticky LB cookies, websocket connections, gRPC long-lived streams), scaling down evicts sessions. Coordinate with a feature flag or drain signal; do not just remove replicas.
- **DB read-replica scale-out**: adding a replica is T3; the replica must catch up via replication before taking traffic. Gate the LB weight until replication lag < threshold.
- **DB primary scale-up**: T3+, requires failover. Treat as a controlled maintenance — never during active incident unless the primary is the root cause. Prefer read-replica offload first.
- **Cache cluster resize** (Redis / Memcached sharded): T3. Resharding invalidates or migrates keys; coordinate with the service's cache-miss tolerance. Warm the new nodes before traffic shift.
- **Queue / stateful worker scale-down**: wait for in-flight message processing to complete; respect visibility timeout. Never terminate a worker mid-transaction.

## Predictive vs Reactive Autoscale

- **Reactive** (HPA / KEDA default): scale in response to observed signal. Lag = one polling interval + cold-start. Fine for gradual ramps; fails at sharp spikes.
- **Predictive** (pre-warm, scheduled min-replica bumps, forecast-driven KEDA): scale *before* observed signal, driven by calendar / forecast / upstream signal. Required when cold-start > tolerable SLO degradation window.
- Use predictive when: marketing sends a campaign, a nightly batch fans out, a cohort release rolls out, time-of-day pattern is known, upstream queue depth is climbing (leading signal).
- Use reactive when: traffic pattern is unforecastable and within cold-start tolerance.

## Anti-Patterns

- Scaling without reading current state first — a re-run can double replicas or fight HPA.
- Scaling horizontally when the bottleneck is a shared downstream (DB, cache, upstream API). Fan-out just moves the pressure.
- Raising `minReplicas` and forgetting to lower it after recovery — silent cost bleed; log a `#TODO(agent)` and a Beacon follow-up.
- Treating stateful scale as idempotent. Partial state (half-migrated shard, half-drained pool) is the default failure mode; always check state before retry.
- Scaling as a substitute for diagnosis. If Triage has not ruled out a bug, scale is a guess.
- Scaling past the downstream limit (DB `max_connections`, upstream rate limit). Verify downstream headroom in PRE-CHECK.
- Fighting the HPA during an incident — either let the HPA scale, or disable the HPA and scale manually; do not do both.

## Handoff

- **Triage ← Mend `scale`**: if the scale action does not stabilize within one verify cycle, return to Triage — the diagnosis was wrong.
- **Beacon ← Mend `scale`**: every successful scale action feeds a capacity-planning data point. If the incident repeats, Beacon owns the preventive sizing / headroom fix.
- **Builder ← Mend `scale`**: if the same scale is needed a second time for the same reason, hand off to Builder with the hotspot evidence (profiler sample, slow-query log, N+1 trace). Scale is masking a code fix.
- **Gear ← Mend `scale`**: if scale requires infra changes beyond the current cluster (new node pool, new region, IaC edit), route to Gear.
