# Nexus Summit Recipe Reference

> **"Multiple engines, five teams, one verdict — quality maximized through orchestrated diversity."**
>
> **Default baseline (2026-05 update): Claude + Codex (dual-engine).** agy is an **optional third axis** when AVAILABLE; dual-engine mode is fully supported and NOT degraded. See `_common/MULTI_ENGINE_RECIPE.md §Base Engine Policy`.

## Contents

- [Overview](#overview)
- [Invocation and Prerequisites](#invocation-and-prerequisites)
- [When to Use Summit](#when-to-use-summit)
- [Topology](#topology)
- [Engine × Team Matrix](#engine--team-matrix)
- [Phase Contracts](#phase-contracts)
- [Sub-Orchestration via Arena](#sub-orchestration-via-rally)
- [Cross-Engine Quorum Rules](#cross-engine-quorum-rules)
- [AUTORUN Chain Template](#autorun-chain-template)
- [Failure Escalation](#failure-escalation)
- [Cost and Latency Profile](#cost-and-latency-profile)
- [Comparison with Apex and Judge](#comparison-with-apex-and-judge)

---

## Overview

Summit is a **quality-maximization recipe** that mobilizes multiple execution engines across five functional teams (Analysis / Design / Execution / Verification / Improvement). It produces engine-attributed, multi-perspective deliverables for strategic decisions and high-stakes outputs where the cost of failure dramatically exceeds the cost of triangulation.

**Default baseline: Claude + Codex (dual-engine).** agy / Antigravity CLI is added as an **optional third axis** when AVAILABLE at PREFLIGHT — it contributes long-context (1M window), multimodal, Deep Think, and Search-grounding capabilities to Phase 1 / 3 / 4 / 5 when reachable, and is gracefully skipped when not. Dual-engine mode (Claude + Codex) is the recipe's normal operating state, NOT a degraded mode. See `_common/MULTI_ENGINE_RECIPE.md §Base Engine Policy + §Engine Availability Modes`.

**Design Team conditional inclusion**: The Design team is included by default but skipped when Phase 0's `mission_charter.yaml` sets `ui_dimension: none` (pure backend / infrastructure tasks with no user-facing surface). When skipped, Design sub-tracks across all phases are bypassed and the recipe operates as a four-team workflow with proportionally reduced cost.

**Key design decisions:**
- **Claude is always the hub**; Codex and (optionally) Antigravity are accessed exclusively through `rally` (no direct CLI invocation from Nexus).
- **agy is OPTIONAL** — when AVAILABLE, the recipe runs in tri-engine mode (Claude + Codex + agy) and the Phase 1 / 3 / 4 / 5 agy branches activate. When UNAVAILABLE or RUNTIME-BROKEN, the recipe runs in dual-engine mode (Claude + Codex); the agy branches are recorded as `skipped (engine unavailable)` and their workload is absorbed by Claude or Codex per the engine-strength routing rules below.
- **Multi-engine triangulation is load-bearing** in Phase 1 (Analysis) and Phase 4 (Verification). Dual-engine triangulation (Claude judgment ‖ Codex code-analysis) satisfies this requirement; the third axis is a quality lift, not a correctness gate.
- **Improvement loop is capped at 3 iterations** with Agent Tennis circuit breaker to prevent runaway cost.
- **User confirmation is mandatory** before launch (same gate as `apex`). Summit spawns 20-50 agents per run (tri-engine) or 14-36 (dual-engine).

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
| `agy` binary | reachable via `which agy` or fallback paths (same list) | **OPTIONAL** — record verdict (AVAILABLE / UNAVAILABLE / RUNTIME-BROKEN). UNAVAILABLE switches the recipe to dual-engine mode (Claude + Codex); does NOT abort. Surface the mode choice to the user in the confirmation prompt |
| `rally` skill available | check `~/.claude/skills/rally/SKILL.md` exists | abort with "rally skill required for engine bridging" |
| `rally.max_depth >= 2` (Codex config) | inspect `~/.codex/config.toml` | warn and continue; sub-spawning may fail |
| User cost acknowledgment | mandatory confirmation prompt | abort if declined |
| Mission charter producible | Phase 0 must produce valid `mission_charter.yaml` | abort if FRAMING fails |

**Why agy is optional (2026-05 policy update):** Earlier versions of this recipe required agy as a hard prerequisite on the assumption that two-engine workflows offered insufficient diversity vs `apex` + `judge`. Field experience with agy v1.0.x (frequent silent runtime failures — quota / OAuth / executor / subagent timeouts) showed that hard dependency made Summit brittle. Dual-engine baseline (Claude judgment + Codex sandbox-execution) provides the load-bearing diversity for tri-engine quorum logic; agy contributes a third axis (1M context / multimodal / Deep Think / Search) that meaningfully lifts quality when reachable but is not a correctness gate. The recipe automatically detects engine availability and adjusts engine distribution, agent counts, and cost estimates accordingly. Users who want guaranteed three-engine coverage should ensure `agy --version` succeeds before invocation.

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

- Codex is unavailable → use single-engine chain or `apex` (Codex is required; only agy is optional)
- User has not confirmed the cost envelope
- The task does not have a clear acceptance criteria definable in Phase 0

> agy unavailability does NOT preclude Summit — the recipe runs in dual-engine mode (Claude + Codex) and surfaces the mode in the pre-launch confirmation. If you specifically need agy's third-axis lift (long-context whole-codebase reasoning, multimodal asset reading, Deep Think alternatives, Search-grounded competitive analysis) and agy is broken, defer Summit until agy is back rather than swapping recipes.

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
                                    │  │  Vision (claude) coords:     │    │
                                    │  │  ├─ Claude: Vision/Prose/Echo│    │
                                    │  │  │   (judgment + language)   │    │
                                    │  │  ├─ Codex:  Pixel/Forge/Flow/│    │
                                    │  │  │   Funnel/Vitrine         │    │
                                    │  │  └─ agy: Sketch/Muse/Frame/  │    │
                                    │  │    Palette/Ink + rally[DT]   │    │
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
                                    │  ├─ judge (tri-engine built-in)      │
                                    │  ├─ Codex: Radar/Voyager/Siege/      │
                                    │  │   Siege/Probe/Sentinel/Matrix   │
                                    │  ├─ agy: Attest/Ripple/Canon/Oath  │
                                    │  │   + rally[independent review]    │
                                    │  └─ Claude: Echo + Palette (if UI)   │
                                    └──────────────────────────────────────┘
                                                   │
                                  CONFIRMED/LIKELY findings
                                                   │
                                                   ▼
                                    ┌──────────────────────────────────────┐
                                    │  Phase 5 IMPROVEMENT LOOP (max 3×)   │
                                    │  orbit drives:                       │
                                    │  ├─ Claude: Zen + Sage (judgment)    │
                                    │  ├─ Codex: Bolt/Tuner/Sweep/Mend/    │
                                    │  │   Schema (executable improve.)    │
                                    │  ├─ agy: Hex/Atlas/Lore/Vista/       │
                                    │  │   Shift (strategic)               │
                                    │  └─ Design: Vision (claude) +        │
                                    │   Palette/Muse (agy) (if UI)         │
                                    │  magi arbitrates → Phase 3 loop      │
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

> **Executive summary for routing planning.** Per-phase contracts below (Phase 0-6) restate the engine assignments inline with phase-specific gates and inputs. When designing a Summit run, use this matrix to allocate agents to engines; when executing a specific phase, follow the phase contract for the full step sequence.

**Engine routing principle:** route each agent to the engine whose distinctive strength best fits the agent's job — Claude is reserved for judgment, orchestration, and ethics; Codex owns code generation, sandbox execution, and test running (Terminal-Bench 77.3% leader); agy owns long-context analysis (1M window), multimodal asset work, Deep Think creative alternatives, and Search grounding. Each cell below lists the agents spawned on that engine for that team.

| | Claude (hub — judgment & orchestration) | Codex (sandbox & code generation) | Antigravity / agy (long-context & multimodal) |
|---|---|---|---|
| **Analysis** | Atlas (architecture trade-offs, ADR drafting), Sherpa (epic decomposition), magi (arbitration of cross-engine findings) | Lens (sandbox-aided codebase mapping), Scout (bug RCA via test execution), Sentinel (SAST scan), Siege (concurrency analysis) | Trail (git-history archaeology, 1M ctx), Trail (legacy code archaeology), Lore (cross-codebase pattern extraction), Atlas (architecture C4 diagrams via multimodal), Field (web-grounded market/tech survey) |
| **Design** *(conditional)* | Vision (direction & arbitration), Echo (persona walkthrough), Prose (UX writing & microcopy) | Pixel (mockup-to-HTML/CSS), Forge (prototype implementation), Flow (CSS/JS animation), Funnel (LP construction), Vitrine (component catalog generation) | Sketch (Gemini-native image generation), Muse (token system synthesis via multimodal mockup analysis), Frame (Figma context extraction via multimodal), Palette (a11y + interaction-quality from screenshots), rally[agy, COMPETE, Deep Think] (creative alternative directions), Ink (SVG icon system generation) |
| **Execution** | Sentinel (security review of generated code), Cloak (privacy review), Crypt (crypto architecture), magi (escalation arbitration), accord (atomic-spec gatekeeping) | Builder (general implementation), Artisan (frontend production), Native (iOS Swift / Android Kotlin), Schema (DB migrations), Bolt (perf-aware implementation), rally[COLLABORATE, codex] (bulk task distribution across DAG) | rally[COLLABORATE, agy] (alternative-implementation generation), Scribe (long-context spec & doc generation), Tome (learning-doc generation from diff), Morph (cross-format document conversion), Tone (game audio code), Lyric (Suno songwriting), Aether (AITuber/streaming pipeline) |
| **Verification** | judge (tri-engine review with built-in fan-out), Echo (UX persona walkthrough), Palette (interaction & a11y), magi (verdict arbitration on conflicts) | Radar (unit/integration tests), Voyager (E2E web + mobile), Siege (load/chaos), Siege (concurrency stress), Probe (dynamic security), Matrix (manual QA scenarios), Sentinel (re-scan post-fix) | Attest (spec compliance via long-context comparison), Ripple (vertical + horizontal impact analysis), Canon (standards compliance: OWASP/WCAG/ISO 25010), Oath (legal/regulatory), rally[agy, review] (independent multimodal review of generated UI screenshots) |
| **Improvement** | Zen (refactor judgment & code-review-style improvements), magi (improvement-selection arbitration), Sage (knowledge synthesis) | Bolt (perf optimization), Tuner (DB query plan + index recommendations), Sweep (dead code removal), Mend (automated remediation runbook execution), Schema (migration improvements) | Hex (technical-debt scoring with multimodal character generation), Atlas (architecture improvement via 1M ctx whole-codebase reasoning), Lore (pattern extraction & metapattern surfacing), Vista (long-range strategic refactor planning), Shift (deprecated-library detection, native-API modernization, tech radar — absorbed from horizon — plus framework/lang migration codemod generation) |

**Cross-engine routing rules:**
- If a task **generates or executes code** → Codex (unless it requires deep ethical/security judgment, then Claude)
- If a task **needs to hold > 200K tokens of context** (large codebase analysis, full doc set) → agy
- If a task **processes images, mockups, screenshots, or diagrams** → agy (multimodal native)
- If a task **requires creative divergence or alternative exploration** → agy (Deep Think) or rally[agy, COMPETE]
- If a task **arbitrates between multiple perspectives or makes a Go/No-Go call** → Claude (magi or Vision)
- If a task **involves security judgment, ethics, or regulatory review** → Claude (Sentinel/Cloak/Crypt/Oath)
- Otherwise default to **Codex** (faster + cheaper for routine work), not Claude

**Why this rebalance:** Previous matrix defaulted to Claude for most teams, leaving codex/agy as light-touch supplements. The new matrix moves all code-execution-heavy work to Codex (sandbox-first wins) and all long-context / multimodal / divergent work to agy (1M context + Deep Think wins). Claude retains exclusive ownership of judgment, orchestration, and ethics — areas where its reasoning quality is irreplaceable. Net effect: ~40% of work shifts from Claude to Codex/agy, increasing per-engine specialization, reducing Hub context pressure, and improving cost efficiency for routine work.

**Engine selection rationale:**

| Task characteristic | Preferred engine | Why |
|--------------------|-----------------|-----|
| Security / design judgment | Claude | Deepest reasoning, OWASP knowledge baseline |
| Large-scale code generation / refactor | Codex | 192K context, sandbox-first, Terminal-Bench 2.0 leader |
| Long-context analysis (codebase > 200K tokens) | agy | 1M context window |
| Multimodal (images, diagrams, screenshots) | agy | Native multimodal support |
| Creative alternatives / divergent thinking | agy | Deep Think mode, different reasoning style |
| Test execution | Codex | Sandbox-first, fast iteration |
| Architecture decisions | Claude | Strongest at trade-off reasoning |

---

## Phase Contracts

### Phase 0: Framing (Claude only, 1-2 agents, 3-5 min)

**Input:** User request (goal text or "/nexus summit" with current task context)

**Agents:**
1. Nexus[classify] — task type detection, complexity scoring
2. Accord[L0-L1 spec] — staged elaboration of vision and requirements (optional, skip if user provides explicit goal)
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

**Gate:** If `cost_budget.max_agents × estimated_token_cost > L4 threshold` OR `risk_tier ∈ {strategic, release-critical}` → require explicit user confirmation before proceeding to Phase 1.

---

### Phase 1: Analysis Team (tri-engine parallel + optional Design sub-track, 6-11 agents, 8-15 min)

**Input:** `mission_charter.yaml`

**Parallel branches (L2 spawn, isolated sub-contexts; engine assignments reflect engine-strength routing):**

```yaml
parallel:
  - branch: claude_judgment
    engine: claude
    agents: [atlas, sherpa]
    mission: architecture trade-off reasoning + epic decomposition (judgment-heavy work that requires deep reasoning)
    output: claude_analysis.json

  - branch: codex_code_analysis
    engine: codex (direct spawn, not via rally wrapper)
    agents: [lens, scout, sentinel, siege]
    mission: sandbox-aided codebase mapping + bug RCA + SAST scan + concurrency analysis
        (all code-execution-heavy; Codex sandbox-first is the right fit)
    output: codex_analysis.json

  - branch: agy_long_context
    engine: agy (direct spawn, not via rally wrapper)
    agents: [trail, lore, atlas, field]
    mission: git-history archaeology + legacy code analysis + pattern extraction + C4 architecture diagrams (multimodal) + web-grounded market survey
        (all long-context or multimodal; agy 1M context + multimodal native + Search grounding wins)
    output: agy_analysis.json

  - branch: design_analysis   # conditional: skip if ui_dimension == none
    parallel_sub:
      - {engine: claude, agents: [echo], mission: persona-based UX walkthrough}
      - {engine: agy,    agents: [frame, palette], mission: Figma/screenshot extraction + interaction-quality scan via multimodal}
    output: design_analysis.json
```

**Engine attribution shift from previous design:** Lens/Scout moved from Claude to Codex (sandbox-first is the right fit for codebase exploration); Trail/Trail/Lore/Atlas/Field moved to agy (long-context + multimodal native wins). Claude retains only the deepest reasoning agents (Atlas/Sherpa) and judgment roles (magi at synthesis).

**Synthesis:** `magi[arbitrate-tri-engine]` runs Logos / Pathos / Sophia perspectives across all three engine reports.

**Output:** `analysis_consensus.md`
```yaml
consensus_findings: [...]    # 3/3 agreement
likely_findings:    [...]    # 2/3 agreement
minority_signals:   [...]    # 1/3 — kept for transparency, marked as low confidence
disputed_findings:  [...]    # active disagreement requiring user judgment
engine_attribution: {...}    # which finding came from which engine
```

**Gate:** If `disputed_findings / total_findings > 0.30` → escalate to user before Phase 2.

---

### Phase 2: Planning (Claude opus, 2-3 agents, 5-8 min)

**Input:** `analysis_consensus.md`

**Agents:**
1. Sherpa[plan_DAG] — convert findings into atomic task DAG
2. Magi[trade-off arbitration] — resolve plan-level conflicts

**Engine assignment rules (applied per-task in DAG):**
- Security-sensitive OR architecture-defining → Claude
- Bulk code generation OR test execution → Codex
- Multimodal OR alternative-exploration → agy
- If ambiguous → Claude (default safe)

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
      agents: [vision, prose, echo]
      mission: direction-setting, UX writing/microcopy, persona validation
          (judgment & language nuance — Claude irreplaceable)
    - branch: codex_implementation
      engine: codex
      agents: [pixel, forge, flow, funnel, vitrine]
      mission: mockup-to-HTML/CSS, prototype implementation, animation code, LP construction, component catalog generation
          (code-generation-heavy — Codex sandbox-first + Terminal-Bench leader)
    - branch: agy_creative_multimodal
      engine: agy
      agents: [sketch, muse, frame, palette, ink]
      mission: Gemini-native image generation, token system synthesis via multimodal mockup analysis,
          Figma context extraction, a11y + interaction-quality from screenshots, SVG icon system generation
          (multimodal-native + creative — agy unique value)
    - branch: agy_divergent
      engine: agy
      agent: rally
      paradigm: COMPETE
      mode: Solo
      mission: creative alternative directions via Deep Think exploration
  synthesis:
    agent: vision (claude)
    role: arbitrate-design-direction
    convergence: single design direction (no enumeration); rejected directions surfaced with one-line reason
  output: design_direction.yaml + design_tokens.json + prototype_links + image_assets
```

**Engine shift:** Muse/Palette/Frame moved from Claude to agy (multimodal mockup/screenshot reading is agy's home turf). Pixel/Flow/Funnel/Vitrine added on Codex (all code-generation). Sketch/Ink added on agy (image/asset generation native to Gemini). Claude retains only Vision/Prose/Echo (direction, language, persona — irreducibly judgment-heavy).

**Track B: Execution Team** (5-15 agents, 20-60 min) — Codex-heavy by default

**Coordinator:** rally[COLLABORATE]

**Default engine assignment rules** (Phase 2 planner applies these per task):

| Task characteristic | Engine | Reason |
|--------------------|--------|--------|
| Code generation, refactor, file edits | **Codex** | sandbox-first, Terminal-Bench 77.3% leader |
| Test writing, test execution | **Codex** | sandbox-first execution |
| DB migration, schema changes | **Codex** (Schema agent) | code + execution |
| Mobile native impl (iOS/Android) | **Codex** (Native agent) | code generation |
| Frontend production | **Codex** (Artisan) | code generation |
| Long-context doc/spec generation | **agy** (Scribe/Tome/Morph) | 1M context wins |
| Cross-format conversion (Markdown/Word/PDF) | **agy** (Morph) | multimodal |
| Audio/music generation code | **agy** (Tone/Lyric) | divergent-creative |
| Streaming pipeline (AITuber) | **agy** (Aether) | multimodal real-time |
| Alternative implementation exploration | **agy** (rally[COMPETE]) | Deep Think |
| **Security review** of generated code | **Claude** (Sentinel) | judgment-critical |
| **Privacy/crypto review** | **Claude** (Cloak/Crypt) | judgment-critical |
| **Spec gatekeeping** between phases | **Claude** (Accord) | judgment-critical |

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

**Parallel branches** (engine-strength routing for verification; Codex owns test/security execution, agy owns compliance/impact analysis, Claude reserved for judgment):

```yaml
parallel:
  - branch: judge_review
    agent: judge
    mode: tri-engine (built-in: codex + agy + claude reviewers in parallel via judge's own fan-out)
    output: judge_findings.json

  - branch: codex_dynamic_verification
    engine: codex
    agents: [radar, voyager, siege, probe, sentinel, matrix]
    mission: unit/integration tests (Radar) + E2E web+mobile (Voyager) + load/chaos (Siege)
        + concurrency stress (Siege) + dynamic security probing (Probe) + re-scan SAST after fixes (Sentinel)
        + manual QA scenario authoring (Matrix)
        — all execution-heavy, Codex sandbox is the right environment
    output: codex_verification.json

  - branch: agy_static_compliance
    engine: agy
    agents: [attest, ripple, canon, oath]
    mission: spec compliance via long-context comparison (Attest) + impact analysis vertical+horizontal (Ripple)
        + standards compliance OWASP/WCAG/ISO 25010 (Canon) + legal/regulatory (Oath)
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
    agents: [echo, palette]      # if ui_dimension != none
    mission: persona-based UX walkthrough (Echo) + interaction-quality and a11y check (Palette)
        — judgment work, Claude irreplaceable
    output: design_findings.json
```

**Engine shift:** Radar/Voyager/Siege/Siege/Probe/Sentinel/Matrix consolidated on Codex (all execution-heavy). Attest/Ripple/Canon/Oath consolidated on agy (all benefit from 1M context for spec+impl simultaneous reasoning). Claude reduced to Echo+Palette (only judgment-driven UX agents). judge keeps its own internal tri-engine fan-out unchanged.

**Design findings integration:** Echo's persona friction reports and Palette's interaction-quality issues join the cross-engine quorum as a fifth signal source alongside judge / codex_dynamic / agy_static / agy_review. A UX regression flagged by Echo is treated as LIKELY severity by default and feeds the Phase 5 improvement loop alongside code-side findings.

**Design findings integration:** Echo's persona friction reports and Palette's interaction-quality issues join the cross-engine quorum as a fourth signal source. A UX regression flagged by Echo is treated as LIKELY severity by default and feeds the Phase 5 improvement loop alongside code-side findings.

**Quorum rules:**

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

**Driver:** orbit (autonomous loop runner)

**Per-loop process** (engine-strength routing; Claude restricted to refactor judgment + arbitration only):

```yaml
loop_iteration:
  parallel_improvement_proposals:
    - branch: claude_judgment_only
      engine: claude
      agents: [zen, sage]
      mission: refactor judgment + knowledge synthesis
          (Claude irreplaceable for nuanced "is this improvement worth it" calls)

    - branch: codex_executable_improvements
      engine: codex
      agents: [bolt, tuner, sweep, mend, schema]
      mission: performance optimization (Bolt) + DB query plan/index recommendations (Tuner)
          + dead code removal (Sweep) + automated remediation runbook execution (Mend)
          + schema migration improvements
          — all execution-heavy improvements; Codex sandbox enables safe verification
    - branch: agy_strategic_improvements
      engine: agy
      agents: [atlas, lore, shift]
      mission: architecture improvement via whole-codebase 1M-context reasoning (Atlas)
          + cross-codebase pattern extraction + metapattern surfacing (Lore)
          + long-range strategic refactor planning (Vista)
          + deprecated-library detection & native-API modernization & tech radar (Shift `detect`/`modernize`/`radar` — absorbed from horizon)
          + framework / lang migration codemod generation (Shift `framework`/`lang`/`codemod`)
          — all benefit from agy's 1M context for codebase-wide reasoning
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

## Sub-Orchestration via Arena

Arena is the **single point of contact** for Codex and agy. Nexus never calls codex or agy directly.

### Arena delegation patterns used by Summit

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

```yaml
recipe: summit
mode: AUTORUN_FULL
required_confirmation: true   # ALWAYS — same gate as apex
prerequisites:
  - claude_available: true
  - codex_available:  true    # abort if false
  - agy_available:    true    # abort if false (no dual-engine fallback)
  - rally_skill:      true
  - cost_acknowledged: true

phase_chain:
  - phase: 0_framing
    agents: [nexus.classify, accord, sherpa]
    engine: claude
    duration_minutes: [3, 5]

  - phase: 1_analysis
    parallel:
      - {engine: claude, agents: [atlas, sherpa]}   # judgment only
      - {engine: codex,  agents: [lens, scout, sentinel, siege]}   # sandbox-aided code analysis
      - {engine: agy,    agents: [trail, lore, atlas, field]}   # long-context + multimodal + grounding
      - if: ui_dimension != none
        parallel_sub:
          - {engine: claude, agents: [echo]}
          - {engine: agy,    agents: [frame, palette]}
    synthesis: {agent: magi, engine: claude, role: arbitrate-tri-engine}
    duration_minutes: [8, 15]
    gate: disputed_findings_ratio < 0.30

  - phase: 2_planning
    agents: [sherpa, magi]
    engine: claude
    model: opus
    duration_minutes: [5, 8]

  - phase: 3_design_and_execution
    parallel_tracks:
      - track: design
        if: ui_dimension != none
        coordinator: vision (claude)
        parallel:
          - {engine: claude, agents: [vision, prose, echo]}             # judgment + language
          - {engine: codex,  agents: [pixel, forge, flow, funnel, vitrine]}   # code generation
          - {engine: agy,    agents: [sketch, muse, frame, palette, ink]}     # multimodal + creative
          - {engine: agy,    agent: rally, paradigm: COMPETE, mode: Solo}     # Deep Think alternatives
        synthesis: {agent: vision, convergence: single_direction}
      - track: execution
        coordinator: rally
        paradigm: COLLABORATE
        engine_distribution_target: {codex: 0.60, agy: 0.25, claude: 0.15}    # Claude restricted to security/judgment tasks only
        engines: [claude, codex, agy]
    convergence: frame_bridges_design_to_implementation
    duration_minutes: [25, 75]
    checkpoint: after_each_parallel_group

  - phase: 4_verification
    parallel:
      - {agent: judge, mode: tri-engine-builtin}
      - {engine: codex, agents: [radar, voyager, siege, probe, sentinel, matrix]}   # all dynamic/execution
      - {engine: agy,   agents: [attest, ripple, canon, oath]}                            # long-context compliance
      - {engine: agy,   agent: rally, paradigm: COMPETE, mode: Solo}                        # independent multimodal review
      - {engine: claude, agents: [echo, palette], if: ui_dimension != none}                 # judgment-driven UX
    quorum: cross_engine_3_of_3
    duration_minutes: [10, 25]

  - phase: 5_improvement
    driver: orbit
    max_loops: 3
    arbiter: magi
    circuit_breakers:
      - agent_tennis_3_turns
      - cost_budget_overrun
      - loops_exceeded
    per_loop_minutes: [10, 15]

  - phase: 6_delivery
    agents: [guardian, launch]
    engine: claude
    output: NEXUS_COMPLETE
    duration_minutes: [3, 5]
```

---

## Failure Escalation

| Failure | Detection Phase | Mitigation | Escalation Threshold |
|---------|----------------|-----------|--------------------|
| agy CLI unreachable | Preflight | Abort with message "use apex instead" | Immediate |
| codex CLI unreachable | Preflight | Abort with message "use apex (claude only) instead" | Immediate |
| Phase 1 disputed findings > 30% | Phase 1 synthesis | Pause, present disagreement matrix | Immediate |
| Phase 4 CONFIRMED CRITICAL after max_loops | Phase 5 exit | Deliver with explicit "unresolved CRITICAL" caveat | Always |
| Agent Tennis (same issue 3+ turns) | Phase 5 loop | Circuit breaker, deliver | Always |
| Cost budget projected overrun | Per-phase gate | Reduce remaining scope to CRITICAL findings only; if still over, escalate | After 50% budget consumed |
| Engine returns invalid schema 3× | Per-phase | Treat engine as DEGRADED for remainder of run, continue with remaining 2 engines (Phase 1/4 quorum degrades to 2/2) | After 3rd schema violation |
| Total wall time > 2× estimate | Per-phase | Pause, present time-vs-quality trade-off to user | Always |

**Hard rule:** Summit never silently degrades to dual-engine. Either it runs as designed with 3 engines, or it aborts and recommends `apex`. Mid-run engine failure (after preflight) is treated as a recipe-level failure requiring user judgment.

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

**Cost shift from previous design:** total agent count rises ~30% because more specialist agents now fan out across Codex and agy in parallel (rather than serializing through fewer Claude agents). Wall time stays similar because the extra agents run in parallel. Per-token cost on Codex and agy is typically lower than Claude opus, so total $ cost drops ~10-20% despite higher agent count.

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

**Cost note:** Agent counts roughly doubled vs the previous Claude-default design, but $ cost only rose modestly (and per-token may drop) because the additional agents run on cheaper engines. The previous "8-22×" estimate was based on Claude-heavy execution; the rebalanced design is "7-25×" because of engine mix.

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
| **Agents** | 8-25 | 3-6 | 32-119 (UI tasks 44-119, non-UI tasks 32-92) |
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

Is agy available?
  └─ NO  → apex (closest substitute) or simpler chain
  └─ YES ↓

Has user acknowledged 8-22× cost vs feature?
  └─ NO  → present cost envelope, get confirmation
  └─ YES → summit
```

---

## Visualization

Mermaid flow diagram: [`summit-recipe-flow.mmd`](summit-recipe-flow.mmd) — full five-team multi-engine topology.
