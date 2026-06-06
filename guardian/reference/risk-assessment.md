# Change Risk Assessment Reference

Purpose: Quantify review and deployment risk from file sensitivity, complexity, hotspot overlap, coverage, familiarity, and Ripple impact.

## Contents

- Risk factors and weights
- Ripple integration
- Risk bands
- Report template
- Mitigations
- Regression prediction
- AUTORUN integration

## Risk Factors

| Factor | Weight | Key thresholds |
|--------|--------|----------------|
| File sensitivity | `25%` | auth, security, crypto, payment, `.env*`, secrets |
| Change complexity | `20%` | cyclomatic delta `1-5` medium, `6-15` high, `>15` critical |
| Hotspot overlap | `15%` | hotspot = `>10` commits or `>3` bug fixes or `>50%` churn in `90` days |
| Dependency impact | `15%` | shared dependency or cross-module changes raise risk |
| Test coverage | `15%` | line `<50%` or branch `<40%` is poor |
| Author familiarity | `10%` | `>50%` prior commits low risk, `20-50%` medium, `5-20%` low familiarity |
| Ripple impact | `10%` | explicit blast-radius amplification from Ripple |

## Ripple Integration

Outgoing handoff:

```markdown
## GUARDIAN_TO_RIPPLE_HANDOFF

**Reason**: changed files have uncertain downstream impact
**Requested output**: dependency and blast-radius analysis
```

Incoming handoff:

```markdown
## RIPPLE_TO_GUARDIAN_HANDOFF

**Blast Radius**: ...
**Critical Dependents**: ...
**Confidence**: ...
```

## Risk Bands

| Band | Score | Default action |
|------|-------|----------------|
| Critical | `85-100` | Sentinel + staged rollout + rollback plan |
| High | `65-84` | extra reviewer + integration tests |
| Medium | `40-64` | standard review with focused checks |
| Low | `0-39` | may expedite |

Recommended canary for elevated risk:
- `1% -> 10% -> 50% -> 100%`

## Report Template

```markdown
## Change Risk Assessment

### Risk Factor Breakdown
- File sensitivity: ...
- Complexity: ...
- Hotspot overlap: ...
- Dependency impact: ...
- Coverage: ...
- Familiarity: ...
- Ripple impact: ...

### High-Risk Files
- `...`

### Risk Mitigation Recommendations
1. ...
```

## Mitigations

By category:
- security-sensitive files -> Sentinel review
- low coverage -> Radar handoff
- hotspot overlap -> Zen or Atlas involvement
- wide blast radius -> Ripple or staged rollout

## Regression Prediction

Elevate regression risk when:
- hotspot overlap is high
- coverage regresses materially
- logic complexity rises sharply
- author familiarity is low

## AUTORUN Integration

Pause when:
- `risk_score > 85`
- risk is high and required evidence is missing
