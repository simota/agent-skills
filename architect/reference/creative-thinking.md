# ENVISION: Value Before a New Agent

Read before drafting a new agent. Use the effort budget and completion gates in SKILL.md; record design decisions, not a prescribed private reasoning transcript.

| Axis | Question that changes the design | Required outcome |
|------|---------------------------------|------------------|
| HEIGHT | Is a different framing or no new agent a better solution? | Compare the proposed abstraction with alternatives |
| BREADTH | Can existing owners or a combination of their capabilities satisfy the need? | Identify reuse and the remaining gap |
| DEPTH | Which root need would still fail after those alternatives? | State the nontrivial capability the new owner must provide |

Synthesize one design premise, its unique value and the constraints it implies. A candidate that adds only a new name or workflow wording does not close a gap.

## Value-First Checklist

```yaml
VALUE_FIRST_CHECKLIST:
  world_comparison:
    without_agent: "[current outcome]"
    with_agent: "[changed outcome]"
    delta: "[specific improvement]"
  primary_beneficiary:
    persona: "[who needs it]"
    pain_point: "[current failure]"
    frequency: "[how often it occurs]"
  success_metric:
    primary: "[measured outcome]"
    measurement: "[how it will be checked]"
    target: "[acceptance threshold]"
```

Before ANALYZE, verify that the problem is understood, all three axes were considered, the value record is complete, not building was considered, and extending an existing agent cannot deliver the required outcome. Missing evidence is a gap to resolve, not a reason to invent a benefit.
