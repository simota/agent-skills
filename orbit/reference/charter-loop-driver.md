# Orbit — Charter-Driven Loop Driver (nexus enact integration)

**Purpose:** Make Orbit Charter-native when `nexus enact` delegates a **build-loop work package**, so the loop gates on the Charter's Definition-of-Done, writes to the Charter's run-log, and resumes with it. This is a driver integration (same shape as the apex Phase 6 / summit Phase 5 drivers), **not** a copy of the `charter` / `enact` recipes — Orbit stays a spoke; `enact` stays the hub.

**Read when:** Orbit receives an `_AGENT_CONTEXT` / `## NEXUS_ROUTING` delegation from `nexus enact` for a multi-iteration implementation package, or a goal references a Charter (`docs/CHARTER.md` + `CHARTER.roster.yaml`).

## Why a driver, not a recipe

`charter` (repo analysis → instruction document) and `enact` (team construction → multi-package orchestration → ship) are **hub-shaped** meta-orchestration — decompose, route, aggregate. Orbit is **loop-shaped** — iterate one unit of work until an external gate says DONE. Cloning `charter`/`enact` into Orbit would make Orbit a second hub (violating both `nexus` hub-spoke and Orbit's own *"never replace Nexus orchestration responsibilities"*) and create an `enact → orbit → enact` cycle, since `enact` already delegates build loops to Orbit. The right seam to close is narrow: teach Orbit to read the Charter slice it is handed and integrate with the Charter's DoD gate + run-log.

## Input: the Charter slice (read-only)

`enact` passes a **slice** of the Charter for the one package being looped — never the whole document, never other packages.

| Charter section | Orbit use |
|-----------------|-----------|
| §4 work package (this one) | goal + atomic steps + per-package AC → Orbit operation contract |
| §5 roster entry | owner skill + model tier + **engine** (Codex CLI always uses the latest gpt-5.6 generation, variant by role — sol=plan/design, terra=implementation, luna=rote; latest-generation mandate `_common/CODEX_ORCHESTRATION.md` C3.0) + `fallback_engine` |
| §7 verification plan (package-scoped) | `verify.sh` / DONE-gate commands |
| §10 per-package DoD checklist | the **external DONE gate** (see below) |
| §3 conventions + §9 run-log path | commit/test/lint/build commands; where to append events |

These sections are **sha256-pinned at loop start** (Orbit AP-13 / AP-16 / AP-20 immutability rule): Orbit consumes them read-only and never edits §4/§5/§7/§10. It appends only to the §9 run-log and its own loop artifacts.

## DONE gate = §10 DoD (not agent self-assessment)

Orbit already forbids agent self-assessment for termination and requires an external gate + independent critic. Under a Charter-driven loop, the external DONE gate **is the §10 per-package DoD checklist**:

- Loop is `DONE`/`SUCCESS` only when **every** DoD item passes (AC met + tests green + lint/build/typecheck + review).
- Partial pass → `PARTIAL`; unrecoverable after the recovery ladder → hand back to `enact` as `SKIPPED(blocked, reason)`.
- This composes with Orbit's existing `CRITIC_MODEL` gate and `PLACEHOLDER_GREP` / mutation checks — DoD is the contract, the critic is the independent verifier of it.

## Run-log: append in enact's §9 vocabulary

Beyond Orbit's own `progress.md` (loop mechanics), Orbit **also appends to the enact append-only run-log** (default `docs/CHARTER.run.log.md`) for the package it owns, using enact's event names:

- `PKG_START` at loop entry (pkg id, owner skill, engine)
- `PKG_RECOVER` per recovery-ladder step (retry / `fallback_engine` / Scout+Builder / alt-owner)
- `PKG_DONE` at terminal (`SUCCESS` | `PARTIAL` | `SKIPPED`) with the DoD result

Append-only, one line per event, written immediately, atomic (temp-then-rename). Two layers, deliberately separate: **Orbit loop state** (`state.env` / `progress.md`) = mechanics for Orbit's own resume; **enact run-log** = the package-level timeline the hub reads.

## Two-level resume

- `enact` resumes the **run** from the run-log tail (last `PKG_DONE`); a package already `PKG_DONE` is skipped.
- Orbit resumes the **loop** for an in-flight package from its own checkpoint (`state.env`, durable execution / checkpoint-replay).
- On `enact resume`, a package interrupted mid-loop is re-handed to Orbit, which replays from its last loop checkpoint — no work repeated, no re-confirmation.

## Engine

Build-loop packages run on the engine §5 assigns — **Codex CLI model `gpt-5.6-terra`** (role-matched variant of the latest generation — build loops=terra, plan/design=sol, rote=luna; never a previous generation — latest-generation mandate `_common/CODEX_ORCHESTRATION.md` C3.0; tune depth within the variant via `model_reasoning_effort`). Run the Codex engine-availability check (`agents.max_depth >= 2`, `spawn_agent`/`wait_agent`/`send_input`/`resume_agent`/`close_agent` permitted) before consuming the contract, exactly as apex Phase 6. If unreachable, apply the package `fallback_engine` and log the substitution as `PKG_RECOVER` (no silent fallback).

## Boundaries (hub-spoke preserved)

- Orbit drives **one** work package's loop. It does **not** construct the team, route other packages, or read the whole Charter — `enact` owns all of that.
- No `orbit → enact → orbit` recursion: Orbit reports terminal status back to `enact` via `_STEP_COMPLETE:` / `## NEXUS_HANDOFF`; `enact` owns cross-package sequencing and aggregation.
- Orbit's standard resilience contract still holds: external termination (iteration cap / timeout / budget), idempotency keys, circuit breaker, no mid-loop mutation of pinned files.

## Delegation handoff (what enact sends)

`enact` delegates via `_AGENT_CONTEXT` with:
- `Task`: build-loop the §4 package `<id>`
- `Input`: Charter slice (§4 package + §5 entry + §7 package gates + §10 DoD + §3 commands + §9 run-log path)
- `Constraints`: engine + `fallback_engine`; file ownership (from §6); budget ceiling (from §8)
- `Expected_Output`: terminal status (`SUCCESS`/`PARTIAL`/`SKIPPED`) + DoD result + run-log lines appended

Orbit returns `_STEP_COMPLETE:` with `Status`, `Output` (DoD result + artifacts), `Handoff` (Builder/Radar/Guardian as needed), `Next` (`CONTINUE`/`VERIFY`/`DONE`).
