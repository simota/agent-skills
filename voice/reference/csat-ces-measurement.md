# CSAT & CES Measurement

Read for operational touchpoint satisfaction/effort surveys. Voice defines the instrument; Field owns one-off research design, Pulse owns dashboard governance, and Echo produces synthetic hypotheses—not measured customer responses.

## Instrument and scale contract

Freeze question wording, labels, direction, channel and instrument version before collecting responses. Never pool different scales or wording variants without a documented comparability analysis.

| Instrument | Question | Scale | Calculation |
|---|---|---|---|
| CSAT | How satisfied were you with [specific interaction]? | 1 Very dissatisfied; 2 Dissatisfied; 3 Neutral; 4 Satisfied; 5 Very satisfied | `100 × count(score in {4,5}) / valid answered ratings`. Label **T2B**; a T1B result is not interchangeable. |
| CES agreement | [Company] made it easy for me to [task]. | 1 Strongly disagree through 4 Neutral to 7 Strongly agree | Mean of valid 1–7 ratings; higher means easier. |
| CES ease variant | How easy was it to complete [task]? | 1 Very difficult through 4 Neutral to 7 Very easy | Same numeric direction, but record a distinct instrument version; do not silently mix with agreement wording. |

Report valid `n`, invited/eligible denominator, response rate, missingness, time window, cohort/channel, distribution, T2B or mean, and the uncertainty method/interval. With `n=0`, report not estimable. Keep CES `4` neutral in raw data; do not recode it as a high-effort answer to strengthen a risk claim.

## Touchpoint and survey rules

| Touchpoint | Instrument / trigger |
|---|---|
| Support resolution | Select CSAT **or** CES for the decision; within 2h of close. |
| Self-service / settings / task completion | CES; article use within 30min, other tasks after completion. |
| Onboarding / first successful feature use / checkout | CSAT after completion, or CES when task effort is the explicit question. |
| Cancellation intent | Exit survey, not a satisfaction proxy. |
| Relationship / advocacy | NPS, not a touchpoint CSAT substitute. |

One rating + free-text why + at most one optional segment question; no bundled CSAT/CES/NPS survey. Ask neutrally, not from a relationship-biased sender. Apply the existing 30-day cross-survey suppression rule. Preserve consent, minimization and access restrictions; use a protected stable subject identifier where follow-up is authorized.

Follow up on CSAT 1–2 (cause of dissatisfaction) or CES 1–3 (highest-friction step) with the recovery owner within 24h. For positive scores, ask what to preserve only when that qualitative context is needed. A missing why is missing evidence, not a guessed reason.

## Operational decision defaults

These are **Voice defaults to confirm against the engagement**, not universal industry benchmarks or independent authorization to stop a release.

| Metric | Default interpretation / next action |
|---|---|
| CSAT T2B ≥85%; 75–84%; 65–74%; <65% | Maintain / iterate on bottom-box themes / targeted improvement / escalate to the accountable owner. |
| CSAT bottom-box (1–2) | Target ≤5%; >10% triggers service-recovery escalation even with high T2B. |
| CES mean ≥6; 5–<6; 4–<5; <4 | Maintain / improve difficult tasks / investigate effort sources / escalate critical effort. |
| CES dashboard target | Mean ≥5.5, high-effort share (1–3) <20%, low-effort share (5–7) >60%; name this target separately from the interpretation bands. |

For a launch/block decision, include the sample limits, measured effect, owner and the **approved** release gate; Voice does not invent deployment authority. Compare external benchmarks only after matching source year, population, question, scale, scoring and channel. Otherwise report non-comparable rather than using a cached industry table.

## Triangulation

Join CSAT/CES/NPS only on comparable cohorts/windows; interpretations below are investigation hypotheses, not measured causes.

| CSAT / CES / NPS | Investigate / action |
|---|---|
| High / High / High | Protect the observed experience. |
| High / High / Low | Brand/value or advocacy gap. |
| High / Low / High | Loved product with task friction; investigate and reduce effort. |
| High / Low / Low | Possible hidden dissatisfaction/churn risk; inspect verbatim evidence. |
| Low / High / High | Specific dissatisfaction despite loyalty; recovery follow-up. |
| Low / Low / Any | Service-recovery priority; close the loop within 24h. |
| Mixed cohorts | Report the divergence; do not let the aggregate conceal the affected cohort. |

## Minimal data contracts

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
  userId: string; // protected identifier; never export identity in public reports
  timestamp: string;
}
```

Store instrument version, collection window, eligibility/response denominators and cohort metadata alongside the response collection. Keep consent/access metadata under the project's existing privacy contract; do not infer consent from a score.

## Report and handoff

Output: metric/value/target/status; touchpoint/score/n/trend; high-effort issue/count/verbatim evidence/uncertain cause; priority/current→target/action/owner; sampling limits and follow-up disposition. Do not fill root-cause cells without evidence.

Route why text to `voice thematic`, relationship triangulation to `voice nps`, stable metrics to Pulse, recovery cohorts to Growth, redesign briefs to Spark, effort hypotheses to Echo, reliability-correlated drops to Beacon, and strategic cohort trade-offs to Magi. The handoff carries instrument version, cohort/window and evidence—not an unsourced industry rank.
