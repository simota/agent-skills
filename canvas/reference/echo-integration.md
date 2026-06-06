# Canvas Echo Integration Reference

Purpose: Read this when Echo provides journey, friction, persona, team, or DX data that must be turned into a visual artifact.

## Contents

- Visualization types
- Handoff schema
- Templates
- Score colors
- Output variants

## Visualization Types

| Echo Data | Canvas Output | Use When |
|-----------|---------------|----------|
| User Journey | Journey Map | Show step-by-step experience |
| Emotion Scores | Friction Heatmap | Highlight pain points |
| Cross-Persona Data | Comparison Matrix / Chart | Compare segments |
| Internal Persona | Profile Card | Visualize team members or stakeholders |
| Workflow Context | Workflow Diagram | Show process context |
| Team Structure | Organization Chart / Collaboration Map | Show roles and links |
| DX Journey | Developer Journey | Visualize engineering workflow pain |

## Standard Handoff Blocks

### Journey Data

```markdown
## Echo -> Canvas Journey Visualization

**Flow**: Checkout
**Persona**: First-Time Buyer
**Average Score**: -0.6

**Journey Data**:
| Step | Action | Score | Friction Type |
|------|--------|-------|---------------|
| 1 | Open cart | +2 | None |
| 2 | Enter address | -2 | Cognitive Overload |
| 3 | Submit payment | -3 | Error Handling |
```

### Cross-Persona Data

```markdown
## Echo -> Canvas Cross-Persona Visualization

**Flow**: Checkout
**Personas**: Newbie, Power, Mobile, Senior

**Comparison Matrix**:
| Step | Newbie | Power | Mobile | Senior | Issue Type |
|------|--------|-------|--------|--------|------------|
| 1 | +1 | +2 | +1 | +1 | Non-Issue |
| 2 | -2 | +1 | -2 | -3 | Segment |
```

### Internal Persona Data

```markdown
## Echo -> Canvas Internal Persona Visualization

**Persona Type**: Internal
**Category**: developer
**Role**: Frontend Developer
```

### Team Structure Data

```markdown
## Echo -> Canvas Team Structure Visualization

**Organization**: Product Team
**Scope**: Department
```

## Templates

### Journey Map

```mermaid
journey
    title Checkout Flow - First-Time Buyer
    section Cart
      View cart: 4: User
    section Address
      Enter address: 2: User
    section Payment
      Submit payment: 1: User
    section Confirmation
      See success: 5: User
```

### Friction Heatmap

```mermaid
flowchart TD
    classDef positive fill:#d5e8d4,stroke:#82b366
    classDef neutral fill:#fff2cc,stroke:#d6b656
    classDef negative fill:#f8cecc,stroke:#b85450
    classDef critical fill:#ff0000,stroke:#b85450,color:#ffffff

    A[Step 1 +2]:::positive --> B[Step 2 -1]:::neutral
    B --> C[Step 3 -2]:::negative
    C --> D[Step 4 -3]:::critical
```

### Cross-Persona Chart

```mermaid
xychart-beta
    title "Cross-Persona Emotion Scores"
    x-axis [Step1, Step2, Step3]
    y-axis "Score" -3 --> 3
    line [2, -1, -3] "Newbie"
    line [3, 2, -2] "Power"
    line [2, -2, -3] "Mobile"
```

### Internal Persona Card

```text
+------------------------------+
| Frontend Developer           |
| Team: Platform               |
| Experience: 3-5 years        |
| Tools: VS Code, DevTools     |
+------------------------------+
```

### Team Structure

```mermaid
flowchart TD
    PM[Product Manager] --> FE1[Frontend Developer]
    PM --> FE2[Frontend Developer]
    PM --> BE[Backend Developer]
    PM --> QA[QA Engineer]
```

## Score Colors

| Score | Meaning | Color |
|-------|---------|-------|
| `+3`, `+2` | Strongly positive | Green |
| `+1`, `0` | Neutral / mild positive | Yellow |
| `-1` | Warning | Orange |
| `-2` | Negative | Red |
| `-3` | Critical friction | Dark red |

## Visual Journey From Navigator

## ECHO_TO_CANVAS_VISUAL_HANDOFF

```markdown
**Visualization Type**: Visual Journey Map | Friction Heatmap | Before/After
**Flow**: Signup
**Persona**: Skeptic
**Screenshots**:
- step1.png
- step2.png
**Key Friction**:
- Initial scan misses CTA
- Error feedback is too subtle
```

## Output Variants

- `## Canvas Journey Map`
- `## Canvas Internal Persona Profile`
- `## Canvas Team Structure`
- `## Canvas Visual Journey Map`

Use the variant that matches the visualization type exactly.
