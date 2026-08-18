# Worked Examples

**Purpose:** Full end-to-end transformations to pattern-match against, including the deliverable's exact shape.
**Read when:** You are in `EMIT` and need the output format, or you want a reference transformation before starting one.

## Contents
- Deliverable shape
- Example 1 — persona + design adjectives
- Example 2 — conflicting instructions, KEEP, and an enforcing layer

---

## Deliverable Shape

Four sections, in this order. Section 3 is a code block. Sections with nothing to report are omitted rather than padded.

1. **Ambiguity Ledger** — original expression · class · competing readings · disposition. `KEEP` rows carry their reason here.
2. **Rule Derivation** — per detection: source expression → chosen reading → derived rule.
3. **Specified Prompt** — Purpose · Audience · Execution rules · Judgment criteria · Constraints · Output format · Quality checks.
4. **Unresolved Parameters** — only conditions that materially change the output.

Then the Exit Checklist result, plus any requirement routed to an enforcing layer.

---

## Example 1 — Persona + Design Adjectives

**Source:** "You are a world-class UX designer. Design a modern, simple admin screen that's easy even for beginners — make it look good."

### 1. Ambiguity Ledger

| Original | Class | Competing readings | Disposition |
|----------|-------|--------------------|-------------|
| world-class UX designer | Role | (a) authority framing (b) a specific set of evaluation axes | `DECOMPOSE` |
| easy even for beginners | Explanation level | (a) first-time user of *this* system (b) novice to admin tools in general | `AUDIENCE` |
| modern, simple | Design | (a) current visual trend (b) restraint and hierarchy | `BEHAVIORALIZE` |
| make it look good | Quality | Unscoped verdict — no standard named | `CRITERIA` |
| admin screen (scope) | Open — undeclared scope | (a) one screen (b) the whole admin surface | `PARAMETERIZE` |

### 2. Rule Derivation

**world-class UX designer** → reading: the title stands for UX evaluation axes, not authority → axes made explicit (user goal, cognitive load, information priority, operation count, consistency, feedback, error prevention, accessibility); the title itself is dropped.

**easy even for beginners** → reading: users who have never operated *this* system and received no prior explanation → assumed-reader block plus output rules.

**modern, simple** → reading: restraint and hierarchy, not a dated trend → eight visual rules.

**make it look good** → reading: the author will judge on the same UX axes already named → folded into the evaluation criteria rather than given separate rules (avoids duplication).

**Scope** → reading: undetermined by the source, and the deliverable differs greatly between one screen and a full surface → `{{SCOPE}}`.

### 3. Specified Prompt

```
Design the admin screen for {{SCOPE}}.

Assumed users
- Users operating this system for the first time.
- Users who received no prior explanation of how it works.

Design rules
- The most frequent operation is reachable in the fewest steps.
- The primary action is the most visually prominent element on the screen.
- One primary purpose per screen.
- Avoid domain jargon; where it is unavoidable, gloss it at first use.
- The same UI pattern for operations that mean the same thing.
- Prevent input errors before they occur rather than reporting them after.
- Give immediate feedback on the result of every operation.
- Express hierarchy through size, spacing, and position — never through color
  or decoration alone.
- No element whose only role is decoration.

Evaluation axes (in priority order)
1. Learning cost
2. Operation efficiency
3. Cognitive load
4. Error prevention
5. Consistency
6. Accessibility

Output format
- A screen composition proposal.
- For each major design decision, name which evaluation axis justifies it.
```

### 4. Unresolved Parameters

- `SCOPE` — one screen versus the full admin surface changes the deliverable's structure, not just its length.

**Exit Checklist:** 8/8 pass. Length delta: −1 line versus source once the persona sentence is removed and "make it look good" is folded into the existing axes.

---

## Example 2 — Conflicting Instructions, KEEP, and an Enforcing Layer

**Source:** "You're the best technical writer alive. Write a comprehensive but concise guide to our API. Cover everything, keep it under 300 words, use the latest endpoint list, and make sure the code samples are always valid JSON. Pick whatever section order works best."

### 1. Ambiguity Ledger

| Original | Class | Competing readings | Disposition |
|----------|-------|--------------------|-------------|
| the best technical writer alive | Role | Authority framing only | `DELETE` |
| comprehensive + concise + under 300 words | Quantity — **conflict** | (a) coverage wins (b) length wins | `RECONCILE` → order |
| cover everything | Quantity | (a) every endpoint (b) every concept a first user needs | `CRITERIA` |
| the latest endpoint list | Judgment (recency) | (a) recall (b) a named source at a stated date | `DATE` |
| code samples are always valid JSON | Technical | Cannot be guaranteed by wording | Routed — enforcing layer |
| whatever section order works best | Judgment | Author deliberately delegated it | `KEEP` |

### 2. Rule Derivation

**the best technical writer alive** → implied axes checked: none the rest of the prompt does not already state → deletes cleanly.

**comprehensive + concise + under 300 words** → the two cannot both hold; 300 words is the only numeric bound the source stated, so it wins → "300 words is a hard bound; coverage is best-effort within it, and what was omitted is named at the end." The dropped absolute reading of "comprehensive" is recorded here, not silently discarded.

**cover everything** → reading (b), since (a) is unachievable inside the bound → a criterion listing what a first-time reader must be able to do after reading.

**the latest endpoint list** → reference date, freshness method, and conflict rule; the endpoint source is user-held → `{{ENDPOINT_SOURCE}}`.

**always valid JSON** → no wording enforces this. Routed to a validator over the samples; the prompt states the requirement without an absolute guarantee.

**whatever section order works best** → `KEEP`. All three tests hold: the executor sees the endpoint list the author did not, the choice is reversible, and pinning an order would foreclose a better one.

### 3. Specified Prompt

```
Purpose
Write a guide to the API that lets a first-time reader make a successful
authenticated request and handle a failed one.

Audience
A developer who has not used this API before and is not assumed to know its
authentication model.

Execution rules
- Lead with the smallest working example.
- Explain each API-specific term at first use.
- Source the endpoint list from {{ENDPOINT_SOURCE}} as of {{AS_OF_DATE}};
  do not rely on recall for endpoint names or parameters.
- Where an older and a newer source disagree, prefer the newer and say so.
- Choose the section order that best serves the endpoint list you are given.

Judgment criteria
After reading, the reader can:
- make one authenticated request end to end
- identify which errors are retryable
- find the reference for anything not covered here

Constraints
- Hard bound: 300 words. Coverage is best-effort within it.
- Name what was omitted in a closing line.
- Code samples must be valid JSON. (Checked by a validator over the samples,
  not by this instruction alone.)

Output format
Prose with fenced code samples. Section order is left to the writer.

Quality checks
- No endpoint named that is absent from {{ENDPOINT_SOURCE}}.
- The omissions line is present.
- Word count is at or under 300.
```

### 4. Unresolved Parameters

- `ENDPOINT_SOURCE` — which artifact is authoritative; without it "latest" is unresolvable.
- `AS_OF_DATE` — defaults to the execution date; state it when the reader's decision depends on freshness.

**Routed to an enforcing layer:** JSON validity of code samples → a validator over the emitted samples. The prompt states the requirement; it does not claim to guarantee it.

**Deliberately left open:** section order — recorded as `KEEP` with the executor-has-better-information reason.

**Exit Checklist:** 8/8 pass.
