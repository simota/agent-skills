# Spark Proposal Templates Reference

Purpose: define the canonical feature proposal structure and the interaction templates Spark may use to clarify scope or validation choices.

Related: for the inter-agent handoff packet shapes that feed into or out of these proposals (e.g. `ECHO_TO_SPARK_HANDOFF`, `SPARK_TO_SHERPA_HANDOFF`), see `reference/collaboration-patterns.md`.

## Contents
- Full proposal template
- Minimal proposal template
- Decision policy example
- Interaction question templates

## Canonical Proposal Template

Use this structure for the default Spark deliverable:

```markdown
# Feature: [Feature Name]

## Input Sources
- [ ] Scout
- [ ] Echo
- [ ] Field
- [ ] Voice
- [ ] Compete
- [ ] Pulse

## JTBD Foundation
- Job Statement
- Functional Job
- Emotional Job
- Social Job
- Force Balance

## Proposal Details
- Persona
- Priority
- RICE Score
- User Story
- Hypothesis
- Feasibility
- Requirements
- Acceptance Criteria

## Validation Plan
- Pre-Implementation
- Post-Implementation
- Decision Criteria

## Next Steps
- Recommended handoff
```

## Minimal Proposal Template

Use this only when the idea is straightforward:

```markdown
# Feature: [Feature Name]

**Persona**: [Primary persona]
**Priority**: [Impact-Effort quadrant]
**RICE Score**: [Calculation]
**User Story**: As a [persona], I want to [action] so that [benefit].
**Hypothesis**: [Measurable statement]
**Feasibility**: [Existing data, logic, or assumptions]

**Requirements**:
- [Requirement]

**Acceptance Criteria**:
- [Criterion]
```

## Example Decision Policy

Keep this style when a proposal includes a go/no-go policy:
- validation with `Experiment` for `2 weeks`
- success metric threshold such as `>= 30%`
- secondary adoption threshold such as `>= 40%`
- iterate band such as `15-30%`
- kill threshold such as `< 15%`

Use project-appropriate numbers, but keep the logic explicit.

## Bad Proposal Check

Reject proposals that:
- have no persona
- have no hypothesis
- have no feasibility note
- have no acceptance criteria
- chase novelty without a product rationale

## Interaction Trigger Question Templates

### `BEFORE_FEATURE_SCOPE`

```yaml
questions:
  - question: "What level of feature proposal do you need?"
    header: "Scope"
    options:
      - label: "Small improvement (Recommended)"
        description: "Extend existing functionality or improve UX"
      - label: "New feature"
        description: "Add new capability or workflow"
      - label: "Feature set"
        description: "Multiple related features as a package"
    multiSelect: false
```

### `ON_PRIORITY_ASSESSMENT`

```yaml
questions:
  - question: "How should we prioritize these features?"
    header: "Priority"
    options:
      - label: "Impact-Effort Matrix (Recommended)"
        description: "Quick visual quadrant analysis"
      - label: "RICE Score"
        description: "Detailed quantitative scoring"
      - label: "Persona Alignment"
        description: "Prioritize by target user needs"
      - label: "All frameworks"
        description: "Comprehensive analysis using all methods"
    multiSelect: false
```

### `ON_PERSONA_SELECTION`

```yaml
questions:
  - question: "Which user persona should this feature primarily target?"
    header: "Target"
    options:
      - label: "Power User"
        description: "Daily users seeking efficiency and advanced features"
      - label: "Casual User"
        description: "Occasional users needing simplicity"
      - label: "Admin/Manager"
        description: "Users with oversight and control needs"
      - label: "New User"
        description: "First-time users in onboarding phase"
    multiSelect: false
```

### `ON_SCOUT_INVESTIGATION`

```yaml
questions:
  - question: "Technical investigation needed. How should we proceed?"
    header: "Investigation"
    options:
      - label: "Request Scout investigation (Recommended)"
        description: "Have Scout analyze codebase for feasibility"
      - label: "Assume feasibility"
        description: "Proceed with proposal and note assumptions"
      - label: "Scope down"
        description: "Reduce the feature to known-feasible parts"
    multiSelect: false
```

### `ON_EXPERIMENT_REQUEST`

```yaml
questions:
  - question: "How should we validate this hypothesis before full implementation?"
    header: "Validation"
    options:
      - label: "A/B test with Experiment (Recommended)"
        description: "Statistical validation with a control group"
      - label: "Prototype with Forge first"
        description: "Prototype before a formal test"
      - label: "Validate with Echo personas"
        description: "Use persona walkthroughs instead of an experiment"
      - label: "Skip validation, proceed to implementation"
        description: "Use only when confidence is already high"
    multiSelect: false
```

### `ON_EXPERIMENT_RESULT`

```yaml
questions:
  - question: "Experiment returned results. What should we do with this hypothesis?"
    header: "Result Action"
    options:
      - label: "Proceed based on verdict (Recommended)"
        description: "Ship, iterate, or kill based on the result"
      - label: "Request deeper analysis"
        description: "Inspect segments or methodology more deeply"
      - label: "Iterate and re-test"
        description: "Adjust the hypothesis and run another test"
      - label: "Override verdict with justification"
        description: "Proceed only with documented reasoning"
    multiSelect: false
```

### `ON_VALIDATION_LOOP`

```yaml
questions:
  - question: "Echo validated the proposal. What's the next step?"
    header: "Next Step"
    options:
      - label: "Hand off to Sherpa for breakdown (Recommended)"
        description: "Ready for implementation planning"
      - label: "Request Experiment validation"
        description: "Need quantitative evidence before build"
      - label: "Iterate on proposal"
        description: "Revise the draft before handoff"
      - label: "Hand off to Forge for prototype"
        description: "Prototype before committing to build"
    multiSelect: false
```
