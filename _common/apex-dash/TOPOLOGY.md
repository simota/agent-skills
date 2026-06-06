# apex-dash — Topology Definition

Defines the apex topology as **declarative data**. At implementation time, transcribe this data verbatim into `web/src/lib/topology.ts` and feed it to xyflow.

---

## 1. Design Principles

1. **Static layout**: node positions are predefined and never animated (state is conveyed through motion)
2. **Phase groups**: P0 through Ship are represented as **subflows** containing agent nodes
3. **Sub-orchestrators**: Vision and Orbit are collapsible groups holding their specialists
4. **Conditional rendering**: agents that depend on scope or UI surface carry a `conditional` flag

## 2. Grid and Coordinates

- Horizontal axis = phase progression (X). Each phase lane is 360 px wide
- Vertical axis = subtracks (Y). Tech on top, UX on bottom
- Grid unit: 80 px

```
   X →
   ┌────────┬────────┬───────┬───────┬───────┬─────────────────┬──────────────┬──────┐
Y  │  P0    │  P1    │  P2   │  P3   │  P4   │  P5 (parallel)  │  P6 (Codex)  │ Ship │
↓  │ 360px  │ 360px  │ 360px │ 360px │ 360px │ 720px           │ 480px        │ 240px│
   └────────┴────────┴───────┴───────┴───────┴─────────────────┴──────────────┴──────┘
```

Total width ~3,300 px. The canvas supports zoom/pan, so it can comfortably exceed screen size.

## 3. Node Types

| `type` | Purpose | Style |
|--------|---------|-------|
| `phaseGroup` | Phase background frame | Rounded rectangle, light tint, label on top |
| `agent` | A single agent | Circle + text; animated by state |
| `subOrchestrator` | Vision / Orbit | Double circle, holds specialists internally |
| `gate` | Risk Gate / phase exit gates | Diamond, coloured by verdict |
| `engineBoundary` | Claude Code → Codex CLI boundary | Vertical dashed bar |

## 4. Node Definitions

These rows are rendered into `topology.ts`. The `conditional` column is evaluated against the run's metadata (goal context).

### 4.1 Phase Groups

| id | label | x | y | w | h |
|----|-------|---|---|---|---|
| `pg.P0` | Phase 0 — Bootstrap | 0 | 0 | 360 | 800 |
| `pg.P1` | Phase 1 — Discovery | 360 | 0 | 360 | 800 |
| `pg.P2` | Phase 2 — Ideate | 720 | 0 | 360 | 800 |
| `pg.P3` | Phase 3 — Verdict | 1080 | 0 | 360 | 800 |
| `pg.P4` | Phase 4 — Spec | 1440 | 0 | 360 | 800 |
| `pg.P5` | Phase 5 — Design + Risk | 1800 | 0 | 720 | 800 |
| `pg.P6` | Phase 6 — Implementation | 2520 | 0 | 480 | 800 |
| `pg.Ship` | Ship | 3000 | 0 | 240 | 800 |

### 4.2 Phase 0 (Bootstrap, autonomous mode only)

| id | label | parent | (rx,ry) | conditional |
|----|-------|--------|---------|-------------|
| `a.project_scan` | project_scan | pg.P0 | (40,40) | autonomous |
| `a.voice` | voice | pg.P0 | (40,140) | autonomous && has_feedback_source |
| `a.pulse` | pulse | pg.P0 | (40,240) | autonomous && has_metrics |
| `a.compete` | compete | pg.P0 | (40,340) | autonomous && has_competitors |
| `a.trace` | trace | pg.P0 | (40,440) | autonomous && has_replay |
| `a.spark` | spark | pg.P0 | (200,140) | autonomous |
| `a.rank` | rank | pg.P0 | (200,240) | autonomous |
| `a.sage` | sage | pg.P0 | (200,340) | autonomous (optional) |
| `a.magi0` | magi (tie-break) | pg.P0 | (200,440) | autonomous && tie_within_10pct |
| `g.boundary` | 👤 boundary confirm | pg.P0 | (200,560) | autonomous |

### 4.3 Phase 1 (Discovery)

| id | label | parent | (rx,ry) | conditional |
|----|-------|--------|---------|-------------|
| `a.plea` | plea | pg.P1 | (60,160) | always |
| `a.field` | field | pg.P1 | (60,300) | always |
| `a.echo1` | echo (current flow) | pg.P1 | (60,440) | existing_product |

### 4.4 Phase 2 / 3 / 4

| id | label | parent | (rx,ry) | conditional |
|----|-------|--------|---------|-------------|
| `a.riff` | riff | pg.P2 | (60,300) | always |
| `a.magi` | magi | pg.P3 | (60,300) | always |
| `g.split` | split decision | pg.P3 | (60,500) | event-driven |
| `a.accord` | accord | pg.P4 | (60,200) | always |
| `a.void` | void | pg.P4 | (60,360) | scope=Full |
| `a.scribe` | scribe | pg.P4 | (60,500) | scope>=Standard |

