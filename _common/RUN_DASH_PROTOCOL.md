# RUN_DASH_PROTOCOL — Universal Observability Contract

How every skill, recipe, and hook coordinates with run-dash so that any agent run is automatically observable. Read this **once** to understand who is responsible for which event; then each layer (hook, recipe, sub-agent) follows the table here without duplication.

> Spec authority: this file is the agent-side contract. The dashboard, schema, and topologies live under `_common/run-dash/`. The shell helper is `_common/scripts/run-emit.sh` (alias `apex-emit.sh` retained for compat).

---

## 1. Architectural Layers

```
┌──────────────────────────────────────────────────────────────┐
│ L1  Claude Code hooks  (settings.json)                        │
│      SessionStart  →  run_start (run_kind=manual)             │
│      PreToolUse:Agent → agent_start                           │
│      PostToolUse:Agent → agent_end                            │
│      PostToolUse:Bash|Read|… → tool_use                       │
│      Stop → run_end                                           │
├──────────────────────────────────────────────────────────────┤
│ L2  Recipe orchestrators (Nexus apex / feature / bug / …)    │
│      Override RUN_ID for the recipe                           │
│      Emit phase / step / risk_gate / spec_gate / orbit_iter   │
│      Restore parent RUN_ID on completion                      │
├──────────────────────────────────────────────────────────────┤
│ L3  Specialist agents (plea / accord / atlas / builder / …)  │
│      DO NOT emit directly                                     │
│      L1 hooks already capture every Agent invocation          │
└──────────────────────────────────────────────────────────────┘
```

The cardinal rule: **never instrument L3 individually**. Adding `run-emit` calls inside specialist skills creates duplicate `agent_start` events and tightens coupling for no observable benefit.

## 2. Responsibility Matrix

| Event | Layer | Notes |
|-------|-------|-------|
| `run_start` (run_kind=manual) | L1 SessionStart | Auto for every Claude Code session |
| `run_start` (run_kind=apex/feature/bug/…) | L2 recipe orchestrator | Overrides session-level run for the recipe |
| `run_end` | L1 Stop OR L2 recipe (whoever started it) | Match the layer that emitted run_start |
| `agent_start` / `agent_end` | L1 PreToolUse:Agent / PostToolUse:Agent | Universal |
| `agent_progress` | L2 / L3 (optional) | Long-running agents may emit explicitly |
| `tool_use` | L1 PostToolUse:Bash\|Read\|Write\|Edit\|Grep\|Glob | ON/OFF via `RUN_DASH_TOOLS=0` |
| `phase_enter` / `phase_exit` | L2 (apex) | Drives Phase rail |
| `step_enter` / `step_exit` | L2 (feature/bug/refactor) | Drives Step rail |
| `risk_gate` | L2 (apex) | After omen/ripple/echo |
| `spec_gate` | L2 (feature) | After accord |
| `rca_done` / `fix_proposed` | L2 (bug) | After scout / builder |
| `orbit_iter` | L2 (orbit sub-orchestrator) | Each loop iteration |
| `engine_switch` | L2 (apex Phase 6 boundary) | claude_code → codex_cli |
| `checkpoint_wait` / `checkpoint_resolved` | L2 (recipe with human gates) | apex Phase 0, etc. |
| `error` | L1 Stop on abnormal exit, L2 on guarded failure | Don't double-emit |
| `note` | Any layer | Free-form annotation |

## 3. Environment Contract

Every layer reads / writes the same env conventions:

| Variable | Meaning | Set by |
|----------|---------|--------|
| `RUN_ID` | Active run identifier | L1 SessionStart (manual-…), L2 overrides (apex-…/feature-…) |
| `RUN_DASH_DIR` | Events root | L1 SessionStart (default `~/.claude/run-dash`) |
| `RUN_DASH_DISABLED=1` | Skip all emits this session | User per-session opt-out |
| `RUN_DASH_TOOLS=0` | Skip per-tool emits (keep agent_start/end) | User opt-out |
| `RUN_REPO_ROOT` | Repo root override | rare, mainly for tests |

Legacy aliases (`APEX_RUN_ID`, `APEX_DASH_DIR`, `APEX_DASH_DISABLED`, `APEX_REPO_ROOT`) remain honoured by `run-emit.sh`.

## 4. Recipe Override Pattern

When a recipe (apex / feature / bug / refactor) starts, it must:

