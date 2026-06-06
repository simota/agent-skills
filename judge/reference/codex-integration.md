# Codex Review Integration

Detailed guide for using `codex review` CLI, interpreting output, and filtering false positives.

---

## Option Selection Guide

| Situation | Option | When to Use |
|-----------|--------|-------------|
| PR review | `--base <branch>` | Reviewing all changes in a PR against target branch |
| Before commit | `--uncommitted` | Reviewing local changes before creating a commit |
| Specific commit | `--commit <SHA>` | Reviewing changes in a specific commit |
| No explicit request | Consider `--uncommitted` | When user says "review" without scope, check for uncommitted changes first |

**Tip**: If the user's request is ambiguous, check `git status` first. If uncommitted changes exist, suggest using `--uncommitted`.

---

## Review Commands

### PR Review Mode

```bash
# Review changes against a base branch
codex review --base main "Focus on: bug detection, logic errors, edge cases, security issues"

# With custom prompt
codex review --base develop "Check for: null handling, error propagation, API contract violations"
```

### Pre-Commit Mode

```bash
# Review uncommitted changes (staged, unstaged, untracked)
codex review --uncommitted "Identify bugs, security issues, and logic errors before commit"
```

### Commit Review Mode

```bash
# Review a specific commit
codex review --commit <SHA> "Analyze this commit for bugs and issues"
```

### Custom Review Instructions

```bash
# Read instructions from stdin
echo "Focus on authentication flow and session handling" | codex review --base main -
```

---

## Severity Categories

### CRITICAL (Must Fix)
- Security vulnerabilities (SQL injection, XSS, auth bypass)
- Data corruption risks
- Memory leaks in production paths
- Unhandled exceptions that crash the app
- Race conditions with data integrity impact

### HIGH (Should Fix Before Merge)
- Logic errors that produce incorrect results
- Missing error handling for likely failure cases
- Null/undefined access in common paths
- Off-by-one errors affecting business logic
- API contract violations

### MEDIUM (Fix Soon)
- Edge cases not handled
- Potential performance issues
- Incomplete error messages
- Missing validation for optional inputs
- Inconsistent state handling

### LOW (Consider)
- Minor optimization opportunities
- Defensive checks that could be added
- Potential future issues
- Documentation suggestions for complex logic

### INFO (Observation)
- Patterns that differ from conventions
- Suggestions for future improvement
- Notes for code maintainers

---

## Output Interpretation

### Mapping codex review Output to Severity

| codex review Signal | Suggested Severity | Rationale |
|---------------------|-------------------|-----------|
| "security vulnerability", "injection", "XSS" | CRITICAL | Direct security impact |
| "null pointer", "undefined access", "crash" | HIGH | Runtime failure |
| "logic error", "incorrect result", "wrong value" | HIGH | Incorrect behavior |
| "missing error handling", "unhandled exception" | HIGH | Potential crash |
| "edge case", "boundary", "corner case" | MEDIUM | Partial failure |
| "performance", "inefficient", "N+1" | MEDIUM | Degraded performance |
| "could be improved", "consider", "suggestion" | LOW/INFO | Enhancement opportunity |
| "style", "naming", "formatting" | INFO | Delegate to Zen |

---

## Filtering False Positives

**Common false positives to verify:**

1. **Type assertions that are valid**
   - codex may flag `as` casts, but they may be intentional
   - Verify: Is the cast backed by runtime check or API contract?

2. **Intentional null returns**
   - "Returns null without check" may be by design
   - Verify: Does the function signature indicate nullable return?

3. **Test file patterns**
   - Mock data may trigger "hardcoded value" warnings
   - Verify: Is this in a test file? Test patterns are acceptable.

4. **Framework conventions**
   - Next.js `'use client'` may flag as "string literal"
   - Verify: Is this a framework-required directive?

---

## Severity Override Guidelines

| If codex says... | But context shows... | Override to... |
|------------------|---------------------|----------------|
| HIGH (null access) | Value guaranteed by type | LOW or dismiss |
| CRITICAL (injection) | Input is from trusted source | MEDIUM |
| MEDIUM (no error handling) | Error would crash entire app | HIGH |
| LOW (performance) | Hot path in production | MEDIUM/HIGH |

---

## Review Checklist

### Correctness
- [ ] Logic matches the stated intent (PR title, commit message)
- [ ] All code paths produce correct output
- [ ] Edge cases are handled appropriately
- [ ] Error conditions are handled gracefully
- [ ] Boundary values are validated

### Security
- [ ] No hardcoded secrets or credentials
- [ ] User input is validated/sanitized
- [ ] SQL queries use parameterized statements
- [ ] Authentication/authorization checks are present
- [ ] Sensitive data is not logged

### Reliability
- [ ] Null/undefined checks where needed
- [ ] Error handling is comprehensive
- [ ] Async operations have proper error handling
- [ ] Resources are properly cleaned up
- [ ] No race conditions

### Intent Alignment
- [ ] Changes match PR/commit description
- [ ] No unrelated changes included
- [ ] Scope is appropriate (not too broad/narrow)
- [ ] Breaking changes are documented

---

## REVIEW.md Integration

If the repository contains a `REVIEW.md` at its root, treat it as project-specific review guidelines.

**Discovery flow:**

1. Check for `REVIEW.md` at the repository root before starting the review.
2. If found, prepend its contents as custom instructions to the `codex review` prompt.
3. Project-specific rules in `REVIEW.md` take precedence over generic review heuristics.
4. If `REVIEW.md` is absent, proceed with default review guidelines — do not warn or block.

**Example usage:**

```bash
# Prepend REVIEW.md content as custom review instructions
cat REVIEW.md | codex review --base main -
```

---

## PR Size Assessment

Measure PR size using `git diff --stat` and classify into tiers. Cognitive load research shows defect detection drops sharply beyond 400 LOC (see `review-effectiveness.md`).

| Tier | LOC (added + deleted) | Review depth | Action |
|------|----------------------|--------------|--------|
| **Small** | < 100 | Deep | Review immediately |
| **Medium** | 100–400 | Adequate | Standard review |
| **Large** | 400–1000 | Declining | Recommend splitting |
| **XL** | > 1000 | Perfunctory risk | Strongly recommend splitting |

**Warning thresholds in review report:**

- **> 1000 LOC**: `⚠️ PR exceeds 1000 LOC. Review quality degrades significantly. Strongly recommend splitting.`
- **> 400 LOC**: `ℹ️ PR exceeds 400 LOC. Consider splitting to reduce reviewer cognitive load.`

---

## Multi-Agent Verification

Cross-verify findings across multiple dimensions to reduce false positive rate below 1%.

**Verification dimensions:**

| Dimension | Focus | Example agents |
|-----------|-------|----------------|
| Correctness | Logic errors, edge cases | Judge (primary) |
| Security | Vulnerabilities, secrets | Sentinel |
| Consistency | Pattern adherence, naming | Zen |

**Confidence rules:**

- **Duplicate finding** (flagged by ≥2 dimensions): Elevate confidence — high-priority fix.
- **Single-dimension finding**: Add a verification note; recommend manual confirmation.
- **Contradictory signals** (one dimension flags, another clears): Report both perspectives; do not auto-dismiss.

**Workflow:** Run Judge's core analysis first, then cross-reference with Sentinel and Zen outputs when available. Merge duplicate findings and annotate confidence level in the report.
