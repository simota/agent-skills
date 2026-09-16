# CLI Compatibility Matrix

> **Tier:** `orchestration` — activates from the hub, a recipe, or on engine detection. Precedence: `_common/OPERATIONAL.md` § Contract Precedence.

Canonical runtime adaptation for this repository. **Documentation checked: 2026-09-17 (JST).** This is a dated compatibility snapshot, not evidence that a CLI, model, entitlement, or tool is installed in the current session. Verify the actual runtime before relying on it. Never infer a callable tool from a model's name.

The existing multi-engine baseline remains **Claude + Codex**; agy remains an optional PREFLIGHT participant under `_common/MULTI_ENGINE_RECIPE.md`. Stable vendor availability alone does not change that architecture. The older fixed-generation/model mandates are replaced by §4's capability- and authorization-based selection; scope, safety, and verification contracts remain unchanged.

## At-a-Glance

| Runtime | Official release snapshot | Execution-time check |
|---------|---------------------------|----------------------|
| Claude Code | 2.1.273, published 2026-09-15 | `claude --version`, available tools, `/model`, active permissions |
| Codex CLI | 0.154.0, published 2026-09-09 | `codex --version`, available tools and model picker, effective configuration |
| Antigravity CLI | CLI documentation identifies v1.2.0 | `agy --version`, `agy models`, `agy agents`, `agy --help` |
| Gemini CLI | Latest stable v0.60.0, published 2026-09-15 | `gemini --version`, `/model`, skill discovery; separate product from agy |
| Cursor CLI | Latest listed changelog entry 2026-08-26; no numeric release ID established here | `agent --version`, advertised tools, account model picker |

Claude Code, Codex CLI, and agy have repository installer targets. Gemini CLI and Cursor are documented secondary readers; do not invent installer targets or assume their native team APIs match the primary CLIs. A publication date is not an installed version or an automatic upgrade instruction.

## 1. Configuration File Paths

| Purpose | Claude Code | Codex CLI | agy |
|---------|-------------|-----------|-----|
| User settings | `~/.claude/settings.json` | `~/.codex/config.toml` | `~/.gemini/antigravity-cli/settings.json` |
| Project settings | `.claude/settings.json`; local overrides `.claude/settings.local.json` | `.codex/config.toml` in trusted projects | Verify active project settings with the installed CLI; do not copy Gemini CLI paths blindly |
| Project rules | `CLAUDE.md` plus the repository's explicit `AGENTS.md` linkage | `AGENTS.md` and applicable ancestor instructions | Verify loaded rules; apply this repository's `AGENTS.md` and agy-specific deltas |
| MCP | `.mcp.json` project; user/local MCP config in `~/.claude.json` | `[mcp_servers.<name>]` in `config.toml` | `~/.gemini/config/mcp_config.json`; project `.agents/mcp_config.json` |

Inspect only non-secret configuration needed for the task. Never recursively read auth stores, credentials, tokens, shell environments, or private global instructions merely to detect a runtime. Managed policy and enforced permissions cannot be overridden by a skill or AUTORUN mode.

## 2. Skill Placement & Discovery

| Reader | User-global skills | Project-local skills |
|--------|--------------------|----------------------|
| Claude Code | `~/.claude/skills/` | `.claude/skills/` |
| Codex CLI | `~/.agents/skills/` | `.agents/skills/` along the applicable repository path |
| agy | `~/.gemini/antigravity-cli/skills/` | `.agents/skills/` |
| Gemini CLI | `~/.gemini/skills/` or `~/.agents/skills/` alias | `.gemini/skills/` or `.agents/skills/` alias; the `.agents` alias wins within a tier |
| Cursor | `~/.cursor/skills/`; compatibility locations are also documented | `.agents/skills/` and documented compatibility locations such as `.claude/skills/` |

`~/.codex/skills/` is a **legacy installation location**, not the current Codex default. Keep existing user-owned files and unrelated links intact. Migrate only this repository's links deliberately; do not leave duplicate copies with the same skill names and assume they merge. Configuration still belongs under `~/.codex/`; configuration roots and skill roots are different.

