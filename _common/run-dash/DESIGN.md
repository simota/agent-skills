# run-dash — Architecture Design

Defines the architecture, data flow, tech stack, and file layout for run-dash, the universal agent-run dashboard. Schema, UI layout, integration, and per-recipe topology details live in dedicated files (`EVENTS.md` / `UI.md` / `INTEGRATION.md` / `TOPOLOGIES/`).

---

## 1. Goals

| ID | Goal | Measure |
|----|------|---------|
| G1 | Any agent run is visibly "alive" on screen | Phase / step / agent transitions reflect within 1 s |
| G2 | One dashboard handles apex, recipes, and ad-hoc runs | Mode auto-switches by `run_kind` |
| G3 | No changes to existing skills required | Hooks-only path emits `agent_start` / `agent_end` automatically |
| G4 | Past runs replay deterministically | Fully reconstructible from `events.jsonl` |
| G5 | Per-repo auto-generation | Fully automated via `GENERATION.md` |
| G6 | 60 fps under 1,000 events/min | Virtual scroll + GPU compositing only |

## 2. Design Principles

1. **Single source of truth = `events.jsonl`**. State is the fold of events.
2. **Append-only / Immutable**. Past lines are never rewritten.
3. **Stateless server**. Tails the file, broadcasts via SSE; holds no state.
4. **Receiver only**. Producers call one emit helper; the dashboard never calls back.
5. **Mode-pluggable UI**. Modes are auto-selected by `run_kind`; unknown extension kinds are ignored, never break rendering.
6. **Local first**. Listens on `localhost` only. No authentication.

## 3. Modes

| Mode | When | Layout | Topology source |
|------|------|--------|-----------------|
| `apex` | `run_kind=apex` | Phase rail + fixed topology + Risk Gate radar + Orbit chart | `TOPOLOGIES/apex.md` |
| `recipe` | `run_kind=feature` / `bug` / `refactor` | Step rail + recipe topology | `TOPOLOGIES/<recipe>.md` |
| `generic` | `run_kind=manual` / `single-agent` / unknown | Timeline (Gantt) + dynamic DAG | `TOPOLOGIES/generic.md` (algorithm) |

The dashboard reads `run_start.run_kind` and selects the mode automatically. A header dropdown allows manual override.

## 4. Overall Architecture

```
                ┌──────────────────────────────────────────┐
                │ Producers                                │
                │  - Claude Code session (Agent tool)      │
                │  - Codex CLI subagents                   │
                │  - Nexus recipes (apex / feature / bug) │
                │  - Single-agent invocations              │
                └──────────────┬───────────────────────────┘
                               │ run-emit.sh OR Claude Code hooks
                               ▼
                ┌──────────────────────────────────────────┐
                │ Storage  (per repo, per run)             │
                │ <repo>/.agents/run-dash/<run-id>/        │
                │   ├─ events.jsonl       (append-only)   │
                │   ├─ state.json         (snapshot)       │
                │   └─ postmortem.md      (on run_end)     │
                └──────────────┬───────────────────────────┘
                               │ chokidar tail
                               ▼
                ┌──────────────────────────────────────────┐
                │ Server   Bun + Hono                      │
                │   GET /                → SPA             │
                │   GET /api/runs        → list + run_kind │
                │   GET /api/state/:run                    │
                │   GET /api/events/:run  (SSE)            │
                │   GET /api/replay/:run  (SSE, throttled) │
                │   GET /api/postmortem/:run               │
                └──────────────┬───────────────────────────┘
                               │ Server-Sent Events
                               ▼
                ┌──────────────────────────────────────────┐
                │ Client   React + xyflow + Recharts       │
                │   - zustand store (event-sourced)        │
                │   - mode picker (apex / recipe / generic)│
                │   - run picker                            │
                │   - panels: Topology / Step rail / …     │
                │   - generic-mode timeline (svg gantt)    │
                └──────────────────────────────────────────┘
```

## 5. Data Flow

1. A producer emits an event by calling `run-emit.sh`
2. Helper appends one line to `events.jsonl` (atomic seq via mkdir lock)
3. Server watches each `events.jsonl` via chokidar
4. On change, new lines are pushed to every SSE subscriber
5. Client receives via `EventSource`; the zustand reducer folds each event
6. React re-renders only the panels whose store slices changed
7. xyflow updates affected nodes via `updateNodeData` (no relayout)
8. On `run_end`, server writes `postmortem.md` (atomic) and emits a `note` event

## 6. Components

### 6.1 Producer

| Path | When | Driver |
|------|------|--------|
| Explicit emit | Recipe-specific events (phase / risk gate / step) | Recipe code calls `run-emit.sh` |
| Claude Code hooks | Generic agent / tool observability | `PreToolUse` / `PostToolUse` / `SessionStart` / `Stop` |
| Codex subagent emit | Phase 6 of apex (or any Codex CLI work) | Spawn scripts call `run-emit.sh` from inside the subagent |

