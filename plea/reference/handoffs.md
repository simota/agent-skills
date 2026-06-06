# Plea Handoff Templates

**Purpose:** Standard inter-agent handoff templates.
**Read when:** Agent collaboration is needed.

---

## Inbound Handoffs

### From Cast (CAST_TO_PLEA_HANDOFF)

```yaml
CAST_TO_PLEA_HANDOFF:
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

### From Voice (VOICE_TO_PLEA_HANDOFF)

Plea does not re-analyze sentiment — these numbers are for calibration reference only.

```yaml
VOICE_TO_PLEA_HANDOFF:
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

### From Field (RESEARCHER_TO_PLEA_HANDOFF)

```yaml
RESEARCHER_TO_PLEA_HANDOFF:
  research_findings:
    key_insights: ["[Insight 1]", "[Insight 2]"]
    unmet_needs: ["[Unmet need 1]"]
    journey_pain_points: ["[Journey pain point 1]"]
  persona_data: "[Persona data from research]"
  grounding_request: |
    Verbalize concrete demands in the user's own
    words, grounded in research findings.
```

### From Echo (ECHO_TO_PLEA_HANDOFF)

```yaml
ECHO_TO_PLEA_HANDOFF:
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

### To Spark (PLEA_TO_SPARK_HANDOFF)

```yaml
PLEA_TO_SPARK_HANDOFF:
  source: Plea
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

### To Rank (PLEA_TO_RANK_HANDOFF)

```yaml
PLEA_TO_RANK_HANDOFF:
  source: Plea
  items_to_prioritize:
    - title: "[Request title]"
      user_urgency: "HIGH | MEDIUM | LOW"
      persona_count: [N]
      emotional_impact: "[Emotional impact summary]"
      churn_risk: "HIGH | MEDIUM | LOW"
  priority_request: |
    Quantify priority factoring in user-felt urgency.
```

### To Accord (PLEA_TO_ACCORD_HANDOFF)

```yaml
PLEA_TO_ACCORD_HANDOFF:
  source: Plea
  user_requirements:
    - requirement: "[Requirement]"
      user_voice: "[User voice]"
      acceptance_criteria:
        - "[Criterion 1]"
  integration_request: |
    Integrate user demands into the requirements
    section of the spec package.
```

### To Scribe (PLEA_TO_SCRIBE_HANDOFF)

```yaml
PLEA_TO_SCRIBE_HANDOFF:
  source: Plea
  user_stories:
    - as_a: "[Persona archetype]"
      i_want: "[Demand]"
      so_that: "[Purpose/value]"
      voice_excerpt: "[User voice excerpt]"
  document_request: |
    Incorporate user stories into the use case
    section of the PRD.
```

### To Saga (PLEA_TO_SAGA_HANDOFF)

```yaml
PLEA_TO_SAGA_HANDOFF:
  source: Plea
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
