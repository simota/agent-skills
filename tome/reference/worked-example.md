# Worked Example Reference

Purpose: Author step-by-step problem-and-solution documents that make expert reasoning visible. Based on Sweller's Cognitive Load Theory (1988) — worked examples reduce extraneous load by replacing means-ends search with studied solutions. Includes faded-guidance progression so learners transition from studying to solving.

## Scope Boundary

- **tome `worked` (this command)**: cognitive-scaffolded problem→reasoning→solution document. Annotates expert thinking and common mistakes; supports faded-guidance sequences.
- **tome `learn` (default)**: standard 5W1H+WhyNot learning doc derived from a real diff. Worked examples may be hypothetical or canonical.
- **tome `diff`**: turns a specific diff into teaching material. Worked example is method-agnostic to source.
- **tome `onboard`**: beginner-depth comprehensive intro. Worked examples are narrower — one problem, one expert mind.
- **tome `record`**: ADR/decision record. Worked example teaches problem-solving steps, not architectural commitments.
- **vs Scribe (elsewhere)**: Scribe authors specs/PRDs/HLDs — formal documents. Worked example is pedagogical.
- **vs Quill (elsewhere)**: Quill writes inline JSDoc/TSDoc. Worked example is a standalone study document.
- **vs Stage (elsewhere)**: Stage produces slide decks for presentation. Worked example is for solo study.

## Workflow

```
SELECT     →  pick a problem with one canonical expert solution
           →  confirm worth scaffolding (high-stakes, frequently confused, foundational)

DECOMPOSE  →  break solution into 4-9 numbered steps
           →  each step is one cognitive operation, not one keystroke

ANNOTATE   →  for each step add (a) expert reasoning, (b) common mistake, (c) why-this-works
           →  reasoning answers "what is the expert noticing here?"

SCAFFOLD   →  if a sequence: design fading guidance (full → partial → solo)
           →  faded variants share scaffolding template, drop annotations stepwise

VALIDATE   →  read as a novice — does each step land before the next demands it?
           →  hand off to Scribe if rule-set extraction or to Quill if inline-doc embedding
```

## Structure Table

| Section | Purpose | Required |
|---------|---------|----------|
| Problem statement | Concrete, bounded, one-paragraph | Yes |
| Prerequisites | Vocabulary, prior steps, assumed familiarity | Yes |
| Expert quick-take | 2-3 sentences: how an expert frames this | Yes |
| Step-by-step solution | Numbered ops with reasoning column | Yes |
| Common mistakes | Annotated near the step where each typically occurs | Yes |
| Why this works | Sidebar explaining the underlying principle | Yes |
| Variations | Edge cases / alt-approach pointers | Optional |
| Faded next | Pointer to the next, less-scaffolded variant | Optional (sequences only) |

## Faded-Guidance Progression

| Stage | Worked steps | Reasoning shown | Common-mistake annotations | Learner does |
|-------|--------------|-----------------|----------------------------|--------------|
| Full worked | All | All | All | Read and recreate |
| Partial-1 | First half | First half | First half | Complete remainder |
| Partial-2 | First step only | First step only | None | Drive remainder |
| Solo problem | Statement only | None | None | Solve from scratch |

Span the four stages across 3-5 problems of equivalent type. Drop one scaffold per stage; do not skip stages.

## Annotation Conventions

| Annotation | Marker | Purpose |
|------------|--------|---------|
| Expert reasoning | `# Expert: ...` | What the expert is noticing or recalling |
| Common mistake | `# Trap: ...` | A frequent novice error and why it fails |
| Why this works | `# Principle: ...` | Underlying rule or invariant |
| Inference | `[Inference: evidence]` | Anything not directly verifiable |

Keep annotations adjacent to the step they describe. Do not collect them at the end — co-location is the entire pedagogical lever.

## Anti-Patterns

- Solution dump without reasoning column — strips the worked example of its teaching value, leaves only an answer key.
- Steps that bundle multiple cognitive operations — overloads working memory exactly where the example was meant to relieve it.
- Common mistakes listed in a footer, not co-located — readers pattern-match the trap only after they have already fallen in.
- Faded sequence that skips the partial-guidance stages — jumping from full-worked to solo recreates the cognitive load wall.
- Toy problems with no transfer — examples must reflect realistic structure, not "Hello World" stand-ins, or learners cannot generalize.
- Missing prerequisites — assuming vocabulary the audience does not have makes expert reasoning unparseable.
- Expert reasoning written as motivational commentary ("just trust the process") — must be falsifiable, mechanism-level explanations.
- One worked example for a multi-method topic — single examples teach a single path; learners overfit. Pair at least two contrasting examples.
- Final reveal hiding the answer — worked examples are not puzzles; visible solutions are the point.

## Handoff

- **To Scribe**: when expert reasoning patterns generalize into a rule set worth promoting to spec or guideline.
- **To Quill**: when a worked-example annotation should travel into the codebase as inline JSDoc or comment near the actual implementation.
- **To Stage**: when the worked example will be presented live — Stage adapts pacing, splits steps across slides, and adds speaker notes.
- **To Saga**: when the problem is best framed as a customer story before becoming a worked example.
- **To Tome `kata`**: when the worked example should graduate into a deliberate-practice exercise (remove solution, keep constraints).
