# Load Testing Guide

Purpose: Use this file for tool selection, workload design, SLO validation, CI integration, and report structure in `LOAD` mode.

## Contents

- Tool comparison
- k6, Locust, and Artillery starter patterns
- Ramp profiles and thresholds
- CI integration
- Load test report template

## Tool Comparison

| Tool | Language | Protocols | Best for | Tradeoff |
| --- | --- | --- | --- | --- |
| `k6` | JavaScript | HTTP, WS, gRPC | CI-friendly performance gates | More scripting than YAML tools |
| `Locust` | Python | HTTP, custom | custom user behavior and Python-heavy stacks | Lighter built-in reporting |
| `Artillery` | YAML/JS | HTTP, WS, Socket.io | quick API and traffic-shape tests | Less flexible than full-code harnesses |

## k6 Patterns

### Basic Load Test

```javascript
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '2m', target: 50 },
    { duration: '5m', target: 50 },
    { duration: '2m', target: 100 },
    { duration: '5m', target: 100 },
    { duration: '2m', target: 0 },
  ],
  thresholds: {
    http_req_duration: ['p(95)<500', 'p(99)<1000'],
    http_req_failed: ['rate<0.01'],
    checks: ['rate>0.99'],
  },
};

export default function () {
  const res = http.get('https://api.example.com/items');
  check(res, {
    'status is 200': (r) => r.status === 200,
    'response time < 500ms': (r) => r.timings.duration < 500,
  });
  sleep(1);
}
```

### SLO Validation

```javascript
export const options = {
  scenarios: {
    slo_validation: {
      executor: 'constant-arrival-rate',
      rate: 100,
      timeUnit: '1s',
      duration: '10m',
      preAllocatedVUs: 50,
      maxVUs: 200,
    },
  },
  thresholds: {
    http_req_failed: ['rate<0.001'],
    http_req_duration: ['p(99)<200'],
  },
};
```

## Ramp Profiles

| Profile | Pattern | Use when |
| --- | --- | --- |
| Linear ramp | gradual increase | general capacity validation |
| Step ramp | hold at each level | finding the breaking point |
| Spike | sudden jump | flash sales or thundering-herd simulation |
| Soak | long steady run | memory leaks or degradation over time |
| Stress | beyond expected peak | limit discovery and graceful-failure tests |

### Step Ramp

```javascript
export const options = {
  stages: [
    { duration: '5m', target: 100 },
    { duration: '5m', target: 100 },
    { duration: '5m', target: 200 },
    { duration: '5m', target: 200 },
    { duration: '5m', target: 400 },
    { duration: '5m', target: 400 },
    { duration: '5m', target: 0 },
  ],
};
```

## Alternative Tool Starters

### Locust

```python
from locust import HttpUser, task, between

class ApiUser(HttpUser):
    wait_time = between(1, 3)

    @task(3)
    def list_items(self):
        self.client.get("/api/items")

    @task(1)
    def create_item(self):
        self.client.post("/api/items", json={"name": "test-item", "price": 9.99})
```

### Artillery

```yaml
config:
  target: "https://api.example.com"
  phases:
    - duration: 120
      arrivalRate: 10
      name: "Warm up"
    - duration: 300
      arrivalRate: 50
      name: "Sustained load"
    - duration: 120
      arrivalRate: 100
      name: "Peak"
  ensure:
    p95: 500
    maxErrorRate: 1
```

## CI Integration

```yaml
load-test:
  runs-on: ubuntu-latest
  steps:
    - uses: grafana/k6-action@v0.3.1
      with:
        filename: tests/load/api-test.js
        flags: --out json=results.json
    - name: Check results
      run: |
        if jq -e '.root_group.checks.passes / .root_group.checks.total < 0.99' results.json; then
          echo "Load test failed: check pass rate below 99%"
          exit 1
        fi
```

## Required Guardrails

- Warm up for `5-10 min` before measuring.
- Report `p50/p95/p99/max`, error rate, and throughput.
- Run important tests at least `3` times.
- Add realistic think time such as `sleep(1-3s)` unless the scenario intentionally models machine traffic.
- Include unhappy-path traffic when the system must survive mixed conditions.

## Load Test Report Template

```markdown
## Load Test Report

### Test Parameters
- Duration: [X] minutes
- Warmup: [X] minutes
- Peak VUs: [N]
- Target RPS: [N]

### Results
| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| p95 latency | < 500ms | Xms | PASS/FAIL |
| p99 latency | < 1000ms | Xms | PASS/FAIL |
| Error rate | < 1% | X% | PASS/FAIL |
| Throughput | > 100 RPS | X RPS | PASS/FAIL |

### Bottlenecks Identified
1. [Description + evidence]

### Recommendations
1. [Action item]
```
