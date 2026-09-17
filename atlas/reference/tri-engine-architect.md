# Multi-Engine Architecture Deliberation

Load only for `/atlas multi`. Shared dispatch, capability/authorization, capture and degraded-mode rules: `_common/MULTI_ENGINE_RECIPE.md` and `_common/CLI_COMPATIBILITY.md`. This is Pattern H: smell confidence and option diversity are separate axes.

## SCOPE / FAN-OUT

Supply the same actual scope, concern (greenfield/bottleneck/debt/modernization/boundary), forces (scale, team, regulation, deployment, latency), prior ADRs/graph/metrics and must-keep/banned/runtime constraints to every selected engine. Names: `architect-codex`, `architect-agy`, `architect-claude`; bind invocation through the shared CLI adapter, not a copied wrapper.

Ask for 2–3 smells and 1–2 options per engine. Do **not** provide MADR/42010 templates, preferred styles (including Modular Monolith/Vertical Slice) or fitness-function catalogs to the independent analysts; apply those in main-context synthesis. Require a named style, both positive and negative trade-offs, migration/rollback and reversibility per option. Never invent a module or measured value. Re-emit Markdown as JSON before integration.

## Two-Stream Payload

```json
{
  "engine": "codex|agy|claude",
  "architectural_smells": [
    {
      "smell": "Cyclic dependency between Auth and Billing modules",
      "evidence": "file/path or metric — Ca=12, Ce=9, instability I=0.43",
      "severity": "CRITICAL|HIGH|MEDIUM|LOW",
      "concern_class": "coupling|cohesion|layering|boundary|complexity|scalability|reliability|evolvability"
    }
  ],
  "adr_options": [
    {
      "option_name": "Extract shared Identity module via Dependency Inversion",
      "architectural_style": "Layered | Hexagonal | DDD | Event-Driven | Modular-Monolith | Microservices | CQRS | Vertical-Slice | Pipeline | Plugin",
      "problem_statement": "Forces at play — what the decision must reconcile",
      "recommendation": "One-paragraph description of the proposed approach",
      "trade_offs": {
        "positive": ["consequence 1", "consequence 2"],
        "negative": ["consequence 1", "consequence 2"]
      },
      "risks": ["risk 1 with likelihood/impact", "risk 2"],
      "migration_strategy": "Strangler Fig phases | Branch-by-Abstraction | Big-bang justification | Incremental refactor sequence",
      "rollback_plan": "Concrete rollback step or feature-flag fallback",
      "fitness_function": "CI-integrated check that would detect regression (ArchUnit / dependency-cruiser / custom rule)",
      "effort_class": "S|M|L|XL",
      "reversibility": "TYPE-1 (one-way door) | TYPE-2 (reversible)"
    }
  ],
  "engine_notes": "Optional: evidence or uncertainty affecting this engine output"
}
```

## CLUSTER / SCORE

Cluster smells only when subject (module/boundary/SCC), `concern_class` and semantic concern all match. Cluster options only when **architectural style, primary intervention and migration-strategy class all match**. Options for the same problem in different styles stay separate. Record the engine set and addressed smell-cluster IDs for each option.

Use the actual usable-engine denominator from the shared contract. With three engines: smells 3/3 CONFIRMED, 2/3 LIKELY, 1/3 CANDIDATE; options 3/3 CONVERGENT, 2/3 CONVERGENT-PARTIAL, 1/3 DIVERGENT-{style}. With two: 2/2 is full convergence, 1/2 is candidate/divergent, and LIKELY is unavailable. A healthy two-engine run is not a failed three-engine run.

Promote grounded convergence to the recommendation; preserve grounded dissent as named alternatives with a rejection reason and reconsideration trigger. Do not fabricate an engine dissent when none exists, or discard a viable style because only one engine proposed it.

## GROUND — Main Context

For each smell, verify cited entities/edges/metrics, check mitigation by existing ADR/refactor/fitness functions, and calibrate severity against `reference/coupling-metrics.md`. Record VERIFIED / LIKELY-VERIFIED / REJECTED-{reason} / NEEDS-INFO under the shared rubric.

For each option, verify feasibility against actual constraints and TYPE-1/TYPE-2 reversibility against the blast radius. Apply `reference/adr-rfc-templates.md`'s completion checks: no benefits-only/strawman/fashion-driven proposal, no missing downstream/operations perspective, and no distributed-monolith synchronous-chain trap. Record VERIFIED / REJECTED-{reason} / NEEDS-TRADE-OFF. Concurrence never establishes existence or removes the grounding requirement.

## SYNTHESIZE / PRESENT

Emit one consensus ADR at `docs/architecture/decisions/ADR-NNNN-{slug}.md` (respect an existing project convention), or the requested RFC from `reference/adr-rfc-templates.md`. Preserve its narrative, and add:

```yaml
status: Proposed
date: YYYY-MM-DD
deciders: [team or stakeholder list]
tri_engine:
  engines_run: [actual engines]
  engines_failed: [failed engines or none]
  smell_confidence: CONFIRMED=N, LIKELY=N, VERIFIED-CANDIDATE=N
  option_perspective: CONVERGENT=N, CONVERGENT-PARTIAL=N, DIVERGENT=N
```

Required additions to the base artifact:
- Context grounded in verified smells; decision drivers; named considered options with engine/confidence/perspective attribution; chosen option and the main context's own constraint-based rationale.
- **Trade-off matrix** across recommendation and dissent: coupling impact, operational burden, migration cost, reversibility, team-topology fit and fitness-function coverage.
- Positive/negative consequences and risks, including risks avoided by dissenting options. For each dissenting option: style, trade-offs, risks, migration, reversibility, why not chosen, and the condition for reconsideration.
- Chosen migration strategy, concrete rollback, fitness-function specification, and appropriate next-agent handoff.
- Engine status, smell coverage, style diversity/coverage gaps, confidence/perspective distributions and condensed rejection counts by reason. Keep rejected material and raw engine output out of the main narrative.

With one usable engine label the artifact single-engine, never consensus; retain defensible alternatives without false attribution. With zero use `adr`; trivial local choices route to `analyze`/Zen.
