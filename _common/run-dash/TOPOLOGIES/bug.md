# Topology — `run_kind=bug`

Declarative topology data and step rail for the **bug** recipe (Nexus). At implementation time, transcribe into `web/src/lib/topologies/bug.ts`.

---

## 1. Step Rail

`bug` runs use a 4-step rail.

| step id | label | description |
|---------|-------|-------------|
| `Reproduce` | Reproduce | Confirm reproduction + minimal repro case |
| `RCA` | RCA | Root-cause analysis |
| `Fix` | Fix | Patch + tests |
| `Verify` | Verify | Regression checks + ship |

State transitions are driven by `step_enter` / `step_exit` events with `meta.step` matching one of the step ids above.

## 2. Extension Kinds Recognised

| `kind` | Drives |
|--------|--------|
| `step_enter` / `step_exit` | step rail and group highlight |
| `rca_done` | Pinned panel showing the cause summary |
| `fix_proposed` | Mid panel showing diff lines + touched files |
| `agent_start` / `agent_end` / `tool_use` | shared core |

## 3. Grid

Each step lane is 320 px wide.

```
   X →
   ┌──────────┬──────────┬──────────┬──────────┐
Y  │Reproduce │   RCA    │   Fix    │ Verify   │
↓  │ 320px    │ 320px    │ 320px    │ 320px    │
   └──────────┴──────────┴──────────┴──────────┘
```

Total ~1,280 px.

## 4. Step Groups

| id | label | x | y | w | h |
|----|-------|---|---|---|---|
| `sg.Reproduce` | Reproduce | 0 | 0 | 320 | 540 |
| `sg.RCA` | RCA | 320 | 0 | 320 | 540 |
| `sg.Fix` | Fix | 640 | 0 | 320 | 540 |
| `sg.Verify` | Verify | 960 | 0 | 320 | 540 |

## 5. Agents

### 5.1 Reproduce

| id | label | parent | (rx,ry) | conditional |
|----|-------|--------|---------|-------------|
| `a.scout` | scout | sg.Reproduce | (60,160) | always |
| `a.triage` | triage | sg.Reproduce | (60,300) | severity>=high |

### 5.2 RCA

| id | label | parent | (rx,ry) | conditional |
|----|-------|--------|---------|-------------|
| `a.scout_rca` | scout (RCA) | sg.RCA | (60,160) | always |
| `a.trail` | trail | sg.RCA | (60,280) | regression_suspected |
| `a.specter` | specter | sg.RCA | (60,400) | concurrency_suspected |

### 5.3 Fix

| id | label | parent | (rx,ry) | conditional |
|----|-------|--------|---------|-------------|
| `a.builder` | builder | sg.Fix | (60,140) | always |
| `a.judge` | judge | sg.Fix | (60,260) | always |
| `a.radar` | radar | sg.Fix | (60,380) | always |

### 5.4 Verify

| id | label | parent | (rx,ry) | conditional |
|----|-------|--------|---------|-------------|
| `a.voyager` | voyager | sg.Verify | (60,140) | ui_flow_affected |
| `a.guardian` | guardian | sg.Verify | (60,280) | always |
| `a.launch` | launch | sg.Verify | (60,400) | release_required |

## 6. Edges

| id | source → target | type | label | conditional |
|----|-----------------|------|-------|-------------|
| `e.repro_to_rca` | `a.scout → a.scout_rca` | flow | "repro confirmed" | always |
| `e.rca_to_fix` | `a.scout_rca → a.builder` | flow | "cause" | always |
| `e.fix_to_verify` | `a.builder → a.guardian` | flow | "fix" | always |
| `e.verify_to_launch` | `a.guardian → a.launch` | flow | — | release_required |
| `e.fix_back_rca` | `a.judge → a.scout_rca` | escalation | "wrong cause" | event-driven |

## 7. Right Rail Adaptation

- Risk Gate radar: hidden
- RCA pinned card: shows `rca_done.meta.cause_summary` at the top of the right rail
- Fix metrics card: shows `fix_proposed.meta.diff_lines`, `meta.touched_files`
- Engine switch: hidden by default

## 8. Postmortem Hooks

`server/postmortem/bug.ts` adds these sections to the common template:

- Reproduction steps reference (`output_ref`)
- Root cause summary
- Fix proposal metrics (diff lines, touched files)
- Tests added (radar `agent_end.meta.tests_added` if available)

## 9. Related

- `EVENTS.md §4.2` — `step_enter` / `step_exit` / `rca_done` / `fix_proposed`
- `INTEGRATION.md §2.4` — bug emit points
- `TOPOLOGIES/apex.md` / `feature.md` / `generic.md` — siblings
