# Test Selection & Prioritization Strategy

Purpose: Cut CI time without throwing away signal. Read this when Radar runs in `SELECT` mode or when suites are too slow to run fully on every change.

Contents:

- changed-file selection
- priority tiers
- incremental gates
- monorepo patterns
- skip conditions

## Changed-File Based Selection

### Vitest

```bash
npx vitest --changed HEAD~1
npx vitest --related src/utils/auth.ts
npx vitest --changed
```

### Jest

```bash
npx jest --findRelatedTests src/utils/auth.ts src/services/user.ts
npx jest --changedSince=main
npx jest --onlyFailures
npx jest --changedSince=main --onlyFailures
```

### pytest

```bash
pip install pytest-testmon
pytest --testmon
pytest --testmon --cov=src
pytest $(git diff --name-only main -- '*.py' | xargs -I{} dirname {} | sort -u)
```

### Go

```bash
CHANGED_PKGS=$(git diff --name-only main -- '*.go' | xargs -I{} dirname {} | sort -u | sed 's|^|./|')
go test $CHANGED_PKGS
go test ./pkg/auth/...
```

### Rust

```bash
cargo nextest run -p my-crate
cargo nextest run --partition count:1/4
cargo nextest run -E 'test(auth::)'
cargo nextest run --run-ignored=only
```

## Fail-Likely-First Prioritization

| Priority | Category | Meaning | Typical Source |
|----------|----------|---------|----------------|
| `P0` | Last-Failed | Failed in the last CI run | `--onlyFailures`, retry list |
| `P1` | Direct | Directly related to changed files | `--findRelatedTests`, `--changed` |
| `P2` | Dependent | Import / dependency graph fallout | reverse dependency analysis |
| `P3` | Proximate | Same module or directory | directory-based fallback |
| `P4` | Full | Everything else | full suite |

Run `P0 -> P1 -> P2` before you consider skipping a risky merge.

## Incremental Execution Pipeline

### 3-Gate Strategy

| Gate | Includes | Time Budget | Typical Outcome |
|------|----------|-------------|-----------------|
| Fast | Lint, type check, unit `P0 + P1` | `<= 2min` | PR block |
| Integration | Related integration and contract tests | `<= 5min` | PR block |
| Full | All tests, optional mutation, performance, security | `<= 15min` | main or nightly |

Related CI planning from the broader test-DX perspective:

- `Gate 1`: lint + type check `< 1min`
- `Gate 2`: affected unit tests `< 3min`
- `Gate 3`: affected integration tests `< 5min`

Use the stricter gate when the pipeline already supports it.

## Retry And Re-Run Rules

Retries are allowed only to surface flakes, not to hide real failures.

```yaml
- name: Run tests with retry
  uses: nick-fields/retry@v3
  with:
    timeout_minutes: 10
    max_attempts: 3
    retry_on: error
    command: npx vitest run --reporter=junit --outputFile=test-results.xml
```

```bash
npx vitest run --retry 2
```

## CI-Specific Patterns

| Pattern | Benefit | When To Use |
|--------|---------|-------------|
| Result cache | Faster re-runs | Stable dependency graph |
| Sharding | Linear speed-up | Large deterministic suites |
| Matrix split | Environment coverage | Only when cross-platform value is real |
| Fail-fast | Faster signal | Safe only when later jobs do not add unique evidence |

## Monorepo Patterns

### Turborepo

```bash
npx turbo run test --filter=...[origin/main]
npx turbo run test --filter=@myorg/auth...
npx turbo run test --filter=...[origin/main] --dry-run
```

### pnpm Workspace

```bash
pnpm --filter "...[origin/main]" run test
pnpm --filter @myorg/auth run test
pnpm -r --parallel run test
```

### Nx

```bash
npx nx affected --target=test --base=main
npx nx run-many --target=test --projects=auth,users
npx nx affected:graph --base=main
```

## Skip Conditions

Safe skip candidates:

- docs-only changes
- pure asset changes with no executable code impact
- config changes that provably cannot affect runtime behavior

Unsafe skip candidates:

- schema changes
- dependency upgrades
- shared library changes
- test utilities or global setup changes

Example:

```yaml
if echo "$CHANGED" | grep -qvE '\\.(md|txt|png|jpg|svg|yml|yaml)$'; then
  echo "skip=false" >> $GITHUB_OUTPUT
else
  echo "skip=true" >> $GITHUB_OUTPUT
fi
```

## Decision Rule

Use the smallest selection strategy that still covers:

1. last failures
2. directly changed behavior
3. high-value dependents
4. integration contracts touched by the change

If that still exceeds the budget, optimize sharding or caching before weakening the gate.

## Quick Reference

| Strategy | Command / Tool | Use Case |
|----------|----------------|----------|
| Changed files | `vitest --changed` | Fast PR validation |
| Related tests | `jest --findRelatedTests` | Dependency-aware JS/TS validation |
| Last failed first | `jest --onlyFailures` | Regression-first reruns |
| Python change selection | `pytest --testmon` | Incremental pytest suites |
| Monorepo scope | `turbo --filter=...[main]` | Affected packages only |
| Retry | `vitest --retry 2` | Flake diagnosis, not permanent masking |
