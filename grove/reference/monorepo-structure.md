# Monorepo Structure Reference

Purpose: Design and audit monorepo directory layouts across Nx, Turborepo, pnpm workspaces, Bazel, and Lerna. Covers package boundary design, internal dependency graph, code-sharing patterns, build cache layout, and polyrepo→monorepo migration. Optimizes for tractable ownership, fast incremental CI, and discoverability at 5–1,000+ packages.

## Scope Boundary

- **grove `monorepo`**: workspace tool selection, top-level layout (apps/ vs packages/ vs libs/), CODEOWNERS map, build-cache strategy, polyrepo→monorepo migration. Filesystem-level decisions only.
- **grove `audit` / `design` / `migrate` (default + siblings)**: single-repo structural audit, generic directory design, level-based migration. Use these when the project is not a workspace-managed monorepo.
- **grove `tests` / `scripts` (siblings)**: tests/ and scripts/ layout — invoked per-package within a monorepo, but layout decisions are scoped to those concerns.
- **Nest (elsewhere)**: LLM-context folder structure for prompt-cache efficiency. Grove `monorepo` cares about build graphs; Nest cares about retrieval ordering.
- **Atlas (elsewhere)**: code-level dependency analysis (cycles, God modules). Grove `monorepo` defines package boundaries; Atlas reports violations within the chosen boundaries.
- **Sigil (elsewhere)**: dynamic skill generation per project. Grove ships repo structure; Sigil ships skill files describing it.

## Workflow

```
DETECT  →  enumerate package manifests, lockfiles, workspace config (pnpm-workspace.yaml, nx.json, turbo.json, WORKSPACE)
        →  count packages, languages, team owners; classify as JS/TS-only, polyglot, or hybrid

SELECT  →  apply tool rubric (size × language mix × CI budget × team count)
        →  Turborepo / Nx / pnpm / Bazel / Lerna decision with explicit trade-offs

LAYOUT  →  choose apps/ libs/ packages/ tools/ split; assign CODEOWNERS by directory
        →  define build-cache root, remote-cache target, dependency-rule policy

VERIFY  →  dry-run build graph, package-boundary lint, CI cache hit ratio simulation
        →  ensure no app→app import, no internal/internal cycles

PRESENT →  layout diagram, tool recommendation, migration plan, CODEOWNERS draft
        →  hand off CI wiring to Gear, IaC to Scaffold, PR slicing to Guardian
```

## Tool Comparison Matrix

| Tool | Sweet spot | Languages | Strength | Weakness |
|------|-----------|-----------|----------|----------|
| pnpm workspaces | 2–20 JS/TS packages | JS/TS | Zero config, fastest install, native to package manager | No task graph, no cache — bring your own runner |
| Turborepo | 5–50 JS/TS packages | JS/TS (Rust core) | Minimal config, remote cache, Vercel-native | Weak boundary enforcement, JS-only |
| Nx | 30–500 packages, enterprise | JS/TS first, polyglot plugins | Enforced module boundaries, generators, distributed CI (~16% faster than Turborepo on single-machine) | Steeper learning curve, opinionated |
| Bazel | 1,000+ packages, polyglot | Any (Starlark rules) | Hermetic builds, remote execution, deterministic | High setup cost, BUILD-file maintenance |
| Lerna | Legacy multi-package npm publish | JS/TS | Familiar publish workflows | Superseded by Nx (now maintained by Nrwl); avoid for new repos |

## Layout Templates

```
apps/                      # deployable units (one CODEOWNERS group each)
  web/
  api/
  worker/
libs/                      # internal shared code (importable by apps and other libs)
  ui/
  domain-billing/
  utils-date/
packages/                  # publishable to npm/PyPI/etc.
  sdk-public/
tools/                     # repo-internal scripts, codegens, generators
infra/                     # Terraform / k8s / Helm (Scaffold owns content)
.github/
  CODEOWNERS               # path-scoped ownership
turbo.json | nx.json | WORKSPACE
pnpm-workspace.yaml | package.json (workspaces)
```

Boundary rules: `apps/*` may import from `libs/*` and `packages/*` but never from `apps/*`. `libs/*` may import from other `libs/*` and `packages/*` but never `apps/*`. Enforce via Nx `enforce-module-boundaries`, Turborepo `--filter`, or package `exports`.

## Build Cache Strategy

