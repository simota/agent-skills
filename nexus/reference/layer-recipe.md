# Nexus Layer Recipe Reference

**Purpose:** Analyze a repository and design **its operating layer** — the coordinated set of project-local skills, repo-tailored recipes, and skill-and-agent workflows it should have, plus a routing map — by driving **Loom** (design), then delegating skill-body authoring to **Sigil** and recipe/workflow/routing registration to **Nexus**. The deliverable is a working operating layer; `design-only` stops at the blueprint.
**Read when:** User invokes `/nexus layer`, or asks to "design this repo's agents, recipes, and workflows together", "set up the project's operating layer", or "give this repo a project skill suite". For authoring **one** skill body, use `sigil` (SKILL_GEN); for a team + work plan, use `charter`.

## Contents
- Overview
- The design → delegate split
- Layer vs Charter vs Spec vs Sigil (disambiguation)
- Invocation Modes
- Topology
- Phases
- Output report
- Failure Modes Prevented
- Scale & Cost
- Shared protocols

---

## Overview

`layer` is the **project-tooling design** recipe. Where `charter` designs a *team + work plan* to deliver a body of work, `layer` designs the *reusable operating layer* a repository should carry going forward: which project-local skills encode its conventions, which repo-tailored recipes chain them for repeatable tasks, which workflows coordinate agents for project outcomes, and a routing map saying which agent or skill owns which repo task.

`layer` is the Nexus surface over the **Loom** agent. Loom is to the project what Architect is to the ecosystem — it **designs the system and delegates the threads**: it never writes a skill body, runs a chain, or authors a hook. This recipe makes that explicit as a chain: Loom designs the blueprint, Sigil authors each skill body, Nexus registers the recipes/workflows/routing map, Latch authors enforcement hooks, Orbit takes any autonomous loop.

## The design → delegate split

| Half | Does | Produces | Owner |
|------|------|----------|-------|
| **Design** (Loom) | Survey the repo, map each recurring task to a mechanism, blueprint the suite + recipes + workflows + routing map under formal topology | **Operating-Layer Blueprint** + delegation specs | Loom |
| **Delegate** (Sigil/Nexus/Latch/Orbit) | Author each skill body (9+/12), register recipes/workflows/routing map, author hooks, spec loops | Installed skills + registered routing | Sigil (bodies), Nexus (registration), Latch (hooks), Orbit (loops) |

`design-only` mode stops after the blueprint + delegation specs (charter-style inspect-before-commit); the default `full` mode runs the delegation and verifies the standing layer.

## Layer vs Charter vs Spec vs Sigil (disambiguation)

| Recipe | Starts from | Primary artifact | Persists as tooling? | Best when |
|--------|-------------|------------------|----------------------|-----------|
| `layer` | The **repository** | **Operating-Layer Blueprint** → installed project skills/recipes/workflows + routing map | **Yes** — reusable capabilities | You want the repo to *have* a coordinated set of project agents/recipes/workflows |
| `charter` | The **repository** | A durable **Charter** (team + work plan) | No — plans one delivery | You want a team design + work breakdown to execute a body of work |
| `spec` | One **feature idea** | A locked feature **spec** | No | You want one feature's requirements nailed down through dialogue |
| `sigil` (SKILL_GEN) | The **repository** | **One** project-local skill body | One skill | You want a single skill authored, not a coordinated suite |

Decision tree: coordinated *set* of reusable project tooling → `layer`. One skill body → `sigil`. Team + work plan for a delivery → `charter`. One feature's requirements → `spec`.

## Invocation Modes

| Form | Behavior |
|------|----------|
| `/nexus layer` (no args) | **Whole-repo mode**. Survey the repo, blueprint the full operating layer, confirm, delegate, verify. |
| `/nexus layer <scope>` | Scope the blueprint to a path/subsystem/domain. |
| `/nexus layer design-only` | Stop at the Operating-Layer Blueprint + delegation specs (no authoring, no registration) — charter-style inspect-before-commit. |
| `/nexus layer resume [<slug>]` | Resume from the persisted blueprint checkpoint. |
| `/nexus layer engines=<auto\|claude\|claude+codex>` | Engine policy for the Sigil-authoring fan-out in DELEGATE. Default `auto`. |

## Topology

```
Phase 0      Phase 1 (survey)              Phase 2          Phase 3     Phase 4 (delegate, parallel)        Phase 5
[Frame]      [Survey]                      [Design]         [Confirm]   [Delegate]                          [Verify]
┌────────┐   ┌──────────────────────────┐  ┌────────────┐   ┌────────┐  ┌──────────────────────────────┐    ┌─────────┐
│ detect │   │ loom (drive SURVEY)      │  │ loom       │   │ review │  │ sigil×N (author bodies 9+/12)│    │ loom    │
│ repo,  │──▶│  ‖ lens (structure)      │─▶│ blueprint: │──▶│ blue-  │─▶│ ‖ latch (hooks)              │ ──▶│ 14-item │
│ stack, │   │  ‖ atlas? (arch→topology)│  │ suite+rec- │   │ print  │  │ ‖ orbit (loop specs)         │    │ + sigil │
│ scope, │   │  + read .claude/ layer   │  │ ipes+work- │   │ (Con-  │  │ → nexus registers recipes/   │    │ 9+/12 + │
│ mode   │   │  + sigil inventory?      │  │ flows+map  │   │ firm)  │  │   workflows/routing map      │    │ single- │
└────────┘   └──────────────────────────┘  └────────────┘   └────────┘  │ ‖ grove (docs placement)     │    │ owner   │
                                                                          └──────────────────────────────┘    └─────────┘
                 ◀──────────── design-only stops here ──────────┘
```

