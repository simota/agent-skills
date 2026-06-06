# Hub-Engine Authoring

Per-engine authoring protocols that apply once the hub orchestrator is detected (see SKILL.md → **Execution Model → Orchestrator Detection**).

## Claude Code hub

Apply `_common/OPUS_48_AUTHORING.md` principles **P4 (parallel subagent triggers), P6 (effort-level awareness), P7 (delegation framing), P9 (effort-calibrated tool use)**.

Opus 4.8 spawns fewer subagents and reasons more by default, respects `effort` strictly, and follows instructions literally — explicit fan-out triggers, per-step model/effort selection, and explicit step scope are mandatory. Spawn prompts must state thinking nudges (P5) and length envelopes (P2).

## Codex CLI hub

Apply `_common/CODEX_ORCHESTRATION.md` principles **C1 (spawn-depth budget), C2 (synchronous fan-out/join), C6 (checkpoint-resume)**, plus C3/C7 for model and approval posture.

Codex has no background-spawn primitive (parallel = N `spawn_agent` → `wait_agent` all), gates fan-out via `agents.max_depth`, and routes effort by model choice (`gpt-5.5` plan / `gpt-5.4`-family execute) plus the `model_reasoning_effort` config key (`minimal|low|medium|high|xhigh`) — not by an Opus `effort` enum.

## agy hub

Best-effort; apply the C-principles by analogy under `_common/CLI_COMPATIBILITY.md §3, §9` constraints.

## Spawn Template Variants

**Claude Code (`Agent(...)`)** uses the canonical template in SKILL.md → **Agent Spawn Template**. The four directive fields (acceptance criteria / output length / tool-use / thinking) are not optional. Opus 4.8 calibrates output length to context, restrains tool calls by default (raise `effort` to increase tool use), and interprets each field literally, so both under- and over-shoot occur when these are implicit. For parallel spawns, issue multiple `Agent(... run_in_background: true)` calls in the same turn. Shared protocol: `_common/OPUS_48_AUTHORING.md`.

**Codex CLI variant**: same prompt body; resolve skill path to `~/.codex/skills/[agent]/SKILL.md` or `<repo>/.agents/skills/[agent]/SKILL.md`. Four directive fields stay required. Authoring follows `_common/CODEX_ORCHESTRATION.md` (C-principles), not the Opus note — effort routed by model choice (`gpt-5.5` plan / `gpt-5.4`-family execute, C3) + `model_reasoning_effort`; fan-out gated by `agents.max_depth` + `agents.max_threads` (C1). API patterns (L1 `spawn_agent`→`wait_agent`, L2 parallel-then-join, L3 `send_input`/`resume_agent`/`close_agent` for checkpoint-resume) → `reference/execution-layers.md` § Codex CLI.

**agy variant**: same prompt body; TUI via `/agent [agent]-[task-slug] "<body>"`, headless via `agy -p "<body>" --dangerously-skip-permissions`. Headless capture is **file-handoff, not stdout** — append the `_common/CLI_COMPATIBILITY.md §9.2` MANDATORY OUTPUT PROTOCOL (absolute-path artifact + `<<<END_OF_OUTPUT>>>` sentinel) and reference files via `@<path>`. Full silent-failure mitigations + verified template → `reference/execution-layers.md` § agy. Replace skill path with `~/.gemini/antigravity-cli/skills/[agent]/SKILL.md` or `<repo>/.agents/skills/[agent]/SKILL.md`.

## Execution-Layer Key Rules

- **Codex**: `spawn_agent` may be lazily hidden — attempt the call when prereqs hold ("tool not visible" ≠ "tool not callable"). Codex tools: `spawn_agent`, `send_input`, `wait_agent`, `resume_agent`, `close_agent`.
- **agy headless**: use `@<path>` to inject file context; mandate absolute-path artifact write + `<<<END_OF_OUTPUT>>>` sentinel — `agy -p` never flushes to non-TTY stdout (issue #115, unfixed v1.0.5). Pass `--print-timeout 15m` for heavy syntheses; `--log-file <path>` for quota/OAuth failure diagnosis.
- **agy Pre-flight Notification**: before the first `agy -p ... --dangerously-skip-permissions` spawn of a session, emit the notification per `_common/CLI_COMPATIBILITY.md §9.1`.
- **Permission model**: agy defaults to `request-review`; autonomous Nexus must switch to `proceed-in-sandbox` (TUI) or `--dangerously-skip-permissions` (headless). Never use `always-proceed` in production.

## Model Selection

Model names are hub-engine-specific. The role → tier mapping is stable; the concrete model per tier depends on the orchestrator engine.

| Agent Role | Tier | Claude Code hub | Codex CLI hub | Rationale |
|-----------|------|-----------------|---------------|-----------|
| Investigation / read-only (Scout, Lens, Trail) | balanced | sonnet | `gpt-5.4` | Cost-efficient |
| Standard implementation (Builder, Artisan, Radar) | balanced | sonnet | `gpt-5.4` | Balanced |
| High-complexity design (Sentinel, Atlas) | high-reasoning | opus | `gpt-5.5` | Precision-critical |
| Lightweight tasks (Quill, Morph) | fast | haiku | `gpt-5.4-mini` | Minimal cost |

Codex hub: route planning / high-complexity steps to `gpt-5.5` and execution steps to `gpt-5.4` / `gpt-5.4-mini` (Plan-and-Execute, `CODEX_ORCHESTRATION.md` C3); tune depth within a tier via `model_reasoning_effort` (`minimal|low|medium|high|xhigh`, default `medium` — verified 2026-06). Legacy IDs `gpt-5.1`/`gpt-5.1-codex-max`/`gpt-5.2`/`gpt-5.3-codex` are deprecated. agy hub: switch via `/model` in TUI (per-session, not per-agent).
