# Spark Opportunity Sizing Reference

Purpose: Produce a defensible estimate of an opportunity's size and confidence before a proposal advances past DISCOVER. Sizing connects a target persona and job-to-be-done to a bounded market, a realistic reachable slice, and a willingness-to-pay signal — so that prioritization frameworks downstream score on real numerators, not wishful reach.

## Scope Boundary

- **Spark `opportunity`**: sizing the opportunity upstream of scoring — TAM/SAM/SOM, reach estimates, willingness-to-pay signals, opportunity tree mapping.
- **vs `Rank`**: Rank orders items with ICE/RICE/WSJF once the numerators exist; `opportunity` supplies the numerators Rank consumes.
- **vs `Void`**: Void prunes scope once sizing exposes that the reachable slice does not justify build cost.
- **vs `Plea`**: Plea role-plays synthetic users to surface unmet needs; `opportunity` quantifies the market those needs live in.
- **vs `Experiment`**: Experiment validates the hypothesis after a proposal ships as test; `opportunity` estimates the upper bound on what validation can possibly earn.

If the question is "how big is this bet?" → `opportunity`. If it is "which of these sized bets do we pick?" → `Rank`.

## TAM / SAM / SOM Sizing

Always produce all three. A TAM-only number is a sales deck, not a proposal.

| Layer | Definition | Method |
|-------|------------|--------|
| `TAM` | Total addressable market — everyone with the job-to-be-done, regardless of reachability | Top-down industry report, cross-checked with census or platform counts |
| `SAM` | Serviceable addressable market — subset reachable by our channel, geography, language, price band | Filter TAM by our delivery constraints |
| `SOM` | Serviceable obtainable market — realistic share in 12–24 months given competition and acquisition capacity | Bottom-up from funnel math, validated against comparable launches |

Require two independent paths to each number: top-down (market report) and bottom-up (funnel × conversion × ARPU). If the two diverge by more than 2x, surface the gap explicitly — do not average them.

## Reach × Impact × Confidence

When the opportunity is internal (an existing product feature, not a net-new market), size it in RICE-compatible units so handoff to Rank is clean.

| Factor | How to source | Trap to avoid |
|--------|---------------|---------------|
| Reach | Segment-specific MAU over a consistent window (usually a quarter) | Using total registered users — always overstates reach |
| Impact | Expected delta on the target KPI, calibrated to Impact = 3 ≥ 10% improvement | Flat 2–3 for every feature ("everything is important") |
| Confidence | Evidence tier (see below) | >80% without quantitative evidence |

Evidence tiers for Confidence:
- `<= 50%`: meeting discussion, analogy, gut
- `50–70%`: qualitative interviews (N≥5), small-N surveys
- `70–85%`: quantitative analytics, prior experiment, large-N survey
- `> 85%`: live A/B result or shipped-feature telemetry on same audience

## Bottom-Up vs Top-Down

Use both, label which is which, reconcile.

```
Top-down:   TAM -> SAM -> SOM  (market report, then filter)
Bottom-up:  eligible_users × reach_rate × conversion × ARPU × retention
```

Bottom-up is where product bets live and die. A 1% of 10B TAM line looks strong until the bottom-up funnel says realistic SOM is 40k users at $20 ARPU = $800k — which may or may not clear the bar for build.

## Willingness-To-Pay Signals

Size is hollow without demand evidence. Accept these signals, ranked by strength:

| Signal | Strength | How to read |
|--------|----------|-------------|
| Paid pilot / LOI | Strongest | Money or signed intent on real terms |
| Van Westendorp / Gabor-Granger survey | Strong | Price-sensitivity range with N≥100 |
| Waitlist with payment capture | Strong | Card on file, not email only |
| Competitor pricing + switching cost | Moderate | "Customers pay $X for worse" is a defensible anchor |
| Fake-door / Smoke test CTR | Moderate | Surface-level intent, not price-bearing |
| Survey "would you pay" | Weak | Well-known to overstate — discount heavily |
| Interview enthusiasm | Weakest | Treat as directional only |

