# Opus 4.8 Authoring Protocol

> Source: Anthropic "Prompting best practices" — *Prompting Claude Opus 4.8* (platform.claude.com, 2026)
> Owner: Architect (canonical doc); referenced by orchestrators, reviewers, investigators
> Supersedes the former Opus 4.7 Authoring Protocol. Opus 4.8 performs well out of the box on existing 4.7 prompts, so P1–P7 still hold; P8–P11 capture 4.8-specific behavior shifts.

Shared protocol that aligns generated and existing skills with Opus 4.8 default behaviors. Reference this file from any SKILL.md that needs Opus 4.8 alignment instead of duplicating the rules.

---

## Why This Exists

Opus 4.8 keeps the 4.7 defaults but sharpens several behaviors. Skills tuned only for 4.6/4.7 will mis-trigger on these:

| Default | Opus 4.7 | Opus 4.8 |
|---------|----------|----------|
| Response length | Calibrated to complexity | Calibrated to complexity (sharper: shorter on lookups, longer on open-ended) |
| Effort | `xhigh` default | `xhigh` default, **respected strictly** — at `low`/`medium` it scopes to exactly what was asked |
| Tool calls | Reasons more, calls less | Favors reasoning even more; **raise effort** (not just prompt) to increase tool use |
| Instruction following | Mostly literal | **Strongly literal** — no silent generalization across items, no inferring unrequested work |
| Subagent spawning | Sparse | Sparse — still must be explicit |
| Thinking | Adaptive (per-step) | Adaptive, **off unless `thinking:{type:"adaptive"}`**; triggering is steerable |
| Progress updates | Manual scaffolding common | Native high-quality interim updates — remove forced "summarize every N calls" scaffolding |
| Prose voice | Neutral | Direct, opinionated, minimal validation-forward phrasing, sparing emoji |
| Frontend/visual | Generic-prone | Persistent "house style" (cream/serif/terracotta); needs concrete alternative, not negation |
| Code-review recall | Reports per stated bar | Follows "only high-severity / don't nitpick" **more faithfully** → measured recall can drop |

Apply the eleven principles below.

---

## The Eleven Principles

### P1. Front-Loaded Task Specification

State intent, constraints, acceptance criteria, and file locations on the first turn. Do not reveal requirements progressively.

**Apply by:**
- Trigger Guidance enumerates first-turn required inputs.
- INTERACTION_TRIGGERS batch related confirmations into a single multi-question prompt.
- AUTORUN `_AGENT_CONTEXT` schemas require all decision-affecting inputs up front; ambiguity resolves to safe defaults (documented), not follow-up questions.
- **4.8 note:** 4.8 is more autonomous and uses more tokens when intent arrives progressively across user turns. Well-specified first-turn task descriptions maximize both autonomy and token efficiency. For interactive coding skills, reduce required user round-trips and prefer an "auto mode".

### P2. Calibrated Response Length

Opus 4.8 calibrates verbosity to task complexity — sharper than 4.7. Skills must state expected output shape and length explicitly.

**Apply by:**
- Reference `_common/OUTPUT_STYLE.md` from the SKILL.md `Output Contract` section. That file is the single source of truth for tier definitions (`S`/`M`/`L`/`XL`), banned filler patterns, and format priority.
- Declare a default tier and per-task overrides in SKILL.md instead of duplicating style rules.
- Output sections specify length envelopes (line counts, bullet counts, table dimensions).
- `_STEP_COMPLETE` and `## NEXUS_HANDOFF` blocks already provide envelopes — keep them; do not let agents emit free-form summaries instead.
- For prose, state length explicitly: "1-3 sentence summary", "5-bullet checklist".
- **4.8 note:** to reduce verbosity, prefer positive concision examples ("Provide concise, focused responses. Skip non-essential context.") over negative "do not" instructions.

### P3. Explicit Tool-Use "When/Why"

Opus 4.8 favors reasoning over tool calls even more than 4.7. Skills that need aggressive tool execution must say so explicitly — and remember that **effort is the stronger lever** (see P9).

**Apply by:**
- For each tool a skill expects to use, document the trigger condition (when) and value (why).
- For eager tool use: "Read all candidate files before deciding, even if confidence seems sufficient — grounding cost is low compared to wrong-decision cost."
- For think-first behavior: "Reason about the design before invoking tools; do not begin file reads until the section contract is decided."
- **4.8 note:** if a skill under-uses a tool (e.g. web search), describe explicitly *why and how* it should be used, and assume `high`/`xhigh` effort — tool usage rises substantially with effort.

### P4. Explicit Parallel Subagent Triggers

Opus 4.8 spawns fewer subagents by default. Skills that benefit from parallel fan-out must spell it out.

