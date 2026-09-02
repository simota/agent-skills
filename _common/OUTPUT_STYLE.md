# Output Density Protocol — OUTPUT_STYLE.md

> **Tier:** `spine` — in effect on every run. Precedence: `_common/OPERATIONAL.md` § Contract Precedence.

> Single source of truth for **runtime output style** across all skills.
> Owner: Architect. Referenced from every SKILL.md `Output Contract` section.
> Distinct from `architect/reference/context-compression.md` (which targets SKILL.md file size, not response density).

Skills inherit these rules so each agent does not re-invent its own output style. Combine with the per-skill `Output Contract` section in SKILL.md.

**What binds where.** Tiers and § Tier-Specific Rules govern the response. § Sufficiency Floor, § Ambiguity Floor and § Cognitive Load govern *any* prose a skill authors — the response, and equally a deliverable written to a file, where a second reading survives longer and is re-read by more people.

---

## Why This Exists

Opus 5 calibrates verbosity to task complexity (`OPUS_5_AUTHORING.md` P2), but without a shared style baseline each skill drifts. Symptoms in the wild:

- Filler preamble before the actual answer ("Let me now…", "I'll proceed to…")
- Restating the user's request in different words
- Closing summaries that repeat what the diff already shows
- SKILL.md section headers mirrored back as response headers
- Prose where a 3-row table would carry more signal

This file defines **what to remove** and **what to choose instead**, with measurable criteria.

---

## Output Tiers

Every skill has a default tier — declared in its `## Output Contract`, or inherited as `M` when it has none (§ Inherited default). A skill MUST pick the smallest tier that fully answers the task.

| Tier | Lines | Use For | Example |
|------|-------|---------|---------|
| `S` | 1–3 | Lookup, status, yes/no, single-fact answer | "ファイルは `src/auth.ts:42` にあります。" |
| `M` | 5–15 | Typical task: plan, finding, short fix, single review | Bug RCA summary, quick refactor proposal |
| `L` | 30–80 | Deliverable, structured doc, multi-section finding | Design proposal, audit report |
| `XL` | 80+ | Full document: spec, design, comprehensive review | PRD, RFC, architecture doc |

### When in doubt, choose smaller

- Default to one tier below your first instinct.
- If the user can ask "more detail please" with one keystroke, the cost of starting smaller is near zero.
- Tier ceilings are advisory caps; the floor matters more — never pad to fill a tier.

### Inherited default

A skill with no `## Output Contract` section **inherits `M`**. There is no undeclared tier — an absent contract is a declaration of `M`, not a licence for unbounded output.

Declare an explicit contract only to state something the inherited default does not: a different default tier, per-task overrides, or domain bans. Skills whose deliverable is an inherently long structured document delivered *in the response* declare `L`; skills that write the deliverable to a file stay `M` and summarize (the document lives in the file, not in the reply).

---

## Banned Patterns

The response opens with the answer or the first action and closes with the § Fixed tail slots —
nothing before the answer, nothing after the tail (§ Cognitive Load "First line answers"). Uncertainty
is stated once, in one place. Two format defects remain worth naming:

### 1. Header echo

If the SKILL.md has sections `Analysis / Proposal / Risks`, do NOT auto-emit those three headers in every response. Headers are for L/XL tier only.

### 2. Same-meaning repetition

```
✗ "簡潔かつ明瞭に" / "fast and quick" / "robust and resilient"
✓ Pick one word.
```

---

## Conditional Requirements

A SKILL.md `## Output Requirements` list describes what a **complete deliverable** carries. It is a ceiling for the largest form of the task, not a floor every turn must reach.

- **Emit only the items the task actually exercised.** A refactor that touched no configs has no config row; a lookup that produced no fix has no fix section.
- **Never pad to satisfy the list.** `N/A`, "none identified", "not applicable in this case", and empty table shells are filler — deleting them loses no information (§ Banned Patterns applies).
- **Collapse empty envelope sections to one line, or drop them.** An empty ledger is `Residuals: none`, never a header plus a header-only table.
- **Required-in-substance ≠ required-in-shape.** When a protocol says a ledger is non-optional, that binds the *content* when content exists; the scaffolding is not the obligation.
- **Scale the envelope to the task, not to the schema.** A SIMPLE task reports in the schema's short form; the full form is for the work that filled it.

This rule is inherited by every skill. A SKILL.md may carry the one-line marker at the head of its `## Output Requirements` list — the point where the mandate is read — but must not reproduce the bullets above.

---

## Sufficiency Floor — the failure this protocol creates

Every rule above cuts. Cutting has its own failure mode, and it is the harder one to see: an
answer that is too short *looks* like a good short answer, while an answer that is too long
announces itself. Brevity is not the goal — **the goal is that nothing the reader needs is
missing and nothing else is present.**

