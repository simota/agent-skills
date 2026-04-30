# run-dash · sample (MVP)

A runnable reference implementation of the run-dash spec at `_common/run-dash/`.
This sample exists so that:

- Schema (`EVENTS.md`), topologies (`TOPOLOGIES/*.md`), and UI behaviour (`UI.md`) are verifiable end-to-end
- `forge` / `builder` can use it as a golden reference when generating per-repo dashboards via `GENERATION.md`

> Renamed from `apex-dash`. The original prototype focused on apex; the implementation works for any agent run, so the package is now `run-dash`. The `apex-emit.sh` shell helper remains as a thin alias of `run-emit.sh` for backward compatibility.

## Stack

| Layer | Choice |
|-------|--------|
| Server | Bun + Hono (SSE) |
| Client | React 18 + @xyflow/react v12 |
| Bundler | Vite 5 |
| State | zustand 5 |
| Watcher | chokidar 4 |
| Charts | Recharts 2 |

## Run

```sh
cd _common/run-dash/sample
bun install
bun run dev
# open http://127.0.0.1:5173
```

Two processes start:

- **server** on `127.0.0.1:5757` — tails `events/<run-id>/events.jsonl`
- **client** on `127.0.0.1:5173` — Vite dev server, proxies `/api/*` to the server

## Demo data

Three pre-seeded runs ship with the sample:

| run-id | run_kind | What it shows |
|--------|----------|---------------|
| `apex-20260430-120000-a3f` | `apex` | Full P0–Ship apex run with risk gate, orbit metrics, engine boundary |
| `feature-20260501-093000-b7e` | `feature` | Discover → Spec → Implement → Ship with spec_gate |
| `manual-20260502-141500-c2d` | `manual` | Ad-hoc lens / scout / fossil exploration with parent_agent + depth |

The dashboard reads `run_start.run_kind` and switches modes accordingly. The header shows the run_kind badge in a colour matching the mode (apex = blue, feature = emerald, bug = red, manual = slate).

## Endpoints

| Route | Purpose |
|-------|---------|
| `GET /api/runs` | List run-ids in `events/` |
| `GET /api/events/:run` | SSE stream of events.jsonl (existing + tail) |
| `GET /api/postmortem/:run` | Generate / read postmortem markdown |

## Postmortem

When a run finishes, the **📄 postmortem** button in the header is enabled. It hits `GET /api/postmortem/:run` which:

- folds events through the same reducer the UI uses
- computes phase / step / agent durations, bottleneck, orbit metrics, engine boundaries
- writes `events/<run-id>/postmortem.md` (atomic) and returns the markdown for browser viewing

CLI form:

```sh
bun run scripts/postmortem.ts                       # newest run
bun run scripts/postmortem.ts apex-20260430-120000-a3f
```

A pre-generated `events/apex-20260430-120000-a3f/postmortem.md` ships so the format is visible without running anything. Spec: `_common/run-dash/POSTMORTEM.md`.

## Limits of this MVP

The sample implements the **apex mode UI** end-to-end but only **partial recipe / generic mode UI**:

- Recipe-mode step rail and bug/feature topology are not yet wired into the canvas (still uses apex topology data). The state reducer **does** track `step_enter` / `step_exit` and exposes `currentStep` / `steps[]` — recipes mode UI hookup is left as a follow-up
- Generic-mode dynamic DAG (dagre) and timeline are not yet rendered. The reducer **does** populate `dynamicNodes[]` from `parent_agent` / `depth`, ready for a panel to consume
- No replay slider, no theme toggle, no keyboard shortcuts
- No run-picker dropdown (uses newest run automatically)

A production dashboard generated via `GENERATION.md §5` is expected to fill these gaps.
