# AI Reverse Engineering Reference

Purpose: Read this when static extraction is insufficient and you need LLM-assisted synthesis from code, specs, or mixed artifacts.

## Contents

- When to use AI assistance
- Extraction workflow
- Static analysis helpers
- Verification rules
- Limits and mitigations

## Use AI Assistance When

- The codebase is large and cross-cutting
- Symbol extraction alone misses intent or runtime relationships
- You need a best-effort candidate before manual verification
- The requested diagram spans multiple layers of abstraction

## Workflow

1. Inventory the source files, routes, models, and key symbols.
2. Extract concrete facts first with static tools or code search.
3. Ask the model to propose a diagram shape from verified facts.
4. Cross-check every node and edge against source files.
5. Mark uncertainty explicitly instead of inventing structure.

## Static Analysis Helpers

| Tool | Useful for |
|------|------------|
| `pyan` | Python call graphs |
| `PyCG` | Python call graph extraction |
| `code2flow` | Multi-language flow approximation |
| `callGraph` | Dependency and call structure |
| `PhpDependencyAnalysis` | PHP dependency extraction |

## Guardrails

- Treat the model as a synthesis step, not a source of truth.
- Do not add nodes, relationships, or state transitions that cannot be traced back.
- Prefer a simpler diagram over a speculative one.
- If the model output and source disagree, the source wins.

## Mitigation Patterns

| Risk | Mitigation |
|------|------------|
| Hallucinated edge | Require source citation for each relationship |
| Wrong abstraction | Narrow the scope and redraw |
| Missing runtime nuance | Add a note: static approximation only |
| Too much density | Split into one clearer diagram per question |

## Common LLM Pitfalls

| Pitfall | Description | Prevention |
|---------|-------------|------------|
| Level confusion | Mixing abstraction levels (e.g., class-level and system-level in one diagram) | Pin one abstraction level per diagram before generation |
| Code-diagram bias | Mirroring source file structure instead of logical architecture | Ask "what does this system do?" not "what files exist?" |
| Runtime blindness | Showing only static structure, missing async flows, queues, events | Explicitly prompt for runtime interactions and data flow |
| Over-connection | Drawing every possible relationship, creating visual noise | Apply density threshold: max 3 edges per node on average |
| Phantom components | Inventing nodes that do not exist in the source | Require source citation for every node added |

## Staged Generation Protocol

Use this 4-stage process to produce accurate diagrams from code or specs:

### Stage 1 — Fact Extraction

- List concrete facts from source: files, classes, functions, routes, DB tables, API endpoints.
- Each fact must include a source reference (file:line or spec section).
- Do not interpret or infer at this stage.

### Stage 2 — Structure Proposal

- Propose diagram structure (nodes and edges) based on extracted facts.
- Mark uncertain elements with `[?]` suffix.
- Choose diagram type and abstraction level.

### Stage 3 — Cross-Check

- For each node: verify existence in source. Remove if no reference found, or mark as `<<inferred>>`.
- For each edge: verify the relationship in source. Remove speculative edges.
- Ensure no phantom components remain.

### Stage 4 — Uncertainty Marking

Apply confidence tags to all elements:

| Tag | Meaning | Visual treatment |
|-----|---------|------------------|
| `confirmed` | Directly traceable to source | Solid line, normal style |
| `inferred` | Logically derived but not explicit in source | Dashed line, italic label |
| `uncertain` | Best guess, needs human validation | Dotted line, `[?]` suffix |

## Validation Techniques

### Edge Source Citation

For every edge in the diagram, record the source reference:

```
A --> B  %% src/api/handler.ts:42 — handler calls service
```

If no source reference can be provided, the edge is suspect.

### Scope Check

Validate that the diagram stays within density thresholds:

- Flowchart: `<=20` nodes
- Sequence: `<=15` messages
- Class: `<=12` classes
- ER: `<=10` entities

If exceeding thresholds, split into focused sub-diagrams.

### Bidirectional Trace

Verify completeness in both directions:

1. **Diagram → Code**: Every node and edge traces back to a source location.
2. **Code → Diagram**: Every significant component in scope appears in the diagram (or is explicitly marked as out-of-scope).
