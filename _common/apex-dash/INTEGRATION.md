# apex-dash — Integration Spec

Defines the integration surface with the apex skill family. **Coupling is limited to a single emit helper** and never touches apex business logic. Following this spec, Nexus apex requires only minimal additions to operate the dashboard in a loosely-coupled fashion.

---

## 1. Integration Overview

```
┌────────────────────────────────────────────────────────────┐
│ Nexus apex (orchestrator)                                  │
│  ├─ pre-flight: ensure_dashboard()        ← §3             │
│  ├─ on phase_enter / phase_exit           ← §2 emit        │
│  ├─ on risk_gate / engine_switch          ← §2 emit        │
│  └─ on checkpoint                          ← §2 emit        │
└────────────────────────────────────────────────────────────┘
        │
        │ Claude Code PostToolUse hook
        ▼
┌────────────────────────────────────────────────────────────┐
│ apex-emit  shell helper                                    │
│  - args: kind, key=value...                                │
│  - writes: <repo>/.agents/apex/<run-id>/events.jsonl       │
└────────────────────────────────────────────────────────────┘
        │
        │ chokidar tail
        ▼
┌────────────────────────────────────────────────────────────┐
│ apex-dash server (auto-spawned, port 5757+)                │
└────────────────────────────────────────────────────────────┘
```

## 2. Emit Protocol

### 2.1 Helper Spec

Implementation: `_common/scripts/apex-emit.sh` (a copy of equivalent logic ships with each generated dashboard).

```sh
apex-emit <kind> [key=value]...
# examples:
apex-emit phase_enter phase=P1_Discovery
apex-emit agent_start agent=plea phase=P1_Discovery engine=claude_code
apex-emit agent_end   agent=plea status=done duration_ms=42000
apex-emit risk_gate   verdict=Conditional-Go omen=pass ripple=conditional echo=pass
apex-emit error       severity=warn source=hook message="seq gap detected"
```

### 2.2 Environment Variables

| Variable | Purpose | Default |
|----------|---------|---------|
| `APEX_RUN_ID` | run-id, exported when Nexus apex begins | (no-op when unset) |
| `APEX_DASH_DIR` | Base output directory for events | `<repo>/.agents/apex` |
| `APEX_REPO_ROOT` | Repo root (resolved via `git rev-parse --show-toplevel`) | auto |
| `APEX_DASH_DISABLED` | `1` disables all emissions | unset |

### 2.3 Operational Requirements

- Failures must not surface (apex execution must not be impacted)
- Must finish within 100ms (non-blocking)
- `seq` increments via atomic update of `.agents/apex/<run-id>/.seq`
- Concurrent writes: short-lived `flock` on `events.jsonl` only during append
- `ts` is generated as ISO8601 UTC

### 2.4 Emit Points (Nexus apex side)

| When | Call |
|------|------|
| Apex starts | `apex-emit run_start goal="..." mode=AUTORUN_FULL scope=Standard` |
| Phase enter | `apex-emit phase_enter phase=P1_Discovery` |
| Phase exit | `apex-emit phase_exit phase=P1_Discovery exit_gate=pass` |
| Before subagent spawn | `apex-emit agent_start agent=plea phase=P1_Discovery engine=claude_code` |
| After subagent finishes | `apex-emit agent_end agent=plea status=done duration_ms=...` |
| After Risk Gate | `apex-emit risk_gate verdict=... omen=... ripple=... echo=...` |
| Before engine boundary | `apex-emit engine_switch from=claude_code to=codex_cli reason=phase6` |
| Checkpoint begins | `apex-emit checkpoint_wait label=Phase0_boundary_confirm deadline=... mode=AUTORUN_FULL_60s` |
| Checkpoint resolved | `apex-emit checkpoint_resolved label=... outcome=timeout_passed` |
| Apex ends | `apex-emit run_end status=completed duration_ms=...` |

### 2.5 Codex CLI Side Emissions

Phase 6 crosses into Codex CLI. Orbit's emitted scripts call **the same `apex-emit.sh`** from inside Codex's working directory; the relative path `<repo>/.agents/apex/<run-id>/events.jsonl` resolves correctly.

| Before Codex spawn | `apex-emit agent_start agent=builder phase=P6_Implementation engine=codex_cli` |
| After Codex spawn | `apex-emit agent_end agent=builder status=done duration_ms=...` |
| Per orbit iter | `apex-emit orbit_iter iter=3 convergence=0.72 cost_per_task=0.41 budget_used=12.4 budget_max=50 circuit=green` |

