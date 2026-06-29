# Loop-Engineering Primitives — Claude Code & Codex (2026-06)

How the **loop engineering** pattern maps onto concrete orchestration primitives in each hub engine. Nexus stays the routing/recipe layer; this file is the reference for *which primitive implements which loop part* when designing a `/goal`-style or apex/summit loop. For the concept, lineage, and applicability limits see `orbit/reference/loop-engineering.md`.

> Snapshot date: 2026-06-29 (refreshed; previously 2026-06-15). Versions move within weeks — verify against primary docs (`code.claude.com/docs`, `developers.openai.com/codex`) before quoting a version number.

## The pattern → primitive map

A loop = scheduled execution + isolated workspaces + maker/checker separation + persistent memory. Both hub engines now ship all parts natively (previously hand-rolled bash).

| Loop part | Claude Code | Codex |
|-----------|-------------|-------|
| Heartbeat (recurring) | `/loop` — **three modes by input** (see § `/loop` modes; interval mode v2.1.72+, self-pace v2.1.92-101); hooks; GitHub Actions / Desktop Scheduled tasks for laptop-closed runs | Automations tab (project + prompt + cadence + local/worktree target); Triage inbox for findings |
| Stop-when-done (in-session) | `/goal` (v2.1.139+): runs until a written condition holds; **a separate fast model — default Haiku — checks completion each turn from what's surfaced in the conversation only (it runs no commands, reads no files)**, so the maker isn't the grader. Bound runaway with a `or stop after N turns` clause in the condition | `/goal` (Codex CLI **v0.128.0**; persisted goal workflows GA'd 2026-05-21, "no longer experimental"): same primitive — works across turns until a verifiable stop condition, with create/pause/resume/clear. Codex has **no native `/loop`** — for a heartbeat, wrap `codex exec` (non-interactive) in a shell/cron loop |
| Workspace isolation | `git worktree`; `--worktree`/`-w` → `.claude/worktrees/<value>/` on branch `worktree-<value>` (v2.1.50); `isolation: worktree` in subagent frontmatter (temp worktree auto-removed if subagent finishes with no changes) | Built-in worktree support; multiple threads hit one repo without collision |
| Maker/checker separation | subagents (`.claude/agents/`, markdown) + agent teams; worktrees isolate *file edits*, subagents/teams coordinate *the work* | subagents spawned in parallel (≤8), results merged into one response; built-in `default`/`worker`/`explorer`; custom agents require `name`/`description`/`developer_instructions` (model + sandbox_mode inherited from parent); on-demand spawn only |
| Persistent memory | markdown / Linear / state files on disk — "the agent forgets, the repo doesn't" | same: state file outside the conversation as the loop's spine |

> **Operational note (Claude Code Week 26, 2026-06-22–26, v2.1.185–v2.1.193):** background subagents now **surface permission prompts in the main session instead of auto-denying** — previously a background checker/critic subagent could silently stall read-only on an auto-denied permission. Relevant whenever a verification subagent runs in the background (the maker/checker row).

## Five moves → six parts → primitives (Osmani/HuaShu framing, 2026-06)

The four-part skeleton above is the minimum. The Orange Book (HuaShu IEEE reformatting, *Loop Engineering: The Anthropic Playbook*, 2026-06) refines it into **five moves** of a single turn, each realized by one of **six parts**, each binding to a concrete primitive. Use this table when deciding *which primitive a recipe step needs* and *which failure it prevents*.

| Move (one turn) | Part | Claude Code primitive | Codex primitive | Skipped → failure |
|-----------------|------|-----------------------|-----------------|-------------------|
| **Discovery** — find this turn's work | Skill | `SKILL.md` invoked by automation (not a pasted instruction wall) | `$skill-name` | Blind loop (human still picks work) |
| **Handoff** — isolate & delegate | Worktree | `--worktree`/`-w`, `isolation: worktree` | background worktree | Tangled loop (parallel agents collide) |
| **Verification** — say "no" | Sub-agent (generator ≠ judge) | `.claude/agents/` + `/goal` fresh-model check | `.codex/agents/` + automation rerun+judge | Nodding loop (self-approval, **most common**) |
| **Persistence** — write state outside the chat | Memory + Connector | state file on disk + MCP | state file + MCP connector | Amnesiac loop (no cumulative progress) |
| **Scheduling** — run round after round | Automation | `/loop`, Cloud Routines, GitHub Actions | Automations tab, cloud (planned) | Manual loop (silently stops) |

- **Discovery sets the ceiling**: surface work via a maintainable skill, not a cron-glued prompt that rots (intent debt). The other four moves done well in service of bad discovery yield nothing.
- **Verification is the floor and the hardest move**: the generator's level decides what the loop *can* produce; the evaluator's level decides what it *will not*. Tune the evaluator to assume-broken and judge by *acting* (Playwright MCP: click/screenshot/run) not reading — see `orbit/reference/loop-engineering.md` and the `goal` recipe.
- The loop **shape** is engine-agnostic; only the brand of command differs. The design question is "are all six parts present?", not "which toolchain?".

## `/loop` modes & safety bounds (Claude Code, verified 2026-06-15)

`/loop [interval] <prompt>` — the **leading token** is parsed as the interval iff it matches `^\d+[smhd]$` (e.g. `5m`, `2h`); the rest is the prompt. Input shape selects one of three modes (primary: `code.claude.com/docs/en/scheduled-tasks`):

| Input | Mode | Behavior |
|-------|------|----------|
| `interval` + prompt (`/loop 5m /babysit-prs`) | **fixed cron** | runs the prompt every interval. `5m → */5 * * * *`. Min granularity 1 min — sub-minute (`30s`) is ceil'd to `ceil(N/60)m` |
| **prompt only** (`/loop <prompt>`, no interval) | **self-paced (dynamic)** | Claude picks each next delay (1 min – 1 hr) from observed state — short while a build/PR is active, long when idle. **Self-terminates** (schedules no next wake-up) once the task is provably complete; can reach for the `Monitor` tool to skip polling entirely. *Platform exception: Bedrock/Vertex/Foundry fall back to a fixed 10-min schedule when the interval is omitted* |
| interval-only / nothing | **maintenance** | runs the built-in maintenance prompt, or `loop.md` (`.claude/loop.md` > `~/.claude/loop.md`; ignored when a prompt is given, falls back to built-in if absent) |

**Runaway bounds (load-bearing safety):**
- All `/loop` tasks are **session-scoped** — starting a new conversation stops them.
- Recurring tasks **auto-expire 7 days after creation**: fire one final time, then self-delete. (Common write-ups claiming "3 days" are **wrong** — verified-refuted; 7 days is correct.)
- Fixed-interval loops run until stopped or 7 days elapse. **Esc** cancels a *waiting* `/loop` iteration — but **not** a `CronCreate` task made by asking Claude directly.

For OS-reboot-persistent recurrence use Desktop Scheduled tasks (Hourly/Daily/Weekdays/Weekly) or Routines, not terminal `/loop` (3-way Cloud / Desktop / `/loop` taxonomy). `/goal` (next-turn, model-checked stop) vs `/loop` (time-elapsed tick, stop-op or Claude's completion call) vs **Stop hook** (your own script decides) are the three official "keep a session running" mechanisms — the docs distinguish them explicitly.

**Official Stop-hook loop primitive:** Anthropic's `ralph-wiggum` plugin (`anthropics/claude-code` → `plugins/ralph-wiggum/`, public marketplace 2025-11-16, "Made by Anthropic / Anthropic Verified") is the packaged form of the "Stop hook decides" mechanism — `hooks/stop-hook.sh` intercepts session exit and re-feeds the prompt, implementing Huntley's Ralph loop-until-done. Reach for it when a recipe wants a community-Ralph-style continuous loop without hand-rolling the hook.

## Engine framing (official)

- Anthropic frames Claude Code itself as the **agentic harness** around Claude: tools + context management + execution environment that turn an LLM into a coding agent. The agentic loop = *models that reason* + *tools that act*; each tool result feeds back to inform the next decision.
- Claude Code's loop is three blended phases — **gather context → take action → verify results** — repeated adaptively until the task is complete (a question may need only context-gathering; a bug fix cycles all three repeatedly).

## How this informs Nexus routing

- **`goal` recipe** (`reference/goal-recipe.md`): `/goal`'s fresh-model completion check *is* the maker/checker split applied to the stop condition. When setting up a goal loop, require a verifiable stop condition (e.g. "all tests in test/auth pass and lint clean"), not a vague "done".
- **`apex` Phase 6 / `summit` Phase 5**: these are loop-engineering loops driven by Orbit. Worktree-per-iteration + independent critic model are the load-bearing reliability primitives — see `reference/apex-recipe.md`, `reference/summit-recipe.md`.
- **Cross-engine portability**: connectors on both engines speak MCP, so a connector written for one usually works in the other. The loop *shape* is engine-agnostic — design the recipe once; bind primitives per `Orchestrator Detection`.
- **Known issue**: Claude Code GitHub issue #50357 — `isolation: worktree` is not applied via top-level `claude --agent`; it works via frontmatter. Surface this if recommending CLI-flag-based isolation.

## Caveats / gaps

- No public, verifiable ROI case study for loop engineering exists yet (esp. solo/consumer-plan). Don't assert efficiency gains as fact.
- Attribution detail and applicability limits live in `orbit/reference/loop-engineering.md`; this file is primitives-only.
