# Interaction Triggers

Purpose: Use this file when Accord must pause and serialize an ask-first decision as a YAML trigger.

## Contents

- Trigger table
- YAML templates
- Detection heuristics

## Trigger Table

| Trigger | Condition | Safe default |
|---|---|---|
| `SCOPE_UNCLEAR` | complexity indicators mix low, medium, and high signals | proceed with `Standard` |
| `TEAM_UNKNOWN` | team composition cannot be inferred safely | assume Biz + Dev + Design |
| `REQUIREMENTS_OVERFLOW` | requirements are `10+` and not decomposed | propose Sherpa first |
| `L2_TECH_DEPTH` | `L2-Dev` needs architecture decisions | consult Atlas or Gateway |
| `L2_DESIGN_SCOPE` | `L2-Design` requires visual deliverables | delegate visuals to Vision or Palette |
| `STAKEHOLDER_EXPANSION` | legal, security, compliance, or other extra stakeholders join | confirm scope expansion |

## YAML Templates

### `SCOPE_UNCLEAR`

```yaml
INTERACTION_TRIGGER:
  type: SCOPE_UNCLEAR
  condition: "Mixed complexity indicators make scope selection ambiguous."
  question: "The complexity signals are mixed. Which scope should Accord use?"
  options:
    - "Full (12+ requirements, complete package)"
    - "Standard (4-11 requirements, involved L2 sections only) (Recommended)"
    - "Lite (1-3 requirements, inline details)"
    - "Other (please specify)"
  context:
    complexity_indicators: "[detected indicators]"
    teams_involved: "[detected teams]"
  default: "Standard"
```

### `TEAM_UNKNOWN`

```yaml
INTERACTION_TRIGGER:
  type: TEAM_UNKNOWN
  condition: "The participating teams cannot be inferred safely."
  question: "Which teams should this package serve?"
  options:
    - "Business, Development, and Design (Recommended)"
    - "Development and Design"
    - "Business and Development"
    - "Other (please specify)"
  context:
    detected_keywords: "[team-related keywords]"
  default: "Business, Development, and Design"
```

### `REQUIREMENTS_OVERFLOW`

```yaml
INTERACTION_TRIGGER:
  type: REQUIREMENTS_OVERFLOW
  condition: "The package would cover 10 or more requirements without decomposition."
  question: "The scope is large. Should Accord ask Sherpa to decompose it first?"
  options:
    - "Decompose with Sherpa first, then write specs (Recommended)"
    - "Keep one Full package"
    - "Write only the highest-priority slice first"
    - "Other (please specify)"
  context:
    requirements_count: "[count]"
    estimated_scope: "Full"
  default: "Decompose with Sherpa first, then write specs"
```

### `L2_TECH_DEPTH`

```yaml
INTERACTION_TRIGGER:
  type: L2_TECH_DEPTH
  condition: "L2-Dev requires architecture or technical trade-off decisions."
  question: "Architecture judgment is required. How should Accord proceed?"
  options:
    - "Consult Atlas or Gateway first (Recommended)"
    - "Assume the current architecture and document only the compatible path"
    - "Keep L2-Dev high level and leave detailed design to the engineering team"
    - "Other (please specify)"
  context:
    technical_decision: "[decision needed]"
    existing_architecture: "[known architecture]"
  default: "Consult Atlas or Gateway first"
```

### `L2_DESIGN_SCOPE`

```yaml
INTERACTION_TRIGGER:
  type: L2_DESIGN_SCOPE
  condition: "L2-Design needs visual artifacts such as mockups or wireframes."
  question: "Accord can define flows and design requirements, but not visual deliverables. Should visual work be delegated?"
  options:
    - "Keep flow and requirements in Accord, delegate visuals to Vision or Palette (Recommended)"
    - "Existing design-system references are enough; no visual deliverable is needed"
    - "The design team will produce the artifacts separately"
    - "Other (please specify)"
  context:
    design_needs: "[detected design needs]"
    existing_design_system: "[yes/no]"
  default: "Keep flow and requirements in Accord, delegate visuals to Vision or Palette"
```

### `STAKEHOLDER_EXPANSION`

```yaml
INTERACTION_TRIGGER:
  type: STAKEHOLDER_EXPANSION
  condition: "Stakeholders beyond Biz, Dev, and Design are needed."
  question: "Additional stakeholders were detected. How should the package scope expand?"
  options:
    - "Add extra L2 sections such as L2-Legal or L2-Security (Recommended)"
    - "Describe those requirements inside the existing L2-Biz section"
    - "Move those requirements into a separate formal document via Scribe"
    - "Other (please specify)"
  context:
    additional_stakeholders: "[detected stakeholders]"
    regulatory_requirements: "[requirements]"
  default: "Add extra L2 sections such as L2-Legal or L2-Security"
```

## Detection Heuristics

| Signal | Trigger |
|---|---|
| "how big", "complex", "simple" | `SCOPE_UNCLEAR` |
| "who uses this", "which teams", "stakeholders" | `TEAM_UNKNOWN` |
| long requirement lists or many stories | `REQUIREMENTS_OVERFLOW` |
| "architecture", "database", "technology choice" | `L2_TECH_DEPTH` |
| "UI", "mockup", "screen", "wireframe" | `L2_DESIGN_SCOPE` |
| "legal", "security", "compliance", "PII" | `STAKEHOLDER_EXPANSION` |
