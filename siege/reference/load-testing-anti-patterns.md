# Load Testing Anti-Patterns

Purpose: Use this file to prevent unrealistic load tests, select performance budgets, and integrate performance checks earlier in delivery.

## Contents

- `AP-01` to `AP-10`
- Azure performance anti-pattern mapping
- Shift-left performance workflow
- Performance budget examples

## Load Testing Anti-Patterns

| ID | Anti-pattern | Symptom | Fix |
| --- | --- | --- | --- |
| `AP-01` | Happy Path Only | only success cases, no degraded traffic | include `20-30%` 4xx/5xx/timeout/error scenarios |
| `AP-02` | Unrealistic Data | test data does not match production distributions | use sanitized production-like data |
| `AP-03` | Single Endpoint Focus | one endpoint looks fine, whole journey still fails | model end-to-end user flows |
| `AP-04` | Missing Think Time | artificial overload from zero pacing | add realistic `sleep(1-3s)` pacing |
| `AP-05` | Flat Load Profile | no insight into scale transitions or spikes | combine ramp, spike, soak, and stress patterns |
| `AP-06` | Testing in Isolation | staging numbers do not predict production | use production-like environments or document scaling corrections |
| `AP-07` | Shared Test Environment | noisy results from parallel teams | reserve isolated capacity or compare against a baseline |
| `AP-08` | No Warmup Phase | cold caches and JIT distort results | warm up for `5-10 min` before measurements |
| `AP-09` | Average-Only Metrics | tails and outliers are hidden | always report `p50/p95/p99/max` and histograms |
| `AP-10` | One-Shot Testing | flaky or non-reproducible conclusions | run at least `3` times and compare variance |

## Azure-Style Performance Anti-Patterns

| Pattern | Why it matters to Siege | Detection hint |
| --- | --- | --- |
| Busy Database | backend is saturated before app code is | DB CPU, long queries, lock wait |
| Busy Front End | browser or edge becomes the bottleneck | main-thread and CPU profile |
| Chatty I/O | too many small calls dominate latency | request count vs latency |
| Extraneous Fetching | payload size is larger than user value | response size vs data used |
| Improper Instantiation | repeated object creation adds GC pressure | allocation and GC frequency |
| Monolithic Persistence | one datastore cannot fit all access patterns | read/write pattern mismatch |
| No Caching | identical expensive work repeats | duplicate query analysis |
| Noisy Neighbor | one tenant distorts another | per-tenant resource dashboards |
| Retry Storm | errors amplify load | retry rate vs backend saturation |
| Synchronous I/O | threads block on remote work | thread-pool starvation and latency growth |

## Shift-Left Performance

| Delivery stage | What Siege should recommend |
| --- | --- |
| Design | define performance budgets and capacity assumptions |
| Development | micro-benchmarks, N+1 checks, component-level hotspots |
| CI | threshold-based regression checks for impacted paths |
| Pre-release | production-like scenario replay and SLO validation |

## Example Performance Budgets

| Resource | Budget example | Measurement |
| --- | --- | --- |
| API latency | `p95 < 200ms`, `p99 < 500ms` | k6 thresholds |
| Page load | `LCP < 2.5s`, `FID < 100ms` | Lighthouse CI |
| Bundle size | JS `< 200KB gzip` | bundle-size tools |
| DB activity | `<= 5` queries/request | ORM query counter |
| Memory | `<= 512MB / pod` | metrics and alerts |

## Routing Notes

- Hand performance bottlenecks and budget overruns to `Bolt`.
- Keep Siege focused on validation, evidence, and reproducibility.
