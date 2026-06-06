# Matrix Strategy

Purpose: Design multi-axis matrix builds in GitHub Actions that cover meaningful combinations (OS x runtime x arch) while keeping CI-time bounded. Pick the sparsest coverage that still detects regressions; expand full fan-out only on nightly or release branches.

## Scope Boundary

- **Pipe `matrix`**: GitHub-Actions-specific matrix mechanics (`strategy.matrix`, `include` / `exclude`, `fail-fast`, `max-parallel`, `fromJSON` dynamic matrix).
- **Gear `ci`**: provider-agnostic CI/CD posture — which provider, which stages, which quality gates. If the question is "should we test on 3 Node versions or 2?", stay in Pipe. If it's "should we use GHA or Buildkite for this matrix?", route to Gear `ci`.
- **`matrix` skill (combinatorial analysis)**: pairwise coverage, orthogonal arrays, universal combination explosion control. Useful upstream for picking which combinations to include — route there when the matrix is still being scoped.

## Axis Selection

| Axis | Typical values | Default coverage |
|------|----------------|------------------|
| OS | `ubuntu-latest`, `windows-latest`, `macos-latest` | Linux always; add Windows/macOS only for platform-specific code paths |
| runtime | `node: [20, 22]`, `python: ['3.11', '3.12', '3.13']`, `go: ['1.22', '1.23']` | current LTS + next LTS; drop EOL versions |
| arch | `x64`, `arm64` | x64 baseline; add arm64 when shipping native binaries or targeting Graviton/Apple Silicon |
| package manager | `pnpm`, `npm`, `yarn`, `bun` | pick one — do not cross-matrix unless the library itself is the subject |
| framework | `react: [18, 19]`, `next: [14, 15]` | only for libraries distributed across versions |

Rule: every added axis multiplies cost. If an axis fails identically across values, it is not giving independent signal — drop it.

## `include` / `exclude`

Use `exclude` to drop impossible or low-value cells from a dense product:

```yaml
strategy:
  fail-fast: false
  matrix:
    os: [ubuntu-latest, windows-latest, macos-latest]
    node: [20, 22]
    exclude:
      - os: windows-latest
        node: 20   # skip legacy Node on Windows
      - os: macos-latest
        node: 20   # skip legacy Node on macOS (cost)
```

Use `include` to add sparse, targeted combinations on top of (or instead of) a product:

```yaml
strategy:
  fail-fast: false
  matrix:
    include:
      - { os: ubuntu-latest,  node: 22, coverage: true }
      - { os: ubuntu-latest,  node: 20, coverage: false }
      - { os: windows-latest, node: 22, coverage: false }
      - { os: macos-latest,   node: 22, coverage: false }
```

Pure-`include` matrices are the sparsest viable coverage — 4 cells instead of the 3x2 = 6 product. Prefer this shape when you know which combinations matter.

## Fail-Fast Policy

| Policy | Use when |
|--------|----------|
| `fail-fast: true` (default) | PR loops where one failure already blocks merge — cancel peers to save minutes |
| `fail-fast: false` | You want complete signal across axes — flaky test investigation, release verification, cross-OS regression hunts |

Default recommendation: `fail-fast: false` on `push: main` and release branches, `fail-fast: true` on PRs.

## `max-parallel`

Cap concurrent matrix jobs when the org has a small runner pool or when each job contends for a shared external resource (database, flaky external API):

```yaml
strategy:
  max-parallel: 4
  matrix:
    ...
```

Without `max-parallel`, GHA runs up to 256 matrix jobs in parallel subject to the plan's concurrency limit. Use explicit caps to bound runner spend and avoid starving other workflows.

## Dynamic Matrix via `fromJSON`

Compute the matrix at runtime (changed packages, supported versions from a file, nightly full coverage vs PR sparse):

```yaml
jobs:
  plan:
    runs-on: ubuntu-latest
    outputs:
      matrix: ${{ steps.set.outputs.matrix }}
    steps:
      - uses: actions/checkout@v4
      - id: set
        run: |
          if [ "${{ github.event_name }}" = "schedule" ]; then
            echo 'matrix={"node":[20,22,24],"os":["ubuntu-latest","windows-latest","macos-latest"]}' >> $GITHUB_OUTPUT
          else
            echo 'matrix={"node":[22],"os":["ubuntu-latest"]}' >> $GITHUB_OUTPUT
          fi

  test:
    needs: plan
    strategy:
      fail-fast: false
      matrix: ${{ fromJSON(needs.plan.outputs.matrix) }}
    runs-on: ${{ matrix.os }}
    steps:
      - run: node --version
```

Common dynamic-matrix drivers: `turbo run --filter`, `nx affected`, `dorny/paths-filter`, a repo `versions.json`.

## Sparse Coverage Patterns

- PR: single OS, single runtime, fast feedback (`< 10 min`).
- `push: main`: LTS matrix (2-3 versions, Linux only).
- Nightly: full product (all OS x all runtimes x arches).
- Release branch: full product + long-running integration.

This tiered shape keeps CI-time bounded for the 99% case while preserving full-signal checkpoints.

## Explosion Guard

If matrix fan-out approaches `100+` jobs, redesign:

1. Can any axis be dropped (duplicate signal)?
2. Can `include` replace the dense product?
3. Can full coverage move to nightly instead of every PR?
4. Can sharding replace breadth (1 job with sharded tests instead of N identical jobs)?

## Pair With Cache

Per-axis cache keys avoid cross-contamination across OS and runtime:

```yaml
key: deps-${{ matrix.os }}-${{ matrix.node }}-${{ hashFiles('**/pnpm-lock.yaml') }}
```

Route to `cache` recipe for the full design.

## Anti-Patterns

- Cross-matrixing package managers AND runtimes AND OS "just to be safe" — combinatorial explosion with no incremental signal.
- `fail-fast: true` on release verification — you lose the signal you actually needed.
- Static matrix for "optional" legacy support — move to dynamic matrix gated on schedule.
- Adding Windows/macOS rows to a pure-TypeScript library — duplicate signal, 2x-10x runner cost.
- No `max-parallel` on a 50-job matrix feeding into a shared staging DB.
