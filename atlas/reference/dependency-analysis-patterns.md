# Dependency Analysis Patterns

## Metrics

| Metric | Definition | Threshold | Tool |
|--------|-----------|-----------|------|
| Afferent Coupling (Ca) | Incoming dependencies | < 20 per module | madge |
| Efferent Coupling (Ce) | Outgoing dependencies | < 10 per module | madge |
| Instability (I) | Ce / (Ca + Ce) | 0.0-0.3 (stable) or 0.7-1.0 (flexible) | calculated |
| Abstractness (A) | Abstract types / Total types | Varies by layer | manual |
| Distance from Main (D) | \|A + I - 1\| | < 0.3 | calculated |

## Resolution Patterns

1. **Dependency Inversion** - Introduce interface between layers
2. **Event-based** - Replace direct call with event/message
3. **Mediator** - Introduce coordinator module

---

## God Class Detection

```bash
# Find files with more than 500 lines
find src -name "*.ts" -o -name "*.tsx" | xargs wc -l | sort -n | tail -20

# Using cloc for detailed analysis
cloc src --by-file --include-lang=TypeScript,JavaScript | sort -k5 -n | tail -20

# ESLint rule for max lines (add to .eslintrc)
# "max-lines": ["warn", { "max": 500, "skipBlankLines": true, "skipComments": true }]
```

## Circular Dependency Detection

```bash
# Using madge
npx madge --circular src/

# With visual output
npx madge --circular --image circular.svg src/

# Using dependency-cruiser
npx depcruise --validate .dependency-cruiser.js src
```

```javascript
// .dependency-cruiser.js
module.exports = {
  forbidden: [
    {
      name: 'no-circular',
      severity: 'error',
      comment: 'Circular dependencies are not allowed',
      from: {},
      to: {
        circular: true
      }
    },
    {
      name: 'no-orphans',
      severity: 'warn',
      comment: 'Modules should be imported somewhere',
      from: {
        orphan: true,
        pathNot: [
          '(^|/)\\.[^/]+\\.(js|cjs|mjs|ts|json)$',
          '\\.d\\.ts$',
          '(^|/)tsconfig\\.json$',
          '(^|/)index\\.(js|ts)$'
        ]
      },
      to: {}
    }
  ],
  options: {
    doNotFollow: {
      path: 'node_modules'
    },
    tsPreCompilationDeps: true,
    enhancedResolveOptions: {
      exportsFields: ['exports'],
      conditionNames: ['import', 'require', 'node', 'default']
    }
  }
};
```

## Dependency Structure Matrix (DSM)

Use DSM to visualize and analyze component dependencies at scale. The matrix provides a compact, systematic mapping of all inter-module dependencies — more navigable than graph diagrams for systems with 30+ modules.

**When to use:** Large-scale dependency audits, circular dependency triage, change impact analysis, and module boundary validation.

**Tools:** NDepend (DSM view), Lattix Architect, IntelliJ IDEA (DSM analysis), dependency-cruiser (matrix output).

**Reading the matrix:** Non-zero cells above the diagonal indicate feedforward dependencies; cells below the diagonal indicate feedback (potential cycles). Clustered non-zero cells reveal tightly coupled module groups — candidates for merging or explicit API boundary extraction.

## Coupling Metrics

```bash
# Generate dependency graph
npx madge --image dependency-graph.svg src/

# Count imports per file
grep -r "^import" src --include="*.ts" --include="*.tsx" | \
  cut -d: -f1 | sort | uniq -c | sort -rn | head -20

# Find most imported modules (high afferent coupling)
grep -rh "from ['\"]" src --include="*.ts" --include="*.tsx" | \
  sed "s/.*from ['\"]\\([^'\"]*\\)['\"].*/\\1/" | \
  sort | uniq -c | sort -rn | head -20
```

## Unused Export Detection

```bash
# Using ts-prune
npx ts-prune

# Using knip (more comprehensive)
npx knip

# knip.json configuration
{
  "entry": ["src/index.ts", "src/pages/**/*.tsx"],
  "project": ["src/**/*.ts", "src/**/*.tsx"],
  "ignore": ["**/*.d.ts", "**/*.test.ts"]
}
```

## Import Graph Analysis

```bash
# Visualize imports for a specific file
npx madge --image file-deps.svg src/components/UserProfile.tsx

# Find all files importing a module
grep -rl "from.*UserService" src --include="*.ts" --include="*.tsx"

# Dependency depth analysis
npx madge --max-depth 3 src/
```

## Layer Violation Detection

```javascript
// .dependency-cruiser.js - Layer rules
module.exports = {
  forbidden: [
    // UI should not import from infrastructure
    {
      name: 'no-ui-to-infra',
      severity: 'error',
      from: { path: '^src/components' },
      to: { path: '^src/infrastructure' }
    },
    // Domain should not import from UI
    {
      name: 'no-domain-to-ui',
      severity: 'error',
      from: { path: '^src/domain' },
      to: { path: '^src/(components|pages|views)' }
    },
    // Domain should not import from infrastructure
    {
      name: 'no-domain-to-infra',
      severity: 'error',
      from: { path: '^src/domain' },
      to: { path: '^src/infrastructure' }
    }
  ]
};
```
