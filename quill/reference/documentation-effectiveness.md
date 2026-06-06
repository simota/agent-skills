# Documentation Effectiveness System (CHRONICLE)

Purpose: Read this after documentation work or when Quill must track rot, evaluate impact, calibrate heuristics, or propagate reusable documentation patterns.

Contents:
- `Overview`: CHRONICLE feedback-loop model
- `RECORD — Log Documentation Activities`: task-level evidence capture
- `EVALUATE — Measure Documentation Impact`: coverage and rot thresholds
- `CALIBRATE — Update Documentation Heuristics`: pattern scoring and adjustment rules
- `PROPAGATE — Share Validated Patterns`: Lore and ecosystem handoff rules
- `Quick CHRONICLE`: lightweight path for small tasks
- `Integration with Ecosystem` / `Feedback to Ecosystem`: downstream propagation and signals

Documentation pattern tracking, rot rate measurement, coverage trend analysis, and documentation quality improvement.
Quill gets better at documenting code by learning from outcomes.

---

## Overview

The CHRONICLE phase runs post-task (or periodically) to close the feedback loop between documentation activities and actual developer outcomes. Without CHRONICLE, JSDoc patterns stay static and documentation rot goes undetected. With it, Quill's documentation becomes progressively more effective and durable.

```
RECORD ──→ EVALUATE ──→ CALIBRATE ──→ PROPAGATE
  │            │            │            │
  │ Log       │ Measure    │ Update    │ Share with
  │ docs &    │ coverage & │ pattern   │ Lore/Scribe
  │ changes   │ rot rate   │ weights   │
```

---

## RECORD — Log Documentation Activities

After each documentation task, record:

```yaml
Task: [task-id]
Type: [JSDoc | README | Type Improvement | API Doc | Comment | CHANGELOG | Coverage Audit]
Scope: [function | module | cross-module | project]
Files_Modified: [count]
Coverage_Delta:
  jsdoc_before: [X%]
  jsdoc_after: [Y%]
  type_before: [X%]
  type_after: [Y%]
Any_Types_Removed: [count]
Links_Fixed: [count]
Patterns_Applied:
  - pattern: [JSDoc tag set | Type guard | README template | Comment style]
    effectiveness: [High/Medium/Low/Unknown]
Downstream_Handoff: [Canvas/Atlas/Gateway/Lore/None]
```

### What to Track

| Data Point | Why | Used For |
|-----------|-----|----------|
| Coverage delta | Core metric for documentation impact | Task prioritization improvement |
| Documentation rot rate | How quickly docs become stale after writing | Rot prevention strategy |
| Pattern effectiveness | Which JSDoc/comment patterns reduce confusion most | Pattern selection heuristic |
| Type improvement impact | Do type improvements reduce related bug reports? | Type strategy optimization |
| README template adoption | Which templates get positive developer feedback? | Template selection improvement |
| Downstream utilization | Did Canvas/Atlas/Gateway use the output? | Output format improvement |

---

## EVALUATE — Measure Documentation Impact

### Coverage Trend Tracking

```
Coverage Improvement Rate = Coverage Delta / Tasks Completed

> +5%/task  = High-impact documentation (maintain approach)
+2-5%/task = Moderate impact (review scope selection)
< +2%/task = Low impact (review prioritization, target higher-value areas)
```

### Documentation Rot Rate

```
Rot Rate = Documents Requiring Update / Total Documents (per quarter)

< 0.15  = Durable documentation (strong patterns)
0.15-0.30 = Normal rot (maintain review cadence)
> 0.30  = Fast decay (review accuracy, coupling to volatile code)
```

### AI-Consumer Coverage (2026 addition)

By 2026 published analytics from documentation platforms show roughly **half of documentation traffic** comes from AI agents (Cursor, Claude Code, ChatGPT, Perplexity, GitHub Copilot, Windsurf). Track an additional surface alongside the JSDoc / type coverage metrics above:

```
AI-Consumer Coverage =
  has_llms_txt           ? 25% : 0%   # llms.txt + llms-full.txt present at repo / docs root
  + headings_are_clean   ? 25% : 0%   # H1 = title, H2 = section, no ambiguous fragments
  + examples_canonical   ? 25% : 0%   # at least one @example per public symbol
  + contracts_structured ? 25% : 0%   # @returns / @throws used; null-on-failure is tagged, not prose

Target: 100% for libraries / SDKs; 75%+ for applications.
```

Stale `llms.txt` is worse than a missing one — the build pipeline must regenerate it on every release. Add a CI gate: fail the build if `llms.txt` was not updated when the source README headings changed.

### Evaluation Triggers

| Trigger | Check |
|---------|-------|
| Developer asks "what does this do?" for documented code | Documentation clarity, completeness |
| JSDoc/comment contradicts code behavior | Accuracy, rot detection |
| README install steps fail | README freshness |
| Type coverage drops after new feature | Type documentation gap |
| Quarterly review | Overall documentation health |

### Per-Period Evaluation Summary

```markdown
### Documentation Evaluation

| Metric | Value | Trend |
|--------|-------|-------|
| Documentation tasks completed | 15 | — |
| JSDoc coverage (project) | 88% | ↑ |
| Type coverage (project) | 93% | ↑ |
| any types removed | 23 | — |
| Link health | 100% | — |
| Rot rate (quarterly) | 12% | ↓ |
| Downstream utilization | 80% (12/15) | — |

**Strongest pattern**: @example with runnable code (highest clarity score)
**Weakest area**: Internal utility documentation (high rot rate)
**Note**: Type guards reduced related bug reports by 25%.
```

