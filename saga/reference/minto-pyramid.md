# Minto Pyramid Principle Reference

Purpose: Apply Barbara Minto's Pyramid Principle to executive/stakeholder narrative delivery — board memos, investor updates, exec briefings, decision docs. Pyramid Principle is *answer-first* communication: the conclusion at the top, supporting arguments grouped MECE, evidence at the bottom. Combine with SB7/Promised Land for emotional resonance underneath the structure.

## Scope Boundary

- **saga `pyramid`**: Minto Pyramid for top-down narrative delivery (this document).
- **saga `narrative` (elsewhere)**: Product positioning. Pyramid is *delivery* of narrative; narrative is the *content*.
- **saga `story` / `customer` / `hero-journey` (elsewhere)**: Bottom-up emotional arcs. Pyramid is structurally inverse but content-compatible.
- **saga `bab` (`reference/before-after-bridge.md`)**: 3-beat emotional copywriting for LP/email/CTA — the opposite use case. **Choose BAB over Pyramid when the audience must *act* (commercial CTA), not *decide* (analytic conclusion).** Pyramid's governing thought is a deductive answer; BAB's Bridge is a conversion CTA. The two can combine — Pyramid as memo spine with a BAB excerpt as the customer-transformation illustration.
- **Scribe (elsewhere)**: Formal document authoring. Pyramid provides the structural skeleton Scribe fills in.
- **Stage (elsewhere)**: Slide generation — Pyramid maps directly to slide outlines.
- **Magi (elsewhere)**: Decision arbitration — Pyramid is the format Magi consumes.

## Core Principle

> **State the answer first. Group supporting arguments. Layer evidence at the bottom.**

Executives have ~30 seconds before deciding to read more. If your first sentence is context-setting, you've lost them. Pyramid Principle reorders the natural inductive flow (evidence → conclusion) into the *deductive* flow audiences need (conclusion → evidence).

```
                    ┌─────────────────────────┐
                    │  Governing Thought      │
                    │  (the answer, 1 line)   │
                    └───────────┬─────────────┘
                                │
              ┌─────────────────┼─────────────────┐
              ▼                 ▼                 ▼
      ┌────────────┐    ┌────────────┐    ┌────────────┐
      │ Argument 1 │    │ Argument 2 │    │ Argument 3 │
      │ (MECE)     │    │ (MECE)     │    │ (MECE)     │
      └─────┬──────┘    └─────┬──────┘    └─────┬──────┘
            │                 │                 │
        ┌───┴───┐         ┌───┴───┐         ┌───┴───┐
        ▼       ▼         ▼       ▼         ▼       ▼
      [evidence pieces — data, examples, citations, calculations]
```

## Three Rules

| Rule | Statement | Test |
|------|-----------|------|
| **Vertical** | Each layer answers the question raised by the layer above | Reader asks "why?" → next level answers it |
| **Horizontal** | Items in the same layer must be MECE (Mutually Exclusive, Collectively Exhaustive) | No overlap; nothing missing |
| **Logical** | Arguments at one layer follow either deduction (rule + case → conclusion) or induction (similar items → group) | Mixing is OK across layers, not within |

If any rule breaks, the pyramid falls. Most weak memos break **horizontal**: arguments overlap, miss a category, or are uneven in granularity.

## SCQA Opening

Before the pyramid, set the situation in **SCQA**:

| Beat | Purpose | Length |
|------|---------|--------|
| **Situation** | Common ground the reader already accepts | 1-2 sentences |
| **Complication** | What changed; what's at stake; why now | 1-2 sentences |
| **Question** | The question the reader is implicitly asking | 1 sentence |
| **Answer** | Your governing thought (top of pyramid) | 1 sentence |

SCQA → Pyramid is the canonical Minto flow. SCQA hooks; Pyramid delivers.

### SCQA example (illustrative)

| Beat | Text |
|------|------|
| Situation | "Our churn has held flat at 4.2% for three quarters." |
| Complication | "But cohort analysis shows month-six retention dropped 11 points in Q3." |
| Question | "Is this a leading indicator we should act on?" |
| Answer | "**Yes — and we should ship onboarding redesign before Q4 to prevent a 3-pt churn lift.**" |

That single bolded answer is then supported by the pyramid below it.

## When to Use Pyramid

