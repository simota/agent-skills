# Fix Templates

**Purpose:** Skeleton templates and Quest-based exemplar patterns for generating fix snippets.
**Read when:** Executing the RECOMMEND phase of the audit workflow.

---

## Fix Generation Rules

1. Fill all `{AGENT_NAME}` placeholders with the actual agent name.
2. Fill all `{AGENT_NAME_LOWER}` placeholders with the lowercase agent name.
3. Customize content descriptions based on the agent's existing SKILL.md content.
4. Follow P0 → P1 → P2 → P3 priority order for fixes.
5. Cite the corresponding Quest section as exemplar for each template.

---

## F1: YAML Frontmatter

**Quest exemplar:** Lines 1-4

```markdown
---
name: {AGENT_NAME}
description: [Japanese description of what the agent does]
---
```

---

## L1: Language Compliance Fix

No template — this requires translating existing Japanese body text to English. Provide specific translation suggestions for each detected Japanese string.

**Rule:** Preserve `description:` in Japanese. Translate all body text to English.

---

## H1-H3: HTML Comment Block

**Quest exemplar:** Lines 6-38

```markdown
<!--
CAPABILITIES_SUMMARY:
- capability_1: [Description of what {AGENT_NAME} can do]
- capability_2: [Another capability]
- capability_3: [Third capability]

COLLABORATION_PATTERNS:
- [SourceAgent] -> {AGENT_NAME}: [What they send]
- {AGENT_NAME} -> [TargetAgent]: [What you send]

BIDIRECTIONAL_PARTNERS:
- INPUT: [Agent1] ([what they send]), [Agent2] ([what they send])
- OUTPUT: [Agent3] ([what you send]), [Agent4] ([what you send])

PROJECT_AFFINITY: [universal | Domain1(H) Domain2(M) Domain3(L)]
-->
```

---

## S1: Trigger Guidance

**Quest exemplar:** "Trigger Guidance" section

```markdown
## Trigger Guidance

Use {AGENT_NAME} when the user needs:
- [primary use case 1]
- [primary use case 2]
- [primary use case 3]

Route elsewhere when the task is primarily:
- [alternative scenario 1]: `[AlternativeAgent]`
- [alternative scenario 2]: `[AlternativeAgent]`
```

---

## S2: Core Contract

**Quest exemplar:** "Core Contract" section

```markdown
## Core Contract

- [Commitment 1 — what {AGENT_NAME} always delivers].
- [Commitment 2 — quality standard or constraint].
- [Commitment 3 — what {AGENT_NAME} never does].
- [Commitment 4 — verification or validation rule].
```

---

## S3: Boundaries

**Quest exemplar:** "Boundaries" section

```markdown
## Boundaries

Agent role boundaries -> `_common/BOUNDARIES.md`

### Always

- [Essential behavior 1].
- [Essential behavior 2].
- [Essential behavior 3].

### Ask First

- [High-stakes situation requiring user confirmation].
- [Another situation].

### Never

- [Genuinely dangerous action 1].
- [Genuinely dangerous action 2].
```

---

## S4: Workflow

**Quest exemplar:** "Workflow" section

```markdown
## Workflow

`{PHASE1} → {PHASE2} → {PHASE3} → {PHASE4} → {PHASE5}`

| Phase | Required action | Key rule | Read |
|-------|-----------------|----------|------|
| `{PHASE1}` | [Action description] | [Key constraint] | `reference/[relevant].md` |
| `{PHASE2}` | [Action description] | [Key constraint] | `reference/[relevant].md` |
| `{PHASE3}` | [Action description] | [Key constraint] | `reference/[relevant].md` |
```

---

## S5: Output Routing

**Quest exemplar:** "Output Routing" section

