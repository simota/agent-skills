# Zen Refactor Mechanics & Complexity Metrics

Zen's playbook for resolving code smells, with complexity thresholds and per-language measurement tooling.

> For the shared smell taxonomy (definitions, recognition patterns, severity hints), see
> `_common/CODE_SMELL_CATALOG.md`. This file only covers Zen-specific refactor mechanics + complexity metrics + tool selection.

## Contents
- [Refactor Mechanic per Smell](#refactor-mechanic-per-smell)
- [Complexity Metrics](#complexity-metrics)
- [Complexity Measurement Tools](#complexity-measurement-tools)
- [Report Formats](#report-formats)

---

## Refactor Mechanic per Smell

Each smell ID below maps to a Zen refactor recipe. See the catalog for definitions.

| Smell ID | Smell | Primary Refactor |
|----------|-------|------------------|
| BLOAT-001 | Long Method | Extract Method, guard clauses, replace temp with query |
| BLOAT-002 | Large / God Class | Extract Class, Split Module by responsibility |
| BLOAT-003 | Long Parameter List | Introduce Parameter Object, Builder |
| BLOAT-004 | Data Clumps | Extract Class around the clump |
| BLOAT-005 | Primitive Obsession | Replace Primitive with Value Object / branded type |
| OOA-001 | Switch Statements | Replace Conditional with Polymorphism, Strategy |
| OOA-002 | Refused Bequest | Replace Inheritance with Delegation |
| OOA-003 | Alternative Classes | Rename Method, Extract Superclass / common interface |
| OOA-004 | Temporary Field | Extract Class, Introduce Null Object |
| CHG-001 | Divergent Change | Extract Class along change axes |
| CHG-002 | Shotgun Surgery | Move Method / Move Field to consolidate; consider Inline Class |
| CHG-003 | Parallel Inheritance | Merge Hierarchies |
| DISP-001 | Dead Code | Remove (coordinate with Sweep for ambiguous cases) |
| DISP-002 | Speculative Generality | Collapse Hierarchy, Inline Class |
| DISP-003 | Comments Masking Bad Code | Rename, Extract Method until code is self-documenting |
| DISP-004 | Duplicate Code | Extract Method, Pull Up Method, parameterize |
| DISP-005 | Lazy Class | Inline Class |
| DISP-006 | Magic Numbers / Strings | Introduce Named Constant |
| DISP-007 | Defensive Excess | See `reference/defensive-excess.md` |
| CPL-001 | Feature Envy | Move Method to the envied class |
| CPL-002 | Inappropriate Intimacy | Move Method, Extract Class, Hide Delegate |
| CPL-003 | Message Chains | Hide Delegate, Tell-Don't-Ask |
| CPL-004 | Middle Man | Remove Middle Man, Inline Method |
| CTRL-001 | Spaghetti Code | Decompose Conditional, guard clauses, state machine |
| TST-001..010 | Test smells | See `reference/test-refactoring.md` for full recipes |

---

## Complexity Metrics

### Cyclomatic Complexity (CC)

Measures the number of linearly independent paths through code.

**Formula:** `CC = E - N + 2P`
- E: edges (control flow paths)
- N: nodes (statements)
- P: connected components (usually 1)

**Quick calculation** — start at 1 and add 1 for each of:
- `if`, `else if`, `else`
- `for`, `while`, `do-while`
- `case` (each case)
- `catch`
- `&&`, `||` (each occurrence)
- `? :` (ternary)

**Thresholds:**

| Score | Risk Level | Action |
|-------|------------|--------|
| 1–10 | Low | Acceptable |
| 11–20 | Moderate | Consider refactoring |
| 21–50 | High | Must refactor — hard to test |
| 50+ | Very High | Untestable — split immediately |

### Cognitive Complexity

Measures how difficult code is to *understand* (vs. test).

**Increments (+1):** `if`, `else if`, `else`, `switch`, `for`, `while`, `do-while`, `foreach`, `catch`, labeled `break`/`continue`, sequences of binary logical operators, recursion.

**Nesting penalty:** +1 per level of nesting (compounds).

**Thresholds:**

| Score | Readability | Action |
|-------|-------------|--------|
| 0–5 | Excellent | Keep as-is |
| 6–10 | Good | Consider simplifying |
| 11–15 | Moderate | Should simplify |
| 16+ | Poor | Must refactor |

### Other Structural Thresholds

| Metric | Threshold | Notes |
|--------|-----------|-------|
| Nesting depth | > 4 | Apply guard clauses |
| Fan-out (collaborators) | > 10 | Candidate for Extract Class |
| Function LOC | > 50 | Candidate for Extract Method |
| Class LOC | > 500 | Candidate for Split Module |

---

## Complexity Measurement Tools

### TypeScript/JavaScript

```bash
npx eslint --rule 'complexity: ["error", 10]' src/
npx tsc --noUnusedLocals --noUnusedParameters --strict
lizard src/ --CCN 10 --length 60 --warnings_only
# Note: plato / es6-plato are unmaintained (~2020). Use lizard or ESLint instead.
```

### Python

```bash
radon cc src/ -a -nc                                  # per-function grade A–F
radon mi src/                                         # maintainability index
radon hal src/                                        # Halstead metrics
xenon --max-absolute B --max-modules B --max-average A src/   # CI gate
pylint --disable=all --enable=R0912,R0915,R0911 src/  # branches/statements/returns
wily build src/ && wily report src/module.py         # trend over git history
```

### Go

```bash
gocyclo -over 10 ./...
gocognit -over 10 ./...
golangci-lint run --enable gocyclo,gocognit,cyclop
go vet ./... && staticcheck ./...
```

### Rust

```bash
cargo geiger                                          # unsafe code metrics
cargo clippy -- -W clippy::cognitive_complexity
tokei src/
```

### Java

```bash
pmd check -d src/ -R category/java/design.xml/CyclomaticComplexity
spotbugs -textui -effort:max build/classes/
checkstyle -c /google_checks.xml src/
```

### Multi-language

```bash
sonar-scanner -Dsonar.projectKey=myproject -Dsonar.sources=src/
lizard src/ --CCN 10 --length 60 --warnings_only
scc --by-file --sort complexity src/
```

### Tool Selection

| Need | Best Tool | Languages |
|------|-----------|-----------|
| Quick CC check | `lizard` | All |
| JS/TS CC in CI | ESLint complexity rule | JS/TS |
| Python grades | `radon cc` | Python |
| Go CI integration | `golangci-lint` | Go |
| Trend over time | `wily` / `lizard` | Varies |
| CI gate (fail on threshold) | `xenon` / ESLint | Varies |

---

## Report Formats

### Smell Report

```markdown
### Code Smell Analysis: [file]

| Line | Smell (Catalog ID) | Severity | Suggested Fix |
|------|--------------------|----------|---------------|
| 45 | Long Method (BLOAT-001) | High | Extract calculateTotal() |
| 78 | Magic Number (DISP-006) | Medium | Introduce MAX_RETRY constant |
| 102 | Dead Code (DISP-001) | Low | Remove unused import |
```

### Complexity Report

```markdown
### Complexity Report: [file]

| Function | LOC | CC | Cognitive | Status |
|----------|-----|----|-----------|--------|
| processOrder | 45 | 12 | 8 | Moderate |
| validateInput | 80 | 25 | 18 | High |
| handleSubmit | 60 | 35 | 22 | Critical |

File average CC: 18.75 (target < 10)
Highest cognitive: 22 (target < 15)
```
