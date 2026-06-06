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

## Claude 4.x Techniques (Opus 4.8 / Sonnet 4.6 baseline, 2026-05)

### Adaptive Thinking

Thinking is off unless `thinking:{type:"adaptive"}` is set; the model then decides depth per step, calibrated by `effort` and query complexity. Budget control moved to `effort` — `budget_tokens` is deprecated.

| Effort | Use case |
|--------|----------|
| `low` | latency-sensitive classification or extraction; on 4.8 scopes strictly to what was asked |
| `medium` | cost-sensitive general production tasks |
| `high` | minimum for intelligence-sensitive work; balances tokens and intelligence |
| `xhigh` | **default**; best for most coding/agentic use cases |
| `max` | deep research or hardest analysis; can overthink (diminishing returns) |

Rules:
- prefer `"think thoroughly"` over brittle hand-written reasoning scripts;
- ask Claude to self-check against explicit criteria;
- if overthinking appears, tell it to choose and commit unless new evidence appears;
- on 4.8, **raise effort** before prompting around shallow reasoning or low tool usage — effort is the stronger lever.

### Opus 4.8 Defaults That Change Prompt Shape

Opus 4.8 keeps the 4.7 shape (existing 4.7 prompts work) but sharpens it. Six concrete consequences for prompt design:

1. **State an output-length envelope explicitly** ("Output is `5-10` lines / ≤ `300` tokens"). Without it, 4.8 over- or under-shoots from its own estimate; prefer positive concision examples over "do not" rules.
2. **State the tool-use directive explicitly** ("Read every file in scope before answering" vs "Do not read files until the design is locked"). 4.8 reads fewer files by default; raise `effort` to `high`/`xhigh` to increase tool usage.
3. **State the thinking nudge at high-stakes decisions** ("Think step-by-step before classifying"). The nudge is a quality lever, not a workaround for a missing capability.
4. **State scope explicitly for broad instructions** ("apply to every section, not just the first"). 4.8 follows instructions literally and won't silently generalize across items or infer unrequested work.
5. **For review/detection prompts, separate finding from filtering.** 4.8 obeys "only high-severity / don't nitpick" faithfully, which can drop low-severity findings; instruct coverage at the finding stage and rank downstream.
6. **Re-check voice and frontend defaults.** Prose trends direct/opinionated; frontend defaults to a fixed cream/serif house style — break it with concrete specs or option-proposal, not negation.

These match `_common/OPUS_48_AUTHORING.md` principles P2 / P3 / P5 / P8 / P10 / P11.

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
- choose effort intentionally; do not default to `high`
- enable prompt caching for stable system prompts
- re-run regression tests after every prompt change
- remove pre-4.6 over-prompting patterns

## Agentic Prompt Patterns

### Parallel Tool Calling

- call independent tools in parallel only when there are no dependencies;
- call dependent tools sequentially;
- never guess missing parameters;
- **on Opus 4.8**: state the parallel trigger explicitly in the prompt ("Spawn each independent track as a separate subagent in the same turn") and pair with the inverse guard ("don't spawn a subagent for work doable in one response"); the model fans out less aggressively than 4.6 by default.

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
