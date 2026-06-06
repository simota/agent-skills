# History Audit Reference

Purpose: Read-only diagnostic of commit history quality over a branch range. Scores atomicity, convention compliance, size excess, WIP/fixup residue, and signature completeness. Recommends the next Guardian Recipe to invoke — `pr` (good as-is), `commit` (restage atomically), `reshape` (full history rebuild), or escalation to `sherpa` for oversized work.

## Contents

- When to run audit
- Range selection
- Score dimensions
- Grading and next-Recipe routing
- Command recipes
- Output template

## When to Run

- Before `pr`: confirm history is review-ready.
- Before `reshape`: confirm reshape is actually warranted (don't reshape clean histories).
- After a long-lived feature branch: detect accumulated noise.
- Post-merge retrospective: audit what landed.
- CI gate: fail fast on Conventional Commits violations.

## Range Selection

| Range | Usage |
|-------|-------|
| `origin/main..HEAD` (default) | Branch-scoped audit — the commits that would enter the PR |
| `<tag>..HEAD` | Release-window audit |
| `HEAD~N..HEAD` | Recent-window audit for interactive cleanup |
| `<base>..<branch>` | Arbitrary range (PR diff) |

Default to `origin/<default-branch>..HEAD` unless user specifies.

## Score Dimensions

All dimensions scored `0–100` and weight-averaged into a History Quality Score.

| Dimension | Weight | Signals |
|-----------|--------|---------|
| **Convention Compliance** | 20 | Conventional Commits format, scope valid, ≤50-char subject, imperative mood |
| **Atomicity** | 25 | One concern per commit, tests paired with impl, no mixed layers |
| **Noise Level** | 20 | WIP/fixup/squash!/tmp/oops markers, commits reverting prior commits in same branch, "address review" meta-commits |
| **Size Hygiene** | 15 | No single commit > 500 lines without justification; no empty commits; no megacommits > 1000 lines |
| **Message Quality** | 10 | Body explains "why", references issue IDs when applicable, no placeholder text ("update", "fix stuff") |
| **Provenance** | 10 | Author consistency, signed commits if repo requires, no generated-bot authorship on human-authored logic |

### Noise Markers (regex)

```
^(wip|WIP|Wip)[: ]
^fixup!
^squash!
^(tmp|temp|quick)[: ]
(forgot|oops|typo fix)
^(address|fix) review
^(rebase|merge) [a-f0-9]{7,}
```

Each marker subtracts `-5` from Noise Level (min 0).

### Atomicity Checks

- Files in one commit span more than 2 top-level directories → `-10`
- Commit contains both test and non-test code but is `>300` lines → `-5` (probably not atomic)
- Commit message has multiple verbs joined by "and" / "、" → `-5`
- Sequential commits touch identical file set → squash candidate → `-5` per pair (see `squash-optimization.md`)

## Grading and Next-Recipe Routing

| Score | Grade | Recommendation |
|-------|-------|----------------|
| 85–100 | A | Proceed with `/guardian pr` — history is clean |
| 70–84  | B | Minor cleanup via `/guardian commit` or interactive rebase suggested spots |
| 55–69  | C | `/guardian reshape` recommended — noise ratio too high for reviewer comfort |
| 35–54  | D | `/guardian reshape` strongly recommended; also consider `/guardian split` if M+ size |
| 0–34   | F | Block PR. Run `/guardian reshape` or decompose via `sherpa` before proceeding |

Hard gates (regardless of overall score):
- Any unresolved `fixup!` / `squash!` → block and recommend autosquash
- Any commit > 1000 lines → recommend `split` or `reshape`
- Any `wip` commit → block unless user explicitly keeps it
- Signed-commits-required repo with unsigned commits → recommend resign via `reshape`

## Command Recipes

### Collect range

```bash
BASE="origin/$(git symbolic-ref --short refs/remotes/origin/HEAD | sed 's|origin/||')"
RANGE="${BASE}..HEAD"

git log --format='%H|%an|%ae|%s|%b' "$RANGE"
git log --format='%H %s' "$RANGE" | wc -l                  # commit count
git log "$RANGE" --numstat --format='__COMMIT__%H'         # per-commit file changes
git log --format='%H %G?' --show-signature "$RANGE" 2>/dev/null   # signature status
```

### Detect noise markers

```bash
git log --format='%s' "$RANGE" | grep -iE '^(wip|fixup!|squash!|tmp|temp|oops|forgot|address review)' | wc -l
```

### Conventional Commits compliance

```bash
# Valid: <type>(<optional-scope>): <subject>
git log --format='%s' "$RANGE" | \
  grep -vE '^(feat|fix|docs|style|refactor|perf|test|chore|ci|security|build|revert)(\([a-z0-9./-]+\))?!?: .{1,50}$' | \
  wc -l
```

### Size outliers

```bash
git log --format='__C__%H %s' --numstat "$RANGE" | \
  awk '/^__C__/{if(total>500)print sha,total,subj;sha=$2;subj=substr($0,index($0,$3));total=0;next}
       NF==3{total+=$1+$2}'
```

### Sequential squash candidates

Defer to `squash-optimization.md` pairwise scoring for grouping. Audit only flags the count.

## Output Template

```markdown
## Guardian History Audit

**Range**: `origin/main..HEAD` (14 commits, 38 files, +890 / -220)
**Branch**: `feat/user-auth`
**History Quality Score**: **62 / 100 (Grade C)**

### Dimension Breakdown

| Dimension | Score | Weight | Contribution |
|-----------|-------|--------|--------------|
| Convention Compliance | 90 | 20 | 18.0 |
| Atomicity             | 45 | 25 | 11.3 |
| Noise Level           | 30 | 20 |  6.0 |
| Size Hygiene          | 80 | 15 | 12.0 |
| Message Quality       | 70 | 10 |  7.0 |
| Provenance            | 78 | 10 |  7.8 |
| **Total**             |    |    | **62.1** |

### Findings

**🔴 Blocking**
- `a1b2c3d` `fixup! add login endpoint` — unresolved fixup (run `git rebase --autosquash`)

**🟡 Warnings**
- `e4f5g6h` `wip: trying token refresh` — WIP commit should be squashed
- `i7j8k9l` `address review comments` — meta-commit, merge into originating commit
- 3 sequential commits on `src/auth/service.ts` — squash candidates (score +28)

**🟢 Passing**
- All commits follow Conventional Commits format
- No commit exceeds 500 lines
- All commits signed by same author

### Next Recipe

**Recommended**: `/guardian reshape`
- Noise level (30/100) and atomicity (45/100) are below B-grade threshold
- 3 squash candidates + 2 WIP/fixup markers warrant full rebuild over pointwise rebase

**Alternatives**:
- Minimal fix: `git rebase -i --autosquash origin/main` + manual squash of 3 pairs → re-run `/guardian audit`
- If blocked by size: `/guardian split` first (branch is 890 LoC, M-size border)
```

## Orbit Boundary

- `audit` is **read-only**. No Git state changes, no force-pushes, no branch creation.
- Output routes to subsequent Guardian Recipes (`commit` / `reshape` / `split` / `pr`) or external tools (`git rebase --autosquash`).
- Integrates with `squash-optimization.md` (pairwise), `commit-analysis.md` (atomicity), `commit-conventions.md` (format rules).
- Can be chained before `pr` as a pre-flight check; a failing audit should not auto-block unless `quality_score < 35` (F grade).
