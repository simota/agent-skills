# Frame Prompt Strategy

Purpose: load this when Frame needs tool-specific prompt wording, chaining order, or scope-control patterns for Figma MCP calls.

## Contents

- [General Principles](#general-principles)
- [get_design_context](#get_design_context)
- [get_variable_defs](#get_variable_defs)
- [get_screenshot](#get_screenshot)
- [get_metadata](#get_metadata)
- [whoami](#whoami)
- [get_code_connect_map](#get_code_connect_map)
- [get_code_connect_suggestions](#get_code_connect_suggestions)
- [add_code_connect_map / send_code_connect_mappings](#add_code_connect_map--send_code_connect_mappings)
- [create_design_system_rules](#create_design_system_rules)
- [get_figjam](#get_figjam)
- [generate_diagram](#generate_diagram)
- [Tool Chaining Patterns](#tool-chaining-patterns)

## General Principles

1. **Be specific about what you need** — Vague prompts return verbose, unfocused data
2. **Specify depth when possible** — Avoid deep recursive extraction when shallow data suffices
3. **Name the output format** — Tell the tool how you want data structured
4. **One concern per call** — Don't ask for everything in one request; layer calls by priority

---

## get_design_context

### Purpose
Extract component structure, styles, Auto Layout properties, and hierarchy.

### Effective Patterns

**Component Analysis (Focused)**
```
Get the design context for this component.
Focus on: Auto Layout properties, spacing, padding, colors, typography.
Include child hierarchy up to 3 levels deep.
File: [URL]
Node: [NODE_ID]
```

**Page Layout Overview (Broad)**
```
Get the design context for this page.
I need: top-level frame layout, navigation structure, content areas.
Depth: 2 levels (frames and their direct children only).
File: [URL]
Node: [PAGE_NODE_ID]
```

**Responsive Analysis**
```
Get the design context for this frame.
Focus on: constraints, min/max dimensions, Auto Layout wrap behavior,
and any responsive variants.
File: [URL]
Node: [NODE_ID]
```

### Anti-Patterns

| Avoid | Why | Better |
|-------|-----|--------|
| "Get everything about this file" | Too broad, wastes rate budget | Target specific pages/components |
| No node_id specified | May return file-level overview only | Always specify target node |
| Deep nesting without limit | Exponential data for complex trees | Specify depth limit |

---

## get_variable_defs

### Purpose
Retrieve Figma Variables (design tokens) with all modes and values.

### Effective Patterns

**Full Token Extraction**
```
Get all variable definitions from this file.
Include: all collections, all modes (light/dark), all variable types.
File: [URL]
```

**Color Token Focus**
```
Get variable definitions from this file.
Focus on color variables only.
I need: variable name, value per mode (light/dark), collection grouping.
File: [URL]
```

**Spacing System**
```
Get variable definitions from this file.
Focus on spacing and dimension variables.
I need: variable name, pixel value, and any aliases/references.
File: [URL]
```

### Tips
- One call typically returns ALL variables in the file — no need to call multiple times
- Variables include mode values (light/dark), so no separate calls per mode needed
- Use the response to construct token mapping tables for Muse handoff

---

## get_screenshot

### Purpose
Capture visual representation of a design node.

### Effective Patterns

**Component Screenshot**
```
Take a screenshot of this component at 2x scale.
File: [URL]
Node: [NODE_ID]
Scale: 2
```

**Full Page Screenshot**
```
Take a screenshot of this page.
File: [URL]
Node: [PAGE_NODE_ID]
Scale: 1
```

### Optimization
- Use 1x scale for overview shots (saves bandwidth, sufficient for layout understanding)
- Use 2x scale for component detail shots (needed for handoff to Artisan/Vision)
- Skip screenshots when `get_design_context` provides sufficient structural detail
- Batch screenshot requests for related components

---

## get_metadata

### Purpose
File and component metadata (version, contributors, last modified).

### Effective Patterns

**File Overview**
```
Get metadata for this Figma file.
I need: file name, last modified date, version, page list.
File: [URL]
```

**Component Metadata**
```
Get metadata for this specific component.
I need: component name, description, documentation links, containing page.
File: [URL]
Node: [NODE_ID]
```

### Tips
- Call once per file at the start of SURVEY phase
- Use page list from metadata to plan extraction strategy
- Last modified date helps detect stale Code Connect mappings

---

## whoami

### Purpose
Verify authentication and check plan/rate information.

### Effective Pattern

```
Who am I? Show my user info, team, and current plan details.
```

### Tips
- Call once per session in CONNECT phase
- Response tells you plan type → determines rate limit strategy
- If auth fails, check connection setup before proceeding

---

## get_code_connect_map

### Purpose
Retrieve existing component-to-code mappings.

### Effective Patterns

**Full Audit**
```
Get all Code Connect mappings for this file.
I need: component names, code paths, prop mappings, last updated dates.
File: [URL]
```

**Specific Component**
```
Get the Code Connect mapping for this component.
File: [URL]
Node: [NODE_ID]
```

---

## get_code_connect_suggestions

### Purpose
AI-generated suggestions for unmapped components.

### Effective Pattern

```
Get Code Connect suggestions for unmapped components in this file.
File: [URL]
```

### Tips
- Run after `get_code_connect_map` to identify gaps
- Cross-reference suggestions with actual codebase before accepting
- Higher confidence suggestions can be mapped directly

---

## add_code_connect_map / send_code_connect_mappings

### Purpose
Create and sync component-to-code mappings.

### Tips
- Validate code paths exist before creating mappings
- Test prop value mappings against actual Figma variants
- Use `send_code_connect_mappings` for batch operations (one call vs. many)
- Always confirm with user before bulk mapping operations

---

## create_design_system_rules

### Purpose
Extract or create design system rules from Figma file structure.

### Effective Pattern

```
Create design system rules from this file.
Focus on: component naming conventions, variant structure,
spacing consistency, color usage patterns.
File: [URL]
```

### Tips
- High information density — one call can reveal design system structure
- Useful as input for Muse (token system) and Showcase (documentation)
- Results should be validated against actual file content

---

## get_figjam

### Purpose
Extract FigJam whiteboard content.

### Effective Pattern

```
Get the content of this FigJam board.
I need: sticky notes (text + color + position), connectors (from/to/label),
sections (name + contents), and any embedded content.
File: [URL]
```

### Tips
- FigJam content is often unstructured — focus on extracting relationships
- Section groupings provide organizational context
- Connector labels define relationships between concepts
- Useful for Canvas to create structured diagrams

---

## generate_diagram

### Purpose
Generate diagrams from design context.

### Effective Pattern

```
Generate a diagram showing the component hierarchy and relationships
in this file.
File: [URL]
```

---

## Tool Chaining Patterns

### Pattern: Full Component Analysis

```
1. get_metadata → File overview, page list
2. get_design_context → Component structure and styles
3. get_variable_defs → Token values used
4. get_screenshot → Visual reference
```

### Pattern: Design System Audit

```
1. get_variable_defs → All tokens
2. create_design_system_rules → System patterns
3. get_code_connect_map → Implementation coverage
```

### Pattern: Code Connect Update

```
1. get_code_connect_map → Current state
2. get_code_connect_suggestions → AI recommendations
3. add_code_connect_map → Create new mappings
4. send_code_connect_mappings → Sync to Figma
```
