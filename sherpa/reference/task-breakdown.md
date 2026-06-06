# Task Breakdown Framework

Purpose: Use this file during `MAP` to define hierarchy, size work, estimate effort, and stop decomposition at the right granularity.

## Contents

- Task hierarchy
- Epic input template
- T-shirt sizing
- Complexity factors
- Estimation formula
- Breakdown rules

## Task Hierarchy

| Level | Size | Description | Example |
| --- | --- | --- | --- |
| Epic | `1-5 days` | large feature or initiative | “Implement payment system” |
| Story | `2-8 hours` | user-facing slice | “Add checkout form” |
| Task | `30-120 min` | technical work unit | “Create PaymentForm component” |
| Atomic Step | `5-15 min` | single testable, committable action | “Define PaymentProps interface” |

## Epic Input Template

```markdown
## Epic: [Name]

**Goal**: [What we are trying to achieve]
**Success Criteria**: [How we know it is done]
**Constraints**: [Time, tech, scope limits]
**Out of Scope**: [What we are not doing]

**Initial Estimate**: [XS/S/M/L/XL]
**Risk Level**: [Low / Medium / High]
```

## T-Shirt Sizing

| Size | Minutes | Interpretation |
| --- | --- | --- |
| XS | `5-10` | trivial, clear path, no unknowns |
| S | `10-15` | simple and ready to execute |
| M | `15-30` | too large for an atomic step, split further |
| L | `30-60` | complex task, must be decomposed |
| XL | `60+` | always decompose immediately |

## Complexity Factors

| Factor | Multiplier | Meaning |
| --- | --- | --- |
| New technology | `1.5x` | first time using a library or API |
| Unclear requirements | `1.5x` | investigation still needed |
| External dependency | `2.0x` | approval, third party, or cross-team dependency |
| High risk | `1.5x` | could break existing functionality |
| Multiple files | `1.3x` | changes span several modules |

## Estimation Formula

```text
Actual Time = Base Estimate × Complexity Multiplier × Risk Buffer

Risk Buffer:
- Low: 1.0x
- Medium: 1.3x
- High: 1.5x
```

### Estimation Output

```markdown
### Time Estimate: [Step Name]

| Aspect | Value |
|--------|-------|
| Base Size | M (20 min) |
| Complexity | New API (1.5x) |
| Risk Level | Medium (1.3x) |
| Estimated | 39 min |

Over the 15-minute threshold -> split further.
```

## Breakdown Rules

1. Keep breaking work down until the current step is under `15 min`.
2. Every atomic step must be testable.
3. Every atomic step must be committable.
4. Identify the responsible agent for each step.
5. mark dependencies before execution starts.
6. Flag XL items immediately.

## Sources

- DORA 2025 report — small, frequent commits correlate with higher software delivery performance. AI-generated PRs are 51% larger on average; atomic decomposition counteracts cognitive-overload and review-skip risk. [dora.dev/research/2025/dora-report/](https://dora.dev/research/2025/dora-report/)
- SAFe 6.0 Story hierarchy and "Reimagining SAFe" (2024-2025 updates) — Epic → Feature → Story → Task granularity. [framework.scaledagile.com/whats-new-in-safe-6-0/](https://framework.scaledagile.com/whats-new-in-safe-6-0/)
- Linear Agent (March 2026) — AI-generated issue hierarchies as raw MAP-phase input for Sherpa validation. [linear.app/changelog/2026-03-24-introducing-linear-agent](https://linear.app/changelog/2026-03-24-introducing-linear-agent)
