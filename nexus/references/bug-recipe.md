# Nexus Bug Recipe Reference

**Purpose:** 4-step chain for bug investigation, fix, and verification.
**Read when:** User invokes `/nexus bug` or reports a bug with reproduction details.

---

## Steps

| Step | Purpose | Primary agents |
|------|---------|----------------|
| **Reproduce** | Confirm reproduction + minimal repro | scout, triage (if severity ≥ high) |
| **RCA** | Root-cause analysis | scout (RCA mode), trail (regression), specter (concurrency) |
| **Fix** | Patch + tests | builder, judge, radar |
| **Verify** | Regression checks + ship | voyager (if UI), guardian, launch (if release) |

Step transitions are driven by `step_enter` / `step_exit` events.

## Topology

See `_common/run-dash/TOPOLOGIES/bug.md` for the canonical step-rail data and agent positions.

## Conditional Agents

| Condition | Add | Skip |
|-----------|-----|------|
| Severity ≥ high | triage in Reproduce | — |
| Regression suspected | trail in RCA | — |
| Concurrency suspected | specter in RCA | — |
| UI flow affected | voyager in Verify | — |
| Release required | launch in Verify | — |
| Hotfix to existing release | — | release planning |

## Live Dashboard Emit

Spec: `_common/RUN_DASH_PROTOCOL.md`, `_common/run-dash/INTEGRATION.md §2.4`, `_common/run-dash/TOPOLOGIES/bug.md`. Specialist agents do not emit; Claude Code hooks capture every Agent invocation.

### Emit Points

| When | Emit |
|------|------|
| Recipe entry | `run_start run_kind=bug recipe=bug project=<git-basename> goal="<goal>" severity=<low\|med\|high\|critical>` |
| Step enter | `step_enter step=<Reproduce\|RCA\|Fix\|Verify>` |
| Step exit | `step_exit step=<...> exit_gate=<pass\|fail>` |
| RCA finished | `rca_done cause_summary="<short string>"` |
| Fix proposed | `fix_proposed diff_lines=<n> touched_files=<n>` |
| Recipe exit | `run_end status=<completed\|aborted\|error> duration_ms=<ms>` |

### Skeleton

```sh
PARENT_RUN_ID="${RUN_ID:-}"
export RUN_ID="bug-$(date -u +%Y%m%d-%H%M%S)-$(uuidgen | head -c 7 | tr A-Z a-z)"
START_S=$(date +%s)
PROJECT=$(basename "$(git rev-parse --show-toplevel 2>/dev/null || pwd)")
EMIT="$HOME/.claude/skills/_common/scripts/run-emit.sh"

bash $EMIT run_start run_kind=bug recipe=bug project="$PROJECT" \
  goal="$GOAL" severity="$SEVERITY"

# Reproduce
bash $EMIT step_enter step=Reproduce
# scout (+ triage?) — hooks handle agent_start/end
bash $EMIT step_exit step=Reproduce exit_gate=pass

# RCA
bash $EMIT step_enter step=RCA
# scout (RCA) (+ trail? + specter?)
bash $EMIT rca_done cause_summary="N+1 query in /api/users on cache miss"
bash $EMIT step_exit step=RCA exit_gate=pass

# Fix
bash $EMIT step_enter step=Fix
# builder → judge → radar
bash $EMIT fix_proposed diff_lines=87 touched_files=3
bash $EMIT step_exit step=Fix exit_gate=pass

# Verify
bash $EMIT step_enter step=Verify
# voyager? → guardian → launch?
bash $EMIT step_exit step=Verify exit_gate=pass

DUR_MS=$(( ($(date +%s) - START_S) * 1000 ))
bash $EMIT run_end status=completed duration_ms=$DUR_MS

[ -n "$PARENT_RUN_ID" ] && export RUN_ID="$PARENT_RUN_ID" || unset RUN_ID
```

### Free via hooks

`agent_start` / `agent_end` for every spawned subagent and `tool_use` for Bash / Read / Write / Edit / Grep / Glob are emitted automatically. Recipe code owns step + rca / fix semantics only.

## Failure Paths

| Failure | Detected by | Action |
|---------|-------------|--------|
| Cannot reproduce | scout | `step_exit step=Reproduce exit_gate=fail`; abort recipe with `run_end status=aborted` |
| RCA wrong cause (judge rejects fix) | judge | escalate to scout for re-RCA; emit `step_enter step=RCA` again |
| Fix breaks tests (radar fails) | radar | loop back to Fix |
| Verify finds regression elsewhere | voyager | broaden Reproduce, restart |

## Cost Profile

| Profile | Approximate agent count | Approximate cost |
|---------|-------------------------|------------------|
| Lite (low severity, fast fix) | 3-4 | Low |
| Standard | 5-7 | Medium |
| Full (regression + concurrency suspect, UI verify, release) | 10-12 | High |

## Related

- `apex-recipe.md` — when bugs reveal architectural issues
- `feature-recipe.md` — sibling
- `_common/run-dash/TOPOLOGIES/bug.md` — UI topology
- `_common/RUN_DASH_PROTOCOL.md` — universal observability contract
