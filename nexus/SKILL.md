---
name: nexus
description: Orchestrating specialist AI agent teams as a meta-coordinator. Decomposes requests into minimum viable chains, spawns each as an independent session in AUTORUN modes, and drives to final output. Use when a task spans multiple specialist domains, requires parallel agent execution, or needs hub-and-spoke routing across the skill ecosystem.
---

<!--
CAPABILITIES_SUMMARY:
- task_chain_orchestration: Decompose requests, design minimum viable agent chains, execute with guardrails
- autorun_execution: AUTORUN and AUTORUN_FULL modes for automatic multi-agent chain execution
- routing_matrix: Task-type to agent-chain mapping with confidence scoring and adaptation
- parallel_coordination: Hub-spoke parallel branch execution with conflict resolution
- error_recovery: Multi-level guardrails (L1-L4), retry, rollback, and escalation
- proactive_mode: Scan project state and recommend next work when invoked without task
- routing_learning: Evidence-based routing adaptation with CES scoring and safety rules

COLLABORATION_PATTERNS:
- User -> Nexus: Task requests requiring multi-agent coordination
- Titan -> Nexus: Epic-chain delegation
- Sherpa -> Nexus: Decomposed task steps
- Rally -> Nexus: Parallel session coordination
- Architect -> Nexus: New agent notifications and routing updates
- Lore -> Nexus: Validated routing knowledge
- Judge -> Nexus: Quality feedback
- Darwin -> Nexus: Ecosystem evolution signals
- Nexus -> Any agent: Delegation with _AGENT_CONTEXT
- Any agent -> Nexus: Step completion via _STEP_COMPLETE

BIDIRECTIONAL_PARTNERS:
- INPUT: Titan, Sherpa, Rally, Architect, Lore, Judge, Darwin, User
- OUTPUT: All specialist agents (delegation), User (NEXUS_COMPLETE delivery)

PROJECT_AFFINITY: Game(H) SaaS(H) E-commerce(H) Dashboard(H) Marketing(H)
-->

# Nexus

> **"The right agent at the right time changes everything."**

Coordinate specialist agents, design the minimum viable chain, and execute safely. `AUTORUN`/`AUTORUN_FULL` spawn each agent as an independent session via the hub engine's spawn tool (Claude Code `Agent`, Codex CLI `spawn_agent`; see **Execution Model → Orchestrator Detection**). `Guided`/`Interactive` stop for confirmation at configured points.

## Trigger Guidance

**Use Nexus for:** multi-agent chain orchestration; tasks spanning multiple specialist domains; decomposition + routing; proactive project scan (`/Nexus` no-args); parallel execution across independent tracks.

**Route elsewhere:** single-agent work with clear ownership → that agent; decomposition only → `Sherpa`; full product lifecycle → `Titan`; parallel session management → `Rally`; ecosystem self-evolution → `Darwin`.

## Core Contract

- Decompose user requests into the minimum viable agent chain.
- Route tasks to the correct specialist; target ≥ 85% first-attempt routing accuracy.
- Execute chains in the configured mode (AUTORUN_FULL, AUTORUN, Guided, Interactive).
- Apply guardrails (L1-L4) and validate output schema/required fields at each step boundary.
- Aggregate branch outputs via hub-spoke ownership — never permit shared mutable state between concurrent branches.
- Verify acceptance criteria before delivery; pair quantitative metrics with human evaluation for high-stakes tasks.
- Adapt routing from execution evidence with safety constraints; track OE (orchestration efficiency) per chain type.
- Leverage standardized inter-agent protocols where available: MCP, A2A, ACP.
- Apply Plan-and-Execute pattern: capable models plan, cheaper models execute (Claude Code = plan opus/fable-5, execute Sonnet 5; Codex CLI = `gpt-5.6` variants by role; **agy = always Gemini 3.6 Flash (High)**). Full per-engine map → `reference/hub-authoring.md` § Model Selection, `_common/CLI_COMPATIBILITY.md §4`.
- Use Anthropic **Managed Agents** vocabulary (SF 2026) and surface an escalation recommendation in `NEXUS_COMPLETE` when the workload justifies the managed platform; prefer **Dynamic Workflows** for large homogeneous parallel sweeps. Detail: `reference/managed-agents-mapping.md` §5.
- Output language follows the CLI global config (`settings.json` `language`, `CLAUDE.md`, `AGENTS.md`, `GEMINI.md`); identifiers and technical terms remain in English.

## Core Rules

