# AI-Assisted Prototyping Guide

> Purpose: use AI to accelerate Forge safely without handing it architecture, domain truth, or quality judgment. Covers both generic AI tooling (Cursor / v0 / Bolt.new / Lovable) and AI-feature PoC patterns (chat / streaming / RAG / agent UI) under the `ai` recipe.

## Contents

- Tool map
- Phase-by-phase use
- Prompt strategy
- Safe use boundaries
- Quality checks
- AI Feature PoC pattern (`ai` recipe)

## Tool Map

| Category | Examples | Best use | Common weakness |
|---|---|---|---|
| General AI chat | Claude, ChatGPT | concept shaping, boilerplate, quick variants | weak long-range state management |
| Component factory | v0 (Vercel) | Production-quality React/Next.js components using shadcn/ui + Tailwind | No backend logic, no database support; credit-limited |
| Full-stack rapid prototype | Bolt.new | Browser-based prototyping with framework flexibility (React, Vue, mobile) | Output needs refinement; not production-grade |
| Working MVP builder | Lovable | Complete apps with Supabase backend (auth, DB, storage, real-time) | Opinionated stack; less control over architecture |
| Design-to-prototype | Figma Make | Design-system-compliant UI generation from text prompts; concept→prototype ~38% faster | Requires existing design system; review output against brand guidelines |
| Multimodal prototyping | Google Stitch | Gemini-based: text/image/wireframe → UI + frontend code generation | Early stage; output quality varies; not production-grade |
| IDE assistants | Claude Code, Cursor, Copilot | local integration, repetitive edits, context-aware refactoring | quality depends on existing project context |

## Best Use by Forge Phase

| Forge phase | Use AI for | Do not delegate |
|---|---|---|
| `SCAFFOLD` | option generation, stack choice, slice framing | deciding product truth without evidence |
| `STRIKE` | boilerplate, starter TSX, mock handlers, sample data | complex domain rules or final architecture |
| `COOL` | quick bug triage, edge-case prompts, checklist generation | final quality judgment |
| `PRESENT` | demo steps, summary bullets, validation prompts | stakeholder decision-making |

## Prompt Strategy

Use staged prompts instead of one giant ask:

1. Ask for the minimum skeleton.
2. Ask for one interaction.
3. Ask for one mock strategy.
4. Ask for review against the current hypothesis.

Good prompt qualities:
- explicit scope
- explicit time-box
- declared prototype type: `Throwaway` or `Evolutionary`
- declared framework and output files
- one request per pass

## Safe AI Boundaries

AI is good at:
- CRUD UI skeletons
- form and table scaffolds
- starter `MSW` handlers
- realistic sample data shapes
- repetitive boilerplate

AI is weak at:
- hidden business rules
- multi-service orchestration
- production-ready state architecture
- long-lived maintainability decisions

Safe Vibe Coding scope:
- throwaway demos
- internal exploration
- quick local-only prototypes

Ask first before relying on AI-generated structure when:
- the prototype is intended to evolve into production
- the domain has non-obvious business constraints
- the prototype spans multiple services

## One-Day Prototype Pattern

Morning:
- frame the hypothesis
- generate the base UI
- connect fixtures or `MSW`

Afternoon:
- add interaction and failure states
- run `COOL` checks
- prepare the demo and decision notes

## Quality Checks for AI-Generated Code

Check these before accepting AI output:

- build passes
- component actually renders
- mock contract matches expected field names
- no unexplained `any`
- no silent missing states
- no invented API behavior
- no hidden third-party dependency creep

### Security Checks (mandatory for handoff)

Injection flaws account for 33.1% of confirmed AI code vulnerabilities. Check:

- no SQL/command/code injection vectors (parameterized queries, no string concatenation in queries)
- no hardcoded secrets (API keys, tokens, credentials in client bundles)
- no client-side auth bypasses (auth checks must happen server-side)
- no exposed internal endpoints or debug routes
- no permissive CORS (`Access-Control-Allow-Origin: *` in production config)
- no unvalidated user input passed to `eval()`, `exec()`, or shell commands

Common failure signals:
- wrong framework API usage
- stale library syntax
- inconsistent data shape
- missing loading / error state
- unexplained business assumptions

## Forge Integration Rules

- Use AI to accelerate scaffolding, not to define the prototype's meaning.
- Require a human review during `COOL`.
- Resolve TypeScript or build errors before `PRESENT`.
- Document why a given AI tool was chosen when the prototype survives beyond a quick check.

---

## AI Feature PoC Pattern (`ai` recipe)

Purpose: Validate an AI-feature hypothesis (chat UX, streaming feel, RAG retrieval quality, agent loop) inside the ≤4h time-box. Use mocked LLM responses during STRIKE; swap in real API only after the happy path works. Ship injection-safe input handling by default.

### Scope Boundary

- **Forge `ai`**: throwaway AI UX prototype (chat shell, streaming feel, RAG demo, agent UI loop). Input/output safety baseline by default.
- **Oracle (elsewhere)**: real prompt engineering, RAG pipeline architecture, eval framework, AI safety design, MLOps.
- **Artisan (elsewhere)**: production chat / streaming UI with accessibility, keyboard, error boundaries, retry UX.

