# Troubleshooting & Git Hooks

Common build errors, CI/CD failures, Docker issues, diagnostic commands, and git hook configuration.

---

## Common Build Errors

| Error | Cause | Solution |
|-------|-------|----------|
| `ERESOLVE unable to resolve dependency tree` | peer dependency conflict | `pnpm config set auto-install-peers true` or use `overrides` |
| `ERR_PNPM_LOCKFILE_MISSING_DEPENDENCY` | lockfile out of sync | `pnpm install` to regenerate |
| `Module not found` | missing dependency or typo | Check import path, run `pnpm install` |
| `EACCES permission denied` | Docker volume permissions | Use `USER 1000:1000` or `chown` in Dockerfile |
| `JavaScript heap out of memory` | OOM during build | `NODE_OPTIONS=--max-old-space-size=4096` |
| `ETARGET` | package version not found | Check npm registry, use `pnpm update` |

---

## CI/CD Failures

| Symptom | Cause | Solution |
|---------|-------|----------|
| Cache miss every run | hash key mismatch | Verify `hashFiles()` pattern matches lockfile |
| Flaky tests | race conditions / timeouts | Add retries, increase timeout, check `--runInBand` |
| `Permission denied` in Actions | missing permissions | Add `permissions:` block to workflow |
| Artifacts not uploading | path mismatch | Verify `path:` matches actual output directory |

---

## Docker Issues

| Error | Cause | Solution |
|-------|-------|----------|
| `COPY failed: file not found` | .dockerignore excluding file | Check `.dockerignore` patterns |
| Layer cache invalidation | wrong COPY order | Move `package.json` COPY before source COPY |
| Large image size | not using multi-stage | Add builder/runner stages |
| `exec format error` | wrong platform | Use `--platform linux/amd64` or multi-arch build |

---

## Quick Diagnostic Commands

```bash
# Check why a package is installed
pnpm why <package>

# Find unused dependencies
npx depcheck

# Check for circular dependencies
npx madge --circular src/

# Verify lockfile integrity
pnpm install --frozen-lockfile

# Check bundle size
npx bundlephobia-cli <package>

# Docker layer analysis
docker history <image> --no-trunc
```

---

## Git Hooks Setup

### Husky + lint-staged

```bash
# Install
pnpm add -D husky lint-staged
pnpm exec husky init
echo "pnpm exec lint-staged" > .husky/pre-commit
```

```json
// package.json
{
  "lint-staged": {
    "*.{ts,tsx}": ["eslint --fix", "prettier --write"],
    "*.{json,md,yml}": ["prettier --write"]
  }
}
```

### Lefthook (Faster Alternative)

```yaml
# lefthook.yml
pre-commit:
  parallel: true
  commands:
    lint:
      glob: "*.{ts,tsx}"
      run: pnpm eslint --fix {staged_files}
    format:
      glob: "*.{ts,tsx,json,md}"
      run: pnpm prettier --write {staged_files}

pre-push:
  commands:
    test:
      run: pnpm test --passWithNoTests
```

### Commitlint (Conventional Commits)

```bash
pnpm add -D @commitlint/cli @commitlint/config-conventional
echo "export default { extends: ['@commitlint/config-conventional'] };" > commitlint.config.js
echo "pnpm exec commitlint --edit \$1" > .husky/commit-msg
```
