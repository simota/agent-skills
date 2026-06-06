# GitHub Actions Secret Architecture

Purpose: Design the secret surface so the workflow runs with the least privilege for the shortest time, and so code cannot leak secrets — even from fork PRs. Prefer OIDC over long-lived credentials; prefer environment secrets over repo secrets; never expose secrets to untrusted code.

## Scope Boundary

- **Pipe `secret`**: GitHub Actions secret surface — OIDC federation, env vs repo secrets, `vars` vs `secrets`, `::add-mask::`, `pull_request` vs `pull_request_target` fork-PR isolation, reusable-workflow secret scoping.
- **Gear `secret`**: application-layer secret management — Vault, AWS Secrets Manager, Doppler, sealed-secrets, SOPS, runtime secret rotation. Complementary: Pipe `secret` delivers the **short-lived cloud token** to the runner; Gear `secret` is where the app reads database passwords and API keys at runtime.
- **Sentinel**: static code scanning for hardcoded secrets. Complementary: Pipe `secret` designs the architecture so secrets never need to be in code; Sentinel catches the cases where a developer pasted one anyway.

## OIDC Federation (Preferred)

GitHub mints a short-lived OIDC token per job. The cloud provider's IAM exchanges it for short-lived credentials scoped to a specific trust policy. No long-lived cloud keys in repo secrets.

### AWS

```yaml
permissions:
  id-token: write     # required to mint OIDC token
  contents: read

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::111122223333:role/gha-deploy
          aws-region: us-east-1
```

Trust policy condition example (scope to repo, branch, environment):

```json
"StringLike": {
  "token.actions.githubusercontent.com:sub":
    "repo:myorg/myrepo:environment:production"
}
```

### GCP

```yaml
- uses: google-github-actions/auth@v2
  with:
    workload_identity_provider: projects/123/locations/global/workloadIdentityPools/gha/providers/github
    service_account: gha@project.iam.gserviceaccount.com
```

### Azure

```yaml
- uses: azure/login@v2
  with:
    client-id: ${{ secrets.AZURE_CLIENT_ID }}
    tenant-id: ${{ secrets.AZURE_TENANT_ID }}
    subscription-id: ${{ secrets.AZURE_SUBSCRIPTION_ID }}
```

Azure federated credentials are configured per subject (repo, branch, or environment) — no client secret stored in GitHub.

### OIDC Custom Property Claims

Embed repo custom properties (`team`, `tier`, `data-classification`) into the OIDC token `sub` claim. Cloud trust policies can scope to properties instead of per-repo configuration — one IAM role covers all `team:payments` repos.

## Environment Secrets vs Repo Secrets

| Scope | Use for | Protection |
|-------|---------|------------|
| Repository secret | Non-prod tokens, shared CI tooling | Available to any workflow in the repo |
| Environment secret | Prod deploy credentials, signing keys | Reviewer gates, branch policies, wait timers |
| Organization secret | Shared registry tokens, code-signing certs | Scoped to selected repos |

Rule: anything that touches prod → environment secret behind an environment with reviewers and branch policy. Repo secrets are effectively "any committer can run a workflow that uses them."

Environment config:

```yaml
jobs:
  deploy-prod:
    environment:
      name: production
      url: https://app.example.com
    runs-on: ubuntu-latest
    steps:
      - run: echo "token=${{ secrets.PROD_API_TOKEN }}"
```

`deployment: false` on environments (GA March 2026) lets you gate non-deploy jobs (approval-only, secret-scoping) without polluting deployment history.

## `vars` vs `secrets`

| Context | Use for | Masked? |
|---------|---------|---------|
| `secrets.*` | Sensitive — tokens, keys, passwords, signing material | Yes (automatically masked in logs) |
| `vars.*` | Non-sensitive — AWS region, service name, API base URL, feature flags | No |

Never stuff configuration into `secrets` to "hide" it — masking adds noise (every occurrence replaced by `***`) and doesn't provide real secrecy. Use `vars` for config, `secrets` only for sensitive material.

```yaml
env:
  AWS_REGION: ${{ vars.AWS_REGION }}
  SERVICE_NAME: ${{ vars.SERVICE_NAME }}
  API_TOKEN: ${{ secrets.API_TOKEN }}
```

## Secret Masking