Our portable frontmatter contract is exactly `name` and `description`, even when a vendor permits optional fields. Keep `CAPABILITIES_SUMMARY` in the body. Resolve references from the skill's own directory and preserve its `_common` symlink. Metadata discovery is not proof that body/reference imports executed.

The project-local `orbit`, `lore`, and `darwin` extensions remain distinct from global skills. Apply `_common/PROJECT_LOCAL_SKILLS.md`; an absent local extension uses its registered fallback, never an invented global path. Verify agy discovery of the repository's folder layout in the installed version; its documentation illustrates more than one packaging surface and a documented root alone is not a load test. Cursor cloud agents do not automatically inherit local global skills.

## 3. Agent Spawn Syntax

Use the host's **advertised** delegation tools and schemas. Names below identify interfaces to discover, not portable function signatures.

| Capability | Claude Code | Codex CLI | agy |
|------------|-------------|-----------|-----|
| Native specialist sessions | Agent tool / documented subagent configuration | Native subagent lifecycle tools | `agy agents` / `/agents`; discover the current subagent interface |
| Concurrent work | Independent background agents where supported | Concurrent native subagents; collect required results before joining | Advertised background subagents; headless processes only with isolated ownership and capture |
| Headless invocation | `claude -p` | `codex exec` | `agy -p` |
| Structured capture | `--output-format json` or `stream-json`; documented `--json-schema` | `--json` events; `--output-schema`; `-o` / `--output-last-message` final artifact | `--output-format json` or `stream-json`; `--json-schema` |

Discover lazily exposed tools before concluding they are unavailable. If the runtime has no discovery mechanism and no spawn capability, record that concrete limitation; never call an invented `wait_agent` or fabricate a specialist's response. Follow `nexus/reference/execution-layers.md` for a verified fallback.

Keep required skills and rules enabled in skill-execution tests: a minimal/bare CLI mode that disables them is not a valid cross-CLI skill test. Use an independent session for genuine verification; copying the producer's conclusion into another role does not create independence.

### Spawn Prompt Template (CLI-Agnostic)

```text
Read the resolved specialist SKILL.md and its applicable contracts.
Task: <requested result, scope, non-goals>
Evidence: <authoritative paths/revisions; only relevant context delta>
Authority: <owned write paths, permitted tools/effects, budget, escalation boundary>
Done when: <observable acceptance criteria and required validation>
Return: <artifact paths/revisions, findings, actual checks, unresolved items, status>
```

Do not append forced internal reasoning, a second copy of the specialist's methods, or model-specific compensation directives. Start independent branches together only after their inputs and ownership are ready; serialize shared state and join before integration.

## 4. Model Selection

| Provider / runtime | Current documented stable coding/general reasoning option | Availability caveat |
|--------------------|-----------------------------------------------------------|---------------------|
| Anthropic / Claude Code | Claude Fable 5.1, API ID `claude-fable-5-1`; Opus 5 and Sonnet 5 remain available options | Fable 5.1 requires Claude Code 2.1.257 or newer; provider gateways and account access can lag. The `fable` alias is not a universal exact-version pin |
| OpenAI / Codex CLI | GPT-6 Astra, `gpt-6-astra`, recommended in the current Codex model guide | Verify account/provider picker; an API listing is not proof of entitlement in every CLI surface |
| Google Gemini API | Gemini 3.8 Flash, `gemini-3.8-flash`, listed stable | Gemini 3.1 Pro is preview; restricted models and preview releases are not the stable default |
| Antigravity CLI | Gemini 3.8 Flash; documented runtime slug includes `gemini-3.8-flash-high` | Resolve actual slugs with `agy models`; do not pass a display label such as a bracketed “High” name as an API ID |
| Gemini CLI / Cursor | Select from the active account's documented model list | Do not copy another CLI's IDs, entitlements, or defaults into these runtimes |

Prefer the latest **stable, available, authorized** model that meets the task's capability and quality needs. Inherit a user's explicit model/effort selection. Change it only with applicable authorization; do not silently substitute an unavailable model, enable paid usage, or fall back to another provider to bypass a refusal or policy constraint. Record an unavailable required model as a limitation and name any explicitly allowed alternative.

