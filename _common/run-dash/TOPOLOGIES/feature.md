# Topology — `run_kind=feature`

Declarative topology data and step rail for the **feature** recipe (Nexus). At implementation time, transcribe into `web/src/lib/topologies/feature.ts`.

---

## 1. Step Rail

`feature` runs use a step rail (4 steps) instead of apex's phase rail.

| step id | label | description |
|---------|-------|-------------|
| `Discover` | Discover | Persona / demand validation |
| `Spec` | Spec | Acceptance criteria + constraints |
| `Implement` | Implement | Build + per-iteration review |
| `Ship` | Ship | PR / CHANGELOG / launch |

State transitions are driven by `step_enter` / `step_exit` events with `meta.step` matching one of the step ids above.

## 2. Extension Kinds Recognised

| `kind` | Drives |
|--------|--------|
| `step_enter` / `step_exit` | step rail and group highlight |
| `spec_gate` | Spec quality gate visualisation in the right rail / mid panel |
| `agent_start` / `agent_end` / `tool_use` | shared core |

## 3. Grid

Each step lane is 360 px wide. Right-most "Ship" lane is 240 px.

```
   X →
   ┌──────────┬──────────┬─────────────────┬──────────┐
Y  │ Discover │   Spec   │ Implement (loop)│   Ship   │
↓  │ 360px    │ 360px    │ 540px           │ 240px    │
   └──────────┴──────────┴─────────────────┴──────────┘
```

Total ~1,500 px.

## 4. Step Groups

| id | label | x | y | w | h |
|----|-------|---|---|---|---|
| `sg.Discover` | Discover | 0 | 0 | 360 | 600 |
| `sg.Spec` | Spec | 360 | 0 | 360 | 600 |
| `sg.Implement` | Implement | 720 | 0 | 540 | 600 |
| `sg.Ship` | Ship | 1260 | 0 | 240 | 600 |

## 5. Agents

### 5.1 Discover

| id | label | parent | (rx,ry) | conditional |
|----|-------|--------|---------|-------------|
| `a.spark` | spark | sg.Discover | (60,140) | always |
| `a.researcher` | researcher | sg.Discover | (60,260) | optional (research_required) |
| `a.echo` | echo | sg.Discover | (60,380) | existing_product |

### 5.2 Spec

| id | label | parent | (rx,ry) | conditional |
|----|-------|--------|---------|-------------|
| `a.accord` | accord | sg.Spec | (60,180) | always |
| `a.scribe` | scribe | sg.Spec | (60,320) | external_review |
| `g.spec_gate` | spec gate | sg.Spec | (60,460) | always |

### 5.3 Implement (orbit-style mini-loop)

| id | label | parent | (rx,ry) | conditional |
|----|-------|--------|---------|-------------|
| `so.orbit` | orbit (mini) | sg.Implement | (40,80) | always |
| `a.builder` | builder | sg.Implement | (220,140) | always |
| `a.artisan` | artisan | sg.Implement | (220,240) | ui_surface |
| `a.judge` | judge | sg.Implement | (220,340) | always |
| `a.radar` | radar | sg.Implement | (220,440) | always |

### 5.4 Ship

| id | label | parent | (rx,ry) |
|----|-------|--------|---------|
| `a.guardian` | guardian | sg.Ship | (40,200) |
| `a.launch` | launch | sg.Ship | (40,360) |

## 6. Edges

| id | source → target | type | label | conditional |
|----|-----------------|------|-------|-------------|
| `e.discover_to_spec` | `a.spark → a.accord` | flow | "demands" | always |
| `e.spec_to_implement` | `a.accord → so.orbit` | flow | "L3 ACs" | always |
| `e.spec_gate_block` | `g.spec_gate → a.accord` | escalation | "fail" | event-driven |
| `e.implement_to_ship` | `so.orbit → a.guardian` | flow | "loop converged" | always |
| `e.guardian_launch` | `a.guardian → a.launch` | flow | — | always |

## 7. Right Rail Adaptation

- Risk Gate radar: hidden (apex-only)
- Active agents: shown
- Spec gate verdict: surfaced as a small badge in the mid panel
- Engine switch: hidden by default (feature recipe stays in claude_code unless explicitly crossed)

## 8. Postmortem Hooks

`server/postmortem/feature.ts` adds these sections to the common template:

- Spec gate verdict
- Implement loop iterations (if orbit was used)
- Files touched count

## 9. Related

- `EVENTS.md §4.2` — `step_enter` / `step_exit` / `spec_gate` extension kinds
- `INTEGRATION.md §2.4` — feature emit points
- `TOPOLOGIES/apex.md` / `bug.md` / `generic.md` — siblings
