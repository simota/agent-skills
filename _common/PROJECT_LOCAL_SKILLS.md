# Project-Local Skills

> **Tier:** `authoring` — activates when creating or auditing skills, not during user work. Precedence: `_common/OPERATIONAL.md` § Contract Precedence.

This registry separates reusable global skills from operating extensions that only make sense inside the `claude-skills` repository.

## Placement Contract

- Global skills live at `<skill-name>/SKILL.md` and may be enabled through global profiles.
- Project-local skills use `.claude/skills/<skill-name>/` as the canonical copy.
- `.agents/skills/<skill-name>/` is the cross-tool mirror and MUST remain byte-identical to the canonical copy.
- A project-local skill that references `_common/` or `_templates/` MUST carry the corresponding resolving symlink beside `SKILL.md` in both canonical and mirror copies. From the current layout the target is `../../../_common` or `../../../_templates`.
- Global profiles MUST NOT list project-local skills.
- A global skill may name a project-local handoff only after verifying that `.claude/skills/<skill-name>/SKILL.md` or `.agents/skills/<skill-name>/SKILL.md` exists in the active workspace.
- When the local skill is unavailable, use the fallback in this registry instead of silently routing to a missing skill.

## Registry

| Skill | Repository-local responsibility | Unavailable fallback |
|-------|---------------------------------|----------------------|
| `orbit` | `nexus-autoloop` contracts, runner generation, and recovery for this repository's loop stack | `Nexus[goal/apex]` for bounded execution; `Sherpa` for decomposition |
| `lore` | `.agents/*.md` synthesis into this repository's `METAPATTERNS.md` knowledge lifecycle | `Tome` for learning documents; `Scribe` for durable pattern documentation |
| `darwin` | Fitness and lifecycle evaluation persisted to this repository's `.agents/ECOSYSTEM.md` | `Prune` for retention audit; `Architect` for approved ecosystem improvements |

## Availability Gate

Before emitting a handoff to `Orbit`, `Lore`, or `Darwin`:

1. Resolve the active workspace root.
2. Check for the skill in `.claude/skills/` or `.agents/skills/`.
3. Route to the local skill only when one copy exists and, when both exist, they are synchronized.
4. Otherwise use the registered fallback and report `project_local_fallback: true` in the handoff or final summary.

## Verification

Run the repository validator after changing a project-local skill:

```bash
make validate
```

`lint-project-local.py` enforces registry/roster agreement, recursive canonical/mirror identity (including symlink targets), and delivery of referenced shared namespaces. `lint-frontmatter.py` is also run explicitly against the canonical project-local root.

For manual diagnosis, the direct mirror checks remain useful:

```bash
diff -rq .claude/skills/orbit .agents/skills/orbit
diff -rq .claude/skills/lore .agents/skills/lore
diff -rq .claude/skills/darwin .agents/skills/darwin
```
