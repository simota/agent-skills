# History Reshape Reference

Purpose: Rebuild a feature branch's commit history from scratch by (1) creating a fresh branch off the base, (2) pulling the entire development branch's diff in as a single squashed working tree, and (3) redistributing that diff into well-structured atomic commits. Use when the dev branch has accumulated WIP/fixup noise, mixed concerns, or out-of-order commits that are not worth rescuing with `rebase -i`.

## Contents

- When to use reshape vs rebase -i vs squash merge
- Preconditions
- Workflow
- Command recipes
- Commit replanning (hand-off to `commit` Recipe)
- Risks and rollback
- Verification checklist

## When to Use

| Situation | Recommendation |
|-----------|----------------|
| 1–3 commits with minor noise | `rebase -i` (cheaper) |
| Linear but WIP-heavy (`WIP`, `fixup`, `tmp`) | `squash-optimization` pairwise squash |
| 10+ commits, mixed concerns, out-of-order work | **reshape** (this Recipe) |
| Want a single commit on merge | merge strategy = `squash` (no reshape needed) |
| Branch already pushed and shared | Ask First — coordinate with collaborators; force-push required |

## Preconditions

Before proposing reshape commands, verify:

1. **Base branch is up to date**: `git fetch origin && git log origin/<base>..<base>` shows no divergence.
2. **Working tree is clean**: `git status` shows no uncommitted changes.
3. **Branch is not shared**: `git log --remotes --oneline <branch> | wc -l` — warn if pushed.
4. **Backup exists**: `git branch <branch>-backup-<YYYYMMDD>` before any destructive step.
5. **Base branch is the right target**: confirm with user (`main` / `develop` / etc.).

If any precondition fails, stop and request confirmation.

## Workflow

```
SURVEY   → Collect diff scope, commit count, file touch map, noise ratio
PLAN     → Design target commit structure (Essential / Supporting split)
BACKUP   → Create `<branch>-backup-<date>` snapshot
RESHAPE  → Create new branch off base, squash-merge dev branch
REPLAN   → Hand off to `commit` Recipe on the squashed staging area
VERIFY   → Diff equivalence check against original branch HEAD
PRESENT  → Command script + commit plan + rollback instructions
```

### Diff Equivalence Invariant

The final tree at the new branch's HEAD must exactly match the original branch's HEAD tree. Verify with:

```bash
git diff <branch>-backup-<date>..<new-branch> -- :!CHANGELOG.md
# Must produce empty output. Any non-empty diff = reshape failed.
```

## Command Recipes

### 1. Collect state

```bash
BASE="main"
SRC="$(git branch --show-current)"
DATE="$(date +%Y%m%d)"
NEW="${SRC}-reshaped"

git fetch origin "$BASE"
git log --oneline "origin/$BASE..$SRC"               # commits to consolidate
git diff --stat "origin/$BASE...$SRC"                # files and lines affected
git log --format='%h %an %s' "origin/$BASE..$SRC" | wc -l  # commit count
```

### 2. Backup (MANDATORY)

```bash
git branch "${SRC}-backup-${DATE}" "$SRC"
# Verify
git show-ref "refs/heads/${SRC}-backup-${DATE}"
```

### 3. Create fresh branch from base

```bash
git checkout -B "$NEW" "origin/$BASE"
```

### 4. Squash-merge the dev branch

Two equivalent techniques — choose based on the desired staging state:

**A. `git merge --squash` (preferred, keeps everything staged)**

```bash
git merge --squash "$SRC"
# Working tree + index now hold the entire cumulative diff.
# No commit is created yet. Ready for commit-replan phase.
```

**B. `git diff | git apply` (fallback when merge conflicts exist)**

```bash
git diff "origin/$BASE...$SRC" | git apply --index
```

### 5. Replan commits (hand off to `commit` Recipe)

With the full diff staged on the new branch:

```bash
git reset                    # unstage so we can split intentionally
git status --short           # scan all modified files
```

Invoke Guardian's `commit` Recipe on this state. The `commit` Recipe's Change Classification produces an atomic commit plan; reshape just executes that plan:

```bash
# For each planned commit:
git add <files for commit 1>
git commit -m "feat(scope): commit 1 subject"
git add <files for commit 2>
git commit -m "refactor(scope): commit 2 subject"
# ... repeat
```

### 6. Verify equivalence

