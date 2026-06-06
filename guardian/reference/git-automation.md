# Git Hooks & Automation

Purpose: Standardize lightweight Git automation for quality checks, secrets scanning, auto-merge, and monorepo-aware CI.

## Contents

- Hook manager selection
- Secret detection
- Auto-merge
- Monorepo CI
- Recommended 2025 stack

## Hook Manager Selection

| Factor | Husky | Lefthook | pre-commit |
|--------|-------|----------|------------|
| Runtime | Node.js | Go | Python |
| Speed | serial / moderate | parallel / fast | slower |
| Config style | `.husky/` shell scripts | YAML | YAML |
| Best fit | JS/TS repos | polyglot repos | Python-heavy repos |

Recommended default:
- `Lefthook` for polyglot or performance-sensitive repos
- `Husky` for JS-first repos already committed to Node tooling

Example `lefthook.yml`:

```yaml
pre-commit:
  parallel: true
  commands:
    lint:
      glob: "*.{ts,tsx}"
      run: npx eslint {staged_files}
    format:
      glob: "*.{ts,tsx,json,md}"
      run: npx prettier --check {staged_files}
    typecheck:
      glob: "*.{ts,tsx}"
      run: npx tsc --noEmit

commit-msg:
  commands:
    commitlint:
      run: npx commitlint --edit {1}
```

Example `husky` + `lint-staged`:

```bash
# .husky/pre-commit
npx lint-staged
```

```json
{
  "lint-staged": {
    "*.{ts,tsx}": ["eslint --fix", "prettier --write"],
    "*.{json,md,yml}": ["prettier --write"]
  }
}
```

## Secret Detection

Recommended tools:
- `gitleaks`
- `detect-secrets`
- `trufflehog`

Rule:
- run secret detection in `pre-commit` or CI before merge

## Auto-Merge

Use auto-merge only for low-risk PRs such as:
- dependency updates
- documentation-only changes
- clearly non-breaking maintenance

Example:

```yaml
name: Auto Merge
on:
  pull_request:
    types: [labeled, synchronize]

jobs:
  auto-merge:
    if: contains(github.event.pull_request.labels.*.name, 'auto-merge')
    runs-on: ubuntu-latest
    steps:
      - uses: pascalgn/automerge-action@v0.16.4
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          MERGE_LABELS: "auto-merge,!wip,!do-not-merge"
          MERGE_METHOD: squash
          MERGE_DELETE_BRANCH: true
```

Require branch protection alongside auto-merge.

## Monorepo CI

Affected package detection:

```bash
turbo run build --affected
nx affected -t build
```

Always set:

```yaml
- uses: actions/checkout@v4
  with:
    fetch-depth: 0
```

Path-based CI:

```yaml
on:
  push:
    paths:
      - 'packages/frontend/**'
      - 'packages/shared/**'
```

Dynamic path detection:

```yaml
- uses: dorny/paths-filter@v3
  id: filter
  with:
    filters: |
      frontend:
        - 'packages/frontend/**'
      backend:
        - 'packages/api/**'
```

Versioning for monorepos:

```bash
npx changeset
npx changeset version
npx changeset publish
```

## Recommended 2025 Stack

| Concern | Recommended default |
|---------|---------------------|
| package manager | `pnpm` |
| task runner | `Turborepo` or `Nx` |
| hooks | `Lefthook` or `Husky` |
| commit validation | `commitlint` |
| versioning | `Changesets` |
| CI/CD | `GitHub Actions` |
