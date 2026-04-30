# run-dash — UI / UX Specification

Defines layout, panel responsibilities, node and edge animations, theme, replay-mode controls, and the mode-pluggable behaviour that lets one dashboard render apex / recipe / generic runs.

---

## 1. Mode Selection

The dashboard reads `run_start.run_kind` and selects a mode automatically. A header dropdown overrides.

| `run_kind` | Mode | Primary panels |
|------------|------|----------------|
| `apex` | **apex** | Phase rail · Topology (fixed) · Risk Gate radar · Orbit chart |
| `feature` / `bug` / `refactor` | **recipe** | Step rail · Topology (recipe-specific) · Active agents |
| `manual` / `single-agent` / unknown | **generic** | Dynamic DAG (dagre) · Timeline (Gantt) · Active agents |

Mode pickers and run pickers coexist in the header.

## 2. Target Resolutions

| Tier | Min | Default | Max |
|------|-----|---------|-----|
| Width | 1280 | 1920 | 2560 |
| Height | 720 | 1080 | 1440 |

## 3. Layout (1920×1080)

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  Header  56px  [run picker] [mode picker] [postmortem]                       │
├──────────────────────────────────────────────────────────────────────────────┤
│  Mode rail  44px (apex: phase rail | recipe: step rail | generic: hidden)    │
├──────────────────────────────────────────────────────────────┬───────────────┤
│                                                              │  Right rail   │
│  Main view                                                   │  360px        │
│   apex/recipe: Topology canvas                               │  ─ Active     │
│   generic   : Dynamic DAG (top half) + Timeline (bottom)     │  ─ Risk Gate* │
│                                                              │  ─ Checkpts   │
│                                                              │  ─ Engine     │
├──────────────────────────────────────────────────────────────┤  *apex only   │
│  Mid panel  240px                                            │               │
│   apex   : Orbit chart                                       │               │
│   recipe : Step summary                                      │               │
│   generic: Tool-use histogram                                │               │
├──────────────────────────────────────────────────────────────┴───────────────┤
│  Event stream  240px                                                          │
└──────────────────────────────────────────────────────────────────────────────┘
```

## 4. Header Panel

```
[ run-id▼ ]  ⬤  goal: passkey login   [mode▼]  AUTORUN_FULL  ⏱ 30:20  [📄 postmortem]
```

| Element | Behavior |
|---------|----------|
| Run picker | Dropdown listing `/api/runs` results; switches SSE connection |
| Mode picker | `auto` / `apex` / `recipe` / `generic`; `auto` follows `run_kind` |
| Goal | run_start.meta.goal; hover shows full text |
| Mode badge | run_start.meta.mode (apex / feature) |
| Elapsed | mm:ss / hh:mm:ss; live tick |
| Postmortem button | `run_end` 後に enabled; opens `/api/postmortem/:run` |

## 5. Mode Rail (44px)

| Mode | Render |
|------|--------|
| apex | Phase rail (P0 → Ship), state colours, current bar |
| recipe | Step rail (recipe-defined steps); same visual language |
| generic | Hidden (no canonical sequence) |

## 6. Main View

### 6.1 apex / recipe — Topology (xyflow)

xyflow ReactFlow with phase / step group containers and agent nodes from `TOPOLOGIES/<recipe>.ts`.

- Minimap right-bottom, controls left-bottom
- `phase_enter` / `step_enter` triggers smooth pan/zoom (800ms ease-in-out)
- Idle edges: thin grey; active edges: animated; engine boundary: dashed purple

### 6.2 generic — Dynamic DAG

Built from `parent_agent` / `depth`:

1. Root = orchestrator inferred from `parent_agent="user"|"nexus"|"orbit"|null`
2. Each `agent_start` adds a node; `parent_agent` adds an edge
3. **dagre** layout (top-down or left-right by viewport) computes positions
4. xyflow nodes are updated via `setNodes(...)` and animated by Framer Motion

Unplaced agents (no parent / unknown) sit in a "loose" cluster.

### 6.3 generic — Timeline (Gantt)

Below the DAG (split at 60/40):

- Y axis: agents (one row per agent)
- X axis: time, scaled to run duration
- Bars: from `agent_start.ts` to `agent_end.ts`; colour by status
- Tool-use ticks within bars (small `▎`)
- Errors show as red diamonds

Rendering: vanilla SVG (no chart library); ~150 LOC.

## 7. Right Rail (360px)

| Card | Modes | Content |
|------|-------|---------|
| Active agents | all | Cards per active agent: name, phase/step, elapsed, last tool |
| Risk Gate radar | apex only | omen / ripple / echo radar (Recharts) |
| Checkpoints + errors | all | Vertical list; waiting checkpoints countdown |
| Engine switch | apex/recipe | Current engine badge + history |

Cards adapt: cards irrelevant to the current mode render compact `(N/A in this mode)` chip and collapse.

## 8. Mid Panel (240px)

| Mode | Panel |
|------|-------|
| apex | Orbit LineChart (convergence / cost_per_task) |
| recipe | Step summary: spec_gate verdict, fix metrics, etc. |
| generic | Tool-use histogram (Recharts BarChart) — top 6 tools used |

## 9. Event Stream (240px)

Virtualised list (`@tanstack/react-virtual`); identical across modes.

- Row: `[hh:mm:ss] [kind chip] [agent] [meta digest]`
- Filter by kind / agent / errors-only
- Click → highlight + pan to corresponding node
- Pin important rows

## 10. Node Animation

| status | Visual | Implementation |
|--------|--------|---------------|
| `pending` | opacity .4, dotted | `.pending` |
| `running` | glow + breathe | `nodePulse` |
| `running + tool_use` | scale spike 200ms | Framer Motion |
| `waiting` | yellow pulse + ⏸ | `pulseYellow` |
| `done` | green check, 70% saturation | static |
| `error` | red, shake 4× | Framer Motion |
| `skipped` | diagonal stripes | repeating-linear-gradient |

Color tokens: accent `#3b82f6`, success `#10b981`, warning `#f59e0b`, danger `#ef4444`, codex `#a78bfa`, muted `#64748b`.

