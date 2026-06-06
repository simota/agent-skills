# Canvas Reverse Engineering Patterns

Purpose: Read this when the request starts from code, schema, routes, auth, tests, or dependencies rather than from a specification.

## Contents

- Pattern catalog
- Extraction rules
- Auto-detect command
- Verification rules

## Pattern Catalog

| # | Pattern | Target | Output | Trigger |
|---|---------|--------|--------|---------|
| 1 | Component Tree | React/Vue components | Mind Map / Flowchart | `/Canvas components` |
| 2 | API Route Map | Next.js/Express routes | Flowchart | `/Canvas api routes` |
| 3 | State Machine | Redux/Zustand/XState | State Diagram | `/Canvas state` |
| 4 | Database Schema | Prisma/TypeORM/SQL | ER Diagram | `/Canvas schema` |
| 5 | Test Structure | Jest/Vitest tests | Mind Map | `/Canvas tests` |
| 6 | Dependency Graph | Imports and package structure | Class Diagram / Flowchart | `/Canvas deps` |
| 7 | Auth Flow | Auth handlers and middleware | Sequence Diagram | `/Canvas auth flow` |
| 8 | Data Flow | API handlers or pipelines | Sequence Diagram | `/Canvas data flow [handler]` |

## Auto-Detect

```text
/Canvas analyze
```

Use this when the user knows the source area but not the best diagram family.

## Extraction Rules

- Build the diagram from files, symbols, routes, state names, schema relations, and explicit calls.
- Prefer verified imports, exports, route handlers, reducer actions, model relations, and middleware chains.
- If static extraction is incomplete, use `reference/ai-reverse-engineering.md` and mark uncertainty.

## Output Defaults

| Pattern | Best Default |
|---------|--------------|
| Component Tree | Mind map for hierarchy, flowchart for explicit nesting |
| API Route Map | Flowchart grouped by route family |
| State Machine | Mermaid state diagram |
| Database Schema | Mermaid ER diagram |
| Test Structure | Mind map |
| Dependency Graph | Flowchart or class-like relation graph |
| Auth Flow | Mermaid sequence diagram |
| Data Flow | Mermaid sequence diagram |

## Verification Rules

- Every node must map to a real file, symbol, route, table, or state.
- Every edge must map to a verified relationship or call.
- If runtime behavior is inferred rather than explicit, label it as inferred.
