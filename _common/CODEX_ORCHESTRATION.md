# Codex Orchestration Authoring Protocol

> Counterpart to `_common/OPUS_48_AUTHORING.md`. That file governs authoring when **Claude Code** drives the Nexus hub; this file governs authoring when **Codex CLI** drives the hub.
> Owner: Architect (canonical doc); referenced by orchestrators (Nexus, Orbit, Rally, Magi) and any SKILL.md whose spawn path can run on Codex CLI.
> Scope: Codex CLI as the **orchestrator engine** (the CLI running the top-level hub session). Codex as a *worker / spawn target* of a Claude hub is covered by `_common/SUBAGENT.md` (MULTI_ENGINE) and `_common/MULTI_ENGINE_RECIPE.md`.

Engine-selection rule for orchestrators:

| Orchestrator engine (hub) | Authoring protocol |
|---------------------------|--------------------|
| Claude Code | `_common/OPUS_48_AUTHORING.md` (P1–P11) |
| **Codex CLI** | **this file (C1–C9)** |
| Antigravity (`agy`) | `_common/AGY_ORCHESTRATION.md` (A1–A9) |

---

## Why This Exists

The Nexus stack historically assumed Claude Code is the hub: the canonical spawn template is `Agent(...)`, model selection is `sonnet/opus/haiku`, parallelism is `run_in_background`, and the authoring protocol is Opus-4.8-specific (effort levels, P4 parallel triggers). None of those map cleanly to a Codex CLI hub, which spawns via `spawn_agent`/`wait_agent`, runs the latest gpt-5.6 generation throughout with role-based variants (sol/terra/luna, see C3.0), has **no background-spawn primitive**, and gates fan-out via `agents.max_depth` rather than a soft "max 3" convention.

When Codex drives the hub, apply the nine principles below instead of the Opus principles. They are grounded in verified repository facts (`_common/CLI_COMPATIBILITY.md`, `nexus/SKILL.md` Execution Layers) and, for the config/prompting levers (C3, C7, C9), in the official Codex docs at `developers.openai.com/codex/*` and the OpenAI Codex prompting guide (verified 2026-06); items with no confirmed source are marked **未確認** and must not be speculatively completed.

---

## The Nine Principles

### C1. Spawn-Depth Budget

Codex gates nested spawning with `agents.max_depth` (default `1` — root is depth 0, so the default allows one child layer and blocks deeper nesting) and caps concurrently-open agents with `agents.max_threads` (default `6`). A hub that itself was spawned (e.g. Nexus launched from a slash command) may already sit at depth 1 and be unable to recurse. Fan-out plans wider than 6 branches queue against `max_threads` — size parallel phases accordingly or raise the key. [Verified 2026-06 against developers.openai.com/codex/config-reference; CLI 0.137.0 "Multi-agent v2" adds per-thread runtime choice but changes neither default.]

**Apply by:**
- Before the first `spawn_agent` of a chain, verify both prereqs hold: `codex features list | grep multi_agent` → `true` (default since v0.115+), and `~/.codex/config.toml` has `[agents] max_depth >= 2`.
- If `max_depth` is insufficient, fall back to internal execution and log the reason concretely (`Execution: internal (reason: agents.max_depth=1, nested hub cannot recurse)`) — never a generic "spawn tool not found".
- Treat depth as the real fan-out governor; the `_common/SUBAGENT.md` "max 3 parallel" convention is a Claude soft-cap, not the Codex limit.
- Tune the fan-out envelope with `[agents] max_threads` (concurrent workers, default `6`), `max_depth` (nesting), and `job_max_runtime_seconds`. For large homogeneous sweeps prefer the built-in **`spawn_agents_on_csv`** batch tool (`csv_path` + `{column}`-templated `instruction` + `output_schema` + `max_concurrency`; each worker reports once via `report_agent_job_result`) over hand-rolled per-item spawns. Built-in roles: `default`, `worker` (execution), `explorer` (read-heavy). [Verified 2026-06 — developers.openai.com/codex/subagents, /config-advanced.]
- **Version caveat:** the subagents docs now state subagents are enabled by default (no flag), while older `config-advanced`/KB sources describe `[features] multi_agent` as an off-by-default experimental flag. This changed recently — confirm on the installed build via `/experimental` rather than assuming either state.

