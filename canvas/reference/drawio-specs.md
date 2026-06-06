# draw.io Specs Reference

Purpose: Read this when the output must be editable in draw.io or diagrams.net.

## Contents

- Minimal XML structure
- ID rules
- Shape and edge defaults
- Layout rules
- Quality checklist

## Minimal XML Skeleton

```xml
<mxfile host="app.diagrams.net">
  <diagram name="Page-1">
    <mxGraphModel>
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

## ID Rules

- Prefix nodes by type, for example: `proc-1`, `db-1`, `actor-1`.
- Keep IDs stable inside one file.
- Do not reuse IDs for different semantic entities.

## Shape Defaults

| Use | Shape |
|-----|-------|
| Process | Rounded rectangle |
| Decision | Diamond |
| Actor | Rectangle or icon-backed node |
| Database | Cylinder |
| Group | Container / swimlane |

## Edge Defaults

- Prefer orthogonal edges for business and architecture flow.
- Use solid edges for primary flow.
- Use dashed edges for optional, async, or inferred relationships.

## Layout Rules

- Keep the main reading direction consistent.
- Avoid crossing edges when the semantic model allows rearrangement.
- Journey cards commonly need around `180px` width to stay readable.

## Quality Checklist

- Node count stays `<=20`
- Labels are short
- Group boundaries are clear
- Edge direction is readable
- File opens cleanly in draw.io

## MCP Integration (draw.io MCP Server)

### Overview

The `@drawio/mcp` package provides an MCP server for programmatic draw.io diagram manipulation, eliminating the need for manual XML generation.

### Capabilities

| Capability | Description |
|------------|-------------|
| Page management | Create, list, rename, and delete diagram pages |
| Shape operations | Add, modify, and position shapes via API calls |
| Edge management | Create and style connections between shapes |
| Style control | Apply styles, themes, and formatting programmatically |
| Export | Render diagrams to SVG/PNG/PDF |

### Canvas usage pattern

```
IF environment has @drawio/mcp configured:
  → Use MCP tools for diagram creation and manipulation (preferred)
  → Benefits: no XML parsing errors, stable IDs, richer styling
ELSE:
  → Fall back to direct XML generation using drawio-specs.md templates
```

### Decision rule

1. Check if MCP tools for draw.io are available in the current environment.
2. If available: use MCP for all draw.io operations. Produces cleaner output with less error risk.
3. If unavailable: generate XML directly following the specs in this document.
4. Always validate output opens cleanly in draw.io regardless of generation method.
