# CLAUDE.md Best Practices

Purpose: load this when Sigil generates, updates, or reconciles project guidance that overlaps with `CLAUDE.md`.

## Contents

1. Maturity model
2. What to include
3. What to exclude
4. RFC 2119 wording
5. `@import`
6. Hierarchical precedence
7. Skeleton template

## Maturity Model (`L0-L6`)

| Level | Name | Typical state |
|-------|------|---------------|
| `L0` | Absent | no `CLAUDE.md` |
| `L1` | Minimal | language and style rules only |
| `L2` | Structured | clear sections for tests, git, tooling |
| `L3` | Comprehensive | architecture, security, CI/CD guidance |
| `L4` | Composable | split via `@import` |
| `L5` | Adaptive | conditional rules by environment or branch |
| `L6` | Self-Evolving | hooks and CI keep rules updated |

### Recommended Path

```text
L0 -> L1 -> L2 -> L3 -> L4 -> L5 -> L6
```

Use `@import` once the file exceeds `500` lines or multiple teams own different sections. Avoid splitting when the file is under `100` lines.

## What to Include

### High-Value Content

| Category | Why it belongs |
|----------|----------------|
| coding conventions | consistency baseline |
| testing policy | quality baseline |
| commit / PR policy | history quality |
| architecture rules | structural consistency |
| explicit prohibitions | error prevention |
| error-handling policy | robustness |

### Medium-Value Content

| Category | When useful |
|----------|-------------|
| dependency policy | library or version control matters |
| security rules | secrets and input validation need explicit rules |
| performance rules | projects have known bottlenecks or budgets |
| documentation rules | public APIs or regulated docs matter |

### Low-Value Content

Avoid unless the project explicitly needs them:
- long project descriptions
- change logs
- team org charts

## What to Exclude

### Anti-Patterns

| Anti-pattern | Why to avoid it |
|--------------|-----------------|
| overspecification | lowers adherence and hides important rules |
| duplicating formatter settings | tools should remain the source of truth |
| vague advice | impossible to validate |
| contradictory layered rules | creates routing and compliance drift |

### Good vs Bad Rule Shape

```markdown
BAD: Write clean code and care about performance.

GOOD: In React components, use `useMemo` or `useCallback` only when the computation is expensive or a memoized child depends on stable props.
```

## RFC 2119 Wording

Use requirement strength intentionally:

| Keyword | Strength | Typical use |
|---------|----------|-------------|
| `MUST` / `MUST NOT` | absolute | security, data integrity |
| `SHOULD` / `SHOULD NOT` | strong recommendation | best practices |
| `MAY` | optional | preference or local choice |

Sigil should use stronger terms only when the project already treats the rule as mandatory.

## `@import`

### Basic Syntax

```markdown
# CLAUDE.md

@import ./docs/coding-standards.md
@import ./docs/testing-policy.md
@import ./docs/security-rules.md
```

### Split Criteria

| Split when | Keep inline when |
|------------|------------------|
| file exceeds `500` lines | file is under `100` lines |
| different teams own different sections | one team owns the full file |
| domain-specific rules diverge | rules are mostly uniform |
| one section changes much more often | change rate is uniform |

## Hierarchical Precedence

Typical order:

```text
~/.claude/CLAUDE.md
project/CLAUDE.md
project/packages/api/CLAUDE.md
```

More specific files override broader ones. Sigil must avoid creating skill guidance that contradicts a more specific local rule.

## Skeleton Template

```markdown
# Project Rules

## Language & Style

## Architecture

## Testing

## Security

## Git & PR

## Do NOT
```
