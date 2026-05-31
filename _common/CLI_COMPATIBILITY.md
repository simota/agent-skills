# CLI Compatibility Matrix

Cross-CLI compatibility reference for Claude Code / Codex CLI / Antigravity CLI (`agy`). SKILL.md authors consult this file before assuming any specific CLI's API, configuration path, or spawn syntax.

> **Date stamps**: As of 2026-05. Antigravity CLI (`agy`) launched 2026-05-19 (Google I/O 2026); Gemini CLI personal-tier service stops 2026-06-18. Re-verify against current docs before relying on any "未確認" item.

> **Engine selection policy (2026-05 update)**: The default baseline for multi-engine recipes is **Claude + Codex (dual-engine)**. agy is an **optional addon** used only when available at PREFLIGHT — never a hard prerequisite. Reason: agy v1.0.x exhibits frequent silent runtime failures (quota, OAuth, executor errors, subagent timeouts — see §9). For canonical policy + tag conventions, see `_common/MULTI_ENGINE_RECIPE.md §Base Engine Policy`.

---

## At-a-Glance

| Aspect | Claude Code | Codex CLI | Antigravity CLI (`agy`) |
|--------|-------------|-----------|------------------------|
| Vendor | Anthropic | OpenAI | Google |
| Binary | `claude` | `codex` | `agy` |
| Successor of | — | — | Gemini CLI (2026-06-18 cutover) |
| Primary config dir | `~/.claude/` | `~/.codex/` | `~/.gemini/antigravity-cli/` |
| Cross-tool rules file (read) | `CLAUDE.md` (native), `AGENTS.md` (also read) | `AGENTS.md` (native) | `AGENTS.md` (native, since v1.20.3 / 2026-03-05), `GEMINI.md` (Antigravity-specific overrides) |
| Spec authority | platform.claude.com / docs.claude.com | platform.openai.com / `~/.codex/` docs | antigravity.google/docs, geminicli.com/docs (transitional) |

---

## 1. Configuration File Paths

| Purpose | Claude Code | Codex CLI | agy |
|---------|-------------|-----------|-----|
| User-global settings | `~/.claude/settings.json` | `~/.codex/config.toml` | `~/.gemini/antigravity-cli/settings.json` |
| Project settings | `<repo>/.claude/settings.json` | `<repo>/.codex/config.toml` | `<repo>/.gemini/settings.json` |
| Local override | `<repo>/.claude/settings.local.json` | (per-project config.toml layered) | (未確認 — community reports project layering, no explicit "local" tier documented) |
| Managed policy | `~/.claude/managed-settings.json` + `managed-settings.d/` | (未確認) | (未確認) |
| Skill instructions (cross-tool) | `CLAUDE.md` + `AGENTS.md` | `AGENTS.md` | `AGENTS.md` + `GEMINI.md` |
| MCP server config | inline in `settings.json` (`mcpServers` key) | (未確認 — Codex MCP integration evolving) | **`mcp_config.json` (independent file)** |
| Custom slash commands | `~/.claude/commands/<name>.md` | (未確認) | `~/.gemini/commands/<name>.toml` (Gemini CLI legacy; agy migration path 未確認) |
| Hooks | `settings.json` `hooks` key (PreToolUse/PostToolUse/etc.) | (未確認) | JSON hooks (lifecycle moments — same format as Antigravity IDE 2.0; PreToolUse/PostToolUse-equivalent) |

> **Rule conflict resolution (agy)**: `GEMINI.md` > `AGENTS.md` when both exist. Source: agentpedia AGENTS.md guide.

---

## 2. Skill Placement & Discovery

