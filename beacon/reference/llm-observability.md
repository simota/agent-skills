# LLM / AI Observability

> GenAI semantic conventions, agentic tracing, token cost tracking, prompt quality metrics, Grafana dashboard design, GenAI observability checklist

---

## 1. GenAI Semantic Conventions (OTel)

OpenTelemetry defines standardized attribute names for AI/LLM telemetry under the `gen_ai.*` namespace (Semantic Conventions v1.40+).

### Key Span Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `gen_ai.system` | string | Provider name (e.g., `openai`, `anthropic`, `vertex_ai`) |
| `gen_ai.operation.name` | string | Operation type (`chat`, `text_completion`, `embeddings`) |
| `gen_ai.request.model` | string | Requested model ID (e.g., `gpt-4o`, `claude-opus-4-6`) |
| `gen_ai.response.model` | string | Model actually used in response |
| `gen_ai.usage.input_tokens` | int | Number of input/prompt tokens consumed |
| `gen_ai.usage.output_tokens` | int | Number of output/completion tokens generated |
| `gen_ai.usage.total_tokens` | int | Total tokens (input + output) |
| `gen_ai.request.temperature` | double | Sampling temperature |
| `gen_ai.request.max_tokens` | int | Token limit set in request |
| `gen_ai.response.finish_reason` | string | Completion reason (`stop`, `length`, `tool_calls`, `content_filter`) |
| `gen_ai.response.id` | string | Response identifier from provider |

### Key Metrics

| Metric | Unit | Description |
|--------|------|-------------|
| `gen_ai.client.token.usage` | `{token}` | Histogram of token usage per request (split by `token.type`) |
| `gen_ai.client.operation.duration` | `s` | Histogram of LLM call duration |
| `gen_ai.server.request.duration` | `s` | Server-side request duration (for self-hosted models) |
| `gen_ai.server.time_to_first_token` | `s` | Time from request to first token in streaming response |

### Attribute Cardinality Warning

Do NOT include prompt content or response content as span attributes — they are high-cardinality and may contain PII. Use span events instead for optional, sampled capture.

```python
# Correct: use span events for prompt content (opt-in, sampled)
span.add_event("gen_ai.content.prompt", {"gen_ai.prompt": prompt_text})
span.add_event("gen_ai.content.completion", {"gen_ai.completion": response_text})
```

---

## 2. Agentic Systems — Multi-Agent Tracing

### Span Chain Design

For multi-agent or tool-calling workflows, each agent invocation and tool call should be a child span.

```
Trace: user-request-abc123
├── Span: orchestrator.plan          [gen_ai.operation.name=chat]
│   ├── gen_ai.usage.input_tokens=450
│   └── gen_ai.usage.output_tokens=120
├── Span: tool.web_search            [kind=CLIENT]
│   └── duration=320ms
├── Span: agent.researcher.execute   [gen_ai.operation.name=chat]
│   ├── gen_ai.usage.input_tokens=1200
│   └── gen_ai.usage.output_tokens=380
└── Span: agent.builder.execute      [gen_ai.operation.name=chat]
    ├── gen_ai.usage.input_tokens=890
    └── gen_ai.usage.output_tokens=640
```

### Key Tracing Attributes for Agents

| Attribute | Description |
|-----------|-------------|
| `gen_ai.agent.name` | Agent identifier (e.g., `researcher`, `builder`) |
| `gen_ai.tool.name` | Tool name when invoking external tools |
| `gen_ai.tool.call.id` | Tool call identifier for correlation |
| `thread.id` | Session or conversation thread identifier |

### Context Propagation

Always propagate W3C TraceContext (`traceparent`, `tracestate`) headers when calling downstream agents or APIs. This ensures the full multi-agent workflow is visible as a single trace.

---

## 3. Token Cost Calculation Patterns

### Basic Formula

```
cost = (input_tokens / 1000) × input_price_per_1k
      + (output_tokens / 1000) × output_price_per_1k
```

### Provider Unit Price Reference (approximate, check current pricing)

| Provider | Model | Input $/1K tokens | Output $/1K tokens |
|----------|-------|-------------------|---------------------|
| Anthropic | claude-opus-4-6 | $0.015 | $0.075 |
| Anthropic | claude-sonnet-4-6 | $0.003 | $0.015 |
| Anthropic | claude-haiku-4-5 | $0.00025 | $0.00125 |
| OpenAI | gpt-4o | $0.0025 | $0.010 |
| OpenAI | gpt-4o-mini | $0.00015 | $0.0006 |
| Google | gemini-2.0-flash | $0.0001 | $0.0004 |

> Note: Prices change frequently. Always verify from official provider documentation.

### OTel Cost Metric

Derive cost as a computed metric in the collector or Grafana:

```yaml
# Prometheus recording rule example
- record: llm_request_cost_usd
  expr: |
    (
      gen_ai_client_token_usage_total{token_type="input", gen_ai_system="anthropic", gen_ai_request_model="claude-sonnet-4-6"}
      * 0.000003
    ) + (
      gen_ai_client_token_usage_total{token_type="output", gen_ai_system="anthropic", gen_ai_request_model="claude-sonnet-4-6"}
      * 0.000015
    )
```

