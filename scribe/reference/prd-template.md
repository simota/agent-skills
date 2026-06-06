# PRD (Product Requirements Document) Template

Purpose: Use this file for business-facing requirements, user value, goals, non-goals, and testable acceptance criteria.

Contents:

- full PRD template
- quick PRD template
- PRD quality checklist
- Spec-Driven Development (SDD) adapter

## 2026 Framing — PRD as the Source of Implementation

By 2026 the industry framing of a PRD has shifted: it is no longer just a hand-off to engineering, it is **the source document an AI coding agent reads to generate the implementation**. The PRD must be self-contained enough that an agent (Claude Code, Cursor, Copilot, Codex CLI, Gemini CLI, Antigravity, etc.) can act on it without prompting the author for clarifications.

Three implications for every PRD authored in 2026:

1. **Write the WHAT and the WHY; do not write the HOW.** Implementation detail belongs in HLD / design docs (`Scribe design-template.md`). When a PRD prescribes the tech stack, the agent inherits the prescription and skips the actual design — and the design rationale is then never recorded.
2. **Acceptance Criteria are the contract the agent will pattern-match against.** Each `AC-NNN` must be Given/When/Then with observable system state; "users feel good" cannot be tested by an agent and will be silently downgraded into vague assertions in code.
3. **Pair the PRD with a project constitution file** (`CLAUDE.md`, `AGENTS.md`, or both — the agent stack determines which). The constitution captures testing conventions, coding standards, non-negotiable policies; the PRD captures *this feature*. Without the constitution, every PRD redundantly re-states org-wide rules.

The Spec-Driven Development ecosystem (GitHub **Spec-Kit** with `~29` agent integrations, AWS **Kiro**, **cc-sdd**, **BMAD**, **Tessl**, **OpenSpec**, Google **Antigravity**) has converged on this PRD → constitution → tasks pipeline; the template below is compatible with all of them.

## Template

```markdown
# PRD: [Feature Name]

## Document Info
| Field | Value |
|-------|-------|
| Version | v0.1 |
| Status | Draft |
| Author | [name] |
| Reviewers | [PM, Tech Lead, QA] |
| Audience | PM, Dev, QA |
| Related Docs | [links] |

## Change History
| Date | Version | Author | Change |
|------|---------|--------|--------|
| YYYY-MM-DD | v0.1 | [name] | Initial draft |

## 1. Overview
### 1.1 Purpose
[Why this document exists]

### 1.2 Background
[Business context, problem, timing]

### 1.3 Goals
- [Goal 1]
- [Goal 2]

### 1.4 Non-Goals (Out of Scope)
- [Non-goal 1]
- [Non-goal 2]

### 1.5 Success Metrics
| Metric | Target | Measurement |
|--------|--------|-------------|
| Activation rate | +15% | product analytics |
| Completion rate | >= 70% | funnel report |

## 2. User Stories
### 2.1 Target Users
- Persona: [who]
- Context: [when and why]

### 2.2 User Stories
As a [user]
I want [goal]
So that [benefit]

## 3. Functional Requirements
### 3.1 [Feature Area]
**REQ-001**: [Requirement title]
- Description: [what must happen]
- Priority: Must / Should / Could
- Trigger: [action or event]
- Output: [observable result]
- Dependencies: [REQ-XXX or external dependency]
- Acceptance Criteria: `AC-001`

**REQ-002**: [Requirement title]
- Description: ...
- Acceptance Criteria: `AC-002`

## 4. Non-Functional Requirements
### 4.1 Performance
**NFR-001**: Response time
- p95 latency: [target]

### 4.2 Security
**NFR-002**: Authentication
- JWT token expiry: `24 hours`

### 4.3 Scalability
**NFR-003**: Load capacity
- [concurrency / throughput target]

### 4.4 Availability
**NFR-004**: Uptime
- [availability target]

### 4.5 Accessibility
**NFR-005**: WCAG compliance
- [target level]

## 5. Acceptance Criteria
**AC-001**: [Criterion for `REQ-001`]
Given [precondition]
When [action]
Then [result]
And [additional check]

**AC-002**: [Criterion for `REQ-002`]
Given ...
When ...
Then ...

## 6. Edge Cases & Error Handling
- [edge case]
- [failure mode]
- [fallback]

## 7. UI/UX Requirements
### 7.1 Wireframes
[link or note]

### 7.2 UI Specifications
- states
- accessibility needs
- copy constraints

### 7.3 Interaction Flow
[step sequence]

## 8. Technical Constraints
### 8.1 Technology Stack
- [relevant constraints only]

### 8.2 Integration Points
- [system or API]

### 8.3 Data Requirements
- [storage, retention, privacy, migration]

## 9. Dependencies
### 9.1 Internal Dependencies
- [team or component]

### 9.2 External Dependencies
- [vendor, SDK, contract]

## 10. Risks & Mitigations
| Risk | Impact | Mitigation |
|------|--------|------------|
| [risk] | [level] | [action] |

## 11. Timeline
| Milestone | Date | Owner |
|-----------|------|-------|
| Draft approved | YYYY-MM-DD | [owner] |

## 12. Open Questions
- [question]

## 13. Appendix
### 13.1 Glossary
- [term]

### 13.2 References
- [doc link]

### 13.3 Traceability Matrix
| Requirement | Design | Test | Code / Doc Target |
|-------------|--------|------|-------------------|
| `REQ-001` | `HLD-3.1` | `TC-001` | `auth.service.ts` |
```