All `secrets.*` values are masked automatically. For **runtime-derived** sensitive values (a token fetched from Vault mid-job, an OIDC-exchanged credential), mask explicitly:

```yaml
- run: |
    TOKEN=$(vault read -field=token secret/gha/deploy)
    echo "::add-mask::$TOKEN"
    echo "TOKEN=$TOKEN" >> $GITHUB_ENV
```

Masking is string-substitution on log output — it does not hide values from downstream steps, artifacts, or scripts that re-emit them. Never `echo $SECRET` "to debug" — structured masking can still leak through base64 encoding, split characters across lines, or JSON formatting.

## Fork-PR Secret Isolation

`pull_request` from a fork runs **without secrets** — GitHub deliberately withholds them so untrusted fork code cannot exfiltrate. This is the correct safety default.

`pull_request_target` runs in the **base repo context with full secrets**, but checks out the **base ref by default**, not the PR head. This is the dangerous pair: if you add `ref: ${{ github.event.pull_request.head.sha }}` to checkout and then run any fork code (tests, linters, build), you have granted the forker arbitrary code execution with your repo's secrets.

**Rule:** `pull_request_target` may inspect metadata (labels, author, title, comments, changed-file list) and run trusted automation, but must never execute fork code.

Safe `pull_request_target` pattern (label-gated run of trusted code):

```yaml
on:
  pull_request_target:
    types: [labeled]

jobs:
  trusted-check:
    if: github.event.label.name == 'safe-to-run'
    runs-on: ubuntu-latest
    permissions:
      pull-requests: write
    steps:
      - uses: actions/checkout@v4
        # checks out base ref — does NOT use head.sha
      - run: ./trusted-script.sh "${{ github.event.pull_request.number }}"
```

CVE history — `pull_request_target` misuse was the root cause of multiple 2024-2025 supply chain incidents (Shai Hulud, HackerBot-CLAW, plus the 2024 tj-actions/changed-files incident). Treat every addition of this trigger as an ask-first decision.

## `GITHUB_TOKEN` Permissions

`GITHUB_TOKEN` is an auto-generated, job-scoped token. Treat it as a secret surface:

```yaml
permissions: {}          # top-level baseline: zero scopes

jobs:
  test:
    permissions:
      contents: read     # grant only what this job needs
    ...
  release:
    permissions:
      contents: write    # explicit, scoped to the one job that needs it
      id-token: write
```

Org baseline: set `GITHUB_TOKEN` default to **read-only** at org level, grant write per-job. A compromised third-party action with `permissions: write-all` inherits the blast radius of every scope.

## Reusable Workflow Secret Scoping

Implicit `secrets: inherit` passes all caller secrets into the reusable workflow — breaks least privilege. Prefer explicit scoping:

```yaml
jobs:
  deploy:
    uses: ./.github/workflows/reusable-deploy.yml
    secrets:
      DEPLOY_TOKEN: ${{ secrets.PROD_DEPLOY_TOKEN }}
      SIGNING_KEY: ${{ secrets.RELEASE_SIGNING_KEY }}
```

2026 roadmap: scoped secrets replace implicit inheritance entirely. Plan migration now.

## Anti-Patterns

- `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY` stored as repo secrets when OIDC is available.
- `pull_request_target` with `checkout ref: ${{ github.event.pull_request.head.sha }}` — fork code + base secrets = RCE.
- `echo ${{ secrets.TOKEN }}` "for debugging" — logs even with masking can leak via artifact upload, error messages, split characters.
- `secrets: inherit` on reusable workflows used by untrusted callers.
- Storing config in secrets just to hide it from curious eyes — use `vars`.
- Long-lived cloud credentials rotated "annually" — OIDC tokens are minutes-long.
- Granting `permissions: write-all` as a shortcut — expands blast radius to every scope.

## Citations

- GitHub Docs — About security hardening with OpenID Connect
- GitHub Docs — Configuring OpenID Connect in cloud providers (AWS / GCP / Azure)
- GitHub Docs — `pull_request_target` event security considerations
- GitHub Docs — `GITHUB_TOKEN` permissions
- GitHub Docs — Secrets in fork pull requests (withheld from `pull_request`, available to `pull_request_target`)
- GitHub Docs — `actions/cache` (for cache-key caveats referenced by `cache` recipe)
