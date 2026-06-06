# SKILL.md Template

**Purpose:** Canonical template and section contract for generated skills.
**Read when:** You are drafting or checking the structure of a skill package.

## Contents
- File Structure Overview
- Complete SKILL.md Template
- NEXUS_HANDOFF
- Output Contract (Output Density Protocol)
- Ma Layout Notes
- Section Guidelines
- Line Count Guidelines
- Quality Checklist

---

## File Structure Overview

```
[agent_name]/
├── SKILL.md              # Main specification (60-120 lines, principle-centered)
└── reference/
    ├── patterns.md       # Design patterns (required)
    ├── examples.md       # Usage examples (required)
    ├── handoffs.md       # Handoff templates (required)
    └── [domain].md       # Domain-specific (optional, 0-4 files)
```

---

## Complete SKILL.md Template

````markdown
---
name: [AgentName]
description: [English description. Keep it within 100 characters and state the agent purpose plus when to use it. Include positive and negative triggers.]
---

<!--
CAPABILITIES SUMMARY (for Nexus routing):
- [Capability 1 - main function]
- [Capability 2]
- [Capability 3]
- [Capability 4]
- [Capability 5]
# 5-10 capabilities that help Nexus route requests

COLLABORATION PATTERNS:
// ...
```
[Agent's core belief - 3-5 lines]
[What drives this agent's decisions]
[What makes this agent unique]
```

---

## Boundaries

**Always do:**
- [Required action 1 - most important]
- [Required action 2]
- [Required action 3]
- [Required action 4]
# 4-8 items, ordered by importance

**Ask first:**
- [Confirmation point 1 - highest risk]
- [Confirmation point 2]
...
```yaml
questions:
  - question: "[Clear question ending with a question mark]"
    header: "[Short Label]"  # Max 12 chars
    options:
      - label: "[Option 1] (Recommended)"
        description: "[Outcome if this option is selected]"
      - label: "[Option 2]"
        description: "[Outcome if this option is selected]"
      - label: "[Option 3]"
        description: "[Outcome if this option is selected]"
    multiSelect: false
```

# Repeat for each trigger that needs user confirmation

---

## [DOMAIN SECTION 1: Core Workflow]

### Overview

[Describe the main workflow or framework]

```
[ASCII diagram of workflow]
```

### Step-by-Step Process

1. **[Step 1 Name]**
   - [Description]
   - [Details]

2. **[Step 2 Name]**
   - [Description]
   - [Details]

---

## [DOMAIN SECTION 2: Key Patterns]

...
```[language]
// Example code or template
```

### Pattern 2: [Pattern Name]

**When to use:** [Condition]

```[language]
// Example code or template
```

---

## [DOMAIN SECTION 3: Integration Points]

### Input Processing

[How this agent receives and processes input]

```yaml
INPUT_FORMAT:
  source: "[Source agent or user]"
  type: "[Input type]"
  required_fields:
    - [field 1]
    - [field 2]
```

### Output Generation

[How this agent generates and formats output]

```yaml
OUTPUT_FORMAT:
  destination: "[Target agent or user]"
  type: "[Output type]"
  fields:
    - [field 1]
    - [field 2]
```

---

## Agent Collaboration

### Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    INPUT PROVIDERS                          │
│  [Agent1] → [Input type 1]                                  │
│  [Agent2] → [Input type 2]                                  │
└─────────────────────┬───────────────────────────────────────┘
                      ↓
            ┌─────────────────┐
            │   [AgentName]   │
            │   [Role label]  │
            └────────┬────────┘
                     ↓
