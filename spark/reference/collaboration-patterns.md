# Spark Collaboration Patterns Reference

Purpose: define the canonical handoff headers and minimum packets Spark uses with partner agents.

Related: for the proposal document structure these handoffs produce or consume, and for user-facing interaction question templates, see `reference/proposal-templates.md`.

## Contents
- Pattern map
- Input handoffs to Spark
- Output handoffs from Spark
- Scout and Canvas integrations
- Security and Growth reviews

## Pattern Map

| Pattern | Flow | Use when |
| --- | --- | --- |
| A | `Echo -> Spark -> Echo` | latent needs need a proposal and persona validation |
| B | `Field -> Spark` | research findings should become a feature proposal |
| C | `Voice -> Spark` | aggregated feedback should become a proposal |
| D | `Compete -> Spark` | competitive gaps or differentiation drive ideation |
| E | `Spark -> Experiment -> Spark` | a hypothesis needs structured validation |
| F | `Spark -> Sherpa/Forge/Builder` | a validated proposal is ready for planning or build |
| G | `Pulse -> Spark` | metrics or funnel gaps should become a proposal |
| H | `Spark -> Sentinel -> Spark` | the feature changes security or privacy posture |
| I | `Spark -> Growth -> Spark` | the feature affects SEO, CRO, or social sharing |

## Input Handoffs To Spark

### `## ECHO_TO_SPARK_HANDOFF`

Required fields:
- `Persona Analyzed`
- `Session Type`
- `Latent Needs Discovered`
  - `Need`
  - `Evidence`
  - `JTBD Context`
  - `Severity`
- `Confusion Points`

### `## RESEARCHER_TO_SPARK_HANDOFF`

Required fields:
- `Research Type`
- `Participants`
- `Key Insights`
  - `Insight`
  - `Evidence`
  - `Frequency`
  - `Impact`
- `Persona Updates`

### `## VOICE_TO_SPARK_HANDOFF`

Required fields:
- `Feedback Period`
- `Total Responses`
- `NPS Score`
- `Top Feature Requests`
  - `Rank`
  - `Request`
  - `Count`
  - `Sentiment`
  - `Representative Quote`
- `Pain Point Clusters`

### `## COMPETE_TO_SPARK_HANDOFF`

Required fields:
- `Competitors Analyzed`
- `Analysis Date`
- `Feature Gap Analysis`
  - `Feature`
  - `Us`
  - `Comp A`
  - `Comp B`
  - `Gap Type`
- `Differentiation Opportunities`
  - `Opportunity`
  - `Why We Can Win`

### `## PULSE_TO_SPARK_HANDOFF`

Required fields:
- `Analysis Period`
- `Primary Metric`
- `Funnel Drop-off Analysis`
  - `Stage`
  - `Current Rate`
  - `Target Rate`
  - `Drop-off %`
  - `Priority`
- `KPI Trends`
  - `Metric`
  - `Current`
  - `30-day Trend`
  - `Anomaly?`

## Output Handoffs From Spark

### `## SPARK_TO_ECHO_VALIDATION`

Required fields:
- `Proposal`
- `Target Persona`
- `Validation Questions`
- `Expected Echo Output`

### `## SPARK_TO_EXPERIMENT_HANDOFF`

Required fields:
- `Feature Proposal`
- `Hypothesis ID`
- `Hypothesis Statement`
  - `We believe`
  - `For`
  - `Will achieve`
  - `Success metric`
  - `Current baseline`
  - `Target goal`
- `Test Design Request`
  - `Recommended method`

### `## EXPERIMENT_TO_SPARK_RESULT`

Required fields:
- `Hypothesis ID`
- `Test Duration`
- `Sample Size`
- `Results`
  - `Metric`
  - `Control`
  - `Treatment`
  - `Δ`
  - `Significance`
- `Statistical Confidence`
- `Verdict`

Verdict values:
- `VALIDATED`
- `INVALIDATED`
- `INCONCLUSIVE`

### `## SPARK_TO_SHERPA_HANDOFF`

Required fields:
- `Feature`
- `Priority` (`P1/P2/P3`)
- `Validation Status`
- `Proposal Document`
- `Implementation Scope`
  - `Must Have`
  - `Should Have`
  - `Could Have`
- `Technical Context`
  - `Relevant files`

### `## SPARK_TO_FORGE_HANDOFF`

Required fields:
- `Feature`
- `Prototype Scope`
- `User Story`
- `Core Interaction`
- `Prototype Fidelity`
- `Validation Goal`

### `## SPARK_METRICS_PROPOSAL`

Required fields:
- `Source`
- `Target Metric`
- `Proposal`
- `Data-Driven Rationale`
  - `Current`
  - `Gap`
  - `Root cause hypothesis`
- `Acceptance Criteria`

### `## SPARK_TO_SENTINEL_HANDOFF`

Required fields:
- `Feature Proposal`
- `Proposal Doc`
- `Security-Relevant Aspects`
  - `Data Handling`
  - `Authentication/Authorization`
  - new input surfaces
  - external services

### `## SENTINEL_TO_SPARK_SECURITY_REQUIREMENTS`

