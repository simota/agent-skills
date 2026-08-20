# Agent Deployment Matrix

Purpose: Read this file when choosing which agents to deploy, skip, or justify for a Nexus[deliver] phase or scope.

## Contents

- Full matrix
- Coverage verification
- Common skip heuristics
- Deployment anti-patterns

Complete mapping of all 57 deployment roles across 9 product lifecycle phases.

### Legend
- **P** = Primary (core agent for this phase) · **S** = Supporting (used when needed) · **—** = Not deployed

---

## Full Matrix

| Agent | Category | DISCOVER | DEFINE | ARCHITECT | BUILD | HARDEN | VALIDATE | LAUNCH | GROW | EVOLVE |
|-------|----------|----------|--------|-----------|-------|--------|----------|--------|------|--------|
| Nexus | Orchestration | P | S | S | S | S | S | S | S | S |
| Sherpa | Orchestration | — | — | — | P | S | — | — | — | — |
| Architect | Meta | — | — | — | — | — | — | — | — | S |
| Rally | Orchestration | — | — | — | P | P | P | P | — | — |
| Scout | Investigation | P | — | — | — | — | — | — | — | — |
| Ripple | Analysis | — | P | — | — | — | — | — | — | P |
| Spark | Strategy | — | P | — | — | — | — | — | — | — |
| Compete | Strategy | P | — | — | — | — | — | — | — | — |
| Voice | Strategy | P | — | — | — | — | — | — | — | P |
| Field | Investigation | P | — | — | — | — | — | — | — | — |
| Trace | UX/Design | — | — | — | — | — | P | — | — | — |
| Canon | Analysis | — | P | — | — | P | — | — | — | — |
| Lens | Investigation | P | — | — | — | — | — | — | — | — |
| Magi | Decision | — | P | P | — | — | — | — | — | — |
| Scribe[unified] | Decision | P | — | — | — | — | — | — | — | — |
| Guardian | Git/PR | — | — | — | — | — | — | P | — | — |
| Launch | Git/PR | — | — | — | — | — | — | P | — | S |
| Trail | Investigation | — | — | — | — | — | — | — | — | P |
| Radar | Testing | — | — | — | S | S | P | — | — | — |
| Voyager | Testing | — | — | — | — | — | P | — | — | — |
| Sentinel | Security | — | — | — | — | P | — | — | — | — |
| Probe | Security | — | — | — | — | P | — | — | — | — |
| Judge | Review | — | — | — | — | P | — | — | — | — |
| Zen | Review | — | — | — | — | P | — | — | — | — |
| Sweep | Review | — | — | — | — | — | — | — | — | P |
| Builder | Implementation | — | — | — | P | — | — | S | — | — |
| Artisan | Implementation | — | — | — | P | — | — | — | — | — |
| Forge | Implementation | — | — | — | P | — | — | — | — | — |
| Schema | Data | — | — | P | — | — | — | — | — | — |
| Stream | Data | — | — | — | S | — | — | — | P | — |
| Bolt | Performance | — | — | — | — | P | — | — | — | — |
| Tuner | Performance | — | — | — | — | P | — | — | — | — |
| Quill | Documentation | — | — | — | — | — | — | P | — | — |
| Scribe | Documentation | — | P | — | — | — | — | — | — | — |
| Canvas | Visualization | — | — | P | — | — | — | P | — | — |
| Scribe | Documentation | — | — | — | — | — | — | P | — | — |
| Atlas | Architecture | — | — | P | — | — | — | — | — | — |
| Gateway | Architecture | — | — | P | — | — | — | — | — | — |
| Grove | Architecture | — | — | P | — | — | — | — | — | — |
| Scaffold | Architecture | — | — | P | — | — | — | — | — | — |
| Vision | UX/Design | — | — | — | S | — | — | — | — | — |
| Palette | UX/Design | — | — | — | S | — | — | — | — | — |
| Muse | UX/Design | — | — | — | S | — | — | — | — | — |
| Flow | UX/Design | — | — | — | S | — | — | — | — | — |
| Echo | UX/Design | — | — | — | — | — | P | — | — | — |
| Vitrine | UX/Design | — | — | — | — | — | — | P | — | — |
| Builder | DevOps | — | — | — | S | — | — | — | — | — |
| Gear | DevOps | — | — | — | — | — | — | P | — | P |
| Triage | Investigation | S | — | — | — | — | — | — | — | — |
| Polyglot | Internationalization | — | — | — | — | — | — | — | P | — |
| Growth | Growth | — | — | — | — | — | — | — | P | — |
| Growth | Growth | — | — | — | — | — | — | — | P | — |
| Pulse | Analytics | — | P | — | — | — | — | — | P | — |
| Experiment | Analytics | — | — | — | — | — | P | — | S | — |
| Vector | Browser | — | — | — | — | — | S | — | — | — |
| Cue | Browser | — | — | — | — | — | — | P | — | — |

---

## Coverage Verification

**Total unique deployment roles: 57** (including Nexus as universal execution engine)

All agents have at least one phase with Primary (P) or Supporting (S) deployment.

Per-phase process details → `reference/delivery-product-lifecycle.md`

## Common Skip Heuristics

| Agent | Usually Skip When | Use When |
|-------|-------------------|----------|
| `Scribe` | `S/M` scope | `L/XL` with formal spec needs |
| `Canvas` | `<= 10` files | Complex systems with `15+` modules |
| `Echo` | CLI, API, or simple UI | User-facing UI with multiple personas |
| `Sentinel` | Prototype or PoC | Pre-release or production code |
| `Vitrine` / `Cue` | No demo requirement | Reusable component library or launch needs |
| `Compete` / `Field` / `Voice` | Known domain, internal tool | New market, unknown users |
| `Spark` | Requirements already clear | Product direction still ambiguous |

## Deployment Anti-Patterns

- Do not deploy agents to fill a phase matrix
- Do not run `Scribe`, `Canvas`, or `Quill` for `S/M` scope
- Do not create `docs/` for a 3-file CLI tool
- Do not deploy full HARDEN stacks on a prototype without release risk
- Do not use Rally for work that is sequential rather than independent
- Do not issue `DISCOVER -> DEFINE -> ARCHITECT` chains for `S/M` scope
