# Sharding Strategy

Reference for Nest's `sharding` recipe. Split large CLAUDE.md / reference docs via `@import` while preserving prompt cache prefixes and avoiding circular references.

> Complements Hone (density audit). Hone identifies *what* to extract; Nest decides *where to put it* and *in what order*.

---

## 1. When to Shard

Trigger thresholds:

| Signal | Threshold | Action |
|---|---|---|
| CLAUDE.md line count | > 300 lines | Plan split |
| CLAUDE.md token count | > 1,200 tokens | Plan split |
| Reference file lines | > 500 lines | Split by sub-domain |
| Single section | > 100 lines | Extract to dedicated file |
| Cache hit rate | < 60% across recent sessions | Re-order for stability |
| Same content appears in 2+ files | duplicate | Extract to shared, `@import` from both |

Don't shard prematurely. Below thresholds, monolithic is faster (fewer file reads, simpler grep).

---

## 2. Split Axis Selection

Choose **one** primary axis per shard layer. Mixing axes within a layer creates inconsistency.

### Axis A: by domain (most common)
```
.claude/rules/
├── coding-standards.md
├── testing-policy.md
├── security-rules.md
├── git-conventions.md
└── deployment.md
```
Use when: rules cluster around well-defined topics.

### Axis B: by lifecycle phase
```
.claude/rules/
├── design.md       # Pre-implementation rules
├── implement.md    # During-coding rules
├── review.md       # Pre-merge rules
└── deploy.md       # Post-merge / release rules
```
Use when: rules apply at distinct workflow stages.

### Axis C: by change frequency (cache-optimal)
```
.claude/rules/
├── stable.md       # < 1 change / month (cache-friendly)
├── monthly.md      # 1-4 changes / month
└── volatile.md     # weekly+ changes (cache-unfriendly)
```
Use when: prompt cache hit rate is the dominant constraint.

### Axis D: by audience
```
.claude/rules/
├── all-agents.md
├── code-agents.md   # builder, artisan, scout
├── review-agents.md # judge, zen
└── ops-agents.md    # gear, beacon
```
Use when: many agents share project but read different rule subsets.

---

## 3. Cache-Preserving Order

Prompt cache invalidates from the **first changed byte** forward. Order matters.

### Stable-first principle
```markdown
# CLAUDE.md

@.claude/rules/stable.md      ← rarely changes (cached for weeks)
@.claude/rules/monthly.md     ← occasionally changes
@.claude/rules/volatile.md    ← changes weekly (invalidates only itself + below)

## Project-specific (most volatile, last)
- Current sprint focus: ...
- Active branch: ...
```

### Within a single file
```markdown
# Stable preamble (license, identity)
# Boundaries (rare changes)
# Core rules (rare changes)
# Workflow (occasional changes)
# Recipes (occasional changes)
# Operational notes (frequent changes — bottom)
```

If a frequently-changed line appears in line 10, every line below 10 invalidates with each edit. Push volatile content to the bottom.

---

## 4. Include Manifest

Document the include graph in `.claude/rules/INDEX.md`:

```markdown
# CLAUDE.md Include Manifest

## Cascade (root → leaf)
- `CLAUDE.md` (project root)
  - @.claude/rules/stable.md       (stability: high; lines: 80)
  - @.claude/rules/coding.md       (stability: medium; lines: 120)
  - @.claude/rules/security.md     (stability: high; lines: 60)
  - @.claude/rules/volatile.md     (stability: low; lines: 40)

## Total tokens: ~1,200 (within budget)

## Override hierarchy
- `packages/api/CLAUDE.md` overrides `coding.md` § 3 (Python-specific)
- `packages/web/CLAUDE.md` overrides `coding.md` § 3 (TypeScript-specific)

## Cycle check: ✓ no circular @import detected (run via scripts/check-cycles.sh)
```

Maintain alongside the actual rules. Stale INDEX.md is worse than no INDEX.md.

