# Frame Code Connect Guide

Purpose: load this when Frame must audit, suggest, map, sync, or maintain Code Connect relationships between Figma components and code.

## Contents

- [What is Code Connect?](#what-is-code-connect)
- [Workflow](#workflow)
- [Phase 1: AUDIT](#phase-1-audit)
- [Phase 2: SUGGEST](#phase-2-suggest)
- [Phase 3: MAP](#phase-3-map)
- [Phase 4: SYNC](#phase-4-sync)
- [Phase 5: MAINTAIN](#phase-5-maintain)
- [Collaboration with Showcase](#collaboration-with-showcase)
- [Best Practices](#best-practices)

## What is Code Connect?

Code Connect links Figma components to their code implementations, enabling:
- Developers see relevant code snippets when inspecting Figma components
- Designers see which components have been implemented
- Teams track design-to-code coverage

---

## Workflow

```
AUDIT → SUGGEST → MAP → SYNC → MAINTAIN
```

| Phase | Action | Tool |
|-------|--------|------|
| **AUDIT** | Review existing mappings | `get_code_connect_map` |
| **SUGGEST** | Get AI-recommended mappings | `get_code_connect_suggestions` |
| **MAP** | Create new mappings | `add_code_connect_map` |
| **SYNC** | Push mappings to Figma | `send_code_connect_mappings` |
| **MAINTAIN** | Monitor for drift | Periodic audit |

---

## Phase 1: AUDIT

```
# Get all existing Code Connect mappings
get_code_connect_map(
  file_url="https://figma.com/file/XXX"
)

# Response includes:
# - Component name and node_id
# - Mapped code file path and export name
# - Prop mappings (Figma prop → code prop)
# - Last updated timestamp
```

### Audit Report Template

```markdown
## Code Connect Audit

**File**: [Figma file URL]
**Date**: [YYYY-MM-DD]

### Coverage Summary
| Metric | Value |
|--------|-------|
| Total components | [N] |
| Mapped | [N] (X%) |
| Unmapped | [N] (X%) |
| Stale (>30 days) | [N] |

### Mapped Components
| Component | Code Path | Props Mapped | Last Updated |
|-----------|-----------|-------------|-------------|
| [name] | [path:export] | [N/N] | [date] |

### Unmapped Components
| Component | Usage Count | Priority |
|-----------|-------------|----------|
| [name] | [N instances] | [H/M/L] |

### Stale Mappings
| Component | Code Path | Days Since Update | Issue |
|-----------|-----------|-------------------|-------|
| [name] | [path] | [N] | [code changed / component updated] |
```

---

## Phase 2: SUGGEST

```
# Get AI suggestions for unmapped components
get_code_connect_suggestions(
  file_url="https://figma.com/file/XXX"
)

# Response includes:
# - Suggested component-to-code matches
# - Confidence level
# - Prop mapping suggestions
```

### Evaluating Suggestions

| Confidence | Action |
|-----------|--------|
| **High** (>80%) | Accept directly, verify prop mappings |
| **Medium** (50-80%) | Review code file, confirm match |
| **Low** (<50%) | Manual investigation needed |

---

## Phase 3: MAP

### Creating a Mapping

```
# Add a single component mapping
add_code_connect_map(
  file_url="https://figma.com/file/XXX",
  component_node_id="COMPONENT_NODE_ID",
  code_path="src/components/Button.tsx",
  export_name="Button",
  props={
    "variant": {
      "figma_prop": "Variant",
      "code_prop": "variant",
      "mapping": {
        "Primary": "primary",
        "Secondary": "secondary",
        "Outline": "outline"
      }
    },
    "size": {
      "figma_prop": "Size",
      "code_prop": "size",
      "mapping": {
        "Small": "sm",
        "Medium": "md",
        "Large": "lg"
      }
    },
    "disabled": {
      "figma_prop": "Disabled",
      "code_prop": "disabled",
      "type": "boolean"
    }
  }
)
```

### Prop Mapping Types

| Type | Description | Example |
|------|-------------|---------|
| **Direct** | Same name, same value | `label` → `label` |
| **Rename** | Different name, same value | `Variant` → `variant` |
| **Value map** | Name + value transformation | `"Primary"` → `"primary"` |
| **Boolean** | Figma toggle → boolean prop | `Disabled` → `disabled: true` |
| **Default** | Not in Figma, fixed in code | — → `className="btn"` |
| **Computed** | Derived from multiple Figma props | `Size` + `Variant` → `className` |

---

## Phase 4: SYNC

```
# Push all mappings to Figma
send_code_connect_mappings(
  file_url="https://figma.com/file/XXX"
)

# This updates the Code Connect panel in Figma Dev Mode
# Developers will see code snippets when inspecting components
```

### Pre-Sync Checklist

- [ ] All new mappings tested against actual code
- [ ] Prop mappings cover all Figma variants
- [ ] Code paths are valid and accessible
- [ ] No conflicting mappings for same component
- [ ] Stale mappings updated or removed

---

## Phase 5: MAINTAIN

### Drift Detection

Code Connect mappings can become stale when:
- Code files are renamed or moved
- Component props change in Figma
- New variants are added
- Code refactoring changes export names

### Drift Detection Procedure

```
1. Run get_code_connect_map → get current mappings
2. For each mapping:
   a. Check "Last Updated" age (flag if >30 days)
   b. Verify code_path still exists in codebase
   c. Compare Figma component props against mapped props
   d. Check for new Figma variants not yet mapped
3. Classify drift:
   - STALE: >30 days since update, props unchanged → low risk
   - BROKEN: code_path no longer exists → critical, needs fix
   - INCOMPLETE: new Figma props/variants not mapped → medium risk
   - ORPHANED: code component deleted → remove mapping
4. Report drift findings in DELIVER phase
```

### Maintenance Schedule

| Frequency | Action |
|-----------|--------|
| Per sprint | Quick audit — check for stale mappings (>30 days) |
| Monthly | Full audit — coverage report, drift detection procedure |
| After design changes | Targeted update — affected components only |
| After code refactoring | Path update — fix moved/renamed files |

---

## Collaboration with Showcase

Frame manages the **Figma side** of Code Connect. Showcase manages the **code side** (Storybook stories, visual regression).

```
Frame ────── Code Connect ────── Showcase
(Figma)     (bidirectional)       (Code)

Frame: Component → code path mapping
Showcase: Code path → Storybook story
Together: Full traceability from design to documentation
```

### Handoff Protocol

**Frame → Showcase**: New mappings created, send component list with code paths for story creation.
**Showcase → Frame**: Code paths changed during refactoring, request mapping update.

---

## Best Practices

1. **Map high-usage components first** — Sort by instance count in Figma
2. **Keep prop mappings simple** — Direct mappings are easier to maintain
3. **Use consistent naming** — Align Figma prop names with code prop names where possible
4. **Document value transformations** — When `"Primary"` becomes `"primary"`, note it
5. **Track coverage metrics** — Aim for >80% coverage on core component library
6. **Sync after design system updates** — Don't let mappings drift
7. **Version awareness** — Note which code version the mapping targets
