# Founder Anti-Patterns

**Purpose:** Catalog of common founder failure modes Sage detects and surfaces during sessions.
**Read when:** You suspect anti-patterns; need detection signals or counter-moves.

Each pattern includes detection signals (≥2 required to surface) and a counter-move. Surface explicitly by ID — soft labeling damages trust.

## Catalog

### AP-01: Build-Before-Validate
- **Signals:** shipping features without user conversations; "we'll launch when it's ready"; building MVP for >3 months without first user.
- **Counter:** stop building. Schedule 5 user calls this week. Show them the current product.

### AP-02: Premature Optimization
- **Signals:** optimizing infra/code before traction; "we need to scale" with <100 users; rebuilding the stack for hypothetical load.
- **Counter:** revert to the simplest stack that works. Re-prioritize on growth, not infra.

### AP-03: Vanity Metrics
- **Signals:** reporting sign-ups, page views, social followers; not reporting retention, revenue, or DAU/WAU.
- **Counter:** pick one true metric (revenue, retention, or engaged-user count) and report only that next session.

### AP-04: Distraction
- **Signals:** pursuing podcasts, conferences, partnerships, side projects while core metric is flat; saying yes to everything.
- **Counter:** cancel 3 commitments this week. Spend reclaimed hours on the core metric.

### AP-05: Pivoting Too Often
- **Signals:** ≥3 pivots in 6 months; current pitch is unrecognizable from 3 months ago.
- **Counter:** commit to current direction for 8 weeks; instrument retention; only pivot on data, not on excitement.

### AP-06: Hiring Too Early
- **Signals:** hiring before product-market fit; "we need an X to make this work"; <$10k MRR with >3 employees.
- **Counter:** freeze hiring. Founder does the work until traction is visible.

### AP-07: Cofounder Conflict
- **Signals:** avoiding cofounder; equity unsigned; one cofounder dominates decisions; "we should talk about that later".
- **Counter:** schedule a structured 60-min cofounder conversation with explicit topics. Get equity written. If unresolvable, surface that this is existential.

### AP-08: Wrong Customer / Wrong Market
- **Signals:** customers churning fast; can't articulate ICP; "everyone could use this"; <30% activation rate.
- **Counter:** define one specific customer (job title, company size, problem). Refuse to sell outside ICP for 4 weeks.

### AP-09: Avoiding Sales
- **Signals:** founder hasn't pitched in person/video this week; "we'll do sales after the product is ready"; product-led growth claims with no organic traction.
- **Counter:** founder books 5 sales calls this week. Treat selling as part of building, not after.

### AP-10: Platform Trap
- **Signals:** building "platform"/"OS"/"infrastructure" with no first concrete product; pitch is a generic enabler.
- **Counter:** kill the platform pitch. Pick one product for one customer. Generalize later only if traction earns it.

### AP-11: Premature Internationalization / Multi-Platform
- **Signals:** launching in 5 languages or 3 platforms before web works; "we want to be global from day 1".
- **Counter:** cut scope to one language, one platform until DAU and retention prove out.

### AP-12: Big-Deal Mirage
- **Signals:** pursuing one large enterprise deal for >2 months; pipeline is "we're talking to Google/IBM/etc.".
- **Counter:** build small-customer revenue in parallel. The big deal is fantasy until contract signed.

### AP-13: Founder-Mode Failures
- **Signals:** delegating customer conversations to ICs; not in code/sales/support yourself; "I'm working on strategy".
- **Counter:** founder spends ≥50% of time on either users or product this week. Strategy without contact is fiction.

### AP-14: Runway Denial
- **Signals:** unclear burn; no monthly runway calculation; "we'll figure out fundraising when we need it".
- **Counter:** calculate default-alive vs default-dead today. If <12 months runway, plan deliberate response (cut, raise, or revenue) within 30 days.

### AP-15: Idea Maze Avoidance
- **Signals:** can't articulate why previous attempts in this space failed; "this hasn't been done before".
- **Counter:** research 3-5 prior failed attempts. Articulate why they failed and why you'll succeed differently. If you can't, that's the answer.

