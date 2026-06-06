# Nexus Apex Recipe Reference

**Purpose:** End-to-end auto-implementation chain spanning discovery, ideation, decision, specification, parallel design, risk gating, implementation loop, and ship — with sub-orchestration via Vision (UX) and Orbit (implementation loop).
**Read when:** User invokes `/nexus apex` or requests "ultimate auto-implementation", full-cycle delivery from user need to release, or any chain requiring 10+ agents across discovery and implementation.

## Contents
- Overview
- When to Use Apex
- Invocation Modes
- Topology
- Phase 0: Bootstrap (no-args / autonomous goal discovery)
- Phase Contracts (1 → 6 + Ship)
- Sub-Orchestration: Vision (UX) and Orbit (Loop)
- Conditional Agent Inclusion
- Risk Gate Criteria
- Workflow Accuracy Rationale
- AUTORUN Chain Template
- Failure Escalation
- Cost and Latency Profile

---

## Overview

Apex is Nexus's heaviest Recipe. It bundles **Phase 0 (autonomous goal discovery, no-args mode only) + 6 sequential phases** with two parallel sub-tracks (Tech / UX) inside Phase 5, gated by a tri-axis Risk Gate (Omen + Ripple + Echo), and executed through Orbit's autonomous loop. Apex deliberately keeps the implementation phase count at **6 (not 7+)** by parallelising design work, since `85% × 7 ≈ 32%` end-to-end success would otherwise dominate.

Apex is **not** a default recipe. It is opt-in for high-stakes new features where every upstream gap (missed user need, weak spec, hidden architecture risk, UX friction) is materially costly to discover post-implementation.

## Invocation Modes

| Form | Behavior |
|------|----------|
| `/nexus apex <goal description>` | **Goal-supplied mode**. Skip Phase 0, start at Phase 1 with the supplied goal. |
| `/nexus apex` (no args) | **Autonomous mode**. Run Phase 0 to discover the highest-priority goal from project state + real feedback + KPI/competitive signals, confirm once at boundary, then run Phase 1-6 + Ship. |
| `/nexus apex goal=auto` | Explicit autonomous mode (same as no-args). |
| `/nexus apex goal=<X> scope=<Y>` | Goal-supplied with optional scope hints (`Lite` / `Standard` / `Full`, `ui=true/false`, `api_change=true/false`, `db_change=true/false`). |

Autonomous mode is the **fully self-driven** form: Apex picks what to build, confirms once, and ships. The single human checkpoint is the boundary confirmation between Phase 0 and Phase 1 — once approved, everything downstream runs without further human input unless internal gates trigger.

## When to Use Apex

Use Apex when the request matches **at least 3** of:

- New customer-facing feature with UI surface (not a backend-only fix)
- Cross-team impact (Biz + Dev + Design)
- Reversibility cost is high (DB migration, API contract change, brand-visible UX)
- Acceptance criteria are not pre-supplied — must be derived from user need
- Architecture decision is required (not just implementation)
- 5+ files / 2+ modules / 2+ days estimated

Route elsewhere when the task is:
- Bug fix → `bug` recipe
- Single-feature small/medium → `feature` recipe
- Refactoring → `refactor` recipe
- Pure design exploration without implementation → Atelier or Vision direct
- Decomposition only (no execution) → Sherpa direct
- Cross-language rewrite preserving behavior (TS→Rust, Go→Rust, …) → `transmute` recipe (`reference/transmute-recipe.md`)

## Topology

