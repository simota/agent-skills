# Zine — AUTORUN `_STEP_COMPLETE` Schema

See `_common/AUTORUN.md` for the protocol (`_AGENT_CONTEXT` input, mode semantics, error handling). On AUTORUN, run `FRAME → DRAFT → STRUCTURE → POLISH → PUBLISH` and emit `_STEP_COMPLETE`. Zine-specific Constraints in `_AGENT_CONTEXT`: `Platform`, `Series`, `Tone`, `Length`, `Language`.

Zine-specific `_STEP_COMPLETE.Output` schema:

```yaml
_STEP_COMPLETE:
  Agent: Zine
  Status: SUCCESS | PARTIAL | BLOCKED | FAILED
  Output:
    deliverable: [article path or inline Markdown]
    artifact_type: Article Draft | Article + Series Index Update | Cross-post Variants
    parameters:
      platform: note | Zenn | Qiita | dev.to | cross-post
      series_position: standalone | series-name-#NN | index
      hook_type: contradiction | number | scene | question | stake
      word_count: [字数 or word count]
      tone: first-person | teaching | opinionated | detached
      cta_type: subscribe | try | share | next-episode | discuss
    files_changed: List[{path, type, changes}]
  Handoff:
    Format: ZINE_TO_[NEXT]_HANDOFF
    Content: [Handoff content for next agent]
  Risks: [LOW CONFIDENCE technical claims; internal-leak risk; tonal drift]
  Next: Growth | Prose | Stage | Canvas | Saga | Morph | DONE
```

---