```bash
# Tree-level diff — must be empty
git diff "${SRC}-backup-${DATE}" "$NEW"

# Line count sanity check
git log --oneline "origin/$BASE..$NEW" | wc -l   # new commit count
git log --oneline "origin/$BASE..${SRC}-backup-${DATE}" | wc -l  # original
```

If the tree diff is non-empty, **stop and rollback** — something was lost.

### 7. Replace original branch (optional, Ask First)

```bash
# Only after user confirms the new branch is good
git branch -M "$NEW" "$SRC"   # rename new branch over original

# If already pushed, force-with-lease is REQUIRED (never plain --force)
git push --force-with-lease origin "$SRC"
```

## Commit Replanning Heuristics

Bucket the cumulative diff by:

1. **Concern**: test infra vs feature code vs config vs docs
2. **Layer**: model → service → controller → view (bottom-up commit order)
3. **Dependency**: introduce types/interfaces before consumers
4. **Reversibility**: pure additions before modifications before deletions

Target commit sizes (align with Guardian size bands):

| Commit size | Files | Lines | Use when |
|-------------|-------|-------|----------|
| Atomic      | 1–5   | 10–100 | ideal — one reviewable concern |
| Compound    | 5–10  | 100–300 | acceptable if tightly coupled |
| Oversized   | 10+   | 300+ | split further |

## Risks

| Risk | Mitigation |
|------|------------|
| Lost commits (missing diff after reshape) | Backup branch + tree diff equivalence check |
| Force-push overwrites collaborator work | Ask First if branch is shared; use `--force-with-lease` |
| CI pipeline assumes specific commit SHAs | Check CI config references to commit SHAs before renaming |
| Signed commits lose signatures | Re-sign new commits (`git commit -S`); flag in plan if signing is required |
| Conflict with merge-queue or stacked PRs | Abort if PR is queued or depends on stack |
| Binary files or large diffs | `git apply` can fail silently on binary — verify with tree diff |

## Rollback

```bash
# If anything goes wrong BEFORE force-pushing
git checkout "${SRC}-backup-${DATE}"
git branch -D "$NEW"

# If already force-pushed and needs recovery from remote
git fetch origin
git reset --hard "origin/${SRC}"  # if remote still has old state
# Otherwise recover from backup branch (local) or reflog
git reflog | grep "$SRC"
```

## Verification Checklist

Deliver this checklist with every `reshape` output:

- [ ] Backup branch created and pushed/tagged
- [ ] New branch created off base (confirmed via `git merge-base`)
- [ ] Tree diff vs backup = empty
- [ ] Each new commit passes `<type>(<scope>): <subject>` convention
- [ ] Each commit is buildable / bisectable (if repo requires it)
- [ ] No binary or large files dropped (file count matches backup)
- [ ] If shared: force-with-lease used; collaborators notified
- [ ] Original branch archived or deleted per team policy

## Output Template

```markdown
## Guardian History Reshape Plan

**Source**: `feat/user-auth` (17 commits, 42 files, +1,240 / -380)
**Base**: `origin/main`
**Target**: `feat/user-auth-reshaped` (5 planned commits)
**Backup**: `feat/user-auth-backup-20260424`

### Target Commit Structure

| # | Type | Scope | Subject | Files | Lines |
|---|------|-------|---------|-------|-------|
| 1 | feat | auth/model | add User and Session schemas | 4 | +210/-0 |
| 2 | feat | auth/service | add token issuance and validation | 6 | +380/-12 |
| 3 | feat | auth/api | expose /login and /logout endpoints | 5 | +250/-8 |
| 4 | test | auth | cover login flow and token lifetime | 8 | +340/-0 |
| 5 | docs | auth | document token lifecycle in README | 2 | +60/-360 |

### Execution Script

\```bash
# ... full command block here ...
\```

### Verification

\```bash
git diff feat/user-auth-backup-20260424 feat/user-auth-reshaped
# Expected: empty
\```

### Rollback

\```bash
git checkout feat/user-auth-backup-20260424
git branch -D feat/user-auth-reshaped
\```
```

## Orbit Boundary

- Guardian `reshape` **proposes** the script and commit plan; it does not auto-execute destructive Git ops.
- User confirms each phase (backup → squash → per-commit add/commit → optional force-push).
- For shared branches, escalate via `GUARDIAN_TO_SHERPA_HANDOFF` if coordination with multiple authors is required.
- Integrates with `commit` Recipe for per-commit atomicity scoring and with `squash-optimization.md` for pairwise grouping when the squashed diff still has natural sub-boundaries.
