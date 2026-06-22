# Steering-Mechanism Selection — Repository Standard

**Purpose:** Canonical decision guide for placing an instruction at the right Claude Code architectural level — CLAUDE.md, rules, skills, subagents, hooks, output styles, or `append-system-prompt`. Fills the cross-skill gap where mechanism choice was previously fragmented (latch ↔ hone ↔ sigil) and "rule vs hook" was undocumented.

**Read when:** A user asks to "always/never do X", to enforce a convention, to add a runbook/checklist, or when `hone` runs the anti-bloat audit, `latch` triages instruction-vs-hook, `sigil` authors project rules, or `architect` decides skill-vs-other.

**Source:** [claude.com — Steering Claude Code: skills, hooks, rules, subagents, and more](https://claude.com/blog/steering-claude-code-skills-hooks-rules-subagents-and-more). Pairs with `PROMPT_CACHE_HIERARCHY.md` (cost dimension) and `hone/reference/key-thresholds.md` (anti-bloat thresholds).

---

## The seven mechanisms

| Mechanism | Loads | Compaction | Context cost | Authority | Best for |
|-----------|-------|-----------|--------------|-----------|----------|
| **CLAUDE.md (root)** | session start, persists | memoized, re-read after compaction | **High** | soft | build cmds, conventions, structure |
| **CLAUDE.md (subdir)** | when that dir is touched | lost until touched again | Low | soft | dir-specific conventions; monorepo per-team (`claudeMdExcludes`) |
| **Rules** `.claude/rules/` | unscoped=start / scoped=on match | re-injected | Medium (Low if scoped) | soft | file-specific constraints, cross-cutting concerns |
| **Skills** `.claude/skills/` | name+desc at start; body on invoke | re-injected, **shared budget, oldest dropped first** | **Low** | soft | procedural workflows, runbooks, checklists |
| **Subagents** `.claude/agents/` | name+desc+tools at start; **body never enters parent** | only final message returns | **Zero until called** | soft | isolated side tasks; **nests ≤ 5 deep** |
| **Hooks** | lifecycle events | **bypasses compaction entirely** | Low | **HARD (deterministic)** | every-time automation, hard blocks |
| **Output styles** `.claude/output-styles/` | every session start | **never compacted** | High | **strongest file-based** | role / instruction-set changes |
| **append-system-prompt** (CLI flag) | invocation, single run, additive only | cached after first request | Moderate | soft, **decays as you add more** | one-off tone / formatting / length |

## The decision rule (the blog's core)

An **instruction is soft**: Claude follows it *most* of the time, but breaks under pressure — long sessions, ambiguity, or **prompt injection** in a file it reads. So:

| If you wrote in CLAUDE.md… | Move it to… | Why |
|----------------------------|-------------|-----|
| "Every time X, always do Y" | **hook** | model *choosing* to run a formatter ≠ formatter *running automatically* |
| "Never do X" (hard constraint) | **hook** (`PreToolUse` deny / `exit 2`) | a soft instruction fails exactly when it matters most |
| a 30-line procedure / runbook / checklist | **skill** | CLAUDE.md is for facts held *all the time*; procedures load on demand |
| an API/path-specific rule, unscoped | **rule + `paths:` frontmatter** | an unscoped rule is *mechanically identical* to CLAUDE.md — always loaded, always billed |
| a personal preference, project-level | **user/local** CLAUDE.md | keep project files team-wide, not personal |
| a large side task cluttering the thread | **subagent** | isolates intermediate results; only the final message returns |

**Inverse caution (subagent):** the body and intermediate reasoning never return to the parent, so the main thread can't steer or see them. Use a **skill** when you need the procedure to play out *in* the main thread step-by-step.

## Anti-patterns

- **Unowned CLAUDE.md bloat:** every team appends, nothing is deleted; cost compounds at scale. Keep it **< 200 lines**, give it an owner, review like code.
- **Unscoped rules** = silent CLAUDE.md-equivalent token waste during unrelated work.
- **Custom output style** *replaces* defaults (scoping changes, comment policy, security handling, test-running) unless `keep-coding-instructions: true`.
- **Prompt-constraint overreliance:** any constraint that must hold even under injection belongs in a hook, never an instruction.

## Cross-skill ownership in this repo

- **latch** — owns instruction→hook triage and all hook authoring (the "every time / never" rows above).
- **hone** — runs the anti-bloat audit ("would Claude do this wrong without it?") and routes failing lines here.
- **sigil** — decides skill vs rule vs CLAUDE.md when authoring project skills (`cross-tool-rules-landscape.md`).
- **architect** — decides whether a new capability is a skill vs hook/rule/subagent at design time.
- **nest** — `.claude/rules/` tiering in monorepos.
