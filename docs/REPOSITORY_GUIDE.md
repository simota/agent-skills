# Repository Guide

> Current-state guide for maintainers and contributors.

This document explains how the repository is organized, what is authoritative, how the active skill roster is counted, and which checks define a valid change. It complements the public catalog in `README.md` / `README_ja.md` and the authoring rules in `CONTRIBUTING.md`.

## Current baseline

The active repository surface is the global skills at `<skill-name>/SKILL.md` plus the project-local skills `orbit`, `lore`, and `darwin`.

This guide deliberately records no measured quantities (skill, recipe, test, or contract counts): they drift with every change and nothing here re-derives them (`_common/OPERATIONAL.md` § Derived Numbers). For the current numbers, run `make check` — each checker prints its own counts and findings, and the test runner prints the number of tests run. The public roster counts in `README.md` / `README_ja.md` / `index.html` are re-derived by `_common/scripts/test_catalog_regressions.py`.

Non-blocking advisories (size or recipe-count warnings, reviewed routing exceptions) are printed by the same checkers and are not failures; their reviewed-exception lists live in the owning checker.

## Repository model

### Global skills

A global skill is a top-level directory containing `SKILL.md`:

```text
<skill-name>/
├── SKILL.md
└── reference/        # optional supporting material
```

Global skills are reusable across projects and may be selected by global profiles. The canonical active count is based on these top-level `SKILL.md` packages, not on archived or mirrored copies.

### Project-local skills

Repository operating extensions live in two synchronized trees:

```text
.claude/skills/<skill-name>/   # canonical copy
.agents/skills/<skill-name>/   # cross-tool mirror
```

The active project-local roster is defined by `_common/PROJECT_LOCAL_SKILLS.md`. Today it contains `orbit`, `lore`, and `darwin`.

Project-local skills are active corpus members, but they are **not global skills** and must not be added to global profiles. The two trees represent the same skills and are not counted twice.

If a project-local skill references `_common/` or `_templates/`, both canonical and mirror copies must contain the corresponding resolving symlink beside `SKILL.md`. With the current directory depth, the shared-root target is `../../../_common` or `../../../_templates`.

### Archived skills

`.archive/` holds a retired skill only while `prune`'s sunset protocol keeps it; it is currently empty, and earlier packages are recoverable from git history. Archived packages are excluded from all active-roster counts and must not be reintroduced into routing, profiles, or public counts accidentally.

## Authoritative sources

Use the following source-of-truth hierarchy when documentation disagrees with implementation:

| Concern | Authoritative source |
|---|---|
| Global skill definition | `<skill-name>/SKILL.md` |
| Skill authoring template | `_templates/SKILL_TEMPLATE.md` |
| Project-local roster and fallback rules | `_common/PROJECT_LOCAL_SKILLS.md` |
| Shared operational contracts | `_common/*.md` according to contract tier/precedence |
| Recipe registration | Each skill's Recipes/Subcommand Dispatch plus recipe validators |
| Public catalog | `README.md`, `README_ja.md`, `index.html`, `compass/reference/catalog.md` |
| Selective loading / packs | `_common/SKILL_PACKS.md` |
| Contributor workflow | `CONTRIBUTING.md` |
| Executable validation entry points | `Makefile` (`make validate`, `make test`, `make check`) |
| Historical change narrative | `CHANGELOG.md` and merged PRs |

Generated or mirrored artifacts should be regenerated or synchronized from their authoritative source rather than edited independently.

## Validation contract

The supported validation entry points are defined in the `Makefile`:

```bash
make validate   # corpus/invariant checks
make test       # regression tests for checkers and tooling
make check      # validate + test
make hooks      # install the repository-managed pre-commit hook
```

`make check` is the default pre-PR command because it exercises both repository invariants and the checker regression suite.

### What `make validate` checks

It runs, in order:

1. global `SKILL.md` frontmatter/structure validation
2. project-local canonical frontmatter/structure validation
3. project-local roster, mirror, symlink, and shared-reference validation
4. recipe validation
5. routing-oracle validation
6. instruction validation
7. contract-delivery validation
8. lessons validation
9. mechanical task-battery validation
10. `index.html` `SUBCOMMANDS` freshness (`generate-index-subcommands.py --check`)
11. Compass Recipes directory freshness (`generate-recipes-directory.py --check`)

