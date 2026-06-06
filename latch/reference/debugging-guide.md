# Hook Debugging Guide

Purpose: Read this when validating a hook change, debugging a hook failure, or implementing a command hook script safely.

## Contents

- [Debug flow](#debug-flow)
- [Command hook contract](#command-hook-contract)
- [Manual tests](#manual-tests)
- [Failure patterns](#failure-patterns)
- [Troubleshooting checklist](#troubleshooting-checklist)

## Debug Flow

Use this sequence in order:

1. Validate `~/.claude/settings.json` with `jq . ~/.claude/settings.json`.
2. Restart Claude Code because hooks load only at session start.
3. Run `/hooks` to confirm the hook is registered on the expected event and matcher.
4. Run `claude --debug` to inspect registration, execution logs, timing, and parse failures.
5. Test the script manually with realistic stdin JSON.
6. Check the exit code and validate any JSON output with `jq .`.

## Command Hook Contract

### Standard Boilerplate

```bash
#!/bin/bash
set -uo pipefail
# Do not use set -e; handle exit codes explicitly.

input=$(cat)

# Parse fields with jq
tool_name=$(echo "$input" | jq -r '.tool_name // empty')
tool_input=$(echo "$input" | jq -r '.tool_input // empty')

# Validation logic here

if [ "${should_block:-false}" = "true" ]; then
  echo '{"hookSpecificOutput":{"permissionDecision":"deny"},"systemMessage":"Reason for blocking"}' >&2
  exit 2
fi

exit 0
```

### Rules

- Read stdin exactly once.
- Use stderr for blocking JSON and debug prints.
- Use stdout only for non-blocking JSON.
- Use PID-scoped temp files such as `/tmp/hook-state-$$`.
- Avoid shared mutable state because hooks in one matcher group run in parallel.

## Manual Tests

### `PreToolUse` Command Hook

```bash
echo '{"tool_name":"Bash","tool_input":{"command":"rm -rf /tmp/old"},"session_id":"test","cwd":"/tmp","hook_event_name":"PreToolUse"}' \
  | bash ~/.claude/hooks/your-hook.sh
echo "Exit code: $?"
```

### `PostToolUse` Command Hook

```bash
echo '{"tool_name":"Write","tool_input":{"file_path":"src/main.ts"},"tool_result":"File written successfully","hook_event_name":"PostToolUse"}' \
  | bash ~/.claude/hooks/your-hook.sh
```

### `SessionStart` Command Hook

```bash
CLAUDE_PROJECT_DIR=/home/user/project \
CLAUDE_ENV_FILE=/tmp/test-env \
bash ~/.claude/hooks/load-project-context.sh
```

### Validate JSON Output

```bash
output=$(echo '{"tool_name":"Write","tool_input":{"file_path":"/tmp/test.txt"}}' | bash ~/.claude/hooks/your-hook.sh)
echo "$output" | jq .
```

## Failure Patterns

| Failure | Symptom | Fix |
|---------|---------|-----|
| Hook not executing | No observable effect | Restart the session, validate JSON, confirm matcher case, confirm hook nesting under `hooks` |
| JSON parse error | `claude --debug` shows malformed output | Send only JSON to stdout, move debug output to stderr, escape quotes and newlines |
| Timeout | Hook is killed before completion | Add explicit `timeout`, reduce I/O, add command timeouts such as `curl --max-time 5` |
| Exit code mismatch | Hook blocks or passes unexpectedly | `0` means success, `2` means block, other codes are non-blocking errors |
| Parallel execution issue | Flaky or inconsistent behavior | Remove shared state, avoid order assumptions, use PID-scoped temp files |

### `set -e` Trap

`set -e` is unsafe for hook scripts because a failing command produces `exit 1`, which is a non-blocking error instead of an intentional block. Use explicit conditionals and explicit `exit 2` when blocking is required.

## Troubleshooting Checklist

1. `jq . ~/.claude/settings.json`
2. Restart Claude Code
3. `/hooks`
4. `claude --debug`
5. Manual stdin test
6. `echo $?`
7. `jq .` on the hook output
8. `chmod +x script.sh`
9. Verify the shebang is `#!/bin/bash`
10. Confirm blocking JSON goes to stderr
