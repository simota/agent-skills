# Spark Proposal Templates Reference

Purpose: define the canonical feature proposal structure and the interaction templates Spark may use to clarify scope or validation choices.

Related: for the inter-agent handoff packet shapes that feed into or out of these proposals (e.g. `ECHO_TO_SPARK_HANDOFF`, `SPARK_TO_SHERPA_HANDOFF`), see `reference/collaboration-patterns.md`.

## Contents
- Full proposal template
- Minimal proposal template
- Decision policy example
- Interaction question templates

## Canonical Proposal Template

Use this structure for the default Spark deliverable:

```markdown
# Feature: [Feature Name]

## Input Sources
- [ ] Scout
- [ ] Echo
- [ ] Field
- [ ] Voice
- [ ] Compete
- [ ] Pulse

## JTBD Foundation
- Job Statement
- Functional Job
- Emotional Job
- Social Job
- Force Balance

## Proposal Details
- Persona
- Priority
- RICE Score
- User Story
- Hypothesis
- Feasibility
- Requirements
- Acceptance Criteria

## Validation Plan
- Pre-Implementation
- Post-Implementation
- Decision Criteria

## Next Steps
- Recommended handoff
```

## Minimal Proposal Template

Use this only when the idea is straightforward:

```markdown
# Feature: [Feature Name]

**Persona**: [Primary persona]
**Priority**: [Impact-Effort quadrant]
**RICE Score**: [Calculation]
**User Story**: As a [persona], I want to [action] so that [benefit].
**Hypothesis**: [Measurable statement]
**Feasibility**: [Existing data, logic, or assumptions]

**Requirements**:
- [Requirement]

**Acceptance Criteria**:
- [Criterion]
```

## Example Decision Policy

Keep this style when a proposal includes a go/no-go policy:
- validation with `Experiment` for `2 weeks`
- success metric threshold such as `>= 30%`
- secondary adoption threshold such as `>= 40%`
- iterate band such as `15-30%`
- kill threshold such as `< 15%`

Use project-appropriate numbers, but keep the logic explicit.

## Bad Proposal Check

Reject proposals that:
- have no persona
- have no hypothesis
- have no feasibility note
- have no acceptance criteria
- chase novelty without a product rationale

## Interaction Trigger Question Templates

### `BEFORE_FEATURE_SCOPE`

```yaml
questions:
  - question: "What level of feature proposal do you need?"
    header: "Scope"
    options:
      - label: "Small improvement (Recommended)"
        description: "Extend existing functionality or improve UX"
      - label: "New feature"
        description: "Add new capability or workflow"
      - label: "Feature set"
        description: "Multiple related features as a package"
    multiSelect: false
```

### `ON_PRIORITY_ASSESSMENT`

```yaml
questions:
  - question: "How should we prioritize these features?"
    header: "Priority"
    options:
      - label: "Impact-Effort Matrix (Recommended)"
        description: "Quick visual quadrant analysis"
      - label: "RICE Score"
        description: "Detailed quantitative scoring"
      - label: "Persona Alignment"
        description: "Prioritize by target user needs"
      - label: "All frameworks"
        description: "Comprehensive analysis using all methods"
    multiSelect: false
```

### `ON_PERSONA_SELECTION`

```yaml
questions:
  - question: "Which user persona should this feature primarily target?"
    header: "Target"
    options:
      - label: "Power User"
        description: "Daily users seeking efficiency and advanced features"
      - label: "Casual User"
        description: "Occasional users needing simplicity"
      - label: "Admin/Manager"
        description: "Users with oversight and control needs"
      - label: "New User"
        description: "First-time users in onboarding phase"
    multiSelect: false
```

### `ON_SCOUT_INVESTIGATION`

```yaml
questions:
  - question: "Technical investigation needed. How should we proceed?"
    header: "Investigation"
    options:
      - label: "Request Scout investigation (Recommended)"
        description: "Have Scout analyze codebase for feasibility"
      - label: "Assume feasibility"
        description: "Proceed with proposal and note assumptions"
      - label: "Scope down"
        description: "Reduce the feature to known-feasible parts"
    multiSelect: false
```

