# Dependency Management

Package manager reference, audit workflows, lockfile handling, version pinning strategies, and multi-language support.

---

## Package Manager Reference

Current stable lines (2026-05): **npm 11.x** (with v12 in development — `--allow-git=none` is planned default), **pnpm 11.x** (released 2026-04-28, requires Node.js 22+, ESM-only), **yarn 4.x** (Berry). Use `corepack enable` to pin the manager version via `packageManager` in `package.json`; Node.js 24 (Oct 2026) is expected to make Corepack opt-in again because of corporate-proxy friction. [Source: [pnpm 11.0 release notes](https://pnpm.io/blog/releases/11.0); [npm trusted publishing docs](https://docs.npmjs.com/trusted-publishers/); [Yarn 4 release](https://yarnpkg.com/blog/release/4.0)]

| Task | npm | pnpm | yarn |
|------|-----|------|------|
| Install all | `npm install` | `pnpm install` | `yarn` |
| Install (CI) | `npm ci` | `pnpm install --frozen-lockfile` | `yarn install --immutable` |
| Add package | `npm install pkg` | `pnpm add pkg` | `yarn add pkg` |
| Add dev dep | `npm install -D pkg` | `pnpm add -D pkg` | `yarn add -D pkg` |
| Remove | `npm uninstall pkg` | `pnpm remove pkg` | `yarn remove pkg` |
| Update all | `npm update` | `pnpm update` | `yarn up` |
| Update pkg | `npm update pkg` | `pnpm update pkg` | `yarn up pkg` |
| Audit | `npm audit` | `pnpm audit` | `yarn npm audit` |
| Audit fix | `npm audit fix` | `pnpm audit --fix` | `yarn npm audit --recursive` |
| Outdated | `npm outdated` | `pnpm outdated` | `yarn outdated` |
| Dedupe | `npm dedupe` | `pnpm dedupe` | `yarn dedupe` |
| Why | `npm explain pkg` | `pnpm why pkg` | `yarn why pkg` |
| List | `npm list` | `pnpm list` | `yarn info` |
| Clean cache | `npm cache clean --force` | `pnpm store prune` | `yarn cache clean` |
| Publish (OIDC) | `npm publish` (uses Trusted Publishing if configured) | `pnpm publish` (native, v11 dropped npm fallback) | `yarn npm publish` |

---

## Audit Response Flow

```bash
# 1. Check vulnerabilities
pnpm audit

# 2. Check for safe updates
pnpm outdated

# 3. Update within semver range (safe)
pnpm update

# 4. If specific package has vulnerability
pnpm update vulnerable-package

# 5. If major version required (ask first)
pnpm add vulnerable-package@latest

# 6. If transitive dependency
pnpm add vulnerable-package --save-dev
# or use overrides in package.json:
# "pnpm": {
#   "overrides": {
#     "vulnerable-package": "^2.0.0"
#   }
# }
```

---

## Dependency Health Check

```bash
# Check for unused dependencies
npx depcheck

# Check for outdated dependencies
pnpm outdated

# Check bundle size impact
npx bundlephobia-cli package-name

# Check for duplicate dependencies
pnpm dedupe --check

# List direct dependencies
pnpm list --depth=0

# Find why a package is installed
pnpm why package-name

# Check peer dependency issues
pnpm install --strict-peer-dependencies
```

---

## Lockfile Conflict Resolution

```bash
# When lockfile conflicts occur:

# 1. Discard lockfile changes and regenerate
git checkout --theirs pnpm-lock.yaml  # or --ours
pnpm install

# 2. Or regenerate from scratch (last resort)
rm pnpm-lock.yaml
pnpm install

# 3. Verify build still works
pnpm build
pnpm test
```

---

## Version Pinning Strategies

```json
{
  "dependencies": {
    // Exact: Most stable, manual updates required
    "critical-lib": "2.0.0",

    // Patch: Auto-update patch versions (recommended for most)
    "stable-lib": "~2.0.0",

    // Minor: Auto-update minor versions
    "flexible-lib": "^2.0.0",

    // Range: Explicit range
    "legacy-lib": ">=1.0.0 <2.0.0"
  },

  // Override transitive dependencies
  "pnpm": {
    "overrides": {
      "vulnerable-package": "^2.0.0",
      "package>nested-vulnerable": "^1.5.0"
    }
  }
}
```

---

## Supply-Chain Hardening (2026)

Mainstream package managers ship secure-by-default policies. Confirm the install-time guards below are active in every Node.js project.

### pnpm 11 defaults (`pnpm-workspace.yaml`)

pnpm 11 (2026-04-28) moved most settings out of `.npmrc` into `pnpm-workspace.yaml` (or `~/.config/pnpm/config.yaml`). The env-var prefix is `pnpm_config_*`. Five legacy build-related settings are consolidated into the single `allowBuilds` map. [Source: [pnpm 11.0 release](https://pnpm.io/blog/releases/11.0); [Socket — pnpm 11 supply-chain defaults](https://socket.dev/blog/pnpm-11-adds-new-supply-chain-protection-defaults)]

```yaml
# pnpm-workspace.yaml
minimumReleaseAge: 1440          # default in v11; minutes. Blocks newly published versions for 24h.
minimumReleaseAgeExclude:        # hotfix bypass list
  - my-trusted-package
blockExoticSubdeps: true         # default in v11; rejects transitive git/tarball URLs
trustPolicy: no-downgrade        # 10.21+; fail install if a package's trust evidence regresses
trustPolicyExclude: []
trustPolicyIgnoreAfter: 525600   # minutes; skip trust check for releases older than ~1 year
allowBuilds:                     # only these packages may run postinstall lifecycle scripts
  - esbuild
  - sharp
```

### npm 11 + Trusted Publishing (OIDC)

Trusted Publishing (GA 2025-07, bulk-config GA 2026-02) eliminates long-lived `NPM_TOKEN`s. The publisher's GitHub Actions / GitLab CI workflow exchanges an OIDC token for a short-lived npm publish credential, and provenance attestations are emitted automatically (no `--provenance` flag needed). Requires **npm CLI ≥ 11.5.1** and **Node ≥ 22.14.0**. [Source: [npm Trusted Publishing docs](https://docs.npmjs.com/trusted-publishers/); [GitHub Changelog 2026-02-18 — bulk config GA](https://github.blog/changelog/2026-02-18-npm-bulk-trusted-publishing-config-and-script-security-now-generally-available/)]

```jsonc
// .npmrc-equivalent install-time guards
// (top-level — repo .npmrc)
"min-release-age=1440"      // minutes; same intent as pnpm's minimumReleaseAge
"ignore-scripts=true"       // refuse all lifecycle scripts; allowlist via npx --allow
```

```yaml
# Publishing workflow (GitHub Actions) — Trusted Publishing
permissions:
  id-token: write   # required for OIDC
  contents: read
steps:
  - uses: actions/setup-node@v4
    with: { node-version: '22', registry-url: 'https://registry.npmjs.org' }
  - run: npm ci
  - run: npm publish   # provenance attestation auto-generated
```

### yarn 4 (Berry)

Yarn 4 is plug-and-play by default, ships official plugins (typescript, interactive-tools) built-in, and replaced Prolog constraints with a JS/TS engine. Use `yarn install --immutable` in CI (replaces `--frozen-lockfile`) and `yarn npm audit --recursive` for transitive audits. Yarn 4 does not yet ship an equivalent of `minimumReleaseAge`; rely on Renovate's cooldown (see below) instead. [Source: [Yarn 4 release](https://yarnpkg.com/blog/release/4.0)]

### Renovate / Dependabot cooldown

Both bots now treat **3-day npm cooldown** as best-practice default. Renovate 42 added `minimumReleaseAge` to `config:best-practices`, and absent release timestamps are treated as "not yet aged" (safer default). [Source: [Renovate docs — minimum-release-age](https://docs.renovatebot.com/key-concepts/minimum-release-age/)]

```json5
// renovate.json
{
  "extends": ["config:best-practices"],
  "minimumReleaseAge": "3 days",     // npm default; raise to "7 days" for higher-risk projects
  "internalChecksFilter": "strict",  // hold PRs until cooldown elapses
  "osvVulnerabilityAlerts": true     // OSV-based vulnerability PRs
}
```

```yaml
# .github/dependabot.yml — grouped updates reduce PR noise 80-90%
version: 2
updates:
  - package-ecosystem: npm
    directory: /
    schedule: { interval: weekly }
    cooldown:
      default-days: 3              # GA 2025; matches Renovate
    groups:
      eslint:
        patterns: ["eslint*", "@typescript-eslint/*"]
      aws-sdk:
        patterns: ["@aws-sdk/*"]
```

Note: native AI-assisted *update review* is not yet a documented Dependabot or Renovate feature as of 2026-05; downstream SCA tools (Endor Labs, Socket, Snyk) provide reachability analysis to suppress non-exploitable advisories.

### SBOM generation (CycloneDX / SPDX)

EU CRA reporting obligations apply from **2026-09-11** (24h early warning / 72h full notification via the ENISA SRP); CE-marking with SBOM as a legal requirement applies from **2027-12-11**. Have SBOM tooling running by 2026-09 even if not yet labelled. Spec versions in production: **CycloneDX 1.6.1** (security-focused, native vulnerability list), **SPDX 3.0** (compliance-focused, deep license metadata). [Source: [Sbomify — SBOM formats 2026](https://sbomify.com/2026/01/15/sbom-formats-cyclonedx-vs-spdx/); [HeroDevs — SPDX vs CycloneDX](https://www.herodevs.com/blog-posts/spdx-vs-cyclonedx-choosing-the-right-sbom-format-for-your-software-supply-chain)]

```bash
# Syft — multi-format SBOM
syft packages dir:. -o cyclonedx-json=sbom.cdx.json -o spdx-json=sbom.spdx.json

# CycloneDX npm plugin
npx @cyclonedx/cdxgen -t npm -o bom.json

# cdxgen — multi-language (Node/Python/Go/Rust/Java/...)
cdxgen -t js -o bom.json
```

For container images see `reference/docker-patterns.md` (Docker Engine 25+ auto-provenance, `--sbom=true`, Cosign v3 keyless).

---

## Bun Runtime

```bash
# Install
curl -fsSL https://bun.sh/install | bash

# Basic commands (pnpm-like)
bun install              # Install dependencies
bun add <pkg>            # Add package
bun remove <pkg>         # Remove package
bun run <script>         # Run script
bun test                 # Run tests
bun build ./src/index.ts --outdir ./dist  # Bundle
```

```yaml
# GitHub Actions with Bun
- uses: oven-sh/setup-bun@v2
  with:
    bun-version: latest

- run: bun install --frozen-lockfile
- run: bun test
- run: bun run build
```

---

## Multi-Language Reference

| Task | Python (uv) | Go | Rust |
|------|-------------|-----|------|
| Install | `uv sync` | `go mod download` | `cargo fetch` |
| Add pkg | `uv add pkg` | `go get pkg` | `cargo add pkg` |
| Build | `uv run python -m build` | `go build ./...` | `cargo build --release` |
| Test | `uv run pytest` | `go test ./...` | `cargo test` |
| Lint | `uv run ruff check` | `golangci-lint run` | `cargo clippy` |
| Format | `uv run ruff format` | `gofmt -w .` | `cargo fmt` |
| Audit | `uv run pip-audit` | `govulncheck ./...` | `cargo audit` |
| Lock | `uv lock` | `go mod tidy` | `cargo generate-lockfile` |

```yaml
# Python CI with uv
- uses: astral-sh/setup-uv@v4
- run: uv sync --frozen
- run: uv run pytest

# Go CI
- uses: actions/setup-go@v5
  with:
    go-version: '1.23'
- run: go mod download
- run: go test ./...
```

Python: PEP 740 attestations (Sigstore-backed provenance on PyPI) are the Python equivalent of npm Trusted Publishing — use `pypi-publish` action with `id-token: write` for OIDC trusted publishing. Rust: `cargo vet` (Mozilla) and `cargo-deny` are the canonical supply-chain guards; pin `GOFLAGS=-mod=readonly` for Go and `bundle config disable_install_extensions` for Ruby to neutralise install-time scripts after the 2026 BufferZoneCorp sleeper campaign (see SKILL.md never-list).
