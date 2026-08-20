# Power User Advocacy Reference

Purpose: Identify the 10-20% of users driving disproportionate engagement and revenue, build an advocacy ladder (active → advocate → referrer → community leader), and activate them through community, referral mechanics, and early-access programs.

## Scope Boundary

- **bond `power-user`**: Power-user identification and advocacy activation (this document).
- **bond `loyalty` (elsewhere)**: Points / tier / reward programs. Power-user is earn-through-behavior; loyalty is earn-through-spend.
- **Voice (elsewhere)**: NPS survey and promoter signals. Power-user consumes Voice's promoter data.
- **Growth (elsewhere)**: Referral mechanics and viral loops. Power-user feeds high-intent candidates into Growth's referral system.
- **Pulse (elsewhere)**: L21+ MAU bucket metrics and overlap analysis.
- **Prose (elsewhere)**: Advocacy program copy.

## Identification Rubric

Combine behavioral + sentiment signals:

```
Power User = (Behavioral signal) ∩ (Sentiment signal) ∩ (Tenure signal)
```

### Behavioral signal (pick any top-quartile)

| Signal | Threshold |
|--------|-----------|
| L21+ MAU bucket (days active in 30-day window) | ≥ 21 days |
| Power User Curve position | top 20% of MAU by engagement |
| Feature breadth | uses ≥ N features (product-specific) |
| Workflow depth | completes multi-step flows frequently |
| Usage volume | top quartile of core action count |

### Sentiment signal

| Signal | Threshold |
|--------|-----------|
| NPS promoter (score 9-10) | Yes |
| Explicit opt-in to testimonial / beta | Yes |
| Verified positive review (G2, Capterra, App Store) | Yes |
| Referred 1+ users organically | Yes |

### Tenure signal

| Signal | Threshold |
|--------|-----------|
| Active ≥ 90 days | filter out new-user enthusiasm |
| No recent churn signal | not in cancel flow |

**Power User identification**: user meets ≥ 1 behavioral + ≥ 1 sentiment + tenure ≥ 90d.

## Advocacy Ladder

```
        Active
          │  sustained engagement
          ▼
       Advocate           (talks about product, replies to reviews, testimonial opt-in)
          │  visible advocacy
          ▼
       Referrer           (actively refers new users, shares signup link)
          │  measurable invite conversions
          ▼
  Community Leader        (runs meetup, writes content, answers questions in community)
```

Not every Active becomes a Leader. Design the ladder with increasing effort + reward per step and clear next-action per tier.

## Per-Tier Activation Triggers

| Tier | Activation trigger | Invitation content |
|------|-------------------|--------------------|
| Active | Meets identification rubric | "You're in the top 20%" — acknowledge, early-access invite |
| Advocate | Opts into testimonial, answers ≥ 2 support questions for others | Swag, beta invite, private Slack channel |
| Referrer | Shares referral link via in-product sharing | Referral bonus (credits, service months) |
| Community Leader | Runs events / writes content / moderates | Stipend, co-marketing, advisory role |

Each step is earned by observed behavior, not claimed. Avoid self-nomination — actions > intent.

## Activation Program Elements

| Element | Tier |
|---------|------|
| Private community (Slack / Discord / forum) | Advocate+ |
| Early-access beta | Advocate+ |
| Quarterly feedback call with PM | Advocate+ |
| Swag | Advocate (branded), Leader (premium) |
| Referral program with financial reward | Referrer |
| Named in release notes / case study | Advocate+ |
| Conference speaking slot, co-marketing | Leader |
| Stipend / contract for community work | Leader |

## Referral Mechanics

For the Referrer tier:

- **Share link** with unique attribution token.
- **Reward both sides** (friend + referrer) — the dual-side incentive drives much higher conversion than one-side.
- **Reward shape**: account credit, extended subscription, premium feature unlock (not cash — cash attracts fraud).
- **Reward trigger**: referee reaches activation threshold (not just signup) — prevents gaming.
- **Fraud guard**: rate-limit referrals per user, verify payment method uniqueness, block known fraud networks.
- **Leaderboard** (optional): top referrers public if opted-in; provides social status.

Benchmark referral rates (Viral K-factor):
- K < 0.5 → referral is supplemental, not driving growth
- K 0.5-1.0 → meaningful contribution
- K ≥ 1.0 → viral growth engine

