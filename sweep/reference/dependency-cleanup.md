# Dependency Cleanup Best Practices

Purpose: safe detection and removal of unused dependencies, with dependency-specific false-positive rules and lockfile-sensitive verification.

## Contents

1. Why dependency cleanup matters
2. Tooling by ecosystem
3. Dependency false positives
4. Safe removal workflow
5. Security considerations
6. CI integration

## Why Dependency Cleanup Matters

Removing unused dependencies reduces:
- package and install size
- attack surface and noisy CVE alerts
- maintenance and upgrade overhead
- build time and license exposure

## Tooling By Ecosystem

### JavaScript / TypeScript

Preferred:

```bash
npx knip --reporter compact
npx knip --include dependencies
npx knip --workspace
npx knip --reporter codeowners --no-exit-code
```

Fallback:

```bash
npx depcheck
npx depcheck --json
npx depcheck --ignores="@types/*,husky"
```

Use `depcheck` only when `knip` is unavailable or incompatible.

### Python

```bash
pipreqs . --force
pip-audit
vulture src/ --min-confidence 80
```

### Go

```bash
go mod tidy -v
go mod why -m <module>
```

### Rust

```bash
cargo +nightly udeps
```

## Dependency False Positives

| Pattern | FP Risk | Why | Countermeasure |
|---------|---------|-----|----------------|
| Build plugins | High | used only in config | scan config files |
| `@types/*` | High | implicit TypeScript usage | ignore or verify type config |
| PostCSS/Babel plugins | High | config-only usage | inspect tool configs |
| Peer dependencies | Medium-High | resolved by host package | confirm package contract |
| CLI tools | Medium | called only from scripts | inspect `package.json` scripts |
| Polyfills | Medium | runtime/global usage | inspect browser/runtime support |
| Dev servers | Low-Medium | dev-only use | inspect local workflows |

## Safe Removal Workflow

1. Detect with dependency-aware tooling.
2. Classify with confidence scoring plus dependency-specific checks:
   - scripts
   - config files
   - CI/CD usage
   - documentation references
3. Create backup branch and snapshot manifest plus lockfile.
4. Remove dependencies incrementally:
   - start with `>=90`
   - remove one package or one category at a time
5. Verify:
   - install succeeds
   - build succeeds
   - tests pass
   - development server still starts if relevant
6. Review lockfile diffs for unintended transitive removals.

## Security Considerations

Unused dependencies still matter:
- they enlarge CVE exposure
- they increase supply-chain risk
- they can introduce unnecessary license obligations

Recommended recurring checks:
- `npm audit`, `pip-audit`, or ecosystem equivalents
- SBOM refresh during major cleanup cycles

## CI Integration

```yaml
name: Dependency Check
on: [pull_request]
jobs:
  knip:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
      - run: npm ci
      - run: npx knip --include dependencies --no-exit-code
```

Use warning-only mode until the project is ready to enforce cleanup gates.
