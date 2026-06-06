# apex-dash

Design specification for a **real-time Web dashboard** that visualises long-running `/nexus apex` sessions.
This directory contains specs only — no executable code. Per repository, generator skills (`forge` / `builder` / `sigil`) read this spec and produce a tailored instance under `<repo>/.agents/apex-dash/`.

## Goals

- Observe apex progress from Phase 0 through Ship on a single screen
- Make "what is happening right now" obvious through node and edge motion
- Replay completed runs for postmortem and Lore training data
- Preserve hub-and-spoke routing — receiver only, no upstream coupling

## Scope

- Primary target: `/nexus apex`
- Schema and topology data are pluggable, so the same dashboard can later cover `feature` / `bug` / `refactor` recipes

## Files

| File | Contents | Read when |
|------|----------|-----------|
| `README.md` | Overview, generation flow, file index | First |
| `DESIGN.md` | Architecture, tech stack, file layout | Before implementation |
| `EVENTS.md` | `events.jsonl` kinds, fields, state-transition rules | Implementing producer or store |
| `TOPOLOGY.md` | Declarative topology data (phases / agents / edges) | Implementing graph nodes |
| `UI.md` | Layout, panel specs, animation specs | Implementing frontend |
| `INTEGRATION.md` | Auto-spawn hook from Nexus apex, emit protocol | Wiring up skill integration |
| `GENERATION.md` | Per-repo generation prompt and file manifest | Materialising the dashboard |

## Generation Flow (overview)

```
/nexus apex starts
       │
       ▼
Pre-flight: does <repo>/.agents/apex-dash/ exist?
       │
       ├── exists → spawn (bun run …) directly
       │
       └── missing
              │
              ▼
       Call forge/builder with the prompt in GENERATION.md
              │
              ▼
       Write the full file set to <repo>/.agents/apex-dash/
              │
              ▼
       Smoke test passes (port listening, SSE handshake)
              │
              ▼
       Continue apex normally + auto-open browser
```

See `INTEGRATION.md §3 Auto-spawn flow` and `GENERATION.md` for full detail.

## Runtime Behavior

A materialised dashboard behaves as follows.

| Action | Behavior |
|--------|----------|
| `/nexus apex` starts | Nexus background-spawns `bun run server/index.ts` and auto-opens the browser |
| Event occurs | Appended to `<repo>/.agents/apex/<run-id>/events.jsonl` → pushed to UI via SSE |
| Run ends | Server self-terminates after a grace window. Replay mode remains available |
| Concurrent runs | Each run-id has its own directory; multiple runs are visualised independently |

## Design Principles

1. **`events.jsonl` is the single source of truth** — the server only tails and broadcasts
2. **Receiver only** — coupling to apex is one emit helper; no new agent-to-agent traffic
3. **Fixed topology + animated state** — layout is static; state is conveyed through motion
4. **Event sourcing** — full state can be rebuilt from events on reload or reconnect
5. **Side-effect free** — observation must not perturb apex behavior

## Non-Goals

- Production SLO / long-term trend monitoring (owned by `beacon`)
- Skill ecosystem-wide overview (use `canvas` for diagrams; `realm` was sunset 2026-06-06)
- Test intelligence dashboards (use `pulse` for KPI/flake/regression timelines + `canvas` for coverage maps; `vista` was merged 2026-06-06)
- Becoming a registered skill under `~/.claude/skills/` (this stays as a Nexus apex companion tool)

## Related

- `nexus/SKILL.md` / `nexus/reference/apex-recipe.md` — apex itself
- `_common/SUBAGENT.md` — Codex CLI subagent contract
- `_common/HANDOFF.md` — agent handoff conventions

## Versioning

Specs are versioned. Every materialised dashboard records the source commit hash in `<repo>/.agents/apex-dash/.spec-version` (see `GENERATION.md`).
