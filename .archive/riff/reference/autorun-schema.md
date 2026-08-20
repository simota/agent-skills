# Riff — AUTORUN `_STEP_COMPLETE` Schema

See `_common/AUTORUN.md` for the protocol (`_AGENT_CONTEXT` input, mode semantics, error handling).

Riff-specific `_STEP_COMPLETE.Output` schema:

```yaml
_STEP_COMPLETE:
  Agent: Riff
  Status: SUCCESS | PARTIAL | BLOCKED | FAILED
  Output:
    session_summary:
      original_theme: [Starting point]
      key_insights:
        - [Insight 1]
        - [Insight 2]
        - [Insight 3]
      idea_candidates:
        - [Candidate 1 with brief context]
        - [Candidate 2 with brief context]
      open_questions:
        - [Unresolved question]
    files_changed: []
    tri_engine:                                  # present only when `multi` Recipe ran
      engines_run: [codex, agy, claude]
      engines_failed: [list or none]
      mode_coverage: "[single-mode | all-modes]"
      active_mode: "[expand | propose | evaluate | subtract | ALL]"
      output_shape: "[per-mode-portfolio | all-modes-matrix]"
      concurrence_distribution:                  # per active mode (or summed across modes when --all-modes)
        UNIVERSAL: [count]
        LIKELY: [count]
        VERIFIED-DIVERGENT: [count]
      rejected: [count + top categories — duplicate-of-prior-turn / hallucination / theme-disconnect / mode-mismatch / sugar-coat]
      user_picks: [list of idea IDs the user selected as seeds for next dialogue turn, or "none yet"]
  Handoff:
    Format: RIFF_TO_[NEXT]_HANDOFF
    Content: [Brainstorming results for next agent]
  Artifacts: []
  Risks:
    - [Identified risks or blind spots]
  Next: [NextAgent] | VERIFY | DONE
  Reason: [Why this next step]
```
