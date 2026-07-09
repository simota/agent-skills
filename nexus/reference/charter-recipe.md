# Nexus Charter Recipe Reference

**Purpose:** Comprehensively analyze a repository and author a **self-contained team Charter** — including the team-construction design — that a development team can self-drive from. Charter **stops at the document**; execution is a separate recipe (`enact`).
**Read when:** User invokes `/nexus charter`, or asks to "analyze the whole repo and produce an instruction document (with team design) a team can run autonomously". For *running* a Charter, see `reference/enact-recipe.md`.

## Contents
- Overview
- The charter → enact split
- Charter vs Apex vs Goal (disambiguation)
- Invocation Modes
- Topology
- Phase 0: Framing
- Phase 1: Comprehensive Repository Analysis
- Phase 2: Objective & Work Breakdown
- Phase 3: Charter Authoring
- Engine Assignment (multi-engine orchestration)
- Charter Document Schema
- Conditional Inclusion
- AUTORUN Chain Template
- Failure Escalation
- Cost and Latency Profile

---

## Overview

Charter is the **repo-centric, document-first planning** recipe. It reads the entire repository, distills a durable Charter artifact (`docs/CHARTER.md`), and **designs the team that will execute it** — but does not build or run that team. The Charter is the deliverable: a single self-contained operating manual that encodes everything a development team needs to run without further human design — repo map, conventions, mission, work breakdown, **role→skill roster + spawn config**, orchestration plan, verification gates, and escalation rules.

Two properties make Charter distinct:

1. **The team is *designed into* the document.** Phase 3 authors a roster (§5) and orchestration plan (§6) so the team is a pure function of the Charter — `enact` (or a fresh Nexus session) reconstructs the identical team by reading the same file. This is what "a self-driving instruction document" means: the document is the source of truth; the team is derived from it.
2. **Comprehensive analysis is the foundation.** Phase 1 is a full multi-axis sweep (structure, architecture, history, conventions, debt, risk) that grounds every roster and work-package decision in repo reality, so the Charter is buildable rather than aspirational.

Charter is **not** a default recipe. It is opt-in when the deliverable is *the plan including who runs it* — onboarding a new initiative into an existing codebase, or producing a reusable team runbook that outlives the session.

## The charter → enact split

Planning and execution are deliberately two recipes:

| Recipe | Does | Produces | Cost |
|--------|------|----------|------|
| `charter` | Analyze repo + author the Charter (team design included) | `docs/CHARTER.md` + `CHARTER.roster.yaml` | Low-Medium |
| `enact` | Read a Charter, construct the team from §5, orchestrate §4 end-to-end | Shipped work + updated Charter | Medium-High |

The split lets a user pay for authoring first, **inspect/edit the Charter**, then commit to execution separately via `enact docs/CHARTER.md` — and re-run the same team later at execution-only cost. Charter never spawns execution agents; it only spawns analysis/authoring agents.

## Charter vs Apex vs Goal (disambiguation)

| Recipe | Starts from | Primary artifact | Runs the work? | Best when |
|--------|-------------|------------------|----------------|-----------|
| `apex` | A goal/feature (discovered or supplied) | Shipped feature | Yes (one chain) | One high-stakes customer-facing feature, discovery→ship in one shot |
| `charter` | The **repository** (full analysis) | A durable **Charter** incl. team design | **No** — design only | You want a reusable, inspectable operating manual + team design before committing to a run |
| `enact` | An existing **Charter** | Shipped work | Yes | Execute a `charter` (or hand-written Charter) end-to-end |
| `goal` | A long-running objective | Loop config (no code exec) | No | Configure `/goal` autonomous loop only |

Route to `apex` when the unit of work is a single feature and you want one-shot discovery→ship. Route to `charter` when you want the analysis + a durable, inspectable team design first; then `enact` to run it.

## Invocation Modes

| Form | Behavior |
|------|----------|
| `/nexus charter` (no args) | **Autonomous mode**. Analyze repo, discover the highest-value body of work (Phase 2 propose+prioritize), author the Charter (incl. team design), deliver. |
| `/nexus charter <objective>` | **Objective-supplied mode**. Analyze repo, author the Charter scoped to the supplied objective, deliver. |
| `/nexus charter scope=<lite\|standard\|full>` | Analysis + Charter depth. Default `standard`. |
| `/nexus charter out=<path>` | Charter output path. Default `docs/CHARTER.md` (durable, committable). |
| `/nexus charter engines=<auto\|claude+codex\|claude\|all>` | Engine policy the §5/§6 design targets. Default `claude+codex` (multi-engine). See **Engine Assignment**. |

