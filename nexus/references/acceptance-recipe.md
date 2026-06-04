# Acceptance Recipe — Proof-Carrying PR Pipeline

Recipe contract for `nexus acceptance` — orchestrates the 5-layer Proof-Carrying PR pipeline (spec graph → oracle generation → adversarial exploration → Acceptance Gate → runtime oracle hookup) defined in `_common/PROOF_CARRYING.md`. Use when a change needs machine-adjudicated merge without human visual confirmation.

**Prerequisites**: `_common/PROOF_CARRYING.md` v2 (mandatory — defines Tier policy, 12 Code-side + 9 Design-side evidence fields, G1-G10 guardrails, Design-Code Contract, Matrix Sampling Policy, Dual-Implementation Oracle). Read first.

**v2 — Two-Axis Decomposition**: Phases 2-4 split into Layer A (Code Acceptance) and Layer B (Design Acceptance). Layer B activates only when `ui_dimension != none`; pure-backend changes skip it entirely. Layer A is orchestrated inline by `nexus`; Layer B is sub-orchestrated by `atelier`. Phase 4 issues a joint verdict — either layer FAIL blocks merge.

**Design-axis prerequisite gate** (Phase 0 sub-check): if the change touches UI but the org lacks Figma + design tokens (Style Dictionary / Tokens Studio) + Code Connect, Layer B downgrades to advisory-only (logged, never blocking). This prevents Design Proof from blocking organizations not yet equipped to satisfy it.

**Distinguishes from**:
- `feature` — implements a change with conventional tests. No spec graph, no evidence package, no Acceptance Gate.
- `apex` — full discovery→ship cycle including spec authoring. `acceptance` assumes the spec graph exists (or is being amended) and focuses on the verification + Gate.
- `summit` — strategic decisions and high-stakes releases. `acceptance` is the merge-time pipeline; `summit` is the upstream judgment.
- `judge` — single-shot tri-engine code review. `acceptance` is a structured pipeline producing a Proof-Carrying PR; `judge` can be invoked as a sub-step.

---

## When to Invoke

Trigger `nexus acceptance` when **all** apply:
- The change touches a Tier-S or Tier-A surface (payment / medical / PII / auth / core revenue flow)
- The repository (or product line) has at least a partial spec graph the change can be validated against
- The organization has committed to the Proof-Carrying PR regime (this is a workflow choice, not a one-off tactic)

Do **not** invoke when:
- Tier-B or Tier-C scope — use `feature` / standard PR + AI review
- No spec graph exists and the user is asking for a one-off fix — recommend `apex` to author the spec first, then `acceptance` for subsequent changes
- The user wants exploration, not shipping — use `judge` or `omen`

---

## Phase Contract

### Phase 0 — Tier Classification + UI Dimension Detection (Nexus, internal)

Read `_common/PROOF_CARRYING.md` v2 Tier table. Classify the change by inspecting:
- Touched paths (auth/, billing/, payment/, pii/, etc. → Tier-S)
- Declared scope from user prompt
- `.agents/PROJECT.md` if a Tier policy file exists

**Outputs**:
- `tier: S | A | B | C`. If C, abort with a recommendation to use `feature` instead — `acceptance` is over-scope for Tier-C.
- `ui_dimension: none | partial | full`:
  - `none` — pure backend / infrastructure / data pipeline / no rendered UI change → Layer B is skipped
  - `partial` — minor UI surface (a copy change, a single component touch) → Layer B runs minimal subset (token + a11y + copy)
  - `full` — significant UI change (new screen, redesigned component, layout overhaul) → Layer B runs full 9 fields
- `design_proof_mode: blocking | advisory | skipped`:
  - `blocking` — org has Figma + design tokens + Code Connect → Layer B verdict can block merge
  - `advisory` — org has Figma but not tokens or Code Connect → Layer B runs but FAIL = log only, no merge block
  - `skipped` — `ui_dimension == none` OR org lacks Figma entirely → Layer B not run

