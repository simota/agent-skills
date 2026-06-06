# Trust Signal Placement Reference

Purpose: Place trust signals — testimonials, logo bars, case studies, certifications, reviews, and scarcity/urgency — where they do the most conversion work without crossing into deceptive patterns. Trust is not a section; it is a distributed asset woven through every scroll stop. This reference covers signal shape/quantity/placement, strength hierarchy, and the line between honest urgency and dark patterns.

## Scope Boundary

- **Funnel `trust`**: trust-signal inventory, hierarchy, and placement across LP sections. Structural decisions about what proof goes where.
- **Prose (elsewhere)**: testimonial pull-quote editing, case-study narrative polish, certification/badge alt-text wording.
- **Growth (elsewhere)**: review-aggregation feed integration (G2 / Capterra / Trustpilot APIs), rich-result schema for stars, ongoing testimonial harvesting playbook.
- **Muse (elsewhere)**: testimonial card / logo bar / badge design tokens (spacing, border-radius, shadow, grayscale treatment).
- **Clause (elsewhere)**: legal review of claim substantiation, endorsement disclosure (FTC / consumer-protection compliance), testimonial contractual rights.

If the question is "what kind of proof goes in the hero and what goes after benefits?" → `trust`. If it's "is this testimonial claim substantiated under FTC guidelines?" → Clause. If it's "how do we pull live reviews from Trustpilot?" → Growth.

## Trust Signal Strength Hierarchy

Not all proof is equal. Rank by strength; place strongest where skepticism is highest.

| Rank | Signal | Strength | Why |
|------|--------|---------|-----|
| 1 | Specific outcome metric with named source | Strongest | "Company X cut close-time 42% in 90 days — VP Sales, Company X" is unfalsifiable-in-public |
| 2 | Named testimonial (photo + name + title + company) | Strong | Attribution makes the claim costly to fabricate |
| 3 | Video testimonial | Strong | Harder to fake; body language adds credibility |
| 4 | Case study with pre/post data | Strong | Long-form, checkable, but requires scroll commitment |
| 5 | Logo bar of well-known customers | Medium-strong | Social proof by association; quantity 6-12 is the sweet spot |
| 6 | User count ("Join 10,000+ teams") | Medium | Abstract but directional |
| 7 | Third-party review aggregation (G2 4.7 / 450 reviews) | Medium | Credible when sourced, weak when unsourced |
| 8 | Media mention logos ("As seen in TechCrunch") | Medium | Declining value over time as category-standard |
| 9 | Certification / compliance badge (SOC2, ISO 27001, GDPR) | Medium (context-dependent) | Strong for enterprise buyers, weak for consumer |
| 10 | Award / industry badge | Weak-medium | Degraded by badge proliferation |
| 11 | Anonymous testimonial ("J.S., Ohio") | Weakest | Suggests fabrication even when real |

**Rule:** use the strongest available signal for the highest-skepticism moment (hero fold, pricing section, final CTA). Degrade gracefully only after.

### GEO Signal Weight (Generative Engine Optimization, 2026)

The 2026 generative engines (ChatGPT, Perplexity, Claude, Gemini, Google AI Overviews) summarise LPs to answer queries elsewhere. The trust-signal hierarchy above maps roughly to **which signals are likely to survive the summarisation** and be quoted in the AI answer:

| GEO survival | Signal pattern | Reason |
|---------------|------------------|---------|
| Likely cited | Named testimonial with quantitative outcome (rank 1) + statistic with named source | The engine treats "[number] — [source]" as an extractable fact |
| Often cited | Third-party review aggregation with provider name (G2 / Trustpilot / Capterra rating) | Aggregator + score is parseable structured data |
| Rarely cited | Logo bar without context, vanity awards, anonymous testimonials | No verifiable string for the engine to lift |
| Hurts citation | Vague superlatives ("the leading…", "best-in-class") without attribution | Marketing-tone phrases get filtered out as boilerplate |

Practical rules for AI-citable trust signals:

- Pair every aggregate stat with the source ("`4.7` on G2 across `450` reviews" — not "`4.7` rating").
- Pair every customer outcome with `name + title + company + a number` so the AI engine has a verbatim citation candidate.
- Ship trust signals as plain text + structured data (`Review`, `AggregateRating`, `Organization` schema.org JSON-LD) — the engines parse both, but JSON-LD survives layout changes better than HTML scraping. See `growth/reference/...` for the schema fields.
- 2026 reference data point: sites present on `4+` review platforms are `~2.8x` more likely to appear in ChatGPT recommendations.

