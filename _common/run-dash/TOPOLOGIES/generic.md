# Topology — `run_kind=manual` / `single-agent` / unknown (generic mode)

Generic mode does **not** have a static topology. Nodes and edges are built dynamically from `parent_agent` and `depth` fields in `agent_start` events. This document specifies the **algorithm**, layout choices, and the timeline view that complements the dynamic DAG.

---

## 1. When This Mode Is Used

| Trigger | Behaviour |
|---------|-----------|
| `run_kind` is `manual` / `single-agent` | mode = `generic` |
| `run_kind` is missing or unknown | mode = `generic` (fallback) |
| User picks `generic` in the mode picker | overrides automatic detection |

This mode is the **catch-all**: every event sequence renders, no per-recipe assumptions are made.

## 2. Inputs

- `agent_start` events with optional `parent_agent`, `depth`, `engine`
- `agent_end`, `agent_progress`, `tool_use`, `error`
- Universal core fields (`ts`, `seq`, `agent`, …)

If `parent_agent` is missing, the algorithm infers a tentative parent (see §3.2).

## 3. DAG Construction

### 3.1 Node Set

```
nodes = {}
for ev in events where ev.kind in {agent_start}:
    nodes[ev.agent] = { id: `a.${ev.agent}#${ev.seq}`,
                        agentName: ev.agent,
                        engine: ev.engine,
                        depth: ev.depth ?? null,
                        startedAt: ev.ts,
                        status: 'running' }
```

The seq suffix prevents collision when the same agent name is invoked multiple times in a single run (treated as separate nodes).

### 3.2 Edge Set

```
edges = []
for ev in events where ev.kind == agent_start and ev.parent_agent:
    parent = nearest_running_node_with_name(ev.parent_agent, before=ev.ts)
    if parent:
        edges.push({ source: parent.id, target: nodes[ev.agent].id })

# Fallback: when parent_agent is missing,
# infer the most recent running agent at depth = ev.depth - 1
# or the run root if ev.depth in {1, null}
```

The "run root" is a synthetic node `root: user/nexus/orbit` (label depends on the first emit). `parent_agent="user"` collapses to the root.

### 3.3 Layout

- Library: **dagre** (`@dagrejs/dagre`)
- Direction: top → bottom by default, left → right when viewport is landscape & ≥1600 wide
- Ranksep: 80 px, nodesep: 40 px
- Node size: 140×40

The xyflow component receives the dagre output directly via `setNodes(...)`.

### 3.4 Live Updates

- New `agent_start` → re-run dagre and animate node entry (Framer Motion fade + scale-from-0.85)
- `agent_end` → flip status, keep position
- `error` event → flash red border on target node

Re-layouts must complete within 80 ms for graphs ≤100 nodes.

## 4. Timeline (Gantt) View

Below the dynamic DAG (60/40 vertical split):

- Y axis: agents (one row per **distinct** node, ordered by `startedAt`)
- X axis: time, scaled to `runStart..now`
- Bar: from `agent_start.ts` to `agent_end.ts` (or `now` if active)
- Bar fill: status colour
- Tool-use ticks (`▎`) inside bars at relative positions
- Errors: red diamond markers above the bar at error.ts

Implementation: vanilla SVG, no chart library.

## 5. Right Rail Adaptation

| Card | Behaviour |
|------|-----------|
| Active agents | shared core |
| Risk Gate radar | hidden |
| Checkpoints + errors | shared core |
| Engine switch | shown only if `engine_switch` events occurred |

## 6. Mid Panel — Tool-use Histogram

Recharts `BarChart` of the top 6 tools by `tool_use` count, fed from `state.toolCounts`.

## 7. Postmortem

Generic template (`server/postmortem/generic.ts`):

- Outcome (status, duration)
- Agents Executed (DAG-derived list, ordered by start time)
- Tool-use histogram (top 6)
- Errors / Warnings
- Engine boundary crossings (if any)
- Lore handoff candidates (heuristic — long-tail agents, repeated errors)

## 8. Performance

- Node animation: GPU compositing only (`transform`, `opacity`)
- Re-layout debounced 50 ms
- Timeline redraws on event ingest at 60 fps for ≤200 bars

## 9. Edge Cases

| Case | Handling |
|------|----------|
| Cycles in `parent_agent` | dagre tolerates; ignore back edges |
| Same agent invoked twice | distinct nodes via `#seq` suffix |
| `agent_end` without `agent_start` | render orphan node with `pending → done` flash |
| Missing `parent_agent` and `depth` | place under root cluster |
| `run_end` arrives before some `agent_end` | mark unfinished agents `error` (timeout) |

## 10. Related

- `EVENTS.md §3` — core kinds powering this view
- `UI.md §6.2 / §6.3` — layout
- `DESIGN.md §6.4` — chosen libraries (xyflow, dagre, Recharts)
- `TOPOLOGIES/apex.md` / `feature.md` / `bug.md` — siblings
