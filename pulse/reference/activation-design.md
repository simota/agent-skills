# Activation Rate Design Reference

Purpose: Aha-moment discovery, Magic Number identification, time-to-value (TTV) measurement, and activation milestone design. Produces an evidence-grounded activation contract that precedes retention in the lifecycle funnel.

## Scope Boundary

- **pulse `activation`**: Aha-moment / Magic Number discovery, activation event design, TTV, activated-vs-not retention overlay (this document).
- **pulse `retention` (elsewhere)**: Retention curves and Power User analysis. Activation feeds retention; they are measured as a linked pair.
- **pulse `funnel` (elsewhere)**: Generic conversion funnel. Activation is one specific conversion step inside that funnel.
- **Onboarding copy (Prose `onboarding`)**: UX writing for the activation flow. Activation measurement owned by Pulse; activation copy owned by Prose.
- **Bond (elsewhere)**: Post-activation habit formation and re-engagement. Activation is pre-Day-7; Bond is Day-7 onwards.

## Workflow

```
DISCOVER  →  compare activated vs non-activated cohorts
          →  surface behaviors that predict retention ≥ 1.5x baseline
          →  candidate events from the "activation suspect list"

MAGIC     →  find the quantitative threshold (N actions, M days)
          →  e.g., "7 friends in 10 days", "2k messages", "5 invoices/mo"
          →  validate via retention lift and regression

DEFINE    →  commit the activation event (name, payload, window)
          →  set target rate (B2C 20-40%, SaaS self-serve 50-70%, PLG top 75%+)
          →  set TTV target (SaaS <7 days, consumer <1 session)

FUNNEL    →  signup → first-value action → activation milestone
          →  measure drop-off per step; instrument events

OVERLAY   →  activated cohort retention vs non-activated (W1/W4/W12)
          →  segment by acquisition channel × plan tier

CONTRACT  →  publish activation registry; alert on drift
          →  handoff to onboarding design (Prose) and experiment (Experiment)
```

## Aha-Moment vs Magic Number

- **Aha-moment**: qualitative experience where the user perceives core value. Discovered via user research (Field), session replay (Trace), and first-session analytics.
- **Magic Number**: quantitative threshold that operationalizes the aha-moment. A measurable threshold the product team can move.

The Magic Number must be:
1. **Behavioral** (user performs action), not demographic (user is in segment X).
2. **Predictive** (activated cohort retains ≥1.5x baseline at Week 4+).
3. **Achievable within TTV window** (most new users can reach it in < target TTV).
4. **Specific and testable** (not "uses the app regularly" — "sends ≥3 messages within 48h").

## Industry Examples

| Product | Aha-moment | Magic Number | Evidence |
|---------|-----------|--------------|----------|
| Facebook | "I see familiar people in my feed" | 7 friends in 10 days | Retention 2x+ vs non-activated |
| Twitter | "I see content I care about" | Follow 30 accounts | Retention 3x+ post-Chamath era |
| Slack | "My team is actually using this" | 2,000 messages sent (team total) | Channel stickiness threshold |
| Dropbox | "My files follow me" | 1 file in 1 folder on 1 device | Early PLG Magic Number |
| Zynga (FarmVille) | "I want to come back tomorrow" | Return on Day 1 | Classic D1 hook |
| HubSpot | "I got a real contact in" | 5 contacts within 1 week | SaaS PLG benchmark |

## Activation Rate Benchmarks (2024-2026)

| Product Type | Target Activation Rate | TTV Target |
|-------------|------------------------|-----------|
| B2C mobile (free) | 20-40% Day-1 activation | In-session (< 5 min) |
| B2C consumer web | 30-50% Day-1 activation | < 1 session |
| SaaS self-serve (PLG) | 50-70% in 7 days | < 7 days |
| SaaS sales-assisted | 60-80% in 30 days | < 30 days (often onboarding-gated) |
| Enterprise | N/A (use deployment milestones) | Measured in weeks post-kickoff |
| Elite PLG | 75%+ | < 1 hour first value |
| AI / agent product (new in 2026) | "First successful task" within first session; aim 50-70% session-1 | Sub-5-minute first usable output; if the model can't deliver value in the first try, the Magic Number must include retry/repair behavior |

AI-product caveat: an activation event for an agent product should be **outcome-grounded** ("first task completed with user-confirmed success"), not "first prompt sent" (which is the AI-native equivalent of `signup_completed` — fires on intent, not on value). Pair with an offline eval score to detect activation rates inflated by users who "completed" a low-quality output.

## Event Schema

```typescript
interface ActivationEvent {
  event_name: "activation_reached";
  user_id: string;
  activation_type: "magic_number" | "milestone" | "aha_moment";
  magic_number_threshold: number;  // e.g., 7 for "7 friends"
  magic_number_actual: number;     // achieved count
  time_to_activation_sec: number;  // TTV from signup
  acquisition_channel: string;
  plan_tier: string;
  first_value_action_at: string;   // ISO timestamp of first value event
  activated_at: string;            // ISO timestamp of activation
}
```

