# Win/Loss Analysis Reference

Purpose: Systematic post-decision interview program that surfaces the real reasons deals were won or lost — not the reasons the rep wrote in the CRM. Win/loss is the highest-signal competitive intelligence input because it is grounded in actual buyer decisions, not analyst opinion or competitor marketing. A formal program yields 15-30% win-rate improvement.

## Scope Boundary

- **compete `winloss`**: post-decision buyer interviews, theme extraction, cadence design, integration with CRM and battle cards.
- **compete `matrix` (default, elsewhere)**: feature comparison — descriptive, not behavioral. Win/loss explains why features matter, not what they are.
- **compete `swot` (elsewhere)**: strategic SWOT — win/loss data feeds SWOT but is not SWOT itself.
- **compete `positioning` (elsewhere)**: positioning maps — win/loss surfaces positioning gaps; positioning resolves them.
- **compete `battle` (elsewhere)**: battle cards consume win/loss themes as their evidence layer. Do not author "why we win/lose" sections from opinion.
- **voice (elsewhere)**: existing-customer feedback and NPS. Voice is post-purchase satisfaction; win/loss is purchase-decision rationale. Different population, different question set.
- **researcher (elsewhere)**: discovery-phase user research and persona work. Researcher designs the methodology; Compete owns the win/loss program structure and competitive lens.
- **plea (elsewhere)**: synthetic-user assumption challenge. Plea is hypothesis stress-testing without real interviews — never substitute for real win/loss.

## Workflow

```
DESIGN    →  define segments (deal-size x vertical x role x outcome)
          →  draft interview script; choose third-party interviewer

RECRUIT   →  invite within 2-6 weeks of decision (sweet spot)
          →  target 30-40% response rate; offer incentive ($100-250)

INTERVIEW →  30-45 min recorded calls; let buyer narrate timeline
          →  cover: trigger, evaluation set, decision criteria, deciding factor

CODE      →  tag each interview by themes; require 3+ mentions to elevate
          →  separate signal from one-off complaints

SYNTHESIZE → quarterly report: themes by segment, trend deltas, action items
           → feed battle cards (objections, why-win/lose), Spark (gaps)

CADENCE   →  quarterly cycle minimum; monthly for high-velocity SMB sales
          →  CRM-integrate findings; close the loop with sales + product
```

## Segmentation Axes

| Axis | Why segment | Typical buckets |
|---|---|---|
| Outcome | Win and loss patterns differ structurally | Won, Lost, No-decision, Churned |
| Deal size | SMB and enterprise buyers cite different reasons | <$10k, $10-100k, $100k-1M, >$1M |
| Vertical | Industry shapes evaluation criteria | Financial, healthcare, retail, tech, public sector |
| Decision-maker role | IC, manager, exec weight criteria differently | End user, champion, economic buyer, technical evaluator |
| Competitor encountered | Loss reasons cluster by competitor | Direct A, Direct B, Substitute, In-house build |
| Sales motion | PLG vs sales-led decisions diverge | Self-serve, inside sales, enterprise field |

Minimum viable program: segment by `outcome x deal-size x competitor`. Add vertical and role once volume supports cross-tabulation (typically 40+ interviews/quarter).

## Interview Script Skeleton

| Phase | Question type | Example |
|---|---|---|
| Context | Trigger and timeline | "Walk me back to when you first realized you needed a solution. What was happening?" |
| Evaluation | Set considered | "Which vendors did you evaluate? How did each enter the consideration set?" |
| Criteria | Decision factors | "What were the top 3 criteria? How were they weighted?" |
| Process | Internal dynamics | "Who was involved? Who held veto power? What changed during evaluation?" |
| Deciding factor | The single moment | "If you had to point to one thing that decided it, what was it?" |
| Counterfactual | Loss-recovery probe (lost only) | "What would have made you choose us? Was there ever a moment we could have won?" |
| Future | Renewal/expansion intent (won) | "Six months from now, what would make you reconsider?" |

Question rule: never lead. "Was pricing the issue?" yields useless yes/no; "What were the top 3 factors?" yields ranked truth.

## Theme Coding Workflow

1. Transcribe every interview (Otter, Fireflies, Gong).
2. First-pass code: tag with predefined themes (price, features, integration, trust, timing, champion-loss, ROI-clarity).
3. Second-pass code: tag emergent themes not in the predefined set.
4. Elevation rule: a theme requires `3+` mentions across interviews before it qualifies as a finding. One-off complaints are noise.
5. Cross-segment analysis: a theme that appears in one segment but not others is a segment-specific finding, not a global one.
6. Quote selection: for each elevated theme, pick 2-3 verbatim quotes as evidence (anonymized).

