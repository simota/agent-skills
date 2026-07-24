# Polyglot — AUTORUN `_STEP_COMPLETE` Schema

See `_common/AUTORUN.md` for the protocol (`_AGENT_CONTEXT` input, mode semantics, error handling).

Polyglot-specific `_STEP_COMPLETE.Output` schema:

```yaml
_STEP_COMPLETE:
  Agent: Polyglot
  Status: SUCCESS | PARTIAL | BLOCKED | FAILED
  Output:
    deliverable: [file paths or inline]
    artifact_type: "[String Extraction | Intl Integration | ICU Messages | Key Structure | RTL Support | Library Setup | Glossary | Audit Report]"
    parameters:
      strings_extracted: "[count]"
      namespaces: ["[namespace list]"]
      locales_affected: ["[locale list]"]
      intl_apis_used: ["[API list]"]
      rtl_changes: "[yes | no]"
      coverage_delta: "[before% → after% per locale]"
      pseudo_locale_configured: "[yes | no]"
  Next: Radar | Muse | Canvas | Quill | Gear | Voyager | DONE
  Reason: [Why this next step]
```
