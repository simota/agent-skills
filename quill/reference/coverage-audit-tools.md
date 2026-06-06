# Coverage Audit Tools

Purpose: Read this when Quill must measure JSDoc coverage, type coverage, link health, example coverage, or produce documentation audit reports.

Contents:
- `Coverage Metrics Targets`: target thresholds and measurement intent
- `Documentation Coverage Script`: exported API JSDoc audit workflow
- `Link Health Checker`: broken-link validation and retry behavior
- `Type Coverage Tools`: `type-coverage` usage and audit flow
- `CI Integration`: automation patterns for recurring checks
- `Report Template`: reusable documentation health report format

## Coverage Metrics Targets

| Metric | Target | How to Measure |
|--------|--------|----------------|
| Public API JSDoc | 100% | Functions/classes without JSDoc |
| Type Coverage | 95%+ | `any` types remaining |
| README Sections | 100% | Essential sections present |
| Link Health | 100% | No broken links |
| Example Coverage | 80%+ | Public APIs with @example |

## Documentation Coverage Script

```typescript
// scripts/doc-coverage.ts
import { Project, SyntaxKind } from 'ts-morph';

interface CoverageReport {
  total: number;
  documented: number;
  coverage: number;
  undocumented: Array<{
    file: string;
    line: number;
    name: string;
    kind: string;
  }>;
}

function auditDocCoverage(tsConfigPath: string): CoverageReport {
  const project = new Project({ tsConfigFilePath: tsConfigPath });
  const report: CoverageReport = {
    total: 0,
    documented: 0,
    coverage: 0,
    undocumented: [],
  };

  for (const sourceFile of project.getSourceFiles()) {
    // Check exported functions
    for (const fn of sourceFile.getFunctions()) {
      if (!fn.isExported()) continue;
      report.total++;
      if (fn.getJsDocs().length > 0) {
        report.documented++;
      } else {
        report.undocumented.push({
          file: sourceFile.getFilePath(),
          line: fn.getStartLineNumber(),
          name: fn.getName() || 'anonymous',
          kind: 'function',
        });
      }
    }

    // Check exported classes
    for (const cls of sourceFile.getClasses()) {
      if (!cls.isExported()) continue;
      report.total++;
      if (cls.getJsDocs().length > 0) {
        report.documented++;
      } else {
        report.undocumented.push({
          file: sourceFile.getFilePath(),
          line: cls.getStartLineNumber(),
          name: cls.getName() || 'anonymous',
          kind: 'class',
        });
      }
    }

    // Check exported interfaces
    for (const iface of sourceFile.getInterfaces()) {
      if (!iface.isExported()) continue;
      report.total++;
      if (iface.getJsDocs().length > 0) {
        report.documented++;
      } else {
        report.undocumented.push({
          file: sourceFile.getFilePath(),
          line: iface.getStartLineNumber(),
          name: iface.getName(),
          kind: 'interface',
        });
      }
    }
  }

  report.coverage = report.total > 0
    ? Math.round((report.documented / report.total) * 100)
    : 100;

  return report;
}
```

## Link Health Checker

```bash
# Install
npm install -g markdown-link-check

# Check single file
markdown-link-check README.md

# Check all markdown files
find docs/ -name '*.md' -exec markdown-link-check {} \;

# CI configuration (.markdown-link-check.json)
{
  "ignorePatterns": [
    { "pattern": "^http://localhost" },
    { "pattern": "^https://internal" }
  ],
  "replacementPatterns": [
    { "pattern": "^/docs/", "replacement": "{{BASEURL}}/docs/" }
  ],
  "httpHeaders": [
    {
      "urls": ["https://github.com"],
      "headers": {
        "Accept": "text/html"
      }
    }
  ],
  "timeout": "10s",
  "retryOn429": true,
  "retryCount": 3
}
```

## Type Coverage Tools

### type-coverage
```bash
# Install
npm install -D type-coverage

# Run
npx type-coverage --detail --strict --at-least 95

# Output example:
# 1234/1300 95.07%
# src/api/client.ts:42 - any
# src/utils/helpers.ts:12 - any
```

### Custom any-type counter
```bash
#!/bin/bash
# scripts/type-audit.sh

echo "=== Type Safety Audit ==="
echo ""

# Count any types
ANY_COUNT=$(grep -rn ': any\|: any\[\]\|as any' src/ --include='*.ts' --include='*.tsx' | wc -l)
echo "Total 'any' types: $ANY_COUNT"

# By file
echo ""
echo "--- By file ---"
grep -rnl ': any' src/ --include='*.ts' --include='*.tsx' | while read f; do
  count=$(grep -c ': any\|as any' "$f")
  echo "  $count  $f"
done | sort -rn

# By type
echo ""
echo "--- By pattern ---"
echo "  $(grep -rn ': any[^[]' src/ --include='*.ts' | wc -l)  : any (param/return)"
echo "  $(grep -rn ': any\[\]' src/ --include='*.ts' | wc -l)  : any[] (array)"
echo "  $(grep -rn 'as any' src/ --include='*.ts' | wc -l)  as any (assertion)"
```

## CI Integration

### GitHub Actions
```yaml
# .github/workflows/docs-quality.yml
name: Documentation Quality
on: [pull_request]

jobs:
  doc-quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Check markdown links
        uses: gaurav-nelson/github-action-markdown-link-check@v1
        with:
          use-quiet-mode: 'yes'
          config-file: '.markdown-link-check.json'

      - name: Lint markdown
        uses: DavidAnson/markdownlint-cli2-action@v16

      - name: Check type coverage
        run: |
          npm ci
          npx type-coverage --at-least 95
```

### ESLint v9 + typescript-eslint (flat config)

ESLint v9 made flat config the default. The legacy `.eslintrc.*` format is now deprecated. Use `eslint.config.mjs`:

```javascript
// eslint.config.mjs
import tseslint from 'typescript-eslint';

export default tseslint.config(
  tseslint.configs.recommended,
  {
    rules: {
      // Warn on explicit `any`; auto-fix converts to `unknown`
      '@typescript-eslint/no-explicit-any': 'warn',
    },
  }
);
```

Note: `tseslint.config()` helper was deprecated in typescript-eslint 8.x in favour of ESLint core's `defineConfig()`. Check your version and migrate accordingly.

Source: [ESLint v9 release](https://eslint.org/blog/2024/04/eslint-v9.0.0-released/) · [typescript-eslint no-explicit-any](https://typescript-eslint.io/rules/no-explicit-any/) · [ESLint flat config extends](https://eslint.org/blog/2025/03/flat-config-extends-define-config-global-ignores/)

## Report Template

```markdown
## Documentation Health Report

**Date:** YYYY-MM-DD
**Scope:** [Repository or module name]

### Summary

| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| JSDoc Coverage | X% | 100% | OK/NG |
| Type Coverage | X% | 95% | OK/NG |
| Link Health | X/Y valid | 100% | OK/NG |
| any Count | X | 0 | OK/NG |

### Top Priorities

1. [File with most undocumented exports]
2. [File with most any types]
3. [Broken links to fix]

### Trend

| Week | JSDoc | Types | Links |
|------|-------|-------|-------|
| W1   | 80%   | 90%   | 98%   |
| W2   | 85%   | 92%   | 100%  |
| W3   | 88%   | 95%   | 100%  |
```
