# Guardian Output Templates

Purpose: Provide the canonical report headings and minimal skeletons Guardian should use for change, PR, risk, branch, squash, and release outputs.

## Contents

- Change analysis
- PR quality score
- Commit message analysis
- Risk assessment
- Hotspot analysis
- Reviewer recommendations
- Branch health
- Pre-merge checklist
- Repository pattern analysis
- Commit split plan
- Squash optimization report
- PR split strategy
- PR description templates
- Monorepo split
- Release notes
- MEGA PR split plan
- AI-generated code notes

## Section 1: Change Analysis Report

```markdown
## Guardian Change Analysis

**Branch:** `feature/example` -> `main`
**Changes:** 47 files, +1234/-567 lines

### Signal/Noise Breakdown
- Essential: ...
- Supporting: ...
- Incidental: ...

### Essential Changes (Review Priority: HIGH)
| File | Change Type | Summary |
|------|-------------|---------|

### Supporting Changes
- tests, types, docs, or config that reinforce essential work

### Noise (Consider Separating)
- formatting-only files
- import reorder
- generated files
```

## Section 2: PR Quality Score Report

```markdown
## PR Quality Score: {total}/100 ({grade})

### Component Breakdown
- Size: ...
- Focus: ...
- Commits: ...
- Tests: ...
- Documentation: ...
- Risk: ...

### Grade: {grade}

### Improvement Suggestions
1. ...
```

## Section 3: Commit Message Analysis Report

```markdown
## Commit Message Analysis

### Message Quality Scores
- commit 1: ...
- commit 2: ...

### Average Score: {avg}/100

### Message Quality Patterns
- vague subject
- missing scope
- WIP noise
```

## Section 4: Risk Assessment Report

```markdown
## Change Risk Assessment

### Risk Breakdown
- File sensitivity: ...
- Complexity: ...
- Hotspot overlap: ...
- Dependency impact: ...
- Coverage: ...
- Familiarity: ...
- Ripple impact: ...

### High-Risk Files
- `...`

### Risk Mitigation Recommendations
1. ...

### Regression Risk
- predicted regression risk: ...
```

## Section 5: Hotspot Detection Report

```markdown
## Hotspot Analysis

### Top Hotspots
| File | Type | Evidence | Recommendation |
|------|------|----------|----------------|

### Current PR Impact
- hotspot overlap ratio: ...

### Recommendations
1. ...
```

## Section 6: Reviewer Recommendation Report

```markdown
## Reviewer Recommendations

### Recommended Reviewers
| Reviewer | Reason | Confidence |
|----------|--------|------------|

### File Ownership Map
- `path` -> owner

### Review Assignment Suggestion
- primary reviewer
- secondary reviewer
```

## Section 7: Branch Health Report

```markdown
## Branch Health Report

### Health Score: {score}/100 ({grade})

### Status Indicators
- Sync: ...
- Age: ...
- Conflict potential: ...
- CI: ...
- Review status: ...

### Recommendations
1. ...
```

## Section 8: Pre-Merge Checklist

```markdown
## Pre-Merge Checklist

### Required (Must Complete)
- [ ] review complete
- [ ] tests pass
- [ ] risk reviewed

### Security (Required for this PR)
- [ ] Sentinel review complete
- [ ] secrets exposure ruled out
```

## Section 9: Repository Pattern Analysis

```markdown
## Repository Pattern Analysis

### Commit Message Patterns
- ...

### Branch Naming Pattern
- ...

### PR Size Calibration
- ...

### Pattern Learning Configuration
- ...
```

## Section 10: Commit Split Plan

```markdown
## Current: 1 commit with 47 files

### Recommended Split
1. feature commit
2. tests
3. docs
4. incidental cleanup

### Git Commands to Execute
# Unstage all
# Stage and commit feature
# Stage and commit tests
```

## Section 11: Squash Optimization Report

```markdown
## Squash Optimization Report

### Before / After
- before: ...
- after: ...

### Squash Groups
- group 1: ...

### Decision Rationale
- ...

### Synthesized Commit Messages
- ...

### Rebase Script (Ready to Paste)
# Run: git rebase -i $(git merge-base HEAD main)

### Post-Squash Verification Checklist
- [ ] diff integrity checked
- [ ] tests pass
```

## Section 12: PR Split Strategy

```markdown
## PR Analysis: 73 files, 2,847 lines (Size: XL)

### Recommended Split
1. ...

### Merge Order
1. ...

### Parallelization
- ...
```

## Section 14: PR Description Templates

### Bad Example (Avoid)

```markdown
## Summary
Updated files.

## Changes
- stuff
```

### Good Example (Follow)

```markdown
## Summary
Add OAuth2 provider support for internal SSO.

## Test plan
- Added integration tests for login callback

## Changes
### Features
- Added OAuth2 provider integration
```

### PR Description Template

```markdown
## Summary

## Test plan

## Changes

## Breaking changes (if applicable)

## Notes (optional)
```

## Section 16: Monorepo PR Split

```markdown
## Recommended PR Structure for Monorepo

### Rationale
- keep package boundaries reviewable
```

## Section 17: Release Notes

```markdown
## v1.3.0 Release Notes

### Features
- ...

### Bug Fixes
- ...

### Breaking Changes
- ...

### Dependencies
- ...
```

## Section 18: Progressive PR Split Plan (MEGA)

```markdown
## MEGA PR Split Plan: 247 files, 8,340 lines

### Overview
- ...

### Week 1
- ...

### Week 2
- ...

### Risk Mitigation
- ...

### Chunked Analysis Mode
- ...
```

## AI-Generated Code Detection Patterns

Use a short addendum when AI-suspected code matters:
- suspected AI ratio
- verification status
- required Judge or Radar follow-up
