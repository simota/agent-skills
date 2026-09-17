# Skill Design Decisions

Use the repository template `_templates/SKILL_TEMPLATE.md`; do not maintain another scaffold. `SKILL.md` frontmatter has only `name` and `description`. Describe actual environment/tool dependencies in the body, bound through `_common/CLI_COMPATIBILITY.md`, not an invented `compatibility` key.

## Complexity Ladder

Choose the lowest level that can satisfy the acceptance criteria. Escalation requires a demonstrated missing capability, not a preference for more agents.

| Level | Mechanism | Escalate only when |
|-------|-----------|--------------------|
| L0 | Prompt + retrieval | The task needs an external action |
| L1 | Prompt + tools | A single tool-using session cannot enforce the required stages or routing |
| L2 | Fixed chaining / routing | Work cannot be fully decomposed before execution |
| L3 | Dynamic workers / evaluator loop | Independent specialists and autonomous coordination are required |
| L4 | Autonomous multi-agent system | No higher default; justify topology, ownership, joins and stop conditions |

Mechanism choice (skill/rule/hook/subagent) belongs to `_common/MECHANISM_SELECTION.md`. Parallel dispatch, ownership and joins belong to `_common/SUBAGENT.md` and `_common/PARALLEL.md`. Route specialists through Nexus; a peer-to-peer diagram does not authorize bypassing the hub.

## Process Constraint Tiers — Fixing Route vs Fixing Outcome

| Tier | Use when | Write |
|------|----------|-------|
| Required Process | Order is necessary for safety, correctness or auditability; name the concrete failure if reordered | MUST steps and the gate each enforces |
| Suggested Scaffold | Decomposition helps a difficult task, but another route can meet the same contract | A conditional scaffold; allow deviation with a reason |
| Internal Method | Multiple approaches satisfy a checkable result | Outcome, evidence and constraints; delegate the method |

Do not prescribe an internal thought sequence as an audit trail. Require observable evidence, assumptions, considered alternatives, reversal conditions and checks. Avoid copying phase-by-phase instructions when these do not change an action.

## Specification Gate

A proposed skill must have one primary responsibility, an owned output and completion evidence, explicit Always / Ask First / Never boundaries, real tool contracts and a differentiated role under `_common/BOUNDARIES.md`. Test the routing distinction with positive and negative cases. Overlap scoring and approval thresholds: `reference/overlap-detection.md`.

References are optional. Extract only detail whose absence causes a specific execution failure and give it a conditional loading path. Do not require examples, diagrams, a minimum number of references or a prescribed word count to make a skill appear complete. Authoritative limits and structure come from the template and repository validation.

## 10.3 Declarative Tool Promotion

Prefer general tools composed into workflows. Introduce a dedicated tool only when at least one boundary requires it:

| Boundary | Necessary distinction |
|----------|-----------------------|
| Security | Enforces authorization or isolates untrusted input beyond prompt instructions |
| Reversibility | Needs explicit confirmation, transactionality, rollback or undo |
| UX presentation | Requires a structured interaction the general tool cannot represent |
| Observability | Needs independently inspectable status, logs, provenance or progress |

A convenient name alone is not a tool boundary. Validate the actual host interface rather than writing plausible API calls from memory.

## 11. Generated-Skill Authoring

Apply `_common/OPUS_5_AUTHORING.md` P1–P12 as the shared authoring contract. Do not copy its rules or cached model comparisons here. For runtime-dependent syntax or capability, consult `_common/CLI_COMPATIBILITY.md` and the running host.

### 11.13 Verification

Use `reference/validation-checklist.md`. Static validity is not evidence that the skill behaves correctly; report which routing, behavior and integration cases were actually exercised.

## Canonical Sources — Consult Only for a Relevant Design Decision

- Agent Skills format and loading behavior: https://agentskills.io/ — verify discovery, activation and optional resource loading; checked 2026-09-17.
- Workflow versus autonomous-agent patterns: https://www.anthropic.com/engineering/building-effective-agents — use to select a mechanism, not as a benchmark or model-performance guarantee; published 2024-12-19, checked 2026-09-17.
- Tool design: https://www.anthropic.com/engineering/writing-tools-for-agents — verify a proposed tool boundary against the actual implementation; checked 2026-09-17.