Failures are silent.

### 6.2 Storage

- Path: `<repo>/.agents/run-dash/<run-id>/`
- run-id: `<run_kind>-YYYYMMDD-HHMMSS-<short-hash>`

### 6.3 Server

- **Bun** + **Hono** (Node 20+ fallback)
- Default port: 5757; auto-increments on collision
- Computes `run_kind` per run from the first `run_start` event; surfaces it in `/api/runs`

### 6.4 Client

- React 18 + TypeScript (strict)
- **zustand** for state
- **@xyflow/react v12** for graphs (apex / recipe modes use static layouts; generic mode uses **dagre** layout)
- **Recharts** for radar / line charts (apex extensions)
- Custom SVG / Framer Motion for timeline (generic mode)
- **Tailwind CSS v4** + CSS keyframes
- **@tanstack/react-virtual** for the event stream

## 7. Tech Stack Rationale

| Layer | Choice | Rationale / Alternative |
|-------|--------|-------------------------|
| Runtime | Bun | Standard across this skill ecosystem |
| Server | Hono | Shortest path to SSE |
| Bundler | Vite | Stable HMR |
| Graph | @xyflow/react v12 | Custom nodes/edges, minimap, controls |
| DAG layout | dagre | Battle-tested layered layout |
| Charts | Recharts | RadarChart and LineChart |
| Animation | Framer Motion + CSS | Node transitions and shake/pulse |
| State | zustand | Localised re-renders vs. Context |
| File watch | chokidar | Robust to append loss |

## 8. File Layout (post-generation)

```
<repo>/.agents/run-dash-app/
  package.json
  tsconfig.json
  vite.config.ts
  .spec-version
  server/
    index.ts
    state.ts
    postmortem.ts
    routes/{runs,events,replay,postmortem}.ts
  web/
    index.html
    src/
      main.tsx / App.tsx / store.ts
      hooks/{useSSE,useReplay}.ts
      modes/{ApexMode,RecipeMode,GenericMode}.tsx
      panels/{Header,PhaseRail,StepRail,Topology,DynamicGraph,Timeline,
              ActiveAgents,RiskGateRadar,OrbitChart,Checkpoints,
              EngineSwitch,EventStream}.tsx
      nodes/{AgentNode,PhaseGroupNode,SubOrchestratorNode}.tsx
      edges/{FlowEdge,EngineBoundaryEdge}.tsx
      lib/topologies/{apex,feature,bug,refactor,dynamic}.ts
      lib/{animations,colors,time}.ts
      types/{events,state}.ts
```

LOC budget: 2,500–3,500 lines total (excluding tests).

## 9. Performance Targets

| Metric | Target |
|--------|--------|
| Event ingest → UI reflection | < 1 s |
| Sustained throughput | 1,000 events/min |
| Burst | 5,000 events/min |
| FPS in apex mode (5 active nodes) | ≥58 |
| FPS in generic mode (50 nodes / 100 edges) | ≥55 |
| EventStream rendering | smooth at 10k rows |
| Memory | < 500 MB over 8h run |
| Cold start | < 3 s |

## 10. Security / Privacy

- localhost binding only
- No authentication
- Snippets in events capped at 280 chars
- Artifacts referenced via symlink, never copied
- `.gitignore` mandates `.agents/run-dash/`

## 11. Extensibility

- Add a new `run_kind` by writing `TOPOLOGIES/<recipe>.md` + a `lib/topologies/<recipe>.ts`
- Pluggable panels: register additional panels in `web/src/panels/index.ts`
- Theming: colours and logos in a single theme file

## 12. Non-Goals

- Multi-user / auth / RBAC
- Cloud sync / persistence
- Long-term trend analytics (`beacon`)
- Becoming a registered skill
- Replacing existing observability tools (`vista`, `realm`)

## 13. Risks and Mitigations

| Risk | Mitigation |
|------|------------|
| Event-volume explosion when hooks emit `tool_use` for everything | Server-side sampling; `RUN_DASH_TOOLS=0` flag |
| Hook overhead on every tool call | Helper completes within 100 ms |
| Unknown agents in DAG | Render under "unplaced" cluster |
| Concurrent runs | Run-id in path; client run picker |
| Stale generation | `.spec-version` records source hash |

## 14. References

- `EVENTS.md` — schema (core + extensions)
- `UI.md` — layout / animation / mode specs
- `INTEGRATION.md` — emit protocol, Claude Code hooks, auto-spawn
- `POSTMORTEM.md` — postmortem and Lore handoff
- `GENERATION.md` — generation prompt + manifest
- `TOPOLOGIES/*.md` — per-recipe topology data