Charter always stops after authoring. To run the result: `/nexus enact <out path>`.

## Topology

```
Phase 0          Phase 1 (parallel sweep)                Phase 2              Phase 3              DELIVER
[Framing]        [Comprehensive Repo Analysis]           [Objective+WBS]      [Charter Authoring]
┌──────────┐     ┌─────────────────────────────────┐     ┌──────────────┐     ┌────────────────┐   ┌──────────────┐
│ detect   │     │ lens   (structure/data-flow)    │     │ spark+rank?  │     │ scribe +accord │   │ docs/CHARTER  │
│ repo type│ ──▶ │ atlas  (arch/deps/debt/ADR)     │ ──▶ │  (autonomous)│ ──▶ │ (trace)        │ ─▶│ .md           │
│ stack,   │     │ grove  (repo/docs layout)       │     │ sherpa (WBS) │     │ + design team  │   │ + roster.yaml │
│ size,    │     │ trail  (history/hotspots)       │     │ accord (AC)  │     │   §5 roster    │   │ → handoff to  │
│ scope,   │     │ sentinel? canon? sweep? pulse?  │     │ magi? omen?  │     │   §6 orch plan │   │   `enact`     │
│ out path │     │ + read CLAUDE/AGENTS/README     │     │ ripple?      │     │ → write files  │   └──────────────┘
└──────────┘     └─────────────────────────────────┘     └──────────────┘     └────────────────┘
                                                  ◀──────── Failure escalation (back to originating phase) ──────┘
```

Hub-and-spoke is preserved: Nexus is the only orchestrator. Charter spawns only analysis/authoring specialists. The Charter's §5 *nominates* sub-orchestrators (Vision/Orbit/Rally) for execution clusters, but they are instantiated later by `enact`, not here.

## Phase 0: Framing

**Purpose:** Establish what is being chartered and how deep to go. No spawn — Nexus-internal detection.

| Detect | Source | Use |
|--------|--------|-----|
| Repo type / stack | file tree, manifest files (`package.json`, `Cargo.toml`, `pyproject.toml`, `go.mod`, …), CI config | Selects which Phase 1 analyzers fire and which skills are eligible for the roster |
| Repo size / maturity | LOC, module count, git age, test presence | Sets `scope` default (lite/standard/full) and analysis breadth |
| Objective | user arg, or `autonomous` if none | Branches Phase 2 (supplied vs propose+prioritize) |
| Conventions sources | `CLAUDE.md`, `AGENTS.md`, `GEMINI.md`, `README`, `.agents/PROJECT.md`, `_common/GIT_GUIDELINES.md` | Seeds the Charter's Conventions & Guardrails section |
| Output path | `out=` or default `docs/CHARTER.md` | Where the durable Charter is written |

**Exit gate:** repo type + stack + scope + objective-mode + out-path resolved.

## Phase 1: Comprehensive Repository Analysis

The **comprehensive-analysis** foundation. Parallel multi-axis sweep; each analyzer owns one lens and returns a structured section. Reconverge into a **Repository Intelligence Report** — the single grounding input for Phase 2-3.

| Agent | Lens | Required | Output section |
|-------|------|----------|----------------|
| `lens` | Codebase comprehension: structure map, feature inventory, data-flow tracing, module responsibilities | Yes | Structure & feature map |
| `atlas` | Architecture: dependency graph, circular refs, God Classes, module boundaries, tech-debt + ADR/RFC seeds | Yes | Architecture & debt |
| `grove` | Repo & docs layout audit: directory design, `docs/` (PRD/specs/ADR), test/script organization, anti-patterns | Standard+ | Layout & docs health |
| `trail` | Git archaeology: history, churn hotspots, regression-prone areas, ownership signals | Standard+ | History & hotspots |
| `sentinel` | Static security baseline: secrets, injection surfaces, dependency CVEs | Conditional: security-sensitive repo | Security baseline |
| `canon` | Standards-compliance gap (OWASP/WCAG/OpenAPI/ISO 25010) | Conditional: full scope | Compliance gaps |
| `sweep` | Dead code, unused/orphaned files | Conditional: full scope | Cleanup signals |
| `pulse` | KPI/metric + test-intelligence signals (flake/coverage) if integrated | Conditional | Health metrics |

