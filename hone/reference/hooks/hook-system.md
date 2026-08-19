# Claude Code Hook System Reference

Purpose: Read this when selecting a hook event, deciding between `prompt` and `command`, editing `settings.json`, or validating hook I/O and lifecycle rules.

## Contents

- [Configuration formats](#configuration-formats)
- [Event catalog](#event-catalog)
- [Hook types](#hook-types)
- [Matcher patterns](#matcher-patterns)
- [Input format](#input-format)
- [Output format](#output-format)
- [Environment variables](#environment-variables)
- [Lifecycle constraints](#lifecycle-constraints)

## Configuration Formats

Hone primarily manages the end-user `settings.json` format.

| Format | Location | Use |
|--------|----------|-----|
| `settings.json` | `~/.claude/settings.json` | Primary end-user hook configuration |
| `hooks.json` | `hooks/hooks.json` | Plugin-oriented configuration under a `{"hooks": {...}}` wrapper |

### `settings.json` Shape

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "bash ~/.claude/hooks/validate-bash.sh",
            "timeout": 10
          }
        ]
      }
    ]
  }
}
```

Structure rules:

- `hooks` lives at the top level.
- Each event key maps to an array of matcher groups.
- Each matcher group has `matcher` plus `hooks`.
- Each hook has `type`, `command` or `prompt`, and optional `timeout`.

## Event Catalog

Full 26-event lifecycle table (timing, block-capable, hook-type support, primary use) → `reference/hooks/event-catalog.md`. Always consult it before choosing an event.

### Event-Specific Contracts

| Event | Required input fields | Special output behavior |
|-------|-----------------------|-------------------------|
| `PreToolUse` | `tool_name`, `tool_input` | May return `permissionDecision` and `updatedInput` |
| `PostToolUse` | `tool_name`, `tool_input`, `tool_result` | Informational only; cannot block |
| `UserPromptSubmit` | `user_prompt` | May block the prompt |
| `Stop`, `SubagentStop` | `reason` | Uses `decision: approve|block` |
| `SessionStart` | Common fields only | Command-only; may write to `$CLAUDE_ENV_FILE` |
| `SessionEnd`, `PreCompact`, `PostCompact`, `Notification` | Common fields only | Command-only |
| `PermissionRequest` | `tool_name`, `tool_input`, `permission_suggestions` | May return `permissionDecision`; does not fire for subagent requests in Agent Teams |
| `SubagentStart` | `subagent_id`, common fields | Command-only; resource limits |
| `InstructionsLoaded` | Common fields only | Command-only |

### `PreToolUse` Blocking Example

```json
{
  "hookSpecificOutput": {
    "permissionDecision": "allow|deny|ask",
    "updatedInput": {"field": "modified_value"}
  },
  "systemMessage": "Explanation for Claude"
}
```

### `Stop` / `SubagentStop` Blocking Example

```json
{
  "decision": "approve|block",
  "reason": "Explanation",
  "systemMessage": "Additional context"
}
```

## Hook Types

### `prompt`

```json
{
  "type": "prompt",
  "prompt": "Evaluate whether this tool use is appropriate: $TOOL_INPUT",
  "timeout": 30
}
```

Use `prompt` for context-aware decisions, policy checks, and nuanced validation. It is supported only on `PreToolUse`, `PostToolUse`, `UserPromptSubmit`, `Stop`, and `SubagentStop`.

### `command`

```json
{
  "type": "command",
  "command": "bash /path/to/script.sh",
  "timeout": 60
}
```

Use `command` for fast deterministic checks, file operations, external tools, and all command-only events.

## Matcher Patterns

| Pattern | Example | Use |
|---------|---------|-----|
| Exact | `"Write"` | One tool only |
| OR | `"Read|Write|Edit"` | Small explicit tool family |
| Wildcard | `"*"` | Everything |
| Regex | `"mcp__.*__delete.*"` | Tool families such as MCP delete operations |

Common examples:

| Matcher | Matches |
|---------|---------|
| `"Write"` | `Write` only |
| `"Write|Edit"` | `Write` or `Edit` |
| `"Bash"` | `Bash` only |
| `"mcp__.*"` | All MCP tools |
| `"mcp__plugin_asana_.*"` | One plugin namespace |
| `"mcp__.*__delete.*"` | MCP delete operations |
| `"*"` | All tools or all events |

Matchers are case-sensitive.

## Input Format

All hooks receive JSON on stdin with common fields:

```json
{
  "session_id": "abc123",
  "transcript_path": "/path/to/transcript.txt",
  "cwd": "/current/working/dir",
  "permission_mode": "ask|allow",
  "hook_event_name": "PreToolUse"
}
```

## Output Format

### Standard Output

```json
{
  "continue": true,
  "suppressOutput": false,
  "systemMessage": "Message for Claude"
}
```

Output fields:

- `continue`: halt processing if `false`
- `suppressOutput`: hide output from transcript if `true`
- `systemMessage`: message injected into Claude's context

### Exit Codes

| Code | Meaning | Behavior |
|------|---------|----------|
| `0` | Success | Stdout appears in the transcript |
| `2` | Blocking error | Stderr is fed back to Claude |
| Other | Non-blocking error | Logged but does not block |

## Environment Variables

| Variable | Description | Availability |
|----------|-------------|--------------|
| `$CLAUDE_PROJECT_DIR` | Project root path | All command hooks |
| `$CLAUDE_PLUGIN_ROOT` | Plugin directory for portable paths | Plugin hooks |
| `$CLAUDE_ENV_FILE` | File used to persist environment variables | `SessionStart` only |
| `$CLAUDE_CODE_REMOTE` | Set when running remotely | All command hooks |

`SessionStart` can persist environment variables with:

```bash
echo "export PROJECT_TYPE=nodejs" >> "$CLAUDE_ENV_FILE"
```

## Lifecycle Constraints

### Load and Restart

- Hooks load only at session start.
- Editing hook configuration does not affect the current session.
- After changes: edit -> restart Claude Code -> verify with `/hooks`.

### Parallelism

- Matching hooks inside the same matcher group run in parallel.
- Hooks do not see each other's output.
- Ordering is non-deterministic.
- Design hooks to be independent.

### Startup Validation

- Invalid JSON prevents loading.
- Missing scripts cause warnings.
- Syntax errors surface in `claude --debug`.
- Use `/hooks` to confirm the active configuration.

### Timeout Defaults

- `prompt`: `30s`
- `command`: `60s`
- Production hooks should still set explicit `timeout` values.


---

# Hook Contract (full)

Canonical detail for the Hook Contract summarized in `SKILL.md`.

### Hook Types

| Type | Best for | Default timeout | Supported events |
|------|----------|-----------------|-----------------|
| `command` | Fast deterministic checks, scripts, and external tools | `600s` | All events |
| `prompt` | Context-aware or policy-heavy decisions | `30s` | Events with "All types? Yes" in Event Selection table |
| `http` | External service integration, audit logging to remote endpoints | `30s` | All events |
| `agent` | Multi-turn verification requiring tool access and deep reasoning | `60s` | Events with "All types? Yes" in Event Selection table |

Selection guidance: Start with `command` hooks for formatting and linting, graduate to `prompt` hooks for security and policy decisions, use `agent` hooks only for deep verification requiring tool access. Prefer `command` for latency-sensitive paths (target ≤ 200ms per hook). Use `http` for external audit trails and webhook integrations. Command hooks do not consume token quota; prompt/agent hooks trigger model invocations that consume quota — reserve them for high-value decisions.

When multiple hooks on the same event return different decisions, the strictest wins: `deny > defer > ask > allow` for PreToolUse; `deny > allow` for PermissionRequest. Identical command hooks (same command string) or HTTP hooks (same URL) matched by multiple matchers are deduplicated and run only once.

### Exit Codes

| Code | Meaning | Behavior |
|------|---------|----------|
| `0` | Success | Stdout parsed for JSON output fields |
| `2` | Blocking error | Stderr is fed back to Claude |
| Other | Non-blocking error | First line of stderr shown |

Hook output injected into context is capped at 10,000 characters; excess is saved to a file with a preview and path.

### Matcher Patterns

| Pattern | Example | Use |
|---------|---------|-----|
| Exact | `"Bash"` | One tool or event only |
| OR | `"Write|Edit"` | Small explicit set |
| Wildcard | `"*"` | All tools or all events |
| Regex | `"mcp__.*__delete.*"` | Family-wide matching such as MCP deletes |

Matchers are case-sensitive: `"write"` does not match `"Write"`.

### `settings.json` Structure

```text
settings.json
└── hooks
    └── Event[]
        └── { matcher, hooks[] }
            └── { type, prompt|command, timeout }
```

Structure rules:

- Edit only the top-level `hooks` section.
- Each event key maps to an array of matcher groups.
- Each matcher group contains one `matcher` string plus a `hooks` array.
- Hooks inside the same matcher group run in parallel.
- Validate with `jq . ~/.claude/settings.json` before finishing.

Hook sources (merged at runtime): `~/.claude/settings.json` (user), `.claude/settings.json` (project shared), `.claude/settings.local.json` (project local), managed policy settings (org-wide), plugin `hooks/hooks.json` (when enabled), skill/agent frontmatter (component lifetime). Hooks defined in skill/agent frontmatter are scoped to the component's lifetime and auto-cleaned up. Enterprise policy `allowManagedHooksOnly: true` blocks all non-managed hooks. `disableAllHooks: true` disables all hooks at the same or lower settings level.

### Common Hook Fields

| Field | Scope | Purpose |
|-------|-------|---------|
| `if` | Tool events | Conditional filter within matcher (e.g., `"if": "Bash(rm *)"` fires only for rm commands) |
| `async` | command/http | `true` runs the hook in background without blocking Claude's execution |
| `statusMessage` | All | Custom spinner text shown while hook runs |
| `once` | Skills/agents only | `true` runs hook once per session, not on every match |
| `timeout` | All | Override default timeout in seconds |

### Command Hook Rules

- Read stdin exactly once.
- On `exit 2`, write blocking JSON to stderr, not stdout.
- On `exit 0`, optional JSON to stdout is safe.
- Use `set -uo pipefail`; avoid `set -e`.
- Use PID-scoped temp files such as `/tmp/hook-state-$$`.
- Set explicit timeouts even when defaults would apply.

### Model-Based Gate Design

When a hook's decision cannot be expressed as a pattern (`security` / `quarantine` recipes reaching for an LLM judgment), copy the shipped auto-mode architecture rather than inventing one. Source: `anthropic.com/engineering/claude-code-auto-mode` (2026-03-25), measured FPR **0.4%** on 10,000 real actions, FNR **17%** on real overeager actions and **5.7%** on synthetic exfiltration.

| Principle | Rule |
|-----------|------|
| **Two-stage cascade** | Stage 1 = single-token classifier tuned to over-block (cheap, runs on every action). Stage 2 = chain-of-thought, invoked **only** on a Stage 1 flag. Never pay CoT latency on the common path. |
| **Starve the judge** | Feed the classifier the **user messages and the executable payload only**. Strip assistant messages, tool-call descriptions, and tool outputs. Anything the agent authored is an attack surface — it lets the agent argue its way past the gate. |
| **Tier before classify** | Tier 1 always-allow (reads, searches). Tier 2 auto-allow (in-project edits — version control is the undo). Tier 3 classify (shell, network, out-of-project paths, **subagent spawns**). Only Tier 3 pays for a model call. |
| **Denials are a tool result, not a crash** | Return the denial to the agent with "find a safer alternative". Then bound it: terminate the session at **3 consecutive** or **20 cumulative** denials and escalate to a human — an agent looping against a gate is a signal, not noise. |
| **Gate both directions on delegation** | Outbound: catch work that looks authorized inside the subagent but was never user-intended. Inbound: screen the subagent's result for injection before it re-enters the orchestrator's context. |

**Timing rule (`quarantine`).** Project-local config — `.claude/settings.json`, including its `hooks` block — must not be parsed until *after* the user's trust prompt is answered. Anthropic shipped this inverted and a repo could execute hook commands pre-consent. Any hook or tool that reads untrusted repo config inherits this ordering requirement. Related ordering bug: **resolve symlinks first, then validate containment** — "symlink resolution has to happen *before* path validation, not after, or a symlink inside an authorized folder can point outside and escape" (`anthropic.com/engineering/how-we-contain-claude`).

**Scope limit.** A hook is a *model-layer* control and never the sole defense. Environment controls (sandbox, egress policy) catch what a classifier misses: prompt-injection success is ~0.1% single-shot but **5-6% under 100 adaptive attempts**, and when the *user* is the one typing the hostile prompt, no intent-anchored classifier fires at all (credentials exfiltrated 24/25 times in Anthropic's own phishing test). Recommend sandboxing alongside any `security` hook — it independently removed 84% of permission prompts.



---

## Signal Keywords -> Recipe (full table)

For natural-language input without an explicit subcommand. Subcommand match wins if both apply. Signals not in the Recipes table map to a workflow focus or reference rather than a Recipe.

| Keywords | Maps to |
|----------|---------|
| `propose`, `design hook`, `what hook` | PROPOSE focus → `reference/hooks/hook-system.md` |
| `configure`, `add hook`, `settings.json` | `configure` |
| `debug`, `hook failing`, `hook slow`, `misfire`, `latency`, `hook performance` | `debug` |
| `pretool`, `updatedInput`, `modify input`, `rewrite`, `redact` | `pretool` |
| `posttool`, `async`, `background`, `non-blocking` | `posttool` |
| `notification`, `slack`, `discord`, `desktop alert` | `notification` |
| `session start`, `sessionstart`, `context injection`, `warm-up` | `sessionstart` |
| `security hook`, `block`, `deny`, `secret regex`, `mcp acl` | `security` |
| `quarantine`, `skill drift`, `plugin install gate`, `mcp rug-pull` | `quarantine` |
| `claudemd-update`, `claude.md proposer`, `should have known` | `claudemd-update` |
| `skill telemetry`, `skill usage`, `popular skill`, `under-trigger`, `usage log` | `skill-telemetry` |
| `quality gate`, `stop hook`, `completion gate` | Stop/SubagentStop → `reference/hooks/hook-recipes.md` |
| `webhook`, `http hook`, `audit log` | HTTP hook → `reference/hooks/hook-system.md` |
| `mcp governance`, `mcp audit` | MCP audit hook → `reference/hooks/hook-system.md` |
| `task hook`, `task naming` | TaskCreated/TaskCompleted → `reference/hooks/hook-system.md` |
| `config change`, `settings guard` | ConfigChange hook → `reference/hooks/hook-system.md` |
| `file watch`, `env change`, `reactive` | FileChanged/CwdChanged → `reference/hooks/hook-system.md` |
| `elicitation`, `mcp input`, `mcp prompt` | Elicitation/ElicitationResult → `reference/hooks/hook-system.md` |
| `worktree`, `git worktree` | WorktreeCreate/WorktreeRemove → `reference/hooks/hook-system.md` |
| `plugin hook`, `hooks.json` | Plugin hook → `reference/hooks/hook-system.md` |
| `conditional`, `if field`, `filter` | `if` field filtering → `reference/hooks/hook-system.md` |
| unclear hook request | PROPOSE focus → `reference/hooks/hook-system.md` |

