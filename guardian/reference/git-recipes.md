# Guardian Git Command Recipes

Purpose: Provide reusable Git and `gh` command patterns for safe analysis, restructuring, PR prep, hotspot inspection, and conflict handling.

## Contents

- Analyze changes
- Interactive commit structuring
- Squash analysis
- Backup and restore
- Branch operations
- PR operations
- Hotspot analysis
- Conflict resolution

## Analyze Changes

```bash
# View staged changes summary
git diff --cached --stat

# View all changes against target branch
git diff main...HEAD --stat

# Find large file changes
git diff main...HEAD --numstat | sort -k1 -rn | head -20

# List commits not in main
git log main..HEAD --oneline
```

## Interactive Commit Structuring

```bash
# Split staged changes interactively
git add -p

# Unstage specific files
git reset HEAD -- path/to/file

# Amend last commit (before push only)
git commit --amend

# Interactive rebase to restructure
git rebase -i HEAD~5
```

## Squash Analysis

```bash
# List all commits from merge-base with stats
git log --oneline --stat $(git merge-base HEAD main)..HEAD

# Compact commit + file list for analysis
git log --format='%h %s' --name-only $(git merge-base HEAD main)..HEAD

# Detect WIP / noise commits
git log --oneline $(git merge-base HEAD main)..HEAD | \
  grep -iE '(^[a-f0-9]+ (WIP|wip|tmp|temp|fixup!|squash!|fix typo|forgot|oops|address review))'

# File overlap between adjacent commits
comm -12 \
  <(git diff-tree --no-commit-id --name-only -r COMMIT_A | sort) \
  <(git diff-tree --no-commit-id --name-only -r COMMIT_B | sort)

# Verify each commit builds independently
git rebase -i --exec 'npm run build' $(git merge-base HEAD main)

# Verify each commit passes tests independently
git rebase -i --exec 'npm test' $(git merge-base HEAD main)
```

## Backup and Restore

```bash
# Create backup branch before rebase
git branch backup/$(git branch --show-current)-pre-squash

# Restore from backup if squash goes wrong
git reset --hard backup/$(git branch --show-current)-pre-squash

# Verify diff integrity after squash (should output nothing)
git diff backup/$(git branch --show-current)-pre-squash..HEAD
```

## Co-Author Verification

```bash
# Extract all unique authors from branch commits
git log --format='%an <%ae>' $(git merge-base HEAD main)..HEAD | sort -u

# Extract existing Co-authored-by lines
git log --format='%B' $(git merge-base HEAD main)..HEAD | grep '^Co-authored-by:' | sort -u

# Count unique contributors
git log --format='%an <%ae>' $(git merge-base HEAD main)..HEAD | sort -u | wc -l
```

## Branch Operations

```bash
# Create branch with proper naming
git checkout -b feat/example-change

# Rename current branch
git branch -m fix/new-branch-name

# Delete merged branch
git branch -d branch-name
```

## PR Operations With `gh`

```bash
# Create PR with generated description (file-based)
gh pr create --title "feat(auth): add oauth support" --body-file pr.md

# Minimal PR for small fixes
gh pr create --title "fix(api): handle empty response" --body "## Summary

Fix empty-response handling.

## Test plan
- Added unit test
"

# View PR diff stats
gh pr diff --stat

# List files changed in PR
gh pr view --json files

# View PR details
gh pr view
```

## Hotspot Analysis

```bash
# Most changed files in last 90 days
git log --since='90 days ago' --name-only --pretty=format: | sort | uniq -c | sort -rn | head -20

# Files with most authors
git shortlog -sne -- $(git ls-files)

# Bug fix frequency per file
git log --since='90 days ago' --grep='fix' --name-only --pretty=format: | sort | uniq -c | sort -rn | head -20
```

## Conflict Resolution

```bash
# View conflicting files
git diff --name-only --diff-filter=U

# Accept theirs (incoming) for specific file
git checkout --theirs path/to/file

# Accept ours (current) for specific file
git checkout --ours path/to/file

# After resolving, mark as resolved
git add path/to/file

# For lock files - regenerate
# rm package-lock.json && npm install
```
