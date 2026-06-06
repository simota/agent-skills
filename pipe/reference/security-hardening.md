# Security Hardening

Purpose: Secure GitHub Actions workflows against supply-chain compromise, privilege escalation, script injection, and secret exfiltration.

## Contents

- Threat model
- Permission model
- SHA pinning
- Safe scripting
- OIDC
- Supply-chain defenses
- 2026 security roadmap (preview / roadmap features)
- Governance checklist

## Threat Model

| Threat | Typical failure | Primary defense |
|--------|------------------|-----------------|
| Supply-chain attack | compromised third-party action executes malicious code | full SHA pinning, allow-lists, automated updates |
| Script injection | untrusted event data interpolated into `run:` | pass untrusted values via `env:` and quote them |
| Secret exfiltration | secrets leaked to logs, artifacts, or outbound traffic | minimal secret scope, masking, egress monitoring |
| Privilege escalation | default or excessive workflow permissions | `permissions: {}` and job-level grants |
| Fork PR abuse | `pull_request_target` runs fork code with secrets | never checkout untrusted fork code in `pull_request_target` |

## Permission Model

Default to zero permissions at the workflow level, then grant the minimum required at job level. Since Feb 2023, the platform default for `GITHUB_TOKEN` in new orgs/enterprises is read-only — explicitly write `permissions: {}` at the top of every workflow so that policy is durable when defaults change.

```yaml
permissions: {}

jobs:
  test:
    permissions:
      contents: read
```

Common grants:

| Need | Permission |
|------|------------|
| Read repo contents | `contents: read` |
| Post PR comments or labels | `pull-requests: write` |
| Upload SARIF | `security-events: write` |
| Mint cloud identity via OIDC | `id-token: write` |
| Push artifact attestations | `attestations: write` |

Never use `permissions: write-all`.

Upcoming separation (2026 roadmap): write access to a repository will no longer grant secret management permissions. Plan to move secret rotation responsibilities to a dedicated custom role before scoped secrets reach GA.

## SHA Pinning

- Pin every third-party action to a full commit SHA.
- Tags are mutable. SHAs are immutable.
- Update pins with Dependabot or Renovate.
- Add a trailing `# v<x.y.z>` comment so reviewers and renovate bots can match SHAs to human-readable versions.

```yaml
# Bad
- uses: actions/checkout@v6

# Good
- uses: actions/checkout@<full-40-char-sha>   # v6.0.2
```

Enforce centrally (GA Aug 2025): the GitHub Actions "allowed actions and reusable workflows" policy now ships a SHA-pinning enforcement checkbox at enterprise, organization, and repository levels, plus a blocklist syntax (`!owner/action`) evaluated last so a compromised dependency can be killed in seconds. The policy walks the full dependency tree, including transitive sub-actions individual workflows cannot control.

The 2026 roadmap extends this with **workflow dependency locking** — a `dependencies:` section in workflow YAML that pins every direct and transitive action by SHA, reviewable via PR diff like `go.sum`. Target: public preview within 3-6 months of the March 2026 announcement, GA roughly 6 months out. Adopt it as soon as it ships and stop relying on best-effort SHA pinning of top-level actions only.

If you inherit legacy config such as `aquasecurity/trivy-action@master`, treat it as technical debt and replace it with a full SHA pin before trusting the workflow.

## Safe Scripting

Treat PR titles, branch names, issue bodies, and commit messages as hostile input.

Bad:

```yaml
- run: echo "${{ github.event.pull_request.title }}"
```

Good:

```yaml
- env:
    PR_TITLE: ${{ github.event.pull_request.title }}
  run: printf '%s\n' "$PR_TITLE"
```

Rules:

- never interpolate untrusted data directly inside shell code
- avoid `eval`
- quote variables
- mask secrets before any diagnostic logging

## OIDC Over Long-Lived Secrets

Prefer workload identity federation to stored cloud keys.

| Cloud | Common action | Notes |
|------|----------------|------|
| AWS | `aws-actions/configure-aws-credentials` | use `role-to-assume` and repository/branch trust conditions |
| GCP | `google-github-actions/auth` | constrain workload identity pool bindings |
| Azure | `azure/login` | scope federated credentials tightly |
| Vault | platform-specific OIDC login | bind claims to repo, ref, and environment |

Grant `id-token: write` only to jobs that actually mint cloud credentials. Always pin the `audience` to a deployment-target-specific value and verify it server-side — generic audiences are the foothold most fork-PR token theft attacks rely on.

**Repository custom property claims (GA April 2026):** OIDC tokens now embed any custom property assigned to the repository (prefixed `repo_property_<key>`). Use this to write attribute-based trust policies (`repo_property_environment: prod`, `repo_property_team: payments`) once at the cloud provider and stop maintaining repo-name allowlists. Configure which properties appear in tokens from the OIDC settings page at repo / org / enterprise level.

**Immutable subject claims (April 2026):** newer subject claim shapes are stable and will not silently change for a given (repo, ref, environment) tuple, so trust policies pinned to `repo:org/name:environment:prod` remain reliable across platform updates. Pin `sub`, not just `repository`.

## Supply-Chain Defenses

Recommended controls (always pin to a SHA; version tags below are for readability only):

| Control | Example |
|---------|---------|
| Runner egress monitoring | `step-security/harden-runner@v2` |
| Build provenance | `actions/attest-build-provenance@v2` |
| SBOM generation | `anchore/sbom-action@v0` |
| SBOM attestation | `actions/attest-sbom@v1` |
| Secret scanning | `gitleaks/gitleaks-action@v2` |
| Scorecard | weekly OpenSSF Scorecard run |
| SARIF upload | `github/codeql-action/upload-sarif@v3` |
| Allowed Actions policy + SHA-pin enforcement | org settings → Actions → Policies (GA Aug 2025) |

