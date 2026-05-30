# {{KIT_NAME}} Kit

A per-project mechanism that turns **{{SIGNAL_NOUN_PLURAL}}** into durable **{{RULE_NOUN_PLURAL}}**, then enforces them on all future work in this domain.

- **Source of truth:** Markdown + assets, version-controlled in the repo (installed as `{{DOMAIN_DIR}}/`).
- **Learning mode:** semi-automated — agents *propose* {{RULE_NOUN_PLURAL}}; a human *approves* before they bind.
- **Structure:** layers = `{{LAYERS}}` (core = universal; others = deltas).

> The {{RULE_NOUN}} files are the contract. {{ARTIFACT_NOUN}}s are evidence. `{{SIGNAL_LOG}}` is the audit trail of *why* each {{RULE_NOUN}} exists.

Generated from `_templates/learning-loop-kit` (base). Config: `<kit-slug>.config.md`.

---

## The Loop

```
CAPTURE → ANALYZE → REVIEW → PROMOTE → ENFORCE
```

| Step | What happens | Owner | Skill(s) |
|------|--------------|-------|----------|
| **1. CAPTURE** | A {{SIGNAL_NOUN}} is appended to `{{SIGNAL_LOG}}` (`status: new`). | anyone | manual / bulk import |
| **2. ANALYZE** | Cluster into themes; draft a {{RULE_NOUN}} only when the threshold ({{PROMOTION_THRESHOLD}}) is met. | agent | {{ANALYZE_SKILLS}} |
| **3. REVIEW** | Human: **Accept / Edit / Reject**. Resolves conflicts. **Mandatory — never auto-approved, even under AUTORUN.** | **human** | `AskUserQuestion` |
| **4. PROMOTE** | Merge accepted {{RULE_NOUN}} into the right layer (slug ID), index it, encode machine-checkable parts ({{MACHINE_ENCODING}}). | agent | {{PROMOTE_SKILLS}} |
| **5. ENFORCE** | Every future task scans `INDEX.md` + reads rules first. **Mandatory PR gate** blocks violations; gaps become new {{SIGNAL_NOUN_PLURAL}}. | agent | {{ENFORCE_SKILLS}} / gate: {{GATE_SKILLS}} |

---

## Directory Layout (installed as `{{DOMAIN_DIR}}/`)

```
{{DOMAIN_DIR}}/
├── README.md                 # this mechanism
├── AGENT_GUIDE.md            # per-step agent procedure + enforcement
├── CLAUDE.snippet.md         # paste into the project's CLAUDE.md
├── {{SIGNAL_LOG}}            # append-only audit trail
├── rules/
│   ├── INDEX.md              # by-tag / by-layer index — scan before working
│   ├── core.md               # universal {{RULE_NOUN_PLURAL}}
│   └── <layer>.md            # one per delta layer in {{LAYERS}}
├── {{ARTIFACT_DIR}}/         # ID-linked evidence (omit if none)
└── _templates/
    ├── rule-entry.md
    └── signal-entry.md
```

---

## Install into a project

1. `cp -R <this kit> <project>/{{DOMAIN_DIR}}`
2. Paste `{{DOMAIN_DIR}}/CLAUDE.snippet.md` into the project's `CLAUDE.md` / `AGENTS.md`.
3. Seed `rules/core.md` with existing conventions, or let the loop populate it.
4. Run the loop whenever a {{SIGNAL_NOUN}} arrives — see `AGENT_GUIDE.md`.

## Kit invariants

- **One {{RULE_NOUN}} = one entry** with a slug ID, testable statement, rationale, tags, source, Do/Don't.
- **Slug IDs** (`{{RULE_PREFIX}}-CORE-<slug>`, `{{SIGNAL_PREFIX}}-YYYYMMDD-<slug>`) — no shared counter, no collisions.
- **Core holds only universals;** context-specific rules are deltas. No two accepted {{RULE_NOUN_PLURAL}} may directly conflict.
- **Human approval mandatory** in every mode; respect the promotion threshold.
- **Every {{RULE_NOUN}} traces to evidence** (a `{{SIGNAL_LOG}}` ID; `baseline` only for seeds).
- **Deprecate, don't delete** — Archive section keeps the active (ENFORCE) list lean.
- **{{REVIEW_CADENCE}} re-review** of {{RULE_NOUN_PLURAL}} with `Last reviewed` > 90 days; archive prior-year signals in the same pass.
