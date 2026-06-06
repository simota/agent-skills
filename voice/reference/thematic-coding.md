# Thematic Analysis Reference (Braun & Clarke)

Purpose: Inductive coding of open-ended feedback (survey free-text, interview transcripts, review bodies) using Braun & Clarke's six-phase reflexive thematic analysis (2006, refined 2019). Surfaces latent themes, tracks saturation, and converts unstructured text into a defensible, citable thematic map — the gold standard for qualitative feedback synthesis.

## Scope Boundary

- **voice `thematic`**: 6-phase Braun & Clarke coding, codebook governance, saturation tracking, inter-coder agreement (Cohen's κ / Krippendorff's α), and thematic map output. Inductive (data-driven) by default; deductive (framework-driven) on request.
- **voice `classify` (elsewhere)**: pre-defined category tagging for high-volume routing. Classify uses fixed buckets; thematic discovers them. Once thematic stabilizes a codebook, hand it off to `classify` for ongoing tagging.
- **voice `sentiment` (elsewhere)**: polarity / emotion detection per response. Orthogonal to themes — a single theme can carry positive and negative sentiment.
- **researcher (elsewhere)**: qualitative interview design and sampling. Researcher owns study design and recruitment; `thematic` owns the coding methodology applied to the resulting transcripts.
- **echo (elsewhere)**: persona-driven UX walkthrough. Thematic findings can validate or challenge persona assumptions; echo cannot substitute for grounded coding.
- **insight (elsewhere)**: synthesis-to-recommendation. Thematic produces themes; `insight` turns themes into prioritized actions.

## Workflow (Braun & Clarke 6 Phases)

```
PHASE 1   →  Familiarization — read all data twice before coding; capture initial impressions
          →  do not skip; analytic depth depends on immersion

PHASE 2   →  Initial coding — line-by-line tags on raw data; descriptive and short
          →  one segment can carry multiple codes; do not collapse early

PHASE 3   →  Theme search — cluster codes into candidate themes; build initial thematic map
          →  themes ≠ codes; themes capture meaning, codes capture surface

PHASE 4   →  Theme review — collapse, split, or drop themes against the full dataset
          →  every theme must have multiple supporting codes from multiple participants

PHASE 5   →  Theme definition — name and define each theme in one sentence; identify essence
          →  if you cannot define it in one sentence, it is two themes

PHASE 6   →  Report — narrative weaving themes with verbatim quotes; cite participant IDs
          →  themes answer the research question, not just summarize the data
```

## Inductive vs Deductive Coding

| Mode | When to use | Risk | Compatible benchmark |
|------|-------------|------|---------------------|
| Inductive (bottom-up) | Discovery, no prior framework, exploratory feedback | Researcher bias drifts theme boundaries | Saturation curve |
| Deductive (top-down) | Hypothesis testing against an existing framework (JTBD, OKR, persona) | Forces data into pre-defined buckets, misses emergent themes | Framework coverage rate |
| Hybrid | Most real studies | Documentation discipline required | Both above |

State the mode in the report header. Hybrid is the default for product feedback — apply a deductive frame (e.g., journey stage) but allow inductive sub-themes inside each frame cell.

## Theme Saturation Tracking

A theme is "saturated" when additional data adds no new codes within it. Track explicitly:

| Saturation indicator | Threshold | Action |
|----------------------|-----------|--------|
| New codes per 5 transcripts / 100 responses | ≤1 for 2 consecutive batches | Theme is saturated |
| Code redundancy rate | >70% of new segments tagged with existing codes | Approaching saturation |
| Outlier codes | Codes appearing in <2 sources | Document but do not theme |
| Negative cases | Data that contradicts the theme | Required — themes without negative-case search are weak |

For text feedback at scale, plot a saturation curve (cumulative unique codes vs. responses coded). Stop coding when the curve flattens for two consecutive batches.

## Sample Size Guidance

| Data source | n for thematic saturation | Notes |
|-------------|---------------------------|-------|
| In-depth interviews (60-90min) | 9-17 (Guest et al., 2006) | 12 is the field benchmark |
| Open-ended survey items | 100-300 responses | Saturation faster than interviews due to brevity |
| App store reviews | 200-500 | Higher noise — needs more volume per theme |
| Support tickets | 150-400 | Pre-classify by category before coding |
| NPS verbatim comments | 100-250 per score band | Saturate Detractor and Promoter bands separately |

Below the lower bound, treat output as exploratory only. Above the upper bound, returns diminish — cohort-split instead.

## 2026 LLM-Assisted Coding Stack

By 2026 the discipline shifted from "code by hand" to **LLM-first / human-validated** coding for any dataset of `200+` responses. Practical tooling:

