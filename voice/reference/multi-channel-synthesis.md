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
| At-Risk | [N] | [+/-X] | [Issue] | -> Growth |
| Churned | [N] | [+/-X] | [Issue] | -> Compete |
```

## Handoff Heuristics

- Route repeated churn-risk themes to `Growth`.
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


---

## Market and Regulatory Context (SKILL.md excerpt)

**2025-2026 NPS industry medians**: all-industry average 32, median 44; B2B SaaS 41, E-commerce 61, Financial Services 68, Healthcare 37 (Retently 2026 — https://www.retently.com/blog/good-net-promoter-score/; CustomerGauge B2B 2025 — https://customergauge.com/blog/b2b-nps-benchmarks-tying-revenue-to-your-experience-program). Always cite the benchmark edition year — scores drift 2-5 points annually.

**VoC platform market (2026)**: Gartner Magic Quadrant for VoC Platforms 2026 (https://www.gartner.com/en/documents/6367011) identifies Qualtrics, Medallia, and Sprinklr as Leaders. The market grew 22% in 2025, driven by AI-powered analysis, omnichannel listening, and autonomous agents. Forrester consolidated its Customer Feedback Management Wave into a broader "Customer Feedback Management and Analytics Solutions" category.

**EU AI Act & GDPR for feedback pipelines**: The EU Digital Omnibus (November 2025) proposed amendments explicitly recognizing AI training on personal data as a legitimate interest under GDPR, subject to data minimisation, transparency, and an unconditional right to object (https://www.whitecase.com/insight-alert/eu-digital-omnibus-what-changes-lie-ahead-data-act-gdpr-and-ai-act). For VoC pipelines: collect only feedback necessary for the stated purpose; disclose that LLM classification is applied to verbatim responses; honour subject opt-out from automated profiling. Applies whenever respondents are EU residents.

**Micro-survey tooling (2026)**: Sprig, Qualaroo, and Hotjar Surveys lead in-product micro-surveys. Sprig supports behavioral targeting and recontact-interval controls; Qualaroo specialises in contextual Nudge-style 1-2 question surveys; Hotjar combines inline surveys with heatmap/session-recording context. Choose after a 2-week pilot with an A/B test before scaling.
