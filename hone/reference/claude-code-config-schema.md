# Claude Code Config Schema

**Purpose:** Comprehensive reference for all Claude Code configuration keys, default values, environment variables, and recommended settings.
**Read when:** Auditing `~/.claude/` or proposing configuration changes.
**Last updated:** 2026-03-12

---

## Config File Locations

| File | Scope | Format | Merge behavior |
|------|-------|--------|---------------|
| `/Library/Application Support/ClaudeCode/managed-settings.json` | Managed (highest priority) | JSON | IT管理者が配布、ユーザー設定を上書き |
| `~/.claude/settings.json` | User (global) | JSON | 全プロジェクト共通 |
| `<project>/.claude/settings.json` | Project (shared) | JSON | git管理、チーム共有 |
| `<project>/.claude/settings.local.json` | Project (local) | JSON | gitignore対象、個人用 |
| `~/.claude/CLAUDE.md` | Global instructions | Markdown | — |
| `<project>/CLAUDE.md` | Project instructions | Markdown | — |
| `<project>/.claude/commands/` | Custom slash commands | Markdown | — |
| `<project>/.claude/skills/` | Skills (structured agents) | Markdown | — |

> **Note:** Array settings (`permissions.allow`, `sandbox.filesystem.allowWrite`, etc.) are **merged** across scopes.

### JSON Schema

```json
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json"
}
```

> Enables autocompletion and validation in editors.

---

## Core Settings

| Key | Type | Default | Description | Audit focus |
|-----|------|---------|-------------|-------------|
| `model` | string | — | Model override | CCM1: must be current |
| `language` | string | — | Response language (e.g., `"Japanese, 日本語"`) | — |
| `outputStyle` | string | — | System-prompt-level style injection (free text) | Conciseness tuning |
| `cleanupPeriodDays` | number | 30 | Days before inactive session data cleanup | Set explicitly |
| `autoUpdatesChannel` | string | `"latest"` | `"stable"` (1-week delay) or `"latest"` | Prefer `"stable"` for production |
| `verbose` | boolean | false | Show full Bash output etc. | M3: should not be permanent |
| `showTurnDuration` | boolean | true | Display response time | — |
| `alwaysThinkingEnabled` | boolean | false | Enable Extended Thinking by default | — |
| `plansDirectory` | string | `~/.claude/plans` | Plan file storage path | — |
| `respectGitignore` | boolean | true | `@` file picker respects .gitignore | Set true |
| `fastModePerSessionOptIn` | boolean | — | Require `/fast` per session to enable fast mode | — |
| `forceLoginMethod` | string | — | `"claudeai"` or `"console"` to restrict login | — |
| `forceLoginOrgUUID` | string | — | Auto-select organization UUID | — |
| `includeGitInstructions` | boolean | true | Include git workflow instructions in system prompt | — |

---

## UI & Display Customization

| Key | Type | Default | Description | Audit focus |
|-----|------|---------|-------------|-------------|
| `theme` | string | — | `dark`, `light`, `light-daltonized`, `dark-daltonized` | — |
| `preferredNotifChannel` | string | — | `iterm2`, `iterm2_with_bell`, `terminal_bell`, `notifications_disabled` | — |
| `prefersReducedMotion` | boolean | false | Reduce animations (accessibility) | — |
| `terminalProgressBarEnabled` | boolean | — | Terminal progress bar display | — |
| `spinnerTipsEnabled` | boolean | — | Show tips during spinner | — |
| `spinnerVerbs` | object | — | Custom spinner text (`mode`: `"append"` / `"replace"`, `verbs`: string[]) | — |
| `spinnerTipsOverride` | object | — | Custom tips (`tips`: string[], `excludeDefault`: boolean) | — |
| `companyAnnouncements` | string[] | — | Random startup messages | Reminders, team announcements |

### StatusLine

| Key | Type | Description |
|-----|------|-------------|
| `statusLine.type` | string | `"command"` |
| `statusLine.command` | string | Custom script path (receives JSON via stdin) |

