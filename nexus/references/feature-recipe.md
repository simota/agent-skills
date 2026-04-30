# Nexus Feature Recipe Reference

**Purpose:** Standard 4-step chain for new feature implementation. Lighter than apex (no risk gate, no engine boundary) — designed for a single Claude Code session.
**Read when:** User invokes `/nexus feature` or asks to implement a new feature with spec + iterate cycle.

---

## Steps

| Step | Purpose | Primary agents |
|------|---------|----------------|
| **Discover** | Persona / demand validation | spark, researcher, echo (if existing product) |
| **Spec** | L3 acceptance criteria + spec_gate | accord, scribe (optional) |
| **Implement** | Build + per-iteration review | builder / artisan, judge, radar (orbit-style mini-loop) |
| **Ship** | PR + release | guardian, launch |

Step transitions are driven by `step_enter` / `step_exit` events (see §3).

## Topology

See `_common/run-dash/TOPOLOGIES/feature.md` for the canonical step-rail data and agent positions.

## Conditional Agents

| Condition | Add | Skip |
|-----------|-----|------|
| Existing product (improvement) | echo in Discover | — |
| Greenfield | — | echo |
| External review needed | scribe in Spec | — |
| UI surface | artisan in Implement | — |
| API surface | radar in Implement | — |
| Backend-only | — | artisan |

## Live Dashboard Emit

Spec: `_common/RUN_DASH_PROTOCOL.md`, `_common/run-dash/INTEGRATION.md §2.4`, `_common/run-dash/TOPOLOGIES/feature.md`. Specialist agents do not emit; Claude Code hooks capture every Agent invocation.

### Emit Points

| When | Emit |
|------|------|
| Recipe entry | `run_start run_kind=feature recipe=feature project=<git-basename> goal="<goal>" scope=<S\|M\|L>` |
| Step enter | `step_enter step=<Discover\|Spec\|Implement\|Ship>` |
| Step exit | `step_exit step=<...> exit_gate=<pass\|fail>` |
| Spec gate verdict | `spec_gate verdict=<pass\|fail> coverage=<0..1>` |
| Recipe exit | `run_end status=<completed\|aborted\|error> duration_ms=<ms>` |

### Skeleton

```sh
PARENT_RUN_ID="${RUN_ID:-}"
export RUN_ID="feature-$(date -u +%Y%m%d-%H%M%S)-$(uuidgen | head -c 7 | tr A-Z a-z)"
START_S=$(date +%s)
PROJECT=$(basename "$(git rev-parse --show-toplevel 2>/dev/null || pwd)")
EMIT="$HOME/.claude/skills/_common/scripts/run-emit.sh"

bash $EMIT run_start run_kind=feature recipe=feature project="$PROJECT" \
  goal="$GOAL" scope="$SCOPE"

# Discover
bash $EMIT step_enter step=Discover
# spark / researcher / echo? — hooks handle agent_start/end
bash $EMIT step_exit step=Discover exit_gate=pass

# Spec
bash $EMIT step_enter step=Spec
# accord (+ scribe?)
bash $EMIT spec_gate verdict=pass coverage=0.92
bash $EMIT step_exit step=Spec exit_gate=pass

# Implement (orbit-style mini-loop)
bash $EMIT step_enter step=Implement
# orbit → builder/artisan/judge/radar (orbit may emit orbit_iter)
bash $EMIT step_exit step=Implement exit_gate=pass

# Ship
bash $EMIT step_enter step=Ship
# guardian → launch
bash $EMIT step_exit step=Ship exit_gate=pass

DUR_MS=$(( ($(date +%s) - START_S) * 1000 ))
bash $EMIT run_end status=completed duration_ms=$DUR_MS

[ -n "$PARENT_RUN_ID" ] && export RUN_ID="$PARENT_RUN_ID" || unset RUN_ID
```

### Free via hooks

`agent_start` / `agent_end` for every spawned subagent and `tool_use` for Bash / Read / Write / Edit / Grep / Glob are emitted automatically. Recipe code owns step + spec_gate semantics only.

## Failure Paths

| Failure | Detected by | Action |
|---------|-------------|--------|
| Spec gate fail | accord | `step_exit step=Spec exit_gate=fail`; loop back to Discover or escalate |
| Implement loop stuck | orbit (convergence) | escalate; emit `error severity=warn source=orbit message="stuck"` |
| Ship blocked (PR conflict) | guardian | `step_exit step=Ship exit_gate=fail`; re-enter Implement |

## Cost Profile

| Profile | Approximate agent count | Approximate cost |
|---------|-------------------------|------------------|
| Lite (Discover skipped) | 4-6 | Low |
| Standard | 8-12 | Medium |
| Full (with scribe + multiple implement iterations) | 14-18 | High |

## Related

- `apex-recipe.md` — heavier full-cycle variant
- `bug-recipe.md` — sibling
- `_common/run-dash/TOPOLOGIES/feature.md` — UI topology
- `_common/RUN_DASH_PROTOCOL.md` — universal observability contract
