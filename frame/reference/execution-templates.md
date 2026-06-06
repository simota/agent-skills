# Frame Execution Templates

Purpose: load this when Frame needs exact phase templates, validation checkpoints, packaging structure, or delivery reporting.

## Contents

- [Phase 1: CONNECT](#phase-1-connect)
- [Phase 2: SURVEY](#phase-2-survey)
- [Phase 3: EXTRACT](#phase-3-extract)
- [Phase 3.5: VALIDATE (Pre-Handoff)](#phase-35-validate-pre-handoff)
- [Phase 4: PACKAGE](#phase-4-package)
- [Phase 5: DELIVER](#phase-5-deliver)
- [Cross-Reference Links](#cross-reference-links)

## Phase 1: CONNECT

### Connection Verification

```markdown
## CONNECT Report

**Timestamp**: [YYYY-MM-DD HH:MM:SS]

### MCP Server Status
- Server: [Connected / Disconnected / Error]
- Method: [Remote (API Key) / Desktop (Plugin)]

### Identity (whoami)
- User: [Figma username]
- Plan: [Starter / Professional / Organization / Enterprise]
- Rate Limit: [X requests/min remaining]

### Rate Budget
| Resource | Used | Remaining | Daily Total |
|----------|------|-----------|-------------|
| Requests | [N] | [N] | [N] |
| Screenshots | [N] | [N] | [N] |

### Connection Issues
- [ ] None detected
- [ ] Auth token expired → Re-authenticate
- [ ] Rate limit near threshold → Reduce scope
- [ ] MCP server unreachable → Check network/config
```

### Tool Invocation

```
# Verify connection and identity
whoami()

# Expected response includes:
# - User name and email
# - Team/organization info
# - Plan type (affects rate limits)
```

---

## Phase 2: SURVEY

### File Inventory

```markdown
## SURVEY Report

**Target File**: [Figma file URL]
**File Name**: [Name]
**Last Modified**: [Date]

### Page Structure
| Page | Components | Frames | Relevance |
|------|------------|--------|-----------|
| [Page name] | [N] | [N] | [H/M/L] |

### Extraction Scope
- Total components: [N]
- Target components: [N] (filtered by relevance)
- Estimated API calls: [N]
- Estimated rate budget: [N requests, ~X min]

### Extraction Strategy
| Priority | Target | Tool | Rationale |
|----------|--------|------|-----------|
| 1 | [Component/Frame] | get_design_context | Core layout structure |
| 2 | [Variables] | get_variable_defs | Token extraction |
| 3 | [Screenshot] | get_screenshot | Visual reference |
| 4 | [Metadata] | get_metadata | Version tracking |

### Extraction Order
1. `get_design_context` — Structure first (highest info density per call)
2. `get_variable_defs` — Variables/tokens if design system extraction
3. `get_screenshot` — Visual reference for handoff
4. `get_metadata` — File/component metadata last
```

### Tool Invocation

```
# Get file overview via metadata
get_metadata(file_url="https://figma.com/file/XXX")

# Survey specific page/frame
get_design_context(
  file_url="https://figma.com/file/XXX",
  node_id="PAGE_ID",
  depth=1  # shallow scan for structure overview
)
```

---

## Phase 3: EXTRACT

### Design Context Extraction

```
# Full component extraction
get_design_context(
  file_url="https://figma.com/file/XXX",
  node_id="COMPONENT_NODE_ID"
)

# Response includes:
# - Component name, type, dimensions
# - Auto Layout properties (direction, spacing, padding)
# - Fill/stroke styles
# - Text styles (font, size, weight, line-height)
# - Constraints and responsive behavior
# - Child hierarchy
```

### Variable Extraction

```
# Extract all variables from file
get_variable_defs(
  file_url="https://figma.com/file/XXX"
)

# Response includes:
# - Color variables (with mode values: light/dark)
# - Spacing variables
# - Typography variables
# - Number variables
# - Boolean variables
# - Variable collections and groups
```

### Screenshot Capture

```
# Capture component screenshot
get_screenshot(
  file_url="https://figma.com/file/XXX",
  node_id="NODE_ID",
  scale=2  # 2x for retina quality
)

# Returns: Base64 encoded image or URL
```

### Extraction Log Template

```markdown
## EXTRACT Log

**Started**: [YYYY-MM-DD HH:MM:SS]

### API Calls
| # | Tool | Target | Status | Rate Used |
|---|------|--------|--------|-----------|
| 1 | get_design_context | [Node] | ✅/❌ | [N] |
| 2 | get_variable_defs | [File] | ✅/❌ | [N] |
| 3 | get_screenshot | [Node] | ✅/❌ | [N] |
| 4 | get_metadata | [File] | ✅/❌ | [N] |

### Rate Budget Status
- Used this session: [N] requests
- Remaining: [N] requests
- Estimated completion: [within budget / need throttling]

### Data Completeness
- [ ] Layout structure extracted
- [ ] Styles captured (fill, stroke, text)
- [ ] Auto Layout properties included
- [ ] Variables retrieved
- [ ] Screenshots captured
- [ ] Metadata recorded

**Completed**: [YYYY-MM-DD HH:MM:SS]
```

---

## Phase 3.5: VALIDATE (Pre-Handoff)

### Validation Checkpoint

Run between EXTRACT and PACKAGE to ensure extraction quality.

```markdown
## Pre-Handoff Validation

### Naming Consistency
- [ ] Figma component names match Code Connect mapping names
- [ ] Variable names follow consistent convention (camelCase, kebab-case, etc.)

### Token Coverage
- [ ] Raw color values mapped to Figma Variables where available
- [ ] Spacing values referenced by variable names, not pixel literals
- [ ] Typography values linked to variable definitions

### Completeness
- [ ] All target components from SURVEY plan successfully extracted
- [ ] No critical components missing (check against SURVEY inventory)
- [ ] Auto Layout properties captured for layout containers

### Code Connect
- [ ] Existing Code Connect mappings retrieved and included
- [ ] Unmapped components flagged for downstream awareness

### Rate Budget
- [ ] Current usage tracked (calls made / daily limit)
- [ ] Sufficient budget remaining for any follow-up extractions

### Gap Documentation
- [ ] Missing data explicitly noted with reason (rate limit, access, complexity)
- [ ] Figma URLs provided for any content not extracted
```

### Validation Failures

| Failure | Action |
|---------|--------|
| Missing critical component | Re-extract if budget allows; otherwise note gap |
| Raw values without token mapping | Re-run `get_variable_defs` to build mapping |
| No Code Connect data | Run `get_code_connect_map`; include coverage gap in handoff |
| Budget exhausted | Deliver partial results with clear scope documentation |

---

## Phase 4: PACKAGE

### Packaging Decision

| Downstream Agent | Format | Key Content |
|-----------------|--------|-------------|
| Muse | Token-focused | Variables, color modes, spacing scales |
| Forge | Quick overview | Layout + screenshot + key styles |
| Artisan | Full detail | Complete structure, styles, constraints, tokens |
| Builder | Data-focused | Form fields, table structures, API patterns |
| Schema | Schema-focused | Data entities, relationships, field types |
| Vision | Visual overview | Screenshots + structural summary |
| Showcase | Code Connect | Component ↔ code mappings |
| Canvas | Diagram-ready | FigJam content, flow structure |

Detailed handoff templates → `handoff-formats.md`

### Package Template

```markdown
## Frame Handoff Package

**Source**: [Figma file URL]
**Extracted**: [YYYY-MM-DD HH:MM:SS]
**Target Agent**: [Agent name]
**File Version**: [Version/Last modified]

### Context Summary
[2-3 sentence overview of what was extracted and why]

### Design Data
[Agent-specific structured data — see handoff-formats.md]

### Visual Reference
[Screenshots with annotations]

### Assumptions
- [Any assumptions made during extraction]

### Gaps
- [Any data that couldn't be extracted or was incomplete]
```

---

## Phase 5: DELIVER

### Delivery Report Template

```markdown
## Frame Delivery Report

### Task Summary
| Field | Value |
|-------|-------|
| Source | [Figma file URL] |
| Status | ✅ Complete / ⚠️ Partial / ❌ Failed |
| Components Extracted | [N] |
| Screenshots Captured | [N] |

### Rate Usage
| Metric | Value |
|--------|-------|
| API calls made | [N] |
| Rate budget used | [N%] |
| Remaining today | [N] |

### Handoff Packages
| Target Agent | Package | Key Content |
|-------------|---------|-------------|
| [Agent] | ✅ Ready | [Brief description] |

### Suggested Next Steps
| Priority | Agent | Action |
|----------|-------|--------|
| 1 | [Agent] | [What they should do with the handoff] |
| 2 | [Agent] | [Secondary action] |

### Issues & Gaps
| Issue | Impact | Recommendation |
|-------|--------|----------------|
| [Issue] | [Impact] | [How to resolve] |
```

---

## Cross-Reference Links

| Reference | Content |
|-----------|---------|
| `infrastructure-constraints.md` | MCP connection, rate limits, troubleshooting |
| `handoff-formats.md` | Agent-specific handoff templates |
| `code-connect-guide.md` | Code Connect workflow and mapping |
| `prompt-strategy.md` | Effective prompts per MCP tool |
| `figma-mcp-server-ga.md` | MCP Server GA tools, features, known issues |
| `design-to-code-anti-patterns.md` | Quality guardrails and failure modes |
