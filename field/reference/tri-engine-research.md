# Multi-Engine Research Design

> **Filename retained** as `tri-engine-research.md` for backward compatibility. Covers both dual-engine baseline (Claude + Codex) and tri-engine optional (Claude + Codex + agy) modes.

Default flow for `/researcher multi`. Run subagents in parallel — one per AVAILABLE engine — to generate **research designs** (methodologies, interview guides, survey scaffolds, recruitment criteria, analysis plans), score them on methodology coverage and triangulation potential, then synthesize either a single Combined Plan (multi-method triangulation) or a Portfolio of independent research programs.

**Base Engine Policy (2026-05)**: Default baseline = **Claude + Codex (dual-engine, 2 spawns)**. agy adds a third axis (tri-engine, 3 spawns) when AVAILABLE at PREFLIGHT. dual-engine mode is NOT degraded. See `_common/MULTI_ENGINE_RECIPE.md §Base Engine Policy + §Engine Availability Modes`.

**Why multiple engines for research design (Pattern D — Divergence-primary):** Each engine carries a different methodological bias. Codex (GitHub-heavy) skews toward quantitative-heavy, instrument-driven designs (A/B tests, survey scales, log analysis). Claude (Anthropic-curated) skews toward qualitative-heavy, ethics-aware designs (open-ended interviews, diary studies, JTBD switch interviews) — together they form the dual-engine baseline covering quant + qual. Antigravity (Google-product-heavy, optional when AVAILABLE) skews toward mixed-methods at-scale (large-N usability, HEART metrics, longitudinal panels) — it patches the at-scale gap when reachable. For the same research question, the engines propose *non-overlapping methodology sets* — and triangulating across methods is the discipline's core quality lever. Single-engine breakthroughs (e.g., a guerrilla-test angle that solo Claude surfaces) are NOT auto-low-value.

**Pattern type:** D (Divergence-primary). See `_common/MULTI_ENGINE_RECIPE.md §Pattern D`. This document specifies only the **Field-specific differences**.

---

## Flow

```
SCOPE → PREFLIGHT → FAN-OUT → NORMALIZE → CLUSTER → SCORE (coverage matrix) → GROUND (ethics/IRB/feasibility) → SYNTHESIZE (Combined or Portfolio) → PRESENT
```

PREFLIGHT, FAN-OUT engine-dispatch table, NORMALIZE, and degraded modes are inherited verbatim from `_common/MULTI_ENGINE_RECIPE.md`. Verb is `research`; subagents are named `research-codex`, `research-agy`, `research-claude`.

---

## 1. SCOPE (Field-specific inputs)

All three subagents share the same scope packet:

- **Research question(s)** — primary + secondary, framed as questions, not features
- **Decision to influence** — what stakeholder choice the findings should de-risk
- **Generative vs evaluative** — exploratory discovery vs validation of a known design
- **Constraint envelope** — timeline (days/weeks), budget, recruitment access, sensitive-population flags
- **Prior evidence** — existing Pulse/Voice/Trace/Compete artifacts, prior personas, JTBD maps
- **Inclusion floor** — minimum diversity dimensions (physical/cognitive/situational/cultural) required
- **Ethics flags** — minors, vulnerable populations, regulated domains, PII handling constraints

Do NOT pass methodology templates, sample-size formulas, SUS/UEQ rubrics, or screener archetypes to subagents — those apply at SYNTHESIZE.

---

## 2. FAN-OUT JSON output schema (Field-specific)

Each subagent returns 2-4 research designs as JSON:

