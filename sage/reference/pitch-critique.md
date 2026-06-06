# Pitch Critique

**Purpose:** Reference for the `pitch` Recipe — critique elevator / Demo Day / investor Q&A pitch material.
**Read when:** You are running `pitch` and need granularity templates, the STRUCTURE → CLARITY → TENSION → RESONANCE → REVISE flow, or pitch anti-patterns.

The `pitch` Recipe is **deliverable critique**, not bottleneck identification. Output is line-level revisions, slide cuts, and pitch anti-pattern citations — not weekly action items. Follow this file end-to-end when running `pitch`; do not load `office-hours-format.md` or `probing-questions.md`.

## Granularity

Confirm granularity at FRAME before critiquing. Refuse to critique without one selected.

| Granularity | Format | Length | Goal |
|-------------|--------|--------|------|
| `30sec` | Single-paragraph elevator pitch | 30-60 sec read aloud, 60-100 words | Stranger walks away knowing what you do, who buys it, and what traction proves it works |
| `demoday` | Slide deck or spoken pitch | 3-10 min, 8-15 slides | Audience leaves with clear `what / who / why now / proof / ask` |
| `qa` | Investor Q&A simulation | 5-15 hostile questions | Founder can answer skeptical, dilutive, or trap questions without flinching |

## Workflow

### FRAME (1-2 exchanges)
- Confirm granularity (`30sec` / `demoday` / `qa`).
- Confirm audience (seed VC / Demo Day investor / corporate buyer / journalist).
- Confirm constraint (time limit, slide count, written vs spoken).
- Ingest material verbatim. If material is missing, request it before critique.

### STRUCTURE
Check the canonical arc.

**30-second arc (3 beats):**
1. Definition: "We make X for Y."
2. Why now / why us: "We do this because Z."
3. Traction proof: "And [number] [users/revenue/growth]."

**Demo Day arc (7 beats):**
1. Hook (what you do, in one sentence, slide 1)
2. Problem (specific persona pain, not generic)
3. Solution (mechanic, not metaphor)
4. Traction (numbers, week-over-week or month-over-month)
5. Market (bottoms-up, not top-down)
6. Team (relevance, not just credentials)
7. Ask (specific funding amount + use of funds + milestone it unlocks)

**Q&A:** no canonical arc; verify the founder can answer hostile questions in `Common Hostile Questions` below.

Score each beat 0-2: 0 missing, 1 weak/buried, 2 clear. Sum out of arc total. Below ~70% → propose restructure.

### CLARITY
Apply the **smart-non-expert test**: a smart non-expert from outside your domain hears the pitch once. Can they restate in one sentence what you do, who buys it, and how it works mechanically?

If no, identify which beat failed:
- Definition unclear → demand a literal "X for Y" rewrite where X is concrete.
- Mechanic unclear → demand one sentence describing how value is created end-to-end.
- Customer unclear → demand a specific persona (job title, company size, problem).

### TENSION
Pitches without tension feel like brochures. Tension comes from specific pain → demonstrated relief.

Check:
- Is there a moment of *named pain* (a specific user, a specific cost, a specific failure)?
- Is there a moment of *demonstrated relief* (a real before/after, a customer quote, a metric delta)?
- Does the founder *care visibly* about the problem, or is this an opportunity story?

Brochure pitches are rejected. Demand a customer voice or live demo moment.

### RESONANCE
Pitches without resonance fail to be remembered an hour later.

Check:
- Is there one *line* an investor would repeat to a partner? (Hook, headline metric, customer quote.)
- Is there one *image* an investor would remember? (Demo screen, before/after, founder credibility moment.)
- Are abstract claims grounded in concrete artifacts? ("$2.4M ARR growing 22% MoM" beats "rapidly growing".)

If nothing repeatable, propose adding one specific moment.

### REVISE
Output line-level revisions. For each problem found in STRUCTURE/CLARITY/TENSION/RESONANCE:

| Field | Rule |
|-------|------|
| **Locator** | Slide number, paragraph, or quote of original line |
| **Issue** | One sentence stating what's wrong; cite anti-pattern ID if applicable |
| **Replace with** | A concrete rewrite, not a direction |
| **Why** | Pattern citation or principle (one line) |

Refuse to leave the session with directions like "make it more concrete" — produce the concrete line.

## Common Hostile Questions (qa mode)

Investor Q&A patterns the founder must rehearse before any meeting.

