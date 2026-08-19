# GitHub Actions Security Anti-Patterns

Purpose: Catch workflow-level security failures early: supply-chain compromise, privilege escalation, secret leakage, injection, and runner hardening gaps.

## Contents

- Supply-chain failures
- 2025 incidents
- Permission and secret scope
- Injection failures
- Runner security

## Supply-Chain Failures

| ID | Anti-pattern | Signal | Fix |
|----|--------------|--------|-----|
| `SC-01` | Tag-only pinning | `uses: ...@v4` or any movable tag | pin a full 40-character SHA |
| `SC-02` | No action allow-list | any marketplace action may run | enable org allow-lists and approval policy |
| `SC-03` | No Dependabot for actions | stale vulnerable action refs | enable `github-actions` updates in Dependabot or Renovate |
| `SC-04` | Artifact poisoning | release deploys consume PR-built artifacts | rebuild from trusted mainline or release refs |
| `SC-05` | Unaudited popular actions | popularity replaces security review | fork or review critical actions before trust |
| `SC-06` | No SLSA / Sigstore | no provenance or artifact attestation | add provenance and SBOM attestation |
| `SC-07` | Unverified runner images | self-hosted base image is opaque | use trusted images, rebuild regularly, keep runners ephemeral |

Reference SHA example preserved from the source set:

```yaml
uses: actions/checkout@a5ac7e51b41094c92402da3b24376905380afc29
```

## 2025 Incidents To Remember

- `tj-actions/changed-files` (`CVE-2025-30066`): mutable tags enabled secret theft at scale.
- `reviewdog/action-setup` (`CVE-2025-30154`): showed that multiple ecosystem actions can fail together.
- GhostAction campaign: outbound network exfiltration stole thousands of secrets.
- Nx `pull_request_target` attack: untrusted input in a privileged workflow became code execution.

## Permission And Secret Scope

| ID | Anti-pattern | Signal | Fix |
|----|--------------|--------|-----|
| `PM-01` | `write-all` permissions | workflow can modify the whole repo by default | start from `permissions: {}` and add minimum job scopes |
| `PM-02` | Job-wide secret scope | every step can read the same secret | pass secrets only to the steps that need them |
| `PM-03` | Long-lived cloud credentials | static cloud keys live in GitHub Secrets | use OIDC and short-lived credentials |
| `PM-04` | Secret in log | `echo`, `print`, or debug output leaks tokens | mask and sanitize before logging |
| `PM-05` | No environment protection | prod deploys run without approval gates | add required reviewers, wait timers, and branch restrictions |

## Injection Failures

- Never interpolate `${{ ... }}` directly into shell code when the value is user-controlled.
- Unsafe inputs include PR titles, issue bodies, commit messages, and branch names.
- Do not use `eval` in workflow shell logic.
- Pass hostile inputs through `env:` and quote them.

## Runner Security

| ID | Anti-pattern | Signal | Fix |
|----|--------------|--------|-----|
| `RS-01` | Persistent self-hosted runners | state survives between jobs | use ephemeral runners |
| `RS-02` | Self-hosted runners on public repos | fork code can reach your infrastructure | use GitHub-hosted runners only for public repos |
| `RS-03` | No network egress control | workflows can call arbitrary hosts | add `step-security/harden-runner` or equivalent controls |
| `RS-04` | Docker socket exposure | containers can control the host | avoid exposing the Docker socket; prefer rootless or isolated builders |
