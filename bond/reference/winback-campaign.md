# Win-Back Campaign Reference

Purpose: Recover cancelled or long-dormant users with a recency-weighted offer sequence, multi-touch cadence, and a reactivation metric tied to Pulse. Distinguishes voluntary from involuntary cancels.

## Scope Boundary

- **bond `winback`**: Cancelled / long-dormant user recovery (this document).
- **bond `reengagement` (elsewhere)**: Still-active dormant user re-activation. Default. Winback is a deeper recovery path.
- **bond `churn` (elsewhere)**: Churn prevention *before* cancellation.
- **Growth (elsewhere)**: New-user acquisition campaigns. Winback is recovery, not acquisition.
- **Prose (elsewhere)**: Campaign copy (`notification`). Winback designs the plan; Prose writes the words.
- **relay (elsewhere)**: Delivery infrastructure.
- **Pulse (elsewhere)**: Reactivation metric and funnel reporting.

## Voluntary vs Involuntary Cancels

```
Involuntary (payment / card failure)  →  Route to dunning first
                                         Clean card issue, attempt re-charge
                                         Separate from winback flow

Voluntary (active choice to leave)    →  Winback candidate
                                         Segment by cancel reason
                                         Apply recency-weighted offer
```

Dunning handles involuntary. Winback handles voluntary only.

## Recency Cohorts

| Cohort | Days since cancel / dormant | Offer strength | Cadence |
|--------|----------------------------|----------------|---------|
| Fresh | 0-14 days | Soft (content, feature reminder) | Light touch, 1-2 emails |
| Warm | 15-30 days | Medium (discount ≤20%, free month) | 3 emails + 1 push |
| Cool | 31-90 days | Strong (discount 30-50%, new feature hero) | 4-5 touches across channels |
| Cold | 91-180 days | Hero (50%+ off or credits) | Final push + quiet |
| Frozen | >180 days | Minimal last attempt | 1 email, then stop |

Rule: **offer strength scales with recency inverse** — stronger for colder. Acquisition-level economics apply to cold winback.

## Segmentation Dimensions

For each recency cohort, further segment by:

1. **Cancel reason** (if captured): price / features / unused / support / switched competitor.
2. **Plan tier at cancel**: free / paid-base / paid-premium / enterprise.
3. **Lifetime value at cancel**: LTV tier (top / mid / low).
4. **Engagement peak**: power user vs. casual vs. never-activated.
5. **Primary use case**: what feature they used most.
6. **Channel preference**: email-only / push-allowed / SMS opted-in.

Never send the same message to all cohorts. A power user who left for price needs different copy than a never-activated user who left for lack of understanding.

## Offer Design

| Cancel reason | Recommended offer |
|---------------|-------------------|
| Price / cost | Discount (scaled to cohort), longer billing period, annual at monthly price |
| Missing features | "We built it" announcement + early access if relevant |
| Didn't see value / underused | Onboarding reset + human help offer + success-story share |
| Support issue | Apology + credit + named CSM / concierge onboarding |
| Switched competitor | Migration assistance + data import + differentiator highlight |
| Lifecycle (no longer needed) | Pause option, archive, come-back-anytime landing |
| Unknown | Soft touch, value reminder, low-friction return path |

Avoid: bribes with no context, identical discount for everyone, discount that undercuts current paying users' price.

## Multi-Touch Cadence Example (Warm cohort, price objection)

```
Day 0   (cancel)   : offboarding email confirming cancel, low-key "come back" link
Day 3   : value reminder email — top 3 features they used
Day 7   : offer — "30% off for 3 months, start where you left off"
Day 14  : feature-launch push (if relevant release since cancel)
Day 21  : final soft touch email — success story from similar user
Day 30  : stop cadence; move to Cool cohort if no return

Quiet period: 60 days before any further contact
```

Frequency cap: no more than 1 marketing touch / 3 days in winback.

## Deliverability and Suppression

- **Global suppression**: honored-opt-out list never gets winback.
- **Complaint list**: spam-reporters never get winback.
- **Hard-bounce list**: invalid addresses suppressed.
- **Winback fatigue suppression**: user who's been through 2 full winback cycles without returning → 180-day cooldown.
- **Regulatory**: CAN-SPAM (unsubscribe ≤ 10 business days), GDPR (legitimate interest balancing test), CASL Canada (consent required), Japan APPI.