```
Phase 0 (no-args only)              Phase 1            Phase 2  Phase 3  Phase 4    ┌── Phase 5 (parallel) ─────────────┐  Phase 6           Ship
[Bootstrap / Goal Discovery]        [Discovery]        [Ideate] [Verdict][SPEC]     │ Tech Track    UX Track            │  [Implement Loop]
┌─────────────────────────────┐     ┌─────────────┐    ┌────┐   ┌────┐   ┌────────┐ │ ┌──────────┐  ┌──────────────┐    │  ┌──────────────┐  ┌────────┐
│ project_scan (proactive)    │     │ plea        │    │riff│   │magi│   │ accord │ │ │ atlas    │  │ vision (sub) │    │  │ orbit         │  │guardian│
│ + voice?  + pulse? +compete?│ ──▶ │ field       │ ─▶ │    │─▶ │    │─▶ │ +void? │▶│ │ +gateway?│  │  ├ muse      │    │▶ │  ├ builder    │ ─▶│ launch │
│ → spark (3-5 ideas)         │     │ +echo (as-is)│    │    │   │    │   │ +scribe?│ │+schema?  │  │  ├ palette   │    │  │  ├ artisan?   │  └────────┘
│ → rank (ICE/RICE)           │     └─────────────┘    └────┘   └────┘   └────────┘ │ └──────────┘  │  ├ prose     │    │  │  ├ vitrine?   │
│ → sage? (bottleneck check)  │                                                     │               │  ├ flow?     │    │  │  ├ judge      │
│ → magi? (tie-break)         │                                                     │               │  ├ frame?    │    │  │  ├ radar      │
│ → 👤 boundary confirm       │                                                     │               │  ├ forge     │    │  │  └ voyager?   │
└─────────────────────────────┘                                                     │               │  └ echo      │    │  └ orbit audits  │
                                                                                    │ ─────────────────────────────────  │       │
                                                                                    │ ★ omen + ripple + echo Risk Gate   │       │
                                                                                    └────────────────────────────────────┘       │
                                                ◀──────── Failure escalation ──────────────────────────────────────────────────┘
```

Hub-and-spoke is preserved: Nexus is the only top-level orchestrator. Vision is the **UX sub-orchestrator** (already contracted to delegate Muse/Palette/Flow/Forge/Frame/Prose). Orbit is the **implementation-loop sub-orchestrator** (drives nexus-autoloop with Builder/Judge/Radar). This two-tier structure keeps each hub at ≤7 specialists.

Phase 0 runs only in autonomous mode and emits a single goal artifact bound as Phase 1 input. The boundary confirm at Phase 0 exit is the **only** human checkpoint in autonomous mode under `AUTORUN_FULL`; everything downstream relies on the internal Risk Gate and Orbit's circuit breaker.

## Phase 0: Bootstrap (Autonomous Goal Discovery)

**Trigger:** `/nexus apex` invoked with no goal, or `goal=auto`. Skipped when a goal description is supplied.

**Purpose:** Discover the highest-priority goal from project state and external signals, score and select a single goal, then bind it as Phase 1 input. The single human checkpoint of autonomous mode lives at the exit of this phase.

### Sub-phases

#### 0a. SCAN (parallel)

| Source | Required | Notes |
|--------|----------|-------|
| Project state scan (Nexus internal, reuses `proactive-mode.md` logic) | Yes | git log (last 30 days), open PRs/issues, TODOs/FIXMEs in code, `.agents/PROJECT.md`, `CLAUDE.md`, README signals, recently-shipped feature flags awaiting cleanup |
| `voice` | Conditional | Real user feedback aggregation if any source is configured (NPS/CSAT/reviews/support tickets/sentiment) |
| `pulse` | Conditional | KPI/metric drops, funnel friction, cohort regressions if metrics integration exists (GA4/Amplitude/Mixpanel/PostHog) |
| `compete` | Conditional | Competitor gap analysis if a competitor list is maintained |
| `trace` | Conditional | Session replay behavioural signals if available |

#### 0b. PROPOSE

| Agent | Role |
|-------|------|
| `spark` | Synthesise **3-5 candidate goals** from 0a output. Each candidate carries: `title`, `hypothesis`, `evidence_refs`, `estimated_impact`, `rough_scope`, `dependencies`. |

#### 0c. PRIORITIZE

