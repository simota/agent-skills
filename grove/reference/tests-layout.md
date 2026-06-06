# Tests Directory Layout Reference

Purpose: Design and audit `tests/` (and co-located test) layouts across unit, integration, e2e, contract, and performance tiers. Covers mirror-source vs centralized trade-offs, fixture/factory placement, test-helper module pattern, and naming conventions. Optimizes for fast feedback at the unit tier and reliable signal at the integration/e2e tiers.

## Scope Boundary

- **grove `tests`**: filesystem layout for tests — directory split, mirror vs centralized, fixtures/factories/helpers placement, file naming. Layout-only.
- **grove `audit` / `design` / `docs` / `migrate` (default + siblings)**: structural audit, generic directory design, docs/, level-based migration. Use these when the focus is not specifically the test tree.
- **grove `monorepo` / `scripts` (siblings)**: workspace-level layout and scripts/ layout — Grove `tests` is invoked per-package within those.
- **Mint (elsewhere)**: factory and fixture content authoring (boundary-value data, synthetic data). Grove `tests` decides where they live; Mint decides what they generate.
- **Radar (elsewhere)**: test additions for coverage gaps and edge cases. Grove `tests` decides directory; Radar fills it with cases.
- **Voyager (elsewhere)**: E2E test implementation (Playwright/Cypress page objects). Grove `tests` decides `e2e/` location; Voyager owns the test code.
- **Nest (elsewhere)**: LLM-context retrieval ordering of the test tree. Grove `tests` ships the layout; Nest tunes it for context windows.

## Workflow

```
DETECT  →  test runner (jest/vitest/pytest/go test/cargo test), existing layout, test counts per tier
        →  measure unit:integration:e2e ratio against the test pyramid

CLASSIFY → split tests into tiers: unit / integration / contract / e2e / performance
        →  identify cross-tier shared fixtures and helpers

LAYOUT  →  choose mirror-source (co-located *.test.ts) vs centralized tests/<tier>/
        →  place fixtures/, factories/, helpers/, __mocks__/ at correct scope

NAMING  →  fix on .test vs .spec, mirror file path, tag conventions (@smoke @slow)

VERIFY  →  test runner discovers all files, no orphan helpers, fixtures resolve from each tier
        →  CI tier-split (unit-fast / integration-medium / e2e-slow) maps to directories

PRESENT →  layout diagram, naming rules, migration steps for legacy tests
        →  hand off content to Mint / Radar / Voyager
```

## Test Taxonomy

| Tier | Scope | Speed | Where it lives |
|------|-------|-------|----------------|
| unit | one function/class, no I/O | < 50 ms each | co-located `*.test.ts` next to source, or `tests/unit/` mirror |
| integration | module + real dependency (DB/HTTP) | 50 ms – 5 s | `tests/integration/` |
| contract | provider/consumer API shape (Pact) | < 1 s | `tests/contract/` |
| e2e | full app, real browser/CLI | 5 s – 60 s | `tests/e2e/` (Playwright/Cypress) |
| performance | load, p95 latency, throughput | minutes | `tests/perf/` or separate repo |

The pyramid: many unit, some integration, few e2e. Inverted pyramids (e2e-heavy) are slow, flaky, and expensive — flag in audit.

## Mirror-Source vs Centralized

| Style | Pros | Cons | Use when |
|-------|------|------|----------|
| Co-located (`src/foo.ts` + `src/foo.test.ts`) | Tests move with code, easy discovery, refactor-safe | Pollutes source tree, requires runner exclusion in builds | Unit tests in JS/TS, Rust (`#[cfg(test)]`), Go (`foo_test.go`) |
| Centralized (`tests/unit/foo.test.ts` mirroring `src/foo.ts`) | Clean source tree, easy CI tier split | Tests drift when source moves, harder discovery | Python (`tests/` convention), polyglot repos, e2e/integration tiers |
| Hybrid | Co-locate unit, centralize integration/e2e | Two conventions to learn | Most production codebases |

Default for new JS/TS: co-locate unit, centralize integration/e2e. Default for Python: centralize all under `tests/`.

## Fixture / Factory / Helper Placement

