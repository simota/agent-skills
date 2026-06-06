# Hook Recipes

Purpose: Read this when you need a proven hook pattern, recipe ID, or stack-specific recipe combination.

For canonical matcher syntax, exit-code semantics, output schemas, and event contracts, see `hook-system.md` (§ Matcher Patterns, § Exit Codes, § Output Format, § Event Catalog). This file only references those rules and shows recipe-specific implementations.

## Contents

- [Recipe catalog](#recipe-catalog)
- [Security recipes](#security-recipes)
- [Quality recipes](#quality-recipes)
- [Context and workflow recipes](#context-and-workflow-recipes)
- [Tech stack sets](#tech-stack-sets)
- [Combining recipes](#combining-recipes)

## Recipe Catalog

| ID | Event | Matcher | Type | Use |
|----|-------|---------|------|-----|
| `S1` | `PreToolUse` | `Write|Edit` | `prompt` | Block writes to sensitive paths |
| `S2` | `PreToolUse` | `Bash` | `prompt` | Guard dangerous shell commands |
| `S3` | `PreToolUse` | `Write|Edit` | `command` | Detect secrets before file writes |
| `S4` | `PreToolUse` | `mcp__.*__delete.*` | `prompt` | Confirm risky MCP deletions |
| `Q1` | `Stop` | `*` | `prompt` | Require tests before stopping |
| `Q2` | `PostToolUse` | `Write|Edit` | `command` | Run linter after edits |
| `Q3` | `Stop` | `*` | `command` | Enforce a type-check gate |
| `Q4` | `Stop` | `*` | `prompt` | Require a successful build |
| `C1` | `SessionStart` | `*` | `command` | Detect project type and load context |
| `C2` | `PreCompact` | `*` | `command` | Preserve critical context before compaction |
| `W1` | `Notification` | `*` | `command` | Log notifications |
| `W2` | `PreToolUse` | `Bash` | `command` | Enable temporary strict mode via flag file |
| `W3` | `SessionStart` / `SessionEnd` | `*` | `command` | Keep a session audit trail |

## Security Recipes

### `S1`: File Write Security Validation

Use when writes must avoid system directories, `.env`, credentials, or traversal.

```json
{
  "PreToolUse": [
    {
      "matcher": "Write|Edit",
      "hooks": [
        {
          "type": "prompt",
          "prompt": "File path: $TOOL_INPUT.file_path. Verify: 1) Not in /etc or system directories 2) Not .env, credentials, or key files 3) Path does not contain .. traversal 4) Not overwriting critical config without reason. Return approve or deny with reason.",
          "timeout": 15
        }
      ]
    }
  ]
}
```

### `S2`: Bash Command Safety Validation

This is the most common safety recipe and must remain easy to discover.

```json
{
  "PreToolUse": [
    {
      "matcher": "Bash",
      "hooks": [
        {
          "type": "prompt",
          "prompt": "Command: $TOOL_INPUT.command. Check for: 1) rm -rf with broad paths 2) Destructive database commands 3) chmod 777 4) Network operations to unknown hosts 5) Package installs from untrusted sources. Return approve, deny, or ask.",
          "timeout": 15
        }
      ]
    }
  ]
}
```

### `S3`: Secret Leak Prevention

Keep this example because it is the canonical `stderr + exit 2 + permissionDecision: deny` pattern.

```json
{
  "PreToolUse": [
    {
      "matcher": "Write|Edit",
      "hooks": [
        {
          "type": "command",
          "command": "bash ~/.claude/hooks/check-secrets.sh",
          "timeout": 10
        }
      ]
    }
  ]
}
```

```bash
#!/bin/bash
set -uo pipefail
input=$(cat)
content=$(echo "$input" | jq -r '.tool_input.content // empty')

if [ -n "$content" ] && echo "$content" | grep -qiE '(api[_-]?key|password|secret|token|private[_-]?key)\s*[:=]\s*["\x27]?[A-Za-z0-9+/]{20,}'; then
  echo '{"hookSpecificOutput":{"permissionDecision":"deny"},"systemMessage":"Potential secret detected in content. Remove secrets before writing."}' >&2
  exit 2
fi

exit 0
```

### `S4`: MCP Delete Operation Guard

```json
{
  "PreToolUse": [
    {
      "matcher": "mcp__.*__delete.*",
      "hooks": [
        {
          "type": "prompt",
          "prompt": "MCP deletion detected. Verify intent, reversibility, and backups. Return ask unless the deletion is clearly safe.",
          "timeout": 15
        }
      ]
    }
  ]
}
```

## Quality Recipes

### `Q1`: Test Execution Enforcement

Keep this as the default `Stop` quality gate.

```json
{
  "Stop": [
    {
      "matcher": "*",
      "hooks": [
        {
          "type": "prompt",
          "prompt": "If code was modified, verify that tests were executed. If no tests ran after code changes, block with reason. Otherwise approve.",
          "timeout": 30
        }
      ]
    }
  ]
}
```

### `Q2`: Auto Lint After Edit

```json
{
  "PostToolUse": [
    {
      "matcher": "Write|Edit",
      "hooks": [
        {
          "type": "command",
          "command": "bash ~/.claude/hooks/auto-lint.sh",
          "timeout": 30
        }
      ]
    }
  ]
}
```

Use a file-extension switch inside the script so the hook exits quickly for unsupported files.

### `Q3`: Type Check Enforcement

```json
{
  "Stop": [
    {
      "matcher": "*",
      "hooks": [
        {
          "type": "command",
          "command": "bash ~/.claude/hooks/check-types.sh",
          "timeout": 60
        }
      ]
    }
  ]
}
```

Use when the project has a deterministic type-check command.

### `Q4`: Build Verification

```json
{
  "Stop": [
    {
      "matcher": "*",
      "hooks": [
        {
          "type": "prompt",
          "prompt": "If code was modified, verify that the project build succeeded. If no build ran after code changes, block and request a build step.",
          "timeout": 30
        }
      ]
    }
  ]
}
```

## Context and Workflow Recipes

### `C1`: Project Context Auto-Load

This is the canonical `SessionStart` context recipe and must stay discoverable.

```json
{
  "SessionStart": [
    {
      "matcher": "*",
      "hooks": [
        {
          "type": "command",
          "command": "bash ~/.claude/hooks/load-project-context.sh",
          "timeout": 10
        }
      ]
    }
  ]
}
```

Use `$CLAUDE_ENV_FILE` to persist variables such as `PROJECT_TYPE` and package-manager hints.

### `C2`: PreCompact Critical Info Preservation

Keep this example because it directly affects context-preserving behavior.

```json
{
  "PreCompact": [
    {
      "matcher": "*",
      "hooks": [
        {
          "type": "command",
          "command": "bash ~/.claude/hooks/preserve-context.sh",
          "timeout": 10
        }
      ]
    }
  ]
}
```

```bash
#!/bin/bash
project_file="$CLAUDE_PROJECT_DIR/.agents/PROJECT.md"

if [ -f "$project_file" ]; then
  content=$(head -50 "$project_file")
  echo "{\"systemMessage\":\"Critical project context (preserve through compaction): $content\"}"
fi

exit 0
```

### `W1`: Notification Logging

```json
{
  "Notification": [
    {
      "matcher": "*",
      "hooks": [
        {
          "type": "command",
          "command": "bash ~/.claude/hooks/log-notification.sh",
          "timeout": 5
        }
      ]
    }
  ]
}
```

### `W2`: Temporary Hook via Flag File

Keep this example because it is the main reversible strict-mode pattern.

```json
{
  "PreToolUse": [
    {
      "matcher": "Bash",
      "hooks": [
        {
          "type": "command",
          "command": "bash ~/.claude/hooks/strict-bash-check.sh",
          "timeout": 10
        }
      ]
    }
  ]
}
```

```bash
#!/bin/bash
FLAG_FILE="$CLAUDE_PROJECT_DIR/.enable-strict-validation"

if [ ! -f "$FLAG_FILE" ]; then
  exit 0
fi

input=$(cat)
command=$(echo "$input" | jq -r '.tool_input.command // empty')

if echo "$command" | grep -qE '\brm\b'; then
  echo '{"hookSpecificOutput":{"permissionDecision":"deny"},"systemMessage":"Strict mode: rm commands blocked. Remove .enable-strict-validation to disable."}' >&2
  exit 2
fi

exit 0
```

Usage:

```bash
touch .enable-strict-validation
rm .enable-strict-validation
# Restart Claude Code after changing the flag state
```

### `W3`: Session Audit Trail

Use paired `SessionStart` and `SessionEnd` command hooks to append session start/end lines to a shared log.

## Tech Stack Sets

Use stack sets as combinations of recipe IDs plus one or two stack-specific checks instead of copying large JSON blocks.

| Stack | Start with | Add these stack-specific checks |
|-------|------------|---------------------------------|
| Node.js / TypeScript | `C1 + S1 + S2 + Q1 + Q2 + Q4` | Guard `node_modules` and `dist`, avoid unsafe `npm publish`, add `Q3` for type-checking |
| Go | `C1 + S1 + Q2 + Q4` | Prevent `vendor/` edits, run `gofmt`, verify `go build`, `go test`, and `go vet` |
| Rust | `C1 + S1 + Q2 + Q4` | Avoid direct `Cargo.lock` edits, run `rustfmt`, verify `cargo check`, `cargo test`, and `clippy` |
| Python | `C1 + S1 + S2 + Q1 + Q2 + Q4` | Guard `.env`, `venv`, and `__pycache__`, run `ruff`, and verify `pytest` plus optional `mypy` |

## Combining Recipes

- Merge recipes by concatenating matcher groups under the same event.
- Keep recipe comments or IDs in the config so the purpose stays discoverable.
- Start with `1-2` recipes and add more gradually.
- Too many hooks can slow the workflow or create false positives.