StatusLine JSON input fields: `workspace`, `model`, `cost`, `context_window`, `session_id`, `transcript_path`

### FileSuggestion

| Key | Type | Description |
|-----|------|-------------|
| `fileSuggestion.type` | string | `"command"` |
| `fileSuggestion.command` | string | Custom script for `@` autocomplete (receives JSON with `query` and `cwd`) |

### Attribution

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `attribution.commit` | string | — | Text appended to git commit messages (empty `""` = disable) |
| `attribution.pr` | string | — | Text appended to PR descriptions (empty `""` = disable) |
| `includeCoAuthoredBy` | boolean | — | **Deprecated**: use `attribution` instead |

---

## Permissions

| Key | Type | Description | Audit focus |
|-----|------|-------------|-------------|
| `permissions.allow` | string[] | Auto-allowed tool patterns | CCP1: no broad `Bash` |
| `permissions.deny` | string[] | Always-denied tool patterns (highest priority) | CCP2: deny destructive ops |
| `permissions.ask` | string[] | Require confirmation | — |
| `permissions.additionalDirectories` | string[] | Extra accessible directories | — |
| `permissions.defaultMode` | string | `acceptEdits`, `askEdits`, `plan`, `execute`, `bypassPermissions` | — |
| `permissions.disableBypassPermissionsMode` | string | `"disable"` to block `--dangerously-skip-permissions` | Enterprise hardening |

### Permission Pattern Syntax

| Pattern | Meaning | Safety |
|---------|---------|--------|
| `"Read"` | Allow all file reads | Generally safe |
| `"Edit"` | Allow all file edits | Moderate risk |
| `"Bash(command*)"` | Allow specific bash commands matching glob | Scope narrowly |
| `"Bash"` | Allow ALL bash commands | High risk — avoid global |
| `"WebFetch(domain:example.com)"` | Allow fetch to specific domain | — |
| `"MCP(server_name)"` | Allow MCP server tools | — |
| `"Agent(agent_name)"` | Allow specific agent | — |
| `"Read(./.env)"` | Read specific file | Use in deny for secrets |
| `"Read(./**/*credentials*)"` | Read files matching glob | Use in deny |

### Recommended Deny Rules

```json
"deny": [
  "Bash(curl *)",
  "Bash(wget *)",
  "Read(./.env)",
  "Read(./.env.*)",
  "Read(./secrets/**)",
  "Read(./**/*credentials*)",
  "Read(./**/*secret*)"
]
```

> `curl`/`wget` are prompt injection vectors — officially recommended to block.

### Permission Audit Criteria

- **CCP1**: Broad `Bash` allow in global settings is risky
- **CCP2**: Missing deny rules for destructive operations
- **CCP3**: Same pattern in both allow and deny (deny wins, but redundant)
- **CCP4**: References to tools/servers that no longer exist

---

## Sandbox Settings

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `sandbox.enabled` | boolean | false | Enable Bash sandboxing |
| `sandbox.autoAllowBashIfSandboxed` | boolean | true | Auto-allow Bash when sandboxed |
| `sandbox.excludedCommands` | string[] | — | Commands to run outside sandbox (e.g., `["git", "docker"]`) |
| `sandbox.allowUnsandboxedCommands` | boolean | true | Allow `dangerouslyDisableSandbox` escape hatch |
| `sandbox.enableWeakerNestedSandbox` | boolean | false | Weaker sandbox inside Docker |
| `sandbox.enableWeakerNetworkIsolation` | boolean | false | Allow TLS trust services (macOS) |

### Sandbox Filesystem

| Key | Type | Description |
|-----|------|-------------|
| `sandbox.filesystem.allowWrite` | string[] | Additional writable paths |
| `sandbox.filesystem.denyWrite` | string[] | Blocked write paths |
| `sandbox.filesystem.denyRead` | string[] | Blocked read paths (e.g., `["~/.aws/credentials", "~/.ssh/*"]`) |

### Sandbox Network