```
tests/
  unit/                    # mirrors src/ — only when not co-located
  integration/
  e2e/
  contract/
  perf/
  fixtures/                # static JSON/YAML/SQL seed data
    users.json
    orders.sql
  factories/               # programmatic builders (Mint owns content)
    user.factory.ts
    order.factory.ts
  helpers/                 # shared test utilities (db setup, http client, time freeze)
    db.ts
    http.ts
    time.ts
  __mocks__/               # framework-required mock placement (jest)
  setup/                   # global setup/teardown
    global-setup.ts
    global-teardown.ts
```

Scope rules: helpers used across tiers go in `tests/helpers/`. Helpers used only within one tier go in `tests/<tier>/helpers/`. Never import production code into helpers — keep the test-realm/prod-realm boundary clean.

## Naming Conventions

| Pattern | Use | Notes |
|---------|-----|-------|
| `*.test.ts` | JS/TS unit and integration | Default for jest/vitest |
| `*.spec.ts` | BDD style or e2e | Common in Cypress/Playwright |
| `test_*.py` | Python pytest | Discovery default |
| `*_test.go` | Go | Required by `go test` |
| `*.test.exs` | Elixir | ExUnit convention |

Pick one per tier and lint it. Mixing `.test` and `.spec` in the same tier without a rule causes runner-config drift. Tag conventions: `@smoke`, `@slow`, `@flaky`, `@security` — wired into CI selectors (`vitest --grep @smoke`, `pytest -m smoke`).

## CI Tier-Split

| Stage | Selector | Budget |
|-------|----------|--------|
| pre-commit | unit (co-located) | < 30 s |
| PR fast | unit + lint + typecheck | < 3 min |
| PR medium | integration + contract | < 10 min |
| PR slow / nightly | e2e + perf | < 30 min |

Layout must make this trivial: `vitest tests/unit` vs `vitest tests/integration`. If selectors require glob gymnastics, layout is wrong.

## Anti-Patterns

- **AP-TS-01 — single tests/ with no tier split**: mixing unit and e2e in one folder forces every PR to run e2e. PR feedback time blows past 15 min. Split into `tests/unit/`, `tests/integration/`, `tests/e2e/`.
- **AP-TS-02 — fixtures inside source tree**: `src/fixtures/` ships test data to production bundles. Move all fixtures under `tests/fixtures/` and exclude from build.
- **AP-TS-03 — helpers importing production code transitively into prod build**: helper imports a util that imports a test-only mock; bundler picks it up. Keep `tests/helpers/` outside `tsconfig` `include` for production builds.
- **AP-TS-04 — mixing .test and .spec without a rule**: runner config grows brittle exclude lists. Pick one convention per tier and lint.
- **AP-TS-05 — e2e in same package as unit**: e2e dependencies (Playwright, browsers) bloat unit-test container; cold starts slow CI. Hoist e2e to `apps/<name>-e2e/` or top-level `tests/e2e/`.
- **AP-TS-06 — factories duplicated per test file**: every `*.test.ts` redefines a `makeUser()` helper; one schema change requires N edits. Centralize in `tests/factories/`.
- **AP-TS-07 — no global setup/teardown convention**: each test boots its own DB; integration suite takes 20+ min. Use `tests/setup/global-setup.ts` for shared expensive resources.
- **AP-TS-08 — orphaned snapshots**: `__snapshots__/` keeps stale snapshots for deleted tests because no `--ci` flag. Run `--ci` and add snapshot-cleanup step.
- **AP-TS-09 — perf tests in PR pipeline**: load tests run on every PR, blow CI budget, and produce noisy failures from shared infra. Move to nightly or dedicated environment.

## Handoff

- **To Mint**: factory file paths defined by Grove become Mint targets — Mint authors `user.factory.ts` content (boundary values, synthetic data).
- **To Radar**: directory and naming rules become Radar's placement template when adding edge-case tests or fixing flakies.
- **To Voyager**: `tests/e2e/` location becomes the Voyager working tree for Playwright/Cypress page objects and journey tests.
- **To Nest**: once layout is stable, Nest can reorder helpers/fixtures for context-cache efficiency (e.g., README ordering, manifest hoisting).
- **To Atlas**: if helpers import production code in unwanted directions, Atlas validates the dependency graph.
- **To Sigil**: Grove publishes the test layout; Sigil generates project-tuned test skills (runner, framework, naming convention).
- **To Gear**: tier-split CI matrix (unit/integration/e2e selectors, parallelism) wired by Gear after layout is locked.
