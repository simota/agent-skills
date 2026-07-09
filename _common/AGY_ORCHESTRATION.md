# agy (Antigravity CLI) Orchestration Authoring Protocol

> Counterpart to `_common/OPUS_48_AUTHORING.md` (Claude Code hub, P1–P11) and `_common/CODEX_ORCHESTRATION.md` (Codex CLI hub, C1–C9). **This file governs authoring when Antigravity CLI (`agy`) drives the Nexus hub.**
> Owner: Architect (canonical doc); referenced by orchestrators (Nexus, Orbit, Rally, Magi) and any SKILL.md whose spawn path can run on agy.
> Scope: agy as the **orchestrator engine** (the CLI running the top-level hub session). agy as a *worker / spawn target* of a Claude or Codex hub is covered by `_common/SUBAGENT.md` (MULTI_ENGINE) + `_common/MULTI_ENGINE_RECIPE.md`.
> Verified facts: `_common/CLI_COMPATIBILITY.md` (re-verified 2026-06-23 against agy v1.0.10). Items not yet confirmed against a T1 source are marked **未確認** and must not be speculatively completed.

Engine-selection rule for orchestrators:

| Orchestrator engine (hub) | Authoring protocol |
|---------------------------|--------------------|
| Claude Code | `_common/OPUS_48_AUTHORING.md` (P1–P11; + Fable 5 F-principles when the hub runs `claude-fable-5`) |
| Codex CLI | `_common/CODEX_ORCHESTRATION.md` (C1–C9) |
| **Antigravity (`agy`)** | **this file (A1–A9)** |

---

## Why This Exists

The Nexus stack was built Claude-Code-first (`Agent(...)` spawns, `sonnet/opus/haiku` tiers, `run_in_background` parallelism, Opus-4.8 effort levels). Codex needed its own protocol because it spawns differently and pins the latest model generation (role-based sol/terra/luna variants). **agy diverges even further from both**, and "apply the C-principles by analogy" (the old stub) under-serves it. The concrete gaps that change how you author and orchestrate:

