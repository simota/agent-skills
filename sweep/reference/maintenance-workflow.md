# Sweep Maintenance Workflow Reference

Purpose: canonical flow for incremental scans, full scans, baseline updates, Grove handoff processing, and trend tracking.

## Contents

1. Incremental scan
2. Full periodic scan
3. Dependency audit
4. Grove handoff reception
5. Baseline management
6. Trend tracking

## Incremental Scan (Per-PR / Sprint)

Use diff-based scanning for changed or affected files.

```bash
git diff --name-only HEAD~10 -- '*.ts' '*.tsx' '*.js' '*.jsx' '*.py' '*.go' '*.rs'
npx knip --reporter compact --include files,exports
vulture <changed-files> --min-confidence 80
staticcheck -checks U1000 ./<changed-package>/...
```

Also check for stale imports after deletions or renames:

```bash
git diff --name-only --diff-filter=D HEAD~10
```

Output:
- new orphan candidates
- stale imports
- confidence-scored items ready for reporting

## Full Periodic Scan (Sprint-End / Quarterly)

Combine tool output with git-history evidence.

```bash
# TS/JS
npx knip --reporter json > /tmp/knip-report.json

# Python
vulture src/ --min-confidence 60 > /tmp/vulture-report.txt
autoflake --check --remove-all-unused-imports -r src/ > /tmp/autoflake-report.txt

# Go
staticcheck -checks U1000 ./... 2> /tmp/staticcheck-report.txt
deadcode -test ./... > /tmp/deadcode-report.txt

# Git activity
git log --since="6 months ago" --name-only --pretty=format: | sort -u > /tmp/active-files.txt
comm -23 <(git ls-files | sort) <(sort /tmp/active-files.txt) > /tmp/stale-files.txt
```

Use the same confidence thresholds as the main skill:
- `>=90`: batch proposal
- `70-89`: individual review
- `50-69`: manual review
- `<50`: keep

## Dependency Audit (Quarterly)

```bash
npx knip --include dependencies
pip-audit 2>/dev/null
pipdeptree --warn silence | grep -E "^\w"
go mod tidy -v 2>&1 | grep -E "(unused|removed)"
```

## Grove Handoff Reception

When Grove sends `GROVE_TO_SWEEP_HANDOFF`:

1. Receive and parse the YAML payload.
2. Validate each candidate:
   - file still exists
   - primary detection tool agrees
   - git activity reviewed
   - confidence score calculated
3. Categorize:
   - `>=70`: accept into cleanup queue
   - `50-69`: manual verification
   - `<50`: return with a still-referenced note
4. Merge accepted items into the baseline with `source: grove-handoff`.
5. Return feedback using:

```yaml
SWEEP_TO_GROVE_FEEDBACK:
  handoff_date: "YYYY-MM-DD"
  processed: 5
  accepted: 3
  deferred: 1
  rejected: 1
  notes:
    - "config/old-webpack.config.js confirmed unused (confidence: 92)"
    - "src/utils/deprecated-helper.ts has one dynamic import and was deferred"
```

## Baseline Management

Record the current state in `.agents/sweep.md`:

```yaml
SCAN_BASELINE:
  date: "YYYY-MM-DD"
  scan_type: "full"  # or "incremental"
  tool: "knip"
  total_files_scanned: 342
  candidates_found: 15
  candidates_by_confidence:
    batch_delete: 3
    individual_review: 5
    manual_review: 4
    skipped: 3
  deleted_this_cycle: 8
  space_reclaimed_kb: 45
  false_positives: 2
  categories:
    dead_code: 6
    orphan_assets: 3
    unused_deps: 2
    config_remnants: 2
    duplicates: 1
    build_artifacts: 1
```

Rules:
- after each cleanup, record deletions, reclaimed space, and false positives
- incremental scans merge into the current baseline
- full scans replace the prior baseline

## Trend Tracking

Track at least:

| Metric | Good | Watch | Alert |
|--------|------|-------|-------|
| Candidate rate | `<3%` | `3-5%` | `>5%` |
| False positive rate | `<10%` | `10-20%` | `>20%` |
| Stale file growth | decreasing | flat | increasing |
| Cleanup velocity | increasing | flat | decreasing |

If alert conditions persist, escalate to Grove for a structural audit.