```markdown
## Output Routing

| Signal | Approach | Primary output | Read next |
|--------|----------|----------------|-----------|
| `[keyword1]`, `[keyword2]` | [Approach description] | [Output type] | `reference/[relevant].md` |
| `[keyword3]`, `[keyword4]` | [Approach description] | [Output type] | `reference/[relevant].md` |
| unclear [domain] request | [Default approach] | [Default output] | `reference/[relevant].md` |

Routing rules:

- If the request mentions [condition], read `reference/[relevant].md`.
- Always read `reference/[relevant].md` for [phase] phase.
```

---

## S6: Output Requirements

**Quest exemplar:** "Output Requirements" section

```markdown
## Output Requirements

Every deliverable must include:

- [Required element 1 (e.g., artifact type)].
- [Required element 2 (e.g., target context)].
- [Required element 3 (e.g., quality criteria)].
- [Required element 4 (e.g., next agent recommendation)].
```

---

## S7: Collaboration

**Quest exemplar:** "Collaboration" section

```markdown
## Collaboration

**Receives:** [Agent1] ([what context]), [Agent2] ([what context])
**Sends:** [Agent3] ([what deliverable]), [Agent4] ([what deliverable])

**Overlap boundaries:**
- **vs [SimilarAgent]**: [SimilarAgent] = [their focus]; {AGENT_NAME} = [your focus].
```

---

## S8: Reference Map

**Quest exemplar:** "Reference Map" section

```markdown
## Reference Map

| Reference | Read this when |
|-----------|----------------|
| `reference/[file1].md` | You need [specific knowledge area]. |
| `reference/[file2].md` | You need [specific knowledge area]. |
```

**For agents without reference/:**

```markdown
## Reference Map

No dedicated references. Domain knowledge is inline in this SKILL.md.
```

---

## S9: Operational

**Quest exemplar:** "Operational" section

```markdown
## Operational

- Journal [domain-specific decisions] in `.agents/{AGENT_NAME_LOWER}.md`; create it if missing.
- Record [reusable patterns, templates, preferences].
- After significant {AGENT_NAME} work, append to `.agents/PROJECT.md`: `| YYYY-MM-DD | {AGENT_NAME} | (action) | (files) | (outcome) |`
- Standard protocols -> `_common/OPERATIONAL.md`
```

---

## A1: AUTORUN Support

**Quest exemplar:** "AUTORUN Support" section

```markdown
## AUTORUN Support

When {AGENT_NAME} receives `_AGENT_CONTEXT`, parse `task_type`, `description`, [domain-specific fields], and `Constraints`, choose the correct output route, run the {WORKFLOW} workflow, produce the deliverable, and return `_STEP_COMPLETE`.

### `_STEP_COMPLETE`

\```yaml
_STEP_COMPLETE:
  Agent: {AGENT_NAME}
  Status: SUCCESS | PARTIAL | BLOCKED | FAILED
  Output:
    deliverable: [artifact path or inline]
    artifact_type: "[list of possible types]"
    parameters:
      [domain_param_1]: "[value]"
      [domain_param_2]: "[value]"
  Next: [Agent1] | [Agent2] | DONE
  Reason: [Why this next step]
\```
```

---

## A2: Nexus Hub Mode

**Quest exemplar:** "Nexus Hub Mode" section

```markdown
## Nexus Hub Mode

When input contains `## NEXUS_ROUTING`, do not call other agents directly. Return all work via `## NEXUS_HANDOFF`.

### `## NEXUS_HANDOFF`

\```text
## NEXUS_HANDOFF
- Step: [X/Y]
- Agent: {AGENT_NAME}
- Summary: [1-3 lines]
- Key findings / decisions:
  - [Domain-specific key 1]: [value]
  - [Domain-specific key 2]: [value]
- Artifacts: [file paths or inline references]
- Risks: [identified risks]
- Open questions: [blocking / non-blocking]
- Pending Confirmations: [Trigger/Question/Options/Recommended]
- User Confirmations: [received confirmations]
- Suggested next agent: [Agent] (reason)
- Next action: CONTINUE | VERIFY | DONE
\```
```
