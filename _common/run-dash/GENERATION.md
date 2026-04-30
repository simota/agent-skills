# run-dash — Generation Spec

Defines the inputs, generator prompt, output manifest, customisation surface, and verification steps for **per-repo auto-generation** of a dashboard.

---

## 1. Generation Strategy

- **Generator skill**: `forge` (rapid prototype) or `builder` (production grade). Default `forge`
- **Output location**: `<repo>/.agents/run-dash-app/`
- **Source of truth**: every `.md` file under `_common/run-dash/`
- **Reproducibility**: source commit hash persisted to `.spec-version`
- **Idempotency**: skip if exists; pass `--regenerate` to rebuild

## 2. Pre-Scan Inputs

### 2.1 Repository Information

| Item | Source | Default |
|------|--------|---------|
| `repo_root` | `git rev-parse --show-toplevel` | cwd |
| `repo_name` | `basename $repo_root` | "project" |
| `package_manager` | `bun.lockb` / `pnpm-lock.yaml` / `yarn.lock` / `package-lock.json` | bun |
| `node_version` | `.nvmrc` / `package.json#engines.node` | "20" |
| `existing_ports` | `dev`/`start` script extraction | [] |
| `tailwind_version` | existing dependency | latest |
| `has_typescript` | `tsconfig.json` presence | true |
| `gitignored_paths` | existing `.gitignore` | [] |
| `recipes_in_use` | grep `run_kind=` in events / nexus references | apex |

### 2.2 Skill Ecosystem Information

| Item | Source |
|------|--------|
| `apex_topology_version` | header of `_common/run-dash/TOPOLOGIES/apex.md` |
| `events_schema_version` | header of `_common/run-dash/EVENTS.md` |
| `spec_commit_hash` | `git -C ~/.claude/skills rev-parse HEAD` |

### 2.3 Port Selection

`5757, 5758, 5759, …` skipping `existing_ports`. Verify via `netstat -an | grep LISTEN`.

## 3. Output Manifest

```
<repo>/.agents/run-dash-app/
├─ .spec-version                  # source commit hash
├─ .gitignore                     # node_modules / dist / .runtime.log
├─ package.json
├─ tsconfig.json
├─ tsconfig.node.json
├─ vite.config.ts
├─ tailwind.config.ts
├─ postcss.config.js
├─ README.md
├─ server/
│  ├─ index.ts                    # Hono entry
│  ├─ tailer.ts                   # chokidar wrapper
│  ├─ state.ts                    # event → state reducer
│  ├─ postmortem/
│  │  ├─ index.ts                 # dispatcher
│  │  ├─ apex.ts
│  │  ├─ feature.ts
│  │  ├─ bug.ts
│  │  └─ generic.ts
│  └─ routes/
│     ├─ runs.ts
│     ├─ events.ts                # SSE
│     ├─ replay.ts                # SSE (throttled)
│     └─ postmortem.ts
├─ web/
│  ├─ index.html
│  └─ src/
│     ├─ main.tsx / App.tsx / store.ts
│     ├─ index.css
│     ├─ hooks/
│     │  ├─ useSSE.ts
│     │  └─ useReplay.ts
│     ├─ modes/
│     │  ├─ ApexMode.tsx
│     │  ├─ RecipeMode.tsx
│     │  └─ GenericMode.tsx
│     ├─ panels/
│     │  ├─ Header.tsx
│     │  ├─ PhaseRail.tsx
│     │  ├─ StepRail.tsx
│     │  ├─ Topology.tsx
│     │  ├─ DynamicGraph.tsx
│     │  ├─ Timeline.tsx
│     │  ├─ ActiveAgents.tsx
│     │  ├─ RiskGateRadar.tsx
│     │  ├─ OrbitChart.tsx
│     │  ├─ ToolHistogram.tsx
│     │  ├─ Checkpoints.tsx
│     │  ├─ EngineSwitch.tsx
│     │  └─ EventStream.tsx
│     ├─ nodes/
│     │  ├─ PhaseGroupNode.tsx
│     │  ├─ AgentNode.tsx
│     │  └─ SubOrchestratorNode.tsx
│     ├─ edges/
│     │  ├─ FlowEdge.tsx
│     │  └─ EngineBoundaryEdge.tsx
│     ├─ lib/
│     │  ├─ topologies/
│     │  │  ├─ apex.ts
│     │  │  ├─ feature.ts
│     │  │  ├─ bug.ts
│     │  │  ├─ refactor.ts
│     │  │  └─ dynamic.ts
│     │  ├─ animations.ts
│     │  ├─ colors.ts
│     │  └─ time.ts
│     └─ types/
│        ├─ events.ts             # zod schema mirroring EVENTS.md
│        └─ state.ts
└─ scripts/
   ├─ smoke.ts                    # boot + SSE check
   └─ postmortem.ts               # CLI postmortem generator
```

