# run-dash — Events Schema

Schema definition for `events.jsonl`. Producer (run-emit helper, Claude Code hooks, Nexus recipes, Codex subagents) and consumer (dashboard server / client) **must follow the same schema**. Schema changes update this document and bump `.spec-version`.

The schema is split into a **core** (universal) and **extensions** (per `run_kind`). Generic mode renders only the core; apex / recipe modes additionally interpret extension kinds.

---

## 1. File Conventions

| Item | Value |
|------|-------|
| Path | `<repo>/.agents/run-dash/<run-id>/events.jsonl` |
| Format | JSON Lines (1 line per event, UTF-8, LF terminator) |
| Writes | Append-only. Past lines must never be rewritten |
| Ordering | Globally ordered by `seq`. Writer guarantees order via mkdir lock |
| Size budget | 200–800 bytes per event; 0.5–10 MB per run |
| Retention | Run directories older than 30 days are reaped by the generator |

`run-id` format: `<run_kind>-YYYYMMDD-HHMMSS-<short-hash>` (e.g. `apex-20260430-120000-a3f`, `feature-20260501-093000-b7e`, `manual-20260502-141500-c2d`).

## 2. Core Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `ts` | string (ISO8601 UTC) | ✓ | Event timestamp |
| `seq` | int | ✓ | Per-run sequence number, starts at 1, no gaps |
| `run_id` | string | ✓ | `<run_kind>-YYYYMMDD-HHMMSS-<hash>` |
| `kind` | string | ✓ | Event kind (core or extension) |
| `run_kind` | string | (`run_start` only) | `apex` / `feature` / `bug` / `refactor` / `manual` / `single-agent` / custom |
| `recipe` | string | optional | Nexus recipe name when relevant |
| `phase` | string | optional | Phase identifier (mainly apex / recipe modes) |
| `agent` | string | (kind-dependent) | Lowercase agent name (e.g. `plea`, `builder`) |
| `engine` | string | optional | `claude_code` or `codex_cli` |
| `parent_agent` | string | optional | Caller agent — used to build dynamic DAGs |
| `depth` | int | optional | Nesting depth from the top-level orchestrator |
| `meta` | object | optional | Kind-specific extras (flat, one nesting level) |

`meta` snippets (e.g. tool argument digests) are capped at 280 characters.

## 3. Core Event Kinds

| `kind` | Purpose | Required extras |
|--------|---------|-----------------|
| `run_start` | Run begins | `run_kind`. Optional: `meta.goal`, `meta.mode`, `meta.scope`, `meta.labels` |
| `run_end` | Run ends | `meta.status` (`completed`/`aborted`/`error`), `meta.duration_ms` |
| `agent_start` | Agent invocation begins | `agent`. Optional: `phase`, `engine`, `parent_agent`, `depth`, `meta.input_ref?` |
| `agent_progress` | In-flight progress | `agent`, `meta.progress` (0–1), `meta.note?` |
| `agent_end` | Agent invocation ends | `agent`, `meta.status`, `meta.duration_ms`, `meta.output_ref?` |
| `tool_use` | Tool call within an agent | `agent`, `meta.tool`, `meta.snippet?`, `meta.duration_ms?`, `meta.exit_code?` |
| `error` | Failure | `meta.severity`, `meta.source`, `meta.message`, `meta.stack?` |
| `note` | Free-form diagnostic | `meta.text` |

## 4. Extension Event Kinds

Extensions are recognised by specific run_kinds; other modes treat them as opaque.

### 4.1 `apex` extensions

| `kind` | Purpose |
|--------|---------|
| `phase_enter` | Apex phase entered (`phase`, `meta.parallel_tracks?`) |
| `phase_exit` | Apex phase ended (`phase`, `meta.exit_gate`) |
| `checkpoint_wait` | Human confirmation waiting (`meta.label`, `meta.deadline?`, `meta.mode`) |
| `checkpoint_resolved` | Confirmation closed (`meta.label`, `meta.outcome`) |
| `risk_gate` | Risk Gate verdict (`meta.verdict`, `meta.axes`) |
| `orbit_iter` | One orbit loop iteration (`meta.iter`, `meta.convergence`, `meta.cost_per_task`, `meta.budget_used`, `meta.budget_max`, `meta.circuit`) |
| `engine_switch` | Engine boundary crossed (`meta.from`, `meta.to`, `meta.reason?`) |

### 4.2 `feature` / `bug` / `refactor` extensions

| `kind` | run_kind | Purpose |
|--------|----------|---------|
| `step_enter` | feature/bug/refactor | Recipe step entered (`meta.step`) |
| `step_exit` | feature/bug/refactor | Recipe step ended (`meta.step`, `meta.exit_gate`) |
| `spec_gate` | feature | Spec quality gate result |
| `rca_done` | bug | Root-cause analysis completed (`meta.cause_summary`) |
| `fix_proposed` | bug | Fix proposal ready (`meta.diff_lines`, `meta.touched_files`) |

