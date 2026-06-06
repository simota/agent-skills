# North Star Metric Deep-Dive Reference

Purpose: NSM selection rubric, classification, input-metric decomposition, counter/guardrail pairing, and stability contract. For teams that need a single, actionable North Star anchored to value delivery instead of vanity activity.

## Scope Boundary

- **pulse `northstar`**: NSM selection, type classification, decomposition tree, counter/guardrail, stability contract (this document).
- **pulse `kpi` (elsewhere)**: Metric tree construction from an already-chosen NSM. Default entry point.
- **pulse `retention` / `activation` (elsewhere)**: Curve-shape diagnostics and aha-moment discovery. NSM decomposition often references these outputs.
- **Experiment (elsewhere)**: Hypothesis validation. NSM is the primary metric a hypothesis should move, not the experiment surface itself.
- **Helm (elsewhere)**: Business strategy and forecast. NSM is a measurement commitment, not a strategic forecast.

## Workflow

```
DISCOVER  →  interview product/business; surface 2-4 NSM candidates
          →  map to Value Exchange vs Engagement vs Experience

CLASSIFY  →  pick NSM type; confirm "drives sustainable revenue"
          →  reject vanity (total signups, pageviews)

DECOMPOSE →  NSM = f(breadth × depth × frequency × efficiency)
          →  derive 3-5 input metrics, each team-controllable

COUNTER   →  pair with counter metric (prevent gaming)
          →  add guardrail (must-not-degrade)

CONTRACT  →  commit to ≥6mo stability (12mo preferred)
          →  document change-triggers (structural shift only)

PUBLISH   →  NSM one-liner + tree diagram + owner + cadence
```

## NSM Type Classification (Amplitude Playbook)

| Type | Pattern | Example | Works Well When |
|------|---------|---------|-----------------|
| Value Exchange | `monetary_value_transacted` | Airbnb: Nights Booked; Shopify: GMV | Revenue is directly transacted on the product |
| Engagement | `meaningful_action_frequency × breadth` | Meta: DAUs; Slack: Messages Sent | Ad-supported or network-effect product |
| Experience | `task_completion × satisfaction` | Netflix: Hours Streamed; Spotify: Time Listening | Consumption depth is the value |

Rejection rule: if the NSM grows while customer value does not (e.g., pageviews after re-theme), it is a vanity metric. Re-classify.

### AI-native product NSM (2026 caveat)

For LLM/agent products, **do not use raw token consumption as the NSM**. Token volume grows because the model is verbose, not because the product creates value. Common 2026 vanity traps to reject: tokens generated, completions returned, average prompt length, model calls per session.

Better candidates (one or two, never all):
- **Task-completion NSM** ("successful outcomes / week"): the share of agent runs where the user's intent is satisfied per a downstream eval (LLM-judge or rule-based). Pair with explicit success criteria.
- **Decision Velocity NSM**: time from user intent → trusted decision/action delivered. Useful for analytics copilots and dev tools.
- **Eval-aligned NSM**: an offline-eval pass rate (e.g., "% queries with grounded, cited answer") promoted as the user-facing NSM, so quality regression is visible to leadership.
- **Retained-value NSM** ("users completing ≥N satisfying agent runs in 7 days"): use when the product is consumption-oriented.

