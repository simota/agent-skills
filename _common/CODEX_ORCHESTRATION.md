# Codex Orchestration Authoring Protocol

> Counterpart to `_common/OPUS_48_AUTHORING.md`. That file governs authoring when **Claude Code** drives the Nexus hub; this file governs authoring when **Codex CLI** drives the hub.
> Owner: Architect (canonical doc); referenced by orchestrators (Nexus, Orbit, Rally, Arena, Magi) and any SKILL.md whose spawn path can run on Codex CLI.
> Scope: Codex CLI as the **orchestrator engine** (the CLI running the top-level hub session). Codex as a *worker / spawn target* of a Claude hub is covered by `_common/SUBAGENT.md` (MULTI_ENGINE) and `_common/MULTI_ENGINE_RECIPE.md`.

Engine-selection rule for orchestrators:

| Orchestrator engine (hub) | Authoring protocol |
|---------------------------|--------------------|
| Claude Code | `_common/OPUS_48_AUTHORING.md` (P1–P11) |
| **Codex CLI** | **this file (C1–C8)** |
| Antigravity (`agy`) | best-effort; no dedicated protocol yet — apply C-principles by analogy, treat `/agent` constraints per `_common/CLI_COMPATIBILITY.md §3, §9` |

---

## Why This Exists

The Nexus stack historically assumed Claude Code is the hub: the canonical spawn template is `Agent(...)`, model selection is `sonnet/opus/haiku`, parallelism is `run_in_background`, and the authoring protocol is Opus-4.8-specific (effort levels, P4 parallel triggers). None of those map cleanly to a Codex CLI hub, which spawns via `spawn_agent`/`wait_agent`, selects `gpt-5.1` / `gpt-5.1-codex-max`, has **no background-spawn primitive**, and gates fan-out via `agents.max_depth` rather than a soft "max 3" convention.

When Codex drives the hub, apply the eight principles below instead of the Opus principles. They are grounded only in verified repository facts (`_common/CLI_COMPATIBILITY.md`, `nexus/SKILL.md` Execution Layers); items with no confirmed source are marked **未確認** and must not be speculatively completed.

---

## The Eight Principles

### C1. Spawn-Depth Budget

Codex gates nested spawning with `agents.max_depth` (default `1`). A hub that itself was spawned (e.g. Nexus launched from a slash command) may already sit at depth 1 and be unable to recurse.

**Apply by:**
- Before the first `spawn_agent` of a chain, verify both prereqs hold: `codex features list | grep multi_agent` → `true` (default since v0.115+), and `~/.codex/config.toml` has `[agents] max_depth >= 2`.
- If `max_depth` is insufficient, fall back to internal execution and log the reason concretely (`Execution: internal (reason: agents.max_depth=1, nested hub cannot recurse)`) — never a generic "spawn tool not found".
- Treat depth as the real fan-out governor; the `_common/SUBAGENT.md` "max 3 parallel" convention is a Claude soft-cap, not the Codex limit.

### C2. Synchronous Fan-Out / Join

Codex has **no background-spawn primitive**. Parallelism = issue N `spawn_agent` calls in one turn, then `wait_agent` on **all** of them. This is a hard barrier, unlike Claude's non-blocking `run_in_background`.

**Apply by:**
- For 2-3 independent branches: emit all `spawn_agent` calls together, then join with `wait_agent` per id before aggregating.
- Do not design recipes that assume a branch can keep running while the hub does other work — Codex joins at `wait_agent`.
- Hub-spoke ownership still holds: no shared mutable state between concurrent branches; aggregate only after the join.

### C3. Reasoning-Effort Routing

Apply Plan-and-Execute across Codex models: a high-reasoning model plans, a cheaper default model executes (Core Contract cost principle).

**Apply by:**
- Planning / high-complexity design steps → `gpt-5.1-codex-max` (reasoning).
- Standard implementation / execution steps → `gpt-5.1` (default).
- The exact Codex reasoning-effort config key name and its level names are **未確認** in current docs — express effort as model choice (codex-max vs default), not as an invented effort enum.

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

Codex runs sandbox-on by default. An autonomous hub must set an approval policy consistent with the active Nexus mode.

**Apply by:**
- AUTORUN / AUTORUN_FULL → `codex exec --full-auto` (or equivalent config) so subagents proceed without per-action prompts.
- Never use `--dangerously-bypass-approvals-and-sandbox` in production or untrusted workspaces; restrict to sandboxed/CI/authorized-dev contexts.
- Guided / Interactive modes keep the default per-action approval; do not silently widen it.

### C8. AGENTS.md Authority

Codex reads `AGENTS.md` (`~/.codex/AGENTS.md` global, `<repo>/AGENTS.md` project) — **not** `CLAUDE.md`. Output language, commit conventions, and naming rules come from there.

**Apply by:**
- Resolve output-language and convention directives from `AGENTS.md`, not from a `CLAUDE.md` assumption.
- When authoring cross-CLI skills, keep shared rules in `AGENTS.md` (per `_common/CLI_COMPATIBILITY.md §7`) so a Codex hub inherits them.

---

## Per-Role Apply Matrix

| Role | Critical (◎) | Recommended (○) |
|------|---|---|
| Orchestrators (Nexus, Orbit, Rally, Arena, Magi, Titan, Sherpa) | C1, C2, C6 | C3, C7 |
| Builders / executors (Builder, Artisan, Forge, Native) spawned by a Codex hub | C4, C5 | C3 |
| Investigators / reviewers spawned by a Codex hub | C4 | C6 |
| Knowledge/Meta (Lore, Compass, Architect) authoring for Codex hubs | C3, C8 | C1 |

(◎ = address explicitly in SKILL.md; ○ = address if relevant)

C8 (AGENTS.md authority) applies to **every** role authored for a Codex hub.

---

## Validation Hooks

When validating a skill's Codex-orchestrator path, use the eight checks below (Architect validation):

- R-C1 Spawn-depth prereqs verified before fan-out; concrete internal fall-back reason
- R-C2 Parallel branches use N `spawn_agent` → `wait_agent` join (no assumed background execution)
- R-C3 Effort expressed as model choice (codex-max plan / default execute); no invented effort enum
- R-C4 Loose-prompt spawn (Role/Target/Output); no methodology padding
- R-C5 Lazy-visibility handling (attempt call when prereqs hold)
- R-C6 Checkpoint-resume via `send_input`/`resume_agent`/`close_agent` for 4+ step chains
- R-C7 Approval posture matches the active Nexus mode; no prod bypass flags
- R-C8 Rules resolved from `AGENTS.md`, not `CLAUDE.md`

Pass criterion: address all `◎` principles for the role; aim for ≥ 6/8 total.

---

## How to Reference This File

In a SKILL.md:

```markdown
- Author for the active orchestrator engine. Claude Code hub → `_common/OPUS_48_AUTHORING.md`;
  Codex CLI hub → `_common/CODEX_ORCHESTRATION.md` (apply C[X], C[Y] for this role).
```

Cite by ID (C1–C8); let this file be the single source of truth. Do not duplicate principle text into individual SKILL.md files.
