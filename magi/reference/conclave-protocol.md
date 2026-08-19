# Conclave Protocol

**Purpose:** Channel a panel of 2-5 figures on one question and surface their genuine contrasts — without flattening disagreement into a fake consensus.
**Read when:** You are running the `advisor conclave` variant (multi-figure panel).

## Principle

A conclave's value is **divergence**, not agreement. If three figures would genuinely clash, the clash *is* the deliverable. Expert Mode never resolves the clash into a verdict; transition to Magi's decision workflow only when the user actually needs to decide.

## Protocol

1. **Select 2-5 figures** with meaningfully different mental models on the question. Pure agreement is a weak panel; aim for productive tension. Refuse/ask per the ethics gate for each figure individually.
2. **Channel each figure independently** (full GROUND → CHANNEL → ATTEST per `channeling-method.md`). Do **not** let one reading anchor the next — channel them blind to each other, then compare. (Same independence logic Magi uses for its lenses.)
3. **Build the contrast map** only after all readings exist:
   - Where do they **converge**? (shared conclusion, possibly different reasons)
   - Where do they **diverge**? Name the underlying values/trade-off driving the split.
   - What **question would settle it** between them?
4. **Preserve disagreement.** Never average two readings into a mushy middle. A 2-vs-1 split stays a split.
5. **Offer the transition.** If the user must choose, pass the panel into Magi's `decide` or `tradeoff` Recipe for arbitration, or back to the user. Expert Mode advises.

## Output shape

```
## Conclave — {Figure A}, {Figure B}, {Figure C} on {problem}

### {Figure A}  — {one-line stance}
{reading} · Attestation: A[n] I[n] S[n]

### {Figure B}  — {one-line stance}
{reading} · Attestation: A[n] I[n] S[n]

### {Figure C}  — {one-line stance}
{reading} · Attestation: A[n] I[n] S[n]

### Contrast map
- Converge on: …
- Diverge on: … (driven by: {value/trade-off})
- Would-settle-it question: …

**Disclaimer:** emulation of documented thinking, not the real persons' statements.
**Next:** decide → Magi `decide`/user · deepen one lens → `expert` · write-up → Scribe
```

## Anti-patterns

- **Forced consensus** — manufacturing agreement the figures would not share.
- **Sequential contamination** — channeling B in light of A's reading instead of independently.
- **Stacked panel** — picking 3 figures who all think alike, producing no real contrast.
- **Verdict creep** — declaring a winner. Surface the tension; switch explicitly to Magi's decision workflow or let the user decide.
