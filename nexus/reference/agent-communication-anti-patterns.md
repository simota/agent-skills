# Agent Communication Anti-Patterns

**Purpose:** Communication failure patterns and schema-first handoff guidance.
**Read when:** Handoffs, message structure, ownership, or state integrity look weak.

## Contents
- 1. The Seven Core Communication Anti-Patterns
- 2. Structured Communication Protocol Design
- 3. Handoff Design Best Practices
- 4. State Management Patterns
- 5. Eighteen Fine-Grained Failure Modes
- 6. Nexus Integration

> Common communication failures between agents: unstructured messaging, handoff collapse, hidden state assumptions, and drifting interfaces.

## 1. The Seven Core Communication Anti-Patterns

| # | Anti-Pattern | Problem | Symptoms | Mitigation |
|---|-------------|---------|----------|------------|
| **AC-01** | **Unstructured Messaging** | Agents communicate with natural language or free-form JSON | Field drift, type mismatch, format inconsistency | Enforce typed schemas as foundational contracts |
| **AC-02** | **Implicit State Assumptions** | Agents rely on undocumented assumptions about state or execution order | One agent closes work opened by another with no explicit ownership | Track state explicitly and validate it at each handoff |
| **AC-03** | **Missing Message Types** | No distinction between `request`, `inform`, `commit`, and `reject` | Agents explore multiple interpretations and respond ambiguously | Use a structured protocol such as JSON-RPC 2.0 with enforced message types |
| **AC-04** | **Context Bloat** | Full conversation history is forwarded to the next agent | Exploding token cost, diffused attention, slower execution | Use structured handoffs carrying only required information |
| **AC-05** | **Interface Drift** | Schemas and action constraints exist only as convention | Agents gradually cross boundaries and drift over time | Enforce input and output schemas at tool boundaries via MCP or equivalent |
| **AC-06** | **No Resource Ownership** | Ownership of DB tables, APIs, or files is undefined | Multiple agents race on the same resource | Assign a single owner per resource plus access control |
| **AC-07** | **Handoff Information Loss** | Important context degrades at each transfer | After three agents, only ~60% of original intent remains | Add handoff integrity checks and structured templates |

---

## 2. Structured Communication Protocol Design

```
Three-layer architecture for agent communication:

  Layer 1: Message schema
    → Apply typed schemas to every message
    → Treat schema violations as system failures
    → Handle with retry → repair → escalation

  Layer 2: Message-type enforcement
    → request: ask for work
    → inform : share information
    → commit : finalize a result
    → reject : refuse work with a reason
    → Define required fields per message type

  Layer 3: Action constraints (Discriminated Union)
    → Restrict the allowed actions for each agent
    → Block execution of undefined actions
    → Log the rationale for the selected action

  ❌ Anti-pattern: passing raw natural-language messages directly
    → High interpretation variance and zero type safety

  ✅ Recommended: schema enforcement + typed messages + action constraints
```

---

## 3. Handoff Design Best Practices

```
Five elements of an effective handoff:

  1. Task context:
     → Original user request (preserve the original wording)
     → Summary of completed steps
     → Current task state

  2. Decision rationale:
     → Why this agent is the next handoff target
     → Why the previous agent made its decision
     → Alternatives considered and rejected

  3. Success criteria:
     → Expected output of the next agent
     → Quality bars and constraints
     → Timeout and retry policy

  4. State information:
     → List of changed resources
     → References to intermediate artifacts
     → Error history, if any

  5. Confidence information:
     → Self-assessed task completion level
     → Self-assessed output quality
     → Clarity of the next step

  Validation rules:
    → Missing required field → reject the handoff
    → Confidence below threshold → escalate
    → Undefined success criteria → request completion before continuing
```

---

## 4. State Management Patterns

```
Managing state in an agent system:

  State persistence (foundation for recovery):
    → Without persisted intermediate state, rollback is impossible
    → Persisted state + idempotent operations = minimal-damage recovery

  Ownership model:
    → Assign one owner for each resource (DB table, API, file)
    → Define the ownership map explicitly
    → Non-owners default to read-only access

  Distributed-state consistency:
    → Each agent sees only part of the global state
    → Add a mechanism to detect inconsistency
    → Use a conflict-resolution protocol

  ❌ Anti-pattern: implicit shared state
    → Multiple agents update the same file concurrently
    → Overwrites occur without conflict detection

  ❌ Anti-pattern: stateless chains
    → No intermediate state is saved; the next agent becomes the only memory
    → Failures force a restart from the beginning

  ✅ Recommended: checkpoints + idempotent operations + ownership model
```

---

## 5. Eighteen Fine-Grained Failure Modes

```
Four categories of fine-grained failure modes:

  Category 1: Specification ambiguity and inconsistency
    → Ambiguous role definitions
    → Undefined success criteria
    → Implicit constraints
    → Contradictory instructions

  Category 2: Organizational collapse
    → Unclear hierarchy
    → Overlapping authority
    → Undefined escalation paths
    → Responsibility ping-pong

  Category 3: Inter-agent communication failures
    → Message-format mismatch
    → Context drop
    → Action based on misunderstanding
    → Misaligned expectations

  Category 4: Coordination failures
    → Deadlock (mutual waiting)
    → Race condition (simultaneous updates)
    → Cascading failure
    → No consensus / termination not reached

  Priority:
    Specification + coordination drive ~79% of failures → fix first
```

---

## 6. Nexus Integration

```
How Nexus uses this reference:
  1. Use handoff-validation.md to prevent AC-01 and AC-07
  2. Use conflict-resolution.md to resolve AC-06 resource conflicts
  3. Use output-formats.md to prevent AC-03 and AC-05 drift
  4. Run context integrity checks throughout execution phases

Quality gates:
  - Natural-language handoff only → require schema (prevents AC-01)
  - Hidden state assumptions → require explicit state tracking (prevents AC-02)
  - Missing message type → require structured protocol (prevents AC-03)
  - Full conversation transfer → convert to structured handoff (prevents AC-04)
  - Schema not enforced → add boundary validation (prevents AC-05)
  - Undefined ownership → require ownership mapping (prevents AC-06)
  - No handoff validation → add integrity checks (prevents AC-07)
```

**Source:** [GitHub Blog: Multi-Agent Workflows](https://github.blog/ai-and-ml/generative-ai/multi-agent-workflows-often-fail-heres-how-to-engineer-ones-that-dont/) · [Augment Code: Why Multi-Agent LLM Systems Fail](https://www.augmentcode.com/guides/why-multi-agent-llm-systems-fail-and-how-to-fix-them) · [OpenReview: Why Do Multiagent Systems Fail?](https://openreview.net/forum?id=wM521FqPvI) · [Codebridge: Multi-Agent Systems & AI Orchestration Guide](https://www.codebridge.tech/articles/mastering-multi-agent-orchestration-coordination-is-the-new-scale-frontier)
