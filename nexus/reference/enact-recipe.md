# Nexus Enact Recipe Reference

**Purpose:** Read an existing **Charter**, construct the team from its roster, and **orchestrate every work package end-to-end** until the work is shipped. Enact is the execution half of the `charter → enact` pair.
**Read when:** User invokes `/nexus enact`, or asks to "run the Charter", "build the team from the instruction document and execute it", or "execute `docs/CHARTER.md` start to finish". For *authoring* the Charter, see `reference/charter-recipe.md`.

## Contents
- Overview
- Input: the Charter contract
- Invocation Modes
- Topology
- Phase 1: Team Construction
- ★ Confirm Gate
- Run-to-Completion Contract (enforced)
- Run Log (append-only)
- Phase 2: End-to-End Orchestration
- Phase 3: Verify & Deliver
- Conditional Inclusion
- AUTORUN Chain Template
- Failure Escalation
- Cost and Latency Profile

---

## Overview

Enact turns a Charter into shipped work. It does **no analysis and no planning** — the Charter (authored by `charter`, or hand-written to the same schema) is the complete source of truth. Enact:

1. **Constructs the team** strictly from Charter §5 (roster) — resolving each role→skill→spawn config and verifying spawn prereqs. The team is a pure function of the document, so re-running enact on the same Charter rebuilds the identical team.
2. **Orchestrates** Charter §4 (work breakdown) via the §6 plan — spawning each work package's owner, running build loops via Orbit, enforcing guardrails, and aggregating hub-spoke.
3. **Verifies & delivers** against §7 (verification plan). Throughout, the orchestrator **appends every progress event to a dedicated append-only run-log file** (see **Run Log**) and keeps Charter §9 as a summary + pointer into it — so the run is auditable and resumable even if interrupted mid-stream.

Because authoring is already paid for, enact is opt-in and explicit: it spawns the full execution team and writes code, so it announces before building (the ★ Confirm Gate).

**Enact runs to completion by default.** Once launched under `AUTORUN_FULL`, enact does not stop mid-run for progress confirmation, recoverable failures, or cost — it drives **every** §4 work package to a terminal state and only then delivers. The only intentional stops are the safety red lines (Charter §8 human-confirm triggers: L4 security, destructive/irreversible actions, out-of-scope changes) and an unsatisfiable precondition (no valid Charter). See **Run-to-Completion Contract**. Forcing completion means "do not stop early", never "mask failures" — a completed run can still deliver FAILED/PARTIAL package statuses, reported honestly.

## Input: the Charter contract

Enact requires a Charter conforming to the schema in `reference/charter-recipe.md` § Charter Document Schema. It reads:

| Section | Used by | For |
|---------|---------|-----|
| §3 Conventions & Guardrails | all phases | commit/test/lint/build commands, branch policy, L4 rules |
| §4 Work Breakdown | Phase 2 | atomic steps, dependencies, sequencing, per-package AC |
| §5 Team Roster | Phase 1 | owner skill + model tier + engine + spawn config per package |
| §6 Orchestration Plan | Phase 2 | chain order, parallel branches + file ownership, checkpoints |
| §7 Verification Plan | Phase 3 | per-package + final gates |
| §8 Escalation & Rollback | all phases | failure tiers, circuit breaker, rollback boundaries |
| §9 Execution Log | Phase 2-3 | run-log **pointer** + final summary; the detailed timeline lives in the append-only run-log file (see **Run Log**), from whose tail `resume` restarts |
| §10 Checklists & Trackers | all phases | pre-flight gate (Phase 1), per-package DoD (terminal-state criterion, Phase 2), progress tracker (ticked at `PKG_DONE`), final delivery checklist (Phase 3) |

The machine-readable companion (`CHARTER.roster.yaml`) is preferred for §5-§6 when present. If the Charter is missing a required section or a roster entry names a non-existent skill, enact stops at Phase 1 and reports the gap rather than improvising (the missing design belongs in `charter`, not here).

## Invocation Modes

| Form | Behavior |
|------|----------|
| `/nexus enact` (no args) | Read `docs/CHARTER.md` (default), construct + **run to completion**. |
| `/nexus enact <path>` | Read the Charter at `<path>`, construct + **run to completion**. |
| `/nexus enact dry-run` | Phase 1 only — construct + verify the team, report constructability, **do not execute**. |
| `/nexus enact resume` | Resume from the **run-log tail** (last terminal package); skips completed packages. Run-to-completion still applies. |
| `/nexus enact log=<path>` | Override the run-log file path. Default: derived from the Charter path (`docs/CHARTER.md` → `docs/CHARTER.run.log.md`). |