It then reports the pre-commit hook state: `hooks on`, `hooks off` (run `make hooks`), or `hook stale` when the Makefile's hook recipe changed since the hook was installed (rerun `make hooks`).

The exact list is executable policy: consult the `validate` target in `Makefile` instead of copying an old ad-hoc command list into new documentation.

### Project-local invariants

`_common/scripts/lint-project-local.py` enforces three blocking invariants:

- **PL-1 — roster agreement:** the registry, `.claude/skills/`, and `.agents/skills/` contain the same project-local skill names.
- **PL-2 — mirror identity:** canonical and mirror trees are recursively identical, including symlink targets.
- **PL-3 — shared-reference delivery:** referenced `_common/` / `_templates/` namespaces resolve to the repository shared roots and referenced concrete files exist.

These checks close a gap that ordinary top-level corpus iteration cannot cover because project-local skills live below hidden roots.

## Documentation consistency map

Changes to the skill ecosystem can require updates in more than one public or routing surface. Use this table before opening a PR.

| Change | Documentation / registry surfaces to review |
|---|---|
| Add/remove/rename a global skill | `README.md`, `README_ja.md`, `index.html`, `compass/reference/catalog.md`, `_common/SKILL_PACKS.md`, `AGENTS.md`, `CLAUDE.md` |
| Change a skill's public capability | README catalogs, Compass catalog, affected collaboration/routing references |
| Add/change Recipes | owning `SKILL.md`, recipe references; regenerate the Compass Recipes directory (`python3 _common/scripts/generate-recipes-directory.py`) and `index.html` `SUBCOMMANDS` (`python3 _common/scripts/generate-index-subcommands.py`); run recipe validation |
| Change global routing | Nexus/Compass routing material and routing-oracle expectations |
| Change a project-local skill | canonical `.claude/skills/*`, mirrored `.agents/skills/*`, `_common/PROJECT_LOCAL_SKILLS.md` when roster/fallback changes |
| Add a shared contract | `_common/` contract metadata/precedence plus reachability; run contract-delivery validation |
| Change installation/link behavior | `README.md`, `README_ja.md`, `Makefile`, installer/hook tests as applicable |
| Change validation tooling | `Makefile`, `CONTRIBUTING.md`, CI workflow, regression fixtures/tests |

For roster changes, do not treat one updated README as completion. Public counts, catalogs, packs, routing, and machine-checked registries need to agree.

## Contribution workflows

### Global skill change

1. Edit the top-level skill package and references.
2. Keep frontmatter, required sections, Recipes, and Reference Map aligned with `_templates/SKILL_TEMPLATE.md` and shared contracts.
3. Update every affected public catalog / registry surface listed above.
4. Run `make check`.
5. Review warnings as well as blocking errors; document intentionally reviewed exceptions in the owning mechanism rather than suppressing them informally.

### Project-local skill change

1. Make the semantic change in `.claude/skills/<name>/`.
2. Apply the same recursive content and symlink change to `.agents/skills/<name>/`.
3. Preserve resolving `_common` / `_templates` links for every referenced shared namespace.
4. Update `_common/PROJECT_LOCAL_SKILLS.md` if the roster, fallback, or project-local contract changes.
5. Run `make check`; `lint-project-local.py` is the authoritative mirror/wiring gate.

### Validation tooling change

Checker code is production infrastructure for this repository. A checker change should include regression cases that demonstrate both the failing repository state and the repaired state. Keep the `Makefile`, CI, hook fixtures, and installer fixtures synchronized when the checker roster changes.

## Recent operational changes reflected here

### 2026-09-15 — project-local validation became executable policy

The merged change behind commit `36e6030` added dedicated validation for project-local skills, wired it into `make validate` and CI, and added resolving shared-contract symlinks to both canonical and mirror trees. The repository now rejects roster drift, mirror drift, and runtime-unresolvable shared references for project-local skills.

### 2026-09-14 — corpus/runtime audit repair

The preceding merged audit repaired staged-content validation, installer-path protection, Markdown parsing, recipe registration, catalog metadata, token-usage checks, execution-loop preservation, atomic report output, HTML escaping, print layout, and kit setup. It also added regression tests for each repaired defect; current test and corpus counts come from `make check`, not from this history.

## Maintenance rule

Prefer **executable truth over duplicated prose**. Counts and catalog text still need to be human-readable, but whenever a fact can drift (rosters, mirrors, recipes, routing, contract reachability), the repository's checker should define the invariant and documentation should point maintainers to that checker.
