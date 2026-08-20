# SSE Streaming Reference

Purpose: Design unidirectional server-to-client streaming over HTTP using Server-Sent Events. Cover reconnection semantics with `Last-Event-ID`, heartbeat / keep-alive, proxy and CDN buffering pitfalls, long-polling fallback, `EventSource` browser compatibility, and the WebSocket comparison that governs transport selection.

## Scope Boundary

- **Relay `sse`**: SSE server architecture, event stream framing, reconnection with `Last-Event-ID`, heartbeat cadence, proxy-safe headers, fallback ladder to long polling, and `EventSource` client contract.
- **Relay `websocket` (adjacent)**: bidirectional, low-latency full-duplex transport. Use when the client must push frequently or upgrade to binary frames. SSE is one-way — do not force duplex over SSE with a second HTTP POST channel when WebSocket fits.
- **Gateway (elsewhere)**: REST/GraphQL request/response API spec — no streaming transport design.
- **Stream (elsewhere)**: batch/stream ETL pipelines (Kafka/Flink/Airflow). SSE carries user-facing events to browsers; Stream moves data between backends.
- **Tempo (elsewhere)**: retry/backoff *policy* for business jobs. SSE reconnect uses client-driven `EventSource` defaults plus server-suggested `retry:` — Tempo owns the broader retry taxonomy.
- **Beacon (elsewhere)**: SLO / dashboard / alert design over SSE metrics (active streams, event lag, disconnect rate). Relay emits metric specs; Beacon shapes the alerting.

If the hypothesis is "server pushes read-only updates to many browser clients" → `sse`. If clients must also send frequent messages → `websocket`. If the pipeline is backend-to-backend data movement → Stream.

## When SSE Beats WebSocket

| Property | SSE | WebSocket |
|----------|-----|-----------|
| Direction | Server → Client only | Full duplex |
| Transport | Plain HTTP/1.1 or HTTP/2 | Upgrade handshake (HTTP/1.1 `Upgrade`, HTTP/2 RFC 8441) |
| Auto-reconnect | Built into `EventSource` | Manual (client-side) |
| `Last-Event-ID` resume | Native protocol feature | Custom app-level protocol |
| Proxy / CDN support | Works through most HTTP proxies | Frequently blocked or buffered |
| Binary frames | No (text only, UTF-8) | Yes |
| Browser API | `EventSource` (no polyfill on modern browsers) | `WebSocket` |
| Backpressure | HTTP/TCP flow control | Application-level |

Pick SSE for: notifications, dashboards, progress updates, chat read receipts from server, token-streaming LLM output, log tailing. Pick WebSocket for: chat send, collaborative editing, multiplayer games, trading clients.

### 2026 AI Streaming Decision Path

The 2026 LLM streaming ecosystem made the SSE / WebSocket split sharper:

- **Plain token streaming** (OpenAI Chat Completions / Anthropic Messages with `stream: true`, Vercel AI SDK, LangChain streaming) is **SSE-first** and remains so. Every major LLM provider ships an SSE stream as the canonical wire format for `delta` tokens.
- **Agentic AI workloads** — tool use approval, mid-stream user interrupts, multi-turn agent dialog, multi-agent coordination, human-in-the-loop checkpoints — outgrow SSE. The 2026 published pattern is "start with SSE, migrate to WebSocket when you need any of: human-in-the-loop approval, cross-device continuity, connection resilience that survives a brief redeploy, or multi-agent coordination".
- **MCP transport, 2026**: the Model Context Protocol **deprecated its standalone SSE transport** in favor of **Streamable HTTP** — `HTTP POST` for client-to-server requests, `SSE` for server-to-client streaming on the same endpoint. New MCP servers should adopt Streamable HTTP by default; legacy SSE-only MCP servers still work but will be migrated in their next major version.

Practical 2026 rule: if the surface is a chat or LLM output stream and the user only watches, SSE remains correct. If the user can interrupt, approve tool calls, or hand off between agents, plan for WebSocket from the start — adding bidirectional control on top of SSE later is a rewrite, not a delta.

## Event Stream Framing

Wire format is `text/event-stream`, UTF-8, line-delimited, terminated by a blank line.

```
id: 42
event: message
retry: 3000
data: {"channel":"room-7","text":"hello"}

id: 43
event: presence
data: {"user":"u_91","status":"online"}

: heartbeat 2026-04-24T10:00:00Z

```

Rules:
- `id:` populates `event.lastEventId` on the client and is echoed back in `Last-Event-ID` on reconnect.
- `event:` routes to `source.addEventListener('message', ...)` — omit to hit the default listener.
- `retry:` is milliseconds — server's hint for reconnect delay. Defaults to ~3000 ms in most browsers if absent.
- Lines starting with `:` are comments — use for heartbeats without dispatching an event to JS.
- Each record ends with a **blank line**. Forgetting the trailing `\n\n` is the single most common SSE bug.

## Reconnection with Last-Event-ID

```
Client GET /stream                    → 200 OK, stream opens
Server sends id: 1, id: 2, id: 3
Network drops after id: 3
Client auto-reconnects (retry: 3000)
Client GET /stream  Last-Event-ID: 3  ← browser sets this header automatically
Server resumes: emits id: 4, id: 5, ...
```

Server contract:
- Persist event IDs durably (Redis stream / Kafka offset / DB sequence) for the resume window.
- Define a **retention horizon** (e.g. 5 minutes). Beyond horizon, respond `204 No Content` or a fresh snapshot event — never silently skip.
- Authenticate the resume request — `Last-Event-ID` is attacker-controlled; do not trust it for authorization scope.

