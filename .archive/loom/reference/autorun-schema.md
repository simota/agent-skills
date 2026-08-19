# Loom — AUTORUN `_STEP_COMPLETE` Schema

See `_common/AUTORUN.md` for the protocol (`_AGENT_CONTEXT` input, mode semantics, error handling).

Loom-specific `_STEP_COMPLETE.Output` schema:

```yaml
_STEP_COMPLETE:
  Agent: Loom
  Task_Type: BLUEPRINT | RECIPE | WORKFLOW | MAP | AUDIT
  Status: SUCCESS | PARTIAL | BLOCKED | FAILED
  Output:
    project: <name + detected stack>
    coverage_matrix:
      - task: <recurring task>
        mechanism: skill | recipe | workflow | hook | scoped_rule | none
        owner: <agent or skill that will own it>
    suite_plan:
      skills: [<proposed project skill names>]
      recipes: [<proposed recipe subcommands>]
      workflows:
        - name: <workflow name>
          topology: hub-spoke | pipeline | hierarchy
          phases: <int (<= 5)>
    routing_map: <which agent/skill owns which task domain>
    delegations:
      - to: Sigil | Nexus | Orbit | Latch | Grove | Architect
        payload: <what that agent receives>
    overlap:
      intra_suite_max: <pct>
      ecosystem_max: <pct + agent if any>
      deferrals: [<task -> existing agent>]
    validation: <pass | fail + failing items>
  Handoff:
    schema: see `_common/HANDOFF.md`
    recommended_next:
      - Sigil   # to author the skill bodies
      - Nexus   # to register routing + chains
      - Orbit   # when a workflow needs an autonomous loop
      - Latch   # when an enforcement hook is part of the layer
  Next: <agent name> | DONE
  Reason: <terse cause for non-SUCCESS, or "blueprint validated; delegations emitted" for SUCCESS>
```

Full schema definitions → `_common/AUTORUN.md`.
