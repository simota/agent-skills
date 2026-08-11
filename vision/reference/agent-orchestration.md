# Agent Orchestration

Purpose: Use this file when Vision must route work across design agents, business validation, or quality pre-validation.

Contents:
- Design-agent boundaries
- Delegation patterns
- Accord validation flow

## Design-Agent Boundaries

| Aspect | Vision | Muse | Palette | Flow | Forge | Echo |
|--------|--------|------|---------|------|-------|------|
| Primary focus | direction | tokens and visual system | UX and usability | motion | prototype | persona validation |
| Writes code | never | yes | yes | yes | yes | never |
| Token decisions | define | implement | consume | consume | consume | review impact |
| Accessibility | require baseline | implement tokens | verify UX | respect motion rules | implement states | validate from user view |

## Core Delegation Patterns

| Pattern | Flow |
|---------|------|
| Full redesign | `Vision -> Muse -> Palette -> Flow -> Forge -> Echo` |
| UX issue resolution | `Vision -> Palette -> Flow` |
| Trend application | `Vision -> Muse -> Palette -> Flow` |
| New product design | `Field -> Vision -> Muse -> Forge -> Echo` |
| Design system construction | `Vision -> Muse -> Palette -> Forge` |
| Design review cycle | `Lens -> Vision -> [Muse/Palette/Flow] -> Lens -> Echo` |

## Delegation Packet

Every delegation should include:
- context and chosen direction
- constraints and non-goals
- scope and priority
- success criteria
- explicit handoff artifact expected

## Business-Validated Design (`Vision <-> Accord`)

Use this pattern when:
- redesign scope affects `3+ pages`
- budget or timeline meaningfully constrains the UI direction
- stakeholder expectations could conflict with design quality

Flow:
1. `Accord` provides business constraints.
2. `Vision` creates `3+` options that respect those constraints.
3. `Vision` requests impact validation from `Accord`.
4. `Vision` adjusts if business fit is weak.
5. `Vision` delegates only after the direction is business-valid.


---

# Collaboration Handoffs and Overlap Boundaries

Referenced from `SKILL.md` -> Collaboration.

Vision receives research and analysis from upstream agents. Vision sends design direction to downstream implementation agents.

| Direction | Handoff | Purpose |
|-----------|---------|---------|
| Field → Vision | `RESEARCHER_TO_VISION` | User research insights and usability findings |
| Compete → Vision | `COMPETE_TO_VISION` | Competitive analysis and positioning data |
| Spark → Vision | `SPARK_TO_VISION` | Feature proposals requiring design direction |
| Vision → Muse | `VISION_TO_MUSE` | Token direction and design system strategy |
| Vision → Palette | `VISION_TO_PALETTE` | Usability direction and interaction guidelines |
| Vision → Flow | `VISION_TO_FLOW` | Animation direction and motion language |
| Vision → Forge | `VISION_TO_FORGE` | Prototype specifications and concept builds |
| Vision → Artisan | `VISION_TO_ARTISAN` | Implementation direction and component specs |
| Vision → Prose | `VISION_TO_PROSE` | Design direction for UX copy and microcopy |
| Echo → Vision | `ECHO_TO_VISION` | Persona-based UI flow validation findings |
| Vision → Frame | `VISION_TO_FRAME` | Figma MCP design context direction and token pipeline strategy |

### Overlap Boundaries

| Agent | Vision owns | They own |
|-------|-------------|----------|
| Muse | Design system strategy and token direction | Token definition, lifecycle, and code implementation |
| Palette | Macro UX direction and journey design | Micro/Meso usability implementation and interaction polish |
| Flow | Motion language and animation strategy | Animation implementation and choreography |
| Forge | Prototype specifications and concept direction | Prototype building and rapid implementation |
| Accord | Design direction alignment with business goals | Formal specification writing and cross-team alignment |
| Frame | Design system strategy and Figma MCP direction | Figma MCP extraction, Code Connect, and plugin execution |
| Echo | Interpreting persona validation results for direction | Persona simulation and UI flow walkthrough |

