# Research Calibration System (DISTILL)

Purpose: Track research quality, recommendation adoption, and method effectiveness over time.
Contents: DISTILL workflow, adoption thresholds, calibration rules, question effectiveness, journal format, ecosystem sharing.

## DISTILL Workflow

`TRACK -> ASSESS -> REFINE -> SHARE`

## What To Track

- method effectiveness by context
- question types that produce rich data
- recommendation adoption
- insight accuracy after shipping
- participant segment usefulness
- bias detection and correction rate

## Adoption Thresholds

| Adoption rate | Interpretation | Action |
|---------------|----------------|--------|
| `> 0.70` | High-impact research | Keep approach |
| `0.40-0.70` | Moderate impact | Improve framing and actionability |
| `< 0.40` | Low impact | Revisit recommendation quality and stakeholder alignment |

## Assessment Triggers

| Trigger | What to assess |
|---------|----------------|
| Feature shipped from insight | Insight accuracy |
| Recommendation ignored | Framing and actionability |
| Persona used by Echo | Persona utility |
| Journey map cited in planning | Synthesis value |
| Quarterly review | Overall research effectiveness |

## Calibration Rules

1. Require `3+ studies` before adjusting method weights.
2. Cap each adjustment at `+/-0.15` per cycle.
3. Apply `10%` decay per quarter toward defaults.
4. Explicit user method preference overrides calibration.
5. For studies with `< 3 insights`, record only; do not update weights.

## Question-Type Calibration

| Question type | Typical richness | Best for |
|---------------|------------------|----------|
| Descriptive | High | Behavior understanding |
| Contrast | High | Value discovery |
| Evaluative | Medium | Emotion mapping |
| Hypothetical | Low-Medium | Latent needs, sparingly |
| Structural | Medium | Priority mapping |

## Journal Entry Format

```markdown
## YYYY-MM-DD - DISTILL: [Study Type]

**Studies assessed**: N
**Overall adoption rate**: X%
**Key insight**: [description]
**Calibration adjustment**: [method/question: old -> new]
**Apply when**: [future scenario]
**reusable**: true

<!-- EVOLUTION_SIGNAL
type: PATTERN
source: Field
date: YYYY-MM-DD
summary: [research methodology insight]
affects: [Field, Echo, Spark, Voice]
priority: MEDIUM
reusable: true
-->
```


## Per-Recipe Behavior (SKILL.md excerpt)

Behavior notes per Recipe:
- `interview`: Define research questions → author guide → design screener. Includes AI-moderation fit evaluation.
- `usability`: Test planning and task scenario design. Apply SUS/SEQ/CASTLE benchmark thresholds.
- `analysis`: Thematic analysis, coding, and affinity mapping. Bias check required.
- `persona`: Generate personas from research data. Disclose WEIRD bias and prepare Cast handoff.
- `journey`: Journey mapping + JTBD switch interview analysis. Includes Echo[demand] handoff determination.
- `survey`: Quantitative survey design — item authoring, scale selection, sample-size calculation, order-bias control, Cronbach's α validation. For usability cognitive walkthrough use Echo; for production KPI tracking events use Pulse; for operational NPS/CSAT feedback pipelines use Voice.
- `diary`: Longitudinal behavioral study — study length, ESM prompt frequency, self-report bias mitigation, fatigue management, media capture. For passive in-product telemetry use Pulse; for single-session cognitive walkthrough use Echo; for retrospective feedback mining use Voice.
- `cards`: IA validation — open / closed / hybrid card sort, tree testing, first-click testing, dendrogram and similarity-matrix analysis. For UI comprehension walkthrough use Echo; for post-launch navigation analytics use Pulse; for post-launch findability complaints use Voice.
- `multi`: Multi-engine research-design generation (see `Multi-Engine Mode` section + `reference/tri-engine-research.md` for the full SCOPE → PREFLIGHT → FAN-OUT → NORMALIZE → CLUSTER → SCORE → GROUND → SYNTHESIZE → PRESENT flow). Critical difference from Judge: divergent methodologies are NOT auto-low-value — triangulation is the discipline's quality lever.



## Secondary Thresholds (SKILL.md excerpt)

| Area | Threshold | Meaning | Default action |
|------|-----------|---------|----------------|
| Benchmark ±20% | `20` users | Rough directional benchmark | Early-stage internal comparison only |
| Benchmark ±10% | `~80` users | Reliable comparison | Cross-release or competitor benchmarking |
| Benchmark ±5% | `~320` users | High precision | Published reports or regulatory claims |
| Usability-only sample | `5-6` users | Small focused tests | Use for fast evaluative studies |
| AI transcription | `95–98%` on clear audio | Drops below 90% for non-native/noisy audio | Verify against source for accented audio |
| UEQ | 26 items, −3 to +3 | Pragmatic + hedonic UX with public benchmarks | Use alongside SUS against the UEQ benchmark dataset |
| NPS (consumer software) | `>21%` (industry avg) | Loyalty benchmark | Context-dependent; compare within vertical |
| Focus group | `6-8 per group` | Discussion balance | Avoid larger groups |