## 11. Edge Animation

| type | Idle | Active |
|------|------|--------|
| `flow` | thin grey | 3–5 particles glide source → target (4s loop) |
| `escalation` | hidden | red reverse particles 1.2s |
| `engineBoundary` | dashed purple | falling particles |
| `dynamicDAG` | thin grey | particles only on active path |

## 12. Camera Behavior

| Trigger | Action |
|---------|--------|
| `phase_enter` / `step_enter` | Smooth pan to that group (800ms) |
| Fit view button | Show whole graph (600ms) |
| Follow active toggle | Track centroid of active agents (live) |
| Event row click | Pan + flash highlight (600ms) |

## 13. Theming

Dark default for long sessions:

```
--bg-base: #0b1220
--bg-elev: #111a2e
--bg-row:  #0e162a
--text:    #e2e8f0
--text-muted: #94a3b8
--border:  #1e293b
--accent:  #3b82f6
--success: #10b981
--warning: #f59e0b
--danger:  #ef4444
--codex:   #a78bfa
```

Light theme swaps `bg-*` to slate-50/white.

Typography: Inter UI / JetBrains Mono numerals.

## 14. Interactions

| Shortcut | Function |
|----------|----------|
| `f` | Fit view |
| `g` | Toggle follow-active |
| `r` | Toggle replay panel |
| `m` | Cycle mode (auto / apex / recipe / generic) |
| `j` / `k` | Event prev/next |
| `1`–`8` | (apex/recipe) Pan to that phase/step |
| `e` | Collapse / expand event stream |
| `?` | Shortcut overview modal |

## 15. Replay Mode

Toggle "Live" → "Replay" surfaces a slider and speed control.

| Control | Behavior |
|---------|----------|
| Play / Pause | Re-emit events in time order; `setTimeout` over `ts` deltas |
| Speed | 0.5× / 1× / 2× / 4× / 10× |
| Seek | Slider folds events up to that `seq`, then resumes |
| Step | Single-event manual advance |

Implementation: `/api/replay/:run` re-streams via SSE with adjusted pacing; client uses the same pipeline.

## 16. Accessibility

- Every interaction has a keyboard equivalent
- State conveyed via animation **plus** icon + label
- `prefers-reduced-motion`: degrade to fade
- ARIA live region announces critical events (`risk_gate`, `error`, `checkpoint`)

## 17. Responsiveness

| Width | Behavior |
|-------|----------|
| ≥1600 | All panels visible |
| 1280–1599 | Right rail toggleable |
| <1280 | Mid panel and Event stream tabbed |

## 18. Performance Budget

| Metric | Budget |
|--------|--------|
| FPS — apex/recipe (5 active) | ≥58 |
| FPS — generic (50 nodes / 100 edges) | ≥55 |
| Event stream row insert | <50ms |
| State reflection | <500ms p95 |
| Initial load | <3s cold, <1s warm |
| Memory | <500MB / 8h run |

## 19. Related

- `EVENTS.md` — drives every animation
- `TOPOLOGIES/apex.md` / `feature.md` / `bug.md` / `generic.md` — node and edge data
- `DESIGN.md §6.4` — chosen libraries
