# Prose — AUTORUN `_STEP_COMPLETE` Schema

See `_common/AUTORUN.md` for the protocol (`_AGENT_CONTEXT` input, mode semantics, error handling).

Prose-specific `_STEP_COMPLETE.Output` schema:

```yaml
_STEP_COMPLETE:
  Agent: Prose
  Status: SUCCESS | PARTIAL | BLOCKED | FAILED
  Output:
    deliverable: [copy path or inline]
    artifact_type: "[Microcopy | Error Messages | Voice Framework | Onboarding Copy | Accessibility Text | AI Context Copy | Content Audit]"
    parameters:
      mode: "[CRAFT | AUDIT | VOICE | ONBOARD | A11Y | DESIGN | DISCLOSE]"
      copy_items: "[count]"
      voice_alignment: "[aligned | new framework | framework update]"
      a11y_coverage: "[ARIA labels, alt text count]"
      translation_ready: "[yes | no]"
  Next: Echo | Polyglot | Artisan | Palette | DONE
  Reason: [Why this next step]
```
