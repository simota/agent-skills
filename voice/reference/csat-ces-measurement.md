# CSAT & CES Measurement Reference

Purpose: Design, deploy, and interpret Customer Satisfaction (CSAT) and Customer Effort Score (CES) surveys at the right touchpoints; map results to industry benchmarks (Zendesk, HubSpot, Gartner); and triangulate CSAT × CES × NPS to separate satisfaction-the-feeling from effort-the-friction from loyalty-the-behavior.

## Scope Boundary

- **voice `csat`**: CSAT and CES instrument design, touchpoint selection, scale governance, benchmark mapping, and combined CSAT × CES × NPS triangulation report.
- **voice `nps` (default, elsewhere)**: relationship loyalty / advocacy. NPS is a leading indicator of growth; CSAT is a touchpoint health measure; CES is a friction measure. Use all three; do not substitute.
- **voice `kano` (elsewhere)**: feature-level classification. Kano explains *why* CSAT is what it is at the feature level; CSAT measures *whether* the experience landed.
- **voice `thematic` (elsewhere)**: open-ended verbatim coding. CSAT/CES asks score-then-why — `thematic` codes the why field.
- **researcher (elsewhere)**: study design rigor for evaluative research. Voice CSAT/CES is operational and continuous; Researcher owns one-off evaluative studies.
- **echo (elsewhere)**: persona walkthrough — predicts CSAT/CES drops; CSAT/CES confirms.
- **pulse (elsewhere)**: dashboards and KPI governance — Pulse owns the CSAT/CES dashboard once Voice has defined the instrument.

## Workflow

```
SELECT    →  match metric to question: CSAT for "did it satisfy?", CES for "was it easy?"
          →  freeze scale (CSAT 1-5; CES 1-7) — non-standard scales lose benchmark comparability

TOUCHPOINT →  trigger CSAT immediately post-interaction (≤24h); CES post-task completion
           →  delays >72h degrade recall accuracy by ~30% (Zendesk benchmark data)

AUTHOR     →  one rating item, one verbatim "why" field, ≤2 demographic fields, no leading words
           →  do not bundle CSAT + CES + NPS in one survey — fatigue inflates abandonment

DEPLOY     →  embed in-channel (email reply / in-app modal / SMS) — context preserves accuracy
           →  channel response rate: SMS 45-60%, in-app 25-40%, email-embedded 15-25%

SCORE      →  CSAT = % top-two-box (4+5 of 5); CES = mean on 1-7 (≥5 = good)
           →  always report n, top-box %, bottom-box %, and CI

TRIANGULATE → cross-reference CSAT × CES × NPS by cohort to separate signals
            → low CES + high CSAT + high NPS = product loved despite friction (fix the friction)

REPORT    →  benchmark vs industry, segment splits, top "why" themes, owner recommendations
          →  alert on bottom-box (CSAT 1-2, CES 1-3) within 24h to recovery owner
```

## CSAT Instrument

Question (canonical wording): "How satisfied were you with [specific interaction / feature]?"

Scale (1-5, do not change):

1. Very dissatisfied
2. Dissatisfied
3. Neutral
4. Satisfied
5. Very satisfied

Score = (count of 4 + count of 5) / total responses, expressed as a percent — top-two-box (T2B). Some industries cite T1B (very satisfied only); state which when reporting.

| CSAT (T2B) | Verdict | Action |
|------------|---------|--------|
| ≥85% | World-class | Maintain; investigate any segment dip |
| 75-84% | Good | Iterate on bottom-box themes |
| 65-74% | Average | Targeted improvement program |
| <65% | Critical | Escalate; pause feature shipping until root-cause fixed |

Bottom-box (1-2) target: ≤5%. A bottom-box >10% is a service-recovery emergency regardless of T2B.

## CES Instrument (CES 2.0)

Question (Gartner/CEB 2013 wording): "[Company] made it easy for me to handle my issue." (or "to complete my task")

Scale (1-7 agreement, do not change):

1. Strongly disagree
2. Disagree
3. Somewhat disagree
4. Neutral
5. Somewhat agree
6. Agree
7. Strongly agree

Score = mean of all responses (1-7). High-effort threshold: 1-3 (counts as "effort experienced"). Treat 4 as ambiguous; weight to 1-3 for risk dashboards.

| CES mean | Verdict | Action |
|----------|---------|--------|
| ≥6.0 | World-class — frictionless | Maintain; document the design |
| 5.0-5.9 | Good | Iterate on bottom-quartile tasks |
| 4.0-4.9 | Friction present | Map effort sources via verbatim coding |
| <4.0 | Critical effort | Block launch / escalate to product fix |

CES is a stronger predictor of repeat purchase and retention than CSAT (Gartner / Dixon et al., 2010 — "Stop Trying to Delight Your Customers"). High effort predicts churn even when satisfaction is recorded as positive.

## Industry Benchmarks (Cite the Source)