## Placement Map by LP Section

```
┌─────────────────────────────────────────────┐
│ HERO               │ Logo bar (6-8) OR user │
│                    │ count OR star rating   │
├─────────────────────────────────────────────┤
│ PAIN / PROBLEM     │ (usually none)         │
├─────────────────────────────────────────────┤
│ SOLUTION OVERVIEW  │ (usually none)         │
├─────────────────────────────────────────────┤
│ BENEFITS           │ 1 outcome-metric       │
│                    │ testimonial inline     │
├─────────────────────────────────────────────┤
│ SOCIAL PROOF       │ 3-5 named testimonials │
│                    │ + review aggregate     │
├─────────────────────────────────────────────┤
│ HOW IT WORKS       │ (usually none)         │
├─────────────────────────────────────────────┤
│ FEATURES           │ Certification badges   │
│                    │ (security/compliance)  │
├─────────────────────────────────────────────┤
│ PRICING            │ Guarantee badge +      │
│                    │ testimonial per plan   │
├─────────────────────────────────────────────┤
│ CASE STUDIES       │ 1-3 deep case studies  │
├─────────────────────────────────────────────┤
│ FAQ                │ (usually none)         │
├─────────────────────────────────────────────┤
│ FINAL CTA          │ Guarantee re-state +   │
│                    │ user count reminder    │
└─────────────────────────────────────────────┘
```

**Rule:** trust density peaks at decision moments (pricing, final CTA), not at the top. Frontloading all proof on the hero wastes it before the reader knows what's being sold.

## Testimonial Shape

Structure each testimonial as **Result → Challenge → Solution** (lead with the outcome).

### Template

```
"[Headline result / quote]"
— [Full name], [Title], [Company]
[Photo, 80-128px, circular or rounded]

Challenge: [one sentence]
Outcome: [metric-forward sentence]
```

### Example (strong)

> "We cut our monthly close from 12 days to 3." — Sarah Chen, VP Finance, Northwind Logistics
>
> Challenge: Month-end consumed 60% of finance team capacity. Outcome: 3-day close, 2 analyst hires avoided, $180k saved annually.

Contrast: "Great product! Really helped us. — Sarah C." says nothing, abbreviates attribution, and increases skepticism.

### Testimonial Quantity

| LP section | Quantity |
|-----------|----------|
| Hero fold | 0-1 (tight pull-quote) |
| Inline in benefits | 1-2 |
| Dedicated social-proof section | 3-5 |
| Pricing section | 1 per plan (optional) |
| Case studies section | 1-3 deep |

**Rule:** more than 5 testimonials in one block reads as overcompensation. Go deeper, not wider.

## Logo Bars (Social Proof / "As Seen In")

### Customer logo bar

- Placement: hero bottom-edge or immediately after hero as an anchor band.
- Quantity: 6-12 logos. Below 6 reads as sparse; above 12 reads as noisy.
- Treatment: grayscale / single-tone to keep visual hierarchy with the primary CTA. Full-color logos compete.
- Label: "Trusted by teams at" / "Powering" / "Chosen by" — concrete verb beats generic "Our customers".
- Rotation: if you have >12 strong logos, rotate 6-8 per page load rather than scroll-carousel (carousels are ignored).

### Media mention logo bar ("As seen in")

- Placement: separate from the customer logo bar. Mixing dilutes both.
- Treatment: same grayscale rule.
- Label with specificity when possible: "Featured in TechCrunch's Series-A watchlist, 2025" beats "As seen in TechCrunch".
- Staleness rule: drop media mentions older than 18 months unless they are category-defining.

## Case Studies

Case studies sit between testimonials (short) and long-form content (marketing site). Decide length by audience.

| Format | Length | Best for |
|--------|--------|----------|
| Metric-forward card | 1 screen, hero metric + 3 supporting numbers + pull quote | Executive / skim audience |
| Story-forward narrative | 400-800 words, challenge → approach → outcome arc | Considered-purchase, enterprise buyers |
| Hybrid | Metric card on LP linking to full narrative page | Default for B2B LP |

**Metric-forward template:** Logo + 3 headline numbers (e.g., `42% close-time reduction · 3-day timeline · $180k annual savings`) + pull quote + `Read full story` link.

