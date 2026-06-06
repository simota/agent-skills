# PR Ship Flow Reference

Purpose: After PR preparation is complete (typically the output of the `pr` Recipe), execute the full delivery flow: create the PR, monitor CI, verify approval gates, merge, and clean up. Every state-changing step is a proposal — guardian does not auto-execute merges without explicit user consent.

## Contents

- When to use ship vs pr
- Preconditions
- Workflow phases
- Command recipes
- Hard gates (cannot bypass)
- Ask First gates
- Risks and rollback
- Verification checklist
- Output template

## When to Use

| Situation | Recommendation |
|-----------|----------------|
| Need PR title/body/risk analysis only | `pr` Recipe (preparation only) |
| Branch is ready and you want end-to-end delivery | **ship** (this Recipe) |
| PR already exists and you want to monitor + merge | **ship** with `--from-existing <PR#>` |
| Large feature spanning multiple PRs | `split` first, then ship each stack member |
| Branch needs history cleanup before shipping | `reshape` first, then ship |
| Release coordination across multiple PRs | Hand off to `launch` |

## Preconditions

Before proposing ship commands, verify:

1. **Working tree is clean**: `git status` shows no uncommitted changes
2. **Branch is pushed and up-to-date with base**: `git fetch origin && git log origin/<base>..HEAD` shows expected commits; `git log HEAD..origin/<base>` is empty (or rebase recommended)
3. **`pr` Recipe output exists**: title, body, reviewer list, quality_score, risk_band
4. **Quality gate passed**: `quality_score >= 65` (B grade or higher) — otherwise stop
5. **Risk gate passed**: `risk_score <= 85` (not Critical) — otherwise require explicit override
6. **Security gate passed**: `security_classification != CRITICAL` — otherwise require Sentinel handoff completion
7. **`gh` CLI authenticated**: `gh auth status` succeeds
8. **CI configuration discovered**: detected required status checks from branch protection rules

If any precondition fails, stop and request confirmation or route to the appropriate Recipe.

## Workflow

```
PREFLIGHT → CREATE → WATCH → GATE → MERGE → CLEANUP
```

| Phase | Goal | State change |
|-------|------|--------------|
| `PREFLIGHT` | Verify preconditions and gates | Read-only |
| `CREATE` | Create the PR (or attach to existing) | Creates remote PR |
| `WATCH` | Monitor CI status until terminal | Read-only |
| `GATE` | Verify approvals, conflicts, branch protection | Read-only |
| `MERGE` | Execute merge per `strategy` Recipe choice | **Ask First** — destructive on shared history |
| `CLEANUP` | Delete local/remote branch, sync base | Local + remote branch deletion |

## Command Recipes

### 1. PREFLIGHT — Verify all gates

```bash
BASE="${BASE:-main}"
SRC="$(git branch --show-current)"

# State checks
git fetch origin "$BASE"
test -z "$(git status --porcelain)" || { echo "uncommitted changes"; exit 1; }
gh auth status >/dev/null || { echo "gh CLI not authenticated"; exit 1; }

# Quality gates (sourced from pr Recipe output)
# - quality_score >= 65
# - risk_score <= 85
# - security_classification != CRITICAL
# - noise_ratio <= 0.30
# - coverage_gap <= 0.40
```

### 2. CREATE — Open the PR

Build the body via HEREDOC to preserve formatting:

```bash
gh pr create \
  --base "$BASE" \
  --head "$SRC" \
  --title "<pr Recipe title>" \
  --body "$(cat <<'EOF'
## Summary
<from pr Recipe>

## Changes
<from pr Recipe Change Classification Table>

## Risk
<from pr Recipe Risk Assessment>

## Test plan
- [ ] <CI suite>
- [ ] <manual verification>
EOF
)" \
  --reviewer "<from pr Recipe>" \
  --label "<inferred from change classification>"
```

For low quality_score (B band 65-74) or first-pass validation, propose `--draft`:

```bash
gh pr create --draft ...   # signals direction-only review
```

### 3. WATCH — Monitor CI to terminal state

```bash
PR_NUMBER=$(gh pr view --json number -q .number)

# Poll with timeout
gh pr checks "$PR_NUMBER" --watch --interval 30 --fail-fast
# Exit codes: 0 = all passed, 1 = one or more failed/cancelled, 8 = pending timeout
```

Surface failing checks with diagnostic context:

```bash
gh pr checks "$PR_NUMBER" --required | awk '$2 == "fail" || $2 == "cancelled"'
gh run view --log-failed   # for the most recent failed run
```

### 4. GATE — Verify merge readiness

```bash
# All required checks green
gh pr view "$PR_NUMBER" --json mergeStateStatus,mergeable,reviewDecision,statusCheckRollup

# Expected:
# mergeStateStatus: CLEAN
# mergeable: MERGEABLE
# reviewDecision: APPROVED
# statusCheckRollup: all SUCCESS
```

Decision table:

| `mergeStateStatus` | Action |
|---|---|
| `CLEAN` | Proceed to MERGE |
| `BLOCKED` | Missing approval or required check; stop |
| `BEHIND` | Base ahead; offer rebase or update-branch |
| `DIRTY` | Merge conflict; route to manual resolution or `reshape` |
| `UNSTABLE` | Non-required check failing; warn + Ask First |
| `HAS_HOOKS` | Pre-merge hook present; verify it will pass |

### 5. MERGE — Ask First, then execute