Model identifiers belong here, not in SKILL.md role rules. Do not equate generations with exact behavior. Native tools, context capacity, compaction, structured output, and independent sessions must be verified separately. Larger context helps retain necessary evidence, but does not justify loading every reference.

Effort is a runtime setting, not an instruction to expose private reasoning. Use only values documented for the installed model/runtime; no universal low/medium/high mapping or mandatory maximum applies. For agy the current headless interface documents `--model <slug>` and `--effort low|medium|high`. For Codex and Claude, inspect the current configuration documentation and effective settings rather than copying an old enum. Benchmark on fixed tasks before asserting a cost/quality improvement.

## 5. Permission Models

Autonomy means finishing **within an existing grant**, not widening it. Keep least-privilege workspace, tool, network, spend, and external-effect boundaries. A recipe's AUTORUN flag does not authorize editing global settings or removing approval gates.

For headless work, arrange narrowly scoped permissions for required actions in an already authorized environment. On current agy, workspace file operations can run under normal policy while approval-only tool calls are **soft-denied** without a prompt. That may still produce exit code zero: inspect stderr, structured status, the actual tool result, and the requested artifact.

`--dangerously-skip-permissions` and analogous bypass flags are **not normal execution requirements**. Do not add them to fix a hang or denial. They require explicit authorization and verified external isolation, must never override a deny/security policy, and are not acceptable in production or an untrusted workspace. A flag named sandbox is not evidence that effects remain contained when bypass is enabled. Never auto-edit global allowlists, use a general interpreter allowance, or grant network access merely to avoid asking.

## 6. MCP Integration

Confirm the configured server is trusted, connected, and exposes the required tools before use. Follow `_common/SECURITY.md` for intake, hashes, and permission boundaries. Hash checks do not themselves create isolation.

### Cross-CLI MCP Authoring Rule

Use the installed client's documented schema, not a combined cross-client config. Claude's current remote entry uses a transport `type` and `url`; Codex uses a `[mcp_servers.<name>]` table; agy's current documentation requires `serverUrl` and says legacy `url` / `httpUrl` are unsupported. This differs from older release observations: verify the installed parser when migrating. Test connection and advertised tool schemas after an authorized edit. Never include real credential values in examples or reports.

## 7. Context Rules Files (Authority Order)

The host controls which files it loads; the repository defines the precedence of its own rules. Consult `AGENTS.md` and `_common/OPERATIONAL.md` for class precedence. Do not claim that a file name alone is universally auto-loaded or that a tool-specific delta can override security, legal, or architecture constraints.

### Recommended Authoring Pattern

Keep cross-tool rules in `AGENTS.md`; `CLAUDE.md` and any `GEMINI.md` contain necessary deltas or an explicit link to common rules. An eager import is deduplication, not progressive disclosure: imported bytes still occupy context. Preserve applicable nested instructions and project-local availability gates.

## 8. Slash Commands & Built-ins

Slash commands are user interfaces, not portable callable tools. Verify command names with the installed help before documenting or invoking them. In current agy, `/agents` manages agents, `/skills` manages skills, `/model` selects a model, and `/tasks` shows background tasks. Do not transplant a historical `/agent <name>` recipe into another CLI. Preview features, including agy's `/teamwork-preview` and Codex's experimental native worktree feature in 0.154.0, are optional—not prerequisites for ordinary skills.

## 9. Known Pitfalls (agy-specific)

Treat past runtime failures as **symptom-gated** diagnostics. Historical v1.0.x reports of non-TTY output loss, shell/PTY failures, quota errors, and premature subagent termination do not establish that current documented JSON output is broken. Conversely, current documentation does not prove every older issue fixed. Reproduce once in a harmless task before selecting a workaround; record version, platform, command shape, and observed failure.

### 9.1. Pre-flight Notification Protocol (canonical)

Before an authorized action expands permissions, uses an external paid service, or invokes a non-default risky execution path, state the affected scope and obtain any still-required approval. Previously granted specific authority need not be requested again. An informational notification is **not** consent to a new bypass flag. Normal read-only probes need no repeated ceremony.

