# Role Decomposition

**Purpose:** Dissolving titles, personas, and seniority claims into the capabilities and evaluation axes they were standing in for.
**Read when:** A detection is classified `DECOMPOSE` or `DELETE`, or the `role` Recipe is active.

## Contents
- Why titles do not work
- The six-slot decomposition
- Standard decompositions
- Decorative theater
- What decomposition must not lose
- Failure modes

---

## Why Titles Do Not Work

A title asks the executor to infer a behavior from a label. The inference is unreliable in both directions: two readers derive different evaluation axes from "senior engineer", and a model given a title does not gain knowledge it lacked. What the title *does* carry — which properties get checked, which trade-offs get named, which mistakes get avoided — is exactly what can be written down instead.

This is the same rule the ecosystem applies to its own agent prompts: focus a spawn on the concrete task and output format, **never on personality adoption** (`nexus/SKILL.md` § Operational Notes for Spawns). Chisel applies it to prompts the user brings in.

Two additional constraints:
- **Never write credentials as fact.** "You are a licensed attorney", "you have 20 years of experience" — these assert something untrue about the executor and can mislead a reader about the output's standing.
- **Never keep a bare title after decomposition.** "As a professional, …" surviving the rewrite means the decomposition did not happen.

---

## The Six-Slot Decomposition

Every `DECOMPOSE` detection fills these slots. Empty slots are omitted, not padded.

| Slot | Question it answers |
|------|---------------------|
| **Domain** | What body of practice does the work draw on? |
| **Evaluation axes** | Which properties of the output get checked? |
| **Method** | What thinking procedure produces the answer? |
| **Judgment rules** | How are trade-offs decided when axes conflict? |
| **Responsibility** | What is the deliverable accountable for? |
| **Prohibited actions** | What does this role's failure mode look like? |

The evaluation-axes slot is the load-bearing one. A decomposition that fills only Domain has removed a title and added nothing.

Worked example:

```
"You are a world-class software engineer."
→
- Evaluate from the perspective of someone who has designed, built, and operated
  large systems.
- Check not only correctness but readability, maintainability, extensibility,
  fault tolerance, security, and performance.
- Consider system-wide impact rather than local optimization.
- Avoid unnecessary abstraction and over-engineering.
- Propose an alternative alongside every problem raised.
- State the trade-offs explicitly.
```

---

## Standard Decompositions

Reusable starting points. Trim to what the source prompt's task actually needs — importing all of a role's axes into a narrow task is over-specification.

### World-class expert

- Account for the field's main theories, established practice, and known failure patterns.
- Do not stop at introductory explanation; cover the exceptions that matter.
- Compare multiple options and give each one's advantages and disadvantages.
- Avoid assertions whose support is weak.
- The word "world-class" itself carries nothing and is dropped.

### Strategy consultant

Structure the problem first · separate ends from means · analyze the highest-weight issues first · state hypotheses explicitly · compare options · assess feasibility and impact · close with a recommendation.

### Senior software engineer

Correctness · readability · maintainability · testability · extensibility · performance · security · failure behavior · edge cases · operational cost. Solve with the minimum necessary complexity; avoid over-engineering.

### Product manager

User problem · business value · usage frequency · implementation cost · risk · priority · success metric · the MVP boundary. Judge by user value, not feature count.

### UX designer

User goal · cognitive load · information priority · number of operations · consistency · feedback · error prevention · accessibility. Do not evaluate on visual appeal alone.

### Researcher

Hypothesis · evidence · falsifiability · correlation vs causation · data quality · sample bias · alternative explanations · uncertainty. Keep fact, hypothesis, and speculation distinguished.

### Critical reviewer

False premises · logical leaps · contradictions · unconsidered cases · bias · risk · counterexamples. Do not stop at criticism — give the remedy.

### Teacher

Assume the learner's prior knowledge explicitly · order from foundation to application · connect new concepts to known ones · use concrete examples · name the common misunderstandings · surface the points that confirm understanding.

### Copywriter

Name the reader · write from the reader's problem and desire · make the benefit concrete · do not lean on abstract adjectives · prefer expressions understood on first read · place a clear call to action where one is warranted.

---

## Decorative Theater

`DELETE` fires on lines whose removal changes nothing about the deliverable.

| Pattern | Disposition |
|---------|-------------|
| "You are a genius", "IQ 200", "the world's best", "the greatest expert in history" | `DELETE` — no derivable behavior |
| "You never make mistakes", "you are always right" | `DELETE` — additionally suppresses the uncertainty signals the reader needs |
| "Take a deep breath", "think step by step" as a magic incantation | `DELETE` — on current models, reasoning depth is a parameter, not a phrase |
| "You are a licensed X", "you have N years of experience" | `DELETE` — a false claim about the executor |

Before deleting, check whether the line implied evaluation axes. "The world's best security engineer" implies a threat-model-first check; delete the title and write the check.

---

## What Decomposition Must Not Lose

Deleting a persona is safe. Deleting what the reader inferred from it is a behavior change disguised as a cleanup.

Before removing any role line, ask: **which properties of the output would a reader have expected to be checked because of this line?** Those become explicit rules. If the honest answer is "none", the line was theater and deletes cleanly.

---

## Failure Modes

| Failure | Looks like | Fix |
|---------|-----------|-----|
| Retitling | "world-class engineer" → "highly skilled engineer" | The output must be capabilities, not a better adjective |
| Silent narrowing | Title deleted, axes never re-expressed | Recover the implied axes first |
| Axis import | A tone-focused prompt receives all ten senior-engineer axes | Trim to the axes the task actually exercises |
| Credential assertion | "You are a certified auditor" preserved for authority | Never — assert capability, never credentials |
| Slot padding | Every slot filled for a one-line task | Empty slots are omitted |