Run-to-completion is the **default and enforced** behavior under `AUTORUN_FULL`. To re-introduce intermediate stops, drop to a confirming mode: `## NEXUS_GUIDED` (confirm at phase boundaries) or `## NEXUS_INTERACTIVE` (confirm every step). These are the only opt-outs; there is no per-package "pause and ask" inside `AUTORUN_FULL`.

## Topology

```
                Phase 1                  ★ Confirm   Phase 2                          Phase 3
                [Team Construction]                  [End-to-End Orchestration]       [Verify & Deliver]
read Charter    ┌──────────────────┐     ┌───────┐  ┌────────────────────────────┐   ┌──────────────┐
docs/CHARTER.md │ §5 → bind        │     │ 👤    │  │ per §4 work package (§6 order):│   │ §7 gates     │
+ roster.yaml ─▶│  role→skill→spawn│ ──▶ │ build │─▶│  spawn assigned owner       │ ─▶│ radar?/judge?│
                │ verify prereqs   │     │ team? │  │  ‖ parallel + file ownership│   │ guardian?    │
                │ sub-orch setup   │     │ cost  │  │  build loops → orbit (sub)  │   │ launch?      │
                │ dry-run check    │     └───────┘  │  checkpoints + guardrails   │   │ → RUN_END    │
                └──────────────────┘                │  aggregate; append run log  │   │ → DELIVER    │
                                                    └──────────────┬─────────────┘   └──────────────┘
                          append-only run log: docs/CHARTER.run.log.md  (Charter §9 = pointer + summary)
                          ◀──────── Failure escalation (per Charter §8) ───────────────────┘
```

Hub-and-spoke is preserved: Nexus is the only top-level orchestrator. Where Charter §5 nominates a sub-orchestrator (Vision for UX clusters, Orbit for build loops, Rally for parallel sessions), Nexus spawns it as a ≤7-specialist sub-hub — never agent-to-agent.

Under `AUTORUN_FULL` the ★ Confirm box is **announce-and-proceed** (no human stop), and the Failure-escalation arrow loops back into Phase 2 to recover and continue rather than halting — the run only exits at DELIVER or a §8 safety red line (see **Run-to-Completion Contract**).

## Phase 1: Team Construction

Instantiate the team strictly from Charter §5. This is "build the dev team from the Charter".

| Step | Action |
|------|--------|
| Bind | For each roster entry, resolve role → skill SKILL.md path, model tier, engine (per Orchestrator Detection), and spawn config |
| Verify prereqs | Confirm the active hub's spawn tool + per-CLI prereqs (`reference/execution-layers.md`); for Codex packages check `multi_agent = true` + `[agents] max_depth ≥ 2`, for agy check the TTY/real-pty path (`_common/CLI_COMPATIBILITY.md §9`). If a §5 engine is unreachable, apply that package's `fallback_engine` (default `claude-code`) and log the substitution + its cost/throughput trade-off; hard-fail only when no fallback is defined |
| Sub-orchestrator setup | Where §5 nominates Vision/Orbit/Rally, prepare its sub-hub contract (≤7 specialists each) |
| Pre-flight checklist | Run the Charter §10 pre-flight checklist (Charter complete, owners constructable, engine prereqs/fallbacks, clean tree/branch, team-readiness); tick each item and log `TEAM_BUILT` |
| Dry-run check | Validate that every §4 work package has a constructable owner; any unconstructable entry escalates before execution begins |

**Exit gate:** every work package has a verified, spawnable owner. Unresolvable roster entries do **not** get improvised — enact reports the gap and recommends re-authoring via `charter` (§5). `dry-run` mode stops here and delivers the constructability report.

## ★ Confirm Gate

Team construction + full orchestration spawns the execution team and writes code (potentially many spawns + iterations + file writes). The gate sits at Phase 1 exit.