**Design-axis prerequisite check** (when `ui_dimension != none`):
- Verify `tokens.json` (or equivalent Style Dictionary / Tokens Studio output) exists in repo
- Verify Figma Code Connect mapping file (`.figma/code-connect.json` or equivalent) exists
- Verify Storybook configuration exists for interactive component coverage
- Missing any → `design_proof_mode` downgrades from `blocking` to `advisory`

### Phase 1 — Spec Diff (sequential)

**Agent**: `attest` (spec compliance) + `accord` (if requirements need to be re-expressed as spec nodes) + `scribe` (only if spec graph needs human-readable annotation)

**Goal**: Produce `spec_diff` — the delta of spec graph nodes touched by this change. If the change is a spec-amendment (not just an implementation), the spec diff is itself subject to multi-view cross-check (see `PROOF_CARRYING.md` Spec Self-Bug section).

**Gate**: Spec diff is parseable, meta-invariants pass (no unreachable FSM nodes, all referenced columns exist, all API contracts have at least one consumer test).

### Phase 2 — Oracle Generation (Layer A + Layer B, parallel fan-out)

#### Phase 2A — Code-Axis Oracles (inline nexus orchestration)

**Agents** (parallel branches):
- `radar` — property-based + edge-case + regression tests
- `mint` — fixture and data generation (boundary, equivalence-class)
- `drill` — manual-equivalent E2E scenarios converted to executable form
- `voyager` — Playwright / CUA flows for UI surfaces (when `ui_dimension != none`, shared with Layer B)
- `sentinel` — SAST + security regression oracles
- `attest` — contract tests from API / DB invariants (if not already covered by attest in Phase 1)

**Dual-Implementation Oracle (in-scope domains, G4)**: For Tier-S/A PRs touching money / authz / state-machines / inventory / regulated logic, spawn `arena` in COMPETE mode:
- AI-A (production implementation) on engine E1
- AI-B (reference oracle) on engine E2 (different LLM family per G4)
- AI-C (adversarial reviewer) on engine E3 (different from both)
- Each receives spec in different form (NL vs formal vs decision table)
- CI runs property-based + production-log replay against both
- Diff classifier (G5) categorizes cosmetic / semantic / breaking
- Any semantic diff blocks merge; Source-of-Truth Spec (G10) is queried to identify which is correct

**Engine routing for Tier-S** (G1 cross-engine diversity): Oracle generation → agy when AVAILABLE (long-context spec reasoning is its strength); when agy is UNAVAILABLE or RUNTIME-BROKEN, route Oracle generation to Codex with explicit "treat spec as ground truth, do not regenerate from training-data priors" framing — this preserves cross-engine diversity against the Claude-based AI-A implementation. Implementation engine recorded for later split-check. See `_common/MULTI_ENGINE_RECIPE.md §Base Engine Policy` for the dual-engine fallback rationale.

#### Phase 2B — Design-Axis Oracles (atelier sub-orchestration, when `ui_dimension != none`)

**Sub-orchestrator**: `atelier` (orchestrates the Design skill chain)

**Agents** (parallel branches inside atelier sub-orchestration):
- `muse` — `token_proof` generator (token allow-list extraction, ESLint custom rule emission)
- `frame` — `component_proof` generator (Code Connect mapping verification + G9 layer 1 AST + layer 4 Code Connect checks)
- `palette` — `state_proof` + `responsive_proof` generators (state coverage requirements per component, viewport assertions)
- `weave` — state machine spec emission for interactive components (XState / DSL)
- `flow` — motion token verification (animation duration / easing token compliance)
- `canon` — `a11y_proof` generator (axe-core + Pa11y rule integration, WCAG 2.2 AA mapping)
- `showcase` — `vrt_proof` generator with Matrix Sampling Policy applied (`matrix` skill produces pairwise / orthogonal-array story set)
- `prose` — `copy_proof` generator (voice/tone rules, banned-word list, length constraints, locale-appropriate copy)

