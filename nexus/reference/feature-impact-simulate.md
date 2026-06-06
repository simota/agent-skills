# Feature Impact Simulate — Reference Recipe (v4 fold-in)

Lightweight reference recipe for predicting feature impact across personas, journeys, and product strategy **before** implementation. Implements the "Feature Impact Simulator" concept from the v4 Persona+Journey+Product proposal using **existing skills only** — no new skill required.

**Prerequisites**:
- `_common/PROOF_CARRYING.md` v3.1 (Authoring Principles + Proposal Intake Checklist)
- `omen` (pre-mortem failure enumeration)
- `ripple` (vertical + horizontal impact analysis)
- `echo` (persona walkthrough, especially `council` Recipe with Persona Contract)
- `experiment` (A/B simulation + metric prediction)
- `magi` (multi-perspective Go/Modify/Reject arbitration)

**Why this is a reference recipe, not a Nexus subcommand**: Magi v4 verdict (C7) explicitly rejected promoting Feature Impact Simulator to a top-level Nexus Recipe because the chain is composable from existing skills. Promoting it would risk Authoring Principles Checklist § Item 1 violation (existing-skill absorption ≥80%). Users invoke this chain manually via `nexus classify` or directly assemble the chain when the explicit need arises.

**Distinguishes from**:
- `nexus apex` — full discovery-to-ship cycle. This recipe is **only the impact prediction phase**, run before any implementation begins.
- `nexus essential` / `killer` — these recipes converge on a single feature verdict. Feature Impact Simulate evaluates **a specific proposed feature** against existing personas/journeys.
- `nexus acceptance` / `growth-acceptance` — these are merge-time / lifecycle gates. Feature Impact Simulate is **pre-design**.
- `magi multi` alone — broader strategic deliberation. Feature Impact Simulate adds omen+ripple+echo grounding before magi judgment.

---

## When to Invoke

Trigger this recipe when **all** apply:
- A specific feature proposal exists (not exploration / brainstorming)
- The feature has potential cross-persona impact (e.g., affects both Power users and beginners)
- Org wants Go/Modify/Reject decision with **machine-grounded evidence** before committing implementation budget
- Time budget allows 15-40 min wall time for the simulation

Do **not** invoke when:
- The feature is trivial (single component, single persona, < 2 hours impl)
- Exploration phase — use `riff` / `magi multi` for divergent thinking
- Discovery phase — use `nexus apex` Phase 0-1 for full discovery
- Strategy-only — use `magi multi` directly without grounding chain

---

## Phase Contract

### Phase 1 — Failure Mode Pre-Mortem (omen)

**Agent**: `omen`

**Task**: Enumerate failure modes of the proposed feature using DEEP work mode. Score each via RPN (Severity × Occurrence × Detection) or AP (H/M/L).

**Output contract**:
```yaml
omen_findings:
  feature_under_evaluation: <feature name>
  failure_modes:
    - id: FM-001
      mode: <description>
      severity: 1-10
      occurrence: 1-10
      detection: 1-10
      rpn: <product>
      ap: H | M | L
      affected_personas: [<persona-id list from echo Persona Contract>]
    - id: FM-002
      ...
  critical_count: <RPN > 400 OR AP=H count>
  s9_count: <severity ≥ 9 count>
```

**Gate**: If `s9_count > 0`, mark feature as `HIGH_RISK` for Phase 5 magi arbitration.

### Phase 2 — Impact Analysis (ripple, parallel with Phase 1)

**Agent**: `ripple`

**Task**: Vertical impact (downstream services / data flows / API consumers) + horizontal impact (sibling features / shared components / cross-team dependencies).

**Output contract**:
```yaml
ripple_findings:
  vertical:
    affected_services: [<service-id list>]
    affected_data_stores: [<datastore-id list>]
    affected_api_consumers: [<consumer-id list>]
    blast_radius: SMALL | MEDIUM | LARGE
  horizontal:
    sibling_features: [<feature-id list>]
    shared_components: [<component-id list>]
    cross_team_dependencies: [<team-id list>]
    consistency_violations: [<violation description list>]
  total_impact_score: 1-100
```

**Gate**: If `blast_radius == LARGE` OR `consistency_violations[]` non-empty, mark for Phase 5 magi arbitration.

### Phase 3 — Persona Council Walkthrough (echo, parallel with Phases 1-2)

**Agent**: `echo` in `council` mode (v4 fold-in)

**Task**: Run Persona Council against the proposed feature mock-up / spec. Use 4-perspective minimum (per v4 proposal): Power user / 初回ユーザー (first-time) / Support / Strategy. Org Tier determines max persona count (Solo skip; SMB max 3; Enterprise max 9). Each persona evaluated with machine-readable Persona Contract.

