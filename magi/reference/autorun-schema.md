# Magi — AUTORUN `_STEP_COMPLETE` Schema

See `_common/AUTORUN.md` for the protocol (`_AGENT_CONTEXT` input, mode semantics, error handling).

Magi-specific `_STEP_COMPLETE.Output` schema:

```yaml
_STEP_COMPLETE:
  Agent: Magi
  Status: SUCCESS | PARTIAL | BLOCKED | FAILED
  Output:
    deliverable: [verdict path or inline]
    artifact_type: "[Architecture | Trade-off | Go/No-Go | Strategy | Priority | Tri-Engine N-Cell] Verdict"
    parameters:
      domain: "[Architecture | Trade-off | Go/No-Go | Strategy | Priority]"
      mode: "[Simple | Engine | Multi]"
      consensus: "[3-0 | 2-1 | 1-1-1 | 0-3]"
      weighted_confidence: "[0-100]"
      dissent: "[perspective and rationale, or none]"
      risk_count: "[count]"
    tri_engine:                                  # present only when `multi` Recipe ran
      engines_run: [codex, agy, claude]          # subset reflecting AVAILABLE engines
      engines_failed: [list or none]
      matrix_size: "[9-cell | 6-cell | 3-cell]"
      # Per-viewpoint concurrence — each viewpoint (logos/pathos/sophia) tagged as:
      #   "<CONFIRMED|LIKELY|CANDIDATE|UNDECIDED> <CONVERGENT|DIVERGENT-N>"
      per_viewpoint_concurrence: { logos: "...", pathos: "...", sophia: "..." }
      # Per-engine consistency — each engine tagged as:
      #   consistent | mostly-aligned | internally-split | consistent-reject
      per_engine_consistency: { codex: "...", agy: "...", claude: "..." }
      matrix_pattern: "[all-cells-approve | all-cells-reject | logos-pathos-split | pathos-block | engine-bias-asymmetry | all-internally-split | other]"
      final_verdict: "[GO | NO-GO | CONDITIONAL | ESCALATE]"
      devils_advocate_run: [true | false]        # true when matrix is all-cells-unanimous
      rejected_cells: [count + top categories — hallucination / mitigated / vague / overconfident]
  Next: Builder | Forge | Atlas | Launch | Sherpa | Nexus | DONE
  Reason: [Why this next step]
```
