# Audit Checklist Reference

**Purpose:** Scoring criteria and test patterns for the AUDIT phase.
**Read when:** Running AUDIT phase to evaluate existing folder structure.

---

## Full Audit Protocol

### Step 1: Tree Analysis

Run `find . -type f | head -200` or equivalent to capture project structure. Classify:

| Metric | How to Measure | Target |
|--------|---------------|--------|
| Total files | `find . -type f \| wc -l` (exclude .git, node_modules) | Document baseline |
| Max depth | Deepest file path from root | ≤ 5 levels |
| Avg files per directory | Total files / total directories | ≤ 15 |
| Orphan directories | Dirs with only 1 file | ≤ 5% of total dirs |
| Generic names | Count of `utils.*`, `helpers.*`, `misc.*`, `common.*` | 0 ideal, ≤ 3 acceptable |

### Step 2: Discovery Test (5 Queries)

Execute each query and record hit rate:

```
Query 1: Find all configuration files
  Patterns: **/*.config.*, **/config/**, **/.{tool}rc
  Pass: All configs found in ≤2 patterns

Query 2: Find all test files
  Patterns: **/*.test.*, **/*.spec.*, **/tests/**, **/__tests__/**
  Pass: All tests found in ≤2 patterns

Query 3: Find API/route definitions
  Patterns: grep -r "router\|endpoint\|handler\|@Get\|@Post"
  Pass: 80%+ route files in top results

Query 4: Find documentation
  Patterns: **/*.md, **/docs/**
  Pass: All docs found in ≤2 patterns, no docs buried in src/

Query 5: Find CLAUDE.md instruction chain
  Patterns: **/CLAUDE.md, **/.claude/**
  Pass: Complete hierarchy discoverable, no orphan rules
```

**Score**: (queries passed / 5) × 100 = Discovery Score

### Step 3: Token Budget Scan

For each context file (CLAUDE.md, .md files in .claude/, rules files):

```
File: [path]
Lines: [count]
Estimated tokens: [lines × 5 for mixed EN/JP]
Budget status: OK (≤200) | WARNING (201-300) | OVER (>300)
Action: [none | split via @import | extract to reference]
```

### Step 4: Cache Topology Evaluation

Score each factor (0-100), then weighted average:

| Factor | Weight | Scoring |
|--------|--------|---------|
| Static-first ordering | 30% | 100: all static before dynamic. 50: mixed. 0: dynamic first |
| Change frequency grouping | 30% | 100: clear separation. 50: partial. 0: no grouping |
| CLAUDE.md stability | 20% | 100: changes <1x/month. 50: weekly. 0: daily |
| Tool definition locality | 20% | 100: all in predictable paths. 50: scattered. 0: no pattern |

### Step 5: Overall Score

```yaml
AUDIT_REPORT:
  project: "[name]"
  date: "[YYYY-MM-DD]"
  scores:
    discovery: [0-100]
    token_budget: [0-100]  # (files within budget / total context files) × 100
    cache_topology: [0-100]
    naming_quality: [0-100]  # (well-named files / total files) × 100
    overall: [weighted average]
  grade: A (≥85) | B (≥70) | C (≥55) | D (<55)
  top_issues:
    - "[issue 1 — highest impact]"
    - "[issue 2]"
    - "[issue 3]"
  recommendations:
    - priority: P1
      action: "[specific action]"
      impact: "[expected improvement]"
    - priority: P2
      action: "[specific action]"
      impact: "[expected improvement]"
```

---

## Naming Quality Scoring

| Pattern | Score | Example |
|---------|-------|---------|
| Domain-descriptive kebab-case | 100 | `user-auth/`, `payment-gateway.ts` |
| Descriptive but inconsistent case | 70 | `UserAuth/`, `paymentGateway.ts` |
| Abbreviated but guessable | 50 | `auth/`, `pay.ts` |
| Generic / ambiguous | 20 | `utils/`, `helpers.ts`, `misc/` |
| Single-letter or opaque | 0 | `a/`, `x.ts`, `tmp/` |

---

## Common Anti-patterns

| Anti-pattern | Symptom | Fix |
|-------------|---------|-----|
| **Flat explosion** | 50+ files in root directory | Group by domain into subdirectories |
| **Deep nesting** | `src/modules/user/services/internal/helpers/` | Flatten to ≤4 levels, co-locate by domain |
| **Type-first grouping** | `models/`, `controllers/`, `views/` separated | Move to domain-first: `user/{model,controller,view}` |
| **Orphan docs** | READMEs scattered without hierarchy | Centralize in `docs/` with topic organization |
| **Monolithic CLAUDE.md** | 500+ line CLAUDE.md | Split via `@import` into `.claude/rules/*.md` |
| **Hidden context** | Rules in non-standard locations | Move to `.claude/rules/` or `CLAUDE.md` |
| **Stale context files** | CLAUDE.md references deleted files | Audit and prune references |
