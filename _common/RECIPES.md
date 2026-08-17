# Recipes / Subcommands Protocol

Common protocol for defining Recipes (internal presets) and exposing them as Subcommands (external aliases) within a single skill. All agents may adopt this protocol; see **Adoption Tiers** below.

---

## Concept

A **Recipe** is a named preset within one skill that pre-selects a workflow mode, evidence strategy, and reference set. Externally, each Recipe is surfaced as a **Subcommand** — the token a user or Nexus passes to activate it.

Key properties:
- Scope is **strictly one skill**. Recipes do not cross skill boundaries.
- One skill should define 2-7 Recipes (recommended for dispatch-table scannability). 8-10 is an accepted corpus-norm band (INFO); 11+ triggers a consolidation review (WARNING). Hub skills (e.g. `nexus`) are exempt — recipe breadth is by design. Default is required; others are optional.
- The `default` Recipe preserves full backward compatibility — any invocation without a matching Subcommand token falls through to it.

---

## Naming Rules

| Rule | Detail |
|------|--------|
| Length | 2-20 characters (favor brevity — aim for ≤ 12; extend only for unavoidable compound words, e.g. `growth-acceptance`) |
| Format | kebab-case (lowercase, hyphens only; a leading digit is allowed for established domain terms, e.g. `5whys`, `1on1`) |
| Reserved words | `default`, `auto`, `help`, `list` — forbidden as Recipe names |
| Abstraction | Must be more specific than the skill name, less specific than a single use case |
| Uniqueness | Unique within the skill; duplication across skills is OK |
| Part of speech | Noun preferred (task category); verb acceptable |

**Good examples:** `bug`, `prod`, `regression`, `cascade`, `consensus`, `api`, `ddd`

**Bad examples:** `react-hooks-null-check` (too specific), `investigate` (too abstract for Scout), `default` (reserved)

---

## SKILL.md Structure

### `## Recipes` table

Include this table when the skill defines 3 or more distinct modes.

```markdown
## Recipes

| Recipe | Subcommand | Default? | When to Use | Read First |
|--------|-----------|---------|-------------|------------|
| [Display Name] | `[token]` | ✓ | [activation condition] | `reference/[file].md` |
| [Display Name] | `[token]` | | [activation condition] | `reference/[file].md` |
```

### Externalized registry (size-ceiling escape hatch)

A skill whose Recipes table has grown large enough to push `SKILL.md` toward the Anthropic size ceiling may move **the table** to a sibling registry file and keep only a **dispatch allowlist** in `SKILL.md`. The split is by purpose: `SKILL.md` keeps what is needed to *choose* (the allowlist, plus any family/keyword grouping), the registry holds what is needed to *execute* (When to Use · Chain Template · Read).

Rules:

1. The `## Recipes` section stays in `SKILL.md` — only its table moves. Removing the section entirely trips `R-REC-05`.
2. The section must name the registry as a backticked path matching `reference/*recipes-index.md`; the validators follow that pointer and validate the table wherever it lives.
3. The allowlist must list **every** subcommand, marking the default. A token absent from it is not a subcommand — Subcommand Dispatch reads the allowlist, not the registry.
4. The registry file states its own purpose and read-trigger like any other reference.

Use this only when the size ceiling actually forces it; a table that fits belongs inline, where it is one read away instead of two. Current user: `nexus` (`nexus/reference/recipes-index.md`) — 39 Recipes.

**Column definitions:**
- **Recipe** — human-readable display name (title case, spaces OK)
- **Subcommand** — the exact token users type (kebab-case, backtick-quoted)
- **Default?** — exactly one row must have `✓`
- **When to Use** — brief activation condition (one clause)
- **Read First** — comma-separated list of files to load at Recipe activation

Optional columns (add when useful): `Length Envelope`, `Thinking`, `Model`

### `## Subcommand Dispatch` section

Required whenever `## Recipes` is defined.

```markdown
## Subcommand Dispatch

Parse the first token of user input.
- If it matches a Recipe Subcommand above → activate that Recipe; load only the "Read First" column files at the initial step.
- Otherwise → default Recipe + automatic triage.
```

---

## Subcommand Dispatch Rules

1. **Token matching** — Extract the first whitespace-delimited token from user input. Compare against all Subcommand values using exact string match (case-sensitive).
2. **Match found** → activate that Recipe immediately; load only its "Read First" files.
3. **No match** → activate the `default` Recipe; pass the full input as free-text; apply the skill's normal triage logic.
4. **Exactly one default** — every skill with a `## Recipes` table must declare exactly one `✓` in the Default? column.
5. **Free-text passthrough** — unrecognized first tokens are never silently dropped; the full original input is passed to the default Recipe.

---

## Nexus Integration

### Agent Spawn Template

When Nexus spawns an agent with a Recipe intent, add the following optional line to the spawn prompt (between the SKILL.md instruction and `Task:`):

```
    Recipe: [recipe-name or auto]               # P-REC: subcommand hint / auto-triage
```

