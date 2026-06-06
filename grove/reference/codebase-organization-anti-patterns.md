# Codebase Organization Anti-Patterns

Purpose: Use this reference when choosing a source tree shape, diagnosing codebase-structure drift, or planning a safe reorganization.

## Contents

- Codebase anti-pattern catalog
- Pattern comparison
- Structure selection rules
- Scalability checkpoints
- Naming rules
- Grove integration

Folder-organization failure modes, layer-vs-feature traps, and scaling risks.

## 1. Codebase Organization Anti-Patterns

| ID | Anti-Pattern | What Goes Wrong | Typical Signals | Recommended Response |
|---|---|---|---|---|
| **CO-01** | **Type-First Trap** | Files are grouped only by technical type (`components/`, `hooks/`, `utils/`) instead of business capability. | Understanding one feature requires crossing `5-7` directories; changes spread across many folders. | Move toward feature-based modules; consider Feature-Sliced Design for larger frontends. |
| **CO-02** | **Copy-Paste Discovery** | Poor structure makes existing code hard to find, so teams duplicate logic. | Similar logic appears in multiple directories; refactors miss copies. | Group by feature, define public module APIs, add barrel exports where appropriate. |
| **CO-03** | **Convention Mismatch** | The layout ignores language-specific defaults. | Go uses `src/`; Python misses package boundaries; Java package layout is broken. | Detect language first, then apply the language-specific template. |
| **CO-04** | **Premature Abstraction** | The structure is too deep too early. | A `3`-file project ships with `5` layers and many empty folders. | Start with the smallest viable structure and refactor as the codebase grows. |
| **CO-05** | **Naming Collision** | Multiple directories serve the same purpose under different names. | `lib/`, `shared/`, `utils/`, `helpers/`, and `common/` coexist. | Pick one name per purpose and enforce it consistently. |
| **CO-06** | **Cyclic Module Dependency** | Modules depend on each other bidirectionally. | Independent testing or deployment becomes impossible; impact analysis is unreliable. | Restore one-way dependencies, extract interfaces, or split shared contracts. |
| **CO-07** | **Test-Source Divorce** | The source tree and test tree stop matching. | Test placement is inconsistent, coverage is hard to measure, CI config grows complex. | Standardize on either co-location or centralized tests per language. |

## 2. Pattern Comparison

### Type-Based

```text
src/
  components/
  hooks/
  services/
  utils/
  styles/
```

- Best only for very small codebases with low domain complexity.
- Degrades quickly because related behavior is split across many directories.
- Encourages wide change amplification and weak ownership boundaries.

### Feature-Based

```text
src/
  features/
    auth/
      components/
      hooks/
      services/
      index.ts
    user/
      components/
      hooks/
      services/
      index.ts
  shared/
    ui/
    utils/
```

- Higher cohesion because one feature lives in one subtree.
- Lower coupling when other modules access the feature only through its public API.
- Works well for most application-scale repositories.

### Feature-Sliced Design

```text
src/
  app/
  pages/
  widgets/
  features/
  entities/
  shared/
```

- Use when the product spans multiple domains and long-lived teams.
- Enforce dependency direction: `app -> pages -> widgets -> features -> entities -> shared`.
- Avoid for small prototypes and marketing sites.

## 3. Structure Selection Rules

| Project size | Approx. file count | Default recommendation |
|---|---:|---|
| Small | `<=20` | Flat structure with minimal subdirectories |
| Medium | `20-100` | Feature-based organization |
| Large | `100-500` | Feature-Sliced Design or DDD-style modularization |
| Very large | `500+` | Monorepo with package-level boundaries |

Decision prompts:
- Team size `1-3`: use simple feature grouping.
- Team size `4-10`: use feature grouping plus public API control.
- Team size `10+`: consider stronger module-boundary enforcement.
- Strong framework conventions: follow them first.
- No strong framework conventions: default to feature-based organization.

## 4. Scalability Checkpoints

| Stage | Signal | Recommended action |
|---|---|---|
| Early | Structure still flat and discoverable | Keep it simple |
| Growth | `20+` files in a domain | Start feature grouping |
| Expansion | `50+` files | Add explicit public APIs and module boundaries |
| Maturity | `100+` files | Evaluate FSD, DDD, or package boundaries |
| Crisis | `AP-001` or `AP-008` already present | Plan a phased structural migration |

## 5. Naming Rules

Use one stable name per purpose:

| Purpose | Preferred name |
|---|---|
| Source | `src/` except Go (`cmd/`, `internal/`) |
| Tests | `tests/` or co-located `*.test.*` |
| Docs | `docs/` |
| Config | `config/` |
| Scripts | `scripts/` |
| Shared code | one of `shared/` or another single agreed name |

Avoid:
- Mixing `lib/`, `shared/`, `utils/`, `helpers/`, and `common/`
- Case conventions that violate the language norm
- Abbreviation-heavy names such as `svc`, `mgr`, `hdlr`
- Versioned directory names like `v2/` or `new-src/`

## 6. Grove Integration

Use this reference in Grove as follows:
1. Detect language and framework conventions before recommending a structure.
2. Screen `CO-01` through `CO-07` during structural audits.
3. Combine these findings with `AP-001` through `AP-016`.
4. Choose a migration strategy based on current size and team structure.

Quality gates:
- Type-based layout at medium scale: recommend feature grouping.
- Repeated logic across features: propose a shared module extraction.
- Language-convention mismatch: propose template correction.
- Too many empty folders: simplify the structure.
- Duplicate-purpose folders: consolidate naming.
- Cyclic dependencies: reorganize dependency direction.

**Source:** [Feature-Sliced Design: Frontend Folder Structure](https://feature-sliced.design/blog/frontend-folder-structure) · [Iterators: Project Codebase Organization](https://www.iteratorshq.com/blog/a-comprehensive-guide-on-project-folder-organization/) · [GitHub Well-Architected: Anti-Patterns](https://wellarchitected.github.com/library/scenarios/anti-patterns/)
