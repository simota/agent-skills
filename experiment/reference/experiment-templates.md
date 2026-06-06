# Experiment Templates

## Hypothesis Document Template

```markdown
## Experiment: [Experiment Name]

### Hypothesis
**If** [we make this change]
**Then** [this metric will improve]
**Because** [this is the underlying mechanism]

### Background
- **Problem Statement:** [What problem are we solving?]
- **Current State:** [Current metric value and user behavior]
- **Evidence:** [What data/research supports this hypothesis?]

### Variants
| Variant | Description | Traffic Allocation |
|---------|-------------|--------------------|
| Control | Current experience | 50% |
| Treatment | [Describe change] | 50% |

### Metrics
**Primary Metric (Decision Metric):**
- Metric: [Name]
- Definition: [Exact calculation]
- Current Baseline: [X%]
- MDE (Minimum Detectable Effect): [Y%]
- Expected Lift: [Z%]

**Secondary Metrics (Reference Metrics):**
1. [Metric name] - [Definition]
2. [Metric name] - [Definition]

**Guardrail Metrics (Guardrail Metrics):**
1. [Metric name] - [Threshold that should not be crossed]
2. [Metric name] - [Threshold]

### Sample Size & Duration
- Required Sample Size: [N per variant]
- Current Daily Traffic: [N users]
- Expected Duration: [X days/weeks]
- Statistical Power: 80%
- Significance Level: 5%

### Success Criteria
- [ ] Primary metric shows statistically significant improvement
- [ ] No guardrail metrics violated
- [ ] Lift >= MDE

### Rollout Plan
- **If wins:** Roll out to 100% on [date]
- **If loses:** Revert and [next action]
- **If inconclusive:** [Extend / iterate / abandon]
```

---

## Experiment Report Template

```markdown
## Experiment Report: [Experiment Name]

### Summary
| Metric | Control | Treatment | Lift | P-Value | Significant |
|--------|---------|-----------|------|---------|-------------|
| Primary: [Name] | X% | Y% | +Z% | 0.0XX | Yes/No |
| Secondary: [Name] | X | Y | +Z% | 0.0XX | Yes/No |
| Guardrail: [Name] | X | Y | -Z% | 0.0XX | No violation |

### Recommendation
**[SHIP / ITERATE / ABANDON]**

[1-2 sentences explaining the recommendation]

### Key Findings
1. [Finding 1 with data support]
2. [Finding 2 with data support]
3. [Finding 3 with data support]

### Detailed Results

#### Primary Metric: [Name]
- Control: [X%] (n=[N])
- Treatment: [Y%] (n=[N])
- Relative Lift: [+Z%]
- 95% CI: [[L%, U%]]
- P-Value: [0.0XX]
- Statistical Power Achieved: [X%]

#### Segment Analysis
| Segment | Control | Treatment | Lift | Significant |
|---------|---------|-----------|------|-------------|
| Mobile | X% | Y% | +Z% | Yes/No |
| Desktop | X% | Y% | +Z% | Yes/No |
| New Users | X% | Y% | +Z% | Yes/No |
| Returning Users | X% | Y% | +Z% | Yes/No |

### Timeline
- Started: [Date]
- Ended: [Date]
- Duration: [X days]
- Total Participants: [N]

### Learnings & Next Steps
1. [Learning 1] → [Next step]
2. [Learning 2] → [Next step]

### Appendix
- [Link to hypothesis document]
- [Link to raw data]
- [Link to dashboard]
```

---

## Experimentation Maturity Model

Use this model to assess your team's current experimentation capability and plan the next step.

| Level | Name | Characteristics |
|-------|------|----------------|
| **Level 1** | Ad Hoc | Experiments run without documentation; no pre-registration; results interpreted post-hoc |
| **Level 2** | Defined | Standard hypothesis template used; sample size calculated upfront; primary metric pre-registered |
| **Level 3** | Managed | Automated assignment and tracking; SRM checks; sequential testing available; centralized platform |
| **Level 4** | Optimized | CUPED variance reduction; automated guardrail monitoring; experimentation culture across teams |
| **Level 5** | Continuous | Always-on adaptive experiments (bandits); warehouse-native analysis; organization-wide learning loops |

---

## Experiment Review Process Template

```markdown
## Pre-Launch Review Checklist

### Hypothesis Quality
- [ ] Falsifiable hypothesis stated (If/Then/Because)
- [ ] Primary metric pre-registered and owned by one team
- [ ] Guardrail metrics defined with explicit thresholds
- [ ] Minimum detectable effect (MDE) is practically significant

### Statistical Design
- [ ] Power analysis completed (80%+ power, 5% significance)
- [ ] Sample size achievable within experiment duration
- [ ] Randomization unit appropriate (user-level, session-level, etc.)
- [ ] No overlapping experiments on same population

### Technical Setup
- [ ] Feature flag configured and tested in staging
- [ ] Exposure tracking implemented and verified
- [ ] SRM check query prepared
- [ ] Rollback plan documented

### Ethical / Risk Review
- [ ] No negative UX impact on critical flows (if yes, approval required)
- [ ] Experiment duration ≤ 4 weeks (if longer, approval required)
- [ ] Data privacy and consent requirements met

---

## Post-Launch Review Checklist

### Data Quality
- [ ] SRM check passed (χ² p-value > 0.05)
- [ ] No mid-flight parameter changes
- [ ] Sample size target reached before analysis

### Results Interpretation
- [ ] Analysis used pre-registered primary metric
- [ ] Confidence intervals reported alongside p-values
- [ ] Segment analysis does not drive primary decision
- [ ] Guardrail metrics reviewed

### Decision and Learning
- [ ] Ship / Iterate / Abandon decision documented
- [ ] Key learnings recorded for future experiments
- [ ] Feature flag cleanup scheduled
```

---

## Experiments with Learning (EwL) Metrics

Beyond primary/secondary metrics, EwL metrics capture *what we learned* — not just *what we measured*.

| EwL Metric | Definition | Why It Matters |
|------------|------------|----------------|
| **Hypothesis Quality Score** | % of experiments with falsifiable, pre-registered hypothesis | Prevents p-hacking and HARK-ing |
| **SRM Detection Rate** | % of experiments that ran an SRM check | Ensures data integrity |
| **Null Result Rate** | % of experiments with null result | Healthy rate (40-60%) signals good calibration |
| **Experiment Velocity** | Experiments shipped per month per team | Tracks learning throughput |
| **Time to Decision** | Days from launch to ship/iterate/abandon decision | Identifies bottlenecks in analysis |
| **Learning Reuse Rate** | % of experiments that reference prior learnings | Measures institutional memory |
