# Scout Output Format

**Purpose:** Canonical investigation report schema, toolkit, and completion criteria.
**Read when:** You are producing the final investigation artifact or checking whether the handoff is complete enough.

## Contents

- Investigation report template
- Investigation toolkit
- Completion criteria
- Confidence levels

## Investigation Report Template

```markdown
## Scout Investigation Report

### Bug Summary
**Title:** [Brief description]
**Severity:** Critical / High / Medium / Low
**Reproducibility:** Always / Sometimes / Rare

### Reproduction Steps
1. [Step 1]
2. [Step 2]

**Expected:** [What should happen]
**Actual:** [What actually happens]

### Root Cause Analysis
**Location:** `src/path/to/file.ts:123` in `functionName()`
**Cause:** [Why the bug occurs]

### Recommended Fix
**Approach:** [High-level fix strategy]
**Files to modify:** [List with expected changes]

### Regression Prevention
**Suggested tests for Radar:** [Test cases to prevent recurrence]

## LLM Fix Prompt
[Paste-ready instruction prompt for a downstream coding LLM. Mandatory for confirmed root causes. See `reference/fix-prompt-generation.md` for verbs, schema, and suppression rules.]
```

Add when available:

- confidence level
- evidence links
- impact scope
- workaround

## Investigation Toolkit

| Category | Tools |
|----------|-------|
| Code | `git log`, `git blame`, `git bisect`, codebase search |
| Runtime | DevTools `Network`, `Console`, `Sources`, debugger |
| State | React/Vue DevTools, Redux DevTools |
| Data | database queries, API inspection |

## Investigation Completion Criteria

### Required

- [ ] Reproducible, or reproduction conditions identified
- [ ] Root cause identified, or a bounded hypothesis set exists
- [ ] Impact scope understood
- [ ] Fix approach can be articulated

### Confidence Levels

| Level | Condition | How to Report |
|-------|-----------|---------------|
| HIGH | Reproduction success + root-cause code identified | Report as confirmed |
| MEDIUM | Reproduction success + cause estimated | Report as estimated and provide verification method |
| LOW | Cannot reproduce + hypothesis only | Report as hypothesis and specify missing information |
