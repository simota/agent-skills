# Automation Recipes

Purpose: Provide practical defaults for PR automation, branch protection, merge queue, environment protection, preview environments, and release workflow automation.

## Contents

- PR automation
- Branch protection
- Merge queue
- Environment protection
- Preview environments
- Release automation

## PR Automation

| Pattern | Use it for | Notes |
|---------|------------|-------|
| Auto-labeler | routing reviews and ownership | keep rules deterministic and repo-specific |
| PR size check | fast review risk signal | do not block docs-only or automation-only changes without intent |
| Auto-assign | default reviewer routing | pair with CODEOWNERS rather than replacing it |
| Stale bot | long-idle issue or PR hygiene | exempt active milestones and high-priority work |
| Auto-merge | low-risk, fully gated changes | require status checks and approval policy first |

## Branch Protection Defaults

| Setting | Recommended default |
|---------|---------------------|
| Require pull request | enabled |
| Required approvals | `1-2` |
| Dismiss stale reviews | enabled |
| Required status checks | enabled and name-matched exactly |
| Require up-to-date branch | enabled when merge health matters |
| Require conversation resolution | enabled |
| Allow force push | disabled |
| Allow branch deletion | disabled |

Use CODEOWNERS for `.github/**` and `.github/workflows/**`.

## Merge Queue

Use merge queue when required checks are expensive and queue order matters.

Defaults from the reference set:

- add `merge_group` to the workflow trigger
- build concurrency: `5`
- minimum group size: `1`
- maximum group size: `5`
- status timeout: `60 min`

Required checks must report on merge-group runs, not just PR runs.

## Environment Protection

| Control | Range or rule |
|---------|----------------|
| Required reviewers | `1-6` |
| Wait timer | `0-43200` minutes |
| Branch restrictions | allow only intended deploy branches |
| Self-review prevention | enable when separation of duties matters |
| Custom rules | add when org policy requires external approval logic |

Secret precedence is: `environment` > `repository` > `organization`.

## Preview Environments

- Deploy preview environments from trusted automation only.
- Clean them up automatically when the PR closes.
- Keep preview secrets minimal and environment-scoped.
- Never treat preview artifacts from untrusted PR code as release artifacts.

## Release Automation

Recommended pattern:

1. Build and verify on trusted code.
2. Promote artifacts, do not rebuild untrusted PR outputs into release.
3. Protect production environments with reviewers.
4. Keep rollback or previous artifact promotion available via controlled manual dispatch.