If the strongest available signal is "interview enthusiasm", flag the proposal as `UNPRICED` and require `Experiment` or a fake-door before Rank scoring.

## Market-Timing Assessment

Sizing a correct market at the wrong time produces killed proposals. Assess:

- **Why now?** — what changed (regulation, platform, cost curve, behavior shift) that makes this viable now but not 2 years ago?
- **Why not yet?** — what enabling condition is still missing? If the answer is "nothing", the opportunity is likely already contested or already failed by others.
- **Window half-life** — if this opportunity exists for 6 months, build speed dominates; if 3+ years, platform quality dominates.
- **Adjacent-move signals** — are larger players signaling entry? (public roadmaps, job listings, acquisitions in the space)

## Opportunity Tree Mapping

Use Teresa Torres's Opportunity Solution Tree to connect sized opportunities to outcomes.

```
Desired Outcome  (KPI-aligned, from OKRs)
    |
    +-- Opportunity A  (pain / desire / unmet need)  ← sized here
    |     +-- Solution A1  (candidate feature)
    |     |     +-- Experiment  (smallest test)
    |     +-- Solution A2
    |
    +-- Opportunity B
          +-- Solution B1
```

Rules:
- An opportunity is a **customer problem statement**, never a feature shape.
- Parent opportunity reach is the sum of child opportunity reach ceilings (de-duplicated by user).
- If a child opportunity is reachable but does not move the parent outcome, it belongs on a different tree — surface the tree mismatch rather than forcing it.
- Limit each level to 3–7 branches; more than 7 means the opportunity is not yet decomposed to actionable size.

## Sizing Output Template

```
## Opportunity Sizing: [Opportunity Name]

Target outcome: [KPI from OKR]
Target persona: [segment]
Job-to-be-done: [progress sought, not activity]

Market:
  TAM (top-down):  $[X]  source: [report]
  SAM (filtered):  $[X]  filters applied: [geo / channel / price]
  SOM (12–24mo):   $[X]  bottom-up path: [funnel math]
  Reconciliation:  [explain >2x divergence, if any]

Reach (internal-feature sizing):
  Eligible segment: [N users], window: [quarterly]
  Reach rate assumption: [%], evidence: [tier]

Willingness-to-pay signal: [tier + detail]
Market timing: why-now / why-not-yet / window half-life

OST placement:
  Outcome -> Opportunity -> candidate Solutions [A1, A2]

Confidence: [tier, with evidence]
Blockers to higher confidence: [named evidence gaps]
```

## Anti-Patterns

- Quoting TAM without SAM and SOM — a TAM-only deck hides reachability.
- Averaging top-down and bottom-up when they diverge — record the divergence, do not smooth it.
- Using total registered users as Reach — use segment-specific active users in a consistent window.
- "1% of the market" assumptions — always derive SOM from a funnel, never from a percentage pulled from thin air.
- Accepting survey "would you pay?" as willingness-to-pay — discount heavily or re-route to a fake-door test.
- Sizing a feature (activity) instead of an opportunity (progress) — features are solutions; opportunities are problems.
- Flat 80% confidence because "we interviewed some users" — map to the evidence tier explicitly.
- Opportunity trees that retrofit existing roadmap items — if every child solution is already being built, this is confirmation, not discovery.
- Ignoring market timing — a correctly sized opportunity at the wrong time still kills.

## Handoff / Next Steps

- If SOM clears the bar and WTP signal is `Strong` or above → hand to `Rank` for RICE/WSJF scoring against peers.
- If SOM is ambiguous but WTP signal is weak → hand to `Experiment` for a fake-door or Van Westendorp before scoring.
- If SOM is small but strategic (wedge into larger market) → hand to `Magi` for Go/No-Go with explicit strategic rationale.
- If opportunity tree shows the parent outcome is not moved by any reachable solution → hand to `Void` to prune and re-frame.
- If willingness-to-pay requires synthetic user probing before survey design → hand to `Plea`.

Record the sized opportunity in `.agents/spark.md` under phantom/underused features so future proposals inherit the sizing work.
