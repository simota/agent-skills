# Voice NPS Survey Design

Purpose: Use this file when the task is loyalty measurement, NPS implementation, follow-up design, or NPS interpretation.

Contents:
- Core NPS question and score bands
- Follow-up prompts by respondent type
- Formula and benchmark ranges
- Minimal implementation contract
- Analysis checklist

## Core Survey

```markdown
## NPS Survey

### Core Question
"How likely are you to recommend [product name] to a friend or colleague?"

| Score | Segment |
|-------|---------|
| 0-6 | Detractors |
| 7-8 | Passives |
| 9-10 | Promoters |
```

## Follow-up Prompts

| Segment | Prompt |
|---------|--------|
| `Promoters (9-10)` | "What do you value most?" |
| `Passives (7-8)` | "What would make this a 10?" |
| `Detractors (0-6)` | "What did not meet your expectations?" |

## Formula and Benchmarks

```text
NPS = % Promoters - % Detractors
```

| NPS Range | Interpretation |
|-----------|----------------|
| `70+` | World-class |
| `50-69` | Excellent |
| `30-49` | Good |
| `0-29` | Needs improvement |
| `Below 0` | Critical |

## Implementation Rules

- Ask only after the user has experienced meaningful value.
- Keep the score mandatory and the open-text follow-up optional but visible.
- Store `score`, `feedback`, `userId`, `segment`, `touchpoint`, and `timestamp`.
- Track the derived category: `promoter`, `passive`, or `detractor`.
- Separate product outreach consent from the survey response if follow-up is planned.

## Minimal Data Contract

```typescript
interface NPSResponse {
  score: number;
  feedback?: string;
  userId: string;
  segment?: string;
  touchpoint?: string;
  timestamp: string;
}

trackEvent('nps_submitted', {
  score,
  category: score >= 9 ? 'promoter' : score >= 7 ? 'passive' : 'detractor',
  has_feedback: Boolean(feedback)
});
```

## Analysis Checklist

- Report overall NPS and response volume.
- Break down NPS by plan, segment, tenure, and touchpoint.
- Extract promoter strengths, passive upgrade opportunities, and detractor pain points.
- Flag statistically weak samples before recommending broad product changes.
- Route recurrent feature requests to `Spark`, churn-risk themes to `Retain`, and metric instrumentation gaps to `Pulse`.

## 2026 Calibration

- NPS response rates across most B2B SaaS programs settle at **`5-15%`** — set sample-size expectations against this baseline before declaring a result "non-significant".
- Open-text follow-up answers median **`4-7` words** — design the prompt to invite *one specific signal* (top reason, missing feature) rather than an open essay. A 4-word answer is the norm, not a failure.
- AI thematic-analysis platforms (Thematic, Buildbetter, Perspective AI, Zonka, Qualtrics XM with LLM, Hotjar AI) report `~90-95%` theme-detection accuracy on English B2B feedback when the codebook is validated against grounded coding (`thematic-coding.md`). Treat the platform output as the **first pass** that still needs human-curated codebook review — see the Inter-Coder Agreement section in `thematic-coding.md`.
- For follow-up routing, the 2026 standard is to feed verbatim into an AI coder with a *team-curated* codebook (not the vendor default) — vendor-default categories rarely match how the business already talks about its product.

## 2025-2026 Industry Benchmarks

| Industry | NPS (median) | Source |
|----------|-------------|--------|
| B2B Software & SaaS | 41 | Retently 2025 |
| E-commerce | 61 | Retently 2026 |
| Technology & Services | 63 | Retently 2026 |
| Financial Services | 68 | Retently 2026 |
| Healthcare | 37 | Retently 2026 |
| All-industry average | 32 | Retently 2026 |
| All-industry median | 44 | Retently 2026 |

B2C brands average 49; B2B brands average 38 (11-point structural gap). Benchmarks drift year-to-year — always cite the edition year.

Sources:
- Retently NPS Benchmark 2025 — https://www.retently.com/blog/good-net-promoter-score/
- CustomerGauge B2B NPS Benchmarks 2025 — https://customergauge.com/blog/b2b-nps-benchmarks-tying-revenue-to-your-experience-program
- CustomerGauge SaaS NPS Benchmarks 2025 — https://customergauge.com/benchmarks/blog/nps-saas-net-promoter-score-benchmarks
