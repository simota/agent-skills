# run-dash

Design specification for a **real-time Web dashboard** that visualises any agent run — `/nexus apex`, other Nexus recipes (`feature` / `bug` / `refactor`), single-skill invocations, and Codex CLI subagents.

This directory contains specs only — no executable code. Per repository, generator skills (`forge` / `builder` / `sigil`) read this spec and produce a tailored instance under `<repo>/.agents/run-dash-app/`.

> **Renamed from `apex-dash`.** The original target was apex specifically; the architecture turned out to be a thin shell over an event log, so it was generalised. apex is now one `run_kind` among several. The `apex-emit.sh` shell helper remains as a thin alias of `run-emit.sh` for backward compatibility.

## Goals

- Observe **any** agent run in real time, regardless of recipe or topology
- Make node and edge motion the primary signal of progress
- Replay completed runs for postmortem and Lore training data
- Receiver-only — preserve hub-and-spoke routing without coupling

## Three Modes

| Mode | When | Layout |
|------|------|--------|
| **`apex`** | `run_kind=apex` | Fixed phase topology (P0–Ship) + Risk Gate + Orbit chart |
| **`recipe`** | `run_kind=feature` / `bug` / `refactor` / … | Recipe-specific step rail + recipe topology |
| **`generic`** | `run_kind=manual` / unknown | Dynamic DAG (built from `parent_agent` / `depth`) + timeline |

The dashboard inspects `run_start.run_kind` and switches mode automatically. A mode picker lets the user override.

## Files

| File | Contents | Read when |
|------|----------|-----------|
| `README.md` | Overview, generation flow, file index | First |
| `DESIGN.md` | Architecture, tech stack, file layout | Before implementation |
| `EVENTS.md` | events.jsonl core schema + extension kinds | Implementing producer or store |
| `UI.md` | Layout, panel specs, animation specs, all 3 modes | Implementing frontend |
| `INTEGRATION.md` | run-emit protocol, Claude Code hooks, auto-spawn | Wiring up integration |
| `POSTMORTEM.md` | Postmortem generation per recipe + Lore handoff | Implementing the postmortem flow |
| `GENERATION.md` | Per-repo generation prompt and file manifest | Materialising the dashboard |
| `TOPOLOGIES/apex.md` | Phase topology for apex runs | Implementing apex mode |
| `TOPOLOGIES/feature.md` | Step rail and topology for feature recipe | Implementing recipe mode |
| `TOPOLOGIES/bug.md` | Step rail and topology for bug recipe | Implementing recipe mode |
| `TOPOLOGIES/generic.md` | Dynamic DAG construction algorithm | Implementing generic mode |

## Generation Flow

```
First /nexus <recipe> starts (or hooks fire)
       │
       ▼
Pre-flight: does <repo>/.agents/run-dash-app/ exist?
       │
       ├── exists → spawn `bun run dev` directly
       │
       └── missing
              │
              ▼
       Call forge/builder with the prompt in GENERATION.md
              │
              ▼
       Write the full file set to <repo>/.agents/run-dash-app/
              │
              ▼
       Smoke test passes
              │
              ▼
       Continue normally + auto-open browser
```

For long-lived sessions where the user wants every Agent tool call observed without changing skills, the **Claude Code hooks** path (`INTEGRATION.md §4`) auto-emits `agent_start` / `agent_end` / `tool_use` for any session — no per-skill instrumentation needed.

## Two Deployment Modes

| Mode | Dashboard | Events root | Best for |
|------|-----------|-------------|----------|
| **Global** | `~/.claude/skills/_common/run-dash/sample/` (1 process) | `~/.claude/run-dash/` | Personal dev — one dashboard for all projects |
| **Per-repo** | `<repo>/.agents/run-dash-app/` (one per repo) | `<repo>/.agents/run-dash/` | Team dev — observability shared via the repo |

Both modes coexist; per-recipe runs (`apex` / `feature` / `bug`) and per-session runs (`manual`) can mix in either mode. See `INTEGRATION.md §9 Global Usage` for the recommended global setup.

## Storage Path

```
<repo>/.agents/run-dash/<run-id>/events.jsonl
```

`run-id` is `<run_kind>-YYYYMMDD-HHMMSS-<short-hash>`, e.g. `apex-…`, `feature-…`, `manual-…`.

## Design Principles

1. **`events.jsonl` is the single source of truth** — server only tails and broadcasts
2. **Receiver only** — coupling is one emit helper; no new agent-to-agent traffic
3. **Mode-pluggable** — schema and topology are split into core and extension; UI swaps modes per `run_kind`
4. **Event sourcing** — full state can be rebuilt from events on reload or reconnect
5. **Side-effect free** — observation must not perturb the run
6. **Local first** — listens on localhost only, no auth

## Non-Goals

- Production SLO / long-term trend monitoring (`beacon`)
- Skill ecosystem-wide overview (`realm`)
- Test intelligence (`vista`)
- Becoming a registered skill — this stays a per-run companion tool

## Related

- `nexus/SKILL.md` and `nexus/references/apex-recipe.md` — recipes that emit
- `_common/SUBAGENT.md` — Codex CLI subagent contract
- `_common/HANDOFF.md` — agent handoff conventions
- `_common/scripts/run-emit.sh` — reference emit helper
- `_common/scripts/apex-emit.sh` — backward-compat alias

## Versioning

Specs are versioned. Every materialised dashboard records the source commit hash in `<repo>/.agents/run-dash-app/.spec-version` (see `GENERATION.md`).
