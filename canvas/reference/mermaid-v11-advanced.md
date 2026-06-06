# Mermaid v11 Advanced Reference

Purpose: Read this when you need Mermaid v11-specific capabilities, advanced layout options, or renderer compatibility guidance.

## Contents

- Version-gated features
- Configuration rules
- ELK guidance
- Anti-patterns

## Version-Gated Features

| Feature | Minimum Version | Use When |
|---------|-----------------|----------|
| Architecture diagrams | `v11.1.0+` | You need service and infrastructure views |
| Kanban / Packet / Block / Radar | `v11+` | The user explicitly asks for newer Mermaid diagram families |
| Semantic shapes | `v11.3.0+` | You want richer shape vocabulary |
| Per-edge curves | `v11.10.0+` | One curve style per relationship matters |
| Radar diagrams | `v11+` | Multi-axis comparison (skills, coverage, scores) |
| Treemap diagrams | `v11+` | Hierarchical proportional area visualization |
| Hand-drawn look | `v11+` | Draft or whiteboard-style diagrams |
| Venn / Ishikawa beta | `v11.12.3+` (`venn-beta`, `ishikawa-beta`) | Set-overlap or fishbone cause-and-effect; syntax may evolve. [Source: Mermaid v11.13.0 blog](https://mermaid.ai/blog/posts/mermaid-v11-13-0-two-new-diagram-types-and-our-most-polished-release-yet) | [Venn syntax](https://mermaid.ai/open-source/syntax/venn.html) | [Ishikawa syntax](https://mermaid.ai/open-source/syntax/ishikawa.html) |
| TreeView beta | `v11.14.0+` (`treeview-beta`) | Indentation-driven hierarchical tree view |
| Wardley map | `v11.14.0+` (`wardley-beta`) | Value-chain / component-evolution strategy map. [Source: Wardley Maps docs](https://mermaid.js.org/syntax/wardley.html) |

## Configuration Rule

- Prefer frontmatter config.
- Treat old `%%{init:}%%` directives as legacy and avoid them in new output.

## Frontmatter Config Examples

Theme override:

```mermaid
---
config:
  theme: dark
---
flowchart LR
    A --> B
```

Flowchart layout tuning:

```mermaid
---
config:
  flowchart:
    nodeSpacing: 30
    rankSpacing: 50
    curve: basis
---
flowchart TD
    A --> B --> C
```

Combined settings:

```mermaid
---
config:
  theme: neutral
  look: handDrawn
  flowchart:
    curve: stepBefore
---
flowchart LR
    A --> B
```

## Hand-Drawn Look

Use `look: handDrawn` in frontmatter for draft, workshop, or whiteboard-style output.

```mermaid
---
config:
  look: handDrawn
  theme: neutral
---
flowchart TD
    A[Brainstorm] --> B[Prototype]
    B --> C[Validate]
```

Appropriate for: early design sessions, RFC drafts, ideation artifacts.
Not appropriate for: formal documentation, production runbooks, API specs.

## Per-Edge Curve Styles

Available since `v11.10.0+`. Override curve style per edge to distinguish flow types.

Supported values: `basis`, `bumpX`, `bumpY`, `cardinal`, `catmullRom`, `linear`, `monotoneX`, `monotoneY`, `natural`, `step`, `stepAfter`, `stepBefore`.

Use case: main flow with `basis` curves, exception/error paths with `step` curves for visual distinction.

```mermaid
---
config:
  flowchart:
    defaultRenderer: elk
---
flowchart TD
    A -->|normal| B
    A -.->|error| C
```

Guideline: limit to 2 curve styles per diagram for readability.

## ELK Guidance

Use ELK when:

- The graph approaches `100+` nodes
- Layout overlap is severe
- The renderer supports ELK

## Anti-Patterns

- Do not assume Mermaid is a pixel-perfect layout tool.
- Do not use v11-only syntax against unknown renderers.
- Do not keep old init directives in newly generated diagrams.
- Do not use `look: handDrawn` for formal documentation, production runbooks, or API specs.
- Do not mix more than 2 per-edge curve styles in one diagram — visual noise outweighs clarity.
