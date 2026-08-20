# Grok — AUTORUN `_STEP_COMPLETE` Schema

See `_common/AUTORUN.md` for the protocol (`_AGENT_CONTEXT` input, mode semantics, error handling). On AUTORUN, run `ANALYZE → GRAMMAR → IMPLEMENT → HARDEN → DOCUMENT` and emit `_STEP_COMPLETE`. Grok-specific Constraints in `_AGENT_CONTEXT`: runtime target, input trust level, engine preference, grammar class, error-message quality target.

Grok-specific `_STEP_COMPLETE.Output` schema:

```yaml
_STEP_COMPLETE:
  Agent: Grok
  Status: SUCCESS | PARTIAL | BLOCKED | FAILED
  Output:
    deliverable: [artifact path or inline grammar/regex]
    artifact_type: Grammar Spec | Regex Audit | DSL Design | AST Transform Plan
    parameters:
      grammar_class: regular | LL(k) | LR(1) | LALR | PEG | Earley | GLR
      engine_choice: RE2 | PCRE | ECMAScript | Oniguruma | hand-written | tree-sitter | ANTLR4 | Chevrotain
      redos_complexity: O(n) | O(n*m) | O(n^2) | exponential | n/a
      ambiguities_resolved: [count]
      test_corpus_size: {positive, negative, worst_case}
    files_changed: List[{path, type, changes}]
  Handoff:
    Format: GROK_TO_[NEXT]_HANDOFF
    Content: [Handoff content for next agent]
  Risks: [Ambiguities tolerated; non-linear regex engine requirements; Unicode edge cases]
  Next: Builder | Radar | Sentinel | Canon | Atlas | Judge | Shift | DONE
  Reason: [Why this Status/Next; if BLOCKED/FAILED, what is needed to unblock]
```

---
