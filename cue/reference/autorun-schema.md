# Cue — AUTORUN `_STEP_COMPLETE` Schema

See `_common/AUTORUN.md` for the protocol (`_AGENT_CONTEXT` input, mode semantics, error handling).

Cue-specific `_STEP_COMPLETE.Output` schema:

```yaml
_STEP_COMPLETE:
  Agent: Cue
  Status: SUCCESS | PARTIAL | BLOCKED | FAILED
  Output:
    deliverable: [artifact path or inline]
    video_type: "[product-demo | explainer | tutorial | onboarding | social | comparison]"
    parameters:
      duration: "[target seconds]"
      scene_count: [N]
      word_count: [N]
      platform: "[YouTube | Twitter | Product Hunt | landing | general]"
      template: "[Problem-Solution | AIDA | Before-After | Step-by-Step | Hook-Payoff]"
    cta: "[CTA description and placement]"
  Next: Cue[demo] | DONE
  Reason: [Why this next step]
```
