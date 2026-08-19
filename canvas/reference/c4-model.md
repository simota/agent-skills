# C4 Model Delta

Purpose: Canvas-specific level and clarification contract. General C4 notation is model-known; source names and relationships must come from the repository or supplied architecture.

## Level Contract

| Level | Use | Default audience |
|---|---|---|
| Context | System boundary and external actors | Product / leadership |
| Container | Deployable or runtime units | Engineering / operations |
| Component | Internals of one container | Implementers / reviewers |

- Default to Context or Container and draw exactly one level per diagram.
- Limit Component scope to one container. Route code-level structure to Canvas `class` rather than inventing a C4 L4 view.
- If Structurizr DSL exists, derive names and relationships from it.

## Clarification Gates

- `ON_C4_LEVEL`: Context / Container / Component.
- `ON_C4_SCOPE`: whole system / one service / one container.
- `ON_C4_AUDIENCE`: product / engineering / operations / mixed.

Ask only when the unresolved choice would materially change the diagram; otherwise use the safest narrow default and state it.

## Verification

- One level and one system boundary per diagram.
- Real actors, containers, components, and relationships only.
- Scope and audience stated in the title or note.
- Syntax and accessibility follow `canvas/SKILL.md` REVIEW gates.
