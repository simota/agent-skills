# Review & Report Templates

Purpose: Use this file when Zen is in review mode or needs an exact output anchor for refactoring reports.

## Contents
- [Review Checklist](#review-checklist)
- [Review Output Format](#review-output-format)
- [Refactoring Report Format](#refactoring-report-format)

## Review Checklist

### Readability
- [ ] Variable and function names are descriptive
- [ ] Code is self-documenting
- [ ] No unnecessary magic numbers or strings
- [ ] Complexity is reasonable (`CC < 10` when possible)

### Structure
- [ ] Functions are focused and usually `<20` lines
- [ ] No unnecessary duplication
- [ ] Abstractions fit the actual problem
- [ ] Nesting depth stays `<=3` when possible

### Correctness
- [ ] Edge cases are handled
- [ ] Error paths remain intact
- [ ] No new null/undefined risk is introduced
- [ ] Logic matches the existing behavior

### Maintainability
- [ ] The code is easier to change later
- [ ] No hidden dependency was introduced
- [ ] The result remains testable
- [ ] The change is reversible if needed

## Review Output Format

```markdown
## Zen Code Review

### Summary
[1-2 sentence overall assessment]
**Review Level**: [Quick Scan / Standard / Deep Dive]

### Complexity Analysis
| File | Function | CC | Cognitive | Status |
|------|----------|----|-----------|--------|
| ... | ... | ... | ... | ... |

### Strengths
- [Specific positive point]

### Suggestions
- **[File:Line]** - [Suggestion]
  - Why: [Reasoning]
  - How: [Concrete fix]

### Issues
- **[File:Line]** - [Issue] (Severity: Minor/Moderate/Critical)
  - Impact: [Why this matters]
  - Fix: [Recommended solution]

### Verdict
Approve | Request Changes | Comment Only
```

## Refactoring Report Format

```markdown
## Refactoring Report: [Component/File]

### Summary
| Metric | Before | After | Change |
|--------|--------|-------|--------|
| Lines of Code | X | Y | -Z% |
| Cyclomatic Complexity (max) | X | Y | -Z% |
| Cognitive Complexity (max) | X | Y | -Z% |
| Functions | X | Y | +Z |
| Max Nesting Depth | X | Y | -Z |
| Code Smells Resolved | - | - | N |

### Changes Applied
1. [Recipe]: [Target] -> [Result]
2. [Recipe]: [Target] -> [Result]

### Test Verification
- Pre-refactor: [Pass/Fail] (X tests)
- Post-refactor: [Pass/Fail] (X tests)
- Coverage: X% -> Y%

### Remaining Opportunities
- [ ] [Next candidate]
```
