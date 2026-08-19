# Reusable Patterns and Maintenance Anti-Patterns

Purpose: Prevent reuse mistakes, monorepo CI drift, workflow maintenance decay, and weak org-level governance in GitHub Actions.

## Contents

- Reuse anti-patterns
- Maintenance pitfalls
- Monorepo CI anti-patterns
- Deployment hygiene
- Organization governance

## Reuse Anti-Patterns

| ID | Anti-pattern | Signal | Fix |
|----|--------------|--------|-----|
| `RW-01` | Copy-paste workflows | same pipeline copied across repos | consolidate after `3+` copies into a reusable workflow |
| `RW-02` | Copy-paste setup steps | checkout/setup/cache repeated everywhere | extract a composite action after `3+` copies |
| `RW-03` | Reusable workflow chaining | reusable workflows call reusable workflows directly | flatten the workflow graph and share steps via composite actions |
| `RW-04` | `@main` reference | shared workflows change without release control | use semver tags or immutable refs |
| `RW-05` | Composite secret limitation ignorance | composite action expects direct secret access | route secret-requiring logic through reusable workflows or caller env |
| `RW-06` | Over-abstraction | abstraction created after only `2` similar uses | keep small duplication until the rule of three is reached |
| `RW-07` | No input validation | bad or empty workflow inputs slip through | use defaults, `required`, and explicit guards |

## Maintenance Pitfalls

- test workflow changes with `workflow_dispatch` or `act` before rollout
- run `actionlint` in CI
- archive or disable zombie workflows instead of leaving them on schedules
- document workflow purpose, triggers, required secrets, and dependencies
- keep naming conventions predictable, such as `ci-*`, `deploy-*`, and `auto-*`

## Monorepo CI Anti-Patterns

| ID | Anti-pattern | Signal | Fix |
|----|--------------|--------|-----|
| `MR-01` | Run everything always | every package tests on every change | route by package or path with `dorny/paths-filter` |
| `MR-02` | Required-check incompatibility | skipped jobs block merges | add an always-run `ci-gate` job |
| `MR-03` | No affected-package detection | shared-library changes miss dependents | use dependency-aware tooling such as `nx affected` or `turbo --filter` |
| `MR-04` | Single workflow for all packages | one giant file controls every package | split by package, team, or domain when logic becomes tangled |

## Deployment Hygiene

- production environments need protection rules
- keep rollback or previous artifact promotion available
- do not deploy directly from PR branches
- run smoke checks after deployment
- avoid all-at-once production rollout when canary, rolling, or blue-green is feasible

## Organization Governance

| ID | Anti-pattern | Signal | Fix |
|----|--------------|--------|-----|
| `OG-01` | No org-level templates | each repo reinvents CI | publish starter workflows in the org `.github` repo |
| `OG-02` | No action governance | any marketplace action can be used | enforce allow-lists and review policy |
| `OG-03` | No shared secrets strategy | secrets are duplicated repo by repo | prefer organization or environment secrets plus OIDC |
