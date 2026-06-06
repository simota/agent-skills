# Documentation Directory Structure

Purpose: Use this reference when a repository needs a structured `docs/` tree aligned with Scribe outputs and review workflows.

## Contents

- Complete `docs/` structure
- Required document categories
- Lifecycle rules
- Naming conventions

Detailed docs/ directory layout aligned with Scribe agent output format.

---

## Complete docs/ Structure

```
docs/
├── prd/                        # Product Requirements Documents
│   └── PRD-{feature-name}.md   #   Business/functional requirements
├── specs/                      # Software Requirements Specifications
│   └── SRS-{feature-name}.md   #   Technical specifications
├── design/                     # Design Documents
│   ├── HLD-{feature-name}.md   #   High-Level Design (architecture)
│   └── LLD-{feature-name}.md   #   Low-Level Design (detailed)
├── checklists/                 # Checklists
│   ├── IMPL-{feature-name}.md  #   Implementation checklists
│   └── REVIEW-{category}.md    #   Review checklists
├── test-specs/                 # Test Specifications
│   └── TEST-{feature-name}.md  #   Test cases and expected results
├── adr/                        # Architecture Decision Records
│   └── ADR-{NNN}-{title}.md    #   Numbered decision records
├── guides/                     # Developer Guides
│   ├── getting-started.md      #   Onboarding guide
│   ├── contributing.md         #   Contribution guidelines
│   └── deployment.md           #   Deployment procedures
├── api/                        # API Documentation
│   ├── openapi.yaml            #   OpenAPI specification
│   └── README.md               #   API overview
└── diagrams/                   # Visual Diagrams
    ├── architecture.mermaid    #   System architecture
    ├── er-diagram.mermaid      #   Entity relationship
    └── sequence/               #   Sequence diagrams
```

---

## Subdirectory Details

### prd/ — Product Requirements Documents

**Owner:** Scribe
**Naming:** `PRD-{feature-name}.md`
**Purpose:** Define business requirements and functional requirements

```markdown
# PRD: {Feature Name}

## Overview
## Background & Motivation
## User Stories
## Functional Requirements (REQ-001, REQ-002, ...)
## Non-Functional Requirements
## Acceptance Criteria (AC-001, ...)
## Out of Scope
## Dependencies
## Timeline
## Change History
```

**When to create:**
- New feature development
- Major feature enhancement
- Business requirement changes

---

### specs/ — Software Requirements Specifications

**Owner:** Scribe
**Naming:** `SRS-{feature-name}.md`
**Purpose:** Define technical requirements and detailed specifications

```markdown
# SRS: {Feature Name}

## System Overview
## Technical Requirements (TREQ-001, ...)
## Data Models
## API Contracts
## Security Requirements
## Performance Requirements
## Constraints & Assumptions
## Traceability Matrix (REQ → TREQ → TC)
## Change History
```

**When to create:**
- Complex technical features
- Features requiring specific technical constraints
- System integration features

---

### design/ — Design Documents

**Owner:** Scribe (HLD/LLD), Atlas (ADR-referenced architecture)
**Naming:** `HLD-{feature-name}.md`, `LLD-{feature-name}.md`

#### HLD (High-Level Design)

```markdown
# HLD: {Feature Name}

## Architecture Overview
## Component Diagram
## Data Flow
## Technology Choices
## Security Design
## Scalability Considerations
## Integration Points
## Deployment Strategy
## Change History
```

#### LLD (Low-Level Design / Detailed Design)

```markdown
# LLD: {Feature Name}

## Module Design
## Class/Interface Design
## Database Schema Changes
## API Endpoint Design
## Error Handling Strategy
## Logging Strategy
## Configuration Design
## Migration Plan
## Change History
```

**When to create:**
- HLD: Every new system/feature with architectural impact
- LLD: Complex features requiring detailed implementation guide

---

### checklists/ — Implementation & Review Checklists

**Owner:** Scribe
**Naming:** `IMPL-{feature-name}.md`, `REVIEW-{category}.md`

#### Implementation Checklist

```markdown
# Implementation Checklist: {Feature Name}

## Prerequisites
- [ ] Design document approved (HLD/LLD)
- [ ] Dependencies available

## Implementation Tasks
- [ ] **IMPL-001**: {Task description}
  - Input: {input spec}
  - Output: {output spec}
  - Reference: REQ-{NNN}

## Integration Tasks
- [ ] API integration verified
- [ ] Database migration tested

## Quality Gates
- [ ] Unit tests pass (>80% coverage)
- [ ] Integration tests pass
- [ ] Code review approved
- [ ] Documentation updated

## Status
| Item | Status | Assignee | Notes |
|------|--------|----------|-------|
```