**Matrix Sampling Policy** (applies to `showcase` + `voyager` VRT runs, per PROOF_CARRYING.md PD-2):
- Tier-S: full pairwise + critical-path full-coverage; full N-way only for payment/auth/PII paths
- Tier-A: pairwise (2-way) on all DS components; 3-way for Tier-A critical user journey
- Tier-B: critical-path only (top 10 user journeys)
- `matrix` skill is the canonical pairwise generator; story count target ≤ 5,000 per build

**Engine routing for Tier-S Layer B**:
- Design Compiler rule-evaluation (deterministic) → Codex (CI / static analysis strength)
- Token / contract validation → Codex
- LLM-as-judge advisory (brand_proof residual) → Claude (judgment strength, advisory only per Unspecifiable Carve-Out)

**Gate (both 2A and 2B)**: Generated oracles must be deterministic (seed = spec-graph hash + Design-Code Contract hash) and pass shadow-run on `main` 3× before becoming Gate-blocking. Matrix new story-set additions also pass shadow-run for ≥3 weeks.

### Phase 3 — Adversarial Exploration (Layer A + Layer B, parallel fan-out)

#### Phase 3A — Code-Axis Adversaries (inline nexus orchestration)

**Agents** (parallel, different personas):
- `vigil` — security attacker persona (auth bypass, IDOR, token replay)
- `sentinel` — static + dynamic attack surface
- `specter` — concurrency / race / state-machine edge cases
- `siege` — load / chaos (Tier-S only)

**Engine routing for Tier-S Layer A** (G1 cross-engine diversity): Adversarial explorers → Claude (judgment + edge-case enumeration).

#### Phase 3B — Design-Axis Adversaries (atelier sub-orchestration, when `ui_dimension != none`)

**Agents** (parallel UI-user personas via `voyager` + `navigator`, orchestrated by `atelier` + `echo`):
- `echo` — persona walkthrough specialist; defines the AI-user persona set per UX-task-proof:
  - Standard new user (typical happy path)
  - Returning user (resumes prior state)
  - Impatient user (double-clicks, navigates away mid-flow)
  - Mobile-first user (touch targets, virtual keyboard)
  - Screen-reader user (focus order, ARIA semantics)
  - Slow-connection / offline user (loading states, error recovery)
  - Payment-failure user (decline → retry / alternative path)
  - Locale-edge user (RTL, long-translation overflow, IME composition)
  - Adversarial user (URL tampering, replayed tokens, malformed input)
- `voyager` + `navigator` — Playwright / CUA execution of persona scripts
- `drill` — converts persona walkthroughs to executable test scenarios

**Engine routing for Tier-S Layer B**: Adversarial UI users → Claude (persona judgment + UX edge enumeration); deterministic UI checks (token / contract violations) → Codex.

#### Combined Output contract

Each adversarial agent (Layer A or B) must produce a non-trivial exploration report. Empty findings without an exploration log = rejected (semantic-emptiness rule per `PROOF_CARRYING.md` Anti-Patterns). The `adversarial_findings` (Code) and `ux_task_proof` (Design) evidence fields cite the persona attempted + the failure modes probed + the rationale why each could not succeed.

**Gate**: Findings from either Layer either fixed in the same PR, or filed with explicit "won't fix" rationale that the Acceptance Gate (Phase 4) can adjudicate.

> **Adversarial-pass cost calibration** [Source: claude.com — *How Anthropic Enables Self-Service Data Analytics with Claude*]: a production measurement of one adversarial-review sub-agent records **+6% accuracy at the cost of +32% tokens and +72% latency**. Two implications for this recipe: (1) the adversarial fan-out is the dominant latency contributor — keep it gated to Tier-S/A and high-risk surfaces (money / authz / state-machine), not every diff; (2) do **not** route the adversarial explorers to a cheaper engine to trim cost — the same study found a cheaper reviewer lost the accuracy gain without recovering latency, which is why G1 routes Tier-S adversaries to Claude for judgment rather than the cheapest available model.

