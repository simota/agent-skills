# Branch Health Diagnostics Reference

Purpose: Score branch readiness by sync, age, conflict risk, CI state, size creep, and review status.

## Contents

- Health indicators
- Aggregate score and grades
- Report template
- Monitoring rules
- Remediation workflows
- Branch lifecycle

## Health Indicators

| Indicator | Weight | Key thresholds |
|-----------|--------|----------------|
| Sync status | `25%` | behind main: `0-5` healthy, `6-15` warning, `16-30` critical, `31+` severe |
| Branch age | `20%` | `0-3` fresh, `4-7` active, `8-14` warning, `15+` stale |
| Conflict potential | `20%` | overlapping files or hunks raise risk |
| CI status | `15%` | failing or unstable CI lowers score immediately |
| Size creep | `10%` | branch keeps growing after review start |
| Review status | `10%` | long-unreviewed branches degrade health |

### Sync Status

```yaml
sync_status:
  commits_behind:
    healthy: 0-5
    warning: 6-15
    critical: 16-30
    severe: 31+
  days_since_rebase:
    healthy: 0-3
    warning: 4-7
    critical: 8-14
    severe: 15+
```

### Branch Age

```yaml
branch_age:
  fresh: 0-3
  active: 4-7
  maturing: 8-14
  stale: 15+
```

## Aggregate Score

| Grade | Score | Meaning |
|-------|-------|---------|
| `Excellent` | `90-100` | ready to merge or review |
| `Healthy` | `75-89` | minor issues only |
| `Warning` | `50-74` | needs attention before merge |
| `Critical` | `25-49` | unsafe without remediation |
| `Severe` | `0-24` | likely requires rebase or split |

## Report Template

```markdown
## Branch Health Report

**Branch:** `feature/example`
**Target:** `main`

### Health Score: 65/100 (Warning)

### Status Indicators
- Sync: warning
- Age: healthy
- CI: healthy
- Review: warning

### Issues Detected
- 12 commits behind `main`
- 9 days since rebase

### Recommended Actions
1. Rebase onto `main`
2. Resolve overlapping files before requesting merge
```

## Proactive Monitoring

Automate checks for:
- branch age
- commits behind target
- CI state
- open review age
- overlapping file growth

## Remediation Workflows

### Rebase Workflow

1. refresh target branch
2. rebase or merge according to team strategy
3. resolve conflicts
4. rerun CI
5. refresh branch health score

### Split Workflow

Use when:
- branch reaches `XL` or larger
- unrelated concerns accumulated
- review or CI churn keeps growing

## Branch Lifecycle

Recommended lifecycle:
- create
- stay short-lived
- review quickly
- merge or close
- auto-delete after merge