### 4.5 Phase 5 (parallel: Tech / UX) + Risk Gate

Tech column at x = 1820 onward, UX column at x = 2180 onward, Gate row at y = 660 onward.

| id | label | parent | (rx,ry) | conditional |
|----|-------|--------|---------|-------------|
| `a.atlas` | atlas | pg.P5 | (40,80) | always |
| `a.gateway` | gateway | pg.P5 | (40,200) | api_change |
| `a.schema` | schema | pg.P5 | (40,320) | db_change |
| `so.vision` | Vision (sub) | pg.P5 | (380,80) | ui_surface |
| `a.muse` | muse | pg.P5 | (380,180) | ui_surface |
| `a.palette` | palette | pg.P5 | (380,260) | ui_surface |
| `a.prose` | prose | pg.P5 | (380,340) | ui_surface |
| `a.flow` | flow | pg.P5 | (380,420) | motion |
| `a.frame` | frame | pg.P5 | (380,500) | figma |
| `a.forge` | forge | pg.P5 | (380,580) | ui_surface |
| `a.echo5` | echo | pg.P5 | (380,660) | ui_surface |
| `g.omen` | omen | pg.P5 | (200,720) | always |
| `g.ripple` | ripple | pg.P5 | (340,720) | always |
| `g.gate` | Risk Gate | pg.P5 | (480,720) | always |

### 4.6 Phase 6 (Implementation, Codex CLI)

`engineBoundary` sits at the phase boundary. `so.orbit` is a collapsible group.

| id | label | parent | (rx,ry) | conditional |
|----|-------|--------|---------|-------------|
| `eb.claude_to_codex` | engine boundary | between P5/P6 | x=2520 | always |
| `so.orbit` | Orbit (loop) | pg.P6 | (40,80) | always |
| `a.builder` | builder | pg.P6 | (200,160) | always |
| `a.artisan` | artisan | pg.P6 | (200,260) | ui_surface |
| `a.vitrine` | vitrine | pg.P6 | (200,360) | components_added |
| `a.judge` | judge | pg.P6 | (200,460) | always |
| `a.radar` | radar | pg.P6 | (200,560) | always |
| `a.voyager` | voyager | pg.P6 | (200,660) | ui_flows |

### 4.7 Ship

| id | label | parent | (rx,ry) |
|----|-------|--------|---------|
| `a.guardian` | guardian | pg.Ship | (40,300) |
| `a.launch` | launch | pg.Ship | (40,440) |

## 5. Edge Definitions (primary edges only)

| id | source → target | type | label | conditional |
|----|-----------------|------|-------|-------------|
| `e.p0_to_p1` | `g.boundary → a.plea` | flow | "auto goal" | autonomous |
| `e.p1_to_p2` | `a.plea → a.riff` | flow | — | always |
| `e.p2_to_p3` | `a.riff → a.magi` | flow | — | always |
| `e.p3_to_p4` | `a.magi → a.accord` | flow | "verdict + AC seed" | always |
| `e.p4_to_p5tech` | `a.accord → a.atlas` | flow | — | always |
| `e.p4_to_p5ux` | `a.accord → so.vision` | flow | — | ui_surface |
| `e.tech_to_gate` | `a.atlas → g.gate` | flow | — | always |
| `e.ux_to_gate` | `a.echo5 → g.gate` | flow | — | ui_surface |
| `e.gate_to_p6` | `g.gate → so.orbit` | flow | "go=true" | always |
| `e.gate_back_p4` | `g.gate → a.accord` | escalation | "no-go" | event-driven |
| `e.engine_switch` | `g.gate → eb.claude_to_codex` | engineBoundary | "claude → codex" | always |
| `e.orbit_to_ship` | `so.orbit → a.guardian` | flow | "loop converged" | always |
| `e.guardian_to_launch` | `a.guardian → a.launch` | flow | — | always |

Edges internal to sub-orchestrators (vision → muse → … → echo5; orbit → builder/judge/…) are defined within their subflows.

## 6. State Model (rendering side)

Each node carries the following `data`, populated by folding events into state.

```ts
type AgentNodeData = {
  agentName: string;
  phase: Phase;
  status: "pending" | "running" | "done" | "error" | "skipped" | "waiting";
  startedAt?: string;
  endedAt?: string;
  duration_ms?: number;
  lastTool?: string;
  progress?: number;       // 0–1
  conditional: boolean;    // whether the display condition is satisfied
};
```

The UI inspects `status` and `progress` to switch CSS classes / Framer Motion variants (see `UI.md §3`).

## 7. Extension Points

- A separate topology for `feature` / `bug` recipes can live in `topology-feature.ts`
- Custom agents can be loaded from `extra-agents.ts` and mounted on top
- Layout coordinates can be overridden by a theme file (compact vs. normal density)

## 8. Related

- `EVENTS.md` — how state is folded from events
- `UI.md` — how this topology is presented on screen
- `DESIGN.md §5.4` — client-side composition
