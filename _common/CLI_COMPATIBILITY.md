# CLI Compatibility Matrix

Cross-CLI compatibility reference for Claude Code / Codex CLI / Antigravity CLI (`agy`). SKILL.md authors consult this file before assuming any specific CLI's API, configuration path, or spawn syntax.

> **Date stamps**: As of 2026-06. Latest releases — **Claude Code 2.1.163**; **Codex CLI 0.137.0** (2026-06-04 — "Multi-agent v2": per-thread runtime choice; 0.136: session archiving; 0.135: named permission profiles); **agy v1.0.5** (per `google-antigravity/antigravity-cli` CHANGELOG.md — 1.0.3: G1 credits UI; 1.0.4: SQLite `.db` conversation storage; 1.0.5: fixed `-p` mode writing metadata into cwd instead of `~/.gemini/antigravity-cli/cache`). Antigravity CLI launched 2026-05-19 (Google I/O 2026, alongside Antigravity 2.0 GA); Gemini CLI personal-tier service stops 2026-06-18. **The agy headless stdout-flush bug (§9.2) is NOT fixed through 1.0.5; the Codex detached-TTY silent-crash #19945 is NOT fixed through 0.137.0 (§9.3).** Re-verify against current docs before relying on any "未確認" item. Update in place via `agy update`.

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
| Nesting / depth control | (config-driven; see Claude Agent SDK). Dynamic Workflows (research preview, v2.1.154+): up to 16 concurrent agents, 1,000 total per run | `agents.max_depth` (default 1; root=depth 0, one child layer) + `agents.max_threads` (default 6 — concurrent open-agent cap; verified 2026-06 config-reference) | **(未確認)** — community guidance says "cap subagent depth" but no documented JSON/TOML key was found; treat as a runtime/budget concern instead of a config knob |
| Long-running goal mode | `/goal` (Claude Code v2.1.139+; completion-condition form added v2.1.141) | `[features] goals = true` (experimental & persistent; requires CLI ≥0.128.0 — official docs still frame it experimental as of 0.137.0; community "default-on since ~0.131" claims are UNCONFIRMED) | `/goal <task>` (run to completion without plan-approval pauses; experimental flag status 未確認) |
| Headless / one-shot | `claude -p` (`--output-format json` + **file redirect** recommended — pipe-capture hits buffering/truncation bugs, §9.3; `--json-schema '<schema>'` for structured output in `.structured_output`; `--bare` for deterministic scripted runs — skips hooks/skills/plugins/MCP/CLAUDE.md; piped stdin capped at 10MB since v2.1.128; **no `-o` artifact flag** — use shell redirect) | `codex exec` (`-o`/`--output-last-message <path>` writes the final message to a file — official artifact channel; `--json` JSONL stream; `--output-schema <file>` structured final JSON; `--ephemeral` skips session persistence for automation. ⚠ **Keep spawns foreground**: detached-TTY + non-trivial prompt silently crashes with no output — #19945, 0.124.0+, unfixed through 0.137.0, §9.3) | `agy -p`, `--dangerously-skip-permissions` (mandatory for non-interactive use — bypasses default `request-review` permission gate; treat as `bypassPermissions` equivalent and restrict to sandboxed/CI/authorized-dev contexts). **stdout is NOT a reliable capture channel** (non-TTY flush bug, unfixed through v1.0.5 — see §9.2 for the mandatory file-handoff protocol). `--output-format json` is UNRELIABLE (conflicting availability reports, no documented schema — §9). File references inside the prompt **must** use `@<path>` syntax — bare path strings trigger silent subagent timeouts (see §9 Known Pitfalls). |

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
- **agy**: paste into a `/agent <slug> "<prompt>"` invocation, or supply via `agy -p "<prompt>" --dangerously-skip-permissions` headless. The skip-permissions flag is mandatory in headless mode because `request-review` cannot be answered there. **Do NOT capture the result from stdout** — apply the file-handoff protocol in §9.2 (prompt-mandated absolute-path artifact write + sentinel + verification chain). `--output-format json` is unreliable (conflicting availability reports, undocumented schema — §9); request JSON inside the artifact file instead. Always reference files with `@<path>` (e.g. `@docs/spec.md`) so the main agent ingests context directly — without `@`, agy delegates file reads to a subagent that hits the 60s timeout and silently exits. `<skills_root>` is `~/.gemini/antigravity-cli/skills/` or `<repo>/.agents/skills/`.

---

## 4. Model Selection

Direct model names are CLI-specific. Authoring tip: write SKILL.md with role names (e.g. `high-reasoning`, `balanced`, `fast`) and let the orchestrator map.

| Role | Claude Code | Codex CLI | agy |
|------|-------------|-----------|-----|
| Default / balanced | `sonnet` (claude-sonnet-4-6) | `gpt-5.4` (flagship professional) | Gemini 3.5 Flash (High/Medium) |
| High-reasoning / precision | `opus` (claude-opus-4-8) | `gpt-5.5` (recommended frontier coding, Apr 2026) | Gemini 3.1 Pro (High/Low), Claude Sonnet 4.6 (Thinking), Claude Opus 4.6 (Thinking) |
| Fast / cheap | `haiku` (claude-haiku-4-5) | `gpt-5.4-mini` (fast) | Gemini 3.5 Flash (Medium), GPT-OSS 120B (Medium) |
| Switching command | per-Agent `model:` parameter | per-`spawn_agent` (未確認) | `/model` inside TUI |

> agy explicitly lists Claude Sonnet 4.6 / Opus 4.6 (Thinking) and GPT-OSS 120B in `/model`. Source: Medium "Getting Started" + tutorial series (2026-05).

> **Codex model lineup (verified 2026-06, developers.openai.com/codex/models)**: `gpt-5.5` (recommended) / `gpt-5.4` / `gpt-5.4-mini` / `gpt-5.3-codex-spark` (research preview, ChatGPT Pro). **Legacy/deprecated: `gpt-5.1`, `gpt-5.1-codex-max`, `gpt-5.2`, `gpt-5.3-codex`** — update any skill that hard-codes them. Claude Code effort levels: `low → medium → high → xhigh → max`; default `high` on Opus 4.8 / Sonnet 4.6 (`xhigh` was the 4.7 default); `/effort ultracode` = `xhigh` + auto workflow orchestration (session-scoped).

> **Codex-as-orchestrator effort routing**: when Codex CLI drives the hub, apply Plan-and-Execute by **model choice** — planning / high-complexity steps → `gpt-5.5`, execution steps → `gpt-5.4` / `gpt-5.4-mini` — plus the **`model_reasoning_effort`** config key (`config.toml` or `-c model_reasoning_effort="..."`), values `minimal | low | medium | high | xhigh`, default `medium`. [Verified 2026-06 — config-reference; resolves the former 未確認 marker.] Full Codex-hub authoring protocol: `_common/CODEX_ORCHESTRATION.md` (C3).

---

## 5. Permission Models

| Tier | Claude Code | Codex CLI | agy |
|------|-------------|-----------|-----|
| Default mode | permissions evaluated `deny → ask → allow` (first match wins) | sandbox-on by default, `--full-auto` opt-in | **`request-review`** (collaborative — pause before terminal / file / external-service ops) |
| Confirm-each | (interactive permission prompts) | (per-action approval) | `request-review` |
| Sandboxed auto | `bypassPermissions` mode (within container/agent) | `--full-auto` | **`proceed-in-sandbox`** (isolated container, no prompts — formally added in CLI v1.0.1 per CHANGELOG) |
| Fully autonomous | (bypassPermissions, audit hooks recommended) | `--dangerously-bypass-approvals-and-sandbox` (do not use in prod) | **`always-proceed`** (host machine, no prompts — production-forbidden) |
| Read-only | hooks/permission deny on write tools | (未確認) | **`strict`** (read-only; all non-read ops require approval) |
| Policy semantics | Hooks can **tighten** (deny) but cannot **loosen** past `settings.json` deny rules. PreToolUse `permissionDecision: "deny"` survives even `bypassPermissions`. | (未確認 — settings precedence documented in `~/.codex/config.toml` reference) | Permission Lists are `action(target)` strings, Allow / Deny / Ask. Positive security model: forbidden unless expressly permitted. |

> **agy known bug**: `request-review` is reported as occasionally ignored for file edits (forum: missing features). Treat this as a runtime risk, not a configuration issue.

---

## 6. MCP Integration

| Aspect | Claude Code | Codex CLI | agy |
|--------|-------------|-----------|-----|
| Config location | inline in `settings.json` (`mcpServers`) | (未確認) | **`mcp_config.json`** (independent file; v1.0.3 CHANGELOG references the path as `config/mcp_config.json` when fixing a TUI server-disable bug — verify the exact subdirectory against your install) |
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
| Usage / quota | `/cost` (legacy `/usage`) | (未確認) | `/usage`, `/quota` (**not live-updated — quit & reload required**, per forum report); `/credits` (v1.0.3 — G1 credits panel: spend G1 credits when standard quota is exhausted, opt-in via `UseG1Credits` setting + live remaining-credit display in status bar; partially mitigates the `/usage` non-live quota-cliff problem in §9) |
| Resume / rewind | `/resume` | (未確認) | `/resume`, `/rewind` |
| MCP management | `/mcp` | (未確認) | `/mcp` |
| Tasks / scheduling | TaskCreate/TaskUpdate (tools) | (未確認) | `/tasks`, `/schedule` |
| Inline shell | `!` prefix | `!` (未確認) | `!command` (TUI-inline shell) |
| File attach | `@path` | `@path` | `@filename` |
| Side question (read-only) | — | — | `/btw` |
| Inspect loaded rules/skills | — | — | `agy inspect` |
| One-shot | `claude -p` (file redirect, not pipe — §9.3) | `codex exec` (`-o <path>` for final-message artifact; keep foreground — §9.3) | `agy -p --dangerously-skip-permissions` (use `@<path>` for files; capture output via §9.2 file-handoff, NOT stdout) |
| Structured output | `--output-format json` + `--json-schema '<schema>'` → `.structured_output` (redirect to file — §9.3) | `--output-schema <file>` + `-o out.json` (⚠ silently ignored when MCP active, #15451) | `--output-format json` UNRELIABLE (§9) — request JSON inside the §9.2 artifact file instead |

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
| **agy requires a TTY + headless stdout-flush bug** — `-p`/`--print` hangs with no controlling terminal AND emits NOTHING to non-TTY stdout even on success (TTY requirement verified 2026-06-08 agy 1.0.6; stdout flush = official issue #115 "Can't Capture CLI Output", OPEN; root cause per gemini-cli #27466: `text_drip.go` renders to TUI but never flushes to a non-TTY stdout) | From a socket-stdin shell (Claude Code `Bash`, CI, cron): bare `agy -p` **hangs to `exit 124`** (empty stdout, no artifact, no log) and `script -q /dev/null agy ...` dies with `tcgetattr/ioctl: Operation not supported on socket` — both are silent-output | **Never use stdout as the deliverable channel, and give agy a real pty.** Allocate the pty via `python3 -c 'import pty; pty.spawn([...])'` (the `script` reattach does NOT work here), then apply the §9.2 file-handoff protocol (prompt-mandated absolute-path artifact + sentinel + verification chain + transcript fallback). Canonical block: §9.2 |
| **Bare file paths in prompts trigger silent subagent timeouts** | Headless `agy -p` exits with `exit 0` + empty stdout when given paths without `@`; main agent delegates file reads to a subagent that dies at the 60s cap (v1.0.2 changelog: "restricted the default 60-second interaction timeout specifically to subagents") | **Always use `@<path>` syntax** to inject file context into the main agent; combine with `--log-file` + post-run grep per `_common/MULTI_ENGINE_RECIPE.md §3.5` |
| **`--output-format json` availability is INCONSISTENT across installs** (2026-06 re-verification: community guide demonstrates it, but a commenter on the same guide reports "flag not defined" error; no JSON schema documented anywhere; official issue #7 notes `stream-json` is Gemini CLI legacy, not agy) | A spawn script depending on the flag may hard-fail on some installs, or succeed with an unparseable schema | **Do not depend on the flag for output capture.** Request the structured JSON inside the §9.2 artifact file via the prompt instead; if the flag is used at all, treat failure as non-fatal |
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
    agy -p "<prompt>" --dangerously-skip-permissions [--log-file ...] [--print-timeout 15m]

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

**Cross-references**: skills must point here rather than re-stating the protocol. References in `nexus/SKILL.md`, `_common/SUBAGENT.md`, `_common/MULTI_ENGINE_RECIPE.md`, `judge/reference/antigravity-review-usage.md`, `orbit/reference/executor-engines.md`, `rally` (engine-paradigm recipe — Codex/agy bridging).

---

### 9.2. agy Headless Output-Capture Protocol (canonical)

> Single source of truth for capturing deliverables from `agy -p` spawns. Verified 2026-06 against agy v1.0.5; **agy-as-agent TTY convention re-verified 2026-06-08 against agy 1.0.6 / codex 0.137.0 / Claude Code 2.1.168 (macOS)**. All skills that spawn agy headless MUST follow this protocol instead of reading stdout.

> **⚠ MANDATORY CONVENTION — read before spawning agy or codex as an agent.** When agy/codex are driven as sub-agents from an orchestrator's shell (Claude Code `Bash`, CI runner, cron — i.e. **no controlling terminal, socket stdin**), the silent-output failure is reproducible and has a verified fix per engine:
> - **agy REQUIRES a TTY.** A bare `agy -p "..." > file` **hangs to timeout** (`exit 124`, empty stdout, **no artifact, no log file at all**) — a textbook silent-output. The previously-recommended pseudo-TTY reattach `script -q /dev/null agy ...` **also fails** in this context (`script: tcgetattr/ioctl: Operation not supported on socket`). The **only** verified mitigation is allocating a real pty via **`python3 -c 'import pty; pty.spawn([...])'`** (see canonical block below) — with the pty, agy runs, writes the artifact + sentinel, and even flushes stdout.
> - **codex is robust** with `-o <abs path>`: foreground *and* fully-detached (`start_new_session` / no controlling tty) + non-trivial prompts both completed correctly (#19945 did NOT reproduce on 0.137.0 when `-o` is the capture channel). Always pass `-o` and treat the artifact (not stdout, not exit code) as the source of truth.

**Why (agy)**: agy `-p`/`--print` mode has two compounding non-TTY failures. (1) **TTY requirement** — agy's runtime opens `/dev/tty`; with no controlling terminal it stalls until `--print-timeout`/the caller's timeout and dies leaving nothing (empty stdout, no artifact, no `--log-file` written). (2) **stdout-flush bug** (official issue #115, OPEN; root cause `text_drip.go` per gemini-cli #27466) — even when it does run, it exits 0 **without writing the response to a piped/redirected stdout**. Unfixed through v1.0.6. Therefore `exit 0/124 + empty stdout` does NOT imply RUNTIME-BROKEN and an empty stdout is also what a *successful* run looks like. Capture must move to disk artifacts, and the process must be given a pty.

**Capture channels, in order of authority**:

1. **Prompt-mandated artifact file (primary)** — print mode executes tools (file writes) and this cannot be disabled, so instruct the agent to write its deliverable to a file. Known failure modes of this channel itself — *phantom writes* (agent claims it wrote; no file) and *sandbox-cwd path mismatch* (agent resolves a relative path against a different cwd) — are mitigated by: **absolute path only**, a **final-line sentinel**, and the **verification chain** below.
2. **agy transcript harvest (fallback)** — every conversation persists `~/.gemini/antigravity-cli/brain/<conv-id>/.system_generated/logs/transcript.jsonl` regardless of stdout. The final answer is the last entry matching `source=MODEL, status=DONE, type=PLANNER_RESPONSE`. Resolve `<conv-id>` via `~/.gemini/antigravity-cli/cache/last_conversations.json` (fallback: newest-mtime `brain/` dir). ⚠ Undocumented internal paths — expect bitrot across versions; re-verify on `agy update` (v1.0.4 also stores conversations as SQLite `.db`).
3. **`--log-file` grep (failure diagnosis)** — quota / OAuth / executor errors per §3.5 of `_common/MULTI_ENGINE_RECIPE.md`. Only after channels 1-2 are both empty does RUNTIME-BROKEN apply.

**Mandatory prompt block** (append to every headless agy prompt; `<slug>` = task slug, absolute path required):

```
MANDATORY OUTPUT PROTOCOL:
- Write your COMPLETE deliverable to the absolute path /tmp/agy-<slug>.md (create or overwrite).
- End that file with a final line containing exactly: <<<END_OF_OUTPUT>>>
- To stdout, print only a single status line: DONE /tmp/agy-<slug>.md
```

**Canonical spawn + verification chain**:

```bash
SLUG="<task-slug>"
OUT="/tmp/agy-${SLUG}.md"          # ABSOLUTE path — agy sandbox cwd ≠ orchestrator cwd
LOG="/tmp/agy-${SLUG}.log"
rm -f "$OUT"
# agy REQUIRES a TTY. In a no-controlling-terminal / socket-stdin context (Claude Code's Bash
# tool, CI, cron) a bare `agy -p` hangs to timeout (empty stdout, no artifact, no log), and
# `script -q /dev/null agy ...` fails immediately ("tcgetattr/ioctl: Operation not supported
# on socket"). Allocate a real pty via python pty.spawn — the ONLY mitigation verified in that
# context (2026-06-08, agy 1.0.6). Exit code is NOT trusted; the artifact below is the truth.
python3 - "$LOG" <<'PY' || true
import pty, sys
log = sys.argv[1]
prompt = open("/tmp/prompt.md").read()
pty.spawn(["agy","-p",prompt,"--dangerously-skip-permissions","--log-file",log,"--print-timeout","15m"])
PY

# Verification chain — ALL must pass before the artifact is trusted
if [ -s "$OUT" ] && grep -q '<<<END_OF_OUTPUT>>>' "$OUT"; then
  echo "OK: deliverable at $OUT"
else
  # Fallback: harvest agy's own transcript (undocumented internal path — bitrot risk)
  BRAIN="$HOME/.gemini/antigravity-cli/brain"
  CONV="$(ls -td "$BRAIN"/*/ 2>/dev/null | head -1)"
  TR="${CONV}.system_generated/logs/transcript.jsonl"
  if [ -f "$TR" ]; then
    grep '"type":"PLANNER_RESPONSE"' "$TR" | grep '"status":"DONE"' | tail -1 > "${OUT}.transcript.json"
  fi
  if [ ! -s "$OUT" ] && [ ! -s "${OUT}.transcript.json" ]; then
    grep -E "RESOURCE_EXHAUSTED|Resets in|error getting token|agent executor error|unexpected end of JSON|subagent.*timeout|interaction timeout" "$LOG" | head -5
    echo "VERDICT: agy RUNTIME-BROKEN"
    exit 42   # caller treats non-0 as RUNTIME-BROKEN; do not silently aggregate
  fi
fi
```

**Typed retry rule**: if the artifact is missing/empty but the transcript shows the model produced content, retry ONCE with an explicit repair directive ("the previous run did not write the file — rewrite your full output to /tmp/agy-<slug>.md"). Max 1 retry; do not loop blindly.

**Structured output**: request JSON *inside the artifact file* ("write a single JSON object to /tmp/agy-<slug>.json, then the sentinel on its own final line"). Do not rely on `--output-format json` (§9 pitfall: inconsistent availability, undocumented schema).

**Precedent**: Codex CLI solves the same problem class officially via `codex exec -o/--output-last-message <path>` (artifact-as-source-of-truth; stdout may contain progress noise and exit 0 can coexist with semantic failure). agy has no `-o` equivalent — the prompt-mandated write is the substitute.

**Cross-references**: `_common/MULTI_ENGINE_RECIPE.md §3.5` (failure-detection contract), `_common/SUBAGENT.md` Dispatch Examples (same snippet — keep in sync), `nexus/SKILL.md` Antigravity CLI section.

---

### 9.3. Codex CLI / Claude Code Headless Output Capture (canonical)

> Companion to §9.2. Verified 2026-06 against Codex CLI 0.137.0 / Claude Code 2.1.163. Every CLI in this matrix has an output-capture failure class — none of the three may be captured naively from a pipe.

**Codex CLI (`codex exec`)**:

- **Artifact-first**: always pass `-o`/`--output-last-message <abs path>` — the final message goes to the file AND stdout. Treat the file as the source of truth; stdout may carry progress noise, and exit 0 can coexist with semantic failure.
- **⚠ Detached-TTY silent crash (#19945, OPEN)**: `codex exec` with stdio detached from a controlling TTY + a non-trivial prompt silently crashes with no output (regression 0.124.0+, unfixed through 0.137.0). Spawning via `setsid` / background-Bash triggers it. Mitigation: keep the process **foreground** with stdout redirected to a file; pseudo-TTY reattach (`script -qfc "codex exec ..." /dev/null`) works but emits a spurious `failed to record rollout items` error. Verification: `[ -s "$ARTIFACT" ]` after exit; empty artifact → RUNTIME-BROKEN.
- **Structured output**: `--output-schema <schema-file>` + `-o out.json`. ⚠ `--json`/`--output-schema` are silently ignored when MCP servers/tools are active (#15451, resolution unconfirmed) — validate the artifact parses before aggregating.
- `--ephemeral` skips session persistence (useful in CI). Official exec docs live at developers.openai.com/codex/noninteractive (`docs/exec.md` in-repo is a stub). Exit-code semantics are undocumented — verify artifacts, not exit codes.

**Claude Code (`claude -p`)**:

- **File redirect over pipe-capture**: Node's 64KB stdout highWaterMark + `process.exit()`-before-drain silently truncates large piped output (#36685 family, closed "not planned"), and `--output-format stream-json` is block-buffered when piped (~4-8KB stalls, #25670 closed as duplicate, effectively unresolved). **Redirect to a file** (`claude -p '...' --output-format json > out.json`) — file redirect bypasses the kernel pipe buffer.
- **Recommended pattern**: `--output-format json` + file redirect, then parse `.result` (or `.structured_output` when using `--json-schema '<JSON Schema>'`). `--bare` for deterministic scripted runs (skips hooks/skills/plugins/MCP/CLAUDE.md auto-discovery; docs note it "will become default for `-p`").
- **Empty-result class partially live**: `-p` occasionally returns an empty `result` while tokens are billed (#38623 closed; successor reports #38805, #38651 — the latter triggered by Stop hooks). Treat `result == ""` as a retryable failure (max 1 typed retry), not as "no findings".
- **No artifact flag**: there is no `codex exec -o` equivalent — shell redirect is the artifact channel. Piped **stdin** is capped at 10MB since v2.1.128 (non-zero exit past the cap; pass a file path instead).

**Shared rule**: for all three CLIs, the deliverable artifact (explicit file, `-o` file, or redirect target) is the source of truth; verify non-empty (+ schema/sentinel where applicable) before aggregating, and never infer engine failure from stdout alone.

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
- agy `--output-format json` — **status downgraded (2026-06, v1.0.5)**: availability is INCONSISTENT across installs (the DEV.to guide demonstrates it; a commenter on the same guide reports "flag not defined"; no schema documented; official issue #7 notes `stream-json` is Gemini CLI legacy). Earlier 2026-05 note in this file calling it "supported but hidden" overstated confidence. Do not depend on it — use the §9.2 artifact-file protocol for structured output. Help-output flags confirmed via `agy --help` (v1.0.2): `--add-dir`, `-c`/`--continue`, `--conversation`, `--dangerously-skip-permissions`, `-i`/`--prompt-interactive`, `--log-file`, `-p`/`--print`/`--prompt`, `--print-timeout`, `--sandbox`.
- Whether `--dangerously-skip-permissions` actually gates anything in `-p` print mode — one community bridge reports it is a no-op there (print mode executes tools regardless); a legacy Gemini CLI note claims the opposite. Keep passing the flag (harmless if no-op, required if not), but do not assume omitting it sandboxes a headless run.
- agy transcript internals (`brain/<conv-id>/.system_generated/logs/transcript.jsonl`, `cache/last_conversations.json`, v1.0.4 SQLite `.db`) — used by §9.2 fallback; undocumented and version-fragile.

When you find a confirmed answer, update this file with a `Source: <URL>` (date) citation and remove the item from this list.

---

## 12. Source Tier

When citing from this file, prefer:

- **T1 (official)**: Google Developers Blog, antigravity.google/docs, google-antigravity GitHub repos, geminicli.com/docs (transitional), claude.com / docs.claude.com, platform.openai.com.
- **T2 (forum / community official)**: discuss.ai.google.dev (Google AI Developers Forum).
- **T3 (high-signal community)**: Medium (Google Cloud), DataCamp tutorials, DEV.to hands-on, agentpedia, Composio.
- **T4 (industry coverage)**: TechCrunch, The Register, BuildFastWithAI, individual dev blogs.

Treat T4 claims as candidates for verification, never as standalone authority.