| Key | Type | Description |
|-----|------|-------------|
| `sandbox.network.allowedDomains` | string[] | Allowed domains (`*.example.com` wildcards) |
| `sandbox.network.allowUnixSockets` | string[] | Allowed Unix sockets |
| `sandbox.network.allowAllUnixSockets` | boolean | Allow all Unix socket connections |
| `sandbox.network.allowLocalBinding` | boolean | Allow localhost binding (macOS) |
| `sandbox.network.httpProxyPort` | number | HTTP proxy port |
| `sandbox.network.socksProxyPort` | number | SOCKS5 proxy port |
| `sandbox.network.allowManagedDomainsOnly` | boolean | (Managed) Only allow managed domains |

### Sandbox Path Prefixes

| Prefix | Meaning |
|--------|---------|
| `//` | Root absolute path |
| `~/` | Home directory relative |
| `/` | Settings file directory relative |

---

## Environment Variables (`env` block)

### Model & Performance Tuning

| Variable | Type | Default | Description | Audit focus |
|----------|------|---------|-------------|-------------|
| `ANTHROPIC_MODEL` | string | — | Model override | CCM1 |
| `CLAUDE_CODE_EFFORT_LEVEL` | string | — | Reasoning effort: `low`, `medium`, `high` | — |
| `CLAUDE_CODE_MAX_OUTPUT_TOKENS` | string | `"32000"` | Max output tokens (max `"64000"`) | CCE1: consider raising |
| `MAX_THINKING_TOKENS` | string | `"31999"` | Extended Thinking budget | CCE2: balance cost vs depth |
| `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` | string | `"95"` | Auto-compact trigger threshold (%) | **CCE3: 70-80 recommended** |
| `CLAUDE_CODE_DISABLE_1M_CONTEXT` | string | — | `"1"` to disable 1M context | — |
| `CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING` | string | — | `"1"` to disable adaptive reasoning | — |
| `CLAUDE_CODE_SUBAGENT_MODEL` | string | — | Model for subagents | — |
| `CLAUDE_CODE_FILE_READ_MAX_OUTPUT_TOKENS` | string | — | File read token limit | — |

### MCP & Tool Optimization

| Variable | Type | Default | Description | Audit focus |
|----------|------|---------|-------------|-------------|
| `ENABLE_TOOL_SEARCH` | string | — | `"auto:0"` for on-demand MCP tool loading | **CCE4: saves ~32% context** |
| `MCP_TIMEOUT` | string | — | MCP server startup timeout (ms) | — |
| `MCP_TOOL_TIMEOUT` | string | — | MCP tool execution timeout (ms) | — |
| `MAX_MCP_OUTPUT_TOKENS` | string | `"25000"` | MCP output limit | — |

### Bash Execution Control

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `BASH_DEFAULT_TIMEOUT_MS` | string | — | Default Bash timeout |
| `BASH_MAX_TIMEOUT_MS` | string | — | Maximum Bash timeout |
| `BASH_MAX_OUTPUT_LENGTH` | string | — | Maximum Bash output characters |
| `CLAUDE_BASH_MAINTAIN_PROJECT_WORKING_DIR` | string | — | Return to project dir after each command |
| `CLAUDE_CODE_SHELL` | string | — | Shell override (e.g., `"bash"`, `"zsh"`) |
| `CLAUDE_CODE_SHELL_PREFIX` | string | — | Prefix for all Bash commands |

### Privacy & Telemetry

| Variable | Type | Description |
|----------|------|-------------|
| `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` | string | **Master switch**: disable all non-essential traffic |
| `DISABLE_TELEMETRY` | string | Disable Statsig telemetry |
| `DISABLE_ERROR_REPORTING` | string | Disable Sentry error reporting |
| `DISABLE_AUTOUPDATER` | string | Disable auto-updates |
| `DISABLE_BUG_COMMAND` | string | Disable /bug command |
| `DISABLE_COST_WARNINGS` | string | Disable cost warnings |
| `DISABLE_NON_ESSENTIAL_MODEL_CALLS` | string | Disable non-critical model calls |
| `DISABLE_INSTALLATION_CHECKS` | string | Disable install warnings |
| `CLAUDE_CODE_HIDE_ACCOUNT_INFO` | string | Hide email/org from UI |