Nexus-internal (no spawn): read and summarize `CLAUDE.md` / `AGENTS.md` / `README` / `.agents/PROJECT.md` into the Conventions seed.

**Exit gate:** Repository Intelligence Report covers — structure, architecture, conventions, dependencies, test/coverage posture, debt, security baseline (if applicable), and history. Gaps flagged as `UNKNOWN` rather than guessed (do not fabricate; verify before asserting).

## Phase 2: Objective & Work Breakdown

Turn analysis (+ objective) into a prioritized, decomposed, acceptance-bounded plan.

| Agent | Role | Required |
|-------|------|----------|
| `spark` | Propose candidate bodies of work from the Intelligence Report | Autonomous mode only |
| `rank` | Score candidates (ICE/RICE/WSJF) and select the chartered scope | Autonomous mode only |
| `sherpa` | Decompose chartered scope into atomic steps / work packages (<15 min each), with dependencies + sequencing | Yes |
| `accord` | Requirements (L0→L3) + measurable acceptance criteria + traceability per work package | Yes |
| `magi` | Arbitrate scope/approach when candidates or decompositions conflict | Conditional: ambiguity / tie |
| `omen` + `ripple` | Pre-mortem (FMEA/RPN) + blast-radius for the planned work → embedded as Charter risk gates | Conditional: full scope or high reversibility cost |

**Exit gate:** every work package has (1) an atomic step list, (2) measurable AC, (3) dependency/sequence position, (4) — provisionally — a recommended owner skill (finalized as the §5 roster in Phase 3). Autonomous mode additionally carries the selected scope + rejected alternatives.

## Phase 3: Charter Authoring

Synthesize Phases 1-2 into the **Charter document** — the self-contained operating manual, including the team-construction design. Authored by `scribe` with `accord` supplying traceability; `void` optionally trims scope (full mode).

The Charter MUST be **self-driving**: a reader (human, `enact`, or a fresh Nexus session) can construct the team and execute every work package from the document alone, without re-running analysis. This self-containment check is the reader-path test of `reference/doc-quality-protocol.md` (W12, reader = `enact`/the executing team); the Charter also follows its grounding (W4-W5 — Phase 1's `UNKNOWN`-over-guessing rule), coherence (W8-W9, terms follow the repo's vocabulary), and freshness (W3: as-of + review trigger) rules. Write it to `out` (default `docs/CHARTER.md`) and a machine-readable companion (`docs/CHARTER.roster.yaml`) holding the roster + orchestration plan for `enact` re-entry.

**Team-construction design (not execution).** Phase 3 finalizes §5 (roster: per work package, owner skill + model tier + engine + spawn config) and §6 (orchestration plan: chain order, parallel branches + file ownership, checkpoints, **per-package engine assignment**). It does **not** verify spawn prereqs or instantiate agents — that is `enact` Phase 1.

**Exit gate:** Charter passes the self-containment check — roster, work breakdown, AC, conventions, orchestration plan, and verification gates are all present and mutually consistent; every work package maps to exactly one owner skill that exists in the ecosystem, and every package carries an engine assignment; and §10 checklists (pre-flight incl. team-readiness, per-package DoD, progress tracker, final delivery) are generated from §3+§4+§7 (team-readiness cross-references §1/§2/§5/§6) with one DoD block and one tracker row per §4 package. Then DELIVER the Charter and hand off to `enact` (recommend the `/nexus enact <out path>` command in `NEXUS_COMPLETE`).

## Engine Assignment (multi-engine orchestration)

The Charter is **multi-engine by default** (`engines=claude+codex`). Phase 3 assigns each §5 work package a runner engine in §6 so `enact` spawns it on the right CLI. This applies the Plan-and-Execute pattern across engines (SKILL.md Core Contract): capable models plan/design, cheaper or coding-tuned engines execute.

