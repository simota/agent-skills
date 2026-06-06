# Imports Cleanup

Reference for Sweep's `imports` recipe. Cleanup of import statements: unused imports, circular dependencies, duplicates, side-effect import survival, barrel-file overhead, and type-only import promotion.

---

## 1. Detection Tools

| Concern | Tool | Language |
|---|---|---|
| Unused imports | ESLint `no-unused-vars` (with `args: 'after-used'`), `eslint-plugin-import` `no-unused-modules` | JS/TS |
| Circular deps | madge, dpdm | JS/TS |
| Duplicate imports | ESLint `no-duplicate-imports` | JS/TS |
| Type-only promotion | TS `--verbatimModuleSyntax`, `eslint-plugin-import` `consistent-type-specifier-style` | TS |
| Barrel file overhead | tsc compilation time profiling, knip `--include exports` | TS |
| Python | pyflakes, ruff `F401`, autoflake | Python |
| Go | goimports, gci | Go |

---

## 2. Categorization

### Hard-unused (safe to remove, confidence ≥ 95)
```ts
import { unusedFn } from './utils';  // never referenced anywhere
```
Detection: tool flags + grep verification → no usage in src/, tests/, or docs.

### Side-effect imports (PROTECT)
```ts
import './polyfills';                 // executes module side effects
import 'reflect-metadata';            // required for decorators
import 'flag-icon-css/css/flag-icons.min.css';  // CSS injection
```
Detection: imports without binding clause. **Never auto-remove.** Tag with `// side-effect` comment; preserve in cleanup.

### Type-only imports (promote, don't remove)
```ts
// Before
import { User } from './types';
function greet(u: User) { return `hi ${u.name}`; }
```
TS 4.5+ with `verbatimModuleSyntax`:
```ts
import type { User } from './types';
```
Promotes runtime import to type-only — eliminated during compilation, smaller bundles.

### Duplicate imports (consolidate)
```ts
import { a } from 'lib';
import { b } from 'lib';
import type { c } from 'lib';
```
→
```ts
import { a, b, type c } from 'lib';
```

---

## 3. Circular Dependencies

### Detection
```bash
npx madge --circular --extensions ts,tsx src/
# or
npx dpdm --no-warning --no-tree --circular src/
```

### Severity
| Severity | Pattern | Fix priority |
|---|---|---|
| HIGH | A → B → A (2-cycle) at module load | Critical — breaks tree shaking, bundlers may bundle unused code |
| MEDIUM | A → B → C → A (3+ cycle) | Refactor extract shared module |
| LOW | Type-only cycle (resolved at compile) | Often OK; convert all imports to `import type` |

### Fix patterns
- Extract shared types/constants to a `shared/` module
- Inversion: depend on abstractions (interfaces) rather than concrete implementations
- Lazy import via dynamic `import()` for runtime-only cycles

---

## 4. Barrel Files

### What
```ts
// src/components/index.ts
export { Button } from './Button';
export { Card } from './Card';
export { Input } from './Input';
// ... 50 more
```
Consumers import: `import { Button } from '@/components';`

### Cost
- Bundlers must follow every export to determine actually-used exports → tree shaking degraded
- IDE autocomplete loads all exports
- TS compilation time grows with barrel size
- Reported 4-7x slower compile in monorepos with deep barrels

### Action
1. **Internal-only barrels** (not part of public API): inline imports — `import { Button } from '@/components/Button'`
2. **Public-API barrels** (library entry point): keep but mark `/* @__PURE__ */` for tree-shake hints
3. **Re-export with types**: `export type { ButtonProps } from './Button'` — type-only re-exports compile away

### Migration
- Use `eslint-plugin-no-barrel-files` for new code prevention
- Use codemod (jscodeshift) for bulk inline conversion of existing imports

---

## 5. Side-Effect Survival Detection

Side-effect imports are easily removed by aggressive cleanup tools and break runtime in subtle ways.

### Detection
```js
// AST check: import without binding
ImportDeclaration {
  specifiers: []        // ← side-effect
  source: 'package'
}
```

### Common side-effect imports (NEVER auto-remove)
- CSS: `import 'styles.css'`
- Polyfills: `import 'core-js/stable'`, `import 'regenerator-runtime/runtime'`
- Decorators metadata: `import 'reflect-metadata'`
- Test setup: `import '@testing-library/jest-dom'`
- Service workers: `import { registerSW } from 'virtual:pwa-register'` (sometimes side-effect even with binding)
- Vite/Webpack magic imports: `import 'virtual:my-module'`

### Detection script (find-and-protect)
```bash
grep -rn "^import '\(.*\)';" src/ | sort -u > side-effect-imports.txt
# Review manually before any removal
```

---

## 6. Verification Workflow

1. **Pre-cleanup baseline**: build + run all tests; record bundle size
2. **Apply removal in batches** of ≤ 50 imports per file
3. **Per-batch verification**:
   - `npm run build` succeeds
   - `npm test` passes
   - `npm run lint` passes
   - Bundle size delta logged
4. **If any check fails**: rollback the batch, re-classify imports
5. **Post-cleanup**: re-run circular dep check; should not increase

---

## 7. Common Pitfalls

| Pitfall | Symptom | Avoidance |
|---|---|---|
| Removing CSS side-effect imports | Styles disappear at runtime | Tag side-effects, never auto-remove |
| Auto-removing `reflect-metadata` | Decorators silently fail | Detect "polyfill" patterns |
| Promoting runtime import to `type` import for value used at runtime | Compile error or runtime undefined | Cross-check usage: type position vs value position |
| Inlining barrel imports breaks public API | Library consumers' code breaks | Distinguish internal vs public barrels |
| Removing imports that are used in JSX template strings | Runtime undefined | grep across JSX, template literals, dynamic property access |
| Cleaning up tests that import side-effects via `setup.ts` | Tests fail intermittently | Trace through Vitest/Jest setup files |
| Type imports removed because TS thinks unused at value level | Runtime works, but documentation broken | Check JSDoc / inline comments for type references |

---

## 8. Decision Walkthrough Template

```
Scope: ____ files
Language: TS / JS / Python / Go / mixed

Tool runs:
  □ ESLint no-unused-vars
  □ ESLint no-duplicate-imports
  □ knip --include exports
  □ madge --circular
  □ ruff F401 (Python)
  □ goimports (Go)

Findings categorization:
  Hard-unused:          ____ (auto-removable, confidence ≥ 95)
  Side-effect:          ____ (PROTECTED)
  Duplicate:            ____ (consolidate)
  Type-only candidate:  ____ (promote)
  Circular HIGH:        ____ (refactor required)
  Circular MED/LOW:     ____ (defer or type-only)
  Barrel inline candid: ____ (codemod)

Verification:
  □ Pre-cleanup baseline build+test pass
  □ Per-batch verification (≤ 50 imports/file)
  □ Bundle size delta logged
  □ No new circular deps post-cleanup

Handoff:
  □ Builder for execution
  □ Atlas for circular dep refactor (architectural)
```

---

## 9. References
- ESLint `no-unused-vars`, `no-duplicate-imports`, `import/no-unused-modules`
- TypeScript `--verbatimModuleSyntax` (5.0+)
- madge / dpdm (circular dependency analysis)
- knip (`--include exports`, `--include types`)
- Vercel: "Why barrel files cause slow Next.js builds"
- Microsoft TypeScript wiki: Performance — barrel file overhead
