# Report Templates

Purpose: Use these canonical report shapes when Harvest must emit summary, detailed, individual, release-note, or quality-trend outputs.

## Contents

- Category detection rules
- Summary report
- Detailed list
- Individual work report
- Release notes
- Quality trends
- Judge feedback integration

## Category Detection Rules

### Prefix mapping

| Prefix | Category |
|--------|----------|
| `feat:` / `feature:` | `feat` |
| `fix:` / `bugfix:` | `fix` |
| `refactor:` | `refactor` |
| `docs:` / `doc:` | `docs` |
| `test:` / `tests:` | `test` |
| `chore:` | `chore` |
| `perf:` | `perf` |
| `style:` | `style` |
| `ci:` | `ci` |
| `build:` | `build` |
| `security:` | `security` |
| `deprecate:` | `deprecated` |

### Label fallback

| Label | Category |
|-------|----------|
| `enhancement`, `feature` | `feat` |
| `bug`, `bugfix` | `fix` |
| `refactoring` | `refactor` |
| `documentation` | `docs` |

## Summary Report

Required sections:

```markdown
# PR Summary Report

**Period:** {start_date} - {end_date}
**Repository:** {repository}
**Generated:** {generation_date}

## Overview
| Metric | Value |
|--------|-------|
| Total PRs | {total} |
| Merged | {merged} ({merged_percent}%) |
| Open | {open} ({open_percent}%) |
| Closed without merge | {closed} ({closed_percent}%) |

## Category Breakdown
| Category | Count | Notes |
|----------|-------|-------|

## Notable Observations
- {observation_1}
- {observation_2}
```

## Detailed List

Required sections:

```markdown
# PR Detailed List

**Period:** {start_date} - {end_date}
**Repository:** {repository}
**Total:** {total_count} PRs

## Merged PRs ({merged_count})
| # | Title | Author | Labels | Created | Merged | Changes |
|---|-------|--------|--------|---------|--------|---------|

## Open PRs ({open_count})
| # | Title | Author | Labels | Created | Age |
|---|-------|--------|--------|---------|-----|

## Closed PRs ({closed_count})
| # | Title | Author | Labels | Created | Closed |
|---|-------|--------|--------|---------|--------|
```

## Individual Work Report

Required sections:

```markdown
# Individual Work Report

**Author:** @{username}
**Period:** {start_date} - {end_date}
**Repository:** {repository}

## Summary
| Metric | Value |
|--------|-------|
| PRs Created | {created_count} |
| PRs Merged | {merged_count} |
| PRs Open | {open_count} |
| Estimated Hours | {estimated_hours} |

## PR Activity
| # | Title | Category | Status | Changes | Estimated Hours |
|---|-------|----------|--------|---------|-----------------|

## Notes
- Work hours are estimated.
- Do not use this report for ranking people.
```

## Release Notes

Use human-facing language and group changes with Keep a Changelog categories.

```markdown
# Release Notes

## {version}

**Release Date:** {release_date}
**Tag:** {tag}
**Commits:** {commit_range}

### Added
- {added_item}

### Changed
- {changed_item}

### Deprecated
- {deprecated_item}

### Removed
- {removed_item}

### Fixed
- {fixed_item}

### Security
- {security_item}
```

Rules:
- Highlight breaking changes before normal changes.
- Omit internal-only refactors unless they change user-facing behavior.
- Use ISO `YYYY-MM-DD` dates.

## Quality Trends Report

Use this when `Judge` feedback exists.

```markdown
# Code Quality Trends Report

**Period:** {start_date} - {end_date}
**Repository:** {repository}
**Data Source:** Judge Feedback Integration

## Quality Overview
| Metric | Current | Previous | Trend |
|--------|:-------:|:--------:|:-----:|
| Average Quality Score | {avg_score}/100 | {prev_avg_score}/100 | {trend_icon} |
| PR Approval Rate | {approval_rate}% | {prev_approval_rate}% | {trend_icon} |
| Avg Review Cycles | {avg_cycles} | {prev_avg_cycles} | {trend_icon} |

## Trend Table
Week    Score   Approval   Cycles
{week_1}   {s1}      {a1}%      {c1}

## Recommendations
### Immediate Actions
- {action}
### Process Improvements
- {process_action}
### Training Opportunities
- {training_action}
```

## Judge Feedback Integration

When receiving `JUDGE_TO_HARVEST_FEEDBACK`, merge these fields if available:

```bash
jq -r '
  "Approval Rate: \(.quality_metrics.approval_rate * 100 | floor)%\n" +
  "Avg Review Cycles: \(.quality_metrics.avg_review_cycles)\n" +
  "Avg Review Time: \(.quality_metrics.avg_review_time_hours)h"
'
```

## AI Reviewer Caveat (2026)

GitHub Copilot Code Review reached GA in 2025-04 (`docs.github.com/en/copilot/concepts/agents/code-review`) and starting 2026-06-01 will consume GitHub Actions minutes (`github.blog/changelog/2026-04-27-...`). When Harvest reports include review-cycle or approval data:
- Tag reviews authored by `@copilot` or the Copilot reviewer account separately from human reviewers.
- Do not count Copilot review comments as human approval — Copilot leaves a "Comment" review only, never "Approve" or "Request changes", and it does not satisfy required-approval branch protection.
- For quality-trend reports comparing pre/post-Copilot adoption windows, follow the same caveat pattern as the DORA AI period note in `engineering-metrics-pitfalls.md`.

## Delivery Notes

- Output language follows the CLI global config (`settings.json` `language` field, `CLAUDE.md`, `AGENTS.md`, or `GEMINI.md`).
- Filenames remain English kebab-case.
- Translate section copy for the audience, but preserve PR titles in their original language.
