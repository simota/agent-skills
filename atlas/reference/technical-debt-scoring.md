# Technical Debt Scoring

## Severity Matrix

| Impact | Effort: Low | Effort: Medium | Effort: High |
|--------|------------|----------------|-------------|
| High | P0: Fix now | P1: Next sprint | P2: Plan |
| Medium | P1: Next sprint | P2: Plan | P3: Backlog |
| Low | P2: Plan | P3: Backlog | P4: Accept |

## Debt Categories

| Category | Examples | Typical Impact |
|----------|----------|----------------|
| **Design Debt** | God classes, tight coupling, missing abstractions | High - affects changeability |
| **Code Debt** | Duplicated code, complex functions, poor naming | Medium - affects readability |
| **Architecture Debt** | Coupling, missing abstractions, layer violations | High - affects scalability |
| **Test Debt** | Missing tests, flaky tests, low coverage | High - affects reliability |
| **Documentation Debt** | Missing docs, outdated docs, unclear APIs | Medium - affects onboarding |
| **Infrastructure Debt** | Outdated dependencies, manual deployments | Medium - affects operations |
| **Dependency Debt** | Outdated packages, CVEs | Medium - affects security |

## Quantification

- Story points estimate for remediation
- Impact score (1-5) on development velocity
- Risk score (1-5) for production incidents

---

## Priority Scoring Matrix

```markdown
## Technical Debt Item: [Name]

### Impact Score (1-5)
- Code touchpoints: [how many files/functions affected]
- Developer friction: [how often developers encounter this]
- Bug correlation: [how many bugs related to this area]
- **Impact Score**: [1-5]

### Fix Cost Score (1-5)
- Estimated effort: [hours/days]
- Risk of regression: [low/medium/high]
- Dependencies: [what else needs to change]
- **Cost Score**: [1-5]

### Priority = Impact × (6 - Cost)

| Debt Item | Impact | Cost | Priority |
|-----------|--------|------|----------|
| God class UserService | 5 | 3 | 15 |
| Missing API validation | 4 | 2 | 16 |
| Duplicated auth logic | 3 | 2 | 12 |
| Outdated React version | 4 | 4 | 8 |
```

## Debt Inventory Template

```markdown
# Technical Debt Inventory

## Summary
- Total items: [count]
- High priority: [count]
- Estimated total effort: [days/weeks]

## High Priority (Address this quarter)

### TD-001: UserService God Class
- **Category**: Design Debt
- **Location**: `src/services/UserService.ts` (2,500 lines)
- **Impact**: 5 - Core service, touched by 80% of features
- **Cost**: 3 - Moderate effort, well-tested
- **Priority**: 15
- **Proposed Fix**: Split into UserAuthService, UserProfileService, UserPreferencesService
- **Dependencies**: None
- **Owner**: [assignee]

### TD-002: Missing Input Validation
- **Category**: Code Debt
- ...

## Medium Priority (Address this half)

### TD-003: ...

## Low Priority (Backlog)

### TD-004: ...
```

## Repayment Plan Template

```markdown
# Technical Debt Repayment Plan: Q1 2025

## Budget
- Allocated time: 20% of sprint capacity
- Estimated capacity: 40 story points

## Goals
1. Reduce high-priority debt items by 50%
2. Improve test coverage from 60% to 75%
3. Eliminate all circular dependencies

## Sprint Allocation

### Sprint 1
- [ ] TD-001: UserService split (Phase 1) - 8 points
- [ ] TD-005: Add missing API tests - 5 points

### Sprint 2
- [ ] TD-001: UserService split (Phase 2) - 8 points
- [ ] TD-002: Input validation - 5 points

### Sprint 3
- [ ] TD-001: UserService split (Phase 3) - 5 points
- [ ] TD-003: Fix circular deps - 8 points

## Success Metrics
- [ ] No God classes > 500 lines
- [ ] Zero circular dependencies
- [ ] All API endpoints validated
- [ ] Test coverage > 75%
```

## ROI Calculation Guide

```markdown
## ROI Analysis: [Debt Item]

### Current Cost (per month)
- Bug fixes in this area: [hours] × [hourly rate] = $[amount]
- Extra development time: [hours] × [hourly rate] = $[amount]
- Onboarding overhead: [hours] × [hourly rate] = $[amount]
- **Total monthly cost**: $[amount]

### Fix Cost (one-time)
- Development effort: [hours] × [hourly rate] = $[amount]
- Testing effort: [hours] × [hourly rate] = $[amount]
- Review/deployment: [hours] × [hourly rate] = $[amount]
- **Total fix cost**: $[amount]

### ROI Calculation
- Break-even point: [fix cost] / [monthly savings] = [months]
- 12-month ROI: ([monthly savings × 12] - [fix cost]) / [fix cost] × 100 = [%]

### Recommendation
[Fix / Defer / Accept]
- Rationale: [explanation]
```
