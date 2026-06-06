# Scoring Frameworks

**Purpose:** Detailed procedures for each prioritization framework.
**Read when:** Executing CRITERIA or SCORE phases.

> **2026 framing.** The 2026 product-management literature continues to put **RICE** and **WSJF** at the top of "frameworks teams actually use" alongside MoSCoW, Kano, and Value-vs-Effort matrices — the toolkit itself has not changed in 2026, but two operating shifts have:
>
> 1. **AI assistance accelerates *scoring*, not the decision.** Tools like ProductBoard / Productboard AI, Roadmunk, Linear's "AI insights", and ChatGPT / Claude can summarise tickets, surface reach data, and propose ICE / RICE values — but the inputs (impact, confidence) remain a human judgement call. Treat AI-suggested scores as *anchors* in a calibration discussion, not as the score.
> 2. **AI feature work needs an explicit "Confidence ≤ X" guardrail.** Empirical 2026 data on AI features shows higher post-ship variance: only ~`1/3` of shipped features hit their target metric (Kohavi et al., Microsoft), and AI-authored implementations carry the additional risk surface documented in `void/reference/over-engineering-anti-patterns.md`. Treat any feature whose `Impact` argument relies on "AI will figure it out" as `Confidence ≤ 50%` until validated.

---

## 1. ICE (Impact × Confidence × Ease)

**Formula:** `ICE Score = Impact × Confidence × Ease`

Each factor scored 1-10:
- **Impact**: How much will this move the target metric? (1=negligible, 10=massive)
- **Confidence**: How sure are we about the impact estimate? (1=guess, 10=data-backed)
- **Ease**: How easy is implementation? (1=months of effort, 10=hours)

**When to use:** Quick triage, early-stage evaluation, limited data available.
**Strengths:** Simple, fast, good for large lists.
**Weaknesses:**
- **Overconfidence bias**: 1–10 absolute scales invite anchoring and optimism bias. Always score ICE relative to at least one reference item, not in isolation.
- No reach component — features affecting 1 user score identically to features affecting 10,000 users if their I×C×E are equal. Upgrade to RICE when reach discrimination matters.
- Multiplication amplifies input noise: a 2-point error in Ease (1→3) triples the score. Cap ICE at directional triage — do not use raw ICE numbers as precise rankings without pairwise calibration.
- **Do not treat ICE alone as definitive** — always apply at least one bias check (consider-the-opposite, anonymous scoring) before presenting results as final.

---

## 2. RICE (Reach × Impact × Confidence / Effort)

**Formula:** `RICE Score = (Reach × Impact × Confidence) / Effort`

