# Hub-Engine Authoring

Per-engine authoring protocols that apply once the hub orchestrator is detected (see § Orchestrator Detection below). **Canonical home** for the Agent Spawn Template and the Orchestrator Detection table — SKILL.md carries only the dispatch-critical minimum and a pointer here.

**Volatile runtime facts:** `_common/CLI_COMPATIBILITY.md` is authoritative for current model IDs, CLI versions, flags, availability, and limits. Dates and product names below explain an authoring branch but never override that compatibility matrix or current official documentation.

## Orchestrator Detection

Before the first spawn, detect which CLI drives **this hub session** (implicit in the available tooling — detect once, reuse), then bind the spawn API, authoring protocol, and model map:

| Signal | Hub engine | Spawn API | Authoring protocol | Model map |
|--------|-----------|-----------|--------------------|-----------|
| `Agent` tool present | **Claude Code** | `Agent(...)` (L1 fg / L2 background) | `_common/OPUS_5_AUTHORING.md` (P); Fable 5 hub → +§ Claude Code hub — Fable 5 (F) | Sonnet 5 default / opus / haiku / fable-5 (§ Model Selection) |
| `spawn_agent` callable (C1 holds) | **Codex CLI** | `spawn_agent`→`wait_agent` (N spawn → join all) | `_common/CODEX_ORCHESTRATION.md` (C) | `gpt-5.6` sol/terra/luna by role (`CLI_COMPATIBILITY.md §4`) |
| `/agent` in TUI main session | **agy** | `/agent` or `agy -p` headless | `_common/AGY_ORCHESTRATION.md` (A1–A9) | Gemini 3.7 Flash (High) mandated ‡, tier via `/model` |

Codex-hub prereqs (C1): `multi_agent = true` + `[agents] max_depth >= 2`; unmet → internal per SKILL.md Core Rule #3 (`spawn_agent` may be lazily hidden — attempt when prereqs hold, C5). Details → `_common/CLI_COMPATIBILITY.md`, `reference/execution-layers.md`. Unknown Claude Code model → author for Opus 5, safe on both.

## Claude Code hub

Apply `_common/OPUS_5_AUTHORING.md` principles **P4 (subagent delegation caps), P6 (effort-level awareness), P7 (delegation framing), P9 (no redundant verification scaffolding)**.

Opus 5 **delegates readily and verifies its own work**, so the hub's job is to *bound* fan-out and *not* to instruct self-checks: state delegation criteria plus a spawn ceiling, and never tell a spawned agent to double-check or re-verify its own output. Independent verification stays — a *different* agent (Radar after Builder, Judge after implementation) is an architectural control, not a self-check. Default effort is `high`; name `xhigh` explicitly for coding/agentic steps and set `max_tokens` ≥ 64k there. Opus 5's output runs long in both channels, so spawn prompts must state length envelopes (P2) and bound step scope (P8) — Opus 5 can widen a task on its own. Thinking is on by default (P5); do not author steps that assume it is off.

## Claude Code hub — Fable 5

> Source: Anthropic "Prompting Claude Fable 5" + "Introducing Claude Fable 5 and Claude Mythos 5" (platform.claude.com, 2026-06). Applies when the Claude Code hub session runs on `claude-fable-5`. The P-principles still hold; the F-principles below **override** them where they conflict, because Fable 5's behavior differs from Opus 5. When the hub model is unknown, author for Opus 5 — safe on both.

Fable 5 is a Mythos-class model: 1M context, adaptive-thinking-only (raw CoT never returned), safety classifiers that can return `stop_reason:"refusal"`. The orchestration-relevant behavior shifts are the F-principles below — each states the Fable 5 action directly, so the Opus 5 baseline is not re-tabled.

**F-principles (apply on top of P4/P6/P7/P9 for a Fable 5 hub):**

