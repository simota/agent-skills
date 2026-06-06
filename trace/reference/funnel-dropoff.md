# Funnel Drop-Off Analysis Reference

Purpose: Quantify where users abandon multi-step flows (signup, checkout, onboarding), identify the single highest-leverage step to fix, and produce cohort-sliced funnel comparisons that Pulse can track as KPIs and Experiment can A/B validate.

## Scope Boundary

- **trace `funnel`**: step-level conversion decomposition from session events, friction scoring, cohort slicing, drop-off root-cause narrative via session replay.
- **pulse (elsewhere)**: owns the funnel KPI definition, dashboard wiring, and long-term trend tracking. Trace supplies the drop-off evidence; Pulse owns the metric.
- **experiment (elsewhere)**: A/B validation of proposed fixes for the worst-drop step. Trace emits the hypothesis; Experiment designs the test.
- **echo (elsewhere)**: predicted drop-off points from persona walkthrough before real data. Funnel confirms or refutes.
- **palette (elsewhere)**: remediation for the highest-friction step once diagnosed.

## Workflow

```
DEFINE    →  specify funnel steps, ordering, required events, and time-window per step
          →  declare conversion goal (final step) and valid entry predicate

COMPUTE   →  per-step conversion rate, overall funnel conversion, time-to-convert p50/p90
          →  cohort slices (new vs returning, device, referrer, locale, cohort week)

RANK      →  friction score per step = drop-off-% * downstream-step-value
          →  identify the single highest-leverage step (max friction score)

INVESTIGATE →  fetch rageclick + dead-click signals on the worst step
            →  fetch replay samples of abandoners at that step (n>=30)

REPORT    →  step drop-off table, cohort comparison, narrative of WHY, handoff
```

## Funnel Step Schema

```yaml
funnel:
  name: "new_user_checkout"
  window: 30_minutes   # max elapsed time from step 1 to final step
  entry_predicate: "event == 'product_viewed' AND is_new_user == true"
  steps:
    - id: 1
      name: "product_view"
      event: "product_viewed"
      required_props: ["product_id"]
    - id: 2
      name: "add_to_cart"
      event: "cart_add"
      max_time_from_prev: 10_minutes
    - id: 3
      name: "checkout_start"
      event: "checkout_started"
    - id: 4
      name: "payment_submit"
      event: "payment_submitted"
    - id: 5
      name: "purchase_complete"
      event: "order_confirmed"
  goal_step: 5
```

Strict vs loose ordering matters. Strict funnels require steps in exact order; loose funnels allow reordering. E-commerce checkout is usually strict; feature-exploration funnels are usually loose. Default to strict and relax only when justified.

## Conversion Computation

```
step_conversion[i]    = count(reached_step_i) / count(reached_step_{i-1})
overall_conversion    = count(reached_goal) / count(entered_funnel)
drop_off_pct[i]       = 1 - step_conversion[i]
friction_score[i]     = drop_off_pct[i] * downstream_value[i]
```

`downstream_value[i]` weights later-step drop-offs higher because losing a user close to conversion is more costly than losing them at the top. Use revenue-per-goal or LTV for commerce; use activation probability for PLG.

## Cohort Slicing

Never report funnel numbers without at least one cohort split. Aggregated funnels hide the meaningful variance.

| Slice | When it matters | Typical signal |
|-------|-----------------|----------------|
| New vs returning | Onboarding friction hides inside new-user cohort | New-user conversion <0.5x returning = onboarding problem |
| Device (mobile / desktop / tablet) | Mobile-specific layout or touch issues | Mobile step-drop >20 percentage points worse than desktop |
| Referrer (organic / paid / direct / email) | Intent mismatch | Paid traffic converting <0.3x organic = bad landing fit |
| Locale / language | I18n or payment-method gaps | Non-default-locale drop at payment step |
| Cohort week | Recent regression vs historical baseline | Step drop worsening week-over-week |
| Persona (via Researcher) | Persona-specific friction | One persona dropping 2x others at a specific step |

Require n>=30 per cohort slice. Smaller cells are directional, not conclusive.

## Time-to-Convert Distribution

Median (p50) hides the tail. Always report p50 + p90 + p99.

- **Fast converters (p10-p50)**: the UX works for them — do not optimize for this group, they already converted.
- **Slow converters (p50-p90)**: the group that *might* convert with a fix — primary target for friction removal.
- **Tail (p90-p99)**: often bot traffic or multi-session conversions — filter and treat separately.

A funnel with p50=2min and p90=45min at the same step suggests two populations: quick-decide and research-heavy. Split the cohort rather than averaging.

## Baseline vs Experiment Comparison

When Experiment runs an A/B variant, Trace provides the behavioral diff beyond conversion rate:

- **Control vs variant step-conversion delta** at each step (not just overall).
- **Time-to-convert shift** — faster conversion can be as valuable as higher conversion.
- **Frustration signal delta** at the changed step (rage clicks, dead clicks).
- **New drop-off points introduced** by the variant (regression surface).

A variant that lifts overall conversion 2% while doubling rage-click rate on a later step is a false win — document the trade-off.

## Anti-Patterns

- Reporting overall funnel conversion without step-level decomposition — hides the step that actually matters.
- Optimizing the biggest drop-off without weighting by downstream value — fixing step 1 (50% drop) may be less valuable than fixing step 4 (20% drop on high-LTV users).
- Comparing funnels across time without holding cohort composition constant — seasonality, traffic-source mix, and campaign spend shift the mix.
- Using window=infinity — lets users "convert" days later and inflates conversion artificially; set a realistic window per funnel type.
- Aggregating across all devices / referrers / personas before slicing — the aggregate funnel hides the meaningful variance.
- Treating n<30 cohort slices as conclusive — directional signal only.
- Ignoring drop-off at the entry step (pre-funnel) — users who see the entry CTA but never click it are a drop-off Trace cannot see without a virtual step 0.

## Handoff

- **To Pulse**: funnel definition YAML, step conversion baselines, cohort slices — Pulse wires these as tracked KPIs and dashboards.
- **To Experiment**: highest friction-score step + proposed intervention + Hypothesis Readiness Score. If score >=7, emit `TRACE_TO_EXPERIMENT`.
- **To Palette**: step-level UX diagnosis (field validation timing, copy clarity, form field count, affordance issues) for the worst step.
- **To Voice**: placement for exit-intent or step-level micro-surveys at the worst drop-off step.
- **To Cast**: if a specific persona converts >=15% worse than expected, emit `TRACE_TO_CAST_DRIFT` with funnel evidence.
