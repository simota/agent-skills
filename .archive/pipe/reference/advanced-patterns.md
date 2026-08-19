# Advanced Patterns

Purpose: Cover monorepo CI, self-hosted runners, multi-platform builds, advanced deployment flows, service containers, and deep workflow debugging.

## Contents

- Monorepo CI
- Self-hosted runners
- Multi-platform builds
- Deployment patterns
- Service containers
- Debugging
- Expressions and functions

## Monorepo CI

Workflow-level `paths` filters are not enough for job-level routing in a monorepo.

| Need | Preferred tool or pattern |
|------|---------------------------|
| Job-level file routing | `dorny/paths-filter` |
| Dependency-aware package routing | `nx affected` or `turbo --filter` |
| Required checks with selective execution | always-run `ci-gate` job |
| Team/package ownership separation | split workflows by package or domain when logic becomes hard to follow |

Safe default:

- detect changed areas first
- run only affected jobs
- keep one always-reporting gate for required checks

## Self-Hosted Runners

Use self-hosted runners only when GitHub-hosted runners cannot satisfy networking, hardware, or compliance constraints.

Rules:

- prefer ephemeral runners
- prefer ARC for elastic scale
- use explicit labels and runner groups
- never use self-hosted runners for public repositories
- rebuild runner images regularly

## Multi-Platform Builds

- Use `docker/setup-qemu-action` and `docker/setup-buildx-action` for multi-arch image builds.
- Keep full OS matrices for PRs, release, or nightly flows, not every push.
- Prefer Ubuntu by default and add Windows/macOS only when required by the product surface.

## Deployment Patterns

| Pattern | Use it when | Guardrail |
|---------|-------------|-----------|
| Rolling | low-risk stateless services | keep health checks and concurrency |
| Blue-green | fast cutover with strong rollback need | keep old environment ready until verification passes |
| Canary | production validation on a small slice | define rollback trigger and evaluation window |
| Manual rollback | previous artifact or config restore | use controlled `workflow_dispatch` |

Deployment rules:

- protect environments with reviewers
- do not cancel active production deploys automatically
- keep rollback entry points explicit

## Service Containers

Use service containers for fast integration tests when the dependency can be expressed locally.

Checklist:

- pin service images
- add health checks
- isolate credentials
- use them only in jobs that need them

## Debugging

| Tool | Use it for |
|------|-------------|
| `actionlint` | YAML, expression, and workflow static validation |
| `act` | local workflow smoke tests |
| `ACTIONS_STEP_DEBUG` / `ACTIONS_RUNNER_DEBUG` | temporary deep logs |
| `workflow_dispatch` | safe repro with explicit inputs |

Typical failure classes:

- trigger did not match filters
- required check name mismatch
- hidden dependency on repo secrets or environment
- unsupported `act` behavior for cloud-only or service-heavy jobs

## Expressions And Functions

Useful functions to keep close:

- `success()`
- `failure()`
- `cancelled()`
- `always()`
- `contains()`
- `startsWith()`
- `hashFiles()`
- `fromJSON()`
- `toJSON()`


---

## Critical Decision Rules Long Form (SKILL.md excerpt)

