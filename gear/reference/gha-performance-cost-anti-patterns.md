# Performance and Cost Anti-Patterns

Purpose: Triage slow or expensive GitHub Actions workflows by focusing on the highest-leverage CI performance and billing failures.

## Contents

- Performance anti-patterns
- Cost traps
- Cache failures
- Build optimization checks

## Performance Anti-Patterns

| ID | Anti-pattern | Signal | Fix |
|----|--------------|--------|-----|
| `PF-01` | No dependency caching | dependency install consumes `40-60%` of CI time | use built-in setup cache or `actions/cache` keyed by lockfile |
| `PF-02` | Cache key mismatch | stale or constantly missed cache | include lockfile hash and OS in cache keys |
| `PF-03` | Cache size explosion | repo cache reaches `10 GB` and churns | cache only what is needed and rotate prudently |
| `PF-04` | No Docker layer cache | container build takes `10-15 min` | enable Docker layer cache with GHA backend |
| `PF-05` | Sequential job graph | CI waits on every job in order | parallelize independent jobs with a diamond graph |
| `PF-06` | Full matrix on every push | dozens of jobs on every small change | keep push matrices small, expand on PR or nightly |
| `PF-07` | Large artifact upload | upload/download dominates runtime | trim artifacts and use short retention |

## Cost Traps

- default to Ubuntu unless platform-specific coverage is required
- Windows costs about `2x` Ubuntu
- macOS costs about `10x` Ubuntu
- ARM can reduce cost by about `37%` for compatible workloads
- concurrency without cancellation burns minutes on superseded PR runs
- schedules without change guards waste recurring minutes
- if your org uses the documented 2026 self-hosted runner platform-fee model, include that fee in runner-cost estimates

## Cache Failures

| ID | Anti-pattern | Signal | Fix |
|----|--------------|--------|-----|
| `CA-01` | No restore key | any lockfile change causes a full reinstall | add prefix-based `restore-keys` |
| `CA-02` | Cache without lockfile | cache invalidates on arbitrary code edits | key the cache from the lockfile, not source files |
| `CA-03` | Duplicate caching | same dependency tree cached twice | prefer built-in caches and add custom caches only for custom data |
| `CA-04` | Branch cache isolation ignorance | feature branches never hit the expected cache | understand default branch cache priming and branch scope behavior |

## Build Optimization Checks

- use affected-package routing in monorepos
- cache framework build outputs only after measuring value
- keep large artifacts rare and scoped
- shard tests only after timing data shows imbalance
- prefer shorter feedback loops on pushes and deeper coverage on PRs or scheduled runs
