# Delivery Checkpoint Format

Load when persisting/resuming `.agents/nexus-delivery-state.md`. Final output is the **Delivery Report** in `reference/deliver-recipe.md` plus `NEXUS_COMPLETE` from `reference/output-formats.md`; do not emit a second, competing completion protocol.

## NEXUS_DELIVERY_STATE

```markdown
## NEXUS_DELIVERY_STATE
- **Project**: [project]
- **Goal**: [frozen user goal, verbatim]
- **Scope**: small | medium | epic
- **Current Phase**: [phase from the selected deliver contract]
- **Phase Progress**: [completed / applicable phases]
- **Epic Progress**: [verified / applicable work packages in this phase]
- **Risk Budget**: [used / authorized limit, or not applicable with reason]
- **Stall Budget**: [used / limit by applicable recovery tier]
- **SUCCESS_CRITERIA**: [frozen AC IDs, targets, PASS/FAIL/UNVERIFIED and evidence]
- **Blockers**: [typed residual ID, dependency, owner and next authorized action]
- **Next Action**: [specific step and its unmet prerequisites]
- **Decision Log**: [path and relevant DEC IDs]
- **Last Updated**: [timestamp with timezone]
- **Update Trigger**: [epic_complete | phase_transition | decision_recorded | antistall_activated | antistall_resolved | rally_start | rally_complete | magi_verdict | scope_change | session_boundary]

### Phase Status
| Phase | Status | Entry Date | Exit Date | Epics |
|---|---|---|---|---|
| [applicable phase] | [verified/in-progress/blocked/not-applicable] | [time] | [time] | [verified/total] |

### Current Roadmap
#### [phase] — [status]
- [x] [verified work package and evidence]
- [ ] [remaining work package, owner, next check]
```

## Resume and transition rules

- Update at each work-package/phase boundary and before a session boundary. Store artifact paths, source revision and verification evidence with the corresponding work package; existence/non-empty text alone is not completion.
- Revalidate the repository revision, artifact evidence, pending approvals and permissions on resume. Stale checkpoints are inputs to reconciliation, not authority to replay side effects.
- Load risk decisions from `reference/delivery-decision-matrix.md`, bounded recovery from `reference/delivery-anti-stall-engine.md`, and applicable exit checks from `reference/delivery-exit-criteria-validation.md` only when that transition needs them.
- Preserve diagnosed attempts and consumed recovery budgets; do not repeat an exhausted attempt merely because the executor changed. Two identical failures require diagnosis.
- An old S/M/L/XL or nine-phase checkpoint must be explicitly reconciled to the selected recipe before continuing. No silent scope conversion, denominator shrinkage, target lowering or completed-state inflation.
- Phase reports carry produced artifacts, AC evidence, decisions, residuals and next prerequisites using the shared handoff. A next iteration is a newly scoped objective; it cannot retroactively turn this iteration's failed ACs into passes.