┌─────────────────────────────────────────────────────────────┐
│                   OUTPUT CONSUMERS                          │
│  [Agent3] ← [Output type 1]                                 │
│  [Agent4] ← [Output type 2]                                 │
└─────────────────────────────────────────────────────────────┘
```

### Collaboration Patterns

| Pattern | Name | Flow | Purpose |
|---------|------|------|---------|
| **A** | [Pattern A Name] | [Flow description] | [Purpose] |
| **B** | [Pattern B Name] | [Flow description] | [Purpose] |
| **C** | [Pattern C Name] | [Flow description] | [Purpose] |

### Handoff Patterns

**From [Source Agent]:**
```
[Describe how to receive handoff from source agent]
```

**To [Target Agent]:**
```
[Describe how to send handoff to target agent]
```

---

## [AgentName]'S JOURNAL

Before starting, read `.agents/[agentname].md` (create if missing).
Also check `.agents/PROJECT.md` for shared project knowledge.

Your journal is NOT a log - only add entries for [DOMAIN-SPECIFIC INSIGHTS].

**Only add journal entries when you discover:**
- [Insight type 1]
- [Insight type 2]
- [Insight type 3]

...
```
| YYYY-MM-DD | [AgentName] | (action) | (files) | (outcome) |
```

Example:
```
| 2025-01-15 | [AgentName] | [Sample action] | [Sample files] | [Sample outcome] |
```

---

## AUTORUN Support (Nexus Autonomous Mode)

When invoked in Nexus AUTORUN mode:
1. Parse `_AGENT_CONTEXT` to understand task scope and constraints
2. Execute normal work ([brief description of work])
3. Skip verbose explanations, focus on deliverables
4. Append `_STEP_COMPLETE` with full details

### Input Format (_AGENT_CONTEXT)

```yaml
_AGENT_CONTEXT:
  Role: [AgentName]
  Task: [Specific task from Nexus]
  Mode: AUTORUN
  Chain: [Previous agents in chain]
  Input: [Handoff received from previous agent]
  Constraints:
    - [Constraint 1]
    - [Constraint 2]
  Expected_Output: [What Nexus expects]
```

### Output Format (_STEP_COMPLETE)

```yaml
_STEP_COMPLETE:
  Agent: [AgentName]
  Status: SUCCESS | PARTIAL | BLOCKED | FAILED
  Output:
    [output_type]:
      - [Detail 1]
      - [Detail 2]
    files_changed:
      - path: [file path]
        type: [created / modified / deleted]
        changes: [brief description]
  Handoff:
    Format: [AGENTNAME]_TO_[NEXT]_HANDOFF
    Content: [Full handoff content for next agent]
  Artifacts:
    - [Artifact 1]
    - [Artifact 2]
  Risks:
    - [Risk 1]
    - [Risk 2]
  Next: [NextAgent] | VERIFY | DONE
  Reason: [Why this next step]
```

---

## Nexus Hub Mode

When user input contains `## NEXUS_ROUTING`, treat Nexus as hub.

- Do not instruct other agent calls
- Always return results to Nexus (append `## NEXUS_HANDOFF` at output end)
- Include all required handoff fields

```text
## NEXUS_HANDOFF
- Step: [X/Y]
- Agent: [AgentName]
- Summary: 1-3 lines
- Key findings / decisions:
  - [Finding 1]
  - [Finding 2]
- Artifacts (files/commands/links):
  - [Artifact 1]
  - [Artifact 2]
- Risks / trade-offs:
  - [Risk 1]
- Open questions (blocking/non-blocking):
  - [Question 1]
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

## Output Contract

This skill follows the Output Density Protocol — see `_common/OUTPUT_STYLE.md`.

```markdown
## Output Contract
- Default tier: [S | M | L | XL]    # see _common/OUTPUT_STYLE.md §Output Tiers
- Style: `_common/OUTPUT_STYLE.md` (banned patterns + format priority)
- Task overrides:
  - [task-name-1]: [tier]
  - [task-name-2]: [tier]
- Domain bans (optional): [skill-specific banned phrases or formats]
```

Tier guidance:

| Tier | Lines | Typical Use |
|------|-------|-------------|
| `S` | 1–3 | Lookup, status, yes/no answers |
| `M` | 5–15 | Typical findings, plans, short fixes |
| `L` | 30–80 | Structured deliverables, multi-section reports |
| `XL` | 80+ | Full specs/designs (justify why) |

Rules:
- Pick the smallest tier that fully answers the task; never pad to fill a tier.
- Do not duplicate banned-pattern lists; reference `_common/OUTPUT_STYLE.md` instead.
- `_STEP_COMPLETE` and `## NEXUS_HANDOFF` blocks are exempt from tier limits — they have their own envelopes.

---

## Output Language

Output language follows the CLI global config (`settings.json` `language` field, `CLAUDE.md`, `AGENTS.md`, or `GEMINI.md`).

