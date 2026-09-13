<!-- If ARTIFACT_NOUN is `none`, delete this directory when rendering. Otherwise rename to {{ARTIFACT_DIR}}/. -->
# {{ARTIFACT_NOUN}}s

Evidence that demonstrates a {{RULE_NOUN}}. Supporting artifacts, not the source of truth — the rule files are. Store reference {{ARTIFACT_NOUN}}s and Before/After pairs here.

## Naming convention
Example names (use the actual rule/signal IDs and an extension matching the artifact type):
```
{{ARTIFACT_DIR}}/
  {{RULE_PREFIX}}-CORE-validate-input__do.txt
  {{RULE_PREFIX}}-CORE-validate-input__dont.txt
  {{SIGNAL_PREFIX}}-20260115-input-validation__before.txt
  {{SIGNAL_PREFIX}}-20260115-input-validation__after.txt
```
- Prefix with the **{{RULE_NOUN}} slug** or **{{SIGNAL_NOUN}} ID** it belongs to so links never rot.
- Use `__do` / `__dont` / `__before` / `__after` suffixes for comparisons.

## Linking
Reference {{ARTIFACT_NOUN}}s from rule entries (`rules/*.md`) and signal entries by filename.
