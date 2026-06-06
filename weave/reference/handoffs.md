# Weave Handoff Templates

**Purpose:** Handoff templates between Weave and other agents.
**Read when:** You need the input or output format for Weave.

---

## Inbound Handoffs (To Weave)

### USER_TO_WEAVE_HANDOFF

```yaml
USER_TO_WEAVE_HANDOFF:
  request_type: "state_machine | saga | approval_flow | workflow"
  domain: "[Business domain description]"
  requirements:
    states: "[Known states or business phases]"
    events: "[Known triggers or actions]"
    constraints: "[Business rules, timeouts, limits]"
  existing_implementation: "[Current code/system if any]"
  expected_output: "state_machine_definition | saga_design | approval_flow | engine_recommendation"
```

### SCRIBE_TO_WEAVE_HANDOFF

```yaml
SCRIBE_TO_WEAVE_HANDOFF:
  spec_type: "[PRD | SRS | HLD]"
  relevant_sections:
    - section: "[Section name]"
      content: "[Extracted workflow-related requirements]"
  business_rules:
    - "[Rule 1]"
    - "[Rule 2]"
  expected_output: "State machine definition integrated into spec"
```

### ATLAS_TO_WEAVE_HANDOFF

```yaml
ATLAS_TO_WEAVE_HANDOFF:
  architecture_context:
    services: ["[Service list]"]
    dependencies: ["[Dependency map]"]
    communication: "[sync | async | event-driven]"
  workflow_concern: "[What workflow needs design]"
  expected_output: "Cross-service workflow / Saga design"
```

### NEXUS_TO_WEAVE_HANDOFF

```yaml
_AGENT_CONTEXT:
  Role: Weave
  Task: "[Specific workflow design task]"
  Mode: AUTORUN
  Chain: "[Previous agents]"
  Input: "[Handoff from previous agent]"
  Constraints:
    - "[Constraint 1]"
  Expected_Output: "[What Nexus expects]"
```

---

## Outbound Handoffs (From Weave)

### WEAVE_TO_BUILDER_HANDOFF

```yaml
WEAVE_TO_BUILDER_HANDOFF:
  summary: "Implement the designed state machine / workflow"
  state_machine:
    definition: "[Complete YAML state machine]"
    states_count: N
    transitions_count: N
    validation: "PASS"
  implementation_guidance:
    recommended_library: "[XState v5 | custom FSM | Temporal SDK]"
    patterns:
      - "[Pattern 1: e.g., use discriminated union for states]"
      - "[Pattern 2: e.g., implement guards as pure functions]"
    type_safety:
      - "State type: union of all state names"
      - "Event type: discriminated union with payloads"
      - "Context type: per-state context shapes"
    test_hooks:
      - "Export state machine for unit testing"
      - "Provide transition test helpers"
  files_to_create:
    - path: "[suggested file path]"
      purpose: "[what this file implements]"
```

### WEAVE_TO_CANVAS_HANDOFF

```yaml
WEAVE_TO_CANVAS_HANDOFF:
  summary: "Visualize the state machine / workflow"
  diagram_type: "stateDiagram-v2 | flowchart"
  state_machine:
    definition: "[Complete YAML state machine]"
  visualization_notes:
    - "Highlight error states in red"
    - "Group compound states"
    - "Show guard conditions on transitions"
  preferred_format: "mermaid | ascii | drawio"
```

### WEAVE_TO_RADAR_HANDOFF

```yaml
WEAVE_TO_RADAR_HANDOFF:
  summary: "Create tests for state machine transitions"
  state_machine:
    definition: "[Complete YAML state machine]"
  test_cases:
    happy_path:
      - name: "[Test name]"
        steps: ["[Event sequence]"]
        expected_final_state: "[State]"
    error_path:
      - name: "[Test name]"
        steps: ["[Event sequence including error]"]
        expected_final_state: "[Error state]"
    edge_cases:
      - name: "[Test name]"
        description: "[What edge case this covers]"
        steps: ["[Event sequence]"]
    guard_tests:
      - name: "[Test name]"
        state: "[Current state]"
        event: "[Event]"
        context: "[Context that should/shouldn't pass guard]"
        expected: "transition | blocked"
  coverage_target:
    state_coverage: "100%"
    transition_coverage: "100%"
    guard_coverage: "100%"
```

### WEAVE_TO_SCRIBE_HANDOFF

```yaml
WEAVE_TO_SCRIBE_HANDOFF:
  summary: "Document the workflow specification"
  workflow_design:
    state_machine: "[Complete definition]"
    saga: "[If applicable]"
    approval_flow: "[If applicable]"
  documentation_sections:
    - section: "State Transition Table"
      content: "[Formatted table]"
    - section: "Business Rules"
      content: "[Extracted guard conditions as rules]"
    - section: "Error Handling"
      content: "[Error states and recovery paths]"
  format: "SRS | HLD"
```

### WEAVE_TO_JUDGE_HANDOFF

```yaml
WEAVE_TO_JUDGE_HANDOFF:
  summary: "Review workflow design for correctness and completeness"
  artifacts:
    - type: "state_machine"
      content: "[Definition]"
    - type: "validation_report"
      content: "[Validation results]"
  review_focus:
    - "State completeness (are all business states represented?)"
    - "Transition correctness (are guards sufficient?)"
    - "Error handling (are all failure modes covered?)"
    - "Compensation design (are rollbacks complete?)"
```
