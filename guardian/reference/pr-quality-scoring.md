# PR Quality Scoring Reference

Purpose: Score PR reviewability and consistency using stable component weights, calibrated thresholds, and reproducible grades.

## Contents

- Component weights
- Aggregate formula
- Grade mapping
- Report template
- Calibration
- AUTORUN integration

## Component Weights

| Component | Weight | Core idea |
|-----------|--------|-----------|
| Size | `25%` | how reviewable the change volume is |
| Focus | `20%` | whether the PR stays on one concern |
| Commits | `15%` | message quality and atomicity |
| Tests | `15%` | adequacy of verification |
| Documentation | `10%` | whether change context is documented |
| Risk | `15%` | inverse quality pressure from risky changes |

Representative size thresholds:
- files `0-5` and lines `<=100` -> excellent
- files `6-10` and lines `<=200` -> strong
- files `11-20` and lines `<=400` -> acceptable
- files `21-35` and lines `<=800` -> weak

## Aggregate Formula

```yaml
total_quality_score:
  size: 0.25
  focus: 0.20
  commit: 0.15
  tests: 0.15
  docs: 0.10
  risk_inverse: 0.15
```

## Grade Mapping

| Grade | Score | Meaning |
|-------|-------|---------|
| `A+` | `95-100` | merge immediately |
| `A` | `85-94` | quick review |
| `B+` | `75-84` | standard review |
| `B` | `65-74` | careful review |
| `C` | `50-64` | consider split |
| `D` | `35-49` | should split |
| `F` | `0-34` | must restructure |

## Report Template

```markdown
## PR Quality Score: {total}/100 ({grade})

### Component Breakdown
- Size: ...
- Focus: ...
- Commits: ...
- Tests: ...
- Documentation: ...
- Risk: ...

### Improvement Opportunities
1. ...
```

## Calibration

Project calibration rules:
- sample size target: `50` PRs
- teams `>10` people can use stricter size thresholds
- excellent PR baseline: `<10` files and `<200` lines
- expected feature score: `75-90`

## AUTORUN Integration

AUTORUN may compute quality score automatically.

Pause when:
- score `< 35`
- risk component alone exceeds `85`