Route compliance checks to Cloak/Oath for regulated regions.

## Reactivation Metric

```
Reactivation Rate = returned_users / winback_recipients (per cohort, per campaign)
```

Benchmarks (typical SaaS):
- Fresh cohort: 15-30%
- Warm: 8-15%
- Cool: 3-8%
- Cold: 1-3%
- Frozen: <1%

Downstream: track LTV of reactivated users vs original LTV. Sticky reactivation means reactivated LTV ≥ 60% of original. Lower than that suggests price-incentive-only returns who churn again.

## Offer Cannibalization Check

Before shipping a winback offer, verify:
- [ ] Current paying users cannot easily discover and exploit the winback discount.
- [ ] Serial cancel-rejoin gaming is rate-limited (one winback offer per 365 days).
- [ ] Offer does not undercut a more expensive plan and drive current users to downgrade.

## Output Template

```markdown
## Win-Back Campaign: [Name]

### Target Segment
- **Recency cohort**: [Fresh / Warm / Cool / Cold / Frozen]
- **Size**: [N users]
- **Primary cancel reason**: [price / features / etc.]
- **Secondary segmentation**: [plan tier, LTV tier, channel preference]

### Offer
- **Type**: [discount / extended trial / feature access / migration help / pause]
- **Strength**: [% or value]
- **Duration**: [days / months]
- **Justification**: matched to cancel reason and cohort economics

### Cadence
| Day | Channel | Content goal | CTA |
|-----|---------|--------------|-----|
| 0 | email | offboarding confirm | "we'll be here" |
| 3 | email | value reminder | "see what's new" |
| 7 | email | offer | "[offer CTA]" |
| ... | ... | ... | ... |

### Compliance
- [ ] Global suppression respected
- [ ] Hard-bounce / complaint lists applied
- [ ] Unsubscribe ≤ 10 business days
- [ ] Regional regulation verified (CAN-SPAM / GDPR / CASL / APPI)

### Metrics
- **Primary**: Reactivation rate (benchmark: [cohort-specific])
- **Secondary**: Reactivated-user 90-day retention, reactivated LTV vs original
- **Guardrail**: current-user cannibalization < 1%, unsubscribe rate < 2%

### Handoffs
- Prose `notification`: copy per touch
- relay: email / push / SMS delivery
- Pulse: reactivation event + funnel
- Experiment: A/B test offer strength and copy
- Cloak / Oath: regulatory review
- Growth: ensure no overlap with active promos
```

## Anti-Patterns

| Anti-pattern | Fix |
|--------------|-----|
| Winback to users who reported spam | Honor complaint list |
| Same discount for everyone | Segment by cancel reason |
| Aggressive SMS without opt-in | Email-only for non-opted cohorts |
| Winback discount leaks to active users | Plug the leak before campaign |
| No LTV analysis post-reactivation | Measure reactivated-LTV to avoid price-only returns |
| Forever-on winback cadence | Hard stop at cohort end; 60-day quiet |
| Winback on dunning-side cancel | Fix dunning first |

## Deliverable Contract

When `winback` completes, emit:

- **Segment definition** (recency cohort × reason × tier × LTV × channel).
- **Offer design** matched to cohort and reason.
- **Cadence table** (day × channel × content × CTA).
- **Compliance checklist** (suppression, regulation, unsubscribe).
- **Metrics plan** (reactivation rate, 90-day retention, LTV, guardrails).
- **Cannibalization check**.
- **Handoffs**: Prose, relay, Pulse, Experiment, Cloak/Oath, Growth.

## References

- Reforge — Winback Playbook
- Andrew Chen — "The Cold-Start Problem" (cohort recovery)
- Sean Ellis — *Hacking Growth* (winback loops)
- CAN-SPAM / GDPR / CASL / APPI regulatory references
- Customer.io, Braze, Iterable — winback automation patterns
- SaaS Metrics Benchmarks (OpenView, KeyBanc) — reactivation rates by recency
