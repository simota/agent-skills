# Advanced Tool Use (Anthropic API)

> Source: platform.claude.com — Tool reference, Tool search tool, Advisor tool, Programmatic tool calling, Web search / Web fetch tool. Verified **2026-07-25**.
> Scope: **API-layer** server/client tools. These are *not* the same as a CLI harness's own tools (Claude Code's `WebSearch`/`WebFetch` are harness-executed and follow different rules).

Four mechanisms cut context and round trips as a tool catalog grows. They compose: tool search decides *what enters context*, programmatic tool calling decides *how tools are invoked*, tool-use examples decide *whether the call is correct*, and the advisor decides *which model does the thinking*.

**Adopt them one at a time, starting from your measured bottleneck** — Anthropic's own guidance is explicitly against implementing all of them at once. Diagnose first: definitions dominating the prompt → §2; round trips and payload size → §3; malformed arguments → §3.5; a cheap model that plans badly → §4.

---

## 1. Tool inventory

| Tool | `type` | Execution | Status |
|------|--------|-----------|--------|
| Web search | `web_search_20260318` · `_20260209` · `_20250305` | Server | GA |
| Web fetch | `web_fetch_20260318` · `_20260309` · `_20260209` · `_20250910` | Server | GA |
| Code execution | `code_execution_20260521` · `_20260120` · `_20250825` | Server | GA |
| Advisor | `advisor_20260301` | Server | Beta `advisor-tool-2026-03-01` |
| Tool search | `tool_search_tool_regex_20251119` · `tool_search_tool_bm25_20251119` | Server | GA |
| MCP connector | `mcp_toolset` | Server | Beta `mcp-client-2025-11-20` |
| Memory | `memory_20250818` | Client | GA |
| Bash | `bash_20250124` | Client | GA |
| Text editor | `text_editor_20250728` (Claude 4+) · `_20250124` (earlier) | Client | GA |
| Computer use | `computer_20251124` · `computer_20250124` | Client | Beta |

**Versioning is not a linear upgrade path.** Four distinct relationships exist, and picking the highest number is not always right:

- **Capability-keyed** — both versions are current; choose by whether you need the capability. `web_search_20260209` / `web_fetch_20260209` add dynamic filtering; `web_fetch_20260309` adds cache bypass; the `_20260318` pair adds response-inclusion control; `code_execution_20260120` adds programmatic tool calling.
- **Model-keyed** — `text_editor_20250728` for Claude 4 and later, `_20250124` for earlier.
- **Variant, not version** — `tool_search_tool_regex` and `_bm25` shipped together; neither supersedes the other.
- **Legacy** — `code_execution_20250522` is Python-only; `_20250825` adds Bash and file operations.

`mcp_toolset` carries no date suffix — its versioning lives in the `anthropic-beta` header.

### Model-support gotchas

Support varies **per tool and per tool version** — never infer it from a model's general capability.

| Gotcha | Detail |
|--------|--------|
| `web_fetch` on Opus 5 | **Not supported.** The tool is GA and un-renamed; Opus 5 is simply absent from its model list. `web_search` *is* supported on Opus 5 |
| Tool search on Sonnet 5 | Sonnet 5 is **absent** from the published tool-search compatibility table (Fable 5, Mythos 5, Opus 5, Opus 4.8/4.7/4.6/4.5, Sonnet 4.6, Sonnet 4.5, Haiku 4.5 are listed). #TODO(agent): re-verify — if accurate, a Sonnet 5 executor cannot defer tool loading |
| Opus 4.1 and earlier | No tool search support |
| Bedrock | Server-side tool search only via `InvokeModel`, not the Converse API. Web search unavailable; web fetch unavailable |
| Google Cloud | Basic web search only (no dynamic filtering); no web fetch |

---

## 2. Tool search — scale past the 30-50 tool ceiling

**The two problems it solves.** Loading every definition up front costs context (a GitHub + Slack + Sentry + Grafana + Splunk setup burns ~55k tokens before any work happens) and degrades selection accuracy (**tool choice starts failing past 30-50 available tools**). Tool search typically cuts definition tokens by **over 85%**, loading the 3-5 tools a request actually needs, and keeps accuracy high across thousands.

**Measured** (Anthropic, *Advanced tool use*): context **191,300 → 122,800 tokens** (~85% reduction in definition tokens); startup cost **~500 tokens** for the search tool alone vs **~72k** for the full catalog. Accuracy on tool selection rose **49% → 74%** (Opus 4) and **79.5% → 88.1%** (Opus 4.5) — note this is a *quality* gain, not just a cost saving: loading fewer, more relevant tools makes the model choose better.

