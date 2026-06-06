# Retention Curve Analysis Reference

Purpose: Deep-dive retention curve shape classification, Power User Curve, Quick Ratio, and stickiness diagnostics. Anchored to a16z, Reforge, and Sarah Tavel frameworks. Produces actionable retention diagnostics with SQL and alert thresholds.

## Scope Boundary

- **pulse `retention`**: Retention curve shape (L / smile / flat), power-user band, Quick Ratio, DAU/MAU (this document).
- **pulse `cohort` (elsewhere)**: General cohort design and churn measurement. Default entry.
- **pulse `activation` (elsewhere)**: Activation rate and aha-moment. Activation precedes retention in the funnel.
- **Bond (elsewhere)**: Retention *strategy* (win-back, habit formation). `retention` owns measurement; Bond owns intervention design.

## Workflow

```
SCOPE     →  confirm product type (B2B SaaS / B2C / mobile / marketplace)
          →  pick window (90/180/365-day minimum)
          →  define "active" event (per NSM)

QUERY     →  build cohort matrix (signup month × months-since-signup)
          →  compute retention % per cell

CLASSIFY  →  shape curve (L / smile / flat)
          →  identify stable plateau (>= month 3)

OVERLAY   →  Power User Curve (MAU engagement frequency band)
          →  Quick Ratio (growth / churn)
          →  DAU/MAU stickiness

DIAGNOSE  →  map shape to pathology (see table below)
          →  prioritize remediation: activation vs engagement vs resurrection

ALERT     →  define drift thresholds for cohort-over-cohort comparison
          →  handoff to Bond for intervention design
```

## Curve Shape Classification

```
Retention %
 100% |                              (all curves start at 100%)
      |\.
      | \..
      |  \...
      |   \.....                     L-shape (BROKEN)
      |    \........                  → falls to 0-10% and keeps falling
      |     \............
      |
 100% |\.
      | \..
      |  \....
      |   \.....                     FLAT (STABLE, low)
      |    \......_______            → stabilizes near 15-40%
      |
 100% |\.
      | \..
      |  \...              __         SMILE (HEALTHY)
      |   \...__________///           → stabilizes, then rises (resurrection)
      |      stable band
```

| Shape | Plateau % (month 3+) | Diagnosis | Priority Fix |
|-------|---------------------|-----------|--------------|
| L-shape | < 10% | Broken product-market fit; users don't return | Rebuild activation; audit aha-moment |
| Flat Low | 10-30% | Niche usage; small core; growth-limited | Broaden use cases; expand personas |
| Flat Healthy | 30-60% (B2C) / 60-90% (B2B SaaS) | Working retention; stable core | Optimize expansion / upsell |
| Smile | Rises after plateau | Excellent; resurrection + network effects | Invest in viral/referral loops |

### B2B SaaS Benchmarks (2025 update)
- Month-1 logo retention: 46.9% (avg), ≥70% (healthy), ≥90% (elite)
- Month-12 logo retention: ≥80% (healthy), ≥95% (elite enterprise)
- NRR (Net Revenue Retention) — 2025 reset: private-SaaS median 101-102%; top performers 104-106%; SMB segment often 90-105% (below 100% increasingly common); enterprise 115-125%; best-in-class enterprise software 120-150%; growing companies with NRR ≥100% grew ~2x faster YoY than peers below 100% in 2025. See `revenue-analytics.md` for source-cited cuts.

### B2C/Consumer Benchmarks
- Day-1: 25-40% (avg mobile)
- Day-7: 10-20%
- Day-30: 3-8%
- Elite social/utility: 25%+ at Day-30

## Power User Curve (a16z)

Beyond aggregate retention, classify users by engagement frequency within MAU. Strong products show a concentration of users on the right-hand side (high engagement days per month).

```
% of MAU
  │
  │███
  │███             █              CLIFF (weak)
  │███             █              → Most MAUs engaged <5 days
  │███████        █               → Heavy left-skew
  │███████████████
  └───────────────────────
    1  5  10  15  20  25  30  days-active-in-month

  │                         ███
  │                        ████
  │                    █████████   SMILE (strong)
  │██████            ███           → Right-skewed MAU
  │██████████████████              → Healthy power-user band ≥21 days
  └───────────────────────
    1  5  10  15  20  25  30
```

Rule of thumb: teams should watch the **L21+ band** (users active 21+ days in 30). Elite consumer products have 30%+ of MAU in L21+.

## Quick Ratio (Growth Velocity)

```
Quick Ratio = (New MRR + Expansion MRR) / (Churn MRR + Contraction MRR)
```

| Value | Classification | Action |
|-------|---------------|--------|
| ≥ 4 | Elite | Invest in growth loops |
| 2 - 4 | Healthy | Maintain + focus on expansion |
| 1 - 2 | Treading water | Fix churn before scaling acquisition |
| < 1 | Shrinking | Emergency churn investigation |

