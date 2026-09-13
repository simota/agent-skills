#!/usr/bin/env node
/**
 * generate-report.js - PRデータからHTMLレポートを生成
 *
 * 使用方法:
 *   node generate-report.js [options]
 *
 * Options:
 *   --days <n>        今日を含むUTC暦日n日間のPRを取得 (default: 7)
 *   --author <name>   特定の著者でフィルタ
 *   --repo <owner/repo>  リポジトリを指定
 *   --output <file>   出力ファイル名 (default: client-report-YYYY-MM-DD.html)
 *   --template <file> 作業ディレクトリ基準のテンプレート (default: bundled client-report.html)
 *   --json            JSONデータのみ出力
 *
 * 例:
 *   node generate-report.js --days 30 --author simota
 *   node generate-report.js --repo owner/repo --output report.html
 */

const { execFileSync } = require('child_process');
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
    template: path.join(__dirname, '../templates/client-report.html'),
    json: false,
    asOf: new Date().toISOString(),
  };

  for (let i = 0; i < args.length; i++) {
    const flag = args[i];
    if (['--days', '--author', '--repo', '--output', '--template'].includes(flag)
        && (!args[i + 1] || args[i + 1].startsWith('--'))) {
      throw new Error(`Missing value for ${flag}`);
    }
    switch (flag) {
      case '--days':
        if (!/^[1-9]\d*$/.test(args[++i]) || Number(args[i]) > 36600) {
          throw new Error('--days must be an integer between 1 and 36600');
        }
        options.days = Number(args[i]);
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
        options.template = path.resolve(args[++i]);
        break;
      case '--json':
        options.json = true;
        break;
      case '--help':
        console.log(`
Usage: node generate-report.js [options]

Options:
  --days <n>          UTC calendar days including today (1-36600, default: 7)
  --author <name>     Filter by author
  --repo <owner/repo> Specify repository
  --output <file>     Output file name
  --template <file>   Template file path
  --json              Output JSON data only
  --help              Show this help
`);
        process.exit(0);
      default:
        throw new Error(`Unknown option: ${flag}`);
    }
  }

  if (options.repo && !/^[A-Za-z0-9_.-]+\/[A-Za-z0-9_.-]+$/.test(options.repo)) {
    throw new Error('--repo must be owner/repo');
  }
  if (!options.json && !fs.statSync(options.template).isFile()) {
    throw new Error(`Template is not a file: ${options.template}`);
  }
  return options;
}

// ============================================
// Date Utilities (Cross-platform)
// ============================================

function getStartDate(days, asOf) {
  const date = new Date(asOf);
  date.setUTCDate(date.getUTCDate() - days + 1);
  return date.toISOString().split('T')[0];
}

function formatDate(isoString) {
  if (!isoString) return '-';
  const date = new Date(isoString);
  return `${String(date.getUTCMonth() + 1).padStart(2, '0')}/${String(date.getUTCDate()).padStart(2, '0')}`;
}

function formatDateFull(isoString) {
  if (!isoString) return '-';
  const date = new Date(isoString);
  return `${date.getUTCFullYear()}年${date.getUTCMonth() + 1}月${date.getUTCDate()}日`;
}

// ============================================
// GitHub CLI Wrapper
// ============================================

function fetchPRs(options) {
  const startDate = getStartDate(options.days, options.asOf);

  const args = ['pr', 'list', '--state', 'merged', '--limit', '501',
    '--search', `merged:>=${startDate}`,
    '--json', 'number,title,author,createdAt,mergedAt,additions,deletions,changedFiles,labels,url'];
  if (options.repo) args.push('--repo', options.repo);
  if (options.author) args.push('--author', options.author);

  const result = execFileSync('gh', args, { encoding: 'utf-8', maxBuffer: 10 * 1024 * 1024 });
  const prs = JSON.parse(result);
  if (!Array.isArray(prs)) throw new Error('GitHub returned an invalid PR list');
  if (prs.length > 500) {
    throw new Error('More than 500 PRs match; narrow --days or --author to avoid a partial report');
  }
  const endDate = options.asOf.split('T')[0];
  return prs.filter(pr => pr.mergedAt && pr.mergedAt.slice(0, 10) >= startDate
    && pr.mergedAt.slice(0, 10) <= endDate);
}

