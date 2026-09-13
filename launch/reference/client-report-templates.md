# Client Report Templates

Purpose: Use these templates when Launch must generate client-facing Markdown, HTML, or PDF reports with effort estimates, timelines, and visual summaries.

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
- optional refinement layers from `reference/effort-estimation.md`

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
| 1 | OAuth2 support | <span class="category-feat">🚀 feat</span> | 16.0h | 01/21-01/22 | <span class="status-complete">✅ Completed</span> |
```

For HTML/PDF export with `styles/report-style.css`, preserve these inline HTML spans so the stylesheet can apply category and status colors. CSS does not select cells by their text or emoji. For plain Markdown renderers that remove HTML, use the icon and label alone; the labels remain readable without color.

### Category icons

| Category | Icon | CSS class |
|----------|------|-----------|
| `feat` | `🚀` | `category-feat` |
| `fix` | `🐛` | `category-fix` |
| `refactor` | `🔧` | `category-refactor` |
| `docs` | `📝` | `category-docs` |
| `test` | `🧪` | `category-test` |
| `perf` | `⚡` | `category-perf` |
| `chore` | `📦` | None (default text color) |

### Status icons

| Status | Icon | CSS class |
|--------|------|-----------|
| Completed | `✅` | `status-complete` |
| In progress | `🔄` | `status-progress` |
| Under review | `👀` | `status-review` |
| Paused | `⏸️` | None (default text color) |
| Not started | `⬜` | None (default text color) |

For a decorative text divider, use explicit markup so its alignment and color are applied:

```html
<p class="report-divider" aria-hidden="true">━━━</p>
```

## HTML/PDF Packaging

Prefer repo assets before external tools:

| Need | Preferred asset or script |
|------|---------------------------|
| HTML report generation | `scripts/generate-report.js` |
| HTML template | `templates/client-report.html` |
| Report styling | `styles/report-style.css` |
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
