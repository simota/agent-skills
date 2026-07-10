# Handoff Templates

**Purpose:** Handoff templates between Saga and other agents.
**Read when:** Receiving input from another agent, or passing output to another agent.

---

## Inbound Handoffs (input to Saga)

### CAST_TO_SAGA_HANDOFF

Receive persona definitions from Cast and generate persona-specific stories.

```yaml
CAST_TO_SAGA_HANDOFF:
  persona:
    name: "[persona name]"
    demographics: "[age, occupation, situation]"
    goals: "[primary goals]"
    frustrations: "[primary frustrations]"
    tech_level: "[tech proficiency level]"
    quotes: "[representative quotes]"
  request:
    story_type: "[use_case | scenario | onboarding]"
    feature_context: "[target feature/product]"
    audience: "[target audience]"
```

### RESEARCHER_TO_SAGA_HANDOFF

Receive research findings from Field and convert them into a narrative.

```yaml
RESEARCHER_TO_SAGA_HANDOFF:
  research_type: "[interview | usability_test | journey_map | survey]"
  key_findings:
    - "[Finding 1]"
    - "[Finding 2]"
  personas: "[persona info (if available)]"
  journey_map: "[journey map (if available)]"
  pain_points:
    - "[Pain 1]"
    - "[Pain 2]"
  request:
    story_type: "[customer_success | use_case | scenario]"
    audience: "[target audience]"
```

### VOICE_TO_SAGA_HANDOFF

Receive customer feedback insights from Voice and convert them into a story.

```yaml
VOICE_TO_SAGA_HANDOFF:
  feedback_summary:
    positive_themes:
      - "[theme 1]"
    negative_themes:
      - "[theme 2]"
    nps_score: "[NPS (if available)]"
  representative_quotes:
    - "[quote 1]"
    - "[quote 2]"
  request:
    story_type: "[customer_success | use_case]"
    focus: "[positive experience | pain point improvement]"
```

### SPARK_TO_SAGA_HANDOFF

Receive a feature proposal from Spark and craft a "why it's needed" narrative.

```yaml
SPARK_TO_SAGA_HANDOFF:
  feature:
    name: "[feature name]"
    hypothesis: "[hypothesis]"
    target_persona: "[target persona]"
    rice_score: "[RICE Score]"
    acceptance_criteria:
      - "[criterion 1]"
  request:
    story_type: "[use_case | pitch]"
    audience: "[dev team | stakeholders | investors]"
```

### COMPETE_TO_SAGA_HANDOFF

Receive competitive analysis from Compete and craft a differentiation narrative.

```yaml
COMPETE_TO_SAGA_HANDOFF:
  differentiators:
    - "[differentiator 1]"
    - "[differentiator 2]"
  competitive_landscape: "[market state]"
  positioning: "[positioning]"
  request:
    story_type: "[product_narrative | pitch]"
    emphasis: "[differentiation | market opportunity]"
```

---

## Outbound Handoffs (output from Saga)

### SAGA_TO_PROSE_HANDOFF

Pass UX copy direction to Prose, derived from Saga's narrative.

```yaml
SAGA_TO_PROSE_HANDOFF:
  narrative_summary: "[narrative summary]"
  brand_voice:
    tone: "[tone: friendly/professional/etc.]"
    personality: "[personality: reliable/empathetic/etc.]"
    vocabulary_notes: "[words to use/avoid]"
  key_messages:
    - "[message 1]"
    - "[message 2]"
  transformation_arc:
    before: "[Before state]"
    after: "[After state]"
  copy_requests:
    - type: "[onboarding | error | cta | tooltip]"
      context: "[screen/situation where used]"
      tone_note: "[tone instructions for this copy]"
```

### SAGA_TO_SCRIBE_HANDOFF

Pass the PRD use-case section to Scribe, derived from Saga's narrative.

```yaml
SAGA_TO_SCRIBE_HANDOFF:
  use_cases:
    - name: "[use case name]"
      actor: "[actor]"
      precondition: "[precondition]"
      main_flow: "[main flow summary]"
      narrative_context: "[background drawn from the story]"
      emotional_context: "[user's emotional state]"
  personas_referenced:
    - "[persona name]"
  assumptions:
    - "[assumption 1]"
```

### SAGA_TO_ACCORD_HANDOFF

Pass the L0 vision's customer experience description to Accord, derived from Saga's narrative.

```yaml
SAGA_TO_ACCORD_HANDOFF:
  vision_narrative: "[product vision narrative]"
  customer_scenarios:
    - persona: "[persona name]"
      scenario: "[scenario summary]"
      desired_outcome: "[desired outcome]"
  transformation:
    before: "[current state]"
    after: "[ideal state]"
  key_value_propositions:
    - "[value proposition 1]"
    - "[value proposition 2]"
```

### SAGA_TO_DIRECTOR_HANDOFF

Pass a demo video scenario to Director, derived from Saga's narrative.

```yaml
SAGA_TO_DIRECTOR_HANDOFF:
  scenario:
    title: "[demo title]"
    duration_target: "[target length: 30s / 60s / 120s]"
    persona: "[protagonist persona]"
    narrative_arc:
      setup: "[situation setup]"
      conflict: "[presentation of the challenge]"
      resolution: "[resolution via the product]"
      outcome: "[outcome]"
    key_screens:
      - screen: "[screen name]"
        action: "[action taken]"
        narration: "[narration/on-screen text]"
        emotion: "[user's emotion at this point]"
  voice_and_tone: "[narration tone instructions]"
```
