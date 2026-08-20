# Claude for Foundation Models (iOS server-side LLM)

> Distilled from the official guide: <https://platform.claude.com/docs/en/cli-sdks-libraries/libraries/apple-foundation-models>
> Package: [`anthropics/ClaudeForFoundationModels`](https://github.com/anthropics/ClaudeForFoundationModels) — Apache 2.0, **beta** (OS 27 betas; APIs may change before GA).

## What it is

A Swift package that conforms **Claude** to Apple's Foundation Models `LanguageModel` protocol, so a server-side Claude call is driven by the **same `LanguageModelSession` API** as Apple's on-device model. `respond(to:)`, streaming, guided generation (`@Generable`), and tool calling all work unchanged — switch model by swapping the `model:` argument.

- Requests go **app → Claude API directly**. Apple is not in the request path and never sees prompts or responses.
- Usage billed to the Anthropic account at standard API pricing.
- **NOT** a general-purpose Messages API client. Public surface is the provider conformance plus config types (`ClaudeLanguageModel`, `ClaudeModel`, `AuthMode`, `ClaudeServerTool`). For raw Messages API access, use a Client SDK instead.

## When to escalate to Claude vs the on-device model

Apple's on-device model is fast, private, offline — but sized for lightweight tasks. Escalate to Claude when the feature needs **larger context, frontier reasoning, or server-side tools** (web search / web fetch / code execution). Same `LanguageModelSession` API → switch is a one-line `model:` change. A common fallback: catch `.rateLimited` and drop to `SystemLanguageModel` for that turn.

## Requirements

- iOS 27 / macOS 27 / visionOS 27 / watchOS 27 (all beta) — the OS releases whose Foundation Models framework supports server-side language models.
- Xcode 27 (beta).
- A Claude API key (Claude Console) for development; a proxy for production (see Authentication).

## Install

```swift
// Package.swift
dependencies: [
  .package(url: "https://github.com/anthropics/ClaudeForFoundationModels.git", from: "0.1.0")
]
```

```swift
import FoundationModels
import ClaudeForFoundationModels
```

## Quick start

```swift
let model = ClaudeLanguageModel(
  name: .opus5,
  auth: .apiKey(ProcessInfo.processInfo.environment["ANTHROPIC_API_KEY"] ?? "")
)
let session = LanguageModelSession(model: model)
let response = try await session.respond(to: "Plan a 4-day trip to Buenos Aires.")
print(response.content)
```

`ClaudeLanguageModel` init also accepts `baseURL` (default `https://api.anthropic.com`), `timeout`, `serverTools`, and `fixedEffort`. A runnable CLI example lives in `Examples/ClaudeExample` (requires a macOS 27 host; `--search` flag enables server-side web search).

## Model selection & capabilities

- Model IDs are `ClaudeModel` values. Use a compiled-in constant (one per shipped model, e.g. a `claude-opus-5` constant) — new models ship as new constants per package release. #TODO(agent): confirm the compiled-in constant names for Opus 5 and Sonnet 5 (e.g. `.opus5` vs `.opus5_0`) — removed the stale `.sonnet4_6` example rather than guess.
- Each `ClaudeModel` **declares its capabilities** (sampling params, effort levels, adaptive thinking, structured output, image input). The package uses this to decide which request fields to send — **sending a field a model rejects is a hard error**, so capabilities are not optional metadata.
- For an ID not compiled in yet, construct one with explicit capabilities (no shorthand that guesses):

```swift
let model = ClaudeModel(
  id: "claude-experimental-x",
  capabilities: .init(samplingParams: false, effortLevels: [.low, .high])
)
ClaudeLanguageModel(name: model, auth: auth)
```

### Effort

`fixedEffort:` pins the effort level for every request and **takes precedence over the framework's per-request reasoning hints**. It is the **only way to request `.xhigh` or `.max`** — the framework's reasoning levels stop at `high`. API defaults to `high` when no effort is sent. The level must be one the model accepts (some models accept no effort at all).

```swift
ClaudeLanguageModel(name: .opus5, auth: auth, fixedEffort: .xhigh)
```

## Authentication

| Mode | Use | Notes |
|------|-----|-------|
| `.apiKey("…")` | **Development only** | A key bundled in the app binary is extractable and bills your account — never ship it. |
| `.proxied(headers:)` + `baseURL:` | **Production** | Gateway at `baseURL` adds the `x-api-key` server-side; app ships no key. `headers` sent on every request so the proxy authorizes the caller (`[:]` if none). |

The proxy receives standard Messages API requests, attaches `x-api-key`, forwards to `https://api.anthropic.com`.

```swift
ClaudeLanguageModel(
  name: .opus5,
  auth: .proxied(headers: ["X-App-Token": "..."]),
  baseURL: URL(string: "https://api.yourapp.com/claude")!
)
```

> Ties into the Native `Never` rule: no client-side API keys (MASWE-0005). The `.proxied` + BFF pattern is the production-correct path.

## Streaming

```swift
let stream = session.streamResponse(to: "Summarize today's top science stories.")
for try await partial in stream { print(partial.content) }
```

Each element is a **cumulative snapshot** of the response so far — **not a delta**.

## Structured output

```swift
@Generable
struct Trip {
  @Guide(description: "Destination city") var destination: String
  @Guide(description: "Length in days") var days: Int
}
let response = try await session.respond(to: "Plan a trip to Tokyo.", generating: Trip.self)
```

Requires a model whose capabilities include structured output (all compiled-in constants do). Otherwise throws `LanguageModelError.unsupportedGenerationGuide` — **no silent degradation**.

## Tool use

- **Client-side**: the framework's `tools:` array works unchanged — conform to `Tool`, pass to `LanguageModelSession`, framework invokes them on-device when Claude calls them.
- **Server-side**: web search / web fetch / code execution run on Anthropic infra in a single round trip (nothing to invoke on-device). Configured per model via `serverTools:`:

```swift
let model = ClaudeLanguageModel(
  name: .opus5, auth: auth,
  serverTools: [.webSearch(maxUses: 5), .codeExecution]
)
```

`.webSearch` / `.webFetch` accept optional `allowedDomains`, `blockedDomains`, `maxUses`. Server-tool activity surfaces in the transcript as `ClaudeServerToolSegment`. Note: `serverTools` is on `ClaudeLanguageModel`, **not** the session (the session type is Apple's) — use multiple model instances for different tool sets per conversation.

## Images

Models declaring image-input capability expose the framework's vision capability; pass image content through the standard session API and the package converts it to Claude's image format.

## Error handling

Claude API errors map onto Apple's `LanguageModelError` where one fits — context overflow → `.contextSizeExceeded`, HTTP 429 → `.rateLimited`, timeout → `.timeout`. Provider errors with no framework equivalent surface as `ClaudeError` (e.g. `ClaudeError.missingCredential`).

```swift
do { let r = try await session.respond(to: prompt); print(r.content) }
catch ClaudeError.missingCredential { /* prompt for key */ }
catch let error as LanguageModelError { /* rate limit, guardrail, context length, decoding */ }
catch { /* transport */ }
```

## Feature support — NOT available through the provider protocol

Features with no representation in Apple's protocol are unreachable here:

- Prompt-caching controls (caching applied automatically; **TTL / breakpoint not configurable**)
- Stop sequences
- Batch processing
- Files API
- Token counting
- Beta headers

## Store-compliance tie-in

Server-side Claude is third-party AI → App Store Review Guideline **5.1.2(i) AI disclosure UI** applies, exactly as for any non-Apple model. Draft the disclosure flow alongside the feature (see `store-compliance.md`). The on-device vs Claude routing decision is also an `AI_DISCLOSURE_UI` interaction trigger.

## Beta caveats

- API may change before GA.
- Apache 2.0; bug reports via GitHub issues. **External PRs not accepted during beta.**
