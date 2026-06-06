# Migration Strategies

Purpose: Use this reference when you need a safe, staged migration plan for structure changes, config cleanup, or full repository reorganization.

## Contents

- Migration principles
- Migration levels
- Decision tree
- Language-specific notes
- PR template

Strategies for restructuring existing repositories safely.

---

## Migration Principles

1. **Never break the build** — Every intermediate step must compile/run
2. **Small, reviewable PRs** — One structural change per PR
3. **Preserve git history** — Use `git mv` for renames
4. **Update imports incrementally** — Path aliases ease the transition
5. **Test after every move** — Run full test suite per step

---

## Migration Levels

### Level 1: Docs Scaffold (Low Risk)

**When:** Repository has no structured documentation.
**Effort:** 1 hour
**Risk:** None (additive only)

```bash
# Step 1: Create docs structure
mkdir -p docs/{prd,specs,design,checklists,test-specs,adr,guides,api,diagrams}

# Step 2: Add placeholder READMEs
for dir in docs/*/; do
  echo "# $(basename $dir)" > "$dir/README.md"
done

# Step 3: Move existing docs (if any scattered docs exist)
git mv docs/requirements.md docs/prd/PRD-initial.md
git mv docs/architecture.md docs/design/HLD-system.md
```

**Commit pattern:**
```
docs: scaffold documentation directory structure
docs: migrate existing documents to structured layout
```

---

### Level 2: Test Reorganization (Medium Risk)

**When:** Tests are scattered or inconsistently organized.
**Effort:** 2-4 hours
**Risk:** Test discovery may break temporarily

```bash
# Step 1: Create test structure
mkdir -p tests/{unit,integration,e2e,fixtures}

# Step 2: Move tests (preserve git history)
git mv src/**/*.test.ts tests/unit/
git mv test/integration/* tests/integration/
git mv e2e/* tests/e2e/

# Step 3: Update test configuration
# - jest.config.ts / vitest.config.ts: update testMatch patterns
# - CI workflows: update test paths
```

**Pre-flight checklist:**
- [ ] Note current test runner configuration
- [ ] List all test file locations
- [ ] Identify test configuration files
- [ ] Verify CI test commands

**Rollback:** `git revert` the migration commit

---

### Level 3: Source Restructure (High Risk)

**When:** Source code needs modularization (God Directory, Flat Hell).
**Effort:** 1-3 days
**Risk:** Import paths break, CI may fail

#### Phase 1: Add Path Aliases (Non-breaking)

```json
// tsconfig.json
{
  "compilerOptions": {
    "paths": {
      "@/features/*": ["src/features/*"],
      "@/shared/*": ["src/shared/*"]
    }
  }
}
```

#### Phase 2: Create Module Directories

```bash
mkdir -p src/features/{auth,user,payment}
mkdir -p src/shared/{utils,types,constants}
```

#### Phase 3: Move Files (One Module at a Time)

```bash
# Move one feature at a time
git mv src/auth.service.ts src/features/auth/
git mv src/auth.controller.ts src/features/auth/
git mv src/auth.types.ts src/features/auth/

# Create barrel export
echo 'export * from "./auth.service";
export * from "./auth.controller";
export * from "./auth.types";' > src/features/auth/index.ts

# Update imports in dependent files
# Run tests
# Commit
```

#### Phase 4: Update Imports

```bash
# Use automated tools
npx ts-morph-scripts update-imports  # or similar
# OR use IDE refactoring tools
# OR manual search-and-replace with verification
```

**Commit pattern (one per module):**
```
refactor(auth): move auth module to features/auth
refactor(user): move user module to features/user
```

---

### Level 4: Config Cleanup (Medium Risk)

**When:** Config Soup detected.
**Effort:** 1-2 hours
**Risk:** Build/lint may break if config paths change

```bash
# Step 1: Identify duplicate configs
ls -la .eslintrc* .prettierrc* tsconfig*

# Step 2: Consolidate to flat config
# Example: ESLint flat config migration
git rm .eslintrc.js .eslintrc.json
# Create eslint.config.js (flat config)

# Step 3: Move non-root-required configs
mkdir -p config
git mv webpack.config.js config/
git mv postcss.config.js config/

# Step 4: Update references in package.json scripts
```

---

### Level 5: Full Restructure (Very High Risk)

**When:** Major repository overhaul needed.
**Effort:** 1-2 weeks
**Risk:** Extended period of instability

**Strategy: Parallel Structure**

```bash
# Step 1: Create new structure alongside old
mkdir -p src-new/features/{auth,user}
mkdir -p src-new/shared

# Step 2: Copy and refactor (don't move yet)
cp -r src/auth* src-new/features/auth/
# Refactor imports in new location

# Step 3: Verify new structure works
# Run tests against new paths

# Step 4: Swap (atomic)
git mv src src-old
git mv src-new src

# Step 5: Clean up
git rm -r src-old
```

---

## Migration Decision Tree

```
Start
  │
  ├─ No docs/ structure?
  │   └─→ Level 1: Docs Scaffold
  │
  ├─ Tests scattered?
  │   └─→ Level 2: Test Reorganization
  │
  ├─ src/ has God Directory?
  │   ├─ < 30 files → Level 3: Source Restructure (Phase 1-4)
  │   └─ > 30 files → Level 5: Full Restructure
  │
  ├─ Config Soup?
  │   └─→ Level 4: Config Cleanup
  │
  └─ Multiple issues?
      └─→ Apply in order: L1 → L4 → L2 → L3/L5
          (docs first, least risky to most risky)
```

---

## Language-Specific Migration Notes

### TypeScript/JavaScript

- Use `tsconfig.json` paths for import aliases
- `eslint-plugin-import` can enforce module boundaries
- Barrel exports (`index.ts`) ease the transition
- Use `--noUnusedLocals` to catch broken imports

### Python

- Update `pyproject.toml` package paths
- Use relative imports within packages
- `isort` configuration needs update after restructure
- Run `mypy` to catch import errors

### Go

- `go mod` handles imports automatically
- Use `goimports` to fix import paths
- `internal/` enforces privacy at compile time
- Move to `cmd/` + `internal/` from flat structure

### Rust

- Update `mod.rs` / `lib.rs` module declarations
- Cargo workspace for multi-crate restructure
- `use` paths auto-validated by compiler
- Run `cargo check` after each move

---

## Migration PR Template

```markdown
## Repository Structure Migration: {Level Name}

### What Changed
- {Description of structural changes}

### Why
- Anti-pattern detected: {AP-XXX}
- Impact: {description}

### Migration Steps Taken
1. {Step 1}
2. {Step 2}
3. {Step 3}

### Verification
- [ ] All tests pass
- [ ] Build succeeds
- [ ] CI pipeline passes
- [ ] Import paths updated
- [ ] No broken references

### Rollback Plan
```bash
git revert {commit-hash}
```

### Files Moved
| From | To |
|------|-----|
| `src/auth.ts` | `src/features/auth/auth.service.ts` |
```
