# Agent Category Guide

**Purpose:** First-pass category selection guide and boundary map.
**Read when:** You need to choose a category before loading the full ecosystem roster.

## Contents
- Selection Rules
- Quick Category Map
- Escalation Rules

Use this file to choose the primary category for a new or improved agent.
Read `reference/agent-categories.md` only after the likely category is narrowed.

---

## Selection Rules

Use the agent's primary output and responsibility, not secondary capabilities.

| If the agent mainly... | Primary category |
|------------------------|------------------|
| Coordinates agents, chains, or lifecycle flow | Orchestration |
| Investigates, researches, diagnoses, or analyzes without implementing fixes | Investigation |
| Writes production code or business logic | Implementation |
| Writes or expands automated tests | Testing |
| Detects or remediates security issues | Security |
| Reviews quality, style, or change safety | Review |
| Optimizes runtime, query, or rendering speed | Performance |
| Produces docs, specs, prompts, or knowledge artifacts | Documentation |
| Designs system structure, boundaries, or schemas | Architecture |
| Designs UI, UX, motion, or visual direction | UX/Design |
| Manages infra, CI/CD, environments, or runtime operations | DevOps |
| Modernizes legacy stacks or replaces deprecated patterns | Modernization |
| Improves acquisition, SEO, CRO, retention, or growth loops | Growth |
| Defines metrics, experiments, analytics, or reporting | Analytics |
| Manages Git, PR hygiene, or release flow | Git/PR |
| Operates browsers, screenshots, or task automation in UI surfaces | Browser |
| Designs data pipelines, warehouses, or database structures | Data |
| Produces market, business, or strategic analysis | Strategy |
| Handles incidents, outages, response, or repair coordination | Incident |
| Builds bots, messaging, or realtime communication surfaces | Communication |
| Generates skills, orchestrates ecosystem evolution, or visualizes the ecosystem itself | Meta / Tooling |

---

## Quick Category Map

| Category | Core question | Code generation | Typical neighbors |
|----------|---------------|-----------------|-------------------|
| Orchestration | "Who should do this next?" | No | Nexus, Sherpa, Titan |
| Investigation | "What is happening and why?" | No | Scout, Triage, Trail |
| Implementation | "How do we build it?" | Yes | Builder, Forge, Artisan |
| Testing | "How do we verify it?" | Yes | Radar, Voyager |
| Security | "How do we prevent or exploit risk safely?" | Mixed | Sentinel, Probe |
| Review | "Is this change safe, clear, and justified?" | Mixed | Judge, Zen, Ripple |
| Performance | "How do we make it faster or cheaper?" | Yes | Bolt, Tuner |
| Documentation | "How do we explain or codify it?" | Mostly text | Quill, Scribe, Lore |
| Architecture | "How should the system be shaped?" | Mixed | Atlas, Architect, Schema |
| UX/Design | "How should it look or feel?" | Mixed | Vision, Muse, Palette |
| DevOps | "How do we run and ship it reliably?" | Yes | Gear, Pipe, Scaffold |
| Modernization | "How do we upgrade or replace old patterns?" | Mixed | Shift (`detect`/`modernize`/`radar` — absorbed from horizon), Sweep |
| Growth | "How do we increase reach or conversion?" | Mixed | Growth, Bond |
| Analytics | "How do we measure or experiment?" | Mixed | Pulse, Experiment |
| Git/PR | "How do we shape the change and review flow?" | Mixed | Guardian, Harvest |
| Browser | "How do we act inside a browser?" | Mixed | Vector, Director |
| Data | "How do we model, move, or store data?" | Mixed | Schema, Stream |
| Strategy | "What should the business or product do next?" | No | Compete, Helm |
| Incident | "How do we stabilize, diagnose, or repair production?" | Mixed | Triage, Mend |
| Communication | "How do we send, route, or orchestrate messages?" | Yes | Relay |
| Meta / Tooling | "How do we improve the ecosystem itself?" | Mixed | Architect, Sigil, Darwin |

---

## Escalation Rules

- If two categories both look valid, choose the one that owns the final deliverable and note the secondary category in design notes.
- If overlap with an existing agent may exceed `30%`, stop category selection and read `reference/overlap-detection.md`.
- If the design introduces complex multi-agent routing, read `reference/multi-agent-system-anti-patterns.md`.
- If the design may fragment the ecosystem or create governance drift, read `reference/ecosystem-architecture-anti-patterns.md`.
- If you still cannot place the agent confidently, ask first instead of forcing a category.
- Once the category is narrowed, read `reference/agent-categories.md` for the full roster and neighboring-agent detail.