| Mode | Behavior |
|------|----------|
| `INTERACTIVE` | Always confirm; user may adjust before build |
| `GUIDED` | Always confirm; approve / abort |
| `AUTORUN` | Explicit Y/N; default abort on no response |
| `AUTORUN_FULL` | **Announce-and-proceed (no objection window)** — the `reference/recipe-contract.md` §3 tier for runs-to-completion recipes where only §8 red lines stop. Print the construction summary (work-package count, roster size, estimated agent count / cost / time) and start immediately, because run-to-completion is the contract. Cost is pre-authorized by invoking enact. |

`dry-run` never reaches execution regardless of mode. The Confirm Gate is the *only* gate at the start; it is not re-evaluated mid-run (run-to-completion).

## Run-to-Completion Contract (enforced)

Under `AUTORUN_FULL`, enact is bound to finish what it starts. It removes every *recoverable* stop point and guarantees forward progress to a terminal state for each work package.

**No-stop rules (recoverable conditions never halt the run):**
- **Progress confirmations are suppressed.** No "continue?" prompts between packages or phases. The single ★ Confirm Gate announce-and-proceeds.
- **Recoverable failures auto-recover and continue.** Per package: retry (max 3) → `fallback_engine` (per §5) → recovery-chain injection (Scout RCA → Builder fix) → alternate owner skill. The run does not pause to ask.
- **A package that still cannot complete is marked `SKIPPED(blocked)` with reason, logged to §9, and the run continues with the remaining packages.** One unsatisfiable package never aborts the whole run.
- **Cost does not pause the run.** Enact proceeds to the Charter §8 budget ceiling automatically; only a genuine ceiling breach escalates, per §8 policy.
- **Interruptions auto-resume.** On context limit / crash / harness restart, enact resumes from the run-log tail (as if `resume`) without asking. The run is "done" only at DELIVER.

**Completion guarantee:** Phase 2 loops until **every** §4 work package is in a terminal state — `SUCCESS`, `PARTIAL`, or `SKIPPED(blocked, reason)`. `BLOCKED` is never a resting state: the recovery ladder above must be exhausted first. DELIVER reports the full per-package status set.

**Safety red lines (the only intentional stops — NOT bypassed by run-to-completion):**
- Charter §8 human-confirm triggers: **L4 security, destructive/irreversible data actions, external system modifications, and edits beyond the file scope §6 pre-authorized** (e.g. 10+ files not covered by package ownership). These pause for confirmation even in force mode — run-to-completion pre-authorizes only what the Charter already scoped, not actions outside it.
- **No valid Charter** (missing/invalid section, roster names a non-existent skill): a precondition failure, not a mid-run stop — enact reports and exits before execution.

**Honesty red line:** Run-to-completion ≠ faking green. §7 verification failures are reported truthfully with output; the run completes and DELIVERs with FAILED/PARTIAL statuses rather than masking, retrying forever, or bypassing checks (global quality rule). "Finish to the end" means reach a true terminal verdict, not a fabricated success.

## Run Log (append-only)

The orchestrator maintains a single **append-only run-log file** and writes one line per progress event as the run unfolds. It is the crash-resilient audit trail and the source of truth for `resume` — never the orchestrator's in-context memory, which a long run outgrows.

**File:** default `<charter_dir>/<charter_stem>.run.log.md` (e.g. `docs/CHARTER.md` → `docs/CHARTER.run.log.md`); override with `log=<path>`. Durable and committable alongside the Charter. Each enact run appends a `## Run <n> — <charter_path> — started <ts>` header, then its events; prior runs' lines are never rewritten.

**Append rules:**
- **Append-only.** Only ever add lines at the end; never edit or delete existing lines. A partial log after a crash is still valid.
- **One line per event**, written *immediately* as the event occurs (not batched at the end) so an interruption loses at most the in-flight line.
- **Line format:** `- [<ISO-8601 ts>] <EVENT> pkg=<id> status=<…> — <one-line note>` (events with no package omit `pkg=`).
- **Flush at every boundary**, then mirror a compact pointer into Charter §9 (`last_event`, `run_log: <path>#<anchor>`) so §9 stays small and the timeline stays in the log file.

**Logged events (minimum):**