## Signal-to-Noise Filtering

| Signal type | Treat as | Reason |
|---|---|---|
| Buyer cites a feature gap that 3+ buyers also cited | High-confidence signal | Cross-buyer convergence |
| Buyer cites a feature gap unique to their context | Segment signal | May be vertical/size specific, do not generalize |
| Buyer cites "price" as #1 reason | Probe deeper | Price is rarely the real reason; usually a proxy for unclear ROI or weak champion |
| Buyer praises competitor by name | High-confidence signal | Direct competitive insight |
| Buyer's narrative contradicts CRM notes | Investigate | CRM rep narrative is biased toward face-saving |
| Buyer says "we just went with the safe choice" | Brand/trust signal | Indicates positioning/credibility gap, not feature gap |

Noise filters: complaints from buyers who never reached late-stage evaluation, blame-shifting language ("my CFO killed it"), and post-rationalization more than 8 weeks after decision.

## Third-Party Interviewer Benefits

| Concern | Internal interviewer | Third-party interviewer |
|---|---|---|
| Buyer candor | Buyer softens criticism to avoid offending vendor | Buyer speaks more honestly to neutral party |
| Bias in coding | Coder unconsciously discounts unflattering data | Independent coder records as stated |
| Sales objection on findings | "Buyer was wrong / didn't understand" | Neutral source is harder to dismiss |
| Reference contamination | Buyer worries about future negotiations | Anonymity protects relationship |
| Cost | Lower direct cost, higher hidden bias cost | $1.5-3k per interview, higher signal quality |

Recommendation: use third-party for `loss` interviews and high-stakes wins; internal acceptable for routine wins where confirmation is the goal.

## Cadence Design

| Cadence | When appropriate | Volume target |
|---|---|---|
| Monthly | High-velocity SMB, >50 deals/month | 8-12 interviews/month |
| Quarterly | Mid-market and enterprise, 20-50 deals/quarter | 15-25 interviews/quarter |
| Ad hoc | <20 competitive deals/quarter | Continuous, no batch |
| Always-on | Any volume, with automation | Trigger every closed-lost above threshold |

Quarterly is the default minimum for B2B SaaS. Below 20 competitive deals/quarter, run ad hoc but never skip — even 5 interviews/quarter beats zero.

## CRM Integration

| Field | Purpose |
|---|---|
| `winloss_interview_completed` | Filter eligible accounts; measure program coverage |
| `winloss_primary_reason` | Coded theme tag for trend analysis |
| `competitor_won` | Loss attribution for win-rate-by-competitor reporting |
| `champion_strength` | Champion presence as predictor variable |
| `decision_role_interviewed` | Validate role-mix balance |
| `interview_recording_url` | Searchable evidence layer for downstream agents |

Integration rule: findings that do not flow back into CRM and battle cards are research theater. Close the loop or stop running the program.

## Anti-Patterns

- Rep-authored loss reasons — reps write "price" or "features" because it protects relationships and pipeline; buyer reality differs in 60-70% of cases.
- No segmentation — pooled win/loss findings hide that SMB lost on price while enterprise lost on integration. Segment or learn nothing.
- Interviewing only losses — wins reveal what to protect; losses alone bias the program toward defensive thinking.
- Interviewing too late — beyond 8 weeks, buyer recall degrades and post-rationalization dominates. Interview within 2-6 weeks.
- One-and-done program — quarterly cadence is the minimum; one-off projects cannot detect trends or measure improvement.
- No theme-elevation rule — promoting a single quote to a finding produces strategic whiplash. Require `3+` mentions.
- Findings without action — if win/loss does not change battle cards, roadmap, or pricing, the program will be defunded.
- Interviewer without training — untrained interviewers ask leading questions and miss the deciding-factor probe.
- Treating "price" at face value — price is the most-cited and least-real loss reason. Probe for ROI clarity, champion strength, and timing instead.

## Handoff

- **To Voice**: pull post-purchase satisfaction quotes from existing customers as supporting evidence for "why we win" themes.
- **To Researcher**: hand off interview script design, persona validation, and qualitative coding methodology refinement.
- **To Helm**: when win/loss reveals a structural shift (segment moving, category re-defining), escalate for strategic simulation.
- **To Spark**: feature gaps that appear in `3+` loss interviews route as feature ideas with competitive and buyer evidence attached.
- **To Growth**: positioning, brand-authority, or first-touch trust gaps route to Growth for messaging and SEO/GEO response.
- **To battle (compete)**: every quarter's themes feed the "why we win / why we lose / objections" sections of battle cards.
- **To Lore**: recurring win/loss patterns that hold across 3+ quarters become institutional knowledge.