Required fields:
- `Feature`
- `Review Date`
- `Risk Level`
- `Required Security Controls`
  - `Control Type`
  - `Implementation`
  - `Priority`

### `## SPARK_TO_GROWTH_HANDOFF`

Required fields:
- `Feature Proposal`
- `Feature Type`
- `SEO Impact Assessment`
- `Social Sharing Impact`
- `Conversion Impact`

### `## GROWTH_TO_SPARK_REQUIREMENTS`

Required fields:
- `Feature`
- `Review Date`
- `SEO Requirements`
- `OGP/Social Requirements`
- `CRO Requirements`

## Scout Integration

### Scout investigation request

Use when:
- data availability is unclear
- similar functionality may already exist
- implementation patterns need confirmation
- dependencies or affected files need discovery

Packet:
- `Feature Concept`
- `Investigation Scope`
- `Specific Questions`

### Scout investigation results

Return:
- `Feature`
- `Investigation Date`
- `Findings Summary`
  - `Data availability`
  - `Existing patterns`
  - `Feasibility`
- `Key Discoveries`
- `Impact on Proposal`

## Canvas Integration

Use Canvas when the proposal needs visualization.

Packets:
- `Feature Roadmap`
  - `Quick Wins`
  - `Big Bets`
  - `Experiments`
- `User Journey`
  - awareness
  - activation
  - retention
  - advocacy
- `Feature Dependencies`
  - new feature
  - existing data stores
  - APIs
  - services
- `Priority Matrix`
  - impact vs effort visualization

## Bidirectional Collaboration Matrix

### Input partners

| Partner | Input type | Trigger | Handoff |
| --- | --- | --- | --- |
| `Echo` | latent needs, confusion points | persona walkthrough complete | `ECHO_TO_SPARK_HANDOFF` |
| `Field` | personas, insights, journey maps | research synthesis complete | `RESEARCHER_TO_SPARK_HANDOFF` |
| `Voice` | feedback clusters, NPS | feedback analysis complete | `VOICE_TO_SPARK_HANDOFF` |
| `Compete` | gaps and positioning | competitive analysis complete | `COMPETE_TO_SPARK_HANDOFF` |
| `Pulse` | funnel data, KPI trends | metrics review complete | `PULSE_TO_SPARK_HANDOFF` |

### Output partners

| Partner | Output type | Trigger | Handoff |
| --- | --- | --- | --- |
| `Sherpa` | task breakdown request | proposal approved | `SPARK_TO_SHERPA_HANDOFF` |
| `Forge` | prototype request | validation needed | `SPARK_TO_FORGE_HANDOFF` |
| `Builder` | implementation spec | prototype validated or simple feature | `SPARK_TO_BUILDER_HANDOFF` |
| `Experiment` | test design | hypothesis needs validation | `SPARK_TO_EXPERIMENT_HANDOFF` |
| `Canvas` | roadmap or matrix visualization | proposal needs visual support | Canvas packet |
| `Echo` | proposal validation | draft proposal ready | `SPARK_TO_ECHO_VALIDATION` |
| `Scout` | technical investigation | feasibility unclear | Scout investigation request |
| `Growth` | SEO/CRO review | growth-sensitive feature | `SPARK_TO_GROWTH_HANDOFF` |
| `Sentinel` | security review | security-sensitive feature | `SPARK_TO_SENTINEL_HANDOFF` |


---

## Handoff Table (SKILL.md excerpt)

Spark receives product signals and insights from upstream agents, generates feature proposals, and hands off validated specifications to downstream agents.

| Direction | Handoff | Purpose |
|-----------|---------|---------|
| Pulse → Spark | Metrics handoff | Usage metrics and funnel data for opportunity analysis |
| Voice → Spark | Feedback handoff | User feedback and NPS signals for feature needs |
| Compete → Spark | Gap handoff | Competitive gaps for feature opportunities |
| Bond → Spark | Engagement handoff | Engagement and churn data for retention features |
| Cast → Spark | Persona handoff | Feature-focused personas for targeted proposals |
| Spark → Scribe | Spec handoff | Validated proposal needs formal specification |
| Spark → Builder | Implementation handoff | Proposal ready for implementation |
| Spark → Artisan | UI handoff | Proposal needs UI implementation |
| Spark → Accord | Integration handoff | Proposal needs integrated specification package |
| Spark → Forge | Prototype handoff | Proposal needs prototype before build |
| Spark → Experiment | Validation handoff | Proposal needs A/B test or experiment design |
| Spark → Canvas | Visualization handoff | Roadmap or feature matrix visualization needed |
| Spark → Magi | Decision handoff | Strategic Go/No-Go decision needed for high-risk proposals |
| Lens → Spark | Codebase insight | Existing data/logic capabilities for reuse opportunities |

**Overlap boundaries:**
- **vs Field**: Field = user research design and synthesis; Spark = feature proposal from research insights.
- **vs Voice**: Voice = feedback collection and sentiment analysis; Spark = feature ideation from feedback data.
- **vs Compete**: Compete = competitive analysis and positioning; Spark = converting competitive gaps into feature specs.
- **vs Scribe**: Scribe = formal specification writing; Spark = initial feature proposal and concept validation.

