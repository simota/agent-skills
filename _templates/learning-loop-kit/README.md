# Learning-Loop Kit (base template)

A parameterized base for **repo-local learning loops**: mechanisms that turn a recurring stream of signals (feedback, review comments, incidents, findings…) into durable, versioned **rules** that agents enforce on all future work.

`design-feedback-kit` is **instance #1** of this base. This template generalizes its machinery so any domain with the same loop shape can be instantiated in minutes.

> The loop machinery is generic. Only the **domain knobs** differ — see `kit.config.template.md`.

---

## The loop (identical across all instances)

```
CAPTURE → ANALYZE → REVIEW → PROMOTE → ENFORCE
```

| Step | Generic behavior | Knob that varies it |
|------|------------------|---------------------|
| **CAPTURE** | Append a `{{SIGNAL_NOUN}}` to `{{SIGNAL_LOG}}` (`status: new`). | `SIGNAL_NOUN`, `SIGNAL_PREFIX`, `SIGNAL_SOURCES` |
| **ANALYZE** | Cluster signals into themes; draft a `{{RULE_NOUN}}` when the **promotion threshold** is met. | `ANALYZE_SKILLS`, `PROMOTION_THRESHOLD` |
| **REVIEW** | **Mandatory human gate** — Accept / Edit / Reject. Never auto-approved, even under AUTORUN. | (always human) |
| **PROMOTE** | Merge accepted rule into the right layer with a slug ID; index it; encode machine-checkable parts. | `RULE_PREFIX`, `LAYERS`, `MACHINE_ENCODING`, `PROMOTE_SKILLS` |
| **ENFORCE** | Every future task reads the rules first; PR gate blocks violations; gaps become new signals. | `ENFORCE_SKILLS`, `GATE_SKILLS` |

Shared invariants (do not change per instance): slug-based collision-free IDs, evidence-traceable rules, deprecate-don't-delete (Archive section), `INDEX.md` discoverability, quarterly re-review cadence.

---

## Knobs (the only things that vary)

Filled per instance in a `*.config.md` (template: `kit.config.template.md`). Summary:

| Knob | Meaning | design-feedback value |
|------|---------|------------------------|
| `KIT_NAME` / `KIT_SLUG` | human + dir name | Design Feedback / `design-feedback` |
| `DOMAIN_DIR` | where it installs in a project | `design` |
| `RULE_NOUN(_PLURAL)` | what a rule is called | principle / principles |
| `RULE_PREFIX` | slug prefix for rules | `P` (→ `P-CORE-control-feedback`) |
| `SIGNAL_NOUN(_PLURAL)` | what an input is called | feedback |
| `SIGNAL_PREFIX` | slug prefix for signals | `FB` (→ `FB-20260115-double-save`) |
| `SIGNAL_LOG` | the audit-trail filename | `feedback-log.md` |
| `LAYERS` | rule partitioning (or `core` only for flat) | core, frontend, ios, android |
| `SIGNAL_SOURCES` | allowed `Source:` values | interview, usability-test, review, … |
| `ANALYZE_SKILLS` | extraction specialists | voice, echo, palette |
| `PROMOTE_SKILLS` | curation / encoding | muse, vision, lore |
| `ENFORCE_SKILLS` | who reads rules before acting | vision, artisan, flow, prose, native |
| `GATE_SKILLS` | PR gate | guardian, canon, judge |
| `PROMOTION_THRESHOLD` | when a theme becomes a rule | ≥2 independent OR 1 high-severity |
| `MACHINE_ENCODING` | how quantitative rules are auto-checked | design tokens via muse |
| `ARTIFACT_NOUN` / `ARTIFACT_DIR` | evidence assets | mockup / mockups |

---

## Instantiate a new kit

Rendering is **part scriptable, part human judgment**. Scalar tokens substitute cleanly; list tokens do not (see step 3).

1. **Config** — copy and fill the knobs:
   ```bash
   cp _templates/learning-loop-kit/kit.config.template.md \
      _templates/learning-loop-kit/instances/<kit-slug>.config.md
   ```
2. **Copy the base:**
   ```bash
   cp -R _templates/learning-loop-kit/base _templates/<kit-slug>-kit
   ```
3. **Substitute tokens:**
   - **Scalar tokens** (`KIT_NAME`, `DOMAIN_DIR`, `RULE_NOUN(_PLURAL)`, `RULE_PREFIX`, `SIGNAL_NOUN(_PLURAL)`, `SIGNAL_PREFIX`, `SIGNAL_LOG`, `ARTIFACT_NOUN`, `ARTIFACT_DIR`, `MACHINE_ENCODING`, `PROMOTION_THRESHOLD`, `REVIEW_CADENCE`) — safe to `sed -i 's/{{KIT_NAME}}/.../g'` across the kit.
   - **List tokens** (`LAYERS`, `SIGNAL_SOURCES`, `ANALYZE_SKILLS`, `PROMOTE_SKILLS`, `ENFORCE_SKILLS`, `GATE_SKILLS`) — **substitute by hand.** They render differently per context (prose "one of …", table rows, comma lists), so blind `sed` produces wrong output. Read each occurrence and expand it appropriately.
4. **Structure fixups:**
   - `mv base.../signals-log.md → <SIGNAL_LOG>` (the filename from your config).
   - `mv artifacts/ → <ARTIFACT_DIR>/`, or delete it entirely if `ARTIFACT_NOUN: none`.
   - For **each delta layer** in `LAYERS` beyond `core`, copy `rules/core.md` → `rules/<layer>.md`, change its title/prefix to that layer, and clear the core seed entries. Add a by-layer row in `rules/INDEX.md`.
   - Replace the `core.md` seed skeleton with 1-3 real baseline rules (or delete it to start empty).
5. **Verify (render gate):**
   ```bash
   _templates/learning-loop-kit/_scripts/check-rendered.sh _templates/<kit-slug>-kit
   ```
   Must print `✓ … clean`. It fails on leftover `{{TOKEN}}`, `YYYY-MM-DD`, or `<slug>`/`<LAYER>` markers outside `_templates/`.
6. **Register** in `INSTANCES.md`.
7. **Install** into a project: `cp -R _templates/<kit-slug>-kit <project>/<DOMAIN_DIR>` and paste its `CLAUDE.snippet.md` into the project's `CLAUDE.md`.

> `design-feedback-kit` is a worked example of the *rendered shape* — but it is a **predecessor / non-strict render** (uses `Scope:`/`Token:` where the base uses `Layer:`/`Check:`). See `instances/design-feedback.config.md`.

---

## When this pattern fits (and when it doesn't)

**Fits** when ALL hold: (a) signals arrive over time, not once; (b) they should crystallize into reusable rules; (c) future work can be checked against those rules; (d) a human should approve rules (a signal ≠ a law); (e) you want an audit trail of *why* each rule exists.

**Doesn't fit:** one-off decisions (use an ADR/doc), purely mechanical config (use lint/CI directly), or rules with no enforcement surface (nobody reads them → dead docs). Candidate domains: see `INSTANCES.md`.
