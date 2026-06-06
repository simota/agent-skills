# Dead Code Detection Guide

Purpose: Use this file before deleting code that might be unused, exported, dynamic, or protected by feature flags.

## Contents
- [Detection Tools by Language](#detection-tools-by-language)
- [Dead Code Categories](#dead-code-categories)
- [Safe Removal Checklist](#safe-removal-checklist)
- [Dead Code Cleanup Pattern](#dead-code-cleanup-pattern)
- [Language-Specific Patterns](#language-specific-patterns)

Comprehensive guide for detecting and safely removing dead code across languages.

---

## Detection Tools by Language

### TypeScript/JavaScript

| Tool | Detects | Command | Notes |
|------|---------|---------|-------|
| `knip` | Unused files, exports, deps, types | `npx knip` | **Recommended** — ~300K weekly downloads; auto-detects tooling; VSCode extension available; `--fix` flag auto-removes unused deps ([knip.dev](https://knip.dev/)) |
| `eslint` | Unused vars, imports | `npx eslint --rule 'no-unused-vars: error' src/` | |
| TypeScript compiler | Unreachable code | `tsc --noUnusedLocals --noUnusedParameters` | |
| `depcheck` | Unused dependencies | `npx depcheck` | Still useful for a focused dep-only check |
| ~~`ts-prune`~~ | ~~Unused exports~~ | ~~`npx ts-prune`~~ | **Archived Sep 19, 2025** — use `knip` instead ([comparison & migration](https://knip.dev/explanations/comparison-and-migration)) |

### Python

| Tool | Detects | Command |
|------|---------|---------|
| `vulture` | Unused code | `vulture src/` |
| `autoflake` | Unused imports/vars | `autoflake --check -r src/` |
| `pylint` | Unused vars, imports | `pylint --disable=all --enable=W0611,W0612 src/` |
| `flake8` | Unused imports | `flake8 --select=F401 src/` |
| `pyflakes` | Unused imports/vars | `pyflakes src/` |

### Go

| Tool | Detects | Command |
|------|---------|---------|
| `deadcode` | Unreachable functions | `deadcode ./...` |
| `staticcheck` | Unused code patterns | `staticcheck ./...` |
| `golangci-lint` | Multiple checks | `golangci-lint run --enable unused` |

### Rust

| Tool | Detects | Command |
|------|---------|---------|
| `cargo` (built-in) | Dead code warnings | `cargo build 2>&1 \| grep "dead_code"` |
| `cargo-udeps` | Unused dependencies | `cargo udeps` |

---

## Dead Code Categories

| Category | Example | Safe to Remove? |
|----------|---------|-----------------|
| Unused local variable | `const unused = 1;` | Yes |
| Unused import | `import { unused } from './lib';` | Yes |
| Commented-out code | `// oldFunction();` | Yes |
| Console.log in production | `console.log('debug');` | Yes |
| Unused private method | `private helper() {}` | Yes |
| Unused exported function | `export function unused() {}` | Check external usage |
| Unused public API | `public unusedMethod() {}` | May be called dynamically |
| Feature flag dead branch | `if (false) { ... }` | Confirm flag is permanent |

---

## Safe Removal Checklist

Before removing code that appears dead:

- [ ] Search for string references (dynamic invocation)
- [ ] Check for reflection/metaprogramming usage
- [ ] Verify not used in tests only
- [ ] Check for external package consumers (if library)
- [ ] Confirm feature flags are truly retired
- [ ] Run full test suite after removal

---

## Dead Code Cleanup Pattern

```typescript
// Step 1: Identify unused code
// Run: npx ts-prune | grep -v "used in module"

// Step 2: Mark for removal (optional comment phase)
/** @deprecated Unused - scheduled for removal */
export function oldHelper() { ... }

// Step 3: Remove and verify
// Delete the code, run tests

// Step 4: Clean up imports
// Remove any import statements that reference deleted code
```

---

## Language-Specific Patterns

### TypeScript: Find Unused Exports

```bash
# knip — recommended replacement for ts-prune (archived Sep 2025)
npx knip

# Auto-fix unused deps and some exports
npx knip --fix

# CI: report findings without failing the build while cleaning up
npx knip --no-exit-code
```

### Python: Remove Unused Imports

```bash
# Auto-fix with autoflake
autoflake --in-place --remove-all-unused-imports -r src/

# Preview only
autoflake --check -r src/
```

### Go: Find Unreachable Functions

```bash
# golang.org/x/tools/cmd/deadcode
go install golang.org/x/tools/cmd/deadcode@latest
deadcode -test ./...
```