function getRepoName(options) {
  if (options.repo) return options.repo;

  try {
    const result = execFileSync('gh', ['repo', 'view', '--json', 'nameWithOwner', '-q', '.nameWithOwner'], {
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

  // Conventional Commit scopes and breaking-change markers are optional.
  const prefix = title.match(/^(feat|feature|fix|bugfix|refactor|docs|doc|test|tests|chore|perf|style)(?:\([^)]*\))?!?:/);
  if (prefix) {
    const aliases = { feature: 'feat', bugfix: 'fix', doc: 'docs', tests: 'test' };
    return aliases[prefix[1]] || prefix[1];
  }

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
  const startDate = getStartDate(options.days, options.asOf);
  const endDate = options.asOf.split('T')[0];

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
      generatedAt: options.asOf,
      generatedAtFormatted: formatDateFull(options.asOf),
    },
    summary: {
      totalTasks: processedPRs.length,
      totalHours: totalHours.toFixed(1),
      totalAdditions: `+${totalAdditions.toLocaleString()}`,
      totalDeletions: `-${totalDeletions.toLocaleString()}`,
      netChange: totalAdditions - totalDeletions,
      completionRate: processedPRs.length ? '100%' : '0%',
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

  for (let i = 0; i < days; i++) {
    const date = new Date(start);
    date.setUTCDate(start.getUTCDate() + i);
    const dateStr = date.toISOString().split('T')[0];
    const label = `${date.getUTCMonth() + 1}/${date.getUTCDate()}`;

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
  const html = fs.readFileSync(templatePath, 'utf-8');
  const textValues = {
    PROJECT_NAME: data.meta.projectName,
    AUTHOR: data.meta.author,
    START_DATE: data.meta.startDateFormatted,
    END_DATE: data.meta.endDateFormatted,
    GENERATED_DATE: data.meta.generatedAtFormatted,
    TOTAL_TASKS: data.summary.totalTasks,
    TOTAL_HOURS: data.summary.totalHours,
    TOTAL_ADDITIONS: data.summary.totalAdditions,
    COMPLETION_RATE: data.summary.completionRate,
  };
  const values = Object.fromEntries(Object.entries(textValues)
    .map(([key, value]) => [key, escapeHtml(value)]));
  Object.assign(values, {
    TABLE_ROWS: generateTableRows(data.prs),
    DAILY_LABELS: JSON.stringify(data.charts.daily.labels),
    DAILY_DATA: JSON.stringify(data.charts.daily.data),
    CATEGORY_LABELS: JSON.stringify(data.charts.category.labels),
    CATEGORY_DATA: JSON.stringify(data.charts.category.data),
  });
  // A single callback pass avoids interpreting $& or template-looking user text.
  return html.replace(/\{\{([A-Z_]+)\}\}/g, (match, key) =>
    Object.hasOwn(values, key) ? values[key] : match);
}

function generateTableRows(prs) {
  return prs.map(pr => `
        <tr>
          <td class="text-center">${pr.no}</td>
          <td>${escapeHtml(pr.title)}</td>
          <td class="text-center"><span class="category-tag category-${pr.category}">${pr.category.toUpperCase()}</span></td>
          <td class="text-right font-mono">${pr.hours.toFixed(1)}h</td>
          <td class="text-center">${pr.mergedDate}</td>
          <td class="text-center"><span class="status-complete">完了</span></td>
        </tr>`).join('\n');
}

function escapeHtml(str) {
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

// ============================================
// Main
// ============================================

function main() {
  const options = parseArgs();

  console.error('Fetching PRs...');
  const prs = fetchPRs(options);
  console.error(`Found ${prs.length} PRs`);

  if (prs.length === 0) {
    console.error('No PRs found in the specified period.');
  }

  console.error('Aggregating data...');
  const data = aggregateData(prs, options);

  if (options.json) {
    console.log(JSON.stringify(data, null, 2));
    return;
  }

  console.log('Generating HTML...');
  const html = generateHTML(data, options.template);

  const outputFile = options.output || `client-report-${options.asOf.split('T')[0]}.html`;
  fs.writeFileSync(outputFile, html);
  console.log(`Report generated: ${outputFile}`);
}

try {
  main();
} catch (error) {
  console.error('Error:', error.message);
  process.exitCode = 1;
}