1. **One mandated model, but a real effort dial.** agy is under a user mandate to run **Gemini 3.5 Flash** for every step and every spawned subagent (`_common/CLI_COMPATIBILITY.md §4 ‡`). Unlike Codex (latest *frontier* model), the mandated model is a **fast** model — so reasoning-heavy steps (plan/design/verify) need the **Flash effort tier (High)** dialed up, not a bigger model. This is the single most important authoring lever (A1).
2. **No reliable headless stdout.** `agy -p` never flushes to a non-TTY stdout (issues #76/#115, OPEN through v1.0.10) and requires a real pty. The deliverable channel is a prompt-mandated artifact file, always (A2).
3. **Model/tier is session-scoped, not per-agent.** There is no per-spawn `model:` parameter like Claude's `Agent(model=…)`. `/model` (TUI) or `agy --model` (headless) sets one model for the whole session (A3).
4. **No background-spawn primitive and no Rally-equivalent L3.** Parallelism is multiple TUI `/agent` invocations (async, polled via `/tasks`) or externally-orchestrated headless one-shots; deep ownership topologies must flatten (A4).
5. **agy-specific failure modes** — `@<path>` context injection (A5), the `--sandbox` + `--dangerously-skip-permissions` sandbox-escape (#36, A6), `GEMINI.md` authority + leak (A7).

When agy drives the hub, apply A1–A9 below instead of P- or C-principles. They are grounded in `_common/CLI_COMPATIBILITY.md`; the model-prompting levers (A8, A9) additionally draw on the official Gemini prompting / structured-output guidance at `ai.google.dev` (cite the version you verified).

---

## The Nine Principles

### A1. Single-Model Effort-Tier Routing  *(the core lever)*

The Plan-and-Execute cost principle is realized for agy **through the Flash effort tier, not through a cheaper or bigger model** — the model stays Gemini 3.5 Flash throughout (mandate, `§4 ‡`, **UNIVERSAL scope**: every agy invocation — hub, chain-step executor, *and* multi-engine diversity-spoke — never Pro/Claude/GPT-OSS/Deep Think). agy `/model` exposes **Gemini 3.5 Flash (High / Medium / Low)**: these map to the Gemini API **`thinking_level`** parameter (`minimal | low | medium | high`; `thinking_budget` is **deprecated**) — reasoning-effort tiers of the *same* Flash model, the agy analog of Codex `model_reasoning_effort` and Claude effort levels. [VERIFIED-T1, ai.google.dev/gemini-api/docs/whats-new-gemini-3.5, 2026-06.] ⚠ **Migration caution:** Gemini 3.5 Flash's default `thinking_level` is **`medium`** (it was `high` on the older `gemini-3-flash-preview`) — a routine step left at the default gets `medium`, not `high`. In multi-engine recipes the agy axis's divergence value comes from **Gemini model-priors + the High tier**, which is why the mandate does not cost the recipes their third-axis independence.

**Apply by:**
- **High** tier → planning, high-complexity design, arbitration, and every VERIFY/acceptance step (a fast model on hard reasoning must compensate with maximum thinking — see A9).
- **Medium** tier → standard implementation, investigation, review (default).
- **Low** tier → trivial/mechanical steps (rename, format, single-line edits).
- **Never** switch the *model* away from Gemini 3.5 Flash to Pro/Claude/GPT-OSS (mandate). Vary only the tier.
- **Tier-selection mechanism:** **verified** — persist the tier in `settings.json` `"model": "Gemini 3.5 Flash (High)"` (session default; T3 Antigravity Lab, 2026-06) or pick it in `/model` (TUI). **Unverified** — whether headless `agy -p` accepts the bracketed tier string as a `--model` argument (`agy --model "Gemini 3.5 Flash (High)"`) or a per-call flag; confirm with `agy models` on the target install. **Per-call headless tier switching is NOT confirmed**, so for a **mixed-effort headless chain** prefer setting the tier in `settings.json` for the dominant step class, or split the chain into separate runs each with its own `settings.json` tier (A3). If neither works on the install, pick the tier that fits the chain's *hardest* step.

### A2. File-Handoff Capture + Real PTY  *(agy-specific, non-negotiable for headless)*

`agy -p` is **not** a stdout tool. From a socket-stdin / no-controlling-terminal shell (Claude Code `Bash`, CI, cron) it hangs to `exit 124` with no output, and even when it runs it never flushes the response to a non-TTY stdout (issues #76 non-TTY/subprocess + #115 Windows/`text_drip`, both OPEN through v1.0.10). `exit 0 + empty stdout` is also what a *successful* run looks like.

**Apply by:**
- Give agy a **real pty** via `python3 -c 'import pty; pty.spawn([...])'` — `script -q /dev/null agy …` fails (`tcgetattr/ioctl: Operation not supported on socket`) from socket-stdin shells.
- Make the deliverable a **prompt-mandated absolute-path artifact + `<<<END_OF_OUTPUT>>>` sentinel**, then run the verification chain (artifact non-empty + sentinel → transcript-harvest fallback → `--log-file` grep → RUNTIME-BROKEN). Canonical block + typed-retry rule: `_common/CLI_COMPATIBILITY.md §9.2`.
- Pass `--print-timeout 15m` (or larger) for heavy multi-file syntheses; `--log-file <path>` for quota/OAuth diagnosis.

### A3. Session-Scoped Model/Tier — No Per-Agent Switch

There is no per-spawn `model:` parameter. `/model` (TUI) and `agy --model` (headless, v1.0.5+) set one model+tier for the *whole session*. A chain that wants High for its plan step and Low for its cleanup step cannot switch mid-session inside one TUI session.

**Apply by:**
- For a **mixed-effort chain**, prefer **separate headless `agy -p` invocations per step**, each pinning its own tier (A1), orchestrated externally by the hub — not one long TUI session.
- For a **single TUI session**, pick the tier that fits the chain's *hardest* step and accept it for the rest, or split the chain at the tier boundary.
- Design recipes so model/tier is chosen at the **chain level**, never assumed switchable per agent (the Claude `Agent(model=…)` pattern does not port).

### A4. Spawn Topology & Fan-Out

agy has **no background-spawn primitive** and **no documented Rally-equivalent** for L3. Subagent depth/concurrency has **no config key** (confirmed-absent 2026-06-23 — runtime/budget-gated, not `agents.max_depth`-style). Spawn surfaces: TUI `/agent <slug> "<task>"` (async, each its own context, polled via `/tasks`) or headless `agy -p` one-shots.

**Apply by:**
- **L1 sequential:** TUI `/agent` or a single headless `agy -p` per step.
- **L2 parallel (2–3 branches):** multiple TUI `/agent` invocations (async; aggregate via `/tasks` — no explicit `wait` primitive) **or** multiple externally-launched headless `agy -p` processes joined by the hub. Hub-spoke ownership still holds: no shared mutable state between concurrent branches.
- **L3 (4+ workers / complex ownership):** **flatten** — there is no Rally to delegate to. Either drive the fan-out directly from the hub in waves, or use a community team pack (`oh-my-antigravity` `/oma:taskboard`) if installed. Log the absence honestly; do not claim a Rally spawn on agy.
- **Subagent context is ISOLATED.** agy subagents each get their own context window and do **not** inherit the parent's full history — pass the task description + only the needed state delta, and **share intermediate results via filesystem artifacts (JSON/CSV)**, the community-recommended handoff (composes with the A2 artifact protocol). Whether a subagent inherits the parent's model/tier is **未確認** — do not assume; the Flash mandate applies to subagents regardless.
- **Session controls:** `/fork` branches the current conversation into a separate workspace (use before risky/destructive trials so the main session stays clean); `/planning` = multi-turn plan mode, `/fast` = skip planning and execute directly (treat `/planning` as built-in-vs-plugin **未確認** — use conservatively).
- **Checkpoint-resume (4+ step chains):** headless resume via `-c` / `--conversation <id>` is **usable since v1.0.8** (the prior transcript-dump bug was fixed) — resume a session instead of re-spawning to preserve context and budget.
- Internal-fallback log form when `/agent` is unavailable: `"/agent slash command unavailable (reason: <not in TUI main session | toolNames does not permit | headless mode>)"` — **never** "spawn_agent not found" (`spawn_agent` is a Codex tool, not agy).

### A5. @-Path Context Injection

agy treats a bare path string (`docs/foo.md`) as literal text and delegates the file read to an internal subagent that dies at the 60s cap (v1.0.2 restricted the timeout to subagents) — a silent `exit 0 + empty` failure.

**Apply by:**
- **Always reference files with `@<path>`** (`Compare @docs/a.md and @docs/b.md …`) so context loads into the main agent directly.
- For unavoidable large delegated reads, split into multiple smaller `agy -p` calls rather than one big delegated read.

### A6. Sandbox / Permission Posture

agy defaults to `request-review` (pause for approval). Headless autonomy needs `--dangerously-skip-permissions` because `-p` cannot answer interactive review prompts. **But `--dangerously-skip-permissions` is not a no-op in `-p` (issue #36): it auto-approves the agent's `bypassSandbox` escape, so combining it with `--sandbox` silently defeats the sandbox** and allows out-of-workspace writes.

**Apply by:**
- AUTORUN headless → `agy -p … --dangerously-skip-permissions`, and **never add `--sandbox`** to that spawn. Contain via **host-level isolation** (ephemeral dev VM / CI runner / authorized workspace), not agy's `--sandbox`.
- Emit the **Pre-flight Notification** (`_common/CLI_COMPATIBILITY.md §9.1`) before the first `--dangerously-skip-permissions` spawn of a session (informational; fires even in AUTORUN).
- TUI autonomy → `proceed-in-sandbox`. Never `always-proceed` in production. `request-review` is reported occasionally ignored for file edits — treat as runtime risk.

### A7. GEMINI.md / AGENTS.md Authority

agy reads `AGENTS.md` (cross-tool, native since v1.20.3) and `GEMINI.md` (agy-specific override) — **not** `CLAUDE.md`. On conflict, `GEMINI.md` > `AGENTS.md`. Output language, commit conventions, and naming come from there.

**Apply by:**
- Resolve output-language and convention directives from `AGENTS.md` (+ `GEMINI.md`), not a `CLAUDE.md` assumption.
- Keep cross-tool rules in `AGENTS.md`; keep `GEMINI.md` minimal — `~/.gemini/GEMINI.md` is hardcode-leaked across Antigravity IDE + Gemini CLI (issue #16058), so scope it to agy-only overrides.

### A8. Structured Output via Artifact + Gemini JSON Discipline

`agy --output-format json` is **UNRELIABLE through v1.0.10** ("flag not defined" on some installs, no documented schema) and there is **no `-o` artifact flag**. Do not depend on either for capture.

The Gemini API *itself* supports hard structured output (`responseMimeType: "application/json"` + `responseSchema`, JSON-Schema subset with `anyOf`/`$ref`, key-order preserved since 2.5) [VERIFIED-T1, ai.google.dev/gemini-api/docs/structured-output] — **but `agy -p` does not reliably surface it**, so via agy you get *best-effort prompt-driven JSON*, not API-enforced JSON.

**Apply by:**
- Request structured output **inside the §9.2 artifact file**: "write a single JSON object to `/tmp/agy-<slug>.json`, then the sentinel on its own final line."
- Use the **schema-first prompt pattern** Gemini rewards: state the exact JSON shape (keys + enum values), give **one example object**, and add the negative constraint **"Return valid JSON only — do not include markdown fences."** One example resolves nearly all output-format ambiguity on Gemini 3.5.
- Keep the schema small and unambiguous (deeply-nested / very large schemas are rejected even at the API level); ambiguous fields are a top cause of malformed output.
- **Always validate the JSON parses before aggregating** (best-effort, not enforced). For a step that genuinely needs *guaranteed* schema conformance, call the Gemini API directly with `responseSchema` rather than routing through `agy -p`.

### A9. Fast-Model Autonomy & Compensation

Gemini 3.5 Flash is a *fast* model running reasoning-heavy orchestration work under the mandate. Quality is recovered through **prompt structure, decomposition, effort tier, and verification gates** — not a bigger model.

**Apply by:**
- **Compensate hard steps with the High effort tier (A1) + tighter decomposition.** Prefer more, smaller, well-scoped steps over one large under-specified step; a fast model degrades faster on ambiguous mega-prompts than a frontier model does.
- **Lean on explicit, structured, literal prompts.** Use the four-section frame Gemini rewards — **Objective / Constraints / Output / Success criteria** — with a short role line. Gemini 3.5 follows instructions *literally* (like Opus) — make implicit expectations explicit and add **negative constraints** ("do not guess", "do not call external APIs without confirmation") to suppress hallucination/over-reach. Top-load instructions in normal prompts; **when injecting a large data/context block, place the instructions AFTER the data** and anchor with "Based on the preceding information…" (Gemini handles instruction-last better for big contexts).
- **Strengthen VERIFY gates.** Because the generator runs fast, weight the recipe's VERIFY/acceptance step (run tests/lint/types, check behavior against ACs) and run it at the **High** tier. Pair quantitative checks with the recipe's own gate.
- **Self-driving directives** (headless run-to-completion): include a persistence directive ("keep going until fully resolved; don't hand back at the first uncertainty — deduce the most reasonable approach and continue") and a **completion oracle** ("Done when …" + self-validation loop). agy has **no confirmed `/goal` command** (not in the published slash-command list) — implement run-to-completion as external loop + headless `agy -p`, not an assumed `/goal`.
- **Gemini-specific prompt do/don'ts** [VERIFIED-T1/T3, ai.google.dev/gemini-api/docs/function-calling + Gemini 3.5 dev guides, 2026-06]:
  - **DON'T write chain-of-thought instructions** ("think step by step"). On Gemini 3.5, raise the **`thinking_level` (High tier)** instead — native reasoning replaces prompt-engineered CoT.
  - **DON'T set `temperature` / `top_p` / `top_k`.** Gemini 3.x degrades (looping) when these are moved off default; leave them unset.
  - **DO cap tool use** with an explicit budget line — "You have a limited action budget of N tool calls; use them efficiently." Active tool sets work best at ≤ 10–20 tools.
  - **DO check `finishReason` / validate every tool call** — Gemini agentic tool-calling misfires a non-trivial fraction of the time; build retry+validate into the harness, never ignore a failed call.
- **Long-context discipline.** Gemini 3.5 Flash = 1,048,576-token input / 65,536 output, but effective accuracy degrades past ~128k ("lost in the middle"). For handoffs > ~128k, **summarize or segment before the next spawn** rather than dumping the full context; label multiple sources with numbered headers ("Document 1", "Document 2"). Do not design single-shot processing that assumes the full 1M window is reliably usable.

---

## Per-Role Apply Matrix

| Role | Critical (◎) | Recommended (○) |
|------|---|---|
| Orchestrators (Nexus, Orbit, Rally, Magi, Titan, Sherpa) | A1, A2, A3, A4, A6 | A8, A9 |
| Builders / executors (Builder, Artisan, Forge, Native) spawned by an agy hub | A2, A5, A9 | A1, A8 |
| Investigators / reviewers spawned by an agy hub | A2, A5 | A1, A9 |
| Knowledge/Meta (Lore, Compass, Architect) authoring for agy hubs | A1, A7 | A4, A9 |

(◎ = address explicitly in SKILL.md; ○ = address if relevant)

A6 (sandbox posture) + A7 (GEMINI.md authority) apply to **every** role authored for an agy hub.

---

## Validation Hooks

When validating a skill's agy-orchestrator path (Architect validation):

- R-A1 Model stays Gemini 3.5 Flash (mandate); effort varied by tier (High plan/design/verify, Medium standard, Low trivial), never by model swap
- R-A2 Headless capture is file-handoff + real pty (`python3 pty.spawn`), not stdout; verification chain present (§9.2)
- R-A3 Model/tier chosen at chain level; no per-agent `model:` assumption; mixed-effort chains split into per-step headless invocations
- R-A4 Parallel = multiple `/agent` or external headless one-shots (no background primitive); L3 flattened (no Rally claim); resume via `-c`/`--conversation` for 4+ steps
- R-A5 File refs use `@<path>`; no bare-path delegated reads
- R-A6 `--dangerously-skip-permissions` for headless autonomy, **never with `--sandbox`** (#36); host isolation; §9.1 Pre-flight emitted
- R-A7 Rules resolved from `AGENTS.md` + `GEMINI.md` (not `CLAUDE.md`); `GEMINI.md` kept minimal (#16058)
- R-A8 Structured output via artifact JSON (not `--output-format json`/`-o`); explicit small schema in prompt
- R-A9 Fast-model compensation: High tier + decomposition on hard steps, strengthened VERIFY, explicit/literal/top-loaded prompts, persistence + completion-oracle for self-driving (no assumed `/goal`)

Pass criterion: address all `◎` principles for the role; aim for ≥ 7/9 total.

---

## How to Reference This File

In a SKILL.md:

```markdown
- Author for the active orchestrator engine. Claude Code hub → `_common/OPUS_48_AUTHORING.md`;
  Codex CLI hub → `_common/CODEX_ORCHESTRATION.md`; agy hub → `_common/AGY_ORCHESTRATION.md`
  (apply A[X], A[Y] for this role).
```

Cite by ID (A1–A9); let this file be the single source of truth. Do not duplicate principle text into individual SKILL.md files.
