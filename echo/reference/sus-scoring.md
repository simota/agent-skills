# SUS (System Usability Scale) Scoring Reference

Purpose: Administer, score, and interpret the System Usability Scale — John Brooke's 10-item instrument (1986) that remains the most cited, validated, and benchmarked quick-measure of perceived usability. Published benchmarks let a single number translate into a defensible grade.

## Scope Boundary

- **echo `sus`**: survey authoring, scoring, and benchmark comparison with percentile ranks, adjective grades, and letter grades. Also covers SUS variants (UMUX-Lite, SUPR-Q, UEQ) when SUS is the wrong fit.
- **echo `heuristic` (elsewhere)**: expert review of potential issues — SUS measures user-reported perception, heuristic measures evaluator-predicted violations. Use both; they rarely agree exactly.
- **field `usability` (elsewhere)**: moderated usability test design — SUS is typically administered at the end. Field owns study design; `sus` owns score interpretation.
- **voice `nps` (elsewhere)**: NPS measures loyalty, SUS measures usability. Correlated but not interchangeable; report both when you want a full picture.
- **palette (elsewhere)**: remediation — SUS is diagnostic, not prescriptive. Low scores route to Palette.

## Workflow

```
SELECT   →  choose SUS vs UMUX-Lite vs SUPR-Q vs UEQ based on study length and goal
         →  flag CASTLE for compulsory-workplace software (SUS is under-calibrated there)

DEPLOY   →  administer at task end, not mid-task; ensure ≥3 completed tasks first
         →  avoid priming — do not explain the scale; ask users to rate "as felt"

SCORE    →  compute per-respondent score (0-100), then mean with 90% CI
         →  do NOT treat SUS as percentage — 68 is average, not "68%"

INTERPRET →  map to grade + adjective + percentile via Sauro/Lewis curved grading
          →  segment by cohort (role, proficiency, device) when n≥10 per segment

REPORT   →  score, CI, grade, percentile rank, sample size, and qualitative context
         →  pair with task-completion and SEQ for triangulation
```

## SUS Item Set (Exactly as Published)

Odd items are positive (agree = good), even items are negative (agree = bad). Do NOT reword — reworded SUS is not comparable to benchmarks.

1. I think that I would like to use this system frequently.
2. I found the system unnecessarily complex.
3. I thought the system was easy to use.
4. I think that I would need the support of a technical person to use this system.
5. I found the various functions in this system were well integrated.
6. I thought there was too much inconsistency in this system.
7. I would imagine that most people would learn to use this system very quickly.
8. I found the system very cumbersome to use.
9. I felt very confident using the system.
10. I needed to learn a lot of things before I could get going with this system.

## Scoring Formula

```
For odd items (1, 3, 5, 7, 9):   contribution = response - 1
For even items (2, 4, 6, 8, 10): contribution = 5 - response
Sum all contributions, then multiply by 2.5.
Result range: 0 to 100.
```

Do NOT average across respondents before converting. Score each respondent (0-100), then take the mean of those 100-point scores.

## Benchmark Interpretation (Sauro / Lewis)

| SUS score | Grade | Adjective | Percentile | Usability verdict |
|-----------|-------|-----------|------------|-------------------|
| ≥80.3 | A | Excellent | 90th+ | Best-in-class |
| 74-80.3 | B | Good | 70-89th | Strong |
| 68-73 | C | OK | 50-69th | Average — the baseline mark |
| 51-67 | D | Poor | 15-49th | Below average, investigate |
| <51 | F | Awful | <15th | Critical usability issue |

68 is the **sample-weighted average** across thousands of Sauro-reported studies. Treat it as the "pass / fail" line for consumer software. Enterprise software trends lower (~62) — CASTLE is a better fit there.

## Minimum Detectable Difference (Sample Size)

| Sample | Detectable SUS difference (90% CI, ±) |
|--------|---------------------------------------|
| n=10 | ±12 points — directional only |
| n=20 | ±8 points — rough comparison |
| n=30 | ±6 points — standard benchmark |
| n=60 | ±4 points — reliable comparison |
| n=120 | ±3 points — precise benchmark |

Below n=30, SUS can only detect coarse differences. Below n=10, the confidence interval is wider than most grade boundaries — do not grade.

## Variants and When to Use Them

| Instrument | Items | Use when |
|------------|-------|----------|
| SUS | 10 | General usability, published benchmark comparison needed |
| UMUX-Lite | 2 | Ultra-short survey, in-product micro-survey, frequent re-measurement |
| SUPR-Q | 8 | Website usability + trust + loyalty + appearance |
| UEQ (short) | 8 | Pragmatic + hedonic UX in a single instrument |
| UEQ (full) | 26 | Deep UX quality with 6 scales (efficiency, perspicuity, dependability, stimulation, novelty, attractiveness) |
| CASTLE | 6 dims | Compulsory / workplace B2B software |
| NASA-TLX | 6 | Task workload, cognitive demand — pair with SUS for task-level diagnosis |

SUS alone is weak for emotional / hedonic quality — pair with UEQ or SUPR-Q if that matters.

## Common Deployment Errors

- Administering SUS mid-task — contaminates responses with task-state bias.
- Converting SUS to a percentage ("68%") — SUS is a score, not a percentage. A SUS of 68 is 50th-percentile (average), NOT "68% usability."
- Translating SUS items without cognitive validation — translated SUS drifts up to 8 points in some languages. Use validated translations (German, Japanese, Spanish published), revalidate otherwise.
- Comparing SUS before vs after a redesign without controlling cohort composition — composition shifts (e.g., more power users in the post sample) inflate scores independent of design.
- Stopping at the number — a SUS of 58 tells you "below average" but not why. Always pair with SEQ, task completion, or open-ended follow-up.
- Dropping items to "save time" — subset SUS is no longer SUS and loses benchmark compatibility. Use UMUX-Lite instead.

## Triangulation Rules

A single SUS number is fragile. Report alongside:

- **Task completion rate**: SUS ≥80 but completion <78% indicates users believe the product is easy despite failing — often a confidence-miscalibration signal.
- **SEQ per task**: pinpoints which specific tasks drag the overall SUS down.
- **NPS or SUPR-Q**: loyalty and satisfaction dimensions that SUS doesn't capture.
- **Open-ended "one thing to fix"**: converts the score into an action list.

SUS ≥80 + completion <78% + low SEQ on one task = strong signal to investigate that specific task, not redesign the whole system.

## Anti-Patterns

- Publishing a SUS score without n and CI — unfalsifiable.
- Using a reworded or shortened SUS and citing Sauro benchmarks — benchmark invalid.
- Treating a single-study SUS as the product's "usability score" — SUS drifts ±5 points run-to-run with stable UI; one number is not a trend.
- Comparing a moderated SUS (in-person) and an unmoderated SUS (remote survey) — published research shows systematic drift between modes.
- Using SUS to compare categorically different products (website vs native app vs kiosk) — domain effects swamp design quality.
- Over-claiming a "good" SUS of 72 without noting it's merely above-average (C grade) — C is not a launch gate.

## Handoff

- **To Palette**: if mean SUS <68 with n≥30, emit top 3 SEQ-weak tasks as the remediation backlog.
- **To Field**: if SUS is ambiguous (68-74 band) or contradicts behavioral data, escalate for a 5-user moderated study.
- **To Judge**: SUS <51 with n≥30 as a ship-blocker with percentile evidence.
- **To Echo `heuristic`**: cross-reference low SUS against heuristic violations — overlap signals the highest-confidence fixes.
- **To Voice**: low SUS with active NPS panel → deploy targeted "what went wrong" micro-survey to detractor cohort.
