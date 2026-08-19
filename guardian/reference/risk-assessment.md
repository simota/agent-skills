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

## Axis-Max Triggers

The weighted score above is a **ranking** instrument. It must not be the only gate, because summing unlike axes lets them cancel: file sensitivity carries 25%, so an auth change with low complexity, no hotspot overlap, good coverage, and a familiar author lands well under the `85` pause threshold. Nothing about the auth exposure got smaller.

Each axis therefore fires on its own, regardless of `risk_score`:

| Axis at `high` | Fires |
|----------------|-------|
| Security sensitivity — auth, authz, secrets, PII, supply chain, crypto | Sentinel review; threat assumptions and negative tests recorded |
| Data migration — backfill, destructive or narrowing conversion, new constraint | data owner review; dry-run, invariants, row counts; Expand–Contract staging |
| Irreversibility — data written, notifications sent, payments taken, contract published | owner + recovery rehearsal; manual gate before rollout |
| Blast radius — shared library, many consumers, all users, irreversible loss | integrator/SRE review; staged rollout with stop conditions |
| Observability — success and failure indistinguishable in production | instrumentation lands **before** the change |
| Novelty — technology, scale, or domain new to the team | experienced peer review; spike or benchmark; scope limited |

Report the axes as a profile, not a single number. Two changes both scoring `60` are not comparable when one is `60` from broad-but-reversible surface area and the other is `60` from an irreversible data conversion.

Never average an axis away, and never round a maxed axis down because "the overall score is fine" — that is the mechanism, not an edge case.

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
- **any** Axis-Max Trigger fires and its required review or evidence is absent — independent of `risk_score`
