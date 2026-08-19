# Channeling Method

**Purpose:** How to build a faithful thinking-model of a named figure and apply it to a problem without sliding into caricature or fabrication.
**Read when:** You are in CHANNEL (`advisor expert` or `advisor critique`).

## The core idea

Channeling is **applying a documented reasoning system**, not impersonating a voice. You are answering: *"Given how this figure is known to think, how would they likely approach this problem — and where would they hesitate or disagree with themselves?"* The output is a reading, not the person speaking.

## Build the thinking-model (GROUND)

Extract, from the figure's documented record (roster profile or fresh research), these layers. Source each; mark gaps `[inferred]`.

| Layer | What to capture | Example (illustrative) |
|-------|-----------------|------------------------|
| **Mental models** | The frameworks they reason *with* | Munger's "latticework of models"; Christensen's jobs-to-be-done |
| **Heuristics** | Quick rules they apply | Bezos: "disagree and commit"; Buffett: "circle of competence" |
| **Characteristic questions** | What they ask first | Feynman: "Can I derive it from first principles?" |
| **Values / priorities** | What they optimize for | Jobs: experience > spec sheet |
| **Trade-offs they accept** | What they knowingly sacrifice | Speed vs. correctness, focus vs. coverage |
| **Blind spots / known errors** | Where they were wrong or criticized | Document these — they prevent hagiography |
| **Vocabulary** | Terms-of-art they use (paraphrase, don't fake quotes) | — |

A model missing the bottom two rows (trade-offs, blind spots) will produce a flattering caricature. Channel the whole person, including their limits.

## Apply the model (CHANNEL)

1. **Re-state the problem in the figure's terms.** What would *they* call this? Which of their frameworks fires first?
2. **Reason forward by their heuristics**, step by step. Show the moves, not just the conclusion.
3. **Surface the trade-off they would accept** and what they would deprioritize.
4. **Name where they would be uncertain** or where this problem sits outside their documented range (→ INFERRED or SPECULATIVE). **For a living figure, a case that post-dates or contests their record is a decline, not an INFERRED extrapolation** (`ethics-and-safety.md` gate step 4) — extrapolating a current view onto a living person fabricates it.
5. **Stop before the verdict.** Expert Mode advises; an actual verdict requires a separate transition into Magi's decision workflow or remains with the user.

## Anti-caricature checklist

Before delivering, confirm:
- [ ] The reading includes at least one trade-off the figure would *accept* (not just what they'd praise).
- [ ] It names a blind spot, uncertainty, or boundary of their competence.
- [ ] No claim rests on a famous catchphrase doing all the work.
- [ ] No verbatim quote appears unless it is sourced (ATTESTED).
- [ ] Grounding is the figure's **primary-language** record, or translated/secondary status is flagged and reliability downgraded one tier (guard against mistranslation and Western-framing distortion of non-English figures).
- [ ] If the roster profile is `record_strength: thin` or `last_reviewed` is stale, that weakness is surfaced in the attestation — a stale or thin record is never silent authority.
- [ ] A skeptic who admires the figure would recognize the reasoning as fair.

## Critique recipe specifics

When a figure critiques the user's plan/draft/decision:
- Critique by the figure's **documented standards**, not generic best practice. ("By Dieter Rams's ten principles…" not "this could be cleaner.")
- Lead with the standard, then the gap, then what the figure would likely change.
- For a **living** figure, **unconditionally** attach the reputational caveat (`ethics-and-safety.md`) and an inline note that this is a *design critique by X's documented standards, not a verdict on the person* — output is forwardable anywhere, so never gate the caveat on publication intent.
- Frame as *"by X's known principles, this would…"* — never *"X says this is bad."*

## Output shape (single channel)

```
## Channeled reading — {Figure} on {problem}
**Frame:** how the figure restates the problem.
**Reasoning:** 2-5 steps in their documented style.
**Trade-off accepted:** what they optimize, what they drop.
**Where they'd hesitate:** uncertainty / boundary of competence.
**Attestation:** ATTESTED [n] · INFERRED [n] · SPECULATIVE [n]  (sources for ATTESTED)
**Disclaimer:** {emulation disclaimer}
**Next:** decision → Magi `decide`/user · more lenses → `advisor conclave` · write-up → Scribe
```
