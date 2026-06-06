# Moat / 7 Powers Assessment Reference

Purpose: Evaluate durable competitive advantage using Hamilton Helmer's 7 Powers framework (2016) — the field's most rigorous moat taxonomy. A Power is a condition that creates the potential for persistent differential returns; only seven such conditions exist. This reference scores moat durability, distinguishes real Powers from anti-moats, and separates the statics (does the Power exist?) from the dynamics (can we get it?).

## Scope Boundary

- **compete `moat`**: structural moat assessment via 7 Powers, durability scoring, anti-moat detection.
- **compete `matrix` (default, elsewhere)**: feature comparison — features are not moats; do not conflate.
- **compete `swot` (elsewhere)**: SWOT lists strengths but does not test durability. Moat assessment is the durability filter applied to SWOT strengths.
- **compete `positioning` (elsewhere)**: positioning maps describe perceived differentiation; moat assessment evaluates whether that differentiation is structurally defensible.
- **compete `battle` (elsewhere)**: tactical sales ammunition. Battle cards may reference moats but cannot create them.
- **compete `winloss` (elsewhere)**: behavioral evidence of differentiation. Win/loss tells you what wins deals today; moat tells you what will still win deals in 10 years.
- **voice (elsewhere)**: customer feedback. Voice surfaces preference; moats explain why preference persists under competitive pressure.
- **researcher (elsewhere)**: empirical user research. Researcher validates customer behavior; moat work analyzes industry structure.
- **plea (elsewhere)**: synthetic-user assumption challenge. Plea stress-tests moat claims that lack market evidence.
- **helm (elsewhere)**: strategic simulation. Helm consumes the moat assessment as input to multi-year scenario planning.

## Workflow

```
INVENTORY →  list all candidate advantages (features, scale, brand, partnerships)
          →  separate genuine Powers from features and from anti-moats

CLASSIFY  →  test each candidate against the 7 Powers definitions
          →  apply the Benefit + Barrier double test (must pass both)

SCORE     →  rate Power magnitude (low/med/high) and durability (years)
          →  apply the decade test: will this still work in 10 years?

DYNAMICS  →  identify the origin story: how did the Power form?
          →  determine if a missing Power is still attainable (Origins phase)

ANTI-MOAT →  flag negative-Power conditions (regulatory, dependence, debt)
          →  estimate erosion rate vs investment needed to defend

REPORT    →  Powers held, Powers absent, anti-moats present, durability score
          →  hand strategic implications to Helm; tactical implications to battle
```

## The 7 Powers (Helmer 2016)

| Power | Benefit (to holder) | Barrier (to challenger) | Typical exemplar |
|---|---|---|---|
| Scale Economies | Lower per-unit cost as volume grows | Subscale challenger faces structural cost gap | Netflix content amortization, AWS infrastructure |
| Network Economies | Value to each user grows with user count | Challenger cannot match utility without users | Visa, LinkedIn, Bloomberg Terminal |
| Counter-Positioning | Novel business model superior to incumbent's | Incumbent rationally chooses not to copy (cannibalization) | Vanguard vs active asset managers, Netflix vs Blockbuster |
| Switching Costs | Customer faces real cost to leave | Challenger must compensate for the switching cost | SAP, Salesforce admin lock-in, learned-workflow tools |
| Branding | Customer assigns higher value at same objective quality | Challenger cannot replicate without history and trust | Tiffany, Hermes, Coca-Cola |
| Cornered Resource | Preferential access to scarce input | Challenger cannot acquire the resource | Pixar's brain trust, ARM IP, exclusive licenses |
| Process Power | Embedded organizational/process superiority | Challenger faces hysteresis — slow, hard-to-replicate development | Toyota Production System, TSMC manufacturing |

The double test: a Power requires **both** a Benefit (improved cash flow for holder) **and** a Barrier (challengers cannot or will not eliminate it). Either alone is insufficient. A great feature with no barrier is just temporary differentiation.

## Durability Scoring Rubric

| Score | Durability | Decade test | Investment to maintain |
|---|---|---|---|
| 1 | <2 years | Will not survive next platform shift | Continuous reinvestment, fragile |
| 2 | 2-5 years | Survives current cycle, fades next | Significant ongoing investment |
| 3 | 5-10 years | Survives one major industry shift | Moderate ongoing investment |
| 4 | 10-20 years | Survives multiple shifts | Compounds with low marginal cost |
| 5 | 20+ years | Generational; new entrant must change category to attack | Self-reinforcing |

Apply the decade test to every claimed Power: "If a smart, well-funded competitor entered tomorrow with the goal of neutralizing this Power, could they do it within 10 years?" If yes, durability is `<=3`. If no, justify why structurally.

## Power Dynamics: Statics vs Dynamics

Helmer separates two questions:

