# Before-After-Bridge (BAB) Reference

Purpose: Apply the BAB copywriting framework to short-form, conversion-driven narratives — landing page hero sections, email subject sequences, ad copy, in-product upsell modals, push notifications. BAB is the most compact transformation arc available to Saga: three beats, one CTA, 200-500 characters total.

## Scope Boundary

- **saga `bab`**: BAB three-part copywriting (this document).
- **saga `customer` (elsewhere)**: Full Before→After arc with case-study depth.
- **saga `hero-journey` (elsewhere)**: 12-stage transformation. BAB is a *radical compression* of hero's journey.
- **saga `narrative` (elsewhere)**: Product positioning. BAB executes the positioning; positioning frames it.
- **saga `pyramid` (`reference/minto-pyramid.md`)**: Top-down MECE answer-first delivery for executive/board memos. **Choose Pyramid over BAB when the audience must *decide* (analytic), not *act* (emotional/conversion).** BAB's Bridge is a product CTA; Pyramid's top is a governing thought + decision ask. The two can also combine — Pyramid for the spine of an exec memo, BAB embedded as a one-pager illustration of the customer transformation.
- **Prose (elsewhere)**: Final UX microcopy and tone polish.
- **Funnel (elsewhere)**: LP construction and conversion architecture.
- **Growth (elsewhere)**: SEO/CRO/SMO optimization of the BAB output.

## Core Structure

```
┌──────────────────────────────────────────────────────┐
│  BEFORE                                              │
│  Customer's current pain — concrete, sensory         │
│                                                      │
│  ↓                                                   │
│                                                      │
│  AFTER                                               │
│  Customer's ideal future — emotional, specific       │
│                                                      │
│  ↓                                                   │
│                                                      │
│  BRIDGE                                              │
│  Your product as the path between Before and After   │
│  Single CTA                                          │
└──────────────────────────────────────────────────────┘
```

The structure exploits a fundamental cognitive bias: humans are loss-averse first, gain-seeking second. Painting the painful Before primes the brain to *want* the After. The Bridge then offers the cheapest available path off that pain.

## Why BAB Works

| Beat | Cognitive lever | Risk if missed |
|------|-----------------|----------------|
| Before | Pain anchoring + present bias | Reader doesn't recognize themselves; bounces |
| After | Hope + future-self | Reader recognizes pain but no escape exists; despairs |
| Bridge | Path of least resistance + CTA | Reader wants to escape but can't act; leaves |

Skipping any beat reduces conversion. Most weak BABs skip Before (jumping to features) — the result reads as ad copy without empathy.

## Length Targets by Channel

| Channel | Total length | Each beat | Notes |
|---------|--------------|-----------|-------|
| Email subject | 50-70 chars | — | Often only Before or After, not full BAB |
| Email preheader | 90-120 chars | — | Compressed BAB possible |
| LP hero (above fold) | 200-400 chars | 60-130 each | Headline = After; subhead = Before; CTA = Bridge |
| LP body section | 300-500 chars | 80-150 each | Full BAB with sub-CTA |
| Ad copy (display) | 90-150 chars | — | Often only Before-Bridge |
| Push notification | 60-120 chars | — | Single beat, usually After or Before |
| Modal upsell | 150-300 chars | 40-100 each | Compressed full BAB |
| Sales email body | 400-700 chars | 100-230 each | Full BAB, sub-headers OK |

## BAB vs Other Three-Part Frameworks

| Framework | Structure | Best for | Key difference |
|-----------|-----------|----------|----------------|
| **BAB** | Before / After / Bridge | Sales copy, LP hero, email | Bridge = your product (commercial) |
| **PAS** | Problem / Agitate / Solution | Pain-heavy direct response | Agitate stage amplifies pain harder; aggressive |
| **AIDA** | Attention / Interest / Desire / Action | General advertising | Linear funnel; less narrative |
| **FAB** | Features / Advantages / Benefits | B2B sales sheets | Product-centric; risk of AP-2 |
| **ABT** | And / But / Therefore | Internal comms, social posts | Narrative *flow*; not necessarily commercial |
| **Pixar Spine** | Once upon / Every day / Until / Because / Until finally | Internal scenarios, elevator pitches | Five beats; longer; emotional |

Choose BAB when:
- The audience needs to *act* (CTA-driven).
- The transformation is concrete and short-form.
- You have one product to offer as the bridge.

Choose PAS when:
- Pain is large enough to dominate.
- Direct-response, infomercial, or pain-niche markets.

Choose ABT when:
- No commercial CTA.
- Internal narrative, social post, manifesto.

## Crafting Each Beat

### Before — make the pain visible

| Lever | Technique | Example |
|-------|-----------|---------|
| Sensory specifics | "Inbox sitting at 1,247 unreads" not "lots of email" | concrete |
| Time pressure | "Friday night, ticket count climbing" | urgency |
| Identity friction | "You promised the team a clean release; here's what happened" | self-image |
| Social cost | "Your manager asked again about the dashboard" | reputation |
| Physical / emotional | "3 AM scroll, knowing you'll be tired tomorrow" | embodied |

Avoid: hyperbole, fake-friend tone, generic "are you tired of...".

### After — make the future tangible

| Lever | Technique | Example |
|-------|-----------|---------|
| Day-in-the-life | "By Tuesday, the dashboard tells you what to fix" | scene |
| Removed friction | "No more 3 AM debugging" | absence |
| Gained capacity | "Your team ships twice a week, not once a month" | metric |
| Identity gain | "You're the engineer who shipped the migration cleanly" | self-image |
| Quiet confidence | "Calm Mondays" | feeling |

Avoid: vague aspiration ("achieve your goals"), unmeasurable claims, future-utopia tropes.

