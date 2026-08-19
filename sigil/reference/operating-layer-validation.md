# Blueprint Validation Checklist

**Purpose:** The 14-item gate every operating-layer blueprint must pass before delivery; also the rubric for `audit` mode.
**Read when:** You are in `VERIFY`, or auditing an existing layer.

## Contents
- Pass criteria
- The 14 items
- Audit-mode usage
- Failure handling

---

## Pass criteria

- All `REQUIRED` items must pass. Delivery is blocked otherwise.
- `RECOMMENDED` items pass at `≥ 80%`.
- Document any item deliberately skipped, with reason.

---

## The 14 items

### Coverage (REQUIRED)

- [ ] **L1** Every recurring task from SURVEY has a mechanism decision in the coverage matrix (skill / recipe / workflow / hook / scoped rule / none). No task left unmapped.
- [ ] **L2** Each chosen mechanism is the cheapest that solves the task (no skill where a hook/rule suffices; no workflow where a recipe suffices). Cross-checked against `_common/MECHANISM_SELECTION.md` (hook/rule/subagent/skill) and `recipe-design.md` / `workflow-design.md` (recipe/workflow — Sigil[blueprint]-local mechanisms).
- [ ] **L3** Grounded in real signals — every proposed component traces to an observed task, pain point, or convention in SURVEY, not a generic stack template.

### Overlap (REQUIRED)

- [ ] **L4** Intra-suite overlap `< 30%` — no two project skills/recipes claim the same primary responsibility.
- [ ] **L5** Ecosystem overlap handled — tasks owned by a global agent (`≥ 30%`) are deferred via the routing map, not duplicated as project skills. `30-49%` cases were confirmed with the user.
- [ ] **L6** Routing map is singly-owned — every task domain has exactly one owner; conflicts resolved.

### Topology & sizing (REQUIRED)

- [ ] **L7** Every designed workflow declares a formal topology (hub-spoke / pipeline / hierarchy). No Bag of Agents.
- [ ] **L8** Every workflow is `≤ 5` phases with verification checkpoints at phase boundaries.
- [ ] **L9** Agent-count and hub-spoke limits respected (`≤ 4` flat / hierarchy beyond; `≤ 7` spokes per hub). Multi-agent use justified (single-agent `< 45%`) or single-skill chosen instead.

### Delegation (REQUIRED)

- [ ] **L10** Every blueprint component names exactly one owning agent (Sigil / Nexus / Orbit / Hone / Grove) with the payload it receives.
- [ ] **L11** No authored skill bodies, executed chains, or installed files are present in Sigil[blueprint]'s output — design and handoffs only.
- [ ] **L12** Loops deferred to Orbit, state machines to Weave, runtime routing to Nexus — none built inline.

### Authoring quality pass-through (RECOMMENDED)

- [ ] **L13** Each skill spec to Sigil requires a third-person, gerund-form name and a `description` with negative triggers.
- [ ] **L14** Each recipe/workflow defines non-overlapping signal keywords / subcommands so Nexus routing is unambiguous.

---

## Audit-mode usage

In `audit` mode, run the same 14 items against an **existing** project layer (no generation). Report each failure with evidence and a remediation proposed as a delegation spec — do not apply changes. Typical audit findings:

| Finding | Item | Remediation owner |
|---------|------|-------------------|
| Two project skills overlap | L4 | Sigil (merge / narrow) |
| Workflow has 8 phases | L8 | Sigil[blueprint] redesign → Nexus re-register |
| Task domain double-owned | L6 | routing-map fix → Nexus |
| Drift: skill no longer matches stack | L3 | Sigil (Skill Evolution) |
| Enforcement done as a skill, not a hook | L2 | Hone (convert to hook) |

---

## Failure handling

- Any REQUIRED item fails → blueprint is `BLOCKED`; fix and re-verify before delivery.
- `RECOMMENDED` below 80% → fix or document the exception in `_STEP_COMPLETE.Output.validation`.
- Repeated failure of the same item across two passes → stop iterating and surface the structural cause (usually a missed SURVEY signal or a mechanism mis-pick) rather than retrying.