- `[recipe-name]` — the exact Subcommand token (e.g., `bug`, `regression`)
- `auto` — let the skill apply triage and select the best Recipe

### `_AGENT_CONTEXT` field

Add `recipe` as an optional field when passing structured context:

```yaml
_AGENT_CONTEXT:
  task_type: "[type]"
  description: "[task]"
  recipe: "[recipe-name or auto]"   # optional; omit if not specified
  constraints: "[constraints]"
```

### routing-matrix.md `Recipe Hints` column

The routing matrix may include a **Recipe Hints** column between `Primary Chain` and `Additions` to pre-select Recipes per task type:

```
| Task Type | Primary Chain | Recipe Hints | Additions |
```

Format: `AgentName[subcommand]`, comma-separated for multi-agent rows.
Use `—` when no Recipe hint applies (skill lacks Recipes, or Phase not yet implemented).

---

## Gauge Validation Hooks

The following rules are evaluated by **Gauge** during normalization audits.

| Rule ID | Condition | Severity |
|---------|-----------|---------|
| R-REC-01 | A skill with `## Recipes` must declare exactly one `Default? = ✓` | ERROR |
| R-REC-02 | All Subcommand values must match `^[a-z0-9][a-z0-9-]{1,19}$` (kebab-case, 2-20 chars; leading digit allowed for domain terms like `5whys`) | ERROR |
| R-REC-03 | Subcommand values must not be reserved words: `default`, `auto`, `help`, `list` | ERROR |
| R-REC-04 | Recipe count, tiered (calibrated 2026-07-03 against the 132-skill corpus, where 54% exceeded the old flat max-7): ≤7 recommended; 8-10 = INFO (corpus norm band, ≤10 = P95); 11+ = WARNING (consolidation review candidate); hub skills (`HUB_SKILLS` in validator, currently `nexus`) always INFO — recipe breadth by design | INFO / WARNING (tiered) |
| R-REC-05 | Presence of `## Recipes` section is RECOMMENDED for skills in Adoption Tiers 1-2, but not required | INFO |

---

## Anti-Patterns

| Anti-Pattern | Why It's Wrong | Correct Approach |
|-------------|----------------|-----------------|
| Defining 2 or fewer Recipes | Output Routing alone is sufficient for binary decisions | Use `## Output Routing` instead |
| Naming a Recipe more abstract than the skill | e.g., `search` in Scout — less specific than "scout" itself | Name must be narrower than the skill's own scope |
| Over-specific Recipe names | `react-hooks-null-check-bug` — too narrow to be reusable | Use `bug` or `regression` |
| Requiring user to specify Recipe when auto-triage suffices | Adds friction without benefit | Reserve explicit Recipes for cases with distinct evidence strategies |
| Using a Recipe to select output format only | Format variation is Output Routing's job, not Recipes' | Use Output Routing signals instead |
| Defining Recipes that cross skill boundaries | A Recipe in Scout cannot route to Builder's Recipe | Recipes are intra-skill; cross-skill routing stays in Nexus |

---

## Adoption Tiers

| Tier | Target Skills | Recommendation |
|------|--------------|----------------|
| **Tier 1 — Recommended** | Skills that appear in the Nexus routing-matrix Primary Chain (e.g., Scout, Builder, Sentinel) | Adopt Recipes; add Recipe Hints to routing-matrix |
| **Tier 2 — Optional** | Skills invoked frequently in standalone usage (e.g., Lens, Zen, Radar) | Adopt if 3+ distinct modes exist |
| **Tier 3 — Defer** | Specialist skills invoked rarely or always through Nexus chains (e.g., Canvas, Morph, Quill) | Omit `## Recipes`; revisit in Phase 2+ |

Phase 1 scope: Scout only. Builder, Sentinel, and other Tier 1 skills adopt Recipes in Phase 2+. As of Phase 2J, all 123 skills have adopted Recipes.

---

## Automation Scripts

| Script | Purpose |
|--------|---------|
| `_common/scripts/validate-recipes.py` | Validate every SKILL.md against R-REC-01〜05 + heading integrity (H-REC-01/02). Default severity (`warning`) always exits 0 — pass `--severity error` to fail on ERROR findings. Run before commit and in CI. |
| `_common/scripts/generate-recipes-directory.py` | Regenerate `compass/reference/recipes-directory.md` from all SKILL.md `## Recipes` tables. Idempotent; run after any Recipe change. |

Usage:

```bash
python3 _common/scripts/validate-recipes.py                          # bare invocation — severity=warning, always exits 0
python3 _common/scripts/validate-recipes.py --severity error          # exit 1 on ERROR findings
python3 _common/scripts/validate-recipes.py --severity error --changed-only  # ERROR-gate, git-diff scope only (CI PR check)
VERBOSE=1 python3 _common/scripts/validate-recipes.py                 # also show INFO for skills without Recipes
python3 _common/scripts/generate-recipes-directory.py                 # refresh compass directory
```
