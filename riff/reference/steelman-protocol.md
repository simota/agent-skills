# Steelman Protocol

Reference for Riff's `steelman` recipe. A disciplined dialogue mode for stress-testing high-stakes ideas by building the strongest possible case **for** the idea and the strongest possible case **against** it — in sequence, not in parallel — before any verdict.

Steelmanning is the inverse of strawmanning. A strawman caricatures the opposing view to defeat it cheaply; a steelman strengthens it until even its strongest version can be evaluated honestly. Riff applies this to both sides of an idea so the user converges on a decision that holds up after the conversation ends.

---

## 1. When to Apply

Use the `steelman` recipe when **at least one** of the following is true:

- The decision is hard to reverse (architecture choice, hire, public commitment, contract).
- The user has already mostly decided and wants validation — friction is the gift here.
- The team is split and needs honest both-sides articulation, not a tiebreaker.
- The cost of being wrong is asymmetric (downside ≫ upside, or vice versa).

Skip `steelman` when:

- The idea is exploratory and pre-decision (use `expand` instead).
- The user wants rapid divergence (use `crazy8`).
- The user wants a structured verdict (route to **Magi**).

---

## 2. The Five-Step Protocol

Steelman dialogues run in five strict phases. The order matters — converging too early collapses the protocol into a debate.

### Step 1: RECEIVE

- Restate the idea in one sentence.
- Confirm with the user before continuing. Do not proceed on a misread.
- Capture stakes: "what changes if this is right? what changes if this is wrong?"

### Step 2: STEELMAN FOR

- Build the strongest possible case **for** the idea.
- Use the *advocate* viewpoint — the most thoughtful person who would champion this.
- Cite mechanisms, not vibes ("works because X, Y, Z" — not "feels promising").
- Ask the user: "is there a stronger case for it I missed?"
- Do not allow counter-arguments yet. Suppress them until Step 3.

### Step 3: STEELMAN AGAINST

- Build the strongest possible case **against** the idea.
- Use the *thoughtful skeptic* viewpoint — not a contrarian, a person who has seen this fail.
- Cite specific failure modes, not generic risks ("X breaks when concurrency exceeds Y" — not "scaling is hard").
- Ask the user: "is there a stronger case against it I missed?"
- Do not let the user answer the criticism yet. Hold it.

### Step 4: SYNTHESIZE

- Surface where the cases collide (same fact viewed from both sides).
- Surface where the cases pass each other (different facts, different concerns).
- Identify the **decisive question** — the one fact that, if known, would resolve the disagreement.
- Identify what's testable, what's bet-on, and what's irreducible taste.

### Step 5: VERDICT (Soft)

- Riff does not decide. Riff hands back a structured choice surface:
  - "Here's what would have to be true for FOR to win."
  - "Here's what would have to be true for AGAINST to win."
  - "Here's the cheapest experiment to learn which one is true."
- Suggest **Magi** for a formal Go/No-Go if the user wants a verdict.

---

## 3. Steelman Quality Test

Before delivering each side, run this check internally:

| Side | Pass criteria |
|------|---------------|
| FOR | Would the most thoughtful proponent recognize this as their actual view, not a strawman? |
| AGAINST | Would the most thoughtful skeptic recognize this as their actual view, not paranoia? |
| Both | Would a third party reading the cases say "this is a fair fight"? |

If the test fails, rebuild the weak side before continuing.

---

## 4. Honest Friction Rules

Steelman protocol depends on Riff being willing to disagree.

- **Do not soften** the AGAINST case to spare feelings. The whole point is the friction.
- **Do not inflate** the FOR case to flatter the user's existing belief.
- **Do not hedge** the verdict with "either could work." The synthesis must surface the actual decisive question.
- If a fatal flaw exists (technical impossibility, ethical issue, known failure pattern), say so directly in Step 3 — not as caveat, as headline.

The user will respect honest friction more than polite agreement.

---

## 5. Dialogue Template

```
Riff (Step 1):
  Restating the idea: [one sentence].
  Stakes: if right → [outcome]. If wrong → [outcome].
  Did I capture it correctly?

User: [confirms / corrects]

Riff (Step 2 — STEELMAN FOR):
  The strongest case for this is:
  - Mechanism: [why it works, structurally]
  - Precedent: [where it has worked, with conditions that match]
  - Strategic fit: [why now, this team, this user]
  Is there a stronger case for it I missed?

User: [adds / refines]

Riff (Step 3 — STEELMAN AGAINST):
  The strongest case against this is:
  - Failure mode: [specific way it breaks, with conditions]
  - Hidden cost: [cost the FOR case minimizes]
  - Better alternative: [what a thoughtful skeptic would do instead]
  Is there a stronger case against it I missed?

User: [adds / refines]

Riff (Step 4 — SYNTHESIZE):
  These cases collide on: [shared fact, different read]
  These cases pass each other on: [different concerns]
  Decisive question: [the one thing that would resolve this]
  Testable / bet / taste: [classification]

Riff (Step 5 — SOFT VERDICT):
  For FOR to win, [X] must be true.
  For AGAINST to win, [Y] must be true.
  Cheapest experiment: [concrete, time-boxed]
  If you want a formal Go/No-Go, route to Magi.
```

---

## 6. Anti-Patterns

- **Lukewarm both-sides**: presenting tepid cases on both sides so neither lands. Make each side as sharp as possible.
- **Sandwich softening**: starting AGAINST with "of course there are good reasons too…". Each step is its own act.
- **Premature synthesis**: collapsing into "well, it depends" before the cases are built.
- **Hidden vote**: tilting the synthesis toward the side Riff secretly preferred. Stay neutral until Step 5.
- **Verdict creep**: telling the user what to do. Riff hands the user a sharper choice; the user decides.

---

## 7. Output Format (SYNTHESIZE Section)

Steelman session summaries should include:

```markdown
## Steelman Summary

### Idea
[One sentence]

### Stakes
- If right: [outcome]
- If wrong: [outcome]

### Strongest case FOR
- [bullet]
- [bullet]
- [bullet]

### Strongest case AGAINST
- [bullet]
- [bullet]
- [bullet]

### Decisive question
[The one fact that would resolve this]

### What it would take
- For FOR to win: [condition]
- For AGAINST to win: [condition]

### Cheapest experiment
[Concrete, time-boxed test]

### Suggested next
- Magi (formal Go/No-Go) if the user wants a decision
- Spark / Accord if FOR wins and needs spec
- Void / Subtract if AGAINST wins and the idea is being scoped out
```

---

## 8. Handoff Routing

| Outcome | Next agent | Why |
|---------|-----------|-----|
| User wants formal verdict | **Magi** | Multi-perspective deliberation produces a Go/No-Go |
| FOR wins, needs spec | **Spark** / **Accord** | Convert idea to feature seed or requirement |
| AGAINST wins, scope cut | **Void** | Systematic YAGNI / removal |
| Idea is on hold pending experiment | (None) | Schedule the test, return to Riff after results |
