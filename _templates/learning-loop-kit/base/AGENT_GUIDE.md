# Agent Guide — {{KIT_NAME}} Kit

Two responsibilities: (A) **run the learning loop** when a {{SIGNAL_NOUN}} arrives, and (B) **enforce** accepted {{RULE_NOUN_PLURAL}} on every domain task. Orchestrate via `/nexus` or run steps directly.

## A. Running the loop

### Step 2 — ANALYZE
Spawn {{ANALYZE_SKILLS}} (parallel where independent), then synthesize.
- Read new entries from `{{SIGNAL_LOG}}` together with unresolved `analyzed` entries left below the promotion threshold. Count independent evidence across runs; exclude `promoted` and `rejected` entries from pending promotion candidates.
- **Promotion threshold** — only draft a {{RULE_NOUN}} when: {{PROMOTION_THRESHOLD}}. Below threshold → mark the {{SIGNAL_NOUN}} `analyzed` and leave to accumulate.
- For themes that clear it, write a draft using `_templates/rule-entry.md` (`status: proposed`). Decide layer: universal across `{{LAYERS}}` → `core`; else the matching delta layer (must not duplicate/contradict a core rule).
- Scan `rules/INDEX.md` by tag first — if a matching {{RULE_NOUN}} exists, propose an **edit** instead of a new entry. Mark the source {{SIGNAL_NOUN}} `analyzed` and link the draft.

### Step 3 — REVIEW (human gate — mandatory, never auto-approved)
**Never skipped — not even under `/nexus` AUTORUN / AUTORUN_FULL.** No agent self-promotes a draft to `accepted`. Present each via `AskUserQuestion`: Statement, source {{SIGNAL_NOUN}} IDs, layer → **[Accept] [Edit] [Reject]**.
- Accept → `status: accepted`, go to PROMOTE. Edit → revise, re-present. Reject → mark source `rejected` + reason.
- **Conflict resolution** — if a draft contradicts an accepted {{RULE_NOUN}}: (a) **supersede** (deprecate old → Archive, set `Superseded by:`), (b) **scope-narrow** (restrict one to a layer/context), or (c) **reject**. Never leave two accepted {{RULE_NOUN_PLURAL}} in direct conflict. {{PROMOTE_SKILLS}} may pre-flag conflicts/dupes.

### Step 4 — PROMOTE
- Append the accepted entry to the right `rules/*.md` with a slug ID combining `{{RULE_PREFIX}}`, the uppercase layer, and a mnemonic (example: `{{RULE_PREFIX}}-CORE-validate-input`). Check existing IDs and recheck concurrent additions before merging. Reuse an ID only for an approved edit to the same {{RULE_NOUN}}; give distinct {{RULE_NOUN_PLURAL}} distinct slugs.
- Add its row to `rules/INDEX.md` (by-tag + by-layer).
- Mark source {{SIGNAL_NOUN}} `promoted` and set `Promoted to:` to the accepted {{RULE_NOUN}}'s actual ID.
- If the {{RULE_NOUN}} has a machine-checkable part, encode it via **{{MACHINE_ENCODING}}** and record the reference in the entry's `Check:` field.
- Add a reference {{ARTIFACT_NOUN}} to `{{ARTIFACT_DIR}}/` (Do, + Before/After) when applicable.

## B. Enforcement (every domain task)

**Before** any work in this domain, an agent MUST:
1. Scan `rules/INDEX.md` by relevant tags, then read `rules/core.md` + the matching layer file. Active list only — `## Archive` is ignored.
2. Treat every `accepted` {{RULE_NOUN}} as a hard constraint. Where a `Check:` is set, satisfy/run it.
3. Self-check the output against the relevant slugs (or delegate to a {{GATE_SKILLS}} agent).

**At PR review the {{RULE_NOUN}} gate is mandatory** ({{GATE_SKILLS}}):
- Verify the diff violates no `accepted` {{RULE_NOUN}}. A violation **blocks** until fixed or human-waived.
- Honesty note: `Check:`-backed rules are machine-verifiable; the rest are reviewer judgment — the gate raises them for attention, it doesn't auto-prove compliance.
- A violation revealing a *missing* rule → file a new `{{SIGNAL_LOG}}` entry (`source: review`). The loop closes on itself.

### Skill → loop-step map
| Step | Skills |
|------|--------|
| ANALYZE | {{ANALYZE_SKILLS}} |
| REVIEW | human via `AskUserQuestion` (+ {{PROMOTE_SKILLS}} for conflict flags) |
| PROMOTE | {{PROMOTE_SKILLS}} |
| ENFORCE | {{ENFORCE_SKILLS}} |
| GATE | {{GATE_SKILLS}} |

> Author spawn prompts per `_common/OPUS_5_AUTHORING.md`: front-load the {{RULE_NOUN}} slugs to honor, set a length envelope, state the thinking directive. Run independent ANALYZE branches as parallel background spawns.
