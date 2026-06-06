# Diagram Tools Comparison

Purpose: Read this when Mermaid is not sufficient and you need to choose another diagram format or tool.

## Contents

- Tool comparison
- Selection rules

## Comparison

| Tool | Best For | Tradeoff |
|------|----------|----------|
| Mermaid | Default docs-native diagrams | Limited pixel-level control |
| draw.io | Editable diagrams, workshops, handoff artifacts | XML overhead; PlantUML import removed end-of-2025 ([migration guide](https://www.drawio.com/blog/plantuml-to-mermaid)) |
| D2 | Layout-heavy text diagrams; ASCII render output supported | Extra toolchain. [Docs](https://d2lang.com/) |
| PlantUML | UML-heavy diagrams | Less native in modern docs flows; draw.io support removed end-of-2025 |
| Structurizr | C4 at scale | Stronger setup dependency |
| Kroki | Unified rendering API for 25+ formats (Mermaid, D2, PlantUML, BPMN, etc.) | External service dependency |
| Excalidraw | Hand-drawn collaborative whiteboards; embeddable via `@excalidraw/excalidraw` (ESM, v0.18+) | Not suitable for formal docs [Source: excalidraw v0.18.0](https://github.com/excalidraw/excalidraw/releases/tag/v0.18.0) |
| tldraw | Infinite-canvas SDK; AI-powered canvas apps; v5.0 ships `@tldraw/mermaid` for Mermaid-to-native-shape conversion [Source: tldraw SDK 5.0](https://tldraw.dev/blog/tldraw-sdk-5-0) | React-only; not text-based DSL |
| ASCII | Terminal/comments/accessibility fallback | Low visual density |

## Selection Rules

- Use Mermaid by default.
- Use draw.io when the user needs editable output. Note: draw.io removed PlantUML import support at end of 2025; migrate PlantUML diagrams to Mermaid or draw.io XML instead.
- Use D2 or PlantUML only when the user explicitly requests them or their feature set solves a real limitation.
- Use Structurizr when the task is large-scale C4 architecture and the environment already supports it.
- Use Excalidraw (`@excalidraw/excalidraw` v0.18+, ESM) when hand-drawn collaborative whiteboard output is required and the target is a React/web app.
- Use tldraw SDK (v5.0+) when building an AI-powered or interactive infinite-canvas app; `@tldraw/mermaid` package converts Mermaid DSL to native tldraw shapes.
- Use ASCII for plain text, comments, or fallback.

## D2 Advanced Features

| Feature | Description | When useful |
|---------|-------------|-------------|
| Layout engines | dagre (default), ELK, TALA (commercial) | TALA for best auto-layout on complex graphs |
| Animations | Animated connections and transitions | Interactive presentations, live demos |
| Tooltips | Hover-triggered detail panels | Dense diagrams where detail-on-demand helps |
| Code snippets | Embedded syntax-highlighted code blocks | Architecture diagrams that reference implementation |
| LaTeX | Mathematical notation in labels | Algorithm or data-science diagrams |
| Layers | Abstraction-level separation within a single file (e.g., Context → Container → Code) | Multi-perspective architecture views |
| Scenarios | Behavioral variants overlaid on the same base diagram (e.g., normal vs error) | System behavior under different conditions |
| Vars & imports | Variables, reusable components, multi-file composition | Large diagram sets with shared elements |

### When to consider D2 over Mermaid

- `100+` nodes where layout quality matters — D2 with ELK/TALA handles dense graphs better. TALA is optimized for architecture diagrams; ELK for port-heavy node-link diagrams.
- Layout control is the primary concern (precise positioning, edge routing).
- Multi-file composition is needed (imports, variables, reusable components).
- Multi-perspective views are needed — D2 layers separate abstraction levels in one file; scenarios overlay behavioral variants.
- **Stay with Mermaid** when: GitHub/GitLab native rendering matters, team familiarity is higher, or the diagram is `<50` nodes.

## Architecture-as-Code Pattern

### Definition

Store diagram source (DSL) in Git alongside code. CI/CD renders diagrams automatically on change.

### Workflow

```
Code change → Update diagram DSL → PR review (diff-friendly) → CI renders → Docs updated
```

### Canvas role

Canvas generates and updates the DSL files. CI/CD rendering and deployment are project-side concerns.

### Recommended structure

```
docs/diagrams/
├── system-context.mmd      # Mermaid source
├── data-flow.mmd
├── deployment.d2           # D2 source (when needed)
└── README.md               # Index and rendering instructions
```

### Tool references

| Tool | Purpose |
|------|---------|
| Swark | Automated code-to-Mermaid generation |
| D2 CLI | `d2 input.d2 output.svg` rendering |
| Mermaid CLI | `mmdc -i input.mmd -o output.svg` rendering |
| GitHub Actions | `mermaid-js/mermaid-cli` action for CI rendering |
| Kroki | Unified rendering API — single endpoint for Mermaid, D2, PlantUML, BPMN, and 20+ formats |
