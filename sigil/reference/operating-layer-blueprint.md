# Blueprint Method

**Purpose:** The SURVEY → MAP method for discovering a repo's operating-layer needs and shaping the suite plan + coverage matrix.
**Read when:** You are running SURVEY or MAP on any repository, or producing the blueprint skeleton.

## Contents
- Principle
- SURVEY: what to read and infer
- MAP: task → mechanism
- Coverage Matrix format
- Suite Plan format
- Common operating-layer shapes by stack

---

## Principle

A repository's operating layer is the set of project-local capabilities that make recurring work fast and consistent: the skills that encode the repo's conventions, the recipes that chain them for repeatable tasks, and the workflows that coordinate multiple agents toward an outcome. Sigil[blueprint] designs that set as **one coherent system**, then delegates each piece to its owner. The output of SURVEY + MAP is a grounded list of what the repo actually does repeatedly — not a generic template.

Design from observed repetition, never from a stack checklist. A capability earns a place in the layer only when SURVEY found a recurring task, pain point, or convention that justifies it.

---

## SURVEY: what to read and infer

Delegate deep code reading to `Lens` and reuse `Sigil`'s inventory; Sigil[blueprint] synthesizes, it does not re-scan line by line.

| Signal | Source | What it tells you |
|--------|--------|-------------------|
| Stack & frameworks | manifests (`package.json`, `pyproject.toml`, `go.mod`, …), lockfiles | Which conventions a skill must mirror |
| Conventions | existing source files, `CLAUDE.md` / `AGENTS.md`, lint/format config | Naming, imports, error handling, testing idioms |
| Recurring tasks | commit history shape, PR templates, `scripts/`, Makefile/justfile targets, CI jobs | What the team does over and over (recipe candidates) |
| Team workflows | branch model, release process, review gates, issue/PR labels | Multi-agent workflow candidates and enforcement points |
| Existing layer | `.claude/skills/`, `.claude/commands/`, project recipes, hooks in `settings.json` | What already exists — never duplicate it |
| Ecosystem inventory | `~/.claude/skills/` roster (via Sigil/Compass) | Tasks already owned by a global agent — defer, don't design |

**Greenfield repos** (no `.claude/` layer, no prior Sigil runs): infer stack and conventions directly from manifests, CI config, scripts, and commit history; Sigil[blueprint] owns this existing-layer scan itself. Sigil's inventory is consulted only when a prior run produced one — never block on its absence.

Stop and ask (per Boundaries → Ask First) if no stack/conventions are detectable or the primary domain is unclear after SURVEY. Do not design from generic templates.

---

## MAP: task → mechanism

For each recurring task or pain point from SURVEY, pick the cheapest mechanism that solves it. Use `_common/MECHANISM_SELECTION.md` for the hook / scoped rule / subagent / skill choice; `recipe` and `workflow` are **Sigil[blueprint]-local mechanisms** defined here and in `recipe-design.md` / `workflow-design.md` (the `_common` file does not cover them). Combined summary:

| The task is... | Mechanism | Owner (delegate to) |
|----------------|-----------|---------------------|
| An enforcement that must run **every time** / must **never** happen | Hook | `Hone` |
| A constraint that applies only under a **path/glob** | Scoped rule (CLAUDE.md / settings) | `Sigil` or direct |
| An **isolated side task** that clutters the main thread | Subagent (`context: fork` skill) | `Sigil` authors |
| A **reusable methodology** invoked on demand | Project-local skill | `Sigil` authors |
| A **repeatable multi-step task** chaining skills/agents | Recipe (subcommand flow) | designed by Sigil[blueprint], registered via `Nexus` |
| A **multi-agent outcome** needing coordination | Workflow / chain | designed by Sigil[blueprint], run via `Nexus` (loop → `Orbit`) |
| Already owned by an ecosystem agent | Nothing new | route to that agent in the routing map |

Flag ecosystem overlap here. If a task overlaps `≥ 30%` with an existing agent, defer it via the routing map; `≥ 50%` is a hard defer; `30-49%` is an Ask-First.

---

## Coverage Matrix format

The MAP deliverable. One row per recurring task.

```
| Task                         | Frequency | Mechanism   | Owner   | Notes                         |
|------------------------------|-----------|-------------|---------|-------------------------------|
| Add a tRPC procedure         | daily     | skill       | Sigil   | mirror @/ alias + Zod loc     |
| Ship a feature end-to-end    | weekly    | recipe      | Nexus   | chains scaffold→build→test→PR |
| Block commits to main        | every-time| hook        | Hone   | PreToolUse guard              |
| Cut a release                | monthly   | workflow    | Nexus   | hub-spoke, 4 phases           |
| Security review of a PR      | weekly    | (ecosystem) | Judge   | defer — Judge owns this       |
```

---

## Suite Plan format

The DESIGN deliverable skeleton (detail filled by `recipe-design.md` / `workflow-design.md`).

```yaml
suite_plan:
  skills:        # → Sigil authoring specs
    - name: new-trpc-procedure
      responsibility: "Generate a tRPC procedure with Zod input + colocated test"
      conventions: [import-alias "@/", zod-in-schemas-dir, vitest]
  recipes:       # → Nexus registration
    - subcommand: ship-feature
      task: "feature from scaffold to opened PR"
      chain: [scaffold, builder, radar, guardian]
  workflows:     # → Nexus (+ Orbit if looped)
    - name: release-train
      outcome: "tagged release with changelog + notes"
      topology: hub-spoke
      phases: [collect, version, changelog, verify]   # <= 5
  routing_map:   # → Nexus
    "db schema":     schema
    "trpc procedure": new-trpc-procedure (project)
    "security review": judge
```

---

## Common operating-layer shapes by stack

Starting hypotheses only — confirm against SURVEY, never auto-apply.

| Stack | Likely skills | Likely recipes | Likely workflows |
|-------|---------------|----------------|------------------|
| Next.js + Prisma + tRPC | new-app-route, new-prisma-model, new-trpc-procedure | ship-feature, add-migration | release-train |
| Python service + FastAPI | new-endpoint, new-pydantic-model | ship-endpoint | deploy-check |
| Monorepo (Turborepo/Nx) | new-package, new-shared-component | scoped-build, cross-package-refactor | affected-test-run |
| Game (Unity/Godot) | new-system, new-entity | add-feature-loop | balance-pass |

For monorepos, scope each component's `PROJECT_AFFINITY` to its package path and ask before designing shared root-level capabilities.
