# run-dash — Integration Spec

Defines the integration surface: how producers emit events, how Claude Code hooks auto-emit for any session, and how the dashboard auto-spawns. Coupling is one emit helper plus a few hook entries — never inside skills' business logic.

---

## 1. Integration Overview

```
┌────────────────────────────────────────────────────────────┐
│ Producers                                                   │
│  ├─ Nexus recipes (apex / feature / bug / refactor)        │
│  │    explicit emits at phase / step / gate boundaries      │
│  ├─ Codex CLI subagents                                     │
│  │    spawn scripts call run-emit.sh                        │
│  └─ Claude Code session generally                          │
│       PreToolUse / PostToolUse / SessionStart / Stop hooks │
└────────────────────────────────────────────────────────────┘
        │
        ▼
┌────────────────────────────────────────────────────────────┐
│ run-emit  shell helper                                     │
│  - args: kind, key=value...                                │
│  - writes: <repo>/.agents/run-dash/<run-id>/events.jsonl   │
└────────────────────────────────────────────────────────────┘
        │
        ▼
┌────────────────────────────────────────────────────────────┐
│ run-dash server (auto-spawned, port 5757+)                 │
└────────────────────────────────────────────────────────────┘
```

## 2. Emit Protocol

### 2.1 Helper

Implementation: `_common/scripts/run-emit.sh` (a copy ships with each generated dashboard).

```sh
run-emit <kind> [key=value]...

# Examples:
run-emit run_start run_kind=apex goal="passkey login" mode=AUTORUN_FULL scope=Standard
run-emit run_start run_kind=feature goal="add api key rotation" recipe=feature
run-emit run_start run_kind=manual goal="explore module"
run-emit phase_enter phase=P1_Discovery
run-emit agent_start agent=plea phase=P1_Discovery engine=claude_code parent_agent=nexus depth=1
run-emit agent_end   agent=plea status=done duration_ms=42000
run-emit risk_gate   verdict=Conditional-Go omen=pass ripple=conditional echo=pass
```

`apex-emit.sh` remains as a thin alias for backward compatibility.

### 2.2 Environment Variables

| Variable | Purpose | Default | Legacy |
|----------|---------|---------|--------|
| `RUN_ID` | run identifier; no-op when unset | unset | `APEX_RUN_ID` (still honoured) |
| `RUN_DASH_DIR` | output dir | `<repo>/.agents/run-dash` | `APEX_DASH_DIR` |
| `RUN_DASH_DISABLED` | `1` to disable all emits | unset | `APEX_DASH_DISABLED` |
| `RUN_REPO_ROOT` | repo root override | `git rev-parse --show-toplevel` | `APEX_REPO_ROOT` |
| `RUN_DASH_TOOLS` | `0` disables `tool_use` emits from hooks | `1` | — |

### 2.3 Operational Requirements

- Failures must not surface (run execution must not be impacted)
- Must finish within 100 ms (non-blocking)
- `seq` increments via mkdir lock under the run directory
- `ts` is ISO8601 UTC

### 2.4 Recipe Emit Points

#### apex

| When | Emit |
|------|------|
| Run start | `run_start run_kind=apex goal=… mode=… scope=…` |
| Phase enter / exit | `phase_enter phase=…` / `phase_exit phase=… exit_gate=…` |
| Subagent spawn / finish | `agent_start agent=… phase=… engine=… parent_agent=nexus depth=1` / `agent_end agent=… status=… duration_ms=…` |
| Risk Gate verdict | `risk_gate verdict=… omen=… ripple=… echo=…` |
| Engine boundary | `engine_switch from=claude_code to=codex_cli reason=phase6` |
| Checkpoint | `checkpoint_wait label=…` / `checkpoint_resolved label=… outcome=…` |
| Run end | `run_end status=completed duration_ms=…` |

#### feature

| When | Emit |
|------|------|
| Run start | `run_start run_kind=feature recipe=feature goal=…` |
| Step enter / exit | `step_enter meta.step=Spec` etc. |
| Spec gate | `spec_gate meta.verdict=pass meta.coverage=0.92` |
| Run end | `run_end status=… duration_ms=…` |

See `TOPOLOGIES/feature.md` for the full step list.

#### bug

| When | Emit |
|------|------|
| Run start | `run_start run_kind=bug recipe=bug goal=…` |
| RCA | `rca_done meta.cause_summary=…` |
| Fix proposed | `fix_proposed meta.diff_lines=… meta.touched_files=…` |
| Step enter / exit | `step_enter meta.step=Reproduce` / `RCA` / `Fix` / `Verify` |

See `TOPOLOGIES/bug.md`.

### 2.5 Codex CLI Side Emissions

Phase 6 (or any Codex run) crosses the engine boundary. Orbit's emit-script reuses `run-emit.sh` from the Codex working directory; it resolves `<repo>/.agents/run-dash/<run-id>/events.jsonl` correctly.

## 3. Auto-spawn Flow (pre-flight)

Insert before the first emit (or at recipe entry):