## 4. Required Dependencies (`package.json`)

```jsonc
{
  "name": "run-dash-app",
  "private": true,
  "type": "module",
  "scripts": {
    "dev":   "concurrently -k \"bun run server/index.ts\" \"vite\"",
    "build": "vite build && bun build server/index.ts --target=bun --outfile=dist/server.js",
    "start": "bun run dist/server.js",
    "smoke": "bun run scripts/smoke.ts"
  },
  "dependencies": {
    "hono": "^4",
    "chokidar": "^4",
    "zod": "^3"
  },
  "devDependencies": {
    "react": "^18",
    "react-dom": "^18",
    "@xyflow/react": "^12",
    "@dagrejs/dagre": "^1",
    "recharts": "^2",
    "framer-motion": "^11",
    "zustand": "^5",
    "@tanstack/react-virtual": "^3",
    "tailwindcss": "^4",
    "@tailwindcss/postcss": "^4",
    "vite": "^5",
    "@vitejs/plugin-react": "^4",
    "typescript": "^5",
    "@types/react": "^18",
    "@types/react-dom": "^18"
  }
}
```

## 5. Generator Prompt (passed to forge / builder)

A copy-pasteable template. `<...>` placeholders filled by the pre-scan results.

```
[ROLE] forge / rapid prototype builder

[GOAL]
Generate a complete `run-dash-app` Web dashboard at <repo_root>/.agents/run-dash-app/.
This dashboard visualises any agent run (apex / feature / bug / refactor / manual / single-agent)
in real time with React + xyflow.

[INPUTS]
- spec dir: ~/.claude/skills/_common/run-dash/
  - DESIGN.md     : architecture & file layout
  - EVENTS.md     : events.jsonl schema (core + extensions)
  - UI.md         : layout / animation / theme / shortcuts / 3 modes
  - INTEGRATION.md: emit protocol & auto-spawn flow & Claude Code hooks
  - POSTMORTEM.md : per-recipe postmortem templates
  - TOPOLOGIES/   : per-recipe topology data (apex / feature / bug / generic)
- repo info:
  - repo_root        = <repo_root>
  - package_manager  = <bun|pnpm|npm|yarn>
  - node_version     = <e.g. 20>
  - chosen_port      = <5757+, free>
  - has_typescript   = <true|false>
- spec commit hash  = <hash>

[OUTPUT]
- write all files under <repo_root>/.agents/run-dash-app/ exactly as listed in
  GENERATION.md §3 (manifest).
- write .spec-version = "<hash>"
- write .gitignore = node_modules/, dist/, .runtime.log
- ensure `bun run dev` starts the dashboard and the SPA renders an empty
  generic-mode timeline when no events are present.

[CONSTRAINTS]
1. Do NOT modify anything outside <repo_root>/.agents/run-dash-app/.
2. Do NOT add network calls beyond localhost.
3. Do NOT include authentication.
4. Bind server to 127.0.0.1:<chosen_port> only.
5. Mirror schema in EVENTS.md exactly (zod schema in web/src/types/events.ts).
6. Mirror topologies in TOPOLOGIES/* (lib/topologies/*.ts).
7. Implement all 3 modes per UI.md (apex / recipe / generic).
8. Implement node/edge animations per UI.md §10-§11.
9. Implement keyboard shortcuts per UI.md §14.
10. Implement replay mode per UI.md §15.
11. Implement postmortem dispatcher per POSTMORTEM.md.
12. Pass `bun run smoke`.

[ACCEPTANCE CRITERIA]
- `bun install` succeeds
- `bun run dev` opens http://127.0.0.1:<chosen_port> and renders SPA
- Test events.jsonl in .agents/run-dash/test-run/ drives UI:
   - apex run: phase rail, topology, risk gate, orbit chart, postmortem button
   - feature run: step rail, recipe topology
   - manual run: dynamic DAG + timeline
- No console errors, no React warnings, TypeScript strict passes

[DELIVER]
- print a tree of created files
- print the launch command (`bun run dev`)
- print the smoke result
```