**Mechanism.** Send *every* tool definition in `tools` on every request — `defer_loading` controls what enters the **context window**, not what you transmit. Non-deferred tools load immediately; deferred ones load only when Claude finds them via search, which returns `tool_reference` blocks (up to 5 per search) that the API expands into full definitions server-side.

**Variants.**

| Variant | Query language | Max length |
|---------|---------------|------------|
| `tool_search_tool_regex_20251119` | Python `re.search()` patterns, case-insensitive (`"get_.*_data"`, `"database.*query\|query.*database"`) | 200 chars |
| `tool_search_tool_bm25_20251119` | Natural language | 500 chars |

Both search tool **names, descriptions, argument names, and argument descriptions**.

**Adopt when** ≥ 10 tools, definitions > 10k tokens, selection accuracy is dropping, you aggregate MCP servers (200+ tools), or the catalog grows over time. **Skip when** < 10 tools, every tool is used every request, or total definitions < 100 tokens.

**Rules and limits.**
- At least one tool must stay non-deferred — all-deferred returns `400`. Never defer the tool search tool itself.
- Keep the 3-5 most-used tools non-deferred so common requests skip the search hop.
- Max **10,000** deferred tools per request.
- Every `tool_reference` must resolve to a definition in `tools`, or `400`.
- A deferred tool **cannot** also carry `cache_control` (`400`) — put the breakpoint on a non-deferred tool.
- Not separately metered; loaded definitions bill as ordinary input tokens.
- Pass `server_tool_use` and `tool_search_tool_result` blocks back unchanged; never return a `tool_result` for a `srvtoolu_...` ID.
- MCP-sourced tools set `defer_loading` on the `mcp_toolset` entry's `default_config` (or per tool in `configs`), not on individual definitions.
- Discoverability is a *description* problem: namespace names by service (`github_`, `slack_`), put user-facing keywords in descriptions, and state the available categories in the system prompt.

**Prompt-cache interaction (the reason this matters beyond token count).** Deferred tools are excluded from the system-prompt prefix before the cache key is computed, and discovered definitions expand inline in the conversation body. **Adding deferred tools therefore does not invalidate an existing cache entry**, and the cache survives both the discovery turn and the call turn. Strict mode still compiles its grammar from the full toolset, so `defer_loading` and `strict` compose without recompilation.

**Custom search** is supported: return `tool_reference` blocks from your own tool's standard `tool_result` (embedding/semantic retrieval), with every referenced tool defined at top level.

---

## 3. Programmatic tool calling — collapse the round trips

With `code_execution_20260120` or later, Claude writes code that calls your tools **inside the sandbox** instead of returning to the model for each invocation. It filters and aggregates before anything reaches context.

- **Measured effect (two independent sets).** Docs, on BrowseComp / DeepSearchQA: **~11% average performance gain with 24% fewer input tokens**. Anthropic *Advanced tool use*, on complex multi-tool tasks: **43,588 → 27,297 tokens (−37%)**, knowledge retrieval **25.6% → 28.5%**, GIA **46.5% → 51.2%**. Latency also drops because the inference passes are eliminated, not just shortened.
- **When it pays:** aggregating or summarizing large result sets, **3+ dependent calls**, filtering/transforming before the model sees anything, and parallel operations across many items. Results are processed inside the sandbox — only the final output enters context.
- **Shape of the win:** 20 per-employee budget lookups become one script — 20 round trips and hundreds of kB collapse to a handful of result lines.
- **Wiring:** `allowed_callers` accepts `"direct"` (default) and `"code_execution_20260120"`. Omitting `"direct"` steers Claude to call the tool only from code. `_20260120` and `_20260521` are interchangeable as caller values; responses always tag the caller as `_20260120`.
- **Supported on** Fable 5, Mythos 5, Opus 5, Opus 4.8/4.7/4.6/4.5, Sonnet 5, Sonnet 4.6, Sonnet 4.5. Claude API, Claude Platform on AWS, and Microsoft Foundry (Hosted-on-Anthropic deployments); **not** Bedrock or Google Cloud.
- Dynamic filtering on `web_search_20260209`+ / `web_fetch_20260209`+ is this mechanism: `allowed_callers` defaults to `["code_execution_20260120"]`, the API provisions code execution automatically, and those calls carry **no extra code-execution charge**. Models without programmatic tool calling must set `allowed_callers: ["direct"]` or the request `400`s with that instruction.

---

## 3.5 Tool-use examples — the cheapest accuracy win