### Phase 4 — Acceptance Gate (Layer A + Layer B joint verdict)

#### Phase 4A — Code Acceptance Gate (inline nexus orchestration)

**Agents**:
- `judge` — tri-engine evidence audit (schema completeness, semantic non-emptiness, cross-engine quorum)
- `attest` — final spec-implementation conformance verdict

**Engine routing for Tier-S** (G1 cross-engine diversity):
- `judge` runs multi-engine — tri-engine (Claude + Codex + agy) when agy AVAILABLE, dual-engine (Claude + Codex) when agy UNAVAILABLE / RUNTIME-BROKEN. See `_common/MULTI_ENGINE_RECIPE.md §Engine Availability Modes`.
- Gate verdict requires 2-of-3 quorum (tri-engine: CONFIRMED or LIKELY) or 2-of-2 quorum (dual-engine: CONFIRMED only — `LIKELY` is unreachable with two engines, so the gate naturally tightens)

**Layer A Decision rules**:
1. All 12 Code-side evidence fields present and non-empty (semantic-non-emptiness rule)
2. Spec consistency: spec changes (if any) pass meta-oracle (per Spec Self-Bug)
3. Cross-engine quorum reached (Tier-S requirement)
4. Dual-Implementation Oracle (when in-scope): semantic diff = 0 OR triangulation against Source-of-Truth Spec confirms one implementation
5. Per-PR compute cap not exceeded
6. G5 Diff Semantics Classifier passed; "Approve all" not invoked on >10 diffs

**Layer A Output**: PASS_A / FAIL_A / ESCALATE_A

#### Phase 4B — Design Acceptance Gate (atelier sub-orchestration, when `ui_dimension != none`)

**Sub-orchestrator**: `atelier`
**Agents** (under atelier):
- `canon` — final WCAG 2.2 AA conformance verdict
- `frame` — final Design-Code Contract conformance verdict (4-layer G9 detection all PASS)
- `vision` — brand_proof advisory verdict (LLM-as-judge, non-blocking per Unspecifiable Carve-Out)

**Engine routing for Tier-S Layer B**:
- Deterministic Design Compiler verdicts → Codex
- Multi-modal compliance checks (long-context VRT review) → agy when AVAILABLE; when UNAVAILABLE, route to Claude (multimodal-capable model — i.e. Claude reading screenshot/image inputs directly, NOT the `vision` skill agent) with explicit "image-by-image VRT comparison" framing. Claude handles screenshots natively; the only loss vs agy is the 1M-context whole-set scan, which can be batched into 5-10 image groups
- Brand / unspecifiable advisory → Claude

**Layer B Decision rules**:
1. All 9 Design-side evidence fields present and non-empty (when `ui_dimension != none`)
2. Design-Code Contract changes (if any) pass Contract Meta-Oracle
3. 4-layer G9 detection all live (AST + Storybook + Runtime DOM + Code Connect) — none missing
4. Matrix Sampling Policy compliance: pairwise default for Tier-A, full critical-path for Tier-S
5. No unspecifiable-quality red flag (brand / ethics / dark-pattern) — if flagged, route to G7 Unmeasurable-Quality Audit
6. `design_proof_mode == blocking` for Layer B FAIL to block merge; `advisory` mode logs but allows merge

**Layer B Output**: PASS_B / FAIL_B / ESCALATE_B / SKIP_B (when ui_dimension == none)

#### Phase 4C — Joint Verdict (sequential after both layers complete)

**Agent**: `guardian` — PR preparation with embedded evidence package containing both Layer A and Layer B verdicts

