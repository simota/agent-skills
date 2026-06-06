# Task Routing Anti-Patterns

**Purpose:** Decomposition and routing failure patterns with prevention rules.
**Read when:** The task split or routing strategy feels too shallow, too deep, or too dynamic.

## Contents
- 1. The Seven Core Routing Anti-Patterns
- 2. Granularity Design
- 3. Routing Accuracy
- 4. Discriminated Union Pattern
- 5. Context Propagation Design
- 6. Nexus Integration

> Common decomposition and routing failures: wrong granularity, role confusion, unstable dynamic delegation, and context loss across chains.

## 1. The Seven Core Routing Anti-Patterns

| # | Anti-Pattern | Problem | Symptoms | Mitigation |
|---|-------------|---------|----------|------------|
| **TR-01** | **Over-Decomposition** | Splitting simple work into unnecessary sub-tasks | Planning overhead, context loss across agents | Assess complexity first; skip decomposition for simple tasks |
| **TR-02** | **Under-Decomposition** | Throwing complex work at one agent without planning | Lower quality, more hallucination, missing work | Define complexity thresholds; decompose automatically above them |
| **TR-03** | **Role Confusion** | An agent executes work outside its intended responsibility | Wrong agent approves contracts, analysis agent performs security review | Enforce explicit role boundaries plus validation checkpoints |
| **TR-04** | **Runaway Dynamic Routing** | Letting AI choose every route dynamically | Unpredictable behavior and compounding routing errors | Keep critical operations on static mappings; reserve dynamic routing for lower-risk decisions |
| **TR-05** | **Ambiguous Delegation** | Delegation requests are too vague to constrain behavior | Non-deterministic outcomes, cross-agent inconsistency | Use action schemas to restrict the allowed actions |
| **TR-06** | **Cross-Layer Context Loss** | Context degrades at each decomposition layer | Agent C receives only ~60% of Agent A's intent | Use structured context propagation plus integrity checks at each hop |
| **TR-07** | **Fallback Routing Abuse** | Failure handlers route to unqualified agents | Critical work lands on the wrong fallback path | Ban fallback routing for critical operations; require escalation instead |

---

## 2. Granularity Design

```
Decision tree for decomposition depth:

  Task received
    ├─ Complexity assessment (low / medium / high)
    │   ├─ Low (single domain, clear procedure)
    │   │   → No decomposition; execute directly
    │   ├─ Medium (2-3 domains, standard procedure)
    │   │   → Decompose into 2-3 sub-tasks
    │   └─ High (multi-domain, non-standard)
    │       → Hierarchical decomposition plus planning phase
    └─ Post-decomposition validation
        ├─ Is each sub-task independently verifiable?
        ├─ Are dependencies explicit?
        └─ Is the merge strategy defined?

  ❌ Anti-pattern: using the same decomposition depth for every task
  ❌ Anti-pattern: decomposing before defining the merge strategy
  ✅ Recommended: adapt granularity to complexity
```

---

## 3. Routing Accuracy

```
Treat the specification like an API contract:
  → Spec ambiguity is a root cause in 41.77% of observed failures
  → Replace narrative-only instructions with machine-checkable constraints where possible
  → Encode role, capability, constraint, and success criteria explicitly

Role-boundary enforcement:
  1. Put explicit role boundaries and limits into every delegation
  2. Prefer static task mappings over unconstrained dynamic routing
  3. Verify that each agent is handling only valid work
  4. Ban fallback routing for critical operations such as approvals or payments
  5. Monitor ownership and alert on violations

Routing confidence and action:
  HIGH (≥0.85)       → Auto-route
  MEDIUM (0.70-0.84) → Route and show rationale
  LOW (0.50-0.69)    → Present multiple candidates
  VERY_LOW (<0.50)   → Escalate to a human
```

---

## 4. Discriminated Union Pattern

```
Designing an action schema to prevent ambiguous delegation:

  ❌ Bad example:
    Instruction: "Analyze this issue and handle it appropriately"
    → Agent A closes it
    → Agent B assigns it
    → Agent C escalates it
    → Non-deterministic and unsuitable for automation

  ✅ Good example (Discriminated Union):
    action:
      type: "close_issue" | "assign_to" | "escalate" | "add_label"
    → The agent must return exactly one predefined action
    → Behavior becomes predictable, auditable, and testable

  Application rules:
    1. Enumerate allowed actions for each step
    2. Define required parameters per action
    3. Block undefined actions
    4. Log the rationale for the selected action
```

---

## 5. Context Propagation Design

```
Preventing context loss:

  Quantifying the problem:
    → A 3-agent chain can degrade the original intent to ~60%
    → Token truncation can silently drop critical details
    → In some 8,000-token windows, as much as 40% of context is lost

  Structured propagation:
    1. Define required fields (goal, constraints, success criteria)
    2. Run integrity checks at every handoff
    3. Pass structured data, not narrative summaries alone
    4. Manage the context window with selective memory

  ❌ Anti-pattern: passing the entire conversation history to the next agent
    → Explodes token cost and diffuses attention

  ✅ Recommended: structured handoff templates
    → Goal + completed work + open issues + constraints
```

---

## 6. Nexus Integration

```
How Nexus uses this reference:
  1. Screen for TR-01 and TR-02 during CLASSIFY
  2. Prevent TR-03 and TR-04 during CHAIN_SELECT
  3. Monitor TR-06 during EXECUTE
  4. Use agent-disambiguation.md to prevent role confusion
  5. Use handoff-validation.md to prevent context loss

Quality gates:
  - Low-complexity task → skip decomposition (prevents TR-01)
  - High-complexity task → planning phase is mandatory (prevents TR-02)
  - Agent choice → validate role boundaries first (prevents TR-03)
  - Critical operation → enforce static mapping (prevents TR-04)
  - Delegation schema → require discriminated union form (prevents TR-05)
  - Multi-hop chain → run context integrity checks at each hop (prevents TR-06)
  - Critical fallback → escalate instead of rerouting blindly (prevents TR-07)
```

**Source:** [Augment Code: Why Multi-Agent LLM Systems Fail](https://www.augmentcode.com/guides/why-multi-agent-llm-systems-fail-and-how-to-fix-them) · [GitHub Blog: Multi-Agent Workflows](https://github.blog/ai-and-ml/generative-ai/multi-agent-workflows-often-fail-heres-how-to-engineer-ones-that-dont/) · [TechAhead: Multi-Agent Reality Check](https://www.techaheadcorp.com/blog/ways-multi-agent-ai-fails-in-production/) · [Google Cloud: Choose a Design Pattern](https://docs.cloud.google.com/architecture/choose-design-pattern-agentic-ai-system)
