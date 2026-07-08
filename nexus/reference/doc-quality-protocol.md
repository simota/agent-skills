# Doc Quality Protocol — deliverable quality for document artifacts

**Purpose:** The shared discipline for maximizing quality when the deliverable is a **document** (or a document package) rather than code. Code has tests; documents have readers — so quality means: the declared reader can make the declared decision from the artifact alone, every externally-checkable fact is grounded, and the document set is internally coherent. Completes the protocol trio: `dialogue-protocol.md` (elicit intent), `autonomy-quality-protocol.md` (execute faithfully), this file (write artifacts worth trusting).

**Read when:** any run whose deliverable includes documents — `package` (all presets, incl. `venture`), `charter`, `layer`, `spec`/`delve` final artifacts, `gedanken` reports, `podium` content, and any chain step where Scribe/Accord/Quill/Tome/Morph authors a doc. Cites — never re-derives — `reference/package-recipe.md` (Universal Grounding Gate, traceability anchors), `reference/autonomy-quality-protocol.md` (Q10 evidence, Q11 artifact gate, Q15 provenance).

---

## 1. Reader Contract (W1–W3) — a document without a declared reader is a draft

| # | Rule | Discipline |
|---|------|-----------|
| W1 | **Audience + decision declared** | Before authoring, each document states: WHO reads it (role, expertise) · WHAT decision or action it supports · WHEN it is consumed (onboarding? incident? quarterly review?). This is the doc-side intent contract (Q1): a technically perfect document for the wrong reader is a miss. Multi-doc packages declare it per document, not per package. |
| W2 | **Register calibration** | Vocabulary, depth, and assumed context follow W1's reader — exec summary ≠ engineering spec ≠ legal clause. Mixed audiences get layered structure (W10), not averaged prose that serves no one. |
| W3 | **Freshness metadata** | Every document carries: `as-of` date for its facts · owner · the **review trigger** (what event or interval makes it stale — "on pricing change", "quarterly"). Documents rot silently; the trigger makes rot detectable. Time-insensitive docs state that instead (`evergreen`). |

## 2. Grounding (W4–W6) — plausible-but-fabricated is the doc failure mode

