# Frame Handoff Formats

Purpose: load this when Frame must package extracted design context for a specific downstream agent. These templates define the required handoff shapes.

## Contents

- [Common Header (All Handoffs)](#common-header-all-handoffs)
- [Frame -> Muse (Design-to-Token)](#frame---muse-design-to-token)
- [Frame -> Forge (Design-to-Prototype)](#frame---forge-design-to-prototype)
- [Frame -> Artisan (Design-to-Production)](#frame---artisan-design-to-production)
- [Frame -> Builder (API/Data Context)](#frame---builder-apidata-context)
- [Frame -> Schema (Data Model)](#frame---schema-data-model)
- [Frame -> Vision (Visual Context)](#frame---vision-visual-context)
- [Frame -> Showcase (Code Connect)](#frame---showcase-code-connect)
- [Frame -> Canvas (Diagram)](#frame---canvas-diagram)

## Common Header (All Handoffs)

```markdown
## Frame Handoff → [Target Agent]

**Source**: [Figma file URL]
**File Version**: [Version / Last modified date]
**Extracted**: [YYYY-MM-DD HH:MM:SS]
**Scope**: [What was extracted — page, component set, selection]
```

---

## Frame → Muse (Design-to-Token)

Focus: Figma Variables → CSS token definitions

```markdown
### Variables Extracted

#### Color Variables
| Collection | Variable | Light Value | Dark Value | Type |
|------------|----------|-------------|------------|------|
| [Collection] | [name] | [#hex/rgba] | [#hex/rgba] | color |

#### Spacing Variables
| Variable | Value | Mapped To |
|----------|-------|-----------|
| [name] | [px/rem] | [semantic name suggestion] |

#### Typography Variables
| Variable | Font | Size | Weight | Line Height |
|----------|------|------|--------|-------------|
| [name] | [family] | [px] | [weight] | [value] |

### Token Mapping Suggestions
| Figma Variable | Suggested CSS Token | Layer |
|---------------|-------------------|-------|
| [variable] | --[token-name] | [primitive/semantic/component] |

### Modes Detected
- [ ] Light mode
- [ ] Dark mode
- [ ] Other: [mode names]

### Token Standard Note
- Figma Variables support W3C DTCG format (`.tokens.json`) for export
- If Muse needs standards-compliant tokens, note DTCG compatibility

### Notes for Muse
- [Any observations about variable organization]
- [Inconsistencies or gaps in variable definitions]
```

---

## Frame → Forge (Design-to-Prototype)

Focus: Quick overview for rapid prototyping

```markdown
### Design Overview
[2-3 sentence description of the design]

### Screenshot
[Embedded screenshot or path]

### Layout Structure
```
[ASCII representation of layout]
e.g.
┌─────────────────────────┐
│ Header (64px, flex-row)  │
├────────┬────────────────┤
│ Sidebar│ Main Content   │
│ 240px  │ flex-grow      │
│        │                │
├────────┴────────────────┤
│ Footer (48px)           │
└─────────────────────────┘
```

### Key Components
| Component | Type | Key Props |
|-----------|------|-----------|
| [Name] | [Button/Card/Form/...] | [size, variant, state] |

### Styles Quick Reference
| Property | Value |
|----------|-------|
| Primary color | [value] |
| Font family | [value] |
| Border radius | [value] |
| Base spacing | [value] |

### Interaction Notes
- [Hover states, transitions, responsive behavior]

### Forge Guidance
- Priority: [What to build first]
- Mock data: [Suggested mock data structure]
- Skip: [What can be simplified for prototype]
```

---

## Frame → Artisan (Design-to-Production)

Focus: Complete structural detail for production implementation

```markdown
### Component Hierarchy
```
ComponentName
├── Header
│   ├── Logo (Image, 32x32)
│   ├── Navigation (flex-row, gap: 24px)
│   │   └── NavItem × N (text, 14px/500)
│   └── Actions (flex-row, gap: 8px)
│       ├── SearchButton (icon-button, 40x40)
│       └── ProfileMenu (avatar + dropdown)
├── Main (flex-col, padding: 24px)
│   └── ...
└── Footer
```

### Auto Layout Details
| Container | Direction | Gap | Padding | Alignment |
|-----------|-----------|-----|---------|-----------|
| [Name] | [row/col] | [px] | [T R B L] | [start/center/end/space-between] |

### Style Specifications
| Element | Property | Value | Token Suggestion |
|---------|----------|-------|-----------------|
| [element] | background | [value] | --bg-[semantic] |
| [element] | color | [value] | --text-[semantic] |
| [element] | font-size | [value] | --text-[scale] |
| [element] | border-radius | [value] | --radius-[size] |
| [element] | shadow | [value] | --shadow-[level] |

### Responsive Behavior
| Breakpoint | Layout Change |
|------------|---------------|
| < 768px | [What changes] |
| < 1024px | [What changes] |
| ≥ 1280px | [What changes] |

### Component States
| Component | Default | Hover | Active | Disabled | Focus |
|-----------|---------|-------|--------|----------|-------|
| [Name] | [styles] | [changes] | [changes] | [changes] | [changes] |

### Constraints
| Element | Horizontal | Vertical |
|---------|------------|----------|
| [Name] | [Left/Right/Center/Scale] | [Top/Bottom/Center/Scale] |

### Screenshots
| View | Path | Description |
|------|------|-------------|
| Full | [path] | Complete component |
| Mobile | [path] | Responsive variant (if available) |

### Artisan Guidance
- Token system: [existing tokens to use, or suggest Muse first]
- Accessibility: [ARIA roles, focus management, color contrast notes]
- Framework hint: [React/Vue/Svelte patterns matching the design]
```

---

## Frame → Builder (API/Data Context)

Focus: Data model inference from form/table designs

```markdown
### Data Entities Detected
| Entity | Source | Fields |
|--------|--------|--------|
| [Name] | [Form/Table/Card] | [field1, field2, ...] |

### Form Analysis
| Field | Type | Required | Validation | Notes |
|-------|------|----------|------------|-------|
| [label] | [text/email/select/...] | [Y/N] | [rules] | [placeholder, options] |

### Table Structure
| Column | Data Type | Sortable | Filterable |
|--------|-----------|----------|-----------|
| [name] | [string/number/date/...] | [Y/N] | [Y/N] |

### API Pattern Inference
| Endpoint | Method | Purpose | Based On |
|----------|--------|---------|----------|
| /api/[entity] | GET | List view | Table component |
| /api/[entity] | POST | Create | Form component |
| /api/[entity]/:id | PUT | Update | Edit form |
| /api/[entity]/:id | DELETE | Delete | Delete button |

### Builder Guidance
- Data relationships: [Inferred relationships between entities]
- Pagination: [If table shows pagination patterns]
- Search/filter: [If search/filter UI is present]
```

---

## Frame → Schema (Data Model)

Focus: Database schema inference from design patterns

```markdown
### Inferred Tables
| Table | Primary Key | Source Design |
|-------|-------------|---------------|
| [name] | [field] | [Figma component] |

### Fields
| Table | Field | Type | Nullable | Unique | Notes |
|-------|-------|------|----------|--------|-------|
| [table] | [field] | [varchar/int/...] | [Y/N] | [Y/N] | [from design label/type] |

### Relationships
| From | To | Type | Based On |
|------|-----|------|----------|
| [table.field] | [table.field] | [1:N/N:M/1:1] | [design evidence] |

### Schema Guidance
- Confidence level: [High/Medium/Low — based on design clarity]
- Ambiguities: [Fields where type inference is uncertain]
```

---

## Frame → Vision (Visual Context)

Focus: Screenshots + structural summary for creative direction

```markdown
### Visual Overview
[Primary screenshot]

### Design Language
| Aspect | Current State |
|--------|---------------|
| Color palette | [dominant colors] |
| Typography | [primary font, scale] |
| Spacing system | [grid/unit] |
| Visual density | [compact/comfortable/spacious] |
| Style direction | [flat/material/glass/neumorphic/...] |

### Component Inventory
| Category | Count | Examples |
|----------|-------|---------|
| Navigation | [N] | [names] |
| Forms | [N] | [names] |
| Cards | [N] | [names] |
| Tables | [N] | [names] |
| Modals | [N] | [names] |

### Screenshots
| View | Path | Notes |
|------|------|-------|
| [name] | [path] | [what it shows] |

### Vision Guidance
- Design system maturity: [none/early/established]
- Consistency issues: [any observed inconsistencies]
- Suggested focus areas: [where Vision should direct attention]
```

---

## Frame → Showcase (Code Connect)

Focus: Component ↔ code mapping data

```markdown
### Current Code Connect Status
| Figma Component | Code Path | Status |
|----------------|-----------|--------|
| [component] | [file:export] | [Mapped/Unmapped/Stale] |

### New Mappings (Suggested)
| Figma Component | Suggested Code Path | Confidence |
|----------------|-------------------|-----------|
| [component] | [file:export] | [High/Medium/Low] |

### Mapping Details
| Figma Component | Props | Code Props | Mapping |
|----------------|-------|------------|---------|
| [component] | [figma prop] | [code prop] | [direct/transform/default] |

### Showcase Guidance
- Storybook stories needed: [components without stories]
- Visual regression: [components with design changes]
- Code Connect sync: [mappings to update]
```

---

## Frame → Canvas (Diagram)

Focus: FigJam content → structured diagram data

```markdown
### FigJam Board Content

#### Sticky Notes
| Section | Content | Color | Author |
|---------|---------|-------|--------|
| [section] | [text] | [color] | [name] |

#### Connectors
| From | To | Label | Type |
|------|-----|-------|------|
| [node] | [node] | [text] | [arrow/line/dashed] |

#### Sections
| Name | Items | Purpose |
|------|-------|---------|
| [name] | [N items] | [inferred purpose] |

### Canvas Guidance
- Suggested diagram type: [flowchart/sequence/mindmap/...]
- Key relationships: [primary connections to emphasize]
- Structure: [hierarchical/sequential/networked]
```
