# Subtraction Patterns Reference — Void

Purpose: Use this file after scoring to choose the safest subtraction pattern for the target.

Contents:
- Pattern overview with default CoK ranges
- Eight subtraction patterns and their entry conditions
- Minimal examples and expected effects
- Pattern-selection flow

## Pattern Overview

| Pattern | Target domain | Typical CoK range | Use when |
|---------|---------------|-------------------|----------|
| `Feature Sunset` | Feature | `6-10` | Low-value feature should be retired in phases |
| `Abstraction Collapse` | Code | `5-10` | One or two implementations do not justify an abstraction layer |
| `Scope Cut` | Feature / Specification | `4-8` | Most variants are unused or disproportionately costly |
| `Pattern Simplification` | Code | `4-8` | Design-pattern overhead exceeds problem complexity |
| `Dependency Elimination` | Dependency | `3-10` | A dependency is weakly used or replaceable |
| `Configuration Reduction` | Configuration | `3-7` | Most options stay at defaults and expand cognitive cost |
| `Process Pruning` | Process | `4-9` | Steps are ceremonial or mostly rubber-stamp |
| `Document Retirement` | Document | `3-8` | Content is stale, duplicated, or rarely read |
| `AI Slop Cleanup` | Code (AI-authored) | `2-6` | An AI-authored diff added speculative helpers, dead branches, or "comprehensive" error handling that no caller needs |

## 1. Feature Sunset

Use when:
- usage is below `5%`
- an alternative exists
- maintenance cost exceeds delivered value

Phases:
```text
ANNOUNCE -> DEPRECATE -> MIGRATE -> REMOVE
```

Example:
```text
Before: 5 export formats, but XML 0.3%, YAML 0.1%, PDF 1.2%
After: keep CSV and JSON only
Effect: fewer parsers, fewer tests, less support burden
```

## 2. Abstraction Collapse

Use when:
- an interface or base class has only `1-2` concrete implementations
- the abstraction was created for speculative future growth
- the abstraction makes code harder to read than direct implementation

Decision rule:
```text
1 implementation  -> collapse is usually correct
2 implementations -> collapse if they always move together
3+ implementations -> collapse is usually unsafe
```

Example:
```text
Before: interface + factory + config for one notification implementation
After: direct email-notification function
```

## 3. Scope Cut

Use when:
- `80/20` usage distribution is visible
- rare variants cost more than they return
- edge-case support dominates maintenance effort

Analysis template:
```yaml
scope_analysis:
  total_variations: X
  usage_distribution:
    - { variation: "A", usage_percent: 65, maintenance_cost: LOW }
    - { variation: "B", usage_percent: 25, maintenance_cost: LOW }
    - { variation: "C", usage_percent: 7, maintenance_cost: HIGH }
    - { variation: "D", usage_percent: 3, maintenance_cost: CRITICAL }
  cut_candidates: ["C", "D"]
  kept_coverage: "90%"
  maintenance_reduction: "60%"
```

## 4. Pattern Simplification

Use when:
- pattern overhead exceeds the real problem size
- the codebase is small enough that indirection no longer pays for itself
- a textbook pattern harms readability

Common simplifications:

| Over-engineered shape | Simpler substitute |
|-----------------------|--------------------|
| Strategy with 2 implementations | `if/else` or `switch` |
| Observer with 1 listener | Direct call |
| Builder for 3 parameters | Constructor or function args |
| Event-driven sync flow | Direct call chain |
| Microservice for tiny traffic | Module in a monolith |

## 5. Dependency Elimination

Use when:
- library usage is below `10%` of its surface
- native APIs or standard libraries can replace it
- security or maintenance burden is high

Decision matrix:

| Usage | Ease of replacement | Recommendation |
|-------|---------------------|----------------|
| `<10%` | High | `ELIMINATE` immediately |
| `<10%` | Low | `ELIMINATE` gradually |
| `10-50%` | High | elimination candidate |
| `10-50%` | Low | `KEEP-WITH-WARNING` |
| `>50%` | Any | usually `KEEP` |

## 6. Configuration Reduction

Use when:
- `80%` of options stay at defaults
- option combinations create unpredictable behavior
- configuration docs cost too much to maintain