```json
{
  "engine": "codex|agy|claude",
  "research_designs": [
    {
      "design_id": "short slug, e.g. 'switch-interview-onboard'",
      "title": "Methodology-named title (e.g. 'JTBD Switch Interview with 8 recent switchers')",
      "research_question": "Which primary question this design addresses",
      "method": "interview | usability-test | survey | diary-study | card-sort | tree-test | ethnographic | jtbd-switch | concept-test | guerrilla-test | a-b-test | mixed-methods",
      "stance": "generative | evaluative | descriptive | causal",
      "qual_quant": "qualitative | quantitative | mixed",
      "sample_size": "integer with rationale string, e.g. '8 (qualitative saturation, ±20% benchmark precision not targeted)'",
      "recruitment": {
        "segment": "Target segment / persona",
        "screener_criteria": ["criterion 1", "criterion 2"],
        "inclusion_dimensions": ["accessibility need", "cultural background", "device class", ...],
        "exclusion_risks": ["screener-bias risk if any"]
      },
      "guide_outline": [
        "section 1 (warm-up, 5 min)",
        "section 2 (probe X, 15 min)",
        "..."
      ],
      "analysis_approach": "thematic-coding | affinity-mapping | jtbd-job-map | grounded-theory | descriptive-stats | inferential-stats | mixed",
      "timeline_days": "integer or range",
      "ethical_considerations": [
        "consent specifics",
        "compensation rationale",
        "data retention / anonymization plan",
        "AI-moderation or synthetic-user disclosure (if used)"
      ],
      "triangulation_partners": ["other method this could triangulate with, e.g. 'survey-quant-scale'"],
      "evidence_strength_expected": "high | medium | low",
      "limitations": ["WEIRD-sample risk", "self-report bias", "small-N", ...]
    }
  ],
  "engine_notes": "Optional: methodological bias this engine knows it brings (e.g. 'I tend toward quantitative scales')"
}
```

If an engine returns free-form Markdown, ask it to re-emit as JSON before integrating.

---

## 3. CLUSTER — identity rules (Field-specific)

Two research designs match into the same cluster ONLY when **all of**:

1. **Same primary research question** (semantic match, not literal)
2. **Same method class** — interview ≠ survey ≠ diary, even when the question matches
3. **Same stance** — generative ≠ evaluative

**Critical Field rule:** designs that share a research question but propose **different methodologies** must remain in **separate clusters**. The whole point of tri-engine research design is to surface methodology divergence; merging "JTBD interview" with "switch-behavior survey" into one cluster would destroy the signal.

Example:
- "8-person interview probing checkout abandonment" → Cluster A (interview / generative)
- "200-person survey on cart-abandonment self-report" → Cluster B (survey / descriptive)
- "Diary study over 2 weeks capturing checkout sessions" → Cluster C (diary / generative)
- All three address the same research question, but they are **three clusters, not one**.

Record the set of engines that produced each cluster.

---

## 4. SCORE — methodology coverage matrix (Pattern D, Field-specific)

Apply Pattern D concurrence labels per `_common/MULTI_ENGINE_RECIPE.md`:

| Engines in cluster | Concurrence label | Interpretation |
|--------------------|-------------------|----------------|
| 3 / 3 | `UNIVERSAL` | All engines independently chose this methodology — standard, defensible, safe |
| 2 / 3 | `LIKELY` | Two engines concur; note what the third proposed instead (likely a complementary triangulation partner) |
| 1 / 3 (pre-grounding) | `CANDIDATE-DIVERGENT` | Single-engine methodology proposal — must pass grounding to become `VERIFIED-DIVERGENT` |

Then build a **coverage matrix** across the qual/quant axis and the generative/evaluative axis:

|              | Generative              | Evaluative              | Descriptive            |
|--------------|-------------------------|-------------------------|------------------------|
| Qualitative  | clusters that fit here  | clusters that fit here  | clusters that fit here |
| Quantitative | clusters that fit here  | clusters that fit here  | clusters that fit here |
| Mixed        | clusters that fit here  | clusters that fit here  | clusters that fit here |

**Coverage gaps are findings.** If the matrix is heavily skewed (e.g., 5 qualitative-generative clusters and 0 quantitative-evaluative), surface the gap in PRESENT. The gap often indicates the research question is itself biased toward one stance.

**Triangulation graph:** for each cluster, list its `triangulation_partners` (other clusters whose method complements it — e.g., interview + survey + log analysis is a classic triangulation triple). Triangulation links are an input to SYNTHESIZE.

---

## 5. GROUND — ethics / IRB / feasibility checks (Field main context, never delegated)

For every cluster (especially `CANDIDATE-DIVERGENT`), the Field main context verifies:

1. **Method-feasibility check** — does the proposed sample size fit the timeline and budget envelope from SCOPE? Reject if obvious mismatch (e.g., 320-person ±5% benchmark in a 3-day timeline).
2. **Ethics / IRB check** — does the design touch minors, vulnerable populations, sensitive topics, or biometric data? If yes, confirm `ethical_considerations` covers consent, compensation, withdrawal rights, data retention. Mark `NEEDS-INFO` if ethics review is plausibly required and not addressed.
3. **Bias-floor check** — does `recruitment.inclusion_dimensions` meet the SCOPE inclusion floor? Reject `WEIRD-only` samples for products with global reach unless explicitly justified.
4. **Hallucination check** — are referenced personas (from Cast registry), prior studies, or product capabilities real? Reject hallucinated entities.
5. **AI-moderation / synthetic-user disclosure** — if the design uses AI moderators or synthetic participants, confirm BEST-framework consideration is present (per `reference/ai-assisted-research.md`). Reject if synthetic participants are positioned as substitutes for real users on emotional-depth or cultural-nuance questions.
6. **Sample-size sanity** — qualitative usability < 5, quantitative < 30, benchmark < 20 → flag the design as under-powered for its stated stance.

Mark each cluster: `VERIFIED-UNIVERSAL` / `VERIFIED-LIKELY` / `VERIFIED-DIVERGENT` / `REJECTED-{reason}` / `NEEDS-INFO`.

---

## 6. SYNTHESIZE — Combined Plan vs Portfolio (Field-specific merge)

Field supports two merge strategies. Default depends on triangulation density: **Combined Plan** when the surviving clusters form a coherent triangulation triple/quad; **Portfolio** when the clusters address independent research questions or compete on stance.

### Combined Plan Merge (default when triangulation graph is dense)

Use when surviving clusters cover at least two cells of the coverage matrix AND share the same primary research question.

1. Pick the **anchor cluster** — typically the `UNIVERSAL` cluster if present; otherwise the highest-strength `LIKELY` cluster.
2. Identify **triangulation partners** — 1-2 additional clusters whose methods complement the anchor (e.g., anchor = qualitative interview; partners = quantitative survey + behavioral log analysis).
3. Sequence them — generative first, then evaluative, then confirmatory quantitative. Define how findings from each phase feed the next.
4. Output a single Combined Research Plan at `docs/research/PLAN-[topic]-[date].md` containing:
   - Unified research questions and decisions to influence
   - Method-by-method section (one per included cluster) with full design details
   - Triangulation logic — which findings cross-validate which
   - Combined sample-size and timeline (sum across phases)
   - Combined ethics/consent posture
   - Aggregated `engine_concurrence` line in front matter (e.g., `engine_concurrence: anchor=3/3 [codex+agy+claude]; partner1=2/3 [agy+claude]; partner2=1/3 [codex-verified]`)

### Portfolio Merge (when research questions diverge or stances compete)

Use when surviving clusters do NOT form a coherent triangulation set — typically because the engines surfaced multiple distinct research questions or stances.

1. Keep all `VERIFIED-UNIVERSAL`, `VERIFIED-LIKELY`, and `VERIFIED-DIVERGENT` clusters (cap at 5-7).
2. Group by research question, then by stance within each question.
3. Order: `UNIVERSAL` first (safe methodology), then `LIKELY`, then `VERIFIED-DIVERGENT` (single-engine angle, often the breakthrough).
4. Output a single Portfolio document at `docs/research/PORTFOLIO-[topic]-[date].md` containing:
   - Coverage matrix summary (qual/quant × gen/eval cell counts)
   - Per-design entry: title, method, sample, guide outline, analysis approach, timeline, ethics, `engine_concurrence` tag
   - Recommendation — which 1-3 designs to run first and why (specific to the coverage matrix and decision-stakes from SCOPE)
   - Rejection ledger (condensed): count by category — duplicate / hallucination / ethics-gap / under-powered / WEIRD-bias / synthetic-misuse

### Engine-attribution rule (both strategies)

Every research design that ships carries an `engine_concurrence` tag:

