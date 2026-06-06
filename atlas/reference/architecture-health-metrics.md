# Architecture Health Metrics

Quantitative indicators for measuring architectural quality.

## Coupling Metrics

| Metric | Formula | Target | Tool |
|--------|---------|--------|------|
| **Afferent Coupling (Ca)** | Incoming dependencies | < 20 per module | madge |
| **Efferent Coupling (Ce)** | Outgoing dependencies | < 10 per module | madge |
| **Instability (I)** | Ce / (Ca + Ce) | 0.0-0.3 (stable) or 0.7-1.0 (flexible) | calculated |
| **Abstractness (A)** | Abstract types / Total types | Varies by layer | manual |
| **Distance from Main (D)** | \|A + I - 1\| | < 0.3 | calculated |

## Complexity Metrics

| Metric | Target | Detection |
|--------|--------|-----------|
| **Lines per File** | < 500 | `find src -name "*.ts" \| xargs wc -l \| sort -n` |
| **Functions per File** | < 20 | ESLint max-lines-per-function |
| **Cyclomatic Complexity** | < 10 per function | ESLint complexity rule |
| **Dependency Depth** | < 5 levels | `npx madge --max-depth 5` |
| **Circular Dependencies** | 0 | `npx madge --circular` |

---

## Health Score Card Template

```markdown
### Architecture Health Report: [Project Name]

**Report Date**: YYYY-MM-DD
**Scope**: [modules analyzed]

#### Coupling Health
| Module | Ca | Ce | I | Status |
|--------|----|----|---|--------|
| auth | 15 | 5 | 0.25 | ✅ Stable |
| orders | 8 | 12 | 0.60 | ⚠️ Zone of Pain |
| shared | 45 | 2 | 0.04 | ✅ Stable (but high Ca) |

#### Complexity Health
| Metric | Current | Target | Status |
|--------|---------|--------|--------|
| Files > 500 lines | 3 | 0 | ❌ |
| Circular dependencies | 2 | 0 | ❌ |
| Avg complexity | 8.2 | < 10 | ✅ |
| Max dependency depth | 4 | < 5 | ✅ |

#### Layer Violations
| Violation | Count | Examples |
|-----------|-------|----------|
| UI → Infrastructure | 2 | OrderPage → PrismaClient |
| Domain → UI | 0 | - |

#### Technical Debt Score
- **Design Debt**: 3 items (High: 1, Medium: 2)
- **Code Debt**: 5 items (High: 0, Medium: 3, Low: 2)
- **Test Debt**: 2 items (Coverage: 72%)

**Overall Health**: ⚠️ Needs Attention
**Priority Actions**:
1. Split UserService.ts (2,500 lines)
2. Fix circular dependency: orders ↔ inventory
3. Add integration tests for payment flow
```

---

## Automated Health Check

```bash
#!/bin/bash
# architecture-health.sh

echo "=== Architecture Health Check ==="

echo "\n📊 File Size Analysis:"
find src -name "*.ts" -o -name "*.tsx" | xargs wc -l | sort -n | tail -10

echo "\n🔄 Circular Dependencies:"
npx madge --circular src/

echo "\n📈 Most Imported Modules (High Ca):"
grep -rh "from ['\"]@/" src --include="*.ts" | \
  sed "s/.*from ['\"]\\([^'\"]*\\)['\"].*/\\1/" | \
  sort | uniq -c | sort -rn | head -10

echo "\n📉 Most Importing Files (High Ce):"
grep -r "^import" src --include="*.ts" | \
  cut -d: -f1 | sort | uniq -c | sort -rn | head -10

echo "\n🚫 Layer Violations:"
npx depcruise --validate .dependency-cruiser.js src 2>/dev/null || echo "Configure .dependency-cruiser.js"
```

---

## CI Integration

```yaml
# .github/workflows/architecture.yml
name: Architecture Health
on: [pull_request]

jobs:
  health-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4

      - name: Check circular dependencies
        run: |
          npx madge --circular src/
          if [ $? -ne 0 ]; then
            echo "::error::Circular dependencies detected"
            exit 1
          fi

      - name: Check file sizes
        run: |
          LARGE_FILES=$(find src -name "*.ts" -exec wc -l {} + | awk '$1 > 500 {print}' | grep -v total)
          if [ -n "$LARGE_FILES" ]; then
            echo "::warning::Files exceeding 500 lines:"
            echo "$LARGE_FILES"
          fi

      - name: Layer validation
        run: npx depcruise --validate .dependency-cruiser.js src
```