| Work-package class | Default engine | Why |
|--------------------|----------------|-----|
| Analysis, architecture, spec, design, review, decision | **Claude Code** (Agent tool) | Planning/judgment quality; native to the hub |
| Build loops + high-volume parallel coding (multi-iteration implementation, test authoring, codemods) | **Codex CLI** (`spawn_agent` → `wait_agent`), model **`gpt-5.6-terra`** (C3.0 variant tiering: sol=plan/design, terra=implementation, luna=rote) | Fresh context per iteration avoids context rot; tuned for autonomous coding cycles; explicit `spawn_agent`/`close_agent` lifecycle makes parallel file-ownership/branch isolation cheap — same rationale as Apex Phase 6 |
| Optional third axis (cross-engine triangulation, extra parallel capacity) | **agy** (`/agent` / `agy -p`) when AVAILABLE | Perspective diversity; only when `engines=all` and prereqs hold |

**Authoring rules:**
- Tag every §5 roster entry with `engine:` and a `model`/`effort`. **Codex packages pin the role-matched gpt-5.6 variant** — `gpt-5.6-terra` for build/implementation packages, `gpt-5.6-sol` for plan/design-critical ones, `gpt-5.6-luna` for rote high-volume ones; never a previous generation (latest-generation mandate `_common/CODEX_ORCHESTRATION.md` C3.0; tune depth within a variant via `effort`/`model_reasoning_effort`). Claude tiers and agy `/model` per `reference/hub-authoring.md` § Model Selection.
- Where §5 nominates **Orbit** for a build loop, pin its sub-hub engine to **Codex CLI** (Orbit drives `spawn_agent` per iteration), mirroring Apex.
- Record per-engine **prerequisites** in §6 so `enact` Phase 1 can verify them: Codex needs `multi_agent = true` + `[agents] max_depth ≥ 2` (`reference/execution-layers.md`, `_common/CLI_COMPATIBILITY.md §9`); agy needs a TTY/real-pty headless path.
- Specify a **fallback** per Codex/agy package (`fallback_engine: claude-code`) so `enact` degrades gracefully when an engine is unreachable instead of hard-failing — and note the cost/throughput trade-off the fallback implies.
- `engines=claude` forces single-engine (no Codex) when the environment cannot reach Codex; `engines=all` adds agy as a third axis; `engines=auto` lets Phase 3 pick per detected availability, defaulting to `claude+codex`.

## Charter Document Schema

The Charter (`docs/CHARTER.md`) contains these sections; the companion `CHARTER.roster.yaml` mirrors §5-§6 machine-readably.

```
§1 Mission & Objectives      goal statement, success definition, non-goals
§2 Repository Map            structure, architecture summary, key modules, data flows  (from Phase 1)
§3 Conventions & Guardrails  commit style, test/lint/build/typecheck commands, coding
                             standards, branch policy, L4/destructive-action rules     (from Phase 0/1)
§4 Work Breakdown            epics → atomic steps, dependencies, sequencing, AC per
                             package, traceability IDs                                  (from Phase 2)
§5 Team Roster               per work package: owner skill + model tier +
                             engine (claude-code|codex-cli|agy) + fallback_engine +
                             spawn config + context envelope; sub-orchestrator
                             nominations (Vision/Orbit/Rally) where a cluster needs one
§6 Orchestration Plan        chain order, parallel branches + file ownership,
                             checkpoints, max-hop limits, aggregation strategy,
                             per-package engine assignment + per-engine prerequisites
                             (multi-engine: Claude Code plan/design, Codex CLI build loops)
§7 Verification Plan         per-package + final gates (tests/build/security/AC checks)
§8 Escalation & Rollback     failure tiers, circuit-breaker, rollback boundaries,
                             human-confirm triggers
§9 Execution Log             (empty at authoring; during execution `enact` keeps this as
                             a pointer + summary and streams the timeline to an append-only
                             run-log file, default `docs/CHARTER.run.log.md`)
§10 Checklists & Trackers    pre-flight checklist (run prerequisites); per-package
                             Definition-of-Done checklist (AC met + tests + lint/build/
                             typecheck + review + docs, derived from §3+§4); progress
                             tracker (one checkbox per §4 package); final delivery
                             checklist (§7 gates + ship readiness + rollback ready)
```

§10 makes the Charter actionable and self-tracking: the **pre-flight** and **DoD** checklists give `enact` (and a human) an explicit, testable gate at each boundary instead of prose judgment, and the **progress tracker** is the at-a-glance status surface (checkboxes `enact` ticks at each `PKG_DONE`, complementing the append-only run log). Author each checklist item as a concrete, verifiable assertion (command to run, file to exist, gate to pass) — not a vague "looks done".

