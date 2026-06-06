# ADR/RFC Templates

## Template Selection Guide

| Situation | Template | When to Use |
|-----------|----------|-------------|
| Major architectural decision | Full ADR | New patterns, breaking changes, technology choices |
| Significant cross-team change | RFC | Needs stakeholder input, migration planning |
| Small/reversible decision | Lightweight DR | Quick records for minor but notable decisions |

---

## ADR Template (Architecture Decision Record)

```markdown
# ADR-XXXX: [Decision Title]

## Status

[Proposed | Accepted | Deprecated | Superseded by ADR-YYYY]

## Context

What is the issue that we're seeing that is motivating this decision or change?

- Current situation: [describe the problem]
- Pain points: [list specific issues]
- Constraints: [technical/business constraints]

## Decision

What is the change that we're proposing and/or doing?

- We will [specific decision]
- This means [implications]

## Alternatives Considered

### Option 1: [Name]
- **Pros**: [advantages]
- **Cons**: [disadvantages]
- **Why rejected**: [reason]

### Option 2: [Name]
- **Pros**: [advantages]
- **Cons**: [disadvantages]
- **Why rejected**: [reason]

## Consequences

What becomes easier or more difficult to do because of this change?

### Positive
- [benefit 1]
- [benefit 2]

### Negative
- [drawback 1]
- [drawback 2]

### Neutral
- [side effect 1]

## Implementation Plan

1. [Step 1]
2. [Step 2]
3. [Step 3]

## References

- [Link to related documentation]
- [Link to discussion]
```

---

## RFC Template (Request for Comments)

```markdown
# RFC: [Proposal Title]

## Summary

One paragraph explanation of the proposal.

## Motivation

Why are we doing this? What problem does it solve?

- **Pain Point**: [specific problem]
- **Impact**: [who is affected and how]
- **Urgency**: [why now]

## Detailed Design

### Current State

```
[diagram or description of current architecture]
```

### Proposed State

```
[diagram or description of proposed architecture]
```

### Key Changes

1. **[Change 1]**: [description]
2. **[Change 2]**: [description]

## Migration Strategy

### Phase 1: Preparation
- [ ] [task 1]
- [ ] [task 2]

### Phase 2: Implementation
- [ ] [task 1]
- [ ] [task 2]

### Phase 3: Cleanup
- [ ] [task 1]
- [ ] [task 2]

### Rollback Plan

If issues arise, we can rollback by:
1. [step 1]
2. [step 2]

## Trade-offs

| Aspect | Before | After |
|--------|--------|-------|
| Complexity | [level] | [level] |
| Performance | [level] | [level] |
| Maintainability | [level] | [level] |

## Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| [risk 1] | Low/Med/High | Low/Med/High | [mitigation] |

## Open Questions

- [ ] [question 1]
- [ ] [question 2]

## Timeline

- Week 1: [milestone]
- Week 2: [milestone]
- Week 3: [milestone]
```

---

## Lightweight Decision Record

```markdown
# Decision: [Title]

**Date**: YYYY-MM-DD
**Status**: Accepted
**Deciders**: [names]

## Context
[1-2 sentences about the situation]

## Decision
[1-2 sentences about what we decided]

## Rationale
[1-2 sentences about why]

## Consequences
- [consequence 1]
- [consequence 2]
```

---

## ADR Status Management

### Directory Structure

```
docs/
└── architecture/
    └── decisions/
        ├── README.md           # Index of all ADRs
        ├── 0001-use-typescript.md
        ├── 0002-state-management.md
        ├── 0003-api-structure.md
        └── template.md
```

### Index Template

```markdown
<!-- docs/architecture/decisions/README.md -->
# Architecture Decision Records

| ID | Title | Status | Date |
|----|-------|--------|------|
| [ADR-0001](0001-use-typescript.md) | Use TypeScript | Accepted | 2024-01-15 |
| [ADR-0002](0002-state-management.md) | Use Zustand for state | Accepted | 2024-02-01 |
| [ADR-0003](0003-api-structure.md) | REST API structure | Superseded by ADR-0005 | 2024-02-15 |

## Status Definitions

- **Proposed**: Under discussion, not yet decided
- **Accepted**: Decision made and in effect
- **Deprecated**: No longer relevant but kept for history
- **Superseded**: Replaced by a newer ADR
```