| Layer | Mechanism | Hit-rate target |
|-------|-----------|-----------------|
| Local | Turborepo / Nx local cache, Bazel disk cache | ≥ 70% incremental |
| Remote | Vercel Remote Cache, Nx Cloud, Bazel BES + RBE | ≥ 50% on PR CI |
| CI matrix | Affected-only graph (`nx affected`, `turbo run --filter=...[HEAD^]`) | run only impacted packages |

Cache key inputs: source files, lockfile, tool versions, env vars listed in `turbo.json` `globalEnv`. Missing env-var declarations cause silent stale-cache bugs.

## Internal-Package Versioning

| Strategy | When | Tool |
|----------|------|------|
| Fixed (lockstep) | Single product, tight coupling | Lerna fixed mode, Nx release group |
| Independent | Multiple products, separate release cadence | Changesets, Nx release independent |
| Workspace `*` (no version) | Internal-only, never published | pnpm `workspace:*` protocol |

Default to `workspace:*` for internal libs to avoid version-bump churn. Publish only what crosses the org boundary.

## Polyrepo→Monorepo Migration Checklist

1. Inventory: list all repos, sizes, last-commit dates, build tools.
2. Tool pick: apply matrix above; lock decision in ADR.
3. Skeleton: create monorepo with empty `apps/`, `libs/`, root `package.json`, workspace config.
4. Import with history: `git subtree add` or `git filter-repo --to-subdirectory-filter` per source repo to preserve blame.
5. CI freeze: read-only mode on source repos; redirect PRs to monorepo.
6. CODEOWNERS: path-scoped owners matching original repo teams day-1.
7. Cache wiring: configure remote cache before opening to all teams.
8. Boundary rules: enable `enforce-module-boundaries` in Evaluate mode for 2 weeks, then Active.
9. Cut over: archive source repos, update internal docs, keep redirects 90+ days.

## Anti-Patterns

- **AP-MR-01 — apps/ importing apps/**: app-to-app imports recreate polyrepo coupling inside the monorepo. One refactor cascades. Enforce with module-boundary lint, not code review.
- **AP-MR-02 — unscoped shared/ or common/ bucket**: every team dumps "utility" code; no public API; refactors break random consumers. Replace with `libs/<domain>-<concern>/` and explicit `exports`.
- **AP-MR-03 — depth > 4 to manifest**: deep nesting balloons Git tree-object count, slows clones, and confuses tools. Flatten to `apps/<name>/` and `libs/<name>/`.
- **AP-MR-04 — single tag for all packages**: lockstep release of independent products eliminates release agility and couples deployments. Use independent versioning (Changesets).
- **AP-MR-05 — env vars not in cache key**: Turborepo/Nx skip env vars by default; missed declaration produces stale builds that pass locally and fail in prod. List every input env in `globalEnv` / `inputs`.
- **AP-MR-06 — no remote cache before open-up**: opening a monorepo to many teams without remote cache causes every CI run to start cold; build times balloon and trust collapses. Wire cache day-1.
- **AP-MR-07 — Lerna for new monorepo**: Lerna is in maintenance mode (under Nrwl/Nx). New repos should pick Nx, Turborepo, or pnpm directly.
- **AP-MR-08 — moved packages without `git subtree`/`filter-repo`**: raw copy loses blame for years of history. Use `git subtree add --prefix=apps/web <source-repo> main` or `git filter-repo --to-subdirectory-filter`.
- **AP-MR-09 — CODEOWNERS added "later"**: without day-1 ownership, every PR pings everyone; review fatigue sets in within a month. Author CODEOWNERS in the same PR as the layout.

## Handoff

- **To Nest**: once monorepo layout is stable, ask Nest to optimize folder ordering for LLM context (e.g., `libs/` README front-loading, package-manifest progressive disclosure).
- **To Atlas**: package boundaries defined by Grove become the input set for Atlas dependency analysis (cycles, God modules within `libs/`).
- **To Sigil**: Grove publishes the monorepo layout; Sigil generates per-package skills tuned to detected conventions (test runner, language, framework).
- **To Anvil**: when monorepo needs a custom CLI for repo-internal tooling (e.g., `repo gen lib`, `repo affected`), Anvil designs the TUI on top of `tools/`.
- **To Gear**: CI matrix wiring (affected-only build, remote cache auth) once layout and tool choice are locked.
- **To Guardian**: PR-slicing strategy for the migration (≤ 50 files per PR, CI-green per commit).
