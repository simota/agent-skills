# Claude Code Skills API Reference

Purpose: load this when a generated skill needs Claude Code-specific metadata, dynamic context injection, sandbox limits, or routing-sensitive `description` tuning.

## Contents

1. Frontmatter fields
2. Dynamic context injection
3. Arguments
4. Placement and precedence
5. `description` tuning
6. `context: fork`
7. `allowed-tools`
8. `disable-model-invocation`

## Frontmatter Fields

### Required Fields

| Field | Type | Why it matters |
|-------|------|----------------|
| `name` | string | Display and routing identifier |
| `description` | string | Strongest routing signal |

### Optional Fields

| Field | Type | Default | Use when |
|-------|------|---------|----------|
| `user-invocable` | boolean | `false` | users should call the skill directly |
| `allowed-tools` | string[] | all | the skill needs sandbox restrictions |
| `disable-model-invocation` | boolean | `false` | direct prompt expansion is safer or cheaper |
| `model` | string | — | the runtime must pin a model such as `sonnet`, `opus`, `haiku` |
| `agent` | boolean | `false` | the skill should run as a background agent |
| `argument-hint` | string | — | the slash command needs a visible placeholder |
| `context` | string | — | the skill needs isolated context, for example `fork` |

### Example

```yaml
---
name: deploy
description: [one Japanese sentence for the deploy workflow]
user-invocable: true
argument-hint: "<environment>"
allowed-tools:
  - Bash
  - Read
  - Glob
---
```

## Dynamic Context Injection

### `!`command`` Syntax

Use shell output only when the generated skill genuinely needs runtime state.

```markdown
Current branch: !`git branch --show-current`
Recent commits: !`git log --oneline -5`
Dependencies: !`cat package.json | jq '.dependencies'`
```

Rules:
- Commands run when the skill is loaded.
- Slow commands delay skill startup.
- Failures insert their error text into the prompt.
- Use only trusted commands.

## Arguments

| Variable | Meaning |
|----------|---------|
| `$ARGUMENTS` | full user argument string |
| `$0` | skill name |
| `$1`, `$2`, ... | positional arguments |

```markdown
---
name: review-pr
user-invocable: true
argument-hint: "<PR-number>"
---

Review PR #$1.
!`gh pr view $1 --json title,body,files`
```

## Placement and Precedence

### Precedence Order

| Priority | Location | Scope |
|----------|----------|-------|
| `1` | Enterprise Policy | organization-wide |
| `2` | `~/.claude/skills/` | user-wide |
| `3` | `.claude/skills/` | project-specific |
| `4` | Plugin / extension | tool-provided |

Same-name conflicts resolve in favor of the higher-priority location.

### Expected Project Layout

```text
.claude/skills/
├── my-skill/
│   ├── SKILL.md
│   └── reference/
│       ├── patterns.md
│       └── examples.md
```

Sigil must also mirror the same structure into `.agents/skills/`.

## `description` Tuning

`description` is the most important routing field. Optimize for clear trigger coverage without becoming noisy.

### Good Patterns

| Pattern | Example effect |
|---------|----------------|
| Trigger keyword coverage | improves activation rate |
| Explicit exclusions | prevents false matches |
| Clear use timing | improves routing confidence |
| Differentiation from nearby skills | reduces collisions |

### Anti-Patterns

| Anti-pattern | Risk |
|--------------|------|
| vague helper wording | weak activation |
| very long description (`5+` lines) | routing noise |
| jargon-only wording | poor natural-language match |
| wording too similar to another skill | routing collisions |

### Practical Limits

- Best length is usually `1-3` sentences.
- Target roughly `50-150` characters when possible.
- Keep the description in Japanese for Claude-style project skills unless project conventions clearly require otherwise.

## `context: fork`

Use `context: fork` when the skill should run in isolated context:

- avoids polluting the parent conversation
- fits long-running analysis
- pairs well with `agent: true`

```yaml
---
name: long-analysis
description: [one Japanese sentence for large-codebase analysis]
context: fork
agent: true
---
```

## `allowed-tools`

Restrict tools to match the skill's safety profile.

```yaml
# Read-only
allowed-tools:
  - Read
  - Glob
  - Grep

# Execute but do not edit
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash

# Full access
# omit allowed-tools
```

Sigil should choose `allowed-tools` only when the skill's execution model depends on it.

## `disable-model-invocation`

Use `disable-model-invocation: true` when the skill should expand directly without an additional model pass.

Typical uses:
- static project rules
- prompt injection of fixed checklists
- low-cost, low-latency boilerplate prompts

Dynamic `!`command`` blocks still run when model invocation is disabled.