### Budget Alert Pattern

```yaml
# Alert when daily LLM cost exceeds $50
- alert: LLMDailyCostBudgetExceeded
  expr: |
    increase(llm_request_cost_usd[24h]) > 50
  for: 5m
  labels:
    severity: warning
  annotations:
    summary: "LLM daily cost budget exceeded"
    runbook: "https://runbooks.internal/llm-cost-alert"
```

---

## 4. Prompt Quality Metrics

### Key Metrics to Track

| Metric | Description | Collection Method |
|--------|-------------|-------------------|
| **Hallucination rate** | Proportion of responses containing factual errors | LLM-as-judge evaluation pipeline |
| **Relevance score** | How relevant the response is to the input intent | Embedding cosine similarity or LLM scoring |
| **Faithfulness** | Whether the response is grounded in provided context (RAG) | RAG evaluation framework (RAGAS, DeepEval) |
| **Latency P50/P95/P99** | Response time distribution | `gen_ai.client.operation.duration` histogram |
| **Refusal rate** | Proportion of requests refused by content filter | `gen_ai.response.finish_reason=content_filter` |
| **Tool call success rate** | Success ratio of agent tool invocations | Custom span attribute + error flag |
| **Retry rate** | How often LLM calls are retried due to errors | Custom counter |

### LLM-as-Judge Evaluation Pattern

```python
# Async evaluation pipeline — do not block production path
async def evaluate_response_quality(
    input: str,
    response: str,
    trace_id: str,
) -> None:
    score = await judge_llm.evaluate(
        criteria=["relevance", "accuracy", "completeness"],
        input=input,
        response=response,
    )
    # Push to metrics backend
    metrics.histogram("llm.quality.relevance", score.relevance, tags={"trace_id": trace_id})
    metrics.histogram("llm.quality.accuracy", score.accuracy, tags={"trace_id": trace_id})
```

---

## 5. Grafana Dashboard Design for LLM

### Panel Layout

```
Row 1: Overview
  ├── Total requests/min (stat)
  ├── P95 latency (stat)
  ├── Error rate % (stat)
  └── Estimated cost today (stat + trend)

Row 2: Token Usage
  ├── Input tokens/min by model (time series)
  ├── Output tokens/min by model (time series)
  └── Token ratio (output/input) — indicates verbosity (gauge)

Row 3: Quality & Reliability
  ├── Finish reasons distribution (pie chart)
  ├── Refusal rate trend (time series)
  └── Tool call success rate by tool (bar chart)

Row 4: Cost Analysis
  ├── Cost by model (time series stacked)
  ├── Cost by user/tenant (table, top 10)
  └── Projected monthly cost (stat + budget threshold line)

Row 5: Traces
  └── Tempo trace explorer link filtered by gen_ai.system
```

### Key Grafana Variables

```yaml
variables:
  - name: gen_ai_system
    query: label_values(gen_ai_client_token_usage_total, gen_ai_system)
  - name: model
    query: label_values(gen_ai_client_token_usage_total{gen_ai_system="$gen_ai_system"}, gen_ai_request_model)
  - name: environment
    query: label_values(gen_ai_client_token_usage_total, environment)
```

---

## 6. GenAI Observability Checklist

### Instrumentation

- [ ] OTel SDK initialized before any LLM client import
- [ ] `gen_ai.*` semantic conventions applied to all LLM calls
- [ ] W3C TraceContext propagated to downstream agents
- [ ] Token usage (`input_tokens`, `output_tokens`) recorded per request
- [ ] Finish reason captured on all responses
- [ ] Error spans recorded with `error.type` for 4xx/5xx/timeout

### Metrics & Alerting

- [ ] `gen_ai.client.operation.duration` histogram with P50/P95/P99 SLOs defined
- [ ] `gen_ai.client.token.usage` tracked by model and token type
- [ ] Cost metric derived and dashboarded
- [ ] Daily/monthly cost budget alert configured
- [ ] High error rate alert (`> 5%` for 5 minutes)
- [ ] High latency alert (P95 > SLO threshold)

### Privacy & Security

- [ ] Prompt/completion content NOT stored as span attributes in production
- [ ] PII/PHI redacted before any telemetry export
- [ ] Content logging is opt-in and subject to data retention policy
- [ ] API keys never appear in telemetry

### Cost Optimization

- [ ] Model selection reviewed: use smaller model for simple tasks
- [ ] Prompt length monitored and optimized (track input token trend)
- [ ] Caching strategy evaluated for repeated queries
- [ ] Token budget set per user/tenant if multi-tenant

---

**Source:** [OTel GenAI Semantic Conventions](https://opentelemetry.io/docs/specs/semconv/gen-ai/) · [OTel AI Agent Observability](https://opentelemetry.io/blog/2025/ai-agent-observability/) · [Grafana LLM Observability](https://grafana.com/docs/grafana-cloud/monitor-applications/llm-observability/)