- **F1 — No reasoning reproduction.** Audit every spawn prompt and the spawned skill's SKILL.md for "show your reasoning / explain step by step in the response / transcribe your thinking" wording. Strip it. For reasoning visibility use summarized thinking + a send-to-user tool, not response-text echo. *(Highest priority — silent fallback-rate inflater.)*
- **F2 — Light spawn prompts, whole-job delegation.** Keep the spawn template's acceptance-criteria + a one-line brevity/outcome instruction; drop enumerated per-behavior directives. Lead spawned agents with "report the outcome first." Give **context rather than constraints** — who the work is for, when it is needed, what success looks like — the way you would brief a colleague, and hand each agent a **complete job described by its outcome**, not a procedure split into intermediate steps: Fable 5 plans, checks itself mid-run, and recovers without restarting, so pre-decomposing a step into micro-prompts wastes the capability the model is being paid for. Two corollaries: (a) **audit inherited corrections** — spawn-prompt wording added to work around an older model's failure mode is a prime P12 deletion candidate and may now be actively harmful, so re-justify it before carrying it forward; (b) **do not overload a branch's context** — start a fresh spawn for a new task rather than extending a long-running one. [Source: claude.com/blog — *Working with Claude Fable 5 in Claude Cowork* (2026-07-16), *Working at the frontier: Rakuten* (2026-07-20), *…Base44* (2026-07-15)]
- **F3 — Default `high` effort.** Plan and execute steps default to `high`. Reserve `xhigh` for the hardest design/verify steps; drop to `medium`/`low` for routine fan-out. Don't over-budget routine work at high effort (Fable 5 over-explores/refactors when un-scoped — add "do the simplest thing; don't refactor/abstract beyond the task" to spawn prompts).
- **F4 — Async fan-out.** Spawn parallel subagents freely; communicate asynchronously; keep the orchestrator working while branches run. Don't serialize on `wait` unless a barrier is genuinely required — long-lived subagents preserve cache and avoid the slowest-branch bottleneck. **A Fable 5 step can run many minutes to hours** (vs minutes on Opus 5), so raise client timeouts, prefer `run_in_background` + async check-in over blocking, and restructure long chains as checkpoint-resumable.
- **F5 — Ground long-run progress.** For chains ≥ 4 steps or autonomous runs, instruct each agent: "Before reporting progress, audit each claim against a tool result from this session; if unverified, say so." Nearly eliminates fabricated status.
- **F6 — Refusal-aware routing.** Steps in offensive-security / biology-life-sciences / reasoning-extraction domains can return `stop_reason:"refusal"` (HTTP 200, not an error). Configure fallback to Opus 5 (`fallbacks` param or SDK middleware); a refused-before-output step is not billed. Treat `refusal` as a routing signal, not a failure.
- **F7 — Verbatim user surfacing in async runs.** For long, asynchronous chains (apex/summit/goal-loop) where a deliverable, a numeric progress update, or a mid-loop reply must reach the user *exactly as written*, give the orchestrating agent a `send_to_user` tool (input = the message; render the input directly, return a bare ack). Tool inputs are never summarized, so the content arrives intact — unlike a final summary, which Fable 5 may re-ground or compress. Use it only when UX depends on verbatim delivery; routine progress narration needs no tool. Pairs with F5 (grounded claims) and the no-reasoning-reproduction rule (F1 — surface summarized `thinking`, never raw CoT).
- **F8 — Fable 5 cost gate.** Fable 5 hub reasoning is expensive — don't spend it on tasks that don't need it. At CLASSIFY, if the task is `SIMPLE` / a single trivial step (no multi-domain planning, no high-reasoning design), **pause and confirm before executing**, recommending the cheaper path: delegate directly to a Sonnet 5 subagent, or suggest re-running the hub on Sonnet 5 / Opus 5. This gate is **contract-level** (`AUTORUN`/`AUTORUN_FULL` cannot skip it) and mirrors the SKILL.md **Ask First** cost gate. Once confirmed, proceed normally. Genuinely complex / multi-agent tasks that need Fable 5-tier planning proceed without the gate — the gate targets *overkill*, not all work. Judge "warrants Fable 5" by the CLASSIFY complexity + chain size, not by wall-clock.

