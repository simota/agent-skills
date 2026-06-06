# Figma MCP Server — GA Reference

Purpose: load this when Frame needs the official GA tool inventory, Schema 2025 features, Code Connect API surface, or known client issues.

Source: https://developers.figma.com/docs/figma-mcp-server/

## Contents

- [Tool Inventory (GA)](#tool-inventory-ga)
- [Code Connect Integration](#code-connect-integration)
- [Schema 2025 New Features](#schema-2025-new-features)
- [Known Issues (MCP Clients)](#known-issues-mcp-clients)
- [Prop Mapping Types (Code Connect)](#prop-mapping-types-code-connect)
- [Supported Clients](#supported-clients)
- [Key URLs](#key-urls)

## Tool Inventory (GA)

### Design Context Tools

| Tool | Function | Output | Notes |
|------|----------|--------|-------|
| `get_design_context` | Structured representation (React+Tailwind by default) | Component tree, styles, Auto Layout | Framework customizable; max 25,000 tokens |
| `get_variable_defs` | Variables and styles (color, spacing, typography) | Token definitions with modes | Filterable by token type |
| `get_screenshot` | Visual capture of selection | Image data | Scale configurable (1x/2x) |
| `get_metadata` | Sparse XML (ID, name, type, position, size) | Lightweight structure | For large designs — lower cost than context |
| `generate_figma_design` | Generate design layers from text | Figma layers | **Remote only**; rate-exempt |
| `whoami` | Auth user info and plan | User/team/plan data | **Remote only**; rate-exempt |

### Code Connect Tools

| Tool | Function | Output | Notes |
|------|----------|--------|-------|
| `get_code_connect_map` | Existing component↔code mappings | Mapping list with props | Includes `codeConnectSrc`, `codeConnectName` |
| `add_code_connect_map` | Set component↔code mapping | Confirmation | **Rate-exempt** |
| `get_code_connect_suggestions` | AI-suggested mappings | Candidate list | Run after mapping for gap detection |
| `send_code_connect_mappings` | Confirm and apply mapping proposals | Sync result | Finalizes suggestions |

### Design System & Diagram Tools

| Tool | Function | Output | Notes |
|------|----------|--------|-------|
| `search_design_system` | Search design libraries for components, variables, styles | Search results | **Rate-exempt**; broad synonym search recommended |
| `create_design_system_rules` | Generate design system rules file | Rules document | For agent context; naming, variants, usage |
| `get_figjam` | FigJam content to XML + screenshot | Structured board data | Sticky notes, connectors, sections |
| `generate_diagram` | Mermaid syntax → FigJam diagram | Generated diagram | Flowchart, Gantt, state, sequence |

### Canvas Write Tools

| Tool | Function | Output | Notes |
|------|----------|--------|-------|
| `use_figma` | Execute Plugin API scripts to create/modify canvas elements | Created/mutated node IDs | **Rate-exempt**; atomic (failed scripts apply no changes); Full seat required for writes outside drafts; pass `skillNames: ["figma-use"]` |

### File Management Tools

| Tool | Function | Output | Notes |
|------|----------|--------|-------|
| `create_new_file` | Create new blank Figma Design or FigJam file | File URL and metadata | Rate-exempt |

---

## Code Connect Integration

When Code Connect is configured, `get_design_context` output includes `<CodeConnectSnippet>` wrappers with:
- Design property values from current selection
- Import statements from mapped code
- Component usage code
- Custom guidance (via "Add instructions for MCP" in Code Connect UI)

### Two Mapping Approaches

| Approach | Source | How It Works |
|----------|--------|--------------|
| **CLI** (`figma connect publish`) | Codebase `.figma.tsx` files | Real code examples from repo |
| **UI** (Code Connect panel in Figma) | GitHub repo connection | AI-generated snippets from component path + props |

---

## Schema 2025 New Features

| Feature | Status | Impact on Frame |
|---------|--------|-----------------|
| **Code Connect UI** | GA (Org/Enterprise) | AI-suggested mappings directly in Figma with GitHub integration (component mapping suggestions, AI-generated snippets); supplements CLI approach |
| **Slots** (Open Beta) | Beta | Placeholder containers in components; new prop type to map |
| **Extended Collections** | Enterprise | Multi-brand design systems with child collection inheritance |
| **Check Designs** | Early Access | Audit designs against design system; detects hardcoded values |
| **generate_figma_design** | GA (Remote) | Text-to-design generation; rate-exempt |
| **npm package integration** | GA | Figma Make imports production React design systems |
| **Variable mode limit increase** | GA | Professional: 10, Organization: 20 modes |

---

## Known Issues (MCP Clients)

| Client | Issue | Workaround |
|--------|-------|------------|
| Claude Code | Response >25,000 tokens causes error | Set `MAX_MCP_OUTPUT_TOKENS=50000` or higher |
| Cursor | "Failed to load" after token expiry | "Clear All MCP Tokens" → re-authenticate |
| General | `get_design_context` may timeout on large files | Use `get_metadata` first, then target specific nodes |
| Code Connect | "Failed to load Code Connect example" despite valid CLI parse | Check Figma component ID match; may be silent server-side issue |

---

## Prop Mapping Types (Code Connect)

| Type | API | Example |
|------|-----|---------|
| `figma.string()` | String prop | `label: figma.string("Label")` |
| `figma.enum()` | Variant mapping | `variant: figma.enum("Variant", { Primary: "primary" })` |
| `figma.boolean()` | Toggle with values | `icon: figma.boolean("Has Icon", { true: <Icon /> })` |
| `figma.instance()` | Nested component | `leadingIcon: figma.instance("Icon")` |
| `figma.slot()` | Placeholder container | `content: figma.slot("Content")` — **v1.4.0+, Beta** |
| `figma.children()` | Child elements | `items: figma.children("ListItem")` |

---

## Supported Clients

Claude Desktop · Claude Code · VS Code · Cursor · Windsurf · Codex (OpenAI)

---

## Key URLs

- MCP Server Docs: https://developers.figma.com/docs/figma-mcp-server/
- Code Connect Docs: https://developers.figma.com/docs/code-connect/
- Code Connect GitHub: https://github.com/figma/code-connect
- MCP Server Guide (GitHub): https://github.com/figma/mcp-server-guide
- Variables API: https://developers.figma.com/docs/rest-api/variables-endpoints/
- Schema 2025 Recap: https://www.figma.com/blog/schema-2025-design-systems-recap/
