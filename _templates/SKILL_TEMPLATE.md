---
name: AgentName
description: "One-line description. What this agent does and when to use it. Don't use for X (Agent), Y (Agent)."
---

<!--
CAPABILITIES_SUMMARY:
- capability_1: Description of what this agent can do
- capability_2: Another capability

COLLABORATION_PATTERNS:
- Pattern A: AgentName → PartnerAgent (deliverable description)
- Pattern B: SourceAgent → AgentName (input description)

BIDIRECTIONAL_PARTNERS:
- INPUT: Agent1 (what they send), Agent2 (what they send)
- OUTPUT: Agent3 (what you send), Agent4 (what you send)

PROJECT_AFFINITY: universal | SaaS(H) E-commerce(M) ...
-->

# AgentName

> **"Motto — one line that captures the agent's philosophy."**

Identity statement (1-2 lines). What you do, what you deliver, scope per invocation.

**Principles:** Principle 1 · Principle 2 · Principle 3 · Principle 4 · Principle 5

## Trigger Guidance

Use AgentName when the task needs:
- [specific task or signal 1]
- [specific task or signal 2]
- [specific task or signal 3]

Route elsewhere when the task is primarily:
- [adjacent concern]: `AlternativeAgent`
- [adjacent concern]: `AlternativeAgent`
- [adjacent concern]: `AlternativeAgent`

## Core Contract

- [Operational commitment 1 — e.g., workflow order, evidence requirements]
- [Operational commitment 2 — e.g., quality gates, quantification rules]
- [Operational commitment 3 — e.g., safety constraints, severity ordering]
- [Domain-specific rule with concrete threshold or rationale]
- Keep changes < 50 lines per modification.

## Boundaries

Agent role boundaries → `_common/BOUNDARIES.md`

### Always

- [Essential behavior 1]
- [Essential behavior 2]
- [Essential behavior 3]
- Check/log to `.agents/PROJECT.md`.

### Ask First

- [High-stakes decision 1]
- [High-stakes decision 2]

### Never

- [Genuinely dangerous action 1 — include rationale or war story if helpful]
- [Genuinely dangerous action 2]

## Workflow

`PHASE_1 → PHASE_2 → PHASE_3 → PHASE_4`

| Phase | Focus | Required checks | Read |
|-------|-------|-----------------|------|
| `PHASE_1` | [What to do] | [What to verify] | `reference/topic.md` |
| `PHASE_2` | [What to do] | [What to verify] | `reference/topic.md` |
| `PHASE_3` | [What to do] | [What to verify] | `reference/topic.md` |
| `PHASE_4` | [What to do] | [What to verify] | — |

## Output Routing

| Signal | Approach | Primary output | Read next |
|--------|----------|----------------|-----------|
| `keyword1`, `keyword2` | [Approach description] | [Deliverable type] | `reference/topic.md` |
| `keyword3`, `keyword4` | [Approach description] | [Deliverable type] | `reference/topic.md` |
| unclear request | [Default approach] | [Default deliverable] | `reference/` |
| complex multi-agent task | Nexus-routed execution | Structured handoff | `_common/BOUNDARIES.md` |

## Recipes (optional — see `_common/RECIPES.md`)

Omit this section if the skill has 2 or fewer modes or if Output Routing above is sufficient. Keep the "When to Use" column in English — concise phrases describing the activation condition.

| Recipe | Subcommand | Default? | When to Use | Read First |
|--------|-----------|---------|-------------|------------|
| [Recipe Name] | `[subcommand]` | ✓ | [Short English phrase describing when to pick this] | `reference/[file].md` |
| [Recipe Name] | `[subcommand]` | | [Short English phrase describing when to pick this] | `reference/[file].md` |

## Subcommand Dispatch (required if Recipes defined)

Parse the first token of user input.
- If it matches a Recipe Subcommand above → activate that Recipe; load only the "Read First" column files at the initial step.
- Otherwise → default Recipe (`[default-subcommand]` = [Default Recipe Name]). Apply the normal workflow.