| Decision | Rule |
|---|---|
| Third-party actions | Pin every third-party action to a full SHA. Use Dependabot or Renovate to refresh pins. Prefer org allow-lists with SHA pinning enforcement policy (GA Aug 2025). When available, use `dependencies` section for deterministic transitive locking. GitHub pivoted from immutable actions (OCI/GHCR) to org-level SHA pinning enforcement + immutable releases with stricter publishing requirements. |
| Cloud auth | Prefer OIDC over long-lived cloud credentials. Add `id-token: write` only to jobs that mint cloud tokens. Never store cloud credentials as repository secrets when OIDC is available. Use OIDC custom property claims (repo custom properties embedded in tokens) for granular trust policies — scope cloud roles to specific teams, environments, or project classifications without per-repo configuration. |
| Egress controls | When available, enable egress firewall in monitor mode first. Build allowlists from observed traffic before switching to enforcement. Define allowed domains, IP ranges, and TLS requirements. Egress firewall operates at L7 outside the runner VM — immutable even with root access inside. |
| CI/CD observability | Enable Actions Data Stream for security-critical pipelines. Telemetry correlates to workflow/job/step/command. Route to S3 or Azure Event Hub. Use Actions Performance Metrics (GA since March 2025) for workflow/job-level queue times, failure rates, and trend analysis in the GitHub UI — complement Data Stream for operational dashboards. Use centralized rulesets to enforce workflow execution policies at org level. |
| Runner cost | Default to Ubuntu (4 vCPU/16 GB since Jan 2026 restructure, up to 39% price reduction across all types). Consider ARM when compatible (37% cheaper than x64, free for public repos). Use Windows or macOS only for platform-specific validation. Self-hosted runner platform charge shelved indefinitely. |
| Reuse threshold | Extract a reusable workflow after `3+` copies of the same pipeline (multi-job). Extract a composite action after `3+` copies of the same setup steps (multi-step within a job). Keep `1-2` copies inline. Don't put job orchestration logic into composite actions. Start with local `./.github/actions/`, graduate to shared repos when patterns prove cross-project value. |


## Per-Recipe Behavior Notes (SKILL.md excerpt)

- `workflow`: New workflow skeleton. Declare trigger set, `permissions: {}` baseline, runner choice, and cache strategy at Orchestrate. SHA-pin every third-party action. Validate with `actionlint` before handoff.
- `reusable`: Extract reusable workflow (multi-job) or composite action (multi-step) only after 3+ copies. Version interface via `@vX` tag plus commit SHA. Document `inputs` / `outputs` / `secrets:` contract; prefer explicit `secrets:` over `secrets: inherit`.
- `security`: Harden an existing workflow. Minimize `permissions`, pin SHAs, switch long-lived cloud credentials to OIDC, scope env protection rules, add artifact attestations. Never checkout fork code in `pull_request_target`.
- `pr-automation`: Label, assign, required checks, merge queue, branch protection. Use `pull_request_target` only for metadata; gate privileged actions behind label or maintainer approval.
- `matrix`: Design a matrix build. Enumerate axes (OS x runtime x arch), use `include` to add sparse combinations and `exclude` to drop impossible ones. Set `fail-fast: false` when axes give independent signal. Cap `max-parallel` to bound concurrency. Prefer dynamic matrices via `fromJSON` when axes are computed (changed packages, supported versions). Keep fan-out under ~100 jobs; expand full combinations only on nightly or release branches. Pair with `cache` for per-axis key strategy. For provider-agnostic CI topology, route to Gear `ci`.
- `cache`: Design `actions/cache` layout. Key by `runner.os` + lockfile hash (`hashFiles('**/pnpm-lock.yaml')`); add `restore-keys` for graceful fallback. Cross-OS compatibility: include `runner.arch` for native binaries. Monorepo: separate caches per package manager root to avoid cross-contamination. Track cache-hit telemetry via step output or Data Stream. Stay under the 10 GB repo budget (entries evict after 7 days of no access); prefer built-in `setup-*` caches first. For provider-agnostic CI caching posture, route to Gear `ci`.
- `secret`: Design the GHA secret surface. Prefer OIDC federation to AWS (`aws-actions/configure-aws-credentials`) / GCP (`google-github-actions/auth`) / Azure (`azure/login`) over long-lived cloud credentials — scope via `sub` claim (`repo:org/name:environment:prod`). Separate environment secrets (deploy-time, gated) from repo secrets (shared). Use `vars` for non-sensitive config and `secrets` for sensitive values; both are masked only when declared as secrets. Add `::add-mask::` for runtime-derived sensitive values. Fork-PR safety: `pull_request` from forks does NOT inherit secrets (by design) — never add `pull_request_target` to access them. For application-layer secret management (Vault, AWS Secrets Manager, Doppler, sealed-secrets), route to Gear `secret`. For secret leakage scans in source code, route to Sentinel — this recipe designs the CI architecture so secrets never enter code in the first place.

