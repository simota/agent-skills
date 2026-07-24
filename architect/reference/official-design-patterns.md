# Official Design Patterns Reference

> Source: "The Complete Guide to Building Skills for Claude" (Anthropic, 2025)

Official design pattern reference for Architect's ENVISION / DESIGN phases.

---

## 1. Three Use Case Categories

### Category 1: Document & Asset Creation

**Used for**: Creating consistent, high-quality output — documents, presentations, apps, designs, code

**Key Techniques**:
- Embedded style guides and brand standards
- Template structures for consistent output
- Quality checklists before finalizing
- No external tools required — uses Claude's built-in capabilities

**Real example**: `frontend-design` skill, Office skills (docx, pptx, xlsx, ppt)

### Category 2: Workflow Automation

**Used for**: Multi-step processes that benefit from consistent methodology, including multi-MCP coordination

**Key Techniques**:
- Step-by-step workflow with validation gates
- Templates for common structures
- Built-in review and improvement suggestions
- Iterative refinement loops

**Real example**: `skill-creator` skill

### Category 3: MCP Enhancement

**Used for**: Workflow guidance to enhance tool access an MCP server provides

**Key Techniques**:
- Coordinates multiple MCP calls in sequence
- Embeds domain expertise
- Provides context users would otherwise need to specify
- Error handling for common MCP issues

**Real example**: `sentry-code-review` skill (Sentry)

### Approach Selection: Problem-first vs Tool-first

| Approach | When | User Mindset |
|----------|------|-------------|
| **Problem-first** | "I need to set up a project workspace" | Describes outcomes; skill handles tools |
| **Tool-first** | "I have Notion MCP connected" | Has access; skill provides expertise |

> Most skills lean one direction. Knowing which framing fits the use case helps choose the right pattern.

---

## 2. Five Official Patterns

> These are implementation patterns for Claude skill design. For inter-agent structural patterns, see Section 7.

### Pattern 1: Sequential Workflow Orchestration

**Use when**: Users need multi-step processes in a specific order.

```markdown
## Workflow: Onboard New Customer
### Step 1: Create Account
Call MCP tool: `create_customer`
Parameters: name, email, company
### Step 2: Setup Payment
Call MCP tool: `setup_payment_method`
Wait for: payment method verification
### Step 3: Create Subscription
Call MCP tool: `create_subscription`
Parameters: plan_id, customer_id (from Step 1)
### Step 4: Send Welcome Email
Call MCP tool: `send_email`
Template: welcome_email_template
```

**Key Techniques**: Explicit step ordering, dependencies between steps, validation at each stage, rollback instructions for failures

---

### Pattern 2: Multi-MCP Coordination

**Use when**: Workflows span multiple services.

**Example**: Design-to-development handoff

| Phase | Service | Actions |
|-------|---------|---------|
| 1. Design Export | Figma MCP | Export assets, generate specs, create manifest |
| 2. Asset Storage | Drive MCP | Create folder, upload assets, generate links |
| 3. Task Creation | Linear MCP | Create tasks, attach links, assign team |
| 4. Notification | Slack MCP | Post summary to #engineering with links and refs |

**Key Techniques**: Clear phase separation, data passing between MCPs, validation before next phase, centralized error handling

---

### Pattern 3: Iterative Refinement

**Use when**: Output quality improves with iteration.

```markdown
## Iterative Report Creation
### Initial Draft
1. Fetch data via MCP
2. Generate first draft report
3. Save to temporary file
### Quality Check
1. Run validation script: `scripts/check_report.py`
2. Identify issues (missing sections, formatting, data errors)
### Refinement Loop
1. Address each identified issue
2. Regenerate affected sections
3. Re-validate
4. Repeat until quality threshold met
### Finalization
1. Apply final formatting
2. Generate summary
3. Save final version
```

**Key Techniques**: Explicit quality criteria, iterative improvement, validation scripts, knowing when to stop