## DAU / MAU Stickiness

| DAU/MAU | Interpretation |
|---------|---------------|
| ≥ 0.50 | Elite daily habit (WhatsApp, Instagram tier) |
| 0.20 - 0.50 | Healthy frequent use (SaaS core tools, Slack) |
| 0.10 - 0.20 | Weekly utility (analytics, reporting) |
| < 0.10 | Occasional; likely a "pull only when needed" tool |

Cross-check: if DAU/MAU is low but NPS and revenue are high, the product may be intentionally low-frequency (tax software, annual tools). Don't force daily usage where the job doesn't require it.

## SQL Patterns

### Cohort retention matrix (BigQuery / Snowflake)

```sql
WITH signups AS (
  SELECT
    user_id,
    DATE_TRUNC('month', signup_at) AS cohort_month
  FROM users
),
activity AS (
  SELECT
    user_id,
    DATE_TRUNC('month', event_at) AS active_month
  FROM events
  WHERE event_name = 'nsm_action_completed'
  GROUP BY 1, 2
)
SELECT
  s.cohort_month,
  DATE_DIFF('month', s.cohort_month, a.active_month) AS months_since_signup,
  COUNT(DISTINCT a.user_id) * 1.0 / cohort_size.total AS retention_rate
FROM signups s
JOIN activity a USING (user_id)
JOIN (
  SELECT cohort_month, COUNT(DISTINCT user_id) AS total
  FROM signups
  GROUP BY 1
) cohort_size USING (cohort_month)
GROUP BY 1, 2, cohort_size.total
ORDER BY 1, 2;
```

### Power User band (L21+)

```sql
WITH monthly_activity AS (
  SELECT
    user_id,
    DATE_TRUNC('month', event_at) AS month,
    COUNT(DISTINCT DATE(event_at)) AS days_active
  FROM events
  WHERE event_name = 'nsm_action_completed'
  GROUP BY 1, 2
)
SELECT
  month,
  COUNT(CASE WHEN days_active >= 21 THEN user_id END) * 1.0
    / COUNT(*) AS l21_share
FROM monthly_activity
GROUP BY 1
ORDER BY 1;
```

### Quick Ratio (monthly)

```sql
WITH mrr_movement AS (
  SELECT
    month,
    SUM(new_mrr) AS new_mrr,
    SUM(expansion_mrr) AS expansion_mrr,
    SUM(churn_mrr) AS churn_mrr,
    SUM(contraction_mrr) AS contraction_mrr
  FROM mrr_movements
  GROUP BY 1
)
SELECT
  month,
  (new_mrr + expansion_mrr) / NULLIF(churn_mrr + contraction_mrr, 0) AS quick_ratio
FROM mrr_movement
ORDER BY 1;
```

## Drift Alerts (Cohort-over-Cohort)

| Signal | Threshold | Severity |
|--------|-----------|----------|
| Month-1 retention drops ≥5pp vs rolling-3-month baseline | Trigger | HIGH |
| L21+ share drops ≥3pp over 2 months | Trigger | MEDIUM |
| DAU/MAU drops ≥0.05 over 30 days | Trigger | MEDIUM |
| Quick Ratio < 1 for 2 consecutive months | Trigger | CRITICAL |

Route CRITICAL alerts to Scout for investigation and Bond for intervention. Route HIGH/MEDIUM to product owner with cohort drill-down.

## Deliverable Contract

When `retention` completes, emit:

- **Cohort retention matrix** (at least 90 days, preferably 180-365).
- **Curve shape classification** (L / flat / smile) with plateau % and benchmark comparison.
- **Power User Curve** with L21+ band percentage.
- **Quick Ratio** trend (last 6 months).
- **DAU/MAU stickiness** ratio.
- **Cohort drift alerts** with thresholds and severity.
- **Diagnosis**: activation gap vs engagement gap vs resurrection opportunity.
- **Handoff targets**: `activation` (activation gap), Bond (re-engagement intervention), Experiment (uplift validation), Scout (anomalous drop).

## References

- a16z — "The Power User Curve: The Best Way to Understand Your Most Engaged Users"
- Sarah Tavel / Benchmark — "Consumer Retention Playbook"
- Reforge — Growth Models and retention measurement
- Brian Balfour — "Why Retention is the Single Most Important Growth Metric"
- Mixpanel — Retention Benchmarks Report 2024
- [High Alpha — 2025 SaaS Benchmarks](https://www.highalpha.com/saas-benchmarks)
- [ChartMogul — The SaaS Retention Report: The New Normal](https://chartmogul.com/reports/saas-retention-the-new-normal/)
- [RockingWeb — SaaS Metrics Benchmarks 2025 (2,000 companies synthesis)](https://www.rockingweb.com.au/saas-metrics-benchmark-report-2025/)
- [Benchmarkit — 2025 SaaS Performance Metrics](https://www.benchmarkit.ai/2025benchmarks)
