# run-dash — Postmortem & Lore Handoff

Defines how a completed run is converted into a markdown postmortem and forwarded to Lore as training data. Templates are per-recipe; the generic template covers any `run_kind`.

---

## 1. Purpose

A finished run (any kind) carries signals — phase / step durations, agent costs, gate verdicts, engine boundaries, errors — that are valuable beyond the moment of viewing. The postmortem turns one run's transient log into:

- An attachable summary for the related PR
- A learning row for Lore (`METAPATTERNS.md` updates, agent-decay detection)
- An archive entry for trend analysis (Pulse, Beacon)

## 2. Trigger

| Trigger | Behaviour |
|---------|-----------|
| `run_end` event arrives | Server emits a `note` event referencing the generated postmortem path |
| `GET /api/postmortem/:run` | Synchronous generation, returned as `text/markdown` |
| `bun run scripts/postmortem.ts --run=<run-id>` | CLI generation |

Generation is **idempotent**: re-running rewrites `postmortem.md` based on the current events.

## 3. Output

Path: `<repo>/.agents/run-dash/<run-id>/postmortem.md`

### 3.1 Common Frontmatter (all run kinds)

```
---
run_id: <run-id>
run_kind: apex | feature | bug | refactor | manual | single-agent
recipe: <recipe-name | none>
goal: <text>
mode: <if applicable>
scope: <if applicable>
status: completed | aborted | error
started_at: <ISO8601>
ended_at: <ISO8601>
duration: hh:mm:ss
final_engine: claude_code | codex_cli
spec_version: <hash>
---
```

### 3.2 apex Template

Adds:

```
verdict: Go | Conditional-Go | No-Go | (none)
```

Body sections:
- Outcome
- Phase Breakdown
- Agents Executed
- Risk Gate
- Orbit (Phase 6)
- Engine Boundary Crossings
- Bottleneck
- Errors / Warnings
- Lore Handoff Candidates

### 3.3 feature / bug / refactor Template

Replaces "Phase Breakdown" with "Step Breakdown". Adds:

- Spec gate verdict (feature)
- RCA summary + fix proposed (bug)
- Refactor scope and tests touched (refactor)

### 3.4 generic Template

Minimal sections — works on any run including ad-hoc:

- Outcome (status, duration)
- Agents Executed (DAG-derived list)
- Tool-use histogram (top 6)
- Errors / Warnings
- Engine Boundary Crossings (if any)
- Lore Handoff Candidates (heuristic)

## 4. Generation Algorithm

```
1. Read events.jsonl line by line
2. Fold events through the same reducer used by the dashboard client
3. Compute aggregates:
     phase_durations[p]   = phase_exit.ts - phase_enter.ts (apex)
     step_durations[s]    = step_exit.ts  - step_enter.ts  (recipe)
     agent_durations[a]   = agent_end.ts  - agent_start.ts
     bottleneck_agent     = argmax(agent_durations)
     bottleneck_phase     = argmax(phase_durations) | argmax(step_durations)
     orbit_total_cost     = sum(iter.cost_per_task) over orbit_iter events
     final_convergence    = last orbit_iter.convergence
     engine_history       = engine_switch events in order
     errors               = error events with severity >= warn
     tool_histogram       = top 6 tools by tool_use count
4. Choose template from run_kind (fallback: generic)
5. Render markdown
6. Write atomically (write tmp + rename)
7. Emit a "note" event referencing the path
```

## 5. Lore Handoff

When `LORE_HANDOFF=1` is set in the server env:

1. Append a single-line summary to `<repo>/.agents/lore/run-history.md`:
   ```
   - 2026-04-30 apex-... goal="passkey login" status=completed duration=29:32 verdict=Go bottleneck=accord(P4)
   - 2026-05-01 feature-... goal="api key rotation" status=completed duration=12:14 spec_gate=pass bottleneck=builder(Implement)
   ```
2. Emit a `note` event with `meta.lore_handoff=true` and `meta.path` pointing to the postmortem
3. Lore consumes both for cross-run pattern extraction (`METAPATTERNS.md`) and agent decay detection

Lore handoff is **opt-in** to keep the local-tool default truly local.

## 6. Privacy

- Snippets in events are already capped at 280 chars (`EVENTS.md §2`); the postmortem inherits the same constraint
- Source code, file paths, and shell commands appear by reference (`output_ref`) — never inline contents
- No environment variables or secrets are read during generation

## 7. Recipe Postmortem Hooks

Recipes can register custom sections by exporting a render function in `server/postmortem/<recipe>.ts`. The dispatcher tries:

1. `<recipe>` template (if registered)
2. `<run_kind>` template
3. generic template

This way new recipes opt in without modifying the dispatcher.

## 8. Related

- `EVENTS.md` — schema being read
- `INTEGRATION.md §2.4` — emit points that feed the reducer
- `DESIGN.md §10` — extensibility surface
- `sample/server/postmortem.ts` — reference implementation
- `sample/events/apex-20260430-120000-a3f/postmortem.md` — generated apex example