## Metrics

| Metric | Definition | Target |
|--------|-----------|--------|
| Power user identification count | Users meeting rubric | 10-20% of MAU |
| Advocacy ladder distribution | # per tier | Pyramid (Active >> Advocate > Referrer > Leader) |
| Advocate opt-in rate | % of identified Actives opting in | 30-50% |
| Referral K-factor | Avg invites × conversion rate | depends on product |
| Referred-user LTV | vs non-referred | ≥ 1.5x |
| Community activity | active members / week | growing |
| Advocate-to-churn rate | Should be < baseline churn | 50% of baseline |

## Segmentation for Power Users

Don't treat all power users the same:

- **B2B admin vs end-user**: admin is the decision-maker; end-user is the champion. Different activation.
- **Industry / vertical**: healthcare power users act differently from SaaS dev tool power users.
- **Plan tier**: enterprise power users demand different handling than free-tier.
- **Region**: community events and swag logistics differ by region.

## Output Template

```markdown
## Power User Advocacy Plan

### Identification
- **Behavioral signal**: [chosen metric + threshold]
- **Sentiment signal**: [NPS / opt-in / review]
- **Tenure signal**: ≥ 90 days active
- **Current identified power users**: [count, % of MAU]

### Advocacy Ladder
| Tier | Count | Criteria | Next-step trigger |
|------|-------|----------|-------------------|
| Active | [N] | rubric met | ... |
| Advocate | [N] | testimonial opt-in + helping others | ... |
| Referrer | [N] | shared link, ≥1 activated referee | ... |
| Leader | [N] | community work | ... |

### Activation Programs
- [ ] Private community (tier: Advocate+)
- [ ] Beta early-access (tier: Advocate+)
- [ ] Quarterly PM feedback call (tier: Advocate+)
- [ ] Referral program with dual-side reward (tier: Referrer)
- [ ] Community Leader stipend (tier: Leader)
- [ ] Swag ladder (per tier)

### Referral Program (if Referrer tier activated)
- **Reward shape**: [credits / service months / feature unlock]
- **Reward trigger**: referee reaches activation, not just signup
- **Fraud guards**: [rate limits, unique payment, fraud detection]
- **Attribution**: unique link, UTM, in-product share

### Metrics
- **Primary**: Referral K-factor
- **Secondary**: Advocate-to-churn ratio (vs baseline), referred-LTV uplift
- **Guardrail**: referral fraud rate < 1%, power-user burnout rate < 5%

### Handoffs
- Voice: NPS promoter signal
- Growth: referral-loop mechanics and viral-growth measurement
- Pulse: L21+ bucket + identification event
- Prose: advocacy-invite and referral copy
- Experiment: test activation thresholds and rewards
- Scribe: community code of conduct
```

## Anti-Patterns

| Anti-pattern | Fix |
|--------------|-----|
| Inviting new signups to be "power users" | Require ≥ 90-day tenure |
| Self-nomination into advocacy | Require observed behavior |
| Cash referral rewards | Credits / service months (fraud-resistant) |
| One-sided referral reward | Reward both sides |
| Referral reward on signup, not activation | Wait for activation threshold |
| Public leaderboard without opt-in | Always opt-in before public attribution |
| Ignoring advocate burnout | Monitor engagement health; rotate community leaders |
| Treating admin and end-user the same | Segment B2B by role |

## Deliverable Contract

When `power-user` completes, emit:

- **Identification rubric** (behavioral × sentiment × tenure).
- **Advocacy ladder** with counts per tier and next-step triggers.
- **Per-tier activation programs**.
- **Referral mechanics** (if Referrer tier active) with reward shape, trigger, fraud guards.
- **Metrics plan** (K-factor, advocate churn, referred LTV, guardrails).
- **Handoffs**: Voice, Growth, Pulse, Prose, Experiment, Scribe.

## References

- a16z — "Power User Curve"
- Sarah Tavel — "Enduring vs Non-Enduring" (power-law engagement)
- Reforge — Community-Led Growth course
- Sangeet Paul Choudary — *Platform Scale* (two-sided power users)
- Brian Balfour — Growth Loops and referral K-factor
- AppsFlyer / Branch — Referral fraud detection patterns
- Dropbox, Airbnb, PayPal — classic dual-side referral case studies
