# Cascade Analysis

**Purpose:** Detect second-order and emergent effects beyond direct dependency chains.
**Read when:** Cascade analysis is triggered (≥3 service boundaries, bidirectional deps, shared resources ≥3 components, or risk ≥7).

---

## Trigger Conditions

| Condition | Threshold | Rationale |
|-----------|-----------|-----------|
| Service boundary crossings | ≥ 3 | Cross-service changes amplify failure propagation |
| Bidirectional dependencies | Any detected | Feedback loops create non-linear risk |
| Shared resource consumers | ≥ 3 affected components | Resource contention risk increases combinatorially |
| Risk score | ≥ 7 (HIGH) | High-risk changes warrant deeper analysis |

---

## Effect Types and Detection

### 1. Feedback Loops

A affects B, B's response amplifies or dampens A.

**Detection:**
```
1. Build bidirectional dependency graph from VERTICAL analysis
2. Identify cycles: A → B → A (direct) or A → B → C → A (transitive)
3. Classify: amplifying (positive feedback) or dampening (negative feedback)
4. Assess stability: amplifying loops are higher risk
```

**Examples:**
- Cache invalidation triggers reload, reload triggers cache invalidation
- Retry storm: failure → retry → overload → more failures
- Auto-scaling: load increase → scale up → connection pool exhaustion → more load

### 2. Cascading Failures

Sequential failure propagation across boundaries.

**Detection:**
```
1. From VERTICAL L2+ results, identify cross-boundary dependencies
2. For each boundary crossing, assess: what happens if this dependency fails?
3. Map failure propagation paths: single failure → downstream failures
4. Check for circuit breakers, bulkheads, or isolation mechanisms
```

**Failure propagation patterns:**
- **Synchronous chain:** A calls B calls C — C failure blocks B blocks A
- **Resource exhaustion:** A failure causes B to retry, exhausting B's thread pool
- **Data corruption:** Invalid data from A propagates through B and C before detection
- **Configuration cascade:** Config change in A invalidates assumptions in B, C

### 3. Emergent Behavior

Combined changes produce unexpected system-level properties.

**Detection:**
```
1. From HORIZONTAL analysis, identify pattern interactions
2. Check: do two independently-valid changes conflict when combined?
3. Assess behavioral invariants that span multiple components
4. Look for implicit contracts (timing assumptions, ordering guarantees)
```

**Common patterns:**
- Two performance optimizations that individually help but together cause thundering herd
- Independent schema migrations that create inconsistent intermediate state
- Feature flags that interact unexpectedly when both enabled

### 4. Resource Contention

Multiple affected components compete for shared resources.

**Detection:**
```
1. Map shared resources: databases, caches, queues, connection pools, file locks
2. For each shared resource, count affected components from VERTICAL analysis
3. Assess current utilization (if available) and projected change
4. Flag resources where affected_components ≥ 3
```

**Shared resource categories:**
- Database connections / connection pools
- Cache (Redis, Memcached) — key space collisions, eviction pressure
- Message queues — consumer lag, partition rebalancing
- File system — lock contention, disk I/O
- External API rate limits — shared quota consumption

### 5. Temporal Cascades

Effects that manifest only under specific timing or ordering.

**Detection:**
```
1. Identify async dependencies in affected scope (event handlers, queues, cron jobs)
2. Check for ordering assumptions: "A always completes before B starts"
3. Assess migration/deployment ordering dependencies
4. Look for race windows created by the change
```

**Risk signals:**
- Eventually-consistent data read by strongly-consistent consumers
- Deployment ordering requirements between services
- Cron job timing assumptions invalidated by the change
- Event ordering guarantees broken by async refactoring

---

## Integration with L0-L3 Analysis

| Depth | Standard Analysis | + Cascade Analysis |
|-------|-------------------|--------------------|
| L0 | Changed file | Identify feedback loops within the file |
| L1 | Direct dependents | Check for bidirectional dependencies, shared resources |
| L2 | Transitive deps | Map cascading failure paths, emergent behavior risks |
| L3+ | Extended reach | Temporal cascades, cross-service failure propagation |

Cascade analysis extends each depth level with second-order effect detection, but does NOT replace the standard confidence degradation (L2 = medium, L3+ = lower confidence).

---

## Output Format: Cascade Risk Map

Append to the standard impact report:

```markdown
## Cascade Risk Map

### Feedback Loops Detected
| Loop | Type | Stability | Risk |
|------|------|-----------|------|
| [A → B → A] | Amplifying | Unstable | HIGH |

### Cascading Failure Paths
| Origin | Path | Boundary Crossings | Mitigation |
|--------|------|--------------------|------------|
| [Component] | [A → B → C] | [count] | [circuit breaker / bulkhead / none] |

### Emergent Behavior Risks
| Interaction | Components | Risk | Detection Difficulty |
|-------------|------------|------|---------------------|
| [description] | [A, B] | [HIGH/MED/LOW] | [HIGH/MED/LOW] |

### Resource Contention Points
| Resource | Affected Components | Current Utilization | Projected Risk |
|----------|--------------------|--------------------|---------------|
| [name] | [count] | [%] | [HIGH/MED/LOW] |

### Temporal Cascade Risks
| Assumption | Invalidated By | Impact | Mitigation |
|------------|---------------|--------|------------|
| [ordering assumption] | [change] | [description] | [recommendation] |
```

---

## Routing After Cascade Analysis

| Finding | Route To |
|---------|----------|
| Unstable feedback loop detected | Beacon (observability) + Sentinel (if security-relevant) |
| Cascading failure path without circuit breaker | Triage (playbook creation) + Builder (circuit breaker implementation) |
| Emergent behavior risk HIGH | Omen (pre-mortem analysis) + Magi (trade-off decision) |
| Resource contention ≥ 3 components | Bolt (performance optimization) |
| Temporal cascade risk | Specter (concurrency analysis) |
