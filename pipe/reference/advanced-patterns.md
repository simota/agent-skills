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