- **Statics** — does the Power exist in the current state? (Use the 7 definitions.)
- **Dynamics** — how was the Power created, and can it still be created?

Powers form during specific industry phases (Origination, Take-Off, Stability). Most Powers can only be acquired during Origination — once an industry is in Stability, the windows have closed. This is why incumbents rarely add new Powers and challengers must wait for industry inflection points.

| Phase | Power-formation opportunity |
|---|---|
| Origination | Cornered Resource, Counter-Positioning, Branding (slow build) |
| Take-Off | Scale Economies, Network Economies, Switching Costs (lock-in race) |
| Stability | Process Power (compounds slowly); other Powers rarely form |

Strategic implication: if the industry is in Stability and you hold no Powers, do not strategize toward acquiring one — the windows are closed. Reposition to a sub-segment in Origination, or accept commodity returns.

## Counter-Positioning vs Differentiation

Counter-Positioning is the most-misunderstood Power. It is **not** "we're different." It is a specific structure:

| Test | Counter-Positioning | Mere differentiation |
|---|---|---|
| Incumbent's response | Rationally declines to copy | Will copy if it works |
| Reason for non-copy | Cannibalizes incumbent's existing business | None — would copy if profitable |
| Time-bound | Persists as long as incumbent business persists | Disappears when copied |
| Examples | Vanguard's index funds (active managers cannibalize) | Most "challenger brand" stories |

Counter-Positioning fails the test if the incumbent could copy without self-harm. Most "we are the disruptor" narratives are differentiation, not Counter-Positioning. Apply this filter ruthlessly.

## Anti-Moat Identification

Anti-moats are structural conditions that erode returns regardless of operational excellence. Detect early; defending is costly.

| Anti-moat | Mechanism | Erosion signal |
|---|---|---|
| Platform dependence | Host platform captures the value | Apple/Google policy changes, App Store fee shifts |
| Regulatory exposure | Returns hostage to political risk | Pending legislation, jurisdictional rulings |
| Customer concentration | One buyer controls margin | >25% revenue from single customer |
| Talent dependence | Power lives in 1-3 individuals | Founder/star-employee non-replaceable |
| Technology debt | Compounding rebuild cost | Refactor cost approaching new-build cost |
| Reverse network effects | More users degrade experience | Spam, moderation cost growing nonlinearly |
| Disintermediation risk | Buyers and suppliers can connect directly | Marketplace transaction-leakage rate rising |
| AI commoditization | LLMs absorb the workflow | Workflow becomes a one-prompt task |

Anti-moat rule: a single anti-moat can neutralize a Power. Score the net moat as `min(Power durability) - (anti-moat severity)`.

## Anti-Patterns

- Calling features "moats" — features without barriers are temporary differentiation. Apply the double test.
- Confusing first-mover advantage with a Power — being first creates no durable advantage unless it triggered a Power-formation mechanism (network, scale, switching cost) during Take-Off.
- Treating brand as a default Power — Branding requires demonstrably higher willingness-to-pay at equal objective quality. Most "brands" are just recognition, not Branding-as-Power.
- Skipping the dynamics question — knowing a Power exists today does not tell you whether you can still acquire one. Map the industry phase.
- Counter-Positioning misuse — labeling any new business model as Counter-Positioning. Test: would the incumbent rationally decline to copy? If they would copy, it is not Counter-Positioning.
- Ignoring anti-moats — a strong Power with a severe anti-moat is fragile; investors and operators routinely overweight Powers and underweight anti-moats.
- Static-only analysis — describing today's moat without explaining how it formed leaves the team unable to defend or extend it.
- Multiple-Power inflation — most companies hold one or zero Powers. Claiming three or more is usually evidence of weak classification discipline.
- Confusing "hard to build" with "hard to replicate" — Process Power requires both organizational embedding **and** hysteresis. Hard-to-build alone (e.g., complex software) is not Process Power; competitors can also build hard things.

## Handoff

- **To Helm**: moat assessment is core input to strategic simulation, scenario planning, and multi-year capital allocation. Pass Powers held, gaps, and anti-moats with confidence levels.
- **To Voice**: validate Branding-as-Power claims with willingness-to-pay studies and customer language about trust.
- **To Researcher**: design empirical studies to validate Switching Costs (real switching attempts) or Network Economies (utility-vs-userbase curves).
- **To Spark**: when a Power could be acquired in Origination/Take-Off phase, route the Power-building feature concept as a strategic bet, not a roadmap item.
- **To Growth**: Branding-as-Power requires deliberate brand investment; route the brand-building program to Growth.
- **To battle (compete)**: tactical implications — which Powers to emphasize in objection handling, which Powers competitors hold against us.
- **To winloss (compete)**: validate Switching Costs claims against actual loss data — if customers switch easily, the Switching Cost is weaker than claimed.
- **To Lore**: validated moat patterns and anti-moat detections become institutional knowledge for future strategic reviews.
