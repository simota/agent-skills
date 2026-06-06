# Resilience & Cost Optimization

> Purpose: Read this when Rally needs explicit retry, fallback, degraded-mode, budget, or recovery policy.

## Table of Contents

1. Three-Layer Resilience
2. Agent-Specific States
3. Saga Compensation
4. Cost Management
5. Recovery Matrix

## Three-Layer Resilience

### Layer 1: Retry

| Strategy | Use when |
|----------|----------|
| Immediate retry | almost never |
| Fixed interval | recovery time is known |
| Exponential backoff | most retryable network calls |
| Exponential backoff + jitter | preferred default |

Hard rule: do not retry non-idempotent operations.

### Layer 2: Fallback

Fallbacks may switch to cached data, reduced functionality, or a simpler plan. The fallback must be simpler and more reliable than the primary path.

### Layer 3: Circuit Breaker

```text
Closed -> Open -> Half-Open
```

Recommended tuning:

| Parameter | Recommended value |
|-----------|-------------------|
| Failure threshold | `50%` errors over `10s` |
| Reset timeout | `30-60s` |
| Minimum request count | `5-10` |

## Agent-Specific States

| State | Rally behavior |
|-------|----------------|
| `Closed` | normal team execution |
| `Degraded` | smaller team, human approval for high-risk work |
| `Open` | stop team execution and fall back to a single session |

## Saga Compensation

Use compensation when the session fails mid-flight.

| Phase | Normal action | Compensation |
|-------|---------------|--------------|
| `SPAWN` | `TeamCreate + Task` | `shutdown_request + TeamDelete` |
| `ASSIGN` | `TaskCreate` | `TaskUpdate (deleted)` |
| `MONITOR` | `TaskList` supervision | replacement spawn or shutdown |
| `SYNTHESIZE` | merge results | escalate manual merge |

## Cost Management

### Model Tiering

| Complexity | Model | Rally use |
|------------|-------|-----------|
| Simple | `haiku` | extraction, lightweight investigation |
| Medium | `sonnet` | default implementation |
| Complex | `opus` | design or hard reasoning |

Model tiering is the highest-ROI cost lever.

### Team Budget

```text
Team Budget = max_teammates x estimated_cost_per_teammate x safety_margin
```

Reserve a `1.5x` safety margin.

### Budget Checkpoints

| Checkpoint | Action |
|------------|--------|
| start | set the budget ceiling |
| `50%` spent | compare progress to budget burn |
| `80%` spent | re-evaluate remaining work priority |
| `100%` spent | shut down and report remaining work |

### Additional Cost Levers

| Lever | Expected effect |
|-------|-----------------|
| Minimal team size | linear cost reduction |
| Context optimization | reduces repeated prompt cost |
| Early shutdown on stalls | avoids sunk-cost expansion |
| `shared_read` discipline | reduces duplicated context loading |

## Recovery Matrix

| Error type | First response | Second response | Third response | Last resort |
|------------|----------------|-----------------|----------------|-------------|
| Teammate hang | DM nudge | scope-reduced retry | replacement spawn | shutdown + report |
| Task failure | context-augmented retry | scope-reduced retry | skip + report | manual escalation |
| Ownership conflict | re-partition | sequentialize | interface separation | manual merge |
| All teammates fail | `TeamDelete` | single-session fallback | — | report alternatives |

### Work Stealing

Treat work stealing as optional future behavior, not the default. Rally currently uses central push-based assignment and should only revisit work stealing when HARMONIZE data justifies it.
