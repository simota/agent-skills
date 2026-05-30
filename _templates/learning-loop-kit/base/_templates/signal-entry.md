# {{SIGNAL_NOUN}} Entry Template

Append this block to `{{SIGNAL_LOG}}` during CAPTURE (fill `status: new`; leave Analysis/Proposed blank until ANALYZE).

## ID scheme (collision-free)
`{{SIGNAL_PREFIX}}-<YYYYMMDD>-<slug>` — capture date + short kebab mnemonic.
- Date + slug avoids the shared-counter collision that plain `-NNN` causes on same-day concurrent logging.

```markdown
### {{SIGNAL_PREFIX}}-YYYYMMDD-<slug>
- **Date:** YYYY-MM-DD
- **Source:** <one of {{SIGNAL_SOURCES}}>
- **Layer:** <one of {{LAYERS}}>
- **Raw {{SIGNAL_NOUN}}:** "<verbatim or close paraphrase — keep original words>"
- **Analysis:** <ANALYZE: theme cluster + severity; blank until analyzed>
- **Proposed {{RULE_NOUN}}:** <{{RULE_PREFIX}}-...-slug draft, or 'none'; blank until analyzed>
- **Status:** new | analyzed | promoted | rejected
- **Reviewed by:** <human, REVIEW step> · **Decision date:** YYYY-MM-DD
<!-- if promoted: -->
- **Promoted to:** {{RULE_PREFIX}}-<LAYER>-<slug>
<!-- if rejected: -->
- **Reject reason:** <why — e.g. below threshold, out of scope, contradicts {{RULE_PREFIX}}-...>
```

## Rules
- **Keep original words** in Raw {{SIGNAL_NOUN}} — interpretation belongs in Analysis.
- **Promotion threshold:** {{PROMOTION_THRESHOLD}}. Below that → mark `analyzed` and leave to accumulate; don't promote one-offs.
- **One signal ≠ one law.** A lone low-severity item can be `analyzed` then `rejected` with a reason; the rejection is useful history.
- **Tag the Layer** so ANALYZE knows whether the resulting {{RULE_NOUN}} is core or a delta.
- **Archive yearly:** move resolved prior-year entries to a `<{{SIGNAL_LOG}} basename>-<YEAR>.md` sibling when the log grows large.