**Joint Verdict Rules** (per PROOF_CARRYING.md Acceptance Gate rule 6):
- PASS_A + PASS_B → PASS (merge eligible)
- PASS_A + SKIP_B → PASS (no UI surface; Layer B not applicable)
- FAIL_A + any → FAIL (Code blocks)
- PASS_A + FAIL_B (blocking mode) → FAIL (Design blocks)
- PASS_A + FAIL_B (advisory mode) → PASS_WITH_ADVISORY (merge allowed; advisory recorded for follow-up)
- ESCALATE_A or ESCALATE_B → ESCALATE (route to human review)

**G7 Unmeasurable-Quality Audit Gate** (when `ui_dimension != none` AND Tier-S/A):
- Tier-S UI: human designer sign-off required even on Compiler/Matrix/Contract PASS (≥10 min recorded review)
- Tier-A UI: weekly aggregate review; sampled per G2
- Designer-review hours YoY tracked; >30% drop triggers atrophy warning

**Output**: PASS / PASS_WITH_ADVISORY / FAIL (specific gaps) / ESCALATE

### Phase 5 — Runtime Oracle Hookup (sequential, on PASS only)

**Agents**:
- `beacon` — registers `rollback_condition` as a live SLO oracle
- `mend` — registers repair runbook with G3 circuit-breaker config (same-signature cap = 3/24h, escalation cap = 7d)

**Gate**: Runtime oracle is live in shadow mode for the canary window before promotion.

### Phase 6 — Random Sampling Audit (asynchronous, post-merge)

For successful Tier-S/A merges:
- Roll a deterministic dice (seed = PR ID + date) at the configured sample rate (5% S / 2% A per `PROOF_CARRYING.md` G2)
- If sampled, file a human-review task with the full evidence package attached
- Review findings feed back into Gate rule updates (no automatic re-routing — explicit human decision required)

This phase does **not** block merge. It audits the Gate, not the change.

---

## Chain Template (AUTORUN)

```
Phase 0: Nexus[classify-tier + detect-ui-dimension + check-design-proof-mode]
         → if tier=C: abort with feature recommendation
         → outputs: {tier, ui_dimension, design_proof_mode}

Phase 1: attest[spec-diff] (+ accord[spec-amend] if spec changes; + scribe if human-readable spec needed)

Phase 2A (Layer A — Code Oracles, parallel, engine=agy for Tier-S when AVAILABLE; else Codex with spec-as-ground-truth framing):
  ‖ radar[property+regression]
  ‖ mint[fixtures]
  ‖ drill[E2E scenarios]
  ‖ sentinel[SAST + security regression]
  ‖ attest[contract tests]
  ‖ if in-scope (money/authz/state-machine/inventory/regulated):
      arena[COMPETE, AI-A on E1 + AI-B on E2 + AI-C on E3, per G4]

Phase 2B (Layer B — Design Oracles, parallel, atelier sub-orchestration, IF ui_dimension != none):
  atelier orchestrates:
    ‖ muse[token_proof]
    ‖ frame[component_proof + G9 4-layer detection coordination]
    ‖ palette[state_proof + responsive_proof]
    ‖ weave[state machine spec]
    ‖ flow[motion tokens]
    ‖ canon[a11y_proof, axe-core/Pa11y]
    ‖ showcase[vrt_proof with matrix-sampled stories]
    ‖ prose[copy_proof]
    ‖ matrix[pairwise / orthogonal-array story generation, per PD-2]

Phase 3A (Layer A — Code Adversaries, parallel, engine=claude for Tier-S):
  ‖ vigil[security attacker]
  ‖ sentinel[attack surface]
  ‖ specter[concurrency edges]
  ‖ if tier=S: siege[load+chaos]

Phase 3B (Layer B — Design Adversaries, parallel, atelier sub-orchestration, IF ui_dimension != none):
  atelier orchestrates:
    ‖ echo[persona definition: standard / returning / impatient / mobile / screen-reader / slow-net / payment-fail / locale-edge / adversarial]
    ‖ voyager + navigator[Playwright/CUA execution of persona scripts]
    ‖ drill[converts persona walkthroughs to test scenarios]

Phase 4A (Code Acceptance Gate, sequential, judge runs tri-engine):
  judge[tri-engine evidence audit] → attest[final conformance]
  → outputs: PASS_A / FAIL_A / ESCALATE_A

Phase 4B (Design Acceptance Gate, sequential, atelier sub-orchestration, IF ui_dimension != none):
  atelier orchestrates:
    canon[final WCAG verdict] → frame[final Contract verdict] → vision[brand advisory]
  → outputs: PASS_B / FAIL_B / ESCALATE_B / SKIP_B

Phase 4C (Joint Verdict, sequential):
  guardian[PR with both Layer A + Layer B evidence]
  Joint Verdict rules:
    PASS_A + (PASS_B | SKIP_B) → PASS
    FAIL_A + * → FAIL
    PASS_A + FAIL_B(blocking) → FAIL
    PASS_A + FAIL_B(advisory) → PASS_WITH_ADVISORY
    ESCALATE_* → ESCALATE → human

Phase 4-G7 (Unmeasurable-Quality Audit, when ui_dimension != none AND Tier-S/A):
  Tier-S UI: human designer sign-off (≥10 min recorded)
  Tier-A UI: weekly aggregate review (sampled per G2)

Phase 5 (Runtime Oracle Hookup, sequential, on PASS / PASS_WITH_ADVISORY only):
  beacon[register runtime oracle] → mend[register repair runbook with G3 circuit breaker]

Phase 6 (Random Sampling Audit, async post-merge, non-blocking):
  sample(rate=5% Tier-S / 2% Tier-A per G2) → human-review task if sampled
  audits the Gate, not the change
```