| Agent | Role |
|-------|------|
| `rank` | Score candidates with **ICE / RICE / WSJF** (auto-pick framework based on signal availability). Output ordered list with confidence. |
| `sage` | (Optional) Socratic sanity check on the #1 candidate — does it pattern-match a known anti-pattern (premature scaling, vanity metric, founder ego project)? |

#### 0d. SELECT

| Condition | Action |
|-----------|--------|
| #1 margin > 10% over #2 | Auto-select #1 |
| Top 2 within 10% | `magi` tri-engine tie-break |
| All candidates ICE < threshold (e.g. < 30) | Escalate "no high-confidence goal" to user, present top 3 for manual selection |

Emit `auto_selected_goal`:

```yaml
auto_selected_goal:
  title: <feature title>
  rationale: <why selected, evidence summary>
  evidence_refs: [project_scan/voice/pulse/compete refs]
  estimated_scope: Lite | Standard | Full
  estimated_cost: <agent_count_est>, <time_est>, <token_est>
  ui_surface: true | false
  api_change: true | false
  db_change: true | false
  rejected_alternatives: [(title, why_not), ...]
```

#### 0e. CONFIRM (boundary safety, single human checkpoint)

| Mode | Behavior |
|------|----------|
| `INTERACTIVE` | Always confirm; user can edit goal before proceeding |
| `GUIDED` | Always confirm; user approves or aborts |
| `AUTORUN` | Confirm with explicit Y/N; defaults to abort on no response |
| `AUTORUN_FULL` | Show selected goal with rationale, **wait 60 seconds for user objection**, then proceed automatically. Any user input within window aborts and re-runs Phase 0 with hint. |

The confirmation message includes: goal title, rationale, top 2 rejected alternatives, estimated cost (agent count / time / token budget), and "edit/abort" instructions. Once approved (explicitly or by timeout in `AUTORUN_FULL`), Apex proceeds to Phase 1 with the goal bound and **no further human input is required** unless an internal Risk Gate or Orbit circuit breaker fires.

### Phase 0 Failure Modes

| Failure | Cause | Action |
|---------|-------|--------|
| No data sources for 0a | Greenfield project, no real users yet | Fall back to "spark from project scan only", flag candidates as low-confidence |
| Spark produces 0 candidates | Project state extremely stable, no TODOs/feedback | Escalate "no work to propose" to user — apex aborts |
| All candidates ICE < threshold | No clearly worthwhile work | Present top 3 to user for manual selection or abort |
| `magi` returns split (1-1-1) | Tie-break failed | Escalate top 2 to user with magi rationale |
| User rejects in 0e | User has different priority | Apex aborts, suggests user invoke with explicit goal |

---

## Phase Contracts

### Phase 1: Discovery

| Agent | Role | Required |
|-------|------|----------|
| `plea` | Synthetic user demands across 3+ personas, paired with LLM prompts | Yes |
| `field` | BEST-framework validation or real research synthesis | Yes |
| `echo` | Friction analysis on current flow (Emotion VAD + dark pattern audit) | Existing-product improvement only |

**Exit gate:** Top-3 demands carry both persona rationale (plea) and evidence anchor (field). If product exists, echo confirms current friction baseline.

### Phase 2: Ideate

| Agent | Role | Required |
|-------|------|----------|
| `riff` | Diamond thinking (Expand → Propose → Evaluate → Subtract), max 4 turns | Yes |

**Exit gate:** ≥2 comparable decision candidates ready for magi.

### Phase 3: Verdict

| Agent | Role | Required |
|-------|------|----------|
| `magi` | Logos / Pathos / Sophia tri-engine deliberation, output verdict + AC seed | Yes |

**Exit gate:** Verdict carries (1) chosen option, (2) acceptance criteria seed, (3) scope boundary, (4) failure conditions. Split decision (1-1-1) escalates to human review.

### Phase 4: Spec

