# Lifecycle Email Drip Reference

Purpose: Design trigger-based, behavior-branched email drip covering the full user lifecycle — onboarding (Day 0-30), activation reminders, milestone celebrations, dormancy triggers, and winback. Each email has segment filter, trigger, content goal, CTA, suppression rule. Includes deliverability and consent compliance.

## Scope Boundary

- **bond `lifecycle-email`**: Full lifecycle email drip design (this document).
- **bond `reengagement` (elsewhere)**: Dormant re-engagement tactics. Lifecycle includes but is broader than re-engagement.
- **bond `winback` (elsewhere)**: Cancelled/long-dormant recovery. Lifecycle is active-user nurture; winback is recovery.
- **Prose `notification` (elsewhere)**: Copy authoring per email. Lifecycle designs the *plan*; Prose writes the *words*.
- **relay (elsewhere)**: Email delivery infrastructure.
- **Pulse (elsewhere)**: Funnel / open / click metrics.
- **Growth (elsewhere)**: Acquisition and top-of-funnel nurture.
- **Cloak / Oath (elsewhere)**: GDPR / CAN-SPAM / CASL / APPI compliance.

## Lifecycle Stages

```
Signup  →  Onboarding  →  Activation  →  Habit  →  Power User  →  Churn Risk  →  Winback
  0           0-30d          7-30d       30d+       60d+            signals      cancelled
```

Each stage has its own email drip purpose:

| Stage | Goal | Email density |
|-------|------|---------------|
| Welcome (D0) | Confirm + orient + 1 CTA | 1 email |
| Onboarding (D1-30) | Guide to activation | 3-6 emails, decreasing density |
| Activation reminder | Nudge stuck users | Behavior-triggered |
| Milestone celebration | Reinforce progress | Triggered on milestone |
| Habit reinforcement | Build cadence, highlight new features | Weekly / bi-weekly |
| Churn risk | Save before cancel | Triggered by signal |
| Post-cancel | Confirm + door open | 1 email |
| Winback (separate) | Recover cancelled | see `winback` |

## Email Contract per Touch

Each email specifies:

```markdown
### Email: [internal name]
- **Trigger**: [event / time / behavior condition]
- **Segment filter**: [who gets this]
- **Suppression rule**: [who does not get this]
- **Content goal**: [1 sentence — what mindset change]
- **Subject**: [subject line ≤ 50 chars]
- **Preheader**: [preheader ≤ 100 chars]
- **Primary CTA**: [verb-led, 2-4 words]
- **Secondary action**: [optional, text link]
- **Send time window**: [local time + day of week]
- **Max frequency**: [cap across all lifecycle email]
- **Exit condition**: [when user removed from this drip]
```

## Onboarding Drip Template (Day 0-30)

| Day | Trigger | Segment | Content goal | Primary CTA |
|-----|---------|---------|--------------|-------------|
| 0 (immediate) | signup_completed | all new users | welcome + first action | "Set up profile" |
| 1 | no first_value_action by D1 | activated=false | push toward aha-moment | "Create first X" |
| 3 | activated=false | activated=false | social proof + shortcut | "Try the example" |
| 7 | activated=false | activated=false | human help offer | "Book a demo" |
| 7 | activated=true | activated=true | next milestone | "Invite a teammate" |
| 14 | any | activated=true, stuck at M1 | next feature | "Try [feature]" |
| 21 | any | active | monthly summary preview | "See your stats" |
| 30 | any | all survivors | milestone + request feedback | "Take survey" |

Rule: if user activates between D1-D7, drop them off the "stuck" branch and move to the activated branch.

## Behavior Branching

Drip paths split based on events:

```
        signup_completed
              │
              ▼
         welcome D0
              │
      ┌───────┴───────┐
      ▼ activated     ▼ not activated by D1
 activated drip      stuck drip (D1, D3, D7 stuck messages)
      │               │
      ▼ activates?    ▼
  continue in       merges back if activated
  activated drip    otherwise → dormancy drip
```

At any point, a user can flow between drips based on events. A mature lifecycle engine tracks user state and routes accordingly.

## Suppression Rules

A user receives an email only if ALL these pass:

- [ ] Has valid email (not bounced hard).
- [ ] Not on global suppression / complaint list.
- [ ] Opted in (per channel + per jurisdiction).
- [ ] Email frequency < cap (usually ≤ 3 per week).
- [ ] Not currently in an active support ticket (for marketing emails).
- [ ] Email type aligned with user's channel preference.
- [ ] Not in quiet hours (by timezone).

## Frequency Cap

| Cap type | Typical value |
|----------|---------------|
| All marketing emails / week | 2-3 |
| All lifecycle + transactional / day | 4 |
| Per single trigger type / week | 1 |
| After-hours send | never (default), unless time-sensitive |

Exceeding caps → skip lower-priority email or defer to next send window.

## Deliverability Contract

Required infrastructure:

- **SPF** record set for sending domain.
- **DKIM** signing enabled.
- **DMARC** policy published (at minimum `p=none` with reporting, preferably `p=quarantine` or `p=reject`).
- **BIMI** (optional but growing — visual trust signal).
- **Warm-up**: new sending domain ramped over 2-4 weeks.
- **Feedback loops**: Gmail, Microsoft, Yahoo postmaster tools integrated.
- **List hygiene**: remove hard bounces immediately; soft-bounce threshold (3 consecutive → suppress).
- **Complaint rate**: keep < 0.1% (Gmail aggressive threshold).
- **Engagement signal**: low engagement → send less frequently to preserve sender reputation.

