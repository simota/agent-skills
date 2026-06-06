# Agent Specification Anti-Patterns

**Purpose:** Prompt, tool, boundary, and role-definition pitfalls for agent specs.
**Read when:** A proposed skill looks vague, overloaded, unsafe, or poorly tooled.

## Contents
- 1. The Eight Core Specification Anti-Patterns
- 2. System Prompt Design Best Practices
- 3. Tool Design Principles
- 4. Role-Definition Patterns
- 5. Separating Planning and Execution
- 6. Architect Integration

## 1. The Eight Core Specification Anti-Patterns

| # | Anti-Pattern | Problem | Symptoms | Mitigation |
|---|-------------|---------|----------|------------|
| **AS-01** | **Task Overload** | One agent is packed with too many unrelated tasks | More hallucination, missed work, lower quality | Keep one agent focused on one responsibility; split when responsibilities multiply |
| **AS-02** | **Ambiguous Instructions** | Instructions leave too much room for interpretation | Output variance and unintended behavior | Use explicit instructions and clear constraints |
| **AS-03** | **Missing Safety Controls** | Autonomous behavior has no guardrails or stop conditions | Cascading errors and runaway execution | Add validation at each step and explicit stop conditions such as `max_iterations` |
| **AS-04** | **Under-Documented Tools** | Tool names, descriptions, or parameters are incomplete | Wrong tool selection and semantic mismatch | Document tools with examples, constraints, and edge cases |
| **AS-05** | **Raw API Exposure** | REST APIs are exposed directly as tools | The model cannot reason naturally about raw API structure | Design business-task-oriented tools instead |
| **AS-06** | **Verbose Prompting** | The prompt is overloaded with 2000+ words of detail | Slower execution, diffused attention, worse compliance | Keep only essential instructions inline and move detail to `reference/` |
| **AS-07** | **Missing Context** | The model is expected to infer background knowledge | Wrong assumptions and domain errors | Provide all required context explicitly |
| **AS-08** | **Static Prompt Lock-In** | The first prompt is kept forever without a feedback loop | The same mistakes repeat and improvement stalls | Use iterative improvement and feed back observed failure patterns |

---

## 2. System Prompt Design Best Practices

```
Structure of an effective system prompt:

  1. Role definition:
     ✅ "You are Architect - the creative meta-designer who..."
     ❌ "You are a helpful assistant"
     → Define persona, specialty, and differentiation clearly

  2. Knowledge base:
     ✅ Provide domain-specific knowledge in structured form
     ❌ Rely on model pretraining alone
     → Use `reference/`, retrieval, and context injection deliberately

  3. Response guidelines:
     ✅ Make format, tone, and constraints explicit
     ❌ "Please answer appropriately"
     → State output structure, prohibitions, and quality bars concretely

  4. Task definition:
     ✅ Define staged workflow
     ❌ "Complete the task"
     → Separate phases, checkpoints, and success criteria

  5. Constraints:
     ✅ Use `Always / Ask first / Never`
     ❌ No constraints or excessive constraints
     → Balance autonomy and safety

  Ma layout usage:
    - Primacy (first 15%): role and principles
    - Recency (last 15%): memorable operating guidance
    - Middle Sag (middle 70%): use structure to offset attention drop
```

---

## 3. Tool Design Principles

```
ACI (Agent-Computer Interface) excellence:

  1. Clarity:
     → Think from the model's point of view
     → Make the tool instantly understandable
     → Include examples, edge cases, and scope

  2. Format choice:
     → Prefer formats the model naturally recognizes
     → Leave enough token budget for reasoning
     → Eliminate friction such as manual line counting or awkward escaping

  3. Poka-yoke:
     → Make mistakes harder through argument design
     → Remove ambiguous parameter names
     → Use safe, helpful defaults

  4. Iterative testing:
     → Test with many input examples
     → Observe actual model failure patterns
     → Improve the tool contract from those failures

Tool-design anti-patterns:

  ❌ Similar-name tools:
    `schedule_meeting` and `create_meeting` coexist
    → Semantic confusion

  ❌ Too many tools:
    50+ tools attached to one agent
    → Worse tool selection and more unintended calls
    → Prefer 10-15 tools or staged loading

  ❌ Unvalidated tool output:
    Tool results feed directly into later steps
    → Invalid data propagates and cascades
    → Validate tool outputs before reuse
```

---

## 4. Role-Definition Patterns

```
Elements of an effective role definition:

  1. Identity:
     → Name plus metaphor
     → 3-5 memorable principles
     → Clear differentiation from other agents

  2. Boundaries:
     Best pattern: three-layer boundary model
     - Always: autonomous obligations
     - Ask first: confirmation points
     - Never: forbidden behavior

  3. Visibility of capabilities:
     → `CAPABILITIES_SUMMARY`: routing-facing surface
     → `reference/`: internal detail
     → Do not pack everything into `SKILL.md`

  4. Collaboration pattern:
     → Explicit INPUT / OUTPUT partners
     → Defined handoff templates
     → Reverse-feedback path preserved

Role-definition anti-patterns:

  ❌ God Agent:
    One agent owns every responsibility
    → Weak specialization, low quality, poor scalability

  ❌ Phantom Agent:
    Defined but never used
    → Ecosystem bloat and maintenance drag

  ❌ Clone Agent:
    `30%+` overlap with an existing agent
    → Routing ambiguity and confusion

  ❌ Orphan Agent:
    INPUT / OUTPUT partners are undefined
    → Isolation from the ecosystem and low reuse
```

---

## 5. Separating Planning and Execution

```
Recommended dual-mode architecture:

  Plan mode:
    - Gather context
    - Clarify requirements
    - Design the approach
    - Confirm with the user when required
    → Read-only tools only

  Act mode:
    - Execute step by step
    - Verify after each step
    - Adapt when problems occur
    → Full tool access as needed

  ❌ Anti-pattern: execution without planning
    → Wrong assumptions surface late and create costly rework

  ❌ Anti-pattern: excessive planning
    → Trying to predict everything before execution
    → Analysis paralysis

  ✅ Recommended cycle:
    plan → approval when needed → execute → verify
    → Architect maps this to `UNDERSTAND → ENVISION → ANALYZE → DESIGN → GENERATE → VALIDATE`
```

---

## 6. Architect Integration

```
How Architect uses this reference:
  1. Screen for AS-01 through AS-08 during `DESIGN`
  2. Validate system-prompt structure during skill generation
  3. Apply ACI principles when the agent includes tools
  4. Check for God / Phantom / Clone / Orphan patterns in role design

Quality gates:
  - `3+` major capabilities → consider splitting (prevents AS-01)
  - Missing `Always / Ask first / Never` → require three-layer boundaries (prevents AS-03)
  - No `reference/` → move detail out of `SKILL.md` (prevents AS-06)
  - No INPUT / OUTPUT partners → require collaboration pattern (prevents Orphan)
  - `30%+` overlap → differentiate or merge (prevents Clone)
  - No observed usage → consider removal (prevents Phantom)
```

**Source:** [Anthropic: Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) · [PromptHub: Prompt Engineering for AI Agents](https://www.prompthub.us/blog/prompt-engineering-for-ai-agents) · [Patronus AI: AI Agent Architecture](https://www.patronus.ai/ai-agent-development/ai-agent-architecture) · [Glaforge: AI Agentic Patterns and Anti-Patterns](https://glaforge.dev/talks/2025/12/02/ai-agentic-patterns-and-anti-patterns/)