| Event | When | Key fields |
|-------|------|-----------|
| `RUN_START` | enact launches | charter path, mode, package count, log path |
| `TEAM_BUILT` | Phase 1 exit | roster size, engines, fallbacks applied |
| `CONFIRM` | ★ Gate | announce-and-proceed / approved / rejected |
| `PKG_START` | a package begins | pkg id, owner skill, engine |
| `PKG_RECOVER` | recovery-ladder step fires | pkg id, step (retry/fallback/scout/alt-owner) |
| `PKG_DONE` | a package reaches terminal | pkg id, status (SUCCESS/PARTIAL/SKIPPED+reason) |
| `SAFETY_STOP` | §8 red line hit | trigger, awaiting-confirm / resolved |
| `VERIFY` | §7 gate result | gate, pass/fail + output ref |
| `RESUME` | run restarts | resumed-from event, packages skipped |
| `RUN_END` | DELIVER | overall status, per-package tally |

**Resume:** on restart, read the run-log tail, treat the last `PKG_DONE` as the checkpoint, emit `RESUME`, and continue with packages not yet terminal. No re-confirmation, no re-running completed packages.

## Phase 2: End-to-End Orchestration

Execute Charter §4 via the §6 Orchestration Plan. Standard Nexus EXECUTE → AGGREGATE machinery, parameterized by the Charter.

- **Spawn per work package** in §4 order; pass only state deltas (`reference/context-strategy.md`). Independent packages run as parallel branches with file ownership from §6 (`_common/PARALLEL.md`); no shared mutable state.
- **Build loops** (multi-iteration implementation packages) delegate to `orbit` as a sub-orchestrator (build → judge → test → converge), as in Apex Phase 6. Engine per Charter §5 (Codex CLI for high-volume coding loops where available). Orbit drives these **Charter-natively** — it receives the read-only §4/§5/§7/§10 slice, uses the §10 per-package DoD as its external DONE gate, and appends `PKG_*` events to the same §9 run-log (`orbit/reference/charter-loop-driver.md`). Orbit owns the single package's loop; enact retains cross-package sequencing and aggregation (hub-spoke).
- **Guardrails** L1-L4 + checkpoint-resume on 4+ step chains; max-hop limit enforced; destructive/L4/out-of-scope actions pause per §3/§8 (safety red line). The circuit breaker after 3 consecutive package failures does **not** abort the run — it marks that package `SKIPPED(blocked)` and moves on (run-to-completion).
- **Run-to-completion recovery:** a failing package walks the recovery ladder (retry → `fallback_engine` → Scout RCA + Builder fix → alternate owner) before being skipped; the run never pauses to ask on recoverable failures.
- **Aggregate** branch outputs hub-spoke; validate schema + semantic correctness at each boundary.
- **Definition of Done.** A package is `SUCCESS` only when its Charter §10 per-package DoD checklist fully passes (AC met + tests green + lint/build/typecheck + review); partial pass → `PARTIAL`, unrecoverable → `SKIPPED`. DoD is the objective terminal-state criterion, not prose judgment.
- **Append** one run-log line per event (`PKG_START` / `PKG_RECOVER` / `PKG_DONE` / `SAFETY_STOP` …) the moment it occurs; at `PKG_DONE` also tick that package's row in the §10 progress tracker. Mirror a compact pointer into Charter §9, so an interrupted run auto-resumes from the run-log tail (see **Run Log**).

**Exit gate:** **every** work package is in a terminal state — `SUCCESS` / `PARTIAL` / `SKIPPED(blocked, reason)`; none left pending or merely `BLOCKED`. Outputs aggregated; skipped packages carry unblock conditions in §9.

## Phase 3: Verify & Deliver

| Agent | Role | Required |
|-------|------|----------|
| `radar` | Fill test gaps / run the verification suite per §7 | Conditional: code changed |
| `judge` | Final review of aggregated changes | Conditional: code changed |
| `guardian` | Commit policy, branch strategy, PR preparation | Yes (if code changed) |
| `launch` | Release/rollback plan | Conditional: release in scope |

Run §7 gates (tests/build/security/AC), appending a `VERIFY` line per gate and a final `RUN_END` line to the run log. Then work the Charter §10 **final delivery checklist** (all gates pass, no release-critical SKIPPED, run-log RUN_END written, rollback ready) — each unticked item is surfaced in DELIVER, not silently passed. Update the Charter (§9 summary/pointer + §4 AC status + §10 tracker/checklist ticks) so the delivered document reflects what was actually done — the living Charter. `DELIVER` returns `NEXUS_COMPLETE` with the Charter path, run-log path, per-package status, the completed §10 checklists, verification results, and follow-ups.