**Apply by:**
- For independent subtasks (multi-file reads, multi-target analysis, voting/consensus), include: "Spawn N subagents in the same turn when fanning out across [items]."
- Pair with the inverse guard: "Do not spawn a subagent for work you can complete directly in a single response (e.g. refactoring a function you can already see)."
- Reference `_common/SUBAGENT.md` for the parallelism-layer choice (skill-internal subagents vs Agent Teams).
- Do not assume the model will infer parallelism from workflow structure alone.

### P5. Adaptive Thinking Hints

Thinking is off unless `thinking:{type:"adaptive"}` is set, and Opus 4.8 decides depth per step. Triggering is steerable. Skills steer this at decision points.

**Apply by:**
- High-stakes decisions: "Think carefully and step-by-step before responding; this decision affects [downstream impact]."
- Throughput-sensitive points: "Prioritize responding quickly rather than thinking deeply."
- If a large/complex SKILL.md makes the model think more often than wanted: "Thinking adds latency and should only be used when it will meaningfully improve answer quality — typically multi-step reasoning. When in doubt, respond directly."
- Do not embed numeric thinking budgets — they are deprecated; control depth via `effort` (P9).

### P6. Effort-Level Awareness

Default effort is `xhigh`, and 4.8 respects effort strictly. Skills should be sized for `xhigh` as the assumed runtime envelope and aware that low effort genuinely narrows scope.

| Effort | When skills should expect this |
|--------|-------------------------------|
| `low` | Short, scoped, latency-sensitive, non-intelligence-sensitive tasks; risk of under-thinking on anything moderately complex |
| `medium` | Cost-sensitive narrow scope; trades intelligence for tokens |
| `high` | Minimum for intelligence-sensitive work; balances tokens and intelligence |
| `xhigh` (default) | Best for most coding/agentic skills — design baseline |
| `max` | Genuinely hard problems; can overthink and show diminishing returns — flag in `description` if a skill expects `max` |

- **4.8 note:** effort matters more on 4.8 than any prior Opus. If reasoning is shallow on a complex task, raise effort rather than prompting around it. At `max`/`xhigh`, set a large `max_tokens` budget (start ~64k) so the model has room to think across tool calls and subagents.

### P7. Delegation-Engineer Framing

Treat the model as a capable engineer being delegated to, not a line-by-line pair programmer.

**Apply by:**
- Skills must be self-directing for the bulk of their workflow.
- Reserve user check-ins for genuine `Ask first` decisions, not micro-steps.
- Provide enough context inside the skill (or via references) that the model does not need to ask clarifying questions for documented decisions.
- Avoid micro-step instructions that prevent the model from exercising judgment; prefer phase-level contracts with verification gates.

### P8. Literal-Scope Instruction Following  *(new in 4.8)*

Opus 4.8 interprets instructions literally and explicitly, especially at lower effort. It does **not** silently generalize an instruction from one item to another, and it does **not** infer requests you didn't make. This yields precision and less thrash, but punishes implicit scope.

**Apply by:**
- State scope explicitly when an instruction should apply broadly: "Apply this to **every** section/file/case, not just the first."
- Don't rely on one worked example to imply a rule across the whole skill — state the rule, then exemplify.
- For structured-extraction / pipeline skills, this literalism is an asset: pin exact output schemas and field-level expectations.
- Audit existing SKILL.md for instructions that assumed the model would "fill in the obvious" — make the obvious explicit.
- Pairs with the anti-overengineering guard: 4.8 won't add unrequested features, abstractions, or defensive code — keep that intent, and request "above and beyond" explicitly when you actually want it.

### P9. Effort-Calibrated Tool Use & Native Updates  *(new in 4.8)*

Effort is the primary control surface on 4.8 — stronger than prompt wording — for both reasoning depth and tool-call volume. The model also emits good interim updates natively.

**Apply by:**
- For tool-eager skills (agentic search, multi-file coding), specify `high`/`xhigh` effort as the baseline rather than only adding "use the tool" prompts.
- For latency/cost-bounded skills held at `low`/`medium`, add a targeted nudge for the rare complex case ("This task involves multi-step reasoning; reason through it before responding.") instead of globally raising effort.
- Remove legacy scaffolding that forces interim status ("summarize progress every 3 tool calls") — 4.8 updates well on its own. If update cadence/shape matters, describe it explicitly with an example rather than a counter.
- Keep thinking off by default; only the workloads that need per-step reasoning should request adaptive thinking (P5).

### P10. Coverage-vs-Filter for Review & Detection Skills  *(new in 4.8)*

Opus 4.8 is better at finding bugs (higher recall and precision internally), but it follows conservative reporting instructions ("only high-severity", "be conservative", "don't nitpick") **more faithfully** than older models. A harness tuned for an older model can show *lower measured recall* — a harness effect, not a capability regression: same investigation depth, fewer findings converted to reports.

