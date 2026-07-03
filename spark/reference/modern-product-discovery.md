# Modern Product Discovery

Purpose: guide Spark through modern discovery frameworks that improve opportunity selection before proposal writing.

## Contents
- Opportunity Solution Tree
- Continuous discovery cadence
- Shape Up
- Outcome-Driven Innovation
- AI-assisted discovery
- Discovery input checklist

## Opportunity Solution Tree (OST)

Map Spark phases to OST:

| OST layer | Spark phase | Use |
| --- | --- | --- |
| Outcome | `IGNITE` | clarify the business result |
| Opportunity | `IGNITE -> SYNTHESIZE` | identify and rank unmet needs |
| Solution | `SYNTHESIZE -> SPECIFY` | define candidate proposals |
| Assumption Test | `VERIFY` | plan validation before build |

Best practices:
- decompose large opportunities into smaller sub-opportunities
- test assumptions, not only full solutions
- update the tree weekly as a living artifact

## Continuous Discovery Habits

Core rule:
- discovery is a weekly rhythm, not a kickoff ceremony

Recommended cadence:
- Monday: review learnings and update the OST
- Tuesday to Thursday: `2-3` customer interviews per week plus assumption tests
- Friday: synthesize and choose the next opportunity

Avoid:
- batch discovery only at project start
- PM-only discovery silos
- jumping to solutions before synthesis
- optimizing only existing areas without exploration

## Shape Up

Key concepts:

| Concept | Meaning |
| --- | --- |
| `6-week cycle` | fixed delivery window for meaningful work |
| `Shaping` | define the pitch at a high level before commitment |
| `Betting Table` | leadership decides whether to invest |
| `Cooldown` | bug fixes, exploration, and next-cycle preparation |

How Spark uses it:
- treat the proposal as the pitch
- define appetite before expanding scope
- combine appetite with `RICE Score` to avoid overcommitment

## Outcome-Driven Innovation (ODI)

Opportunity Score:

```
Opportunity Score = Importance + max(Importance - Satisfaction, 0)
```

Opportunity zones:

| Zone | Importance | Satisfaction | Strategy |
| --- | --- | --- | --- |
| `Underserved` | high | low | invest first |
| `Overserved` | low | high | reduce or avoid investment |
| `Appropriately Served` | high | high | maintain quality |

Spark integration:
- extract job steps from existing data and workflows
- estimate `Importance` and `Satisfaction`
- prioritize `Underserved` opportunities during `IGNITE`

## AI-Assisted Discovery

Good use cases:

| Area | AI assist | Typical gain |
| --- | --- | --- |
| interview synthesis | summarization and pattern extraction | about `50%` faster qualitative synthesis |
| artifact drafting | PRDs and user-story drafts | about `26%` time savings |
| brainstorming | edge cases and concept expansion | wider idea set |
| prototyping | interactive mockups | faster validation loops |

Warnings:
- AI summaries may miss `20-40%` of important details
- AI is additive, not a replacement for speaking with users
- human review is mandatory for synthesized insights

## Discovery Input Checklist

Quantitative inputs:
- underused features or dormant datasets from `Pulse`
- funnel drop-off points
- error-rate and support-ticket trends

Qualitative inputs:
- research synthesis from `Field`
- feedback clusters from `Voice`
- competitor gaps from `Compete`

Opportunity evaluation:
- map insights to the OST opportunity layer
- use ODI scoring where possible
- confirm technical feasibility with `Scout` or `Lens`

## Discovery Discipline (Core Contract rationale + sources)

Extended rationale and sources for the Spark Core Contract discovery rules:

- **Name by the user problem, not the solution** — discovery starts with pain points, not feature shapes. [Source: productboard.com — product discovery framework; herbig.co — product discovery guide]
- **Outcomes, not outputs** — define the behavioral change or business impact, not just the feature shape. [Source: itonics-innovation.com — outcome-oriented development trend 2026]
- **OST → OKR alignment** — the OST metric must align with a KPI from your OKRs; only initiatives that can move that metric warrant active investigation. [Source: producttalk.org — Teresa Torres CDH framework]
- **Fail Condition** — teams are overly lenient with success criteria, but a fail condition (the measurement that disproves the hypothesis) forces intellectual honesty. [Source: kromatic.com — Lean Startup validation]
- **Weekly discovery rhythm** — Torres's minimum cadence is weekly customer touchpoints (interviews, 5-second tests, prototype probes). If a proposal rests on research older than ~4 weeks, refresh at least one evidence source before handoff — evidence decays. [Source: producttalk.org — Continuous Discovery Habits; maze.co — continuous product discovery]
- **Progress, not activities** — frame customer jobs as progress sought, not activities. "Users want to generate reports" is an activity; the real job is the progress it unlocks ("demonstrate progress to stakeholders" or "cover myself in an audit"). Activity framing produces feature shapes; progress framing reveals opportunities. [Source: kaizenko.com — JTBD framework; productschool.com — JTBD framework]

## Non-Consumption & Workarounds

The most overlooked competitor is "nothing." Include non-consumption and workarounds in competitive framing:

- Airbnb found 40% of guests would not have traveled at all without it; they were competing with non-consumption, not hotels.
- Compensating behaviors (manual spreadsheets, email threads, copy-paste workflows) are hiring signals that reveal unmet jobs.

[Source: Christensen Institute — Non-consumption is your fiercest competition; thrv.com — Jobs-to-be-Done]

## AI-Assisted Discovery (2026 addenda)

Extends the AI-Assisted Discovery section above:

- **Encode quality gates** so AI-assisted automation (feedback theme analysis, opportunity backlogs linked to user goals, story-map slices reflecting technical constraints, comparisons against prior work) is helpful but never unaccountable. [Source: storiesonboard.com — AI agents in PM 2026]
- **Methodology-first, not prompt-first** — AI output quality depends on structured inputs (explicit OST node, persona, hypothesis, fail condition), not prompt cleverness. 94% of enterprise PMs use AI daily; the gap between transformative and merely-helpful traces to input quality, not tool choice. Feed Pulse/Voice/Compete findings through OST/JTBD framing before asking AI to synthesize. [Source: productboard.com — AI product discovery; ainna.ai — AI product management 2026]
- **Collapse low-value steps, not judgment steps** — AI is strong at interview transcription, theme clustering, and surface-level synthesis. Keep persona selection, fail-condition definition, and cross-opportunity trade-off reasoning human-led; AI-generated versions anchor to training-data averages, not the current customer. [Source: producttalk.org — 2026 roadmap / AI-powered discovery]