### 9.2. agy Headless Output-Capture Protocol (canonical)

Prefer the documented structured channel. With an already authorized prompt and model selection, the basic capture shape is:

```sh
agy -p "$PROMPT" --output-format json > "$RESULT_JSON" 2> "$DIAGNOSTICS"
```

Check process status, parse the JSON object, inspect its `status`, select `structured_output` when a schema was requested or `response` otherwise, and validate the expected artifact/effect against the ACs. Check stderr for denied tools. Do not count a terminal response, usage total, or non-empty file as successful implementation.

If the installed version demonstrably loses/truncates output, use a unique scoped artifact file with a completeness marker and validate its current-run provenance, schema, and full content. Allocate a PTY only for a reproduced terminal requirement, not unconditionally. Keep the same permissions; a capture workaround never authorizes a bypass. Do not reuse a previous run's artifact or trust a stale sentinel. Resume only a verified matching conversation/repository state.

### 9.3. Codex CLI / Claude Code Headless Output Capture (canonical)

Prefer each CLI's documented structured/final-output channel from §3. Keep logs separate from the deliverable, wait for the actual terminal result, and bind checks to the artifact revision. A historical detached-session failure warrants a foreground retry only when reproduced; it is not a universal ban on supported background agents. Missing output is a failed/partial run, not an empty success. Repeated identical failures require diagnosis.

## 10. Skill Authoring Checklist (Cross-CLI)

Check portable frontmatter, direct spine delivery and local references, role/ownership boundaries, actual tool availability, least privilege, output parsing, model selection, and evidence-based completion. Run existing checks. For each accessible CLI, additionally smoke-test discovery, a read-only task, a scoped write plus validation, a denied effect, and a joined independent subtask. Record inaccessible runtimes as **not executed**, not PASS. Do not install or authenticate a provider as a hidden part of static validation.

## 11. Items Still Unverified (do not invent)

Local CLI versions, model/account entitlements, rollout defaults, native tool signatures, concurrency/depth limits, and plugin loading are runtime facts. The repository's static tests do not exercise live providers. Re-check agy folder-based discovery and historical capture symptoms in the actual installed environment. Do not assert that a CLI can use a model simply because its provider API lists it.

## 12. Source Tier

Primary documentation reviewed 2026-09-17 (JST); re-check these pages on a model/runtime upgrade or observed incompatibility:

- Anthropic: [models](https://platform.claude.com/docs/en/models/overview), [model configuration](https://code.claude.com/docs/en/model-config), [changelog](https://code.claude.com/docs/en/changelog), [skills](https://code.claude.com/docs/en/skills), [subagents](https://code.claude.com/docs/en/sub-agents), [MCP](https://code.claude.com/docs/en/mcp).
- OpenAI: [models](https://developers.openai.com/codex/models), [changelog](https://developers.openai.com/codex/changelog), [skills](https://developers.openai.com/codex/skills), [subagents](https://developers.openai.com/codex/subagents), [MCP](https://developers.openai.com/codex/mcp), [skill/prompt guidance](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra).
- Google: [Gemini model catalog](https://ai.google.dev/gemini-api/docs/models), [agy models](https://antigravity.google/docs/models/), [CLI reference](https://antigravity.google/docs/cli/reference), [headless interface](https://antigravity.google/docs/cli/headless/), [skills/plugins](https://antigravity.google/docs/cli/plugins/), [MCP](https://antigravity.google/docs/cli/mcp/).
- Secondary readers: [Gemini CLI latest stable](https://geminicli.com/docs/changelogs/latest/), [Gemini CLI skills](https://geminicli.com/docs/cli/skills/), [Cursor skills](https://cursor.com/docs/skills), [Cursor CLI changelog](https://cursor.com/docs/cli/changelog).

**Lifecycle:** failure: stale runtime facts become mandatory skill behavior; effect: one dated primary-source matrix plus explicit runtime checks, not live-provider certification; owner: compatibility maintainers; removal: replace only when a tested runtime adapter delivers equivalent discovery, permission, capture, and model-availability guarantees to all consumers.