**Apply by (reviewers/detectors — Judge, Gauge, Sentinel, Radar, Attest, Canon, Probe, Warden, Drill, Vigil, Cull, Chain):**
- Separate *finding* from *filtering*. At the finding stage, instruct coverage explicitly: "Report every issue you find, including uncertain and low-severity ones. Do not filter for importance or confidence here — a later stage ranks them. Tag each with confidence + estimated severity."
- Move confidence/severity filtering to a downstream verification, dedup, or ranking stage.
- If self-filtering must happen in one pass, set a **concrete** bar, not a qualitative one: "report anything that could cause incorrect behavior, a test failure, or a misleading result; omit only pure style/naming nits."
- Validate recall/F1 against a known eval subset after any prompt change.

### P11. Calibrated Voice & Design Defaults  *(new in 4.8)*

**(a) Prose voice.** Opus 4.8 trends direct and opinionated, with minimal validation-forward phrasing and sparing emoji. Re-evaluate voice prompts against this baseline.
- If a product voice is warmer/more conversational, state it: "Use a warm, collaborative tone. Acknowledge the user's framing before answering."
- Relevant to Prose, Tone, Quill, Scribe, Cue, Zine, Crest, content/marketing skills.

**(b) Frontend & visual defaults.** Opus 4.8 has strong design instincts but a persistent house style — warm cream/off-white (~`#F4F1EA`), serif display type (Georgia/Fraunces/Playfair), italic accents, terracotta/amber. Great for editorial/hospitality/portfolio; wrong for dashboards, dev-tools, fintech, healthcare, enterprise. Appears in slides too.
- Generic negation ("don't use cream", "make it minimal") just shifts to *another* fixed palette. Two reliable breaks: (1) specify a concrete alternative (exact palette hexes, typography, radius, spacing); (2) have the model propose 3–4 distinct directions first, then implement the chosen one.
- 4.8 needs *less* anti-"AI slop" prompting than prior models — a short `<frontend_aesthetics>` snippet suffices.
- Relevant to Vision, Muse, Palette, Flow, Forge, Artisan, Funnel, Bazaar, Vitrine, Stage, frontend skills.

---

## Per-Role Apply Matrix

Reference this matrix to know which principles your skill must address.

| Role | Critical (◎) | Recommended (○) |
|------|---|---|
| Orchestrators (Nexus, Titan, Sherpa, Rally, Arena, Magi, Darwin, Orbit) | P4, P6, P7, P9 | P1, P8 |
| Investigators (Scout, Lens, Trail, Atlas, Fossil, Triage) | P3, P5, P8 | P2, P9 |
| Reviewers/Detectors (Judge, Gauge, Sentinel, Probe, Radar, Warden, Attest, Canon, Drill, Vigil, Cull, Chain) | P2, P5, P10 | P1, P8 |
| Builders (Builder, Artisan, Forge, Anvil, Native) | P5, P7, P8 | P3, P9, P11 |
| Designers (Vision, Muse, Palette, Schema, Gateway, Stratum, Flow) | P1, P11 | P5, P8 |
| Writers (Prose, Tone, Quill, Scribe, Cue, Zine, Crest) | P2, P11 | P8 |
| Knowledge/Meta (Lore, Compass, Sigil, Architect) | P6, P7, P8 | P1, P9 |

(◎ = address explicitly in SKILL.md; ○ = address if relevant)

P8 (literal-scope following) applies to **every** role — make implicit scope explicit regardless of domain.

---

## Validation Hooks

When validating a skill against this protocol, use the eleven checks below (mirrors Architect `validation-checklist.md` Section 7):

- R7.1 Front-loaded context capture
- R7.2 Calibrated response length
- R7.3 Explicit tool-use rationale
- R7.4 Parallel subagent triggers
- R7.5 Adaptive thinking hints
- R7.6 Effort-level expectations declared
- R7.7 Delegation-engineer framing
- R7.8 Literal-scope: broad-application instructions state their scope explicitly
- R7.9 Effort-calibrated tool use; no legacy forced-progress scaffolding
- R7.10 (reviewers/detectors) Coverage-vs-filter separation; concrete severity bar
- R7.11 (writers/designers) Voice baseline re-evaluated; design defaults broken with concrete specs or option-proposal

Pass criterion: skills must address all `◎` principles for their role; aim for ≥ 7/11 total.

---

## How to Reference This File

In a SKILL.md:

```markdown
- Author for Opus 4.8 defaults. See `_common/OPUS_48_AUTHORING.md` (apply P[X], P[Y], P[Z] for this role).
```

Avoid duplicating the principle text in individual SKILL.md files. Cite by ID (P1–P11) and let this file be the single source of truth.