---

## Failure Escalation

| Failure | Trigger | Escalation |
|---------|---------|------------|
| Spec parse fails | Phase 1 | Block; ask user to fix spec syntax or remove spec changes |
| Meta-oracle fails | Phase 1 | Block; spec change is internally inconsistent (e.g., unreachable state) |
| Oracle generation non-deterministic | Phase 2 | Block; seed not stable or generator has un-seeded randomness — investigate before allowing as Gate-blocking |
| Shadow-run flaky on main | Phase 2 | Defer new oracle to shadow-only for 3 more weeks; do not Gate-block |
| Adversarial empty without exploration log | Phase 3 | Hard re-run with explicit exploration requirement; reject if re-runs also empty |
| Cross-engine quorum fails (Tier-S) | Phase 4 | Block; require 2-of-3 CONFIRMED/LIKELY before merge eligible |
| Compute cap exceeded | Phase 4 | Escalate to human triage; do not auto-extend |
| Unspecifiable-quality flag raised | Phase 4 | Route to human review regardless of Tier evidence completeness |
| Repair-loop signature cap hit (same-signature 3/24h) | Phase 5 runtime | Auto-rollback, 7d escalation, no further auto-repair on that signature |
| Hot-fix needed mid-pipeline | Any phase | Switch to Hot-Fix Fast-Path: downgrade Tier-S→A, Tier-A→B; require normal-Gate follow-up within 24h |
| Design-axis prerequisite missing (no tokens / no Code Connect) | Phase 0 sub-check | `design_proof_mode` downgrades to `advisory`; Layer B runs but cannot block merge |
| Dual-Implementation same-LLM family detected | Phase 2A | Block; G4 requires different families for AI-A / AI-B / AI-C; recipe re-selects engines |
| Dual-Implementation semantic diff non-zero | Phase 2A | Block; triangulate against Source-of-Truth Spec (G10); incorrect implementation must be fixed |
| G9 4-layer detection incomplete (AST/Storybook/Runtime/CodeConnect not all live) | Phase 2B | `component_proof` downgrades to advisory until all 4 live |
| Matrix story count >5,000 per build | Phase 2B | Block; apply equivalence partitioning + pairwise reduction; escalate matrix sampling skill |
| VRT diff classifier flags "Approve all" attempt on >10 diffs | Phase 4 | Block; G5 enforces tool-level ban; force PR split if >50 diffs |
| Layer B FAIL with `design_proof_mode == blocking` | Phase 4C | Block merge; Code-side PASS does not split-merge |
| Layer B FAIL with `design_proof_mode == advisory` | Phase 4C | Allow merge with `PASS_WITH_ADVISORY`; advisory recorded; >3 advisories/sprint per product flags process review |
| Unmeasurable-Quality flag raised on UI change | Phase 4-G7 | Tier-S routes to designer human sign-off; Tier-A queues for weekly audit |
| Designer-review hours dropped >30% YoY | Phase 4-G7 monitoring | Atrophy warning logged; flag for review process audit |
| Carve-out invoked on >20% of Tier-S/A PRs in quarter | Cross-phase monitoring | Process review: either extend Design Compiler rules OR invest in human design review capacity |
| Component Sandbox prototype aged >6 months without promotion/removal | Cross-phase monitoring | Cleanup task auto-filed; sandbox SLA enforcement |
| Time-Boxed Deviation exceeded 90-day expiration | Cross-phase monitoring | Auto-rollback to Contract OR force removal; >3 active deviations per product triggers brand-system review |

