# Voice CSAT & CES Surveys

Purpose: Use this file when the task is touchpoint satisfaction measurement, effort measurement, or post-action survey design.

Contents:
- CSAT scale and calculation
- CES scale, targets, and touchpoints
- Follow-up rules
- Minimal data contracts
- CES analysis format

## CSAT Framework

```markdown
## CSAT Survey: [Touchpoint]

### Core Question
"How satisfied were you with [specific action or touchpoint]?"

| Score | Label | Emoji |
|-------|-------|-------|
| 5 | Very satisfied | 😄 |
| 4 | Satisfied | 🙂 |
| 3 | Neutral | 😐 |
| 2 | Dissatisfied | 🙁 |
| 1 | Very dissatisfied | 😞 |
```

```text
CSAT = (satisfied responses / total responses) x 100
```

Best moments:
- after purchase completion
- after support resolution
- after first successful feature use
- after onboarding completion

## CES Framework

```markdown
## CES Survey

### Core Question
"How easy was it to complete [task]?"

| Score | Label | Interpretation |
|-------|-------|----------------|
| 1 | Very difficult | High effort, churn risk |
| 2-3 | Difficult | Friction exists |
| 4 | Neutral | Mixed signal |
| 5-6 | Easy | Healthy experience |
| 7 | Very easy | Loyalty driver |
```

```text
CES = total score / total responses
Target: 5.5+ on the 7-point scale
```

Operational thresholds:
- `1-3` = high effort
- `4` = neutral
- `5-7` = low effort
- high-effort share target: `<20%`
- low-effort share target: `>60%`

## Best CES Touchpoints

| Touchpoint | Trigger | Example question |
|------------|---------|------------------|
| Support resolution | ticket closed | "How easy was it to resolve your issue?" |
| First feature use | first successful use | "How easy was it to start using [feature]?" |
| Settings change | settings updated | "How easy was it to change this setting?" |
| Onboarding completion | account setup complete | "How easy was it to set up your account?" |
| Purchase completion | checkout complete | "How easy was it to complete your purchase?" |

## Follow-up Rules

- CSAT `1-2`: ask what caused dissatisfaction.
- CSAT `4-5`: ask what worked well when qualitative context is needed.
- CES `1-3`: ask where effort or friction was highest.
- CES `6-7`: ask what made the experience easy enough to preserve.

## Minimal Data Contracts

```typescript
interface CSATResponse {
  score: 1 | 2 | 3 | 4 | 5;
  touchpoint: string;
  feedback?: string;
}

interface CESResponse {
  score: 1 | 2 | 3 | 4 | 5 | 6 | 7;
  touchpoint: string;
  feedback?: string;
  userId: string;
  timestamp: string;
}
```

## CES Analysis Report: [Period]

```markdown
## CES Analysis Report: [Period]

### Summary
| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| Average CES | [X.X] | 5.5+ | [Met/Not Met] |
| High Effort (1-3) | [X%] | <20% | [Met/Not Met] |
| Low Effort (5-7) | [X%] | >60% | [Met/Not Met] |

### CES by Touchpoint
| Touchpoint | CES Score | Responses | Trend |
|------------|-----------|-----------|-------|
| Onboarding | [X.X] | [N] | Up/Down/Flat |
| First purchase | [X.X] | [N] | Up/Down/Flat |
| Support | [X.X] | [N] | Up/Down/Flat |
| Settings | [X.X] | [N] | Up/Down/Flat |

### High Effort Issues
| Issue | CES | Count | Root Cause | Fix |
|-------|-----|-------|------------|-----|
| [Issue 1] | [X.X] | [N] | [Cause] | [Action] |

### Effort Reduction Priorities
1. **[Touchpoint]**: [Current CES] -> [Target CES]
   - Action: [Specific improvement]
   - Owner: [Team]
```
