# Naming Guide Reference

**Purpose:** File and folder naming conventions optimized for LLM discoverability.
**Read when:** Evaluating or fixing naming for LLM navigation improvement.

---

## Core Principle

LLMs discover files through two primary mechanisms:
1. **Glob patterns** — `**/*.test.ts`, `src/components/**`
2. **Grep/content search** — `function handlePayment`, `class UserService`

File and folder names must support both discovery paths.

---

## Directory Naming Rules

### DO

| Rule | Example | Why |
|------|---------|-----|
| Kebab-case | `user-auth/`, `data-pipeline/` | Consistent, no quoting needed in shell |
| Domain-descriptive | `payment-gateway/`, `email-templates/` | LLM can infer contents from name |
| Plural for collections | `components/`, `routes/`, `tests/` | Signals "contains many items" |
| Singular for modules | `auth/`, `billing/`, `notification/` | Signals "cohesive domain unit" |

### DON'T

| Anti-pattern | Problem | Fix |
|-------------|---------|-----|
| `utils/`, `helpers/`, `misc/` | Opaque — LLM cannot infer contents | Name by domain: `string-helpers/`, `date-utils/` |
| `common/`, `shared/` (bare) | Too generic — what's shared? | `shared-types/`, `shared-ui/`, or flatten into consumers |
| `lib/` (bare) | Ambiguous scope | Name by function: `api-client/`, `validation/` |
| `internal/` | LLM doesn't know what's inside | Name by domain or flatten |
| Abbreviations: `cfg/`, `mgmt/`, `svc/` | Grep misses: "config" won't match `cfg` | Use full words |

---

## File Naming Rules

### Suffix Conventions

Consistent suffixes enable reliable glob-based discovery:

| Suffix Pattern | Glob Pattern | Purpose |
|---------------|-------------|---------|
| `*.test.ts`, `*.spec.ts` | `**/*.test.*` | Test files |
| `*.config.ts`, `*.config.js` | `**/*.config.*` | Configuration |
| `*.types.ts`, `*.d.ts` | `**/*.types.*` | Type definitions |
| `*.stories.tsx` | `**/*.stories.*` | Storybook stories |
| `*.schema.ts` | `**/*.schema.*` | Validation schemas |
| `*.middleware.ts` | `**/*.middleware.*` | Middleware |
| `*.service.ts` | `**/*.service.*` | Business logic services |
| `*.route.ts`, `*.controller.ts` | `**/*.route.*` | HTTP routes |

### File Name Body

| Rule | Bad | Good | Reason |
|------|-----|------|--------|
| Domain-descriptive | `handler.ts` | `payment-handler.ts` | Unique in grep results |
| Action + subject | `process.ts` | `process-refund.ts` | Clear intent |
| No single-word generics | `index.ts` (barrel only) | `user-routes.ts` | Barrel exports OK; logic files need names |
| Match exported entity | `class PaymentService` in `service.ts` | `class PaymentService` in `payment-service.ts` | File name predicts content |

---

## Index File Policy

Index files (`index.ts`, `__init__.py`) are acceptable ONLY as barrel exports / re-exports:

```typescript
// GOOD: index.ts as barrel export
export { UserService } from './user-service'
export { PaymentService } from './payment-service'

// BAD: index.ts containing business logic
// LLM finds "index.ts" but cannot infer what's inside
export class UserService { ... }
```

**Rule**: If `index.ts` contains >10 lines of logic, extract to a named file and re-export.

---

## CLAUDE.md File Naming

| Location | Name | Purpose |
|----------|------|---------|
| Project root | `CLAUDE.md` | Project-wide conventions |
| `.claude/rules/` | `{concern}.md` | Modular rules by concern |
| Package root | `CLAUDE.md` | Package-specific overrides |
| Module directory | `CLAUDE.md` | Module-specific context (rare) |

Rule files in `.claude/rules/` should be named by concern, not by team or priority:
- `coding-standards.md` (concern)
- `testing-policy.md` (concern)
- `security-rules.md` (concern)

---

## Rename Assessment Template

When evaluating files for rename:

```yaml
RENAME_ASSESSMENT:
  file: "[current path]"
  issues:
    - type: generic_name | abbreviation | missing_suffix | inconsistent_case
      severity: high | medium | low
  proposed: "[new path]"
  glob_improvement: "[pattern that now works]"
  grep_improvement: "[search term that now finds this file]"
  breaking_changes:
    - "[import path X needs update]"
    - "[CI config Y references old path]"
```

---

## Validation: Discovery Smoke Test

After renaming, verify discoverability:

```bash
# Test 1: Can we find all files of each type?
find . -name "*.test.*" | wc -l    # Should match known test count
find . -name "*.config.*" | wc -l  # Should match known config count

# Test 2: Do domain searches return relevant results?
grep -rl "payment" src/ | head -10  # Should find payment-related files
grep -rl "auth" src/ | head -10     # Should find auth-related files

# Test 3: Are there remaining generic names?
find . -name "utils.*" -o -name "helpers.*" -o -name "misc.*" | wc -l
# Target: 0
```
