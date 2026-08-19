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

## Collaboration Patterns and Overlap Boundaries (SKILL.md excerpt)

**Receives:** Cast (persona definitions), Voice (real feedback for calibration), Field (research findings), Echo (flow evaluation results), Compete (competitive intelligence)
**Sends:** Spark (feature request seeds), Rank (user urgency for prioritization), Scribe[unified] (user voice requirements), Scribe (PRD user stories), Saga (narrative material), Cast (PERSONA_FEEDBACK for calibration results and coverage gaps)

### Collaboration Patterns

| Pattern | Name | Flow | Purpose |
|---------|------|------|---------|
| **A** | Persona Pipeline | Cast → Echo[demand] → Spark | Personas to demands to proposals |
| **B** | Priority Advocacy | Echo[demand] → Rank | Feed user-felt urgency into priority scoring |
| **C** | Demand-Validation | Echo[demand] ↔ Echo | Demand generation ↔ existing flow verification |
| **D** | Reality Calibration | Voice → Echo[demand] | Calibrate synthetic demands with real feedback |
| **E** | Requirement Enrichment | Echo[demand] → Scribe[unified] | Integrate demands into spec packages |
| **F** | Research Grounding | Field → Echo[demand] | Generate demands grounded in real research findings |

### Overlap Boundaries

| vs | Their domain | Echo[demand]'s domain |
|----|-------------|---------------|
| **Voice** | Real customer feedback analysis (NPS, reviews, support tickets) | Synthetic demand generation when real data is absent or biased |
| **Echo** | Cognitive walkthrough of existing UI (what users feel) | Unmet demand discovery (what is missing) — Echo[demand] verbalizes the demand Echo's friction implies |
| **Field** | Real-user research design + validation (interviews, surveys, JTBD validation) | Synthetic hypothesis seeding — Echo[demand] outputs `synthetic: true` artifacts that Field validates |
| **Spark** | Structured feature proposal with hypothesis, KPIs, RICE scoring | Echo[demand] stops at first-person demand verbalization; hands off to Spark for structuring |
| **Cast** | Persona registry, lifecycle, evolution at `.agents/personas/registry.yaml` | Echo[demand] consumes Cast personas; never generates personas as a primary output (proto-personas are an emergency fallback only) |
| **Saga** | Customer-centric product narratives and stories | Echo[demand] provides raw user voice that Saga shapes into narrative arcs |

See `_common/PERSONA_CLUSTER_GUIDE.md` for the Cast / Echo[demand] / Voice / Echo cluster taxonomy.

### Handoff Patterns

See `reference/handoffs.md` for full handoff templates.

---

