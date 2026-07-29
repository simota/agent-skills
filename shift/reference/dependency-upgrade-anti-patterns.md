# Dependency Upgrade Anti-Patterns

> Failure patterns in npm/Node.js dependency upgrades, version-management traps, and best practices for update strategy

## 1. The 7 Major Dependency Upgrade Anti-Patterns

| # | Anti-Pattern | Problem | Symptoms | Countermeasure |
|---|-------------|------|------|------|
| **DU-01** | **All-at-Once** | Updating multiple major versions simultaneously | Unresolvable dependency conflicts, undebuggable failures | Batch patch/minor updates together; commit each major update individually |
| **DU-02** | **Changelog Skip** | Bumping versions without checking Breaking Changes | Integration failures, unexpected API changes, runtime errors | Always review the "Breaking Changes" section of GitHub Releases |
| **DU-03** | **Version Drift** | A large gap accumulates from going long periods without updating | Latest libraries don't run on Node 16, an "Upgrade Cliff" forms | Regular small updates; use Renovate/Dependabot |
| **DU-04** | **Legacy Peer Deps Abuse** | Ignoring peer dependency conflicts with `--legacy-peer-deps` | Runtime errors, unexpected behavior, root causes left unaddressed | Use only as a temporary workaround; prioritize a proper fix |
| **DU-05** | **Binary Breakage Blindness** | Ignoring native module breakage on a Node major version change | Image-processing/crypto tools misbehave, build failures | Remove node_modules + lockfile → reinstall, verify C++ addons |
| **DU-06** | **Manual Version Editing** | Manually rewriting version numbers in package.json | Typos, inconsistency with the lockfile, wrong version ranges | Use an interactive tool such as `pnpm update -i` / `npx ncu -i` |
| **DU-07** | **Ambiguous Versioning** | Allowing wide version ranges with `^` or `*` | Different versions installed across environments, unreproducible bugs | Commit the lockfile; pin versions strictly for production |

---

## 2. Update Strategy Framework

```
Staged update procedure:

  Step 1: Batch patch/minor updates
    → Apply all Green/Yellow (patch/minor) updates
    → Run tests → single commit
    → "chore: update non-breaking dependencies"

  Step 2: Update major versions individually
    → Update one package's major version at a time
    → Review the changelog's Breaking Changes
    → Run tests → commit each package separately

  Step 3: Replace deprecated packages
    → Split into a separate ticket (don't mix into a maintenance PR)
    → Research alternative libraries → PoC → phased migration

  Step 4: Update the Node.js runtime
    → Migrate to an LTS version
    → Declare the minimum version in the engines field
    → Verify native module behavior

  Automation:
    → Renovate Bot: auto-merge patches, open PRs for majors
    → Dependabot: automatic PRs for security updates
    → Dependency update tests in the CI pipeline
```

---

## 3. SemVer Decision Criteria

```
What version numbers mean and how to respond:

  PATCH (x.y.Z):
    → Bug fixes, security patches
    → Usually safe, backward compatible
    → Response: can auto-merge

  MINOR (x.Y.z):
    → New features added, backward compatibility maintained
    → Response: merge after running tests

  MAJOR (X.y.z):
    → Intentional Breaking Changes
    → API changes, removals, behavior changes
    → Response: review changelog → fix code → test → commit individually

  ⚠️ Note: SemVer is a "promise," not a "guarantee"
    → Even a minor bump can include a breaking change
    → Updating without tests is always a risk
```

---

## 4. Dependency Lock Strategy

```
Lockfile management best practices:

  Required:
    □ Commit package-lock.json / pnpm-lock.yaml / yarn.lock
    □ Install from the lockfile in CI (npm ci / pnpm install --frozen-lockfile)
    □ Guarantee the same dependency tree across environments

  Private repositories:
    → Leverage an internal package repository
    → "A protective layer against arbitrary dependency upgrades"
    → Prevents unexpected behavior changes when promoting to production

  engines field:
    → Declare the minimum Node.js/pnpm version in package.json
    → Auto-verify in CI/CD
    → Keep the whole team's environments aligned
```

---

## 5. Integration with `detect`

```
Usage within `detect`:
  1. Screen for DU-01 through DU-07 during the ASSESS phase
  2. Run regular audits in coordination with dependency-health-scan.md
  3. Apply the staged update strategy during the PREPARE phase
  4. Submit the update report during the COMPLETE phase

Quality gates:
  - Batch major update → split into individual updates (prevents DU-01)
  - Changelog not reviewed → Breaking Changes review required (prevents DU-02)
  - Long unupdated → set a regular update cycle (prevents DU-03)
  - `--legacy-peer-deps` used → a root-cause fix plan is required (prevents DU-04)
  - Node version change → native module verification (prevents DU-05)
  - Lockfile not committed → committing must be enforced (prevents DU-07)
```

**Source:** [DEV.to: Updating Node Dependencies - The 2025 Survival Guide](https://dev.to/sarveshh/updating-node-dependencies-the-2025-survival-guide-1ge4) · [ButterCMS: Strategies for Keeping Dependencies Updated](https://buttercms.com/blog/strategies-for-keeping-your-packages-and-dependencies-updated/) · [4markdown: Full Tutorial on Updating Dependencies](https://4markdown.com/full-tutorial-on-updating-dependencies-in-js-projects/) · [freeCodeCamp: How to Update NPM Dependencies](https://www.freecodecamp.org/news/how-to-update-npm-dependencies/)