Recipes can register additional kinds in their `TOPOLOGIES/<recipe>.md`.

## 5. JSON Schema (summary)

Materialised in `web/src/types/events.ts` as a zod schema. Conceptual definition:

```ts
type Event = {
  ts: string;
  seq: number;
  run_id: string;
  kind: EventKind;
  run_kind?: RunKind;
  recipe?: string;
  phase?: string;
  agent?: string;
  engine?: "claude_code" | "codex_cli";
  parent_agent?: string;
  depth?: number;
  meta?: Record<string, unknown>;
};

type RunKind =
  | "apex" | "feature" | "bug" | "refactor"
  | "manual" | "single-agent"
  | string;  // custom run_kinds are accepted

type EventKind =
  // core
  | "run_start" | "run_end"
  | "agent_start" | "agent_progress" | "agent_end"
  | "tool_use"
  | "error" | "note"
  // apex extensions
  | "phase_enter" | "phase_exit"
  | "checkpoint_wait" | "checkpoint_resolved"
  | "risk_gate" | "orbit_iter" | "engine_switch"
  // recipe extensions
  | "step_enter" | "step_exit"
  | "spec_gate" | "rca_done" | "fix_proposed"
  | string;
```

## 6. State Transition Rules (reducer spec)

| Event | Effect |
|-------|--------|
| `run_start` | `state.run_id`, `state.run_kind`, `state.recipe`, `state.goal`, `state.mode`, `state.scope`, `state.startedAt` |
| `agent_start` | push to `activeAgents`; ensure DAG node + edge from `parent_agent` |
| `agent_progress` | update `activeAgents[name].progress` |
| `agent_end` | move to `completedAgents` with status / duration |
| `tool_use` | update `activeAgents[name].lastTool`; bump `tool_counts[tool]` |
| `phase_enter` / `phase_exit` (apex) | update `state.phases[phase]` |
| `risk_gate` | set `state.riskGate` |
| `orbit_iter` | append to `state.orbit.iters` |
| `engine_switch` | set `state.engine`, push to `state.engineHistory` |
| `step_enter` / `step_exit` (recipe) | update `state.steps[step]` |
| `error` | push to `state.errors` (last 50 retained) |
| `run_end` | set `state.endedAt`, `state.finalStatus` |

Reducer **must not** reject unknown kinds — they are appended to the event stream and ignored by mode-specific panels.

## 7. Validation

Producer (emit helper, hooks) does **not** validate — best-effort append.
Consumer **must guard**:

- Invalid JSON → skip + record a `warn` in `state.errors`
- Unknown `kind` → accept; render in event stream with grey kind chip
- Missing or duplicated `seq` → warn but continue
- Unknown `agent` (not in topology) → place in "unplaced" cluster on dynamic DAG

## 8. Sample (apex)

```jsonl
{"ts":"2026-04-30T12:00:00.000Z","seq":1,"run_id":"apex-20260430-120000-a3f","kind":"run_start","run_kind":"apex","meta":{"goal":"passkey login","mode":"AUTORUN_FULL","scope":"Standard"}}
{"ts":"2026-04-30T12:00:01.000Z","seq":2,"run_id":"apex-20260430-120000-a3f","kind":"phase_enter","phase":"P1_Discovery"}
{"ts":"2026-04-30T12:00:02.000Z","seq":3,"run_id":"apex-20260430-120000-a3f","kind":"agent_start","agent":"plea","parent_agent":"nexus","depth":1,"phase":"P1_Discovery","engine":"claude_code"}
```

## 9. Sample (manual / generic)

```jsonl
{"ts":"2026-05-02T14:15:00.000Z","seq":1,"run_id":"manual-20260502-141500-c2d","kind":"run_start","run_kind":"manual","meta":{"goal":"explore database module","labels":["adhoc"]}}
{"ts":"2026-05-02T14:15:02.000Z","seq":2,"run_id":"manual-20260502-141500-c2d","kind":"agent_start","agent":"lens","parent_agent":"user","depth":1,"engine":"claude_code"}
{"ts":"2026-05-02T14:15:30.000Z","seq":3,"run_id":"manual-20260502-141500-c2d","kind":"tool_use","agent":"lens","meta":{"tool":"Read","snippet":"db/schema.sql"}}
```

## 10. Extension Policy

- New core kinds are backward compatible — older consumers ignore them
- Adding fields to existing kinds is allowed; removing fields is forbidden
- Adding enum values is allowed; removing them is forbidden
- Per-recipe extensions live in `TOPOLOGIES/<recipe>.md`
- Breaking changes bump the major `.spec-version`

## 11. Related

- `INTEGRATION.md` — emit helper and Claude Code hooks
- `TOPOLOGIES/*` — recipe-specific topology + extension kinds
- `DESIGN.md §4` — overall data flow