- **Reach**: Number of people/events affected **within a fixed time window** (typically per quarter or per month — explicitly choose one and hold it constant across all items). Original Intercom definition: "customers per quarter." [Source: Intercom Blog — RICE: Simple prioritization for product managers (updated January 2025) https://www.intercom.com/blog/rice-simple-prioritization-for-product-managers/]
- **Impact**: How much does it affect each user? (3=massive, 2=high, 1=medium, 0.5=low, 0.25=minimal)
- **Confidence**: How sure are we? (100%=high, 80%=medium, 50%=low)
- **Effort**: Person-months of work (absolute estimate)

**When to use:** Product feature prioritization with user data.
**Strengths:** Includes reach, penalizes high-effort items.
**Weaknesses:** Reach inflation is the most common failure mode — avoid scoring a settings menu as 100% of users when actual open-rate is 10–20%. Effort estimation variance makes cross-team comparisons unreliable without a shared estimation anchor.

---

## 3. WSJF (Weighted Shortest Job First)

**Formula:** `WSJF = Cost of Delay / Job Duration`

**Cost of Delay** = User-Business Value + Time Criticality + Risk Reduction/Opportunity Enablement

Each component scored using modified Fibonacci (1, 2, 3, 5, 8, 13, 20 — SAFe 6.0 uses 1–13 range for CoD components, avoiding 20 to keep relative comparison tractable):
- **User-Business Value**: Revenue/satisfaction impact
- **Time Criticality**: How much value decays with delay?
- **Risk Reduction / Opportunity Enablement (RR&OE)**: Does this reduce future risk or enable other work? SAFe 6.0 explicitly warns that RR&OE is the most under-counted component — always probe for it, especially for platform and infrastructure work.
- **Job Duration**: Relative size of the work (same Fibonacci scale)

**When to use:** SAFe/Lean environments, PI planning, time-sensitive decisions. SAFe 6.0 confirms WSJF remains the primary sequencing mechanism for Feature-level backlogs at the ART (Agile Release Train) layer. [Source: Scaled Agile Framework — WSJF Extended Guidance https://framework.scaledagile.com/wsjf] [Source: Scaled Agile Framework — Cost of Delay Glossary https://framework.scaledagile.com/blog/glossary_term/cost-of-delay]
**Strengths:** Explicitly values time, balances multiple value dimensions.
**Weaknesses:** Requires team calibration on Fibonacci scales. Fibonacci scoring introduces relative-comparison benefits but makes cross-team or cross-PI absolute comparisons unreliable — treat WSJF as an intra-team ordering tool, not an inter-team budget allocator.

---

## 4. MoSCoW

**Categories:**
- **Must have**: Non-negotiable for this release. Without it, the release fails.
- **Should have**: Important but not critical. Workaround exists.
- **Could have**: Nice to have. Only if time/resources allow.
- **Won't have (this time)**: Explicitly excluded from this scope.

**Rule of thumb:** Must ≤ 60% of effort, Should ≤ 20%, Could ≤ 20%.

**When to use:** Stakeholder alignment, scope definition, release planning.
**Strengths:** Simple, inclusive, good for non-technical stakeholders.
**Weaknesses:**
- **"Must" inflation** (primary failure mode): stakeholders escalate items to Must as a political move. If Must > 60% of total effort, force a Must-Have Audit — remove each item mentally and check whether the release still functions without it.
- **"Should" over-population**: Should-have items accumulate each sprint and are rarely delivered, creating a permanent shadow backlog that erodes stakeholder trust. Set a Should → Could demotion rule when items survive three consecutive sprints undelivered.
- No ordering within categories — combine with RICE or ICE for intra-category sequencing when Must-tier items still exceed available capacity.

---

## 5. Cost of Delay (CoD)

**Three profiles:**
- **Standard**: Linear value loss over time. CoD = $/week of delay.
- **Urgent (Fixed Date)**: Deadline-driven. Value drops to zero after date. CoD spikes near deadline.
- **Peak (Time-Sensitive)**: Seasonal or market-window driven. CoD peaks at optimal launch window.

**Calculation:**
```
Weekly CoD = (Expected revenue per week) × (probability of achieving if on time) 
           - (Expected revenue per week) × (probability of achieving if delayed)
```

**When to use:** Economic decision-making, ROI-driven organizations.
**Strengths:** Connects priorities to money, hard to argue against.
**Weaknesses:** Requires revenue/cost data, hard to estimate for infrastructure work.

---

## 6. Kano Model

**Categories:**
- **Must-be (Basic)**: Expected. Absence causes dissatisfaction. Presence doesn't increase satisfaction.
- **One-dimensional (Performance)**: More = better. Linear relationship with satisfaction.
- **Attractive (Delighter)**: Unexpected. Absence doesn't cause dissatisfaction. Presence delights.
- **Indifferent**: Users don't care either way.
- **Reverse**: Presence causes dissatisfaction for some users.

**Classification method:** Pair of questions per feature:
1. "How do you feel if this feature IS present?" (functional)
2. "How do you feel if this feature is NOT present?" (dysfunctional)

Cross-reference answers to classify.

**Category migration (critical in 2025–2026):** Kano categories are not static. AI-powered or novel features frequently migrate from Attractive → One-dimensional → Must-be within 12–18 months as competitors copy and user expectations normalize. Run a Kano pulse at least quarterly for any market with rapid AI feature adoption — what delighted users last year is baseline expectation today. [Source: Kano Analysis — Hypersense Software (January 2025) https://hypersense-software.com/blog/2025/01/12/kano-analysis-in-software-development/]

**When to use:** UX-driven prioritization, user satisfaction optimization.
**Strengths:** User-centric, reveals hidden delighters.
**Weaknesses:** Requires user research data; categories shift over time (especially fast in AI-feature markets). A one-time Kano survey is not sufficient — treat it as a recurring measurement, not a one-shot classification.

---

## 7. Value vs Effort Matrix

**Axes:**
- X: Effort (Low → High)
- Y: Value (Low → High)

**Quadrants:**
| Quadrant | Value | Effort | Action |
|----------|-------|--------|--------|
| Quick Wins | High | Low | Do first |
| Major Projects | High | High | Plan carefully |
| Fill-ins | Low | Low | Do if time allows |
| Thankless Tasks | Low | High | Avoid or defer |

**When to use:** Team workshops, visual alignment, quick consensus.
**Strengths:** Intuitive, collaborative, good for teams.
**Weaknesses:** Low precision, groupthink risk in workshops.

---

## 8. AHP + LLM (Analytic Hierarchy Process with LLM assistance)

**Formula:** Pairwise comparison matrix → normalized eigenvector → priority weights per criterion

**Workflow:**
1. Define 3–8 criteria (e.g., user value, technical debt reduction, strategic alignment, time criticality)
2. Ask an LLM to propose pairwise importance ratios (1–9 scale) for each criterion pair — use as calibration anchors only
3. Team reviews and adjusts each ratio; rebuild matrix; compute eigenvector
4. Apply criterion weights to score each candidate item
5. Run consistency ratio check (CR < 0.1 = acceptable; CR ≥ 0.1 = recalibrate)

**When to use:** Complex decisions with 5+ criteria that conflict (e.g., simultaneous roadmap, risk, and cost optimization). Too heavyweight for weekly grooming — reserve for quarterly strategic prioritization or when WSJF/RICE rankings are contested.

**AI-assist rule:** LLM-generated pairwise ratios must survive at least one round of team challenge before being accepted. Treat LLM output as a starting anchor, not the score. [Source: arXiv 2402.07404 — Enhancing Multi-Criteria Decision Analysis with AI: Integrating AHP and GPT-4 for Automated Decision Support https://arxiv.org/abs/2402.07404]

**LLM scoring for requirements (2025 research):** A web-based tool using AI agents + prompt engineering to automate task prioritization across MoSCoW, AHP, and 100-Dollar-Test showed LLMs distribute automation at scale but require human validation to control hallucination risk. [Source: arXiv 2405.01564 — Prioritizing Software Requirements Using Large Language Models https://arxiv.org/abs/2405.01564]

**Strengths:** Handles multi-criteria trade-offs rigorously; LLM acceleration reduces manual pairwise work for large criterion sets.
**Weaknesses:** Consistency ratio failures require full matrix rebuild; LLM hallucinations on domain-specific ratios require expert review; overkill for < 5 criteria.
