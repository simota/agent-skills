# Calibration Techniques

**Purpose:** Methods to improve scoring accuracy and detect biases.
**Read when:** Executing CALIBRATE phase.

---

## Pairwise Comparison

Compare items in pairs rather than scoring independently.

**Procedure:**
1. For each pair (A, B), ask: "If we could only do one, which has more impact?"
2. Record wins for each item
3. Calculate win rate: `wins / total comparisons`
4. Use win rate to validate and adjust absolute scores

**When to apply:** Always in FULL mode. Skip in QUICK mode.
**Benefit:** Reduces anchoring bias — relative judgment is more reliable than absolute.

**Efficiency:** For N items, full comparison = N(N-1)/2 pairs. For N > 10, use Swiss-tournament style (log₂N rounds).

---

## Anchor Calibration

Prevent first-scored items from anchoring subsequent scores.

**Procedure:**
1. Score a well-understood "reference item" first (team agrees on its score)
2. Score all other items relative to the reference
3. Re-score the first 3 items last (they were most affected by anchoring)
4. Compare initial vs final scores for drift detection

---

## Bias Detection Checklist

| Bias | Signal | Correction |
|------|--------|------------|
| **HIPPO** (Highest Paid Person's Opinion) | One stakeholder's items consistently top-ranked | Anonymous scoring first, then reveal |
| **Recency** | Recently discussed items score higher | Randomize presentation order |
| **Sunk Cost** | "We already invested X" inflates priority | Score only future value, not past investment |
| **Confirmation** | Items supporting current strategy always win | Include devil's advocate scorer |
| **Groupthink** | No dissent in team scoring | Independent scoring before group discussion |
| **Availability** | Items related to recent incidents score high | Use base rates, not recent events |
| **IKEA Effect** | Self-built features rated higher | External benchmarking |
| **AI-anchor bias** (2026) | Team adopts the LLM-suggested score with no debate | Score independently *first*, reveal the AI proposal after, then reconcile — the AI proposal must lose at least one round to prove the group is not rubber-stamping it |
| **"AI will figure it out"** (2026) | Impact argument depends on an undelivered model behavior | Cap `Confidence` at `≤ 50%` until validated; track separately as research, not feature work |

---

## Sensitivity Analysis

Test how robust the ranking is to score changes.

**Procedure:**
1. Identify the top-ranked item and the 2nd-ranked item
2. For each scoring dimension, calculate: "How much would this score need to change to flip the ranking?"
3. If a small change (±1 on a 10-point scale) flips the ranking, flag as **low confidence**
4. Report sensitivity per ranking position

**Output format:**
```
Item A (Rank 1, Score 82): Stable — needs ≥3 point change to lose rank
Item B (Rank 2, Score 79): Sensitive — 1 point change in Impact flips to Rank 1
```

---

## Re-ranking Triggers

When to re-run prioritization:
- New information changes Impact or Effort estimates by ≥ 20%
- External event changes market/competitive landscape
- Sprint velocity data invalidates Effort estimates
- User feedback contradicts assumed Impact
- Quarterly review (minimum cadence)

---

## Cross-Framework Correlation

When using multiple frameworks in FULL mode:

1. Calculate Spearman rank correlation (ρ) between framework rankings
2. Interpret:
   - ρ > 0.8: Strong agreement → high confidence in ranking
   - ρ 0.5-0.8: Moderate agreement → investigate divergences
   - ρ < 0.5: Weak agreement → frameworks measuring different things, escalate to Magi

3. For divergent items, document which framework's perspective matters more for this context
