# Sweep False Positives Catalog Reference

Purpose: prevent accidental deletion of files that static tools often misclassify as unused.

Scope boundary:
- This file = **detection patterns** (what static tools miss and why).
- `language-patterns.md` = **per-language tooling** (knip/vulture/staticcheck/cargo-udeps choice and fallback hierarchy).
- `troubleshooting.md` = **recovery procedures** (restoring from backup, aborting cleanup, scan-perf fixes).

## Contents

1. Dynamic loading
2. Framework convention files
3. Build-time references
4. Magic-string references
5. Verification checklist
6. Risk matrix

## Dynamic Import And Lazy Loading

Commonly misdetected patterns:

```typescript
const module = await import(`./plugins/${name}`);
const LazyComponent = React.lazy(() => import('./HeavyComponent'));
import(/* webpackChunkName: "feature" */ './feature');

if (process.env.NODE_ENV === 'development') {
  require('./devTools');
}
```

Verify by:
- searching for `import(` and `require(` patterns
- checking bundler chunk configuration
- searching for string-literal references to the target name

## Framework Convention Files

| Framework | Convention Files | Why Static Detection Fails |
|-----------|------------------|----------------------------|
| Next.js | `pages/**/*`, `app/**/*` | File path defines the route |
| Nuxt | `pages/**/*`, `components/**/*` | Auto-import convention |
| Remix | `routes/**/*`, `root.tsx` | File-based routing |
| Gatsby | `src/pages/*`, `gatsby-*.js` | Convention-driven config |
| Jest | `**/*.test.ts`, `**/*.spec.ts` | Test runner auto-discovery |
| Storybook | `**/*.stories.tsx` | Storybook auto-discovery |

Always check framework configuration before proposing deletion.

## Build-Time Only References

Files often used only through tooling:

```text
babel.config.js
webpack.config.js
postcss.config.js
tailwind.config.js
vite.config.ts
```

Verify by:
- checking config imports and plugin lists
- confirming tool usage in scripts, CI, or hooks

## Magic-String References

Files may be referenced indirectly:

```typescript
const icon = `icon-${name}`;
themes.forEach(t => import(`./themes/${t}`));
```

Also check:
- `package.json` `main`, `exports`, `bin`
- `tsconfig.json` paths
- Storybook, Jest, or bundler config

## Verification Checklist

Confirm all relevant checks before deletion:

```text
□ Searched for the filename without extension
□ Checked for dynamic import or require patterns
□ Confirmed it is not a framework convention file
□ Checked build and tooling config references
□ Checked package.json main/exports/bin
□ Checked tsconfig path aliases
□ Checked Storybook and test-runner configuration
```

## False Positive Risk Matrix

| Pattern | False Positive Risk | Countermeasure |
|---------|---------------------|----------------|
| Files in `pages/` or `app/` | Very High | Framework check required |
| `*.config.*` | High | Verify tool ownership and CI use |
| `*.stories.*` | High | Verify Storybook discovery |
| `*.test.*` / `*.spec.*` | High | Verify test-runner discovery |
| `hooks/use*.ts` | Medium | Check indirect hook consumption |
| `utils/*.ts` | Medium | Check dynamic imports and aliases |
| `assets/*` | Medium | Check CSS/HTML/string references |
| `types/*.d.ts` | Low | Keep unless package/type usage is clear |
