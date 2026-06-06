# Cultural DNA Profiling (absorbed from Totem)

Purpose: Use this reference when you need to profile repository conventions, detect drift, or generate an onboarding-oriented convention guide.

## Contents

- When to apply
- DNA dimensions
- Profiling workflow
- Output format

Project-specific convention profiling, deviation detection, and onboarding guide generation. Previously a standalone agent (Totem), now integrated as a Grove capability.

---

## When to Apply

Use as part of Grove's repository audit when:
- Onboarding new team members (generate convention guide)
- Detecting convention drift after many contributors
- Establishing baseline conventions for a new project
- Pre-refactoring to understand existing patterns

---

## 8 DNA Dimensions

| Dimension | What It Captures | Score 0-3 |
|-----------|-----------------|-----------|
| **Naming** | Variables, functions, files, directories | 0=chaotic → 3=strict convention |
| **Abstraction** | Function size, nesting depth, module boundaries | 0=god objects → 3=clean boundaries |
| **Error Handling** | Error patterns, logging, recovery | 0=swallowed → 3=systematic |
| **Comments** | Style, density, purpose | 0=none → 3=explains "why" |
| **Testing** | Coverage patterns, test naming, fixtures | 0=none → 3=comprehensive |
| **Architecture** | Layer separation, dependency direction | 0=tangled → 3=clear layers |
| **Git** | Commit style, branch strategy, PR patterns | 0=random → 3=conventional |
| **Dependencies** | Version pinning, update strategy, selection criteria | 0=floating → 3=managed |

---

## Discovery Method

### Sampling Strategy

```
1. Read 10-15 representative files across directories
2. Check configuration files (eslint, prettier, tsconfig, etc.)
3. Read recent git history (last 50 commits)
4. Check for style guides, CONTRIBUTING.md, ADRs
5. Examine test directory patterns
```

### Per-Dimension Analysis

| Dimension | What to Check |
|-----------|--------------|
| Naming | Variable casing (camelCase/snake_case), file naming, import aliases |
| Abstraction | Average function length, nesting depth, module exports count |
| Error Handling | try/catch patterns, custom error classes, logging usage |
| Comments | JSDoc/docstring presence, inline comment ratio, TODO patterns |
| Testing | Test file naming (*.test.ts vs *.spec.ts), describe/it patterns |
| Architecture | Directory depth, circular imports, layer violations |
| Git | Commit message format (conventional?), PR template usage |
| Dependencies | Lockfile freshness, version range style (^ vs ~), deprecated packages |

---

## DNA Profile Output

```markdown
## Project DNA Profile — [Project Name]

**Profiled**: [YYYY-MM-DD]
**Files Sampled**: [N]
**Language**: [Primary language]

### Dimension Scores

| Dimension | Score | Pattern | Notes |
|-----------|-------|---------|-------|
| Naming | [0-3] | [e.g., camelCase, kebab-case files] | [observations] |
| Abstraction | [0-3] | [e.g., small functions, DDD] | [observations] |
| Error Handling | [0-3] | [e.g., Result type, try/catch] | [observations] |
| Comments | [0-3] | [e.g., JSDoc on exports] | [observations] |
| Testing | [0-3] | [e.g., *.test.ts, vitest] | [observations] |
| Architecture | [0-3] | [e.g., feature-based] | [observations] |
| Git | [0-3] | [e.g., conventional commits] | [observations] |
| Dependencies | [0-3] | [e.g., renovate, pinned] | [observations] |

### Overall Convention Strength: [Weak/Moderate/Strong]
```

---

## Deviation Detection

When reviewing code changes, flag deviations from established DNA:

| Severity | Example | Action |
|----------|---------|--------|
| **High** | Architecture layer violation | Block in review |
| **Medium** | Naming convention break | Suggest correction |
| **Low** | Comment style inconsistency | Note for awareness |

### False Positive Avoidance

- New patterns may be intentional evolution, not deviation
- Generated code (protobuf, openapi) follows generator conventions
- Test files may have looser naming than production code
- Migration files follow framework conventions, not project conventions

---

## Onboarding Guide Generation

Use DNA Profile to generate a quick-start convention guide:

```markdown
## [Project] — Convention Quick Start

### How We Name Things
[Naming dimension summary + examples]

### How We Handle Errors
[Error handling dimension summary + examples]

### How We Test
[Testing dimension summary + examples]

### How We Commit
[Git dimension summary + examples]

### Key Patterns to Follow
[Top 3-5 most important conventions]

### Common Mistakes to Avoid
[Top 3-5 deviations newcomers make]
```