| Context | Pyramid? | Why |
|---------|----------|-----|
| Board memo | Yes | Executives skim; need answer first |
| Investor update | Yes | Same — answer-first respects time |
| Engineering RFC | Mostly | Technical readers prefer the structure too |
| Decision doc / DACI | Yes | Decision = governing thought |
| Customer success story | No | Use Hero's Journey or Customer arc |
| Marketing landing page | No | Use BAB or SB7 — emotional first |
| Slide deck for execs | Yes | Each slide = one node in pyramid |
| Long-form thought piece | Sometimes | Pyramid + narrative anecdotes hybrid |
| Announcement to all-staff | No | Narrative + Pyramid hybrid; emotional matters |

Rule of thumb: **decision-driving content → Pyramid; emotional/narrative content → bottom-up storytelling**.

## Combining Pyramid with Saga Frameworks

Pyramid is structural; Saga's other frameworks are emotional. They combine:

| Combination | Use case |
|-------------|----------|
| Pyramid + SB7 | Executive ask backed by customer-hero context |
| Pyramid + Promised Land | Strategic shift / fundraise memo |
| Pyramid + Hero's Journey | Year-end review with anchor case study |
| Pyramid + BAB | One-pager with answer + Before/After context |

The pattern: **Pyramid for the spine, narrative for the muscle.** Open SCQA-style with a brief narrative anchor (one sentence), then deliver the Pyramid, then close with a narrative call to action.

## Argument Grouping Patterns

Three classic MECE groupings for the second layer:

| Pattern | Use when | Example |
|---------|----------|---------|
| **Time-based** | Process or sequence matters | "Q1: research / Q2: build / Q3: launch" |
| **Structure-based** | Components of a system | "People / Process / Technology" |
| **Degree-based** | Severity or priority | "Must / Should / Could" |

Mixing patterns within one layer breaks horizontal MECE. Pick one per layer.

## Workflow

```
INPUT      →  receive: audience, decision/ask, key data, length budget
           →  identify the *one* governing thought (answer in 1 sentence)

SCQA       →  draft Situation (common ground)
           →  draft Complication (what changed)
           →  formulate the Question the audience implicitly has
           →  state the Answer = Governing Thought

PYRAMID    →  list 3-5 arguments (MECE, parallel grammar)
           →  for each, list 2-4 evidence pieces
           →  test vertical: does each layer answer "why?" of the layer above?
           →  test horizontal: MECE — no overlap, nothing missing
           →  test logical: deduction or induction, not mixed

DRAFT      →  open with SCQA (≤ 4 sentences)
           →  state Governing Thought in bold
           →  one paragraph (or slide) per argument, lead-sentence first
           →  evidence as bullets / table / data callouts

REFINE     →  read top sentences only — does the standalone story make sense?
           →  if not, governing thought or arguments are wrong

DELIVER    →  output formatted memo or slide outline
           →  hand off to Stage for slides, Scribe for full doc, Magi for decision
```

## The "Read the Top Sentences Only" Test

A correctly structured pyramid passes this test: read only the SCQA + governing thought + first sentence of each argument. The reader should already understand the full case. Evidence is for those who want to dig.

If the top-sentence-only read leaves a gap, fix the structure — don't add more evidence.

## Output Templates

### Memo template

```markdown
## [Title — answer-driven, not topic-driven]

**Situation**: [common-ground sentence]
**Complication**: [what changed]
**Question**: [implicit question]
**Answer (Governing Thought)**: **[one bold sentence stating the conclusion or recommendation]**

### Why — Argument 1: [parallel-grammar lead sentence]
[Evidence: data, example, calculation]

### Why — Argument 2: [parallel-grammar lead sentence]
[Evidence]

### Why — Argument 3: [parallel-grammar lead sentence]
[Evidence]

### What we're asking
- **Decision needed**: [yes/no / approve / fund]
- **By when**: [date]
- **From whom**: [decision-maker / committee]
- **If not decided**: [what we lose]

### Risks & alternatives
- [Risk 1 + mitigation]
- [Alternative considered + why rejected]
```

### Slide outline template

```
Slide 1: Title — answer-driven
Slide 2: SCQA on one slide (4 lines)
Slide 3: Governing Thought (full-bleed, big text)
Slide 4: Argument 1 + supporting evidence
Slide 5: Argument 2 + supporting evidence
Slide 6: Argument 3 + supporting evidence
Slide 7: Decision asked + timing
Slide 8: Risks & alternatives
```

