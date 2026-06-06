# Jobs-to-be-Done (JTBD) Reference

Purpose: Apply Clayton Christensen's Jobs-to-be-Done framework to reframe a market, product, or feature in terms of the *job* a customer is hiring the product to do — not by product category or demographic. Produces job statements, forces-of-progress analysis, and competitive-set-by-job mapping.

## Scope Boundary

- **helm `jtbd`**: Christensen JTBD — strategic framing (this document).
- **helm `porter` (elsewhere)**: Industry structure. JTBD and Porter are complementary; Porter frames incumbents; JTBD reframes the market by customer intent.
- **Spark (elsewhere)**: Feature-level proposals. JTBD feeds into Spark by identifying under-served job dimensions.
- **Researcher (elsewhere)**: Primary research. JTBD framework; Researcher conducts interviews.
- **Voice (elsewhere)**: Customer feedback analysis. JTBD can be informed by NPS verbatims but is more structural.
- **Spark vs. JTBD**: Spark proposes features; JTBD reframes the strategic question about what the product should even be.

## Core Concepts

### Job Statement Syntax

```
When [situation / context],
I want to [motivation],
so I can [expected outcome].
```

Example — "milkshake":
> When I'm commuting alone on a long drive in the morning, I want to have one hand occupied and a pleasant taste for 30 minutes, so I can stay engaged while my body is idle.

Compare to bad framing:
> Morning breakfast shake for commuters aged 25-40. (Demographic, not job.)

### Three Job Dimensions

| Dimension | Description | Example for the milkshake |
|-----------|-------------|----------------------------|
| Functional | Practical task | Thick enough to last 30 min; one-handed |
| Emotional | Internal feelings | Feels like a small treat; starts the day right |
| Social | How it looks to others | Not childish; acceptable to order as an adult |

A product wins by covering all three. Competitors often cover only functional.

## Four Forces of Progress

Understand the customer's *switching* moment — why they move from their current solution to yours (or why they don't).

```
              PUSH of current situation
              (dissatisfaction, friction)
                       │
                       ▼
       ┌──────────── SWITCH ────────────┐
       │                                 │
       ▼                                 ▼
 HABIT of present            ANXIETY of new solution
 (inertia, familiarity)      (risk, learning curve)

                       ▲
                       │
              PULL of new solution
              (attraction, promise)
```

- **Push > Pull > Anxiety + Habit** → customer switches.
- Design the product by **increasing push (surface the problem)** and **pull (articulate the outcome)**, while **reducing anxiety (guarantees, trial, onboarding)** and **habit (migration tools, one-click switch)**.

Anxiety and habit are often underweighted. A superior product that does not reduce switching cost loses.

## Competitive Set by Job

Traditional competitive analysis: "What other widget companies sell widgets?"

JTBD analysis: "What does the customer currently hire to do the same job?"

