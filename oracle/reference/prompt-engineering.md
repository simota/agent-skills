Purpose: Use this file when you are designing prompts, choosing Claude-specific prompting techniques, or defining prompt tests and versioning rules.

## Contents
- Instruction boundary — what belongs in a prompt
- Triage before rewriting a prompt
- Core design patterns
- Claude 4.x techniques
- Prompt versioning
- Prompt testing
- Optimization checklist
- Agentic prompt patterns

# Prompt Engineering Patterns

## Instruction Boundary — What Belongs In A Prompt

A prompt carries intent; it does not carry guarantees. Strong wording ("absolutely", "100%
accurate", "never leak") adds no detection ability, no capability, and no permission — and it
pushes the model toward confident phrasing that hides uncertainty. Classify each requirement
before writing it.

| Class | Test | Examples |
|-------|------|----------|
| `MUST SPECIFY` | only a human holds it, and a wrong guess makes the output a different artifact | goal, deliverable + use condition, audience, case facts, hard constraints, conflict priority, source of truth, acceptance criteria, how to treat unverified items |
| `SHOULD SPECIFY` | the model can guess, but stating it cuts variance | prior knowledge, depth, locale/jurisdiction, information freeze date, glossary, compat constraints, citation rules |
| `CONDITIONAL` | value depends on task and model — decide per case, never as a blanket rule | few-shot, persona, output schema, tables, length, self-review, search, code execution, clarifying questions |
| `DELEGATE` | reversible exploration where the model beats an up-front guess | section order, naming, wording, candidate designs, search order, implementation shape |
| `DO NOT RELY ON PROMPT` | must hold under ambiguity, long sessions, and injection | access scope, spend caps, type validity, sandboxing, secret isolation, audit logging, irreversible-action approval |

Classification is per case, not per item name: length is usually `CONDITIONAL`, becomes `MUST` at a
hard ad slot, and moves to `DO NOT RELY ON PROMPT` when the API truncates mechanically.

Requirement → the layer that actually enforces it:

| Requirement | Prompt-only failure mode | Enforcing layer |
|-------------|--------------------------|-----------------|
| always valid JSON | stray prose, missing key, wrong type | Structured Outputs + schema validator + retry |
| never exceed a spend cap | misread, off-by-a-digit, injected override | code-side check before the call |
| never touch secrets | complies in wording, reads anyway | tool permission + secret isolation |
| facts are current | training cutoff, missed retrieval | retrieval + source-date check |
| confirm before a destructive act | conversation state or attacker text drifts it | confirmation gate in the application |
| output is correct | self-assertion ≠ measured quality | eval set + independent verification + human review |

`Prompt · Retrieval · Schema · Code/Validator · Tool Permission · Eval · Human Review` are
different guarantees, and a system message is influential rather than binding — Microsoft's current
guidance states it does not ensure compliance and must be paired with filtering and evaluation.
When a requirement wants "absolutely", move it down this list instead of intensifying the wording.

Repo counterpart: `_common/MECHANISM_SELECTION.md` answers the same question one level up — which
Claude Code mechanism holds an instruction. This table answers it inside an LLM application.

## Triage Before Rewriting A Prompt

Bad output is not evidence of a bad prompt. Rewriting instructions when the fault is elsewhere
delays the diagnosis and grows the prompt permanently.

| Layer | Owns | Fault looks like | What rewording cannot fix |
|-------|------|------------------|---------------------------|
| Instruction | task, constraints, priority | ignores a stated constraint, wrong shape | — |
| Context | facts, case specifics, history | generic answer; treats a stale draft as truth | supply and label the authoritative source |
| Capability | what the model can do at all | consistently wrong on this task class | change model or decompose the task |
| Tool | search, execution, data access | stale facts, arithmetic errors | add the tool, not the adjective |
| Evaluation | what counts as success, and how measured | passes review, fails downstream | define observable criteria and measure |

Order: goal and success criteria → is the needed fact in context → is the model capable → is a tool
missing → does the eval measure what you actually want → only then reword. The recurring
misdiagnosis is judging a RAG answer's wording when retrieval never returned the passage
(`reference/evaluation-observability.md` scores retrieval separately for this reason).

## Core Design Patterns

| Pattern | Best for | Note |
|---------|----------|------|
| Role-based | fixing what the model looks at | define responsibility and review focus — a persona does not add knowledge, credentials, or accuracy, and authority framing ("world-class", "20 years") is unverifiable. Measured: 162 personas × 4 model families × 2,410 factual questions produced no general gain, with effects varying unpredictably and no reliable way to pick the best persona (Zheng et al., 2024). Role, refusal conditions, and policy are still required — for consistency and safety, not accuracy |
| Chain-of-Thought / extended thinking | complex reasoning | prefer model-native thinking over micromanaged step scripts |
| Few-shot | format consistency, tone | pick by role (below), not by count; `3-5` is a ceiling, not a target |
| Self-consistency | high-stakes reasoning | multiple paths, then compare |
| ReAct | tool-using agents | use for dynamic sub-tasks |
| Plan-and-Execute | long multi-step workflows | default for auditable agent plans |

### Few-Shot Composition

Examples are specification, not illustration: label space, input distribution, and format carry
much of the effect, example order alone moves results measurably, and the model follows examples
over stated rules when the two disagree. Select by role, not by count.

| Role | Purpose |
|------|---------|
| typical | the ordinary case |
| boundary | near-identical input, different label |
| insufficient-info | the case that must return "needs confirmation" instead of an answer |
| format | the shortest example that pins output shape |

If you cannot name a given example's role, it is duplicate rent. Evaluate on inputs *unlike* the
examples — scoring only on look-alikes hides overfitting. Skip few-shot when the output spec is
already clear, when examples would crowd out source documents, or when they encode a superseded
rule.

State precedence explicitly where examples and rules can drift apart — `current glossary > hard
constraint > example` — and instruct the model to report the conflict rather than imitate a stale
example. Version examples with the rules and re-run the regression set when either changes.

## Prompt Structure Template

```markdown
## Goal
[What the reader can decide or do after using the output — not the task name]

## Deliverable
[Noun + use condition: "a memo an exec can approve funding from", not "a report"]

## Audience
[Who reads it, and what they already know]

## Focus
[Responsibility and what to prioritize looking at — not authority or years of experience]

## Context
[Case facts; which source is authoritative; what is background vs instruction]

## Constraints
- Hard: [violating it fails the deliverable]
- Priority on conflict: [1 … 2 … 3 …]

## Acceptance criteria
- [observable check 1]
- [observable check 2]

## Unknowns
[Stop and ask only when the answer changes the goal, a legal/safety boundary, or an irreversible
decision. Otherwise assume, and list assumptions separately from the deliverable.]

## Output Format
[Only the contract the next consumer needs]

## Examples
<examples>...</examples>
```

Two rules for using it: **slots are drop-if-unused** — a slot with nothing case-specific in it is
rent, not structure; and **specify process only where order carries correctness** (`Required
Process` in `architect/reference/agent-specification-anti-patterns.md` § 2). A numbered step list
as a default slot caps the answer at the requester's first idea, so state outcome conditions and
leave the route free unless the sequence is itself the requirement.

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
- use enums and defaults to reduce output drift;
- **do not lock a schema during exploration** — required fields pull the model into filling slots and drop findings the schema never anticipated. Explore free-form, let a human or evaluator choose the fields, then freeze the schema and validate. Applies to planning, research, hypothesis generation, and long-form drafting;
- keep the schema small and stable, and separate machine-consumed fields from human-facing prose — optional commentary fields grow downstream parsing code;
- fix the format only for what the next consumer contractually needs; a human reader is not a consumer that needs a schema.

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

Bump on the contract a consumer relies on, never on where the text changed.

| Change type | Version bump |
|-------------|--------------|
| output schema, label/enum definition, tool contract, or primary objective changes | Major |
| few-shot examples, added optional guidance, or a system-prompt rewrite that leaves the contract intact | Minor |
| wording tweak with no behavioral target | Patch |

Redefining an existing label is Major even when it edits three words; rewriting the whole system prompt while preserving schema, labels, tools, and objective is not.

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
- **on Opus 5 / Sonnet 5 only:** remove prior-generation over-prompting patterns and strip self-verification instructions (§ Claude 4.x Techniques, rule 3). Do not carry this to model families whose own provider guidance does not support it — a provider's local behavior note is not a universal prompting law

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