## Quick Template (Minimal)

```markdown
# PRD: [Feature Name]

## Overview
[problem, user, value]

## User Story
As a [user], I want [goal], so that [benefit].

## Requirements
| ID | Description | Priority | Acceptance Criteria |
|----|-------------|----------|---------------------|
| `REQ-001` | [Description] | Must | [Criteria] |
| `REQ-002` | [Description] | Should | [Criteria] |

## Edge Cases
- [edge case]

## Out of Scope
- [non-goal]

## Open Questions
- [question]
```

## PRD Quality Checklist

- [ ] All requirements have IDs (`REQ-XXX`)
- [ ] Every requirement maps to acceptance criteria
- [ ] `Non-Goals` is present
- [ ] Success metrics are measurable
- [ ] PRD explains `What` and `Why`, not implementation `How`
- [ ] Edge cases and dependencies are explicit
- [ ] Traceability matrix exists when downstream design or tests are expected

### SDD-Specific Checklist (when handing off to an AI coding agent)

- [ ] Every Acceptance Criterion uses Given/When/Then with **observable** system state — no "feels right"
- [ ] No specific tech stack named unless it is a hard external constraint (mark such constraints `CONSTRAINT-NNN`, not `REQ-NNN`)
- [ ] Repo has an up-to-date `CLAUDE.md` / `AGENTS.md` constitution covering testing conventions, file structure, and non-negotiable policies — the PRD links to it instead of restating
- [ ] If the codebase already ships a Spec-Kit-style harness (`/specify`, `/plan`, `/tasks`), the PRD lives where that harness expects it (`docs/specs/<slug>/spec.md` is the de-facto location across Spec-Kit, cc-sdd, Kiro)
- [ ] The PRD names which **agent persona** will act on it (`Builder` / `Artisan` / `Native` / `Forge`) so the constitution and acceptance bar can be picked correctly

## Spec-Driven Development (SDD) Adapter

When the PRD is consumed by an AI coding agent, structure it so the agent's `/plan` step can run against it without re-asking the author. The mapping from this template to the Spec-Kit / cc-sdd flow:

| Spec-Kit phase | Source in this template |
|----------------|-------------------------|
| `/specify` (intent) | Section 1 Overview + Section 2 User Stories + Section 1.4 Non-Goals |
| `/plan` (design + constraints) | Section 4 NFR + Section 8 Technical Constraints + Section 9 Dependencies — *plus* the project constitution file |
| `/tasks` (atomic implementation steps) | Section 3 Functional Requirements (1 task per `REQ-NNN`) with Section 5 Acceptance Criteria as the test contract |
| `/implement` (agent execution) | Agent reads the artefacts above; PR-as-safety-gate stays in effect (see `mend/reference/safety-model.md`) |

If the SDD harness already provides a `spec.md` schema (Spec-Kit / OpenSpec), prefer that schema and use this template only as a checklist of fields not to forget. Do not maintain two PRD shapes in the same repo.