**Story-forward template:** `HEADLINE` (transformation in one sentence) → `CHALLENGE` (metric-anchored) → `APPROACH` (specific features used) → `OUTCOME` (metric-anchored, time-bounded) → optional `LOOKING AHEAD`.

## Certifications, Badges, and Guarantees

### When they help

- **Enterprise buyers**: SOC 2, ISO 27001, HIPAA, GDPR badges genuinely shorten the sales cycle. Place near pricing and in the footer.
- **E-commerce**: money-back guarantee, secure-payment badge near checkout CTA. Lifts conversions 8-15%.
- **Regulated verticals (health, finance)**: required compliance badges near claims they substantiate.

### When they hurt

- Consumer LPs overloaded with "Award Winner 2019" / "Best of Web" badges — reads as defensive and dated.
- Badge clutter near the hero CTA competes for attention with the CTA itself.

**Rule:** badge quantity cap per section: 3. Badge size cap: no larger than the CTA button.

## Review Aggregation

When integrating third-party reviews (G2, Capterra, Trustpilot, App Store):

- Show source + aggregate score + review count: `★ 4.7 · 450 reviews on G2`.
- Link out to the source — unlinked stars trigger skepticism.
- Do not cherry-pick only 5-star reviews on the aggregation card; the aggregate score earns trust because it includes imperfect reviews.
- Refresh cadence: stale "250 reviews" next to a live source showing 1,200 is a trust-killer. Pull live or refresh quarterly.

## Scarcity and Urgency vs Deceptive Patterns

Scarcity and urgency are legitimate trust tools when honest. They become dark patterns when fabricated.

| Honest | Deceptive (avoid) |
|--------|-------------------|
| "Enrollment closes Friday — next cohort in March" (verifiably true) | Perpetual "Ends today" countdown that resets on page load |
| "4 seats remaining in the March cohort" (real inventory) | "Only 3 left!" on infinite-inventory SaaS |
| "Early-bird pricing through Oct 15" (real deadline with a real after-price) | "50% off — today only" repeating every day |
| Live attendance indicator driven by real data | Fake "17 people viewing" counter |
| Waitlist with real queue position | "Join 10,000 on the waitlist" when list is < 100 |

**Red lines** (never ship):

- Countdown timers that reset on refresh.
- "X people bought this in the last hour" notifications with randomized data.
- Pre-checked "Yes, send me marketing" boxes.
- Price anchoring to a never-actual "was" price.
- Hidden conditions that only surface at checkout.

**Rule:** if the scarcity message would be false when the user refreshes or comes back tomorrow, it is a dark pattern. Cut it.

## Anti-Patterns

- ❌ Anonymous testimonial with only initials and a state ("J.S., Ohio") — weaker than no testimonial.
- ❌ All testimonials from the same week / same industry — looks coordinated.
- ❌ Stock-photo headshots on testimonials (reverse-image search by a skeptic ends the deal).
- ❌ "Trusted by the world's best companies" with no logos beneath — empty claim.
- ❌ Full-color competing logos in the logo bar (fights the CTA for attention).
- ❌ Certification badges larger than the primary CTA.
- ❌ Fake countdown timers on evergreen offers.
- ❌ Review aggregate without a link to the source.
- ❌ Testimonial carousels that auto-rotate — users cannot re-read and skip entirely.
- ❌ Case studies with outcomes but no starting metrics (42% improvement from what?).
- ❌ Claiming certifications the product does not actually hold.

## Handoff

**To Prose** (copy polish):

- Raw testimonial quotes with attribution — Prose returns polished pull-quote editing while preserving original meaning.
- Case-study narrative drafts — Prose returns voice-aligned final wording.
- Badge alt-text for accessibility compliance.

**To Growth** (trust infrastructure):

- Review-aggregation source list (G2, Capterra, Trustpilot, App Store) — Growth wires live API integration and schema.org markup for rich results.
- Testimonial harvesting playbook cadence.
- Dark-pattern audit checklist for ongoing scrutiny.

**To Clause** (legal):

- Testimonial claims requiring substantiation (specific metrics, outcomes, named persons).
- Endorsement disclosure obligations (FTC, EU consumer protection).
- Certification badge usage rights (SOC 2 mark license terms, ISO re-certification deadlines).

**To Muse** (visual tokens):

- Testimonial card states (default / featured / with-video / compact).
- Logo bar spacing and grayscale treatment tokens.
- Badge size/placement tokens.
