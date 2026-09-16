# Subagent Parallel Protocol

> **Tier:** `orchestration` — activates from the hub, a recipe, or on engine detection. Precedence: `_common/OPERATIONAL.md` § Contract Precedence.

Common protocol for individual skills to delegate independent subtasks using the runtime's advertised subagent interface.
For Nexus internal parallel branches → `_common/PARALLEL.md`. For full team orchestration (4+ workers) → Rally.

---

## Scope: Three Layers of Parallelism

| Layer | Orchestrator | Workers | Use When |
|-------|-------------|---------|----------|
| **Skill-internal** (this doc) | Individual skill agent | 2-3 Task subagents | Independent subtasks within a single skill's work |
| **Nexus parallel branches** | Nexus | Agent chains per branch | AUTORUN_FULL multi-branch execution |
| **Rally team** | Rally | Multiple Claude instances | 4+ parallel workers, complex coordination |

---

## Decision: When to Spawn Subagents

### USE subagents when:
- 2-3 **independent** subtasks exist (no data dependencies)
- Multiple **perspectives/engines** improve quality (Multi-Engine Mode)
- Parallel **verification** reduces wall-clock time (test + lint + type-check)
- Different **code areas** need simultaneous investigation

### DO NOT use subagents when:
- Tasks have **sequential dependencies** (B needs A's output)
- Working on a **single file** (subagents cannot share file ownership)
- Task completes in **< 30 seconds** (spawn overhead exceeds benefit)
- **4+ workers** needed → use Rally instead
- Task requires **shared mutable state** or iterative refinement

### Decision Flow

```
Task received
  ├─ Single focus, < 30s? ──────────────────→ Do it yourself
  ├─ 2-3 independent subtasks? ─────────────→ Spawn subagents (this protocol)
  ├─ 4+ independent subtasks? ──────────────→ Delegate to Rally
  └─ Sequential chain? ────────────────────→ Do it yourself (or Nexus AUTORUN)
```

### Why subagents pay: context isolation, not extra hands

A subagent's value is that it explores in a **clean context window** and returns a **condensed, distilled summary — Anthropic's reference figure is 1,000–2,000 tokens** (*Effective context engineering for AI agents*). The detailed exploration (dozens of file reads, dead ends, raw tool output) is spent inside the subagent and *never enters the parent's context*; only the distillation crosses the boundary. That separation of detailed search from high-level synthesis is the mechanism — a subagent that streams its raw findings back has paid the spawn cost and kept the context cost.

**Two consequences for authoring:**
- **Give each spawn an appropriate return ceiling**, not a token quota. Return evidence pointers and unresolved issues rather than raw traces; `_STEP_COMPLETE` / `## NEXUS_HANDOFF` supply the structure. Large artifacts may remain in files.
- **Judge a fan-out by context saved, not tasks parallelized.** If each branch would return its full trace, the parent's context grows as fast as if it had done the work inline, and only wall-clock improves.

---

## Agent Tool Quick Reference

Discover the installed runtime's agent interface, allowed tools, capacity, nesting, isolation and join/resume semantics through `_common/CLI_COMPATIBILITY.md`. Custom subagent definitions and `SKILL.md` are different formats: the repository's skills retain exactly `name` and `description` frontmatter keys.

### subagent_type Selection

Choose an advertised read-only investigator for research, a suitably scoped writer for implementation, and a separate verifier where required. A role label does not enforce read-only access: check the actual grant.

### model Selection

Inherit the authorized model/effort unless a supported, evidence-justified alternative is within budget. Do not hard-code generation names in skill prompts.

### Key Frontmatter Fields (Custom Subagents)

Use only fields documented for the actual CLI and version. Never copy custom-agent configuration fields into this repository's SKILL.md frontmatter. Context isolation, file ownership and permission scopes must be checked at dispatch.

### Parallel Launch

Launch independent work through the available concurrent interface, then join all prerequisite results. A familiar tool name or multiple sequential calls does not prove parallel execution.

## Codex Orchestrator Parallelism

Use `_common/CODEX_ORCHESTRATION.md` for Codex and `_common/AGY_ORCHESTRATION.md` for agy; apply the same outcome, authority, ownership and merge contracts. Runtime details stay in the compatibility layer.

---

## Patterns

### RESEARCH_FAN_OUT

Multiple Explore agents investigate different areas in parallel.

**When:** Broad investigation across distinct code areas, documentation, or domains.

**Setup:**
- 2-3 `Explore` subagents, each with a distinct search scope
- Each agent receives: Role + Target area + Output format
- No shared files or overlapping scope

**Merge:** Union — collect all findings → deduplicate → consolidate → report.

---

### MULTI_ENGINE

Multiple AI engines independently work on the same task, leveraging diverse knowledge bases. **Default baseline: Claude + Codex (dual-engine).** agy / Antigravity is added as a third axis when AVAILABLE at PREFLIGHT — never required. See `_common/MULTI_ENGINE_RECIPE.md §Base Engine Policy` for tag conventions and Engine Availability Modes.

**When:** Quality-critical tasks where diverse perspectives catch blind spots (security scans, bug hunts, edge-case tests, refactoring proposals).

#### Engine Dispatch Table

Bind installed authorized engines through `_common/CLI_COMPATIBILITY.md`; collect runtime outcomes under `_common/MULTI_ENGINE_RECIPE.md` §3.5. No engine may be declared successful from exit status alone.

#### Loose Prompt Rules

Pass a bounded task, authoritative inputs/revision, acceptance criteria, output schema, allowed effects and prohibited outcomes. Withhold other engines' conclusions and prescriptive domain frameworks until synthesis to preserve independence. “Loose” never means omitting security, scope or legal constraints.

#### Dispatch Examples

Use the available native spawn API, or a documented headless CLI inside its approved sandbox. Validate structured output and required artifacts; do not copy historical permission-bypass/PTY recipes into every skill. Exact commands and conditional workarounds → `_common/CLI_COMPATIBILITY.md` §9.

#### Fallback Rule

Use the Degraded Modes in `_common/MULTI_ENGINE_RECIPE.md`. Same-engine independent sessions may provide additional perspectives but never count as missing engines or acquire their provenance tags. Report missing independent verification instead of simulating it.

#### Merge Strategies for Multi-Engine

| Strategy | When | Process |
|----------|------|---------|
| **Union** | Findings should be comprehensive (scans, tests, investigations) | Collect all → deduplicate same-location/same-type → boost confidence for multi-engine hits → sort by severity → report |
| **Compete** | Best single output needed (refactoring, proposals) | Collect all → evaluate against criteria → select best (or combine best parts) → present with rationale |

Each skill defines its own merge details (criteria, dedup rules, output format) in its SKILL.md.

---

### INDEPENDENT_IMPL

Parallel implementation of independent files/modules.

**When:** Multiple files need changes with no shared dependencies.

**Setup:**
- Each `general-purpose` subagent owns specific files (declare ownership upfront)
- No two subagents may modify the same file

**Merge:** Concat — combine all changes (no conflicts expected).

---

### VERIFICATION_PARALLEL

Run multiple verification tasks simultaneously.

**When:** Test suite, linter, type checker, and/or security scan can all run independently.

**Setup:**
- Each subagent runs one verification tool
- Results are independent pass/fail

**Merge:** All-pass gate — all must pass for overall success. Any failure blocks.

---

### COMPETITIVE_APPROACH

Multiple subagents implement different solutions to the same problem, then the best is selected.

**When:** Design exploration, algorithm comparison, or uncertain approach.

**Setup:**
- 2-3 `general-purpose` subagents, each with a different approach/constraint
- Each works in isolation on the same problem

**Merge:** Compete — evaluate each against criteria → select winner → adopt (or combine best elements).

---

## Result Aggregation

| Strategy | Description | Use With |
|----------|-------------|----------|
| **Union** | Collect all → deduplicate → consolidate → rank | RESEARCH_FAN_OUT, MULTI_ENGINE (comprehensive) |
| **Concat** | Combine all outputs (no overlap expected) | INDEPENDENT_IMPL |
| **All-pass** | Every result must pass; any failure = overall failure | VERIFICATION_PARALLEL |
| **Compete** | Evaluate against criteria → select best | COMPETITIVE_APPROACH, MULTI_ENGINE (selective) |

---

## Error Handling

| Scenario | Action |
|----------|--------|
| **1 of 3 subagents fails** | Continue with remaining results; note reduced coverage in report |
| **All subagents fail** | Fall back to sequential single-agent execution |
| **Timeout** (subagent takes too long) | Use available results; note incomplete coverage |
| **Conflicting results** | Flag contradictions explicitly; escalate to user if safety-critical |
| **Engine unavailable** (MULTI_ENGINE) | Apply truthful degraded mode; never relabel a same-engine result |

---

## Constraints

| Rule | Limit | Reason |
|------|-------|--------|
| Max parallel subagents | **~3 (default guideline)** | Not an absolute ceiling — tune to available capacity, ownership, measured benefit and authorized budget. For large parallel workloads, delegating to Rally for proper coordination is recommended. |
| File ownership | **Exclusive** | No two subagents modify the same file |
| Cost awareness | **Each subagent consumes runtime resources** | Only parallelize when benefit > overhead |
| Spawn decision | **Agent's judgment** | Unless Nexus explicitly instructs `multi-engine` |
| Nesting | **Prohibited** | Subagents cannot spawn other subagents |
| Output style | **No completion preamble** | See `_common/OUTPUT_STYLE.md §Subagent Completion Pattern` — open with the deliverable, never with "completed/finished/here is the report" |

## Subagent Output Rules

Subagents return text to the orchestrator (parent skill or user). Apply universally regardless of `subagent_type`:

- **Open with the deliverable.** No "All work is complete. Here's the summary." Begin with the first `## ` header, table, or lead finding. The completion is implicit.
- **End at the last deliverable line.** No trailing closer ("以上で完了です", "Let me know if anything else").
- **Tier the report.** Pick S/M/L/XL based on what was actually asked; don't pad to fill an L-tier report shape when M would do. See `_common/OUTPUT_STYLE.md §Output Tiers`.
- **Structure beats prose.** ≥3 distinct items → table or bullet list, not paragraph.
- **`_STEP_COMPLETE` and handoff blocks are exempt** from tier limits but must NOT be preceded by prose preamble.

When invoking a subagent via the `Agent` tool, instruct it explicitly in the prompt: *"Open with the deliverable, not with completion preamble."*

## Context Inheritance Rules

Do not assume parent history, skills, permissions or MCP connections transfer identically across engines. Verify actual inheritance through `_common/CLI_COMPATIBILITY.md`; explicitly supply the scoped task, applicable contracts and evidence references. Restrict tools/effects with host controls where possible. A textual prohibition alone is not sandbox isolation.

## Lifecycle

- **failure:** F1: model-specific payloads and assumed tool signatures could misroute delegation.
- **effect:** Use verified interfaces and scoped evidence without duplicating specialist methods; live-runtime evaluation remains required.
- **owner:** Rally
- **removal:** Retire adapter-specific text after all callers use the compatibility contract and delegation fixtures preserve ownership and result joins.
