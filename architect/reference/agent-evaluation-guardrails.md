# Agent Evaluation & Guardrails

**Purpose:** Evaluation design, safety guardrails, and production-readiness rules for agent specifications.
**Read when:** You are validating a skill or designing quality and safety checks.

## Contents
- 1. The Six Core Evaluation Anti-Patterns
- 2. Two-Layer Evaluation Architecture
- 3. IVO (Immediately Validatable Output)
- 4. Production Readiness Checklist
- 5. Continuous Improvement Framework
- 6. Human-on-the-Loop Design
- 7. Architect Integration

## 1. The Six Core Evaluation Anti-Patterns

| # | Anti-Pattern | Problem | Symptoms | Mitigation |
|---|-------------|---------|----------|------------|
| **AE-01** | **Vibe Check** | Declaring success because the agent "kind of works" | The first real problem appears in production | Use Golden Responses, LLM-as-a-Judge, and a formal evaluation phase |
| **AE-02** | **Missing Baseline** | Never comparing against a simpler approach | A complex agent performs worse than a simple prompt | Always benchmark against the simplest viable baseline |
| **AE-03** | **Silent Confabulation** | Hallucinated claims slip through even with retrieval | Users trust and act on unsupported output | Enforce source citation and IVO output |
| **AE-04** | **Point-in-Time Validation Only** | Validating isolated steps but not the full execution trace | Systemic failures remain invisible | Analyze the complete execution trace |
| **AE-05** | **Manual Tests Only** | No automated quality verification | Testing effort grows and regressions slip through | Add CI integration and automated evaluation |
| **AE-06** | **Static Evaluation** | Initial testing happens once, with no ongoing assessment | Quality degrades silently over time | Add continuous monitoring and feedback loops |

---

## 2. Two-Layer Evaluation Architecture

```
Tier 1: Real-time guardrails (validate each step)

  Hallucination detection:
    → Detect information not grounded in provided context
    → Attach an automatic "source unknown" flag when needed

  Prompt-injection defense:
    → Detect and neutralize malicious instructions in input
    → Fall back to safe default behavior

  Dangerous-operation prevention:
    → Block destructive commands in advance
    → Require human-in-the-loop for high-risk actions

  Quality checks:
    → Verify output-format compliance
    → Check brand voice and tone consistency when relevant
    → Prevent leakage of personal or confidential information

Tier 2: Structural trace analysis (post-execution validation)

  Tool-selection errors:
    → Detect recurring wrong-tool patterns
    → Feed improvements back into tool design

  Instruction misinterpretation:
    → Identify the gap between intent and execution
    → Propose system-prompt improvements

  Memory inconsistency:
    → Detect contradictions inside the conversation or workflow
    → Improve context management

  Orchestration failures:
    → Detect inter-agent coordination failure patterns
    → Propose collaboration-architecture improvements
```

---

## 3. IVO (Immediately Validatable Output)

```
IVO = output that a user can verify at a glance

  Practical rules:

  1. Enforce source citation:
     → "This is based on [source]"
     → Flag unsupported claims

  2. Prefer structured output:
     → Use tables, lists, and code blocks for clarity
     → Avoid ambiguous narrative where verification matters

  3. Show diffs:
     → Use Before / After views for changes
     → Make the delta obvious immediately

  4. Design explicit confirmation points:
     → Ask before major decisions when risk warrants it
     → Keep the line between autonomous execution and manual confirmation clear

  Ecosystem application:
    → Run IVO checks during the `VALIDATE` phase
    → Verify that agent outputs can be checked immediately
    → Preserve handoff integrity across agent boundaries
```

---

## 4. Production Readiness Checklist

```
Production readiness for an agent design:

  □ Specification completeness:
    ✅ Role, boundaries, and collaboration patterns are explicit
    ✅ `CAPABILITIES_SUMMARY` is sufficient for routing
    ✅ Domain knowledge is documented in `reference/`

  □ Safety:
    ✅ `Always / Ask first / Never` boundaries are defined
    ✅ Stop conditions such as `max_iterations` are set when relevant
    ✅ High-risk and destructive actions use human-in-the-loop
    ✅ Fallback behavior exists for failure paths

  □ Observability:
    ✅ `Activity Logging` exists
    ✅ Journal entry criteria are clear
    ✅ Handoff success and failure can be traced

  □ Testing:
    ✅ Golden Responses are defined
    ✅ Edge-case scenarios are documented
    ✅ Baseline comparison is completed
    ✅ The `VALIDATE` phase passes

  □ Operations:
    ✅ `AUTORUN Support` exists
    ✅ Nexus Hub Mode is supported
    ✅ Reverse-feedback channels exist
    ✅ Self-improvement triggers are defined when applicable
```

---

## 5. Continuous Improvement Framework

```
Three feedback-loop levels:

  Level 1: Immediate feedback (inside one task)
    → Validation result for each step
    → Tool-usage success and failure patterns
    → In-context prompt adaptation

  Level 2: Session feedback (across tasks)
    → Record INSIGHTS in the journal
    → Detect repeated patterns
    → Update `Health Score`

  Level 3: Ecosystem feedback (system-wide)
    → Lore synthesizes shared knowledge
    → Darwin emits evolution triggers
    → Architect runs `INTROSPECT` for self-improvement

  Priority windows:
    P0 (<24h): safety failures
    P1 (<1wk): functional failures
    P2 (<2wk): quality improvements
    P3 (<1mo): optimization work

  ❌ Anti-pattern: operating without improvement
    → "If it works, don't touch it" invites silent degradation

  ✅ Recommended: measure → analyze → improve
    → Use the PDCA triggers in `review-loop.md`
    → Track `Health Score` quantitatively
```

---

## 6. Human-on-the-Loop Design

```
Balancing autonomy and oversight:

  Routine (fully autonomous):
    → Repetitive, low-risk decisions
    → Example: code search, document reading, format conversion

  Escalation (requires human confirmation):
    → Ambiguous requirements, high-risk actions, unusual situations
    → Example: file deletion, external API calls, major design decisions

  Monitor (human watches a dashboard):
    → Real-time visibility into agent activity
    → Alerts for abnormal patterns
    → Low-latency intervention channel

  ❌ Anti-pattern: all-autonomous or all-manual
    → All-autonomous raises unpredictability risk
    → All-manual destroys the value of the agent system

  ✅ Recommended: tune autonomy to task risk
    → Architect's `Ask first` layer is the control surface for this
    → Increase autonomy gradually as trust is earned
```

---

## 7. Architect Integration

```
How Architect uses this reference:
  1. Screen for AE-01 through AE-06 during `VALIDATE`
  2. Run production-readiness checks during new-agent design
  3. Apply IVO principles to output design
  4. Use `Health Score` to drive continuous improvement

Quality gates:
  - No tests defined → require Golden Responses (prevents AE-01)
  - No baseline comparison → compare against a simple method (prevents AE-02)
  - No source citation → apply IVO (prevents AE-03)
  - No Activity Logging → require observability section (prevents AE-04)
  - Incomplete `Always / Ask first / Never` → complete the three-layer boundary model
  - `Health Score < C` → create an improvement plan (prevents AE-06)
```

**Source:** [Patronus AI: AI Agent Architecture](https://www.patronus.ai/ai-agent-development/ai-agent-architecture) · [Anthropic: Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) · [Glaforge: AI Agentic Patterns and Anti-Patterns](https://glaforge.dev/talks/2025/12/02/ai-agentic-patterns-and-anti-patterns/) · [Comet: AI Agent Design Patterns](https://www.comet.com/site/blog/ai-agent-design/)