§10 template (GitHub-flavored checkboxes so they render and tick in-place):

```markdown
### Pre-flight
- [ ] Charter §1-§8 present and self-consistent
- [ ] Every §4 package maps to a constructable §5 owner skill
- [ ] Engine prereqs met (Codex `max_depth ≥ 2`) or `fallback_engine` set
- [ ] Working tree clean; branch per §3 policy

### Team readiness (human-agent teaming — 5 diagnostic questions)
Derived from the human-agent-team diagnostic [Source: claude.com/blog/building-effective-human-agent-teams]. Each item is a cross-reference to the Charter section that must already answer it — a failed item means that section is under-specified, not a new work package.
- [ ] **Information public & searchable** — every fact an owner/agent needs to act is in the Charter or a path it cites (§2 repo map, §3 conventions); no load-bearing knowledge lives only in a human's head or an unsearchable channel (§1·L1)
- [ ] **Roster written, ownership unambiguous** — every team member (human + agent) and what they own is named; every §4 package maps to exactly one §5 owner (§5·L2)
- [ ] **Tool/engine access matches the job** — each §5 owner has the engine + tool access its package requires; prereqs met or `fallback_engine` set (§5/§6·L2)
- [ ] **Verification rubric or test exists** — every package has a testable gate, not prose judgment (§7 + §10 DoD·L4)
- [ ] **North Star referenced** — §1 Mission is an ambitious, written goal every owner can point to, and at least one owner is tasked to propose North-Star-aligned work proactively (§1·L3)

### Per-package DoD (one block per §4 package, instantiated from §3 commands)
- [ ] PKG-<id>: acceptance criteria (§4) met
- [ ] PKG-<id>: tests added/updated and green (`<§3 test cmd>`)
- [ ] PKG-<id>: lint + typecheck + build pass (`<§3 cmds>`)
- [ ] PKG-<id>: reviewed (judge) / docs updated if public surface changed

### Progress tracker (one row per §4 package)
- [ ] PKG-001 <title> — owner <skill> — status: pending
- [ ] PKG-002 <title> — owner <skill> — status: pending

### Final delivery
- [ ] All §7 gates pass (or failures reported honestly)
- [ ] No SKIPPED package is release-critical (else flagged in DELIVER)
- [ ] Run log RUN_END written; Charter §9 pointer current
- [ ] Rollback plan (§8) ready; launch artifacts (if in scope) prepared
```

§5 + §6 make the team a pure function of the document. Each §5 entry is a ready-to-use spawn spec aligned to the Agent Spawn Template (SKILL.md) — role → skill SKILL.md path, model tier, engine, acceptance criteria, output envelope — so `enact` can construct the team without re-deriving anything.

## Conditional Inclusion

| Condition | Add | Skip |
|-----------|-----|------|
| Autonomous (no objective) | spark, rank in Phase 2 | — |
| Objective supplied | — | spark, rank |
| `scope=lite` | — | grove, trail, canon, sweep; accord at Lite threshold |
| `scope=full` | canon, sweep, omen+ripple, void | — |
| Security-sensitive repo | sentinel (P1) | — |

## AUTORUN Chain Template

```
# ── Autonomous mode (no objective) ───────────────────
Nexus AUTORUN charter
  ── Phase 0 Framing ──────────────────────────────────
  → detect(repo_type, stack, size, scope, out_path); objective = autonomous
  ── Phase 1 Comprehensive Analysis (parallel) ────────
  → [parallel] lens(structure+dataflow)
            ‖ atlas(arch+deps+debt+ADR)
            ‖ grove(layout)?       ‖ trail(history)?
            ‖ sentinel(sec)?       ‖ canon(std)? ‖ sweep(dead)? ‖ pulse(health)?
  → internal: read CLAUDE/AGENTS/README/PROJECT → conventions seed
  → reconverge → Repository Intelligence Report
  ── Phase 2 Objective & WBS ──────────────────────────
  → spark(propose) → rank(ICE/RICE select)        # autonomous only
  → sherpa(atomic step WBS) → accord(AC + trace)
  → magi(arbitrate)? → omen+ripple(risk gate)?
  ── Phase 3 Charter Authoring (incl. team design) ────
  → scribe(+accord trace, void? full)
       → finalize §5 roster + §6 orchestration plan
       → assign engine per package: Claude Code (plan/design/review)
         ‖ Codex CLI model=gpt-5.6-terra (build loops + high-volume parallel
           coding; Orbit sub-hub pinned to Codex) ‖ agy? (engines=all)
       → record per-engine prereqs + fallback_engine in §6
       → write docs/CHARTER.md + CHARTER.roster.yaml
  → [self-containment check]
  ── DELIVER ──────────────────────────────────────────
  → NEXUS_COMPLETE(charter_path) + recommend `/nexus enact docs/CHARTER.md`


# ── Objective-supplied mode ──────────────────────────
Nexus AUTORUN charter "<objective>"
  → Phase 0-1 same; Phase 2 skips spark+rank (objective bound directly)
  → Phase 3 + DELIVER identical
```