| Tier | Claude Code | Codex CLI | agy |
|------|-------------|-----------|-----|
| Global skills | `~/.claude/skills/` | `~/.codex/skills/` (未確認) | `~/.gemini/antigravity-cli/skills/` |
| Workspace skills (preferred) | `<repo>/.claude/skills/` | `<repo>/.agents/skills/` | `<repo>/.agents/skills/` |
| Skill file format | `SKILL.md` (frontmatter: `name`, `description`) | `SKILL.md` (same spec) | `SKILL.md` (same spec) |
| Progressive disclosure | description-based | description-based | description-based (community reports description-driven matching; tool-bloat risk if vague) |
| Install command | manual file copy / `claude` plugin marketplace | (未確認) | `agy plugin install <url>` / `npx skills add <repo> -a antigravity` / `npx antigravity-awesome-skills --antigravity` |
| Cross-tool registry | — | — | [`sickn33/antigravity-awesome-skills`](https://github.com/sickn33/antigravity-awesome-skills) (1,400+ skills, Antigravity / Claude Code / Cursor / Codex CLI / Gemini CLI cross-indexed) |

> **Authoring guidance**: A SKILL.md targeting multiple CLIs should keep frontmatter to `name` + `description` only (the official Agent Skills spec; Chain rejects custom keys). CLI-specific behavior goes in the Markdown body, gated by a `## Compatibility` section.

---

## 3. Agent Spawn Syntax

| Layer | Claude Code | Codex CLI | agy |
|-------|-------------|-----------|-----|
| L1 (sequential 1-4 step chain) | `Agent(prompt, mode: bypassPermissions)` foreground tool | `spawn_agent(prompt)` → `wait_agent(id)` | `/agent <name> "<task>"` inside TUI (asynchronous subagent) **or** `agy -p "<prompt>" --dangerously-skip-permissions` one-shot non-interactive (flag required — headless cannot answer `request-review` prompts) |
| L2 (parallel 2-3 branches) | multiple `Agent(..., run_in_background: true)` calls in one turn | multiple `spawn_agent` → `wait_agent` all | multiple `/agent` invocations in TUI (each runs in its own context window asynchronously) |
| L3 (4+ workers, complex ownership) | spawn Rally as Agent | `spawn_agent` with Rally prompt | (未確認 — no published Rally-equivalent; community packs like `oh-my-antigravity` use role-driven team patterns with `/oma:taskboard` priority queues) |
| Subagent control tools | `Agent` (foreground/background), TeammateTool (peer-to-peer SDK) | `spawn_agent`, `send_input`, `wait_agent`, `resume_agent`, `close_agent` | `/agent <name>`, `/tasks`, `/resume`, `/rewind`, `/btw` (read-only side question) |
| Nesting / depth control | (config-driven; see Claude Agent SDK) | `agents.max_depth` (default 1; explicit config key) | **(未確認)** — community guidance says "cap subagent depth" but no documented JSON/TOML key was found; treat as a runtime/budget concern instead of a config knob |
| Long-running goal mode | `/goal` (Claude Code v2.1.139+) | `[features] goals = true` (experimental) | `/goal <task>` (run to completion without plan-approval pauses; experimental flag status 未確認) |
| Headless / one-shot | `claude -p` | `codex exec` | `agy -p`, `--dangerously-skip-permissions` (mandatory for non-interactive use — bypasses default `request-review` permission gate; treat as `bypassPermissions` equivalent and restrict to sandboxed/CI/authorized-dev contexts), `--output-format json` (hidden flag — not in `agy --help` v1.0.2 but confirmed by official DEV.to examples). File references inside the prompt **must** use `@<path>` syntax — bare path strings trigger silent subagent timeouts (see §9 Known Pitfalls). |

> ⚠ **Naming collision**: `spawn_agent` is a Codex CLI built-in tool name. `khanhbkqt/spawn-agent` is a community Antigravity skill that delegates to other engines — they are not the same thing.

### Spawn Prompt Template (CLI-Agnostic)

```
You are the <AgentName> agent.
First, read <skills_root>/<agent>/SKILL.md and follow its instructions.

Recipe: <recipe-name or auto>
Task: <task_description>
Context from previous step: <handoff_context>
Constraints: <constraints>
Acceptance criteria: <front-loaded criteria>
Output length envelope: <length_envelope>
Tool-use directive: <tool_use_directive>
Thinking directive: <thinking_directive>

On completion, emit _STEP_COMPLETE with Agent / Status / Output / Next.
```

Per-CLI delivery:
- **Claude Code**: pass as `prompt:` to `Agent(...)` with `subagent_type: general-purpose`, `mode: bypassPermissions`, model `sonnet|opus|haiku`.
- **Codex CLI**: pass as the `prompt` argument of `spawn_agent`; wait with `wait_agent(id)`; resolve `<skills_root>` from `~/.codex/skills/` or `<repo>/.agents/skills/`.
- **agy**: paste into a `/agent <slug> "<prompt>"` invocation, or supply via `agy -p "<prompt>" --dangerously-skip-permissions --output-format json` for machine-readable non-interactive result. The skip-permissions flag is mandatory in headless mode because `request-review` cannot be answered there. `--output-format json` is a hidden flag — absent from `agy --help` v1.0.2 but confirmed in official DEV.to examples; safe to use. Always reference files with `@<path>` (e.g. `@docs/spec.md`) so the main agent ingests context directly — without `@`, agy delegates file reads to a subagent that hits the 60s timeout and silently exits. `<skills_root>` is `~/.gemini/antigravity-cli/skills/` or `<repo>/.agents/skills/`.

---

## 4. Model Selection

Direct model names are CLI-specific. Authoring tip: write SKILL.md with role names (e.g. `high-reasoning`, `balanced`, `fast`) and let the orchestrator map.

| Role | Claude Code | Codex CLI | agy |
|------|-------------|-----------|-----|
| Default / balanced | `sonnet` (claude-sonnet-4-6) | `gpt-5.1` (or current default) | Gemini 3.5 Flash (High/Medium) |
| High-reasoning / precision | `opus` (claude-opus-4-7) | `gpt-5.1-codex-max` (reasoning) | Gemini 3.1 Pro (High/Low), Claude Sonnet 4.6 (Thinking), Claude Opus 4.6 (Thinking) |
| Fast / cheap | `haiku` (claude-haiku-4-5) | (lighter variants per docs) | Gemini 3.5 Flash (Medium), GPT-OSS 120B (Medium) |
| Switching command | per-Agent `model:` parameter | per-`spawn_agent` (未確認) | `/model` inside TUI |

> agy explicitly lists Claude Sonnet 4.6 / Opus 4.6 (Thinking) and GPT-OSS 120B in `/model`. Source: Medium "Getting Started" + tutorial series (2026-05).

> **Codex-as-orchestrator effort routing**: when Codex CLI drives the hub, apply Plan-and-Execute by **model choice** — planning / high-complexity steps → `gpt-5.1-codex-max`, execution steps → `gpt-5.1`. The exact Codex reasoning-effort config key name and its level names are **未確認**; do not invent an effort enum. Full Codex-hub authoring protocol: `_common/CODEX_ORCHESTRATION.md` (C3).

---

## 5. Permission Models

| Tier | Claude Code | Codex CLI | agy |
|------|-------------|-----------|-----|
| Default mode | permissions evaluated `deny → ask → allow` (first match wins) | sandbox-on by default, `--full-auto` opt-in | **`request-review`** (collaborative — pause before terminal / file / external-service ops) |
| Confirm-each | (interactive permission prompts) | (per-action approval) | `request-review` |
| Sandboxed auto | `bypassPermissions` mode (within container/agent) | `--full-auto` | **`proceed-in-sandbox`** (isolated container, no prompts) |
| Fully autonomous | (bypassPermissions, audit hooks recommended) | `--dangerously-bypass-approvals-and-sandbox` (do not use in prod) | **`always-proceed`** (host machine, no prompts — production-forbidden) |
| Read-only | hooks/permission deny on write tools | (未確認) | **`strict`** (read-only; all non-read ops require approval) |
| Policy semantics | Hooks can **tighten** (deny) but cannot **loosen** past `settings.json` deny rules. PreToolUse `permissionDecision: "deny"` survives even `bypassPermissions`. | (未確認 — settings precedence documented in `~/.codex/config.toml` reference) | Permission Lists are `action(target)` strings, Allow / Deny / Ask. Positive security model: forbidden unless expressly permitted. |

> **agy known bug**: `request-review` is reported as occasionally ignored for file edits (forum: missing features). Treat this as a runtime risk, not a configuration issue.

---

## 6. MCP Integration

| Aspect | Claude Code | Codex CLI | agy |
|--------|-------------|-----------|-----|
| Config location | inline in `settings.json` (`mcpServers`) | (未確認) | **`mcp_config.json`** (independent file) |
| Remote MCP URL field | `url` | (未確認) | **`serverUrl`** — silent failure if `url` is copied across from Claude Code config |
| Transport | HTTP (OAuth 2.1 + PKCE required), stdio | (未確認) | HTTP (per spec inheritance from MCP standard) |
| Tool description pinning | community-recommended SHA-256 hash + diff (no built-in) | (未確認) | community-recommended SHA-256 hash + diff (no built-in); audit via `chain` skill |
| RFC 8707 resource indicators | required for OAuth (MCP spec 2026-03-15) | (未確認) | required (spec applies regardless of CLI) |
| Plugin/extension migration | — | — | `agy plugin import gemini` (extensions / model prefs / auth — but **not custom themes**) |

### Cross-CLI MCP Authoring Rule

When a skill consumes an MCP server, declare the server name + required tool set in the SKILL.md body (not in frontmatter), and document **both** field names (`url` and `serverUrl`) in setup snippets so users on either CLI can copy the right one.

---

## 7. Context Rules Files (Authority Order)

| File | Read by | Role |
|------|---------|------|
| `~/.claude/CLAUDE.md` | Claude Code (global) | User's private global instructions for Claude Code |
| `<repo>/CLAUDE.md` | Claude Code (project) | Project-level Claude Code rules |
| `~/.gemini/AGENTS.md` | agy (global) | Cross-tool global rules also readable by Cursor / Claude Code |
| `<repo>/AGENTS.md` | agy / Claude Code / Cursor (project) | **Cross-tool standard** — recommended single source of truth |
| `~/.gemini/GEMINI.md` | agy (global) | agy-specific overrides; **wins against `AGENTS.md`** on conflict (per agentpedia) |
| `<repo>/GEMINI.md` | agy (project) | Same precedence |
| `~/.codex/AGENTS.md` | Codex CLI (global) | Codex-native rules file |

> ⚠ **Issue #16058 leak**: Both Antigravity IDE and Gemini CLI hardcode `~/.gemini/GEMINI.md`. Keep that file scoped to *only* Antigravity-specific overrides to avoid rule leaks into other tools.

### Recommended Authoring Pattern

1. Put **cross-tool common rules** (commit conventions, naming, language policy) in `AGENTS.md` at the repo root.
2. Keep tool-specific overrides minimal:
   - `CLAUDE.md` → only what's unique to Claude Code (hooks, agent SDK, slash commands).
   - `GEMINI.md` → only what's unique to agy (`/agent`, `/goal` modes, `serverUrl` MCP).
3. Use `@file.md` imports inside `GEMINI.md` to reference shared sections for progressive disclosure (≤200 lines recommended, ≤300 absolute ceiling).

---

## 8. Slash Commands & Built-ins

| Command | Claude Code | Codex CLI | agy |
|---------|-------------|-----------|-----|
| Help | `/help` | `/help` | `/help`, `?` (34-command list per Medium tutorial) |
| Config | `/config` | (未確認) | `/config`, `/settings` |
| Permissions | (in settings.json) | (未確認) | `/permissions` |
| Model switch | (per-Agent) | (per-session) | `/model` |
| Usage / quota | `/cost` (legacy `/usage`) | (未確認) | `/usage`, `/quota` (**not live-updated — quit & reload required**, per forum report) |
| Resume / rewind | `/resume` | (未確認) | `/resume`, `/rewind` |
| MCP management | `/mcp` | (未確認) | `/mcp` |
| Tasks / scheduling | TaskCreate/TaskUpdate (tools) | (未確認) | `/tasks`, `/schedule` |
| Inline shell | `!` prefix | `!` (未確認) | `!command` (TUI-inline shell) |
| File attach | `@path` | `@path` | `@filename` |
| Side question (read-only) | — | — | `/btw` |
| Inspect loaded rules/skills | — | — | `agy inspect` |
| One-shot | `claude -p` | `codex exec` | `agy -p --dangerously-skip-permissions --output-format json` (use `@<path>` for files) |
| Structured output | `--output-format json` (未確認 globally) | (未確認) | `--output-format json` |

---

## 9. Known Pitfalls (agy-specific)

Surface these in any skill that targets agy. Each is sourced from the official Google Developers Forum (`discuss.ai.google.dev`) — treat as production-relevant.

| Pitfall | Impact | Mitigation in skills |
|---------|--------|----------------------|
| `agy` binary not documented in official docs (2026-05) | Onboarding friction | Include `agy --version` smoke step in `Quick Start` |
| WSL authentication state not persisted | Re-auth every session | Detect WSL in setup; document repair recipe |
| WSL launcher / scripts missing | Manual repair required | Same |
| `/usage` not updating live (only on `/quit` & reload) | Long tasks hit quota cliff mid-run | For >20 min tasks, prefer `agy -p` one-shot + cron/loop trigger |
| `AI Credit Overages` setting ignored from CLI | Billing surprises | Note in skill output requirements |
| `request-review` occasionally ignored for file edits | Security model breach | Set `proceed-in-sandbox` as the recommended default for skills that auto-edit |
| Mode selection (`build` / `plan` / `auto-accept`) absent | UX regression vs Gemini CLI | Document workarounds; skill should not assume modes exist |
| `~/.gemini/GEMINI.md` rule leak (Issue #16058) | Cross-tool config pollution | Keep `GEMINI.md` minimal; prefer `AGENTS.md` |
| MCP `url` → `serverUrl` rename | Silent connection failure | Always document `serverUrl` in MCP setup snippets |
| Skill description vague → tool bloat | 40-50K token overhead | Keep `description:` ≤2 sentences with explicit trigger keywords |
| `agy plugin import gemini` does not migrate custom themes | Cosmetic regression | Note in migration guides |
| **Bare file paths in prompts trigger silent subagent timeouts** | Headless `agy -p` exits with `exit 0` + empty stdout when given paths without `@`; main agent delegates file reads to a subagent that dies at the 60s cap (v1.0.2 changelog: "restricted the default 60-second interaction timeout specifically to subagents") | **Always use `@<path>` syntax** to inject file context into the main agent; combine with `--log-file` + post-run grep per `_common/MULTI_ENGINE_RECIPE.md §3.5` |
| **`--output-format json` absent from `agy --help` v1.0.2** | Flag appears unsupported via help text but is documented in official DEV.to examples (`agy -p "..." --output-format json`) | Treat as a hidden but supported flag; still pin schema in the prompt body as defense against future schema drift |
| **`--print-timeout` default 5min on heavy reviews** | Long multi-file syntheses may exceed default; main agent (not subagent) terminates | Pass `--print-timeout 15m` or larger for documents >1000 lines or multi-file comparisons |
| **`linuxcommandlibrary` man page is for the Antigravity IDE GUI launcher**, not the CLI | Flags like `--new-window`, `--reuse-window`, `-g` are IDE-only and will fail with the CLI | Source CLI flags only from `agy --help`, official DEV.to articles, and `google-antigravity/antigravity-cli`; ignore `michaelw9999/antigravity-cli` (unofficial fork) |
| **`agy --dangerously-skip-permissions` spawned as a Claude Code subagent (via Bash) creates an autonomous agent loop that bypasses Claude Code's approval gate** | Safety-judged unsafe: a long-running agy session can issue arbitrary tool calls (file writes, shell, MCP) with no human gate on the agy side and no per-call gate on the Claude Code side either | **Mandatory Pre-flight Notification** — see §9.1 below. Before the first `agy -p ... --dangerously-skip-permissions` of a session (or whenever the allowlist is not yet in place), emit the notification recommending `/update-config` to add the specific Bash pattern to `settings.json` `permissions.allow`. This is the SAFE configuration — without the allowlist, every spawn surfaces a Claude Code permission prompt that defeats headless autonomy; with the allowlist, the user has explicitly consented to the pattern once, scoped narrowly |

---

### 9.1. Pre-flight Notification Protocol (canonical)

> Single source of truth. All skills that invoke agy headless (`agy -p ... --dangerously-skip-permissions`) via Claude Code's `Bash` tool MUST emit this notification before the first such spawn in a session.

**Why this exists**: combining `agy --dangerously-skip-permissions` (autonomous tool use inside agy) with Claude Code's `Bash` tool (autonomous shell from Claude) produces a two-layer bypass — neither side gates the agy session's tool calls. The mitigation is **explicit, scoped, persistent consent** registered in `settings.json` via the `update-config` skill, so the user has acknowledged the pattern once.

**Notification rules**:
1. Fires **before** the first agy headless spawn of a session. May skip subsequent spawns in the same session if the allowlist entry is confirmed present.
2. Fires **even in AUTORUN / AUTORUN_FULL modes** — this is an *informational* notification, not a confirmation gate. AUTORUN continues without waiting for user input.
3. Idempotent: same content each time. Safe to re-emit if uncertain.

**Notification template** (insert the actual command being run):

```
⚠ Pre-flight (agy headless spawn)
This session is about to invoke:
    agy -p "<prompt>" --dangerously-skip-permissions [--output-format json] [--log-file ...] [--print-timeout 15m]

Running agy as a Claude Code subagent with --dangerously-skip-permissions creates an
autonomous agent loop that bypasses approval gates on BOTH sides (no agy-side prompt,
no Claude Code-side prompt for the spawned Bash call once allowlisted).

→ If you haven't already, please run the update-config skill ONCE to allowlist the
  Bash pattern in settings.json (recommended scope: user-level, narrow pattern):

    /update-config allow Bash(agy -p:*) in user settings

  Or for tighter scope (recommended for shared/sensitive repos):

    /update-config allow Bash(agy -p:* --dangerously-skip-permissions:*) in user settings

→ Restrict the host environment: only run this pattern in sandboxed dev VMs, CI
  runners with ephemeral filesystems, or workspaces you have explicit authorization
  to modify. Never on production hosts or shared infrastructure.

Continuing the spawn now …
```

**Confirming the allowlist is in place**: skills MAY check `~/.claude/settings.json` (`permissions.allow`) for an entry matching `Bash(agy -p*` before emitting; if present, the notification can be downgraded to a single-line reminder (`✓ agy allowlist confirmed in user settings; proceeding`).

**Cross-references**: skills must point here rather than re-stating the protocol. References in `nexus/SKILL.md`, `_common/SUBAGENT.md`, `_common/MULTI_ENGINE_RECIPE.md`, `judge/references/antigravity-review-usage.md`, `orbit/references/executor-engines.md`, `arena/references/team-mode-guide.md`, `arena/references/engine-cli-guide.md`.

---

## 10. Skill Authoring Checklist (Cross-CLI)

Before publishing a SKILL.md that should work across CLIs, verify:

- [ ] Frontmatter contains exactly `name` and `description` (official Agent Skills spec; `chain` rejects custom keys).
- [ ] `description:` includes 3-5 trigger keywords and primary use case in ≤2 sentences.
- [ ] A `## Compatibility` section documents which CLIs the skill has been tested on, with version stamps.
- [ ] Spawn syntax is abstracted (use role names + a CLI-agnostic template). Do not hard-code `Agent(...)` if the skill is meant to run on agy or Codex.
- [ ] Model selection uses role names (`high-reasoning`, `balanced`, `fast`) mapped via this file.
- [ ] MCP setup snippets cover **both** `url` and `serverUrl` field names.
- [ ] Permission-mode assumption is explicit (`request-review` default, `proceed-in-sandbox` allowed, `always-proceed` forbidden).
- [ ] Output-language directive references the CLI global config (`settings.json` `language`, `CLAUDE.md`, `AGENTS.md`, or `GEMINI.md`).
- [ ] Known pitfalls section mentions any agy-specific risks the skill is exposed to.
- [ ] Source citations for any best-practice claim include URL + date; "未確認" is preferred over speculation.

---

## 11. Items Still Unverified (do not invent)

These are referenced in community sources but lack a confirmed official document. Treat as runtime concerns until verified:

- Exact JSON/TOML key name for agy subagent depth limit (the `agents.max_depth` term is Codex's, not agy's).
- Whether `/goal` autonomous loop is marked experimental in official agy docs.
- agy "Deep Think" CLI flag (distinct from `/model` Claude *(Thinking)* variants).
- agy MCP tool description hash-pin built-in (none confirmed; SHA-256 manifest must be self-built).
- agy managed-settings / MDM-tier equivalent.
- ~~agy `--output-format json` schema stability across versions.~~ **Re-verified (v1.0.2, 2026-05)**: flag is **supported but hidden** — absent from `agy --help` but documented in official Google DEV.to examples. Schema stability across future versions remains open; pin expected fields in the prompt body. Help-output flags confirmed via `agy --help`: `--add-dir`, `-c`/`--continue`, `--conversation`, `--dangerously-skip-permissions`, `-i`/`--prompt-interactive`, `--log-file`, `-p`/`--print`/`--prompt`, `--print-timeout`, `--sandbox`. Help-omitted but confirmed flags: `--output-format`. Earlier 2026-05 note in this file incorrectly claimed `--output-format` was absent — that was based on `--help` alone and did not cross-check official examples.

When you find a confirmed answer, update this file with a `Source: <URL>` (date) citation and remove the item from this list.

---

## 12. Source Tier

When citing from this file, prefer:

- **T1 (official)**: Google Developers Blog, antigravity.google/docs, google-antigravity GitHub repos, geminicli.com/docs (transitional), claude.com / docs.claude.com, platform.openai.com.
- **T2 (forum / community official)**: discuss.ai.google.dev (Google AI Developers Forum).
- **T3 (high-signal community)**: Medium (Google Cloud), DataCamp tutorials, DEV.to hands-on, agentpedia, Composio.
- **T4 (industry coverage)**: TechCrunch, The Register, BuildFastWithAI, individual dev blogs.

Treat T4 claims as candidates for verification, never as standalone authority.