```sh
# 1. Save the session-level run-id (if any)
PARENT_RUN_ID="${RUN_ID:-}"

# 2. Issue a recipe-scoped run-id
export RUN_ID="<run_kind>-$(date -u +%Y%m%d-%H%M%S)-$(uuidgen | head -c 7 | tr A-Z a-z)"

# 3. Emit run_start with run_kind / project / recipe / goal
PROJECT=$(basename "$(git rev-parse --show-toplevel 2>/dev/null || pwd)")
run-emit.sh run_start run_kind=<kind> project="$PROJECT" goal="$GOAL" recipe=<kind>

# 4. ... recipe execution, emitting phase/step/gate events ...

# 5. Emit run_end
run-emit.sh run_end status=completed duration_ms=$(( ($(date +%s) - START_S) * 1000 ))

# 6. Restore parent run-id (so subsequent hook events go back to the manual run)
if [ -n "$PARENT_RUN_ID" ]; then
  export RUN_ID="$PARENT_RUN_ID"
else
  unset RUN_ID
fi
```

Both runs end up under `RUN_DASH_DIR` and can be replayed independently in the dashboard.

## 5. What Specialist Agents (L3) Must NOT Do

- Do **not** call `run-emit.sh` from inside a specialist SKILL.md
- Do **not** read `RUN_ID` to log into events.jsonl directly
- Do **not** write to the dashboard's events directory

The only legitimate per-agent emit case is `agent_progress` for **multi-minute** long-running specialists (e.g. orbit, voyager) that want to surface partial progress; even then, prefer letting the recipe orchestrator drive it.

## 6. What Hooks (L1) Must Do — Minimum Viable Set

Configured via `update-config` skill in `~/.claude/settings.json`:

| Event | Hook | Behaviour |
|-------|------|-----------|
| SessionStart | `~/.claude/hooks/run-dash-session-start.sh` | Issue manual RUN_ID, persist to shared state, emit `run_start` |
| PreToolUse (Agent) | `~/.claude/hooks/run-dash-pre-tool.sh` | Read RUN_ID, emit `agent_start` |
| PostToolUse (Agent) | `~/.claude/hooks/run-dash-post-tool.sh` | Emit `agent_end` |
| PostToolUse (Bash\|Read\|Write\|Edit\|Grep\|Glob) | same script, branch on tool name | Emit `tool_use` (when `RUN_DASH_TOOLS != 0`) |
| Stop | `~/.claude/hooks/run-dash-stop.sh` | Emit `run_end` |

Reference scripts ship under `~/.claude/hooks/run-dash-*.sh` (see R2 of the run-dash work). Hook env-var naming may shift between Claude Code versions; verify via the `latch` skill.

## 7. State Sharing Between Hooks

SessionStart sets RUN_ID, but it doesn't persist to the parent shell. To let PreToolUse / PostToolUse / Stop find the same RUN_ID, the hooks use **shared state files**:

```
~/.claude/run-dash/
  .current-run-id        # plain text, current RUN_ID
  .current-project       # plain text, current project
  .current-agent         # plain text, name of innermost active Agent (for tool_use)
```

Each hook reads / writes these. They are best-effort — concurrent sessions can race, but personal use rarely hits this.

## 8. Concurrency and Multiple Sessions

Each Claude Code session starts its own SessionStart hook → its own `manual-…` RUN_ID. The shared-state files above are last-write-wins. For users with multiple parallel sessions, prefer:

- one dashboard, distinct run-ids per session (current default)
- per-session state files (`~/.claude/run-dash/.session-<sid>.run-id`) — see R5 follow-up

## 9. Failure Behaviour

`run-emit.sh` is silent on every failure. The contract:

- If the dashboard server is down → events still queue in `events.jsonl`; dashboard catches up on next start
- If `events.jsonl` write fails (disk full, perms) → emit silently drops, run continues
- If RUN_ID is unset → emit no-ops
- If a hook script is missing → Claude Code logs but proceeds

There is **never** a path where instrumentation aborts a run.

## 10. Verification

After hook configuration, test the loop end-to-end:

```sh
# 1. Open the dashboard
cd ~/.claude/skills/_common/run-dash/sample
RUN_DASH_EVENTS_DIR=$HOME/.claude/run-dash bun run dev

# 2. Start a Claude Code session in some repo
cd ~/some-repo && claude

# 3. Within the session, ask Claude to call any subagent (e.g. "run lens on this repo")

# 4. In the browser, the Run picker should show:
#    [some-repo] manual-YYYYMMDD-…  · manual
#    Selecting it should display lens as agent_start → agent_end with tool_use ticks.

# 5. Run a recipe to verify L2 override:
#    /nexus apex
#    The picker gains [some-repo] apex-YYYYMMDD-… · apex
```

Use the `latch` skill (`/latch verify`) to confirm hook env-var names map onto Claude Code's runtime.

## 11. Related

- `_common/run-dash/INTEGRATION.md §9` — Global Usage runbook
- `_common/run-dash/EVENTS.md` — wire format
- `_common/run-dash/TOPOLOGIES/*.md` — how recipe events map to UI
- `_common/scripts/run-emit.sh` — emit helper
- `nexus/references/apex-recipe.md §13` — apex recipe emit checklist
- `nexus/references/feature-recipe.md` — feature recipe emit checklist
- `nexus/references/bug-recipe.md` — bug recipe emit checklist