---

## Git Commit & PR Guidelines

Follow `_common/GIT_GUIDELINES.md` for commit messages and PR titles:
- Use Conventional Commits format: `type(scope): description`
- **DO NOT include agent names** in commits or PR titles
- Keep subject line under 50 characters
...
````

---

## Ma Layout Notes

When generating SKILL.md, consider attention-optimized placement of sections.

### Zone Placement Guide

| Zone | Position | Content | Attention Level |
|------|----------|---------|-----------------|
| Zone 1 | First 15% | Identity, capabilities, boundaries, triggers (table) | Highest |
| Zone 2 | Next 35% | Primary workflow, domain sections, key decisions | Moderate |
| Zone 3 | Next 35% | Catalogs, collaboration, journal, daily process, tactics | Lower |
| Zone 4 | Last 15% | AUTORUN, Nexus Hub, handoffs, git guidelines, closing | Heightened |

### Context Efficiency Targets

| Agent Size | Lines | Token Target | Boilerplate Max |
|-----------|-------|-------------|-----------------|
| Compact | 400-600 | 1500-2500 | 10% |
| Standard | 600-1000 | 2500-4000 | 12% |
| Extended | 1000-1400 | 4000-5500 | 15% |

See `reference/context-compression.md` for detailed compression strategies and Ma principles.

---

## Section Guidelines

### Frontmatter

```yaml
---
name: agent-name       # kebab-case, 1-2 syllables preferred
description: English description  # Max 100 chars, include positive/negative triggers
---
```

### CAPABILITIES_SUMMARY

- 5-10 bullet points
- Action-oriented verbs
- Helps Nexus route requests to this agent
- Be specific, not generic

### Boundaries

| Section | Count | Purpose |
|---------|-------|---------|
| Always do | 4-8 | Mandatory behaviors |
| Ask first | 2-5 | User confirmation required |
| Never do | 3-6 | Forbidden actions |

### INTERACTION_TRIGGERS

| Timing | Use Case |
|--------|----------|
| BEFORE_START | Critical decisions before work begins |
| ON_DECISION | Choice points during work |
| ON_RISK | Risk mitigation |
| ON_AMBIGUITY | Clarification needed |
| ON_COMPLETION | Post-work confirmations |

### Domain Sections

- 3-10 sections based on agent specialty
- Include code examples where relevant
- Use ASCII diagrams for workflows
- Reference external files when appropriate

### Collaboration Section

- ASCII diagram showing input/output flow
- Table of collaboration patterns
- Handoff template references

---

## Line Count Guidelines

| Component | Min Lines | Max Lines |
|-----------|-----------|-----------|
| Frontmatter | 4 | 6 |
| CAPABILITIES comment | 15 | 30 |
| Philosophy | 5 | 15 |
| Boundaries | 20 | 40 |
| INTERACTION_TRIGGERS | 40 | 100 |
| Domain sections | 150 | 600 |
| Collaboration | 40 | 80 |
| Journal | 15 | 30 |
| Daily Process | 20 | 50 |
| Tactics/Avoids | 15 | 30 |
| AUTORUN Support | 40 | 80 |
| Nexus Hub Mode | 25 | 40 |
| **Total** | **400** | **1400** |

---

## Quality Checklist

Before finalizing SKILL.md:

- [ ] Frontmatter complete (name, description)
- [ ] CAPABILITIES_SUMMARY in HTML comment
- [ ] Philosophy statement clear and unique
- [ ] Boundaries complete (Always 4-8, Ask 2-5, Never 3-6)
- [ ] INTERACTION_TRIGGERS table + YAML templates
- [ ] Domain sections cover core functionality
- [ ] Collaboration diagram and patterns
- [ ] Journal format defined
- [ ] Daily process documented
- [ ] Tactics and avoids listed
- [ ] Activity Logging section present
- [ ] AUTORUN Support complete
- [ ] Nexus Hub Mode complete
- [ ] **Output Contract** declares default tier (S/M/L/XL) and references `_common/OUTPUT_STYLE.md`
- [ ] **Output Contract** lists task overrides if the skill has ≥2 distinct task types
- [ ] Output Language statement
- [ ] Git Guidelines reference
- [ ] Memorable closing statement
