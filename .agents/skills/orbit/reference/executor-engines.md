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
portable_timeout "${EFFECTIVE_TIMEOUT}" bash -c "${EXEC_CMD}" 2>&1 | tee -a "${LOOP_DIR}/runner.log"
```

The whole `EXEC_CMD` string is parsed by Bash once, preserving quoted executable paths and multiword prompts. It is trusted operator-authored shell configuration and must never be populated from untrusted task text or model output. Prefer a wrapper script when constructing complex invocations; pass external text as quoted arguments within that wrapper.

Any executor must provide:

| Requirement | Why |
|-------------|-----|
| non-interactive mode | Orbit has no TTY |
| existing scoped grants; no unresolved prompts | loops cannot grant themselves permission |
| CWD-based operation | runner changes into project root first |
| process status plus actual completion evidence | `0` alone is not a passed DONE gate |
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

## Engine Quick Reference

Select the executor through `_common/CLI_COMPATIBILITY.md`. Orbit's loop contract requires an installed, authorized, noninteractive interface and an independent DONE gate; it does not require permission bypass. Verify the effective model/effort, tool grants, output schema and timeout behavior before freezing `EXEC_CMD`.

| Engine | Documented headless entry | Orbit integration |
|--------|---------------------------|-------------------|
| Codex | `codex exec` | Inherit approved model and sandbox; inspect structured result plus changed files |
| Antigravity | `agy -p` | Normal scoped grants; validate JSON/result, diagnostics and required artifacts |
| Claude Code | `claude -p` | Preauthorized narrowly scoped tools; validate result and external DONE gate |
| Gemini CLI / custom | Verify installed help | Do not assume agy flags or model IDs are interchangeable |

## Codex

### Recommended command

```bash
# Schematic, operator-authored configuration. Run only after approved grants are verified.
EXEC_CMD='codex exec "Read goal.md and complete its authorized task; report actual checks and blockers"'
```

### Key flags

Current model, effort, output, permission and workspace flags → `_common/CLI_COMPATIBILITY.md`. A loop cannot approve an action; a denied required action is a blocker, not a reason to disable the sandbox. Do not infer success from process exit alone.

### Cloud execution

Use only an explicitly selected, authorized cloud workflow supported by the installed CLI. Applying its patch remains subject to ownership, revision checks and the external DONE gate. Local skills/global settings may not transfer to a cloud worker.

## Antigravity (`agy`)

### Recommended command

```bash
# Normal headless execution; required tools must already have scoped authorization.
EXEC_CMD='agy -p "Read goal.md and complete its authorized task; report actual checks and blockers"'
```

### Key flags (verified against `agy --help` v1.0.0)

Legacy heading, **not a current flag matrix**. Resolve current supported flags in `_common/CLI_COMPATIBILITY.md` §3–§5 and §9.2. Structured output and per-call model selectors are documented in current releases; PTY/file capture is conditional on a reproduced legacy defect. Never automatically install plugins, harvest another run's transcript or treat a soft-denied tool as completed work.

## Claude Code

### Recommended commands

```bash
# Normal print mode under existing scoped permissions, not an unrestricted loop.
EXEC_CMD='claude -p "Read goal.md and complete its authorized task; report actual checks and blockers"'
```

### Key flags

Use the current compatibility adapter and installed help for structured capture, turn/budget limits and skill loading. A configured turn cap is not a monetary cap; a worktree is not a security sandbox. Keep the immutable Orbit contract and external loop limits even when native long-running execution is available.

## Engine Selection Guide

### Characteristics

Choose from verified tool access, model availability, structured results, isolated workspaces, resumability, measured task results and authorized cost. Do not assign universal speed/quality rankings to vendor names.

### Recommended Pairing

Light/Standard/Heavy/Marathon retain their existing timeout and budget contracts. Select a supported stable executor that satisfies those contracts; no generation is pinned here. If a required capability is missing, report the precise blocker or use the explicitly authorized fallback.

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
