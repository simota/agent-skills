# Topology — `run_kind=apex`

Declarative topology data for the **apex** mode. At implementation time, transcribe this into `web/src/lib/topologies/apex.ts` and feed it to xyflow.

> Apex is one `run_kind` of run-dash. Other recipes have their own `TOPOLOGIES/<recipe>.md` and follow the same shape. Generic mode (`TOPOLOGIES/generic.md`) builds nodes dynamically from `parent_agent` / `depth`.

---

## 1. Design Principles

1. **Static layout**: positions are predefined; state is conveyed through motion
2. **Phase groups**: P0–Ship are subflow containers
3. **Sub-orchestrators**: Vision and Orbit are collapsible groups
4. **Conditional rendering**: scope / UI flag flips visibility per agent

## 2. Extension Kinds Recognised

| `kind` | Purpose |
|--------|---------|
| `phase_enter` / `phase_exit` | Drives phase rail and group highlight |
| `risk_gate` | Drives Risk Gate radar |
| `orbit_iter` | Drives Orbit chart |
| `engine_switch` | Drives engine boundary visualisation |
| `checkpoint_wait` / `checkpoint_resolved` | Drives checkpoints panel |

## 3. Grid and Coordinates

- Horizontal: phase progression (X). Each phase is 360 px wide
- Vertical: subtracks (Y). Tech top, UX bottom
- Grid unit: 80 px

```
   X →
   ┌────────┬────────┬───────┬───────┬───────┬─────────────────┬──────────────┬──────┐
Y  │  P0    │  P1    │  P2   │  P3   │  P4   │  P5 (parallel)  │  P6 (Codex)  │ Ship │
↓  │ 360px  │ 360px  │ 360px │ 360px │ 360px │ 720px           │ 480px        │ 240px│
   └────────┴────────┴───────┴───────┴───────┴─────────────────┴──────────────┴──────┘
```

Total ~3,300 px. Canvas supports zoom/pan.

## 4. Node Types

| `type` | Style |
|--------|-------|
| `phaseGroup` | Rounded rectangle, light tint, label |
| `agent` | Circle + text; animated by state |
| `subOrchestrator` | Double circle, holds specialists |
| `gate` | Diamond, coloured by verdict |
| `engineBoundary` | Vertical dashed bar |

## 5. Phase Groups

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

## 6. Agents

### 6.1 Phase 0 (autonomous mode only)

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
| `a.magi0` | magi (tie-break) | pg.P0 | (200,440) | autonomous && tie |
| `g.boundary` | 👤 boundary confirm | pg.P0 | (200,560) | autonomous |

### 6.2 Phase 1

| id | label | parent | (rx,ry) | conditional |
|----|-------|--------|---------|-------------|
| `a.plea` | plea | pg.P1 | (60,160) | always |
| `a.researcher` | researcher | pg.P1 | (60,300) | always |
| `a.echo1` | echo (current) | pg.P1 | (60,440) | existing_product |

### 6.3 Phase 2 / 3 / 4

| id | label | parent | (rx,ry) | conditional |
|----|-------|--------|---------|-------------|
| `a.riff` | riff | pg.P2 | (60,300) | always |
| `a.magi` | magi | pg.P3 | (60,300) | always |
| `g.split` | split decision | pg.P3 | (60,500) | event-driven |
| `a.accord` | accord | pg.P4 | (60,200) | always |
| `a.void` | void | pg.P4 | (60,360) | scope=Full |
| `a.scribe` | scribe | pg.P4 | (60,500) | scope>=Standard |

### 6.4 Phase 5 + Risk Gate

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

### 6.5 Phase 6 (Codex CLI)

| id | label | parent | (rx,ry) | conditional |
|----|-------|--------|---------|-------------|
| `eb.claude_to_codex` | engine boundary | between P5/P6 | x=2520 | always |
| `so.orbit` | Orbit (loop) | pg.P6 | (40,80) | always |
| `a.builder` | builder | pg.P6 | (200,160) | always |
| `a.artisan` | artisan | pg.P6 | (200,260) | ui_surface |
| `a.showcase` | showcase | pg.P6 | (200,360) | components_added |
| `a.judge` | judge | pg.P6 | (200,460) | always |
| `a.radar` | radar | pg.P6 | (200,560) | always |
| `a.voyager` | voyager | pg.P6 | (200,660) | ui_flows |

### 6.6 Ship

| id | label | parent | (rx,ry) |
|----|-------|--------|---------|
| `a.guardian` | guardian | pg.Ship | (40,300) |
| `a.launch` | launch | pg.Ship | (40,440) |

## 7. Edges

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
| `e.guardian_launch` | `a.guardian → a.launch` | flow | — | always |

## 8. Node Data Schema

```ts
type AgentNodeData = {
  agentName: string;
  phase: Phase;
  status: "pending" | "running" | "done" | "error" | "skipped" | "waiting";
  startedAt?: string;
  endedAt?: string;
  duration_ms?: number;
  lastTool?: string;
  progress?: number;
  conditional: boolean;
  parentAgent?: string;
  depth?: number;
};
```

## 9. Related

- `EVENTS.md` — how state is folded
- `UI.md` — how this topology is rendered
- `TOPOLOGIES/feature.md` / `bug.md` / `generic.md` — siblings
