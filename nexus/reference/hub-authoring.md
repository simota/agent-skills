# Hub-Engine Authoring

Per-engine authoring protocols that apply once the hub orchestrator is detected (see SKILL.md → **Execution Model → Orchestrator Detection**).

## Claude Code hub

Apply `_common/OPUS_48_AUTHORING.md` principles **P4 (parallel subagent triggers), P6 (effort-level awareness), P7 (delegation framing), P9 (effort-calibrated tool use)**.

Opus 4.8 spawns fewer subagents and reasons more by default, respects `effort` strictly, and follows instructions literally — explicit fan-out triggers, per-step model/effort selection, and explicit step scope are mandatory. Spawn prompts must state thinking nudges (P5) and length envelopes (P2).

## Claude Code hub — Fable 5

> Source: Anthropic "Prompting Claude Fable 5" + "Introducing Claude Fable 5 and Claude Mythos 5" (platform.claude.com, 2026-06). Applies when the Claude Code hub session runs on `claude-fable-5`. The P-principles still hold; the F-principles below **override** them where they conflict, because Fable 5's behavior differs from Opus 4.8. When the hub model is unknown, author for Opus 4.8 — safe on both.

Fable 5 is a Mythos-class model: 1M context, adaptive-thinking-only (raw CoT never returned), safety classifiers that can return `stop_reason:"refusal"`. The orchestration-relevant behavior shifts:

| Behavior | Opus 4.8 | Fable 5 → Nexus action |
|----------|----------|------------------------|
| Default effort | `xhigh` | `high`; `xhigh` only for capability-sensitive steps, `low`/`medium` for routine (still exceed prior-model `xhigh`). Lower effort if a step finishes but runs longer than needed |
| Spawn-prompt verbosity | Four directive fields mandatory; enumerate behaviors | **Lighter** — a brief outcome+brevity instruction steers as well as enumerating; over-prescriptive prompts/skills *degrade* output |
| Parallel subagents | Sparse — explicit fan-out triggers mandatory (P4) | Dispatches readily; relax explicit triggers. Prefer **async** orchestrator↔subagent communication over blocking on each `wait`; long-lived subagents save cache + avoid slowest-branch bottleneck |
| Turn length | Minutes | Can run many minutes/hours per step. Raise client timeouts, prefer `run_in_background` + async check-in over blocking; restructure long chains as checkpoint-resumable |
| Reasoning visibility | Returnable | Raw CoT never returned. **Never** instruct a spawned agent to echo/show/transcribe/explain its reasoning as response text — trips `reasoning_extraction` refusal → forced Opus 4.8 fallback. Read summarized `thinking` blocks instead |

**F-principles (apply on top of P4/P6/P7/P9 for a Fable 5 hub):**

