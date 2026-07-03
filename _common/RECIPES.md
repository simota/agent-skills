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

Phase 1 scope: Scout only. Builder, Sentinel, and other Tier 1 skills adopt Recipes in Phase 2+. As of Phase 2J, 126 of 130 skills have adopted Recipes.

---

## Automation Scripts

| Script | Purpose |
|--------|---------|
| `_common/scripts/validate-recipes.py` | Validate every SKILL.md against R-REC-01〜05 + heading integrity (H-REC-01/02). Exit non-zero on ERROR. Run before commit and in CI. |
| `_common/scripts/generate-recipes-directory.py` | Regenerate `compass/reference/recipes-directory.md` from all SKILL.md `## Recipes` tables. Idempotent; run after any Recipe change. |

Usage:

```bash
python3 _common/scripts/validate-recipes.py          # exit 1 on errors
VERBOSE=1 python3 _common/scripts/validate-recipes.py  # also show INFO for skills without Recipes
python3 _common/scripts/generate-recipes-directory.py  # refresh compass directory
```