## 3. Auto-spawn Flow (pre-flight)

Insert the following step **just before Phase 0 (or Phase 1)** in Nexus apex.

```
1. dash_root = "${APEX_REPO_ROOT}/.agents/apex-dash"
2. if not exists(dash_root):
     spawn forge agent with prompt = GENERATION.md::§5 (template)
     wait until exists(dash_root + "/server/index.ts")
     run smoke test (port listening, /api/state returns 200)
     if smoke fails → emit error severity=fatal, abort dashboard but continue apex
3. if not running(dash_root):
     spawn `bun run server/index.ts --repo=<root> --port=5757 --open`
        - background process
        - log to <dash_root>/.runtime.log
4. set APEX_RUN_ID = "apex-${date}-${shorthash}"
5. emit run_start
```

**Important**: dashboard generation or spawn failure must not abort apex. The dashboard is purely optional.

### 3.1 Spec-Version Consistency Check

If `<dash_root>/.spec-version` does not match the current commit hash of `_common/apex-dash/`, log a `note` to `events.jsonl` warning of the drift, and continue with the existing version unless the user passes `--regenerate`.

## 4. Claude Code Hooks (optional)

The primary integration is explicit emits inside Nexus apex. As an optional supplement, Claude Code hooks can be wired via the `update-config` skill into `settings.json`.

### 4.1 PostToolUse Hook (optional)

Use this only if you want to emit `tool_use` per tool call. **Disabled by default** to avoid UI saturation.

```jsonc
// ~/.claude/settings.json (example)
{
  "hooks": {
    "PostToolUse": [
      {
        "command": "_common/scripts/apex-emit.sh tool_use agent=$AGENT tool=$TOOL_NAME",
        "when": "env.APEX_RUN_ID != ''"
      }
    ],
    "Stop": [
      {
        "command": "_common/scripts/apex-emit.sh run_end status=completed",
        "when": "env.APEX_RUN_ID != ''"
      }
    ]
  }
}
```

In practice, calling `apex-emit` from inside Nexus apex is **simpler and safer**. Hooks are auxiliary.

## 5. File Layout and Permissions

| Path | Role | Notes |
|------|------|-------|
| `<repo>/.agents/apex/` | Root for run data | Add to `.gitignore` |
| `<repo>/.agents/apex/<run-id>/events.jsonl` | Append-only log | 0644 |
| `<repo>/.agents/apex/<run-id>/state.json` | Snapshot (optional) | Server can rebuild |
| `<repo>/.agents/apex-dash/` | Generated dashboard tree | `.gitignore` decision is per project |
| `<repo>/.agents/apex-dash/.runtime.log` | Server stdout/stderr | Auto-removed after 7 days |
| `_common/scripts/apex-emit.sh` | Shared helper in this skill repo | Common utility |

## 6. Suggested `.gitignore` Additions

```gitignore
# apex-dash
.agents/apex/
.agents/apex-dash/.runtime.log
.agents/apex-dash/node_modules/
.agents/apex-dash/dist/
```

Whether to ignore `.agents/apex-dash/` itself is a per-repo decision (commit it if the team wants to share the dashboard configuration).

## 7. Minimal Edits to Nexus Apex (design pointers only)

Actual code changes are deferred to a separate task; pointers are recorded here.

- Add **§13 Live Dashboard Integration** to `nexus/reference/apex-recipe.md` and reference this document
- Insert one-line `emit phase_enter ...` calls at the top of each phase description in `nexus/reference/apex-walkthrough.md`
- Annotate the Output Routing table in `nexus/SKILL.md`: "When `/nexus apex` starts, run dashboard pre-flight"
- No new skills or new references are required

## 8. Test Considerations

Validate the emit helper and end-to-end consistency:

- Helper is a no-op when `APEX_RUN_ID` is unset
- 5 concurrent producers writing 1,000 events produce no `seq` gaps
- Every line conforms to the `EVENTS.md` schema
- If events arrive without `run_start`, the UI displays a warning but continues to render

## 9. Related

- `EVENTS.md` — schema written by emits
- `GENERATION.md` — generation prompt invoked by auto-spawn
- `DESIGN.md §3` — overall architecture
- `POSTMORTEM.md` — postmortem generation triggered by `run_end`
- `_common/scripts/apex-emit.sh` — reference helper implementation
