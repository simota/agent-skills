# Narrative Arc Design

## Purpose

Design a presentation's story structure before any slide is drafted. A talk without an arc collapses into a list of facts; a clear arc makes the audience remember one thing and act on it.

## Scope Boundary

- IN scope: arc framework selection, beat-by-beat outline, hook design, call-to-action shaping, tension/resolution pacing.
- OUT of scope: slide-level visual design (`visual` subcommand), framework-specific syntax (`marp`/`reveal`/`slidev`), delivery technique (`rehearsal`).

## Core Concepts

### The "One Memorable Sentence" Test

Every talk must compress to a single sentence the audience can repeat 24 hours later. If the sentence cannot be written, the arc is not yet ready. This is Nancy Duarte's "Big Idea" gate from *Resonate*.

### Contrast as Engine

Duarte's analysis of canonical talks (King's "I Have a Dream", Jobs's iPhone keynote) shows audiences engage when speakers oscillate between **what is** and **what could be**. Flat narration loses attention within 90 seconds.

### Recommended Frameworks

| Framework | Source | Beats | Best For |
|-----------|--------|-------|----------|
| Pixar Formula | Emma Coats (Pixar) | Once upon a time → Every day → One day → Because of that → Until finally | Product launches, customer stories |
| Hero's Journey (Compressed) | Joseph Campbell / Christopher Vogler | Ordinary world → Call → Threshold → Trial → Transformation → Return | Keynotes, vision talks |
| Problem-Solution-Benefit | Classic sales / B2B | Status quo pain → Why now → Solution → Proof → Benefit → CTA | Sales decks, internal proposals |
| Minto Pyramid | Barbara Minto (McKinsey) | Answer first → Why (3 supporting arguments) → How (data per arg) | Executive briefings, board updates |
| Andy Raskin's Strategic Narrative | Andy Raskin | Name the change → Stakes → Promised land → Obstacles → Evidence | Pitch decks, fundraising |
| What/So What/Now What | Borton (1970) reflective model | Observation → Implication → Action | Retrospectives, post-mortems, lessons-learned |

### Arc Selection Heuristics

| Audience Signal | Recommended Arc |
|-----------------|----------------|
| Time-constrained executives | Minto Pyramid (answer first) |
| Investors / fundraising | Strategic Narrative (Raskin) |
| Engineers / technical peers | Problem-Solution-Benefit with concrete data |
| General / mixed audience at conference | Hero's Journey or Pixar Formula |
| Internal team retrospective | What / So What / Now What |

### Hook Construction (First 90 Seconds)

The hook must land within the first 90 seconds. Patterns that consistently work:

1. **Concrete contradiction** — "We doubled traffic and revenue dropped 40%."
2. **Audience-shared pain** — "Raise your hand if your last incident review felt like theater."
3. **Counterfactual question** — "What would your code look like if tests were free?"
4. **Stat that breaks expectation** — "73% of AI agent failures are context failures, not model failures."

Avoid: speaker bio, conference thanks, agenda slides — these waste the highest-attention window.

### Tension / Resolution Pacing

Within each beat, alternate tension (problem, conflict, surprising data) and resolution (insight, evidence, technique). The Duarte sparkline visualization plots time on the X axis and "what is" vs "what could be" on the Y axis; healthy talks oscillate, flat lines bore.

### Call to Action

Every talk ends with a CTA. CTAs come in three sizes:

| Size | Effort | Example |
|------|--------|---------|
| Small | < 5 minutes | "Star this repo" / "Tweet one takeaway" |
| Medium | < 1 hour | "Try the demo on your own codebase tonight" |
| Large | Multi-week | "Adopt this framework on your next project" |

Mix one of each; do not end with vague "thank you".

## Workflow

1. **Define the Big Idea** — write the one memorable sentence. If you cannot, do not proceed.
2. **Identify audience archetype** — executive / engineer / mixed / customer / internal team.
3. **Select arc framework** from the table above.
4. **Outline beats** — one bullet per beat, no slide content yet.
5. **Insert tension/resolution markers** — annotate each beat with `T` (tension) or `R` (resolution); ensure oscillation.
6. **Design the hook** — pick one of the four patterns; draft the opening 90 seconds verbatim.
7. **Design the CTA** — three sizes, concrete actions.
8. **Walk the sparkline** — visualize "what is" vs "what could be" over time; flatten = revise.

## Output Template

```yaml
narrative_design:
  big_idea: "One sentence the audience repeats tomorrow"
  audience: executive | engineer | mixed | customer | team
  arc_framework: Pixar | Hero | PSB | Minto | Raskin | WhatSoWhat
  beats:
    - id: 1
      label: "Hook"
      type: T | R
      content: "..."
      duration_sec: 90
    - id: 2
      label: "..."
      ...
  hook_pattern: contradiction | shared_pain | counterfactual | shocking_stat
  hook_verbatim: "First 90 seconds, written out"
  cta:
    small: "..."
    medium: "..."
    large: "..."
  sparkline_check: PASS | FLAT(beat=N)
```

## Anti-Patterns

- Starting with self-introduction or agenda — burns the prime hook window.
- Three-act structure with no tension oscillation — feels academic.
- CTA is "any questions?" — no behavioral intent.
- Big Idea is two sentences joined by "and" — not one idea, abandon and re-scope.
- Borrowing TED-style cadence on a 5-minute LT — formats demand different arcs.
- Choosing the framework after writing slides — reverse-engineering an arc onto slides almost always fails.

## Deliverable Contract

A narrative design is complete when:

- Big Idea is one sentence under 20 words.
- Arc framework chosen with explicit reason.
- Every beat has T/R label and second-budget.
- Hook is written verbatim (not summarized).
- CTA covers small / medium / large.
- Sparkline check passes (no two adjacent beats share T/R label without justification).

Hand off to `draft` (slide content) only after this contract passes.

## Format-Specific Beat Budgets (verified 2026-05)

Hard time formats override the arc framework. Validate the beat list against the format's clock before drafting.

| Format | Total | Per-slide | Beats supported | Source |
|--------|-------|-----------|-----------------|--------|
| Pecha Kucha (20×20) | 6 min 40 s | 20 s auto-advance, 20 slides | 3–5 beats; no demo | https://en.wikipedia.org/wiki/PechaKucha |
| Ignite (20×15) | 5 min | 15 s auto-advance, 20 slides | 3–4 beats; no Q&A | Ignite Talks format |
| Lightning Talk | 5 min | speaker-paced | 1 arc, 1 CTA | Conference-dependent |
| Standard conference talk | 20–30 min | ~1 slide/min | Full arc + Q&A | — |
| TED | 18 min hard cap | speaker-paced | Single Big Idea | TED2026 program — https://conferences.ted.com/ted2026 |

For 20×20 / 20×15 formats, the Hero's Journey and Strategic Narrative arcs do not fit — collapse to Problem-Solution-Benefit or What/So What/Now What.

## References

- Nancy Duarte, *Resonate: Present Visual Stories that Transform Audiences* (2010).
- Andy Raskin, "The Greatest Sales Deck I've Ever Seen" (Medium, 2016) — Strategic Narrative.
- Barbara Minto, *The Pyramid Principle* (1987) — Minto Pyramid.
- Christopher Vogler, *The Writer's Journey* (1992) — compressed Hero's Journey.
- Emma Coats, "22 Story Basics" (Pixar, 2011) — Pixar Formula.
- Chris Anderson, *TED Talks: The Official TED Guide to Public Speaking* (2016); TED2026 program, "All of Us" theme — https://conferences.ted.com/ted2026