| # | Rule | Discipline |
|---|------|-----------|
| W4 | **Universal grounding, all doc runs** | Every **externally-checkable fact** (market sizes, statistics, competitor features, salary ranges, dates, "studies show") is `sourced` (citation/evidence) · `ASSUMPTION` (flagged inline) · or `research-to-do`. Fails on any ungrounded fact. This generalizes `package`'s Universal Grounding Gate to every doc-producing run — internal propositions (the user's own plan, opinions, recommendations) are exempt; the gate targets facts a reader could check and find false. |
| W5 | **UNKNOWN over fabrication** | A gap the run could not verify is written as `UNKNOWN` / `TBD(owner)` — never filled with a plausible guess. Specifics are where fabrication hides: numbers, product/model names, URLs, API signatures, legal citations are **verified or flagged, never improvised** (`charter`'s Phase 1 rule, generalized). |
| W6 | **Quote fidelity** | Anything presented as a quotation, spec excerpt, or reproduced requirement is verbatim-from-source, or explicitly marked as paraphrase. Silent paraphrase inside quotation marks is fabrication with extra steps. |

## 3. Structure & coherence (W7–W9) — a package is one artifact, not N files

| # | Rule | Discipline |
|---|------|-----------|
| W7 | **Template completeness** | A document authored against a template (spec template, Charter §-layout, preset blueprint) carries every required section — present, or `N/A` with a one-line reason. A silently missing section reads as "considered and empty" when it means "never considered". |
| W8 | **Single source of truth across docs** | In a multi-document set, every shared fact (a number, a date, a scope boundary, an entity name) has ONE owning document; others reference it rather than restating it. Restated facts fork silently on the first edit. Multi-doc packages use the preset's **traceability anchor** (`package-recipe.md`) as the spine for this ownership. |
| W9 | **Terminology ledger** | One concept, one term, package-wide. Synonym drift ("user"/"member"/"account" for the same entity) is a defect, not style. On existing repos, terms follow the codebase's established vocabulary — the doc adapts to the code, not vice versa. |

## 4. Readability (W10–W11) — the reader's time is the budget

| # | Rule | Discipline |
|---|------|-----------|
| W10 | **Summary-first, layered** | Every document opens with what the W1 reader needs in ~5 lines (the decision-relevant core), then layers detail progressively. Front-load conclusions; never make the reader excavate them. Tables for short enumerable facts; prose for reasoning; a diagram when structure beats words (Canvas). |
| W11 | **Scannability envelope** | One idea per section; headings state findings ("Auth tokens expire too early"), not topics ("Token analysis"); section length matched to the reader's stake in it. A document nobody finishes delivers nothing regardless of its accuracy. |

## 5. Doc Quality Gate (W12) — the Q11 specialization for documents

Before DELIVER, the document (or package) passes an adversarial artifact review — the doc-specific instantiation of `autonomy-quality-protocol.md` Q11:

| Dimension | Question |
|-----------|----------|
| Reader-path | Can the W1 reader make the W1 decision from this artifact **alone** (no author present to explain)? |
| Grounding | Zero ungrounded externally-checkable facts (W4–W6)? |
| Coherence | Shared facts single-sourced, terminology consistent, no cross-doc contradictions (W8–W9)? |
| Completeness | Every template section present or `N/A`+reason (W7)? |
| Readability | Summary-first, findings-headed, scannable (W10–W11)? |
| Freshness | as-of / owner / review-trigger present (W3)? |

Reviewer ≠ author (Q9). The Reader-path check is run **as the W1 reader** — Echo/Cast persona walkthrough when the audience is non-technical. Findings are fixed or explicitly downgraded into the document's own open-questions/risks section — never silently passed. Recipes with a stronger native gate (podium's Verification Team, spec's Spec Quality Gate, package Phase 5) **subsume** W12 — they add these dimensions where missing rather than running a second gate.

## Failure Modes Prevented

| Failure | Mitigation |
|---------|------------|
| Technically perfect doc for the wrong reader | W1 audience+decision contract, W2 register |
| Silent rot (facts age, nobody notices) | W3 as-of + review trigger |
| **Plausible-but-fabricated specifics** (numbers, names, citations) | W4 grounding gate + W5 UNKNOWN-over-fabrication + W6 quote fidelity |
| Missing section read as "considered and empty" | W7 present-or-N/A+reason |
| Shared facts forking across a package on first edit | W8 single source of truth via traceability anchor |
| Synonym drift confusing readers | W9 terminology ledger |
| Buried conclusions / doc nobody finishes | W10 summary-first + W11 scannability |
| Author-graded prose shipped as reviewed | W12 gate with reviewer ≠ author + reader-path walkthrough |

## Wiring

- **`package`** — the Universal Grounding Gate is W4's origin (floor for all presets); Phase 5 cross-doc consistency + traceability matrix implement W8; W1/W3/W12's reader-path check apply per document in Phase 3 tracks and the Phase 5 gate.
- **`charter` / `layer`** — the self-containment check IS the reader-path test (reader = `enact` / the executing team); W5 is charter Phase 1's UNKNOWN rule, generalized.
- **`spec` / `delve`** — their quality gates add the W dimensions they lack (W3 freshness, W10–W11 readability); grounding of external facts in EXPAND/EXCAVATE research follows W4.
- **`podium`** — Verification + Improvement teams subsume W12; W1/W2 feed Phase 0 framing.
- **Any chain step authoring a doc** (Scribe/Accord/Quill/Tome/Morph) — the spawn prompt carries the W1 reader contract and W4–W5 grounding duty in its output envelope; the hub runs W12 at VERIFY.

This protocol governs **document deliverables**; the run that produces them still follows `autonomy-quality-protocol.md` (Q1–Q15) end-to-end — W rules specialize, never replace, the Q rules.