### AP-16: Investor-Validated Theater
- **Signals:** pitching to investors more than to customers; "investors love it" without customer revenue; raising as a substitute for product-market fit.
- **Counter:** customer signal precedes investor signal. Pause investor meetings until 5 paying customers exist.

### AP-17: AI Wrapper Without Moat (2026)
- **Signals:** product is a prompt + UI on top of a single foundation model (GPT-4o, Claude, Gemini); no proprietary data, workflow embedment, or distribution lock-in; pitch leans on "AI-powered" as the differentiation. AI-wrapper churn benchmarks are substantially higher than traditional SaaS norms (90-day retention is a key investor probe at this stage — know your number).
- **Counter:** stop competing on model access. Pick one regulated or workflow-deep vertical (medical coding, contract review, claims, schedule routing). Earn one of: proprietary dataset, signed integration into the customer's system of record, or human-in-the-loop QA layer customers cannot easily rebuild. Per Garry Tan (Feb 2026): ~50% of AI agent activity is in coding; the remaining verticals are wide open and are where the next billion-dollar companies will be built (x.com/garrytan — YC RFS Spring 2025).

### AP-18: GPU Burn Denial (2026)
- **Signals:** founder cannot quote per-customer or per-request inference cost; >40% of total burn is GPU/API spend with no margin trendline; gross margin under 50% and unmodeled at scale; "we'll fix margins when we scale" without a credible cost-down plan. Investor benchmark: AI-first SaaS starts at 50-60% GM vs ~75% for classical SaaS — credible path to 70%+ GM within 18 months is the expected ask, not 75-80% today.
- **Counter:** instrument cost-per-request and cost-per-active-user weekly. Pick at least one lever (smaller model routing, prompt caching, batched inference, fine-tune vs few-shot, or self-host on rented GPUs) and ship it within 4 weeks. If unit economics cannot reach 70%+ steady-state GM within 18 months, the business model is wrong, not the cost. Source for GM benchmarks: pitch-critique.md "2026 AI-Era Deck Expectations".

### AP-19: Revenue Misrepresentation (2026)
- **Signals:** ARR claims that mix pilots, LOIs, free credits, or one-time consulting with recurring contracted revenue; growth charts without a defined revenue definition; founder hesitates when asked "walk me through last 3 months bank-deposited revenue". YC formally reminded founders in Apr 2026 to be precise about revenue after a wave of inflated ARR claims in the AI cohort — "ARR refers to recurring revenue actually invoiced and paid on a regular basis per contract".
- **Counter:** adopt one definition (e.g., contracted recurring revenue billed in the last 30 days, excluding pilots and credits). Re-state every number against it. Disclose pilots separately. The trap is not the inflated number — it is the loss of investor and team trust when the real number eventually surfaces. Source: Garry Tan / YC, "Being Truthful And Precise About Revenue", Apr 2026 (artificiallawyer.com/2026/04/27/y-combinator-tells-founders-be-truthful-on-revenue/ and x.com/garrytan/status/2048017824895909901).

## Detection Logic

Surface an anti-pattern only when **≥2 signals** are observed in the session. Below 2, hold the diagnosis — premature labeling damages trust.

When detected, name it explicitly:

> "This looks like AP-04 (Distraction). The signals I'm seeing are: (1) you've taken 3 podcast invitations this month and (2) the core metric is flat. Counter-move is to cancel 3 commitments this week."

Do not soften. Do not hedge with "maybe" or "it could be that". State the diagnosis, name the signals, propose the counter.

## Counter-Move Tone

Counter-moves are commitments the founder makes, not suggestions Sage offers. Convert each counter into an ACTION owned by the founder with a date. See `action-extraction.md`.

## Escalation

If three or more anti-patterns are detected in a single session, that itself is a meta-pattern: the founder is either in early-stage chaos (surface as such, recommend triage focus on one) or is rationalizing systematically (surface as such, recommend honest reflection before more building).
