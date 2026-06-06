# Quantitative Survey Design Reference

Purpose: Design exploratory quantitative surveys with statistical rigor — item authoring, scale selection, sample-size calculation, question-order bias control, screener design, and response-rate levers. Output is a deployable instrument plus analysis plan, not a data-collection tool.

## Scope Boundary

- **Researcher `survey`**: Exploratory / research-purpose survey design (Likert, MaxDiff, Conjoint, semantic differential). Instrument authoring, sample-size math, order-bias control, reliability checks.
- **vs Echo**: Echo runs persona-based cognitive walkthroughs on UI flows; it does not design statistical instruments. UI comprehension check → Echo; attitudinal / preference measurement → `survey`.
- **vs Pulse**: Pulse defines production KPI tracking events and funnel metrics embedded in the product. Ongoing in-product NPS/CSAT pipelines and dashboard specs → Pulse; one-shot research survey → `survey`.
- **vs Voice**: Voice owns operational feedback surveys (NPS/CSAT/CES), sentiment analysis, and review mining on recurring feedback streams. Operational feedback loop → Voice; exploratory research instrument → `survey`.

Rule of thumb: if the result lives in a research report, `survey`. If it lives in a dashboard or event stream, Pulse or Voice.

## Scale Selection

| Scale | Use when | Anchors | Watch out |
|-------|----------|---------|-----------|
| 5-point Likert | Agreement / frequency, short surveys | Strongly disagree → Strongly agree | Central-tendency bias |
| 7-point Likert | Finer gradation, more variance | Same, expanded | Respondent fatigue on long instruments |
| Semantic differential | Perception / brand attributes | Bipolar adjectives (e.g. cheap ↔ premium) | Requires anchor validation |
| Single-item 0–10 | NPS-style, fast to answer | 0 = Not at all, 10 = Extremely | Low reliability alone |
| MaxDiff (best-worst) | Rank importance across 8+ items | Pick best and worst from sets of 3–5 | Needs ≥300 respondents for stable utilities |
| Conjoint (choice-based) | Trade-off / willingness-to-pay | Choose preferred product profile | Design complexity; use Sawtooth / Conjointly |
| Constant sum | Budget allocation across options | Distribute 100 points | Cognitively heavy; cap at 5 options |

Default for attitudinal research: **5-point Likert** with neutral midpoint. Use 7-point only when the analysis plan requires the extra variance.

## Sample-Size Calculation

For proportions, with desired margin of error `e`, confidence level `z`, and expected proportion `p`:

```
n = (z² × p × (1 − p)) / e²
```

| Confidence | z | Typical use |
|------------|----|------------|
| 90% | 1.645 | Internal directional study |
| 95% | 1.960 | Published / external-facing claim |
| 99% | 2.576 | Regulatory or high-stakes decision |

Worked examples (assume worst-case `p = 0.5`):

| Margin of error | 90% CI | 95% CI |
|-----------------|--------|--------|
| ±10% | 68 | 96 |
| ±5% | 271 | 384 |
| ±3% | 752 | 1067 |

For MaxDiff: minimum `300` respondents for stable item-level utilities. For Conjoint: `200–400` per segment. For factor analysis: `≥10` respondents per item, minimum `200`.

## Question-Order Bias Control

| Bias | Mechanism | Mitigation |
|------|-----------|-----------|
| Priming | Earlier question shapes later interpretation | Randomize question blocks where valid |
| Anchoring | First numeric answer pulls later numerics | Separate numeric blocks, vary order across respondents |
| Consistency | Respondents align later answers with earlier ones | Reverse-code a subset of Likert items |
| Fatigue | Variance drops late in survey | Keep under 10 minutes; place critical items first |
| Satisficing | Respondent picks "neutral" to finish | Attention checks; trim to essential items |

Randomize item order within a scale block, but keep block order fixed when blocks build context (e.g. awareness → usage → satisfaction).

## Screener Design for Quantitative

Screeners must exclude disqualified respondents without revealing target criteria.

- **Buried criteria**: list the target behavior among distractors (e.g. "Which of these apps have you used in the past 30 days?" with 6 options, target is one).
- **Quota-based acceptance**: define age / geography / usage quotas up front; stop recruiting when filled.
- **Straight-line detection**: include at least one reverse-coded item and one attention check ("Select 'Agree' for this item") in screener or instrument.
- **Professional-respondent filters**: reject if completion time < 30% of median, or if they have taken >10 surveys this month on the panel.

## Response-Rate Levers

| Lever | Effect | Cost |
|-------|--------|------|
| Incentive (gift card, entry to draw) | +10–30% completion | Budget |
| Personalized invite subject line | +5–15% open rate | Low |
| Mobile-optimized form | +10–20% on panels with ≥50% mobile | Low |
| Progress bar | +5% completion on surveys ≥5 min | Low |
| Estimated duration in invite | +3–8% open | Low (must be truthful) |
| Reminder at 48h and 5 days | +15–25% total response | Low |
| Instrument length ≤ 10 min | Dominant predictor of completion | Design effort |

## Reliability & Validity Checks

- **Cronbach's α ≥ 0.70** for multi-item scales measuring one construct. Report α in final output.
- **Test-retest reliability**: if the construct should be stable, retest a 10% subsample after 2 weeks; correlation ≥ 0.70 expected.
- **Construct validity**: confirm item loadings via exploratory factor analysis when the scale is new.
- **Content validity**: expert review of item wording before deployment — minimum 2 reviewers.

## Anti-Patterns

- Using 11-point NPS as the only measure of satisfaction — it captures loyalty, not satisfaction; pair with CSAT or 5-point satisfaction.
- Double-barreled items ("How satisfied are you with the speed and reliability?") — split into two items.
- Leading wording ("How much do you love our new feature?") — mirror neutral framings used in prior waves.
- Running MaxDiff with <200 respondents — utilities will be unstable.
- Skipping the pilot — always pilot with 10–15 respondents, verify median completion time, and fix items with >20% skip rate.
- Reporting means on ordinal Likert data without also reporting medians and distributions.
- Conflating statistical significance with practical significance — always report effect size (Cohen's d, odds ratio) alongside p-values.
- Deploying without a pre-registered analysis plan — leads to HARKing and p-hacking.

## Handoff

- **To Voice**: if the survey surfaces an operational feedback need (recurring CSAT tracking), hand off instrument + cadence recommendation.
- **To Pulse**: if any item should become an in-product event (e.g. post-onboarding satisfaction), hand off event-schema suggestion.
- **To Spark**: if MaxDiff / Conjoint surfaces unmet needs with high utility, hand off prioritized feature list.
- **To Cast**: if segmentation analysis yields distinct clusters, hand off cluster profiles for persona update.
- **Always include** in handoff: sample size, confidence interval, Cronbach's α per scale, response rate, known non-response bias, analysis plan link.