### `ON_EXPERIMENT_REQUEST`

```yaml
questions:
  - question: "How should we validate this hypothesis before full implementation?"
    header: "Validation"
    options:
      - label: "A/B test with Experiment (Recommended)"
        description: "Statistical validation with a control group"
      - label: "Prototype with Forge first"
        description: "Prototype before a formal test"
      - label: "Validate with Echo personas"
        description: "Use persona walkthroughs instead of an experiment"
      - label: "Skip validation, proceed to implementation"
        description: "Use only when confidence is already high"
    multiSelect: false
```

### `ON_EXPERIMENT_RESULT`

```yaml
questions:
  - question: "Experiment returned results. What should we do with this hypothesis?"
    header: "Result Action"
    options:
      - label: "Proceed based on verdict (Recommended)"
        description: "Ship, iterate, or kill based on the result"
      - label: "Request deeper analysis"
        description: "Inspect segments or methodology more deeply"
      - label: "Iterate and re-test"
        description: "Adjust the hypothesis and run another test"
      - label: "Override verdict with justification"
        description: "Proceed only with documented reasoning"
    multiSelect: false
```

### `ON_VALIDATION_LOOP`

```yaml
questions:
  - question: "Echo validated the proposal. What's the next step?"
    header: "Next Step"
    options:
      - label: "Hand off to Sherpa for breakdown (Recommended)"
        description: "Ready for implementation planning"
      - label: "Request Experiment validation"
        description: "Need quantitative evidence before build"
      - label: "Iterate on proposal"
        description: "Revise the draft before handoff"
      - label: "Hand off to Forge for prototype"
        description: "Prototype before committing to build"
    multiSelect: false
```


---

# Per-Recipe Behavior Notes and VERIFY Gates

Canonical home for the per-recipe notes referenced from `SKILL.md` -> Subcommand Dispatch. Each `**VERIFY**:` gate runs **in addition to** Spark's universal discipline.