### Feature Flags

| Variable | Type | Description |
|----------|------|-------------|
| `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` | string | `"1"` to enable Agent Teams |
| `CLAUDE_CODE_DISABLE_FAST_MODE` | string | Disable fast mode |
| `CLAUDE_CODE_DISABLE_AUTO_MEMORY` | string | Disable auto memory |
| `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS` | string | Disable background tasks |
| `CLAUDE_CODE_DISABLE_CRON` | string | Disable scheduled tasks |
| `CLAUDE_CODE_DISABLE_GIT_INSTRUCTIONS` | string | Remove git workflow instructions |
| `CLAUDE_CODE_SIMPLE` | string | `"1"` for minimal mode (Bash + file R/W only) |
| `CLAUDE_CODE_ENABLE_TASKS` | string | `"false"` for legacy TODO list |
| `CLAUDE_CODE_ENABLE_PROMPT_SUGGESTION` | string | `"false"` to disable prompt suggestions |
| `CLAUDE_CODE_DISABLE_FEEDBACK_SURVEY` | string | Disable session quality survey |
| `CLAUDE_CODE_DISABLE_TERMINAL_TITLE` | string | Disable terminal title updates |
| `CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS` | string | Disable anthropic-beta headers |

### Authentication & Provider

| Variable | Type | Description |
|----------|------|-------------|
| `ANTHROPIC_API_KEY` | string | API key |
| `ANTHROPIC_AUTH_TOKEN` | string | Custom Bearer token |
| `ANTHROPIC_CUSTOM_HEADERS` | string | Custom headers |
| `CLAUDE_CODE_USE_BEDROCK` | string | Use AWS Bedrock |
| `CLAUDE_CODE_USE_VERTEX` | string | Use Google Vertex AI |
| `CLAUDE_CODE_USE_FOUNDRY` | string | Use Microsoft Foundry |
| `CLAUDE_CODE_SKIP_BEDROCK_AUTH` | string | Skip Bedrock auth (LLM gateway) |
| `CLAUDE_CODE_SKIP_VERTEX_AUTH` | string | Skip Vertex auth |
| `CLAUDE_CODE_SKIP_FOUNDRY_AUTH` | string | Skip Foundry auth |
| `CLAUDE_CODE_CLIENT_CERT` | string | mTLS client certificate path |
| `CLAUDE_CODE_CLIENT_KEY` | string | mTLS private key path |
| `CLAUDE_CODE_CLIENT_KEY_PASSPHRASE` | string | Encrypted key passphrase |

### Telemetry & Monitoring

| Variable | Type | Description |
|----------|------|-------------|
| `CLAUDE_CODE_ENABLE_TELEMETRY` | string | `"1"` to enable OpenTelemetry |
| `OTEL_METRICS_EXPORTER` | string | OTel exporter (e.g., `"otlp"`) |
| `CLAUDE_CODE_OTEL_HEADERS_HELPER_DEBOUNCE_MS` | string | OTel header refresh interval (default 29min) |

### Miscellaneous

| Variable | Type | Description |
|----------|------|-------------|
| `CLAUDE_CONFIG_DIR` | string | Custom config/data directory location |
| `CLAUDE_CODE_TMPDIR` | string | Temporary directory override |
| `CLAUDE_CODE_TASK_LIST_ID` | string | Share task list across sessions |
| `CLAUDE_CODE_API_KEY_HELPER_TTL_MS` | string | Auth credential refresh interval |
| `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD` | string | Load CLAUDE.md from `--add-dir` dirs |
| `CLAUDE_CODE_EXIT_AFTER_STOP_DELAY` | string | Auto-exit delay after idle (ms) |

---

## Hooks Configuration

> **Note:** Detailed hook design and debugging is handled by the **Latch** agent. Hone audits hooks configuration only for structural validity and security concerns.

