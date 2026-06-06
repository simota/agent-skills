# Voice Multi-Channel Feedback Synthesis

Purpose: Use this file when feedback must be merged across surveys, support, reviews, social channels, interviews, or sales notes.

Contents:
- Source inventory and channel priority
- Unified taxonomy
- Normalization contract
- Priority-scoring rule
- Cross-channel report format
- Handoff heuristics

## Source Inventory

| Channel | Type | Typical collection method | Priority |
|---------|------|---------------------------|----------|
| NPS Survey | Quantitative | email or in-app | Primary |
| CES Survey | Quantitative | post-action | Primary |
| CSAT Survey | Quantitative | touchpoint prompt | Primary |
| In-app Widget | Qualitative | always-on | High |
| Support Tickets | Qualitative | Zendesk, Intercom | High |
| Exit Survey | Qualitative | cancellation flow | High |
| App Store Reviews | Public | API or export | Medium |
| G2 / Capterra | Public | API or scraping | Medium |
| Social Media | Public | monitoring tools | Monitor |
| Sales Calls | Qualitative | CRM notes | Medium |
| User Interviews | Qualitative | scheduled research | Low volume, high value |

## Unified Taxonomy

Apply the same tags across all sources.

| Dimension | Allowed values |
|-----------|----------------|
| `Category` | `bug`, `feature`, `ux`, `performance`, `pricing`, `support`, `praise`, `other` |
| `Sentiment` | `positive (+1)`, `neutral (0)`, `negative (-1)` |
| `Urgency` | `critical`, `high`, `medium`, `low` |
| `Segment` | `enterprise`, `pro`, `starter`, `free`, `trial` |
| `Journey Stage` | `awareness`, `consideration`, `onboarding`, `active`, `at-risk`, `churned` |
| `Impact` | `revenue`, `retention`, `satisfaction`, `efficiency` |

## Normalization Contract

```typescript
interface UnifiedFeedback {
  id: string;
  source: 'nps' | 'ces' | 'csat' | 'widget' | 'support' | 'exit' | 'review' | 'social' | 'sales' | 'interview';
  originalId: string;
  content: string;
  category: string;
  sentiment: 'positive' | 'neutral' | 'negative';
  sentimentScore: number;
  urgency: 'critical' | 'high' | 'medium' | 'low';
  segment: string;
  journeyStage: string;
  npsScore?: number;
  cesScore?: number;
  csatScore?: number;
  userId?: string;
  userMRR?: number;
  timestamp: string;
  keywords: string[];
  actionable: boolean;
  themes: string[];
}
```

## Priority Scoring

Themes that appear across multiple channels carry more weight than single-channel anecdotes.

```text
priorityScore = frequency * (revenueImpact / 1000) * (1 - sentimentImpact)
```

Use the score to rank issues after normalization, not before.

## Multi-Channel Feedback Report: [Period]

```markdown
## Multi-Channel Feedback Report: [Period]

### Executive Summary
| Metric | Value | vs Previous | Trend |
|--------|-------|-------------|-------|
| Total Feedback | [N] | [+/-X%] | Up/Down/Flat |
| Avg Sentiment | [X.X] | [+/-X] | Up/Down/Flat |
| NPS | [X] | [+/-X] | Up/Down/Flat |
| CES | [X.X] | [+/-X] | Up/Down/Flat |
| CSAT | [X%] | [+/-X%] | Up/Down/Flat |

### Volume by Channel
| Channel | Count | % of Total | Sentiment | Key Theme |
|---------|-------|------------|-----------|-----------|
| NPS Survey | [N] | [X%] | [+/-X] | [Theme] |
| CES Survey | [N] | [X%] | [+/-X] | [Theme] |
| In-app Widget | [N] | [X%] | [+/-X] | [Theme] |
| Support Tickets | [N] | [X%] | [+/-X] | [Theme] |
| App Reviews | [N] | [X%] | [+/-X] | [Theme] |
| Social | [N] | [X%] | [+/-X] | [Theme] |

### Cross-Channel Theme Analysis
| Theme | NPS | CES | Widget | Support | Reviews | Total | Priority |
|-------|-----|-----|--------|---------|---------|-------|----------|
| [Theme 1] | [N] | [N] | [N] | [N] | [N] | [Sum] | P1 |

### Prioritized Issues
| Rank | Issue | Frequency | Revenue Impact | Sentiment | Action |
|------|-------|-----------|----------------|-----------|--------|
| 1 | [Issue] | [N] | $[X] at risk | [-X.X] | [Action] |

### Segment-Specific Insights
| Segment | Volume | Top Issue | Sentiment | Action |
|---------|--------|-----------|-----------|--------|
| Enterprise | [N] | [Issue] | [+/-X] | [Action] |

### Journey Stage Analysis
| Stage | Volume | Sentiment | Top Concern | Handoff |
|-------|--------|-----------|-------------|---------|
| Onboarding | [N] | [+/-X] | [Issue] | -> Echo |
| Active | [N] | [+/-X] | [Issue] | -> Roadmap |
| At-Risk | [N] | [+/-X] | [Issue] | -> Retain |
| Churned | [N] | [+/-X] | [Issue] | -> Compete |
```

## Handoff Heuristics

- Route repeated churn-risk themes to `Retain`.
- Route repeated feature demand with evidence to `Spark`.
- Route competitor mentions or switching reasons to `Compete`.
- Route bug clusters to `Scout`.
- Route metric gaps or dashboard needs to `Pulse`.

## LLM-Powered Synthesis (2025-2026)

When using LLMs to synthesise cross-channel feedback at scale, apply the hybrid pipeline pattern confirmed by 2025 research:

- Use few-shot LLMs for aspect identification and opinion-term extraction (~90% accuracy on B2B English feedback).
- Use fine-tuned compact models (BERT-class) for per-aspect sentiment classification at high volume — better cost/latency profile.
- Multimodal ABSA (combining text + behavioural signals) is emerging: the LRSA framework (2025) injects LLM-generated rationales into smaller models via dual cross-attention for improved accuracy on ambiguous feedback.
- Always build confusion matrices per channel — systematic misclassification patterns differ by source (support tickets vs app reviews vs NPS verbatims).

Sources:
- Frontiers in AI — "Model uncertainty and variability in LLM-based sentiment analysis" (2025) — https://www.frontiersin.org/journals/artificial-intelligence/articles/10.3389/frai.2025.1609097/full
- arXiv — "Beyond the Star Rating: Scalable ABSA Using LLMs and Text Classification" (2026) — https://arxiv.org/html/2602.21082
- arXiv — "Enhanced Multimodal ABSA by LLM-Generated Rationales" (2025) — https://arxiv.org/abs/2505.14499
