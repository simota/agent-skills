# Unified Specification Template

Purpose: Use this file when writing the canonical cross-functional package with `L0`, `L1`, `L2`, `L3`, and `Meta`.

## Contents

- Structure overview
- Audience reading paths
- Canonical template
- Quality gates
- Glossary pattern

## Structure Overview

```text
L0: Vision
L1: Requirements
L2-Biz: Business Context
L2-Dev: Technical Design
L2-Design: Design Specification
L3: Acceptance Criteria
Meta: Management
```

## Audience Reading Paths

- Business: `L0 -> L1 -> L2-Biz -> L3`
- Development: `L0 -> L1 -> L2-Dev -> L3`
- Design: `L0 -> L1 -> L2-Design -> L3`
- Alignment review: `L0 -> L3`

## Canonical Template

```markdown
# [Project / Feature Name]

## L0: Vision

### Problem (Why)
[Describe the current pain in 1-3 sentences.]

### Target Users (Who)
| Persona | Role | Main pain |
|---|---|---|
| [Name] | [Role] | [Pain] |

### Success Metrics (KPI)
| Metric | Current | Target | Measurement |
|---|---:|---:|---|
| [KPI] | [Current] | [Target] | [Method] |

### Scope
**In**
- [Item]

**Out**
- [Item]

### Timeline
| Milestone | Target date |
|---|---|
| Spec aligned | YYYY-MM-DD |
| Build complete | YYYY-MM-DD |
| Release | YYYY-MM-DD |

## L1: Requirements

### User Stories

#### US-001: [Story title]
**As a** [persona], **I want to** [action], **so that** [value].
**Priority:** Must / Should / Could / Won't
**Linked REQs:** REQ-001, REQ-002

### Functional Requirements

#### REQ-001: [Requirement title]
- **Description:** [detail]
- **Input:** [input]
- **Output:** [expected result]
- **Constraints:** [constraints]
- **Priority:** Must / Should / Could / Won't
- **Linked:** US-001, DESIGN-001, AC-001

### Non-Functional Requirements

| Category | Requirement | Target |
|---|---|---|
| Performance | [Requirement] | [Number] |
| Security | [Requirement] | [Standard] |
| Accessibility | [Requirement] | [WCAG level] |
| Compatibility | [Requirement] | [Browser/device] |

### MoSCoW Priority Matrix
| Priority | Requirements | Reason |
|---|---|---|
| Must | REQ-001 | [Reason] |
| Should | REQ-002 | [Reason] |
| Could | REQ-003 | [Reason] |
| Won't | REQ-004 | [Reason] |

## L2-Biz: Business Context

- Market opportunity
- Competitive context
- Business impact
- Risks and dependencies
- Stakeholders
- Go-to-market

## L2-Dev: Technical Design

- Architecture overview
- API design
- Data model
- Constraints and trade-offs
- Dependencies
- Migration plan when relevant

## L2-Design: Design Specification

Accord defines flow, interaction, and accessibility requirements only.
Visual artifacts belong to Vision or Palette.

- User flows
- Interaction patterns
- Component usage
- Accessibility requirements
- Responsive behavior

## L3: Acceptance Criteria

### BDD Scenarios

#### AC-001: [Scenario title] — Linked: REQ-001
**Given** [precondition]
**When** [action or event]
**Then** [expected result]

#### AC-002: [Scenario title] — Linked: REQ-001
**Given** [precondition]
**And** [additional precondition]
**When** [action or event]
**Then** [expected result]
**And** [additional expected result]

#### AC-003: [Edge case] — Linked: REQ-002
**Given** [abnormal precondition]
**When** [abnormal action]
**Then** [error handling]

### Edge Case List
| Case | Input | Expected behavior | Linked REQ |
|---|---|---|---|
| [Case] | [Input] | [Behavior] | REQ-XXX |

### Traceability Matrix
| REQ | User Story | Design | BDD Scenario | Test |
|---|---|---|---|---|
| REQ-001 | US-001 | DESIGN-001 | AC-001, AC-002 | - |

## Meta: Management

### Document Metadata
| Field | Value |
|---|---|
| Status | Draft / Review / Approved / Deprecated |
| Version | v0.1 |
| Created | YYYY-MM-DD |
| Last updated | YYYY-MM-DD |
| Author | [Name] |

### Version History
| Version | Date | Change | Author |
|---|---|---|---|
| v0.1 | YYYY-MM-DD | Initial draft | [Name] |

### Review And Approval
| Team | Reviewer | Status | Date |
|---|---|---|---|
| Business | [Name] | Pending / Approved / Rejected | - |
| Development | [Name] | Pending / Approved / Rejected | - |
| Design | [Name] | Pending / Approved / Rejected | - |

### Open Questions
| ID | Question | Owner | Status |
|---|---|---|---|
| Q1 | [Question] | [Owner] | Open / Resolved |
```

## Quality Gates

### `L0`

- problem is concrete
- personas feel real
- KPI is measurable
- `Out` is explicit
- one-page limit is respected

### `L1`

- every story includes value
- every `REQ` has a unique ID
- every `REQ` has priority
- non-functional requirements use measurable targets
- MoSCoW is explicit

### `L3`

- every `REQ` has at least one linked `AC`
- happy path and edge cases both exist
- `Given/When/Then` uses concrete, testable outcomes
- traceability matrix is not empty
- all three teams can understand the scenarios

## Glossary Pattern

Use a glossary when one concept is named differently by each team.

```markdown
## Glossary
| Term | Business meaning | Development meaning | Design meaning |
|---|---|---|---|
| [Term] | [Definition] | [Definition] | [Definition] |
```
