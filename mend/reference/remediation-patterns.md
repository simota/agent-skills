# Remediation Pattern Catalog

Purpose: Read this file when matching incident symptoms to a known pattern, checking confidence modifiers, or selecting a catalog-backed remediation and verification path.

## Contents

- Infrastructure patterns
- Application patterns
- Configuration patterns
- Deployment patterns
- Pattern matching protocol

Known failure patterns organized by category. Each pattern includes symptoms, root cause, safety tier, and remediation steps.

---

## Category: Infrastructure (INFRA)

### INFRA-001: Pod CrashLoopBackOff

| Field | Value |
|-------|-------|
| **Symptoms** | Pod status CrashLoopBackOff, repeated restart count > 3, OOMKilled or Error exit codes |
| **Root Cause** | Memory limit exceeded, missing config/secret, application startup failure |
| **Safety Tier** | T1 (restart) / T2 (resource adjustment) |
| **Confidence Factors** | +20% if OOMKilled in events, +15% if recent deploy, -20% if no recent changes |

**Remediation Steps:**
1. Check pod events for OOMKilled → If yes: increase memory limit (T2)
2. Check for missing ConfigMap/Secret → If yes: verify and recreate (T2)
3. Check application logs for startup error → If known error: apply known fix
4. If none of above: restart pod with increased resource limits (T2)

**Verification:** Pod running stable for > 60s, no restart within 5 min

---

### INFRA-002: Node Resource Exhaustion

| Field | Value |
|-------|-------|
| **Symptoms** | Node CPU/Memory > 90%, pod evictions, scheduling failures |
| **Root Cause** | Insufficient node capacity, resource leak, unexpected traffic spike |
| **Safety Tier** | T2 (scale-out) |
| **Confidence Factors** | +25% if gradual increase, +15% if correlated with traffic, -10% if sudden spike |

**Remediation Steps:**
1. Identify top resource consumers → Check for resource leaks
2. If leak detected: restart leaking pods (T1)
3. If capacity issue: trigger horizontal pod autoscaler or node scale-out (T2)
4. If traffic spike: activate rate limiting (T2)

**Verification:** Node utilization < 80%, no pending pods, no evictions

---

### INFRA-003: Disk Pressure

| Field | Value |
|-------|-------|
| **Symptoms** | Disk usage > 85%, DiskPressure node condition, log write failures |
| **Root Cause** | Log accumulation, temp file buildup, large artifacts |
| **Safety Tier** | T1 (cleanup) / T2 (if data volumes) |
| **Confidence Factors** | +30% if /var/log large, +20% if /tmp large, -15% if data volume |

**Remediation Steps:**
1. Identify largest directories consuming disk
2. If logs: trigger log rotation (T1)
3. If temp files: clean temp directories (T1)
4. If data volume: alert and escalate (T3 — data sensitivity)

**Verification:** Disk usage < 80%, DiskPressure condition cleared

---

### INFRA-004: DNS Resolution Failure

| Field | Value |
|-------|-------|
| **Symptoms** | DNS lookup timeouts, NXDOMAIN errors for internal services, intermittent connection failures |
| **Root Cause** | CoreDNS pod issue, DNS cache corruption, network policy blocking |
| **Safety Tier** | T1 (restart CoreDNS) / T3 (DNS config change) |
| **Confidence Factors** | +25% if CoreDNS pod unhealthy, +15% if recent network policy change |

**Remediation Steps:**
1. Check CoreDNS pod health → If unhealthy: restart CoreDNS pods (T1)
2. If healthy: flush DNS cache (T1)
3. If persists: check network policies for DNS port blocking (T3)

**Verification:** DNS resolution succeeds for all internal services within 2s

---

## Category: Application (APP)

### APP-001: Connection Pool Exhaustion

| Field | Value |
|-------|-------|
| **Symptoms** | Connection timeout errors, "no available connections" in logs, increasing response latency |
| **Root Cause** | Connection leak, pool size too small, downstream service slow |
| **Safety Tier** | T1 (pool reset) / T2 (pool size adjustment) |
| **Confidence Factors** | +30% if active connections = max, +20% if downstream latency high |