**Engine diversity (Tier-S/A)**: Run via `rally engine-paradigm` mode (Codex + Antigravity + Claude) — single-engine Council forbidden for Tier-S.

**Output contract**:
```yaml
echo_council_findings:
  feature_under_evaluation: <feature name>
  org_tier: solo | smb | enterprise
  engine_mode: single | rally-engine-paradigm
  personas_evaluated: <count>
  per_persona_results:
    - persona_id: power-user
      weight: secondary  # power users are usually secondary unless feature is power-user-specific
      result: PASS | FAIL | INCONCLUSIVE
      disqualification_triggers: [<DISQ-ID list>]
      success_achieved: [<SUCC-ID list>]
      correction_proposals: [...]
      confidence: [hypothesis] | [validated]  # default [hypothesis] until Voice/Trace calibration
    - persona_id: first-time
      weight: primary
      ...
    - persona_id: support
      weight: risk  # support burden = risk persona
      ...
    - persona_id: strategy
      weight: risk  # product strategy violation = risk
      ...
  cross_persona_findings:
    universal_friction: [<finding list shared across ≥2 personas>]
    primary_failure: <true if any primary-weight persona FAIL>
    risk_persona_failure: <true if any risk-weight persona FAIL>
```

**Gate**: If `primary_failure == true` OR `risk_persona_failure == true`, mark for Phase 5 magi arbitration.

### Phase 4 — Metric Prediction (experiment)

**Agent**: `experiment`

**Task**: Predict metric impact using A/B-style modeling. Reference Insight Ledger (via tome) for historical patterns. Output predicted change for: activation rate / retention / support ticket volume / NPS / time-to-value.

**Output contract**:
```yaml
experiment_predictions:
  feature_under_evaluation: <feature name>
  reference_baseline:
    insight_ledger_refs: [<insight-id list with N≥3>]
    historical_similar_features: [<feature-id list>]
  predictions:
    activation_rate:
      direction: + | - | neutral
      magnitude_percent: <numeric>
      confidence_interval: [<lower>, <upper>]
    retention_d30:
      ...
    support_ticket_volume:
      ...
    nps:
      ...
    time_to_value_seconds:
      ...
  prediction_confidence: HIGH | MEDIUM | LOW
  insufficient_baseline_warning: <true if reference data is thin>
```

**Gate**: If `prediction_confidence == LOW` AND `insufficient_baseline_warning == true`, mark for Phase 5 magi arbitration (cannot predict reliably; human judgment needed).

### Phase 5 — Multi-Perspective Arbitration (magi)

**Agent**: `magi` in `arbitrate` mode (Simple 3-lens or Multi if Tier-S)

**Inputs**: omen_findings + ripple_findings + echo_council_findings + experiment_predictions

**Task**: Logos (technical feasibility + omen risk weight) / Pathos (echo council human impact) / Sophia (ripple long-term impact + experiment metric direction) deliberation. Produce Go / Modify / Reject verdict.

**Output contract**:
```yaml
magi_verdict:
  feature_under_evaluation: <feature name>
  decision: GO | MODIFY | REJECT
  confidence: HIGH | MEDIUM | LOW
  per_lens:
    logos:
      vote: APPROVE | REJECT | ABSTAIN
      rationale: <2-3 sentences>
    pathos:
      vote: APPROVE | REJECT | ABSTAIN
      rationale: <2-3 sentences>
    sophia:
      vote: APPROVE | REJECT | ABSTAIN
      rationale: <2-3 sentences>
  consensus: <3-0 | 2-1 | mixed>
  conditions:  # if MODIFY
    - <specific change required>
  blocking_findings:  # if REJECT
    - <which omen / ripple / echo / experiment finding triggered rejection>
  go_conditions:  # if GO
    - <specific guardrails to maintain during implementation>
```

---

## Chain Template (AUTORUN)

```
Parallel Phase 1-3 (independent evaluations):
  ‖ omen[pre-mortem of feature → RPN/AP scored failure modes]
  ‖ ripple[vertical + horizontal impact + blast radius]
  ‖ echo[council mode with 3-9 personas per Org Tier; rally engine-paradigm for Tier-S/A]

Sequential Phase 4 (after parallel completes):
  experiment[metric prediction based on Insight Ledger historical patterns]

Sequential Phase 5 (final arbitration):
  magi[arbitrate with Logos+Pathos+Sophia over all 4 prior outputs → GO/MODIFY/REJECT]

DELIVER:
  Feature Impact Report = omen + ripple + echo + experiment + magi outputs
  + machine-readable verdict + recommended next-step nexus recipe
```