Each `**VERIFY**:` is the recipe-specific gate at the VERIFY phase **in addition to** Spark's universal discipline (named by user problem not solution, specific persona never "everyone", outcome not output, validation path + fail condition, reuse existing data/logic).
- `propose`: Narrow to one proposal. Must include persona, JTBD, RICE score, fail conditions, and OST integration. **VERIFY**: exactly ONE feature; an `Alternative Framings Considered` section lists ≥2 problem framings with why-not notes, **at least one of which is an ambitious `H2`/`H3` bet (not all incremental)**; the chosen proposal carries a Horizon tag; if the safe `H1` was selected over a bolder framing, the why-not note must say *why the bold option lost* (not merely that it was riskier); RICE + fail condition + OST node (Outcome→Opportunity→Solution→Experiment) all present; JTBD framed as progress sought, not an activity; duplication with shipped features called out.
- `plan`: Score existing candidates with RICE/MoSCoW. Strictly adhere to RICE guardrails (Impact distribution, Confidence rationale). **VERIFY**: Reach is segment-specific (not total users); ≤20% of items at Impact=3; Confidence >50% only with cited evidence; Effort includes design+test+doc+maintenance +≥30% buffer; strategic initiatives routed to Magi (RICE is feature-level); ranking treated as relative, not false precision.
- `brainstorm`: Explore opportunity patterns (unused data, repetitive actions, friction) **and deliberately diverge beyond them** — apply contrarian inversion ("what if we did the opposite of the obvious fix?"), 10x reframing ("what would make this category-defining, not just better?"), and cross-domain analogy (route to `Flux` for paradigm shifts). Friction-pattern mining is the safe floor; a brainstorm that returns only incremental reuse plays has under-diverged. Link to OST nodes. **VERIFY**: candidates span the Horizon ladder — at least one `H2`/`H3` bet present, not an all-`H1` list; candidates drawn from real opportunity patterns AND ≥1 genuinely non-obvious/aggressive idea; each linked to an OST node whose metric maps to an OKR KPI; ≥2 problem framings explored (confirmation-biased discovery rejected); retrofitting tell checked (if every opportunity maps to an already-roadmapped feature → re-discover).
- `refine`: Take an existing RFC and reinforce hypotheses, fail conditions, and acceptance criteria. Run a duplication check. **VERIFY**: the hypothesis is testable (persona + metric + baseline + target + method); a fail condition (specific metric + kill threshold) is defined, not just success criteria; acceptance criteria specified; duplication check run; if underlying research is >4 weeks old, ≥1 evidence source refreshed before handoff.
- `opportunity`: Size the opportunity upstream of scoring — TAM/SAM/SOM with two independent paths, reach × impact × confidence in RICE-compatible units, WTP signal tier, market-timing assessment, OST placement. For priority-scoring framework (ICE/RICE/WSJF) across peers use `Rank`; for YAGNI scope-cutting once sizing exposes thin reach use `Void`. **VERIFY**: TAM/SAM/SOM derived via two independent estimation paths (cross-checked); reach×impact×confidence in RICE-compatible units; non-consumption / workarounds named in the competitive framing (the "nothing" competitor); WTP signal tier stated; thin reach routed to Void.
- `kill`: Kill-criteria authoring and sunset decision. Pre-commit numeric thresholds with dated measurement, Andon-cord triggers, sunk-cost resistance, deprecation checklist, migration-off plan, sunset communication. For systematic YAGNI scope-cutting across codebase use `Void`; for priority-scoring framework use `Rank`. **VERIFY**: numeric kill threshold pre-committed **with a dated measurement point** (e.g. "<2% adoption at 30 days"); Andon-cord trigger defined; sunk-cost reasoning explicitly resisted; migration-off plan + sunset communication + deprecation checklist all present.
- `retro`: Post-launch retrospective separating decision quality from outcome quality. Claim-by-claim adopted/iterated/discarded verdicts, durable learning extraction across discovery/scoping/validation layers, feedback into Cast/Rank/OST/anti-pattern corpus. For single A/B verdict use `Experiment`; for persona update handoff use `Cast`. **VERIFY**: decision quality assessed separately from outcome quality (a good decision can have a bad outcome); every original claim given an adopted/iterated/discarded verdict; durable learnings extracted across discovery/scoping/validation; feedback routed into Cast/Rank/OST/anti-pattern corpus; single A/B verdicts deferred to Experiment.
- `multi`: Tri-engine proposal generation. Spawn Codex / Antigravity / Claude subagents in one message; each produces 3-5 proposals independently with loose prompts (Role + Target + Output format only). Plea-style Concurrence-Divergence scoring: `UNIVERSAL` (3/3) = safe bets, `LIKELY` (2/3) = strong-with-one-dissenter, `VERIFIED-DIVERGENT` (1/3 after grounding) = breakthrough candidates. Two merge strategies — default `Portfolio` (5-7 complementary proposals, RFC-style document) or explicit `multi --compete` (single best RFC, re-mixing best wording across engines). Critical difference from Judge: divergent proposals are NOT auto-low-value; the breakthrough often comes from one engine's unique training data. See `reference/tri-engine-proposal.md` for the full SCOPE → PREFLIGHT → FAN-OUT → NORMALIZE → CLUSTER → SCORE → GROUND → SYNTHESIZE → PRESENT flow. **VERIFY**: dual-engine baseline actually spawned (Claude+Codex; agy added only when AVAILABLE at PREFLIGHT); loose prompts only (no JTBD/RICE/OST templates passed at FAN-OUT); every proposal concurrence-scored (UNIVERSAL/LIKELY/VERIFIED-DIVERGENT) with a mandatory engine-attribution tag; VERIFIED-DIVERGENT (1/3) grounded before shipping and NOT auto-deprioritized; merge strategy (Portfolio default / Compete) declared in the output.