If the hypothesis is "does this UX feel right to the user?" → `ai`. If it's "does the prompt / retrieval / eval actually work?" → Oracle.

### Hypothesis Types

| Hypothesis | Minimum prototype |
|------------|-------------------|
| Chat affordance fits the task | Message list + input + send + mock streaming reply |
| Streaming feels fast enough | Token-chunked fake response at 30–60 tok/s, cursor blink |
| RAG shows sources usefully | Inline citation chips, hover preview, mock retrieval |
| Agent tool-use loop is intuitive | Animated "thinking / calling tool / result" state machine |
| Inline AI suggestion is accepted | Greyed ghost text, `Tab` to accept, `Esc` to dismiss |

Pick one. Pick exactly one.

### Workflow

```
SCAFFOLD  →  declare hypothesis (UX / retrieval / streaming / agent loop / inline)
          →  pick UI shape (chat / inline / side-panel / overlay)
          →  decide mock vs real LLM for STRIKE (default: mock)
          →  set token budget ceiling for any real-API segment

STRIKE    →  build UI shell first (scrollable message list, input, send)
          →  wire mock streaming (see "Mock Streaming" below)
          →  sanitize user prompt, escape rendered markdown output
          →  happy path demoable without network

COOL      →  swap one path to real API if hypothesis demands it, budget-check
          →  verify empty, in-flight, error, abort, rate-limit states have placeholders
          →  prompt-injection spot-check: paste a jailbreak string, confirm escape

PRESENT   →  ADOPT / ITERATE / DISCARD
          →  ADOPT → hand off to Oracle (prompt/RAG/eval) + Artisan (production UI)
```

### Mock Streaming

Real streaming is cheap to fake and removes network from the demo loop.

```ts
// mock/stream.ts
export async function* mockStream(text: string, tokPerSec = 40): AsyncGenerator<string> {
  const tokens = text.split(/(\s+)/);
  for (const tok of tokens) {
    yield tok;
    await new Promise(r => setTimeout(r, 1000 / tokPerSec));
  }
}

// usage
for await (const chunk of mockStream(answer)) {
  setText(prev => prev + chunk);
}
```

Keep mock latency realistic — too fast (>200 tok/s) makes reviewers think the UX is fake; too slow (<15 tok/s) makes the UX feel broken.

### Injection-Safe Input / Output

During STRIKE, even throwaway code must do these three things — they're cheap and prevent the demo itself from showing exploitable markdown. (General injection / secret-leak checks live in "Security Checks" above; the rules below are LLM-output-specific.)

1. **Escape rendered markdown**: use a sanitizer (DOMPurify / rehype-sanitize) before rendering assistant output. Raw `dangerouslySetInnerHTML` on LLM output is a demo-breaker when a reviewer pastes an injection.
2. **Strip hidden unicode**: remove zero-width / control chars from user input to prevent "hidden" prompt-injection tokens.
3. **Never render tool-call JSON inline**: tool calls in agent UI must be a separate UI affordance, not inline-executed markdown.

These are the minimum — Oracle owns the full guardrail design.

### Token-Cost Budget (when using real API)

Before any real-API path in COOL:

```
budget = demo_runs × avg_tokens_per_run × model_price_per_1k
```

Set a hard cap. A chat PoC typically needs ≤ $2 for the full session. If the demo is >20k tokens/run, stay on mocks and only show the real call once.

### Agent-Loop UI Pattern

If the hypothesis is "does tool-use feel right?", show the loop states explicitly:

```
┌────────────────────────────────────────┐
│ 🤔 Thinking…                           │  ← planning
│ 🔧 search_docs("pricing")              │  ← tool call
│    ↳ 3 results                         │  ← tool result
│ 📝 Drafting answer…                    │  ← synthesis
│ ✓ Answer ready                         │
└────────────────────────────────────────┘
```

Fake each state with `setTimeout` during STRIKE. Reviewers care about the *shape* of the loop, not the real orchestration.

### Time-Box Anti-Patterns (`ai` recipe)

- ❌ Integrate real vector DB (pgvector / pinecone / weaviate) in STRIKE — mock retrieval with a JSON array.
- ❌ Add real OpenAI / Anthropic SDK setup before UI shell exists.
- ❌ Polish markdown rendering edge cases (tables / code blocks with syntax highlight) unless that is the hypothesis.
- ❌ Build conversation history persistence (IndexedDB / server store) — keep it in `useState`.
- ❌ Implement proper abort / retry / rate-limit UX — use placeholder states only.

### Handoff to Oracle + Artisan

**To Oracle:**
- Hypothesis outcome (retrieval feel / streaming feel / agent loop feel).
- Mock prompts / fake tool-call shapes used — Oracle designs the real prompt and retrieval.
- Token budget observed, cost concern flags.
- Safety gaps intentionally left (prompt injection variants not handled, PII redaction, jailbreak detection).

**To Artisan:**
- Final UI shape (chat / inline / side panel) and component boundaries.
- Streaming render contract (chunk type, abort handle, scroll-lock behavior).
- States the prototype skipped (error, rate limit, abort, retry, long-running tool) — Artisan owns production.
