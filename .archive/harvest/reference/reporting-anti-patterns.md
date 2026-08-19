# Reporting Anti-Patterns

Purpose: Use this reference when Harvest must ensure reports stay actionable, contextual, and resistant to metric gaming.

## Contents

- Report-design anti-patterns
- Goodhart and gaming
- Reporting cadence
- Audience layers
- Quality checklist

## Report-Design Anti-Patterns

| ID | Anti-pattern | Guardrail |
|----|--------------|-----------|
| `RA-01` | Too many metrics | Keep `3-5` core metrics for the audience |
| `RA-02` | No context | Include previous period, target, or trend |
| `RA-03` | Cherry-picking | Show negative and positive signal together |
| `RA-04` | Individual ranking | Prefer team aggregates; keep personal detail private |
| `RA-05` | Over-reporting | Match frequency to decision cadence |
| `RA-06` | Snapshot bias | Add trend lines or period comparisons |
| `RA-07` | No next action | Attach actions to important findings |
| `RA-08` | Blind trust in automation | Review anomalies before publishing |

## Goodhart And Gaming

Typical patterns to watch:

| Signal | Possible gaming |
|--------|------------------|
| PR sizes suddenly become uniform | Artificial PR splitting |
| Review times collapse with no comments | Rubber-stamp approvals |
| Friday evening merges spike | Weekly metric chasing |
| Coverage jumps without assertion growth | Hollow test additions |

## Reporting Cadence

| Cadence | Best for |
|---------|----------|
| Daily | Build status, open PR count, urgent operations |
| Weekly | Cycle time, merge volume, review responsiveness |
| Monthly | Quality trends, DORA-style patterns, effort summaries |
| Quarterly | Tech debt, long-term architecture or process health |

## Audience Layers

| Layer | Focus |
|-------|-------|
| `L1 Executive` | Business impact and delivery status |
| `L2 Manager` | Team performance and bottlenecks |
| `L3 Engineer` | Detailed PR-level technical feedback |

## Quality Checklist

- Is the audience explicit?
- Are the core metrics limited and contextualized?
- Does the report include both signal and caveats?
- Does it avoid personal ranking?
- Does it end with next actions?

## 2026 Caveat Additions

- **AI period flagging**: When the report covers any window in which the team's AI-assistant adoption rate changed materially, flag the change inline. DORA 2025 reports AI now positively correlates with throughput but negatively with delivery stability — so a "throughput up" headline without the stability counter-context is misleading.
- **DORA 2025 vocabulary**: Use percentile language ("Top 15%", "Top 15-30%") and 7 team archetypes instead of Elite/High/Medium/Low when sourcing DORA-style commentary.
- **Copilot Code Review split**: When review-time metrics include the Copilot reviewer, separate human and AI review timestamps; otherwise rubber-stamping detection and pickup-time benchmarks misclassify automated comments as human review activity.
