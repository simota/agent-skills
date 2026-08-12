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


## Per-Recipe Behavior + VERIFY Gates (SKILL.md excerpt)

Behavior notes per Recipe. Each `**VERIFY**:` is the recipe-specific gate enforcing Guardian's Hard Gates and Output Requirements at PRESENT.
- `pr`: Execute in order Change Classification → Quality Score → Risk Assessment → PR title/body → Reviewer recommendation. **VERIFY**: all 5 mandatory Output sections present (classification table / size+noise ratio / quality score+grade / risk band / actionable rec); apply the Hard gates above; size band assigned and split recommended at L+.
- `commit`: Classify changes as Essential/Supporting/Incidental and generate a plan to split into atomic commits. **VERIFY**: each proposed commit is atomic (one logical change, independently revertible); every message is Conventional-Commits typed/scoped; no WIP/fixup residue survives in the plan; every Essential change is preserved (none silently dropped).
- `naming`: Conventional Commits compliance check. Validate scope, verb, and 50-character limit. **VERIFY**: type ∈ allowed set (feat/fix/refactor/docs/test/chore/perf/security/…); imperative-mood verb; subject ≤50 chars; scope present where it adds clarity; zero agent names in the message.
- `strategy`: Choose GitHub Flow / Git Flow / Trunk-Based based on DORA metrics and branch lifetime. **VERIFY**: the choice is grounded in actual DORA metrics + branch lifetime (not guessed); long-lived branches are not defaulted to GitFlow (cascading-conflict-debt anti-pattern); the merge strategy matches the branch model; `rework_rate>0.30` surfaced if present.
- `reshape`: Create a new branch off the base → squash-import the development branch via `git merge --squash` → apply the same Change Classification as the `commit` Recipe to re-split into atomic commits and reshape history. **Backup branch creation is required**; force push or application to remote shared branches is Ask First; execution commands are proposals only and run after user consent. **VERIFY**: a backup branch is created **before** any history rewrite (non-negotiable); force-push / shared-branch application gated Ask First; every command is a proposal run only after consent; the reshaped tip's content diff against base is **identical** to the original (reshape changes history, never the final tree).
- `audit`: Read-only diagnosis of commit history in the specified range (`origin/main..HEAD` by default). Detect WIP/fixup residue, Conventional Commits violations, atomicity score, size deviation, and missing signatures, then recommend the next Recipe (`commit` / `reshape` / `pr` / proceed as-is). Zero side effects. **VERIFY**: zero side effects (no branch/commit/index mutation); range stated explicitly; WIP/fixup + CC-violation + atomicity + size-deviation + signature all checked; output ends in a concrete next-Recipe recommendation.
- `split`: Generate a plan to decompose an M+ branch into stacked PRs. Size each PR to 10-15 minutes of review, and present dependency order (bottom-up), file boundaries, estimated review time, and tool selection (Graphite / ghstack / git-town / jj). Execution commands are proposals only; run in stages after user consent. **VERIFY**: each stacked PR is sized to ~10–15 min review; dependency order is bottom-up and acyclic; file boundaries are distinct per PR; execution commands are proposals only (staged consent); XXL/MEGA routed to Sherpa.
- `health`: Inventory the repo's local/remote branches. Classify stale (30+ days without updates), upstream divergence, merged-but-undeleted, and high conflict-probability branches, and recommend delete, rebase, or archive. Branch deletion is Ask First. **VERIFY**: every branch classified (stale / diverged / merged-undeleted / conflict-risk); each carries a delete/rebase/archive recommendation; branch deletion gated Ask First (never auto-deleted); no destructive op executed in the inventory pass.
- `ship`: Execute end-to-end PR delivery — `PREFLIGHT → CREATE → WATCH → GATE → MERGE → CLEANUP`. Consume `pr` Recipe output for title/body/reviewers and `strategy` Recipe output for merge mode (default `--squash --delete-branch`). Hard gates: `quality_score >= 65`, `risk_score <= 85`, `security != CRITICAL`, `intent_alignment != FAIL` (Judge verdict; `NOT_CHECKED` permitted only with an explicit note that intent was not verified), all required CI green, `reviewDecision == APPROVED`, `mergeStateStatus == CLEAN`. Ask First on every MERGE execution; `--admin` bypass and force-merge over `UNSTABLE` are Ask First. Never auto-merge without explicit consent. For XXL/MEGA branches, refuse and route to `split` first. **VERIFY**: all seven Hard gates above are green before MERGE; the Ask-First requirements above were followed exactly as stated — routine merge confirmation, and separately for `--admin` bypass / force-merge over `UNSTABLE` — with zero auto-merge; XXL/MEGA refused → `split`.

