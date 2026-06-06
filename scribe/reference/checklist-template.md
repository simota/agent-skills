# Checklist Templates

Purpose: Use this file for implementation readiness, review gates, and compact delivery checklists.

Contents:

- implementation checklist
- review checklist
- quick checklist
- checklist writing guidance

## Implementation Checklist Template

```markdown
# Implementation Checklist: [Feature Name]

## Document Info
| Field | Value |
|-------|-------|
| Version | v0.1 |
| Status | Draft |
| Related Design | `HLD/LLD-[name]` |
| Related Requirements | `REQ/FR` links |

## Pre-Implementation
### Requirements Verification
- [ ] Requirements and acceptance criteria approved
- [ ] Scope and non-goals confirmed
- [ ] Open questions resolved or tracked

### Design Verification
- [ ] HLD/LLD available
- [ ] Interfaces and data contracts stable
- [ ] Risks and rollback reviewed

### Environment Setup
- [ ] Required env vars and secrets available
- [ ] Local/test environment documented
- [ ] Dependencies installed

## Implementation Phase
### Core Implementation
- [ ] `IMPL-001`: [deliverable] -> reference `REQ-001`
- [ ] `IMPL-002`: [deliverable] -> reference `FR-002`

### Data Layer
- [ ] Schema or migration work complete
- [ ] Data validation and error paths covered

### API Layer
- [ ] Contracts implemented
- [ ] Error codes and status handling aligned with SRS

### Business Logic
- [ ] Main decision paths implemented
- [ ] Edge cases covered

### UI Layer (if applicable)
- [ ] States and accessibility handled

## Quality Assurance
- [ ] Unit tests added or updated
- [ ] Integration tests added or updated
- [ ] Logging and observability verified
- [ ] Security review complete

## Before Handoff / PR
- [ ] Traceability updated
- [ ] Docs updated if needed
- [ ] Known risks recorded
- [ ] Next handoff identified

## Notes
- [note]

## Follow-up Items
- [TODO]
```

## Review Checklist Template

```markdown
# Code Review Checklist: [PR/MR Title]

## Review Info
| Field | Value |
|-------|-------|
| Reviewer | [name] |
| Related Requirements | [list] |
| Related Design | [link] |

## Functional Review
- [ ] Requirements compliance
- [ ] Business logic correctness

## Code Quality Review
- [ ] Readability
- [ ] Structure
- [ ] Consistency

## Technical Review
- [ ] Architecture alignment
- [ ] Error handling
- [ ] Performance
- [ ] Security

## Testing Review
- [ ] Coverage is adequate
- [ ] Tests are readable and stable

## Documentation Review
- [ ] Specs and checklists remain accurate

## Review Result
### Status
- [ ] Approved
- [ ] Changes requested

### Summary
[summary]

### Comments
- [comment]

## Sign-off
- [sign-off details]
```

## Quick Checklist (Minimal)

```markdown
# Quick Implementation Checklist: [Feature]

## Before Coding
- [ ] Requirements understood
- [ ] Scope confirmed

## Implementation
- [ ] Main behavior implemented
- [ ] Edge cases covered

## Before PR
- [ ] Tests updated
- [ ] Docs updated if needed
- [ ] Risks noted
```

## Checklist Quality Guidelines

Good checklist items:

- concrete deliverable
- traceable ID
- observable completion state

Avoid:

- vague verbs such as "handle" or "support" without a concrete result
- items with no owner or reference
- items that duplicate requirements instead of decomposing them
