# Translation Patterns

**Purpose:** How to turn a detection into a rule, per disposition, with worked patterns for the cases that recur.
**Read when:** You are in `TRANSLATE` and need the shape of the rule a given disposition produces.

## Contents
- The three shapes
- QUANTIFY
- BEHAVIORALIZE
- CRITERIA
- AUDIENCE
- CONDITION
- DATE
- PARAMETERIZE
- Design language
- Conflict reconciliation
- Failure modes

---

## The Three Shapes

Every translated rule takes one of three shapes. If a candidate rule fits none of them, it is still vague.

| Shape | Checkable by | Example |
|-------|--------------|---------|
| **Bound** | Counting or measuring | "at most 5 bullet points" |
| **Behavior** | Reading the output and observing presence or absence | "define each term at first use" |
| **Criterion** | Scoring against a list without asking the author | "states which claims are inferred rather than sourced" |

---

## QUANTIFY

Fires when the term maps to a countable dimension **and** the source licenses a bound.

```
"concise"
→ lead with the conclusion
→ body of at most 500 characters as a target
→ at most 5 key points
→ do not restate the same content in different words
```

Rules:
- Label estimates as targets ("as a target", "aim for") and reserve absolute phrasing for bounds the source actually stated.
- Prefer a range to a point value when the source gave neither — a range is honest about the uncertainty a point value hides.
- Attach the counting unit explicitly (characters vs words vs paragraphs differ by an order of magnitude across languages).

Do not quantify when the number is a proxy for something else. "Short" usually means "no padding", which is `BEHAVIORALIZE`; a character limit that permits dense padding has not solved the author's problem.

---

## BEHAVIORALIZE

Fires when the term is not measurable but is visible in the output's shape.

```
"easy to understand"
→ explain each technical term at first use
→ one claim per sentence
→ attach at least one concrete example to every abstract concept
→ state required prior knowledge explicitly when the explanation assumes it
→ order as conclusion → reason → example
```

Rules:
- Each line must be independently observable. "Write in a friendly way" is not; "address the reader directly in the second person" is.
- Prefer positive instructions; add a prohibition only where the default behavior is the failure ("do not open with a restatement of the question").
- Three to six lines is usually sufficient. Beyond that, the added lines stop constraining and start describing.

---

## CRITERIA

Fires on evaluation words. The output is a checklist the author could hand to a third party.

```
"a high-quality answer"
→ the answer must:
   - address the question asked, not an adjacent one
   - state the assumptions it depends on
   - distinguish fact from inference
   - contain no repeated content
   - be actionable — the reader can act without a follow-up question
   - contain no internal contradiction
```

Rules:
- Write criteria as pass/fail statements, not as scored dimensions, unless the source asked for a score.
- Do not add quality dimensions the author never implied. "High-quality" in a source about factual accuracy does not license criteria about tone.
- If a criterion cannot be checked without asking the author what they meant, it has not been translated.

---

## AUDIENCE

Fires on abstract reader classes. Produces two blocks — the reader model, then the rules that follow from it.

```
"for beginners"
→ assumed reader:
   - has not studied this topic systematically
   - knows few of its technical terms
   - needs base concepts explained before anything is built on them
→ resulting output rules:
   - explain each technical term at first use
   - assume no prior knowledge
   - use concrete examples
   - keep advanced exceptions out of the main line of the explanation
```

The reader model is the part that makes the rules checkable later; emitting only the rules loses the reason they exist and invites arbitrary edits.

---

## CONDITION

Fires on discretion wording. **The else-branch is mandatory** — an if without an else re-delegates the same decision.

```
"add examples as needed"
→ add an example when:
   - the abstract statement alone is hard to act on
   - more than one reading of the statement exists
   - actual usage is the point being made
→ otherwise, do not add an example.
```

Rules:
- The trigger must be observable from the material at hand, not from the author's intent.
- Two or three triggers is the working range; a list of eight is a rewritten "as appropriate".
- When no honest trigger exists, this is a `PARAMETERIZE` or a `KEEP`, not a fabricated condition.

---

## DATE

Fires on recency wording. Produces three parts; omitting any one leaves the instruction broken in a different way.

```
"use the latest information"
→ reference date: {{AS_OF_DATE}} (default: the date of execution)
→ freshness check: for facts that change, confirm against a source rather than recall
→ conflict rule: when an older and a newer source disagree, prefer the newer and say so
→ label the reference date in the output when the reader's decision depends on it
```

A fixed date with no freshness method converts a vague instruction into a confidently stale one — the specific failure this pattern exists to prevent.

---

## PARAMETERIZE

Fires when only the user holds the value **and** it materially changes the output.

```
"a short article"
→ Maximum length: {{MAX_LENGTH}}
→ Unresolved Parameters: MAX_LENGTH — the structure differs between 800 and 5,000 characters
```

Rules:
- Keep the variable set small. Six or more variables means the prompt has become a form, and the author will abandon it.
- Only parameterize what changes the output's *shape*. Preferences that change wording alone belong in `BEHAVIORALIZE` or `KEEP`.
- Every variable gets an Unresolved Parameters row explaining what changes with it — a bare `{{X}}` moves the ambiguity rather than resolving it.

---

## Design Language

Design adjectives translate to visual rules about hierarchy, restraint, and consistency — never to a brand name.

```
"a modern, simple UI"
→ one primary purpose per screen
→ the primary action is the most visually prominent element
→ minimum necessary number of colors
→ generous whitespace between groups
→ the same UI pattern for the same meaning throughout
→ no element whose only role is decoration
→ express hierarchy through size, spacing, and position
→ no heavy use of shadows, gradients, or rules
```

Named-brand comparisons resolve to properties, not imitation. "Apple-like" → restraint in color count, large type scale contrast, generous spacing, one primary action per view.

---

## Conflict Reconciliation

Runs in `RECONCILE`. Three outcomes, in order of preference.

| Outcome | Use when | Example |
|---------|----------|---------|
| **Merge** | Both instructions can hold in different parts of the output | "concise" + "very detailed" → "keep the conclusion concise; supply the detail below it" |
| **Order** | They genuinely collide and one must win | "cover everything" + "under 300 characters" → "300 characters is the hard bound; coverage is best-effort within it, and what was omitted is named" |
| **Escalate** | Neither merging nor ordering is defensible without the author's decision | Ask, or hand to `Magi` when it is a product trade-off |

Never resolve a conflict by silently dropping the instruction that was harder to satisfy. A dropped constraint must appear in the ledger as a dropped constraint.

---

## Failure Modes

| Failure | Looks like | Fix |
|---------|-----------|-----|
| Vague-for-vague | "clear" → "easy to read" | Apply one of the three shapes; if none fits, it is not translated |
| Fabricated precision | "short" → "exactly 237 characters" | Run the Numeric Licensing Cascade |
| Scope creep | Adding accessibility criteria to a prompt about tone | Every rule traces to a detection or to source text |
| Rule duplication | The same constraint in Execution rules and Quality checks | Deduplicate in `RECONCILE`; state each rule once |
| Condition without an else | "add an example when it helps" | The else-branch is mandatory |
| Over-specification | Pinning section order on an exploratory task | Check the ambiguity budget before translating |