---

## Failure Escalation

| Failure | Trigger | Escalation |
|---------|---------|------------|
| omen finds S≥9 critical | Phase 1 | Forward to Phase 5 with HIGH_RISK flag |
| ripple blast_radius=LARGE | Phase 2 | Forward to Phase 5; suggest `nexus apex` for full discovery |
| echo primary persona FAIL | Phase 3 | Forward to Phase 5; suggest re-design before re-evaluation |
| echo risk persona FAIL | Phase 3 | Forward to Phase 5 as REJECT candidate |
| experiment LOW confidence + insufficient_baseline | Phase 4 | Forward to Phase 5; magi may require user research before proceeding |
| Insight Ledger insufficient evidence | Phase 4 | Block Phase 4; queue field for fresh research; resume when N≥3 |
| Persona Council single-engine on Tier-S | Phase 3 setup | Block; require `rally engine-paradigm` engine diversity |
| Org Tier persona cap exceeded | Phase 3 | Truncate persona list to cap; flag deferred personas for next session |

---

## Cost & Scale Profile

| Org Tier | Persona Count | Engine Mode | Wall Time | Agent Count | Cost vs Single magi |
|----------|--------------:|-------------|-----------|------------:|--------------------:|
| Solo | n/a (skip echo) | n/a | 10-15 min | 4 (omen + ripple + experiment + magi) | 3× |
| SMB | up to 3 | single | 15-25 min | 5 (+ echo) | 5× |
| Enterprise (Tier-A) | up to 9 | single | 20-35 min | 5 | 8× |
| Enterprise (Tier-S) | up to 9 | rally engine-paradigm (3 engines) | 25-40 min | 7 (+ rally engine-paradigm ×3) | 12× |

**Cap**: Total budget ≤ $50 per simulation (Magi v4 C5 — operator burnout prevention). If projected to exceed, downgrade to single-engine mode or reduce persona count.

---

## Anti-Patterns

| Anti-Pattern | Counter-Rule |
|--------------|--------------|
| Promoting feature_impact_simulate to a top-level Nexus subcommand | Reference recipe only — Authoring Principles § Item 1 forbids new top-level if existing skills absorb ≥80% |
| Running on trivial features (< 2 hours impl, single persona) | Phase 1 entry check — skip and recommend direct implementation |
| Single-engine Council for Tier-S | Phase 3 enforcement — require `rally engine-paradigm` |
| Treating echo Council output as `[validated]` without Voice/Trace calibration | echo `council` Always — output is `[hypothesis]` by default |
| Skipping Phase 4 experiment because "we don't have data" | Block Phase 4; queue field; do not proceed to magi without baseline |
| magi verdict without all 4 prior phases | Phase 5 enforcement — magi receives all 4 outputs as input, none optional |
| Re-running simulation as a "stalling tactic" | Track simulation count per feature; > 3 runs without change triggers escalation |

---

## Integration with Existing Recipes

- **Before `nexus apex`** — if `feature-impact-simulate` REJECTs, `apex` should not be invoked (saves Phase 1-6 cost)
- **Before `nexus acceptance`** — if `feature-impact-simulate` MODIFY conditions exist, address them before submitting to acceptance gate
- **Before `nexus growth-acceptance` Phase 0** — Enterprise org-tier should run this as a Phase 0 preparation step
- **After `magi multi` strategic decision** — once strategy chooses a feature, run this recipe before implementation

---

## References

- `_common/PROOF_CARRYING.md` v3.1 — Authoring Principles + Proposal Intake Checklist (justifies why this is a reference recipe, not a top-level)
- `_common/GROWTH_BRAND_PROOF.md` — Friction Ledger, Insight Ledger (Phase 4 reference baseline)
- `omen/SKILL.md` — pre-mortem DEEP mode
- `ripple/SKILL.md` — vertical + horizontal impact analysis
- `echo/SKILL.md` — Persona Council Recipe with machine-readable Persona Contract
- `experiment/SKILL.md` — A/B simulation + Incrementality Decision Tree
- `magi/SKILL.md` — arbitrate Recipe (Simple 3-lens; Multi for Tier-S)
- `nexus/reference/apex-recipe.md` — full discovery-to-ship; this recipe is the pre-design preparation
- `nexus/reference/growth-acceptance-recipe.md` — Phase 0 Pre-Design lifecycle gate
- Magi v4 verdict (Persona+Journey+Product proposal review): C7 mandates this be a reference recipe, not a new skill
