# Oracle Recipe Registry

The full Recipe table for `oracle`. `oracle/SKILL.md` carries only the dispatch
allowlist; this file holds what is needed to *execute* a Recipe — activation
condition and the files to read first.

**Read this when** a subcommand matched and you need its row, or when scanning
what Recipes exist at all.

---

| Recipe | Subcommand | Default? | When to Use | Read First |
|--------|-----------|---------|-------------|------------|
| Prompt Engineering | `prompt` | ✓ | Prompt design and optimization | `reference/prompt-engineering.md` |
| RAG Design | `rag` | | RAG design (retrieval + generation) | `reference/rag-design-anti-patterns.md` |
| AI Safety | `safety` | | Guardrails, red-teaming | `reference/ai-safety-guardrails.md` |
| MLOps Pipeline | `mlops` | | MLOps pipeline design | `reference/llm-application-patterns.md` |
| Agent System Design | `agent` | | Application-level LLM agent design (tool-use loops, tool schemas, memory, subagent delegation, termination) | `reference/agent-design.md` |
| LLM Cost Optimization | `cost` | | LLM-API cost tuning (token budget, prompt caching, model tier routing, batch vs streaming, context compression) | `reference/cost-optimization.md` |
| Embedding Strategy | `embed` | | RAG embedding pipeline deep dive (chunking, embedding model, vector index, re-ranking, hybrid BM25+vector) | `reference/embedding-strategy.md` |
| AI Architecture Review | `review` | | Reviewing a design that embeds AI before build or before raising its authority: 12 lenses, risk tiers R0–R3, conditional approval, re-review triggers | `reference/architecture-review.md` |
| Advanced Tool Use | `tooling` | | Scaling an Anthropic-API tool catalog: tool search + `defer_loading`, programmatic tool calling, advisor tool (server-side Plan-and-Execute), per-tool/per-version model support | `reference/advanced-tool-use.md` |