**Remediation Steps:**
1. Check connection pool metrics (active vs max)
2. If pool exhausted: reset connection pool (T1)
3. If downstream slow: activate circuit breaker (T2)
4. If pool too small for load: increase pool size (T2)

**Verification:** Connection pool utilization < 70%, response latency normalized

---

### APP-002: Memory Leak (Gradual)

| Field | Value |
|-------|-------|
| **Symptoms** | Steadily increasing memory usage over hours/days, no corresponding traffic increase |
| **Root Cause** | Application memory leak (event listeners, cache unbounded, connection leak) |
| **Safety Tier** | T1 (rolling restart) |
| **Confidence Factors** | +30% if linear memory growth, +20% if heap dump shows growth, -15% if traffic correlated |

**Remediation Steps:**
1. Confirm gradual memory increase pattern (not traffic-correlated)
2. Execute rolling restart of affected service pods (T1)
3. Monitor memory pattern post-restart
4. If pattern returns quickly: escalate to Builder for code fix

**Verification:** Memory usage returns to baseline, stable for 10 min

---

### APP-003: Upstream Service Timeout

| Field | Value |
|-------|-------|
| **Symptoms** | Timeout errors to specific upstream, cascading latency, thread pool saturation |
| **Root Cause** | Upstream service degraded, network issue, timeout too aggressive |
| **Safety Tier** | T2 (circuit breaker / timeout adjustment) |
| **Confidence Factors** | +25% if upstream health check failing, +20% if network metrics degraded |

**Remediation Steps:**
1. Verify upstream service health status
2. If upstream down: activate circuit breaker for affected route (T2)
3. If upstream slow: increase timeout temporarily (T2)
4. If own service saturated: scale out to absorb retry load (T2)

**Verification:** Error rate returned to baseline, no cascading timeouts

---

## Category: Configuration (CONFIG)

### CONFIG-001: Feature Flag Misconfiguration

| Field | Value |
|-------|-------|
| **Symptoms** | Feature behavior unexpected after flag change, error spike correlated with flag toggle |
| **Root Cause** | Incorrect flag state, flag dependency conflict, stale cache |
| **Safety Tier** | T2 (flag toggle) |
| **Confidence Factors** | +35% if error spike within 5 min of flag change, +20% if flag recently modified |

**Remediation Steps:**
1. Identify recently changed feature flags (last 1 hour)
2. Correlate error spike timing with flag change
3. Revert flag to previous state (T2)
4. Clear feature flag cache across services (T1)

**Verification:** Error rate matches pre-flag-change baseline

---

### CONFIG-002: Resource Limit Misconfiguration

| Field | Value |
|-------|-------|
| **Symptoms** | OOMKill events, CPU throttling, pods stuck in Pending |
| **Root Cause** | Resource requests/limits too low for workload |
| **Safety Tier** | T2 (resource adjustment) |
| **Confidence Factors** | +30% if OOMKill matches limit, +25% if CPU throttle percentage high |

**Remediation Steps:**
1. Compare current resource usage to configured limits
2. Calculate appropriate limits (current peak × 1.5 for memory, × 1.3 for CPU)
3. Apply updated resource limits (T2)
4. Monitor for scheduling issues after adjustment

**Verification:** No OOMKill events, CPU throttle < 5%, pods running stable

---

### CONFIG-003: TLS/Certificate Expiry

| Field | Value |
|-------|-------|
| **Symptoms** | TLS handshake failures, certificate expiry warnings, HTTPS connection refused |
| **Root Cause** | Certificate expired or about to expire |
| **Safety Tier** | T3 (certificate rotation) |
| **Confidence Factors** | +40% if cert expiry date passed, +30% if expiry within 24h |

**Remediation Steps:**
1. Identify expired/expiring certificates
2. If auto-renewal configured: trigger renewal (T2)
3. If manual: request approval for certificate rotation (T3)
4. Verify new certificate propagation across all endpoints

**Verification:** TLS handshake succeeds, certificate valid for > 30 days

---