## 6. Per-Repo Customisation

| Item | Default | Override |
|------|---------|----------|
| Port | auto from 5757 | `<dash_root>/config.json` → `"port": N` |
| Theme | dark | `"theme": "light"` |
| Density | normal | `"density": "compact"` |
| Logo | run-dash wordmark | `web/public/logo.svg` |
| Topology | shipped recipes | add `lib/topologies/<recipe>.local.ts` to override |
| Extra panel | none | `web/src/panels/local/*.tsx` registered via `panels/index.ts` |
| Postmortem template | per-recipe | `server/postmortem/<recipe>.local.ts` |

## 7. Verification (smoke test)

`scripts/smoke.ts` spec:

1. Start server in a separate process (port via CLI arg)
2. Within 5s, confirm `GET /api/runs` returns 200
3. Append 5 events to a test `.agents/run-dash/smoke-run/events.jsonl`
4. Connect SSE to `GET /api/events/smoke-run`; assert all 5 within 5s
5. Kill server, exit 0

Failure: non-zero exit + stderr; auto-spawn falls back gracefully.

## 8. Regeneration and Compatibility

| Scenario | Behavior |
|----------|----------|
| Minor schema update | Existing dashboard continues to work |
| Major update | Banner on launch; `--regenerate` to rebuild |
| Generation failure | Keep previous; record `note` in events.jsonl (auto rollback) |
| Mid-generation interruption | `.generation.lock`; auto-clean on next start |

## 9. Privacy / Security Checklist

- [ ] localhost binding only
- [ ] No authentication code
- [ ] Events writes confined to repo
- [ ] node_modules in `.gitignore`
- [ ] No third-party telemetry
- [ ] Env vars never in web bundle (server-side only)

## 10. Sample Orchestration (Nexus side, pseudocode)

```python
def ensure_dashboard(repo_root):
    dash = f"{repo_root}/.agents/run-dash-app"
    if exists(dash) and version_match(dash, current_spec_hash):
        return dash
    if exists(dash):
        warn("run-dash spec mismatch — regenerate? [y/N]")
        if not confirmed: return dash  # use stale
    spawn_agent("forge", prompt=GENERATION_PROMPT.format(
        repo_root=repo_root,
        package_manager=detect_package_manager(repo_root),
        node_version=detect_node_version(repo_root),
        chosen_port=pick_free_port(starting=5757),
        has_typescript=exists(f"{repo_root}/tsconfig.json"),
        hash=current_spec_hash(),
    ))
    if not run_smoke(dash):
        emit_error("dashboard smoke failed; continuing without dashboard")
        return None
    return dash
```

## 11. Related

- `DESIGN.md` — what to build
- `EVENTS.md` / `UI.md` / `TOPOLOGIES/*` — how to build (referenced by the prompt)
- `INTEGRATION.md` — auto-spawn, emit, Claude Code hooks
- `POSTMORTEM.md` — postmortem templates