**Exit gate:** §7 verification passes (or failures surfaced honestly with output, per global quality rules); Charter persisted and current.

## Conditional Inclusion

| Condition | Add | Skip |
|-----------|-----|------|
| `dry-run` | — | ★ Confirm, Phase 2, Phase 3 |
| `resume` | — | packages already terminal in the run-log tail |
| No code changes (docs/plan-only Charter) | — | radar, judge, guardian, launch |
| Work cluster needs hierarchy (per §5) | Vision/Orbit/Rally sub-orchestrator | — |
| Release in scope (per §7/§8) | launch | — |

## AUTORUN Chain Template

```
Nexus AUTORUN enact docs/CHARTER.md
  ── read Charter ─────────────────────────────────────
  → parse docs/CHARTER.md (+ CHARTER.roster.yaml if present)
  → validate required sections (§3-§8, §10); missing/invalid → stop + report gap
  → open run log docs/CHARTER.run.log.md (append "## Run <n>" + RUN_START)
  ── Phase 1 Team Construction ────────────────────────
  → for each §5 roster entry: bind(role→skill→spawn) + verify prereqs
  → run §10 pre-flight checklist (tick all) → sub-orch setup? → dry-run check
     (enact dry-run → STOP + deliver constructability report)
  ── ★ Confirm Gate ───────────────────────────────────
  → AUTORUN_FULL: announce construction summary → proceed immediately (no wait)
  ── Phase 2 End-to-End Orchestration (run to completion) ─
  → loop until every §4 package is terminal (SUCCESS|PARTIAL|SKIPPED):
       spawn(owner_skill, contract=package.AC, model=§5.tier, engine=§5.engine)
       ‖ parallel branches with §6 file ownership
       build-loop packages → orbit(sub-orchestrator)
       terminal = §10 per-package DoD checklist result (SUCCESS|PARTIAL|SKIPPED)
       append run-log: PKG_START → PKG_RECOVER* → PKG_DONE (immediately)
         → tick §10 progress-tracker row at PKG_DONE
       on recoverable failure: retry→fallback_engine→Scout+Builder→alt owner
         → still failing: mark SKIPPED(blocked, reason), CONTINUE (no abort)
       on safety red line (L4/destructive/out-of-scope per §8): pause + confirm
       on interruption: auto-resume from run-log tail
       mirror §9 pointer per package boundary
  → aggregate hub-spoke
  ── Phase 3 Verify & Deliver ─────────────────────────
  → radar? + judge? → §7 gates (tests/build/sec/AC); append VERIFY lines
  → work §10 final delivery checklist (unticked items surfaced in DELIVER)
  → guardian(commit/PR)? → launch(release)?
  → append RUN_END; update Charter (§9 pointer + AC status + §10 ticks)
  → NEXUS_COMPLETE(charter_path, run_log_path, checklists, statuses)
```

## Failure Escalation

Under run-to-completion, only **precondition** and **safety red line** failures stop the run; every recoverable failure continues.

| Failure | Detected by | Escalation (run-to-completion) |
|---------|-------------|------------|
| Charter missing/invalid section | enact parse | **Stop (precondition)** — report which section; recommend `charter` to re-author. Cannot run without a valid Charter |
| §5 roster names a non-existent skill | enact bind | **Stop (precondition)** at Phase 1; report the gap; do not improvise an owner |
| Phase 1 engine prereq unmet (e.g. Codex `max_depth < 2`) | Nexus | **Continue** — apply package `fallback_engine` (log substitution + trade-off); skip only that package if no fallback, run continues |
| Phase 2 package repeat failure | judge/radar | **Continue** — recovery ladder (retry→fallback→Scout RCA+Builder→alt owner); if still failing, mark `SKIPPED(blocked)` + log §9, proceed to remaining packages. Never aborts the run |
| Build loop stuck / over budget | orbit | **Continue** — orbit switches strategy and keeps going; only a real §8 budget-ceiling breach escalates per §8 (not a blanket pause) |
| Safety red line (L4 / destructive / out-of-scope per §8) | Nexus / §8 | **Stop + confirm** — the one intentional mid-run pause; resumes on approval, aborts only that action on denial |
| §7 verification fails | radar/judge | **Continue to DELIVER** — report honestly with output; deliver FAILED/PARTIAL status; do not mask, retry forever, or bypass checks (global quality rule) |