| Agent | Role | Required |
|-------|------|----------|
| `accord` | L0 Vision → L1 Requirements → L2 Team Detail → L3 Acceptance Criteria + traceability | Yes |
| `void` | YAGNI scope cutting | Conditional: accord scope = Full |
| `scribe` | Formal PRD/SRS/HLD/LLD or AI-agent-consumable spec | Conditional: M+ size or external review |

**Exit gate:** accord traceability completeness meets scope-mode threshold (Full ≥95% / Standard ≥85% / Lite ≥70%). L3 ACs are measurable and orbit-consumable.

### Phase 5: Design + Risk Gate (parallel)

#### Tech Track

| Agent | Role | Required |
|-------|------|----------|
| `atlas` | Architecture decision + ADR (MADR/Nygard) + dependency graph | Yes |
| `gateway` | API design + OpenAPI spec | Conditional: API change |
| `schema` | DB schema + migration plan | Conditional: DB change |

#### UX Track (orchestrated by Vision)

| Agent | Role | Required |
|-------|------|----------|
| `vision` | Creative direction + delegation plan (sub-orchestrator) | Yes (if UI surface) |
| `muse` | Design tokens (spacing, color, typography, dark mode) | Yes |
| `palette` | Interaction design + a11y + cognitive load | Yes |
| `prose` | Microcopy, error/empty-state, voice/tone | Yes |
| `flow` | Animation / motion specification | Conditional: motion in scope |
| `frame` | Figma MCP extraction + Code Connect | Conditional: Figma in workflow |
| `forge` | Rapid prototype (working slice) | Yes |
| `echo` | Cognitive walkthrough + WCAG 3.0 simulation + dark pattern audit | Yes |
| `polyglot` | i18n string extraction strategy | Conditional: multi-locale |
| `pixel` | Mockup-to-code | Conditional: mockup supplied |

UX Track internal pipeline: `vision → muse → [palette ‖ prose ‖ flow] → frame? → forge → echo`.

#### Risk Gate (parallel, post-Tech and post-UX)

| Agent | Role | Pass Criterion |
|-------|------|----------------|
| `omen` | FMEA + RPN + Mitigation 3-layer (Detection / Prevention / Recovery) | High RPN residuals = 0, or Mitigation defined |
| `ripple` | Vertical + horizontal impact + blast radius | Go or Conditional-Go (No-Go blocks) |
| `echo` | UX friction signals fed into gate | Emotion Valence ≥ median, dark pattern = 0, WCAG 3.0 Bronze ≥ 3.5 |

Plea ↔ Echo loop closure: if echo's actual walkthrough reaction diverges fatally from plea's predicted demand, send back to Phase 4 (accord) for spec refinement.

**Exit gate:** `go = ripple.verdict ∈ {Go, Conditional-Go} ∧ omen.high_rpn_count == 0 ∧ echo.gate_pass`. On No-Go, escalate to the originating phase.

### Phase 6: Implementation Loop

Driven by Orbit. Orbit consumes accord L3 ACs + omen Mitigations + echo friction signals to author the loop contract, generates the nexus-autoloop script set, and audits convergence.

**Runner Engine: Codex CLI (fixed for Apex).** Apex pins Orbit's execution layer to **Codex CLI subagents** rather than Claude Code's Agent tool. All in-loop specialists (Builder / Artisan / Vitrine / Judge / Radar / Voyager) are spawned via `spawn_agent` and awaited via `wait_agent`. Phase 0-5 still run on Claude Code (Nexus orchestration); only the implementation loop crosses the engine boundary.

Why Codex CLI is fixed for Phase 6:
- **Iteration cost**: implementation loops typically run 4-8 iterations × 4-7 specialists = 16-56 spawns. Codex CLI subagents are tuned for high-volume autonomous coding cycles.
- **Context isolation**: each Codex subagent gets a fresh context window per iteration, avoiding context rot in Claude Code's main session.
- **Parallel branch ownership**: Codex CLI's `agents.max_depth` and explicit `spawn_agent` / `close_agent` lifecycle make file ownership and branch isolation cheaper to enforce than spawning Claude Code background agents.
- **Engine-mode handoff**: the Phase 5 → Phase 6 boundary becomes a clean engine switch (Claude Code → Codex CLI), making it easy to swap Codex for another runner per project policy without disturbing upstream phases.