The milkshake competes with:
- Bananas (quick, one-handed, but too fast)
- Donuts (one-handed, messy, not filling)
- Bagels with cream cheese (needs two hands)
- Coffee (not filling; doesn't fight boredom)
- Nothing (skip breakfast)

Widen the competitive set. The real competitor is often "do nothing" or "non-consumption".

## JTBD Workflow

```
OBSERVE     →  witness customer in situation (or review interview transcripts)
            →  note what they stopped doing, what they hired

STATEMENT   →  write job statement: When [situation], I want [motivation], so I can [outcome]
            →  include functional + emotional + social

FORCES      →  map push / pull / anxiety / habit
            →  quantify where possible

SET         →  identify what's currently hired (competitive set by job)
            →  include "nothing" and non-consumption

GAPS        →  find unmet job dimensions
            →  prioritize job dimensions with largest gap × largest market

DESIGN      →  strategy: meet unmet dimensions; reduce anxiety + habit
            →  hand off feature implications to Spark
```

## Interview Guide Sketch

When conducting JTBD interviews (hand to Researcher for full design):

1. "Take me back to the moment you first realized you needed [product]."
2. "What were you doing when that happened?"
3. "What did you try before [product]?"
4. "What almost stopped you from buying?"
5. "Who else did you talk to about this decision?"
6. "What did you expect it to do?"
7. "How did you measure whether it worked?"

Always ask about the *moment* — the specific situation. Abstract "why" questions yield demographics, not jobs.

## Output Template

```markdown
## JTBD Analysis: [Product / Market]

### Job Statement
"When [situation], I want to [motivation], so I can [outcome]."

### Dimensions
| Dimension | Customer's ideal |
|-----------|------------------|
| Functional | [list] |
| Emotional | [list] |
| Social | [list] |

### Forces of Progress
| Force | Current state | Strength (1-5) |
|-------|---------------|----------------|
| Push (of current situation) | [what frustrates] | [score] |
| Pull (of new solution) | [what attracts] | [score] |
| Anxiety (of switching) | [fear, risk] | [score] |
| Habit (of present) | [inertia] | [score] |

**Switch likelihood**: Push + Pull vs Anxiety + Habit = [net]

### Competitive Set by Job
| Current solution | How it serves the job | Limitation |
|-----------------|----------------------|------------|
| [option A] | [coverage] | [gap] |
| [option B] | ... | ... |
| Doing nothing | ... | ... |

### Unmet Dimensions
- [Dimension X] — large gap, high market — PRIORITIZE
- [Dimension Y] — small gap — lower priority

### Strategic Recommendation
- **Increase push**: [tactic]
- **Increase pull**: [tactic]
- **Reduce anxiety**: [tactic — guarantee, trial, onboarding]
- **Reduce habit**: [tactic — migration tool, one-click switch]

### Handoffs
- Spark: feature implications from unmet dimensions
- Researcher: validate job statement via customer interviews
- Compete: benchmark how incumbents handle forces
- Voice: mine existing NPS verbatims for job-statement support
- Magi: Go/No-Go on strategic pivot
- Saga: customer-story framing that lives inside the job
```

## Anti-Patterns

| Anti-pattern | Fix |
|--------------|-----|
| Job statement = demographic | "When I'm [feeling], I want [action]" — situation-anchored |
| Only functional dimension | Always include emotional + social |
| Ignoring anxiety and habit | They often outweigh push + pull |
| Narrow competitive set | Include "nothing" and non-consumption |
| Multiple jobs in one statement | One job per statement; spawn more statements if needed |
| Inferring jobs from demographics | Observe situations; interview about the moment |
| Jobs-as-features | Jobs are outcomes, not features |

## Deliverable Contract

When `jtbd` completes, emit:

- **Job statement** in When/I want/So I can form.
- **Three dimensions** (functional / emotional / social) with customer's ideal outcomes.
- **Four forces** (push/pull/anxiety/habit) with strength scores.
- **Competitive set by job** including "nothing".
- **Unmet dimensions** prioritized.
- **Strategic recommendations** by force.
- **Handoffs**: Spark, Researcher, Compete, Voice, Magi, Saga.

## References

- Clayton Christensen — *Competing Against Luck* (definitive JTBD). Christensen passed away **2020-01-23**; the framework is now stewarded by the **Christensen Institute** (christenseninstitute.org), which since 2024 has published a running series — `AI and Disruptive Innovation`, `Stewardship in AI`, `Navigation & Guidance in the Age of AI: 5 Trends to Watch (2025)` — applying JTBD-adjacent reasoning to GenAI products and education.
- Tony Ulwick — *JOBS TO BE DONE: Theory to Practice* (the refined 2016+ Strategyn formulation; companion site jobs-to-be-done-book.com). Ulwick's **Outcome-Driven Innovation (ODI)** treats job statements as the *stable* unit and customer-desired outcomes as the measurable, prioritizable layer — Strategyn case studies cover Microsoft, Bosch, Abbott Medical Optics, Arm & Hammer, Kroll Ontrack, and Hussmann.
- Bob Moesta & Greg Engle — *Demand-Side Sales 101* (Lioncrest, 2020). Reframes selling as "help the customer make progress." Re-Wired Group continues to run JTBD workshops through 2026; pair with Moesta's *Learning to Build* as the practitioner follow-up. Distinguishes **supply-side selling** (features and persuasion) from **demand-side facilitation** (understand the job, reduce switching cost).
- Alan Klement — *When Coffee and Kale Compete* (job statement examples)
- Harvard Business Review — "Know Your Customers' Jobs to Be Done" (Christensen et al., 2016)
- Jim Kalbach — *The Jobs To Be Done Playbook* (practitioner guide)

### AI-Era JTBD Considerations (2025-2026)

- **"Job" of an AI product is unstable**: GenAI tools often get hired for a stated job (draft email) but absorb adjacent jobs (think out loud, replace a colleague conversation). Re-interview cohorts every 90 days; static job statements decay faster than in classical SaaS.
- **The competitive set now includes the model itself**: For thin-wrapper AI products, "the model directly via chat" replaces "doing nothing" as the dominant non-consumption alternative. Map it explicitly in the competitive-set-by-job table.
- **Forces of progress shift**: *Anxiety* now leads with hallucination risk, IP/data leakage, and audit traceability; *Habit* now includes "I already paste into ChatGPT." Reducing anxiety via grounded citations and SOC2/ISO 42001 evidence is often higher-leverage than adding pull.