| Question | What it tests | Failure mode |
|----------|---------------|--------------|
| "Why hasn't [BigCo] built this?" | Idea-maze depth (P-53) | Founder dismisses or panics |
| "What's your moat?" | Defensibility thinking | Vague "first mover" answer |
| "Who's your competition?" (after they've claimed none) | Honesty + market awareness | "We have no competition" (PA-06) |
| "What's your CAC and LTV?" | Unit economics literacy | Doesn't know either number |
| "Walk me through your last 3 months of revenue." | Real traction vs vanity | Reports MAU instead |
| "How will you spend this round?" | Capital efficiency | Generic "team and growth" |
| "What happens if you don't raise this round?" | Default-alive thinking (P-03) | Existential panic answer |
| "Why are you the right team for this?" | Founder-market fit | Generic credentials, no relevance |
| "What's the riskiest thing about your business?" | Self-awareness | "Nothing really" or evasion |
| "What did the last 5 churned users say?" | User-contact depth (P-12) | Hasn't talked to churned users |

Simulate ≥5 in any `qa` session. Score answer quality 0-2. Surface failures as REVISE items with rehearsed replacement answers.

## Pitch Anti-Patterns

Surface explicitly by ID when ≥1 signal is observed (single signal threshold — pitch problems are usually visible at first read).

| ID | Name | Signal | Fix |
|----|------|--------|-----|
| `PA-01` | Lede burial | "What we do" not stated by slide 3 / first 30 seconds | Move definition to slide 1 / first sentence |
| `PA-02` | Vague problem | Generic pain ("It's hard to X") without persona, cost, or frequency | Anchor in a named persona's specific cost |
| `PA-03` | Analogy-only definition | "We're Uber for Y" without defining the mechanic | Add one mechanic sentence after the analogy |
| `PA-04` | Top-down TAM | "$X trillion market" with no bottoms-up build | Replace with `# customers × ACV × penetration` math |
| `PA-05` | Adjective inflation | "Revolutionary", "disruptive", "seamless", "next-gen", "AI-powered" used as substantive claim | Cut adjective; replace with measurable comparison |
| `PA-06` | "No competition" | Founder claims no competitors | List 3-5 alternatives (including status quo / Excel / spreadsheets); state your specific edge |
| `PA-07` | Credentials before product | Team slide before product/traction | Reorder: product → traction → team |
| `PA-08` | Demo theater | "Demo" is logos and screenshots, not a working flow | Replace with a 30-sec live or recorded flow |
| `PA-09` | Hidden ask | No specific funding amount, milestone, or use-of-funds | Add: amount + use-of-funds buckets + milestone unlocked |
| `PA-10` | Future tense product | Everything is "will be" / "we plan to" / "in v2" | Cut all future-tense claims; speak only about what exists today |
| `PA-11` | Slide-reading | Spoken pitch verbatim matches slide bullets | Slides become images / single-line headlines; speech adds context |
| `PA-12` | Q-deflection | Founder answers a different question than asked | Force the founder to repeat the question, then answer it directly |
| `PA-13` | Metric without unit | "We grew 300%" without time period or base | Always state: metric (number) over period (time) from base (number) |
| `PA-14` | Investor-pleasing | Pitch is shaped to what investors "want to hear" rather than what's true | Surface as P-40 (customer signal precedes investor signal) |
| `PA-15` | Model-as-moat (2026) | Pitch leans on the foundation model (GPT-4o / Claude / Gemini) as the differentiator; no proprietary data, workflow embedment, or distribution edge | Replace with one of: proprietary dataset, signed integration into a system of record, regulated-vertical depth. Cite P-60 |
| `PA-16` | Tool pitch instead of work pitch (2026) | Deck sells "AI-powered tool" / "copilot" / "assistant"; no replaced budget line, no per-outcome pricing, no SLA | Restructure to outcome-based: "We do JOB, customer pays per JOB completed, SLA is X." Cite P-61 (Sequoia "Services: The New Software" — sequoiacap.com/article/services-the-new-software/) |
| `PA-17` | Inflated ARR (2026) | ARR claim mixes pilots, LOIs, credits, or consulting with recurring revenue; founder hesitates when asked for the bank-deposited number | Define ARR explicitly (contracted recurring billed last 30 days), restate every number; disclose pilots separately. Cite AP-19 / YC Apr 2026 "Be Truthful" |

## 2026 AI-Era Deck Expectations

Sequoia AI Ascent 2026 (Apr 2026, sequoiacap.com/article/ai-ascent-2026/) and "Services: The New Software" (sequoiacap.com/article/services-the-new-software/) signaled what a current AI pitch deck must address beyond the classic arc:

- **Reliability and evaluation** — show how you measure agent correctness; cite eval set, pass rate, regression cadence.
- **Data advantage** — what proprietary signal does your agent see that the foundation lab does not?
- **Workflow depth** — which system of record are you embedded in, and what would it cost the customer to rip out?
- **Customer ROI** — replaced budget line in dollars or hours, not a productivity adjective.
- **Pricing power** — per-seat is the weak default; per-outcome, per-resolved-ticket, or per-completed-job is the strong frame.
- **Unit economics path** — for AI-first products, investors expect a credible path to 70%+ steady-state gross margin (current AI-SaaS baseline is 50-60% GM; classical SaaS is ~75%). Cite AP-18 if unaddressed.

If any of these is missing on a `demoday` deck in 2026, surface as a STRUCTURE deficit and demand a slide for the gap.

## Output Contract

Each `pitch` session must produce:

- Granularity confirmed (`30sec` / `demoday` / `qa`)
- Structure score (e.g., "5/7 Demo Day beats clear")
- Clarity verdict (smart-non-expert test pass/fail)
- Tension verdict (named pain + demonstrated relief present?)
- Resonance verdict (one repeatable line + one memorable image?)
- Anti-patterns detected (list of `PA-` IDs with signals)
- Line-level revisions (locator + issue + replacement + why)
- One-sentence next step ("Rewrite slides 1-3 and re-run pitch flow")

## Tone

Pitch critique is the most direct mode in sage. The founder is asking for criticism on a deliverable. Hedge-free. Pattern-matched. Specific. Avoid "you might consider" / "perhaps" / "have you thought about" — replace with "this fails because X; rewrite as Y".

The kindness is in the specificity. Vague advice wastes the founder's prep time before a real meeting.

## Boundary

Do not generate the founder's pitch from scratch. Do not invent customer quotes, traction numbers, or team credentials. If the original material lacks the required substance, the verdict is "the underlying business doesn't yet support this pitch — go back to `1on1` flow on the missing fundamental (traction, customer specificity, runway)" — not a fabricated rewrite.