- `[codex+agy+claude]` — 3/3 UNIVERSAL
- `[codex+agy]` (or any 2-engine combo) — 2/3 LIKELY
- `[codex-verified]` (or `[agy-verified]` / `[claude-verified]`) — 1/3 VERIFIED-DIVERGENT after grounding

For research designs that pass ethics/feasibility grounding with caveats, append `[NEEDS-IRB]` or `[NEEDS-INFO:<dim>]` after the concurrence tag.

---

## 7. PRESENT

**Combined Plan output**: a single research plan matching the standard Field report structure (`## User Research Report` → `### Research Objective` → `### Methodology` → ...), with the multi-method composition surfaced explicitly under `### Methodology` and `engine_concurrence` front matter at the top.

**Portfolio output**: a single document with:

- Header: which engines ran, which failed, total clusters surfaced, total shipped after grounding
- Coverage matrix table (qual/quant × gen/eval cell counts)
- Concurrence distribution (`UNIVERSAL: N, LIKELY: N, VERIFIED-DIVERGENT: N`)
- Per-design entries (see Portfolio Merge step 4)
- Rejection ledger (condensed)
- Recommendation: which 1-3 designs to run first, with reasoning tied to decision-stakes and coverage gaps

Do not surface engine-raw JSON. Do not include rejected clusters in the main list — they live only in the rejection ledger.

---

## Parallel Subagent Prompt Skeleton

Use the Agent tool three times **in the same message**. Each subagent receives a self-contained prompt:

```
You are the {engine} research-design subagent for Field.

# Role
Design {N=2-4} research approaches for the target below. You are one of three engines working independently — surface what your training data suggests is the most informative methodology mix. Do not try to be exhaustive; depth over breadth.

# Target
- Research question(s): {primary + secondary}
- Decision to influence: {what stakeholder choice the findings de-risk}
- Stance preference: {generative | evaluative | descriptive | open}
- Constraint envelope: timeline={days}, budget={amount or "open"}, recruitment access={notes}
- Prior evidence: {Pulse / Voice / Trace / Compete / prior personas if any}
- Inclusion floor: {minimum diversity dimensions}
- Ethics flags: {minors / vulnerable populations / sensitive topics / regulated domain — if any}

# Output format
Return ONLY JSON matching this exact schema (no commentary outside the JSON):

{JSON schema from §2 above}

# Constraints
- Methods must serve the research question — do not propose a method just because it is fashionable
- Separate observation from interpretation in analysis_approach
- For qualitative usability, never propose N < 5; for quantitative benchmarks, never propose N < 30
- If you propose AI-moderated interviews or synthetic participants, declare BEST-framework fit and human-oversight plan
- Inclusion dimensions must meet the floor — no WEIRD-only samples unless explicitly justified
- Do not write implementation code — research designs only
- Do not fabricate personas, prior studies, or product capabilities; if you reference existing artifacts, name them specifically
- Open with the deliverable (no completion preamble)
```

The three subagents return JSON; Field main context handles NORMALIZE through PRESENT.

---

## Cross-References

- `_common/MULTI_ENGINE_RECIPE.md` — base protocol, PREFLIGHT, degraded modes, attribution tags
- `_common/SUBAGENT.md §MULTI_ENGINE` — engine dispatch, loose prompts, fallback rules
- `spark/reference/tri-engine-proposal.md` — canonical Pattern D implementation
- `field/reference/interview-guide.md` — applied at SYNTHESIZE for interview-method clusters
- `field/reference/participant-screening.md` — applied at GROUND for recruitment/inclusion checks
- `field/reference/bias-checklist.md` — applied at GROUND for bias-floor checks
- `field/reference/ai-assisted-research.md` — applied at GROUND for AI-moderation / synthetic-user disclosure
- `field/reference/survey-quantitative-design.md` — applied at SYNTHESIZE for survey-method clusters
- `field/reference/continuous-discovery-mixed-methods.md` — applied at SYNTHESIZE for Combined-Plan triangulation logic
- `_common/OPUS_48_AUTHORING.md` — spawn prompt sizing, parallel-fan-out triggers
