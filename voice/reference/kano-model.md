# Kano Model Reference

Purpose: Classify product features by the asymmetric relationship between functionality and customer satisfaction (Kano 1984). Distinguishes "must-have" features (whose absence causes severe dissatisfaction but whose presence yields no delight) from "delighters" (whose absence is unnoticed but whose presence creates outsized satisfaction). Drives prioritization beyond simple "wanted / not wanted" rankings.

## Scope Boundary

- **voice `kano`**: Kano-style paired functional + dysfunctional surveys, classification matrix, Better/Worse coefficient computation, and feature prioritization recommendation. Operationalizes Kano on existing or proposed features.
- **voice `nps` (default)**: relationship loyalty score, not feature-level classification. NPS tells you "would they recommend"; Kano tells you "which features earn that recommendation."
- **voice `csat` / `ces` (elsewhere)**: touchpoint satisfaction or task effort. Kano operates at the feature level, CSAT/CES at the experience level.
- **researcher (elsewhere)**: exploratory feature discovery and JTBD interviews. Researcher generates the candidate feature list; Voice `kano` classifies it.
- **spark (elsewhere)**: feature ideation and product framing. Kano feeds Spark a prioritized backlog; Spark turns "delighters" into shipping specs.
- **echo (elsewhere)**: persona-level cognitive walkthrough. Kano segments persona may diverge — must-haves for power users may be delighters for novices.

## Workflow

```
SCOPE     →  freeze the feature list to be classified (5-20 features works best)
          →  exclude bug fixes, infra, and compliance items — Kano doesn't apply

AUTHOR    →  for each feature, write the paired functional + dysfunctional question
          →  use Kano's exact 5-option response set; do not reword or shorten

SAMPLE    →  recruit n≥30 per segment for stable classification; n≥100 for coefficients
          →  segment by persona, plan tier, or tenure — Kano categories shift across cohorts

CLASSIFY  →  map each respondent's paired answers to one of M/P/D/I/R/Q via the matrix
          →  feature category = mode of respondent classifications (or % distribution)

COEFFICIENT →  compute Better = (D+P) / (M+P+D+I) and Worse = -(M+P) / (M+P+D+I)
            →  plot on Better/Worse quadrant for prioritization

REPORT    →  category per feature, Better/Worse coefficients, segment splits, build/skip recommendation
          →  hand off Must-Haves to Spark for shipping specs, Delighters to Helm for differentiation
```

## The Five Kano Categories

| Category | Code | If present | If absent | Treat as |
|----------|------|------------|-----------|----------|
| Must-Have / Basic | M | No satisfaction (taken for granted) | Severe dissatisfaction | Table stakes — ship or do not launch |
| Performance / One-Dimensional | P | Linear satisfaction with quality | Linear dissatisfaction | Compete on degree — more is better |
| Delighter / Attractive | D | Outsized satisfaction | No dissatisfaction | Differentiator — unexpected wins |
| Indifferent | I | No reaction | No reaction | Cut — neither delights nor disappoints |
| Reverse | R | Dissatisfaction | Satisfaction | Anti-feature — remove if shipped |
| Questionable | Q | (Inconsistent answers) | (Inconsistent answers) | Survey error — exclude or re-ask |

Delighters decay over time: today's delighter becomes tomorrow's performance feature, then a must-have (Kano's lifecycle). Re-run Kano every 12-18 months for evolving categories.

## Paired Question Template (Use Verbatim)

For every feature X, ask both:

- **Functional**: "How would you feel if [feature X] were present?"
- **Dysfunctional**: "How would you feel if [feature X] were NOT present?"

Use exactly these 5 response options on both questions — published evaluation tables assume this exact set:

1. I like it that way
2. I expect it to be that way
3. I am neutral
4. I can live with it that way
5. I dislike it that way

Do NOT reword (e.g., "I love it" or "It would be great"). Reworded options break the published classification matrix.

## Kano Classification Matrix

Cross-tab functional × dysfunctional answers to derive category:

| Functional ↓ \ Dysfunctional → | Like | Expect | Neutral | Live with | Dislike |
|--------------------------------|------|--------|---------|-----------|---------|
| Like | Q | D | D | D | P |
| Expect | R | I | I | I | M |
| Neutral | R | I | I | I | M |
| Live with | R | I | I | I | M |
| Dislike | R | R | R | R | Q |

Keep this matrix verbatim — Berger et al. (1993) is the canonical reference. Cell `(Like, Like)` = Q because liking both presence and absence is contradictory.

## Better / Worse Coefficient Computation

Per Berger et al. (1993):

```
Better = (Delighter + Performance) / (Must + Performance + Delighter + Indifferent)
Worse  = -(Must + Performance)     / (Must + Performance + Delighter + Indifferent)
```

Plot features on a 2×2 quadrant: Better on Y-axis (0 to 1), Worse on X-axis (-1 to 0).

| Quadrant | Interpretation | Action |
|----------|----------------|--------|
| High Better, High Worse | Performance — competitive battleground | Invest, optimize quality |
| High Better, Low Worse | Delighter — differentiation lever | Ship, market heavily |
| Low Better, High Worse | Must-Have — risk if absent | Ship without fanfare |
| Low Better, Low Worse | Indifferent — neither wins nor loses | Defer or cut |

Drop Reverse (R) and Questionable (Q) features from the plot; they require their own treatment.

## Sample Size Calibration

| n per segment | Use | Notes |
|---------------|-----|-------|
| 10-29 | Internal directional only | Do not publish; Kano category boundaries are unstable here |
| 30-99 | Category mode reliable | Better/Worse coefficients have wide CI |
| 100-249 | Standard Kano study | Coefficients stable to ±0.05 |
| 250+ | Segmented Kano | Enables sub-segment classification (persona × tenure × plan) |

Below n=30 per segment, only the modal category is meaningful — coefficients fluctuate too much to support prioritization claims.

## Anti-Patterns

- Single-question Kano (asking only "do you want X?") — collapses all five categories into "yes/no" and erases the asymmetry that makes Kano useful.
- Reworded response options — breaks the published Berger matrix; results are no longer Kano.
- Mixing features and bug fixes in the same Kano study — bugs are always Must-Have or Reverse and crowd out signal on real features.
- Ignoring the Indifferent category — features classified as I are the highest-value cuts and the most often shipped anyway because someone advocated for them.
- Treating Delighters as launch must-ships — Delighters are nice-to-have by definition; they should never block launch on a Must-Have gap.
- One-time Kano without lifecycle re-runs — Delighters decay; classification 18 months ago is stale data.
- Pooling all respondents instead of segmenting — power users and novices often disagree on category, and the pooled mode hides the conflict.
- Using Kano for B2B procurement features without segmenting buyer vs user — what the buyer rates as Performance, the end user rates as Indifferent (or worse).

## Handoff

- **To Spark**: Must-Have gaps → blocking shipping specs; Delighter candidates → differentiation feature briefs.
- **To Pulse**: Performance features → KPI dashboards tracking the linear satisfaction relationship over time.
- **To Helm**: Delighter category map → strategic differentiation positioning.
- **To Researcher**: Questionable (Q) responses ≥10% → flag as ambiguous wording or unfamiliar feature; escalate for qualitative follow-up interviews.
- **To Echo**: Kano category divergence across personas → persona-specific walkthrough to confirm the cognitive gap.
- **To Compete**: Performance + High Worse features → competitor benchmark to size the parity gap.
- **To Retain**: Reverse (R) features in shipped product → candidates for removal or opt-out, especially in churn-correlated segments.
