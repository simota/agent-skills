# Resilience Patterns Reference

Purpose: Use this file for resilience-pattern verification, especially retry, timeout, circuit-breaker, bulkhead, and fallback behavior.

## Contents

- Pattern overview
- Circuit breaker parameters
- Retry strategies and decision matrix
- Bulkhead sizing
- Verification checklist

## Pattern Overview

| Pattern | Purpose | Failure type |
| --- | --- | --- |
| Circuit Breaker | stop calling a failing dependency | downstream failure |
| Retry | recover from transient issues | transient failure |
| Bulkhead | isolate failure domains | resource exhaustion |
| Timeout | bound wait time | slow response |
| Fallback | return degraded service | persistent failure |
| Rate Limiter | protect from overload | traffic spike |
| Shed Load | reject excess work | capacity exceeded |

## Circuit Breaker

### Parameters

| Parameter | Meaning | Typical value |
| --- | --- | --- |
| Failure threshold | failures required to open | `5` failures in `60s` |
| Success threshold | successes required to close | `3` consecutive |
| Recovery timeout | time spent OPEN | `30-60s` |
| Half-open limit | probes allowed in HALF-OPEN | `1-3` requests |

### Example

```python
class CircuitBreaker:
    def __init__(self, failure_threshold=5, recovery_timeout=30, success_threshold=3):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.success_threshold = success_threshold
        self.state = "CLOSED"
```

## Retry Patterns

### Strategies

| Strategy | Delay pattern | Use |
| --- | --- | --- |
| Immediate | `0ms` | rare network blip only |
| Fixed delay | `1s, 1s, 1s` | simple rate-limited APIs |
| Exponential backoff | `1s, 2s, 4s, 8s` | generic transient failure |
| Exponential + jitter | randomized exponential | high concurrency |
| Linear backoff | `1s, 2s, 3s` | gradual recovery |

### Decision Matrix

| Error type | Retry? | Strategy |
| --- | --- | --- |
| `4xx` | No, except `429` | none |
| `429` | Yes | respect `Retry-After` |
| `500` | Maybe `1-2` times | exponential backoff |
| `502/503/504` | Yes | exponential backoff + jitter |
| Connection timeout | Yes | exponential backoff |
| Connection refused | No | favor circuit breaker |
| DNS resolution | Yes once | short delay |

### Jitter Example

```python
import random
import time

def retry_with_backoff(func, max_retries=3, base_delay=1.0, max_delay=30.0):
    for attempt in range(max_retries + 1):
        try:
            return func()
        except RetryableError:
            if attempt == max_retries:
                raise
            delay = min(base_delay * (2 ** attempt), max_delay)
            time.sleep(delay * random.uniform(0.5, 1.5))
```

## Bulkhead

### Isolation Strategies

| Type | Mechanism | Granularity |
| --- | --- | --- |
| Thread pool | separate pool per dependency | per dependency |
| Semaphore | separate connection limit | per dependency |
| Process | separate process | per service |
| Pod | separate deployment | per workload |

### Sizing Formula

```text
Pool size = target_rps × p99_latency_seconds × safety_margin

Example:
100 RPS × 0.5s × 2 = 100
```

## Verification Checklist

```markdown
## Circuit Breaker Tests
- [ ] Opens after threshold
- [ ] Rejects while OPEN
- [ ] Moves to HALF-OPEN after timeout
- [ ] Closes after success threshold
- [ ] Re-opens on HALF-OPEN failure
- [ ] Exposes state metrics

## Retry Tests
- [ ] Retries only retryable errors
- [ ] Respects retry limit
- [ ] Applies backoff and jitter
- [ ] Total timeout bounds all retries

## Bulkhead Tests
- [ ] Limits concurrency per dependency
- [ ] Rejects excess work
- [ ] Failure in one bulkhead does not affect others
- [ ] Exposes active, queued, and rejected metrics

## Combined Pattern Tests
- [ ] Retry -> Circuit Breaker -> Fallback works
- [ ] Retries count toward breaker thresholds
- [ ] Fallback activates when circuit is OPEN
```
