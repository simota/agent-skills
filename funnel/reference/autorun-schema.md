# Funnel — AUTORUN `_STEP_COMPLETE` Schema

When invoked with `_AGENT_CONTEXT`, parse task scope and constraints, execute BRIEF → STRUCTURE → COPY → BUILD → OPTIMIZE workflow, skip verbose explanations, and return `_STEP_COMPLETE`.

### `_STEP_COMPLETE`

```yaml
_STEP_COMPLETE:
  Agent: Funnel
  Status: SUCCESS | PARTIAL | BLOCKED | FAILED
  Output:
    framework: "[AIDA/PAS/BAB/4Ps]"
    sections: "[list of sections with purpose]"
    headline: "[main headline]"
    cta_primary: "[primary CTA copy]"
    files_changed:
      - path: "[file path]"
        type: "[created / modified]"
        changes: "[brief description]"
  Handoff:
    Format: FUNNEL_TO_[NEXT]_HANDOFF
    Content: "[Full handoff for next agent]"
  Risks:
    - "[Identified conversion risks]"
  Next: Artisan | Growth | Echo | Experiment | DONE
  Reason: "[Why this next step]"
```