### Bridge — offer the cheapest path

| Lever | Technique | Example |
|-------|-----------|---------|
| Verb-led CTA | "Start free trial" not "Sign up now" | action verb |
| Risk reversal | "14-day trial, no card" | reduce anxiety |
| Time-anchored | "Live in 5 minutes" | speed promise |
| Social proof tail | "Join 8,000 teams already shipping" | herd signal |
| One CTA only | Don't offer A/B/C — pick one | decision fatigue |

Avoid: stacked CTAs, generic "Learn more", buried CTA, hidden price.

## Workflow

```
INPUT      →  receive: target audience, channel, character budget,
           →           product positioning (or invoke Saga `narrative`)

PAIN-MAP   →  identify the specific painful moment (one, not many)
           →  specify sensory detail (visual / time / role / consequence)

GAIN-MAP   →  identify the inverse future state
           →  make it concrete (metric, scene, identity)

PATH       →  state the simplest action that bridges the two
           →  apply risk reversal + time-anchored promise

DRAFT      →  write Before / After / Bridge to length budget
           →  one sentence each for short channels; one paragraph for LP

REFINE     →  AP-1~AP-9 anti-pattern check via reference/anti-patterns.md
           →  especially AP-3 missing tension, AP-9 ad copy disguise, AP-7 jargon wall
           →  read aloud to test rhythm

DELIVER    →  output BAB + alternatives (2-3 variants) for A/B testing
           →  recommend Funnel/Growth/Prose/Experiment for handoff
```

## Output Template

```markdown
## BAB Narrative: [Channel / Audience]

### Context
- **Audience**: [persona — pull from Cast registry if available]
- **Channel**: [LP hero / email subject / push / modal / ad]
- **Length budget**: [chars]
- **Single CTA**: [verb + outcome]

### Variant A
- **Before**: [pain — concrete, sensory]
- **After**: [future state — specific, emotional]
- **Bridge**: [product as path + CTA]

### Variant B (alternative emphasis)
- **Before**: [...]
- **After**: [...]
- **Bridge**: [...]

### Variant C (alternative tone)
- **Before**: [...]
- **After**: [...]
- **Bridge**: [...]

### Recommended Variant
- **Choice**: [A / B / C]
- **Reason**: [tone fit, audience match, CTA strength]

### Anti-Pattern Check
Run the full AP-1~AP-9 checklist from `reference/anti-patterns.md` and report results in the standard format. BAB emphasizes AP-3 (Missing Tension — Before must be concrete), AP-7 (Jargon Wall — short copy can't carry it), and AP-9 (Ad Copy Disguise — the largest risk for conversion copy). AP-8 (Happy Path Only) is typically marked N/A for short-form BAB.

### Test Plan
- **Hypothesis**: variant X drives more conversion than control
- **Metric**: CTR / signup / activation
- **Sample size**: [calc via Experiment]
- **Holdout**: [%]

### Handoffs
- Funnel: integrate BAB into LP hero / above-fold
- Growth: SMO/SEO copy adapted from BAB
- Prose: final tone polish + microcopy CTAs
- Experiment: A/B test variants
- Director: video script seeded from BAB
```

## Examples (illustrative, not real)

### LP hero (350 chars)

> **Before**: Friday 9 PM. Your dashboard says ship-rate dropped 30% this quarter and no one knows why. The team's exhausted from manual checks.
>
> **After**: By next Friday, the same dashboard tells you which 3 changes broke it — and the fix is already in review.
>
> **Bridge**: [Acme] reads your CI history and points to the bottleneck. **Start free trial — 14 days, no card.**

### Email subject + preheader (110 chars)

> **Subject**: Still spending Sunday night on the report?
> **Preheader**: Acme generates it Friday afternoon. 14-day trial.

### Push notification (90 chars)

> Three teammates already migrated to clean checkout. Your turn? **Open Acme →**

## Anti-Patterns Specific to BAB

| Anti-pattern | Fix |
|--------------|-----|
| Skipping Before — straight to After + CTA | Add concrete pain anchor; reader needs to recognize themselves |
| After is feature list ("with X, Y, Z") | Rewrite as scene or feeling |
| Bridge is generic ("contact us") | Verb-led, time-anchored, risk-reversed CTA |
| Multiple CTAs ("trial OR demo OR docs") | Pick one |
| Pain is manufactured ("are you tired of slow...") | Use real pain from research / NPS verbatims |
| Bridge requires too much before payoff ("complete onboarding to see value") | Promise immediate first-value moment |
| AP-9 disguise: reads as ad copy | Anchor in specific user research, not industry tropes |
| BAB on top of BAB (stacking variants on same page) | One BAB per surface; alternative variants live in test cells |

## Deliverable Contract

When `bab` completes, emit:

- **Audience + channel + length budget** stated.
- **Three variants (A/B/C)** of full BAB.
- **Recommended variant** with reason.
- **Anti-pattern check** (AP-1~AP-9 per `reference/anti-patterns.md`).
- **Test plan** (hypothesis, metric, sample size, holdout).
- **Handoffs**: Funnel, Growth, Prose, Experiment, Director.

## References

- Joseph Sugarman — *The Adweek Copywriting Handbook* (slippery slope + BAB foundations)
- Eugene Schwartz — *Breakthrough Advertising* (pain + state-of-mind levers)
- Robert Bly — *The Copywriter's Handbook* (BAB and PAS comparison)
- Donald Miller — *Building a StoryBrand* (BAB-compatible 7-part frame)
- Joanna Wiebe — Copyhackers (modern conversion copy + BAB research methods)
- VWO / Optimizely — A/B testing benchmarks for hero variants
- HubSpot / Mailchimp — subject line and CTA benchmark studies
