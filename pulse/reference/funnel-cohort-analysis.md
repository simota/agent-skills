# Funnel & Cohort Analysis

## 2026 Note on Attribution

With third-party cookies still present in Chrome (Google's **2025-04-22** cancellation of TPC deprecation) but Privacy Sandbox APIs **retired 2025-10-17** (Topics, Protected Audience, Attribution Reporting all gone), last-touch click attribution remains the practical default — but it under-credits early funnel steps for users in EEA/UK whose consent has been denied. Combine event-based funnels with one of:

- **Marketing-mix modeling (MMM)** — re-emerged in 2024-2026 as the cookieless-attribution fallback ([Google's Meridian](https://developers.google.com/meridian), Robyn, PyMC-Marketing). Better suited to aggregate attribution than user-level.
- **CausalImpact / Bayesian structural time series** — for "did the feature launch move the metric" questions.
- **Geo / switchback experiments** — for incrementality testing where pure A/B is contaminated.
- **Snowflake Cortex / BigQuery ML anomaly detection** — passive funnel-drift detection.

Do not present funnel conversion rates without disclosing the consent-denial blind spot for EEA/UK traffic (see `privacy-consent.md` for the 2025-07-21 Consent Mode v2 enforcement context).

## Funnel Definition Template

```markdown
## Funnel: [Funnel Name]

**Goal:** [What conversion does this funnel measure?]
**Timeframe:** [How long should conversion window be?]

### Steps

| Step | Event | Criteria |
|------|-------|----------|
| 1 | `landing_page_viewed` | page_type = "landing" |
| 2 | `signup_form_started` | - |
| 3 | `signup_form_submitted` | - |
| 4 | `email_verified` | - |
| 5 | `onboarding_completed` | - |

### Expected Conversion Rates

| Step | Target Rate | Action if Below |
|------|-------------|-----------------|
| 1→2 | 30% | Improve CTA visibility |
| 2→3 | 70% | Reduce form friction |
| 3→4 | 80% | Improve email deliverability |
| 4→5 | 50% | Simplify onboarding |

### Segments to Analyze

- By acquisition source (organic, paid, referral)
- By device type (mobile, desktop)
- By user plan (free, paid)
```

## Funnel Implementation (GA4)

```typescript
// Track funnel steps
import { getAnalytics, logEvent } from 'firebase/analytics';

const analytics = getAnalytics();

// Step 1: Landing page view
logEvent(analytics, 'landing_page_viewed', {
  page_type: 'landing',
  campaign: 'summer_sale'
});

// Step 2: Signup started
logEvent(analytics, 'signup_form_started', {
  form_location: 'hero_section'
});

// Step 3: Signup submitted
logEvent(analytics, 'signup_form_submitted', {
  signup_method: 'email'
});

// Step 4: Email verified
logEvent(analytics, 'email_verified', {
  verification_time_minutes: 5
});

// Step 5: Onboarding completed
logEvent(analytics, 'onboarding_completed', {
  steps_completed: 5,
  total_steps: 5
});
```

---

## Cohort Definition Template

```markdown
## Cohort: [Cohort Name]

**Cohort Type:** [Acquisition | Behavioral | Time-based]
**Cohort Event:** [Event that defines cohort membership]
**Retention Event:** [Event that defines "active" for this cohort]
**Time Period:** [Weekly | Monthly]

### Cohort Table Structure

| Cohort | Week 0 | Week 1 | Week 2 | Week 3 | Week 4 |
|--------|--------|--------|--------|--------|--------|
| Jan W1 | 100% | 40% | 30% | 25% | 22% |
| Jan W2 | 100% | 42% | 32% | 27% | - |
| Jan W3 | 100% | 38% | 28% | - | - |
| Jan W4 | 100% | 45% | - | - | - |

### Benchmark Targets

| Period | Target Retention | Industry Average |
|--------|------------------|------------------|
| Week 1 | 40% | 35% |
| Month 1 | 25% | 20% |
| Month 3 | 15% | 10% |
```

## Cohort Analysis Implementation

```typescript
interface CohortConfig {
  cohortEvent: string;       // Event that creates cohort membership
  retentionEvent: string;    // Event that counts as "retained"
  cohortProperty?: string;   // Optional: property to segment cohorts
  periodType: 'day' | 'week' | 'month';
  periodsToAnalyze: number;
}

const signupCohortConfig: CohortConfig = {
  cohortEvent: 'user_signed_up',
  retentionEvent: 'session_started',
  periodType: 'week',
  periodsToAnalyze: 12
};

// SQL query for cohort analysis (BigQuery/Snowflake)
const cohortQuery = `
WITH cohorts AS (
  SELECT
    user_id,
    DATE_TRUNC(MIN(event_timestamp), WEEK) as cohort_week
  FROM events
  WHERE event_name = 'user_signed_up'
  GROUP BY user_id
),
activity AS (
  SELECT
    user_id,
    DATE_TRUNC(event_timestamp, WEEK) as activity_week
  FROM events
  WHERE event_name = 'session_started'
  GROUP BY user_id, activity_week
)
SELECT
  c.cohort_week,
  DATE_DIFF(a.activity_week, c.cohort_week, WEEK) as weeks_since_signup,
  COUNT(DISTINCT c.user_id) as users
FROM cohorts c
LEFT JOIN activity a ON c.user_id = a.user_id
GROUP BY cohort_week, weeks_since_signup
ORDER BY cohort_week, weeks_since_signup
`;
```
