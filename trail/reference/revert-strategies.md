# Revert Strategies Reference

Purpose: Decision framework for undoing changes safely. Covers `git revert` (history-preserving inverse commit) vs. `git reset --hard` (history rewrite), merge-commit reverts with `-m`, partial reverts via `checkout`, revert-of-revert when reintroducing fixed work, and the post-revert verification + communication checklist. The goal is the smallest, safest, most auditable undo that restores correctness without orphaning teammates' work.

## Scope Boundary

- **trail `revert`**: choose and document the revert strategy. Produces a revert plan + verification checklist + comms template. Does not push to remote unilaterally.
- **trail `regression` / `bisect` (elsewhere)**: identify *what* to revert. `revert` decides *how* to undo it.
- **trail `blame` / `history` (elsewhere)**: post-revert archaeology — confirm the revert didn't reintroduce older bugs.
- **Triage (elsewhere)**: live incident command. `revert` is the technique Triage may invoke; routing depends on whether incident is open (Triage owns) or resolved (Trail owns).
- **Builder (elsewhere)**: executes the fix-forward path when revert is rejected or high-risk.
- **Guardian (elsewhere)**: PR strategy for reintroducing reverted work (revert-of-revert split into smaller PRs).
- **Scout (elsewhere)**: post-revert RCA if the original bug's root cause is still unclear.
- **Launch (elsewhere)**: rollback at the release/feature-flag level, not the commit level.

## Workflow

```
SCOPE    →  identify target commit(s), branch context (main/release/feature)
         →  classify: single commit / range / merge commit / partial file
         →  audit downstream: who is built on top? open PRs? deployed?

DECIDE   →  pick strategy via decision matrix below
         →  if shared/pushed → revert (history-preserving)
         →  if local-only and clean undo desired → reset --hard (with reflog backup)
         →  if merge → git revert -m <parent> with parent rationale documented

EXECUTE  →  create branch backup: git branch backup/pre-revert-$(date +%s)
         →  run the chosen command in a worktree if shared
         →  resolve conflicts honoring "what we want to undo, not what we want to keep"

VERIFY   →  run the failing test that motivated the revert — must now pass
         →  run smoke + regression suite — no new failures
         →  diff against the pre-bug ancestor — confirm intended state restored

COMMS    →  post revert notice (template below) before merging
         →  link: incident, breaking commit, revert commit, fix-forward plan
         →  notify authors of dependent commits/PRs

PLAN     →  schedule the revert-of-revert (reintroducing fixed work) if applicable
         →  hand off to Builder (forward fix) and Guardian (PR strategy)
```

## Decision Matrix: revert vs. reset

| Situation | Strategy | Rationale |
|-----------|----------|-----------|
| Commit pushed to shared branch | `git revert <sha>` | Reset rewrites history, breaks teammates |
| Commit local, branch not pushed | `git reset --hard <sha>^` (with reflog) | Cleaner history, no inverse commit noise |
| Hot-fix on production, multiple commits | `git revert <oldest>..<newest>` (range, no `--no-commit`) | One inverse per commit, easy to bisect later |
| Merge commit on main from feature branch | `git revert -m 1 <merge-sha>` | `-m 1` keeps mainline, drops the feature side |
| Bad merge from main into feature (rare) | `git revert -m 2 <merge-sha>` | `-m 2` keeps feature, drops what main brought in |
| Single file change inside a multi-file commit | `git checkout <sha>^ -- path/to/file` + new commit | Surgical undo, leaves rest intact |
| Single hunk inside a file | `git checkout -p <sha>^ -- path/to/file` | Interactive hunk-level revert |
| Reverted work is now ready to ship again | `git revert <revert-sha>` (revert-of-revert) | Reintroduces the original change cleanly |
| Force-push to main/master | NEVER without explicit operator approval | Destroys others' work; almost always wrong |

## Merge Commit Revert: `-m` Parent Selection

```
       A---B---C  (feature)
      /         \
*---D---E---F---M---G  (main)
```

- `M` is the merge commit. `git revert -m 1 M` undoes A,B,C from main (mainline = parent 1 = E).
- `git revert -m 2 M` undoes D,E,F from main (feature = parent 2 = C). Almost never what you want.
- Confirm with `git show M` — first listed parent is `-m 1`.
- Document the choice in the revert commit message: `Revert "Merge feature/x" (-m 1: drop feature, keep main)`.