```
1. dash_root = "${RUN_REPO_ROOT}/.agents/run-dash-app"
2. if not exists(dash_root):
     spawn forge agent with prompt = GENERATION.md::§5
     wait until exists(dash_root + "/server/index.ts")
     run smoke test
     if smoke fails → emit error severity=fatal, abort dashboard but continue run
3. if not running(dash_root):
     spawn `bun run server/index.ts --repo=<root> --port=5757 --open`
        - background process
        - log to <dash_root>/.runtime.log
4. set RUN_ID = "<run_kind>-${date}-${shorthash}"
5. emit run_start run_kind=<kind> ...
```

Dashboard generation or spawn failure must not abort the run.

## 4. Claude Code Hooks (universal observability)

This is the path that lights up every Claude Code session without per-skill changes. Configure via the `update-config` skill:

```jsonc
// ~/.claude/settings.json
{
  "hooks": {
    "SessionStart": [
      {
        "command": "[ -z \"$RUN_ID\" ] && export RUN_ID=manual-$(date -u +%Y%m%d-%H%M%S)-$(uuidgen | head -c 7); _common/scripts/run-emit.sh run_start run_kind=manual goal=\"$CWD\""
      }
    ],
    "PreToolUse": [
      {
        "matcher": "Agent",
        "command": "_common/scripts/run-emit.sh agent_start agent=$AGENT_TYPE engine=claude_code parent_agent=$CALLER_AGENT depth=$AGENT_DEPTH"
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Agent",
        "command": "_common/scripts/run-emit.sh agent_end agent=$AGENT_TYPE status=$AGENT_STATUS duration_ms=$AGENT_DURATION_MS"
      },
      {
        "matcher": "Bash|Read|Write|Edit|Grep|Glob",
        "command": "[ \"${RUN_DASH_TOOLS:-1}\" = \"1\" ] && _common/scripts/run-emit.sh tool_use agent=$CURRENT_AGENT tool=$TOOL_NAME duration_ms=$TOOL_DURATION_MS"
      }
    ],
    "Stop": [
      {
        "command": "_common/scripts/run-emit.sh run_end status=completed"
      }
    ]
  }
}
```

> The exact env var names (`$AGENT_TYPE`, `$CALLER_AGENT`, `$AGENT_DEPTH`, `$CURRENT_AGENT`, `$TOOL_NAME`, …) follow Claude Code's hooks contract. Verify with the `latch` or `update-config` skill before rolling out. Where a variable isn't surfaced, the emit sends an empty value (consumer tolerates).

### 4.1 Disabling for Specific Sessions

```sh
RUN_DASH_DISABLED=1 claude   # one shot
```

```sh
RUN_DASH_TOOLS=0 claude      # skip per-tool emits, keep agent_start/end
```

### 4.2 Hook Performance Budget

- Each hook invocation < 100 ms wall time
- Helper is bash + a single append; ~5–15 ms typical
- For very chatty sessions, set `RUN_DASH_TOOLS=0` to halve the volume

## 5. File Layout and Permissions

| Path | Role | Notes |
|------|------|-------|
| `<repo>/.agents/run-dash/` | run data root | Add to `.gitignore` |
| `<repo>/.agents/run-dash/<run-id>/events.jsonl` | append-only log | 0644 |
| `<repo>/.agents/run-dash/<run-id>/postmortem.md` | generated on run_end | 0644 |
| `<repo>/.agents/run-dash-app/` | generated dashboard tree | per-repo decision |
| `<repo>/.agents/run-dash-app/.runtime.log` | server stdout/stderr | auto-removed after 7 days |
| `_common/scripts/run-emit.sh` | shared helper | used by recipes / hooks / Codex |
| `_common/scripts/apex-emit.sh` | thin alias | back-compat |

## 6. Suggested `.gitignore`

```gitignore
# run-dash
.agents/run-dash/
.agents/run-dash-app/.runtime.log
.agents/run-dash-app/node_modules/
.agents/run-dash-app/dist/
```

## 7. Minimal Edits to Recipes (design pointers only)

- `nexus/references/apex-recipe.md` — references RUN_ID alongside legacy APEX_RUN_ID
- `nexus/references/feature-recipe.md` — add a §"Live Dashboard Integration" referencing `TOPOLOGIES/feature.md`
- Same for bug / refactor

## 8. Test Considerations

- Helper no-ops when `RUN_ID` and `APEX_RUN_ID` are unset
- 5 concurrent producers writing 1,000 events produce no `seq` gaps
- Every line conforms to the `EVENTS.md` core schema
- Out-of-order `run_start` → UI shows warning
- Hooks-only flow produces a usable generic-mode timeline without manual emits

## 9. Related

- `EVENTS.md` — schema written by emits
- `UI.md §1` — mode selection by `run_kind`
- `GENERATION.md` — invoked by auto-spawn
- `POSTMORTEM.md` — generated on `run_end`
- `_common/scripts/run-emit.sh` — reference helper
- `_common/scripts/apex-emit.sh` — back-compat alias