| Agent | Role | Required | Spawn API |
|-------|------|----------|-----------|
| `orbit` | Loop contract design + convergence detection + cost-per-task tracking + circuit breaker | Yes | Spawned by Nexus on Claude Code, then writes Codex spawn scripts |
| `builder` | Business logic / backend implementation | Yes | Codex `spawn_agent` |
| `artisan` | Production frontend (promotes forge prototype) | Conditional: UI surface | Codex `spawn_agent` |
| `vitrine` | Storybook stories | Conditional: components added | Codex `spawn_agent` |
| `judge` | Per-iteration code review | Yes | Codex `spawn_agent` |
| `radar` | Unit / integration tests | Yes | Codex `spawn_agent` |
| `voyager` | E2E persona-driven tests (reuses echo personas) | Conditional: UI flows | Codex `spawn_agent` |

Orbit audits via Codex subagent return values: `convergence_detection`, `deduplication_guard`, `cost-per-completed-task`, `circuit_breaker`. Stuck-loop or budget-exceeded triggers `close_agent` on the running spawn and escalates to user.

**Engine availability check (Phase 5 → 6 handoff prerequisite):** Orbit verifies Codex CLI is reachable, `agents.max_depth ≥ 2`, and required subagent tools (`spawn_agent`, `wait_agent`, `send_input`, `resume_agent`, `close_agent`) are permitted before consuming the contract. If unavailable, Orbit fails the handoff with a clear runner error rather than silently falling back to Claude Code Agent — Apex's cost and convergence model assumes Codex execution.

### Ship

| Agent | Role | Required |
|-------|------|----------|
| `guardian` | Commit policy, branch strategy, PR preparation | Yes |
| `launch` | Release plan + CHANGELOG + rollback plan | Yes |

## Sub-Orchestration

| Sub-hub | Engine | Specialists | Cap |
|---------|--------|-------------|-----|
| Nexus (top) | Claude Code (Agent tool) | plea, field, riff, magi, accord, atlas, vision, orbit, guardian, launch | ≤10 (acceptable; phases serialise most) |
| Vision (UX sub) | Claude Code (Agent tool) | muse, palette, prose, flow, frame, forge, echo, polyglot, pixel | ≤9 (parallelisable inside) |
| **Orbit (loop sub)** | **Codex CLI (`spawn_agent`)** — fixed | builder, artisan, vitrine, judge, radar, voyager | ≤6 (loop iterations) |

Direct agent-to-agent handoff is forbidden across hubs. Within a sub-hub, the sub-orchestrator owns delegation. The Phase 5 → Phase 6 boundary doubles as an engine boundary: Claude Code (Nexus, Vision) → Codex CLI (Orbit). Orbit's spawn calls cross the engine via Nexus's documented Codex subagent contract (see `_common/SUBAGENT.md`).

## Conditional Agent Inclusion

| Condition | Add | Skip |
|-----------|-----|------|
| No-args / `goal=auto` invocation | Phase 0 (project_scan + spark + rank, plus voice/pulse/compete/sage/magi as data permits) | — |
| Goal supplied explicitly | — | Phase 0 entirely |
| Existing product (improvement) | echo in Phase 1 | — |
| New product (greenfield) | — | echo in Phase 1 |
| accord scope = Full | void, scribe | — |
| accord scope = Standard | scribe (optional) | void |
| accord scope = Lite | — | void, scribe |
| API change | gateway | — |
| DB change | schema | — |
| Motion in scope | flow | — |
| Figma in workflow | frame | — |
| Mockup supplied | pixel | — |
| Multi-locale | polyglot | — |
| UI surface | vision, muse, palette, prose, forge, echo, artisan, vitrine | — |
| Backend-only | (skip UX track entirely) | vision and downstream |
| UI flows present | voyager | — |

