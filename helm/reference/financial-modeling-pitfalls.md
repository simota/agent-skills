Purpose: Use this reference when Helm models SaaS, growth, runway, or investment outcomes. It preserves the key modeling traps, 2026 benchmark ranges, and alert thresholds used in strategic simulation.

## Contents
- `FM-01..FM-10`
- SaaS benchmarks
- scenario design guidance
- Helm alert thresholds

# Financial Modeling Pitfalls & SaaS Benchmarks 2026

## Financial Modeling Anti-Patterns

| ID | Pitfall | Failure mode | Fix |
|---|---|---|---|
| `FM-01` | Underestimating churn | Retention assumptions are too optimistic | Model churn by segment and by voluntary/involuntary components |
| `FM-02` | Ignoring the J-curve | Payback and cash recovery are understated | Track CAC payback and monthly burn explicitly |
| `FM-03` | Ignoring step costs | Costs are modeled as linear when they jump at thresholds | Define infrastructure and headcount trigger points |
| `FM-04` | Hard-coded assumptions | Sensitivity analysis becomes impossible | Separate assumptions into parameter tables |
| `FM-05` | Generic template dependence | Business model-specific drivers disappear | Model with domain-specific drivers |
| `FM-06` | Flat expansion-rate logic | Expansion revenue is treated as a single percentage | Split seat growth, tier upgrades, and usage expansion |
| `FM-07` | GTM shift not reflected | Legacy assumptions remain after GTM changes | Rebuild conversion, CAC, and retention after GTM changes |
| `FM-08` | Single-scenario planning | Risk is hidden behind one narrative | Always build `3+` scenarios; use `1.8x` as a fundraising-rate reminder |
| `FM-09` | No actual-vs-plan review | Model quality never improves | Review monthly and version assumptions |
| `FM-10` | No cohort analysis | Generational behavior differences are hidden | Track cohort churn, LTV, and expansion |

## SaaS Benchmarks

### Core Metrics

| Metric | Benchmark | Interpretation |
|---|---|---|
| Rule of 40 | `40%+` healthy, `50%+` top quartile, `60%+` elite. Q4 2025 public SaaS **median is only 28%**, with only `~20%` of 58 actively-traded SaaS names clearing the 40 line (Aventis Advisors 2026) | `<20%` is a warning |
| Burn Multiple | `<1.0x` at `$25-50M ARR`; AI-native cohorts run **0.8x-1.2x** at the same scale (High Alpha 2026); early-stage default is `~3.4x` (SaaS Capital efficiency tracker 2026) | `>2.0x` is a red flag |
| NRR | overall median `106%` (2026 broad survey); Optifai 939-company panel: Enterprise ACV >$100K `118%`, Mid-Market `108%`, SMB `97%`; Bessemer Cloud Index (public-co structural advantage) `114%`; **AI-native median `48%` with GRR `40%`** (m3ter / SaaS Mag 2026) — most AI tools below the $250/mo line have not yet reached durable PMF; AI premium tier above $250/mo: GRR `70%`, NRR `85%`; elite `130%+` | `<100%` means net shrink — apply segment context for SMB and AI-native cohorts |
| Gross Margin | classical SaaS `70-80%`; **AI-native new normal `60-70%`** (SFAI Labs 2026 disclosure tracker; Bessemer "Shooting Stars" run `~60%` post custom-model + inference reset) | reset benchmark down for AI workloads |
| CAC Payback | `12-18 months` | `>24 months` is weak |
| LTV:CAC | `3:1+` | below this suggests poor unit economics |
| Magic Number | `>0.75` | efficient sales and marketing spend |

### Churn Benchmarks

| Segment | Monthly churn | Annual churn |
|---|---|---|
| B2B SaaS overall | `0.3%-1.0%` | `3.5%-5%` |
| Enterprise | `<=1.0%` | `<=10%` |
| SMB | `3%-7%` | `30%-58%` |
| Usage-based / freemium | `5%-10%+` | `50%+` |
| B2C SaaS | `0.4%-1.0%` | `6%-8%` |

Additional churn split:

```text
Voluntary churn:    2.6%-3.3%
Involuntary churn:  0.8%-1.1%
```

## Scenario Design

| Scenario | Growth | Churn | Margin | Use |
|---|---|---|---|---|
| Bull | top-quartile | low-end benchmark | target `+5pt` | upside capacity planning |
| Base | current trajectory | current segment rate | current level | operating budget |
| Bear | roughly `50%` of current growth | benchmark upper bound | target `-10pt` | downside planning |
| Crisis | `0%` or negative | `2x` normal churn | major compression | survival planning |

### Assumption Management

1. Keep assumptions separate from formulas.
2. Tag each assumption by confidence.
3. Reconcile assumptions monthly against actuals.
4. Run `±20%` sensitivity on major assumptions.
5. Never ship only one scenario.

### Checklist

- Churn is segmented.
- Expansion is modeled by mechanism.
- Step-cost thresholds exist.
- CAC is channel-specific.
- Seasonality is represented if material.
- GTM assumptions match the current motion.

## Helm Alert Thresholds

| Signal | Threshold | Response |
|---|---|---|
| Churn | `>1.5x` segment benchmark upper bound | `RED` |
| Burn Multiple | `>2.0x` | `RED` |
| Rule of 40 | `<20%` | `YELLOW` |
| NRR | `<100%` | `RED` |
| CAC Payback | `>24 months` | `YELLOW` |

## Helm Integration

Use this with:

- `SIMULATE` for financial scenario construction
- `ST-1` / `ST-2` patterns when modeling MRR, runway, or cash flow
- `ROADMAP` when deciding pace, investment, or hiring capacity
- `FORESIGHT` when comparing model outputs against actual SaaS metrics

## 2026 AI-Native Modeling Addendum

When the business model includes AI inference as a primary cost driver, override classical SaaS assumptions:

| Driver | Classical SaaS default | AI-native 2026 default | Rationale |
|---|---|---|---|
| Gross margin | 75% | 60-65% (worst-case 50%) | Inference COGS varies with usage; per-token margin pressure persists even after model price cuts ([SFAI Labs 2026](https://sfailabs.com/guides/the-ai-project-gross-margin-reset-every-saas-company-is-about-to-face)) |
| NRR | 106% | Treat `<85%` as expected baseline below $250/mo ACV until PMF proven; require 90-day cohort GRR before forecasting expansion | AI-native median NRR `48%` / GRR `40%` reflects churn-driven retention |
| CAC Payback | 12-18 months | 6-12 months (compressed by faster activation) **but** rebound risk: churn at month 12-18 if value is novelty-driven | Optimistic curve can disguise downstream cliff |
| Per-active-user cost | rarely tracked | **mandatory**: track inference + storage cost per WAU; flag when COGS/seat > 20% of ARPU | Without this view, healthy Rule-of-40 can mask negative contribution margin per power user |

### Series B Fundability Filter (Carta + Bessemer 2026 read)

Bar in 2026:
- Growth + profitability margin `>40%` (Rule of 40)
- Burn Multiple `<2.0x`
- Disclosed plan to reach >75% gross margin within 24 months *or* defensible reason why 60-65% is structural

Companies missing all three are dropping out of the Series B-fundable pool that would have been raised in 2021 ([Aventis Advisors 2026](https://aventis-advisors.com/rule-of-40-in-saas-2026/), [High Alpha 2026](https://www.highalpha.com/blog/mastering-the-saas-tightrope-between-growth-efficiency-and-ai-costs-in-2026)).