## Category: Deployment (DEPLOY)

### DEPLOY-001: Failed Deployment Rollback

| Field | Value |
|-------|-------|
| **Symptoms** | Error rate spike immediately after deploy, new error types in logs, health check failures |
| **Root Cause** | Bug in new deployment, missing dependency, incompatible configuration |
| **Safety Tier** | T2 (rollback to last-known-good) |
| **Confidence Factors** | +35% if error spike within 10 min of deploy, +25% if new error types, +15% if health check failing |

**Remediation Steps:**
1. Confirm error correlation with deployment timing
2. Identify last-known-good version
3. Execute rollback to previous version (T2)
4. Notify team of rollback with error details

**Verification:** Error rate matches pre-deploy baseline, all health checks passing

---

### DEPLOY-002: Canary Failure

| Field | Value |
|-------|-------|
| **Symptoms** | Canary instances showing higher error rate than stable, latency deviation > 20% |
| **Root Cause** | New version has regression |
| **Safety Tier** | T1 (canary abort) / T2 (full rollback if promoted) |
| **Confidence Factors** | +30% if error rate canary > 2× stable, +25% if latency deviation > 20% |

**Remediation Steps:**
1. Compare canary metrics vs stable (error rate, latency, resource usage)
2. If canary only: abort canary deployment (T1)
3. If already promoted: execute full rollback (T2)
4. Capture canary metrics for Builder debugging

**Verification:** All instances running stable version, metrics normalized

---

### DEPLOY-003: Configuration Drift

| Field | Value |
|-------|-------|
| **Symptoms** | Inconsistent behavior across replicas, partial failures, some pods healthy while others fail |
| **Root Cause** | ConfigMap/Secret not propagated to all pods, stale config cache |
| **Safety Tier** | T1 (rolling restart) / T2 (config sync) |
| **Confidence Factors** | +25% if pod configs differ, +20% if recent configmap change |

**Remediation Steps:**
1. Compare configuration across all replicas
2. If config mismatch: trigger rolling restart for affected pods (T1)
3. If cache issue: invalidate config caches (T1)
4. If persistent: force config sync and rolling restart (T2)

**Verification:** All replicas reporting identical config version, consistent behavior

---

## Pattern Matching Protocol

### Confidence Calculation

```
Base confidence = number of matching symptoms / total pattern symptoms × 100
Adjusted confidence = Base + Σ(confidence factors that apply)
Time decay = -5% × floor(days_since_last_successful_match / 30)
Final confidence = min(max(Adjusted + Time decay, 0), 100)
```

### Confidence Decay

Patterns that haven't been matched recently lose confidence over time to prevent stale remediation:

| Days Since Last Match | Decay | Effect |
|-----------------------|-------|--------|
| 0-29 | 0% | Full confidence |
| 30-59 | -5% | Minor reduction |
| 60-89 | -10% | Noticeable reduction |
| 90+ | Triggers review | Pattern health check required (see learning-loop.md) |

**Rationale:** Infrastructure evolves continuously. A pattern that hasn't matched in 90+ days may target components that no longer exist or behave differently. Decay ensures stale patterns are reviewed before blind application.

### Match Thresholds

| Confidence | Classification | Action |
|------------|---------------|--------|
| ≥ 90% | High confidence | Auto-execute (if T1/T2) |
| 70-89% | Medium confidence | Notify + execute |
| 50-69% | Low confidence | Request approval |
| < 50% | No match | Escalate to Builder |

### Multi-Pattern Scenarios

When multiple patterns match:
1. Rank by confidence score (highest first)
2. Check for pattern dependencies (e.g., INFRA-001 may cause APP-001)
3. Address root cause pattern first
4. If equal confidence: address highest safety tier first (safer = first)

---

## 2026 Pattern Extensions

The catalog above covers durable production incidents. The patterns below were added in 2026 as workload shapes shifted toward LLM-backed services, edge-resident compute, and AI-assisted investigation.

### INFRA-005: LLM Provider Rate-Limit / Quota Breach