#### Review Checklist

```markdown
# Review Checklist: {Category}

## Code Quality
- [ ] Naming conventions followed
- [ ] No magic numbers
- [ ] Error handling complete

## Security
- [ ] Input validation
- [ ] No hardcoded secrets
- [ ] OWASP compliance

## Performance
- [ ] No N+1 queries
- [ ] Appropriate indexing
- [ ] Caching considered
```

---

### test-specs/ — Test Specifications

**Owner:** Scribe
**Naming:** `TEST-{feature-name}.md`

```markdown
# Test Specification: {Feature Name}

## Test Scope
## Test Environment

## Test Cases
### Unit Tests
| ID | Description | Input | Expected | Priority |
|----|-------------|-------|----------|----------|
| TC-001 | ... | ... | ... | High |

### Integration Tests
| ID | Description | Precondition | Steps | Expected |
|----|-------------|-------------|-------|----------|

### Edge Cases
| ID | Description | Input | Expected |
|----|-------------|-------|----------|

## Test Data
## Acceptance Criteria Cross-Reference
| AC | Test Cases | Status |
|----|-----------|--------|
```

---

### adr/ — Architecture Decision Records

**Owner:** Atlas
**Naming:** `ADR-{NNN}-{title}.md` (zero-padded 3-digit number)

```markdown
# ADR-{NNN}: {Decision Title}

## Status
[Proposed | Accepted | Deprecated | Superseded by ADR-XXX]

## Context
## Decision
## Consequences
## Alternatives Considered
## Date: YYYY-MM-DD
```

---

### guides/ — Developer Guides

**Owner:** Quill
**Recommended files:**

| File | Purpose | Audience |
|------|---------|----------|
| `getting-started.md` | Development environment setup | New developers |
| `contributing.md` | Contribution guidelines | All developers |
| `deployment.md` | Deployment procedures | DevOps / Developers |
| `architecture.md` | Architecture overview | Senior developers |
| `troubleshooting.md` | Common issues and solutions | All developers |

---

### api/ — API Documentation

**Owner:** Gateway
**Contents:**

- `openapi.yaml` — OpenAPI 3.x specification
- `README.md` — API overview, authentication, rate limits
- `examples/` — Request/response examples (optional)

---

### diagrams/ — Visual Diagrams

**Owner:** Canvas
**Formats:** Mermaid (`.mermaid`), draw.io (`.drawio`), PlantUML (`.puml`)

| Diagram Type | File | Purpose |
|-------------|------|---------|
| Architecture | `architecture.mermaid` | System-level view |
| ER Diagram | `er-diagram.mermaid` | Database relationships |
| Sequence | `sequence/{flow}.mermaid` | Interaction flows |
| State Machine | `state/{entity}.mermaid` | State transitions |
| Class Diagram | `class/{module}.mermaid` | Module structure |

---

## Document Lifecycle

```
1. PLAN     → PRD created (Scribe)
2. SPEC     → SRS created (Scribe), ADR recorded (Atlas)
3. DESIGN   → HLD/LLD created (Scribe), diagrams added (Canvas)
4. PREPARE  → Implementation checklist created (Scribe)
5. BUILD    → Checklist tracked during development
6. TEST     → Test spec created (Scribe), executed (Radar/Voyager)
7. REVIEW   → Review checklist applied (Scribe → Judge)
8. RELEASE  → Guides updated (Quill), API docs updated (Gateway)
```

---

## Naming Conventions

| Category | Pattern | Example |
|----------|---------|---------|
| PRD | `PRD-{feature}.md` | `PRD-user-auth.md` |
| SRS | `SRS-{feature}.md` | `SRS-user-auth.md` |
| HLD | `HLD-{feature}.md` | `HLD-payment-system.md` |
| LLD | `LLD-{feature}.md` | `LLD-payment-gateway.md` |
| Implementation | `IMPL-{feature}.md` | `IMPL-user-auth.md` |
| Review | `REVIEW-{category}.md` | `REVIEW-security.md` |
| Test Spec | `TEST-{feature}.md` | `TEST-user-auth.md` |
| ADR | `ADR-{NNN}-{title}.md` | `ADR-001-use-postgresql.md` |

**Rules:**
- Use kebab-case for feature names
- ADR numbers are zero-padded to 3 digits
- Keep names concise but descriptive
- One document per feature per type