| Tool | Strength | Use when |
|------|----------|----------|
| **Thematic** | AI theme discovery + impact scoring against NPS / churn + collaborative theme editor | Default for ongoing CX programs that want auto-routing + business-language taxonomy |
| **Buildbetter** | Conversation / call analysis + theme extraction | Sales calls, customer interviews at volume |
| **Perspective AI** | Mid-market default; explainable scoring | Teams that need both theme + sentiment in one pass |
| **Zonka / Qualaroo / Qualtrics XM** | LLM theme extraction layered on traditional survey platform | Teams already on a survey platform; avoid double-import |
| **Custom Claude / GPT-4 / Gemini pipeline** | Maximum control; pair with codebook from `Codebook Discipline` below | Highly proprietary taxonomies, regulated industries |

Quality bar from published benchmarks (2026): `~90-95%` theme-detection accuracy + sentiment on English B2B feedback when the LLM is given **a team-curated codebook**. Vendor-default categories rarely match how the business already discusses its product — always start from your `phase 4` locked codebook, not the tool's defaults.

### Human-in-the-Loop Discipline (mandatory)

- **Codebook ownership stays human.** The LLM proposes; the analyst accepts / merges / splits / rejects each candidate code before the codebook locks.
- **Spot-check Cohen's κ on 5-10% of LLM-assigned codes** before publishing themes. Below `κ = 0.6` agreement vs the analyst, the codebook needs another round.
- **Negative-case search remains a human task.** LLMs over-fit to dominant patterns; the "data that contradicts the theme" rule from the Saturation Tracking section is the analyst's job, not the model's.
- **Cite the LLM transcript ID** alongside participant ID for every quoted segment — the audit trail mirrors what Mend / Beacon require for AI-assisted artefacts.

## Codebook Discipline

- One code = one analytic idea. Prefer "feels lost in onboarding" over "onboarding bad."
- Code names are short (≤6 words), descriptive, and analyst-neutral (no judgmental words).
- Every code carries: definition (≤2 sentences), 2-3 verbatim examples, exclusion rule.
- New codes during phase 2/3 trigger codebook revision; revisions force re-coding of prior data.
- Lock the codebook only at phase 4 — phase 5/6 changes require re-opening phase 4.

## Inter-Coder Agreement

For multi-coder studies, measure agreement before reporting:

| Coefficient | Use | Threshold |
|-------------|-----|-----------|
| Cohen's κ | 2 coders, nominal codes | ≥0.61 substantial, ≥0.81 almost perfect |
| Krippendorff's α | ≥2 coders, missing data, ordinal/nominal | ≥0.667 acceptable, ≥0.80 strong |
| Percent agreement | Quick directional check only | Not publishable alone — inflated by chance |

Below the "acceptable" threshold, return to phase 5 to clarify code definitions, then re-code. Do NOT publish thematic results without an agreement statistic when ≥2 coders contributed.

## LLM-Assisted Coding (Augment, Don't Replace)

LLMs accelerate phase 2 (initial coding) but degrade phase 3-5 (theme construction) without human oversight.

- Use LLMs to generate first-pass codes on raw segments at temperature 0; require structured JSON output.
- Compare LLM codes against a 10-20% human-coded sample; reject if κ < 0.60 — re-prompt or fall back to manual.
- Never let LLMs name themes — theme construction is interpretive and the highest-bias step.
- Document LLM model, version, prompt, and seed in the report; LLM-coded studies are not reproducible without this.

## Anti-Patterns

- Skipping familiarization — coding cold produces shallow, surface-level codes that miss latent meaning.
- Treating frequent codes as themes — frequency ≠ significance; a single rich quote can anchor a theme that a frequency count would bury.
- Naming themes after categories ("Onboarding") instead of meaning ("Onboarding feels like a test you can fail") — category names are descriptive, not analytic.
- One-coder studies with no audit trail — irreproducible; demand at least a second-coder spot-check on 10% of data.
- Forcing all data into themes — leaving 5-15% as "outlier / unthemed" is honest; forcing 100% theme coverage manufactures themes.
- Ignoring negative cases — themes without disconfirming-evidence search are confirmation bias dressed up.
- Reporting themes without verbatim quotes — the evidence trail collapses; readers cannot verify.
- Pooling Detractor and Promoter NPS comments into one thematic pass — scoring asymmetry produces fundamentally different themes; code separately, then compare.
- Using deductive coding without naming the framework — readers cannot tell whether a theme was discovered or imposed.

## Handoff

- **To `voice classify`**: stable codebook (≥2 saturation batches) → operationalize as classifier categories for ongoing tagging at scale.
- **To `voice insight`**: theme-level findings with verbatim evidence → translation into prioritized actions and owner recommendations.
- **To Researcher**: ambiguous themes or persona divergence → escalate for moderated interviews to disambiguate.
- **To Spark**: themes describing unmet jobs or workarounds → feature proposals.
- **To Echo**: themes pointing to persona-specific friction → cognitive walkthrough validation.
- **To Retain**: themes correlating with churn cohort feedback → retention-program inputs.
- **To Helm**: cross-segment recurring themes → strategic narrative inputs.

References: Braun & Clarke (2006), "Using thematic analysis in psychology"; Braun & Clarke (2019), "Reflexive thematic analysis"; Guest, Bunce & Johnson (2006) on saturation thresholds.