## Failure Escalation

| Failure | Detected by | Escalation |
|---------|-------------|------------|
| Phase 1 analyzer can't read a subsystem | lens/atlas | Flag section `UNKNOWN`, continue; never fabricate |
| Phase 2 no worthwhile work (autonomous) | rank | Present top candidates or abort, suggest explicit objective |
| Phase 2 scope/approach tie | magi | Pause for human verdict |
| Phase 3 self-containment check fails | scribe/accord | Re-author missing sections before DELIVER |
| Phase 3 a work package has no constructable owner skill | scribe | Re-scope or flag the gap in §5 (so `enact` does not hit an unresolvable roster) |
| Risk gate No-Go | omen/ripple | Return to Phase 2 (re-scope) |

## Failure Modes Prevented

Consolidated view of what charter's analysis-grounding and self-containment gates guard against — a summary surface over the **Failure Escalation** table above (the per-row escalation rules remain the source of truth). Because charter **stops at the document and runs no execution** (`reference/recipe-contract.md` §3: no execution → **no confirm gate**), the failures it prevents are *authoring* failures that would otherwise surface expensively downstream in `enact`.

| Failure mode | Without charter's gates | Prevented by |
|--------------|-------------------------|--------------|
| Aspirational, unbuildable plan | A Charter assumes repo facts that aren't true | Phase 1 comprehensive analysis grounds every roster/work-package decision in repo reality; gaps flagged `UNKNOWN`, never fabricated |
| Charter that can't self-drive | A reader (or `enact`) must re-run analysis to act | Phase 3 self-containment check — roster, WBS, AC, conventions, orchestration plan, gates all present and mutually consistent before DELIVER |
| Unresolvable roster downstream | `enact` Phase 1 hits a work package with no constructable owner | Self-containment check: every §4 package maps to exactly one owner skill that exists in the ecosystem; gap re-scoped/flagged in §5 here, not at run time |
| Engine assumptions fail silently at run | `enact` can't reach the assigned engine and hard-fails | §6 records per-engine prereqs + a `fallback_engine` per Codex/agy package so `enact` degrades gracefully instead of hard-failing |
| Building the wrong body of work (autonomous) | Charter scopes low-value work | Phase 2 spark + rank (ICE/RICE/WSJF) select the chartered scope; no worthwhile work → present candidates or abort |
| Scope/approach deadlock | Conflicting decompositions stall authoring | Phase 2 magi arbitration; risk-gate No-Go returns to Phase 2 re-scope |
| Untrackable execution | `enact` has no objective gate, only prose judgment | §10 checklists generated from §3+§4+§7: pre-flight, per-package DoD, progress tracker, final delivery — testable gates `enact` ticks |

## Cost and Latency Profile

| Profile | Phases active | Approx agent count | Approx cost |
|---------|---------------|--------------------|-------------|
| lite | 0, 1(core), 2, 3 | 5-8 | Low |
| standard | 0, 1, 2, 3 | 7-11 | Low-Medium |
| full (autonomous + risk gate) | All + spark/rank + canon/sweep + omen/ripple + void | 10-15 | Medium |

Charter only spawns analysis/authoring agents, so it stays cheap relative to `enact`. The durable Charter means the user reviews the Charter before paying for execution — and the same Charter can drive `enact` repeatedly.

---

## Visualization

Topology ASCII above. The Charter document (`docs/CHARTER.md`) is the human-facing artifact; `CHARTER.roster.yaml` is the machine-readable team/orchestration spec consumed by `enact`.
