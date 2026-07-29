# Coding Kata Reference

Purpose: Design deliberate-practice coding exercises in the kata tradition (Dave Thomas, "Code Kata," 2005). Katas are short, repeatable problems practiced under constraints to build technique — not to ship features. Repetition with reflection beats breadth.

## Scope Boundary

- **tome `kata` (this command)**: deliberate-practice exercise spec. Includes constraints, difficulty progression, comparison-target solutions, and facilitator notes.
- **tome `worked`**: shows the expert solution with reasoning. Kata withholds the solution; the learner produces it.
- **tome `learn` (default)**: explanation-oriented learning doc grounded in a real diff. Kata is practice-oriented and synthetic.
- **tome `onboard`**: comprehensive material for new joiners. Kata is narrower and skill-targeted.
- **tome `record`**: ADR. Kata teaches a technique; ADR records a decision.
- **vs Scribe (elsewhere)**: Scribe writes specs/PRDs. Kata is exercise material.
- **vs Quill (elsewhere)**: Quill produces inline code documentation. Kata is a standalone exercise document.
- **vs Stage (elsewhere)**: Stage builds slide presentations. Kata is for hands-on practice, not presentation.

## Workflow

```
SELECT       →  pick a problem small enough to attempt in 30-60 min
             →  confirm it isolates a single technique (parsing, recursion, modeling, etc.)

CONSTRAIN    →  design 1-3 constraints (time / language / paradigm / no-loops / TDD-only)
             →  constraints are the practice — without them it is just an exercise

PROGRESS     →  define 3 difficulty tiers (Bronze / Silver / Gold)
             →  each tier adds a constraint or removes a hint

COMPARE      →  prepare 2+ reference solutions (idiomatic, contrasting paradigm)
             →  shown ONLY after the learner submits an attempt

FACILITATE   →  write notes for solo, pair, and group runs
             →  include retrospective prompts and stuck-state hints
```

## Constraint Catalog

| Constraint | Mechanism | Trains |
|------------|-----------|--------|
| Time-box | 30 / 45 / 60 minutes hard stop | Decisive simplification |
| Language switch | Solve in unfamiliar language | Concept vs syntax separation |
| No-loops | Recursion / map-reduce only | Functional thinking |
| TDD-only | Red-green-refactor strict | Test-first discipline |
| No mouse | Keyboard-only navigation | Tooling fluency |
| No `if` | Polymorphism / table-driven | Branching alternatives |
| Pair-driver | Driver implements; navigator reads spec only | Communication |
| Mute pair | Pair writes only — no speech | Code-as-message clarity |

Pick constraints that pressure the technique you want to train. Stacking 3+ constraints usually breaks the kata; cap at 2 unless explicit.

## Tier Structure (Bronze / Silver / Gold)

| Tier | Constraint count | Hint level | Comparison target |
|------|------------------|------------|-------------------|
| Bronze | 0-1 | Step-by-step approach hint provided | One canonical solution shared after attempt |
| Silver | 1-2 | Approach-only hint | Two contrasting solutions shared after attempt |
| Gold | 2-3 | Problem statement only | Three+ solutions including expert anti-pattern note |

Gate progression on completion within time-box, not subjective satisfaction. Repeating the same tier with a fresh constraint is normal practice.

## Common Katas (Reference)

| Kata | Trains | Typical constraints |
|------|--------|---------------------|
| FizzBuzz | Branching / table-driven thinking | No `if`, table-driven |
| Roman Numerals | Lookup vs algorithm trade-offs | TDD-only, time-box |
| Bowling Game | State machine, sequence parsing | No mutable state |
| Gilded Rose | Refactoring under tests | Cannot rewrite from scratch |
| Tennis Game | Domain modeling, naming | No primitives in interface |
| Mars Rover | Command parser, state | Functional only |
| Bank OCR | Parsing, ambiguity handling | Streaming I/O only |
| Diamond | Symmetry, generative thinking | TDD with property tests |

Cite the source kata when adapting; do not present folklore as new.

## Platform Landscape (2026)

Match the platform to the practice goal, not vice versa. As of 2026-05:

| Platform | 2026 strength | Best for |
|----------|---------------|----------|
| **Exercism** | 82 language tracks with mentored feedback (free, volunteer mentors) | Language fluency, paradigm-shift katas, getting external feedback |
| **Codewars** | 67 language challenges, gamified; 2026 roadmap announced platform upgrades and AI partnerships | Daily repetition, ranking-driven practice, language switching |
| **LeetCode / HackerRank** | Interview-style problems | Interview prep — not deliberate-practice katas |
| **Frontend Mentor** | Frontend project briefs (HTML/CSS/JS/React) | UI kata, visual-design constraints |
| **Scrimba** | Practice-while-learning, integrated editor | Tutorial-driven warmup before kata work |

[Source: scrimba.com/articles — Best Coding Practice Platforms 2026; algocademy.com — 7 Best Coding Kata Sites]

**Trend signal:** consistency over intensity remains the dominant 2026 advice — daily short sessions outperform weekly marathons. Pair facilitation guidance with a platform that supports the constraint you want to train (e.g., Exercism's mentor channel for "code-as-message" katas where written explanation is part of the practice).

## Pair vs Solo vs Group

| Mode | Strength | Watch out for |
|------|----------|----------------|
| Solo | Honest self-confrontation, deep reflection | No external check on rationalization |
| Pair (driver/navigator) | Communication forced, double-loop learning | Dominant partner monopolizes keyboard |
| Mob (3-5) | Shared mental model, language exchange | Slow; energy drain past 90 min |
| Code-review kata | Reading skill, articulation of bad smells | Requires curated bad code; production code rarely fits |

## Facilitator Notes

- Time-box is non-negotiable. Stop on the buzzer regardless of completion. Reflection requires uncompleted attempts more than complete ones.
- Reflection prompts beat retrospective venting. Use: "What surprised you? What did the constraint force? What would change the second pass?"
- Reveal reference solutions only after attempts. Prematurely showing comparison targets converts a kata into a worked example.
- Encourage throwing the code away. Persistence-of-output is a feature anti-pattern; the technique is internalized in the hands and head.

## Anti-Patterns

- Kata without constraints — degenerates into a regular coding problem; deliberate-practice value drops to near zero.
- Constraint stacking 3+ at Bronze tier — overwhelming; learners attribute failure to the kata, not the technique.
- Skipping comparison-target solutions — learners cannot calibrate their solution against the technique being trained.
- Showing solutions before attempts — converts kata to worked example; recall-strengthening effect is lost.
- Reusing katas without rotation — same problem, same insight, no growth. Rotate techniques across sessions.
- Production code masquerading as kata — too large, too entangled with codebase context, no clean technique isolation.
- No facilitator notes — pair/group modes go off the rails without dominance and time-box guardrails.
- "Winner" framing in group katas — ranking individual solutions destroys the learning culture katas depend on.
- Treating completion as the goal — completion is incidental; the constraint-induced struggle is the practice.

## Handoff

- **To Scribe**: when a kata reveals a technique worth promoting to a team coding standard or spec rule.
- **To Quill**: when kata-discovered patterns deserve inline annotation in the codebase.
- **To Stage**: when running a kata-night talk — Stage handles pacing, slide-by-slide reveals, and speaker notes.
- **To Saga**: when a kata-derived insight should become a customer-story narrative.
- **To Tome `worked`**: pair this kata with a worked example of the canonical solution for learners who get stuck repeatedly.
