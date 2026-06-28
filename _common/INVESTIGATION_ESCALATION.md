# Investigation Escalation Protocol

Escalation standard across the investigation skill cluster (Scout, Lens, Trail).

## Escalation Flow

```
[Vague Report / Unknown Issue]
    │
    ▼
  Lens (SCOPE→SURVEY) ─── comprehension sufficient ─── DONE
    │
    ▼ anomaly pattern / potential bug found
  Scout (TRIAGE→TRACE) ─── bug identified ─── Builder handoff
    │
    │ history investigation needed
    ▼
  Trail (bisect/archaeology)
```

## Ownership Rule

One bug = one leader skill. Others serve as support roles. The leader is the skill that first completes TRIAGE/SCOPE.

## Unified Confidence Scale

| Level | Score | Evidence Threshold | Reporting Rule |
|-------|-------|--------------------|----------------|
| `HIGH` | ≥ 0.8 | 3+ independent evidence | Report as confirmed |
| `MEDIUM` | 0.5–0.79 | 2 independent evidence | Report as estimated; add verification steps |
| `LOW` | < 0.5 | ≤1 evidence | Report as hypothesis; list missing information |

## Cross-Cluster Handoff Formats

### LENS_TO_SCOUT_HANDOFF

```yaml
LENS_TO_SCOUT_HANDOFF:
  investigation_id: "[unique-id]"
  discovery_type: "[anomaly_pattern | potential_bug | dead_code_risk | comprehension_debt_hotspot]"
  location: "[file:line references]"
  evidence: "[what was observed during comprehension]"
  severity_estimate: "[HIGH | MEDIUM | LOW]"
  suggested_investigation_mode: "[Focused Hunt | History-Led | Observability-Led | Multi-Engine | Cascading Failure]"
```

### SCOUT_TO_LENS_HANDOFF

```yaml
SCOUT_TO_LENS_HANDOFF:
  investigation_id: "[unique-id]"
  request_type: "[context_needed | flow_trace_needed | dependency_map_needed]"
  bug_context: "[what is known so far]"
  specific_questions: "[what Scout needs to understand]"
  scope_hint: "[files/modules to focus on]"
```

## Stall Protocol (Cross-Cluster)

1. 3 probes without progress → switch hypothesis
2. All hypotheses exhausted → escalate to adjacent skill
3. 3+ round-trips between 2 skills → promote to Nexus (prevent Agent Tennis)

## Duplicate Investigation Prevention

- Do not start parallel investigations on the same bug across multiple skills
- Pass the Investigation_ID on escalation to prevent duplication
- The leader skill aggregates all escalation results and integrates them into the final report
