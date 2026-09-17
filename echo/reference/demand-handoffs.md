# Echo[demand] Handoff Templates

**Purpose:** Standard inter-agent handoff templates.
**Read when:** Agent collaboration is needed.

---

## Inbound Handoffs

### From Cast (CAST_TO_ECHO_DEMAND_HANDOFF)

```yaml
CAST_TO_ECHO_DEMAND_HANDOFF:
  personas:
    - name: "[Persona name]"
      archetype: "[Archetype]"
      registry_id: "[Cast registry ID]"
      key_traits: "[Key traits]"
      pain_points: "[Known pain points]"
  product_context: "[Product overview]"
  focus_area: "[Feature/area to focus on]"
  mode_suggestion: "EXPLORE | CHALLENGE | DEEP | COMPETE | EDGE"
```

### From Voice (VOICE_TO_ECHO_DEMAND_HANDOFF)

Echo[demand] does not re-analyze sentiment — these numbers are for calibration reference only.

```yaml
VOICE_TO_ECHO_DEMAND_HANDOFF:
  real_feedback_summary:
    top_complaints: ["[Complaint 1]", "[Complaint 2]"]
    underrepresented_segments: ["[Segment not captured 1]"]
    sentiment_distribution:
      positive: "[X%]"
      neutral: "[Y%]"
      negative: "[Z%]"
  calibration_request: |
    Generate synthetic demands for segments
    underrepresented in real feedback.
```

### From Field (RESEARCHER_TO_ECHO_DEMAND_HANDOFF)

```yaml
RESEARCHER_TO_ECHO_DEMAND_HANDOFF:
  research_findings:
    key_insights: ["[Insight 1]", "[Insight 2]"]
    unmet_needs: ["[Unmet need 1]"]
    journey_pain_points: ["[Journey pain point 1]"]
  persona_data: "[Persona data from research]"
  grounding_request: |
    Verbalize concrete demands in the user's own
    words, grounded in research findings.
```

### From Echo (ECHO_TO_ECHO_DEMAND_HANDOFF)

```yaml
ECHO_TO_ECHO_DEMAND_HANDOFF:
  walkthrough_results:
    friction_points: ["[Friction point 1]", "[Friction point 2]"]
    confusion_areas: ["[Confusion area 1]"]
    emotion_scores:
      - touchpoint: "[Touchpoint]"
        score: "[Emotion score]"
  demand_request: |
    Generate improvement demands that users would
    want for friction points found in flow evaluation.
```

---

## Outbound Handoffs

### To Spark (ECHO_DEMAND_TO_SPARK_HANDOFF)

```yaml
ECHO_DEMAND_TO_SPARK_HANDOFF:
  source: Echo[demand]
  session_summary:
    personas_used: [N]
    total_requests: [M]
    mode: "EXPLORE | CHALLENGE | DEEP | COMPETE | EDGE"
  feature_requests:
    - title: "[Request title]"
      personas: ["[Persona 1]", "[Persona 2]"]
      user_urgency: "HIGH | MEDIUM | LOW"
      user_voice_excerpt: "[User voice excerpt]"
      acceptance_criteria:
        - "[Criterion 1]"
        - "[Criterion 2]"
  cross_persona_patterns:
    - pattern: "[Shared pattern]"
      mentioned_by: ["[Persona 1]", "[Persona 2]"]
  assumption_challenges:
    - assumption: "[Team assumption]"
      counter: "[User reality]"
  proposal_request: |
    Convert user demands into structured feature proposals.
    Prioritize shared patterns and high-urgency requests.
```

### To Rank (ECHO_DEMAND_TO_RANK_HANDOFF)

```yaml
ECHO_DEMAND_TO_RANK_HANDOFF:
  source: Echo[demand]
  items_to_prioritize:
    - title: "[Request title]"
      user_urgency: "HIGH | MEDIUM | LOW"
      persona_count: [N]
      emotional_impact: "[Emotional impact summary]"
      churn_risk: "HIGH | MEDIUM | LOW"
  priority_request: |
    Quantify priority factoring in user-felt urgency.
```

### To Scribe[unified] (ECHO_DEMAND_TO_SCRIBE_HANDOFF)

```yaml
ECHO_DEMAND_TO_SCRIBE_HANDOFF:
  source: Echo[demand]
  user_requirements:
    - requirement: "[Requirement]"
      user_voice: "[User voice]"
      acceptance_criteria:
        - "[Criterion 1]"
  integration_request: |
    Integrate user demands into the requirements
    section of the spec package.
```

### To Scribe (ECHO_DEMAND_TO_SCRIBE_HANDOFF)

```yaml
ECHO_DEMAND_TO_SCRIBE_HANDOFF:
  source: Echo[demand]
  user_stories:
    - as_a: "[Persona archetype]"
      i_want: "[Demand]"
      so_that: "[Purpose/value]"
      voice_excerpt: "[User voice excerpt]"
  document_request: |
    Incorporate user stories into the use case
    section of the PRD.
```

### To Saga (ECHO_DEMAND_TO_SAGA_HANDOFF)

```yaml
ECHO_DEMAND_TO_SAGA_HANDOFF:
  source: Echo[demand]
  narrative_material:
    personas:
      - name: "[Persona name]"
        emotional_journey: "[Emotional progression]"
        key_quotes: ["[Quote 1]", "[Quote 2]"]
    transformation_potential:
      before: "[Current struggling state]"
      after: "[State after demand is fulfilled]"
  story_request: |
    Convert user voices into customer stories.
```

---

## Paste-ready demand prompts

Every request carries `### LLM Instruction Prompt`; every report closes with `## LLM Orchestration Prompt (paste-ready)`. Preserve first-person voice verbatim, persona/demand IDs, acceptance criteria and contradictions. Mark `synthetic: true`; engine agreement is not real-user validation. Carry calibration and observed `engine_concurrence` with the actual usable-engine denominator.

| Verb | Receiving task |
|---|---|
| `ANALYZE` | Scope/root cause/market fit; Field, Compete or Rank |
| `PROPOSE` | Feature hypothesis and KPIs; Spark |
| `DESIGN` | UX flow or interaction model; Vision/Palette |
| `DRAFT-SPEC` | PRD/user stories/spec package; Scribe |
| `PROTOTYPE` | Authorized runnable prototype; Forge/Builder |
| `REFINE` | Narrow/ground a demand, resolve explicit contradictions; Echo/Field/Voice |

Per-request prompt fields: Persona (name/archetype/context/emotion), Demand (ID/title/scene), User voice (verbatim), Why it matters, Acceptance criteria, **Your task** (one verb + expected deliverable), Constraints (synthetic hypothesis; no silent feasibility rejection; flag assumptions and blocking ambiguities).

Per-report prompt fields: Source (scope/personas/demand count), structured Demands with attribution, Cross-persona analysis, Assumption challenges (at least three where the mode requires them), **Your task** (one selected receiving role and artifact), Constraints (synthetic provenance; demand-ID traceability; contradictions retained; unresolved AC ambiguity surfaced before committing to a solution).

Do not repeat every receiving role's job inside the same executable task or treat the prompt itself as authorization to implement/publish. Calibration promotion still requires the cited real-data match in `reference/demand-calibration.md`.