## Risk Gate Criteria

The Phase 5 Risk Gate is **tri-axis**. All three must pass:

1. **Failure mode coverage (omen)**: No High RPN residuals; AP-class A items have full Detection/Prevention/Recovery layers.
2. **Impact and blast radius (ripple)**: Verdict in `{Go, Conditional-Go}`. On Conditional-Go, omen Mitigations must address the conditions before forwarding to orbit.
3. **UX friction (echo)**: Emotion Valence ≥ baseline median; zero dark patterns; WCAG 3.0 Bronze tier average ≥ 3.5; cognitive load within target range.

**Plea-Echo divergence check** (early-warning): if plea's predicted user reaction and echo's measured prototype walkthrough diverge fatally on a top-priority demand, return to Phase 4 — do not proceed even if all three axes nominally pass.

## Workflow Accuracy Rationale

Nexus core rule: chains with 6+ agents require hierarchical decomposition. Apex satisfies this via two-tier sub-orchestration (Vision, Orbit). Sequential phase count is held at 6 because:

- Architect threshold: `85% per-step accuracy ^ 6 ≈ 38%` end-to-end. Acceptable only with verification gates between phases.
- Adding a 7th sequential phase drops projected success to ~32% — UX cannot become its own phase.
- Parallelisation does not multiply error rates because branches reconverge at the Risk Gate, not via shared mutable state.

Verification gates are mandatory:

- Phase 3 → 4: magi verdict carries measurable AC (not abstract narrative)
- Phase 4 → 5: accord traceability ≥ scope-mode threshold
- Phase 5 → 6: Risk Gate tri-axis pass
- Phase 6 internal: orbit convergence + cost-per-task + circuit breaker

## AUTORUN Chain Template

```
# ── Goal-supplied mode ───────────────────────────────
Nexus AUTORUN apex goal="<feature description>"
  ── Phase 1 Discovery ────────────────────────────────
  → [parallel] plea(personas=3+, output=demands+llm_prompts)
            ‖ field(BEST_validation, output=evidence)
            ‖ echo(current_flow)?           # if existing product
  ── Phase 2 Ideate ───────────────────────────────────
  → riff(diamond_thinking, max_turns=4)
  ── Phase 3 Verdict ──────────────────────────────────
  → magi(mode=engine, output=verdict+ac_seed)
  → [gate] split_decision → human_review
  ── Phase 4 Spec ─────────────────────────────────────
  → accord(scope=auto, input=magi_verdict)
       ├─(Full)→ void(yagni_check) → accord(refine)
       └─(M+)→  scribe(prd|srs|hld|lld)
  ── Phase 5 Design + Risk Gate ───────────────────────
  → [parallel:Tech]  atlas(adr) + (gateway? schema?)
  ‖ [parallel:UX]    vision(direction)
                       └─ muse(tokens)
                       └─ [parallel] palette ‖ prose ‖ flow?
                       └─ frame?
                       └─ forge(prototype)
                       └─ echo(walkthrough + WCAG3 + dark_pattern)
  → [Risk Gate] omen(fmea) ‖ ripple(blast) ‖ echo(emotion+a11y)
       go = ripple.ok ∧ omen.high_rpn==0 ∧ echo.gate_pass
       └─ No-Go → originating phase (4 or 5-track)
  ── Phase 6 Implementation Loop (engine = Codex CLI) ─
  → [engine_check] codex.available ∧ agents.max_depth≥2 ∧ subagent_tools_permitted
       └─ NG → handoff_error(runner_unavailable)
  → orbit(contract = accord.L3 + omen.mitigations + echo.friction, engine=codex)
       └─ nexus-autoloop emits Codex spawn scripts:
             codex.spawn_agent(builder, prompt=<BE contract>)        ‖
             codex.spawn_agent(artisan, prompt=<FE contract>)?
             → codex.wait_agent(all)
             → codex.spawn_agent(vitrine)? → codex.wait_agent
             → codex.spawn_agent(judge) → codex.wait_agent
             → codex.spawn_agent(radar) → codex.wait_agent
             → codex.spawn_agent(voyager)? → codex.wait_agent
       └─ orbit audits via Codex return values:
             convergence + cost-per-task + circuit_breaker
       └─ on stuck/budget → codex.close_agent + escalate
  ── Ship ─────────────────────────────────────────────
  → guardian(commit, branch, PR) → launch(release + rollback)


# ── Autonomous mode (no goal supplied) ───────────────
Nexus AUTORUN apex            # or: apex goal=auto
  ── Phase 0 Bootstrap ────────────────────────────────
  → [parallel:0a] project_scan(proactive)
                ‖ voice(real_feedback)?
                ‖ pulse(kpi_signals)?
                ‖ compete(gap_analysis)?
                ‖ trace(behavioural_signals)?
  → spark(propose 3-5 candidates from 0a)
  → rank(ICE|RICE|WSJF auto-select framework)
  → sage(socratic_check on #1)?
  → [select]
       margin>10% → auto_select #1
       top2 within 10% → magi(tie_break)
       all ICE<threshold → escalate "no clear goal" to user
  → [boundary_confirm]
       AUTORUN_FULL: 60s objection window → proceed
       AUTORUN     : explicit Y/N
       GUIDED      : explicit Y/N
       INTERACTIVE : confirm + allow edit
  ── Phase 1-6 + Ship: same as goal-supplied mode ─────
  → (proceed exactly as the Goal-supplied chain above, with
     `auto_selected_goal` bound as Phase 1 input)
```

