# Sweep Troubleshooting Reference

Purpose: recovery steps for false positives, build breaks, slow scans, and aborted cleanup runs.

Scope boundary:
- This file = **recovery procedures** (restore, abort, scan-perf, exclusion reporting).
- `false-positives.md` = **detection patterns** to prevent the false positive in the first place.
- `language-patterns.md` = **per-language tool selection** (prefer knip over ts-prune/depcheck to reduce the re-export and `@types/*` false positives handled below).

## Common Tool Issues

### `ts-prune` false positives

Problem: re-exported symbols are reported as unused.

```bash
npx ts-prune --ignore "index.ts"
npx knip
```

### `depcheck` and `@types/*`

Problem: type packages are reported as unused.

```bash
npx depcheck --ignores="@types/*"
grep -r "types" tsconfig.json
```

## Build Breaks After Cleanup

Recovery order:
1. Restore from the backup branch: `git checkout backup/pre-cleanup-YYYY-MM-DD`
2. Identify the breaking file from the build or test error
3. Find the missed reference pattern
4. Add the pattern to `.sweepignore` or project notes
5. Re-run cleanup excluding the false positive

## Scan Performance Issues On Large Repositories

```bash
npx depcheck --ignore-dirs="node_modules,dist,coverage"
git diff --name-only HEAD~10 | xargs -I {} sh -c 'echo "Checking {}"'
find src -name "*.ts" | xargs -P 4 -I {} grep -l "unused" {}
```

Prefer incremental scans over full scans when the repository is large and the task is PR-scoped.

## When To Abort Cleanup

Abort when:
- build or tests fail and the cause is unclear
- multiple files show unexpected references
- core infrastructure files appear unused
- git history shows delete-and-restore churn
- the user is uncertain about a critical file

If cleanup must be abandoned, restore from the backup branch first. Only use destructive workspace reset commands on a disposable cleanup branch.

## Reporting False Positives

When a tool misclassifies a candidate:
1. Add a project-specific exclusion in `.sweepignore`
2. Record the pattern in `.agents/sweep.md`
3. Adjust future scans and review templates accordingly
