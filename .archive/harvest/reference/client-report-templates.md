# Client Report Templates

Purpose: Use these templates when Harvest must generate client-facing Markdown, HTML, or PDF reports with effort estimates, timelines, and visual summaries.

## Contents

- Report structure
- Work-hour inputs
- Chart options
- Work-items table
- HTML/PDF packaging
- Command examples

## Work-Hour Inputs

Client reports may use:
- the implemented baseline estimation from `scripts/generate-report.js`
- optional refinement layers from `work-hours.md`

Always label the result as an estimate.

## Client Report Structure

```markdown
# Work Report

**Project:** {project_name}
**Reporting Period:** {start_date} to {end_date}
**Report Date:** {report_date}
**Owner:** {author_name}

## Summary
- Completed Tasks: {completed_count}
- Estimated Hours: {total_hours}h
- Code Changes: +{additions} / -{deletions}

## Work Timeline
{timeline_chart}

## Daily Activity
{daily_activity_chart}

## Hours by Category
{category_breakdown_chart}

## Work Details
{work_items_table}

## Progress Summary
{progress_summary}
```

## Chart Options

| Chart | Best format | Use when |
|------|-------------|----------|
| Timeline | Mermaid `gantt` or ASCII timeline | Showing task periods and sequencing |
| Daily activity | Mermaid `xychart-beta` or ASCII bars | Showing effort over time |
| Category breakdown | Mermaid `pie` or table | Showing effort share by category |
| Progress | ASCII progress bars | PDF-safe summary view |

Use ASCII fallback when Mermaid rendering is unreliable in the target export path.

## Work-Items Table

Canonical table:

```markdown
| No. | Task | Category | Hours | Period | Status |
|:---:|------|:--------:|------:|--------|:------:|
| 1 | OAuth2 support | 🚀 feat | 16.0h | 01/21-01/22 | ✅ Completed |
```

### Category icons

| Category | Icon |
|----------|------|
| `feat` | `🚀` |
| `fix` | `🐛` |
| `refactor` | `🔧` |
| `docs` | `📝` |
| `test` | `🧪` |
| `perf` | `⚡` |
| `chore` | `📦` |

### Status icons

| Status | Icon |
|--------|------|
| Completed | `✅` |
| In progress | `🔄` |
| Under review | `👀` |
| Paused | `⏸️` |
| Not started | `⬜` |

## HTML/PDF Packaging

Prefer repo assets before external tools:

| Need | Preferred asset or script |
|------|---------------------------|
| HTML report generation | `scripts/generate-report.js` |
| HTML template | `templates/client-report.html` |
| Report styling | `styles/harvest-style.css` |
| HTML -> PDF | `scripts/html-to-pdf.sh` |
| Puppeteer fallback | `scripts/puppeteer-pdf.js` |

## Command Examples

```bash
# Weekly client report
node scripts/generate-report.js --days 7 --output client-report-YYYY-MM-DD.html

# Monthly client report for one author
node scripts/generate-report.js --days 30 --author username --output client-report-YYYY-MM-DD.html

# Convert HTML to PDF
./scripts/html-to-pdf.sh client-report-YYYY-MM-DD.html
```

## Delivery Notes

- Keep the report readable for non-engineers.
- Prefer impact, progress, and risks over raw implementation detail.
- Do not expose private repository URLs, sensitive labels, or personal data.
- If the team uses AI coding assistants materially during the reporting window, add a one-line disclosure (e.g., "AI-assisted development was active during this period"). DORA 2025 shows AI shifts throughput and stability in opposite directions — clients reading the LOC and hours columns should know that context.