Hub-and-spoke preserved: Nexus is the only orchestrator. Loom designs; the delegation fan-out spawns Sigil/Latch/Orbit specialists; Nexus registers. No direct agent-to-agent handoffs.

## Phases

**Phase 0 — FRAME** (no spawn). Detect repo type, stack, existing `.claude/` layer (skills/commands/recipes/hooks), scope, and mode (full vs design-only). Exit gate: stack + scope + mode + existing-layer inventory resolved.

**Phase 1 — SURVEY**. Loom drives; `lens` maps structure + feature inventory; `atlas` (conditional) supplies architecture for topology decisions; read `.claude/skills/` + recipes + `CLAUDE.md`/`AGENTS.md` directly, and consult Sigil's inventory when a prior run produced one. **Greenfield** (no `.claude/` layer): infer from manifests, CI, scripts, history — never block on Sigil's absence. Exit gate: recurring-task list grounded in repo reality; gaps flagged `UNKNOWN`, never fabricated.

**Phase 2 — DESIGN**. Loom authors the **Operating-Layer Blueprint**: coverage matrix (task → mechanism via `_common/MECHANISM_SELECTION.md` for hook/rule/subagent/skill; `recipe`/`workflow` are Loom-local), skill-suite plan, recipe set, workflow set (each with formal topology + `≤ 5` phases), and routing map (single-owner per task domain; ecosystem-owned tasks deferred, never duplicated). Exit gate: every recurring task has a mechanism + owner; intra-suite and ecosystem overlap < 30%.

**Phase 3 — CONFIRM** (**Confirm-before-launch; contract-level — AUTORUN cannot skip**). Present the blueprint. DELEGATE writes files and changes routing, so confirm before authoring; **Ask First** when the blueprint proposes 10+ skills or changes an existing project's established routing/conventions. `design-only` stops here and delivers the blueprint + delegation specs.

**Phase 4 — DELEGATE** (parallel). Sigil authors each skill body to its install paths (gate 9+/12; recraft 6-8 once per Sigil's own rule); Latch authors enforcement hooks; Orbit specs autonomous loops; Nexus registers the recipes/workflows/routing map; Grove places docs/recipes (skill install dirs are Sigil's, not Grove's). Loom authors nothing. Exit gate: every blueprint component has executed against its owner.

**Phase 5 — VERIFY**. Loom's 14-item blueprint checklist + each authored skill at 9+/12 + routing-map single-owner + every workflow formal-topology & `≤ 5` phases. On failure, return to the owning phase. Emit the Layer Report and ship.

## Output report

`NEXUS_COMPLETE` with the base `## Nexus Execution Report` **plus the named Operating-Layer Blueprint** (coverage matrix · suite plan · recipes · workflows + topology · routing map · delegation specs · overlap analysis). In `full` mode, append a **Layer Report** tail: skills authored (+ quality scores), recipes/workflows registered, hooks/loops delegated, and 14-item validation result. `design-only` delivers the Blueprint alone.

## Failure Modes Prevented

| Failure mode | Without `layer`'s gates | Prevented by |
|--------------|-------------------------|--------------|
| Generic, ungrounded tooling | Skills authored from a stack template, < 30% activation | Phase 1 grounds every component in an observed recurring task; gaps flagged `UNKNOWN` |
| Duplicating an ecosystem agent | A project skill re-does what Judge/Schema/etc. already own | Phase 2 routing map defers `≥ 30%`-overlap tasks to the existing owner; never duplicates |
| Bag-of-Agents workflows | A workflow ships with no topology / too many phases | Phase 2 requires formal topology + `≤ 5` phases per workflow; VERIFY rejects violations |
| Loom drifting into authoring | The designer writes skill bodies inline, no quality gate | Phase 4 delegates bodies to Sigil (9+/12); Loom authors nothing (its Never list) |
| Routing double-owner | Two skills/agents claim one task domain | VERIFY single-owner check on the routing map |
| Committing to a wrong layer | Authoring + routing changes land before review | Phase 3 Confirm-before-launch; `design-only` lets the user inspect the blueprint first |

## Scale & Cost

| Mode | Phases active | Approx agents | Cost |
|------|---------------|---------------|------|
| `design-only` | 0,1,2,(3 stop) | 3-6 (loom + lens + atlas? + verify) | Low |
| `full` | 0-5 | 5-15 (+ sigil×N authoring + latch?/orbit?) | Low-Medium |

Checkpoint-resume: with ≥ 4 phases, the blueprint persists at the CONFIRM boundary so an interrupted run resumes from the last checkpoint (`layer resume`).

## Shared protocols

- Loom's own design references own the method: `loom/reference/blueprint-method.md` (SURVEY/MAP), `loom/reference/recipe-design.md`, `loom/reference/workflow-design.md`, `loom/reference/validation-checklist.md` (the 14-item gate).
- `_common/MECHANISM_SELECTION.md` — hook/rule/subagent/skill mechanism choice (recipe/workflow are Loom-local, not in this file).
- `_common/SUBAGENT.md` — parallelism layer for a designed workflow.
- `reference/recipe-contract.md` — this recipe's authoring standard.

---

## Termination bound

No outer quality loop (**N/A** for the recipe shape — `layer` is design-then-delegate, not an iterate-to-rubric loop). The only bounded iteration is per-skill **recraft inside Sigil** (Sigil's own 6-8 → recraft-once rule); the recipe does not add an outer loop. For an iterate-to-a-quality-bar build, wrap with `converge`.