## Heartbeat / Keep-Alive

| Layer | Risk | Heartbeat |
|-------|------|-----------|
| Browser idle-tab throttle | Silent connection hold | 15–30 s comment ping |
| Corporate proxy idle timeout | Drop after 30–60 s of silence | ≤ 25 s comment ping |
| NAT / load balancer idle timeout | AWS ALB default 60 s, GCP default 600 s, Cloudflare default 100 s | ≤ idle / 2 |
| HTTP/2 flow-control stall | Window exhaustion under burst | Periodic `WINDOW_UPDATE` (stack-handled) |

Default cadence: 15 seconds, send as a comment line `: ping\n\n`. Comments do not fire JS listeners — they keep the TCP/HTTP path warm without polluting application events.

## Proxy / CDN Buffering

SSE fails loudly on buffering proxies because events must flush immediately.

Required response headers:
```
Content-Type: text/event-stream
Cache-Control: no-cache, no-transform
Connection: keep-alive
X-Accel-Buffering: no          ← nginx; disables proxy_buffering for this response
```

Infrastructure checklist:
- **nginx**: `proxy_buffering off` on the location, or send `X-Accel-Buffering: no`.
- **CloudFront**: disable response buffering (supported in origin behaviors for streaming origins); otherwise SSE stalls until full chunk.
- **Cloudflare**: enable "Response Buffering off" (streaming endpoints). Cloudflare Workers `ReadableStream` passthrough is SSE-safe.
- **ALB / NLB**: ALB buffers response bodies in older configurations — verify with a live stream; prefer NLB for large fan-out.
- **HTTP/2**: confirm server does not buffer per-stream beyond flow-control window.

If a client sees events arrive in bursts instead of one-by-one, the proxy is buffering.

## Long-Polling Fallback

When `EventSource` is unavailable (ancient browser, hostile proxy stripping `text/event-stream`, or intermediary HTTP/1.0) fall back to long polling — **not** short polling.

```
Client GET /poll?since=42
Server holds request up to 25 s
  → on event: respond { events: [...], cursor: 57 }
  → on timeout: respond 204 (client re-polls)
Client re-issues GET /poll?since=57
```

Keep the cursor wire-compatible with `Last-Event-ID` so SSE and long-poll clients share the same event store. Long poll should be the documented fallback, not the default.

## EventSource Browser Compatibility

- Modern evergreen browsers (Chrome, Firefox, Safari, Edge): native `EventSource`. No polyfill needed.
- IE / legacy Edge: no native support — polyfill (e.g. `event-source-polyfill`) supports custom headers (native `EventSource` does **not** allow custom request headers except `Last-Event-ID`).
- Custom auth headers: native `EventSource` cannot set `Authorization`. Use cookies (with `withCredentials: true`) or put the token in the URL (scoped, short-lived) — or switch to a `fetch` + `ReadableStream` implementation.
- `withCredentials`: required for cross-origin cookie-based auth; server must send `Access-Control-Allow-Credentials: true` and an explicit origin (not `*`).

## Anti-Patterns

- Shipping SSE without heartbeats and then blaming "flaky network" when the LB drops idle connections.
- Returning `Content-Type: application/json` or `text/plain` for the stream endpoint — clients will not treat the body as `text/event-stream`.
- Forgetting the trailing blank line — events never dispatch and the bug looks like a server hang.
- Re-serializing event payloads on every reconnect from scratch instead of resuming from `Last-Event-ID` — turns a 5-second blip into a thundering-herd full-state refresh.
- Using SSE for client-to-server messaging by pairing it with ad-hoc POSTs — pick WebSocket if duplex is required.
- Mounting SSE behind a CDN with default response buffering — events arrive in multi-second bursts and the UX feels broken.
- Trusting `Last-Event-ID` for authorization scope — it is a client-supplied header and must only select *which events to resume*, never *what the user may see*.
- Disabling HTTP/2 "because SSE is HTTP/1.1" — SSE works over HTTP/2 and benefits from multiplexing when a single origin serves many streams.
- Hard-coding a 3-second client reconnect when backends are flapping — send `retry:` with increasing values to spread the reconnect storm.

## Handoff / Next Steps

**To Builder** (RELAY_TO_BUILDER):
- Server architecture (event source: Redis Streams / Kafka / DB sequence), ID allocation scheme, retention horizon, heartbeat cadence.
- Response header contract and proxy/CDN configuration required for deployment.
- Reconnection protocol including `Last-Event-ID` window and out-of-horizon behavior (snapshot vs 204).
- Long-poll fallback endpoint contract if required.

**To Scaffold** (RELAY_TO_SCAFFOLD):
- LB / proxy idle timeouts (must exceed heartbeat × 2), buffering disabled, HTTP/2 enabled, connection limits per pod.
- Horizontal scaling story: sticky sessions are *not* required if events come from a shared bus (Redis Streams / Kafka); flag when they are.

**To Beacon** (RELAY_TO_BEACON):
- Metrics: active stream count, event emit rate, per-client lag (now − last-delivered-event-time), reconnect rate, 5xx rate, heartbeat miss rate.
- SLO target: ≥ 99.5% of events delivered within 2 s p95 once emitted.

**To Sentinel** (RELAY_TO_SENTINEL):
- Auth posture on the stream endpoint (cookie vs token-in-URL vs custom-header fetch), CORS with credentials, `Last-Event-ID` trust boundary.