Five things survive compression at every tier. Cutting one is a defect, not a style choice:

- **The direct answer to what was asked.** A related answer, a partial answer, or the answer to
  the question the response found easier is not it.
- **Anything the reader must decide.** A choice made silently on their behalf is the most
  expensive omission, because they cannot know it happened.
- **What was not verified.** Unexercised paths, assumptions, and skipped checks. A short answer
  that quietly drops its own caveats is worse than a long one that keeps them.
- **The number or fact that would change the conclusion** if the reader knew it.
- **Where to look.** The `path:line`, command, or identifier the reader needs to act or check.

**Never trade the floor for the tier.** When a task's honest answer exceeds its declared tier,
the tier gives way — it is a cap on padding, never a licence to omit. Say the whole thing.

---

## Ambiguity Floor — the other failure this protocol creates

§ Sufficiency Floor covers one failure of cutting: the reader needed something and it is gone. This
is the other, and the more expensive one: everything needed is present, and a sentence admits a
reading the writer did not mean. The reader does not stop — they act on the wrong reading and find
out later.

**A text is finished when no sentence has a second reading a fair reader could act on.** Not when
it is short. Compress against that bar, never through it. Like the sufficiency floor, it does not
yield to the tier.

### Precision vs. redundancy — the test that separates them

Both add words, so length cannot tell them apart. One question does: **does this word remove a
reading, or repeat one already excluded?**

- Removes a reading → precision. Keep it, though the sentence grew.
- Repeats an excluded reading → redundancy. Cut it, though it is short.

`50ms` earns its place over `fast`; `the caller validates` over `input is validated`; the sentence
restating what the previous one already fixed does not. Saying a rule twice in different words is
not reinforcement — it starts a search for the distinction between the two phrasings.

### Defects that leave a second reading

