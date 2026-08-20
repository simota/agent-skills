# Oracle Reference Index

Every `reference/` file `oracle` owns, and the condition that makes it worth
reading. `oracle/SKILL.md` keeps only the shared-contract rows and a pointer here.

**Read this when** you need a reference and the Recipe registry did not already
name it, or when scanning what this skill can consult at all.

---

| File | Read this when |
|------|----------------|
| `reference/prompt-engineering.md`                     | Designing prompts, deciding what a prompt cannot guarantee, triaging bad output by layer, structured outputs, Claude-specific behavior, or prompt tests. |
| `reference/rag-design-anti-patterns.md`         | Retrieval architecture, chunking, Hybrid Search defaults, or RAG anti-pattern checks. |
| `reference/llm-application-patterns.md`         | Choosing agent patterns, MCP design, tool-use contracts, or caching strategy. |
| `reference/ai-safety-guardrails.md`                 | OWASP LLM coverage, guardrail layers, hallucination controls, or PII handling. |
| `reference/evaluation-observability.md`         | Building eval suites, CI gates, tracing, monitoring, or rollout checks. |
| `reference/cost-optimization.md`                       | Model routing, caching, batching, effort tuning, cost monitoring, or quality-floor gating. |
| `reference/llm-production-anti-patterns.md` | Production failure modes, architecture anti-patterns, MCP pitfalls, reasoning compensations. |
| `reference/agent-design.md` | Application-level LLM agents — tool-use loops, schemas, context/memory, delegation, termination, failure modes. |
| `reference/embedding-strategy.md` | RAG embedding pipeline — chunking, model selection, vector index, re-ranking, hybrid retrieval. |
| `reference/advanced-tool-use.md` | The tool catalog is the bottleneck (`>=10` tools or `>10k` tokens of definitions, falling selection accuracy, aggregated MCP servers). Covers tool search, `defer_loading`, programmatic calling, the advisor tool. |
| `reference/human-ai-trust.md` | A human decides whether to accept the output — explanation design, over/underreliance and sycophancy metrics, the disagreement policy, verification affordances by risk class, escalation-to-human. |
| `reference/agent-behavior-contract.md` | How much role, policy, memory, relationship, and character an agent needs — necessity axes, budgets, invariant/parameter/state, spec vs prompt vs enforcement, drift. |
| `reference/autorun-schema.md` | Emitting the AUTORUN `_STEP_COMPLETE` block — Oracle-specific Output/Next schema. |
| `_common/OPUS_5_AUTHORING.md` | Sizing the design, thinking depth at DESIGN, front-loading use case/budget/tier at PROFILE. Critical: P3, P5. |