## Codex CLI hub

Apply `_common/CODEX_ORCHESTRATION.md` principles **C1 (spawn-depth budget), C2 (synchronous fan-out/join), C6 (checkpoint-resume)**, plus C3/C7 for model and approval posture.

Codex has no background-spawn primitive (parallel = N `spawn_agent` → `wait_agent` all), gates fan-out via `agents.max_depth`, and runs the latest gpt-5.6 generation for every step and subagent with role-based variants (hub/plan=sol, standard implementation=terra, rote subagents=luna — C3.0), tuning depth within a variant via the `model_reasoning_effort` config key (`minimal|low|medium|high|xhigh`), not by an Opus `effort` enum.

## agy hub

Apply `_common/AGY_ORCHESTRATION.md` (A1–A9) — the first-class agy authoring protocol (analog of OPUS_5_AUTHORING / CODEX_ORCHESTRATION). Core levers: **A1** single-model effort-tier routing (model mandate ‡, full definition in § Model Selection — recipe steps run High with no downgrade + the Deep Reasoning Directive per A1-R/A9-D), **A2** file-handoff capture + real pty (headless `agy -p` never flushes non-TTY stdout), **A3** session-scoped model/tier (no per-agent switch — split mixed-effort chains into per-step headless invocations), **A4** spawn topology (no background primitive / no Rally L3 — flatten; resume via `-c`/`--conversation` since v1.0.8), **A6** never `--sandbox` + `--dangerously-skip-permissions` (#36). Full constraints: `_common/CLI_COMPATIBILITY.md §3, §9`.

## Agent Spawn Template

> Canonical template — SKILL.md § Execution Model carries only the P1/P2/P8 always-include rule and the no-self-verification prohibition inline; this is the full prompt structure those rules bind.

```
Agent(
  name: "[agent]-[task-slug]"
  description: "[Short task description]"
  subagent_type: general-purpose
  mode: bypassPermissions
  model: [claude-sonnet-5 (task-appropriate default) | opus | haiku]
  prompt: |
    You are the [AgentName] agent.
    First, read ~/.claude/skills/[agent]/SKILL.md and follow its instructions.

    Recipe: [recipe-name or auto]                # P-REC
    Task: [task_description]
    Context from previous step: [handoff_context]
    Constraints: [constraints]
    Acceptance criteria: [acceptance_criteria]   # P1 — always
    Output length envelope: [length_envelope]    # P2 — always
    Scope bound: [in_scope / out_of_scope]       # P8 — always
    Prohibited outcomes: [must_not_happen | none]           # Q2 — always
    Authority: allowed=[effects this step may cause]
               denied=[effects it may not]
               redelegation: false               # Q23 — always
    Completion bound: finish every in-scope item; no TODO/FIXME/placeholder/
      stub bodies in what you produce. Do not relax the acceptance criteria
      to make your output pass, and do the hard part before the polish.
      Cannot finish an item? return PARTIAL with residual + class
      (blocked-external | gate-pending | out-of-contract | budget-exhausted)
      and name the alternative you already tried — never SUCCESS over a
      skeleton, never BLOCKED on a first attempt.    # Q16-Q17, Q20-Q22 — always
    Tool-use directive: [tool_use_directive]     # P3 — optional
    Thinking directive: [thinking_directive]     # P5 — optional

    On completion, emit:
    _STEP_COMPLETE:
      Agent: [AgentName]
      Status: SUCCESS | PARTIAL | BLOCKED | FAILED
      Output: [deliverable — strictly within the envelope above]
      Residual: [none | <item> (class: …, marker: file:line)]   # Q17-Q18
      Next: [recommended next agent or DONE]
)
```

**The `Completion bound` field is not optional.** A spawned agent that trims the hard 20% into a "future work" note is the single largest source of unfinished chains: the hub aggregates a `SUCCESS`, the residue never reaches the Residual Ledger, and DELIVER reports a skeleton as done. The field is a *scope-honesty* control, not a quality exhortation — it tells the agent that `PARTIAL` + a typed residual is the **preferred** answer when it genuinely cannot finish, which is why it does not read as "try harder" filler. It never widens the task: `Scope bound` (P8) still decides what is in scope; `Completion bound` only decides that whatever is in scope is carried to done. Full contract: `reference/autonomy-quality-protocol.md` §0 + §7 (Q16–Q22); the hub owns the Q18 ledger and the Q19 sweep — never delegate a step's completion sweep to that same step (Q9). The Q20–Q22 half of the field is deliberately phrased as three concrete behaviors, not as encouragement: "do your best" / "never give up" wording is P12 filler that costs tokens and changes nothing, while "do not relax the criteria" and "name the alternative you tried" are checkable at AGGREGATE.

**The `Authority` and `Prohibited outcomes` fields are the effect-side counterpart of `Scope bound`.** Scope says which files and questions are the step's; Authority says which *effects* are the step's, and prohibited outcomes say which results must not occur however the step works. They are load-bearing because the platform grants a spawned agent the hub's own permissions: `mode: bypassPermissions` is a *capability*, never an authorization, so an unstated grant reads as "everything the tools can reach". Write the narrowest set the acceptance criteria actually need — `allowed=read + edit under src/auth/**`, `denied=git push, dependency installs, external requests, further spawns` — and keep `redelegation: false` unless the step is a feature-lead that genuinely coordinates sub-agents (Core Rule #9), in which case name the sub-grant, which can only narrow. A step that finds it needs a wider effect set **returns and asks**; a step that takes it is the failure Q23 exists to catch. Effects the hub itself is not authorized to cause cannot be granted at all — a grant never satisfies an **Ask First** trigger. Full contract: `reference/autonomy-quality-protocol.md` §8.

**Never include self-verification wording** ("verify your work", "double-check", "re-verify before responding") — Opus 5 self-verifies and these cause over-verification (P9); independent verification lives in the *chain* as a separate agent, never in a producer's own prompt. Fable 5 hub directives are lighter, not heavier, and must never request reasoning reproduction (`reasoning_extraction` refusal). Detailed flows → `reference/execution-phases.md`, `reference/orchestration-patterns.md`.

## Spawn Template Variants

> The directive fields below are the **vetted library** that `reference/adaptive-prompt-policy.md` selects and dials within when it tailors a spawn prompt to project + session context. That policy chooses *which* envelope/effort/directive values to use; this file defines the safe ranges and the per-engine rules it must honor.

**Claude Code (`Agent(...)`)** uses the canonical template above → **Agent Spawn Template**. On an **Opus 5** hub the load-bearing fields are acceptance criteria, **output length envelope**, and **scope bound**: Opus 5's default output runs long in both channels and it can widen a task on its own, and effort does not shorten visible output. Omit self-check wording entirely (P9) — it triggers over-verification. Tool-use directives stay useful, but effort is what moves call volume. On a **Fable 5** hub these directives are lighter (F2): keep acceptance-criteria + a one-line brevity/outcome instruction, drop enumerated per-behavior directives, and **never** include reasoning-reproduction wording (F1 — trips `reasoning_extraction` refusal). For parallel spawns, issue multiple `Agent(... run_in_background: true)` calls in the same turn (Fable 5 dispatches these readily — F4). Shared protocol: `_common/OPUS_5_AUTHORING.md`; Fable 5 deltas: § Claude Code hub — Fable 5.

**Codex CLI variant**: same prompt body; resolve skill path to `~/.codex/skills/[agent]/SKILL.md` or `<repo>/.agents/skills/[agent]/SKILL.md`. Four directive fields stay required. Authoring follows `_common/CODEX_ORCHESTRATION.md` (C-principles), not the Opus note — always the latest gpt-5.6 generation with the role-matched variant (sol/terra/luna, C3.0), depth via `model_reasoning_effort` (C3); fan-out gated by `agents.max_depth` + `agents.max_threads` (C1). API patterns (L1 `spawn_agent`→`wait_agent`, L2 parallel-then-join, L3 `send_input`/`resume_agent`/`close_agent` for checkpoint-resume) → `reference/execution-layers.md` § Codex CLI.

**agy variant**: same prompt body; TUI via `/agent [agent]-[task-slug] "<body>"`, headless via `agy -p "<body>" --dangerously-skip-permissions` — pin the model mandate ‡ (§ Model Selection) before spawning. For every recipe spawn, append the **Deep Reasoning Directive** per A1-R (§ agy hub). Headless capture is **file-handoff, not stdout** — append the `_common/CLI_COMPATIBILITY.md §9.2` MANDATORY OUTPUT PROTOCOL (absolute-path artifact + `<<<END_OF_OUTPUT>>>` sentinel) and reference files via `@<path>`. Full silent-failure mitigations + verified template → `reference/execution-layers.md` § agy. Replace skill path with `~/.gemini/antigravity-cli/skills/[agent]/SKILL.md` or `<repo>/.agents/skills/[agent]/SKILL.md`.

## Execution-Layer Key Rules

Codex tool-visibility (`spawn_agent`/`send_input`/`wait_agent`/`resume_agent`/`close_agent`), agy headless artifact-capture (issues #76/#115/#36) + pre-flight notification, and the agy permission model (`request-review` → `proceed-in-sandbox`/`--dangerously-skip-permissions`) are owned by `reference/execution-layers.md` § Codex CLI / § Antigravity CLI and `_common/CLI_COMPATIBILITY.md` §9.1 — same issue numbers, not restated here.

## Model Selection

Model names are hub-engine-specific. The role → tier mapping is stable; the concrete model per tier depends on the orchestrator engine.

| Agent Role | Tier | Claude Code hub | Codex CLI hub | Rationale |
|-----------|------|-----------------|---------------|-----------|
| Investigation / read-only (Scout, Lens, Trail) | balanced | **Sonnet 5** (`claude-sonnet-5`) ¶ | `gpt-5.6-terra` † | Cost-efficient |
| Standard implementation (Builder, Artisan, Radar) | balanced | **Sonnet 5** (`claude-sonnet-5`) ¶ | `gpt-5.6-terra` † | Balanced |
| High-complexity design (Sentinel, Atlas) | high-reasoning | opus / **fable-5** | `gpt-5.6-sol` † | Precision-critical |
| Lightweight tasks (Quill, Scribe) | fast | haiku | `gpt-5.6-luna` † | Minimal cost |

> **† Codex latest-generation mandate + variant tiering (user policy, `CODEX_ORCHESTRATION.md` C3.0):** the Codex column is always the **latest generation — currently the `gpt-5.6` family**; never a previous generation. Within the family, the variant follows the role (hub/plan/design = sol, standard implementation = terra, rote/high-volume = luna, per official guidance). Differentiate further via `model_reasoning_effort`. (Claude Code tiering is unaffected.)
>
> **‡ agy model mandate (user policy, 2026-06-23):** when **agy** drives the hub, every step and every spawned subagent uses **Gemini 3.7 Flash (High)** — never tier-switched to Gemini 3.1 Pro / Claude / GPT-OSS. Pin with `agy --model "Gemini 3.7 Flash (High)"` / `/model`. Stricter than the Codex mandate (which tiers by variant within the latest generation): agy is one fixed fast model with no tiering. Detail: `_common/CLI_COMPATIBILITY.md §4 ‡`.
>
> **¶ Claude Code subagent default (user policy, 2026-07-02):** when **Claude Code** drives the hub, spawned subagents use **Sonnet 5 (`claude-sonnet-5`)** by default, selected **task-appropriately** — Sonnet 5 for the balanced/execution tier (investigation, read-only, standard implementation), escalating to **opus / fable-5** only for the high-reasoning tier (planning, high-complexity design/verify) and dropping to **haiku** only for trivial/lightweight steps. Unlike the Codex `†` and agy `‡` mandates (one fixed model regardless of tier), this is a **task-aware default, not a blanket lock** — the Plan-and-Execute split still governs (capable model plans, Sonnet 5 executes). Pin a spawn with `model: claude-sonnet-5` in the Agent Spawn Template.
>
> *Vendor backing for the ¶ default:* Anthropic positions **Sonnet as the tier for high-volume sub-agents in multi-agent setups**, and states that model choice follows **task difficulty, not domain** — with the recommended procedure being to start from the most capable generally available model and then step down using **effort levels**, guided by your own evals. That ordering matters for a chain: pick the tier by how hard the step is, then tune `effort` within it, rather than reaching for a different model first. The published lineup is **Mythos** (trusted-org-restricted) → **Fable** (public, additional safeguards) → **Opus** → **Sonnet** → **Haiku**. [Source: claude.com/blog — *Claude models explained: choosing the best model for your use case*, 2026-07-24]

Fable 5 hub: `claude-fable-5` serves the high-reasoning tier (plan + hardest design/verify steps); default effort `high`, `xhigh` only for capability-sensitive steps, `medium`/`low` for routine fan-out — Fable 5's lower effort already exceeds prior-model `xhigh`. Route refusal-prone domain steps with an Opus 5 fallback (F6). Full behavior deltas → § Claude Code hub — Fable 5.

**Advisor tool — the API-native form of this split.** When a chain step is implemented as a *Messages API call* rather than a spawned CLI agent, `advisor_20260301` (beta `advisor-tool-2026-03-01`) lets a cheap executor consult a stronger advisor mid-generation inside one request — no orchestration round trip. Pairing rule: the advisor must be at least as capable as the executor, so `Sonnet 5 executor + Opus 5 advisor` is valid and matches the ¶ default, while an Opus 5 executor may only take a Fable 5 / Mythos 5 / Opus 5 advisor. Bound it with `max_uses` (per-request cap) and enable `caching` only past 3 calls. This does **not** replace hub spawning — it is the option for API-implemented steps. Contract + gotchas (encrypted `advisor_redacted_result` on Opus 5/Fable 5 advisors, history-stripping on cutoff) → `oracle/reference/advanced-tool-use.md` §4.

Codex hub: the hub runs **`gpt-5.6-sol`**; every spawned subagent runs the role-matched gpt-5.6 variant (sol=plan/design, terra=standard implementation, luna=rote — latest-generation mandate, `CODEX_ORCHESTRATION.md` C3.0; never a previous generation). Tune depth within a variant via `model_reasoning_effort` (`minimal|low|medium|high|xhigh`, default `medium` — re-verified 2026-07; start at the lowest acceptable effort, no exact 5.5→5.6 mapping). agy hub: mandated per ‡ above — not per-agent.


## Operational Notes for Spawns
- **Scoring:** use the discrete evidence bands and typed blocking-unknown gate in `confidence-scoring.md`; do not invent source weights or average away an unresolved Authority/Scope/Goal.
- **References:** load only files in the current Workflow phase row; structural rejection rules live with their owner (`routing-matrix.md`, `handoff-validation.md`, `guardrails.md`).
- **Output:** `_STEP_COMPLETE`/`NEXUS_HANDOFF` minimum is Summary + Status + Next; add Recommended/Optional fields by complexity per `_common/HANDOFF.md`.
- **State:** track Phase + Step at minimum; keep full `_NEXUS_STATE` for 4+ step chains.
- **Agent roles:** focus on the concrete task and output format, not personality adoption.
