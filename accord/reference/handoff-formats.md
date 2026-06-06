# Handoff Formats

Purpose: Use this file when Accord must consume or emit a structured handoff payload.

## Contents

- Inbound handoffs
- Outbound handoffs

## Inbound Handoffs

### `RESEARCHER_TO_ACCORD`

```yaml
RESEARCHER_TO_ACCORD:
  source: Researcher
  target: Accord
  payload:
    insights:
      user_needs: ["[need]"]
      pain_points: ["[pain point]"]
      journey_highlights: ["[journey highlight]"]
    personas: ["[persona: summary]"]
    evidence:
      research_method: "[interview/survey/observation]"
      sample_size: "[N]"
    expected_output: "Specification package with personas and insights reflected"
```

### `CAST_TO_ACCORD`

```yaml
CAST_TO_ACCORD:
  source: Cast
  target: Accord
  payload:
    personas:
      - name: "[persona]"
        role: "[role]"
        goals: ["[goal]"]
        frustrations: ["[frustration]"]
        tech_literacy: "[high/medium/low]"
    context:
      persona_source: "[generated/registry]"
    expected_output: "Persona-informed L0 target user definition"
```

### `VOICE_TO_ACCORD`

```yaml
VOICE_TO_ACCORD:
  source: Voice
  target: Accord
  payload:
    feedback:
      nps_score: "[0-10]"
      themes: ["[theme]"]
      quotes: ["[quote]"]
    sentiment: "[Positive/Neutral/Negative]"
    expected_output: "Specification package updated with stakeholder or user feedback"
```

## Outbound Handoffs

### `ACCORD_TO_SHERPA`

```yaml
ACCORD_TO_SHERPA:
  source: Accord
  target: Sherpa
  payload:
    specification:
      scope: "[Full/Standard/Lite]"
      requirements_count: "[N]"
      priority_breakdown:
        must: ["REQ-001", "REQ-003"]
        should: ["REQ-002"]
        could: ["REQ-005"]
    deliverables:
      l0_vision: "[vision summary]"
      requirements: ["REQ-XXX: summary"]
    context:
      teams: ["Biz", "Dev", "Design"]
      timeline: "[milestone]"
    expected_output: "Atomic steps suitable for execution planning"
```

### `ACCORD_TO_BUILDER`

```yaml
ACCORD_TO_BUILDER:
  source: Accord
  target: Builder
  payload:
    l2_dev:
      architecture: "[summary]"
      apis: ["API-001: summary"]
      data_models: ["DATA-001: summary"]
      tradeoffs: ["[choice: reason]"]
      dependencies: ["[dependency: version]"]
    requirements:
      must: ["REQ-XXX: build target"]
    acceptance_criteria:
      bdd_scenarios: ["AC-XXX: Given-When-Then"]
    context:
      non_functional:
        performance: "[target]"
        security: "[target]"
    expected_output: "Implementation based on L2-Dev"
```

### `ACCORD_TO_RADAR`

```yaml
ACCORD_TO_RADAR:
  source: Accord
  target: Radar
  payload:
    bdd_scenarios:
      - id: "AC-XXX"
        linked_req: "REQ-XXX"
        given: "[precondition]"
        when: "[action]"
        then: "[expected result]"
    edge_cases:
      - case: "[case]"
        input: "[input]"
        expected: "[expected behavior]"
    coverage_target:
      must_reqs: ["REQ-XXX"]
      scope: "[Full/Standard/Lite]"
    expected_output: "Test cases derived from BDD scenarios"
```

### `ACCORD_TO_VOYAGER`

```yaml
ACCORD_TO_VOYAGER:
  source: Accord
  target: Voyager
  payload:
    acceptance_criteria:
      scenarios: ["AC-XXX: Given-When-Then"]
    user_flows:
      - flow: "[flow]"
        steps: ["[step1]", "[step2]"]
        branches: ["[condition -> alternate path]"]
    context:
      target_env: "[browser/device]"
      a11y_level: "[WCAG AA/AAA]"
    expected_output: "E2E scenarios"
```

### `ACCORD_TO_CANVAS`

```yaml
ACCORD_TO_CANVAS:
  source: Accord
  target: Canvas
  payload:
    diagram_requests:
      - type: "[flowchart/sequence/er/state]"
        source: "[L2-Dev/L2-Design/L1]"
        content: "[what to render]"
    context:
      format: "[Mermaid/ASCII/draw.io]"
      audience: "[Biz/Dev/Design/All]"
    expected_output: "Diagrams that can be embedded into the package"
```

### `ACCORD_TO_SCRIBE`

```yaml
ACCORD_TO_SCRIBE:
  source: Accord
  target: Scribe
  payload:
    spec_package:
      scope: "[Full/Standard/Lite]"
      sections_completed: ["L0", "L1", "L2-Dev", "L3"]
    formal_doc_request:
      type: "[PRD/SRS/HLD/LLD]"
      audience: "[executive/engineering/client]"
      format: "[Markdown/Word/PDF]"
    context:
      traceability: "[complete/partial]"
    expected_output: "Formalized documentation"
```

### `ACCORD_TO_LORE`

```yaml
ACCORD_TO_LORE:
  source: Accord
  target: Lore
  payload:
    pattern:
      type: "SPECIFICATION_PATTERN"
      context: "[context]"
      scope: "[Full/Standard/Lite]"
      effectiveness:
        alignment_score: "[High/Medium/Low]"
        revisions: "[count]"
        downstream_adoption: "[adoption rate]"
      insight: "[validated pattern]"
      reusable: true
    expected_output: "Knowledge-base entry"
```
