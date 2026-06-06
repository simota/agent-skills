# Distribution & Packaging Anti-Patterns

**Purpose:** Failure patterns for binary packaging, package-manager distribution, release safety, and cross-platform delivery.
**Read when:** Shipping a CLI binary, choosing install channels, reviewing release safety, or debugging cross-platform packaging issues.

## Contents

- Seven Binary Distribution Anti-Patterns
- Package-Manager-Specific Traps
- Security Anti-Patterns
- Release and Versioning Anti-Patterns
- Cross-Platform Build Anti-Patterns
- How To Use With Anvil

## 1. Seven Binary Distribution Anti-Patterns

| # | Anti-Pattern | Problem | Signals | Fix |
|---|-------------|---------|---------|-----|
| **DP-01** | **Fat Package** | Bundling binaries for every platform into a single package | `npm install` downloads 100+ MB and `node_modules` bloats quickly | Publish per-platform packages and fetch only the required binary via `optionalDependencies` or equivalent |
| **DP-02** | **postinstall Reliance** | Downloading binaries only in `postinstall` | Locked-down environments disable postinstall hooks; supply-chain risk grows | Use `optionalDependencies` as the primary path and `postinstall` only as a controlled fallback |
| **DP-03** | **No Integrity Check** | Skipping hash verification for downloaded binaries | Binary replacement or MITM attacks can slip through | Verify SHA256 checksums, ship signatures, and provide an SBOM |
| **DP-04** | **Permission Loss** | Losing executable bits during packaging or CI | Users hit `EACCES: permission denied` and need manual `chmod +x` | Set executable permissions explicitly during packaging and validate them in CI |
| **DP-05** | **Single Registry Dependency** | Shipping through only one registry channel | Registry outages or enterprise proxies block installation | Provide multiple channels such as registry + GitHub Releases + Homebrew/Scoop |
| **DP-06** | **No Upgrade Path** | Offering no built-in update guidance | Users stay on stale versions indefinitely | Provide `app update`, version checks, or clear update notifications |
| **DP-07** | **Platform Matrix Gap** | Missing major platform/architecture combinations | Apple Silicon, Windows ARM, or musl targets are unsupported | Cover the core matrix `{linux,darwin,windows} × {amd64,arm64}` in CI |

---

## 2. Package-Manager-Specific Traps

```text
npm distribution traps:
  ❌ optionalDependencies fragility:
    → Users can disable them with `--ignore-optional`
    → Platform detection can fail inside containerized builds
    → Fix: pair `optionalDependencies` with a controlled fallback path

  ❌ postinstall security exposure:
    → `postinstall` can execute arbitrary code and becomes a supply-chain target
    → Security-conscious environments often disable it
    → Fix: keep scripts minimal, verify integrity, and constrain what can execute

  ❌ Moving binaries across `node_modules`:
    → Copying `node_modules` between VMs or containers can mismatch architectures
    → Fix: install dependencies in each target environment

pip/PyPI distribution traps:
  ❌ No wheels:
    → Users must build from source and often fail on native dependencies
    → Fix: ship manylinux / musllinux wheels per platform

  ❌ Weak reproducibility:
    → Builds drift unless dependencies are locked and verified
    → Fix: use `pip freeze`, hashes, and tools such as `pip-tools` or `uv`

Cargo distribution traps:
  ❌ `cargo install` slowness:
    → Full source builds are expensive and include unnecessary work
    → Fix: publish prebuilt binaries via `cargo-binstall` or GitHub Releases

  ❌ Poor upgrade ergonomics:
    → Updating often requires another full build
    → Fix: support cargo-update or direct binary releases

Go distribution traps:
  ❌ `go install @latest` ambiguity:
    → Users install different versions over time and lose reproducibility
    → Fix: document version-pinned installs such as `pkg@v1.2.3`

  ❌ No build-hook escape hatch:
    → Integrating native dependencies via CGO complicates portability
    → Fix: plan cross-compilation, static linking, and CGO constraints explicitly
```

---

## 3. Security Anti-Patterns