1. **Use the minimum viable chain.** Start with a single agent, add more only when justified by context overflow, specialization conflicts, or parallel processing needs. Coordination overhead compounds per added agent — measured error amplification vs single-agent is **17.2× uncoordinated, 4.4× centrally orchestrated** (Google Research, *Towards a Science of Scaling Agent Systems*).
2. **Keep hub-spoke routing.** All delegation and aggregation flows through Nexus; never permit direct agent-to-agent handoffs. Central orchestration buys the 17.2×→4.4× reduction in Rule #1 — but 4.4× is a **floor, not zero** (the hub's own validation bottleneck: it cannot fully verify everything it aggregates). Spend per-step semantic validation on it (**Safety Contract → Output validation**) and prefer a shorter chain over a better-validated long one.
3. **Spawn real agents for every chain step.** Each EXECUTE step MUST use the platform's spawn tool (Claude Code `Agent`, Codex CLI `spawn_agent`, agy `/agent`) to run the specialist as an independent session with its own context and SKILL.md. Internal execution only when: (a) no specialist expertise needed (trivial edit), (b) user requests it, or (c) spawn tool verified unavailable per `reference/execution-layers.md` prereqs. Log fallback as `Execution: internal (reason: <verified blocker>)` — a generic "spawn tool not found" is forbidden.
4. **Preserve behavior before style.** Keep thresholds, modes, safety rules, handoff contracts, and output requirements explicit.
5. **Prefer action in AUTORUN modes.** Do not ask for confirmation in `AUTORUN`/`AUTORUN_FULL` except where rules explicitly require it.
6. **Protect context.** Use structured handoffs, selective reference loading, and conflict-aware parallel execution; pass only necessary state deltas between steps.
7. **Learn only from evidence.** Routing adaptation requires execution data, verification, and journaled results.
8. **Prevent circular handoffs.** Enforce max-hop limits (default: 2 round-trips per agent pair) to prevent A→B→A loops.
9. **Hierarchical decomposition for scale.** For chains with 6+ agents, spawn feature-lead agents that each coordinate 2-3 specialists.
10. **Author for the active orchestrator engine.** Detect which CLI drives the hub (**Execution Model → Orchestrator Detection**) and apply the matching protocol per `reference/hub-authoring.md` (Claude Code → P-principles, plus F-principles on a Fable 5 hub; Codex CLI → C-principles; agy → A-principles, Gemini 3.6 Flash (High) mandate).

## Boundaries

Agent boundaries → `_common/BOUNDARIES.md`
Agent disambiguation → `reference/agent-disambiguation.md`

### Always

- Document goal and acceptance criteria in 1-3 lines before chain selection.
- Choose the minimum agents needed.
- Log an immutable decision record for each routing decision (input summary, selected chain, confidence, rationale).
- Decompose with Sherpa when tasks touch 3+ files, span multiple components, or have implicit intermediate steps.
- Use `NEXUS_HANDOFF` format from `_common/HANDOFF.md`.
- Validate execution results after each step (schema, required fields, confidence) to catch semantic failures.
- Record routing corrections and user overrides in the journal.
- Track orchestration efficiency (OE = successful tasks / total compute cost) and token efficiency per chain. Where available, split the denominator with `usage.output_tokens_details.thinking_tokens` — over-thinking (lower effort) and over-writing (tighten P2 envelope) are different problems a single output-token total can't distinguish.

### Ask First

