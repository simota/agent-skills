# Sweep Safe Deletion Protocol Reference

Purpose: canonical rules for deletion readiness, rollback preparation, confidence scoring, cleanup reporting, and Grove handoff handling.

## Contents

1. Pre-deletion checklist
2. Deletion categories
3. Rollback preparation
4. Confidence scoring
5. Cleanup report template
6. `GROVE_TO_SWEEP_HANDOFF` handling
7. Dependency report format

## Pre-Deletion Checklist

Before recommending any deletion, confirm all applicable checks:

- [ ] No active imports or runtime references
- [ ] No dynamic references or string-based loading
- [ ] No config, alias, or build-tool references
- [ ] No test, fixture, or story dependency
- [ ] Git history reviewed
- [ ] Not an entry point, exported package target, or public CLI
- [ ] No external documentation reference

## Deletion Categories

| Category | Meaning | User Confirmation |
|----------|---------|-------------------|
| Safe to Delete | Evidence is strong and reversible | Batch confirmation |
| Verify Before Delete | Evidence is promising but incomplete | Individual confirmation |
| Potentially Needed | Signals conflict or context is weak | Detailed review required |
| Do Not Delete | Safety boundary or active usage exists | Explain why it stays |

## Rollback Preparation

Always prepare rollback before any executed cleanup:

```bash
# Create a restoration branch before cleanup
git checkout -b backup/pre-cleanup-YYYY-MM-DD

# After confirmation, perform cleanup on the working branch
git checkout original-branch
```

Use the backup branch as the primary restoration path. If cleanup affects dependencies, also snapshot manifest and lockfile changes before continuing.

## Confidence Scoring

### Score Calculation

| Factor | Weight | Criteria |
|--------|--------|----------|
| Reference Count | 30% | `0 refs = 30`, `1 ref = 15`, `2+ refs = 0` |
| File Age | 20% | `>1 year = 20`, `6-12 months = 15`, `1-6 months = 5`, `<1 month = 0` |
| Git Activity | 15% | No recent commits `= 15`, some activity `= 5`, active `= 0` |
| Tool Agreement | 20% | Multiple tools `= 20`, single tool `= 10`, manual only `= 5` |
| File Location | 15% | `test/docs = 15`, `utils = 10`, `core/lib = 0` |

### Score Interpretation

| Score | Confidence | Action |
|-------|------------|--------|
| `90-100` | Very High | Batch deletion proposal |
| `70-89` | High | Individual review and confirmation |
| `50-69` | Medium | Manual review queue |
| `30-49` | Low | Keep unless manually re-verified |
| `0-29` | Very Low | Do not delete |

## Cleanup Report Template

### Executive Summary

```markdown
## Repository Cleanup Report

**Scan Date:** YYYY-MM-DD
**Repository:** [repo-name]
**Total Files Scanned:** X
**Cleanup Candidates Found:** Y
**Estimated Space Savings:** Z KB/MB

### Summary by Category

| Category | Count | Size | Risk |
|----------|-------|------|------|
| Dead Code | X | XX KB | High |
| Orphan Assets | X | XX KB | Medium |
| Unused Dependencies | X | - | Low |
| Build Artifacts | X | XX KB | Low |
| Duplicates | X | XX KB | Medium |
| Config Remnants | X | XX KB | Medium |
| **Total** | **X** | **XX KB** | - |
```

### Detailed Finding Format

```markdown
### [CATEGORY-NNN] File/Item Name

- **Path:** `src/path/to/file.ts`
- **Category:** Dead Code / Orphan Asset / Unused Dependency / Build Artifact / Duplicate / Config Remnant
- **Size:** XX KB
- **Risk Level:** Critical / High / Medium / Low
- **Last Modified:** YYYY-MM-DD (X months ago)
- **Last Author:** [git author]

**Evidence:**
- No imports found in the codebase
- No references in: [files checked]
- Similar file exists: [if duplicate]

**Recommendation:** Delete / Review / Keep
**Reason:** [Explanation]
**Confidence Score:** XX/100
```

## `GROVE_TO_SWEEP_HANDOFF` Reception

When receiving `GROVE_TO_SWEEP_HANDOFF` from Grove:

1. Parse the YAML payload and extract candidates.
2. Validate each candidate:
   - file still exists
   - primary detection tool agrees
   - git history is checked
   - confidence score is calculated
3. Categorize:
   - `>=70`: accept into cleanup queue
   - `50-69`: defer for manual verification
   - `<50`: return to Grove with a still-referenced note
4. Tag accepted items with `source: grove-handoff`.
5. Report processing results back to Grove.

For full scan cadence and baseline updates, see `maintenance-workflow.md`.

## Dependency Report Format

```markdown
### Unused Dependencies

| Package | Type | Size | Last Used | Recommendation |
|---------|------|------|-----------|----------------|
| lodash | prod | 1.2MB | Never imported | Remove |
| @types/node | dev | 50KB | Type-only, keep | Keep |
```
