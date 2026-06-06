# Voice Exit Survey (Churn Analysis)

Purpose: Use this file when the task is churn-reason capture, cancellation-flow feedback, save-offer design, or churn analysis.

Contents:
- Trigger points and response-rate targets
- Churn-reason taxonomy and save offers
- Exit-survey flow and data contract
- Churn analysis report structure
- Recommended handoffs

## Trigger Points

| Trigger | Priority | Response-rate target |
|---------|----------|----------------------|
| Cancel button click | Critical | `80%+` (blocking) |
| Downgrade flow | High | `70%+` |
| Renewal cancellation | High | `60%+` |
| Trial end | Medium | `40%+` |
| Long inactivity | Medium | `30%+` |

## Churn Reason Taxonomy

| Category | Example sub-reasons | Typical save offer |
|----------|---------------------|--------------------|
| `Pricing` | too expensive, budget cut, low ROI | discount or downgrade plan |
| `Features` | missing feature, too complex, competitor advantage | roadmap share or training |
| `Experience` | hard to use, performance issues, support dissatisfaction | onboarding reset or guided setup |
| `Situation` | project ended, company decision, temporary pause | account pause |
| `Competitive` | switching to named competitor | differentiation follow-up |

## Recommended Survey Flow

1. Capture the primary churn reason.
2. Capture the sub-reason and competitor when relevant.
3. Ask whether the user would return in the future.
4. Offer optional open-text feedback.
5. Trigger a save attempt only when the selected category has a valid save offer.

## Minimal Data Contract

```typescript
interface ExitSurveyResponse {
  primaryReason: string;
  secondaryReasons?: string[];
  competitor?: string;
  feedback?: string;
  wouldReturn: boolean;
  userId: string;
  planType: string;
  tenure: number;
}

trackEvent('exit_survey_completed', {
  primary_reason: primaryReason,
  sub_reason: subReason,
  has_competitor: Boolean(competitor),
  would_return: wouldReturn,
  tenure_days: tenure
});
```

## Churn Analysis Report: [Period]

```markdown
## Churn Analysis Report: [Period]

### Overview
| Metric | Value | vs Previous | Target |
|--------|-------|-------------|--------|
| Churn Rate | [X.X%] | [+/-X%] | <[X%] |
| Churned Revenue | $[X] | [+/-X%] | - |
| Survey Response Rate | [X%] | [+/-X%] | >60% |

### Churn Reasons Breakdown
| Reason | Count | % | Revenue Lost | Trend |
|--------|-------|---|--------------|-------|
| Pricing | [N] | [X%] | $[X] | Up/Down/Flat |
| Features | [N] | [X%] | $[X] | Up/Down/Flat |
| Experience | [N] | [X%] | $[X] | Up/Down/Flat |
| Situation | [N] | [X%] | $[X] | Up/Down/Flat |
| Competitive | [N] | [X%] | $[X] | Up/Down/Flat |

### Competitor Analysis
| Competitor | Lost Users | % of Churn | Key Differentiator |
|------------|------------|------------|-------------------|
| [Comp A] | [N] | [X%] | [What they offer] |

### Save Attempt Effectiveness
| Offer Type | Attempts | Saved | Rate | Revenue Saved |
|------------|----------|-------|------|---------------|
| Discount | [N] | [N] | [X%] | $[X] |
| Training | [N] | [N] | [X%] | $[X] |
| Pause | [N] | [N] | [X%] | $[X] |

### Churn by Segment
| Segment | Churn Rate | Primary Reason | Action |
|---------|------------|----------------|--------|
| Enterprise | [X%] | [Reason] | [Action] |
| Pro | [X%] | [Reason] | [Action] |
| Starter | [X%] | [Reason] | [Action] |

### Would Return Analysis
| Response | Count | % | Follow-up Action |
|----------|-------|---|------------------|
| Yes | [N] | [X%] | win-back campaign eligible |
| No | [N] | [X%] | post-mortem interview |
```

## Handoff Rules

- Repeated competitor-loss patterns -> `/Compete analyze [competitor] advantage`
- Save-offer and churn-response execution -> `/Retain address churn: [primary reason]`
- Product gaps with strong evidence -> `Spark`