Behavior notes per Recipe (keep English — describe the step sequence and any recipe-specific rules):
- `[subcommand]`: [One-line English description of the phase order and key constraints.]
- `[subcommand]`: [One-line English description of the phase order and key constraints.]

## [Domain-Specific Section(s)]

<!-- The heart of the skill — decision tables, critical thresholds, framework coverage, etc. -->
<!-- Use tables for decision logic and quick reference -->
<!-- Keep actionable knowledge inline; move detailed reference material to reference/ -->

## Output Requirements

Every deliverable must include:

- [Required element 1]
- [Required element 2]
- [Required element 3]
- Output language follows the CLI global config (`settings.json` `language` field, `CLAUDE.md`, `AGENTS.md`, or `GEMINI.md`). Code, identifiers, file paths, CLI commands, and technical terms remain in English. (SKILL.md structure itself — Recipes table, Subcommand Dispatch, section headings — is written in English.)

## Collaboration

AgentName receives [what] from upstream agents. AgentName sends [what] to downstream agents.

| Direction | Handoff | Purpose |
|-----------|---------|---------|
| SourceAgent → AgentName | `SOURCE_TO_AGENTNAME` | [What they send] |
| AgentName → TargetAgent | `AGENTNAME_TO_TARGET` | [What you send] |

### Overlap Boundaries

| Agent | AgentName owns | They own |
|-------|----------------|----------|
| RelatedAgent1 | [Your responsibility] | [Their responsibility] |
| RelatedAgent2 | [Your responsibility] | [Their responsibility] |

## Reference Map

| File | Read this when... |
|------|-------------------|
| `reference/topic-1.md` | You need [specific knowledge] |
| `reference/topic-2.md` | You need [specific knowledge] |
| [`_common/BOUNDARIES.md`](_common/BOUNDARIES.md) | Role boundaries are ambiguous |
| [`_common/OPERATIONAL.md`](_common/OPERATIONAL.md) | You need journal, activity log, AUTORUN, Nexus, Git, or shared operational defaults |

## Operational

**Journal** (`.agents/{name}.md`): Record only [skill-specific topic] — [brief description of what to record].

- Activity log: append `| YYYY-MM-DD | AgentName | (action) | (files) | (outcome) |` to `.agents/PROJECT.md`.
- Follow `_common/GIT_GUIDELINES.md`.

Shared protocols: [`_common/OPERATIONAL.md`](_common/OPERATIONAL.md)

## AUTORUN Support

When AgentName receives `_AGENT_CONTEXT`, parse `task_type`, `description`, and `Constraints`, execute the standard workflow (skip verbose explanations, focus on deliverables), and return `_STEP_COMPLETE`.

### `_STEP_COMPLETE`

```yaml
_STEP_COMPLETE:
  Agent: AgentName
  Status: SUCCESS | PARTIAL | BLOCKED | FAILED
  Output:
    deliverable: [primary artifact]
    artifact_type: "[deliverable type]"
    parameters:
      key_param_1: "[value]"
      key_param_2: "[value]"
  Validations:
    completeness: "[complete | partial | blocked]"
    quality_check: "[passed | flagged | skipped]"
  Next: [NextAgent] | DONE
  Reason: [Why this next step]
```

## Nexus Hub Mode

When input contains `## NEXUS_ROUTING`, do not call other agents directly. Return all work via `## NEXUS_HANDOFF`.

### `## NEXUS_HANDOFF`

```text
## NEXUS_HANDOFF
- Step: [X/Y]
- Agent: AgentName
- Summary: [1-3 lines]
- Key findings / decisions:
  - [domain-specific items]
- Artifacts: [file paths or "none"]
- Risks: [identified risks]
- Open questions (blocking/non-blocking):
  - [blocking: yes/no] [question]
- Pending Confirmations:
  - Trigger: [INTERACTION_TRIGGER name if any]
  - Question: [Question for user]
  - Options: [Available options]
  - Recommended: [Recommended option]
- User Confirmations:
  - Q: [Previous question] → A: [User's answer]
- Suggested next agent: [AgentName] (reason)
- Next action: CONTINUE | VERIFY | DONE
```

---

> Closing line — a memorable reminder of the agent's purpose.
