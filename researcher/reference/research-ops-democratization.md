# Research Ops & Democratization

Purpose: ResearchOps maturity, repository design, Atomic Research, and self-service governance.
Contents: maturity levels, Atomic Research model, repository rules, democratization boundaries, tool selection.

## ResearchOps Maturity

| Level | Name | Characteristics | Researcher response |
|-------|------|-----------------|---------------------|
| L1 | Ad-hoc | Sporadic research, no standard process | Run DEFINE basics |
| L2 | Emerging | Dedicated researcher, basic tools | Use full study workflow |
| L3 | Scaling | ResearchOps support, repository, democratization | Add DISTILL and governance |
| L4 | Strategic | Research in decision-making, AI-enabled ops | Use full workflow plus AI guardrails |

## Atomic Research

```text
Experiments
  -> Facts
    -> Insights
      -> Recommendations
```

Principles:
- atomic granularity
- reuse across decisions
- traceability from recommendation back to evidence
- searchable taxonomy

## Repository Essentials

- tag by theme, segment, study type, confidence, and freshness
- preserve traceability from recommendation to evidence
- keep insight cards reusable across reports

## Democratization Governance

| Level | Who | Allowed work | Governance |
|-------|-----|--------------|------------|
| Self-service | PM / Designer / Engineer | unmoderated usability tests, short surveys, qualitative follow-up to experiments | templates + guidelines |
| Guided | PwDR with researcher support | moderated interviews, themed synthesis | researcher review |
| Expert-led | Dedicated researcher | strategic, mixed-methods, sensitive, or complex studies | full research workflow |

## Self-Service Boundaries

Allowed:
- unmoderated usability tests with `5-6` participants
- short surveys (`<=10` questions)
- qualitative follow-up for experiments
- heuristic competitor reviews

Do not self-service:
- exploratory interviews
- sensitive topics
- vulnerable populations
- large mixed-methods studies

## Tool Selection

| Situation | Default choice |
|-----------|----------------|
| Team of `5+` researchers, democratization active | Dovetail or Condens |
| Solo researcher, lightweight ops | Notion or Airtable with templates |
| Strong panel-management need | Rally |
| Stakeholder-sharing emphasis | EnjoyHQ |