Analysis template:
```yaml
config_analysis:
  total_options: X
  default_usage_rate:
    - { option: "timeout", default_rate: "98%", action: "HARDCODE" }
    - { option: "retries", default_rate: "95%", action: "HARDCODE" }
    - { option: "theme", default_rate: "60%", action: "KEEP" }
    - { option: "language", default_rate: "40%", action: "KEEP" }
```

## 7. Process Pruning

Use when:
- `80%+` of steps are rubber-stamp approvals
- meetings are poorly attended or output is unused
- wait time dwarfs value-creation time

Analysis template:
```yaml
process_analysis:
  process_name: "<Process Name>"
  total_steps: X
  step_evaluation:
    - { step: "Team Lead Approval", value: HIGH, rubber_stamp_rate: "10%", action: "KEEP" }
    - { step: "Director Approval", value: LOW, rubber_stamp_rate: "95%", action: "ELIMINATE" }
  total_wait_time: "3 days"
  after_wait_time: "0.5 day"
```

## 8. Document Retirement

Use when:
- no meaningful update for `6+` months
- view count is near zero
- newer documents already supersede it
- inaccurate content creates risk

Analysis template:
```yaml
document_analysis:
  total_documents: X
  evaluation:
    - { doc: "Initial Design v1", last_updated: "2023-01", views_90d: 0, action: "RETIRE" }
    - { doc: "API Spec v2", last_updated: "2024-06", views_90d: 45, action: "KEEP" }
    - { doc: "Dev Guide v1", last_updated: "2023-06", views_90d: 3, action: "MERGE" }
```

## 9. AI Slop Cleanup

Use when:
- An AI assistant (Copilot, Claude Code, Cursor auto-edit, Cody, etc.) generated the target diff or file.
- The diff contains helpers, adapters, or "future-proofing" utilities with `0` callers in the same PR.
- Error handling expands beyond actual system-boundary inputs (defensive `try` blocks around internal pure functions, `null` checks on values the type system already excludes).
- Tests assert on internal call sequence rather than behavior, or pin to literal AI-generated strings instead of contract.

### Entry Conditions

- The PR is labelled AI-authored, or `>40%` of the lines come from an assistant.
- The change touches code where the human author cannot fluently summarise control flow.
- Existing similar code in the repo solves the same problem in fewer lines.

### Default Cuts (in priority order)

| Target | Action | Why |
|--------|--------|-----|
| Helpers with `0` same-diff callers | DELETE | Speculative `OE-11`; recreate when the second caller arrives |
| Interfaces / abstract classes with one implementation | COLLAPSE | `OE-01`; merge into the concrete site |
| `try / catch` around internal-only pure functions | DELETE catch | Defensive `OE-10`; let the framework handle it at the boundary |
| Generated docstrings restating the obvious | TRIM | Comprehension debt, not signal |
| Tests pinning literal AI-generated strings (e.g., snapshot of synthesised log message) | REPLACE with behavioural assertion | Snapshot churn without value |
| Duplicated logic across files (often `2x` GitClear baseline) | DEDUPE only on Rule of Three; otherwise DELETE the speculative second copy | `OE-09` risk if forced too early |

### Phased Approach

```text
1. AUDIT     — list every AI-authored addition with no caller / no test of behaviour
2. RECONCILE — confirm with author which entries are deliberate vs reflex
3. CUT       — delete in one commit; keep diff small enough for human review
4. RE-TEST   — run existing suite; new gaps are evidence the cut was wrong
5. RECORD    — annotate the journal so the same speculative shape is rejected next time
```

### Example

```text
Before: AI-authored "user service" added UserRepository interface (1 impl),
        UserMapper helper (used once inline), UserValidationError class
        (used by no caller), comprehensive try/catch around an internal
        pure function, and 4 snapshot tests on synthesised log strings.

After:  Direct PostgresUserStore class; inline mapping at the call site;
        no defensive try/catch; 2 behavioural tests checking the actual
        contract.

Effect: ~60% line reduction, 0 behaviour change, comprehension debt drops
        to "one team member explains the whole flow in 2 sentences."
```

## Pattern Selection Guide

```text
1. Confirm the target category from evaluation-criteria.md
2. Map category to the default subtraction pattern
3. Check entry conditions and exceptions
4. Evaluate blast radius
5. Design a phased approach when removal is not instant-safe
6. If the target was AI-authored within the last 30 days,
   prefer "AI Slop Cleanup" first to remove speculative shape
   before any other pattern is applied.
```
