# Attestation Tiers

**Purpose:** The labeling discipline that keeps channeling honest — separating what a figure documentably thought from what we extrapolated.
**Read when:** You are in ATTEST, handling quotes/sources, or writing the disclaimer.

## Why this exists

The failure mode of a channeling agent is **confident fabrication**: a fluent, plausible reading that the figure never actually held, delivered as if attested. Tiers make the epistemic status of every claim explicit so the reader can trust the strong parts and discount the rest.

## The three tiers

| Tier | Definition | Evidence bar | Quote rule |
|------|------------|--------------|------------|
| `ATTESTED` | A framework, heuristic, or position the figure is documented to hold | Citable source (book, talk, interview, paper, well-attested record) | Paraphrase + cite. Verbatim quotes ONLY when the exact wording is sourced. |
| `INFERRED` | Extrapolation from the figure's known principles to a case they did not directly address | Logically follows from ≥1 ATTESTED principle | No quotes. Phrase: "by their documented principles, they would likely…" |
| `SPECULATIVE` | Reasoning-by-analogy where the record is thin — **deceased / historical figures only** | Weak or no direct grounding | Flag prominently. **Never apply to a living person or a contested topic** — decline instead (see `ethics-and-safety.md` gate step 3). |

## Tagging rules

- Tag **every substantive claim**, not just the reading as a whole. A reading is usually a mix.
- A reading that is **all SPECULATIVE** means you lack the record to channel this figure faithfully → say so and offer to research or decline (`ethics-and-safety.md`).
- ATTESTED positions are **date-scoped**: note when the figure held the view, and flag if the user's problem post-dates the documented record or the figure is known to have reversed. For a **living** figure, a post-record or contested case is a decline, not a tier (gate step 4).
- **Source-language flag**: note whether grounding is the figure's primary-language record or a translation/secondary source. For translated/secondary grounding, downgrade one tier (ATTESTED → INFERRED) and flag possible cultural / framing distortion.
- Promote SPECULATIVE → INFERRED → ATTESTED only when you actually have the grounding. Never inflate a tier to sound more authoritative.

## Quote handling (the hard rule)

- **Never invent a verbatim quote.** Not even a "representative" one. Not even clearly in-character.
- A verbatim quote requires a real, citable source. If you cannot cite it, paraphrase the idea and tag the *idea* ATTESTED, not the wording.
- "In the spirit of X" rewordings are INFERRED, never presented in quotation marks.

## Attestation map

Every deliverable carries a compact map:

```
Attestation: ATTESTED 4 · INFERRED 2 · SPECULATIVE 0
Sources (ATTESTED): [1] {work/talk, year} · [2] {…}
```

For conclave or critique outputs, show the map per figure.

## Emulation disclaimer (required, every deliverable)

Use this or a close paraphrase:

> **Emulation notice:** This is a reconstruction of how *{Figure}* might approach the problem, based on their documented thinking. It is not a statement, quote, endorsement, or current view of the real person. Decisions remain with you.

For living persons, append: *"It makes no claim about {Figure}'s private or present opinions."*