```bash
# Strategy from `strategy` Recipe output (default: squash for feature branches)
gh pr merge "$PR_NUMBER" --squash --delete-branch
# Alternatives:
# gh pr merge "$PR_NUMBER" --rebase --delete-branch     # linear history
# gh pr merge "$PR_NUMBER" --merge --delete-branch      # preserve merge commit
# gh pr merge "$PR_NUMBER" --auto --squash              # queue when checks pass
```

If repository uses merge queue:

```bash
gh pr merge "$PR_NUMBER" --auto --squash
# GitHub merge queue handles batching and bisection
```

### 6. CLEANUP — Sync base, prune local

```bash
git checkout "$BASE"
git pull --ff-only origin "$BASE"
git branch -D "$SRC" 2>/dev/null || true
git remote prune origin
```

Verify merge landed:

```bash
git log --oneline -1 origin/"$BASE"   # should contain merged commit subject
gh pr view "$PR_NUMBER" --json state -q .state   # MERGED
```

## Hard Gates (cannot bypass)

| Gate | Condition | Action |
|------|-----------|--------|
| Quality | `quality_score < 65` | Stop; route to Zen or Builder for fixes |
| Risk | `risk_score > 85` | Stop unless explicit override with justification |
| Security | `security_classification == CRITICAL` | Blocking Sentinel handoff required |
| CI | Any required check failed | Stop; surface failures |
| Approvals | `reviewDecision != APPROVED` | Stop; request reviewers |
| Conflicts | `mergeStateStatus == DIRTY` | Stop; route to `reshape` or manual rebase |
| Branch protection | Bypass attempt | Refuse; never bypass protection rules |

## Ask First Gates

| Action | Why |
|--------|-----|
| Actual `gh pr merge` execution | Irreversible on shared branches |
| `--admin` flag (bypass protection) | Compliance and audit risk |
| Force-merge over `UNSTABLE` state | Non-required checks may signal real issues |
| Merge to default branch outside business hours | Reduced rollback bandwidth |
| Skip merge queue | Defeats batching/bisection safety |
| Direct merge without squash on `feat/*` branches | Pollutes history |

## Never

- Auto-merge without explicit user consent
- Use `--admin` or otherwise bypass branch protection
- Delete unmerged branches
- Skip required CI checks
- Merge with failing security scans
- Force-push to the PR branch after approval without re-requesting review

## Risks

| Risk | Mitigation |
|------|------------|
| Approved PR merged after silent rebase changes diff | `--require-review-after-push` policy; warn if HEAD changed after last approval |
| CI passes but post-merge integration fails | Recommend merge queue for trunk-based teams |
| Merge race with another PR touching same files | Detect via `mergeStateStatus`; refresh and re-watch |
| Auto-merge fires before reviewers see latest push | Use `--auto` only when no further changes planned |
| Deleted branch contained unmerged work | Verify `gh pr view --json state` == MERGED before deletion |
| CI configuration missing required checks | Discovery step lists branch protection rules; warn if minimal |

## Rollback

Pre-merge rollback (PR open):

```bash
gh pr close "$PR_NUMBER" --comment "Rolling back: <reason>"
# Branch remains; resume after fixes
```

Post-merge rollback (already merged):

```bash
# Revert commit on base (preferred — preserves history)
gh pr revert "$PR_NUMBER"   # opens a revert PR
# OR manual:
git checkout "$BASE" && git pull
git revert -m 1 <merge-commit-sha>
git push origin "$BASE"
```

If destructive recovery is needed (force-push reversal), escalate to user; never auto-execute.

## Verification Checklist

Deliver this with every `ship` output:

- [ ] All preconditions satisfied (clean tree, pushed, base synced, `gh` authed)
- [ ] All hard gates passed (quality, risk, security, CI, approvals)
- [ ] PR title and body match `pr` Recipe output
- [ ] Reviewers requested per CODEOWNERS + expertise routing
- [ ] CI watched to terminal state (no premature merge)
- [ ] `mergeStateStatus == CLEAN` before merge
- [ ] Merge strategy matches `strategy` Recipe choice
- [ ] Branch deleted both locally and remotely
- [ ] Base branch synced post-merge
- [ ] PR final state confirmed as `MERGED`

## Output Template

```markdown
## Guardian Ship Plan

**Source**: `feat/payment-webhook` (HEAD: a1b2c3d)
**Base**: `origin/main`
**PR**: #1234 (to be created) | existing #1234
**Strategy**: squash + delete-branch
**Quality**: 88/100 (A) | **Risk**: Low (22/100) | **Security**: NEUTRAL

### Preflight
- Working tree: clean
- Base sync: up-to-date
- `gh` auth: OK
- Required checks discovered: `ci/test`, `ci/lint`, `ci/security-scan`

### Execution Script (proposal — Ask First on MERGE)

\```bash
# PREFLIGHT, CREATE, WATCH, GATE — see Command Recipes
# MERGE step prompts before execution
gh pr merge 1234 --squash --delete-branch
\```

### Hard Gates
- [x] quality_score 88 >= 65
- [x] risk_score 22 <= 85
- [x] security NEUTRAL
- [ ] CI to be verified at WATCH
- [ ] Approval to be verified at GATE

### Rollback
\```bash
gh pr revert 1234
\```
```

## Orbit Boundary

- `ship` consumes `pr` Recipe output as input — it does not re-derive title/body/reviewers
- `ship` consumes `strategy` Recipe output for merge mode — defaults to `--squash` when absent
- For XXL/MEGA branches, refuse `ship` and route to `split` first
- For PRs requiring deep architecture review, route to `judge` before MERGE phase
- Release-coordinated merges (multiple dependent PRs) hand off to `launch`
- Auto-bisection of failing merge queue batches stays in merge queue's domain — `ship` only reports outcomes