| Industry | CSAT (T2B) | CES (mean) | Source notes |
|----------|------------|------------|--------------|
| SaaS | 78-83% | 5.1-5.5 | HubSpot State of Service |
| E-commerce | 80-86% | 5.3-5.7 | Zendesk CX Trends |
| Financial services | 73-78% | 4.8-5.2 | ACSI sector reports |
| Telecom | 65-72% | 4.5-4.9 | Gartner CX benchmarks |
| Healthcare (patient) | 70-78% | 4.6-5.0 | Press Ganey, ACSI Health |
| Hospitality | 80-87% | 5.4-5.8 | ACSI Travel & Hospitality |
| Government services | 60-68% | 4.0-4.5 | ACSI Federal Government |

Always cite source year — benchmarks drift 2-5 points annually. Use the latest publication; do not back-cast a 2018 number to a 2025 product.

## Combined-with-NPS Triangulation Matrix

A single metric is fragile. Cross-tab CSAT × CES × NPS by cohort to find actionable contradictions:

| CSAT | CES | NPS | Diagnosis | Action |
|------|-----|-----|-----------|--------|
| High | High | High | Healthy core experience | Protect; document patterns |
| High | High | Low | Satisfied but no advocacy | Investigate brand / value perception |
| High | Low | High | Loved despite friction | Fix the friction before competitor offers smoother path |
| High | Low | Low | Polite resignation | Severe hidden churn risk — investigate immediately |
| Low | High | High | Loyal complainer | Acknowledge issue; recovery follow-up |
| Low | Low | Any | Service-recovery emergency | Block-and-fix; close-loop within 24h |
| Mixed across cohorts | — | — | Segment divergence | Cohort-specific roadmap |

The "high CSAT + low CES" cell is the single most valuable insight CSAT alone cannot surface — customers say they are satisfied while quietly burning effort that predicts churn.

## Touchpoint Selection

| Touchpoint | Best metric | Trigger window |
|------------|-------------|----------------|
| Support ticket close | CSAT + CES | ≤2h post-resolution |
| Self-service article view | CES | ≤30min post-view |
| Onboarding milestone | CSAT | Immediately on completion |
| Checkout / purchase | CSAT | Order confirmation page |
| Cancellation flow | Exit survey, not CSAT | At intent, not after |
| Quarterly relationship | NPS, not CSAT | Calendar-driven |
| Feature first-use | CSAT (transactional) | After first successful use |

Do not run relationship-level CSAT — it conflates touchpoints and dilutes signal. Use NPS for relationship; CSAT/CES for touchpoint.

## Survey Hygiene

- One rating item per survey. Bundling CSAT + CES doubles abandonment (HubSpot 2023 data).
- Verbatim "why" field is required — score without context cannot be acted on.
- Maximum 3 questions total (rating + why + optional segment tag).
- Send from a neutral identity, not a personal CSM — relationship bias inflates CSAT 4-9 points.
- Apply 30-day suppression — do not survey the same user twice in 30 days across CSAT/CES/NPS.
- For SMS: send within 2 hours of the event or response rates drop ~32%.

## Anti-Patterns

- Reporting CSAT mean instead of T2B — averages hide bimodal distributions where 50% love and 50% hate the experience.
- Using a 7-point CSAT or 5-point CES — non-standard scales break benchmark comparability and mid-point bias differs.
- Bundling CSAT + CES + NPS in one survey — fatigue inflates abandonment, especially on mobile.
- Treating CES "neutral" (4) as good — neutral is friction unacknowledged; weight to bottom-quartile for risk dashboards.
- Sending CSAT from a CSM's personal email — relationship bias is real and measurable.
- Acting on CSAT without segmenting by plan / persona / channel — segment splits often show one cohort masking another.
- Ignoring CES while celebrating high CSAT — the "polite resignation" cohort churns silently.
- Surveying after every touchpoint — survey fatigue at 30-day window collapses response rate by 40-60%.
- Using closed "why" pickers instead of free-text — pre-defined categories miss the actual reason and bias toward the listed options.

## Handoff

- **To `voice thematic`**: verbatim "why" responses → 6-phase coding for theme extraction.
- **To `voice nps`**: CSAT/CES results into the relationship NPS context for triangulation reporting.
- **To Pulse**: stable instrument → dashboard governance and KPI tracking.
- **To Retain**: bottom-box (CSAT 1-2 / CES 1-3) cohorts → 24h recovery follow-up and churn-risk flag.
- **To Spark**: persistent low-CSAT touchpoints → feature redesign briefs.
- **To Echo**: low-CES tasks → cognitive walkthrough to identify the specific friction step.
- **To Beacon**: CSAT/CES drops correlated with SLO breaches → joint reliability + experience root-cause.
- **To Helm**: cross-cohort CSAT × CES × NPS divergence → strategic positioning input.

References:
- Dixon, Freeman & Toman (2010), "Stop Trying to Delight Your Customers" (HBR / CEB CES origin)
- Gartner CES 2.0 canonical wording (2013)
- Zendesk CX Trends (cite year of edition used)
- HubSpot State of Service (cite year of edition used)
- ACSI sector benchmarks — https://www.theacsi.org/
- Retently CSAT benchmark report 2026 — https://www.retently.com/blog/customer-satisfaction-score-csat/
- Gartner Magic Quadrant for Voice of the Customer Platforms 2026 — https://www.gartner.com/en/documents/6367011
- CES predictiveness vs CSAT: Gartner research cited in Ringly.io CES statistics 2026 — https://www.ringly.io/blog/customer-effort-score-statistics-2026
