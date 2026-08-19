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

## Admission: is the line worth its rent?

The decision rule above answers *where*. This answers *whether*. Anything placed at an always-on
level is re-read in every future session, so it pays rent forever while competing with files, tool
output, and the conversation itself. Size limits alone do not settle this — a 12-line file of
low-signal advice is worse than a 40-line file of facts the model cannot infer.

Weigh benefit against the recurring cost, not against zero:

| Ask | Yes → | No → |
|-----|-------|------|
| Needed in most sessions? | always-on candidate | scoped rule or on-demand skill |
| Hard for the model to infer from code, manifests, tests, and docs? | worth keeping | delete — it is restating what is already readable |
| Convertible into an action? | rule candidate | rewrite until it is, or drop it |
| Concretely verifiable? | it can carry a completion condition | keep as guidance only, and say so |
| Stable over time? | safe at the root | note the version, or move it to a source that gets updated |
| Is a violation unacceptable? | **hook / permission** — soft text fails under pressure | an instruction is fine |

A line that cannot be defended on **error reduction × scope relevance × durability ×
verifiability**, divided by what it costs every session, does not belong at an always-on level.
Optimize placement, not length: the goal is that detail arrives at the moment it is needed.

**Four ways always-on content goes bad.** These are what audits actually find:

- **Inferable facts** — a script list already in `package.json`, a copied directory tree, class
  names restated from source. Adds no information, only a surface that goes stale. (`gauge` CQ1
  measures the general-knowledge form of this; the repository-self-restating form is the same
  defect against a different baseline.)
- **Duplicated source of truth** — the same procedure in README, `AGENTS.md`, and `CLAUDE.md`.
  They drift on the next independent edit, and then nothing tells the agent which one to believe.
  (`_common/scripts/lint-instructions.py` I3 catches the exact-match case in CI.)
- **Temporary work left permanent** — a one-off migration step, a workaround for a closed issue, a
  short-lived branch TODO. It keeps being read at full strength long after its premise expired.
  Give anything time-bound an owner and a removal condition when you add it, not later.
- **Exceptions promoted to absolutes** — one package's rule placed at the root; "always run every
  test", "never add a dependency". Stated unconditionally, they misfire on docs-only edits and
  throwaway experiments. Attach the condition, or scope the file.

## Budget review: report the always-on delta

A change to an instruction file is a change to every future session's prefix. When proposing one,
state the net effect on always-on content, not just what was added:

```
Added:            + 3 lines   public API change trigger
Removed:          - 42 lines  duplicated setup tutorial
Moved:            → 68 lines  to docs/agent/api-migration.md (on-demand)
Always-on delta:  - 39 lines
```

Line count is not a quality measure, and a positive delta is often correct. The point is that the
recurring cost becomes visible and gets weighed, instead of only the benefit being argued. Two
rules keep the figure meaningful:

- **Count the resolved total.** `@path` imports load with their host, so moving lines behind an
  import is a delta of zero. Only a move to a `paths:`-scoped rule, a skill body, a doc, or a hook
  actually reduces the always-on figure.
- **Measure bytes, not files.** Splitting one file into six changes the file count and nothing
  about what gets loaded.

## Anti-patterns

- **Unowned CLAUDE.md bloat:** every team appends, nothing is deleted; cost compounds at scale. Keep it **< 200 lines**, give it an owner, review like code.
- **Split theater:** reorganizing an oversized file into `@path` imports and calling the size finding fixed. The imports resolve at load time — organization improved, recurring cost unchanged.
- **Unscoped rules** = silent CLAUDE.md-equivalent token waste during unrelated work.
- **Custom output style** *replaces* defaults (scoping changes, comment policy, security handling, test-running) unless `keep-coding-instructions: true`.
- **Prompt-constraint overreliance:** any constraint that must hold even under injection belongs in a hook, never an instruction.

## Cross-skill ownership in this repo

- **latch** — owns instruction→hook triage and all hook authoring (the "every time / never" rows above).
- **hone** — runs the anti-bloat audit ("would Claude do this wrong without it?") and routes failing lines here.
- **sigil** — decides skill vs rule vs CLAUDE.md when authoring project skills (`cross-tool-rules-landscape.md`).
- **architect** — decides whether a new capability is a skill vs hook/rule/subagent at design time.
- **Grove `llm`** — `.claude/rules/` tiering in monorepos.
