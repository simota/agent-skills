# Multi-Agent System Design Anti-Patterns

**Purpose:** Collaboration-topology pitfalls and coordination-tax guidance.
**Read when:** The design may be over-orchestrated or using the wrong multi-agent pattern.

## Contents
- 1. The Seven Core Multi-Agent Anti-Patterns
- 2. Collaboration Pattern Selection
- 3. Coordination Tax
- 4. Architect Integration

## 1. The Seven Core Multi-Agent Anti-Patterns

| # | Anti-Pattern | Problem | Symptoms | Mitigation |
|---|-------------|---------|----------|------------|
| **MA-01** | **Premature Multi-Agent Design** | A multi-agent system is introduced when a single agent is enough | Hard debugging, exploding cost, higher latency | Optimize the single-agent-plus-tools path first |
| **MA-02** | **Prompting Fallacy** | System-level coordination failures are treated like prompt-only problems | The same failure repeats while the prompt grows | Revisit the architecture itself |
| **MA-03** | **Supervisor Bottleneck** | Every task routes through one orchestrator | Latency spikes and context-window exhaustion | Use hierarchical or peer patterns where appropriate |
| **MA-04** | **Scaling Illusion** | More agents are assumed to improve performance linearly | Performance plateaus or declines while coordination overhead grows | Design with coordination tax in mind |
| **MA-05** | **Topology Mismatch** | The same architecture is applied to every task | Some task classes perform much worse | Match topology to task characteristics |
| **MA-06** | **Infinite Bounce Loop** | Tasks bounce forever between agents | Cost burns without resolution and debugging becomes impossible | Require iteration caps, timeouts, and termination conditions |
| **MA-07** | **Context Accumulation** | Stateful patterns grow token usage without bound | Token-budget overflow and degraded quality | Use summarization, selective memory, and window management |

---

## 2. Collaboration Pattern Selection

| Pattern | Best Use | Risk | Architect Ecosystem Mapping |
|---------|----------|------|-----------------------------|
| **Supervisor-based (serial)** | Ordered reasoning, compliance checks | Cognitive bottleneck, latency | Nexus hub-and-spoke |
| **Blackboard (shared memory)** | Creative work, iterative refinement | External storage needs, coordination overhead | Shared `PROJECT.md` and journal |
| **Peer-to-peer** | Exploration, discovery, navigation | Fragmentation and unverified loops | Direct agent-to-agent handoff risk |
| **Swarm** | Large parallel search | Token burn, drift, output sprawl | Rally-style parallel execution |
| **Hybrid** | Fast parallel work with periodic aggregation | Design complexity | Nexus plus specialist agents |

```
Three design questions to ask before selecting a pattern:

  Q1: Organization — what information flow fits the task?
    → Sequential → Supervisor / Handoffs
    → Parallel   → Subagents / Router
    → Iterative  → Blackboard / Evaluator-Optimizer

  Q2: Hiring — which model or agent type fits each role?
    → Generation and planning → decoder-style reasoning model
    → Analysis and verification → evaluation-oriented model or agent
    → Logic-heavy reasoning → dedicated reasoning-capable model

  Q3: Scaling risk — how will the design fail as complexity grows?
    → Nonlinear coordination tax
    → Context-window exhaustion
    → Error amplification across stages
```

---

## 3. Coordination Tax

```
Hidden costs of multi-agent systems:

  Communication cost:
    - Message passing between agents
    - Token spend for shared context
    - Information loss during handoff

  Latency:
    - Serial execution accumulates response times
    - Parallel execution is bottlenecked by the slowest branch
    - Aggregation adds merge overhead

  Debugging complexity:
    - Requires analysis of 10-50+ LLM calls
    - Causal tracing is harder
    - Non-determinism reduces reproducibility

  Quality risk:
    - Compounding errors
    - Hallucination injected in intermediate stages
    - Blurred task boundaries

Decision rule:
  ✅ Multi-agent is justified when:
    - Clearly different domain expertise is required
    - Multiple conversation contexts must be maintained
    - The tool surface no longer fits one prompt responsibly

  ❌ Multi-agent is excessive when:
    - A single agent plus tools can solve the task
    - Reproducibility and predictability matter most
    - Cost and latency budgets are tight
```

---

## 4. Architect Integration

```
How Architect uses this reference:
  1. Ask the three pattern-selection questions during `ANALYZE`
  2. Screen for MA-01 through MA-07 when proposing new agents
  3. Estimate coordination tax before expanding the ecosystem
  4. Validate topology fit when designing Nexus routing

Quality gates:
  - Solvable by one agent → reject multi-agent expansion (prevents MA-01)
  - `3+` failed prompt-only iterations → revisit architecture (prevents MA-02)
  - Every route passes through one hub → consider hierarchy or distribution (prevents MA-03)
  - More agents reduce performance → reassess coordination tax (prevents MA-04)
  - No termination condition → require iteration cap (prevents MA-06)
  - Stateful design without context strategy → require memory management plan (prevents MA-07)
```

**Source:** [Anthropic: Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) · [O'Reilly: Designing Effective Multi-Agent Architectures](https://www.oreilly.com/radar/designing-effective-multi-agent-architectures/) · [LangChain: Choosing the Right Multi-Agent Architecture](https://blog.langchain.com/choosing-the-right-multi-agent-architecture/)
