# Commit Message Analysis Reference

Purpose: Score commit messages, detect weak sequences, and prepare safe rewrite or rebase recommendations.

## Contents

- Message structure analysis
- Sequence quality
- Rewrite suggestions
- Rebase guidance
- Report templates
- AUTORUN integration
- Convention learning

## Message Structure Analysis

Conventional Commits format spec (type list, scope rules, subject/body conventions, length limits) lives in `commit-conventions.md` § Conventional Commits and § Atomic Commit Rules. This file extends that spec with scoring rules below — score each component (Type, Scope, Subject, Body, Footer) against the rules in `commit-conventions.md` and aggregate per the rubrics that follow.

## Commit Sequence Analysis

Check sequence quality for:
- atomicity
- bisectability
- noise commits such as `WIP`, `tmp`, `fix typo`, `oops`
- mixed concerns in a single sequence

Practical warning triggers:
- `avg_score < 40`
- `wip_commits > 3`

## Message Improvement Suggestions

Rewrite when:
- subject is vague
- scope is missing or wrong
- body is empty for a non-trivial change
- multiple commits describe the same logical unit poorly

### Rewrite Template

```text
feat(auth): add OAuth2 provider support

Explain why the change was needed and any non-obvious constraints.
```

## Interactive Rebase Guidance

### Rebase Plan Template

```text
# Interactive rebase — review and edit the todo list before execution
pick abc1234 feat(auth): add OAuth2 provider integration
fixup def5678 WIP: oauth progress
fixup ghi9012 fix typo in oauth config
pick jkl3456 test(auth): add OAuth2 integration tests
reword mno7890 docs(auth): update OAuth2 setup guide
```

### Non-Interactive Alternative

```bash
# 1. Create backup
git branch backup/$(git branch --show-current)-pre-rewrite

# 2. Soft reset to merge-base (keeps changes staged)
git reset --soft $(git merge-base HEAD main)

# 3. Re-commit in optimal structure
# 4. Verify diff integrity
git diff backup/$(git branch --show-current)-pre-rewrite..HEAD
```

## Report Templates

### Individual Commit Report

```markdown
## Commit Analysis: {hash}

### Score: {score}/100
- Type: ok
- Scope: warning
- Subject: good
- Body: missing
```

### Branch Commit Summary

```markdown
## Commit Message Analysis

### Commit Scores
- feat(auth): 92
- WIP: 20

### Distribution
- Excellent: 2
- Good: 3
- Poor: 1

### Common Issues
- 2 vague subjects
- 1 missing body

### Recommended Rebase Plan
- squash WIP into previous feature commit
```

## AUTORUN Integration

AUTORUN may:
- score commit messages
- flag weak sequences
- generate rewrite suggestions
- generate a review-ready rebase plan

Pause if:
- history rewrite is required on a shared branch
- attribution or multi-author concerns are unresolved

## Project Convention Learning

Store learned preferences in `.agents/guardian.md`, such as:
- preferred scopes
- body verbosity
- acceptable exceptions to conventional formatting
