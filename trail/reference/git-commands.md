# Trail Git Command Reference

## Safety Classification

### 🟢 Safe Commands (Always OK)

These commands are read-only and do not modify the repository state.

#### History Viewing

```bash
# Basic log
git log --oneline              # Concise history
git log --oneline -20          # Latest 20 commits
git log --oneline --all        # All branches
git log --graph --oneline      # Graph display

# Detailed log
git log -p                     # With patch
git log --stat                 # With statistics
git log --name-status          # With file change types

# Filtering
git log --since="2024-01-01"   # After date
git log --until="2024-01-31"   # Before date
git log --author="alice"       # Filter by author
git log -- path/to/file        # Specific file

# Specific commit
git show <commit>              # Commit details
git show <commit>:<file>       # File at specific version
git show <commit> --stat       # Change statistics
```

#### Search Commands

```bash
# String search (find additions/deletions)
git log -S "searchString"      # pickaxe search
git log -S "searchString" --oneline

# Regex search (in diff)
git log -G "pattern"           # regex in diff
git log -G "TODO.*fix"

# Commit message search
git log --grep="bug fix"       # Search in messages
git log --grep="fix" --grep="bug" --all-match  # AND search

# Code search
git grep "pattern"             # Current code
git grep "pattern" <commit>    # At specific commit
```

#### Blame Analysis

```bash
# Basic blame
git blame <file>               # All lines
git blame -L 100,150 <file>    # Line range
git blame -L :functionName <file>  # Function

# Detailed blame
git blame -w <file>            # Ignore whitespace changes
git blame -M <file>            # Detect line movements
git blame -C <file>            # Detect copies too
git blame --since="1 year ago" <file>  # Limited period
```

#### Diff Commands

```bash
# Diff between commits
git diff <commit1>..<commit2>
git diff <commit1>..<commit2> -- <file>
git diff <commit1>..<commit2> --stat

# Diff of specific commit
git diff <commit>^..<commit>   # Diff with parent
git diff <commit>~3..<commit>  # Diff from 3 commits ago
```

#### Reference Resolution

```bash
# SHA resolution
git rev-parse HEAD
git rev-parse <branch>
git rev-parse <tag>

# Tag/branch listing
git tag -l
git branch -a
git describe --tags <commit>

# Common ancestor
git merge-base <commit1> <commit2>
```

---

### 🟡 Caution Commands (Requires Confirmation)

These commands temporarily change HEAD or working directory.

#### Git Bisect

```bash
# Start (HEAD becomes detached)
git bisect start
git bisect bad <commit>
git bisect good <commit>

# Manual operations
git bisect good                # Mark current commit as good
git bisect bad                 # Mark current commit as bad
git bisect skip                # Skip current commit

# Automated execution
git bisect run <test_command>

# End (REQUIRED!)
git bisect reset               # Return to original state
git bisect log                 # Output log

# Resume from log
git bisect replay <logfile>
```

**Cautions:**
- During bisect, you're in detached HEAD state
- Always end with `bisect reset`
- Stash any uncommitted changes first

#### Checkout (Read-only purposes)

```bash
# Specific file only (safer)
git checkout <commit> -- <file>  # Get specific file

# Checkout entire commit (detached HEAD)
git checkout <commit>          # Warning: detached HEAD

# Return
git checkout -                  # Return to previous branch
git checkout <branch>          # Return to branch
```

**Cautions:**
- `git checkout <commit>` results in detached HEAD
- Use only for verification, don't make changes
- Always return to original branch after checking

#### Stash (If preserving work)

```bash
# Temporarily save work
git stash push -m "Trail investigation"
git stash list
git stash show -p stash@{0}

# Restore
git stash pop                  # Apply and delete
git stash apply                # Apply only (don't delete)
```

---

### 🔴 Forbidden Commands (Never Run)

These commands are NEVER executed by Trail.

```bash
# Destructive reset
git reset --hard              # ❌ Changes will be lost
git checkout .                # ❌ Changes will be lost

# File deletion
git clean -f                  # ❌ Untracked files deleted
git clean -fd                 # ❌ Directories too

# History modification
git rebase                    # ❌ History changes
git commit --amend            # ❌ Commit changes
git filter-branch             # ❌ History changes

# Remote operations
git push                      # ❌ Outside Trail's scope
git push --force              # ❌ Especially dangerous
```

---

## Common Patterns

### Pattern 1: Regression Bisect

```bash
# 1. Save current state (if there are changes)
git stash push -m "Before bisect"

# 2. Start bisect
git bisect start

# 3. Set bad/good
git bisect bad HEAD
git bisect good v1.0.0

# 4. Automated execution
git bisect run npm test

# 5. Check result
git bisect log

# 6. End (important!)
git bisect reset

# 7. Restore work
git stash pop
```

### Pattern 2: File History Deep Dive

```bash
# Full file history (with rename tracking)
git log --follow --oneline -- path/to/file

# History for specific period
git log --since="2024-01-01" --until="2024-06-30" -- path/to/file

# Detailed diff for each commit
git log --follow -p -- path/to/file

# With statistics
git log --follow --stat -- path/to/file
```

### Pattern 3: Code Archaeology

```bash
# 1. Blame the lines
git blame -L 100,120 src/utils.ts

# 2. Get commit details
git show abc1234

# 3. Find PR/merge containing that commit
git log --merges --ancestry-path abc1234..HEAD --oneline

# 4. Find related changes
git log -S "functionName" --oneline
```

### Pattern 4: Impact Analysis

```bash
# List of changed files
git diff --name-only v1.0.0..v2.0.0

# Statistics
git diff --stat v1.0.0..v2.0.0

# Change details for specific file
git log --oneline v1.0.0..v2.0.0 -- src/critical.ts

# High-frequency change files
git log --name-only --pretty=format: v1.0.0..v2.0.0 | \
  sort | uniq -c | sort -rn | head -20
```

### Pattern 5: Ownership Analysis

```bash
# Contributors for file/directory
git shortlog -sn -- src/payment/

# Recent contributors
git log --since="6 months ago" --format="%an" -- src/payment/ | \
  sort | uniq -c | sort -rn

# Owner distribution per line
git blame --line-porcelain src/payment/index.ts | \
  grep "^author " | sort | uniq -c | sort -rn
```

---

## Bisect Edge Cases

### Flaky Test Handling

```bash
# Run 3 times and use majority vote
git bisect run bash -c '
  PASS=0
  for i in 1 2 3; do
    npm test && PASS=$((PASS+1))
  done
  [ $PASS -ge 2 ]
'
```

### Build Failure Handling

```bash
# Skip on build failure (exit 125)
git bisect run bash -c '
  npm run build || exit 125  # 125 = skip
  npm test
'
```

### Large Range Narrowing

```bash
# First narrow down to relevant commits
git log --oneline -S "problematicFunction" v1.0.0..HEAD

# Bisect within the hit commit range
git bisect start
git bisect bad <first_hit>
git bisect good <last_hit>~1
```

---

## Safety Checklist

Checklist before starting bisect:

- [ ] Confirm no uncommitted changes (stash if needed)
- [ ] Manually verify good commit is actually good
- [ ] Manually verify bad commit is actually bad
- [ ] Verify test command works correctly
- [ ] Don't forget to reset after bisect completes
