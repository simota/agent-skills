# Narrative Arc Delta

Purpose: Stage `narrative` planning and handoff contract. Story frameworks are model-known.

## Design Gates

- Write one audience-specific governing idea before drafting slides.
- Select an arc because it fits the audience's decision or experience, not because the framework is fashionable.
- Build beats from supplied evidence and claims that can be sourced.
- Assign a time budget to each beat using the actual event format, Q&A, demo, and transition constraints.
- Open with the most decision-relevant tension, contradiction, or question; do not fabricate a statistic for a hook.
- End with one primary action appropriate to the audience and setting.

## Required Output

```yaml
narrative_design:
  audience: "..."
  governing_idea: "..."
  framework: "..."
  selection_reason: "..."
  beats: [{label: "...", purpose: "...", evidence: "...", duration_sec: 0}]
  opening: "..."
  primary_action: "..."
  total_duration_sec: 0
  unresolved_claims: []
```

## Verification

- Beat durations plus demo, transition, and Q&A time fit the hard clock.
- The governing idea survives when slide titles are read alone.
- Tension resolves through evidence rather than rhetoric.
- Format-specific rules such as PechaKucha or Ignite are verified against the event's current primary documentation.
- Hand off to Stage `draft` only after the outline and claims are stable.
