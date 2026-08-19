# Performance and Caching

Purpose: Reduce CI latency and cost through cache design, efficient job graphs, bounded matrices, and disciplined artifact handling.

## Contents

- Cache strategy
- Job graph design
- Matrix strategy
- Artifacts and concurrency
- Runner cost
- Optimization checklist

## Cache Strategy

| Technique | Use it when | Key rules |
|-----------|-------------|-----------|
| built-in `setup-*` cache | language ecosystem supports it | prefer this first because it is simpler and less error-prone |
| `actions/cache` | you need custom paths or multiple cache layers | include OS and lockfile hash in the key |
| Docker layer cache | image builds dominate runtime | use `docker/build-push-action` with `type=gha` cache |
| framework cache | `.next/cache`, Turbo, Nx, uv, Go build cache | cache only the minimum useful directories |

Repository cache facts:

- total cache budget is `10 GB` per repository
- entries not accessed for `7 days` are evicted
- use restore keys for fallback

Good pattern:

```yaml
- uses: actions/cache@<full-sha>   # v4.x
  with:
    path: ~/.pnpm-store
    key: pnpm-${{ runner.os }}-${{ runner.arch }}-${{ hashFiles('**/pnpm-lock.yaml') }}
    restore-keys: |
      pnpm-${{ runner.os }}-${{ runner.arch }}-
```

Backend migration (Feb 1, 2025): the cache service was rewritten end-to-end. `actions/cache@v1` and `@v2` were retired on that date — all workflow runs still referencing them fail. Self-hosted runners must be on Runner 2.231.0+ for v3/v4 and 2.327.1+ for the newest releases. Stay on `@v4` for the stable line; track Renovate updates for newer majors as they ship.

Cache eviction (enforced Nov 2025): GitHub evaluates eviction **every hour** instead of every 24 hours. Repos that churned through `>10 GB` per day now feel that pressure immediately — design keys so a single PR-shaped cache miss does not cascade into thrashing on the next push.

Rules:

- prefer built-in setup caches first (`setup-node`, `setup-python`, `setup-go`, `setup-java`, `setup-dotnet`, `astral-sh/setup-uv`)
- key caches by OS, arch, and lockfile hash — include `runner.arch` whenever a native binary or wheel is in the cache, otherwise ARM and x64 will clobber each other
- gate dependent steps on `steps.<id>.outputs.cache-hit == 'true'` to skip redundant installs
- do not cache entire `node_modules` unless you have measured a need
- avoid duplicate caches such as `setup-node` cache plus an overlapping `actions/cache`
- expect at most 10 GB per repo (users can request up to 10 TB for personal repos; enterprise / org / repo admins can raise the cap); entries unread for 7 days are evicted regardless
- treat the cache as an untrusted blob: the Mini Shai-Hulud TanStack wave (May 2026) poisoned the Actions cache with malicious binaries from a fork PR, then extracted runner OIDC tokens. Never key on user-controllable values like PR titles or branch names from forks.

## Job Graph Design

| Pattern | Use it when | Avoid |
|---------|-------------|-------|
| Parallel independent jobs | lint, unit tests, static analysis are independent | serializing everything with `needs:` |
| Diamond graph | multiple checks feed one build or deploy | long linear chains |
| Conditional jobs | monorepo or environment-specific paths | giant workflow-level skip logic |

Prefer:

```yaml
lint ─┐
test ─┼─> build ─> deploy
scan ─┘
```

over:

```yaml
lint -> test -> build -> deploy
```

## Matrix Strategy

| Rule | Guidance |
|------|----------|
| `fail-fast: false` | use when each axis gives independent signal |
| `include` / `exclude` | trim impossible or low-value combinations |
| push vs PR coverage | keep pushes small, expand on PRs or nightly |
| explosion guard | redesign if matrix fan-out approaches `100+` jobs |

Dynamic matrices are appropriate when the changed package set or supported versions are computed at runtime.

## Artifacts And Concurrency

| Topic | Rule |
|-------|------|
| Artifact actions | `upload-artifact@v4`+ / `download-artifact@v4`+ are the only supported lines on github.com. v1-v3 were sunset Jan 30, 2025; v3.2.2 is the GHES-only fallback. |
| Immutability | artifact names within a workflow run are immutable; no multi-job uploads to the same name (use a per-matrix suffix) |
| Performance | v4 backend is up to ~98% faster on upload + download vs v3 |
| Non-zipped uploads (Feb 2026) | `actions/upload-artifact@v7` adds `archive: false` for direct (unzipped) uploads; `actions/download-artifact@v8` consumes them. `archive` defaults to `true` for backward compatibility — opt in only when you need browser-viewable HTML / images / pre-zipped payloads. |
| Artifact cap | max `500` artifacts per job |
| PR concurrency | use `cancel-in-progress: true` |
| Deploy concurrency | use `cancel-in-progress: false` to preserve queue order |
| Queue depth (May 2026) | `queue: max` allows up to **100** pending runs in the same concurrency group, processed sequentially. Only valid when `cancel-in-progress` is `false` or unset — pairing with `cancel-in-progress: true` is a validation error. |

PR pattern:

```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true
```

Deploy pattern (preserve every queued release, up to 100):

```yaml
concurrency:
  group: deploy-production
  cancel-in-progress: false
  queue: max
```

Multi-job artifact pattern (matrix-aware, v4+):

```yaml
- uses: actions/upload-artifact@<full-sha>   # v4.x
  with:
    name: build-${{ matrix.os }}-${{ matrix.arch }}
    path: dist/
```

## Runner Cost Guide

| Runner | Relative cost | Use it for |
|--------|---------------|------------|
| `ubuntu-latest` | baseline | default CI |
| Windows | `2x` | Windows-only checks |
| macOS | `10x` | Apple-platform validation |
| ARM (Linux) | about `37%` cheaper than comparable x64 | compatible Linux workloads; free for public repos |

January 2026 pricing restructure: the Linux default jumped to 4 vCPU / 16 GB at no extra charge, and per-minute prices dropped by up to 39% across runner types. Self-hosted runners remain free; the platform charge GitHub had floated was shelved indefinitely.

Illustrative GitHub-hosted pricing examples (verify current rates in your billing settings):

- `ubuntu-latest`: `$0.008` / min (post-restructure baseline)
- `windows-latest`: `$0.016` / min
- `macos-latest`: `$0.08` / min
- `macos-latest-xlarge`: `$0.12` / min

## Optimization Checklist

- keep clones shallow unless history is required
- combine tiny steps that pay repeated setup costs
- use timeouts on long-running jobs
- shard tests only after measuring imbalance
- route monorepo work with path filters or affected-package tooling
- profile artifact upload/download before blaming test runtime
- watch the Actions Performance Metrics dashboard (GA since March 2025) for queue time and failure-rate regressions; turn on Actions Data Stream when near-real-time per-step telemetry is worth the routing cost
- use `act` or `workflow_dispatch` to validate expensive changes before broad rollout