- **F1 — No reasoning reproduction.** Audit every spawn prompt and the spawned skill's SKILL.md for "show your reasoning / explain step by step in the response / transcribe your thinking" wording. Strip it. For reasoning visibility use summarized thinking + a send-to-user tool, not response-text echo. *(Highest priority — silent fallback-rate inflater.)*
- **F2 — Light spawn prompts.** Keep the spawn template's acceptance-criteria + a one-line brevity/outcome instruction; drop enumerated per-behavior directives. Lead spawned agents with "report the outcome first."
- **F3 — Default `high` effort.** Plan and execute steps default to `high`. Reserve `xhigh` for the hardest design/verify steps; drop to `medium`/`low` for routine fan-out. Don't over-budget routine work at high effort (Fable 5 over-explores/refactors when un-scoped — add "do the simplest thing; don't refactor/abstract beyond the task" to spawn prompts).
- **F4 — Async fan-out.** Spawn parallel subagents freely; communicate asynchronously; keep the orchestrator working while branches run. Don't serialize on `wait` unless a barrier is genuinely required.
- **F5 — Ground long-run progress.** For chains ≥ 4 steps or autonomous runs, instruct each agent: "Before reporting progress, audit each claim against a tool result from this session; if unverified, say so." Nearly eliminates fabricated status.
- **F6 — Refusal-aware routing.** Steps in offensive-security / biology-life-sciences / reasoning-extraction domains can return `stop_reason:"refusal"` (HTTP 200, not an error). Configure fallback to Opus 4.8 (`fallbacks` param or SDK middleware); a refused-before-output step is not billed. Treat `refusal` as a routing signal, not a failure.
- **F7 — Verbatim user surfacing in async runs.** For long, asynchronous chains (apex/summit/goal-loop) where a deliverable, a numeric progress update, or a mid-loop reply must reach the user *exactly as written*, give the orchestrating agent a `send_to_user` tool (input = the message; render the input directly, return a bare ack). Tool inputs are never summarized, so the content arrives intact — unlike a final summary, which Fable 5 may re-ground or compress. Use it only when UX depends on verbatim delivery; routine progress narration needs no tool. Pairs with F5 (grounded claims) and the no-reasoning-reproduction rule (F1 — surface summarized `thinking`, never raw CoT).
- **F8 — Fable 5 cost gate.** Fable 5 hub reasoning is expensive — don't spend it on tasks that don't need it. At CLASSIFY, if the task is `SIMPLE` / a single trivial step (no multi-domain planning, no high-reasoning design), **pause and confirm before executing**, recommending the cheaper path: delegate directly to a Sonnet 5 subagent, or suggest re-running the hub on Sonnet 5 / Opus 4.8. This gate is **contract-level** (`AUTORUN`/`AUTORUN_FULL` cannot skip it) and mirrors the SKILL.md **Ask First** cost gate. Once confirmed, proceed normally. Genuinely complex / multi-agent tasks that need Fable 5-tier planning proceed without the gate — the gate targets *overkill*, not all work. Judge "warrants Fable 5" by the CLASSIFY complexity + chain size, not by wall-clock.

## Codex CLI hub

Apply `_common/CODEX_ORCHESTRATION.md` principles **C1 (spawn-depth budget), C2 (synchronous fan-out/join), C6 (checkpoint-resume)**, plus C3/C7 for model and approval posture.

Codex has no background-spawn primitive (parallel = N `spawn_agent` → `wait_agent` all), gates fan-out via `agents.max_depth`, and runs the latest gpt-5.6 generation for every step and subagent with role-based variants (hub/plan=sol, standard implementation=terra, rote subagents=luna — C3.0), tuning depth within a variant via the `model_reasoning_effort` config key (`minimal|low|medium|high|xhigh`), not by an Opus `effort` enum.

## agy hub

