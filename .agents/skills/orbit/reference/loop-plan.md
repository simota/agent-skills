# Orbit Loop Plan

Purpose: load this for the `plan` Recipe. The `plan` Recipe is **document-first** — it converts a goal into a durable markdown loop plan (`LOOP_PLAN.md`) and **stops at the document**. It generates no scripts and runs no loop. Pair it with `generate`, which consumes an approved `LOOP_PLAN.md` to produce the runnable script set.

`plan` is to `generate` what nexus `charter` is to `enact`: design and approval first, construction second.

## Contents

- [When to use](#when-to-use)
- [Output: LOOP_PLAN.md schema](#output-loop_planmd-schema)
- [Phase contract](#phase-contract)
- [Quality gates before delivery](#quality-gates-before-delivery)
- [pdm sprint → plan unit](#pdm-sprint--plan-unit)
- [plan → generate handoff](#plan--generate-handoff)

## When to use

Use `plan` when the user wants the loop **designed and reviewable** before any script exists:

- a goal needs hardening into ACs, tier, resilience config, and escalation paths, captured as a reviewable artifact
- the loop will run unattended and the operator wants to sign off on terminators, budget caps, and bounded-autonomy limits first
- a pdm plan item / WBS leaf should be recorded as a self-contained loop design others can read
- a pdm **sprint** must become a reviewable multi-loop plan before any loop runs (see [pdm sprint → plan unit](#pdm-sprint--plan-unit))

Do **not** use `plan` when:

- the user wants a runnable loop now → `generate`
- only the contract needs hardening (no full loop design) → `contract`
- a live loop must be assessed or repaired → `audit` / `recover`

## Output: `LOOP_PLAN.md` schema

Write one markdown document. Default path: `LOOP_PLAN.md` in the target `loop_dir` (or repo root when none is given). Numbered sections, every claim measurable or explicitly deferred to `generate`.

| § | Section | Required content |
|---|---------|------------------|
| §1 | Goal & Why | one-line objective, why it matters, expected end state |
| §2 | Operation Contract | `3-6` measurable ACs, **each mapped to a machine-checkable verify command**; out-of-scope notes; ≥ 1 external terminator (`LOOP_TIMEOUT` and/or `USD_PER_RUN_CAP`) — never `MAX_ITERATIONS` alone for unattended runs (`operation-contract.md`) |
| §3 | Loop Tier & Defaults | selected Loop Tier + the Core Defaults that deviate from baseline (`MAX_ITERATIONS`, `LOOP_TIMEOUT`, `USD_PER_RUN_CAP`, `CIRCUIT_THRESHOLD`, `DEDUP_WINDOW`) with rationale (`core-defaults.md`) |
| §4 | Script Set Design | which scripts `generate` will emit (`bootstrap.sh` / `run-loop.sh` / `recover.sh` / `verify.sh` / `notify.sh`), executor engine (`EXEC_CMD`), commit convention, branch policy / `AUTOCOMMIT` — **described, not generated** (`script-templates.md`, `executor-engines.md`) |
| §5 | Resilience & Bounded Autonomy | retry+timeout+circuit-breaker as one unit; idempotency keys for effectful calls; memory-pointer for outputs > 1KB; escalation paths; audit trail; staged-autonomy rollout level (`resilience-patterns.md`) |
| §6 | Verification & DONE Gate | AC→verify mapping table; placeholder-grep / mutation / `CRITIC_MODEL` plan; rollback note requirement (`operation-contract.md` DONE Evidence Gate) |
| §7 | Risk & Failure-Class Anticipation | likely failure classes (`STATE_DRIFT`, `VERIFY_GAP`, `REWARD_HACK`, `BURN_RATE_ANOMALY`, …) with pre-planned mitigations (`failure-catalog.md`) |
| §8 | Next Step | explicit `plan → generate` handoff: what `generate` consumes, open questions, sign-off checklist |

Keep §4 design-level: name engines, conventions, and policies, but emit no script bodies — that is `generate`'s job.

## Phase contract

Within the standard workflow `INTAKE → CONTRACT → CLASSIFY → PRE_FLIGHT → GENERATE_OR_AUDIT → VERIFY → HANDOFF → COMPLETE → LEARN`, `plan` specializes:

- `INTAKE` — classify as `GENERATE` (plan-only); confirm the deliverable is a document, not a runner.
- `CONTRACT` — author §1–§2 (this is the heaviest phase; reuse `vague-goal-handling.md` AC templates when the goal is weak).
- `CLASSIFY` — no live loop to classify; instead anticipate failure classes for §7.
- `PRE_FLIGHT` — lightweight: confirm target `loop_dir` is writable; no `.run-loop.lock` / disk gates (no execution).
- `GENERATE_OR_AUDIT` — author §3–§8 of `LOOP_PLAN.md`. **No `*.sh` produced.**
- `VERIFY` — run the [quality gates](#quality-gates-before-delivery) on the document; no `bash -n` (no scripts).
- `HANDOFF` — recommend `generate` as the next step (or `contract` if §2 is still weak).
- `COMPLETE` / `LEARN` — emit the footer contract; fire `RF-01`.

## Quality gates before delivery

Block delivery of `LOOP_PLAN.md` until all pass:

| Gate | Rule | On fail |
|------|------|---------|
| AC-oracle completeness | every §2 AC resolves to a verify command | strengthen via `vague-goal-handling.md` before delivering |
| Terminator bound | §2 declares ≥ 1 of `LOOP_TIMEOUT` / `USD_PER_RUN_CAP` | reject; require an explicit bound for unattended runs |
| Measurability | no AC uses generic verbs without a numeric/boolean threshold | apply Three-Hypothesis Protocol |
| Scope guard | §4 names engine, commit convention, and branch policy explicitly (no TODO placeholders) | resolve before delivery |
| No execution leakage | document contains no generated script bodies and triggers no loop run | remove; defer to `generate` |

## pdm sprint → plan unit

A pdm **sprint** maps **1:1 to one `LOOP_PLAN.md`** — the sprint *is* the plan unit. This sits one level above the existing **pdm WBS leaf → one loop goal** (`goal.md`) mapping, which is preserved and nested inside the plan.

| pdm unit | Orbit unit | Recipe |
|----------|-----------|--------|
| Sprint (goal + leaves + exit criteria) | Plan unit (`LOOP_PLAN.md`, multi-loop design) | `plan` |
| WBS leaf / gap item | Loop goal (`goal.md`, single loop) | `generate` / `contract` |

Consume the sprint via `PDM_TO_ORBIT_HANDOFF` with `scope: sprint`. pdm is read-only: it supplies the sprint goal, the sized loop-ready WBS leaves, and the sprint exit criteria; Orbit authors the plan, ACs, and contracts. Map the sprint into `LOOP_PLAN.md` as a **multi-loop plan**:

- sprint goal → §1 plan objective and §6 plan-level DONE gate (sprint exit criteria)
- each sprint WBS leaf → one **constituent loop goal** listed in §2/§4 (one objective + 3-6 candidate ACs), preserving the leaf→loop-goal 1:1 rule
- inter-leaf dependencies → §4 loop sequencing (parallel / sequential / loop-of-loops per the SKILL **Multi-Loop Rules**); keep separate `state.env` / `progress.md` per constituent loop
- sprint-level risks → §7 failure-class anticipation

Then each constituent loop goal flows to `generate` (or `contract` first when its ACs are still weak) at the existing single-loop granularity. The sprint plan is the design; the per-leaf loops are its realization. When a pdm leaf is itself too large for one loop, split it into loop-sized constituent goals at §2 rather than overloading a single loop.

## `plan → generate` handoff

`generate` treats an approved `LOOP_PLAN.md` as its input contract:

- §2 → `goal.md` (ACs, terminators, out-of-scope)
- §3 → Core Defaults overrides in `state.env` / runner config
- §4 → which templates to emit and how to configure `EXEC_CMD`, commit convention, branch policy
- §5–§7 → resilience wiring (circuit breaker, idempotency, escalation, critic gate) in the generated scripts

If §2 fails an AC-oracle or measurability gate at `generate` time, route back to `contract` before generating. The plan is design intent; `generate` is its faithful, runnable realization.
