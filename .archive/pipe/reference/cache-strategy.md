# Cache Strategy

Purpose: Design `actions/cache` entries that maximize hit rate while staying under the 10 GB per-repository budget. Cache layout is a correctness concern — a wrong key either misses (slow) or hits the wrong payload (broken).

## Scope Boundary

- **Pipe `cache`**: GitHub Actions-specific caching — `actions/cache`, built-in `setup-*` caches, Docker layer cache via `type=gha`, key/`restore-keys` design, 10 GB / 7-day eviction.
- **Gear `ci`**: provider-agnostic CI caching posture — which layers to cache across providers, remote-cache backends (Turbo remote cache, Nx Cloud, Bazel remote). If the question is "should we use GHA cache or an external remote cache?", route to Gear `ci`; this recipe assumes you chose GHA cache.

## Repository Cache Facts

- Total budget: **10 GB per repository**. Oldest entries evict first when full.
- Idle eviction: entries not accessed for **7 days** are removed.
- Entries are keyed per branch with fallback to the default branch — PR caches read from the base branch automatically.
- Cross-OS entries are incompatible; the OS token in the key prevents silent corruption.
- `actions/cache@v4` uses Azure blob storage (migrated from the legacy backend — plan for `v4` everywhere; `v3` was EOL'd).

## Key Design

The key must be **deterministic and payload-specific**:

```yaml
- uses: actions/cache@v4
  with:
    path: ~/.pnpm-store
    key: pnpm-${{ runner.os }}-${{ runner.arch }}-${{ hashFiles('**/pnpm-lock.yaml') }}
    restore-keys: |
      pnpm-${{ runner.os }}-${{ runner.arch }}-
      pnpm-${{ runner.os }}-
```

Key components, in order:

1. **Tool/purpose** (`pnpm`, `next-build`, `cargo-target`) — namespace.
2. **OS** (`runner.os`) — `Linux`, `Windows`, `macOS` payloads are incompatible.
3. **Arch** (`runner.arch`) — `X64` vs `ARM64` native binaries differ; omit only for pure-source caches.
4. **Lockfile hash** (`hashFiles('**/pnpm-lock.yaml')`) — the single source of truth for dependency content.
5. Optional: tool version (`node-${{ matrix.node }}`), config hash (`hashFiles('tsconfig.json')`).

Never key by timestamp, commit SHA, or `github.run_id` — every run misses.

## `restore-keys` Fallback

`restore-keys` are prefix matches tried in order when the primary key misses. They enable "warm start" — restore a close-enough cache, then update it:

```yaml
key: pnpm-${{ runner.os }}-${{ hashFiles('**/pnpm-lock.yaml') }}
restore-keys: |
  pnpm-${{ runner.os }}-
```

Rules:

- Strip the most variable suffix first (lockfile hash), then less variable (OS), never the namespace.
- Each `restore-keys` entry returns the **most recent** entry matching the prefix.
- A restore-key hit still writes a **new** entry at the primary key, so the next run warm-starts on the new lockfile.
- Don't fall back across namespaces (`pnpm-` → `npm-`) — incompatible payloads.

## Cross-OS Compatibility

Matrix caches with shared lockfiles still need per-OS keys because native modules (Sharp, esbuild, native Rust binaries) differ:

```yaml
key: deps-${{ matrix.os }}-${{ matrix.node }}-${{ hashFiles('**/pnpm-lock.yaml') }}
```

For Windows-specific path separators, prefer `actions/cache@v4` which handles them automatically. Avoid caching absolute paths that bake in the runner user's home directory.

## Monorepo Multi-Cache

Cache each package-manager root separately to prevent cross-package invalidation:

```yaml
- uses: actions/cache@v4
  with:
    path: |
      ~/.pnpm-store
      apps/web/.next/cache
      apps/api/.turbo
    key: mono-${{ runner.os }}-${{ hashFiles('pnpm-lock.yaml') }}-${{ hashFiles('turbo.json') }}
    restore-keys: |
      mono-${{ runner.os }}-${{ hashFiles('pnpm-lock.yaml') }}-
      mono-${{ runner.os }}-
```

For independent package layers (Turbo, Nx), key each layer separately and keep framework build caches (`.next/cache`, `.turbo`) distinct from dependency caches. Over-bundling one key means every change invalidates everything.

## Built-In `setup-*` Caches First

Language `setup-*` actions ship built-in caching that handles key construction for you:

```yaml
- uses: actions/setup-node@v4
  with:
    node-version: 22
    cache: pnpm
    cache-dependency-path: pnpm-lock.yaml
```

Prefer these for the common case. Reach for `actions/cache` when:

- caching custom artifacts (Next.js `.next/cache`, Turbo, Cargo target, ccache).
- caching across jobs (e.g., a build cache consumed by multiple test jobs).
- the built-in cache misses a path you need.

Never stack `setup-node` cache + overlapping `actions/cache` on the same path — duplicate writes, no benefit.

## Cache-Hit Telemetry

`actions/cache` sets `cache-hit: 'true' | 'false'` as a step output. Measure it:

```yaml
- name: Cache deps
  id: cache
  uses: actions/cache@v4
  with:
    path: ~/.pnpm-store
    key: pnpm-${{ runner.os }}-${{ hashFiles('**/pnpm-lock.yaml') }}

- name: Log hit rate
  run: echo "::notice::cache-hit=${{ steps.cache.outputs.cache-hit }}"
```

Route hit-rate to Actions Data Stream (S3 / Azure Event Hub) for workflow-level dashboards. A hit rate below 70% on a stable lockfile indicates key design problems (over-specific key, missing `restore-keys`).

## Eviction Management

The 10 GB cap is firm. When a repo hits it:

1. Largest caches evict first (Next.js `.next/cache` can be 500 MB+).
2. Idle-7-days caches evict regardless of size.
3. Dead branches hold caches until branch deletion → enable branch-delete cache cleanup.

Tactics:

- Cap expensive caches: only cache `~/.next/cache` on `push: main`, skip on PR.
- Prune via `gh actions-cache delete` in a scheduled job.
- For transient branches, key by `${{ github.ref_name }}` only when the cache is small.

## Anti-Patterns

- Key without lockfile hash — cache goes stale on every dependency change.
- Key by `github.sha` — every run misses.
- Cache entire `node_modules` — large, OS-specific, and `pnpm` / `yarn` symlinks break between runners.
- No `restore-keys` — cold start on every lockfile bump, even for unchanged deps.
- Caching `.git` — never needed; blows the budget.
- Duplicate caches from `setup-node` + `actions/cache` on the same path.
- Sharing one cache across a monorepo's 20 packages — any change invalidates everything.