## Consent Compliance

| Jurisdiction | Rule |
|--------------|------|
| US (CAN-SPAM) | Unsubscribe ≤ 10 business days, physical address required, no deceptive subject |
| EU (GDPR + ePrivacy) | Opt-in required for marketing, legitimate-interest possible for transactional, unsubscribe 1-click |
| Canada (CASL) | Express consent required, sender identification, unsubscribe 10 business days |
| Japan (APPI + 特定電子メール法) | Opt-in required, sender identification, unsubscribe honored 3 business days |
| California (CCPA/CPRA) | Do Not Sell / Share, GPC honor |
| Brazil (LGPD) | Consent required, DPO contact |

Coordinate with Cloak (privacy engineering) and Oath (regulatory audit) for regulated regions.

## Metrics per Drip

| Metric | Typical target |
|--------|----------------|
| Delivered rate | ≥ 98% |
| Open rate | 15-30% (varies by industry) |
| Click-through rate (CTR) | 2-5% |
| Click-to-conversion | 15-40% of clicks |
| Unsubscribe rate per email | < 0.5% |
| Spam complaint rate | < 0.1% |
| Drip-end activation uplift | measured vs control (holdout group) |
| Day-30 retention lift | A/B vs no-drip control |

Reserve a 5-10% holdout group (no lifecycle emails) to measure incrementality.

## Output Template

```markdown
## Lifecycle Email Drip: [Audience]

### Lifecycle Stage Coverage
- [x] Welcome
- [x] Onboarding (D0-30)
- [x] Activation reminder
- [ ] Habit reinforcement
- [ ] Churn risk save
- [x] Post-cancel confirm

### Drip Table
| # | Day/Trigger | Segment | Suppression | Subject | Primary CTA | Exit condition |
|---|-------------|---------|-------------|---------|-------------|----------------|
| 1 | D0 | new signup | hard-bounce | "..." | "..." | signup completed |
| 2 | D1 activated=false | stuck | ... | ... | ... | activates or D7 |
| ... | ... | ... | ... | ... | ... | ... |

### Branching Logic
- [ ] Activated users route to habit drip
- [ ] Non-activated users route through stuck drip
- [ ] Churn-risk signals trigger save drip
- [ ] Cancelled users exit lifecycle, enter winback cohort

### Compliance
- [ ] SPF/DKIM/DMARC configured
- [ ] Unsubscribe ≤ 10 bus days
- [ ] Physical address in footer (CAN-SPAM)
- [ ] Opt-in verified for EU/Canada/Japan
- [ ] Channel preferences respected

### Frequency Caps
- Marketing emails / week: 2-3
- Total emails / day: 4
- Per trigger / week: 1

### Holdout / Measurement
- **Holdout size**: [% of cohort, typically 5-10%]
- **Primary metric**: [activation / retention / revenue — with uplift target]
- **Measurement window**: [days]

### Handoffs
- Prose `notification`: copy each email (subject + preheader + body + CTA)
- relay: delivery, tracking, bounce handling
- Pulse: drip-level funnel + primary metric
- Experiment: A/B test copy, subject lines, timing
- Cloak / Oath: regulatory review for launched regions
- Scaffold: domain + DNS setup
```

## Anti-Patterns

| Anti-pattern | Fix |
|--------------|-----|
| Everyone gets same sequence | Segment by activation state, plan, persona |
| Sending to hard-bounced addresses | Suppress immediately |
| No holdout to measure incrementality | Reserve 5-10% no-email holdout |
| Ignoring timezone → 3am sends | Send-time optimization per user timezone |
| No frequency cap across drips | Cap total marketing exposure / week |
| Transactional + marketing in one send | Split addresses and reputation |
| Sunset policy missing for inactive | Remove unengaged subscribers after N months to protect reputation |
| Subject lines in ALL CAPS | Spam filter trigger |
| Single-sender IP for everything | Separate IPs for transactional vs marketing |

## Deliverable Contract

When `lifecycle-email` completes, emit:

- **Lifecycle stage coverage** checklist.
- **Drip table** (day × segment × suppression × subject × CTA × exit).
- **Branching logic** (how users flow between drips).
- **Compliance checklist** per jurisdiction.
- **Frequency caps** and quiet-hours rule.
- **Holdout plan** for incrementality measurement.
- **Metrics per drip** with targets.
- **Handoffs**: Prose, relay, Pulse, Experiment, Cloak/Oath, Scaffold.

## References

- Customer.io, Braze, Iterable, HubSpot — lifecycle marketing platforms
- CAN-SPAM / GDPR / CASL / APPI / LGPD regulatory references
- Mailchimp / Litmus — subject line and preheader benchmarks
- Google / Microsoft / Yahoo postmaster tools
- MarketingSherpa / Campaign Monitor — industry benchmark reports
- Sean Ellis — *Hacking Growth* (lifecycle email examples)
- Reforge — Lifecycle Marketing course
