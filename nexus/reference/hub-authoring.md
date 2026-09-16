# Hub-Engine Authoring

Canonical spawn brief and adapter selection for the orchestration control plane. Domain methods remain in the selected skill. Current model IDs, CLI flags, paths and release facts live only in `_common/CLI_COMPATIBILITY.md`; load it when binding or changing a runtime, not once per task step.

## Orchestrator Detection

Use the host's identity and advertised tool schemas. A familiar tool name alone does not identify a CLI or prove a capability. Discover native spawning, capacity/nesting, join/resume, permissions and result channels once; refresh after a configuration change or capability failure.

| Verified host | Adapter | Required evidence |
|---------------|---------|-------------------|
| Claude Code | `_common/CLI_COMPATIBILITY.md` + shared P-principles | Available agent interface, allowed tools and effective grants |
| Codex CLI | `_common/CODEX_ORCHESTRATION.md` | Advertised subagent tools, capacity and supported configuration |
| Antigravity CLI | `_common/AGY_ORCHESTRATION.md` | Installed version/help, authorized model selection and headless result schema |
| Other / unknown | `_common/CLI_COMPATIBILITY.md` | Discover an equivalent capability; never guess a spawn command |

Verified unavailability follows `reference/execution-layers.md` and SKILL.md Core Rule #3. Record the discovery evidence; do not simulate multiple independent specialists inside one context.

## Claude Code hub

Apply `_common/OPUS_5_AUTHORING.md` P4/P6/P7/P9: bounded delegation, inherited authorized model/effort, complete outcome briefs, and concrete validation instead of generic self-check exhortations. Native background execution is useful only for independent work. Worktrees isolate writes, not semantic integration.

## Claude Code hub — Fable 5

Legacy heading and F1–F8 identifiers remain for existing references; these are portable controls, **not a model-specific override**. Generation facts and optional API features must be verified in the compatibility layer.

- **F1 — No reasoning reproduction.** Request decisions, evidence and concise rationale, never private reasoning transcripts.
- **F2 — Whole-job delegation.** Supply the outcome, relevant context, authority and acceptance criteria. Do not split a specialist's reasoning into mandatory micro-prompts.
- **F3 — Effort follows evidence.** Inherit the authorized setting. Change only to a value the selected runtime supports and when task evaluation justifies its cost.
- **F4 — Dependency-aware concurrency.** Run independent branches concurrently within the authorized budget; join before dependent work or final reporting. Checkpoint long jobs using supported mechanisms.
- **F5 — Grounded progress.** Bind status claims to observed tool results and the correct revision/run; distinguish plans, attempts and verified effects.
- **F6 — Refusal-aware routing.** Distinguish policy refusal from transport/quota failure. Never switch models, rephrase a prohibited goal or retry to circumvent a safety refusal. Explain the boundary; pursue only permitted alternatives. Do not infer billing from an HTTP status.
- **F7 — User-visible delivery.** Use only an available, authorized output channel. Preserve exact artifacts when required; do not invent a `send_to_user` tool or assume a transport preserves content verbatim.
- **F8 — Cost gate.** Ask before an unapproved model, effort, concurrency or spend escalation. Existing explicit authorization need not be requested again merely because a task is simple. This gate remains binding in AUTORUN modes.

## Codex CLI hub

Use `_common/CODEX_ORCHESTRATION.md` C1/C2/C6 for capacity, fan-out/join and checkpoint/resume. C3 selects supported authorized models, not a frozen generation or fabricated variants. C7 preserves sandbox and approval boundaries.

## agy hub

Use `_common/AGY_ORCHESTRATION.md` A1–A9. Prefer documented headless structured output and scoped permissions. PTY/file capture is a **verified legacy workaround**, not the normal path. A9-D no longer appends a forced-thinking block. A missing artifact, denied required tool or failed result cannot become “no findings.”

## Agent Spawn Template

The following is a **prompt brief, not an API argument schema**. Pass it through the discovered spawn interface. Fill the existing handoff contract instead of adding a second competing schema.

```text
Skill: [resolved SKILL.md; load its applicable contracts and task-specific references]
Task: [complete bounded outcome, intended audience]
Recipe: [selected recipe, or none]
Inputs: [revision/run, relevant files, evidence, prerequisite outputs]
Acceptance criteria: [frozen AC IDs and observable checks]
Output length envelope: [appropriate ceiling; full artifacts may be separate files]
Scope bound: [in-scope deliverables / non-goals / exclusive file ownership]
Prohibited outcomes: [inherited constraints, or none]
Authority: allowed=[authorized effects]; denied=[excluded effects]; redelegation=false
Completion bound: finish all in-scope items without lowering the ACs; run applicable
  checks and report actual results. A skeleton, TODO or untested claim is not SUCCESS.
  Residuals require a class: blocked-external | gate-pending | out-of-contract |
  budget-exhausted. For BLOCKED, name the failed permitted alternative; never try
  an unsafe action merely to satisfy this field.

Return the contracted _STEP_COMPLETE / NEXUS_HANDOFF with deliverables, status,
revision-bound evidence, typed residuals and next action. Open with the outcome.
```

**Mandatory controls:** Recipe, acceptance criteria, output envelope, scope, prohibited outcomes, authority and completion bound. Tool-specific directions are conditional on a real integration need; the old `Thinking directive` is retired. The brief must not demand private reasoning or duplicate the specialist's methodology.

The hub owns aggregate constraints and independent completion sweeps (Q18–Q19); producer tests remain necessary but are not independent verification (Q9). `Authority` bounds effects, not just files, and cannot enlarge the hub's own grant. Wider effects return for approval. See `reference/autonomy-quality-protocol.md` §0, §7 and §8; `_common/HANDOFF.md` remains the wire contract.

## Spawn Template Variants

The same brief applies to every engine. Adapt only skill-path resolution, available tool/result schemas, scope isolation and checkpoint mechanics through `_common/CLI_COMPATIBILITY.md`. Never append duplicated generation-specific prose. `reference/adaptive-prompt-policy.md` may shorten or select directives but cannot relax ACs, authority or prohibited outcomes.

## Execution-Layer Key Rules

`reference/execution-layers.md` owns verified spawn/fallback choice; the compatibility layer owns runtime workarounds. Permission bypass is neither a headless prerequisite nor a substitute for a grant. Check actual result content, required effects and command outcomes before aggregation.

## Model Selection

Inherit the explicit authorized choice. Without one, select a currently available stable model supported by the host and task budget using `_common/CLI_COMPATIBILITY.md` §4. Planning, implementation and verification may have different capability needs; use measured task results rather than vendor stereotypes to choose. No preview/restricted model, effort or paid escalation is automatic.

Record a concrete model ID and version when the host exposes them, otherwise `未確認`; do not invent IDs or assert that an alias is a reproducible snapshot. Current prices, context limits and API-only advisor features require official verification before use.

## Operational Notes for Spawns

- **Scoring:** use evidence bands and typed blocking unknowns in `confidence-scoring.md`; do not average away unresolved authority, scope or goals.
- **References:** open applicable contracts once per context and only the domain references needed for the task; carry critical constraints explicitly across isolated contexts.
- **Output:** follow `_common/HANDOFF.md`; a successful process is not a verified deliverable.
- **State:** track phase and step; use full `_NEXUS_STATE` for 4+ step chains. Resume with revision, evidence and residuals, not the full transcript.
- **Roles:** preserve specialist ownership and the independent verifier; personality and model identity do not grant authority.
