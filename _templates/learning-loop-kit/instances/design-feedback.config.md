# Kit Config — Design Feedback

The config for **instance #1**, `_templates/design-feedback-kit/`. ⚠ The shipped kit **predates this base** and is a **non-strict render** — it was hand-authored first, then generalized into the base. It is NOT byte-for-byte reproducible from `base/` because of two intentional vocabulary differences:

| Concept | base/ token | shipped design-feedback-kit |
|---------|-------------|------------------------------|
| layer/partition field | `Layer:` | `Scope:` |
| machine-check field | `Check:` | `Token:` |

The base names (`Layer` / `Check`) are the generic forms; the shipped kit's `Scope` / `Token` are domain-flavored. **A fresh render of this config would produce `Layer` / `Check`** — that is correct and expected. Do not "fix" the shipped kit to match; leave it as the predecessor. New kits use the base vocabulary.

This config documents the knob values; the shipped kit is the worked example of the *rendered shape*, not a guaranteed identical output.

```yaml
# --- identity ---
KIT_NAME:            "Design Feedback"
KIT_SLUG:            "design-feedback"
DOMAIN_DIR:          "design"

# --- vocabulary ---
RULE_NOUN:           "principle"
RULE_NOUN_PLURAL:    "principles"
RULE_PREFIX:         "P"                          # P-CORE-control-feedback
SIGNAL_NOUN:         "feedback"
SIGNAL_NOUN_PLURAL:  "feedback"
SIGNAL_PREFIX:       "FB"                          # FB-20260115-double-save
SIGNAL_LOG:          "feedback-log.md"
ARTIFACT_NOUN:       "mockup"
ARTIFACT_DIR:        "mockups"

# --- structure ---
LAYERS:              ["core", "frontend", "ios", "android"]

# --- enums ---
SIGNAL_SOURCES:      ["interview", "usability-test", "review", "support-ticket", "analytics", "app-store-review", "echo-walkthrough"]

# --- skill wiring ---
ANALYZE_SKILLS:      ["voice", "echo", "palette"]
PROMOTE_SKILLS:      ["muse", "vision", "lore"]
ENFORCE_SKILLS:      ["vision", "artisan", "flow", "prose", "native"]
GATE_SKILLS:         ["guardian", "canon", "judge"]

# --- policy ---
PROMOTION_THRESHOLD: ">=2 independent items OR 1 high-severity (data loss / blocked task / a11y blocker)"
MACHINE_ENCODING:    "design token via muse"
REVIEW_CADENCE:      "quarterly"
```