---

### Pattern 4: Context-Aware Tool Selection

**Use when**: Same outcome, different tools depending on context.

**Example**: Smart file storage with decision tree

| Condition | Tool |
|-----------|------|
| Large files (>10MB) | Cloud storage MCP |
| Collaborative docs | Notion/Docs MCP |
| Code files | GitHub MCP |
| Temporary files | Local storage |

**Key Techniques**: Clear decision criteria, fallback options, transparency about choices (explain to user why that tool was chosen)

---

### Pattern 5: Domain-Specific Intelligence

**Use when**: Skill adds specialized knowledge beyond tool access.

**Example**: Financial compliance in payment processing

```markdown
### Before Processing (Compliance Check)
1. Fetch transaction details via MCP
2. Apply compliance rules:
   - Check sanctions lists
   - Verify jurisdiction allowances
   - Assess risk level
3. Document compliance decision
### Processing
IF compliance passed → process transaction
ELSE → flag for review, create compliance case
### Audit Trail
- Log all compliance checks
- Record processing decisions
- Generate audit report
```

**Key Techniques**: Domain expertise embedded in logic, compliance before action, comprehensive documentation, clear governance

---

### Pattern Selection Guide

| Your Need | Primary Pattern | Secondary Pattern |
|-----------|----------------|-------------------|
| Ordered multi-step process | Sequential Workflow | — |
| Cross-service coordination | Multi-MCP Coordination | Sequential Workflow |
| Quality-sensitive output | Iterative Refinement | Sequential Workflow |
| Context-dependent routing | Context-Aware Tool Selection | Domain-Specific Intelligence |
| Regulatory/domain constraints | Domain-Specific Intelligence | Sequential Workflow |
| Complex workflow spanning services + quality | Multi-MCP Coordination | Iterative Refinement |

---

## 3. Planning Methodology

### Use Case Definition Template

```
Use Case: [Name]
Trigger: [What user says or does]
Steps:
1. [Action with tool/MCP reference]
2. [Action]
3. [Action]
Result: [Expected outcome]
```

### Technical Requirements Checklist

1. **Tools inventory**: Built-in capabilities vs MCP requirements
2. **File structure**: `SKILL.md` + `scripts/` + `reference/` + `assets/`
3. **Dependencies**: Environment requirements → `compatibility` field
4. **Folder naming**: kebab-case, matching `name` field

### Planning Questions

- What does a user want to accomplish?
- What multi-step workflows does this require?
- Which tools are needed (built-in or MCP)?
- What domain knowledge or best practices should be embedded?

---

## 4. Success Criteria Framework

### Quantitative Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Trigger accuracy | 90%+ on relevant queries | 10-20 test queries, track auto-load rate |
| Workflow efficiency | X tool calls (baseline comparison) | Same task with/without skill |
| API reliability | 0 failed calls per workflow | MCP server logs, retry rates |

### Qualitative Metrics

| Metric | Assessment |
|--------|-----------|
| Self-guided completion | Users don't need to prompt Claude about next steps |
| Correction-free execution | Same request 3-5 times yields consistent quality |
| First-try accessibility | New user accomplishes task with minimal guidance |

### Baseline Comparison Template

| Dimension | Without Skill | With Skill |
|-----------|--------------|------------|
| User instructions | Provided each time | Automatic |
| Back-and-forth | ~15 messages | ~2 clarifying questions |
| Failed API calls | ~3 requiring retry | 0 |
| Token consumption | ~12,000 | ~6,000 |

> Note: These are aspirational targets — rough benchmarks rather than precise thresholds. Anthropic is actively developing more robust measurement guidance and tooling.

### Empirical Evidence for Skill Impact