---

## 5. Cycle Prevention

`@import` graphs must be a DAG (Directed Acyclic Graph).

### Allowed
```
A.md → B.md → C.md
A.md → C.md (diamond OK)
```

### Forbidden
```
A.md → B.md → A.md  (cycle)
A.md → B.md → C.md → A.md  (cycle)
```

### Detection script (bash, conceptual)
```bash
#!/bin/bash
# scripts/check-cycles.sh
declare -A graph
for f in $(find .claude -name '*.md'); do
  for ref in $(grep -oE '@\S+\.md' "$f" | tr -d '@'); do
    graph["$f"]+="$ref "
  done
done
# DFS cycle detection
# (full implementation: prefer madge or a Python/Node script)
```

Run on pre-commit if rule-file edits happen frequently.

---

## 6. Sharding Strategy Decision Matrix

| Project state | Recommended axis | Rationale |
|---|---|---|
| Greenfield | Axis A (domain) | Most readable, easiest to grow |
| Mature, large team | Axis A + Axis D (domain × audience) | Reduces irrelevant context per agent |
| Cache-cost dominated | Axis C (change frequency) | Maximize cache hit rate |
| Workflow-heavy (CI/CD pipeline) | Axis B (lifecycle phase) | Aligns with stage gates |
| Polyglot monorepo | Axis A at root, language-specific in packages | See `monorepo-topology.md` |

---

## 7. Verification After Sharding

| Check | Method |
|---|---|
| Total token count under budget | `wc -w` × 1.3 estimate; aim < 1,200 for root CLAUDE.md |
| No content lost | Diff merged content vs. original CLAUDE.md |
| Imports resolve | Grep for `@.claude/rules/` and verify each file exists |
| No cycles | Run cycle detection script |
| Cache prefix stable | Check that lines 1-50 of root CLAUDE.md haven't moved |
| LLM agent finds rules | Discovery test (see `audit-checklist.md`) |
| Override chain works | Test with package-level CLAUDE.md present |

---

## 8. Common Pitfalls

| Pitfall | Avoidance |
|---|---|
| Shard by author / team → political fragmentation | Shard by content axis, not org chart |
| Volatile content at top → cache invalidates daily | Stable-first ordering |
| Circular `@import` chain → infinite loop or silent truncation | Cycle detection on pre-commit |
| Shard count > 10 at one level → discovery overhead | Cap shards at 5-7 per directory |
| Inconsistent axis at same level → confusing | One axis per layer |
| INDEX.md not maintained → drift | Hand off to Lore for periodic audit |
| Each shard independently fine, sum > budget | Measure total post-shard, not per-file |
| Ignore `@import` resolution depth | Cap depth at 3 levels (root → package → module) |

---

## 9. Decision Walkthrough Template

```
Source file to shard: ____________
Current size: ____ lines / ~____ tokens
Trigger reason: □ size threshold  □ duplication  □ cache rot  □ audience mismatch

Split axis: □ A (domain)  □ B (lifecycle)  □ C (frequency)  □ D (audience)
Rationale: ____________

Planned shards (3-7 max):
  1. ____________  (~____ lines, stability: high/med/low)
  2. ____________  (~____ lines, stability: high/med/low)
  3. ____________  (~____ lines, stability: high/med/low)
  ...

Order in root CLAUDE.md (stable → volatile):
  1. @____
  2. @____
  3. @____

Override layers needed:
  □ Package-level overrides
  □ Module-level overrides
  □ None (single layer)

Cycle check: ✓ / pending

INDEX.md maintained: ✓ / ✗

Verification:
  □ Total tokens under budget
  □ Diff vs original = no content loss
  □ All @import paths resolve
  □ Cache prefix stable
  □ Discovery test passes
```

---

## 10. References
- Anthropic prompt cache documentation
- Claude Code `@import` syntax
- madge (cycle detection for JS/TS, adaptable concept)
- Hone skill (density audit complement)
