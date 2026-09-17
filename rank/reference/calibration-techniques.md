# Calibration and Ranking Delivery

Load at CALIBRATE; keep the SKILL's framework selection, bias reporting and escalation gates. FULL uses pairwise comparison and sensitivity analysis; QUICK does not require an exhaustive pairwise matrix.

## Calibration Algorithm

1. Establish a team-agreed reference item, score other items relative to it, then re-score the first three last; report drift.
2. FULL: compare pairs by the selected dimension and compute `wins / comparisons`. Full round-robin has `N(N−1)/2` pairs; for N>10 use approximately `ceil(log2(N))` Swiss-style rounds and report incomplete coverage rather than claiming exhaustive comparisons.
3. For adjacent ranked items, vary each dimension to find the smallest change that reverses their order. A ±1 change on a ten-point scale makes that position low-confidence; report the dimension and flip point, not a fictional sample score.
4. Compute Spearman ρ across frameworks with a consistent tie policy. Interpretation: >0.8 strong; 0.5–0.8 moderate; <0.5 weak and escalate to Magi. The SKILL separately requires stakeholder input below 0.7; do not silently average disagreeing frameworks. Record which value lens governs each divergence.

## Bias Interventions

| Signal | Action |
|---|---|
| Leader's proposals dominate | Anonymous independent scoring before reveal |
| Recent discussion/incident dominates | Randomize order and compare base rates |
| Prior investment inflates value | Score future value, not sunk cost |
| Strategy/self-built proposals always win | Consider opposing evidence and external alternatives |
| No dissent | Obtain independent judgments before group discussion; do not invent dissent to satisfy a quota |
| LLM proposal adopted unexamined | Score independently before revealing it; retain evidence-based agreement or disagreement, never require the LLM to “lose a round” |
| Benefit depends on unvalidated model behavior | Cap Confidence at ≤50% and classify as research pending validation |

Re-rank when new evidence changes Impact/Effort by ≥20%, market context changes, velocity invalidates effort, user evidence contradicts impact, or the quarterly review is due.

## Mode-Specific Delivery

Use the SKILL's Output Requirements without padding unexercised sections.

| Mode | Additional fields / format |
|---|---|
| FULL | Item count, frameworks, ρ with interpretation, overall confidence; ranked per-framework scores, final order, rationale/data source, sensitivity, bias corrections and next-agent/action reasons |
| QUICK | Rank, Item, ICE score, rationale; disclose single-framework scope |
| BATCH | MoSCoW groups with item counts and effort shares; per-item RICE/Effort/Action, Won't reasons, and top-five Must details |

A “Final Score” requires a declared, justified aggregation and compatible scales. Otherwise report final **order and rationale** alongside separate framework scores. Do not imply raw ICE/RICE numbers can be averaged. Per-item confidence stays explicit; unmeasured inputs stay estimates.