| Event | Trigger | Hone audit scope |
|-------|---------|-----------------|
| `PreToolUse` | Before a tool executes | Check matcher validity, no secrets in commands |
| `PostToolUse` | After a tool executes | Check matcher validity, no secrets in commands |
| `UserPromptSubmit` | When user submits prompt | Check command validity |
| `SessionStart` | When session starts | Check command validity |
| `Notification` | When a notification is sent | Check command validity |
| `Stop` | When agent stops | Check command validity |
| `SubagentStop` | When a subagent stops | Check command validity |
| `PreCompact` | Before context compaction | Check command validity |

### Hook-Related Settings

| Key | Type | Description |
|-----|------|-------------|
| `disableAllHooks` | boolean | Disable all hooks |
| `allowManagedHooksOnly` | boolean | (Managed) Only managed hooks allowed |
| `allowedHttpHookUrls` | string[] | Allowed HTTP hook URL patterns |
| `httpHookAllowedEnvVars` | string[] | Env vars accessible by HTTP hooks |

### Hook Audit Criteria (Structural Only)

- **Validity**: Hook commands are executable and paths exist
- **Security**: No plaintext secrets in hook commands or environment
- **Matcher validity**: Tool matchers reference existing tools
- **Delegation**: Complex hook logic should be reviewed by Latch

---

## MCP Server Configuration

```json
{
  "mcpServers": {
    "server-name": {
      "command": "npx",
      "args": ["-y", "@scope/mcp-server"],
      "env": { "API_KEY": "${env:API_KEY}" }
    }
  }
}
```

### MCP-Related Settings

| Key | Type | Description |
|-----|------|-------------|
| `enableAllProjectMcpServers` | boolean | Auto-approve all `.mcp.json` servers |
| `enabledMcpjsonServers` | string[] | Approved MCP servers |
| `disabledMcpjsonServers` | string[] | Rejected MCP servers |
| `allowedMcpServers` | string[] | (Managed) Allow list |
| `deniedMcpServers` | string[] | (Managed) Deny list |

### MCP Audit Criteria

- **CCS1**: Server command exists and is executable
- **CCS2**: No unused/orphaned server configs
- **CCS3**: No plaintext secrets — use `${env:VAR}` syntax
- **CCS4**: Server packages are current
- **CCS5**: Global vs project placement is appropriate

---

## Plugin Settings

| Key | Type | Description |
|-----|------|-------------|
| `enabledPlugins` | object | Plugin ON/OFF (`"plugin-name@marketplace": true/false`) |
| `extraKnownMarketplaces` | object | Additional marketplaces |
| `strictKnownMarketplaces` | string[] | (Managed) Allowed marketplaces only |
| `blockedMarketplaces` | string[] | (Managed) Blocked marketplaces |

---

## Agent Teams

| Key | Type | Description |
|-----|------|-------------|
| `teammateMode` | string | `auto`, `in-process`, `tmux` |

---

## Authentication Helpers

| Key | Type | Description |
|-----|------|-------------|
| `apiKeyHelper` | string | Script to generate auth value (runs via `/bin/sh`) |
| `awsAuthRefresh` | string | AWS credential refresh script |
| `awsCredentialExport` | string | AWS credential JSON output script |
| `otelHeadersHelper` | string | OpenTelemetry header generation script |

---

## CLAUDE.md Instruction Files

| File | Scope | Purpose | Audit focus |
|------|-------|---------|-------------|
| `~/.claude/CLAUDE.md` | Global | Global instructions for all projects | Non-empty, clear, up-to-date, no secrets |
| `<project>/CLAUDE.md` | Project | Project-level instructions | Relevant to project, no contradictions with global |
| `<project>/.claude/CLAUDE.md` | Project (hidden) | Alternative project instructions location | Check for duplicates with root CLAUDE.md |

### CLAUDE.md Audit Criteria

- **CCI1**: At least one instruction file exists (global recommended)
- **CCI2**: Content reflects current project state and tool capabilities
- **CCI3**: No API keys, tokens, or credentials in instruction files
- **CCI4**: Project and global instructions are consistent

