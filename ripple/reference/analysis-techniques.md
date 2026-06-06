# Analysis Techniques

Detailed commands, categories, and quality standards for Ripple's vertical and horizontal analysis.

## Dependency Tracking Commands

```bash
# Find all files importing a module
grep -rl "from.*ModuleName" src --include="*.ts" --include="*.tsx"

# Using madge for dependency tree
npx madge --depends-on src/path/to/file.ts src/

# Find reverse dependencies (what depends on this)
npx madge --why src/target/file.ts src/

# Generate dependency graph for specific file
npx madge --image impact.svg src/path/to/file.ts
```

## Impact Categories

| Category | Description | Detection Method |
|----------|-------------|------------------|
| **Direct Dependents** | Files that directly import the changed module | `grep -rl "from.*changed-module"` |
| **Transitive Dependents** | Files that depend on direct dependents | `npx madge --depends-on` recursive |
| **Interface Consumers** | Code using exported types/interfaces | TypeScript compiler, grep for type names |
| **Test Files** | Tests that cover the changed code | `*.test.ts`, `*.spec.ts` matching patterns |
| **Configuration** | Config files that reference the module | Package.json, tsconfig paths, etc. |

## Breaking Change Detection

| Change Type | Risk Level | Detection |
|-------------|------------|-----------|
| **Rename export** | HIGH | All importers break |
| **Remove export** | CRITICAL | All importers break, no fallback |
| **Change function signature** | HIGH | All callers need update |
| **Change return type** | MEDIUM-HIGH | Type-dependent code breaks |
| **Add required parameter** | HIGH | All callers need update |
| **Change default value** | LOW-MEDIUM | Behavior change, may be silent |
| **Internal refactoring** | LOW | No external impact if API unchanged |

## Impact Depth Levels

```
Level 0: Changed file itself
    ↓
Level 1: Direct importers (high confidence)
    ↓
Level 2: Importers of importers (medium confidence)
    ↓
Level 3+: Transitive dependencies (lower confidence)
```

## Pattern Categories to Check

| Category | Examples | Detection |
|----------|----------|-----------|
| **Naming Conventions** | Variable names, function names, file names | Regex patterns, ESLint rules |
| **File Structure** | Component organization, folder hierarchy | Directory comparison |
| **Code Patterns** | Error handling, data fetching, state management | AST analysis, grep patterns |
| **API Patterns** | Request/response format, error codes | Schema comparison |
| **Type Patterns** | Interface naming, type organization | TypeScript analysis |

## Naming Convention Checks

```bash
# Check function naming (camelCase)
grep -E "function [A-Z]" src/ -r --include="*.ts"

# Check component naming (PascalCase)
grep -E "const [a-z].*= \(" src/components -r --include="*.tsx"

# Check interface naming (I-prefix or no prefix)
grep -E "interface [^I]" src/ -r --include="*.ts"

# Check file naming patterns
find src -name "*.ts" | grep -v -E "^[a-z-]+\.ts$"
```

## Pattern Compliance Matrix Template

| Pattern | Status | Evidence |
|---------|--------|----------|
| Error handling | ✅ / ⚠️ / ❌ | Uses project's ErrorBoundary pattern |
| State management | ✅ / ⚠️ / ❌ | Follows Zustand conventions |
| API calls | ✅ / ⚠️ / ❌ | Uses established fetcher pattern |
| Type definitions | ✅ / ⚠️ / ❌ | Interfaces in types/ directory |
| Test structure | ✅ / ⚠️ / ❌ | Follows describe/it pattern |

## Existing Pattern Discovery

```bash
# Find similar implementations for reference
grep -rl "similar pattern" src --include="*.ts" | head -5

# Count pattern usage across codebase
grep -c "pattern" src/**/*.ts | sort -t: -k2 -rn | head -10

# Find established conventions in similar files
ls src/components/*.tsx | head -5
```

## Quality Standards

### Analysis Completeness Checklist

#### Vertical Impact
- [ ] All direct dependents identified
- [ ] Transitive dependencies traced to level 2+
- [ ] Breaking changes explicitly listed
- [ ] Test files in scope identified
- [ ] Configuration files checked

#### Horizontal Consistency
- [ ] Naming conventions verified
- [ ] File structure patterns checked
- [ ] Code patterns compared to existing
- [ ] Type patterns validated
- [ ] Error handling patterns confirmed

#### Risk Assessment
- [ ] All five risk dimensions scored
- [ ] Scores justified with evidence
- [ ] Overall risk level determined
- [ ] Mitigation strategies proposed
- [ ] Go/No-go recommendation provided

### Report Quality Gates

| Criterion | Requirement |
|-----------|-------------|
| Affected files listed | 100% of known impacts |
| Risk scores | All 5 dimensions with evidence |
| Pattern violations | Specific file:line citations |
| Recommendations | Actionable, not vague |
| Test requirements | Specific test cases suggested |
