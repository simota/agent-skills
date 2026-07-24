Purpose: Use this file when you are designing prompts, choosing Claude-specific prompting techniques, or defining prompt tests and versioning rules.

## Contents
- Core design patterns
- Claude 4.x techniques
- Prompt versioning
- Prompt testing
- Optimization checklist
- Agentic prompt patterns

# Prompt Engineering Patterns

## Core Design Patterns

| Pattern | Best for | Note |
|---------|----------|------|
| Role-based | domain-specific tasks | assign explicit expertise in the system prompt |
| Chain-of-Thought / extended thinking | complex reasoning | prefer model-native thinking over micromanaged step scripts |
| Few-shot | format consistency, tone | start with `3-5` examples only |
| Self-consistency | high-stakes reasoning | multiple paths, then compare |
| ReAct | tool-using agents | use for dynamic sub-tasks |
| Plan-and-Execute | long multi-step workflows | default for auditable agent plans |

## Prompt Structure Template

```markdown
## Role
You are [role] with expertise in [domain].

## Context
[Background relevant to the task]

## Instructions
1. [Step 1]
2. [Step 2]

## Output Format
[Exact format with example]

## Constraints
- [Constraint 1]
- [Constraint 2]

## Examples
<examples>...</examples>
```

## Claude 4.x Techniques (Opus 5 / Sonnet 5 baseline, 2026-05)

### Adaptive Thinking

On Opus 5 and Sonnet 5 adaptive thinking is **on by default**; the model decides depth per step, calibrated by `effort` and query complexity. Budget control lives in `effort` — `budget_tokens` is deprecated. `thinking:{type:"disabled"}` is accepted only at effort `high` or below on Opus 5; pairing it with `xhigh`/`max` returns a 400 error.

| Effort | Use case |
|--------|----------|
| `low` | latency-sensitive classification or extraction, and subagents; notably stronger on Opus 5 than on earlier Opus models |
| `medium` | cost-saving step-down; viable for real agentic work where evals hold |
| `high` | **default** on the Claude API and Claude Code; complex reasoning, difficult coding, agentic tasks |
| `xhigh` | recommended starting point for coding/agentic and long-horizon (30 min+) work |
| `max` | deep research or hardest analysis; can overthink (diminishing returns) |

Rules:
- prefer `"think thoroughly"` over brittle hand-written reasoning scripts;
- **do not add self-check instructions** — Opus 5 verifies its own work, and explicit "double-check / re-verify" prompts cause over-verification. Put verification in a *separate* agent instead;
- if overthinking appears, tell it to choose and commit unless new evidence appears;
- control cost with lower effort rather than by disabling thinking; effort affects response text, tool calls, and thinking together;
- hold effort constant inside a cached conversation — changing it invalidates the cached prefix.

### Opus 5 Defaults That Change Prompt Shape

Opus 5 has sharp defaults that shape how prompts must be written. Six concrete consequences for prompt design:

1. **State an output-length envelope explicitly** ("Output is `5-10` lines / ≤ `300` tokens"). Opus 5's default output runs long in two channels — chat responses *and* files written to disk — and lowering effort does not reliably shorten visible output. Prefer positive concision examples over "do not" rules, and repeat a short reminder near the end of a long prompt.
2. **State the tool-use directive explicitly** ("Read every file in scope before answering" vs "Do not read files until the design is locked"). Effort governs call volume: lower effort combines operations into fewer calls, higher effort makes more and explains first. For vision work, tools beat a bigger reasoning budget.
3. **Do not instruct verification or self-checks.** Opus 5 verifies its own work unprompted; carried-over "include a final verification step" / "use a subagent to verify" instructions waste tokens with no quality gain. Keep thinking nudges for genuinely high-stakes decisions ("Think step-by-step before classifying") — that is a quality lever, not a self-check.
4. **Bound scope explicitly.** Opus 5 can *expand* a task, adding unrequested steps; state what is in and out of scope. Separately, state broad scope where it applies ("apply to every section, not just the first").
5. **For review/detection prompts, separate finding from filtering.** Opus 5 obeys "only high-severity / don't nitpick" faithfully, which can drop low-severity findings; instruct coverage at the finding stage and rank downstream. Accuracy holds at low effort, so a cheap wide pass plus a thorough adjudication pass is a valid design.
6. **Cap subagent delegation.** Opus 5 delegates readily; state criteria and a ceiling rather than encouraging fan-out, and forbid using subagents to check its own work.

These match `_common/OPUS_5_AUTHORING.md` principles P2 / P3 / P9 / P8 / P10 / P4.

### Structured Outputs

- prefer tool-based schemas or `output_format` JSON mode over plain-text JSON prompting;
- validate every output with a schema before downstream use;
- use enums and defaults to reduce output drift.

### XML Tags

- use clear tags such as `<instructions>`, `<context>`, `<documents>`, and `<output_format>`;
- place long source documents near the top of the prompt;
- use `<example>` blocks to keep examples separate from instructions.

### Prefill Deprecation

| Old pattern | Replacement |
|-------------|-------------|
| force JSON via assistant prefill | Structured Outputs API or tool choice |
| skip preamble | direct system instruction |
| continue partial answer | explicit continuation instruction |

## Prompt Versioning

| Change type | Version bump |
|-------------|--------------|
| system prompt rewrite | Major |
| few-shot example changes | Minor |
| wording tweak | Patch |

Keep prompts versioned like code:
- system prompt
- examples
- config
- active registry mapping

## Prompt Testing

| Category | Priority |
|----------|----------|
| Happy path | Must pass |
| Edge cases | Must pass |
| Adversarial | Must pass |
| Format | Must pass |
| Consistency | Should pass |
| Regression | Must pass |

Rules:
- keep a stable regression set;
- add new tests from real failures;
- run A/B tests with the same cases and fixed metrics;
- measure quality and cost together.

## Optimization Checklist

- remove context that does not measurably help output quality
- reduce few-shot count until quality drops
- try a smaller model before escalating to a larger one
- set `max_tokens` to realistic output needs
- choose effort intentionally; re-sweep rather than carrying settings across model generations
- enable prompt caching for stable system prompts (Opus 5 caches from 512 tokens)
- re-run regression tests after every prompt change
- remove prior-generation over-prompting patterns, and strip self-verification instructions

## Agentic Prompt Patterns

### Parallel Tool Calling

- call independent tools in parallel only when there are no dependencies;
- call dependent tools sequentially;
- never guess missing parameters;
- **on Opus 5**: the model delegates readily, so lead with the ceiling, not the trigger — "delegate only to large, genuinely independent tracks; don't spawn a subagent for work doable in one response; don't use subagents to check your own work; prefer one over several."

### Autonomy vs Safety

- freely take local, reversible actions;
- ask before hard-to-reverse actions or changes to shared systems;
- when the agent can be reached by attacker-controlled text (RAG sources, customer messages, scraped pages), follow the **secure plan-then-execute** pattern: planning sees the untrusted text; the executor only sees the *plan*, never the raw input.

### Subagent Orchestration

- light custom agents `<3k` tokens enable fluid orchestration;
- heavy custom agents `25k+` tokens create bottlenecks;
- use subagents for parallel or isolated work, not trivial single-step tasks.

### CodeAct Prompting

When the task is data-shape-heavy or tool-graph-heavy:
- frame the assistant turn as "emit a Python (or TS) program that uses the provided tools to solve the task";
- enumerate the available tool surface as importable functions, not as JSON tool calls;
- require the program to print a structured result to stdout that downstream code can parse;
- always run the emitted program in a sandboxed runtime (separate process, scoped FS, blocked network unless explicitly required).