| Field | Value |
|-------|-------|
| **Symptoms** | `429` / `529` from the model provider, p95 latency spikes only on LLM-call paths, retry-storm warnings in logs |
| **Root Cause** | Tenant quota exceeded, regional capacity throttle, prompt-cache hit-rate collapse from a deploy that invalidated the cache prefix |
| **Safety Tier** | T1 (failover to cheaper model) / T2 (route to fallback provider) |
| **Confidence Factors** | +`30%` if provider status page reports throttling, +`20%` if cache hit-rate dropped >`30%` within `30` min, -`15%` if isolated to a single tenant |

**Remediation Steps:**
1. Check provider status + per-tenant quota dashboard.
2. If quota: route low-priority traffic to a smaller model (`opus` → `sonnet`, `sonnet` → `haiku`) via the gateway flag (T1).
3. If regional throttle: failover to the configured secondary provider (T2); update gateway routing.
4. If cache-hit collapse: restore prefix prompt to the version pre-deploy, then bring the new prefix back gradually (T2).

**Verification:** LLM error rate < `1%`, p95 latency back within `1.2x` baseline, prompt-cache hit-rate within `10%` of baseline.

### APP-004: Retrieval / Vector-Index Stale or Corrupted

| Field | Value |
|-------|-------|
| **Symptoms** | RAG answer-faithfulness drops (eval harness alerts), `Recall@5` < threshold, missing-citation count spikes |
| **Root Cause** | Index rebuild failed mid-write, embedding model version drift, corpus update did not propagate to all replicas |
| **Safety Tier** | T2 (reindex from last-known-good) / T3 (model version pin) |
| **Confidence Factors** | +`30%` if `Recall@5` dropped > `20%` within an hour of a corpus job, +`20%` if embedding model version mismatch between read/write paths |

**Remediation Steps:**
1. Snapshot current index for forensics (T1).
2. Pin embedding model to last-known-good version across read + write paths (T2).
3. Trigger reindex from the latest validated corpus snapshot (T2).
4. Hold canary on the new model version until eval harness re-passes (T2 — see `canary-remediation.md`).

**Verification:** `Recall@5 ≥ 0.8`, `Faithfulness ≥ 0.8`, no missing-citation regressions for `30` min.

### DEPLOY-004: Edge Worker Cold-Start Storm

| Field | Value |
|-------|-------|
| **Symptoms** | Edge runtime p95 spikes at the top of every minute, increase in `522` / `523` from CDN, cache-miss rate jumps |
| **Root Cause** | New worker version invalidated the V8 isolate pool, regional rollout pushed all workers cold at once |
| **Safety Tier** | T2 (traffic-shift partial rollback) |
| **Confidence Factors** | +`30%` if cold-start counter correlates with deploy timestamp, +`20%` if isolate count dropped to zero before recovering |

**Remediation Steps:**
1. Confirm cold-start counter spike vs deploy timestamp.
2. Shift traffic back to the prior worker version regionally (T2 — see `canary-remediation.md`).
3. Re-deploy with `0.5%` → `5%` → `25%` cohort ramp instead of a flat regional push (T2).

**Verification:** Edge p95 within `1.2x` baseline, `522` / `523` rate back to baseline.

### PROCESS-001: AI Investigation Handoff Incomplete

| Field | Value |
|-------|-------|
| **Symptoms** | An autonomous investigation agent (Bits AI SRE, Azure SRE Agent, Wiz Green Agent) requested a remediation but the handoff omitted required fields |
| **Root Cause** | Investigation agent did not classify the proposed action against the safety tier, or omitted the failing signal / cohort / candidate root cause |
| **Safety Tier** | n/a — this is a **gate**, not a remediation |
| **Confidence Factors** | n/a |

**Remediation Steps:**
1. Reject the handoff. Do not act.
2. Reply with the missing fields explicitly (`safety_tier`, `failing_signal`, `cohort`, `candidate_root_cause_with_confidence`).
3. Log the rejection so Lore can pattern-match repeated incompleteness from the same investigation source.

**Verification:** Subsequent handoff carries all four required fields. See `safety-model.md` § "Autonomous Investigation, Governed Remediation".