`input_examples` on a tool definition carries **sample invocations**, not prose. It closes the gap between what JSON Schema can express (types, required-ness) and what correct usage actually looks like: format conventions, nested structure shape, which optional parameters travel together, domain-specific encodings.

- **Measured** (Anthropic, *Advanced tool use*): **72% → 90%** accuracy on complex parameter handling. That is the largest single-technique accuracy delta of the four, at negligible token cost — a handful of example objects against a schema that was already being sent.
- **When it pays:** deeply nested structures, many optional parameters with implicit inclusion rules, domain conventions a schema cannot state, and disambiguating two similar tools.
- **Availability:** user-defined and Anthropic-schema **client** tools. **Not** available on server tools. Tool search composes with it — a deferred tool's `input_examples` expand along with its definition on discovery.
- Schema rigor and examples are not substitutes: keep narrow types (`enum`, `minimum`, `pattern`) *and* show one canonical call. The schema constrains, the example communicates.

## 4. Advisor tool — server-side Plan-and-Execute

A faster **executor** model consults a higher-intelligence **advisor** model mid-generation. The advisor reads the full transcript, returns a plan or course correction, and the executor continues — **all inside one `/v1/messages` request**, no extra client round trips. This is the API-native form of the Plan-and-Execute split: near advisor-solo quality with the bulk of tokens generated at executor rates.

```json
{ "type": "advisor_20260301", "name": "advisor", "model": "claude-fable-5", "max_uses": 3 }
```

Beta header: `advisor-tool-2026-03-01`.

**Mechanics.** The executor emits `server_tool_use` with `name: "advisor"` and an **empty input** — the executor signals *timing*, the server supplies *context*. Anthropic runs a separate inference on the advisor under its own system prompt, quoting the executor's full transcript (system prompt, tool definitions, prior turns and results, and the text produced so far this turn). The advisor runs **without tools and without context management**, and its thinking blocks are dropped — only advice text returns as `advisor_tool_result`.

**Parameters.** `type`, `name` (must be `"advisor"`), and `model` are required. `max_uses` caps calls **per request** (not per conversation); past the cap, calls return `max_uses_exceeded` and the executor simply continues unadvised. `max_tokens` caps advisor output (thinking + text) per call, minimum 1024. `caching: {"type":"ephemeral","ttl":"5m"|"1h"}` is an on/off switch for the advisor's own transcript — not a breakpoint; the server places boundaries. Enable it only when you expect **3+ advisor calls** in a conversation.

**Pairing rule.** The advisor must be Sonnet 4.6 or better **and at least as capable as the executor**; equal-capability models may advise each other. Invalid pairs `400`.

| Executor | Valid advisors |
|----------|----------------|
| Haiku 4.5 · Sonnet 4.6 | Fable 5, Mythos 5, Opus 5, Opus 4.8/4.7/4.6, Sonnet 4.6 |
| Sonnet 5 | Fable 5, Mythos 5, Opus 5, Opus 4.8/4.7 |
| Opus 5 | Fable 5, Mythos 5, Opus 5 |
| Fable 5 | Fable 5, Opus 5 |

**Gotchas.**
- With Opus 5 / Fable 5 / Mythos 5 as advisor, the result is an **encrypted `advisor_redacted_result`** — the executor reads it server-side, your client cannot. Only a `claude-opus-4-8` advisor returns plaintext `advisor_result`. Debug the advice with an Opus 4.8 advisor, then switch.
- Advisor billing is at the **advisor model's** rates and draws from that model's rate-limit bucket. An advisor rate limit surfaces as `too_many_requests` *inside the tool result*; an executor rate limit fails the whole request with HTTP 429.
- Conversation-level budgets must be enforced client-side. When you cut the advisor off, remove the tool from `tools` **and strip every `advisor_tool_result` block from history**, or the next request `400`s.
- Beta on the Claude API and Claude Platform on AWS only — not Bedrock, Google Cloud, or Microsoft Foundry.

---

## 5. Selection

| Symptom | Reach for |
|---------|-----------|
| Tool definitions dominate the prompt; selection accuracy dropping | Tool search + `defer_loading` (§2) |
| Many sequential calls over the same tool; large intermediate payloads | Programmatic tool calling (§3) |
| Right tool chosen, arguments malformed | `input_examples` (§3.5) — cheapest fix, largest accuracy delta |
| Cheap model does the work well but plans badly | Advisor tool (§4) |
| Need page/PDF content on Opus 5 | `web_search` + citations, or model that one step on Sonnet 5 / Fable 5 (§1) |
| < 10 small tools, all used every turn | Plain tool calling — none of the above |
