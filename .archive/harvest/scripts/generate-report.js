#!/usr/bin/env node
/**
 * generate-report.js - PRデータからHTMLレポートを生成
 *
 * 使用方法:
 *   node generate-report.js [options]
 *
 * Options:
 *   --days <n>        過去n日間のPRを取得 (default: 7)
 *   --author <name>   特定の著者でフィルタ
 *   --repo <owner/repo>  リポジトリを指定
 *   --output <file>   出力ファイル名 (default: client-report-YYYY-MM-DD.html)
 *   --template <file> テンプレートファイル (default: templates/client-report.html)
 *   --json            JSONデータのみ出力
 *
 * 例:
 *   node generate-report.js --days 30 --author simota
 *   node generate-report.js --repo owner/repo --output report.html
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

// ============================================
// Configuration
// ============================================

const CONFIG = {
  // Work hours calculation weights by file type
  fileWeights: {
    test: 0.7,      // *.test.*, *.spec.*
    config: 0.5,    // *.json, *.yaml, *.yml, *.toml
    docs: 0.3,      // *.md, *.txt, *.rst
    source: 1.0,    // default
  },
  // Bonus hours for new file creation
  newFileBonus: 0.5,
  // Minimum hours per PR
  minHours: 0.5,
  // Lines per hour base rate
  linesPerHour: 100,
  // Complexity multiplier per changed file
  fileComplexityMultiplier: 0.25,
};

// ============================================
// Argument Parsing
// ============================================

function parseArgs() {
  const args = process.argv.slice(2);
  const options = {
    days: 7,
    author: null,
    repo: null,
    output: null,
    template: 'templates/client-report.html',
    json: false,
  };

  for (let i = 0; i < args.length; i++) {
    switch (args[i]) {
      case '--days':
        options.days = parseInt(args[++i], 10);
        break;
      case '--author':
        options.author = args[++i];
        break;
      case '--repo':
        options.repo = args[++i];
        break;
      case '--output':
        options.output = args[++i];
        break;
      case '--template':
        options.template = args[++i];
        break;
      case '--json':
        options.json = true;
        break;
      case '--help':
        console.log(`
Usage: node generate-report.js [options]

Options:
  --days <n>          Past n days (default: 7)
  --author <name>     Filter by author
  --repo <owner/repo> Specify repository
  --output <file>     Output file name
  --template <file>   Template file path
  --json              Output JSON data only
  --help              Show this help
`);
        process.exit(0);
    }
  }

  return options;
}

// ============================================
// Date Utilities (Cross-platform)
// ============================================

function getStartDate(daysAgo) {
  const date = new Date();
  date.setDate(date.getDate() - daysAgo);
  return date.toISOString().split('T')[0];
}

function formatDate(isoString) {
  if (!isoString) return '-';
  const date = new Date(isoString);
  return `${String(date.getMonth() + 1).padStart(2, '0')}/${String(date.getDate()).padStart(2, '0')}`;
}

function formatDateFull(isoString) {
  if (!isoString) return '-';
  const date = new Date(isoString);
  return `${date.getFullYear()}年${date.getMonth() + 1}月${date.getDate()}日`;
}

// ============================================
// GitHub CLI Wrapper
// ============================================

function fetchPRs(options) {
  const startDate = getStartDate(options.days);

  let cmd = 'gh pr list --state merged --limit 500';
  cmd += ' --json number,title,author,createdAt,mergedAt,additions,deletions,changedFiles,labels,url';

  if (options.repo) {
    cmd += ` -R ${options.repo}`;
  }
  if (options.author) {
    cmd += ` --author ${options.author}`;
  }

  try {
    const result = execSync(cmd, { encoding: 'utf-8', maxBuffer: 10 * 1024 * 1024 });
    const prs = JSON.parse(result);

    // Filter by date
    return prs.filter(pr => pr.mergedAt >= startDate);
  } catch (error) {
    console.error('Error fetching PRs:', error.message);
    process.exit(1);
  }
}

function getRepoName(options) {
  if (options.repo) return options.repo;

  try {
    const result = execSync('gh repo view --json nameWithOwner -q ".nameWithOwner"', {
      encoding: 'utf-8'
    });
    return result.trim();
  } catch {
    return 'Unknown Repository';
  }
}

// ============================================
// Work Hours Calculation
// ============================================

function calculateWorkHours(pr) {
  const { additions, deletions, changedFiles } = pr;
  const totalLines = (additions || 0) + (deletions || 0);

  // Base calculation
  let hours = totalLines / CONFIG.linesPerHour;

  // File complexity bonus
  hours += (changedFiles || 0) * CONFIG.fileComplexityMultiplier;

  // Apply minimum
  hours = Math.max(hours, CONFIG.minHours);

  // Round to 0.5h increments
  return Math.round(hours * 2) / 2;
}

function detectCategory(pr) {
  const title = pr.title.toLowerCase();
  const labels = (pr.labels || []).map(l => l.name.toLowerCase());

  // Check title prefix
  if (title.startsWith('feat:') || title.startsWith('feature:')) return 'feat';
  if (title.startsWith('fix:') || title.startsWith('bugfix:')) return 'fix';
  if (title.startsWith('refactor:')) return 'refactor';
  if (title.startsWith('docs:') || title.startsWith('doc:')) return 'docs';
  if (title.startsWith('test:') || title.startsWith('tests:')) return 'test';
  if (title.startsWith('chore:')) return 'chore';
  if (title.startsWith('perf:')) return 'perf';
  if (title.startsWith('style:')) return 'style';

  // Check labels
  if (labels.includes('enhancement') || labels.includes('feature')) return 'feat';
  if (labels.includes('bug') || labels.includes('bugfix')) return 'fix';
  if (labels.includes('documentation')) return 'docs';
  if (labels.includes('refactoring')) return 'refactor';

  return 'other';
}

// ============================================
// Data Aggregation
// ============================================

function aggregateData(prs, options) {
  const startDate = getStartDate(options.days);
  const endDate = new Date().toISOString().split('T')[0];

  // Process each PR
  const processedPRs = prs.map((pr, index) => ({
    no: index + 1,
    number: pr.number,
    title: pr.title,
    author: pr.author?.login || 'unknown',
    category: detectCategory(pr),
    hours: calculateWorkHours(pr),
    additions: pr.additions || 0,
    deletions: pr.deletions || 0,
    changedFiles: pr.changedFiles || 0,
    createdAt: pr.createdAt,
    mergedAt: pr.mergedAt,
    mergedDate: formatDate(pr.mergedAt),
    url: pr.url,
  }));

  // Aggregate by category
  const byCategory = {};
  processedPRs.forEach(pr => {
    if (!byCategory[pr.category]) {
      byCategory[pr.category] = { count: 0, hours: 0 };
    }
    byCategory[pr.category].count++;
    byCategory[pr.category].hours += pr.hours;
  });

  // Aggregate by date
  const byDate = {};
  processedPRs.forEach(pr => {
    const date = pr.mergedAt?.split('T')[0];
    if (date) {
      if (!byDate[date]) {
        byDate[date] = { count: 0, hours: 0 };
      }
      byDate[date].count++;
      byDate[date].hours += pr.hours;
    }
  });

  // Calculate totals
  const totalHours = processedPRs.reduce((sum, pr) => sum + pr.hours, 0);
  const totalAdditions = processedPRs.reduce((sum, pr) => sum + pr.additions, 0);
  const totalDeletions = processedPRs.reduce((sum, pr) => sum + pr.deletions, 0);

  return {
    meta: {
      projectName: getRepoName(options),
      author: options.author || 'All Contributors',
      startDate,
      endDate,
      startDateFormatted: formatDateFull(startDate),
      endDateFormatted: formatDateFull(endDate),
      generatedAt: new Date().toISOString(),
      generatedAtFormatted: formatDateFull(new Date().toISOString()),
    },
    summary: {
      totalTasks: processedPRs.length,
      totalHours: totalHours.toFixed(1),
      totalAdditions: `+${totalAdditions.toLocaleString()}`,
      totalDeletions: `-${totalDeletions.toLocaleString()}`,
      netChange: totalAdditions - totalDeletions,
      completionRate: '100%',
    },
    prs: processedPRs,
    byCategory,
    byDate,
    charts: {
      daily: generateDailyChartData(byDate, startDate, options.days),
      category: generateCategoryChartData(byCategory),
    },
  };
}

function generateDailyChartData(byDate, startDate, days) {
  const labels = [];
  const data = [];
  const start = new Date(startDate);

  for (let i = 0; i < Math.min(days, 14); i++) {
    const date = new Date(start);
    date.setDate(start.getDate() + i);
    const dateStr = date.toISOString().split('T')[0];
    const label = `${date.getMonth() + 1}/${date.getDate()}`;

    labels.push(label);
    data.push(byDate[dateStr]?.hours || 0);
  }

  return { labels, data };
}

function generateCategoryChartData(byCategory) {
  const categoryLabels = {
    feat: 'Feature',
    fix: 'Bug Fix',
    refactor: 'Refactor',
    docs: 'Documentation',
    test: 'Test',
    chore: 'Chore',
    perf: 'Performance',
    style: 'Style',
    other: 'Other',
  };

  const labels = [];
  const data = [];

  Object.entries(byCategory)
    .sort((a, b) => b[1].hours - a[1].hours)
    .forEach(([cat, stats]) => {
      labels.push(`${categoryLabels[cat] || cat} (${stats.hours.toFixed(1)}h)`);
      data.push(stats.hours);
    });

  return { labels, data };
}

// ============================================
// HTML Generation
// ============================================

function generateHTML(data, templatePath) {
  const scriptDir = path.dirname(__filename);
  const harvestDir = path.dirname(scriptDir);
  const fullTemplatePath = path.isAbsolute(templatePath)
    ? templatePath
    : path.join(harvestDir, templatePath);

  if (!fs.existsSync(fullTemplatePath)) {
    console.error(`Template not found: ${fullTemplatePath}`);
    console.log('Generating standalone HTML...');
    return generateStandaloneHTML(data);
  }

  let html = fs.readFileSync(fullTemplatePath, 'utf-8');

  // Replace meta placeholders
  html = html.replace(/\{\{PROJECT_NAME\}\}/g, data.meta.projectName);
  html = html.replace(/\{\{AUTHOR\}\}/g, data.meta.author);
  html = html.replace(/\{\{START_DATE\}\}/g, data.meta.startDateFormatted);
  html = html.replace(/\{\{END_DATE\}\}/g, data.meta.endDateFormatted);
  html = html.replace(/\{\{GENERATED_DATE\}\}/g, data.meta.generatedAtFormatted);

  // Replace summary placeholders
  html = html.replace(/\{\{TOTAL_TASKS\}\}/g, data.summary.totalTasks);
  html = html.replace(/\{\{TOTAL_HOURS\}\}/g, data.summary.totalHours);
  html = html.replace(/\{\{TOTAL_ADDITIONS\}\}/g, data.summary.totalAdditions);
  html = html.replace(/\{\{COMPLETION_RATE\}\}/g, data.summary.completionRate);

  // Replace chart data
  const dailyLabels = JSON.stringify(data.charts.daily.labels);
  const dailyData = JSON.stringify(data.charts.daily.data);
  const categoryLabels = JSON.stringify(data.charts.category.labels);
  const categoryData = JSON.stringify(data.charts.category.data);

  // Update Chart.js configurations
  html = html.replace(
    /labels:\s*\[['"][^[\]]*['"]\]/g,
    (match, offset) => {
      // Determine which chart based on context
      const before = html.substring(Math.max(0, offset - 200), offset);
      if (before.includes('dailyChart') || before.includes('Daily')) {
        return `labels: ${dailyLabels}`;
      } else if (before.includes('categoryChart') || before.includes('Category')) {
        return `labels: ${categoryLabels}`;
      }
      return match;
    }
  );

  html = html.replace(
    /data:\s*\[\d+(?:\.?\d*)?(?:,\s*\d+(?:\.?\d*)?)*\]/g,
    (match, offset) => {
      const before = html.substring(Math.max(0, offset - 300), offset);
      if (before.includes('dailyChart') || before.includes('Daily')) {
        return `data: ${dailyData}`;
      } else if (before.includes('categoryChart') || before.includes('Category')) {
        return `data: ${categoryData}`;
      }
      return match;
    }
  );

  return html;
}

function generateStandaloneHTML(data) {
  const categoryColors = {
    feat: { bg: '#d4edda', color: '#155724' },
    fix: { bg: '#f8d7da', color: '#721c24' },
    refactor: { bg: '#e2d5f1', color: '#4a2c7a' },
    docs: { bg: '#fff3cd', color: '#856404' },
    test: { bg: '#cce5ff', color: '#004085' },
    other: { bg: '#e9ecef', color: '#495057' },
  };

  const tableRows = data.prs.map(pr => {
    const catStyle = categoryColors[pr.category] || categoryColors.other;
    return `
        <tr>
          <td class="text-center">${pr.no}</td>
          <td>${escapeHtml(pr.title)}</td>
          <td class="text-center"><span class="category-badge" style="background:${catStyle.bg};color:${catStyle.color}">${pr.category.toUpperCase()}</span></td>
          <td class="text-right mono">${pr.hours.toFixed(1)}h</td>
          <td class="text-center">${pr.mergedDate}</td>
          <td class="text-center"><span class="status-badge status-complete">完了</span></td>
        </tr>`;
  }).join('\n');

  return `<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>作業報告書 - ${escapeHtml(data.meta.projectName)}</title>
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <style>
    @page { size: A4; margin: 15mm 12mm; }
    @media print { body { -webkit-print-color-adjust: exact; print-color-adjust: exact; } }
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { font-family: "Hiragino Kaku Gothic ProN", "Yu Gothic", sans-serif; font-size: 10pt; line-height: 1.65; color: #1a1a2e; background: #fff; width: 210mm; margin: 0 auto; padding: 15mm 12mm; }
    h1 { font-size: 24pt; text-align: center; margin-bottom: 6px; color: #16213e; }
    h2 { font-size: 11pt; border-left: 4px solid #16213e; padding-left: 12px; margin: 28px 0 16px; color: #16213e; }
    .subtitle { text-align: center; font-size: 10pt; color: #5a6a7a; margin-bottom: 8px; }
    .report-header { text-align: center; padding-bottom: 20px; margin-bottom: 24px; border-bottom: 2px solid #16213e; }
    .report-meta { display: flex; justify-content: center; gap: 40px; margin-top: 16px; }
    .meta-item { text-align: center; }
    .meta-label { font-size: 8pt; color: #8a9aaa; text-transform: uppercase; }
    .meta-value { font-size: 10pt; font-weight: 600; color: #16213e; }
    .summary-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin: 24px 0; }
    .summary-card { background: #f8f9fb; border: 1px solid #e4e8ed; border-radius: 8px; padding: 20px 16px; text-align: center; }
    .summary-card.primary { border-top: 3px solid #16213e; }
    .summary-value { font-size: 28pt; font-weight: 700; color: #16213e; }
    .summary-unit { font-size: 12pt; color: #5a6a7a; }
    .summary-label { font-size: 8pt; color: #7a8a9a; text-transform: uppercase; margin-top: 8px; }
    .chart-row { display: grid; grid-template-columns: 1.2fr 0.8fr; gap: 20px; margin: 24px 0; }
    .chart-box { background: #fafbfc; border: 1px solid #e4e8ed; border-radius: 8px; padding: 20px; }
    .chart-title { font-size: 9pt; font-weight: 600; color: #3a4a5a; text-align: center; margin-bottom: 16px; text-transform: uppercase; }
    .chart-wrapper { height: 200px; position: relative; }
    table { width: 100%; border-collapse: collapse; margin: 16px 0; font-size: 9pt; }
    thead tr { background: linear-gradient(180deg, #16213e, #1a2a3e); }
    th { color: #fff; font-weight: 600; padding: 12px 10px; text-align: left; font-size: 8pt; text-transform: uppercase; }
    td { padding: 11px 10px; border-bottom: 1px solid #e8ebee; }
    tbody tr:nth-child(even) { background: #fafbfc; }
    tfoot tr { background: #f0f2f5; }
    tfoot td { font-weight: 600; border-top: 2px solid #16213e; }
    .text-right { text-align: right; }
    .text-center { text-align: center; }
    .mono { font-family: "SF Mono", Monaco, monospace; }
    .status-badge { display: inline-block; font-size: 7pt; font-weight: 600; padding: 3px 10px; border-radius: 12px; }
    .status-complete { background: #d4edda; color: #155724; }
    .category-badge { display: inline-block; font-size: 7pt; font-weight: 600; padding: 3px 8px; border-radius: 3px; }
    .report-footer { margin-top: 40px; padding-top: 16px; border-top: 1px solid #e4e8ed; display: flex; justify-content: space-between; font-size: 8pt; color: #9aa; }
  </style>
</head>
<body>
  <header class="report-header">
    <h1>作業報告書</h1>
    <p class="subtitle">${escapeHtml(data.meta.projectName)}</p>
    <div class="report-meta">
      <div class="meta-item">
        <div class="meta-label">報告期間</div>
        <div class="meta-value">${data.meta.startDateFormatted} — ${data.meta.endDateFormatted}</div>
      </div>
      <div class="meta-item">
        <div class="meta-label">担当者</div>
        <div class="meta-value">${escapeHtml(data.meta.author)}</div>
      </div>
    </div>
  </header>

  <section>
    <h2>Executive Summary</h2>
    <div class="summary-grid">
      <div class="summary-card primary">
        <div class="summary-value">${data.summary.totalTasks}</div>
        <div class="summary-label">完了タスク</div>
      </div>
      <div class="summary-card">
        <div class="summary-value">${data.summary.totalHours}<span class="summary-unit">h</span></div>
        <div class="summary-label">総工数</div>
      </div>
      <div class="summary-card">
        <div class="summary-value">${data.summary.totalAdditions}</div>
        <div class="summary-label">追加行数</div>
      </div>
      <div class="summary-card">
        <div class="summary-value">100<span class="summary-unit">%</span></div>
        <div class="summary-label">完了率</div>
      </div>
    </div>
  </section>

  <section>
    <h2>Activity Analysis</h2>
    <div class="chart-row">
      <div class="chart-box">
        <div class="chart-title">Daily Work Hours</div>
        <div class="chart-wrapper"><canvas id="dailyChart"></canvas></div>
      </div>
      <div class="chart-box">
        <div class="chart-title">Category Distribution</div>
        <div class="chart-wrapper"><canvas id="categoryChart"></canvas></div>
      </div>
    </div>
  </section>

  <section>
    <h2>Work Details</h2>
    <table>
      <thead>
        <tr>
          <th style="width:36px" class="text-center">No</th>
          <th>タスク名</th>
          <th style="width:72px" class="text-center">カテゴリ</th>
          <th style="width:56px" class="text-right">工数</th>
          <th style="width:64px" class="text-center">完了日</th>
          <th style="width:64px" class="text-center">状態</th>
        </tr>
      </thead>
      <tbody>
${tableRows}
      </tbody>
      <tfoot>
        <tr>
          <td colspan="3" class="text-right">Total</td>
          <td class="text-right mono">${data.summary.totalHours}h</td>
          <td colspan="2"></td>
        </tr>
      </tfoot>
    </table>
  </section>

  <footer class="report-footer">
    <div>Generated by Harvest Agent</div>
    <div>${data.meta.generatedAtFormatted} 作成</div>
  </footer>

  <script>
    Chart.defaults.font.family = "'Hiragino Kaku Gothic ProN', sans-serif";

    new Chart(document.getElementById('dailyChart'), {
      type: 'bar',
      data: {
        labels: ${JSON.stringify(data.charts.daily.labels)},
        datasets: [{
          data: ${JSON.stringify(data.charts.daily.data)},
          backgroundColor: '#16213e',
          borderRadius: 4
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { display: false } },
        scales: {
          y: { beginAtZero: true, grid: { color: 'rgba(0,0,0,0.04)' } },
          x: { grid: { display: false } }
        }
      }
    });

    new Chart(document.getElementById('categoryChart'), {
      type: 'doughnut',
      data: {
        labels: ${JSON.stringify(data.charts.category.labels)},
        datasets: [{
          data: ${JSON.stringify(data.charts.category.data)},
          backgroundColor: ['#1e6f5c', '#c49000', '#b33939', '#6c5ce7', '#0984e3', '#636e72'],
          borderWidth: 2
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        cutout: '60%',
        plugins: {
          legend: { position: 'bottom', labels: { font: { size: 9 }, padding: 12 } }
        }
      }
    });
  </script>
</body>
</html>`;
}

function escapeHtml(str) {
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

// ============================================
// Main
// ============================================

function main() {
  const options = parseArgs();

  console.log('Fetching PRs...');
  const prs = fetchPRs(options);
  console.log(`Found ${prs.length} PRs`);

  if (prs.length === 0) {
    console.log('No PRs found in the specified period.');
    process.exit(0);
  }

  console.log('Aggregating data...');
  const data = aggregateData(prs, options);

  if (options.json) {
    console.log(JSON.stringify(data, null, 2));
    return;
  }

  console.log('Generating HTML...');
  const html = generateHTML(data, options.template);

  const outputFile = options.output || `client-report-${new Date().toISOString().split('T')[0]}.html`;
  fs.writeFileSync(outputFile, html);
  console.log(`Report generated: ${outputFile}`);
}

main();
