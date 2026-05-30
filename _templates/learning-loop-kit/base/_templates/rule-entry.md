# {{RULE_NOUN}} Entry Template

Copy this block into the right layer file during the PROMOTE step.

## ID scheme (collision-free + discoverable)
Use a **kebab-case slug**, not a running number: `{{RULE_PREFIX}}-<LAYER>-<slug>`.
- e.g. `{{RULE_PREFIX}}-CORE-<slug>`.
- Slugs never collide on concurrent appends (no shared counter) and read as their own index.
- If a slug is already taken, the {{RULE_NOUN}} already exists — update it instead of duplicating.

```markdown
### {{RULE_PREFIX}}-<LAYER>-<slug> — <one-line imperative title>
- **Statement:** <single testable rule — what must be true>
- **Rationale:** <why this matters; the cost of violating it> [Source: <signal IDs or standard>]
- **Layer:** <one of {{LAYERS}}>
- **Tags:** <1-3 topic tags, for INDEX.md>
- **Source {{SIGNAL_NOUN}}:** <{{SIGNAL_PREFIX}}-YYYYMMDD-slug[, ...]> | baseline
- **Do:** <concrete positive example>
- **Don't:** <concrete anti-example>
- **Check:** <{{MACHINE_ENCODING}} reference if machine-checkable, else —>
- **Status:** proposed | accepted | deprecated
- **Added:** YYYY-MM-DD · **Last reviewed:** YYYY-MM-DD
<!-- if deprecated: move under the file's `## Archive (deprecated)` section and add: -->
- **Superseded by:** {{RULE_PREFIX}}-<LAYER>-<slug>
```

## Rules
- **Statement must be testable.** A reviewer (human or a {{GATE_SKILLS}} agent) can decide pass/fail.
- **Layering:** put it in `core` only if true across all of {{LAYERS}}; otherwise it is a delta and must not contradict an accepted `core` {{RULE_NOUN}}.
- **No {{RULE_NOUN}} without evidence:** `Source {{SIGNAL_NOUN}}` is required (`baseline` only for seeded defaults).
- **Tags are mandatory** — they drive `INDEX.md` discoverability past a handful of {{RULE_NOUN_PLURAL}}.
- **Deprecate, don't delete:** move superseded entries to `## Archive (deprecated)` so the active list (what ENFORCE reads) stays lean.
