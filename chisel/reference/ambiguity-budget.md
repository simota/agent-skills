# Ambiguity Budget

**Purpose:** Deciding what to leave unspecified, proving each added line earns its place, and scoring the Exit Checklist.
**Read when:** You are in `CLASSIFY` deciding on a `KEEP`, in `RECONCILE` running the delete test, or the `audit` Recipe is active.

## Contents
- The premise
- The KEEP test
- Where ambiguity is load-bearing
- The delete test
- Requirements a prompt cannot hold
- Over-specification failure modes
- Exit Checklist scoring

---

## The Premise

"Eliminate every vague term" is not the goal, and pursued literally it produces a worse prompt. Specification has a cost: each fixed rule removes a decision the executor could have made better with the material in front of it, and each added line competes for attention with the lines that matter.

The goal is that **every ambiguity is either resolved or deliberate**. An unexplained vague term is a defect. So is a term specified when it should have been delegated. The ledger makes the difference visible.

---

## The KEEP Test

`KEEP` requires all three to hold. If any fails, translate it.

1. **The executor has better information than the author did.** The right choice depends on material the executor will see and the author could not anticipate.
2. **The choice is reversible.** A wrong pick costs a revision, not a wasted deliverable.
3. **A guess would narrow the space unhelpfully.** Fixing it early forecloses options that are the point of the task.

Every `KEEP` row records which of these applied. "Left vague" with no reason is indistinguishable from an oversight, and a later reader will remove it.

---

## Where Ambiguity Is Load-Bearing

| Situation | Why specifying hurts |
|-----------|---------------------|
| Exploration and ideation | Fixing the output shape makes the executor fill blanks instead of finding what matters. Formalize after the content settles, not before |
| Wording, naming, section order | Reversible surface choices the executor makes better in context; pinning them adds lines and removes nothing |
| Candidate generation | A stated count or format biases toward filling the quota rather than toward quality |
| Approach selection on an unsolved problem | Prescribing the method pre-commits to the author's guess about a solution they do not have |
| Process whose order carries no correctness | A fixed sequence with no safety, correctness, or auditability rationale is over-specified process (`architect/reference/agent-specification-anti-patterns.md` AS-09, Process Constraint Tiers) |

The inverse also holds: order **is** worth fixing when the sequence itself carries correctness, safety, or auditability — measure before optimizing, reproduce before fixing, snapshot before mutating.

---

## The Delete Test

Every line added to the rewritten prompt must pass: **remove it, and would the output plausibly differ?** If not, it does not ship.

Common failures:
- A rule restating what the model already does by default.
- A rule already implied by a stronger rule three lines above.
- A quality criterion no reader could check.
- A prohibition against a failure the task cannot produce.

This is the same admission rule the ecosystem applies to its own instructions (`_common/MECHANISM_SELECTION.md` § Admission). A specified prompt is frequently **shorter** than its source, because decorative role text and duplicated rules are removed. Net growth without a per-line justification means over-specification crept in.

---

## Requirements a Prompt Cannot Hold

Some detections should not be translated into stronger wording at all, because no wording enforces them. Name the enforcing layer instead and route it.

| Requirement | Prompt-only failure | Enforcing layer |
|-------------|---------------------|-----------------|
| Always valid structured output | Stray prose, missing key, wrong type | Schema validation plus retry |
| Never exceed a spend or usage cap | Misread, or overridden by injected text | Code-side check before the call |
| Never touch secrets or out-of-scope data | Complies in wording, reads anyway | Tool permission, secret isolation |
| Facts are current | Recall beyond the cutoff, missed retrieval | Retrieval plus source-date check |
| Irreversible action requires approval | Wording ignored under ambiguity | Approval gate outside the prompt |

Full classification — `MUST SPECIFY` / `SHOULD SPECIFY` / `CONDITIONAL` / `DELEGATE` / `DO NOT RELY ON PROMPT` — lives in `oracle/reference/prompt-engineering.md` § Instruction Boundary. Chisel consumes that classification; it does not restate it.

**Before rewriting at all**, confirm the prompt is the problem. When the complaint is a bad output, run the five-layer triage in the same file (Instruction / Context / Capability / Tool / Evaluation) — retrieval failures and evaluator failures are routinely misdiagnosed as prompt failures, and rewriting wording fixes neither.

---

## Over-Specification Failure Modes

| Mode | Symptom | Cost |
|------|---------|------|
| Premature formatting | A schema or section list fixed during an exploratory task | Discovery drops; the executor fills blanks |
| Process pinning | A step order stated where order carries no correctness | Blocks better paths for no safety gain |
| Criterion inflation | Twelve quality criteria for a two-paragraph answer | Attention spreads; none is enforced |
| Variable sprawl | Six or more `{{VARIABLE}}` placeholders | The prompt becomes a form and gets abandoned |
| Redundant restatement | The same rule in Execution rules and Quality checks | Signals the author does not trust the first statement; both get skimmed |

---

## Exit Checklist Scoring

Used by the `audit` Recipe and before every `EMIT`. Score each item pass or fail with the offending line cited.

| # | Item | Fails when |
|---|------|-----------|
| 1 | No vague-for-vague substitution | A translated rule contains a term from the lexicon with no bound, behavior, or criterion attached |
| 2 | Roles became capabilities | A bare title, seniority claim, or credential survives |
| 3 | Discretion words resolved | An "as appropriate" remains without either both branches or a recorded `KEEP` |
| 4 | Numbers are licensed | A figure appears that traces to neither source text, a labeled estimate, nor a variable |
| 5 | Conflicts handled | Two rules collide with no merge, no stated precedence, and no ledger entry |
| 6 | No duplication; delete test passed | A rule appears twice, or a line's removal would change nothing |
| 7 | Intent preserved | A goal, audience, or constraint appears that is not in the source, or one from the source is missing |
| 8 | Third-party checkable | A reader who never saw the original could not score the output pass or fail |

Any failure blocks delivery. For `audit`, return the failing items with the minimal patch for each — not a rewritten prompt, which is the `spec` Recipe's deliverable.
