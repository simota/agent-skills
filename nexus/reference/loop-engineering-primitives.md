# Loop-Engineering Primitives — Claude Code, Codex & agy

How the **loop engineering** pattern maps onto concrete orchestration primitives in each hub engine. Nexus stays the routing/recipe layer; this file is the reference for *which primitive implements which loop part* when designing a `/goal`-style or apex/summit loop. For the concept, lineage, and applicability limits see `.claude/skills/orbit/reference/loop-engineering.md`.

> Capability mapping, not a version registry. `_common/CLI_COMPATIBILITY.md` owns current versions, flags, model IDs, and availability. Verify current primary docs before executing a version-sensitive branch; parenthetical versions below are historical provenance only.

## The pattern → primitive map

A loop = scheduled execution + isolated workspaces + maker/checker separation + persistent memory. Both hub engines now ship all parts natively (previously hand-rolled bash).

| Loop part | Claude Code | Codex |
|-----------|-------------|-------|
| Heartbeat (recurring) | `/loop` — **three modes by input** (see § `/loop` modes; interval mode v2.1.72+, self-pace v2.1.92-101); hooks; GitHub Actions / Desktop Scheduled tasks for laptop-closed runs | Automations tab (project + prompt + cadence + local/worktree target); Triage inbox for findings |
| Stop-when-done (in-session) | `/goal` (v2.1.139+): runs until a written condition holds; **a separate fast model — default Haiku — checks completion each turn from what's surfaced in the conversation only (it runs no commands, reads no files)**, so the maker isn't the grader. Bound runaway with a `or stop after N turns` clause in the condition | `/goal` (Codex CLI **v0.128.0**; persisted goal workflows GA'd 2026-05-21, "no longer experimental"): same primitive — works across turns until a verifiable stop condition, with create/pause/resume/clear. Codex has **no native `/loop`** — for a heartbeat, wrap `codex exec` (non-interactive) in a shell/cron loop |
| Workspace isolation | `git worktree`; `--worktree`/`-w` → `.claude/worktrees/<value>/` on branch `worktree-<value>` (v2.1.50); `isolation: worktree` in subagent frontmatter (temp worktree auto-removed if subagent finishes with no changes) | Built-in worktree support; multiple threads hit one repo without collision |
| Maker/checker separation | subagents (`.claude/agents/`, markdown) + agent teams; worktrees isolate *file edits*, subagents/teams coordinate *the work* | subagents spawned in parallel (≤8), results merged into one response; built-in `default`/`worker`/`explorer`; custom agents require `name`/`description`/`developer_instructions` (model + sandbox_mode inherited from parent); on-demand spawn only |
| Persistent memory | markdown / Linear / state files on disk — "the agent forgets, the repo doesn't" | same: state file outside the conversation as the loop's spine |
| **Loop-wide token bound** | **Not available in Claude Code** — `task_budget` is a Messages API feature and is explicitly unsupported on Claude Code and Cowork surfaces. In-session, bound with a `stop after N turns` clause plus `max_tokens`; the countdown mechanism is unavailable | n/a — Codex has no equivalent; bound via harness-side turn counting |

### agy column

agy ships **fewer** loop parts natively than either engine above, so more of the loop is hand-rolled by the hub. Author against these (`_common/AGY_ORCHESTRATION.md` A2/A4/A9, `reference/execution-layers.md` § Antigravity CLI):

| Loop part | agy | Note |
|-----------|-----|------|
| Heartbeat (recurring) | **No `/loop` equivalent.** `/schedule` exists in the slash-command list but its semantics are unverified — do not build on it | Implement the heartbeat *outside* agy: cron / CI / an external shell loop driving headless `agy -p` one-shots |
| Stop-when-done (in-session) | **No confirmed `/goal`** (absent from the published slash-command list — do not assume it) | Implement run-to-completion as an **external loop + completion oracle in the prompt** ("Done when …" + a self-validation pass) plus a persistence directive; the hub owns the stop decision |
| Workspace isolation | `/fork` branches the conversation into a separate workspace; git worktrees are managed by the hub, not by agy | Fork before risky/destructive trials so the main session stays clean |
| Maker/checker separation | Separate `/agent` invocations or separate headless one-shots — contexts are isolated by construction | **Ports cleanly and matters more here**: the generator is a fast model, so keep the checker at the High tier and give it an assume-broken rubric (A9) |
| Persistent memory | Filesystem artifacts (the same channel A2 mandates for deliverables) | The artifact bus doubles as the loop's state spine; `-c`/`--conversation <id>` resume (v1.0.8+) preserves session context between rounds |
| Loop-wide token bound | Not available — no `task_budget`, no countdown the model can see | Bound harness-side: turn counting + `--print-timeout`; poll `/usage` between rounds (it does not update live mid-run) |

**Consequence for recipe design:** an agy loop is *always* hub-driven. Every one of the five moves that Claude Code or Codex would delegate to a native primitive (heartbeat, stop-when-done) becomes explicit hub logic on agy — which means an agy loop must never be authored as "tell agy to keep going until done".

### `task_budget` — a loop bound for API-implemented steps only (beta `task-budgets-2026-03-13`)

**The one primitive that gives a loop a token budget the model itself can see**, so it paces work and finishes gracefully instead of being cut off. Verified 2026-07-25.

- **What it counts:** everything Claude *sees* in the agentic loop — thinking, tool calls, tool results, output. Not what the client resends: replayed history is counted once, so the countdown is far smaller than cumulative payload.
- **Relationship to effort:** orthogonal and complementary — **`effort` tunes depth per step, `task_budget` tunes breadth across the loop.** `max_tokens` remains the only hard cap (per request); the budget is a **soft hint** the model may exceed rather than abandon an action mid-flight.
- **Sizing:** measure a representative task set *without* a budget, then **start at the p99** of per-task spend. Minimum accepted `total` is **20,000 tokens** (below → 400).
- **The failure mode to know:** a budget that is too small for the task reads as impossible and produces **refusal-like behavior** — the model declines, aggressively de-scopes, or stops early with a partial. If unexpected refusals or premature stops appear after adding a budget, **raise the budget before debugging anything else.**
- **Do not mirror the countdown client-side.** Decrementing `remaining` while also resending full history double-counts: the model sees an under-reported budget and wraps up too early. Pass `remaining` **only** when the loop compacts or rewrites context between requests (the server has no memory across a rewrite); otherwise omit it and let the server track.
- **Caching:** the budget value renders into the prompt, so changing it mid-conversation invalidates the cache prefix. Set it once on the initial request.
- **Support:** Opus 5, Fable 5, Mythos 5, Opus 4.8, Opus 4.7. **Not** Sonnet 5, Opus 4.6, Sonnet 4.6, Haiku 4.5 — and **not Claude Code**. So for a Nexus loop this applies only to steps implemented as direct Messages API calls, never to the `/loop` + `/goal` in-session path.

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
- **Verification is the floor and the hardest move**: the generator's level decides what the loop *can* produce; the evaluator's level decides what it *will not*. Tune the evaluator to assume-broken and judge by *acting* (Playwright MCP: click/screenshot/run) not reading — see `.claude/skills/orbit/reference/loop-engineering.md` and the `goal` recipe.
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
- Attribution detail and applicability limits live in `.claude/skills/orbit/reference/loop-engineering.md`; this file is primitives-only.
