# Dependency Graph Analysis

Reference for Lens's `dependency` recipe. Deep dependency graph analysis: fan-in/fan-out, transitive closure, circular dependencies, direction violations, package boundary leakage.

---

## 1. Tools by Language

| Language | Tool | Notes |
|---|---|---|
| TypeScript / JavaScript | `madge`, `dpdm`, `ts-prune` | Module graph + circular detection |
| Python | `pydeps`, `pyan3`, `snakefood` | Function + module graph |
| Go | `go list -deps`, `goda` | Built-in dependency listing |
| Java / Kotlin | `jdeps`, JArchitect | JVM bytecode analysis |
| Rust | `cargo-modules`, `cargo-deps` | Crate-level + intra-crate |
| Ruby | `RubyMine`, `Reek` | Object dependency analysis |

---

## 2. Metrics

### Fan-In (Afferent Coupling)
Number of modules that depend on this module.
- High fan-in = "god module" or core utility
- Investigation: is fan-in justified (true core)? Can it be split?

### Fan-Out (Efferent Coupling)
Number of modules this module depends on.
- High fan-out = orchestrator or coupled module
- Investigation: too many responsibilities? Apply Dependency Inversion?

### Instability Index (I)
```
I = Fan-Out / (Fan-In + Fan-Out)
```
- 0 = stable (depended-on)
- 1 = unstable (depends on others)
- Stable + abstract (interfaces) = good
- Stable + concrete = brittle (refactor risk)

### Transitive Closure Size
Total reachable dependencies (direct + indirect).
- Large closure = harder to test in isolation
- Useful for "what would break if X changes?"

---

## 3. Circular Dependencies

### Severity classification
| Pattern | Severity | Action |
|---|---|---|
| 2-cycle (A → B → A) at module load | HIGH | Refactor immediately; breaks tree shaking |
| 3+ cycle within same package | MEDIUM | Extract shared module |
| Type-only cycle (resolved at compile) | LOW | Convert to `import type`, often OK |
| Cross-package cycle | HIGH | Architectural violation; likely DI needed |

### Detection
```bash
npx madge --circular --extensions ts,tsx src/
# Output: list of cycle chains
```

---

## 4. Dependency Direction Violations

Define allowed directions, then detect violations:

```yaml
allowed:
  - presentation → application → domain
  - any → shared

forbidden:
  - domain → presentation
  - domain → infrastructure
  - UI → DB (must go through application)
```

### Detection
```bash
# TS example: find UI components importing DB modules directly
grep -rE "^import.*from ['\"].*\\b(db|database|prisma|knex)" src/components/
```

Tools: `dependency-cruiser` (TS) supports rule-based dependency policies.

---

## 5. Package Boundary Leakage

If language supports `internal` / private packages, detect external access:

| Language | Private convention |
|---|---|
| Go | `internal/` directory — compiler-enforced |
| TypeScript | `_*` prefix (convention only); ESLint rule via `import/no-internal-modules` |
| Python | `_*` prefix (convention only); `__all__` declaration |
| Rust | `pub(crate)` / `pub(super)` — compiler-enforced |

### Detection example
```bash
# TS: imports of files starting with _
grep -rE "import.*from ['\"][^'\"]*/_" src/
```

---

## 6. Output Format

```yaml
file: src/services/UserService.ts
metrics:
  fan_in: 23      # 23 modules import this
  fan_out: 8      # this imports 8 modules
  instability: 0.26  # 8 / (23 + 8)
  classification: stable_concrete  # WARNING: refactor candidate
  transitive_closure: 47

circular_dependencies:
  - chain: [UserService, AuthService, UserService]
    severity: HIGH
    fix: "Extract shared UserContext interface"

direction_violations:
  - file: src/components/UserCard.tsx
    line: 12
    violation: "UI directly imports prisma client"
    expected: "Use UserService instead"

package_leakage:
  - importer: src/components/AdminPanel.tsx
    target: src/_internal/rawDb.ts
    severity: HIGH
```

---

## 7. Common Pitfalls

| Pitfall | Avoidance |
|---|---|
| Treating high fan-in as bad | Core utilities legitimately have high fan-in |
| Ignoring type-only cycles | Convert to `import type`; fewer runtime issues |
| madge missing dynamic imports | Cross-check with grep for `import(...)` |
| Counting test dependencies | Filter `**/*.test.*`, `**/__tests__/**` separately |
| Ignoring monorepo workspace boundaries | Run per-workspace; aggregate carefully |
| God module split = many small files = worse fan-out | Sometimes consolidation is correct; check responsibility cohesion |

---

## 8. Decision Walkthrough Template

```
Scope: ____ files / packages
Tools used: madge / dpdm / pydeps / dependency-cruiser

Findings:
  Top 5 fan-in modules:
    1. ____ (fan-in: ___)
    ...
  Top 5 fan-out modules:
    1. ____ (fan-out: ___)
    ...
  Instability hotspots (stable_concrete): ____ files

  Circular deps: ____ HIGH, ____ MEDIUM, ____ LOW
  Direction violations: ____
  Package leakage: ____

Recommendations:
  □ Refactor stable_concrete top-N to abstract interfaces
  □ Break HIGH circular deps
  □ Add ESLint dependency-cruiser config to prevent regression

Handoff:
  □ Atlas for architectural decision (ADR)
  □ Sweep for orphaned dependency removal
  □ Builder for refactor execution
```

---

## 9. References
- madge / dpdm / dependency-cruiser docs
- Robert C. Martin: "Clean Architecture" (Stable Dependencies Principle, Stable Abstractions Principle)
- Go: `internal` package conventions
