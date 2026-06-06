# Executor Engine Reference

Purpose: load this when selecting or changing `EXEC_CMD`. It defines the non-interactive requirements Orbit depends on and gives engine-specific command patterns.

## Contents

1. Shared executor requirements
2. Quick reference
3. Codex
4. Gemini
5. Claude Code
6. Engine selection
7. Custom executor
8. Troubleshooting

## Shared Executor Requirements

Orbit runs `EXEC_CMD` through `portable_timeout`:

```bash
portable_timeout "${EFFECTIVE_TIMEOUT}" ${EXEC_CMD} 2>&1 | tee -a "${LOOP_DIR}/runner.log"
```

Because `EXEC_CMD` is shell-expanded without quoting, the whole command string must already include the binary, flags, and prompt.

Any executor must provide:

| Requirement | Why |
|-------------|-----|
| non-interactive mode | Orbit has no TTY |
| auto-approval or no prompts | loops cannot answer confirmations |
| CWD-based operation | runner changes into project root first |
| standard exit codes | `0` success, non-zero failure |
| stdout/stderr output | runner logs through `tee` |
| SIGTERM handling | `portable_timeout` terminates hung runs |

### 3-Tier Timeout Architecture

Orbit enforces timeouts at three independent layers:

| Layer | Variable | Default | Scope | On timeout |
|-------|----------|---------|-------|------------|
| Tool | `TOOL_TIMEOUT` | `120s` | single tool/command invocation within executor | kill tool process, log `[TIMEOUT:TOOL]`, continue iteration |
| Iteration | `ITER_TIMEOUT` (alias: `EXEC_TIMEOUT`) | `600s` | one full iteration of the main loop | kill executor, log `[TIMEOUT:ITER]`, trigger retry policy |
| Loop | `LOOP_TIMEOUT` | `0` (unlimited) | entire loop execution from start to finish | graceful shutdown sequence (see `script-template-runner.md`) |

#### Layer Interaction

```text
┌─ Loop timeout (LOOP_TIMEOUT) ────────────────────────────┐
│  ┌─ Iteration timeout (ITER_TIMEOUT) ──────────────────┐  │
│  │  ┌─ Tool timeout (TOOL_TIMEOUT) ──┐                 │  │
│  │  │  single tool call              │                 │  │
│  │  └────────────────────────────────┘                 │  │
│  │  ┌─ Tool timeout (TOOL_TIMEOUT) ──┐                 │  │
│  │  │  another tool call             │                 │  │
│  │  └────────────────────────────────┘                 │  │
│  └─────────────────────────────────────────────────────┘  │
│  ┌─ Iteration timeout (ITER_TIMEOUT) ──────────────────┐  │
│  │  ...next iteration...                               │  │
│  └─────────────────────────────────────────────────────┘  │
└───────────────────────────────────────────────────────────┘
```

#### Tier-Specific Defaults

| Tier | `TOOL_TIMEOUT` | `ITER_TIMEOUT` | `LOOP_TIMEOUT` |
|------|----------------|----------------|----------------|
| Light | `60s` | `300s` | `3000s` |
| Standard | `120s` | `600s` | `12000s` |
| Heavy | `180s` | `900s` | `27000s` |
| Marathon | `240s` | `1200s` | `0` (unlimited) |

#### Fallback Behavior

| Timeout hit | Fallback action |
|-------------|-----------------|
| `TOOL_TIMEOUT` | log warning, skip tool result, let executor decide next action |
| `ITER_TIMEOUT` | kill executor, apply retry policy (transient classification) |
| `LOOP_TIMEOUT` | trigger graceful shutdown: save state → log partial results → cleanup → exit |

Note: `TOOL_TIMEOUT` is advisory — it requires executor-level support. Executors that do not support per-tool timeouts will rely on `ITER_TIMEOUT` as the effective boundary.

Recommended prompt pattern:

```bash
EXEC_CMD='codex exec --full-auto "Read goal.md and complete the task described in it"'
```

## Engine Quick Reference

