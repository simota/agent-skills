# Mutation Testing Delta

Purpose: Siege `mutate` program-level selection, baseline, and CI contract. Mutation operators and tool basics are model-known.

## Program Contract

- Select the tool from the repository language, runner, and installed versions; verify current syntax in primary docs.
- Establish a baseline on a bounded, behavior-critical module before setting a gate.
- Exclude generated code, migrations, declarations, and proven equivalent-mutant regions explicitly.
- Classify survivors as missing test, weak assertion, dead code, uncovered code, timeout, or equivalent mutant.
- Start with the risk-tier defaults in `siege/SKILL.md` when no local policy exists, then calibrate them from the measured baseline, runtime budget, and module criticality.

```text
mutation_score = killed / (total - no_coverage - accepted_equivalent) × 100
```

## CI Strategy

| Tier | Scope |
|---|---|
| PR | changed or critical modules within a fixed time budget |
| Nightly | broader incremental suite |
| Release | risk-selected full baseline comparison |

Fail only on a documented regression or risk-tier gate. Report timeouts and no-coverage separately so score improvements cannot hide shrinking scope.

## Required Output

Provide tool/version, source/test scope, exclusions, baseline and current scores, survivor classification, runtime cost, new tests or removals, accepted equivalents with rationale, and proposed CI gate. Hand individual assertion fixes to Radar; hand dead code to Sweep/Zen.
