# New-Skill Nexus Integration

Use when adding or changing a routing surface. The shared envelopes and hub behavior are authoritative in `_common/AUTORUN.md` and `_common/HANDOFF.md`; read them rather than reimplementing `_AGENT_CONTEXT`, `NEXUS_HANDOFF` or direct-spawn instructions here. The skill-specific completion fields remain in `reference/autorun-schema.md`.

## Routing Records

Choose an existing task type when it accurately represents the owned outcome; add a type only for a real uncovered route. Inspect the current routing registry, not a cached list of task types. Record both the chain placement and positive/negative triggers:

```yaml
ROUTING_ENTRY:
  task_type: "[TASK_TYPE]"
  simple_chain:
    - "[Agent1]"
    - "[NewAgent]"
    - "[Agent2]"
  complex_chain:
    - "[Agent1]"
    - "[Sherpa]"
    - "[NewAgent]"
    - "[Agent2]"
    - "[Agent3]"
  additions:
    - condition: "[Condition]"
      add: "[Agent]"
```

```yaml
TRIGGER_REGISTRATION:
  keywords:
    - "[keyword1]"
    - "[keyword2]"
    - "[keyword3]"

  patterns:
    - "[pattern with wildcards]"

  negative_patterns:
    - "[patterns that should NOT trigger]"
```

## Integration Gate

- A direct positive request and a Nexus-chain request both reach the intended owner; negative requests stay with their existing owner.
- Upstream inputs, downstream output fields and partial/blocked behavior agree with the actual partner contracts.
- The hub receives pending confirmations, completion state and a proposed next step; a handoff recommendation never directly invokes another specialist.
- Shared paths resolve from the installed skill directory and required contracts are actually delivered. Optional project-local partners follow `_common/PROJECT_LOCAL_SKILLS.md`.
- Update the current routing/roster registries required by the repository's authoring instructions; do not maintain copies in this reference.
- Exercise new/changed routing and error cases. Record unexecuted cases as unverified.

Use the existing hub guardrails and owning lifecycle rules for escalation or rollback. A failed integration test does not authorize deleting an existing skill or bypassing its retirement/migration approvals.
