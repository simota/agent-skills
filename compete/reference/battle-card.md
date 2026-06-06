# Battle Card Design Reference

Purpose: Sales-enablement one-pager that equips reps with head-to-head positioning, objection handling, and "why we win / why we lose" narratives for a specific competitor. Battle cards convert raw competitive intelligence into deal-winning ammunition at the moment of need (discovery call, demo, late-stage objection).

## Scope Boundary

- **compete `battle`**: design and govern battle cards as living artifacts — structure, freshness rules, distribution, win-rate measurement.
- **compete `matrix` (default, elsewhere)**: feature comparison matrix across N competitors — input to battle cards, not a substitute.
- **compete `swot` (elsewhere)**: strategic SWOT for executive decisions — battle cards are tactical, SWOT is strategic.
- **compete `positioning` (elsewhere)**: positioning maps and category design — battle cards operationalize the positioning, they do not invent it.
- **compete `winloss` (elsewhere)**: post-deal interviews. Win/loss feeds the "why we win / why we lose" sections; do not author them from internal opinion.
- **voice (elsewhere)**: real customer feedback. Use Voice quotes as battle card evidence; do not synthesize testimonials.
- **researcher (elsewhere)**: empirical user-research interviews. Researcher informs persona-fit talking points; battle cards are not research artifacts.
- **plea (elsewhere)**: synthetic-user assumption challenge. Plea stress-tests battle card claims that lack real-world validation.

## Workflow

```
INTAKE   →  pick one competitor; confirm tier (direct/indirect/substitute)
         →  pull win/loss themes, deal review notes, recent product moves

DRAFT    →  fill one-pager template (overview, why we win, why we lose,
            objections, traps, landmines, proof, pricing posture)
         →  every claim cites a source (URL, deal ID, quote attribution)

REVIEW   →  product validates feature claims; sales validates objection realism
         →  legal reviews competitor-naming risk before external use

DISTRIBUTE → embed in CRM (deal-stage triggered), pre-call brief, deal room
           → announce in sales standup; train via role-play once per quarter

GOVERN   →  90-day max freshness; weekly micro-updates on competitor moves
         →  measure adoption + win-rate lift; sunset cards below threshold
```

## One-Pager Structure

| Section | Content | Length |
|---|---|---|
| Header | Competitor name, tier, last-updated date, owner, version | 1 line |
| TL;DR | 3-bullet positioning (when we win, when we lose, when to disqualify) | 3 bullets |
| Why We Win | 3-5 differentiators with proof (metric, customer quote, demo step) | <=5 bullets |
| Why We Lose | 2-4 honest weak spots with mitigation play | <=4 bullets |
| Objection Handling | Top 5 competitor talking points + our reframe | 5 pairs |
| Landmines | Questions to ask the prospect that expose competitor gaps | 3-5 questions |
| Traps to Avoid | Topics where we lose if we engage (do-not-debate list) | 2-4 items |
| Pricing Posture | Their list, discounting behavior, our counter-offer guidance | 1 paragraph |
| Proof Points | 2-3 named wins, public case studies, third-party reviews | <=3 references |
| Source Footer | URLs with access dates, internal deal IDs, win/loss quotes | full citations |

## Objection-Handling Pairs

Every battle card must include the top 5 objections in `Their Claim -> Our Reframe -> Proof` triples. Examples:

| Their Claim | Our Reframe | Proof |
|---|---|---|
| "We have 2x more integrations" | "Integration count != integration depth — our top 20 cover 95% of customer use" | Integration usage data, customer quote |
| "We are cheaper" | "TCO including implementation, training, and downtime is 30% lower with us" | TCO calculator, named customer ROI |
| "We are the market leader" | "Leader in legacy segment; we lead the modern AI-native segment" | Analyst quadrant, growth-rate comparison |

Pair authoring rule: never refute without proof. Refutation without evidence trains reps to lose credibility.

## Freshness Governance

| Trigger | Action | Owner | SLA |
|---|---|---|---|
| Competitor pricing-page change | Update pricing posture section | CI lead | 24h |
| Competitor product launch / release notes | Update why-we-win + objection pairs | CI + PM | 72h |
| Competitor funding / M&A | Update header context + strategic note | CI lead | 1 week |
| New named win against competitor | Add proof point; refresh testimonial | Sales ops | 1 week |
| New named loss to competitor | Update why-we-lose + landmines | CI + sales | 2 weeks |
| Quarterly review | Full re-validation, retire stale claims | CI lead | 90 days max |

Freshness rule: any battle card untouched for 90 days is auto-flagged stale and pulled from active distribution until refreshed. Stale cards destroy rep trust faster than no cards.

## Distribution to GTM

| Channel | Format | When triggered |
|---|---|---|
| CRM deal record | Sidebar card linked to competitor field | Stage = "Discovery" with competitor identified |
| Pre-call brief | Slack/email digest summarizing the card | T-24h before call when competitor in opportunity |
| Deal room (late stage) | Linked PDF + objection FAQ | Stage = "Negotiation" |
| Sales enablement LMS | Module + role-play scenario | New-hire onboarding + quarterly recerts |
| Slack #competitive channel | Micro-update post on each refresh | Every change event |

Embedding rule: battle cards delivered in the rep's existing workflow (CRM, Slack, deal room) achieve ~85% adoption; standalone wiki pages achieve ~30%. Author for the consumption context.

## Win-Rate Measurement

Tag every competitive deal in CRM with `competitor_present`, `battle_card_used`, and `outcome`. Compute the lift formula:

```
win_rate_lift = win_rate(card_used) - win_rate(card_not_used)
```

Healthy program targets: +5 to +10 percentage points within 2-3 quarters; battle card users report up to 30% win-rate increase in mature programs. Adoption thresholds: <40% = content quality issue; 60-70% = healthy; >80% = excellent.

## Anti-Patterns

- Outdated cards in active circulation — anything past 90 days erodes rep trust. Auto-sunset stale cards rather than pretend currency.
- Sales-only authoring — without product/CI input, claims drift into sales fiction and break in technical evaluations.
- Marketing-only authoring — overweight branding language, underweight tactical objection handling.
- No win-rate measurement — without `battle_card_used` tagging, the program cannot prove ROI and gets defunded.
- "Everything is a differentiator" — listing 15 why-we-wins dilutes the top 3. Force a 5-bullet cap.
- Refutation without proof — every objection reframe needs a source or it teaches reps to bluff.
- No "why we lose" section — pretending the competitor has no strengths makes the card useless in honest conversations and trains reps to freeze when objections land.
- One-time launch, no governance — battle cards are living artifacts, not deliverables. Without an owner and refresh cadence, they decay within a quarter.
- Universal card per competitor — segment cards by deal-size or vertical when objections diverge significantly (SMB vs enterprise objections rarely overlap).

## Handoff

- **To Voice**: pull customer quotes for proof points and testimonial validation. Voice owns the source-of-truth quote library.
- **To Researcher**: when objections lack empirical backing, hand off for moderated user/customer interviews to validate the reframe.
- **To Helm**: if win/loss patterns reveal a structural strategic gap (e.g., losing the entire enterprise tier), escalate to Helm for strategic simulation.
- **To Spark**: when "why we lose" patterns repeatedly cite a missing capability, route as a feature idea with competitive evidence attached.
- **To Growth**: when objections center on brand authority or category framing, route positioning fixes to Growth.
- **To Lore**: validated objection-handling patterns that work across multiple competitors become reusable institutional knowledge.