| # | Defect | Looks like | Fix |
|---|--------|-----------|-----|
| A1 | Unbound referent | `it` · `this` · `the above` · `likewise` with more than one candidate antecedent | Name the thing again — repeating a *name* is not redundancy |
| A2 | Unquantified qualifier | `appropriately` · `sufficient` · `large` · `soon` · `as needed` | A number, a threshold, or the name of who decides |
| A3 | Unowned action | `must be validated` · `is to be checked` | Subject and moment: who does it, at which point |
| A4 | Undeclared exception | `as a rule` · `generally` · `basically`, exception unnamed | Name the exception, or delete the hedge — one of the two is true |
| A5 | Two things, one name | one term covering two concepts (the inverse of § Cognitive Load's *one name per thing*) | Split the term; a distinction with no word of its own is not read |
| A6 | Unfalsifiable rule | a requirement whose violation nobody could point at | Write the observable failure. If there is none, it is a preference, not a rule |

The examples are English; the defects are not. Each has an equivalent in whatever language the output is written in (`OPERATIONAL.md` § Output Language), and the row is matched by the defect, not by the word.

### Intent is carried once

State the rule **and the failure it prevents** — the rule alone gets applied literally where it does
not fit. State that pair in one place. The same rationale echoed at three sites is the redundancy
this section otherwise bans, and the three copies drift (`HARNESS_DEBT.md` `HD-DRIFT`).

---

## Cognitive Load — the reader is a person, reading once

Density makes output *small*. It does not make it *cheap to read*. These rules target the second
cost, and they bind at every tier: a 3-line answer can still make its reader work twice.

- **First line answers.** Result, decision, or state change — before method, before context,
  before caveats. A reader who stops after one line should still have the answer, not the setup.
- **Forward-only.** No term used before it is defined, no "as explained below", no conclusion
  resting on a paragraph further down. Backtracking costs the reader more than the words saved.
- **One name per thing.** The same file, error, or concept keeps one label throughout. Synonym
  variation reads as a distinction and forces the reader to check whether one exists.
- **No arithmetic left to the reader.** Give the delta, not two numbers to subtract; the share
  *and* its base ("3 of 55"), not one of them. If a comparison matters, compute it.
- **The discriminator goes first.** In a list or table row, lead with the word that lets a reader
  skip it. Rows that must be read to the end to be dismissed are read in full, every one.
- **Uncertainty is a block, not a seasoning.** Hedges spread across sentences make every sentence
  need re-reading. State confidence once, in one place, and let the rest read as assertion.
- **Emphasis is a budget.** More than one bolded phrase per block spends it to zero.
- **Order by the reader's need, not by the work's sequence.** The order steps were performed is
  almost never the order they matter in. Rewrite the sequence into the priority.

**Structure serves scanning, not symmetry.** A table earns its shape when rows are compared; a
list when items are independent. Splitting content across files or sections to satisfy a size
number *raises* load — navigation costs more than a few extra visible rows (§ Density rules).

### Fixed tail slots

The last block of a response carries the same three things in the same order, every time:

```
changed:     what is different now
decide:      what needs the reader's judgment
unverified:  what was not exercised
```

Empty slots collapse to one word (`unverified: none`) and are never dropped — an absent slot and an
empty one look identical to a reader who has to search for it. Labels may be reworded to fit the
response's language and register; **the order is fixed**, because the value here is positional. A
reader learns one location once and stops scanning for it in every reply afterwards. Rotating the
position of "what's next" between responses spends that saving on nothing.

`S` tier omits the block — a 1–3 line answer *is* the tail. Envelope formats (`_STEP_COMPLETE`,
`NEXUS_HANDOFF`, `NEXUS_COMPLETE`) carry their own field order and are exempt.

### Name the one check worth running

Evidence-binding (`nexus/reference/autonomy-quality-protocol.md` Q10) requires claims to cite what
was observed. It does not rank them, so ten cited pieces of evidence present the reader with a
choice between auditing everything and auditing nothing — and nothing usually wins.

When a response makes a claim the reader may want to confirm, name **the single cheapest check that
would catch the most likely error**: one command, one `path:line`. Not the audit trail — the door
into it. Choose it by where this particular result would most plausibly be wrong, not by what is
easiest to quote.

---

## Format Priority

When data is structured, **don't prose it**. Order of preference:

```
table  >  bulleted list  >  numbered list  >  prose
```

| Data shape | Use |
|-----------|-----|
| Comparison across ≥3 attributes | Table |
| Sequence of steps | Numbered list |
| Independent items | Bulleted list |
| Single-thread reasoning | Prose (≤3 sentences) |
| Code, paths, commands | Code block / inline backticks |

### Density rules

- **1 bullet = 1 claim.** No ", and also" inside a bullet.
- **Paragraphs ≤ 3 sentences.** More → list.
- **Tables stay whole.** Split one only when rows stop being comparable, never to hit a row count — a reader scanning a visible table pays less than one who must open a second file. Past roughly 15 rows, add a sort order or group the rows rather than moving them.
- **No nested bullets past depth 2.** Flatten or section.
- **Inline code over fenced** for single tokens (`auth.ts` not a code block).

---

## Tier-Specific Rules

### S tier (1–3 lines)

- No headers, no lists, no closers.
- Lead with the answer; cite path:line if applicable.
- If a question has no answer, say so in one line.

### M tier (5–15 lines)

- At most one short header (often none).
- Use a 3–5 row table or bullet list when ≥3 distinct items.
- Close with the next action only if non-obvious.

### L tier (30–80 lines)

- 2–4 headers max.
- Mix dense (table) and sparse (1-line principle) blocks (Ma rhythm — see `architect/reference/context-compression.md` §Ma).
- Open with a 1-paragraph TL;DR before sections.

### XL tier (80+ lines)

- Apply Ma layout (Zone 1/2/3/4).
- Every section must justify its existence; if a section fits in 2 lines, fold it elsewhere.
- Provide a contents list at the top if >150 lines.

---

## Self-Audit Before Sending

Six-question check the model runs internally before emitting. The first three cut; the last three
are what cutting breaks, so they are asked **after**, on the cut version:

1. **Filler?** Is there a sentence that, if deleted, the user loses no information?
2. **Structure?** Is any 3+ line prose block actually a table or list in disguise?
3. **Tier?** Could one tier smaller still answer the question?
4. **Complete?** Are all five items of § Sufficiency Floor still present — the direct answer, every
   decision the reader must make, what went unverified, the fact that would change the conclusion,
   and where to look?
5. **One pass?** Does the first line answer, and can the rest be read straight through without
   backtracking to resolve a term, a reference, or a number?
6. **Two readings?** Read as an outsider who wants a different answer: does any sentence let them
   act on one — an unbound `it`, an unquantified `appropriately`, an ownerless obligation (§ Ambiguity
   Floor A1–A6)? Cutting is what creates these, which is why this is asked last.

Yes to 1–3 → cut. No to 4 or 5, or yes to 6 → restore, reorder, or constrain, even if it costs the
tier. A word that removes a reading is never cut to make a tier.

---

## Domain Overrides

Specific skills may add domain-banned phrases in their `Output Contract`. Examples:

- **Investigators (Scout/Lens/Trail):** never emit "I think" without evidence — say "evidence: …" or "unverified: …" instead.
- **Reviewers (Judge/Gauge/Sentinel):** never restate the file under review; reference by path:line.
- **Builders (Builder/Artisan/Forge):** never narrate code being written — let the diff speak.
- **Designers (Vision/Muse/Palette):** prefer parametric output (`_common/parametric-output.md`) over single-value declarations.

---

## Subagent Completion Pattern (universal ban)

Reports returned from the `Agent` tool (any `subagent_type`, including `general-purpose`) MUST NOT open with completion-announcement preamble. The fact that the subagent finished is **implicit** in the act of returning text — stating it adds zero signal.

**Banned openers (do not emit):**

```
✗ "All work is complete. Here's the summary report."
✗ "X が完了しました。最終レポートを返します。"
✗ "十分な調査が完了しました。350語以下で構造化されたレポートをまとめます。"
✗ "Successfully completed the task. Below is the summary."
✗ "全ての変更を適用しました。以下に結果をまとめます。"
```

**Open instead with the first deliverable line:**
- a `## ` section header that names the deliverable
- a table header
- the lead finding ("V4 のバックスラッシュエスケープは 0 件。`_common` リンクもクリーン。")
- a `_STEP_COMPLETE` / handoff envelope directly (no prose preamble before it)

**Why this matters:** Subagent reports are read in batch by an orchestrator (Architect, Nexus, the user). Completion preamble is filler that orchestrators ignore — but it costs tokens and pushes the actual deliverable below the attention fold.

This rule applies even when the skill's `Output Contract` does not explicitly mention it; subagent invocations inherit OUTPUT_STYLE universally.

---

## Interaction with Existing Protocols

| Protocol | Relationship |
|----------|-------------|
| `OPUS_5_AUTHORING.md` P2 | This file is the implementation. P2 says "calibrate length"; OUTPUT_STYLE says how. |
| `architect/reference/context-compression.md` | Different target: that file compresses SKILL.md; this file shapes runtime responses. |
| `_common/parametric-output.md` | Compatible. Parametric blocks are valid M/L tier content. |
| `_common/AUTORUN.md` | `_STEP_COMPLETE` and `NEXUS_HANDOFF` blocks are exempt from tier limits — they have their own envelopes. |

---

## How to Reference This File

In a SKILL.md `Output Contract` section:

```markdown
## Output Contract
- Default tier: M (5-15 lines per turn)
- Style: `_common/OUTPUT_STYLE.md`
- Task overrides:
  - `validate` → S
  - `generate-spec` → L
- Domain bans: <skill-specific banned phrases, if any>
```

Cite by tier and rule ID (e.g., "§ Fixed tail slots", "Banned Pattern §1"); don't duplicate the rule text inside individual SKILL.md files.

---

## Validation Hooks

Skills validating against ODP must pass:

- **R8.1** Output Contract section exists in SKILL.md, **or** the skill inherits the `M` default and needs no override (see § Inherited default). A contract that only restates `M` with no overrides and no domain bans is redundant and fails R8.1 for the opposite reason.
- **R8.2** Default tier declared (S/M/L/XL) when a contract is present.
- **R8.3** OUTPUT_STYLE.md is referenced (not duplicated) — including § Conditional Requirements.
- **R8.4** Task overrides table present when the skill has ≥2 distinct task types **and** they differ in tier.

See `architect/reference/validation-checklist.md` Section 8.

---

## Complexity Budget — § Ambiguity Floor

Per `_common/HARNESS_DEBT.md` §3b. Scoped to this section; the rest of the file predates the budget and acquires its fields when next edited for another reason.

| Field | Declaration |
|-------|-------------|
| `failure` | `F1 — wrong work`: a contract or deliverable is written densely, read the way it was not meant, and acted on. The corpus had a floor against cutting too much (§ Sufficiency Floor) and none against cutting into precision, so an unquantified `appropriately`, an unexplained `as a rule`, and an ownerless `must be validated` all read as compliant density. |
| `effect` | Turns the vaguest failures into six named defects with fixes (A1–A6), gives the cut/keep decision one test that word count cannot answer, and adds one self-audit question run after cutting. It does **not** catch prose that is unambiguous and wrong, and it has **no script**: A2 and A4 are lintable as word lists, A1/A3/A5/A6 are not, and a half-corpus linter would report the checkable third as the whole. Enforcement is the self-audit and review. |
| `owner` | `architect` — owns this file and the SKILL.md authoring rules that inherit it. `gauge` reads it as review criteria in compliance sweeps. |
| `removal` | Delete when either holds: (1) a lint lands that covers A1–A6, at which point this section becomes the checker's documentation and shrinks to the table; or (2) two consecutive `darwin` evaluation cycles find no defect in the corpus or in shipped deliverables attributable to A1–A6 — a floor nothing ever hits is describing a failure that does not occur here. Partial removal counts: a row that never fires across a cycle is dropped on its own. |
