# Targeted Patch Reference

Purpose: Execute a surgical code change with minimal blast radius. Smaller than `fix` (which still includes investigation context), lighter than `harden`. Ideal for copy fixes, config tweaks, single-line bug fixes, flag toggles, and minor polish.

## Scope Contract

A targeted patch **must** satisfy all of:

- ≤ 30 lines of code changed
- ≤ 3 files touched
- Zero refactoring, reformatting, or unrelated cleanup
- Zero new dependencies
- Zero new abstractions (no extracted helpers, no new types)
- Single logical concern (one-line fix AND a doc typo = two patches)

If any rule is violated → not a patch. Upgrade to `fix` (with Scout handoff) or `ddd` / `crud` depending on size.

## Typical Use Cases

| Case | Example |
|------|---------|
| Copy fix | typo in user-facing error message |
| Config tweak | timeout 30s → 60s based on production data |
| Off-by-one | `i <= N` → `i < N` at known location |
| Defensive null check removal | known-non-null path |
| Feature flag default | `enabled: false` → `enabled: true` |
| Import path fix | old module path → renamed |
| Env var name change | align with new convention |
| Missing awaits | known async call |

## Workflow

```
1. DEFINE scope (file + line + expected change)
2. ASSERT it fits the scope contract (if not, escalate)
3. READ the change location + surrounding context
4. CHANGE the specific lines
5. TEST: add / update 1 regression test
6. VERIFY: run targeted test + adjacent test file
7. HANDOFF to Guardian (size XS PR)
```

## Regression Test Coupling

Every patch requires exactly one regression test added or modified:

```ts
// Before patch: test didn't cover this input
it('handles empty string', () => {
  expect(slugify('')).toBe('');  // new
});
```

If no test is feasible (pure config with no behavior), document why in PR:
```
# No code test: this is a config value. Verified via staging load test.
```

## Output Template

```markdown
## Builder Targeted Patch

**Location**: `src/api/checkout.ts:142`
**Scope**: 1 file, 3 lines changed, 1 test added
**Concern**: off-by-one in pagination cursor
**Scout handoff**: no (obvious; see line 142)

### Diff
```diff
-  return items.slice(offset, offset + limit + 1);
+  return items.slice(offset, offset + limit);
```

### Test added
```ts
it('returns exactly limit items, not limit+1', () => {
  const items = [1,2,3,4,5,6,7,8,9,10];
  expect(paginate(items, 0, 3)).toEqual([1,2,3]);
});
```

### Rollback
Single-commit revert is safe; no dependent changes.

### Next
- Guardian `pr` with size XS
- Radar may want to extend pagination test coverage separately
```

## Anti-Patterns

- "While I'm here, let me also..." (every extra line breaks the scope contract)
- Reformatting unrelated code (style changes belong in a separate PR)
- Renaming along with fixing (rename = separate patch)
- Adding a new helper function (violates "no new abstractions")
- Skipping the test because "it's just a one-liner" (even one-liners need regression pinning)
- Bundling 3 unrelated config tweaks (each is its own patch)

## When to Upgrade

| Signal | Escalate to |
|--------|-------------|
| Exceeds 30 lines | `fix` |
| Requires investigation | Scout → `fix` |
| Adds abstraction | `crud` or `ddd` |
| External API involved | `integrate` |
| Cross-file refactor | `harden` or Zen |

## Handoff

- **Guardian → `pr`**: size XS, minimal review overhead
- **Radar**: if patch exposes a coverage gap, broader test task
- **Guardian ← Scout**: if investigation uncovered the fix location, Scout handoff may upgrade this to `fix`