## Failure Modes Prevented

Consolidated view of what enact's run-to-completion contract, recovery ladder, and red lines guard against (drawn from the Run-to-Completion Contract, the recovery ladder, §8 red lines, and Failure Escalation). The design goal is **forward progress to a true terminal verdict** — never an early stop, never a faked green.

| Failure mode | Without enact's contract | Prevented by |
|--------------|--------------------------|--------------|
| Stalling on a recoverable failure | The run pauses mid-stream and waits for a human on every hiccup | Recovery ladder: retry (max 3) → `fallback_engine` (§5) → Scout RCA + Builder fix → alternate owner — auto-recovers without asking |
| One blocked package aborting the whole run | A single unsatisfiable step kills an otherwise-complete delivery | `SKIPPED(blocked, reason)` terminal state — the run continues with remaining packages; circuit breaker (3 failures) skips, never aborts |
| Engine unreachable hard-fails the run | Codex/agy down stops everything | Per-package `fallback_engine` (default `claude-code`) with logged cost/throughput trade-off; hard-fail only when no fallback defined |
| Cost pausing the run open-endedly | Spend prompts interrupt an authorized run | Cost does not pause; proceeds to the Charter §8 budget ceiling automatically — only a genuine ceiling breach escalates |
| Lost progress on interruption | A crash/context-limit restarts from scratch | Append-only run-log tail + auto-resume (treat last `PKG_DONE` as checkpoint; skip terminal packages; no re-confirm) |
| Faking green to "finish" | Run-to-completion misread as "report success regardless" | Honesty red line: §7 failures reported truthfully with output; DELIVER carries FAILED/PARTIAL — terminal verdict, never fabricated |
| Acting outside the Charter's scope | Force-mode runs destructive/L4/out-of-scope actions unprompted | §8 safety red lines pause for confirm even in force mode — run-to-completion pre-authorizes only what the Charter already scoped |
| Improvising past a bad Charter | Missing section / non-existent skill silently patched | Precondition stop at parse/Phase 1 — report the gap, recommend re-authoring via `charter`; never improvise an owner |

## Boundaries / vs neighbors

Enact is the **execution half** of the `charter → enact` pair — it runs a document, it does not author one. How it differs from its siblings:

| vs neighbor | Enact | The neighbor |
|-------------|-------|--------------|
| **charter** | **Executes** the Charter: constructs the team from §5, orchestrates §4 end-to-end, ships | **Authors** the Charter (analysis + team design) — stops at the document, spawns no execution agents |
| **apex** | Charter-driven, **multi-package**: runs a pre-authored roster of work packages to completion (no discovery) | Self-contained **single-feature** discovery→ship: picks its own goal, specs, designs, builds, ships one feature in one chain |
| **summit** | Drives every §4 package to a terminal state; one owner per package (no competition) | Quality-max tournament — multiple candidate solutions compete on one problem, judged to a winner |

Decision tree: have a Charter (from `charter` or hand-written) and want it run end-to-end → **enact**. Need the Charter authored first → **charter**. One high-stakes feature, discovery→ship, no Charter → **apex**. Quality-max with competing candidates → **summit**.

## Cost and Latency Profile

| Profile | Phases active | Approx agent count | Approx cost |
|---------|---------------|--------------------|-------------|
| dry-run | 1 | per §5 roster size (no execution) | Low |
| small Charter (no build loops) | 1, 2, 3 | 6-12 | Medium |
| standard Charter (1-2 build loops) | All | 12-20 | Medium-High |
| large Charter (multiple build loops + sub-orchestrators) | All + orbit loops + Vision/Rally | 20-30+ | High |

Enact is the expensive half of the pair; the ★ Confirm Gate, 5+-agent chain confirmation, orbit cost-per-task tracking, and L4 gates bound spend. Because the team is reconstructed from the Charter, `enact` can be re-run (or `resume`d) without re-paying for analysis/authoring.

---

## Visualization

Topology ASCII above. Enact consumes `docs/CHARTER.md` (+ `CHARTER.roster.yaml`), streams every progress event to the append-only run log `docs/CHARTER.run.log.md`, and writes back the Charter §9 pointer/summary; the Charter stays the single source of truth and the run log is the auditable, resumable timeline.
