# Evolution Patterns

Purpose: load this when installed skills drift from the repository and Sigil must decide whether to update, replace, split, merge, or archive them.

## Contents

1. Lifecycle states
2. Triggers
3. Update strategies
4. Migration workflows
5. Report template

## Skill Lifecycle States

```text
ACTIVE -> STALE -> DEPRECATED -> ARCHIVED
  ^         |          |
  |         +-> UPDATE |
  +-------------REPLACE+
```

| State | Detection | Action |
|-------|-----------|--------|
| `ACTIVE` | Re-evaluation `>= 9/12` | Keep as-is |
| `STALE` | Re-evaluation `6-8/12` | Trigger evolution workflow |
| `DEPRECATED` | Re-evaluation `< 6/12` or superseded by successor | Mark deprecated and create successor |
| `ARCHIVED` | Framework or library removed from the project | Remove from active directories after confirmation when removal is required |

## Evolution Triggers

### Automatic Detection During `SCAN`

| Trigger | Detection method | Example |
|---------|------------------|---------|
| Dependency version change | Manifest diff | React `18 -> 19` |
| Framework migration | Framework removed and another added | Pages Router -> App Router |
| Convention change | Rule/config diff | strict mode enabled |
| Directory restructure | Expected path no longer exists | `src/` -> `app/` |
| Testing framework change | Test dependencies changed | Jest -> Vitest |

### User-Initiated Signals

| Trigger | Signal |
|---------|--------|
| Explicit refresh request | User asks to update skills |
| Bug report | Generated skill is now incorrect |
| Feature request | Existing skill no longer covers needed patterns |

## Update Strategies

### Strategy 1: In-Place Update

Use for minor convention changes or small feature additions.

1. Read the existing skill.
2. Edit only affected sections.
3. Preserve unaffected structure and references.
4. Re-score with the quality rubric.

### Strategy 2: Replace

Use for major framework or architectural changes.

1. Generate a new skill from current context.
2. Preserve the skill name when continuity matters.
3. Mark the old skill deprecated.
4. Archive the old skill only after user confirmation if active files must be removed or replaced.

### Strategy 3: Split

Use when one skill has grown too broad.

1. Identify distinct responsibilities.
2. Create `2-3` focused successor skills.
3. Archive the broad skill after confirmation if removal is required.
4. Update references that pointed to the original skill.

### Strategy 4: Merge

Use when several skills overlap heavily.

1. Confirm overlap is greater than `50%`.
2. Merge into one clearer skill.
3. Archive redundant predecessors after confirmation if active copies must be removed.
4. Promote to Full if the merged workflow becomes complex.

## Migration Workflows

### Framework Version Upgrade

1. Detect the version change.
2. Identify breaking changes.
3. Map old patterns to new patterns.
4. Update affected templates and conventions.
5. Re-validate all affected skills.

### Framework Switch

1. Detect framework removal and replacement.
2. Mark old-framework skills as `DEPRECATED`.
3. Run a fresh `DISCOVER` for the new framework.
4. Generate the new skill set.
5. Archive deprecated skills only after user confirmation.

### Convention Evolution

1. Detect rule or config changes.
2. Extract the new conventions.
3. Update convention-type skills first.
4. Update template sections in workflow skills.
5. Re-validate convention compliance.

## Evolution Report Template

```markdown
## Skill Evolution Report

### Trigger
- **Type**: [dependency_change | framework_migration | convention_update | user_request]
- **Detail**: [specific change]
- **Affected skills**: [list]

### Analysis
| Skill | Current State | Strategy | Impact |
|-------|---------------|----------|--------|
| [name] | STALE/DEPRECATED | In-place/Replace/Split/Merge | [description] |

### Changes Applied
- [Skill name]: [change summary]

### Quality Re-Evaluation
| Skill | Before | After | Delta |
|-------|--------|-------|-------|
| [name] | [score]/12 | [score]/12 | [+/-N] |

### Sync Status
- All updated skills synced to `.claude/skills/` and `.agents/skills/`: YES/NO
```
