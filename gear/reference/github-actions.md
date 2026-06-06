# GitHub Actions Templates

> **Note:** For advanced GHA workflow design (trigger strategy, security hardening, performance optimization, PR automation, Reusable/Composite design, monorepo CI, self-hosted runners), see the **Pipe** agent (`pipe/SKILL.md`).

CI/CD workflow templates, composite actions, reusable workflows, OIDC authentication, and security scanning.

Runner snapshot (2026-05):
- **arm64 Linux/Windows runners GA** (2024-09-03). Free for public repos since 2025-01-16 (`ubuntu-24.04-arm` label). [Source: [arm64 runners GA](https://github.blog/changelog/2024-09-03-github-actions-arm64-linux-and-windows-runners-are-now-generally-available/); [Free for public repos](https://github.blog/changelog/2025-01-16-linux-arm64-hosted-runners-now-available-for-free-in-public-repositories-public-preview/)]
- **macOS M2 (arm64) larger runners GA**: use `macos-latest-xlarge`, `macos-15-xlarge`, or `macos-14-xlarge`. [Source: [GHA November 2025 releases](https://github.blog/changelog/2025-11-06-new-releases-for-github-actions-november-2025/)]
- **Node.js 20 deprecated in GHA** (announced 2025-09-19): runners default to Node 24 on **2026-06-16**; Node 20 removed **2026-09-16**. Update `actions/cache` → **v5**, `actions/setup-node` → **v4**, etc. Test early with `FORCE_JAVASCRIPT_ACTIONS_TO_NODE24=true`. [Source: [Node 20 deprecation](https://github.blog/changelog/2025-09-19-deprecation-of-node-20-on-github-actions-runners/)]
- **Action allowlisting** (GA all plans, 2026-02): define exactly which actions and reusable workflows may run per repository, now available on Free / Team / Enterprise. [Source: [Early Feb 2026 updates](https://github.blog/changelog/2026-02-05-github-actions-early-february-2026-updates/)]
- Reusable workflows now support up to **10 nested levels** and **50 called workflows** per run (up from 4 / 20).

---

## CI Workflow (Lint, Test, Build)

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

jobs:
  lint:
# ...
```

---

## Matrix Testing (Node Versions, OS)

```yaml
# .github/workflows/test-matrix.yml
name: Test Matrix

on:
  push:
    branches: [main]
  pull_request:

jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      fail-fast: false
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
# ...
```

---

## CD Workflow (Deploy)

```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [main]
  workflow_dispatch:
    inputs:
      environment:
        description: 'Deploy environment'
        required: true
        default: 'staging'
        type: choice
        options:
          - staging
# ...
```

---

## Release Workflow (Semantic Release)

```yaml
# .github/workflows/release.yml
name: Release

on:
  push:
    branches: [main]

permissions:
  contents: write
  issues: write
  pull-requests: write

jobs:
  release:
    runs-on: ubuntu-latest
# ...
```

---

## Dependabot Configuration

```yaml
# .github/dependabot.yml
version: 2
updates:
  # npm dependencies
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "weekly"
      day: "monday"
    open-pull-requests-limit: 10
    groups:
      dev-dependencies:
        dependency-type: "development"
        patterns:
          - "*"
# ...
```

---

## Composite Action (DRY Setup)

```yaml
# .github/actions/setup-node-pnpm/action.yml
name: 'Setup Node + pnpm'
description: 'Common setup for Node.js projects with pnpm'

inputs:
  node-version:
    description: 'Node.js version'
    default: '20'
  install-deps:
    description: 'Run pnpm install'
    default: 'true'

runs:
  using: 'composite'
  steps:
# ...
```

Usage in workflows:
```yaml
- uses: ./.github/actions/setup-node-pnpm
  with:
    node-version: '20'
```

---

## Reusable Workflow

```yaml
# .github/workflows/ci-reusable.yml
name: Reusable CI

on:
  workflow_call:
    inputs:
      node-version:
        type: string
        default: '20'
      run-e2e:
        type: boolean
        default: false
    secrets:
      NPM_TOKEN:
        required: false
# ...
```

---

## OIDC Authentication (Passwordless)

```yaml
# AWS without secrets
permissions:
  id-token: write
  contents: read

steps:
  - uses: aws-actions/configure-aws-credentials@v4
    with:
      role-to-assume: arn:aws:iam::123456789:role/github-actions
      aws-region: ap-northeast-1

# GCP without secrets
  - uses: google-github-actions/auth@v2
    with:
      workload_identity_provider: 'projects/123/locations/global/workloadIdentityPools/github/providers/github'
# ...
```

---

## Security Scanning in CI

> **WARNING — trivy-action supply-chain incident (2026-03-19)**: A threat actor force-pushed malicious code into 76/77 version tags of `aquasecurity/trivy-action`. Always pin to a **full commit SHA** (not a mutable tag). Verify the SHA against the [security advisory](https://github.com/aquasecurity/trivy/security/advisories/GHSA-69fq-xp46-6x23) before use.

```yaml
# Gitleaks (secret detection) — pin to commit SHA, never a mutable tag
- uses: gitleaks/gitleaks-action@<full-commit-sha>
  env:
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

# Trivy (vulnerability scan) — pin to a known-clean commit SHA post 2026-04-09
# DEPRECATED: aquasecurity/trivy-action@master was compromised in Mar 2026
- uses: aquasecurity/trivy-action@<full-commit-sha>
  with:
    scan-type: 'fs'
    severity: 'CRITICAL,HIGH'
```

[Source: [Trivy supply chain incident advisory](https://github.com/aquasecurity/trivy/security/advisories/GHSA-69fq-xp46-6x23); [GHA workflow security hardening post-incident](https://github.com/aquasecurity/trivy/discussions/10402)]

---

## Renovate Configuration (Dependabot Alternative)

```json
// renovate.json
{
  "$schema": "https://docs.renovatebot.com/renovate-schema.json",
  "extends": ["config:recommended"],
  "schedule": ["before 6am on monday"],
  "timezone": "Asia/Tokyo",
  "labels": ["dependencies"],
  "packageRules": [
    {
      "matchUpdateTypes": ["minor", "patch"],
      "automerge": true
    },
    {
      "matchPackagePatterns": ["eslint", "prettier", "typescript"],
      "groupName": "linting"
// ...
```