---

## Cost & Scale Profile

| Tier | ui_dimension | Layer A Agents | Layer B Agents | Total | Wall Time | Cost vs `feature` |
|------|--------------|---------------:|---------------:|------:|----------:|------------------:|
| S | none | 14-18 | 0 | 14-18 | 35-60 min | 6-10× |
| S | full | 14-18 | 8-12 (+ atelier orch) | 22-30 | 50-90 min | 9-15× |
| A | none | 8-12 | 0 | 8-12 | 18-35 min | 3-5× |
| A | full | 8-12 | 6-9 (+ atelier orch) | 14-21 | 28-55 min | 5-8× |
| B | * | (use `feature` recipe) | — | — | — | 1× |
| C | * | (use `feature` or standard PR) | — | — | — | 1× |

**Confirm with user before launching Tier-S** — agent count and cost rival or exceed `apex` when Layer B activates. Tier-A with full UI is comparable to `kaizen` + `judge` combined.

**Dual-Implementation cost overhead**: When in-scope (money / authz / state-machine / inventory / regulated), add 2-4 agents (arena COMPETE + AI-A + AI-B + AI-C) and 1.4-1.8× compute multiplier on implementation tokens. Strictly enforce per-PR compute cap.

---

## Anti-Patterns Specific to Acceptance

| Anti-Pattern | Counter-Rule |
|--------------|--------------|
| Running `acceptance` on Tier-C scope | Phase 0 aborts; use `feature` |
| Single-engine evidence for Tier-S | G1 cross-engine diversity is mandatory; Phase 4 quorum check enforces |
| Skipping shadow-run on new oracles | Phase 2 Gate; new oracles are shadow-only until 3 weeks of stability |
| Treating "no findings" as proof | Phase 3 requires exploration log; semantic-emptiness is rejected |
| Bypassing Gate for "urgent" merges | Use Hot-Fix Fast-Path; never invent `[skip-acceptance]` style labels |
| Auto-repair loop without circuit breaker | Phase 5 G3 enforces same-signature 3/24h cap |
| Spec change without meta-oracle re-validation | Phase 1 blocks; spec changes are themselves Proof-Carrying |
| Quality dimensions reduced to spec | Phase 4 unspecifiable-quality carve-out routes to human |
| Layer A + Layer B run in series (vs parallel) | Phase 2-3 explicitly parallel; serial run wastes wall time |
| Layer B blocking on org without prerequisites | Phase 0 prerequisite check downgrades to advisory |
| Code Proof PASS shipped despite Design Proof FAIL | Phase 4C joint verdict rules — split-merge forbidden in blocking mode |
| Dual-Implementation with same engine for AI-A and AI-B | G4 mandatory diversity check at Phase 2A spawn time |
| Matrix taken literally as full Cartesian product | PD-2 default to pairwise; full N-way Tier-S critical-path only |
| Compiler PASS celebrated as "design approved" | G7 Unmeasurable-Quality Audit Gate enforces human sign-off on Tier-S UI |
| Atelier replaced by inline nexus orchestration | Layer B coordination requires design-domain expertise; atelier is the sub-orchestrator by design |