Apply `_common/AGY_ORCHESTRATION.md` (A1–A9) — the first-class agy authoring protocol (analog of OPUS_48_AUTHORING / CODEX_ORCHESTRATION). Core levers: **A1** single-model effort-tier routing (Gemini 3.5 Flash mandate ‡; vary High/Medium/Low per step — High for plan/design/verify), **A2** file-handoff capture + real pty (headless `agy -p` never flushes non-TTY stdout), **A3** session-scoped model/tier (no per-agent switch — split mixed-effort chains into per-step headless invocations), **A4** spawn topology (no background primitive / no Rally L3 — flatten; resume via `-c`/`--conversation` since v1.0.8), **A6** never `--sandbox` + `--dangerously-skip-permissions` (#36). Full constraints: `_common/CLI_COMPATIBILITY.md §3, §9`.

## Spawn Template Variants

> The directive fields below are the **vetted library** that `reference/adaptive-prompt-policy.md` selects and dials within when it tailors a spawn prompt to project + session context. That policy chooses *which* envelope/effort/directive values to use; this file defines the safe ranges and the per-engine rules it must honor.

**Claude Code (`Agent(...)`)** uses the canonical template in SKILL.md → **Agent Spawn Template**. On an **Opus 4.8** hub the four directive fields (acceptance criteria / output length / tool-use / thinking) are not optional: Opus 4.8 calibrates output length to context, restrains tool calls by default (raise `effort` to increase tool use), and interprets each field literally, so both under- and over-shoot occur when these are implicit. On a **Fable 5** hub these directives are lighter (F2): keep acceptance-criteria + a one-line brevity/outcome instruction, drop enumerated per-behavior directives, and **never** include reasoning-reproduction wording (F1 — trips `reasoning_extraction` refusal). For parallel spawns, issue multiple `Agent(... run_in_background: true)` calls in the same turn (Fable 5 dispatches these readily — F4). Shared protocol: `_common/OPUS_48_AUTHORING.md`; Fable 5 deltas: § Claude Code hub — Fable 5.

**Codex CLI variant**: same prompt body; resolve skill path to `~/.codex/skills/[agent]/SKILL.md` or `<repo>/.agents/skills/[agent]/SKILL.md`. Four directive fields stay required. Authoring follows `_common/CODEX_ORCHESTRATION.md` (C-principles), not the Opus note — always the latest gpt-5.6 generation with the role-matched variant (sol/terra/luna, C3.0), depth via `model_reasoning_effort` (C3); fan-out gated by `agents.max_depth` + `agents.max_threads` (C1). API patterns (L1 `spawn_agent`→`wait_agent`, L2 parallel-then-join, L3 `send_input`/`resume_agent`/`close_agent` for checkpoint-resume) → `reference/execution-layers.md` § Codex CLI.

**agy variant**: same prompt body; TUI via `/agent [agent]-[task-slug] "<body>"`, headless via `agy -p "<body>" --dangerously-skip-permissions`. **Model mandate (user policy, 2026-06-23): pin Gemini 3.5 Flash for every step / subagent** — `agy --model "Gemini 3.5 Flash"` (headless) or `/model` (TUI) before spawning; never Gemini 3.1 Pro / Claude / GPT-OSS (stricter than the Codex latest-generation mandate ‡ — one fixed *fast* model, no variant tiering). Headless capture is **file-handoff, not stdout** — append the `_common/CLI_COMPATIBILITY.md §9.2` MANDATORY OUTPUT PROTOCOL (absolute-path artifact + `<<<END_OF_OUTPUT>>>` sentinel) and reference files via `@<path>`. Full silent-failure mitigations + verified template → `reference/execution-layers.md` § agy. Replace skill path with `~/.gemini/antigravity-cli/skills/[agent]/SKILL.md` or `<repo>/.agents/skills/[agent]/SKILL.md`.

## Execution-Layer Key Rules

- **Codex**: `spawn_agent` may be lazily hidden — attempt the call when prereqs hold ("tool not visible" ≠ "tool not callable"). Codex tools: `spawn_agent`, `send_input`, `wait_agent`, `resume_agent`, `close_agent`.
- **agy headless**: use `@<path>` to inject file context; mandate absolute-path artifact write + `<<<END_OF_OUTPUT>>>` sentinel — `agy -p` never flushes to non-TTY stdout (issues #76 non-TTY/subprocess + #115 Windows/`text_drip`, both OPEN, unfixed through v1.0.10 / 2026-06-23). Pass `--print-timeout 15m` for heavy syntheses; `--log-file <path>` for quota/OAuth failure diagnosis. **Never add `--sandbox` to a `--dangerously-skip-permissions` spawn** (issue #36 — the skip flag auto-approves `bypassSandbox`, defeating the sandbox); contain via host-level isolation. Headless resume (`-c`/`--conversation <id>`) is usable since v1.0.8.
- **agy Pre-flight Notification**: before the first `agy -p ... --dangerously-skip-permissions` spawn of a session, emit the notification per `_common/CLI_COMPATIBILITY.md §9.1`.
- **Permission model**: agy defaults to `request-review`; autonomous Nexus must switch to `proceed-in-sandbox` (TUI) or `--dangerously-skip-permissions` (headless). Never use `always-proceed` in production.

## Model Selection

Model names are hub-engine-specific. The role → tier mapping is stable; the concrete model per tier depends on the orchestrator engine.

| Agent Role | Tier | Claude Code hub | Codex CLI hub | Rationale |
|-----------|------|-----------------|---------------|-----------|
| Investigation / read-only (Scout, Lens, Trail) | balanced | **Sonnet 5** (`claude-sonnet-5`) ¶ | `gpt-5.6-terra` † | Cost-efficient |
| Standard implementation (Builder, Artisan, Radar) | balanced | **Sonnet 5** (`claude-sonnet-5`) ¶ | `gpt-5.6-terra` † | Balanced |
| High-complexity design (Sentinel, Atlas) | high-reasoning | opus / **fable-5** | `gpt-5.6-sol` † | Precision-critical |
| Lightweight tasks (Quill, Morph) | fast | haiku | `gpt-5.6-luna` † | Minimal cost |

> **† Codex latest-generation mandate + variant tiering (user policy, `CODEX_ORCHESTRATION.md` C3.0):** the Codex column is always the **latest generation — currently the `gpt-5.6` family**; never a previous generation. Within the family, the variant follows the role (hub/plan/design = sol, standard implementation = terra, rote/high-volume = luna, per official guidance). Differentiate further via `model_reasoning_effort`. (Claude Code tiering is unaffected.)
>
> **‡ agy model mandate (user policy, 2026-06-23):** when **agy** drives the hub, every step and every spawned subagent uses **Gemini 3.5 Flash** — never tier-switched to Gemini 3.1 Pro / Claude / GPT-OSS. Pin with `agy --model "Gemini 3.5 Flash"` / `/model`. Stricter than the Codex mandate (which tiers by variant within the latest generation): agy is one fixed fast model with no tiering. Detail: `_common/CLI_COMPATIBILITY.md §4 ‡`.
>
> **¶ Claude Code subagent default (user policy, 2026-07-02):** when **Claude Code** drives the hub, spawned subagents use **Sonnet 5 (`claude-sonnet-5`)** by default, selected **task-appropriately** — Sonnet 5 for the balanced/execution tier (investigation, read-only, standard implementation), escalating to **opus / fable-5** only for the high-reasoning tier (planning, high-complexity design/verify) and dropping to **haiku** only for trivial/lightweight steps. Unlike the Codex `†` and agy `‡` mandates (one fixed model regardless of tier), this is a **task-aware default, not a blanket lock** — the Plan-and-Execute split still governs (capable model plans, Sonnet 5 executes). Pin a spawn with `model: claude-sonnet-5` in the Agent Spawn Template.

Fable 5 hub: `claude-fable-5` serves the high-reasoning tier (plan + hardest design/verify steps); default effort `high`, `xhigh` only for capability-sensitive steps, `medium`/`low` for routine fan-out — Fable 5's lower effort already exceeds prior-model `xhigh`. Route refusal-prone domain steps with an Opus 4.8 fallback (F6). Full behavior deltas → § Claude Code hub — Fable 5.

Codex hub: the hub runs **`gpt-5.6-sol`**; every spawned subagent runs the role-matched gpt-5.6 variant (sol=plan/design, terra=standard implementation, luna=rote — latest-generation mandate, `CODEX_ORCHESTRATION.md` C3.0; never a previous generation). Tune depth within a variant via `model_reasoning_effort` (`minimal|low|medium|high|xhigh`, default `medium` — re-verified 2026-07; start at the lowest acceptable effort, no exact 5.5→5.6 mapping). agy hub: **mandated to Gemini 3.5 Flash for all steps/subagents (‡)** — set per-session via `/model` (TUI) or `agy --model "Gemini 3.5 Flash"` (headless); not per-agent.