---

## Custom Slash Commands vs Skills

| | Custom Slash Commands | Skills |
|---|---|---|
| Location | `~/.claude/commands/` (global), `.claude/commands/` (project) | `.claude/skills/` |
| Format | Single Markdown file (prompt template) | Structured: `SKILL.md` + reference files |
| Invocation | User explicitly calls `/command-name` | Claude auto-selects or `/skill-name` |
| Complexity | Simple — 1 file = 1 prompt | Structured — references, templates, workflows |
| Arguments | `$ARGUMENTS` | `ARGUMENTS:` block |
| Use case | Repetitive prompt shortcuts | Domain expertise, agent-like behavior |

### Command Audit Criteria

- **CCK1**: Command files are valid Markdown
- **CCK2**: No hardcoded secrets in command templates

---

## Model Configuration

| Method | Scope | Description |
|--------|-------|-------------|
| `ANTHROPIC_MODEL` env var | Session | Override model for current session |
| `/model` command | Session | Interactive model selection |
| `model` key in settings.json | Persistent | Override in settings |
| `settings.json` env block | Persistent | Set via env vars |

### Current Model Identifiers

| Model | ID | Recommendation |
|-------|-----|----------------|
| Claude Opus 4.8 | `claude-opus-4-8` | Most capable; long-horizon agentic, coding, complex tasks (default `xhigh` effort) |
| Claude Opus 4.6 | `claude-opus-4-6` | Prior Opus; complex tasks |
| Claude Sonnet 4.6 | `claude-sonnet-4-6` | Balanced performance and speed |
| Claude Haiku 4.5 | `claude-haiku-4-5-20251001` | Fast; simple tasks |

---

## Authentication

| Method | Configuration | Use when |
|--------|--------------|----------|
| API Key | `ANTHROPIC_API_KEY` env var | Direct API access |
| Claude Pro/Team | OAuth via `claude login` | Subscription-based access |

### Auth Audit Criteria

- **CCA1**: Authentication method is set up and working
- **CCA2**: `ANTHROPIC_API_KEY` not hardcoded in settings.json or CLAUDE.md
- Env var security: API keys use environment variables, not file literals

> **NEVER read:** `~/.claude/credentials.json`, `~/.claude/statsig/`, or any auth/session files.

---

## Power User Hacks & Tips

### Context Optimization

| Hack | Setting | Effect |
|------|---------|--------|
| Early compaction | `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE: "70-80"` | Default 95% is too late; earlier compaction preserves quality |
| MCP lazy loading | `ENABLE_TOOL_SEARCH: "auto:0"` | On-demand MCP tool loading saves ~32% context |
| Output expansion | `CLAUDE_CODE_MAX_OUTPUT_TOKENS: "64000"` | Prevent truncation on large outputs |
| Thinking budget | `MAX_THINKING_TOKENS: "10000"` | Reduce from 31K default for cost savings |

### Workflow Optimization

| Hack | Setting | Effect |
|------|---------|--------|
| Style injection | `outputStyle: "ultra-concise..."` | System-prompt-level output style control |
| Startup reminders | `companyAnnouncements: [...]` | Random messages at session start |
| Smart file suggest | `fileSuggestion.command` | Custom `@` autocomplete with git-aware script |
| Attribution removal | `attribution: { commit: "", pr: "" }` | Remove all Claude signatures |

### Parallel Execution Tips

- Multiple terminal tabs with numbered instances
- `claude.ai/code` for web sessions in parallel
- `/teleport` to bring cloud sessions local
- `Ctrl+B` to move subagents to background

---

## Version History

| Date | Change | Source |
|------|--------|--------|
| Initial | Schema documented from Claude Code v1.x | T2: anthropics/claude-code GitHub |
| 2026-03-12 | Major expansion: env vars, sandbox, hooks, plugins, power user hacks | T1: code.claude.com/docs, T2: GitHub, T3: community blogs |

> This schema should be refreshed when major Claude Code versions are released. Check `reference/web-sources.md` for staleness thresholds.
