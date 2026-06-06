# Branching Strategies

Purpose: Choose the branch workflow that matches team size, release model, CI maturity, and feature-flag capability.

## Contents

- Strategy comparison
- Selection guide
- Feature flags vs feature branches
- Naming guidance
- Anti-patterns

## Strategy Comparison

| Factor | Trunk-Based | GitHub Flow | Git Flow |
|--------|-------------|-------------|----------|
| Branch lifetime | hours to `1-2` days | a few days | days to weeks |
| Branch count | minimal | low | high |
| Release model | continuous deployment | merge to `main` drives deployment | release-branch based |
| Team size fit | any mature team | small to medium | medium to large |
| Complexity | low | low to medium | high |
| Best fit | SaaS, web, internal apps | SaaS, web, service repos | versioned products, multi-version support |

## Selection Guide

Use:
- `Trunk-Based` when CI/CD is mature, feature flags exist, and the team can keep branches short-lived.
- `GitHub Flow` when simplicity matters more than release-branch ceremony.
- `Git Flow` when you must support parallel versions or hotfixes with explicit release branches.

### Prerequisites for Trunk-Based

- strong CI/CD pipeline
- feature-flag infrastructure
- consistent code review culture
- reliable automated test coverage

### When Git Flow Is Justified

- predictable, scheduled release cycles
- concurrent support of multiple released versions
- separate hotfix handling is operationally required

## Feature Flags vs Feature Branches

| Factor | Feature Branches | Feature Flags |
|--------|------------------|---------------|
| Isolation method | Git branch | runtime gating |
| Deployability | after merge | before exposure |
| A/B testing | weak | strong |
| Merge-conflict risk | increases with branch age | none from branching itself |
| Debt type | branch cleanup | stale-flag cleanup |

Recommended default for 2025-era teams:
- build on short-lived feature branches
- roll out in production with feature flags

Representative flag platforms:
- `LaunchDarkly`
- `Statsig`
- `Unleash`
- `Flagsmith`

## Naming Guidance

Guardian's default branch naming remains:

```text
<type>/<short-kebab-description>
```

Alternative org-specific patterns can still be supported if they are already established:

```text
feature/<issue-id>-<short-description>
fix/<issue-id>-<short-description>
hotfix/<version>-<description>
release/<version>
chore/<description>
```

## Anti-Patterns

| Pattern | Risk | Safer default |
|---------|------|---------------|
| long-lived branches | conflict buildup and context drift | merge or rebase within `1-2` days when possible |
| direct commits to `main` in larger teams | bypassed review and quality gates | protect branches and require review |
| inconsistent naming (`feature/`, `feat/`, `f/`) | weak discoverability and automation | standardize and automate naming |
| abandoned stale branches | repository clutter | auto-delete after merge and alert on stale age |
| too many release branches | management overhead grows fast | keep only the minimum supported branches |