| Engine | Base command | Non-interactive flag | Auto-approve flag | Model override | Output format |
|--------|--------------|----------------------|-------------------|----------------|---------------|
| Codex | `codex exec` | default | `--full-auto` | `-m <model>` (default: auto) | `--json` + `-o <path>` artifact. ⚠ Keep spawns **foreground** — detached-TTY silently crashes with no output (#19945, unfixed 0.137.0; `_common/CLI_COMPATIBILITY.md §9.3`) |
| Antigravity | `agy` | `-p "prompt"` | `--dangerously-skip-permissions` | not supported (always default) | not supported (pin schema in prompt) |
| Claude Code | `claude` | `-p "prompt"` | `--dangerously-skip-permissions` | `--model <model>` (default: auto) | `--output-format json` (capture via file redirect, not pipe — §9.3) |

All engines use their default model when no model flag is specified. Do not specify a model unless there is a specific reason to override the default.

## Codex

### Recommended command

```bash
EXEC_CMD='codex exec --full-auto "Read goal.md and complete the task described in it"'
```

### Key flags

| Flag | Required | Meaning |
|------|----------|---------|
| `--full-auto` | Yes | skip confirmations (workspace-write sandbox) |
| `-s <sandbox>` | No | `read-only` / `workspace-write` / `danger-full-access` |
| `-C <dir>` | No | override working directory |
| `--add-dir <dir>` | No | grant write access to additional directory |
| `--json` | No | JSONL structured output (exec mode) |
| `--search` | No | enable live web search |
| `--skip-git-repo-check` | No | allow non-git directories |
| `--ephemeral` | No | skip disk persistence |

Note: `--dangerously-skip-permissions` (`--dangerously-bypass-approvals-and-sandbox`) disables all safety checks including sandboxing. Use `--full-auto` for Orbit loops.

Model is not specified by default — Codex uses its own default model. Override with `-m <model>` only when needed.

### Cloud execution

```bash
codex cloud "Read goal.md and complete the task described in it" --attempts 2
codex apply <TASK_ID>
```

## Antigravity (`agy`)

### Recommended command

```bash
EXEC_CMD='agy -p "Read goal.md and complete the task described in it" --dangerously-skip-permissions'
```

### Key flags (verified against `agy --help` v1.0.0)

| Flag | Required | Meaning |
|------|----------|---------|
| `-p, --print, --prompt "<str>"` | Yes | Run a single prompt non-interactively and print the response |
| `--dangerously-skip-permissions` | Yes | Auto-approve all tool permission requests (Gemini CLI's `--yolo` is renamed to this) |
| `--sandbox` | No | Run in a sandbox with terminal restrictions enabled |
| `--add-dir <path>` | No | Add a directory to the workspace (repeatable) |
| `-c, --continue` | No | Continue the most recent conversation |
| `--conversation <id>` | No | Resume a previous conversation by ID |
| `-i, --prompt-interactive "<str>"` | No | Run an initial prompt interactively and continue the session |
| `--print-timeout <duration>` | No | Timeout for print mode wait (default 5m0s) |
| `--log-file <path>` | No | Override CLI log file path |

Subcommands: `changelog`, `help`, `install` (configure environment paths), `plugin` / `plugins` (list/install/uninstall/enable/disable/import/validate/link), `update`.

**Not supported in Antigravity CLI** (vs Gemini CLI): `--yolo` (renamed to `--dangerously-skip-permissions`), `-e`/`--extensions` (use `agy plugin install` instead), `--approval-mode`, `-m`/`--model`, `--include-directories` (use `--add-dir`), `--all-files`, `--allowed-tools`, `--checkpointing`.

**`--output-format <fmt>` — UNRELIABLE (re-verified 2026-06, v1.0.5)**: availability is inconsistent across installs ("flag not defined" reports) and no schema is documented. Do not depend on it. **stdout itself is also not a capture channel** — `agy -p` never flushes to non-TTY stdout even on success (issue #115, unfixed through v1.0.5). For any flow that must consume agy output, mandate an absolute-path artifact write + sentinel in the prompt and verify per `_common/CLI_COMPATIBILITY.md §9.2`; loop runners that verify goal completion via files/git state (not stdout) are unaffected.

**File context injection**: always reference files in the prompt with `@<path>` syntax (e.g. `@docs/spec.md`). Without `@`, agy treats the path as plain text and delegates the read to an internal subagent that hits the 60s timeout cap (v1.0.2 changelog: "restricted the default 60-second interaction timeout specifically to subagents"), producing the `exit 0 + empty stdout` silent-failure pattern.

**⚠ Pre-flight Notification (mandatory before first headless spawn)**: emit the canonical notification per `_common/CLI_COMPATIBILITY.md §9.1`. Recommends `/update-config` to allowlist the Bash pattern in `settings.json` `permissions.allow`. Required because the agy autonomous loop + Claude Code Bash spawn combine into a two-layer approval-gate bypass.

Authentication: resolved from the Google login session (interactive `agy` launch). No `agy auth login/logout/status` subcommands — manage via the IDE/CLI launch flow.

Context file: `GEMINI.md` in project root for persistent instructions (Antigravity CLI continues to read this file).

## Claude Code

### Recommended commands

Full autonomy:

```bash
EXEC_CMD='claude -p "Read goal.md and complete the task described in it" --dangerously-skip-permissions'
```

Restricted tools:

```bash
EXEC_CMD='claude -p "Read goal.md and complete the task described in it" --dangerously-skip-permissions --allowedTools "Read,Write,Edit,Bash,Glob,Grep"'
```

Budget-constrained:

```bash
EXEC_CMD='claude -p "Read goal.md and complete the task described in it" --dangerously-skip-permissions --max-budget-usd 5.00'
```

Turn-limited:

```bash
EXEC_CMD='claude -p "Read goal.md and complete the task described in it" --dangerously-skip-permissions --max-turns 10'
```

### Key flags

| Flag | Required | Meaning |
|------|----------|---------|
| `-p "prompt"` | Yes | non-interactive (print) mode |
| `--dangerously-skip-permissions` | Yes | skip all permission prompts |
| `--allowedTools "Tool1,Tool2"` | No | auto-approve specific tools only |
| `--disallowedTools "Tool1"` | No | block specific tools |
| `--max-budget-usd <amount>` | No | cost cap per session — ⚠ absent from the current headless docs (2026-06 re-verification); confirm via `claude --help` before relying on it in a loop contract |
| `--max-turns <N>` | No | limit agent turns — ⚠ same caveat as `--max-budget-usd` |
| `--output-format <fmt>` | No | `text` / `json` / `stream-json` — capture via **file redirect**, not pipe (64KB pipe truncation + stream-json block-buffering; `_common/CLI_COMPATIBILITY.md §9.3`) |
| `--json-schema <schema>` | No | enforce structured output via JSON Schema |
| `--effort <level>` | No | `low` / `medium` / `high` / `max` (Opus only) |
| `--add-dir <dir>` | No | additional working directories |
| `-w, --worktree` | No | execute in isolated git worktree |
| `--append-system-prompt <text>` | No | append to default system prompt |
| `--mcp-config <file>` | No | load MCP server configuration |
| `--fallback-model <model>` | No | fallback on overload |

Model is not specified by default — Claude Code uses its own default model. Override with `--model <model>` (aliases: `sonnet`, `opus`) only when needed.

Note: `--permission-mode bypassPermissions` is deprecated. Use `--dangerously-skip-permissions` for non-interactive loops.

## Engine Selection Guide

### Characteristics

| Aspect | Codex | Gemini | Claude Code |
|--------|-------|--------|-------------|
| strength | code generation and refactoring | broad general execution | agentic execution and tool use |
| speed | fast | moderate | moderate |
| cost | low to medium | low to medium | medium to high |
| autonomy | high | high | high |
| sandbox | Seatbelt/Landlock | Docker/Podman | git worktree |
| structured output | `--json` (JSONL) + `-o <path>` artifact | prompt-mandated artifact file per `CLI_COMPATIBILITY.md §9.2` (`--output-format json` unreliable; stdout never flushes to non-TTY) | `--output-format json/stream-json` |
| budget control | — | — | `--max-budget-usd`, `--max-turns` |
| special control | cloud exec, MCP server | approval modes, extensions | tool restrictions, effort levels, agents |

### Recommended Pairing

| Loop tier | Recommended engine | Rationale |
|-----------|--------------------|-----------|
| Light | Codex | fastest turnaround |
| Standard | Codex or Claude | balanced speed and capability |
| Heavy | Claude or Codex | stronger reasoning for complex tasks |
| Marathon | Claude with `--max-budget-usd` | predictable long-run cost |

All pairings use each engine's default model. Override only when the default does not meet the task's requirements.

## Custom Executor

Any custom executor is acceptable if it:
- accepts the prompt as part of the command string
- writes to stdout/stderr
- returns standard exit codes
- handles SIGTERM
- runs without prompts

Example wrapper:

```bash
EXEC_CMD='/path/to/my-executor.sh "Read goal.md and complete the task"'
```

```bash
#!/usr/bin/env bash
set -euo pipefail
my-ai-tool --no-interactive --prompt "$1"
```

## Common Troubleshooting

| Problem | Cause | Fix |
|---------|-------|-----|
| timeout kills useful work | `EXEC_TIMEOUT` too short | increase timeout or enable `ADAPTIVE_TIMEOUT=true` |
| malformed prompt | quoting problem in `EXEC_CMD` | use single quotes outside, double quotes inside |
| API key error | key not exported into loop shell | export the key in the same shell or source an env file |
| success treated as failure | non-standard exit codes | normalize through a wrapper script |
| tool call hangs indefinitely | no per-tool timeout | set `TOOL_TIMEOUT` and ensure executor supports it |
| loop runs too long without progress | no loop-level timeout | set `LOOP_TIMEOUT` to bound total execution time |
