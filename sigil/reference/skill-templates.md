# Skill Templates

Purpose: load this during `CRAFT` to choose Micro vs Full, preserve required structure, and fill templates with project-specific conventions.

## Contents

1. Frontmatter rules
2. Type selection
3. Micro template
4. Full template
5. Authoring guardrails
6. File and size rules

## Frontmatter Rules

Every generated skill MUST include YAML frontmatter:

```yaml
---
name: skill-name
description: [one Japanese sentence]
---
```

Ecosystem-specific constraints (additive to the official spec — see [`official-skill-guide.md` § 2 YAML Frontmatter 完全仕様](official-skill-guide.md#2-yaml-frontmatter-完全仕様) for the canonical kebab-case / 1024-char / XML / reserved-name rules and the rationale behind them):

- `name`: unique within the project, normally `2-4` words
- `description`: one Japanese sentence, concise, routing-friendly (project guardrail — official limit is 1024 chars)
- Add optional fields only when the generated skill truly needs them

## Type Selection

| Use this type | When | Expected size |
|---------------|------|---------------|
| Micro | Single task, clear outcome, `0-2` decision points | `10-80` lines |
| Full | Multi-step process, `3+` decision points, significant domain knowledge, or multiple variants | `100-400` lines |

Promote to Full when rollback guidance, multiple patterns, or supporting references are required for safe execution.

## Micro Template

Use English headings by default, but match the project's established skill language if existing skills use another convention.

```markdown
---
name: [skill-name]
description: [one Japanese sentence]
---

# [Skill Title]

## Purpose
[Explain when and why to use this skill.]

## Steps

1. [Step 1]
2. [Step 2]
3. [Step 3]

## Template

\```[lang]
[Project-specific starter template]
\```

## Conventions
- [Naming rule]
- [File placement rule]
- [Testing or error-handling rule]
```

Micro minimum:
- Purpose: `1-2` sentences
- Steps: `3+`
- Include at least one of `Template` or `Conventions`

## Full Template

```markdown
---
name: [skill-name]
description: [one Japanese sentence]
---

# [Skill Title]

## Purpose
[Explain scope, prerequisites, and expected outcome.]

## Design Principles
- [Project-specific principle 1]
- [Project-specific principle 2]
- [Project-specific principle 3]

## Workflow

### Step 1: [Phase Name]
[Actionable instructions]

### Step 2: [Phase Name]
[Actionable instructions]

### Step 3: [Phase Name]
[Actionable instructions]

## Templates

### Pattern A: [Simple case]

\```[lang]
[Template code]
\```

### Pattern B: [Complex case]

\```[lang]
[Template code]
\```

## Error Handling
[Project-specific failure and recovery rules]

## Testing
[Framework-specific test expectations]

## Checklist
- [ ] [Check 1]
- [ ] [Check 2]
- [ ] [Check 3]
```

Full minimum:
- Purpose: `3+` sentences including prerequisites
- Workflow: `3+` phases
- Templates: `2+` patterns or variations
- Explicit `Error Handling`, `Testing`, and `Checklist`

## Authoring Guardrails

### Variable Substitution

| Variable | Source | Example |
|----------|--------|---------|
| `[ProjectName]` | manifest name | `my-app` |
| `[Framework]` | framework detection | `Next.js` |
| `[FrameworkVersion]` | manifest dependencies | `14.1.0` |
| `[ComponentDir]` | directory scan | `src/components` |
| `[TestDir]` | test layout detection | `__tests__` |
| `[TestFramework]` | dependencies | `vitest` |
| `[CSSApproach]` | config or deps | `tailwind` |
| `[PackageManager]` | lock files | `pnpm` |
| `[ImportAlias]` | `tsconfig.json` | `@/` |

Rules:
1. Replace every `[Variable]` before install.
2. If the value is unknown, use the safest framework default and add `<!-- TODO: verify -->`.
3. If multiple values are valid, use conditional branches instead of guessing.
4. Never ship raw placeholders in installed skills.

### Structural Guardrails

- Every step must be executable in the target project.
- All code blocks must have language tags.
- Use the project's actual paths and dependency set.
- Do not hardcode developer-specific machine paths.
- Keep references one hop away from `SKILL.md`.
- For Claude Code-specific fields and sandbox choices, cross-check `claude-code-skills-api.md`.
- For final scoring, use `validation-rules.md`.

## File and Size Rules

### Required Layout

- `.claude/skills/[skill-name]/SKILL.md`
- `.agents/skills/[skill-name]/SKILL.md`
- Full Skills may add:
  - `.claude/skills/[skill-name]/reference/[topic].md`
  - `.agents/skills/[skill-name]/reference/[topic].md`

### Naming Rules

Project-specific layout (canonical naming and file-structure rules — directory kebab-case, exact `SKILL.md` spelling, no `README.md` inside skill folders — live in [`official-skill-guide.md` § 5 File Structure Requirements](official-skill-guide.md#5-file-structure-requirements)):

- Reference files: `reference/[topic].md` (one hop from `SKILL.md`)
- Skills are installed to both `.claude/skills/` and `.agents/skills/` (Sigil-specific dual-install)

### Size Guidelines

| Type | Lines | Sections | Templates |
|------|-------|----------|-----------|
| Micro | `10-80` | `3-5` | `0-1` |
| Full | `100-400` | `6-10` | `2-5` |
