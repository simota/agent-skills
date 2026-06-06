# Diagram Library Reference

Purpose: Read this when diagrams must be saved, listed, updated, regenerated, or reused across the project.

## Contents

- Library location
- Commands
- Saved file schema
- Update rules
- Clarification triggers

## Library Location

Store project diagrams in:

```text
.agents/diagrams/{project}/
```

## Commands

```text
/Canvas save diagram
/Canvas save diagram as [name]
/Canvas list diagrams
/Canvas show [diagram-name]
/Canvas update [diagram-name]
/Canvas regenerate [diagram-name]
```

## Saved File Schema

Use frontmatter for discoverability:

```yaml
---
name: auth-sequence
title: Authentication Sequence
format: mermaid
type: sequence
target:
  - src/app/api/auth/login/route.ts
sources:
  - src/app/api/auth/login/route.ts
updated_at: 2026-03-06
---
```

Then include:

1. Purpose
2. Diagram code
3. Legend
4. Explanation

## Update Rules

- Update an existing diagram when the same scope and same question already exist.
- Save under a new name when the abstraction or audience meaningfully changes.
- Regenerate from source when the diagram is stale enough that manual patching is riskier than redraw.

### ON_DIAGRAM_SAVE

- Save with generated default name
- Save with custom name
- Do not save

### ON_DIAGRAM_UPDATE

- Patch existing diagram
- Replace existing diagram
- Save as new variant

### ON_DIAGRAM_CONFLICT

- Prefer existing canonical diagram
- Create parallel variant
- Ask for naming decision