### C2. Synchronous Fan-Out / Join

Codex has **no background-spawn primitive**. Parallelism = issue N `spawn_agent` calls in one turn, then `wait_agent` on **all** of them. This is a hard barrier, unlike Claude's non-blocking `run_in_background`.

**Apply by:**
- For 2-3 independent branches: emit all `spawn_agent` calls together, then join with `wait_agent` per id before aggregating.
- Do not design recipes that assume a branch can keep running while the hub does other work — Codex joins at `wait_agent`.
- Hub-spoke ownership still holds: no shared mutable state between concurrent branches; aggregate only after the join.

### C3. Reasoning-Effort Routing

> **C3.0 — Latest-generation mandate + variant tiering for Codex (user policy, 2026-07-10).** Codex always runs on the **latest model generation — currently the `gpt-5.6` family** for **every step and every spawned subagent** (orbit build loops, `spawn_agent` fan-out, charter §5 roster, recipe plan/execute steps); never fall back to a previous generation (`gpt-5.5` and older) on cost grounds. **Within the generation, select the variant by role** (aligned with the official guidance at learn.chatgpt.com/docs/models):
> - **`gpt-5.6-sol`** (flagship) — hub/orchestrator, planning, design, and high-stakes work: ambiguous, high-value tasks where failure is costly (complex code changes, deep research, security review, architecture). **The hub itself is always sol.**
> - **`gpt-5.6-terra`** (balanced) — standard implementation: feature builds, bug fixes, test authoring, build loops. Official "pragmatic all-rounder" and the natural upgrade path from gpt-5.5 (comparable capability, ~half the price).
> - **`gpt-5.6-luna`** (fast) — spawned subagents doing well-shaped high-volume work: extraction, classification, transformation, formatting, structured summaries, docs.
>
> "Latest generation" is the contract — when a newer family supersedes gpt-5.6, update this block and everything follows. When a step doesn't fit a tier cleanly, prefer the higher variant.

Plan-and-Execute's cost principle (Core Contract) is realized for Codex through **variant tiering (sol plan / terra execute / luna rote) plus `model_reasoning_effort`** — the generation stays gpt-5.6 throughout.

**Apply by (verified 2026-07 against learn.chatgpt.com/docs/models; gpt-5.6 released 2026-07-09):**
- Planning / design / hub → `gpt-5.6-sol`; standard implementation → `gpt-5.6-terra`; rote/high-volume subagents → `gpt-5.6-luna` (C3.0). Within a variant, differentiate by `model_reasoning_effort`.
- Reasoning effort is tunable via the **`model_reasoning_effort`** config key (`config.toml` or `-c model_reasoning_effort="..."`), values `minimal | low | medium | high | xhigh` (default `medium`; `xhigh` model-dependent; a `max` level for sol is third-party-reported, 未確認). [Verified — config-reference.]
- **Official effort principle:** start with the lowest effort that yields acceptable results, then escalate; there is **no exact effort mapping from gpt-5.5 to gpt-5.6** (official migration note) — re-calibrate per task rather than copying old settings.
- **Verification caveat:** sol at maximum effort is reported (third-party benchmark) to hallucinate more than gpt-5.5 — keep independent verification steps thick for precision-critical output.

### C4. Loose-Prompt Spawning

Codex subagents perform best with minimal, unbiased framing — **Role / Target / Output** only (`_common/SUBAGENT.md` MULTI_ENGINE loose-prompt rule). Over-specifying with checklists, category lists, or methodology descriptions suppresses Codex's independent perspective.

**Apply by:**
- Pass the CLI-agnostic spawn template body (Role, Task, Context delta, Constraints, Acceptance criteria, Output envelope) but resist padding it with domain frameworks the specialist's own SKILL.md already supplies.
- The specialist reads its own `SKILL.md` (`~/.codex/skills/` or `<repo>/.agents/skills/`); do not duplicate that content into the spawn prompt.