---

## CALIBRATE — Update Documentation Heuristics

### Pattern Effectiveness Scoring

Track which documentation patterns work best in which contexts:

```yaml
# Default pattern effectiveness by context
jsdoc_patterns:
  public_api: 0.95
  internal_utility: 0.70
  react_component: 0.85
  event_handler: 0.75
type_improvement_patterns:
  api_response_typing: 0.95
  generic_function: 0.90
  event_handler_typing: 0.85
  dynamic_object: 0.80
  third_party_wrapping: 0.75
readme_templates:
  library: 0.90
  application: 0.85
  cli_tool: 0.80
comment_styles:
  why_comment: 0.95
  context_comment: 0.90
  how_comment: 0.60
  what_comment: 0.20

# Calibrated (from CHRONICLE data)
# Example: React component JSDoc more effective than expected
jsdoc_patterns:
  react_component: 0.85 → 0.92  # @example with props table highly adopted
```

### Calibration Rules

1. **3+ tasks required** before adjusting pattern effectiveness scores
2. **Max adjustment per cycle**: ±0.15 (prevent overcorrection)
3. **Decay**: Adjustments decay 10% per quarter toward defaults
4. **Override**: User explicit documentation preferences always win

### Documentation Scope Calibration

Track optimal documentation scope by context:

| Context | Default Scope | Calibrated Scope | Notes |
|---------|-------------|-----------------|-------|
| New public API | Full JSDoc + @example | Full JSDoc + @example | Always high value |
| Refactored code | Update existing JSDoc | Add missing + update | Often JSDoc was absent pre-refactor |
| Bug fix | Explain why (inline comment) | Explain why + edge case | Edge case docs prevent regression |
| Type improvement | Replace any + add guard | Replace any + guard + @example | Examples clarify complex types |
| README update | Affected sections only | Affected + verify all links | Link rot often accompanies changes |

### Comment Density Calibration

Track optimal comment density by code complexity:

| Code Complexity | Default Density | Calibrated Range | Notes |
|----------------|----------------|-----------------|-------|
| Simple CRUD | Minimal (JSDoc only) | JSDoc + brief module comment | Too many comments = noise |
| Business logic | Moderate (why comments) | Why + business rule refs | Business rule links most valued |
| Algorithm | High (how + why) | How + why + @example | Runnable examples essential |
| Regex/math | High (explanation) | Full explanation + test cases | Regex without explanation = tech debt |
| Config/setup | Moderate (.env docs) | .env.example + inline constraints | Missing constraints = production incidents |

---

## PROPAGATE — Share Validated Patterns

### Journal Entry Format

Record CHRONICLE insights in `.agents/quill.md`:

```markdown
## YYYY-MM-DD - CHRONICLE: [Documentation Type]

**Tasks assessed**: N
**Coverage improvement**: +X%
**Key insight**: [description]
**Calibration adjustment**: [pattern/scope: old → new]
**Apply when**: [future scenario]
**reusable**: true

<!-- EVOLUTION_SIGNAL
type: PATTERN
source: Quill
date: YYYY-MM-DD
summary: [documentation insight]
affects: [Quill, Scribe, Lore]
priority: MEDIUM
reusable: true
-->
```

### Pattern Library

Build a library of effective documentation approaches by context:

| Context | Best Approach | Key Elements | Effectiveness |
|---------|--------------|-------------|---------------|
| New public API | Full JSDoc | @param + @returns + @throws + @example | Very High |
| Type migration (any→typed) | Categorize → Replace → Guard | Interface + type guard + @example | High |
| README creation | Template-based | Project type template + .env.example | High |
| Complex algorithm | Why + How comment | Business rule ref + complexity note + @example | High |
| API documentation | OpenAPI annotation | swagger-jsdoc + request/response examples | High |
| Documentation audit | Coverage script | doc-coverage + type-coverage + link-check | Medium-High |

### Quick Calibration (Small Tasks)

For tasks with < 3 files modified:

```markdown
## Quick CHRONICLE

**Tasks**: 1 completed
**Files**: 2 (too few to calibrate)
**Note**: @example with actual use case improved function clarity
**Action**: No weight change (insufficient data)
```

Rule: Do not adjust weights from a single small task. Accumulate data across tasks.

---

## Integration with Ecosystem

CHRONICLE data feeds into documentation decisions:

| CHRONICLE Signal | Ecosystem Impact |
|----------------|--------------------|
| Coverage improving steadily | Documentation approach is working — continue |
| Coverage stagnating | Re-examine scope selection, prioritize high-traffic code |
| High rot rate detected | Increase automation (CI checks), prefer docs closer to code |
| Pattern consistently effective | Standardize across project |
| Low downstream utilization | Adjust output format, improve handoff quality |
| Validated documentation pattern | Share with Lore, update Scribe templates |

---

## Feedback to Ecosystem

When CHRONICLE discovers patterns valuable beyond a single task:

1. **Record in journal** with `reusable: true` tag
2. **Emit EVOLUTION_SIGNAL** for Lore to collect
3. **Feed to Scribe** if documentation patterns improve specification quality
4. **Inform Gateway** if API documentation patterns improve spec accuracy
5. **Update pattern defaults** if new documentation approaches prove more effective