---

## Integration with Existing Recipes

- `apex` Phase 6 (Ship) can chain into `acceptance` for Tier-S deliverables. `apex` produces the spec and implementation; `acceptance` provides the Gate.
- `summit` strategic-decision deliverables that result in code changes flow through `acceptance` for Tier-S/A scope.
- `feature` is the recommended downgrade when `acceptance` Phase 0 classifies as Tier-B/C.
- `kaizen` improvements to Tier-S/A surfaces should chain `kaizen → acceptance` (kaizen produces the improvement; acceptance gates the merge).

---

## References

- `_common/PROOF_CARRYING.md` v2 — the protocol; required reading (defines Tier policy, evidence fields, G1-G10 guardrails, Design-Code Contract, Matrix Sampling Policy, Dual-Implementation Oracle)
- `nexus/references/apex-recipe.md` — discovery→ship cycle; `acceptance` is the merge-gate portion
- `nexus/references/summit-recipe.md` — engine-strength routing pattern that `acceptance` Tier-S inherits

**Layer A (Code) skill references**:
- `judge/SKILL.md` — tri-engine evidence audit
- `attest/SKILL.md` — spec compliance verification + final conformance
- `arena/SKILL.md` — Dual-Implementation Oracle (COMPETE mode, G4 orchestration)
- `radar/SKILL.md` — property-based + regression oracle generation
- `mint/SKILL.md` — fixture / data generation
- `drill/SKILL.md` — E2E scenario authoring
- `sentinel/SKILL.md` — SAST + attack-surface (Layer A oracle + Layer A adversary)
- `vigil/SKILL.md` — security attacker persona (Layer A adversary)
- `voyager/SKILL.md` — Playwright/CUA E2E (shared Layer A + Layer B)
- `navigator/SKILL.md` — browser automation for UI persona walkthroughs
- `specter/SKILL.md` — concurrency / race condition edge cases
- `siege/SKILL.md` — load + chaos (Tier-S only)
- `beacon/SKILL.md` — runtime oracle registration
- `mend/SKILL.md` — repair runbook with circuit-breaker semantics
- `guardian/SKILL.md` — PR preparation with embedded evidence package

**Layer B (Design) skill references**:
- `atelier/SKILL.md` — Layer B sub-orchestrator; coordinates muse + frame + palette + canon + showcase + prose + echo + vision + matrix + weave + flow
- `muse/SKILL.md` — design token allow-list + `token_proof`
- `frame/SKILL.md` — Design-Code Contract + Code Connect + `component_proof` + G9 4-layer detection coordination
- `palette/SKILL.md` — `state_proof` + `responsive_proof`
- `weave/SKILL.md` — state machine spec (XState DSL for interactive components)
- `flow/SKILL.md` — motion token verification (animation duration / easing)
- `canon/SKILL.md` — `a11y_proof` (WCAG 2.2 AA, axe-core/Pa11y integration)
- `showcase/SKILL.md` — `vrt_proof` with Matrix Sampling
- `prose/SKILL.md` — `copy_proof` (voice / tone / banned words / length / locale)
- `echo/SKILL.md` — UX persona definition for `ux_task_proof`
- `vision/SKILL.md` — brand_proof advisory (LLM-as-judge, non-blocking)
- `matrix/SKILL.md` — pairwise / orthogonal-array story-set generation