### C5. Lazy Tool Visibility

Codex does not always list `spawn_agent` in the model's visible tool inventory. "Not visible" ≠ "not callable".

**Apply by:**
- If both C1 prereqs hold but `spawn_agent` appears absent, attempt the call anyway rather than falling back to internal.
- Only log an internal fall-back after an actual call failure, with the concrete error.

### C6. Checkpoint-Resume via Session Tools

For chains with 4+ steps (the SKILL checkpoint-resume threshold), continue an existing subagent instead of re-spawning.

**Apply by:**
- Use `send_input` to feed the next step's delta into a live subagent, and `resume_agent` to revive a checkpointed one, rather than spawning a fresh session each step.
- Call `close_agent` to release a finished subagent's context and keep the depth/budget envelope clear.
- Omitted spawn fields inherit from the parent session — pass only the state delta, not the full context.

### C7. Sandbox / Approval Posture

Codex runs sandbox-on by default. An autonomous hub must set an approval policy consistent with the active Nexus mode. Excessive per-action approval prompting is the **single biggest cause of lost autonomy** ("interrupts you forty times") — set the posture deliberately, do not leave the cautious default in an AUTORUN run. [Verified 2026-06 — developers.openai.com/codex/config-reference, /agent-approvals-security.]

**Apply by:**
- AUTORUN / AUTORUN_FULL → `approval_policy = "never"` + `sandbox_mode = "workspace-write"` in `config.toml` (or `-c` overrides) so subagents proceed without per-action prompts while writes stay confined to the workspace. (`--full-auto` is the legacy shortcut for this pairing and is now flagged **deprecated** in the CLI reference — prefer the explicit keys; the canonical key is `approval_policy` / `--ask-for-approval`, not the older `approval_mode` alias.)
- To keep a safety gate without pausing for the human, route eligible approvals through the automated reviewer: `approvals_reviewer = "auto_review"` (vs `"user"`), or `approval_policy = { granular = { … } }` to auto-reject only high-risk categories.
- Network is **off by default** under `workspace-write`; if the task needs installs/fetches, pre-grant `[sandbox_workspace_write] network_access = true` so it does not stall at the network boundary mid-run.
- Never use `--dangerously-bypass-approvals-and-sandbox` (alias **`--yolo`**) in production or untrusted workspaces; restrict to sandboxed/CI/authorized-dev contexts.
- Guided / Interactive modes keep the default per-action approval; do not silently widen it.
- Known bug (track, don't rely on the per-session toggle): approval prompts can repeat even under auto-approve/`never`, notably in the VS Code extension (GitHub openai/codex #10187, #5038). The reliable mitigation is the config-level `never` + sandbox posture above.

### C8. AGENTS.md Authority

Codex reads `AGENTS.md` (`~/.codex/AGENTS.md` global, `<repo>/AGENTS.md` project) — **not** `CLAUDE.md`. Output language, commit conventions, and naming rules come from there.

**Apply by:**
- Resolve output-language and convention directives from `AGENTS.md`, not from a `CLAUDE.md` assumption.
- When authoring cross-CLI skills, keep shared rules in `AGENTS.md` (per `_common/CLI_COMPATIBILITY.md §7`) so a Codex hub inherits them.

### C9. Autonomy / Self-Driving Maximization

The most common Codex underperformance is **premature stopping** — it analyzes instead of finishing, asks clarifying questions instead of acting, or hands back at the first uncertainty. Config (C3 effort, C7 approval) removes the *mechanical* interrupts; this principle removes the *behavioral* ones via the spawn prompt and `AGENTS.md`. These are the highest-leverage autonomy levers and several are **Codex-specific (opposite of general GPT-5 advice)**. [Verified 2026-06 — OpenAI Codex prompting guide + GPT-5 prompting guide (developers.openai.com/cookbook), /codex/learn/best-practices.]

**Apply by:**
- **Persistence directive** — include in the spawn prompt / `AGENTS.md`: *"Keep going until the query is completely resolved before yielding back. Never stop or hand back when you encounter uncertainty — research or deduce the most reasonable approach and continue."* Directly counters early termination.
- **Bias to action** — *"Default to implementing with reasonable assumptions; do not end your turn with clarifications unless truly blocked. Decide the most reasonable assumption, proceed, and document it after acting."* Counters "asks instead of doing".
- **⚠️ Remove preamble/plan/status-update prompting (Codex-specific).** On Codex models, prompting for an upfront plan, preambles, or running status updates *causes the model to stop abruptly* — the inverse of general GPT-5 guidance. If you ported a Claude/GPT-5 system prompt, strip these. This is the most-missed lever; it composes with C4 (loose-prompt spawning).
- **Completion oracle ("Done when")** — give an explicit stop condition + self-validation loop (write/run tests, lint, types, confirm behavior matches request). Without it Codex "fixes one test and stops". Pairs with the recipe's own VERIFY gate.
- **Raise effort for long-horizon work** — combine with C3: `model_reasoning_effort = "high"` (or `"xhigh"`) sustains multi-step autonomous runs; OpenAI's own guidance is to raise reasoning effort to increase tool-calling persistence and reduce clarifying questions.
- Keep `AGENTS.md` short and command-exact (C8): paste runnable build/test/lint commands and concrete prohibitions so the agent self-validates rather than pausing to ask how.

---

## Per-Role Apply Matrix

| Role | Critical (◎) | Recommended (○) |
|------|---|---|
| Orchestrators (Nexus, Orbit, Rally, Magi, Titan, Sherpa) | C1, C2, C6, C9 | C3, C7 |
| Builders / executors (Builder, Artisan, Forge, Native) spawned by a Codex hub | C4, C5, C9 | C3, C7 |
| Investigators / reviewers spawned by a Codex hub | C4 | C6, C9 |
| Knowledge/Meta (Lore, Compass, Architect) authoring for Codex hubs | C3, C8 | C1, C9 |

(◎ = address explicitly in SKILL.md; ○ = address if relevant)

C8 (AGENTS.md authority) applies to **every** role authored for a Codex hub.

---

## Validation Hooks

When validating a skill's Codex-orchestrator path, use the nine checks below (Architect validation):

- R-C1 Spawn-depth prereqs verified before fan-out; concrete internal fall-back reason
- R-C2 Parallel branches use N `spawn_agent` → `wait_agent` join (no assumed background execution)
- R-C3 All Codex steps and spawned subagents run on the latest gpt-5.6 generation with the role-matched variant (hub/plan/design=sol, standard implementation=terra, rote subagents=luna, C3.0); no fallback to a previous generation; depth tuned via `model_reasoning_effort` (`minimal|low|medium|high|xhigh`), no invented level names beyond these.
- R-C4 Loose-prompt spawn (Role/Target/Output); no methodology padding
- R-C5 Lazy-visibility handling (attempt call when prereqs hold)
- R-C6 Checkpoint-resume via `send_input`/`resume_agent`/`close_agent` for 4+ step chains
- R-C7 Approval posture matches the active Nexus mode (AUTORUN → `approval_policy="never"`+`workspace-write`, `network_access` pre-granted if needed); no prod bypass flags
- R-C8 Rules resolved from `AGENTS.md`, not `CLAUDE.md`
- R-C9 Autonomy directives present for self-driving runs: persistence + bias-to-action + **no preamble/plan/status prompting (Codex-specific)** + completion oracle; effort raised for long-horizon work

Pass criterion: address all `◎` principles for the role; aim for ≥ 7/9 total.

---

## How to Reference This File

In a SKILL.md:

```markdown
- Author for the active orchestrator engine. Claude Code hub → `_common/OPUS_48_AUTHORING.md`;
  Codex CLI hub → `_common/CODEX_ORCHESTRATION.md` (apply C[X], C[Y] for this role).
```

Cite by ID (C1–C9); let this file be the single source of truth. Do not duplicate principle text into individual SKILL.md files.