## Partial Revert Techniques

| Scope | Command | When |
|-------|---------|------|
| Whole commit | `git revert <sha>` | Default — preserves history |
| Specific file at old state | `git checkout <sha>^ -- file` then commit | Multi-file commit, only one file regressed |
| Specific hunk | `git checkout -p <sha>^ -- file` | Single function regressed inside larger refactor |
| Specific lines via patch | `git show <sha> -- file \| git apply -R --include=file` | Scriptable, CI-friendly |
| Range with conflicts batched | `git revert --no-commit A..B && git commit` | Single revert commit for a range |

## Hot-Fix Revert Chains

For production hot-fixes:
1. Branch from the deployed tag, not from `main` HEAD: `git checkout -b hotfix/revert-x v2.4.1`.
2. Apply the revert there.
3. Tag and deploy the hot-fix (`v2.4.2`).
4. Merge the hot-fix branch back to `main` to keep histories aligned.
5. Plan the revert-of-revert (reintroduction with the bug fixed) as a separate PR — never bundle.

## Post-Revert Verification Checklist

- [ ] The failing test/symptom that motivated the revert no longer reproduces.
- [ ] Full regression suite green at the post-revert SHA.
- [ ] Build artifacts identical (or expectedly different) compared to pre-bug ancestor.
- [ ] No new lint/type errors introduced by conflict resolution.
- [ ] Open PRs targeting the reverted commit have been notified and rebased.
- [ ] Database migrations: if reverted commit included a migration, decide reversal vs. forward-only and document.
- [ ] Feature flags: any flag introduced by the reverted commit is removed or defaulted off.
- [ ] Deployment manifest, lockfile, version bump match the post-revert state.
- [ ] Reflog / backup branch exists for 30 days (`backup/pre-revert-<ts>`).

## Communication Template

```
Subject: Revert: <one-line summary of reverted change>

What: Reverted <SHA> ("<commit subject>") on <branch>.
Why: <symptom> — see incident #<id> / bisect report at <link>.
How: `git revert <sha>` / `git revert -m 1 <merge-sha>` / partial via checkout.
Verification: <test/check> now passes; full suite green at <revert-sha>.
Impact: <users/services affected>; rollback window <start>-<end>.
Next: Fix-forward owner: <name>. ETA for revert-of-revert: <date or TBD>.
Authors of dependent commits notified: <names>.
Backup branch: backup/pre-revert-<ts> (kept 30 days).
```

## Anti-Patterns

- `git reset --hard` on a shared branch — silently destroys teammates' commits and forces force-push. Always use `git revert` for pushed history.
- Reverting a merge commit without `-m` — git refuses; engineers then run `reset --hard` instead. Always specify `-m` and document the parent choice.
- Reintroducing reverted work without revert-of-revert — manually re-applying the original diff confuses bisect later. Use `git revert <revert-sha>` to restore cleanly.
- Bundling revert + forward fix in one commit — defeats the audit trail. Revert and fix-forward are separate commits, ideally separate PRs.
- Skipping the backup branch — if the revert is wrong, recovery without `backup/pre-revert-*` requires reflog spelunking under time pressure. Always tag a backup first.
- Reverting without rerunning the originating test — confirm the symptom actually disappears; otherwise the revert is theater.
- Force-push to recover from a botched revert — compounds the damage. Use forward-only `git revert <bad-revert-sha>` instead.
- No comms before merge — downstream PR authors discover the revert via merge conflicts. Always notify before merging the revert.
- Reverting database migrations as code-only — schema diverges from code. Migrations need an explicit down migration or forward-only "no-op-ify" patch.

## Handoff

- **To Builder**: revert plan executed; fix-forward implementation owns the corrected reintroduction (paired with revert-of-revert).
- **To Guardian**: PR strategy for revert-of-revert — split large reverted features into reviewable chunks.
- **To Triage**: if the revert was part of an open incident → return control with revert SHA, verification status, and remaining risks.
- **To Radar**: missing regression test that would have caught the originally-reverted bug.
- **To Launch**: if rollback is better handled at the deploy/feature-flag layer than the commit layer.
- **To Scout**: if root cause of the originally-reverted bug is still unknown after revert — Scout investigates before reintroduction.
- **To Sentinel**: if the reverted commit was a security fix, escalate immediately — reverting a security patch reopens the vulnerability.
