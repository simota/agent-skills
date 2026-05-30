<!-- If ARTIFACT_NOUN is `none`, delete this directory when rendering. Otherwise rename to {{ARTIFACT_DIR}}/. -->
# {{ARTIFACT_NOUN}}s

Evidence that demonstrates a {{RULE_NOUN}}. Supporting artifacts, not the source of truth — the rule files are. Store reference {{ARTIFACT_NOUN}}s and Before/After pairs here.

## Naming convention
```
{{ARTIFACT_DIR}}/
  {{RULE_PREFIX}}-CORE-<slug>__do.<ext>
  {{RULE_PREFIX}}-CORE-<slug>__dont.<ext>
  {{SIGNAL_PREFIX}}-YYYYMMDD-<slug>__before.<ext>
  {{SIGNAL_PREFIX}}-YYYYMMDD-<slug>__after.<ext>
```
- Prefix with the **{{RULE_NOUN}} slug** or **{{SIGNAL_NOUN}} ID** it belongs to so links never rot.
- Use `__do` / `__dont` / `__before` / `__after` suffixes for comparisons.

## Linking
Reference {{ARTIFACT_NOUN}}s from rule entries (`rules/*.md`) and signal entries by filename.
