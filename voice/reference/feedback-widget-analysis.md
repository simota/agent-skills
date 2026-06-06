# Voice Feedback Widget & Analysis

Purpose: Use this file when the task is in-app feedback capture, feedback categorization, sentiment analysis, or user-response templates.

> **2026 widget landscape.** Hotjar, Zonka, Qualaroo, Sprig, FullStory, LogRocket, and dozens of others ship in-app NPS / feedback widgets with `~2-minute` setup and **AI categorisation built in**. The 2026 differentiator is no longer "do you have an AI categoriser" — it is **whose codebook the categoriser uses**. Vendor-default categories almost never match how the business already discusses its product; pipe widget submissions through your team-curated taxonomy from `thematic-coding.md` before they drive routing decisions. The keyword tables below are the **fallback for low-volume / sample-of-one feedback**, not the production classifier — for any volume worth analysing, use a tuned LLM coder against the same locked codebook.
>
> **Tool name changes (2023→):** Apptentive (formerly a standalone mobile feedback platform) was acquired by Alchemer in January 2023 and is now branded **Alchemer Mobile** (https://www.alchemer.com/apptentive-is-now-alchemer-mobile/). Do not reference "Apptentive" as an independent product — use Alchemer Mobile.

Contents:
- Widget design and event contract
- Feedback categories and sentiment rules
- Minimal analysis logic
- Feedback analysis report format
- Close-the-loop response templates

## In-App Feedback Widget

Recommended feedback types:

| Type | Use for |
|------|---------|
| `bug` | broken behavior or defects |
| `feature` | net-new capability requests |
| `improvement` | workflow or UX improvements |
| `praise` | positive reinforcement and value moments |
| `other` | uncategorized feedback |

Minimal submission contract:

```typescript
interface FeedbackSubmission {
  type: 'bug' | 'feature' | 'improvement' | 'praise' | 'other';
  message: string;
  page: string;
  userId?: string;
  screenshot?: string;
}

trackEvent('feedback_submitted', {
  type,
  message_length: message.length,
  page: window.location.pathname
});
```

## Feedback Categorization Framework

| Category | Description | Example |
|----------|-------------|---------|
| `Usability` | friction in discoverability or flow | "I can't find the button." |
| `Performance` | speed or stability issue | "This page loads too slowly." |
| `Feature Request` | request for a new capability | "Please add bulk export." |
| `Bug Report` | broken or incorrect behavior | "Saving fails after submit." |
| `Content` | unclear copy or documentation | "The explanation is confusing." |
| `Praise` | positive signal worth preserving | "This flow is very convenient." |

## Sentiment Classification

| Sentiment | Score | Typical indicators |
|-----------|-------|--------------------|
| `positive` | `+1` | convenient, helpful, great, thank you |
| `neutral` | `0` | question, suggestion, mixed statement |
| `negative` | `-1` | confusing, slow, broken, difficult |

## Minimal Analysis Logic

```typescript
interface AnalyzedFeedback {
  original: string;
  sentiment: 'positive' | 'neutral' | 'negative';
  sentimentScore: number;
  categories: string[];
  keywords: string[];
  actionable: boolean;
}

const positiveKeywords = ['convenient', 'good', 'helpful', 'great', 'thanks'];
const negativeKeywords = ['problem', 'slow', 'error', 'confusing', 'hard'];
```

Rules:
- mark feedback as `actionable` when it maps to `feature`, `bug`, or `usability`
- allow multi-label categorization
- prefer human review for low-confidence sentiment or sarcasm

## Feedback Analysis Report: [Period]

```markdown
## Feedback Analysis Report: [Period]

### Summary
| Metric | Value | vs Previous Period |
|--------|-------|-------------------|
| Total Feedback | [N] | [+/-X%] |
| NPS Score | [X] | [+/-X points] |
| Positive Sentiment | [X%] | [+/-X%] |
| Negative Sentiment | [X%] | [+/-X%] |

### Category Breakdown
| Category | Count | % of Total | Trend |
|----------|-------|------------|-------|
| Feature Requests | [N] | [X%] | Up/Down/Flat |
| Bug Reports | [N] | [X%] | Up/Down/Flat |
| Usability Issues | [N] | [X%] | Up/Down/Flat |
| Praise | [N] | [X%] | Up/Down/Flat |
| Other | [N] | [X%] | Up/Down/Flat |

### Top Issues
| Rank | Issue | Count | Impact | Recommendation |
|------|-------|-------|--------|----------------|
| 1 | [Issue description] | [N] | [H/M/L] | [Action] |

### Recommended Actions
1. **High Priority:** [Action] - [Expected impact]
2. **Medium Priority:** [Action] - [Expected impact]
3. **Low Priority:** [Action] - [Expected impact]
```

## Close-the-Loop Response Templates

### Positive Feedback

```markdown
Thank you for the feedback. We are glad [specific point] is working well for you.
We will keep investing in that experience.
```

### Feature Request

```markdown
Thank you for the suggestion. We have logged [feature name] for review alongside similar requests.
We will share an update if it moves forward.
```

### Bug Report

```markdown
Thank you for reporting this issue. We are sorry for the inconvenience.
We are investigating [issue] and will follow up after we confirm the fix.
```

### Negative Feedback

```markdown
Thank you for sharing this. We are sorry the experience around [issue] was frustrating.
We are reviewing the feedback seriously and will communicate the next step.
```
