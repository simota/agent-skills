# Chaos Experiment Safety Contract

Purpose: Siege `chaos` safety, authorization, and output contract. Fault catalogs and tool syntax are model-known and must be verified against the target environment.

## Preconditions

- Named owner and explicit authorization for the target environment.
- Steady-state SLI baseline and observation window.
- One falsifiable hypothesis and one bounded fault.
- Known blast radius, affected tenants/data, and protected exclusions.
- Tested kill switch, rollback/recovery procedure, and on-call coverage.
- Abort thresholds tied to user impact, data integrity, and recovery time.

Production, shared infrastructure, data-destructive faults, DNS/network policy changes, and broad resource exhaustion require explicit confirmation. Start in an isolated or canary scope.

## Experiment Record

```yaml
chaos_experiment:
  target: "..."
  hypothesis: "..."
  baseline: [{sli: "...", expected: "..."}]
  fault: {type: "...", scope: "...", duration: "..."}
  abort_conditions: []
  kill_switch: "..."
  recovery: "..."
  observers: []
  evidence: []
```

## Execution Gates

1. Capture baseline and confirm telemetry freshness.
2. Inject one fault and continuously evaluate abort conditions.
3. Abort immediately on data corruption, unexpected scope expansion, missing telemetry, or kill-switch failure.
4. Restore and prove recovery before any next experiment.
5. Record timeline, observed behavior, gaps, owners, and due dates.

Never copy a destructive command from a generic reference into an environment without resolving exact targets and rollback behavior.