A production deployment quantifies how much externalizing procedural knowledge into skills matters: in Anthropic's internal self-service analytics agent, the same task scored **21% accuracy without skills and consistently above 95% with skills** — the largest single lever in the stack. The transferable lesson for skill design: the bottleneck is rarely the model's raw capability or its access to information, but whether procedural knowledge (table grain, scope, exclusions, gotchas, common patterns) is encoded as a retrievable, LLM-readable skill. Auto-generating that knowledge with an LLM *failed* — it encoded ambiguity instead of resolving it; human curation of the reference material remained essential. [Source: claude.com — *How Anthropic Enables Self-Service Data Analytics with Claude*]

---

## 5. Progressive Disclosure Design Principle

### Three-Level System

| Level | Content | Loading | Design Goal |
|-------|---------|---------|-------------|
| **1st** | YAML frontmatter | Always in system prompt | Minimal: just enough for Claude to know WHEN to use |
| **2nd** | SKILL.md body | When skill judged relevant | Full instructions, core workflow |
| **3rd** | `reference/`, `scripts/`, `assets/` | On-demand navigation | Detailed docs, validation, templates |

### Application in Design

- **SKILL.md**: Keep under 5,000 words. Focus on core instructions.
- **reference/**: Detailed API patterns, rate limiting, pagination, error codes
- **scripts/**: Deterministic validation (code > language instructions for critical checks)
- **assets/**: Templates, fonts, icons used in output

---

## 6. Composability Principle

### Portability

- Skills work identically across **Claude.ai**, **Claude Code**, and **API**
- Create once, works across all surfaces
- Note environment dependencies in `compatibility` field

### MCP Complementarity (Kitchen Analogy)

| | MCP | Skills |
|---|-----|--------|
| **Metaphor** | Professional kitchen | Recipes |
| **Provides** | Tool access, real-time data | Workflows, best practices |
| **Answers** | What Claude **can** do | How Claude **should** do it |

### Multi-Skill Coexistence

- Skills should work alongside others
- Don't assume exclusive capability
- Design for composition, not isolation

### Distribution Considerations

| Surface | Capability |
|---------|-----------|
| Claude.ai | Upload via Settings > Capabilities > Skills |
| Claude Code | Place in skills directory |
| API | `/v1/skills` endpoint, `container.skills` parameter |
| Organization | Admin workspace-wide deployment |

---

## 7. Agentic Composable Patterns (Anthropic 2025-2026)

> Source: Anthropic "Building effective agents" (2025) + subsequent updates (2026)

The 5 patterns in Section 2 are intra-skill implementation patterns. This section covers inter-agent and inter-workflow structural patterns.

### Design Philosophy: Simplicity First

The key to successful agent systems is to start with the simplest possible configuration and only add complexity when there is measurable improvement. Rather than introducing frameworks or orchestration layers upfront, build up from composable primitive patterns as needed.

### Pattern A: Prompt Chaining

**Structure**: Fixed-step sequential pipeline. Each step's output becomes the next step's input.

```
Step 1 → Gate ✓ → Step 2 → Gate ✓ → Step 3 → Output
                ✗ → Abort/Retry
```

**When to use**: Tasks naturally decompose into independent subtasks, and you want to gate quality at each step.
**Skill design implication**: Superset of Sequential Workflow Orchestration (Pattern 1). Explicitly insert gates (quality checks, approvals, validations) between steps.

### Pattern B: Routing

**Structure**: Classify input and dispatch to specialized handlers.

```
Input → Classifier → Handler A (domain 1)
                   → Handler B (domain 2)
                   → Handler C (domain 3)
```

**When to use**: Different input types require different optimal processing paths. Each path can be optimized independently.
**Skill design implication**: Generalization of Context-Aware Tool Selection (Pattern 4). Nexus routing logic is a canonical example. Use `Output Routing` tables to make branching conditions explicit.

### Pattern C: Parallelization

**Structure**: Execute tasks concurrently and aggregate results. Two variants:

| Variant | Description | Example |
|---------|-------------|---------|
| **Sectioning** | Split task into independent parts for parallel processing | Concurrent review of multiple files |
| **Voting** | Execute the same task multiple times and aggregate results | Multi-perspective evaluation, consensus judgment |

**When to use**: Subtasks are independent (Sectioning), or reliability/diversity is needed (Voting).
**Skill design implication**: Nexus chains and Rally (Sectioning) are existing implementations. Specify parallelizable partners in `COLLABORATION_PATTERNS`.

### Pattern D: Orchestrator-Worker

**Structure**: Central orchestrator dynamically decomposes tasks and delegates to workers.

```
Orchestrator → [dynamic task decomposition]
  → Worker 1 (Task A)
  → Worker 2 (Task B)
  → Worker N (Task N)
Orchestrator ← [result synthesis]
```

**When to use**: Task decomposition cannot be predicted in advance and requires runtime judgment.
**Skill design implication**: Nexus Hub-and-Spoke model and Titan's 9-phase lifecycle exemplify this pattern. Ensure hub compatibility via the `Nexus Compatibility` section.

### Pattern E: Evaluator-Optimizer

**Structure**: Generate → Evaluate → Improve feedback loop.

```
Generator → Output → Evaluator → Feedback
    ↑                                 │
    └─────────── Refine ──────────────┘
```

**When to use**: Clear evaluation criteria exist, and iterative refinement improves quality.
**Skill design implication**: Structured version of Iterative Refinement (Pattern 3). Judge→Builder feedback loop is a canonical example. Extract evaluation criteria into `reference/` and separate generation from evaluation responsibilities.

### Pattern F: Autonomous Agent

**Structure**: Autonomously loop tool usage based on environment feedback.

```
while (!done) {
  Observe → Plan → Act (tool use) → Evaluate result
}
```

**When to use**: Exploratory tasks, multi-stage problem solving, or tasks requiring environment interaction.
**Skill design implication**: Scout (bug investigation) and Vector (browser automation) are existing implementations. Always design loop termination conditions and guardrails (max iterations, timeouts, safety constraints).

### Existing ↔ Agentic Pattern Mapping

| Agentic Pattern | Closest Existing Pattern (Section 2) | Relationship | Ecosystem Example |
|----------------|--------------------------------------|--------------|-------------------|
| A: Prompt Chaining | P1: Sequential Workflow | P1 is a concrete impl of A | Orbit (runner scripts) |
| B: Routing | P4: Context-Aware Tool Selection | P4 is B specialized for tool selection | Nexus (Output Routing) |
| C: Parallelization | — (new) | No existing pattern | Rally (Sectioning) |
| D: Orchestrator-Worker | P2: Multi-MCP Coordination | P2 is D specialized for MCP | Nexus, Titan |
| E: Evaluator-Optimizer | P3: Iterative Refinement | P3 is a self-contained version of E | Judge↔Builder loop |
| F: Autonomous Agent | P5: Domain-Specific Intelligence | P5 adds domain knowledge to F | Scout, Vector |

---

## 8. Simplicity-First Design Principle

### Decision Ladder

A framework for progressively escalating agent system complexity. Do not advance to a higher level if the lower level can solve the problem.

| Level | Composition | When to Use |
|-------|-------------|-------------|
| **L0** | Single prompt + retrieval | One-shot Q&A, knowledge lookup |
| **L1** | Single prompt + tools | Single task with external integration |
| **L2** | Prompt Chaining / Routing | Fixed-flow multi-stage processing |
| **L3** | Orchestrator-Worker / Evaluator-Optimizer | Dynamic task decomposition or iterative refinement needed |
| **L4** | Multi-Agent Autonomous | Multiple autonomous agents cooperating |

### Application to Skill Design

- **ENVISION phase**: Map requirements to the Decision Ladder and identify the minimum level.
- **DESIGN phase**: Apply the Agentic Pattern corresponding to the chosen level. Document specific reasons before escalating to a higher level.
- **VALIDATE phase**: Verify the final design uses the minimum necessary complexity.

---

## 9. Interoperability Awareness

### MCP (Model Context Protocol)

Industry-standard protocol connecting AI models to external services and data sources.

- When a skill depends on MCP servers, declare it explicitly in the `compatibility` field.
- Skills in the MCP Enhancement category (Section 1) assume MCP server availability.
- Recommend **graceful degradation** so basic functionality works without MCP.

### A2A Protocol (Agent-to-Agent)

Agent-to-agent communication protocol proposed by Google. Defines capability advertisement via Agent Cards and task-based asynchronous communication.

- No direct impact on skill design at present, but recognized as a future consideration.
- The ecosystem's `CAPABILITIES_SUMMARY` is conceptually equivalent to Agent Card capability advertisement.
- The Nexus Hub-and-Spoke model is structurally similar to A2A's task delegation pattern.

### Agent Harness Pattern (Anthropic 2026)

State management pattern for long-running agents. Structures interruption, resumption, and state recovery.

- Limited direct applicability since the current ecosystem uses a 1-session = 1-task model.
- However, Orbit's `state files` and Rally's `multi-session` design are partial implementations of this pattern.
- Recorded as a reference pattern for future cross-session design.

---

## 10. Intelligence Harnessing Principles

> Source: Anthropic "Harnessing Claude's Intelligence" (2025)

Three design principles for building agent systems that adapt to evolving model capabilities. These principles complement the Simplicity-First Decision Ladder (Section 8) with empirical evidence and concrete design rules.

### 10.1 General Tools Over Specialized Tools

Prefer composing general-purpose tools (bash, text editor, file I/O) into patterns over building specialized single-purpose tools.

| Evidence | Result |
|----------|--------|
| SWE-bench Verified (2025-Q1 historical reference) | Claude 3.5 Sonnet achieved 49% using only bash + text editor. Current Claude 4.x results have surpassed this number; the historical figure is preserved here to anchor the design rule that simple tools + good models often beat custom-tool architectures. |

**Design rule**: Skills, programmatic tool calling, and memory systems should build on general tool composition. Create specialized tools only when general composition is insufficient — and only when one of the four boundary conditions in Section 10.3 is met.

### 10.2 "What Can I Stop Doing?" Audit

Systematically question whether each piece of orchestration scaffolding is still necessary as model capabilities improve. Three audit dimensions:

| Dimension | Principle | Evidence (as of 2025) | Design Implication |
|-----------|-----------|----------------------|-------------------|
| **Orchestration** | Let agents write code to filter tool outputs instead of routing all results through context | BrowseComp: 45.3% → 61.6% with self-filtering (2025-era Opus-class measurement; not re-verified on Opus 5) | Design agents with code execution for output filtering; avoid piping all tool results through context window |
| **Context management** | Progressive disclosure via skills instead of pre-loading all instructions | See Section 5 (Three-Level System) | Keep L1 frontmatter minimal; load L2/L3 on demand |
| **Persistence** | Memory folders (file-based) vs compaction (in-context summarization) | BrowseComp: 84% with memory folders (2025-era Opus-class measurement) vs 43% flat (Sonnet 4.5); not re-verified on Opus 5 | For Opus-class models, design for file-based persistence; for Sonnet-class, keep context in-window. Effectiveness is model-dependent |

**Application**: Use `_common/HARNESS_EVOLUTION.md` Systematic Scaffold Audit protocol to evaluate each scaffolding component against these dimensions.

### 10.3 Boundary-Aware Design

Three sub-principles for setting effective boundaries without introducing dead weight:

**Prompt caching optimization**: Structure context with stable content first (system prompts, tool definitions, skill instructions), then dynamic content (user input, conversation history, retrieved context). Cached tokens cost 10% of base input tokens. Use ToolSearch for dynamic tool discovery to avoid bloating the static tool list and breaking cache prefixes.

**Declarative tool promotion criteria**: Promote an action from general tool composition to a dedicated declarative tool ONLY when it crosses one of four thresholds:

| Threshold | Rationale | Example |
|-----------|-----------|---------|
| Security boundary | Credential isolation, input sanitization | API calls requiring auth tokens |
| Reversibility | Destructive actions need confirmation gates | Database writes, file deletion |
| UX presentation | Structured output for user-facing display | Rich UI rendering, formatted reports |
| Observability | Structured logging, audit trails | Compliance-sensitive operations |

If none of these thresholds apply, keep the action as a composed general-tool pattern.

**Dead weight pruning**: Every safeguard encodes an assumption about model limitations. Regularly audit whether these assumptions still hold. See `_common/HARNESS_EVOLUTION.md` for the evaluation cycle and simplification conditions.

---

## 11. Opus 5 Operating Principles for Generated Skills

> Source: Anthropic *Prompting Claude Opus 5* + *Migrating to Claude Opus 5* + *Effort* (platform.claude.com, verified 2026-07-25)
> Canonical detail: `_common/OPUS_5_AUTHORING.md` (P1–P11). This section mirrors it for the generation pass.

Opus 5 has sharp default behaviors that generated skills must author for explicitly. Apply these when designing new agents or updating existing ones. **Three defaults cost tokens on every workload and are the highest-value checks: long output (11.2), scope expansion (11.8), and automatic self-verification (11.9).**

### 11.1 Front-Loaded Task Specification

Opus 5 rewards complete first-turn intent over progressive disclosure across multiple turns, and uses more tokens when intent arrives progressively. Generated skills should bias users and orchestrators toward stating intent, constraints, acceptance criteria, and file locations up front, and minimize required user round-trips for interactive skills.

**Design rules**:
- Trigger Guidance section should explicitly list what callers must provide on the first turn (target files, success criteria, constraints).
- INTERACTION_TRIGGERS should batch multiple confirmations into a single multi-question prompt rather than serializing them across turns.
- AUTORUN `_AGENT_CONTEXT` schemas should require all decision-affecting inputs be present before execution begins; ambiguity should resolve to safe defaults with documentation, not to a follow-up question.

### 11.2 Explicit Length Control

Opus 5's default output runs **longer** than prior Opus models', in two independent channels — conversational responses and files written to disk. Effort controls thinking volume, not visible length, so lowering effort does not shorten output. Length must be prompted.

**Design rules**:
- Output sections (reports, handoffs, summaries) must specify length envelopes (line counts, bullet counts, or table dimensions).
- `_STEP_COMPLETE` and `## NEXUS_HANDOFF` blocks already provide structural envelopes — keep them; do not let agents emit free-form summaries instead.
- For user-facing prose, state length explicitly (e.g., "1-3 sentence summary", "5-bullet checklist").
- For skills that author documents to disk, add a separate calibration line: "Match the length of written documents to what the task needs; do not pad with filler sections, redundant summaries, or boilerplate."
- In a long SKILL.md, repeat a one-line brevity reminder near the end — a single top-of-file instruction under-steers.

### 11.3 Explicit Tool-Use Guidance

Effort governs tool-call volume: lower effort combines operations into fewer calls and acts without preamble; higher effort makes more calls and explains the plan first. Skills state "when" and "why" per tool and pick a baseline effort to match.

**Design rules**:
- For each tool a skill expects to use, document the trigger condition (when) and the value the tool provides (why).
- If a workflow benefits from eager tool use (e.g., reading multiple files to ground decisions), state it: "Read all candidate files before deciding, even if confidence seems sufficient — grounding cost is low compared to wrong-decision cost", and baseline it at `high`/`xhigh`.
- Conversely, for skills that should think before acting, state it: "Reason about the design before invoking tools; do not begin file reads until the section contract is decided."
- For vision/visual skills, give tools for iterative crop-and-verify — tool use is a more cost-effective lever than a larger reasoning budget.
- Web tooling is asymmetric on Opus 5: `web_search` is supported, `web_fetch` is not (the tool is GA and un-renamed — Opus 5 is just absent from its model list). Generate skills that reach the web via `web_search`, and where full-page/PDF content is genuinely required, make the fetch a separately-modelled step (Sonnet 5 / Fable 5) rather than an assumption.

### 11.4 Subagent Delegation Caps

Opus 5 **delegates to subagents readily** — the authoring job is to bound fan-out, not encourage it. Delegation pays off on large independent tracks and wastes tokens on small ones.

**Design rules**:
- State delegation criteria and a cap: "Delegate only for large, genuinely independent, parallelizable tasks. Do not delegate work finishable in a handful of tool calls, and do not use subagents to verify your own work. Prefer one subagent over several; keep spawn counts low."
- Multi-agent coordination is a strength (writer-verifier patterns work; agents rarely clobber each other) — keep independent-verifier architectures, cut self-check fan-out.
- Reference `_common/SUBAGENT.md` for the parallelism-layer decision (skill-internal subagents vs Agent Teams).

### 11.5 Thinking Is On By Default

Thinking runs on by default in adaptive mode. `thinking: {type: "disabled"}` is accepted only at effort `high` or below — pairing it with `xhigh`/`max` returns a 400 error. `max_tokens` caps thinking + response text together.

**Design rules**:
- Never author a skill that assumes thinking is off, and never instruct the model not to think or reason — such rules increase internal-XML-tag leakage.
- Steer depth instead of toggling: "Think carefully and step-by-step before responding; this decision affects [downstream impact]" at high-stakes points; "Prioritize responding quickly rather than thinking deeply" at throughput-sensitive ones.
- Control cost with lower effort, not by disabling thinking.
- Do not embed numeric thinking budgets — control depth via `effort` (11.6).

### 11.6 Effort-Level Awareness

The default effort level is **`high`** on the Claude API and Claude Code. Opus 5 supports all five levels and its effort scale was recalibrated — settings carried over from earlier models must be re-swept on real evals.

| Effort | When skills should expect this |
|--------|-------------------------------|
| `low` | Short scoped tasks, subagents, latency-sensitive work — genuinely stronger on Opus 5 than earlier Opus models |
| `medium` | Cost-saving step-down; viable for real agentic work wherever evals hold |
| `high` (default) | Complex reasoning, difficult coding, agentic tasks; equivalent to omitting the parameter |
| `xhigh` | Recommended starting point for coding/agentic and long-horizon (30 min+) work |
| `max` | Unconstrained token spend; can overthink simpler tasks — flag in `description` if a skill expects it |

If a skill's correctness depends on `xhigh`/`max`-level effort, state that expectation in the `description` and Trigger Guidance so callers can opt in, and note that `max_tokens` should start around 64k at those levels.

### 11.7 Delegation-Engineer Framing

Treat the model as a capable engineer being delegated to, not a line-by-line pair programmer. Skills should be authored to support coherent long sessions with infrequent check-ins.

**Design rules**:
- Skills must be self-directing for the bulk of their workflow; reserve user check-ins for genuine `Ask first` decisions.
- Provide enough context inside the skill (or via references) that the model does not need to ask clarifying questions for documented decisions.
- Avoid micro-step instructions that prevent the model from exercising judgment; prefer phase-level contracts with verification gates.

### 11.8 Scope Discipline — Both Directions

Two behaviors, opposite in sign. **(a)** Opus 5 can *expand* scope, adding steps that weren't requested or re-deciding what the task should be. **(b)** It follows *restrictive* instructions literally, so conservative phrasing suppresses output (see 11.10).

**Design rules**:
- Bound narrow tasks explicitly: "Deliver what was asked, at the scope intended. Make routine judgment calls yourself, and check in only when different readings would lead to materially different work. Finish the whole task, and stop short of actions clearly beyond what was asked." State what is out of scope.
- When an instruction should apply broadly, state the scope: "Apply this to **every** section/file/case, not just the first."
- For structured-extraction/pipeline skills, pin exact output schemas and field-level expectations.
- Audit generated SKILL.md files for restrictive phrasing that will be taken literally and cost coverage.

### 11.9 Delete Redundant Verification & Narration Scaffolding

**Opus 5 verifies its own work and catches its own mistakes unprompted.** Explicit "verify", "double-check", "re-verify before responding", or "use a subagent to verify" instructions compound with that behavior and cause over-verification — wasted tokens, no quality gain. The same applies to legacy harness scaffolding that bolts on self-check steps.

**Design rules**:
- Do not generate self-check / re-verification instructions in SKILL.md prompts or spawn templates.
- Distinguish **self**-verification from **independent** verification: a *different* agent checking a producer's output (`producer ≠ verifier`) is an architectural control and stays. Cut only agents told to re-check their own work.
- Remove forced interim-status scaffolding ("summarize every N tool calls"). If cadence matters, describe the shape with an example: one sentence before the first tool call, brief updates only on discovery or direction change, outcome-first close.
- Bound correction narration: "Only correct an earlier statement when the error would change the user's code, conclusions, or decisions; otherwise make the fix and move on."

### 11.10 Coverage-vs-Filter for Review & Detection Skills

Opus 5 reviews with high precision *and* recall, and accuracy holds at lower effort — but it follows conservative reporting instructions ("only high-severity", "don't nitpick") faithfully, so a harness tuned for older models shows *lower measured recall* (harness effect, not regression).

**Design rules (reviewers/detectors)**:
- Separate *finding* from *filtering*: at the finding stage instruct coverage ("report every issue including uncertain/low-severity; tag confidence + severity; a later stage ranks").
- Move confidence/severity filtering to a downstream verification/ranking stage.
- If self-filtering in one pass, set a **concrete** bar ("anything that could cause incorrect behavior, a test failure, or a misleading result"), not "important".
- Exploit effort-insensitivity: wide pass at `low`/`medium`, `xhigh` reserved for adjudication.
- Validate recall/F1 against an eval subset after prompt changes.

### 11.11 Voice & Artifact Defaults

Opus 5 prose trends direct/opinionated with sparing emoji and narrates self-corrections readily. Vision and UI/frontend visual replication are strong; it generates multi-sheet spreadsheets and structured slide decks but needs the target style or template supplied.

**Design rules**:
- For writer skills: state warmer/conversational tone explicitly when the product needs it; bound correction narration (11.9).
- For document/slide skills: pass the style or template in — do not rely on a house default.
- For design/frontend skills: give a concrete alternative palette/typography, or have the model propose 3–4 directions first — generic negation just shifts to another fixed palette. The warm-cream/serif house style observed on prior Opus models is **not documented for Opus 5**; treat it as unverified rather than assumed.

### 11.12 Application in Architect Phases

| Phase | Apply |
|-------|-------|
| `UNDERSTAND` | Confirm caller-provided context is complete (11.1); flag missing fields once, not iteratively |
| `DESIGN` | Bake length envelopes for both channels (11.2), tool-use rationale (11.3), delegation caps (11.4), thinking-on assumptions (11.5), scope bounds (11.8), and — for reviewers — coverage-vs-filter (11.10) into the section contract |
| `GENERATE` | Verify generated SKILL.md states effort-level expectations against a `high` default (11.6), delegation-engineer framing (11.7), scope bounds (11.8), carries **no** self-verification scaffolding (11.9), and (writers/designers) voice/artifact defaults (11.11) |
| `VALIDATE` | Add Opus 5 readiness checks to the validation pass — a skill that omits 11.2 / 11.8 / 11.9 guidance will over-produce, over-reach, and over-verify at runtime |