Anti-pattern: naming this event "user_activated" without the numeric evidence makes it impossible to audit or re-tune when the Magic Number shifts.

## Funnel Instrumentation

```
SIGNUP
   │
   ├─[signup_completed] ─ t=0
   │
   ▼
ACCOUNT SETUP
   │
   ├─[profile_completed]
   ├─[first_workspace_created]
   │
   ▼
FIRST VALUE ACTION (milestone 1)
   │
   ├─[first_value_action]              ← must be logged separately
   │                                     (e.g., first_message_sent)
   ▼
MAGIC NUMBER PROGRESS
   │
   ├─[magic_progress_1] ─ threshold * 0.25
   ├─[magic_progress_2] ─ threshold * 0.50
   ├─[magic_progress_3] ─ threshold * 0.75
   │
   ▼
ACTIVATION
   │
   └─[activation_reached]              ← retention predictive threshold
```

## SQL — Activated vs Non-Activated Retention

```sql
WITH activated_cohort AS (
  SELECT
    user_id,
    DATE(activated_at) AS activation_date
  FROM events
  WHERE event_name = 'activation_reached'
),
all_signups AS (
  SELECT
    user_id,
    DATE(signed_up_at) AS signup_date
  FROM users
),
cohort_labels AS (
  SELECT
    s.user_id,
    s.signup_date,
    CASE WHEN a.user_id IS NOT NULL THEN 'activated' ELSE 'not_activated' END AS status
  FROM all_signups s
  LEFT JOIN activated_cohort a USING (user_id)
)
SELECT
  c.status,
  DATE_DIFF('week', c.signup_date, DATE(e.event_at)) AS weeks_since_signup,
  COUNT(DISTINCT e.user_id) * 1.0 /
    COUNT(DISTINCT c.user_id) OVER (PARTITION BY c.status) AS retention_rate
FROM cohort_labels c
LEFT JOIN events e
  ON e.user_id = c.user_id
  AND e.event_name = 'nsm_action_completed'
  AND e.event_at >= c.signup_date
GROUP BY c.status, weeks_since_signup
ORDER BY weeks_since_signup;
```

Expected signal: activated cohort retains ≥1.5x (preferably ≥2x) vs non-activated at Week 4+. If lift < 1.5x, the Magic Number is not yet predictive — refine the threshold or event definition.

## Segment Cuts

Always report activation rate broken down by:

1. **Acquisition channel** (organic / paid / referral / direct) — paid traffic often activates lower.
2. **Plan tier** (free / trial / paid) — paid usually activates higher; intentional, not a warning.
3. **Signup cohort week** — watch for week-over-week drift (≥5pp drop = alert).
4. **Persona / role** (if self-reported) — B2B SaaS varies 2x-5x across persona.
5. **Device / platform** (mobile / desktop) — mobile often activates faster but shallower.

## Activation Drift Alerts

| Signal | Threshold | Severity |
|--------|-----------|----------|
| Overall activation rate drops ≥5pp vs 4-week baseline | Trigger | HIGH |
| TTV increases ≥30% vs baseline | Trigger | MEDIUM |
| Activated cohort W4 retention drops ≥5pp | Trigger | CRITICAL (Magic Number eroding) |
| Single channel activation drops ≥10pp | Trigger | MEDIUM (likely acquisition quality shift) |

## Activation Registry Template

```markdown
## Activation: [Product]
- **Aha-moment (qualitative)**: [user perception]
- **Magic Number (quantitative)**: [N actions] within [M time window]
- **Event name**: activation_reached
- **Target rate**: [e.g., 60% in 7 days]
- **Current rate**: [%]
- **TTV target / actual**: [e.g., <7d / median 4.2d]
- **Retention lift (W4)**: [e.g., 2.3x vs non-activated]
- **Owner**: [team]
- **Last reviewed**: [date]
- **Known gaming vectors**: [e.g., automated signup + bulk action]
```

## Deliverable Contract

When `activation` completes, emit:

- **Aha-moment statement** (qualitative one-liner from research).
- **Magic Number** (quantitative threshold, window, evidence of retention lift).
- **Activation event schema** (typed, with payload contract).
- **Funnel instrumentation plan** (signup → first value → progress → activation).
- **Activated-vs-not retention comparison** (W1/W4/W12 with lift ratio).
- **Segment cuts** (channel, plan, device).
- **Drift alerts** with thresholds and severity.
- **Activation Registry entry** (template above).
- **Handoff targets**: Prose for onboarding copy, Experiment for uplift testing, Bond for post-activation engagement, Field for qualitative validation.

## References

- Sean Ellis — "Hacking Growth" (activation definition + north star)
- Hila Qu — "The Art of PLG Activation" and Reforge PLG course
- Facebook / Chamath Palihapitiya — "7 friends in 10 days" (Stanford talk, 2015)
- Andrew Chen — "New Data Shows Losing 80% of Mobile Users is Normal"
- Amplitude — Product-Led Growth Playbook (activation benchmarks)
- Appcues — PLG Benchmarks Report 2024 (TTV, activation rate)