Always pair AI NSM with a **CFO-translatable lagging indicator** (revenue per task, retention lift, hours saved priced in $) — if you cannot translate the NSM to dollars within one quarter, it is still an internal dashboard, not a North Star. (Source: [Eric Weber — North star metrics for AI data products](https://ericdataproduct.substack.com/p/north-star-metrics-for-ai-data-products))

## Decomposition Formula

Generic form: `NSM = Users_Active × Action_Depth × Frequency × Quality_Multiplier`

| Product | NSM | Decomposition |
|---------|-----|---------------|
| Airbnb | Nights Booked | `(Guests) × (Bookings/Guest) × (Nights/Booking)` |
| Slack | Messages Sent (in teams ≥3) | `(Active Teams) × (Active Users/Team) × (Messages/User/Day)` |
| Zoom | Weekly Meeting Minutes | `(Hosts) × (Meetings/Host/Week) × (Avg Minutes/Meeting)` |
| Notion | Pages Edited/Week | `(Workspaces) × (Editors/Workspace) × (Pages/Editor/Week)` |

Input-metric rule: every factor must be **team-controllable** and have an owner. If no team can move it, it is an output, not an input.

## Counter and Guardrail Pairing

NSMs incentivize behavior; bad NSMs incentivize gaming. Always pair with:

| Pair Type | Purpose | Example |
|-----------|---------|---------|
| Counter Metric | Balances NSM pressure | NSM "Messages Sent" → Counter "Messages/User Over 7 Days" (prevent spam spikes) |
| Guardrail | Must-not-degrade threshold | Latency P95 < 200ms, Error Rate < 1%, CSAT ≥ 4.2 |
| Leading Indicator | Predicts NSM movement | Activation Rate, W1 Retention |
| Lagging Confirmation | Confirms NSM drove value | MRR, NRR, Customer LTV |

Anti-pattern: NSM without counter → team optimizes for the number, not the value. Facebook's early "DAU" had no quality counter; led to notification spam.

## Stability Contract

NSM changes should be **rare and structural**. Acceptable change triggers:

1. **Product pivot** (B2C → B2B, freemium → enterprise).
2. **Market redefinition** (new segment, new geography with different value).
3. **NSM-to-value drift** (metric moves up, revenue flat for 2+ quarters).

Never change NSM because:
- A campaign or feature launch did not move it (that's expected).
- Leadership wants a "cleaner number" (that's political).
- A new dashboard tool is easier with different metric.

Minimum commitment window: 6 months. Preferred: 12 months. Document the change in the NSM Registry with rationale, predecessor, and retention period for historical comparability.

## NSM Registry Template

```markdown
## NSM: [Name]
- **Definition**: [precise operational definition, including units]
- **Type**: Value Exchange | Engagement | Experience
- **Formula**: [decomposition]
- **Input Metrics (3-5)**: [team-owned drivers]
- **Counter Metric**: [prevents gaming]
- **Guardrails**: [must-not-degrade thresholds]
- **Owner**: [person / team accountable]
- **Measurement Window**: [daily | weekly | monthly]
- **Stability Commitment**: [start date] → [minimum end date]
- **Data Source**: [warehouse table / event name]
- **Known Gaming Vectors**: [how teams might gamble this]
```

## Anti-Patterns

| Anti-Pattern | Symptom | Fix |
|-------------|---------|-----|
| Multiple North Stars | "Our NSM is DAU, MRR, and CSAT" | Pick one; demote others to guardrails or output KPIs |
| Output as NSM | Revenue or MRR as NSM | Revenue is lagging; NSM should lead revenue by 1-3 quarters |
| Unmoveable NSM | No input metric team can influence this quarter | Decompose further until drivers are controllable |
| Vanity NSM | Total signups, total users, pageviews | Replace with active/engaged/retained variant |
| NSM Drift | Moves up, revenue flat 2+ quarters | Re-examine; value is leaking between NSM and revenue |
| NSM Churn | Changed 3 times in 12 months | Freeze for 6 months; build trust before iterating |

## Deliverable Contract

When `northstar` completes, emit:

- **NSM one-liner** (under 15 words, no jargon).
- **Decomposition tree** (NSM → 3-5 inputs → leading indicators → events).
- **Counter + guardrail pair** with thresholds.
- **Stability commitment** (start date, minimum end date, change-trigger criteria).
- **NSM Registry entry** (template above).
- **Gaming-vector audit** (how the metric could be gamed; detection plan).
- **Handoff targets**: `kpi` for tree expansion, `retention` for leading-indicator overlay, `dashboard` for visualization.

## References

- Amplitude — North Star Metric Playbook
- Reforge — Growth Loops and NSM framework (Brian Balfour)
- Sean Ellis — "Hacking Growth" NSM chapter
- Reid Hoffman / LinkedIn — Engagement NSM evolution
- Eric Weber (2026) — [North star metrics for AI data products](https://ericdataproduct.substack.com/p/north-star-metrics-for-ai-data-products) — argues against token-volume NSM for AI products
- LeanPivot (2025) — [Finding Your Agent's "North Star" Metric](https://leanpivot.ai/blog/finding-your-agents-north-star-metric/)