| # | Anti-Pattern | Problem | Signals | Fix |
|---|-------------|---------|---------|-----|
| **SC-01** | **Dependency Confusion** | Public packages can shadow private package names | The wrong package installs silently | Use scoped names such as `@org/pkg` and explicit registry configuration |
| **SC-02** | **Unsigned Binaries** | Shipping binaries without code signing | macOS Gatekeeper or Windows SmartScreen warns or blocks installs | Sign releases with Apple Developer ID / Authenticode where appropriate |
| **SC-03** | **No SBOM** | Shipping no software bill of materials | Dependency risk cannot be audited cleanly | Generate and publish CycloneDX or SPDX SBOMs |
| **SC-04** | **Stale Dependencies** | Failing to update known-vulnerable dependencies | Known CVEs remain in shipped releases | Automate updates with Dependabot or Renovate and run regular audits |

---

## 4. Release and Versioning Anti-Patterns

```text
Versioning traps:

  ❌ SemVer Lie:
    → Shipping breaking changes in patch releases
    → Users’ scripts fail after “safe” updates
    → Fix: enforce SemVer and use API-diff checks where possible

  ❌ No Changelog:
    → Users cannot see what changed
    → Upgrades feel risky and opaque
    → Fix: publish a generated `CHANGELOG.md` tied to release automation

  ❌ Breaking Without Migration:
    → Renaming flags or arguments without a migration path
    → CI scripts and shell aliases break unexpectedly
    → Fix: warn, provide a migration window, then remove the deprecated surface

  ❌ No Prerelease Channel:
    → Stable is the only release lane
    → Users cannot test risky changes safely
    → Fix: publish beta/canary channels such as npm dist-tags or GitHub prereleases

  ❌ Tag-Only Release:
    → Creating a Git tag without shipping installable binaries
    → Users must build everything locally
    → Fix: build and upload binaries automatically during release workflows
```

---

## 5. Cross-Platform Build Anti-Patterns

```text
Build matrix traps:

  ❌ CI-Only Build:
    → Cross-platform builds work only in CI
    → Debugging becomes slow and opaque
    → Fix: support local cross-build paths with Docker, cross-rs, zig cc, or equivalent

  ❌ Dynamic Link Trap:
    → Shipping binaries that depend on system glibc or similar shared libraries
    → Users see `GLIBC_2.XX not found`
    → Fix: use musl/static builds or build against sufficiently old base images

  ❌ No Smoke Test:
    → Releasing binaries without execution checks
    → Link or dependency issues ship unnoticed
    → Fix: smoke-test `app --version` and one basic command on every target

  ❌ Architecture Detection Failure:
    → Misdetecting Rosetta or ARM environments
    → Users receive the wrong binary variant
    → Fix: combine `uname -m`, platform checks, and OS-specific probes such as `sysctl`
```

---

## 6. How To Use With Anvil

```text
Use within Anvil:
  1. Review DP-01 to DP-07 during BLUEPRINT to shape the distribution strategy
  2. Review integrity and signing during HARDEN
  3. Review release/versioning ergonomics during PRESENT
  4. Review cross-platform matrix health throughout the workflow

Quality gates:
  - One package ships every platform binary → split by platform (prevent DP-01)
  - `postinstall` is the only fetch path → add a safer fallback strategy (prevent DP-02)
  - Downloaded binaries lack checksum verification → add SHA256 validation (prevent DP-03)
  - Major target platforms are missing → extend the CI matrix (prevent DP-07)
  - Unsigned binaries ship publicly → add code signing (prevent SC-02)
  - Patch releases contain breaking changes → enforce SemVer + API diff checks (prevent SemVer Lie)
  - Dynamically linked Linux binaries ship broadly → evaluate musl/static builds (prevent Dynamic Link Trap)
```

**Source:** [Sentry Engineering: Publishing Binaries on npm](https://sentry.engineering/blog/publishing-binaries-on-npm) · [Andrew Nesbitt: Package Manager Design Tradeoffs](https://nesbitt.io/2025/12/05/package-manager-tradeoffs.html) · [Rust CLI: Packaging](https://rust-cli.github.io/book/tutorial/packaging.html) · [CMU: Reproducible Packaging Study](http://www.cs.cmu.edu/~ckaestne/pdf/icse25_rb.pdf) · [Orhun: Packaging Rust for npm](https://blog.orhun.dev/packaging-rust-for-npm/)
