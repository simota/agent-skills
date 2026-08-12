# Launch Release Strategies

Purpose: Use this file when you need versioning rules, CHANGELOG and release-note structure, rollback options, rollout defaults, hotfix flow, or release-window guidance.

## Contents

1. Versioning strategies
2. CHANGELOG rules
3. Release notes
4. Rollback options
5. Feature flag strategy
6. Release checklist and Go/No-Go
7. Hotfix workflow
8. Release windows and cadence
9. Git and GitHub commands

## 1. Versioning Strategies

### Semantic Versioning

`MAJOR.MINOR.PATCH`

- `MAJOR`: breaking changes
- `MINOR`: backwards-compatible features
- `PATCH`: backwards-compatible fixes

| Change type | Version bump | Example |
|-------------|--------------|---------|
| Breaking API change | `MAJOR` | `1.4.2 -> 2.0.0` |
| New feature | `MINOR` | `1.4.2 -> 1.5.0` |
| Bug fix | `PATCH` | `1.4.2 -> 1.4.3` |
| Security fix | `PATCH` | `1.4.2 -> 1.4.3` |
| Dependency update | `PATCH` or `MINOR` | depends on impact |
| Documentation only | none | no release bump required |

### Pre-release labels

| Label | Use for |
|-------|---------|
| `alpha` | early development |
| `beta` | feature complete, test-heavy |
| `rc` | release candidate |

Guardrails:

- Keep `rc` windows under `2 weeks`.
- If `alpha` or `beta` exceeds `1 month`, recommend stabilizing or canceling the channel.

### CalVer

Use `CalVer` when time-based releases or continuous delivery make strict SemVer noisy.

Examples:

- `YYYY.MM.DD` -> `2026.03.06`
- `YYYY.MM.MICRO` -> `2026.03.3`
- `YY.MM` -> `26.03`

Recommended fit:

| Project type | Preferred strategy |
|--------------|--------------------|
| OSS library | SemVer |
| SaaS with frequent deployment | CalVer or automated build numbering |
| Mobile app | SemVer plus build number |
| Internal tool | CalVer |
| Public API | URI/API version + SemVer |

## 2. CHANGELOG Rules

Use Keep a Changelog categories:

| Category | Use for |
|----------|---------|
| `Added` | new features |
| `Changed` | behavior changes |
| `Deprecated` | soon-to-be removed features |
| `Removed` | removed behavior |
| `Fixed` | bug fixes |
| `Security` | security work |

Commit mapping:

| Commit type | CHANGELOG category |
|-------------|--------------------|
| `feat` | `Added` |
| `fix` | `Fixed` |
| `security` | `Security` |
| `perf` | `Changed` |
| `refactor` | `Changed` |
| `deprecate` | `Deprecated` |
| `remove` | `Removed` |
| `docs` | skip unless user-facing and significant |
| `chore` | skip |
| `test` | skip |
| `ci` | skip |

## 3. Release Notes

Release notes are user-facing. CHANGELOG is developer-facing.

| Aspect | Release notes | CHANGELOG |
|--------|---------------|-----------|
| Audience | end users / stakeholders | developers |
| Tone | plain language | technical |
| Focus | benefits and impact | exact change list |
| Timing | per release | continuous record |

Minimum release notes content:

- release version and date
- highlights
- user-visible changes
- fixes and security changes worth calling out
- migration / caution notes if relevant

## 4. Rollback Options

Default rollback trigger:

- `error_rate > 5% for 5 minutes`

Preferred rollback methods:

| Method | Typical command shape | Time | Risk |
|--------|------------------------|------|------|
| Disable feature flag | API or dashboard toggle | `< 1 minute` | Low |
| Roll back deployment | `kubectl rollout undo ...` | `2-5 minutes` | Low |
| Revert config | config rollback | `1-3 minutes` | Low |
| Reverse DB migration | migration rollback | `5-15 minutes` | Medium |
| Restore backup | backup / restore | `15-60 minutes` | High |

Post-rollback actions:

- notify stakeholders
- create incident record
- schedule postmortem
- tag or document the rolled-back version

## 5. Feature Flag Strategy

### Flag types

| Type | Purpose | Example |
|------|---------|---------|
| `Release Flag` | hide incomplete features | `enable-new-checkout` |
| `Ops Flag` | emergency switch / circuit breaker | `disable-cache-v2` |
| `Experiment Flag` | controlled test | `pricing-v3-experiment` |
| `Permission Flag` | user segmentation | `beta-users-only` |

### Rollout default

`5% -> 25% -> 50% -> 100%`

Minimum rollout requirements:

- canary size at least `5%`
- canary duration at least `24 hours`
- explicit success criteria
- explicit rollback conditions

### Flag lifecycle