Verify attestations at consumption time with `gh attestation verify <artifact> --repo <owner>/<repo>` (or the equivalent OCI command). Generating attestations without anyone verifying them is theater.

Real incidents to keep in mind:

- `tj-actions/changed-files` (CVE-2025-30066, March 2025): every tag was force-pushed to a malicious commit that scraped runner memory for secrets. Repos pinning to a SHA were unaffected.
- `reviewdog/action-setup` (CVE-2025-30154, March 2025): chained compromise that enabled the tj-actions intrusion.
- `aquasecurity/trivy-action` + `setup-trivy` (TeamPCP, March 2026): 76 of 77 tags and all 7 `setup-trivy` tags rewritten in one push; lateral spread to Checkmarx KICS, LiteLLM, and Telnyx Actions.
- Bitwarden CLI npm + Trivy compromises (TeamPCP, March-April 2026): same operator targeting build-tooling supply chain.
- Shai-Hulud waves (Sept 2025 / Nov 2025 "Second Coming" / Shai-Hulud 3.0 "Golden Path"): self-replicating worm that abused `pull_request_target` and stolen npm tokens; 3.0 drops the dead-man switch and bootstraps Bun via `bun_installer.js` at install time.
- Mini Shai-Hulud / SAP CAP (April 29 2026, ~2h19m window): CircleCI `cloudmtabot` token chained with GHA OIDC extraction to publish `@cap-js/sqlite@2.2.2`, `@cap-js/postgres@2.2.2`, `@cap-js/db-service@2.10.1`, `mbt@1.2.48`. IOC: a new `.github/workflows/discussion.yaml`, a self-hosted runner named `SHA1HULUD`, and commits prefixed `OhNoWhatsGoingOnWithGitHub:[Base64]`.
- Mini Shai-Hulud TanStack wave (May 11 2026): 84 npm artifacts across 42 `@tanstack/*` packages; attacker forked the repo, opened a PR that triggered a `pull_request_target` workflow, poisoned the Actions cache with malicious binaries, and exfiltrated OIDC tokens from runner memory.
- PhantomRaven 2nd-4th waves (Nov 2025 - Feb 2026, 88 packages): Remote Dynamic Dependencies (RDD) — an HTTP URL declared as a dependency, fetched and executed during `npm install`. Counter with `npm config set ignore-scripts true` and rejecting non-registry URLs in any dep field.
- GhostAction secret-exfiltration campaign + Nx-style `pull_request_target` + unsanitized-input attacks remain active templates.

## 2026 Security Roadmap (Preview / Roadmap Features)

GitHub announced a five-pillar Actions security roadmap in March 2026. Adopt these as they leave preview; design new workflows so adoption is a config flip, not a rewrite.

| Pillar | Status (May 2026) | What it gives you |
|--------|--------------------|-------------------|
| Workflow dependency locking (`dependencies:`) | Roadmap → public preview within 3-6 mo | go.sum-style SHA lockfile covering direct + transitive actions, reviewable in PR diff |
| Policy-driven execution controls | Roadmap → public preview within 3-6 mo | Ruleset-based controls over who can trigger workflows and which events are permitted; "evaluate" mode to dry-run policies |
| Scoped secrets | Roadmap → public preview within 3-6 mo | Secrets bound to specific repos / branches / environments / reusable workflows; ends implicit inheritance |
| Native egress firewall | Roadmap → public preview within 6-9 mo | L7 firewall outside the runner VM, immutable from inside; monitor mode first, then enforce allowlists |
| Immutable releases (action publishing) | Future / no timeline | Stricter publishing requirements so tags cannot be silently force-pushed |
| Actions Data Stream | Roadmap → public preview within 3-6 mo, GA 6-9 mo | Near real-time telemetry to S3 / Azure Event Hub correlated per workflow / job / step |

Operational guidance:
- Turn on the egress firewall in **monitor mode** first, harvest the allowlist from a 2-week observed-traffic sample, then flip to enforcement.
- Treat scoped secrets as the end of `secrets: inherit` in reusable workflows. Refactor callees to declare an explicit `secrets:` block now so the migration is non-breaking.
- Wire Data Stream into the same SIEM that consumes cloud audit logs; correlate OIDC `sub` claims with runner-side step telemetry to catch token theft within minutes.

## Governance Checklist

- all third-party actions are SHA-pinned
- org-level "require SHA pinning" policy is enabled (GA Aug 2025)
- Dependabot or Renovate updates GitHub Actions dependencies
- workflow defaults to read-only or empty permissions (`permissions: {}` at top)
- `actionlint` (and `zizmor` if you maintain a large fleet) runs in CI for `.github/workflows/`
- GitHub code scanning is enabled for Actions workflows (flags injection / privilege-escalation patterns automatically)
- no secrets are printed, echoed, or stored in artifacts
- `pull_request_target` never checks out untrusted fork code
- `npm config set ignore-scripts true` (or `pnpm install --ignore-scripts` / `yarn install --ignore-scripts`) is the default install step; non-registry HTTP URLs in any dep field are rejected
- runners never see preinstall / postinstall hooks from untrusted packages unless explicitly allowlisted
- deploy jobs use environment protection and concurrency
- CODEOWNERS includes `.github/workflows/`
- org allow-list or approval policy exists for actions
- OIDC is preferred over long-lived cloud secrets; `audience` is pinned to a target-specific value
- artifact attestations are generated for release artifacts and verified at consumption (`gh attestation verify`)
- Scorecard, secret scanning, and provenance are enabled where appropriate
