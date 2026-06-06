# Analysis Patterns

**Purpose:** Detailed analysis patterns and knowledge extraction techniques for different change types.
**Read when:** Selecting an analysis approach during the ANALYZE phase.

---

## Pattern Catalog

| Pattern | Target | Output |
|---------|--------|--------|
| Refactoring Analysis | Refactoring changes | Design improvement learning points |
| Bug Fix Archaeology | Bug fixes | Root cause and prevention knowledge |
| Feature Addition | New feature additions | Architecture decisions and integration points |
| Dependency Change | Library/dependency changes | Trade-off analysis and migration knowledge |
| Performance Optimization | Optimization changes | Measurement → hypothesis → improvement flow |
| Security Hardening | Security fixes | Threat model and defense patterns |

---

## Pattern 1: Refactoring Analysis

Extract design principles from refactoring changes.

### Signals
- File split/merge → separation of concerns / cohesion decisions
- Naming changes → domain model revision
- Function extraction → DRY principle / reusability intent
- Type changes → type safety strengthening
- Test additions → quality assurance policy

### Framework
```yaml
REFACTORING_ANALYSIS:
  before:
    code_smell: "[Code smell present before change]"
    symptoms: "[Problem symptoms: hard to read, hard to change, etc.]"
  change:
    technique: "[Refactoring technique applied]"
    scope: "[Impact scope]"
  after:
    improvement: "[Quality attributes improved]"
    principle: "[Underlying design principle]"
  teaching:
    - "Signs that this refactoring should be applied"
    - "Cases where it should NOT be applied"
    - "Related refactoring techniques"
```

---

## Pattern 2: Bug Fix Archaeology

Extract root cause analysis and prevention knowledge from bug fixes.

### Signals
- Conditional branch additions/fixes → edge case oversight
- Null/undefined checks → lack of type safety
- Race condition fixes → insufficient concurrency consideration
- Input validation additions → trust boundary awareness gaps

### Framework
```yaml
BUGFIX_ANALYSIS:
  bug:
    symptom: "[Problem observed by user]"
    root_cause: "[Root cause]"
    category: "[Classification: logic/race/null/boundary/state]"
  fix:
    approach: "[Fix approach]"
    alternative: "[Alternative fixes considered]"
  prevention:
    pattern: "[Prevention pattern for the future]"
    test: "[Tests added]"
    checklist: "[Review checklist items]"
```

---

## Pattern 3: Feature Addition

Extract design decisions from new feature additions.

### Signals
- New file creation → module design decisions
- API additions → interface design
- Test additions → test strategy
- Config additions → flexibility vs simplicity balance

### Framework
```yaml
FEATURE_ANALYSIS:
  feature:
    purpose: "[Feature purpose]"
    user_story: "[User story]"
  architecture:
    placement: "[Where the feature was placed]"
    rationale: "[Reason for placement]"
    alternatives: "[Other placements considered]"
  integration:
    touchpoints: "[Integration points with existing code]"
    contracts: "[Interfaces defined]"
  extensibility:
    design_for_change: "[Design anticipating future changes]"
    yagni_notes: "[What was deliberately NOT built]"
```

---

## Pattern 4: Dependency Change

Extract trade-off decisions from library/dependency changes.

### Signals
- package.json / requirements.txt changes → dependency add/remove/update
- Import statement changes → API migration
- Config file changes → new configuration system

### Framework
```yaml
DEPENDENCY_ANALYSIS:
  change:
    type: "[add/remove/upgrade/downgrade/replace]"
    from: "[Pre-change dependency]"
    to: "[Post-change dependency]"
  rationale:
    why_change: "[Reason for change]"
    evaluation: "[Evaluation criteria: performance/security/maintainability/license]"
  tradeoffs:
    gained: "[What was gained]"
    lost: "[What was lost]"
    risks: "[Risks introduced]"
  migration:
    breaking_changes: "[Breaking changes present?]"
    migration_steps: "[Migration steps]"
```

---

## Pattern 5: Performance Optimization

Extract optimization techniques from performance improvement changes.

### Framework
```yaml
PERFORMANCE_ANALYSIS:
  problem:
    metric: "[Metric to improve]"
    baseline: "[Pre-improvement value]"
    target: "[Target value]"
  approach:
    technique: "[Optimization technique applied]"
    rationale: "[Why this technique was chosen]"
  result:
    achieved: "[Achieved value]"
    side_effects: "[Side effects: readability decrease, etc.]"
  teaching:
    when_to_apply: "[Scenarios where this optimization is effective]"
    when_not_to_apply: "[Scenarios where it would be over-optimization]"
    measurement: "[How to measure effectiveness]"
```

---

## Pattern 6: Security Hardening

Extract defense patterns from security-related changes.

### Framework
```yaml
SECURITY_ANALYSIS:
  vulnerability:
    type: "[Vulnerability type (OWASP classification etc.)]"
    severity: "[Severity]"
    vector: "[Attack vector]"
  fix:
    approach: "[Fix approach]"
    defense_in_depth: "[Defense-in-depth considerations]"
  teaching:
    threat_model: "[Threat model]"
    secure_pattern: "[Secure pattern]"
    insecure_pattern: "[Insecure pattern (no specific attack code)]"
    checklist: "[Security review checklist]"
```

---

## Combining Patterns

When a change matches multiple patterns, select one primary pattern (based on main intent) and add secondary patterns as supplements. Connect them via Learning Points that explain how the patterns interact.

---

## AI-Assisted Diff Explanation (2026 baseline)

Treat AI assistants as a drafting tool, not the source of truth. Always read the actual diff first, then use the assistant to surface missed angles. As of 2026:

- **GitHub Copilot Chat on PRs** now includes comments, file changes, commits, and reviews as context, and can be invoked directly from a diff to walk through changes. Useful for first-pass extraction of intent before applying the 5W1H+WhyNot framework. [Source: github.blog/changelog 2026-04-23 — Copilot Chat improvements for pull requests]
- **Copilot's March 2026 agentic code-review** rewrite moved from shallow line-by-line analysis to tool-calling that reads related files and traces cross-file dependencies. Pair the agent's findings with Tome's `Why Not` section to capture rejected alternatives the agent will not infer. [Source: github.blog/changelog 2026-03 — agentic code review]
- **Adoption vs trust gap.** Stack Overflow's 2025 Developer Survey reports 84% of developers use or plan to use AI tools, but only 29% trust them, and 66% cite "almost-right-but-not-quite" output as the biggest frustration. Tome's `[Inference: evidence]` labelling is the explicit hedge for this gap — never copy AI-generated rationale unverified. [Source: stackoverflow.blog 2025-12-29 — 2025 Developer Survey; survey.stackoverflow.co/2025/ai]
- **Workflow guardrail.** When AI drafts a learning doc, run the Tome Quality Scorecard against it before delivery — unverified AI claims default to `C` on the Fact/Inference Ratio axis until they are either cited or marked as inference.