| Phase | Required fields |
|-------|-----------------|
| `CREATE` | owner, purpose, type, expiry, fallback, cleanup ticket |
| `ROLLOUT` | stages, success criteria, rollback trigger |
| `STABLE` | 100% reached, side effects checked, metrics stable |
| `CLEANUP` | code removal PR created, tests updated |
| `REMOVED` | code and flag-service cleanup complete |

## 6. Release Checklist And Go/No-Go

Minimum gate set:

- all relevant tests passing
- security scan passing
- staging verification complete
- rollback plan available
- CHANGELOG complete
- stakeholder approval if required
- on-call or incident coverage ready
- release window acceptable
- code coverage `> 80%`

Go/No-Go logic:

- `GO` only if all mandatory gates pass
- `NO-GO` if any mandatory blocker remains
- preferred gates can warn, but do not override mandatory blockers

## 7. Hotfix Workflow

Use a hotfix when production impact is critical and waiting for the next planned release is unacceptable.

Typical flow:

1. Create a hotfix branch from the affected release tag.
2. Apply the smallest possible fix.
3. Get expedited review.
4. Deploy with reduced ceremony but not without rollback.
5. Tag the hotfix.
6. Cherry-pick or merge the fix back to the mainline.

Suggested branch naming:

- `hotfix/v1.2.1`

## 8. Release Windows And Cadence

Preferred windows:

- Tuesday to Thursday
- business hours with support coverage

Avoid:

- Friday releases without explicit approval
- low-staff windows
- major freeze periods without approval

Cadence rule:

- Prefer at least one release per week to avoid oversized batches.

## 9. Git And GitHub Commands

### Release branch

```bash
git checkout -b release/v1.2.0 main
```

### Hotfix from tag

```bash
git checkout -b hotfix/v1.2.1 v1.2.0
```

### CHANGELOG input

```bash
git log v1.1.0..HEAD --oneline --no-merges
```

### Release creation

```bash
gh release create v1.2.0 --notes-file releases/v1.2.0.md
```


---

## Critical Decision Rules Long Form (SKILL.md excerpt)

| Area | Rule |
|---|---|
| Go/No-Go | Use a scored checklist (each criterion 1.0 = met, 0.5 = partial, 0 = unmet; threshold ≥ 80%). Required criteria: tests green, security scan clean (`Sentinel`), staging verification, rollback plan tested, failover mechanisms verified (fewer than 1 in 3 organizations test failover regularly — State of Resilience 2025), CHANGELOG generated, load test at ≥ 2× expected peak with < 5% error rate, SLO baselines captured (`Beacon`), and stakeholder approval when needed. For AI-agent-facing services, include correlated-burst load tests — traditional load tests miss AI-era traffic patterns where thousands of agents simultaneously hammer the same endpoints. Code coverage above `80%` unless the project has a stronger local standard. Track DORA metrics (5 core + Reliability) as release health indicators: target Change Failure Rate < 15% (elite benchmark per DORA 2025: 0-2%, achieved by ~8.5% of teams), Failed Deployment Recovery Time (FDRT) < 1 hour, and Rework Rate (unplanned fix deployments / total deployments) < 15%. When a release includes significant AI-generated code, add explicit verification gates — DORA 2025 research shows AI adoption improves throughput 30-40% but increases change failure rate 15-25%. |
| Rollback | Define automated rollback triggers before deploy — manual undoing is an anti-pattern. Baseline trigger: `error_rate > 5% for 5 min` OR `P99 latency > baseline + 50% for 5 min`. Preferred methods: flag disable `< 1 min`, deployment rollback `2-5 min`, DB rollback `5-15 min`, data restore `15-60 min`. Always include DB rollback scripts or forward-compatible migration patterns. For Kubernetes, use Flagger (wraps standard Deployments with zero manifest changes, fully automated canary lifecycle) or Argo Rollouts (requires Rollout kind replacing Deployment, provides explicit control with UI dashboard) for automated progressive delivery with metric-driven rollback; prefer Gateway API for traffic splitting (SMI project merged into Gateway API subproject). Conduct rollback drills quarterly or before major releases. |
| Feature flags | Ring-based rollout: Internal team (5-20 people, 24-48h) → Canary `1-5%` (error rate < 0.1%) → Beta `10-25%` (user feedback) → GA `100%` (7-day stability). Minimum canary duration `24 hours`. Nesting depth `1`. Approval if active flags exceed `50`. Stale release flag cleanup after `60 days`. Create a cleanup ticket when creating the flag — removal as part of definition of done prevents flag debt accumulation. Define success metrics before enabling each flag. Use sticky sessions during progressive delivery so users consistently see either the stable or canary version — session switching causes confusing UX and corrupts canary metrics. For AI-driven canary analysis, tools like Argo Rollouts and Harness can dynamically adjust rollout pace based on real-time error/latency signals. |
