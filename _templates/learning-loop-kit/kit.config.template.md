# Kit Config — <KIT_NAME>

Fill every knob, then render `base/` into `<kit-slug>-kit` by substituting each `{{TOKEN}}`. One config = one instance. Keep this file with the rendered kit so the instance is reproducible.

```yaml
# --- identity ---
KIT_NAME:            "<Human Name, e.g. Review Knowledge>"
KIT_SLUG:            "<kebab, e.g. review-knowledge>"
DOMAIN_DIR:          "<install dir in target repo, e.g. review>"

# --- vocabulary ---
RULE_NOUN:           "<singular, e.g. convention>"
RULE_NOUN_PLURAL:    "<plural, e.g. conventions>"
RULE_PREFIX:         "<short, e.g. C>"          # rule slug: <RULE_PREFIX>-<LAYER>-<slug>
SIGNAL_NOUN:         "<singular, e.g. review comment>"
SIGNAL_NOUN_PLURAL:  "<plural, e.g. review comments>"
SIGNAL_PREFIX:       "<short, e.g. RC>"         # signal id: <SIGNAL_PREFIX>-YYYYMMDD-<slug>
SIGNAL_LOG:          "<filename, e.g. comments-log.md>"
ARTIFACT_NOUN:       "<evidence noun, e.g. example | snippet | repro | none>"
ARTIFACT_DIR:        "<dir, e.g. examples | none>"

# --- structure ---
LAYERS:              ["core"]                    # flat. OR e.g. ["core","frontend","ios","android"]
                                                 # core = universal; others = deltas that must not contradict core

# --- enums ---
SIGNAL_SOURCES:      ["<source-a>", "<source-b>", "..."]   # allowed Source: values for a signal

# --- skill wiring (loop steps → specialists) ---
ANALYZE_SKILLS:      ["<skill>", "..."]          # cluster signals, draft rules
PROMOTE_SKILLS:      ["<skill>", "..."]          # curate, dedup, encode
ENFORCE_SKILLS:      ["<skill>", "..."]          # read rules before acting
GATE_SKILLS:         ["<skill>", "..."]          # PR gate

# --- policy ---
PROMOTION_THRESHOLD: "<when a theme becomes a rule, e.g. '>=2 independent items OR 1 high-severity'>"
MACHINE_ENCODING:    "<how quantitative rules auto-check, e.g. 'lint rule (Semgrep)' | 'design token' | 'alert rule' | 'none'>"
REVIEW_CADENCE:      "quarterly"                 # re-validate rules whose Last reviewed > 90d
```

## Notes per knob
- **RULE_PREFIX / SIGNAL_PREFIX** must be unique within the kit and short. Slugs (not numbers) keep IDs collision-free under concurrent appends.
- **LAYERS** — choose `["core"]` (flat) unless the domain genuinely has a universal layer + context-specific deltas. Common axes: platform, service, language, audience.
- **MACHINE_ENCODING** decides how much of ENFORCE is mechanical vs reviewer-judgment. If `none`, the PR gate is human-judgment only — state that honestly in the rendered `AGENT_GUIDE.md`.
- **ARTIFACT_NOUN: none** drops the artifacts directory entirely (some domains have no visual/asset evidence).
