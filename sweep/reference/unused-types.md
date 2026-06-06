# Unused Types Cleanup (TypeScript / Flow)

Reference for Sweep's `types` recipe. Detect orphan interfaces, transitively unused types, generic constraint pollution, deprecated type re-exports, and `any` accumulation handoff.

---

## 1. Detection Tools

| Concern | Tool | Notes |
|---|---|---|
| Unused exported types | `ts-prune` (legacy), `knip --include exports types` | Flag exported types with no imports |
| Unused local types | TS `--noUnusedLocals` | Catches function-scope types |
| Unused parameters | TS `--noUnusedParameters` | Adjacent concern |
| Re-export chains | `ts-unused-exports` | Detects pass-through re-exports with no consumers |
| `any` accumulation | `eslint-plugin-typescript-eslint`, `@typescript-eslint/no-explicit-any` | Track `any` density per file |

---

## 2. Categories

### Hard-orphan types (safe to remove, confidence ≥ 95)
```ts
// Defined, exported, but never imported anywhere
export interface UnusedConfig {
  legacyFlag: boolean;
}
```
Detection: `knip` flags + grep verification across src, tests, and `*.d.ts`.

### Transitively unused types
```ts
export type A = { x: B };  // A unused
export type B = { y: number };  // B used only by A → also unused
```
Iterative pass: remove A → re-run → B becomes orphan → remove → ...

### Generic constraint pollution
```ts
export type Container<T extends Identifiable> = { item: T };
//                       ^^^^^^^^^^^^^^^^^^
// If `Identifiable` is used ONLY as a constraint here, it's not "unused" by ts-prune
// but it's load-bearing — keep.
```
But:
```ts
export type LegacyConstraint = { id: string; deprecated: true };
export type SomeContainer<T extends LegacyConstraint> = { ... };
// SomeContainer never used → both candidates for removal.
```

### Deprecated re-exports
```ts
// public-api.ts
export { OldType } from './internal';  // marked @deprecated
```
If no consumers → remove. If consumers exist but `@deprecated` is past sunset date → flag for migration handoff to `Shift`.

### `any` accumulation (HANDOFF, not removal)
```ts
function process(data: any): any { ... }
```
Don't auto-remove `any` — escalate to `Quill` for proper typing. Sweep can quantify the problem (count of `any` per file/module) but won't fix.

---

## 3. Detection Workflow

### Pass 1: Initial scan
```bash
npx knip --include exports types
npx ts-prune --error  # legacy alternative
```

### Pass 2: Cross-verify
For each candidate, grep across:
- `src/` source code
- `tests/`, `__tests__/`, `*.test.ts`
- `*.d.ts` declaration files
- `*.stories.tsx` Storybook files
- `docs/` (in case types are used in code samples)

```bash
grep -rn "MyType" --include='*.ts' --include='*.tsx' --include='*.d.ts' .
```

### Pass 3: Verify no string-based usage
Some libraries reference type names as strings (rare):
- `tRPC` router definitions
- `class-validator` decorators
- `io-ts` codecs

If found, mark as PROTECTED.

### Pass 4: Iterate (transitive)
After removing batch N, re-run scan. Newly orphan types appear as previous-iteration types are removed.

---

## 4. False Positive Patterns

| Pattern | Why ts-prune flags it | Why it's NOT removable |
|---|---|---|
| Type used in `.d.ts` ambient declarations | Not in module graph | Required for global typing |
| Type used as generic constraint elsewhere | Not "imported" | Bound by `extends` clause |
| Type used in JSDoc `@type {Foo}` in JS file | Not parsed by TS | Used by `--checkJs` |
| Type re-exported from `index.ts` for public API | No internal consumers | External package consumers |
| Type in `*.config.ts` consumed by build tooling | Tool-specific resolution | Vite/Webpack plugins read it |
| Type used by Code Connect figma file | Different file extension | Used by Figma MCP integration |
| Type used by tRPC router type inference | Inference is implicit | Critical for type safety end-to-end |

### Detection for false positives
- Check `package.json` `"types"` / `"exports"` entries — types listed there are public API
- Check `tsconfig.json` `"include"` / `"files"` — non-default paths may not be tracked
- Check for `.d.ts` declarations that reference the type
- Check for Code Connect `*.figma.ts` files (Frame agent integration)

---

## 5. Re-export Chain Flattening

### Pattern
```ts
// internal/types.ts
export interface Button { ... }

// internal/index.ts
export type { Button } from './types';

// public/index.ts
export type { Button } from '../internal';
```

### Tools
- `ts-unused-exports` detects re-exports with no consumers
- Manual: trace each `export ... from` chain, find consumers at the end

### Outcome
- If end of chain has consumers → flatten (consumer imports directly from source)
- If no consumers → remove all chain links

---

## 6. `any` Accumulation Handling

Don't remove. Quantify and hand off.

### Quantify
```bash
# Count `any` per file
grep -rcE ':\s*any\b|<\s*any\s*>|as\s+any\b' src/ --include='*.ts' --include='*.tsx' \
  | sort -t: -k2 -nr | head -20
```

### Output
```
Top files by `any` count:
  src/legacy/parser.ts: 47
  src/api/handlers.ts: 23
  src/utils/helpers.ts: 18
```

### Handoff
- Recipient: `Quill`
- Payload: file list + count + suggested concrete types if discoverable
- Quill replaces `any` with proper types incrementally

---

## 7. Verification

1. `tsc --noEmit` passes
2. `tsc --noEmit --strict` passes (catches subtle issues)
3. All tests pass
4. Bundle size delta logged (type-only removals = 0 runtime delta, but build time may improve)
5. No new `tsc` errors introduced
6. Public API documentation is updated if types were public

---

## 8. Common Pitfalls

| Pitfall | Avoidance |
|---|---|
| Removing types used in `.d.ts` ambient declarations | grep across all `.d.ts` files |
| Removing types used as generic constraints | TS strict checks catch most; verify with `tsc --strict` |
| Removing types re-exported as part of public API | Check `package.json` exports field |
| Removing types used by `tRPC` end-to-end inference | Test API client codegen post-removal |
| Removing types used in Storybook `Meta<>` declarations | Run Storybook build |
| Bulk removing `any` instead of replacing | Hand off to Quill |
| Removing `@deprecated` types still in use | Coordinate sunset migration via Shift first |

---

## 9. Decision Walkthrough Template

```
Scope: ____ files (TS / TSX / d.ts)
Tools run:
  □ knip --include exports types
  □ ts-unused-exports
  □ tsc --noUnusedLocals

Findings:
  Hard-orphan types:        ____ (auto-removable, conf ≥ 95)
  Transitively unused:      ____ (iterative removal, ≥ 90)
  Re-export chain orphan:   ____ (flatten or remove)
  Public API types:         ____ (PROTECTED — package.json exports)
  Generic constraints:      ____ (verify with tsc --strict)
  `any` density top-N:      ____ files (HANDOFF to Quill)

Verification:
  □ tsc --noEmit baseline pass
  □ tsc --strict baseline pass
  □ All tests pass
  □ Storybook build pass (if applicable)
  □ tRPC client codegen pass (if applicable)
  □ Code Connect lint pass (if applicable)

Handoff:
  □ Builder for execution
  □ Quill for `any` cleanup
  □ Shift for `@deprecated` type migration
```

---

## 10. References
- knip docs (`--include exports types`)
- `ts-unused-exports` npm package
- TypeScript `--noUnusedLocals`, `--noUnusedParameters`
- `@typescript-eslint/no-explicit-any` (any-counter)
- TypeScript Performance Wiki — re-export chain overhead
