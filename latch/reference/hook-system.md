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

Latch primarily manages the end-user `settings.json` format.

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

| Event | Timing | Can block | Prompt hook | Primary use |
|-------|--------|-----------|-------------|-------------|
| `PreToolUse` | Before tool execution | Yes | Yes | Approve, deny, or modify tool calls |
| `PostToolUse` | After tool completion | No | Yes | Feedback, logging, post-action automation |
| `UserPromptSubmit` | When the user sends a prompt | Yes | Yes | Prompt validation or context injection |
| `Stop` | When the main agent considers stopping | Yes | Yes | Completion and quality gates |
| `SubagentStop` | When a subagent considers stopping | Yes | Yes | Subagent completion checks |
| `SessionStart` | When the session starts | No | No | Context loading and environment setup |
| `SessionEnd` | When the session ends | No | No | Cleanup, final logging, state save |
| `PreCompact` | Before context compaction | No | No | Preserve critical context |
| `Notification` | When Claude sends a notification | No | No | External forwarding and audit logging |
| `PermissionRequest` | When a permission dialog is about to show | Yes | No | Automated permission decisions (allow/deny) |
| `SubagentStart` | When a subagent starts | No | No | Subagent resource limits and task redirection |
| `PostCompact` | After context compaction | No | No | Post-compaction logging and state verification |
| `InstructionsLoaded` | After instructions are loaded | No | No | Instruction validation and augmentation |

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
