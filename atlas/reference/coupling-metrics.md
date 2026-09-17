# Coupling and Architecture Health

Load for `coupling`, architecture health, or fitness-function design. Record module boundaries, graph scope, tool/version and evidence before scoring; raw import-line frequency is not a count of distinct dependent modules. Apply targets by role, not by globally minimizing a metric.

## Core Metrics

| Metric | Definition | Interpretation |
|--------|------------|----------------|
| Ca | Count of distinct modules depending on this module | Fan-in; a legitimate foundation may be high. |
| Ce | Count of distinct modules this module depends on | Fan-out. |
| I | `Ce / (Ca + Ce)` | Use 0 for an isolated node as this report's calculation convention; label it isolated rather than inferring stability from reuse. |
| A | Abstract types / total types | Bind abstract-type counting to the actual language. With no countable types, report N/A rather than inventing a fraction. |
| D | `abs(A + I - 1)` | Distance from `A + I = 1`; N/A when A is unavailable. |

| Classification | Criterion | Proposed action |
|----------------|-----------|-----------------|
| Main Sequence | D < 0.3 | Preserve. |
| Acceptable drift | 0.3 ≤ D < 0.5 | Monitor. |
| Outside band | D ≥ 0.5 | Investigate against role and change evidence. |
| Zone of Pain | A < 0.2 and I < 0.2 | Stable abstraction / public-API boundary; check actual downstream impact. |
| Zone of Uselessness | A > 0.8 and I > 0.8 | Verify consumers; propose deletion via Void or connect a real consumer. |
| Unstable foundation | I > 0.7 and Ca > 5 | Reduce Ce or separate stable core from unstable extension. |
| Over-abstract | A > 0.6 and Ca < 2 | Check whether a real variant warrants the abstraction; otherwise route to Void. |

| Module role | Target I | Target A |
|-------------|----------|----------|
| Domain model/entities | 0.0–0.2 | 0.6–0.9 |
| Shared library/SDK | 0.0–0.2 | 0.7–0.9 |
| Service/application | 0.3–0.6 | 0.3–0.5 |
| Adapter/infrastructure | 0.6–1.0 | 0.0–0.3 |
| Entry point/CLI/UI | 0.8–1.0 | 0.0–0.2 |

Small modules can have volatile ratios; declare the minimum sample size/exclusions. Do not classify a zone from I alone or treat every high-Ca foundation as defective.

## Architecture Health / Fitness Targets

Use these existing Atlas review targets unless a justified project-specific target is declared. Distinguish warning/reporting targets from authorized blocking CI policy.

| Metric | Target |
|--------|--------|
| Ca / Ce per module | Ca <20; Ce <10, interpreted with the role table |
| Instability bands | 0.0–0.3 (stable) or 0.7–1.0 (flexible), subject to role |
| Distance | D <0.3 |
| Lines / functions per file | <500 lines; <20 functions |
| Cyclomatic complexity | <10 per function |
| Dependency depth | <5 levels |
| Circular dependencies | 0 |

Use the repository's configured module graph, AST counters and architecture rules. Confirm installed tool support rather than copying commands for another language. A function-length rule does not count functions per file; a suppressed analyzer error is not a passing fitness function. Define each new check's expected failure and test it against a known violation without overwriting existing CI/configuration.

## Report

Required evidence: date/scope/tool, per-module Ca/Ce/I/A/D and role, zone distribution and named offenders, complexity actual/target/status, layer violations, debt categories and priority actions. For each proposal include the evidence, target, effort, handoff and fitness-function baseline/acceptance condition. Report unmeasured values as unmeasured; do not reuse fictional example counts or derive a zone from a metric the tool never computed.

Language-specific graph/API evidence: `reference/module-boundary-evaluation.md`. Cycle treatment: `reference/circular-dependency-remediation.md`.