## Output Template

```markdown
## Pyramid Narrative: [Audience / Decision]

### Audience & Context
- **Audience**: [exec / board / investors / cross-functional leaders]
- **Decision/ask**: [what you need from them]
- **Length budget**: [memo length / slide count]

### SCQA
- **Situation**: [...]
- **Complication**: [...]
- **Question**: [...]
- **Answer (Governing Thought)**: [...]

### Pyramid Structure
| Layer | Content |
|-------|---------|
| Top | [Governing Thought, 1 sentence] |
| Argument 1 | [parallel sentence] |
| Argument 2 | [parallel sentence] |
| Argument 3 | [parallel sentence] |
| Evidence (per argument) | [bulleted under each] |

### MECE Check
- [ ] Arguments do not overlap
- [ ] Arguments collectively cover the question
- [ ] Parallel grammar across arguments
- [ ] Grouped by one pattern (time / structure / degree)

### Top-Sentence-Only Test
[Read SCQA + governing thought + lead sentence of each argument]
- [ ] Standalone story is coherent without evidence
- [ ] If not: restructure before delivery

### Anti-Pattern Check
Run the full AP-1~AP-9 checklist from `reference/anti-patterns.md` and report results in the standard format. Pyramid emphasizes AP-1 (Feature Dump — arguments must be MECE, not feature lists), AP-6 (Narrative Bias — exec memos need stated assumptions), AP-7 (Jargon Wall — must be accessible to non-technical execs), and AP-9 (Ad Copy Disguise — pyramid is analytic, not promotional).

### Decision Ask
- **Decision needed**: [...]
- **By when**: [...]
- **If not decided**: [cost of inaction]

### Combined Frameworks (if applicable)
- **Narrative spine**: [SB7 / Promised Land / Hero's Journey hook used in opening]

### Handoffs
- Stage: slide outline (one slide per pyramid node)
- Scribe: full memo authoring
- Magi: decision arbitration if multiple options
- Prose: tone polish for sentences
```

## Anti-Patterns Specific to Pyramid

| Anti-pattern | Fix |
|--------------|-----|
| Bottom-up writing (context → conclusion at end) | Lead with answer; everything else justifies it |
| Governing thought is a topic, not an answer | Rewrite as a complete sentence with verb and stance |
| Arguments overlap (not Mutually Exclusive) | Re-cluster; one item should belong to exactly one bucket |
| Missing categories (not Collectively Exhaustive) | Add the missing branch or explicitly scope it out |
| Mixed grouping patterns within one layer | Pick time OR structure OR degree, not all three |
| Inconsistent grammar across arguments | Use parallel verb/noun structures |
| Evidence layered above arguments | Push evidence to bottom; keep middle layer abstract |
| No SCQA — straight into pyramid | Without SCQA, reader doesn't know why this matters |
| Multiple governing thoughts | One pyramid = one answer; split into multiple pyramids if needed |
| Overlong governing thought (3+ sentences) | Compress to one declarative sentence |

## Deliverable Contract

When `pyramid` completes, emit:

- **SCQA opening** (4 components stated explicitly).
- **Governing Thought** as one declarative sentence.
- **3-5 MECE arguments** with parallel grammar.
- **Evidence** under each argument.
- **MECE check** (overlap / coverage / parallelism / grouping pattern).
- **Top-sentence-only test** result.
- **Anti-pattern check** (AP-1~AP-9 per `reference/anti-patterns.md` + Pyramid-specific table below).
- **Decision ask** (what / when / consequence).
- **Handoffs**: Stage, Scribe, Magi, Prose.

## References

- Barbara Minto — *The Pyramid Principle: Logic in Writing and Thinking* (canonical text)
- Barbara Minto — *The Minto Pyramid Principle* (1996, McKinsey roots)
- McKinsey & Company — internal communication training materials
- *The McKinsey Way* — Ethan Rasiel (popular adaptation)
- BCG / Bain — derivative consulting communication frameworks
- HBR — "How to Write a Memo" (Pyramid-aligned)
- *Pyramid Principle Made Simple* — Roy Lewis (workbook)
- Andy Raskin — "The Greatest Sales Deck I've Ever Seen" (pairs Promised Land with answer-first delivery)
