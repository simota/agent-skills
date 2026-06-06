# Orchestration Anti-Patterns

**Purpose:** Design pitfalls and cost traps in orchestration architecture.
**Read when:** The plan may be overbuilt, bottlenecked, or using the wrong orchestration pattern.

## Contents
- 1. The Seven Core Orchestration Anti-Patterns
- 2. Pattern Selection Framework
- 3. Cost Optimization Strategy
- 4. Control-Flow Design Principles
- 5. Nexus Integration

> Common orchestration design failures: bad pattern selection, over-orchestration, bottlenecks, loop hazards, and cost-blind control flow.

## 1. The Seven Core Orchestration Anti-Patterns

| # | Anti-Pattern | Problem | Symptoms | Mitigation |
|---|-------------|---------|----------|------------|
| **OA-01** | **Premature Multi-Agent Design** | Introducing multiple agents when a single agent plus tools is enough | Hard debugging, rising cost, added latency | Optimize the single-agent path first; split only after clear limits appear |
| **OA-02** | **Over-Orchestration** | Using an AI orchestrator for deterministic workflows | Unnecessary model calls, unpredictable behavior | Use fixed pipelines for deterministic flows; reserve AI orchestration for dynamic paths |
| **OA-03** | **Orchestrator Bottleneck** | Routing every task through one overloaded coordinator without hierarchy or relief | Latency spikes, context starvation, serialized throughput | Distribute with hierarchical or peer patterns when the hub becomes a hotspot |
| **OA-04** | **Pattern Mismatch** | Applying the same orchestration pattern regardless of task characteristics | Severe performance drop on specific task classes | Match the pattern to dependency structure, quality needs, and dynamism |
| **OA-05** | **Infinite Looping** | Missing or unreachable termination conditions | Runaway cost, hangs, resource exhaustion | Define explicit exit conditions, iteration caps, and timeouts |
| **OA-06** | **Cost Blindness** | Designing chains without monitoring accumulated model cost | Billing spikes and budget overruns | Add cost monitoring, budget caps, and tiered-model usage |
| **OA-07** | **Prompting Fallacy** | Trying to fix structural coordination failures with prompt tweaks alone | Repeated failures, expanding prompts, no durable improvement | Redesign the architecture; structural problems need structural fixes |

---

## 2. Pattern Selection Framework

```
Three questions for choosing an orchestration pattern:

  Q1: Is the workflow deterministic or dynamic?
    Deterministic → Sequential / Parallel / Iterative Refinement (no AI orchestrator required)
    Dynamic       → Coordinator / Hierarchical / Swarm

  Q2: What are the task dependencies?
    Independent         → Parallel
    Strictly sequential → Sequential / Pipeline
    Interdependent      → Coordinator / Swarm

  Q3: What quality level is required?
    Standard      → Single pass
    High quality  → Review & Critique / Iterative Refinement
    Maximum       → Swarm (and maximum cost)
```

| Pattern | Best Use | Risk | Nexus Mapping |
|---------|----------|------|---------------|
| **Sequential** | Structured, repeatable processes | Accumulated latency, no skipped steps | Pattern A |
| **Parallel** | Independent work that benefits from concurrency | Resource contention, merge complexity | Pattern B |
| **Coordinator** | Adaptive routing | Routing errors, higher cost | `CHAIN_SELECT` |
| **Hierarchical** | Deep multi-stage decomposition | Context loss, hard debugging | Multi-level chains |
| **Review & Critique** | High-accuracy requirements | Reviewer bottleneck, cost accumulation | Pattern F |
| **Swarm** | Creative collaborative exploration | No consensus, extreme cost | Rally integration |
| **ReAct** | Dynamic single-agent adaptation | Error propagation, runaway reasoning loops | Single-agent internal loop |

---

## 3. Cost Optimization Strategy

```
Recommended Plan-and-Execute pattern:
  → High-capability model designs the strategy
  → Cheaper model executes routine steps
  → Often cuts cost by ~90% vs all-frontier-model execution

Cost tiering:
  Tier 1 (frontier): planning, hard reasoning, orchestration
  Tier 2 (mid): standard task execution
  Tier 3 (lightweight): routing and high-frequency decisions

  ❌ Anti-pattern: frontier models for every agent
  ❌ Anti-pattern: production deployment with no cost monitoring
  ✅ Recommended: real-time cost monitoring plus threshold alerts
```

---

## 4. Control-Flow Design Principles

```
Treat the agent system like a distributed system:
  1. Design for failure first
  2. Validate every agent boundary
  3. Constrain actions before adding agents
  4. Log intermediate state
  5. Expect retries and partial failure
  6. Model the system as distributed execution, not just chat

  ❌ Anti-pattern: designing agents as if they are only a conversation
    → The real problem is stateful distributed coordination

  ❌ Anti-pattern: optimistic execution
    → Assumes every step succeeds and leaves no recovery path

  ✅ Recommended: verification gate and fallback for each step
```

---

## 5. Nexus Integration

```
How Nexus uses this reference:
  1. Screen for OA-01 through OA-07 during CHAIN_SELECT
  2. Apply the Q1-Q3 selection framework when choosing a pattern
  3. Reflect cost optimization rules during EXECUTE
  4. Feed anti-pattern detection into CES evaluation in routing-learning.md

Quality gates:
  - Solvable by a single agent plus tools → reject multi-agent expansion (prevents OA-01)
  - Deterministic workflow → use a fixed pipeline (prevents OA-02)
  - Hub turning into a bottleneck → consider hierarchy or distribution (prevents OA-03)
  - Three failed prompt-only attempts → revisit architecture (prevents OA-07)
  - Any loop pattern → require termination condition and cap (prevents OA-05)
```

**Source:** [Google Cloud: Choose a Design Pattern for Your Agentic AI System](https://docs.cloud.google.com/architecture/choose-design-pattern-agentic-ai-system) · [Microsoft: AI Agent Orchestration Patterns](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns) · [GitHub Blog: Multi-Agent Workflows](https://github.blog/ai-and-ml/generative-ai/multi-agent-workflows-often-fail-heres-how-to-engineer-ones-that-dont/) · [StackAI: 2026 Guide to Agentic Workflow Architectures](https://www.stackai.com/blog/the-2026-guide-to-agentic-workflow-architectures)