## Failure Escalation

| Failure | Detected by | Escalation |
|---------|-------------|------------|
| Phase 0 no candidates | spark (autonomous mode) | Apex aborts, suggests user invoke with explicit goal |
| Phase 0 all ICE < threshold | rank (autonomous mode) | Present top 3 to user for manual selection |
| Phase 0 split tie-break | magi (autonomous mode) | Escalate top 2 to user with magi rationale |
| Phase 0 boundary rejected | user (autonomous mode) | Apex aborts; user input within 60s window cancels |
| Phase 3 split decision | magi | Pause for human verdict |
| Phase 4 traceability < threshold | accord | Re-run accord with scope downgrade or refine inputs |
| Risk Gate No-Go | omen / ripple / echo | Return to originating phase |
| Plea-Echo divergence | echo | Return to Phase 4 (accord re-spec) |
| Orbit stuck loop | orbit (convergence_detection) | Triage handoff |
| Orbit budget exceeded | orbit (cost-per-task) | User confirmation before continuation |
| Builder/Artisan repeat failure | judge / radar | Scout investigation, then back to orbit |

## Cost and Latency Profile

| Profile | Phases active | Approx agent count | Approx cost |
|---------|---------------|--------------------|-------------|
| Lite (no UI, accord=Lite) | 1, 2, 3, 4, 5-Tech, 5-Gate, 6 | 8-10 | Low |
| Standard (UI, accord=Standard) | All | 14-18 | Medium |
| Full (greenfield, accord=Full) | All + void + scribe + frame + polyglot | 20-25 | High |
| Autonomous bootstrap (Phase 0 added) | + 4-8 agents (project_scan + spark + rank + voice/pulse/compete/sage/magi as available) | +4-8 over base | + 10-20% over base |

Apex is not free. Budget guardrails (orbit cost-per-task, Nexus chain confirmation for 5+ agent chains, L4 confirmation gates) are enforced. Autonomous mode adds Phase 0 (~10-15 minutes, 4-8 agents) and one boundary-confirm checkpoint, but downstream cost is identical to goal-supplied mode. For repeated similar requests, propose a Sigil-generated project skill to amortise the chain design cost.

---

## Visualization

Mermaid flow diagram: [`apex-recipe-flow.mmd`](apex-recipe-flow.mmd) — render via mermaid.live or compatible viewer for the full apex topology.
