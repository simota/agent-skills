# Sweep Detection Strategy Reference

Purpose: thresholds and decision cues for candidate prioritization across file types, risk levels, and git history.

## Contents

1. Detection by file type
2. Detection by risk level
3. Quantitative thresholds
4. Confidence-gated flow
5. Git history checks

## By File Type

| File Type | Primary Method | Risk | Tooling |
|-----------|----------------|------|---------|
| Source code | Import and symbol analysis | High | `knip`, `ts-prune`, `vulture`, `staticcheck` |
| Assets | Reference search | Medium | `rg`, custom scripts |
| Config | Tool and workflow verification | Medium | Manual + scripts |
| Dependencies | Import and script scan | Low | `knip`, `depcheck`, package-manager tooling |
| Build output | `.gitignore` and VCS check | Low | `git status`, ignore rules |
| Duplicates | Hash comparison | Medium | `md5`, `fdupes`, custom scripts |

## By Risk Level

| Risk | Typical Targets | Required Approach |
|------|-----------------|-------------------|
| Critical | Core source, entry points, configs | Manual review only |
| High | Feature code, tests, framework files | Verify all references and conventions |
| Medium | Assets, utilities, duplicates | Check direct and indirect usage |
| Low | Cache, temp, committed artifacts | Safe to propose once verified |

## Quantitative Thresholds

### File Age

| Age | Priority | Meaning |
|-----|----------|---------|
| `< 7 days` | Very Low | Likely still in active use |
| `7-30 days` | Low | Verify before deletion |
| `30-90 days` | Medium | Investigate usage |
| `90-365 days` | High | Strong stale candidate |
| `> 365 days` | Very High | Likely unused, still verify references |

### File Size

| Size | Impact | Action |
|------|--------|--------|
| `< 1 KB` | Low | Standard verification |
| `1-10 KB` | Low | Standard verification |
| `10-100 KB` | Medium | Check reuse potential |
| `100 KB - 1 MB` | High | Ask first and review carefully |
| `> 1 MB` | Very High | Investigate before proposing deletion |

### Reference Count

| References | Meaning | Action |
|------------|---------|--------|
| `0` | Orphan candidate | Strong candidate |
| `1 (self only)` | Dead-code candidate | Verify no entry-point role |
| `1-2` | Low usage | Check whether references are live |
| `3+` | Active | Usually keep |

### Dependency Metrics

| Metric | Threshold | Meaning |
|--------|-----------|---------|
| Unused exports | `> 50%` | File may need refactoring or pruning |
| Circular deps | `Any` | Investigate before cleanup |
| Transitive deps | `> 10` | Treat as core or central utility |

## Confidence-Gated Flow

Use this order:

1. Skip anything in exclusions or never-delete lists.
2. Check whether ignored or generated output is committed.
3. Check imports and references.
4. Check config or build ownership.
5. Check duplicates.
6. Apply confidence scoring:
   - `>=90`: batch proposal
   - `70-89`: individual review
   - `50-69`: manual review queue
   - `30-49`: keep
   - `<30`: never delete

## Git History Verification

```bash
git log -1 --format="%ai %an" -- path/to/file
git log --oneline -- path/to/file
git log --diff-filter=D --name-only -- path/to/file
git log --diff-filter=A --format="%h %s" -- path/to/file
git log --all --grep="filename"
```

### Git-Based Decision Cues

| Criterion | Safer to Delete | Caution Required |
|-----------|-----------------|------------------|
| Last modified | `> 6 months ago` | `< 1 month ago` |
| Commit frequency | `1-2 commits total` | many edits over time |
| Last author | bot or maintenance actor | core contributor |
| Commit intent | `temp`, `wip`, `test` | feature or release work |
| Delete/restore history | never restored | restored before |