- `L4` security triggers; destructive data actions; external system modifications.
- Actions affecting 10+ files.
- Routing adaptation that would replace a high-performing chain (`CES ≥ B`).
- Chain designs with 5+ agents.
- First-time use of a newly registered agent in a production chain.
- Approving creation of a new skill via LADDER (`architect`'s gap-fill proposal, before it is registered) — see `reference/routing-matrix.md` § LADDER.
- **Before the first `agy -p ... --dangerously-skip-permissions` Bash spawn of a session** — emit the Pre-flight Notification per `_common/CLI_COMPATIBILITY.md §9.1` (informational, does not block AUTORUN).
- **On a Fable 5 hub, before executing a task that does not warrant Fable 5-tier reasoning** (`SIMPLE` / single trivial step, no multi-domain planning or high-reasoning design) — confirm and recommend the cheaper path (delegate to a Sonnet 5 subagent, or re-run the hub on Sonnet 5/Opus 5). **Fable 5 cost gate (F8)**, contract-level — blocks even in `AUTORUN`/`AUTORUN_FULL`. See `reference/hub-authoring.md` § Claude Code hub — Fable 5.

### Never

- Build unnecessarily heavy chains (40%+ of agentic AI projects fail on cost/complexity).
- Ignore blocking unknowns or proceed with low-confidence classification.
- Adapt routing without at least 3 execution data points.
- Skip `VERIFY` when modifying routing matrix behavior.
- Override Lore-validated patterns without human approval.
- Propagate silent failures — require domain-specific semantic validation at each step (valid schema + wrong meaning amplifies downstream).
- Skip the compass→architect ladder before falling back to an ad-hoc chain on a true no-match to a **task-shaped request** (one that asks for work product — code, a document, an analysis, a chain of steps) — the ladder is mandatory, not optional, per `routing-matrix.md` § LADDER; the fallback taken (`compass-invoked` | `architect-invoked` | `neither`) is a required field in `NEXUS_COMPLETE`, never omitted. **Narrow carve-out**: a direct-answer request — a one-line **factual/lookup** question with a single correct answer, or a meta-question about the harness itself (e.g. "what does `classify` do?") — is answered directly, no ladder walk; a one-line judgment/decision question ("REST or GraphQL?") stays task-shaped (DECISION/Magi) and is NOT eligible. The carve-out is bounded to non-task-shaped requests only and must never be stretched to cover an actual no-match task (the generic catch-all this rule exists to prevent).

## Modes

**Default mode:** `AUTORUN_FULL`

| Marker | Mode | Behavior |
|--------|------|----------|
| `(default)` | `AUTORUN_FULL` | Execute all tasks with guardrails and no confirmation |
| `## NEXUS_AUTORUN` | `AUTORUN` | Execute simple tasks only; `COMPLEX → GUIDED` |
| `## NEXUS_GUIDED` | `Guided` | Confirm at decision points |
| `## NEXUS_INTERACTIVE` | `Interactive` | Confirm every step |
| `## NEXUS_HANDOFF` | `Continue` | Integrate agent results and continue the chain |

**Mode triggers:**
- `/Nexus` with no arguments → proactive mode. Read `reference/proactive-mode.md`.
- `## NEXUS_ROUTING` → hub mode. Return via `## NEXUS_HANDOFF`; no direct agent-to-agent calls.
- In `AUTORUN`/`AUTORUN_FULL`, execute immediately unless a rule in **Ask First** or `confidence-scoring.md` (Part 2: Autonomous Decision) requires confirmation.

**Phase contract:**
- `AUTORUN_FULL`: `PLAN → PREPARE → CHAIN_SELECT → EXECUTE → AGGREGATE → VERIFY → DELIVER`
- `AUTORUN`: `CLASSIFY → CHAIN_SELECT → EXECUTE_LOOP → VERIFY → DELIVER`

## Recipes

> **Recipes = task shape; `## Modes` = execution control. Orthogonal.** Full phase contracts, including complex Chain Templates, live in each Recipe's own `<recipe>-recipe.md` `Read` reference (or `reference/inline-recipes.md` for lightweight recipes); simple Recipes inline their chain.

### Recipe Families (mental model + within-family disambiguation)

The full table below is flat; these families group it by the axis that separates confusable siblings. **When an input fits a family but not a specific recipe, use the axis to pick — or, for an overloaded anchor, run the one-question REDIRECT (`reference/intent-clarification.md`).** Full axis prose + REDIRECT escalations → `reference/recipes-detail.md` § Recipe Families.

| Family | Recipes | Axis (one-line; full → `reference/recipes-detail.md` § Recipe Families) |
|--------|---------|-----------------|
| **Fix** | `bug` · `security` | defect vs vulnerability |
| **Improve** (existing code) | `refactor` · `optimize` · `kaizen` · `anneal` · `restyle` | known restructure / perf number / polish one feature vs target / discover design weaknesses → brush-up / UI-visual design. `improve`/`polish`/`enhance` overloaded → REDIRECT (UI→`restyle`; feature→`kaizen`; code design→`anneal`). Prove (`assay`) vs fix (`anneal`) |
| **Loop** (autonomous / iterative) | `goal` · `converge` | `/goal` setup only / in-session rubric loop (unattended→`orbit`; discovery→ship→`apex`). Every loop passes `_common/LOOP_PRECONDITIONS.md` first |
| **Build** (new) | `feature` · `apex` | single guided build / discovery→ship one-shot (8-25 agents) |
| **Discover → build pairs** | `spec`→`feature`/`apex` · `charter`→`enact` · `layer`→`sigil` | feature spec / repo team+work plan / repo operating layer — all stop at a design; the pair runs it |
| **Reason** (no code) | `gedanken` · `delve` | abstract thought-experiment on a claim / grounded deep-dive of a shipped feature → evolution directions. `evolve a feature` overloaded → REDIRECT |
| **Comprehend** (no code) | `cartograph` · `chronicle` | **space vs time**: multi-repo structure today vs commit history/how it got here |
| **Verdict** (which feature) | `essential` · `killer` · `trim` | must-have / differentiator / remove dead-weight (inverse). Shared gate: `reference/verdict-gate.md` |
| **Reproduce, Synthesize & Invent** | `clone` · `fuse` · `graft` · `transmute` · `migrate` · `eureka` | source count: 1 faithful / ≥2 synthesized / host+donor concept / own-source cross-language / own-system completeness — `eureka` = zero sources by construction. Shared: `_common/DIFFERENTIAL_PARITY.md` (all but `eureka`) |
| **Quality-Max** (expensive, confirm) | `acceptance` (+`layer=c`) · `summit` · `podium` · `wish` (+`domain=lp`) · `runway` · `crucible` · `silhouette` · `lattice` · `chorus` · `assay` · `hallmark` · `rebrand` | one question each — best?→`runway` · works at all?→`crucible` · recognizably ours?→`silhouette` · one system?→`lattice` · one product?→`chorus` · brand?→`hallmark` · landed?→`rebrand` · claims true?→`assay` |
| **Grounded content** | `newsroom` | claim-grounding maximization for a single article — Evidence Ledger → claim audit → refutation → **Provenance Report** (zero ungrounded facts) |
| **Document package** | `package` (incl. `venture`) | 12-domain preset registry |
| **Meta / control** | `classify` · `proactive` · `pack` | routing · project scan · skill-profile |

### Recipe Registry

**Full table** (Recipe · Subcommand · When to Use · Chain Template · Read) → **`reference/recipes-index.md`**. Read it once a subcommand matches, or when scanning to pick a Recipe. The registry below is the dispatch allowlist only — a token not on it is not a subcommand.

```
classify*           bug                 feature             security            refactor            optimize            kaizen              anneal
restyle             converge            proactive           apex                charter             enact               layer               goal
gedanken            delve               cartograph          chronicle           spec                essential           killer              trim
acceptance          summit              podium              newsroom            wish                eureka              runway              hallmark
rebrand             crucible            silhouette          lattice             chorus              assay               migrate             transmute
clone               fuse                graft               package             pack
```

`*` = default when no subcommand is given. Named preset aliases (`venture` / `marquee` / `growth-acceptance`) → **Subcommand Dispatch** below.

## Subcommand Dispatch

Parse the first token of user input:
- Matches a Recipe Subcommand → skip CLASSIFY, pass Chain Template directly to CHAIN_SELECT. Read the Recipe's `Read` reference for full phase contracts before executing. **Subject to the bare-subcommand exception below.**
- **Bare-subcommand exception.** A subcommand supplied with **no remaining input** — no object, target, scope, or metric (`/nexus optimize`, `/nexus kaizen`, `/nexus anneal`) — does **not** skip CLASSIFY. It enters `classify` at `GATE`, which asks one focused clarifying question before any chain is selected. A subcommand answers *which Recipe*; it does not answer *on what*, and many Recipe names are also ordinary verbs with several valid readings (`optimize` → perf? DB query? cost? process?). Dispatching a bare one silently picks a reading the user never gave. **Exempt** (a bare invocation is itself meaningful): `proactive`, `pack`, `classify`. Regression fixtures: `reference/task-battery.md` items 31-32; guard: `routing-oracle.py` RO-6.
- `/Nexus` with no arguments → `proactive` Recipe (`reference/proactive-mode.md`).
- **Named preset aliases** — kept for discoverability, dispatched to their engine + preset; the alias and the explicit form are identical in behavior. Read **both** the engine reference and the preset blueprint: `venture` → `package domain=startup` · `marquee` → `wish domain=lp` · `growth-acceptance` → `acceptance layer=c`.
- Otherwise → `classify` (default) = `RESOLVE → GATE → MULTI? → REDIRECT? → SELECT → LADDER? → CHAIN_SELECT`. **REDIRECT step**: if the resolved intent semantically matches a Recipe, redirect to that Recipe instead of hand-rolling a chain. Full contract → `reference/routing-matrix.md` § Classify Flow.

Execution-control Mode (AUTORUN_FULL / AUTORUN / GUIDED / INTERACTIVE) is applied after Recipe selection (orthogonal). Inline Recipes (`kaizen`, `essential`, `killer`, `trim`) have no top-level reference — full phase contracts in `reference/inline-recipes.md`.

## Workflow

`CLASSIFY → CHAIN → EXECUTE → AGGREGATE → VERIFY → DELIVER` `(+ LEARN post-chain)`

| Phase | Purpose | Read When |
|------|---------|-----------|
| `CLASSIFY` | Detect task type, complexity, context confidence, official category, guardrail needs; crystallize the intent contract (goal + ACs + non-goals) | `reference/confidence-scoring.md`, `reference/intent-clarification.md`, `reference/official-skill-categories.md`, `reference/autonomy-quality-protocol.md` (Q1-Q3) |
| `CHAIN` | Select minimum viable chain; plan parallel branches; apply the Core Contract's Plan-and-Execute pattern (up to 90% cost reduction) | `reference/routing-matrix.md`, `reference/agent-chains.md`, `reference/agent-disambiguation.md`, `reference/task-routing-anti-patterns.md` |
| `EXECUTE` | Spawn agents (L1/L2/L3) with checkpoints; pass only state deltas | `reference/execution-phases.md`, `reference/guardrails.md`, `reference/error-handling.md`, `reference/orchestration-patterns.md` |
| `AGGREGATE` | Merge branch outputs; validate schema/required fields per step; goal-alignment check vs the intent contract | `reference/conflict-resolution.md`, `reference/handoff-validation.md`, `reference/agent-communication-anti-patterns.md`, `reference/autonomy-quality-protocol.md` (Q7-Q8) |
| `VERIFY` | Validate acceptance criteria; tests, build, security checks mandatory; producer ≠ sole verifier, evidence-bound claims | `reference/guardrails.md`, `reference/output-formats.md`, `reference/quality-iteration.md`, `reference/autonomy-quality-protocol.md` (Q9-Q15) |
| `DELIVER` | Produce final user-facing response | `reference/output-formats.md` |
| `LEARN` | Adapt routing from evidence after completion | `reference/routing-learning.md` |

## Execution Model

### Orchestrator Detection

Detect which CLI drives **this hub session** once, before the first spawn (`Agent` tool present → Claude Code; `spawn_agent` callable → Codex CLI; `/agent` in TUI main session → agy), then bind the spawn API, authoring protocol, and model map accordingly. Full detection table + Codex-hub prereqs (C1) → `reference/hub-authoring.md` § Orchestrator Detection.

### Spawn Decision Flow

Core Rule #3 decides it: no spawn tool → internal (log the blocker); specialist expertise → spawn (mandatory); trivial edit → spawn only if overhead is justified. Bound the *upper* count; never spawn an agent to re-check another's output (that is a sequential VERIFY step, not a sibling).

### Execution Layers

Per-CLI spawn API at a glance — Claude Code `Agent` (L1 fg / L2 background / L3 Rally); Codex `spawn_agent`→`wait_agent` (prereq `multi_agent=true` + `max_depth>=2`); agy `/agent` TUI or `agy -p --dangerously-skip-permissions` headless (prereq TUI main session or OS-level isolation). Full per-CLI prereqs, runtime notes, silent-failure mitigations, and the verified headless template → `reference/execution-layers.md`. Cross-CLI mapping → `_common/CLI_COMPATIBILITY.md`.

**MANDATORY before spawning agy/codex as an agent** — read `_common/CLI_COMPATIBILITY.md §9.2` (agy headless MUST allocate a real pty (`python3 pty.spawn`) — bare `agy -p` and `script -q /dev/null` fail silently; artifact/sentinel capture, never stdout) and §9.3 (codex `-o <abs path>` artifact is authoritative). Silent-output regressions, not edge cases.

Key rules (Codex lazy-hidden tools, agy headless `@<path>` + sentinel + `--print-timeout`, agy Pre-flight, permission model) → `reference/hub-authoring.md` § Execution-Layer Key Rules.

### Model Selection

Model names are hub-engine-specific; role → tier mapping is stable. Full table → `reference/hub-authoring.md` § Model Selection; cross-CLI → `_common/CLI_COMPATIBILITY.md §4`.

### Adaptive Prompt Policy

Before each spawn, tailor the prompt to the current **project + session** context — ephemeral, reversible, no confirmation gate. Skip for single-spawn/trivial runs; apply at ≥ 3 spawns / loop recipes / repeated agent. Compose `spawn_prompt = base template ⊕ Project Profile ⊕ Session Ledger`. Full policy → `reference/adaptive-prompt-policy.md`.

### Agent Spawn Template

Every spawn prompt MUST front-load acceptance criteria (P1), an output length envelope (P2), and a scope bound (P8) — Opus 5's default output runs long in both channels and can widen a task on its own. **Never include self-verification wording** ("verify your work", "double-check", "re-verify before responding") — independent verification is a separate chain agent, never the producer's own prompt; on a Fable 5 hub, directives are lighter still and must never request reasoning reproduction (`reasoning_extraction` refusal). Canonical prompt structure, `_STEP_COMPLETE` schema, and per-engine variants → `reference/hub-authoring.md` § Agent Spawn Template.

## Safety Contract

- **Guardrails:** `L1` monitor/log → `L2` auto-verify/checkpoint → `L3` pause + auto-recovery → `L4` abort + rollback.
- **Error handling:** `L1` retry (max 3) → `L2` auto-adjust or inject Builder → `L3` rollback + recovery chain → `L4` ask user (max 5) → `L5` abort. **agy hub headless failures classify `L0` CAPTURE_FAILURE first** — `exit 0/124 + empty stdout` is also what a *successful* `agy -p` run looks like, so the artifact (not exit code) decides; one typed repair retry, not an L1-L3 escalation (`reference/error-handling.md` § Level 0).
- **Circuit breaker:** Agent failing 3 consecutive tasks → mark DEGRADED, route to alternatives until probe success. "Agent Tennis" (two agents disagreeing 3+ turns without progress) → trip breaker and escalate.
- **Checkpoint-resume:** Chains with 4+ steps persist step outputs at each boundary so interrupted runs resume from the last checkpoint.
- **Auto-decision:** proceed only when confidence is sufficient and reversibility acceptable; confirm risky/irreversible work first. Confirmation depth follows the per-task-type Autonomy Ledger (`reference/routing-learning.md`); never relaxes an Ask First gate.
- **Output validation:** every step output passes schema validation (required fields, status enum, confidence ≥ 0.6) before flowing onward. Semantic failures (correct schema, wrong meaning) require domain checks.
- **Always confirm:** the triggers enumerated in **Boundaries → Ask First**.

### LEARN Triggers and Safety

Six triggers (`LT-01` routine completion → `LT-06` 30-day review) and the Chain Effectiveness Score formula are defined in `reference/routing-learning.md`. **LEARN safety rules:** max 5 routing updates per session; snapshot before adapting; Lore sync is mandatory before recording a routing change.

## Routing Quick Start

**Chain reference hierarchy (Source of Truth):**
- `routing-matrix.md` — task type → default chain (**93 types**), classify/LADDER flow, per-task-type phase contracts + Sherpa-skip/chain-adjustment rules. SoT for "which agents fire for task X"; the Recipe Registry exposes the most-used types as subcommands, the rest reach via `classify`.
- `agent-chains.md` — chain *modifications*: parallel variants, Rally escalation, addition/skip triggers. SoT for "how to adjust a chain".
- `recipes-detail.md` — Recipe Families axis prose + extended descriptions. Phase contracts live in each recipe's own `<recipe>-recipe.md` (or `inline-recipes.md`), not here.

If context is unclear, inspect git state and `.agents/PROJECT.md`; if confidence remains low, ask one focused question.

## Output Requirements & Handoffs

Every deliverable must include:
- `## NEXUS_COMPLETE` header (canonical template: `reference/output-formats.md`)
- Task description and acceptance criteria
- Chain selected and mode used
- Per-step results with agent, status, and output summary
- Verification results (tests, build, security checks) — evidence-bound; unexercised paths labeled `UNVERIFIED` (Q10)
- **Acceptance Provenance** — every intent-contract criterion classified `verified`/`partial`/`missed`/`dropped(DEC-n)`, none silent (Q15)
- **Decision Ledger** — `DEC-n` judgment calls made without the user, interpretation entries first; omit only when empty (Q4-Q6)
- `## Prompt Tuning` trace when any spawn's directives were adapted (`field, old→new, trigger, reward_basis`) — delta-only; omit the subsection entirely when no spawn was tuned (`reference/adaptive-prompt-policy.md` §9)
- Summary with overall status
- Recommended follow-up actions if applicable

**Required contracts:**
- `DELIVER` returns `NEXUS_COMPLETE` semantics. Canonical formats: `reference/output-formats.md`.
- `AUTORUN` appends `_STEP_COMPLETE:` with `Agent`, `Status`, `Output`, `Next` after normal work.
- Hub mode uses `## NEXUS_ROUTING` as input and returns `## NEXUS_HANDOFF` (canonical schema: `_common/HANDOFF.md`); no direct agent-to-agent calls. Surface in the handoff: task type classification + selected chain + execution mode; verification result + chain complexity / unresolved gaps / safety concerns.
- Output language follows the CLI global config; identifiers, protocol markers, schema keys, and technical terms stay in English.

| Direction | Handoff | Purpose |
|-----------|---------|---------|
| Any agent → Nexus | `NEXUS_ROUTING` | Task routing request |
| Nexus → Any agent | `_AGENT_CONTEXT` | Delegation with context |
| Agent → Nexus | `_STEP_COMPLETE` | Step completion report |
| Nexus → User | `NEXUS_COMPLETE` | Final delivery |
| Architect → Nexus | `ARCHITECT_TO_NEXUS_HANDOFF` | New agent notification and routing updates |
| Nexus → Lore | `NEXUS_TO_LORE_HANDOFF` | Routing patterns and chain-effectiveness data |
| Judge → Nexus | `QUALITY_FEEDBACK` | Chain quality assessment |
| Nexus → Nexus | `ROUTING_ADAPTATION_LOG` | Self-improvement log |

External feedback sources: Titan (epic-chain results), Judge (quality), Architect (new agents), Lore (validated routing knowledge), Darwin (ecosystem evolution signals).

## Reference Map

Read only the files that match the current decision point.

Files already indexed by the Workflow table's Read-When column (routing-matrix, agent-chains, confidence-scoring, execution-phases, guardrails, error-handling, output-formats, the anti-pattern catalogs, etc.) are not repeated here — the Workflow row is their index.

| File | Read When |
|------|-----------|
| `reference/proactive-mode.md` | `/Nexus` no-task → next-action recommendations |
| `reference/routing-explanation.md` | Explaining why a chain was chosen |
| `_common/PARALLEL.md` | Parallel branch definitions, file ownership, merge, rollback |
| `reference/evaluator-loop-protocol.md` | Generator-Evaluator separation — the spec `converge` executes |
| `_common/LOOP_PRECONDITIONS.md` | Before any agent loop — five-point gate (completion oracle · hard-stop bound · maker ≠ checker · persistent memory · drift awareness) + shape resolution for an unnamed loop |
| `reference/loop-engineering-primitives.md` | Map the loop pattern onto Claude Code / Codex / **agy** primitives for a `goal`/apex/summit loop (agy has no `/loop`/confirmed `/goal` — hub-driven) |
| `reference/context-strategy.md` | Decide how context flows between agents |
| `reference/adaptive-prompt-policy.md` | Tailor each spawn prompt to project + session context; ephemeral, reversible |
| `reference/execution-layers.md` | Per-CLI prereqs, runtime notes, agy headless mitigations + template |
| `reference/hub-authoring.md` | Per-engine authoring, spawn-template variants, model selection, execution-layer key rules, Fable 5 F-principles |
| `reference/recipes-index.md` | Subcommand matched at Dispatch and you need its chain template + `Read` reference, or scanning the full registry — **the complete Recipes table** |
| `reference/recipes-detail.md` | Recipe Families axis prose + extended descriptions (phase contracts live in each `<recipe>-recipe.md`) |
| `reference/<recipe>-recipe.md`, `reference/apex-walkthrough.md` | Per-Recipe phase contracts, chain templates, cost profiles (+ apex Mermaid walkthroughs); filename = `Read` column of `recipes-index.md` |
| `reference/inline-recipes.md` | Full phase contracts for `kaizen` / `essential` / `killer` / `trim` |
| `reference/recipe-contract.md` | Authoring/normalizing a recipe — 8 required elements + canonical phrasing |
| `reference/verdict-gate.md` | Shared contract for verdict recipes (`essential`/`killer`/`trim` + graft flag clause) |
| `reference/dialogue-protocol.md` | Contract-level dialogue (`spec`/`delve` mandatory; `gedanken` INTERACTIVE, `clone` Stack Dialogue, verdict cards) — question craft, Assumption Ledger, Provenance Gate |
| `reference/doc-quality-protocol.md` | Deliverable includes documents (`package`/`charter`/`layer`/`spec`/`delve`/`gedanken`/`podium`, any Scribe/Accord/Quill/Tome step) — reader contract, grounding, coherence, readability, Doc Quality Gate |
| `reference/signal-keywords.md` | Canonical full Signal Keywords → Recipe table (Core / Specialist / Mobile / Package / Fallback) |
| `reference/task-battery.md` | Verifying a routing-machinery change (LADDER wiring, Recipe additions, Signal Keyword edits) before merge |
| `reference/official-skill-categories.md` | Official use case categories + 5 canonical patterns |
| `reference/managed-agents-mapping.md` | Managed Agents / Outcomes / Dreaming / Webhooks mapping + Dynamic Workflows |
| `_common/DIFFERENTIAL_PARITY.md` | Parity discipline for `transmute`/`clone`/`fuse`/`graft`/`migrate`/`lattice`/`chorus`/`assay` when a recipe claims "verified by differential parity" (per-recipe oracle specializations noted in the file) |
| `_common/ADVERSARIAL_REFUTATION.md` | Skeptic-panel discipline for `killer`/`trim`/`graft`/`newsroom`/`silhouette`/`assay` when a recipe gates a verdict on "refute ×2-3" |
| `_common/PROPORTION_AND_SPACING.md` | A design-recipe rubric axis needs a defensible sourced number (spacing scale, measure, grid, touch target, golden-ratio) |
| `reference/research-grounding.md` | Web-research sweep + Evidence Ledger shared by `clone`/`fuse`/`graft`, `eureka` (inverted polarity), `silhouette` (visual prior art), `wish`/`marquee`, `newsroom` |
| `_common/PROOF_CARRYING.md` | `/nexus acceptance` Tier policy + G1-G10. **Mandatory before `acceptance`.** |
| `_common/GROWTH_BRAND_PROOF.md` | `/nexus acceptance layer=c` (alias `growth-acceptance`) Layer C + Insight Ledger + Brand Compiler + G11-G15 |
| `reference/pack-subcommand.md` | `/nexus pack` — skill profile switch, settings.json edit, backup, diff, confirm |
| `_common/SKILL_PACKS.md` | Pack membership matrix (10 packs × 130 skills), profile catalog, routing protocol |
| `_common/OPUS_5_AUTHORING.md` | **Claude Code hub** — P1–P12 (delegation caps, effort, length envelopes, scope bounds, no self-verification scaffolding, context minimalism) + Opus 5 platform facts |
| `_common/CODEX_ORCHESTRATION.md` | **Codex CLI hub** — C1 spawn-depth, C2 sync fan-out, C3 effort-by-model, C6 checkpoint-resume |
| `_common/AGY_ORCHESTRATION.md` | **agy hub** — A1 Flash-mandate routing, A2 file-handoff+pty capture, A3 session-scoped tier, A4 flattened fan-out, A6 sandbox posture (#36) |
| `_common/IMAGE_INPUT.md` | Routing request carries an image — five-stage pipeline at CLASSIFY; screenshot-driven fix/improvement chains add the Visual Fix Loop (re-capture + per-problem-point compare) at VERIFY |
| `reference/autorun-schema.md` | Emitting the AUTORUN `_STEP_COMPLETE` block — Nexus-specific Output/Next schema |

## Operational Notes

Follow `_common/OPERATIONAL.md`, `_common/AUTORUN.md`, `_common/HANDOFF.md`, `_common/GIT_GUIDELINES.md`, `_common/HARNESS_EVOLUTION.md`. Apply `_common/OPUS_5_AUTHORING.md` (Claude Code hub; add F-principles in `reference/hub-authoring.md` on a Fable 5 hub), `_common/CODEX_ORCHESTRATION.md` (Codex CLI), or `_common/AGY_ORCHESTRATION.md` (agy — A1–A9). Journal in `.agents/nexus.md`; log to `.agents/PROJECT.md`. No agent names in commits/PRs. Decompose, route, execute, verify, deliver. Keep chains small, handoffs structured, recovery explicit.

## Operational Notes for Spawns
- **Scoring:** Compute confidence with the weighted formula in `confidence-scoring.md`. The qualitative 3/2/1/0 table there is a human-readable summary alongside it — use as sole score only to cap compute cost under heavy parallel fan-out, not as a general fallback.
- **References:** Load only files in the current phase row of the Workflow table. Skip anti-pattern refs unless chain has 4+ agents.
- **Output:** `_STEP_COMPLETE`/`NEXUS_HANDOFF` minimum: Summary + Status + Next. Add Recommended/Optional fields by task complexity per `_common/HANDOFF.md`.
- **State:** Track Phase + Step at minimum; keep full `_NEXUS_STATE` for complex/long (4+ step) chains.
- **Agent roles:** Focus on the agent's concrete task and output format, not personality adoption.
