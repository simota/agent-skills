# Nexus Summit Recipe Reference

> **"Multiple engines, five teams, one verdict — quality maximized through orchestrated diversity."**
>
> Engine baseline and agy's optional third-axis role: see § Overview (and `_common/MULTI_ENGINE_RECIPE.md §Base Engine Policy`).

## Contents

- [Overview](#overview)
- [Invocation and Prerequisites](#invocation-and-prerequisites)
- [When to Use Summit](#when-to-use-summit)
- [Topology](#topology)
- [Engine × Team Matrix](#engine--team-matrix)
- [Phase Contracts](#phase-contracts)
- [Sub-Orchestration via Rally](#sub-orchestration-via-rally)
- [Cross-Engine Quorum Rules](#cross-engine-quorum-rules)
- [AUTORUN Chain Template](#autorun-chain-template)
- [Failure Escalation](#failure-escalation)
- [Cost and Latency Profile](#cost-and-latency-profile)
- [Comparison with Apex and Judge](#comparison-with-apex-and-judge)

---

## Overview

Summit is a **quality-maximization recipe** that mobilizes multiple execution engines across five functional teams (Analysis / Design / Execution / Verification / Improvement). It produces engine-attributed, multi-perspective deliverables for strategic decisions and high-stakes outputs where the cost of failure dramatically exceeds the cost of triangulation.

**Default baseline: Claude + Codex (dual-engine).** agy / Antigravity CLI is added as an **optional third axis** when AVAILABLE at PREFLIGHT — it contributes long-context (1M window), multimodal, High-effort-tier reasoning, and Search-grounding capabilities to Phase 1 / 3 / 4 / 5 when reachable, and is gracefully skipped when not (agy is mandated to Gemini 3.7 Flash (High) — `_common/CLI_COMPATIBILITY.md §4 ‡`; no Deep Think — its divergence value is Gemini model-priors at the High effort tier). Dual-engine mode (Claude + Codex) is the recipe's normal operating state, NOT a degraded mode. See `_common/MULTI_ENGINE_RECIPE.md §Base Engine Policy + §Engine Availability Modes`.

**Design Team conditional inclusion**: The Design team is included by default but skipped when Phase 0's `mission_charter.yaml` sets `ui_dimension: none` (pure backend / infrastructure tasks with no user-facing surface). When skipped, Design sub-tracks across all phases are bypassed and the recipe operates as a four-team workflow with proportionally reduced cost.

**Key design decisions:**
- **Claude is always the hub**; Codex and (optionally) Antigravity are accessed exclusively through `rally` (no direct CLI invocation from Nexus).
- **agy is optional** — see Overview for the tri-engine/dual-engine mode switch.
- **Multi-engine triangulation is load-bearing** in Phase 1 (Analysis) and Phase 4 (Verification) — and the dual-engine baseline satisfies it (the third axis is a quality lift, not a correctness gate).
- **Improvement loop is capped at 3 iterations** with Agent Tennis circuit breaker to prevent runaway cost.
- **Confirm before launch — always** (unconditional; same gate as `apex`/`wish`. Intentionally stronger than `podium`'s conditional gate — stated to prevent drift). Summit spawns 20-50 agents per run (tri-engine) or 14-36 (dual-engine).

---

## Invocation and Prerequisites

### Invocation

```
/nexus summit                 # Goal-supplied mode (current task context)
/nexus summit "<goal>"        # Explicit goal mode
```

### Prerequisites (preflight, in Nexus main context)

| Prerequisite | Check | Failure Action |
|--------------|-------|---------------|
| `claude` binary | always available (host) | n/a |
| `codex` binary | reachable via `which codex` or fallback paths (`~/.bun/bin/`, `~/.local/bin/`, `/usr/local/bin/`, `/opt/homebrew/bin/`, `~/.npm-global/bin/`) | abort with "Codex CLI required for summit; install or use apex/feature instead" |
| `agy` binary | reachable via `which agy` or fallback paths (same list) | **OPTIONAL** — record the verdict (AVAILABLE / UNAVAILABLE / RUNTIME-BROKEN) and surface the resulting mode in the confirmation prompt; never an abort (§ Overview) |
| `rally` skill available | check `~/.claude/skills/rally/SKILL.md` exists | abort with "rally skill required for engine bridging" |
| `rally.max_depth >= 2` (Codex config) | inspect `~/.codex/config.toml` | warn and continue; sub-spawning may fail |
| User cost acknowledgment | mandatory confirmation prompt | abort if declined |
| Mission charter producible | Phase 0 must produce valid `mission_charter.yaml` | abort if FRAMING fails |

---

## When to Use Summit

### Use Summit for

- Strategic decisions with multi-year impact (architecture pivots, platform migrations, product direction)
- Final pre-release verification for high-risk launches (financial, medical, safety-critical)
- Large refactors where blind spots compound (legacy modernization, security overhauls)
- Decisive differentiator features where competitor analysis must triangulate with internal user research and creative reframing
- Any task where the cost of an undetected error exceeds the cost of 20-50 agents and 1-2 hours of wall time

### Do NOT use Summit for

- Single-feature implementation → `feature` or `apex`
- PR review → `judge` (already tri-engine)
- Routine bug fixes → `bug`
- Performance tuning of a known hotspot → `optimize`
- Time-bounded tasks (under 30 min) → `feature` or direct agent
- Cost-sensitive contexts (individual hobby projects, small teams) → simpler recipes
- Linear tasks with no parallelism benefit → sequential chain

### Do NOT use Summit when

- Codex is unavailable → use single-engine chain or `apex` (Codex is required — see Overview)
- User has not confirmed the cost envelope
- The task does not have a clear acceptance criteria definable in Phase 0

> If you specifically need agy's third-axis lift (long-context whole-codebase reasoning, multimodal asset reading, High-effort-tier alternatives, Search-grounded competitive analysis) and agy is broken, defer Summit until agy is back rather than swapping recipes.

---

## Topology

```
                  ┌──────────────────────────────────┐
                  │       Nexus (Claude, hub)        │
                  └────────────────┬─────────────────┘
                                   │
       ┌───────────────────────────┼───────────────────────────┐
       │                           │                           │
   Phase 0                     Phase 1                     Phase 2
   FRAMING                     ANALYSIS                    PLANNING
   (Claude only)               (tri-engine ‖)              (Claude opus)
       │                           │                           │
       ▼                           ▼                           ▼
  mission_charter        analysis_consensus              execution_plan
                                                               │
                                                               ▼
                                    ┌──────────────────────────────────────┐
                                    │  Phase 3 (Design ‖ Execution Tracks) │
                                    │  ┌──────────────────────────────┐    │
                                    │  │ DESIGN TRACK (if UI)         │    │
                                    │  │  Vision (claude) coordinates;│    │
                                    │  │  agents per engine × team    │    │
                                    │  │  matrix below                │    │
                                    │  └──────────────────────────────┘    │
                                    │  ┌──────────────────────────────┐    │
                                    │  │ EXECUTION TRACK              │    │
                                    │  │  rally[COLLABORATE]          │    │
                                    │  │  Target: 60% Codex /         │    │
                                    │  │          25% agy /           │    │
                                    │  │          15% Claude (judg.)  │    │
                                    │  └──────────────────────────────┘    │
                                    │  Convergence: Frame bridges design   │
                                    │              → implementation        │
                                    └──────────────────────────────────────┘
                                                               │
                                                               ▼
                                    ┌──────────────────────────────────────┐
                                    │  Phase 4 VERIFICATION TEAM (‖)       │
                                    │  judge (tri-engine built-in) +       │
                                    │  per-engine agents — see Engine ×    │
                                    │  Team Matrix (Verification row)      │
                                    └──────────────────────────────────────┘
                                                   │
                                  CONFIRMED/LIKELY findings
                                                   │
                                                   ▼
                                    ┌──────────────────────────────────────┐
                                    │  Phase 5 IMPROVEMENT LOOP (max 3×)   │
                                    │  orbit drives per-engine agents —    │
                                    │  see Engine × Team Matrix            │
                                    │  (Improvement row); magi arbitrates  │
                                    │  → Phase 3 loop                      │
                                    └──────────────────────────────────────┘
                                                               │
                                                               ▼
                                                          Phase 6
                                                          DELIVERY
                                                  (Guardian + Launch)
                                                               │
                                                               ▼
                                                   NEXUS_COMPLETE
```

---

## Engine × Team Matrix

> **This matrix is the sole owner of agent → engine assignments.** Per-phase contracts below (Phase 0-6) list only phase-specific deltas (gates, inputs, branch names) — for which agent runs on which engine, consult this matrix.

**Engine routing principle:** route each agent to the engine whose distinctive strength best fits the agent's job — Claude is reserved for judgment, orchestration, and ethics; Codex owns code generation, sandbox execution, and test running (Terminal-Bench 77.3% leader); agy owns long-context analysis (1M window), multimodal asset work, High-effort-tier creative alternatives (Gemini 3.7 Flash (High), High tier — no Deep Think), and Search grounding. Each cell below lists the agents spawned on that engine for that team.

| | Claude (hub — judgment & orchestration) | Codex (sandbox & code generation) | Antigravity / agy (long-context & multimodal) |
|---|---|---|---|
| **Analysis** | Atlas (architecture trade-offs, ADR drafting), Sherpa (epic decomposition), magi (arbitration of cross-engine findings) | Lens (sandbox-aided codebase mapping), Scout (bug RCA via test execution), Sentinel (SAST scan), Siege (concurrency analysis) | Trail (git-history archaeology, 1M ctx), Trail (legacy code archaeology), Lore (cross-codebase pattern extraction), Atlas (architecture C4 diagrams via multimodal), Field (web-grounded market/tech survey) |
| **Design** *(conditional)* | Vision (direction & arbitration), Echo (persona walkthrough), Prose (UX writing & microcopy) | Pixel (mockup-to-HTML/CSS), Forge (prototype implementation), Flow (CSS/JS animation), Funnel (LP construction), Vitrine (component catalog generation), Builder[image] (image-generation API integration) | Muse (token system synthesis via multimodal mockup analysis), Frame (Figma context extraction via multimodal), Palette (a11y + interaction-quality from screenshots), rally[agy, COMPETE, Flash-High] (creative alternative directions), Ink (SVG icon system generation) |
| **Execution** | Sentinel (security review of generated code), Cloak (privacy review), Crypt (crypto architecture), magi (escalation arbitration), scribe[unified] (atomic-spec gatekeeping) | Builder (general implementation), Artisan (frontend production), Native (iOS Swift / Android Kotlin), Schema (DB migrations), Bolt (perf-aware implementation), rally[COLLABORATE, codex] (bulk task distribution across DAG) | rally[COLLABORATE, agy] (alternative-implementation generation), Scribe (long-context spec & doc generation), Tome (learning-doc generation from diff), Scribe (cross-format document conversion) |
| **Verification** | judge (tri-engine review with built-in fan-out), Echo (UX persona walkthrough), Palette (interaction & a11y), magi (verdict arbitration on conflicts) | Radar (unit/integration tests), Voyager (E2E web + mobile), Siege (load/chaos), Siege (concurrency stress), Probe (dynamic security), Matrix (manual QA scenarios), Sentinel (re-scan post-fix) | Attest (spec compliance via long-context comparison), Ripple (vertical + horizontal impact analysis), Canon (standards compliance: OWASP/WCAG/ISO 25010), Canon[regulatory] (legal/regulatory), rally[agy, review] (independent multimodal review of generated UI screenshots) |
| **Improvement** | Zen (refactor judgment & code-review-style improvements), Magi (improvement-selection arbitration and knowledge synthesis) | Bolt (perf optimization), Tuner (DB query plan + index recommendations), Sweep (dead code removal), Mend (automated remediation runbook execution), Schema (migration improvements) | Atlas (architecture improvement via 1M ctx whole-codebase reasoning), Lore (pattern extraction & metapattern surfacing), Vista (long-range strategic refactor planning), Shift (deprecated-library detection, native-API modernization, tech radar — absorbed from horizon — plus framework/lang migration codemod generation) |

**Cross-engine routing table — canonical.** This is the single owner of the per-task engine heuristic; every phase that assigns a task to an engine (Phase 2 DAG planning, Phase 3 Track B, and every rally dispatch) applies this table rather than restating it.

| Task characteristic | Engine | Why |
|--------------------|--------|-----|
| Code generation, refactor, file edits, DB migration (Schema), mobile native (Native), frontend production (Artisan) | **Codex** | 192K context, sandbox-first, Terminal-Bench 2.0 / 77.3% leader |
| Test writing and test execution | **Codex** | Sandbox-first, fast iteration |
| Holding > 200K tokens of context — large-codebase analysis, full doc set, long-context spec/doc generation (Scribe/Tome) | **agy** | 1M context window |
| Images, mockups, screenshots, diagrams; cross-format conversion (Scribe) | **agy** | Native multimodal support |
| Creative divergence / alternative exploration | **agy** (Gemini 3.7 Flash, High tier) or rally[agy, COMPETE] | Different (Gemini) reasoning priors |
| Architecture decisions, design judgment, arbitration between perspectives, Go/No-Go calls (Atlas, Vision, magi) | **Claude** | Strongest at trade-off reasoning |
| Security, ethics, privacy/crypto, regulatory review (Sentinel/Cloak/Crypt/Canon[regulatory]) | **Claude** | Deepest reasoning, OWASP knowledge baseline |
| Spec gatekeeping between phases (Scribe[unified]) | **Claude** | Judgment-critical |
| Ambiguous **risk** class — could be security-sensitive or architecture-defining | **Claude** | Safe default when the risk class itself is unclear |
| Anything else (routine, clearly non-judgment work) | **Codex** | Faster + cheaper; the fallback is Codex, **not** Claude |

---

## Phase Contracts

### Phase 0: Framing (Claude only, 1-2 agents, 3-5 min)

**Input:** User request (goal text or "/nexus summit" with current task context)

**Agents:**
1. Nexus[classify] — task type detection, complexity scoring
2. Scribe[unified: L0-L1 spec] — staged elaboration of vision and requirements (optional, skip if user provides explicit goal)
3. Sherpa[atomic decomposition] — break into team missions

**Output:** `mission_charter.yaml`

```yaml
goal: "<explicit goal statement>"
acceptance_criteria:
  - "<measurable criterion 1>"
  - "<measurable criterion 2>"
team_missions:
  analysis:     "<what analysis must answer>"
  execution:    "<what execution must produce>"
  verification: "<what verification must validate>"
  improvement:  "<what improvement axis to optimize>"
cost_budget:
  max_agents: 50
  max_wall_time_minutes: 120
  max_loops: 3
risk_tier: strategic | release-critical | major-refactor
user_acknowledged: true
```

**Gate: Ask First** when `cost_budget.max_agents × estimated_token_cost > L4 threshold` OR `risk_tier ∈ {strategic, release-critical}` — this is the L4 tier on top of the unconditional Confirm-before-launch gate; require explicit user confirmation before proceeding to Phase 1.

---

### Phase 1: Analysis Team (tri-engine parallel + optional Design sub-track, 6-11 agents, 8-15 min)

**Input:** `mission_charter.yaml`

**Parallel branches (L2 spawn, isolated sub-contexts). Rosters are owned by § Engine × Team Matrix — each branch names its Matrix cell plus any phase-specific delta:**

```yaml
parallel:
  - branch: claude_judgment
    engine: claude
    agents: Matrix[Analysis × Claude] less magi (magi runs at synthesis, below)
    mission: architecture trade-off reasoning + epic decomposition
    output: claude_analysis.json

  - branch: codex_code_analysis
    engine: codex (direct spawn, not via rally wrapper)
    agents: Matrix[Analysis × Codex]
    mission: sandbox-aided codebase mapping + bug RCA + SAST scan + concurrency analysis
    output: codex_analysis.json

  - branch: agy_long_context
    engine: agy (direct spawn, not via rally wrapper)
    agents: Matrix[Analysis × agy]
    mission: git-history + legacy archaeology, pattern extraction, C4 diagrams, web-grounded market survey
    output: agy_analysis.json

  - branch: design_analysis   # conditional: skip if ui_dimension == none
    parallel_sub:
      - {engine: claude, agents: [echo], mission: persona-based UX walkthrough}
      - {engine: agy,    agents: [frame, palette], mission: Figma/screenshot extraction + interaction-quality scan}
    output: design_analysis.json
```

**Synthesis:** `magi[arbitrate-tri-engine]` runs Logos / Pathos / Sophia perspectives across all three engine reports.

**Output:** `analysis_consensus.md`
```yaml
consensus_findings: [...]    # 3/3 agreement
likely_findings:    [...]    # 2/3 agreement
minority_signals:   [...]    # 1/3 — kept for transparency, marked as low confidence
disputed_findings:  [...]    # active disagreement requiring user judgment
engine_attribution: {...}    # which finding came from which engine
```

**Gate:** disputed-findings ratio exceeds threshold → escalate to user before Phase 2 (threshold + rationale defined once in § Cross-Engine Quorum Rules → Disagreement escalation).

---

### Phase 2: Planning (Claude opus, 2-3 agents, 5-8 min)

**Input:** `analysis_consensus.md`

**Agents:**
1. Sherpa[plan_DAG] — convert findings into atomic task DAG
2. Magi[trade-off arbitration] — resolve plan-level conflicts

**Engine assignment:** Sherpa tags every DAG task with an engine by applying the canonical cross-engine routing table (§ Engine × Team Matrix) — the per-task assignments this phase emits are what Phase 3 Track B dispatches against.

**Output:** `execution_plan.yaml`
```yaml
tasks:
  - id: T1
    description: "..."
    engine: claude | codex | agy
    dependencies: []
    risk_level: low | medium | high
    estimated_agents: N
  - id: T2
    ...
parallel_groups:
  - [T1, T3]    # can run together
  - [T2]        # must wait for T1
```

**Model selection:** Phase 2 uses `claude-opus` for planning (Plan-and-Execute pattern: capable model plans, cheaper models execute — up to 90% cost reduction in execution phase).

---

### Phase 3: Design + Execution Teams (parallel tracks, 7-22 agents, 25-75 min)

When `ui_dimension != none`, Phase 3 splits into **two parallel tracks** that run concurrently and converge through Frame (design → code bridging) before Phase 4.

**Track A: Design Team** (5-10 agents, 10-25 min) — aggressive codex/agy usage

```yaml
design_track:
  coordinator: vision   # Claude — direction + arbitration only (judgment role)
  parallel:
    - branch: claude_judgment
      engine: claude
      agents: Matrix[Design × Claude]
      mission: direction-setting, UX writing/microcopy, persona validation
    - branch: codex_implementation
      engine: codex
      agents: Matrix[Design × Codex]
      mission: mockup-to-HTML/CSS, prototype implementation, animation code, LP construction, component catalog
    - branch: agy_creative_multimodal
      engine: agy
      agents: Matrix[Design × agy] less rally (own branch, below)
      mission: image generation, token synthesis from mockups, Figma extraction, a11y/interaction from screenshots, SVG icons
    - branch: agy_divergent
      engine: agy
      agent: rally
      paradigm: COMPETE
      mode: Solo
      mission: creative alternative directions via Gemini High-effort-tier exploration
  synthesis:
    agent: vision (claude)
    role: arbitrate-design-direction
    convergence: single design direction (no enumeration); rejected directions surfaced with one-line reason
  output: design_direction.yaml + design_tokens.json + prototype_links + image_assets
```

**Track B: Execution Team** (5-15 agents, 20-60 min) — Codex-heavy by default

**Coordinator:** rally[COLLABORATE]

**Default engine assignment:** per-task, as tagged by the Phase 2 planner from the canonical cross-engine routing table (§ Engine × Team Matrix). Track B dispatches each task to the engine the plan names; it does not re-decide routing.

**Process:**
1. rally receives `execution_plan.yaml` and DAG with per-task engine assignments
2. Codex tasks (majority): rally dispatches to `codex exec` with task-specific spec
3. agy tasks (long-context / multimodal / creative): rally dispatches to `agy`
4. Claude tasks (only judgment / security / arbitration): direct Agent spawn
5. Per parallel_group, all tasks fan out concurrently across engines
6. Integration step after each group: Nexus aggregates, resolves file-level conflicts using `conflict-resolution.md` ownership rules

**Default engine distribution target:** ~60% Codex, ~25% agy, ~15% Claude (judgment only). Deviation from this distribution is allowed but logged in execution report so the user can audit engine routing.

**Track convergence:** When both tracks complete, Frame (Claude) bridges design tokens and component contracts into the implementation, and rally[Artisan / Native] applies UI bindings. If `ui_dimension == none`, only Track B runs.

**Checkpoint:** after each parallel_group completes in either track, persist outputs (Core Rule: 4+ step chains need checkpoint-resume).

**Output:** Working implementation + design direction + tokens + prototypes + per-task execution log + engine attribution per file.

---

### Phase 4: Verification Team (tri-engine quorum + optional Design sub-track, 4-9 agents, 10-25 min)

**Parallel branches.** Rosters per § Engine × Team Matrix (Verification row); each branch names its cell plus any phase-specific delta:

```yaml
parallel:
  - branch: judge_review
    agent: judge
    mode: tri-engine (built-in: codex + agy + claude reviewers in parallel via judge's own fan-out)
    output: judge_findings.json

  - branch: codex_dynamic_verification
    engine: codex
    agents: Matrix[Verification × Codex]
    mission: unit/integration + E2E web+mobile + load/chaos + concurrency stress + dynamic security probe
        + post-fix SAST re-scan + manual QA scenario authoring
    output: codex_verification.json

  - branch: agy_static_compliance
    engine: agy
    agents: Matrix[Verification × agy] less rally (own branch, below)
    mission: spec compliance, vertical+horizontal impact, standards (OWASP/WCAG/ISO 25010), legal/regulatory
        — all need 1M context to hold spec + implementation simultaneously
    output: agy_compliance.json

  - branch: agy_independent_review
    engine: agy
    agent: rally
    paradigm: COMPETE
    mode: Solo
    mission: independent multimodal review of generated UI screenshots and outputs
    output: agy_review.json

  - branch: claude_judgment_verification
    engine: claude
    agents: Matrix[Verification × Claude] less judge (own branch) and magi (arbitration only)
    if: ui_dimension != none
    mission: persona-based UX walkthrough + interaction-quality and a11y check
    output: design_findings.json
```

judge keeps its own internal tri-engine fan-out unchanged.

**Design findings integration:** Echo's persona friction reports and Palette's interaction-quality issues join the cross-engine quorum as an additional signal source alongside judge / codex_dynamic / agy_static / agy_review. A UX regression flagged by Echo is treated as LIKELY severity by default and feeds the Phase 5 improvement loop alongside code-side findings.

**Quorum rules** (label definitions in § Cross-Engine Quorum Rules below; this table crosses them with severity):

| Concurrence | Finding Severity | Action |
|-------------|------------------|--------|
| CONFIRMED (3/3 agree) | CRITICAL or HIGH | Block release → force Phase 5 |
| CONFIRMED (3/3 agree) | MEDIUM or LOW | Annotate, deliver with caveat |
| LIKELY (2/3 agree) | CRITICAL or HIGH | Force Phase 5 |
| LIKELY (2/3 agree) | MEDIUM or LOW | Annotate |
| CANDIDATE (1/3 only) | any | Grounding verification by Nexus → if VERIFIED → treat as LIKELY |

**Output:** `verification_report.md` with engine-attributed findings, concurrence labels, and quorum verdict.

**Gate:** If any CONFIRMED+CRITICAL/HIGH or LIKELY+CRITICAL/HIGH finding → mandatory Phase 5 loop.

---

### Phase 5: Improvement Team (PDCA loop, 3-6 agents per loop, max 3 loops)

**Driver:** project-local Orbit when available; otherwise Nexus drives the bounded loop directly and records `project_local_fallback: true` (`_common/PROJECT_LOCAL_SKILLS.md`).

**Per-loop process.** Rosters per § Engine × Team Matrix (Improvement row); each branch names its cell plus any phase-specific delta:

```yaml
loop_iteration:
  parallel_improvement_proposals:
    - branch: claude_judgment_only
      engine: claude
      agents: Matrix[Improvement × Claude] less magi (arbitration step, below)
      mission: refactor judgment + knowledge synthesis

    - branch: codex_executable_improvements
      engine: codex
      agents: Matrix[Improvement × Codex]
      mission: perf optimization, DB query-plan/index work, dead-code removal, remediation runbooks,
          schema migration improvements — Codex sandbox enables safe verification
    - branch: agy_strategic_improvements
      engine: agy
      agents: Matrix[Improvement × agy] less vista (long-range planning is out of the loop's scope)
      mission: whole-codebase 1M-ctx architecture improvement, cross-codebase pattern/metapattern extraction,
          Shift `detect`/`modernize`/`radar` + `framework`/`lang`/`codemod`
    - branch: design_improvements   # conditional: skip if ui_dimension == none
      parallel_sub:
        - {engine: claude, agents: [vision], mission: design direction refinement (judgment)}
        - {engine: agy, agents: [palette, muse], mission: visual + token refinement based on Phase 4 design_findings.json via multimodal}

  arbitration:
    agent: magi
    role: select-improvements-to-apply
    output: applied_improvements.yaml (with per-improvement rationale)

  apply_loop:
    if applied_improvements.non_empty:
      → Phase 3 (re-execute affected tasks)
      → Phase 4 (re-verify)
      → check Phase 4 quorum:
          if CONFIRMED/LIKELY CRITICAL still present → next iteration (up to max_loops)
          else → exit loop, proceed to Phase 6
    else:
      → exit loop, proceed to Phase 6
```

**Circuit breakers:**

| Condition | Action |
|-----------|--------|
| `loop_count >= max_loops` (default 3) | Exit loop, deliver with caveat about remaining issues |
| Agent Tennis: same issue debated 3+ turns without resolution | Trip circuit breaker, escalate to user |
| Cost budget projected to exceed | Reduce loop scope to CRITICAL findings only |
| All quorum findings resolved | Exit loop early (success path) |

---

### Phase 6: Delivery (Claude, 1-2 agents, 3-5 min)

**Agents:**
1. Guardian[PR-prep] — classify changes, recommend granularity, prepare commit strategy
2. Launch[release-plan] — versioning, CHANGELOG, release notes, rollback plan

**Output:** `NEXUS_COMPLETE` with the full evidence trail:

```markdown
## Nexus Execution Report

Task: <goal>
Chain: summit (3-engine, 4-team)
Mode: AUTORUN_FULL with mandatory pre-launch confirmation

### Phase Results
| Phase | Status | Engine Attribution | Key Output |
| ...

### Engine Contributions
- Claude:    <files / decisions / findings>
- Codex:     <files / decisions / findings>
- agy:       <files / decisions / findings>

### Quorum Summary
- CONFIRMED findings: N (all resolved | N remaining)
- LIKELY findings:    N
- Minority signals:   N (kept for transparency)

### Improvement Loop Summary
- Loops executed: N / 3
- Improvements applied: N
- Circuit breaker tripped: yes/no

### Verification
- Tests:        pass/fail summary
- Build:        result
- judge:        N findings (severity breakdown)
- Ripple:       impact scope

### Summary
<status, recommended next steps, follow-ups>

### Cost
- Wall time:        N minutes
- Total agents:     N
- Estimated tokens: ~N M
```

---

## Sub-Orchestration via Rally

`rally` is the **single point of contact** for Codex and agy. Nexus never calls codex or agy directly.

### Rally delegation patterns used by Summit

| Phase | Paradigm | Engines | Mode | Purpose |
|-------|----------|---------|------|---------|
| 1 ANALYSIS | COMPETE | codex (alone) | Team | Codex-perspective analysis |
| 1 ANALYSIS | COMPETE | agy (alone) | Team | agy-perspective analysis |
| 3 EXECUTION | COLLABORATE | codex + agy | Team | Task decomposition across engines |
| 3 EXECUTION | COMPETE | agy (alone) | Solo | Alternative implementation proposals |
| 4 VERIFICATION | COMPETE | agy (alone) | Solo | Independent review |
| 5 IMPROVEMENT | COMPETE | agy (alone) | Solo | Pattern extraction + architectural alternatives |

### Engine isolation contract

Each rally invocation produces an isolated sub-context for the target engine. Findings/outputs flow back to Nexus through `_STEP_COMPLETE` with engine attribution. **Cross-engine contamination is prevented at the rally boundary** — engines never see each other's intermediate outputs during a phase.

---

## Cross-Engine Quorum Rules

Applied in Phase 1 (Analysis synthesis) and Phase 4 (Verification).

### Concurrence Labels

| Label | Definition | Default Trust |
|-------|------------|---------------|
| CONFIRMED | 3/3 engines independently surface the same finding | High — proceed without grounding |
| LIKELY | 2/3 engines surface the same finding | Medium — proceed but flag |
| CANDIDATE | 1/3 engines surface a finding | Low — requires grounding verification by Nexus before action |
| MINORITY | 1/3 engines surface a finding that other engines explicitly considered and rejected | Very low — log as transparency, do not act |

### Grounding verification protocol (for CANDIDATE findings)

Nexus (in main context) reads the actual code referenced by the finding and classifies:

| Verdict | Definition | Treatment |
|---------|------------|-----------|
| VERIFIED | Finding accurately describes a real issue | Promote to LIKELY |
| REJECTED | Finding does not match code reality | Discard, log as engine false positive |
| MITIGATED | Finding describes a real issue that is already addressed elsewhere | Discard with note |
| STYLE-ONLY | Finding is preference, not correctness | Discard |
| NEEDS-INFO | Cannot verify without external context | Escalate to user |

### Disagreement escalation

If `disputed_findings / total_findings > 0.30` in Phase 1, Nexus pauses and presents the disagreement matrix to the user before proceeding. This catches recipe-level failures where one engine has fundamentally misunderstood the task.

---

## AUTORUN Chain Template

> The run skeleton only. Per-phase rosters come from § Engine × Team Matrix; per-phase inputs, outputs, branch structure, and gate criteria come from § Phase Contracts. Both are authoritative over this template.

```yaml
recipe: summit
mode: AUTORUN_FULL
required_confirmation: true   # ALWAYS — same gate as apex
prerequisites:
  - claude_available:  true
  - codex_available:   true    # abort if false — Codex is required
  - agy_available:     detect  # optional third axis (§ Overview)
  - rally_skill:       true
  - cost_acknowledged: true

phase_chain:
  - phase: 0_framing
    engine: claude
    duration_minutes: [3, 5]

  - phase: 1_analysis
    parallel: one branch per engine + design sub-track (if ui_dimension != none)
    synthesis: {agent: magi, engine: claude, role: arbitrate-tri-engine}
    duration_minutes: [8, 15]
    gate: disputed_findings_ratio < 0.30

  - phase: 2_planning
    engine: claude
    model: opus
    duration_minutes: [5, 8]

  - phase: 3_design_and_execution
    parallel_tracks:
      - track: design         # if ui_dimension != none
        coordinator: vision (claude)
        synthesis: {agent: vision, convergence: single_direction}
      - track: execution
        coordinator: rally
        paradigm: COLLABORATE
        engine_distribution_target: {codex: 0.60, agy: 0.25, claude: 0.15}
    convergence: frame_bridges_design_to_implementation
    duration_minutes: [25, 75]
    checkpoint: after_each_parallel_group

  - phase: 4_verification
    parallel: judge[tri-engine-builtin] + one branch per engine
    quorum: cross_engine_3_of_3
    duration_minutes: [10, 25]

  - phase: 5_improvement
    driver: orbit
    max_loops: 3
    arbiter: magi
    circuit_breakers: [agent_tennis_3_turns, cost_budget_overrun, loops_exceeded]
    per_loop_minutes: [10, 15]

  - phase: 6_delivery
    engine: claude
    output: NEXUS_COMPLETE
    duration_minutes: [3, 5]
```

---

## Output Report — **Summit Verdict** (named)

Emitted inside `NEXUS_COMPLETE` on top of the base `## Nexus Execution Report`:

- **Engine roster** — which engines were reachable, the resulting quorum rule (3/3 or degraded 2/2), and any mid-run DEGRADED transition
- **Finding ledger** — every finding with its per-engine votes and resulting CONFIRMED / LIKELY / disputed status
- **Dispute record** — the `disputed_findings / total_findings` ratio and the Phase 1 escalation outcome when it exceeded 0.30
- **Design sub-track findings** — Echo / Palette results folded into the quorum, when the run included them
- **Improvement trajectory** — per-cycle results across the ≤ 3 cycles, Agent Tennis breaker status
- **Release disposition** — blocked / delivered-with-caveat per the CONFIRMED × severity table
- **Exit reason** (canonical vocabulary) + residual gap when not `ACCEPT`

## Failure Escalation

Merged view of every failure mode Summit guards against, with detection phase and escalation threshold (supersedes a separate "Failure Modes Prevented" table — same content, one table).

| Failure | Detection Phase | Mitigation | Escalation Threshold |
|---------|----------------|-----------|--------------------|
| Single-engine blind spot accepted as truth | Any phase (structural) | **Tri-engine quorum**: a finding is CONFIRMED only on 3/3 agreement; single-engine findings are LIKELY at best | N/A (design guarantee) |
| agy CLI unreachable | Preflight | Dual-engine mode (§ Overview); agy branches recorded as `skipped (engine unavailable)`, Phase 1/4 quorum degrades to 2/2 (CONFIRMED only) | Never — not an abort |
| codex CLI unreachable | Preflight | Abort with message "use apex (claude only) instead" (Codex is required) | Immediate |
| agy fails mid-run (after preflight: quota / OAuth / executor / subagent timeout) | Any phase | Mark agy DEGRADED, absorb its workload into Claude/Codex per engine-strength routing, continue in dual-engine mode; log the transition | Never (graceful) |
| Phase 1 disputed-findings ratio exceeds threshold | Phase 1 synthesis | Pause, present disagreement matrix (definition + rationale in § Cross-Engine Quorum Rules → Disagreement escalation) | Immediate |
| Phase 4 CONFIRMED CRITICAL/HIGH after max_loops | Phase 5 exit | Deliver with explicit "unresolved CRITICAL" caveat; non-`ACCEPT` exit reports best-so-far + residual gap | Always |
| Agent Tennis (same issue debated 3+ turns without resolution) | Phase 5 loop | Circuit breaker trips, deliver | Always |
| Runaway/overrun cost | Per-phase gate (Phase 0 pre-authorizes; Phase 5 caps `loop ≤ 3`) | Reduce remaining scope to CRITICAL findings only; if still over, escalate | After 50% budget consumed |
| Engine returns invalid schema 3× | Per-phase | Treat engine as DEGRADED for remainder of run, continue with remaining 2 engines (Phase 1/4 quorum degrades to 2/2) | After 3rd schema violation |
| Total wall time > 2× estimate | Per-phase | Pause, present time-vs-quality trade-off to user | Always |
| UX regressions invisible to code-only review | Phase 4 (Design sub-track) | Echo persona-friction + Palette interaction-quality findings join the cross-engine quorum as a first-class signal at LIKELY severity | N/A (structural) |
| The producer reviewing its own output | Phase 4 (Verification Team) | Verification Team is Generator-excluded (Q9) per `reference/autonomy-quality-protocol.md` | N/A (structural) |

**Hard rule:** only a **Codex** failure is a recipe-level failure — unreachable at preflight aborts, mid-run requires user judgment. Every agy outcome is handled by the rows above and announced, never silent.

---

## Cost and Latency Profile

### Per-phase profile (Design Team included; subtract Design sub-track agents/time when `ui_dimension == none`)

Agent counts updated to reflect the rebalanced engine routing (more Codex + agy specialists per phase):

| Phase | Agents (UI / non-UI) | Parallel | Wall Time (UI / non-UI) | Tokens |
|-------|----------------------|----------|--------------------------|--------|
| 0 FRAMING | 1-2 / 1-2 | 1 | 3-5 min | ~30K |
| 1 ANALYSIS | 13-16 / 11-14 | 4-5 / 3 | 8-15 min | ~280-380K |
| 2 PLANNING | 2-3 / 2-3 | 1 | 5-8 min | ~60K (opus) |
| 3 DESIGN+EXEC | 13-27 / 5-15 | 4-6 / 3-5 | 25-75 min / 20-60 min | ~600-1700K |
| 4 VERIFICATION | 14-18 / 12-16 | 5 / 4 | 10-25 min / 10-20 min | ~280-360K |
| 5 IMPROVEMENT (per loop) | 13-17 / 10-14 | 4 | 10-20 min / 10-15 min | ~200-280K |
| 6 DELIVERY | 1-2 / 1-2 | 1 | 3-5 min | ~20K |

### Total envelopes

| Scenario | Agents (UI / non-UI) | Wall Time (UI / non-UI) | Tokens |
|----------|----------------------|--------------------------|--------|
| No improvement loops | 44-68 / 32-50 | 54-133 min / 49-113 min | 1.45-2.7M |
| 1 loop | 57-85 / 42-64 | 64-153 min / 59-128 min | 1.65-3.0M |
| 2 loops | 70-102 / 52-78 | 74-173 min / 69-143 min | 1.85-3.3M |
| 3 loops (max) | 83-119 / 62-92 | 84-193 min / 79-158 min | 2.05-3.6M |

### Engine distribution targets

| Engine | Target share of total agent-minutes | Cost rationale |
|--------|-------------------------------------|---------------|
| **Codex** | ~50-55% | Sandbox + Terminal-Bench leader; cheapest per code-gen task |
| **agy** | ~25-30% | 1M context + multimodal native; cheapest per long-context/visual task |
| **Claude** | ~20% | Judgment + orchestration only; most expensive per token, irreplaceable for reasoning |

Phase 6 DELIVER includes an "Engine Distribution Audit" section showing actual vs target shares so the user can detect drift back toward Claude-default.

### Cost comparison

| Recipe | Agents | Wall Time | Relative $ Cost |
|--------|--------|-----------|------------------|
| `feature` | 3-5 | 5-15 min | 1× (baseline) |
| `apex` | 8-25 | 30-90 min | 4-8× |
| `summit` non-UI (no loops) | 32-50 | 49-113 min | 7-13× |
| `summit` UI (no loops) | 44-68 | 54-133 min | 9-16× |
| `summit` non-UI (3 loops) | 62-92 | 79-158 min | 11-20× |
| `summit` UI (3 loops) | 83-119 | 84-193 min | 13-25× |

**Rule of thumb:** Summit costs 7-25× a typical `feature` chain depending on UI inclusion and loop count. Use only when the cost of failure exceeds the cost of triangulation by at least an order of magnitude. For pure-backend strategic work, force `ui_dimension: none` in Phase 0 to skip the Design Team and recover ~25% of cost.

---

## Comparison with Apex and Judge

| Dimension | `apex` | `judge` | `summit` |
|-----------|--------|---------|---------|
| **Purpose** | Full-cycle feature delivery (discovery → ship) | Cross-engine code review | Quality-maximizing strategic execution |
| **Engines** | Claude + Codex | Claude + Codex + agy (review only) | Claude + Codex + agy (full participation) |
| **Structure** | Phase-driven linear with sub-orchestration | Single-phase parallel review | 5-team × 3-engine matrix with PDCA loop |
| **Teams** | Implicit (sub-orchestrators) | Single (verification) | Explicit (analysis / **design** / execution / verification / improvement; Design conditional on `ui_dimension`) |
| **Verification** | Risk Gate (pre-implementation) + Judge in loop | Tri-engine quorum review | Cross-engine quorum + grounded verification + UX walkthrough + improvement loop |
| **Loop** | Implementation loop (Orbit) | None (single-shot) | Improvement loop (max 3, magi-arbitrated, includes design refinement) |
| **Agents** | 8-25 | 3-6 | 20-50 (tri-engine) / 14-36 (dual-engine) |
| **Wall time** | 30-90 min | 5-15 min | 49-193 min |
| **Cost multiplier vs feature** | 4-8× | 0.5-1× | 7-25× (lowered vs previous 8-28× due to engine rebalance) |
| **Engine distribution** | Claude + Codex (apex spec) | judge built-in multi | tri-engine: ~50-55% Codex / ~25-30% agy / ~20% Claude · dual-engine fallback: ~65-70% Codex / ~30-35% Claude |
| **agy required** | No (optional) | No (optional — judge falls back to dual-engine) | No (optional — dual-engine fallback) |
| **User confirmation** | Yes (mandatory) | No | Yes (mandatory) |
| **Best for** | New features needing full lifecycle | PR review, pre-commit checks | Strategic decisions, high-stakes releases, design-critical launches |

### Decision tree

```
Is the task a new feature needing discovery → ship?
  └─ YES → apex
  └─ NO ↓

Is the task a behavior-preserving cross-language rewrite (TS→Rust, Go→Rust, …)?
  └─ YES → transmute (reference/transmute-recipe.md)
  └─ NO ↓

Is the task purely code review?
  └─ YES → judge
  └─ NO ↓

Does the task require strategic / release-critical quality maximization?
  └─ NO  → feature / bug / refactor / etc. (simpler recipes)
  └─ YES ↓

Is Codex available?
  └─ NO  → apex (Codex is required for summit) or simpler chain
  └─ YES ↓ (agy is optional — present whether the run is tri-engine or dual-engine)

Has user acknowledged 7-25× cost vs feature?
  └─ NO  → present cost envelope (+ tri/dual-engine mode), get confirmation
  └─ YES → summit
```
