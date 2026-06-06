# Proof-Carrying PR Protocol

Cross-skill protocol for shipping changes with **machine-verifiable evidence packages** that an Acceptance Gate can adjudicate without human visual confirmation. Inspired by the AAOS (Autonomous Acceptance OS) framing: encode product correctness as executable specifications, then refuse to merge any PR whose evidence package does not match the spec graph.

**Audience**: Skills participating in change-shipping pipelines.
- **Code axis** (Layer A): `attest`, `judge`, `guardian`, `radar`, `voyager`, `sentinel`, `vigil`, `mend`, `beacon`, `rally` (dual-implementation via `engine-paradigm`), `nexus[acceptance]`, `nexus[apex]`, `nexus[summit]`.
- **Design axis** (Layer B): `atelier` (sub-orchestrator), `muse`, `frame`, `palette`, `canon`, `vitrine`, `prose`, `echo`, `vision`, `weave`, `flow`, `matrix` (pairwise sampling).

**Prerequisites**: `_common/HANDOFF.md` (handoff schema), `_common/MULTI_ENGINE_RECIPE.md` (cross-engine fan-out).

**Version**: v3.1 — adds Proposal Intake Checklist (Authoring Principles section, structural deceleration against accumulated-adoption fatigue per Magi v4 C8). Otherwise unchanged from v3: 3-tier structure (Foundation / Production Pipeline / Market-Brand Acceptance), cross-cutting guardrails G11 (KB Write Authority Separation) / G14 (Regulatory Envelope Pre-Flight) / G15 (Constitution Lifecycle Discipline). Layer C (Market + Research + Brand axes) lives in the separate `_common/GROWTH_BRAND_PROOF.md` companion protocol — adopt independently per Org Tier.

**v2 baseline retained**: Code axis (Layer A) + Design axis (Layer B) + G1-G10 + Dual-Implementation Oracle + Matrix Sampling + Design-Code Contract. Solo / SMB orgs operate at v2 baseline; Enterprise orgs may adopt Layer C via Phased Adoption (see GROWTH_BRAND_PROOF.md).

---

## Three-Tier Structure (v3)

The protocol stack now organizes into three tiers, each adoptable independently:

| Tier | Scope | Guardrails | Skills | Adoption |
|------|-------|-----------|--------|----------|
| **Tier A — Foundation** | LLM output integrity, evidence completeness, repair-loop safety | G1 / G2 / G3 | judge, attest, beacon, mend, sentinel | Required for any Proof-Carrying regime |
| **Tier B — Production Pipeline** | Code merge-time + Design merge-time gates (this file's main body) | G4-G10 + Dual-Impl + Matrix + Contract | radar, voyager, vigil, atelier, frame, muse, palette, canon, vitrine, prose, echo, vision, weave, flow, matrix, rally | Solo OK with subset; SMB+ full |
| **Tier C — Market-Brand Acceptance** | Pre-design + ship-time + post-launch lifecycle gates (M / R / B axes) | G11* / G12 / G13 / G14* / G15* | field, voice, trace, plea, pulse, experiment, funnel, bazaar, compete, crest, clause, oath, ledger (FinOps), harvest, tome | Enterprise only; SMB optionally adopts Step 1 Measurement Loop |

\* Cross-cutting guardrails (G11 / G14 / G15) apply to Tier A and Tier B knowledge bases as well, not only Layer C. They are documented in this file below.

**Read order**: Tier A+B users read this file end-to-end. Tier C users read this file first, then `_common/GROWTH_BRAND_PROOF.md`.

---

---

## Core Premise

The bottleneck in AI-assisted shipping is no longer code generation — it is the last-mile human judgment ("does this work as intended? does it break existing flows? is it brand-appropriate?"). Eliminating that bottleneck requires:

1. A **specification graph** (state machines, API contracts, DB invariants, a11y constraints, KPI floors, regression memory) that is machine-readable and acts as a **judge**, not as documentation.
2. An **oracle generator** that derives test oracles (contract, E2E, property-based, fuzz, VRT, a11y, DB integrity, security regression) from the spec graph.
3. **Adversarial AI explorers** — not approvers — that try to break the change.
4. A **Proof-Carrying PR**: every PR must carry an evidence package, and an **Acceptance Gate** (not a human) decides merge.
5. **Runtime oracles + auto-rollback** as the last safety net, with circuit breakers to prevent repair-loop oscillation.

The constraint that distinguishes this from "AI writes tests": AI agents are positioned as **adversarial explorers**, not approvers. Their value is "couldn't break it", not "looks fine".

### Two-Axis Decomposition: Code Proof + Design Proof

A Proof-Carrying PR decomposes into two parallel evidence packages that the Acceptance Gate adjudicates independently and then jointly:

- **Code Proof** (Layer A): type / lint / unit / integration / contract / property / regression / security / migration / observability / rollback. Orchestrated by existing `acceptance` Phase 2-4 Layer A.
- **Design Proof** (Layer B): token / component / state / responsive / a11y / VRT / copy / UX task / brand. Orchestrated by `atelier` as Layer B sub-orchestrator (only when `ui_dimension != none`).

Both packages must be PASS for merge. Either FAIL blocks merge. A change with no UI surface skips Layer B entirely. A change with no code surface (rare — pure design token bump) skips Layer A.

This separation is **orthogonal to the 5-layer pipeline**: the 5 layers are temporal (what happens when), the 2 axes are categorical (what kind of evidence). Layer 2 (oracle generation) and Layer 3 (adversarial exploration) each split into Code-axis and Design-axis sub-tracks; Layer 4 Acceptance Gate adjudicates both before issuing a single PASS/FAIL.

---

## Tier-Based Application Policy

Not every PR needs full proof. Apply by criticality tier:

| Tier | Scope | Code Proof | Design Proof | Dual-Impl | Matrix Sampling | Gate Behavior |
|------|-------|-----------|--------------|-----------|-----------------|---------------|
| **S** | Payment / Medical / Aviation / PII / Auth-critical | 11/11 all | 9/9 all (if UI) | mandatory (regulated domains) | full pairwise + critical-path | Block merge until full evidence + 2-of-3 cross-engine quorum |
| **A** | Core revenue features / Customer-facing flows | 11/11 all | 9/9 all (if UI) | mandatory for money / auth / state-machine / inventory | pairwise (2-way) | Block on spec mismatch; advisory on adversarial gaps |
| **B** | Internal tools / Secondary features | 8/11 (skip migration / observability / rollback if not applicable) | 6/9 (token / component / state / a11y / VRT / copy) | opt-in | critical-path only | Block on test failure; spec graph optional |
| **C** | UI tweaks / Copy changes / Docs | 4/11 (type / lint / unit / security) | 3/9 (token / a11y / copy) | none | none | Standard CI; recommend `feature` recipe instead of `acceptance` |

Every PR must declare its Tier at the top. Tier-S+A PRs without an evidence package are auto-rejected. Tier-C PRs invoking `acceptance` recipe auto-downgrade to `feature`.

**Design Proof exemption**: Tier-S/A PRs with `ui_dimension == none` (pure backend / infrastructure / data pipeline) skip Design Proof entirely. The exemption is recorded in the evidence package as `design_proof: skipped (no UI surface)`.

**Why Tier-based**: AAOS at full scope is over-engineering for ~99% of PRs (omen FM-L4-1: evidence-completeness illusion; magi DA challenge: YAGNI for non-critical paths). Tier-based application is the DA-compelled boundary that keeps the cost-benefit positive.

---

## Evidence Package — Required Fields

Every Tier-S/A PR must attach:

| Field | What | Owner Skill |
|-------|------|-------------|
| `intent` | Change purpose in 1-3 sentences | author / `scribe` |
| `scope` | Affected files, modules, user journeys | `ripple` |
| `spec_diff` | Diff of spec graph nodes touched | `attest` / `accord` |
| `generated_tests` | Auto-generated contract / property / fuzz / E2E / a11y / VRT | `radar` / `voyager` / `mint` / `matrix` (qa-scenario) |
| `execution_log` | Full test run output (pass / fail / coverage) | CI |
| `ui_trace` | Playwright / CUA trace for UI changes | `voyager` / `vector` |
| `screenshot_diff` | Before/after with diff% | `voyager` (visual comparison) |
| `db_diff` | Schema + sample-row delta | `schema` / `tuner` |
| `api_contract_diff` | OpenAPI / Pact contract delta | `attest` |
| `adversarial_findings` | What attackers / edge-case agents tried + couldn't break | `vigil` / `sentinel` / `voyager` |
| `rollback_condition` | Runtime metrics that auto-roll-back the change | `beacon` / `mend` |
| `regression_proof` | Evidence existing spec invariants are preserved | `attest` / `radar` |

Missing fields = automatic Gate rejection. The author cannot self-attest completeness — at least one independent agent (or engine, see Cross-Engine Diversity below) must verify each field.

---

## Design-Side Evidence Fields (Layer B)

When `ui_dimension != none`, the following 9 fields are required in addition to the 12 Code-side fields above. Orchestrated by `atelier`, evaluated by the Design Compiler (see below).

| Field | What | Owner Skill |
|-------|------|-------------|
| `token_proof` | All colors / spacing / radii / shadows / typography resolve to allow-listed design tokens | `muse` |
| `component_proof` | All interactive elements use design-system components, not ad-hoc `<div onClick>` (G9 4-layer detection) | `frame` |
| `state_proof` | Every interactive component declares hover / focus / disabled / loading / error / empty states | `palette` / `weave` (state machine spec) |
| `responsive_proof` | Layout passes at mobile / tablet / desktop viewports (320 / 768 / 1280 minimum) | `palette` |
| `a11y_proof` | WCAG 2.2 AA via axe-core / Pa11y; keyboard navigation; focus order; aria correctness | `canon` |
| `vrt_proof` | Visual regression diff within tolerance per Matrix Sampling Policy (see below) | `vitrine` / `voyager` (visual comparison) |
| `copy_proof` | Microcopy passes voice/tone rules, banned-word list, length constraints, locale-appropriate | `prose` |
| `ux_task_proof` | AI user personas (impatient / first-time / screen-reader / mobile / payment-failure) complete primary tasks | `echo` / `matrix` (qa-scenario) |
| `brand_proof` | Visual identity, illustration style, motion language conform to brand rules (advisory if unspecifiable — see Carve-Out) | `vision` |

Each field carries the same semantic-non-emptiness rule as Code-side: empty findings without an exploration log = rejected, not "no issues".

**Prerequisite for Design Proof adoption**: organization runs Figma + design tokens (Style Dictionary / Tokens Studio) + Code Connect (or equivalent Figma↔code mapping). Organizations missing any of these three should treat Design Proof as opt-in advisory, not blocking. Without tokens, `token_proof` cannot be machine-evaluated; without Code Connect, `component_proof` requires manual audit.

---

## Design Compiler vs Design Reviewer

A common failure pattern in 2024-2025 was deploying LLMs as "design reviewers" asked open questions like "is this design good?" — the LLM produces plausible-sounding flattery and false positives, designers lose trust, the practice is abandoned. Avoid this.

**Use AI as a Design Compiler, not a Design Reviewer:**

```
INPUT  : Figma + Design Tokens + Component Library + UX Rules + Brand Rules + A11y Rules
COMPILER: rule-based (token allow-list, AST checks, axe-core, state coverage)
        + LLM-as-judge (advisory only, never blocking) for the residual ~20-30%
OUTPUT : PASS / FAIL per rule, with rule-citation for every FAIL
```

The Compiler answers closed binary questions ("does this UI violate rule R?"), never open ones ("is this UI good?"). 70-80% of Design Proof fields are decidable by deterministic rules (token check, AST, axe-core, Storybook coverage); the remaining 20-30% (brand voice, motion feel, illustration quality) routes to the Unspecifiable-Quality Carve-Out.

---

## Acceptance Gate — Decision Rules

The Gate (typically `judge` + `attest` for Layer A; `atelier` + `canon` for Layer B) is the merge authority for Tier-S/A. Rules:

1. **Schema completeness** — every required field (12 Code + 9 Design when applicable) must be present and non-empty. Empty `adversarial_findings` or `ux_task_proof` ≠ "no findings"; require a non-trivial exploration report.
2. **Spec consistency** — if `spec_diff` is non-empty, the spec change itself must be re-validated against meta-invariants (see Spec Self-Bug below). Design-side equivalent: Design-Code Contract changes must pass Contract Meta-Oracle (see below).
3. **Cross-engine quorum** — for Tier-S, evidence must be produced or verified across at least 2 different engines. **Default baseline: Claude + Codex (dual-engine, always available).** Tri-engine combinations (Claude + Codex + agy) add coverage when agy is AVAILABLE at PREFLIGHT. Single-engine evidence is CANDIDATE, not CONFIRMED. See `_common/MULTI_ENGINE_RECIPE.md §Base Engine Policy`.
4. **No semantic short-circuit** — schema-valid but semantically empty outputs (e.g. "no issues found" with zero exploration) trigger a hard re-run, not a pass.
5. **Random sampling escape valve** — see Success-PR Random Review below.
6. **Layer A + Layer B joint verdict** — when both layers apply, PASS requires both. Either FAIL blocks merge. A common failure mode is "Code Proof PASS shipped despite Design Proof FAIL" — the Gate must not split-merge.
7. **Unmeasurable-Quality Audit (G7)** — Compiler/Matrix/Contract PASS is not sufficient for merge when human-judgment dimensions are touched. See G7 below.

If the Gate rejects, the change cannot bypass via `--no-verify` style escapes. The only legitimate bypass is the Hot-Fix Fast-Path (see below).

---

## Three Mandatory Guardrails (omen-derived)

These are not optional polish — without them the Proof-Carrying PR pipeline degrades into a more expensive version of conventional CI.

### G1. Cross-Engine Diversity for Adversarial Roles

**Problem**: If `implementer-AI`, `oracle-generator-AI`, and `adversarial-explorer-AI` all run on the same model family, they share blind spots. The adversary cannot find a bug the implementer didn't think of, because both reason from the same priors. omen FM-L3-4 calls this **correlated LLM failure** — the most insidious failure mode because no individual run looks wrong.

**Rule**: For Tier-S, the implementer engine and the adversarial-verifier engine must be different families. Recommended split:

**Tri-engine (when agy AVAILABLE at PREFLIGHT):**
- Implementer → Codex (code-gen strength, sandbox-first)
- Oracle generator → agy (long-context spec reasoning)
- Adversarial explorer → Claude (judgment + edge-case enumeration)

**Dual-engine baseline (default when agy UNAVAILABLE):**
- Implementer → Codex (code-gen strength, sandbox-first)
- Oracle generator → Codex with explicit "treat spec as ground truth, do not regenerate from training-data priors" framing — uses a fresh Codex subagent with different prompt context to preserve cross-frame diversity against the implementer
- Adversarial explorer → Claude (judgment + edge-case enumeration)

For Tier-A, two-engine split is sufficient (Claude + Codex baseline). Tier-B can run single-engine.

Reference: `_common/MULTI_ENGINE_RECIPE.md` (engine dispatch), `nexus/reference/summit-recipe.md` (engine-strength routing).

### G2. Success-PR Random Review

**Problem**: When humans only see failed PRs (as the AAOS end-state implies — "the only PRs humans review are the ones that failed"), reviewer skill atrophies (omen FM-L4-6, RPN=900) and Gate false-negatives become invisible (omen FM-L4-1). Confidence in the Gate becomes self-referential.

**Rule**: A randomly sampled fraction of *successful* Tier-S/A PRs must be routed to human review post-merge. Suggested rate: 5% for Tier-S, 2% for Tier-A. Findings feed back to:
- Gate rule updates (false-negative correction)
- Adversarial explorer prompt tuning (new attack vectors)
- Reviewer skill maintenance

Random sampling is recorded as Gate evidence, not as a delay — sampled PRs ship normally; the review is asynchronous and audits the Gate, not the change.

### G3. Repair-Loop Circuit Breaker

**Problem**: Runtime oracles trigger auto-rollback → trace capture → minimal-repro generation → AI-authored fix PR → Acceptance Gate re-runs. This is theoretically a closed loop. In practice, the same root cause can manifest as multiple distinct-looking symptoms, and the AI repair-PR system can generate cosmetically-different fixes for the same underlying bug indefinitely. omen FM-L5: **infinite remediation loop**.

**Rule**: Repair attempts are rate-limited per failure signature:
- Same signature (normalized stack + endpoint + error class): **max 3 repair attempts per 24h**
- After cap, the Gate escalates to a human and refuses further auto-repair on that signature for 7d
- Different signature on the same module: separate counter

Repair-loop telemetry (signature counts, escalation rate) is a first-class SLO. A rising escalation rate is itself a signal of spec-graph rot or correlated-failure leakage.

Reference: `mend/SKILL.md` (repair runbook safety tiers), `beacon/SKILL.md` (runtime oracle metrics).

---

## Additional Guardrails (G4-G10, v2)

These extend G1-G3 with concerns surfaced when Code Proof + Design Proof two-axis decomposition is introduced. Each cites the omen failure mode it mitigates.

### G4. Differential Implementation Diversity

**Problem**: "Two AIs implement the same spec, CI diffs them — if diff = 0, ship." This works only when the two AIs do not share the same misreading. If both are the same LLM family, they share priors and the same statistical bias → silent agreement on a wrong reading (omen FM-A1, RPN=630, S=9). LLM-vendor diversity is not the same as training-data diversity (omen FM-A8, RPN=540).

**Rule**: When Dual-Implementation Oracle is used (see §Dual-Implementation Oracle):
1. AI-A (production) and AI-B (reference oracle) MUST run on different LLM families. **Default baseline**: AI-A on Claude, AI-B on Codex (or vice versa) — these are the two always-available engines and have non-overlapping training-data priors. agy may substitute for either when AVAILABLE. Same-family combinations (e.g. two Claude subagents) FAIL G4 even with prompt differentiation.
2. Prompt scaffolding MUST differ (one-shot vs few-shot, English vs Japanese spec, natural-language vs formal spec).
3. AI-A and AI-B verdicts triangulate against Source-of-Truth Spec (see G10), not against each other only.
4. Adversarial reviewer (AI-C) runs on yet a third engine to defeat reviewer bias toward either implementation (omen FM-A6). **When only 2 engines are available** (Claude + Codex, agy UNAVAILABLE), AI-C runs on a fresh subagent of whichever engine was NOT the implementer, with an explicit "adversarial mode — assume the implementer made plausible-looking mistakes" framing. Two-engine cyclic assignment (AI-A:Claude, AI-B:Codex, AI-C:Claude-adversarial) is acceptable for Tier-S when agy is UNAVAILABLE.

### G5. Diff Semantics Classifier

**Problem**: VRT runs and dual-implementation runs produce diff floods. Floating-point ordering changes, 1px shifts, and locale rerenders generate hundreds of cosmetic diffs that bury the rare semantic diff. Reviewers learn to click "Approve all" — VRT formalism stays, signal dies (omen FM-B2, RPN=720; FM-A4, RPN=504).

**Rule**: Every diff (code, VRT snapshot, dual-impl output) MUST be classified before reaching a reviewer:
- `cosmetic` — floating-point trailing digits, sub-pixel shifts, deterministic re-renders → auto-approve eligible
- `semantic` — different computed value, different state set, different rendered text → MUST be reviewed
- `breaking` — type change, API contract break, removed UI affordance → senior review + full property-test re-run

"Approve all" actions on >10 diffs are forbidden at the tool level. Diffs >50 force PR split. Classifier model is itself shadow-run before becoming Gate-blocking (per Cost & Scalability).

### G6. Goodhart-Resistant Coverage Metrics

**Problem**: When Compiler / VRT / Contract coverage becomes a KPI, teams optimize for "rule areas easy to coverage-up" (color tokens, padding) and neglect rule-hard areas (motion feel, brand consistency, cross-axis combinations). Coverage rises, perceived quality falls (omen FM-C4 / FM-B4).

**Rule**: Coverage metrics are never published alone. Pair each coverage number with a second-axis indicator:
- Compiler coverage % ↔ NPS or qualitative-review-hours
- VRT coverage % ↔ user-reported visual regression count
- Contract coverage % ↔ post-merge design-fix PRs
- A11y rule coverage % ↔ assistive-tech user feedback

Single-metric OKRs are forbidden for proof-system coverage. Quarterly audit reviews where coverage grew vs where it stayed flat — uneven growth flags Goodhart drift.

### G7. Unmeasurable-Quality Audit Gate

**Problem**: Design Compiler PASS ≠ "design is good". Compiler verifies what is rule-encoded. Out-of-rule dimensions (timing of a confirmation modal, emotional tone of an empty state, brand fidelity of an illustration, fairness of an interaction pattern) are not in the rule set, and a Compiler PASS bestows false confidence on dimensions never evaluated (omen FM-C1, RPN=800; FM-C3, RPN=729; FM-D3, RPN=567).

**Rule**: For Tier-S/A UI changes, Compiler/Matrix/Contract PASS triggers a separate Unmeasurable-Quality Audit before merge:
- **Tier-S UI**: human designer sign-off on "feel / timing / overall coherence" with recorded review time (≥10 min)
- **Tier-A UI**: weekly summary review of merged changes; sampled deep-review per G2
- The PASS badge wording MUST say "rule coverage verified" — never "quality verified" or "design approved"
- If designer-review hours decrease >30% YoY after Compiler adoption, flag atrophy warning

This is the design-side equivalent of G2 (success-PR random review) — protects against reviewer atrophy in dimensions that machines cannot judge.

### G8. Design Hot-Fix Fast-Path + Component Sandbox

**Problem**: Design-Code Contract rigor prevents experimentation. New components, A/B test variants, marketing LP one-offs, and emergency brand reactions all need to bypass Contract — without a sanctioned path, teams invent unofficial bypasses (omen FM-D5, FM-D6, FM-C7).

**Rule**: Two sanctioned channels prevent unofficial bypass invention:

1. **Component Sandbox** — Figma + Storybook region for exploratory prototypes outside Contract. Production routes cannot import from sandbox. Promotion from sandbox to Contract follows a reverse-direction flow: prototype first, contractualize after validation.
2. **Design Hot-Fix Fast-Path** — marketing LPs, time-boxed campaigns, emergency brand reactions can deviate from token / contract under a **90-day expiration**: by day-90, the deviation is either promoted to Contract or removed. Tracked the same way as Code Hot-Fix Fast-Path (auditable, >3/month per product triggers process review).

The Hot-Fix Fast-Path (existing, code-side) is extended below in its own section to cover Design side.

### G9. UI-Structure Detection Layer (Swiss-Cheese 4-Layer)

**Problem**: "AI builds button as `<div onClick>` instead of `<Button>` → fail" is the proposal's stated rule. Without an actual detection implementation, the rule is aspirational. A single detection layer misses something (`<span role="button">`, `<a onClick>` with no `href`, custom hooks wrapping a `div`) (omen FM-D4, RPN=512).

**Rule**: Component contract enforcement requires 4 independent detection layers (Swiss-Cheese model — one layer's miss is caught by another):
1. **AST static analysis** — ESLint custom rule: any interactive element not from the DS component allow-list fails build.
2. **Storybook coverage** — every interactive element type must have at least one Storybook story; CI fails if production imports types absent from Storybook.
3. **Runtime DOM trace** — E2E suites snapshot the rendered DOM; non-allow-listed interactive selectors fail.
4. **Code Connect mapping** — every imported DS component must resolve to a Figma component via Code Connect; unmapped imports fail.

Any single layer missing makes Contract enforcement Swiss cheese. All 4 layers MUST be live before `component_proof` is treated as Gate-blocking; until then it ships as advisory-only.

### G10. External Spec Source-of-Truth Lock

**Problem**: Without a single authoritative spec, two implementations can drift in opposite directions (each adjusting to symptoms) and oracle drift becomes invisible (omen FM-A2, RPN=512; FM-A7, RPN=448).

**Rule**: Dual-Implementation, Design-Code Contract, and Design Compiler all share one Source-of-Truth Spec:
- Spec is in executable form (formal spec / type-level / contract test / state machine DSL) — not free-text docs
- AI-A, AI-B, Figma Component, Code Connect mapping all verify against Spec, never against each other directly
- Spec drift (implementation evolves independently) is monitored quarterly via spec-vs-implementation diff
- External SaaS outages (Figma / Chromatic / MCP Server) are themselves part of Spec — degraded-mode behavior is specified, not improvised

This locks the architecture against the "everyone is correct relative to everyone else, but no one is correct relative to the spec" failure pattern.

---

## Cross-Cutting Guardrails (v3 — apply to Tier A / B / C)

These three guardrails address failure modes that span every tier: the integrity of the knowledge base AI references, the regulatory envelope that constrains autonomous action, and the lifecycle discipline of long-lived authoritative artifacts.

### G11. Knowledge Base Write Authority Separation

**Problem**: When AI can both **read** authoritative knowledge (specs, design tokens, brand constitutions, insight ledgers, runbooks) and **write** to it, systematic self-justification follows. Successful artifacts cause AI to silently raise the confidence of supporting entries; failed artifacts cause AI to shorten the expiration of contradicting entries. Within months the knowledge base reflects AI's confirmation bias, not reality (omen FM-F1 RPN=729).

**Rule**: For any authoritative knowledge base AI references during generation:
1. **AI is read-only** — cannot directly mutate entries
2. **Proposed edits go to a queue** — only a human role (Research Lead / Brand Director / Architect / Spec Owner) can merge
3. **Confidence is deterministic** — formula-derived (N × variance × age × counter-evidence weight), never hand-set
4. **Provenance and diff are logged** — every mutation records editor identity, evidence delta, counter-evidence delta
5. **Devil's Advocate reviewer LLM** — different LLM family from the generator; signs every human-merge

**Scope**: applies to spec graphs (Tier A/B), design tokens & Constitution (Tier B/C), insight ledgers (Tier C), and any runbook / playbook AI can author.

**Anti-pattern**: "AI can write with audit log" — audit is reactive, bias accrues before detection.

### G14. Regulatory Envelope Pre-Flight Check

**Problem**: Autonomous-action systems (auto-scale, auto-rollback, auto-generation, auto-publish) operate by default-permit unless a regulatory check intervenes. Regulated industries (medical / financial / aviation / public-sector / pharmaceutical / political) require pre-approval, content auditing, and human sign-off that conflict with default-permit. A single regulation change (iOS ATT semantics, Cookie deprecation, EU AI Act, DMA / DSA, 薬機法 / 景表法 / 金商法 / 公職選挙法) cascades into 4-system simultaneous degradation (omen FM-E6 / FM-X4 / FM-X6).

**Rule**:
1. **Every action artifact (PR / campaign / spec change) declares `regulatory_jurisdiction`** — industry + country + applicable laws
2. **Per-jurisdiction toggle** — auto-scaling, holdout testing, AI-generated content, auto-rollback are independently enable/disable per jurisdiction; regulated default: OFF
3. **Quarterly Regulatory Horizon Scan** — Legal + DataEng publish expected upcoming changes
4. **Per-concept Assumption Document** — for each gate (Code/Design/Market/Research/Brand), document which signals required, which jurisdictions affected
5. **Pre-built fallback measurement stacks** — MMM / geo-experiments / synthetic control ready to activate when primary measurement is jurisdictionally unavailable

**Scope**: applies to Tier A merge gates (compliance code) + Tier B design (a11y / GDPR cookie / DMA) + Tier C all autonomous market action.

**Anti-pattern**: "We're not regulated" — DMA / DSA / GDPR reach extends beyond intuition.

### G15. Constitution Lifecycle Discipline

**Problem**: Static authoritative artifacts (Spec Graphs, Design Systems, Brand Constitutions, Style Guides, Compliance Frameworks) drift from reality silently. Five-year-old artifacts continue blocking new work that doesn't fit the old worldview, while no one feels authorized to update them. Outcomes: customer-implementation mismatch, designer creativity lattice, brand mummification (omen FM-G2 / FM-G7 / FM-X3).

**Rule**: Every authoritative artifact partitions into 3 layers with different update cadences:

| Layer | Stability | Review Cadence | Editor Authority | Example |
|-------|-----------|----------------|------------------|---------|
| **Core** | 10-year stable | Decade challenge only | Founder / Board sign-off | "Our mission is privacy" / "All payments must be auditable" |
| **Strategic** | 3-5 year review | Annual review + ad-hoc challenge | C-level + senior leadership | Target segment, positioning, distinctive assets |
| **Operational** | 12-18 month review | Quarterly review mandatory | Department lead + 2-person sign-off | Tone rules, banned words, current campaign constraints, current spec versions |

**Enforcement**:
1. Operational layer auto-expires; Compiler / Gate refuses to pass new artifacts if Operational is stale (forcing function)
2. Two-person sign-off required for any edit (no single editor authority)
3. Emergency Override (single-editor patch) is time-boxed: 48h fast-path, must be replaced by normal-Gate within 7 days
4. Quarterly "Constitution Health Audit" — % of Operational entries refreshed in past 6 months

**Scope**: applies to spec graphs (Tier A/B), design tokens & systems (Tier B), brand constitutions & voice guides (Tier C), all "we have always said X" type artifacts.

**Anti-pattern**: "Annual review meeting" — historically skipped under quarterly business pressure.

---

## Spec Self-Bug Problem

The spec graph is now the oracle. **What validates the oracle?** This is the classic specification-of-specification problem (omen FM-L1-1, magi Sophia S2). AAOS-style systems collapse silently when the spec is wrong, because every layer below trusts it.

**Mitigation**: Spec changes themselves are subject to:

1. **Multi-view cross-check** — same intent expressed as (a) user story, (b) state machine, (c) API contract / DB invariant. The three must be consistent; divergence flags the spec change for human review.
2. **Meta-invariant tests** — small set of invariants that must hold across all spec versions (e.g. "no state in the FSM is unreachable", "every API contract has at least one consumer test", "no DB invariant references a column that doesn't exist").
3. **Spec-graph diff is itself Proof-Carrying** — spec changes get their own evidence package, generated by a different agent than the one proposing the spec change.

The spec is never trusted just because it parses. It is trusted because it passes its own meta-oracle.

---

## Unspecifiable-Quality Carve-Out

Some properties resist machine specification. Both Code-side and Design-side have unspecifiable dimensions:

**Code-side unspecifiable**:
- Ethical edge cases (discrimination in scoring, fairness in ranking, manipulation in recommendations)
- Dark-pattern detection (opt-out friction, hidden costs, confirmation traps)
- Cross-cultural appropriateness of business logic

**Design-side unspecifiable** (added in v2):
- Brand voice, tone, illustration style coherence
- "Feel" of motion / animation timing / interaction quality
- Information density and cognitive load
- Empty-state and error-state emotional appropriateness
- Custom dashboards, data visualization, bespoke canvases — anything not reducible to DS components

**Rule**: These are explicitly declared **out of scope** for the Acceptance Gate. Changes touching these dimensions require human review regardless of Tier. The Gate must not silently approve them on the basis that "no oracle flagged it" or "Compiler returned PASS" — absence of evidence is not evidence of absence.

LLM-as-judge MAY produce advisory opinions on these dimensions but MUST NOT block merge. Advisory opinions are recorded as `unspecifiable_advisory` in the evidence package; humans choose whether to act.

**Carve-out monitoring**: track the % of Tier-S/A PRs that invoke the carve-out per quarter. If >20%, this signals either (a) Design Compiler rules are under-specified — extend rules, or (b) the product is operating in genuinely unspecifiable territory — invest in human design review capacity. Either way, the trend matters.

This is the Procrustes-effect mitigation (magi Sophia S7 + omen FM-C1). Without it, AAOS-style systems reduce product quality to "what the spec graph and design rules can represent", and unspecifiable dimensions decay invisibly while metrics show green.

---

## Hot-Fix Fast-Path

**Problem**: Heavyweight evidence requirements on every PR — including 3am production fixes — create organizational pressure to invent unofficial bypasses (`[skip-acceptance]` labels, emergency branches). Once a bypass exists, it normalizes and the whole regime degrades (magi Pathos P1).

**Rule**: Provide an official Fast-Path so no one invents an unofficial one:

1. **Trigger**: P0/P1 incident declared by `triage` (or equivalent on-call agent)
2. **Reduced Gate**: Tier-S downgrades to Tier-A evidence requirements; Tier-A downgrades to Tier-B
3. **Time-boxed**: Fast-Path PR must be replaced by a normal-Gate follow-up within **24h** or it auto-creates a tracking issue and pages the team
4. **Logged**: Every Fast-Path use is auditable; >3/month per service triggers a process review

The Fast-Path is not an escape hatch — it is the official channel that prevents escape-hatch invention.

**Design Fast-Path extension (v2)**: For Design Proof, two sanctioned channels are available (per G8):

1. **Component Sandbox** — Figma + Storybook prototypes outside Contract. Production cannot import from sandbox. Reverse-direction promotion: prototype first, contractualize after validation.
2. **Time-Boxed Deviation** — marketing LPs / time-boxed campaigns / emergency brand reactions can deviate from token / contract under 90-day expiration. By day-90: promoted to Contract or removed. Same audit trail as code Hot-Fix Fast-Path.

Both Design channels are tracked: >3 active Time-Boxed Deviations per product triggers a brand-system process review. Sandbox prototypes that age past 6 months without promotion or removal are flagged for cleanup.

---

## Spec Graph Versioning

Spec graph must be version-controlled alongside code:

- Same repository, same PR
- State-machine nodes are atomic merge units; concurrent edits to the same node trigger conflict resolution (not auto-merge)
- Spec-graph hash is fed as a seed into property-based / fuzz oracle generation, so identical spec produces identical tests (determinism = reproducible Gate verdicts)
- Past spec versions are retained for historical-bug replay

Without this, the spec graph either drifts from code (defeating the purpose) or becomes a parallel-development bottleneck.

---

## Dual-Implementation Oracle (PD-3)

For Tier-S/A PRs touching the regulated-correctness domains below, two independent AI implementations triangulate against the Source-of-Truth Spec. This is a Code-axis-only practice (Design has no equivalent — see Matrix Sampling instead).

**In-scope domains** (Tier-S/A mandatory; Tier-B opt-in):
- Money: pricing, tax, discount, currency conversion, refund computation
- Authorization: RBAC / ABAC, IDOR-prone resource ownership, permission propagation
- State machines: order / booking / payment / workflow transitions, idempotency keys
- Inventory / reservation / two-phase commit
- Regulated-business domain logic (financial, medical, aviation, public-sector)

**Out-of-scope domains** (Dual-Implementation actively harmful):
- UI rendering (continuous 1-px diffs flood signal)
- Text / translation generation (continuous output drift)
- Performance-critical paths (CI cost doubles)
- Legacy-compatibility code (spec is the legacy itself)

**Required protocol** (per G4 Diversity):
1. AI-A (production) on engine E1, AI-B (reference oracle) on engine E2, AI-C (adversarial reviewer) on engine E3 — three different LLM families
2. AI-A receives spec in form F1 (e.g., natural-language); AI-B receives spec in form F2 (e.g., formal spec / decision table)
3. CI runs property-based inputs + production-log replay + boundary values against both implementations
4. Diff classifier (G5) separates cosmetic / semantic / breaking
5. Any semantic diff blocks merge; Source-of-Truth Spec is queried to identify which implementation is correct
6. Both-implementations-agree does NOT auto-pass; G2 success-PR random review still applies; property-based assertions over Spec (G10) MUST be the third triangulation axis
7. `rally engine-paradigm` in COMPETE mode orchestrates AI-A vs AI-B; `judge` adjudicates with AI-C input

**Cost note**: Dual-Implementation effectively doubles implementation tokens for in-scope domains. Apply the per-PR compute cap (Cost & Scalability §) strictly. If cost growth exceeds 1.5× per quarter, narrow the in-scope domain list rather than removing the practice.

---

## Matrix Sampling Policy (PD-2)

The Component State Matrix promises "every component × every state × every viewport × every theme × every locale × every density" coverage. Taken literally, this is exponential in 6 axes. A 200-component DS at 8 states × 3 viewports × 2 themes × 5 locales × 2 densities = **96,000 stories per build** — Chromatic-bankrupting and reviewer-overwhelming (omen FM-B1 / FM-B2).

**Rule**: Default to pairwise (2-way coverage) sampling, escalate to higher coverage only when justified.

| Tier | Default Sampling | Escalation Trigger |
|------|------------------|---------------------|
| **S** | Full pairwise + critical-path full-coverage | Full N-way only for components on payment / auth / PII paths |
| **A** | Pairwise (2-way) on all DS components | 3-way for components on Tier-A critical user journey |
| **B** | Critical-path only (top 10 user journeys) | Pairwise opt-in per component owner |
| **C** | No Matrix sampling | (use conventional VRT only) |

**Reduction techniques** (apply in order):
1. **Equivalence partitioning** — Button variants 6× → 1 parametric story
2. **Pairwise / orthogonal array** — `matrix` skill is the canonical implementation; 2-way coverage typically reduces story count by 10-30× vs full Cartesian product
3. **Critical-path priority** — top user journeys sampled at higher coverage than rare paths
4. **Visual fingerprint dedup** — perceptual-hash identical snapshots collapse into one

**Targets**:
- Story count ≤ 5,000 per build (default ceiling)
- VRT monthly cost ≤ 1.5× existing budget
- "Approve all" actions on >10 diffs forbidden at tool level (G5 enforcement)
- Diff >50 forces PR split

**Locale snapshot semantic limit**: VRT pixel-diff alone cannot detect translation quality, tone breakage, or cultural inappropriateness (omen FM-B4, RPN=560). For Tier-S/A multi-locale PRs, native-speaker semantic review of new copy is required in addition to VRT — pixel-match ≠ translation quality.

---

## Design-Code Contract (PD-4)

Figma component ↔ code component must form a 1:1 typed contract. Violations block merge.

**Four required layers** (all four must be present, per G9 Swiss-Cheese model):

| Layer | Spec | Tooling |
|-------|------|---------|
| 1. Design Tokens | Colors / spacing / radii / shadows / typography in `tokens.json` | Style Dictionary / Tokens Studio |
| 2. Component Map | Figma component ↔ code component path | Figma Code Connect |
| 3. Motion Tokens | Animation duration / easing as tokens | CSS variables / Framer Motion config |
| 4. State Machine Spec | Interactive state transitions (default / hover / focus / active / disabled / loading / error) | XState / `weave` skill state DSL |

**Contract content** (per component):
```
Figma: PrimaryButton
Code: <Button variant="primary" />
Token: color.primary.600 / spacing.button.md / radius.md
States: default → hover → focus → active → disabled → loading
Motion: token motion.button.hover (150ms ease-out)
A11y: role=button, keyboard actionable, focus ring visible (token focus.ring)
```

**Enforcement** (per G9 4-layer detection):
- AI generates `<div onClick>` instead of `<Button>` → ESLint layer 1 fail
- AI uses a color not in token allow-list → AST layer 1 fail
- AI drops the focus state from a Button → Storybook layer 2 fail (state coverage gap)
- AI ships interactive element absent from Storybook → Runtime DOM layer 3 fail
- AI imports a DS component absent from Figma → Code Connect layer 4 fail

**Contract Meta-Oracle** (parallel to Spec Self-Bug rule): Design-Code Contract changes themselves are Proof-Carrying. A Contract edit must (a) be expressed in multiple views (Figma component, token JSON, state DSL), (b) not violate existing meta-invariants (no component without states, no token without category, no orphan Code Connect mapping), (c) propose migration for affected call sites or accept v1/v2 coexistence with documented sunset.

**Contract Versioning** (omen FM-D9 mitigation): v1 → v2 transitions are time-boxed (≤6 months coexistence) and tracked. Indefinite v1+v2 coexistence is a process failure flag.

**External dependency notes**:
- Figma SaaS outage (FM-D1): degraded-mode is part of Spec (G10) — CI behavior under Figma down is specified, not improvised. Default: Contract verification skips, merge allowed with banner; Figma comes back up → contract re-verified post-merge.
- Figma API rate limit (FM-D2): caching layer (`frame` skill) batches CI verification requests; per-team rate budgeting prevents one team starving others.
- Figma MCP version lock (FM-D7): Contract schema version pinned in `.proof-carrying.yml`; MCP breaking changes require a planned migration PR.

**Off-Figma origins** (FM-D8): designs from Slack screenshots / paper sketches / external tools require an intake flow (`frame` skill) to convert into Figma components before Contract verification can proceed. Direct AI implementation from off-Figma source bypassing the intake = Gate FAIL.

---

## Cost & Scalability Guardrails

Full evidence generation per PR is expensive. Without explicit bounds the regime is fiscally unsustainable.

- **Per-PR compute cap**: declare a $ ceiling (e.g. $5/PR for Tier-A, $20/PR for Tier-S). Exceeding the cap escalates to human triage rather than silently consuming budget.
- **Impact-based test selection**: ML-driven selection of which generated oracles to actually run per PR, based on diff analysis. Full re-run only on schedule (nightly / pre-release).
- **Shadow run before block**: new oracle types run in shadow (logged but non-blocking) for ≥3 weeks before becoming Gate-blocking, to surface flakiness.

---

## What Belongs HERE vs in Skill-Specific Files

This protocol defines the **shared concepts and vocabulary**. Skill-specific implementation lives in:

**Code axis (Layer A)**:
- `attest/SKILL.md` — spec compliance verification (Layer 1 + Layer 4 Gate)
- `radar/` `voyager/` `matrix/` (qa-scenario) `mint/` — oracle generation (Layer 2)
- `vigil/` `sentinel/` `voyager/` — adversarial exploration (Layer 3)
- `judge/` — Acceptance Gate adjudication (Layer 4)
- `guardian/` — PR preparation with evidence package (Layer 4 delivery)
- `beacon/` `mend/` — runtime oracle + repair loop (Layer 5)
- `rally/` (engine-paradigm recipe) — Dual-Implementation Oracle (COMPETE mode, G4 orchestration)

**Design axis (Layer B, v2)**:
- `atelier/` — Layer B sub-orchestrator (drives all design skills below)
- `muse/` — design token allow-list + `token_proof`
- `frame/` — Design-Code Contract + Code Connect + `component_proof` + 4-layer G9 detection coordination
- `palette/` — `state_proof` + `responsive_proof`
- `weave/` — state machine spec (interactive component states)
- `flow/` — motion tokens (animation duration / easing)
- `canon/` — `a11y_proof` (WCAG 2.2 AA verification)
- `vitrine/` — `vrt_proof` (visual regression with Matrix Sampling)
- `prose/` — `copy_proof` (microcopy / voice / tone / banned words)
- `echo/` — `ux_task_proof` (persona-based task walkthroughs)
- `vision/` — `brand_proof` (creative direction, advisory for unspecifiable dimensions)
- `matrix/` — pairwise / orthogonal-array sampling for Component State Matrix

**Orchestration**:
- `nexus/reference/acceptance-recipe.md` — Layer A + Layer B orchestrated chain

When implementing one of the above, reference this protocol rather than restating it. When the protocol itself changes, downstream skills inherit automatically.

---

## Anti-Patterns

| Anti-Pattern | Why It Fails | Counter-Rule |
|--------------|--------------|--------------|
| Full AAOS on every PR | YAGNI for ~99% of changes; cost-prohibitive | Tier-based application (S/A/B/C) |
| Single-engine evidence | Correlated failure invisible | G1 Cross-Engine Diversity for Tier-S |
| "No findings" passes the Gate | Schema-valid semantic emptiness | Require non-trivial adversarial exploration report |
| Humans only see failed PRs | Reviewer atrophy + invisible false-negatives | G2 Success-PR Random Review |
| Auto-repair without stop condition | Infinite remediation loop | G3 Repair-Loop Circuit Breaker |
| Spec trusted because it parses | Spec self-bug invisible | Multi-view cross-check + meta-invariants |
| All quality reduced to spec | Brand / ethics / feel decay silently | Unspecifiable-Quality Carve-Out |
| Heavyweight Gate on hot-fixes | Invents unofficial bypasses | Hot-Fix Fast-Path with time-boxed follow-up |
| Spec graph in a separate repo | Drift or parallel-dev bottleneck | Same-repo, same-PR, node-atomic merges |
| Unbounded compute per PR | Fiscally unsustainable | Per-PR cap + impact-based selection + shadow-then-block |
| Dual-Implementation with same LLM family | Correlated misreading invisible (FM-A1/A8) | G4 different LLM families + different prompt scaffolding + G10 Spec triangulation |
| "Diff = 0 means correct" in Dual-Impl | Both can be wrong with same misreading | G10 — verdict requires Spec triangulation, not just A vs B agreement |
| Cosmetic diff floods, "Approve all" | Reviewer fatigue masks semantic regressions (FM-B2) | G5 Diff Semantics Classifier + tool-level "Approve all" ban above 10 diffs |
| Component State Matrix taken literally as full Cartesian product | 96,000 stories, Chromatic bankruptcy | Matrix Sampling Policy — pairwise default, full only for Tier-S critical paths |
| Locale snapshot = translation quality | Pixel-match doesn't catch tone breakage (FM-B4) | Native-speaker semantic review required for Tier-S/A multi-locale |
| Compiler PASS treated as "design approved" | False confidence, designer atrophy (FM-C1/C3) | G7 Unmeasurable-Quality Audit + "rule coverage verified" wording only |
| AI optimizes for "minimum viable PASS design" | 47 identical primary buttons (FM-C5) | Component Variety scoring + brand_proof advisory + Component Sandbox for exploration |
| "AI built button as `<div onClick>`" with single detection layer | Misses `<span role="button">`, custom hooks, etc. (FM-D4) | G9 Swiss-Cheese 4-layer (AST + Storybook + Runtime + Code Connect) — all 4 required |
| Design-Code Contract treated as creative ceiling | Designer creativity atrophies, product museumifies (FM-D6) | G8 Component Sandbox + reverse-direction promotion flow |
| Figma SaaS treated as runtime requirement | SPOF risk (FM-D1) | Degraded-mode in Spec (G10) + post-merge re-verification |
| Indefinite Contract v1 + v2 coexistence | Versioning hell (FM-D9) | Time-boxed (≤6 months) coexistence + tracked sunset |
| Code Proof PASS shipped despite Design Proof FAIL | Split-merge defeats two-axis gate | Acceptance Gate rule 6 — joint verdict; either FAIL blocks |
| Coverage metrics published alone as KPI | Goodhart drift (FM-C4 / FM-B4) | G6 paired second-axis indicators + quarterly Goodhart audit |
| AI can write to authoritative knowledge base (spec / tokens / constitution / ledger) | Self-justification accrues; knowledge base reflects AI confirmation bias | G11 KB Write Authority Separation (AI read-only, human merge, deterministic confidence) |
| Auto-action default-permit in regulated industries | Pharma / financial / political auto-violations; cascade on regulation changes | G14 Regulatory Envelope Pre-Flight (per-jurisdiction toggle, default OFF, quarterly Horizon Scan) |
| Static authoritative artifact drifts unmaintained | Constitution mummification / customer mismatch / creativity lattice | G15 Constitution Lifecycle Discipline (Core / Strategic / Operational layers, forcing function expiration, 2-person edit) |
| **Living Architecture Twin Tyranny** (centralized Architecture Knowledge Graph elevated to Single Source of Truth; reality codebase "corrected" to match Twin when divergence detected) | Twin out-evolves reality, then reality is forced backward to match Twin → 5-10 year architecture mummification, innovation death (omen v5 FM-V-7 RPN 1080, S=10 catastrophic) | Architecture KG stays **advisory**; when KG vs reality diverges, reality wins; KG updates to match reality (NOT the reverse). G11 + G15 applied to Architecture sub-graph in `lore` |
| **Generated Views Only over-strict** (suppressing whiteboard / sketch / draft diagrams as "Proof violations") | Exploration phase thinking is suppressed, design discussions atrophy (omen v5 FM-V-2 / FM-GV-1, RPN 504-576) | Generated Views Only applies to final CI-gated artifacts only; exploration / sketch / draft / proposal diagrams are explicitly carved out. canvas + atlas (c4-model recipe) SKILL.md Always sections enforce the carve-out |
| **Line-based citation silent drift** (`@source:src/api.ts#L12-45` references that point to unrelated code after refactor but still pass existence checks) | False confidence in "evidence-based" docs while actually citing wrong code (omen v5 FM-D-2, RPN 648) | Prefer symbol-based (`@source:billing::createInvoice`) or content-hash (`@source:openapi.yaml#sha256:abc...`) citations. Line-number citations require paired content-hash anchor for drift detection. attest enforces. |
| **Ops Knowledge Graph centralization as separate KG** (parallel ops-side node/edge catalog elevated to its own SoT alongside `lore` Architecture sub-graph; drift between architecture KG and ops KG silently accumulates) | Recreates Twin Tyranny on the ops side (omen v6 FM-5 RPN 640); two KGs evolve in opposite directions, neither matches reality | Ops node types (`secret` / `config` / `feature_flag` / `environment` / `cluster` / `iam_role` / `vulnerability` / `metric` / `terraform_resource` / `kubernetes_object` / `container_image`) and ops edges (`reads_secret` / `exposes_data` / `has_vulnerability` / `scaled_by` / `rolled_back_by` / `deployed_to`) are absorbed as **extension of the existing `lore` Architecture sub-graph**, not a new KG. G11 + G15 + advisory-only-reality-wins rule inherited unchanged. |
| **"Zero-Human Ops Gate" regime drift** (PROOF_CARRYING.md repurposed as platform-engineering bible covering post-merge ops decisions; collides with Phase 5 beacon + mend territory) | Pre-merge acceptance regime semantics blurred with post-merge runtime ops; Compiler PASS at ops layer reproduces G7 false-confidence (omen v6 FM-3 RPN 504, magi v6 Sophia REJECT) | Pre-merge = Acceptance Gate (deterministic, machine-adjudicated); post-merge = beacon SLO oracle + mend repair loop + G3 circuit breaker (already specified Phase 5). Security/Tuning/Environment/Configuration concerns absorbed into existing skills (sentinel/vigil/cloak/attest/oath/bolt/tuner/siege/beacon/scaffold/gear/mend), NOT as new top-level Proof axes. |
| **"No Manual Production Mutation" absolutism** (zero-manual-change rule mandated; drift-detector→AI-follow-up-PR loop assumed to handle 3AM P0 incident speed) | Incident response reality requires seconds-latency manual mutation; mandating drift→AI-PR pushes ops into unofficial bypass (the exact failure Hot-Fix Fast-Path exists to prevent; omen v6 FM-9 RPN 432) | Drift detection is **advisory only** in `gear/environment_drift`; output flows to `mend` for runbook generation; merge never blocked by drift. Existing Hot-Fix Fast-Path with T1-T4 safety tiers + G3 circuit breaker covers the legitimate emergency-response path. |
| **"Reflective Decision OS" pre-proposal meta-gate** (proposing 5 upper-layer Proof axes — Meta / Metacognition / Concept / Philosophy / Decision — positioned ABOVE all existing Code/Design/Product/Security/Ops Proofs, plus parallel Assumption Ledger / Concept Graph / Philosophy Constitution / Decision Contract / Decision Court / Reflective Loop infrastructure) | Compounds 7 known anti-patterns simultaneously: (a) AI self-attestation gaming on narrative Proofs without G11 (omen v7 FM-V7-7 RPN 630), (b) Philosophy Proof Goodhart moralism reproducing G7 false-confidence at meta layer (FM-V7-8 RPN 432), (c) Assumption Ledger ⊥ Insight Ledger dual-SoT recreating Twin Tyranny (FM-V7-6 RPN 405), (d) Cumulative Adoption Fatigue +42 Proof fields breaches proof_theater_rate freeze threshold (FM-V7-2 RPN 360), (e) Constitution proliferation past G15 ceiling (FM-V7-5 RPN 360), (f) Decision Court duplicates magi multi-mode arbitration paths (FM-V7-4 RPN 252), (g) precedent-collapse risk voids Intake Checklist regulatory force after 3 consecutive REJECT (FM-V7-1 RPN 300) | Counter-Rule: absorb intent via **narrow extensions to existing skills only** — `magi` Pre-Decision Framing Check (problem level + alternative framing + implicit assumption gate), `spark` ≥2 alternative framings rule, `lore` `concept_consistency_audit` capability on existing Architecture sub-graph, `harvest` `prediction_vs_actual_check` on existing Insight Ledger `decision_refs`, Insight Ledger schema `category: product_decision` extension (NOT a new Assumption Ledger), `omen` pre-merge advisory premortem surfacing. Zero new protocols / guardrails / ledgers / contracts / constitutions added. |
| **"Proof of Proof / Gate Governance / Meta-Meta-Layer" regress without termination clause** (proposing 14 axes including Proof of Proof above existing gates + Gate Governance L0-L3 + Data Reality + Legal/IP + Business/Finance + Customer Ops + Organization + Vendor + Incident + Agent Lifecycle + Complexity + Sunset + Trust + Exception governance — positioned as meta-meta-layer above v7's meta-layer, with no terminal "who verifies the verifier" stop condition) | 4th consecutive meta-layer proposal in a recurrence pattern (v5 Twin Tyranny → v6 Zero-Human Ops Gate → v7 Reflective Decision OS → v8 Proof of Proof). Compounds: (a) recursive-meta infinite regress with no fixed point (omen v8 FM-V8-4 RPN 432, FM-V8-14 RPN 540), (b) slippery slope endpoint at total-skepticism-architecture where nothing ships (FM-V8-10 RPN 700), (c) Legal-claim gate gaming via LLM interpretation reproduces G7 Goodhart at legal layer (FM-V8-11 RPN 560), (d) Gate Governance L0-L3 ⊥ G15 Constitution Core/Strategic/Operational identical 3-layer collision (FM-V8-5 RPN 450), (e) Customer Ops Proof release-blocking on subjective deliverables = documentation theater (FM-V8-9 RPN 480), (f) Cumulative Adoption Fatigue ~130 proof fields at 4.3× target = proof_theater_rate auto-breach (FM-V8-2 RPN 400), (g) v7 auto-reject rule literal trigger (FM-V8-1 RPN 300) | Counter-Rule: absorb the **4 genuinely uncovered narrow gaps** via existing-skill extensions only — `clause.claim_compliance_check` (advertising claim 景表法 advisory, B.hard wiring, non-blocking), `oath.vendor_risk_assessment` extended with `vendor_lock_in_scoring + exit_playbook + sla_machine_readable_ref` advisory fields, `launch.customer_success_asset_bundle` optional advisory (non-blocking per FM-V8-9), `darwin.capability_regression_baseline` for per-agent prompt/model upgrade regression, `triage.pre_staged_templates_audit + regulated_breach_notification_routing` to clause, `pulse.semantic_metric_schema` capability, Insight Ledger schema `category: metric_definition` extension. **Strategic observation (omen v8 Sophia)**: the recurring "this isn't enough" gap user feels across 4 rounds is NOT closed by adding more meta-layers — it points to **operational under-execution of the existing Quarterly Compliance Tracking Report** (v3.1, defined but not yet measured-in-practice). Strengthening that report's actual quarterly publication discipline (proof_theater_rate sampling, operator_satisfaction survey, checklist_bypass_attempts counting) addresses the underlying architectural concern that no further protocol layer can. |
| **"Sophia Hijack" — citing the prior REJECT's Sophia reasoning as authority for current acceptance** (proposing a new integration / OS / framework spec that quotes the previous round's Sophia observation as legitimacy ground, while structurally substituting "more specification" for the "measurement execution" Sophia called for. Example v9 form: "Autonomous Acceptance OS Spec" cites omen v8 Sophia "the answer is measurement execution, not more frameworks" then proposes 5-component OS framework + 8 completion criteria as the "operational answer". The hijack pattern: when a proposal cites the prior REJECT's reasoning as authority for acceptance, that IS the hijack pattern, not its resolution — the cleverness is itself the signal.) | Most sophisticated form of the meta-layer accumulation anti-pattern (omen v9 FM-V9-11 RPN **900**, max in v-series, S=10/P=10/D=9). Detectability is critical-low because the proposal *appears to be compliance* with the prior audit. Compounds with: completion-criteria-as-forcing-function-escape (FM-V9-8 RPN 648 — 8 measurable conditions substitute for actual measurement of proof_theater_rate / operator_satisfaction / checklist_bypass_attempts that v8 forcing function demanded), 5th-consecutive-precedent-collapse (FM-V9-10 RPN 600). If accepted, framework regulatory force becomes "breakable with sufficiently sophisticated framing"; v10/v11 unconstrained. | Counter-Rule: **the only proposal that can legitimately answer a Sophia observation is the artifact Sophia demanded, not another specification artifact citing Sophia**. v8 forcing function applies to all v9+ proposals regardless of framing: defer all structural protocol changes (including integration-framed / OS-framed / spec-framed proposals) until the **measurement artifact** (Quarterly Compliance Tracking Report with sampled proof_theater_rate, operator_satisfaction survey, checklist_bypass_attempts count) exists. Genuinely-novel synthesis components (e.g. v9 Autonomy Maturity Model L0-L5, Bootstrap Roadmap Phase 1-5 excluding Phase 6 per FM-V8-4 recursive-meta rejection) are admissible as fold-in candidates AFTER Q3 Report publication via Item 7-(a) extension, never as new protocols. v10+ admissibility unchanged regardless of framing sophistication; detect via: does proposal cite prior REJECT reasoning as legitimacy ground? → Sophia Hijack pattern present → defer per v8 forcing function. |

---

## Authoring Principles — Proposal Intake Checklist (v3.1)

After 4 iterations (AAOS → Code+Design → Growth+Brand → Persona+Journey+Product) the protocol stack accumulated **116+ enumerated failure modes, 15 guardrails (G1-G15), 4 protocol files, multiple ledgers/contracts, and 30+ Proof fields**. The 4th iteration's Magi+Omen review surfaced **Cumulative Adoption Fatigue (max RPN 810)** as the dominant risk pattern: each new proposal looks individually valuable but stacking them tips the system into Proof Theater (form-filling without genuine evaluation), Contract proliferation, and operator burnout.

This section is a **structural deceleration device**. Before extending this protocol (new Proof fields, new contracts, new ledgers, new guardrails, new tier, new layer), the proposer (human or AI) MUST process the Intake Checklist below. The checklist deliberately raises the bar for new additions and biases the system toward **fold-in (extend existing skill SKILL.md)** over **bolt-on (new protocol file / new contract / new ledger / new guardrail)**.

### The Checklist (mandatory before any v3.x or v4.x extension)

```
1. EXISTING-SKILL ABSORPTION CHECK (must complete first)
   For each new concept in the proposal, identify:
   - Which existing skill's SKILL.md already covers ≥50% of this concept?
   - What schema/section/Always-Never extension would close the gap?
   - If ≥80% can be absorbed by existing-skill extension, REJECT new protocol/contract/ledger creation.

2. CUMULATIVE-LOAD AUDIT
   - Current Proof field count per skill (target: <10 obligations/skill)
   - Current ledger/contract count (target: ≤3 globally)
   - Current guardrail count (target: ≤15)
   - If proposal pushes any threshold over target, REQUIRE explicit deprecation of existing element.

3. NOVELTY RATIO
   - True-new percentage = (concept not addressable by existing skills + existing protocols) / total proposal
   - If True-new < 20%, REJECT as net-new protocol; absorb into existing.
   - If True-new ≥ 20% AND ≥ 50% of existing-skill absorption tried, allow extension.

4. PROOF-THEATER MONITOR
   - Each new Proof field must declare:
     - Who emits it (specific skill role)
     - Who consumes it (specific gate or downstream agent)
     - What happens on absence (block / advise / log only)
   - Reject Proof fields with vague "ensures quality" purpose statements.

5. ORG-TIER COMPATIBILITY
   - Declare which Org Tier (Solo / SMB / Enterprise) can adopt this extension
   - Solo-incompatible extensions belong in a companion protocol (e.g., GROWTH_BRAND_PROOF.md), not in PROOF_CARRYING.md core.

6. SUNSET / REVIEW CLAUSE
   - Every new addition must declare a review checkpoint (default: 1 quarter post-adoption)
   - Review measures: Proof Theater rate, operator satisfaction, wired skill count, false-positive rate
   - Threshold-breach triggers rollback, not silent persistence.

7. FOLD-IN PRECEDENCE RULE
   Default decision tree on the proposer's question "where does this go?":
     a. Can an existing SKILL.md absorb it via schema/Always-Never extension? → Extend that SKILL.md.
     b. Can an existing companion protocol absorb it via minor update? → Update that protocol.
     c. Is this truly orthogonal AND ≥20% novel AND Org-Tier-incompatible with core? → New companion protocol.
     d. Otherwise → REJECT.

8. NAMING CONFLICTS
   - Check `claude-skills` skill registry for naming collisions before proposing new skill names
   - Avoid Ledger/Contract/Compiler proliferation: prefer "category" extension of existing Ledger over new Ledger
```

### Why this matters

Without this checklist, the empirical pattern observed across v1→v4 is:
- **v1→v2 marginal value**: HIGH (Design axis closes a real gap)
- **v2→v3 marginal value**: MEDIUM-HIGH (Growth/Brand closes commercial gap)
- **v3→v4 marginal value**: LOW (70% absorbable by existing skills, 30% novel)
- **v4→v5 projection without checklist**: marginal value approaches zero while accumulated load triggers operational collapse (Proof Theater rate ≥60%, operator satisfaction <40%)

The checklist's purpose is not to reject all extensions — it is to **force the proposer to do existing-skill absorption analysis first**, which converts most extensions from "new protocol" into "minor SKILL.md update", preserving the ecosystem's coherence.

### Process

1. Proposer (human or AI) drafts the new concept.
2. Before opening a PR / starting implementation, run the Checklist as a self-review.
3. Document the answer to each item in the PR description.
4. Magi `arbitrate` or `multi` Recipe reviews the checklist output before approving the extension.
5. Architect coordinates the fold-in vs bolt-on decision (default: fold-in).

### Exemption clause

The Checklist does not apply to:
- Bug fixes / typo corrections in existing protocol text
- Documentation-only clarifications (no schema change)
- Sunset / deprecation of existing fields (encourages reduction)
- Cross-references between existing skills (improves discoverability without adding obligations)

### Quarterly Compliance Tracking Report (v3.1, added by v5 fold-in)

The Proposal Intake Checklist is only effective if its application is **measured continuously**. Without measurement, the Checklist degrades into a documentation artifact ignored at proposal time (this is exactly the failure pattern Magi v5 / omen v5 reviewed when scoring "Cumulative Adoption Fatigue" at RPN 810).

A Quarterly Compliance Tracking Report is therefore part of the protocol. Magi (or any designated steward) MUST publish the report each quarter; threshold breaches trigger automatic Magi arbitration before the next proposal can be accepted.

**Report contents (mandatory)**:

```yaml
quarterly_compliance_report:
  quarter: <YYYY-Q[1-4]>
  proposals_reviewed: <count>
  outcomes:
    rejected_at_item_1_absorption: <count>   # existing-skill absorption >=80%
    rejected_at_item_2_cumulative_load: <count>
    rejected_at_item_3_novelty: <count>      # True-new <20%
    needs_rework_at_item_4_proof_theater: <count>
    routed_to_fold_in: <count>               # existing SKILL.md extension
    routed_to_companion_protocol: <count>    # new _common/*.md companion
    routed_to_new_protocol: <count>          # NEW PROOF_CARRYING.md core extension (rare)
  cumulative_metrics:
    proof_field_total_per_skill_max: <number>  # threshold: <10/skill
    ledger_contract_count_global: <number>     # threshold: <=3
    guardrail_count: <number>                  # threshold: <=15 (G1-G15)
    protocol_file_count: <number>              # threshold: <=4 (PROOF_CARRYING, GROWTH_BRAND, GIT, HANDOFF)
  health_indicators:
    proof_theater_rate_sample: <%>             # sampled audit of Tier-S/A PRs; target <=20%
    operator_satisfaction_survey: <%>          # target >=60%
    checklist_bypass_attempts: <count>         # proposals that tried to skip Checklist
  next_proposal_block:
    triggered: <true|false>                    # any threshold breach => true
    reason: <which threshold>
```

**Threshold breach behavior**:
- `proof_field_total > 40` (any skill) → next proposal MUST pass Item 2 with explicit deprecation
- `ledger_contract_count > 5` → next proposal that adds another ledger/contract is auto-rejected
- `guardrail_count > 18` → next proposal that adds another guardrail is auto-rejected
- `proof_theater_rate > 30%` → freeze on new Proof field additions until rate returns to target
- `operator_satisfaction < 40%` → mandatory Magi `multi` arbitration on regime continuation

**Authoring discipline**: Steward (default: Magi at every `arbitrate` invocation) MUST refer to the most recent Quarterly Report when processing a new proposal. The Checklist is not a one-time gate at protocol introduction; it is a continuous discipline.

**Audit trail**: Every accepted extension MUST cite which Quarterly Report's thresholds it was evaluated against. This enables retroactive audit if regression is detected later.

**v5 baseline (initial)**: At v5 fold-in time the baseline values are: proof_field_total ~30, ledger_contract_count 4 (Spec / Design-Code / Insight / Growth-Brand), guardrail_count 15, protocol_file_count 4. These are the **soft ceiling** for v6+ proposals.

**v9 audit trail (Round 9 — "Autonomous Acceptance OS Spec" proposal: 5 integration components — Unified Knowledge Graph + Proof Pack Standard + Acceptance Gate Protocol 4-tier (Hard/Risk/Learning/Advisory) + Autonomy Maturity Model L0-L5 + Bootstrap Roadmap Phase 1-6 + 8 completion criteria)**: Reviewed and **REJECTED as new protocol** under v3.1 Intake Checklist + v8 forcing function. **5th consecutive REJECT** confirms Intake Checklist regulatory force as durable architectural law that survives even the most sophisticated framing attempts. magi 3-0 HYBRID — REJECT_AS_NEW_PROTOCOL + DEFER-NARROW-EXTENSIONS (weighted confidence 83, REJECT) + DEFER (74, fold-in) conditional on 2026-Q3 Quarterly Compliance Tracking Report publication. omen 12-of-12 AP=H failure modes (TOP-3 RPN: **FM-V9-11 Sophia Hijack 900** — the highest RPN in v-series and most insidious pattern named yet / FM-V9-8 completion-criteria-as-forcing-function-escape 648 / FM-V9-10 5th-consecutive-precedent-collapse 600). 5 modes at S=10 (critical). **Critical insight surfaced this round**: v9 is the *most sophisticated* form of the meta-layer accumulation anti-pattern — it correctly diagnoses (v5-v8 added layers, integration not addition is needed) and then produces an artifact that *looks like the cure but operates as the disease*. The cleverness is the signal: cite prior REJECT reasoning as authority for current acceptance = hijack pattern, not its resolution. Newly named anti-pattern row added above ("Sophia Hijack"). **Component-by-component coverage audit (magi)**: Unified KG ~92% rebrand of lore Architecture sub-graph (v5/v6/v7/v8-extended); Proof Pack Standard ~90% rebrand of existing 12+9 evidence package fields; Gate Protocol 4-tier ~85% rebrand of Tier S/A/B/C + B.hard/B.pattern/B.tone + design_proof_mode; Autonomy Maturity Model ~40% (60% net-new — L0-L5 per-decision autonomy ladder is genuinely distinct from Org Tier Solo/SMB/Enterprise which sizes the *organization*); Bootstrap Roadmap ~55% (45% net-new — full-stack Tier A+B+C sequencing). Aggregate ~83% rebrand, ~17% net-new — fails Item 3 (<20% novelty threshold) but the genuinely-novel 17% (Maturity Model + Roadmap synthesis) deserves preservation as deferred fold-in candidates. Item-by-item Checklist scores: Item 1 HARD FAIL (~78% absorbable at edge of 80%); Item 2 HARD FAIL (would breach protocol/ledger/contract ceiling simultaneously); Item 3 FAIL (~17% novelty); Item 5 HARD FAIL (Solo cannot operate proposed Universal-Proof-Pack mandatory artifact); Item 8 HARD FAIL (5 simultaneous naming collisions: Unified KG ⊥ lore / Proof Pack ⊥ Evidence Package / Hard-Risk-Learning-Advisory ⊥ Tier-S-A-B-C × B.hard-B.pattern-B.tone × design_proof_mode / Maturity Model ⊥ Phased Adoption + Org Tier / Bootstrap Roadmap ⊥ Phased Adoption). **v8 forcing function assessment**: literally triggered (PROOF_CARRYING.md line 733 "if no report exists by 2026-Q3, v9 auto-rejected regardless of content"; today 2026-05-25; deadline 2026-07-01; 37 days remaining; no Quarterly Compliance Tracking Report has been published). All escape grounds analyzed and rejected: (a) "v9 IS Sophia's operational answer" → omen v8 Sophia specifically said EXECUTION not SPECIFICATION; v9 contains 0 measured values; (b) "integration not addition" → proposal still adds 6 net-new framework artifacts under "integration" branding; (c) "forcing function too rigid" → re-litigated 1 day after commit = framework collapse. **Folded in narrowly (smallest yet, 2 files)**: this anti-pattern row + this v9 audit-trail entry + `GROWTH_BRAND_PROOF.md` Phased Adoption Cross-Tier Note. **Deferred fold-in candidates (post-Q3 Report publication)**: Maturity Model L0-L5 → `nexus/reference/acceptance-recipe.md` Phase 0 as `autonomy_level` axis alongside existing `tier` / `ui_dimension` / `design_proof_mode`; Bootstrap Roadmap Phase 1-5 (Phase 6 excluded per v8 FM-V8-4 recursive-meta rejection) → new `nexus/reference/adoption-sequence.md` cross-referencing existing Tier A/B/C + GROWTH_BRAND Phased Adoption. Both deferrals strictly conditional on first Quarterly Compliance Tracking Report publication with measured `proof_theater_rate / operator_satisfaction_survey / checklist_bypass_attempts` values. **Zero** new protocols / guardrails / ledgers / contracts / constitutions / Proof fields added this round. Cumulative load held flat at v5 baseline (proof_field ~30 / ledger 4 / guardrail 15 / protocol 4). **Forcing function carried forward unchanged**: next proposal that adds another guardrail/contract/ledger/constitution/protocol remains auto-rejected; integration-framed proposals before Q3 Report publication also auto-deferred (newly clarified this round); v10+ admissibility unchanged regardless of framing sophistication. **Authoring discipline confirmed across 5 iterations** — including against the most sophisticated rebrand attempted yet. Sophia Hijack pattern now explicitly documented so v10+ can be detected even if it adopts further-sophisticated framings (e.g. citing v9 audit trail as authority).

**v8 audit trail (Round 8 — Proof of Proof / Gate Governance / Meta-Meta Layer proposal: 14 axes including Proof of Proof + Gate Governance L0-L3 + Data Reality + Legal/IP + Business + Customer Ops + Org/Incentive + Vendor + Incident + Agent Lifecycle + Complexity + Sunset + Trust + Exception)**: Reviewed and **REJECTED as new protocol** under v3.1 Intake Checklist. **4th consecutive REJECT** establishes Intake Checklist regulatory force as **durable architectural law**, not artifact-of-the-moment. magi 3-0 HYBRID — REJECT_AS_NEW_PROTOCOL (weighted confidence 86) + EXTEND_EXISTING_NARROW (confidence 74). omen 15-of-15 AP=H failure modes (TOP-3 RPN: FM-V8-10 slippery slope endpoint 700 / FM-V8-11 Legal Goodhart 560 / FM-V8-14 Total Skepticism exit-clause absence 540; max RPN 700 highest in v-series). 11 modes at S≥9. Item-by-item Checklist scores: Item 1 HARD FAIL (~78% absorbable — edge of 80% threshold), Item 2 HARD FAIL (proposal adds ~100 proof fields / multiple ledgers / contracts / constitutions / courts simultaneously), Item 3 FAIL (~22% true-new), Item 5 HARD FAIL (Solo/SMB cannot operate ~100 fields + L0-L3 + Court), Item 7 → (a) extend existing for genuine gaps + (d) REJECT meta-meta framing, Item 8 HARD FAIL (Gate Governance L0-L3 ⊥ G15 Core/Strategic/Operational 100% naming collision; Proof of Proof ⊥ radar mutation + judge tri-engine + G2/G3; Trust/Explainability ⊥ magi audit + attest; Exception Governance ⊥ Hot-Fix Fast-Path; multiple others). v7 auto-reject rule **literally triggered**. **Recursive-meta failure pattern (v5 Twin → v6 Ops Gate → v7 Reflective OS → v8 Proof-of-Proof) explicitly named as durable anti-pattern**: each REJECT leaves residual dissatisfaction that the next round re-articulates one abstraction layer higher, with no terminal fixed point. Folded in narrowly for 4 genuine partial gaps: `clause.claim_compliance_check` (景表法 / 薬機法 / FTC Endorsement Guides advisory, Brand Compiler B.hard wiring, non-blocking per G7) + `oath.vendor_risk_assessment` extended with vendor_lock_in_scoring + exit_playbook + sla_machine_readable_ref + deprecation_calendar_ref advisory + `launch.customer_success_asset_bundle` optional advisory (help/FAQ/support/sales/customer-notification refs, non-blocking per FM-V8-9 documentation-theater prevention) + `darwin.capability_regression_baseline` (per-agent prompt/model upgrade regression on existing EFS trajectory, Shadow Mode) + `triage.pre_staged_templates_audit + regulated_breach_notification_routing` (Pattern G triage→clause for GDPR 72h / HIPAA / 個情法) + `pulse.semantic_metric_schema` (KPI YAML with formal_definition / event_source / exclusion_rules / bot_filter / dupe_detection / polysemy_caveats) + Insight Ledger schema `category: metric_definition` (single ledger now 4 categories: market_insight | product_decision | friction | metric_definition). **Zero** new protocols / guardrails / ledgers / contracts / constitutions / Proof fields added. Cumulative load held flat at v5 baseline (proof_field ~30 / ledger 4 / guardrail 15 / protocol 4). **omen Sophia strategic observation** (recorded for v9 prevention): the recurring "this isn't enough" gap user feels across 4 rounds is **NOT** an architectural void to fill with more meta-layers — it points to **operational under-execution of the v3.1 Quarterly Compliance Tracking Report itself**. The Report is defined but has not yet been measured-in-practice in this repository (no quarterly proof_theater_rate sampling, no operator_satisfaction survey, no checklist_bypass_attempts counting). Strengthening that Report's actual publication discipline — quarterly measurement + publication + threshold-breach response — addresses the underlying architectural concern that no further protocol layer can. **Recommended forcing function for next quarter**: publish first concrete Quarterly Compliance Tracking Report with measured values before any v9 proposal is accepted; if no report exists by 2026-Q3, v9 auto-rejected regardless of content. **Authoring discipline confirmed across 4 iterations**: user-emphasis ("core / important / biggest missing area") repeatedly did not override structural threshold rules. Cumulative Adoption Fatigue (omen v6 FM-10 RPN 810) prevention precedent now stands on 4 data points. Next proposal that adds another guardrail / contract / ledger / constitution / protocol remains auto-rejected.

**v7 audit trail (Round 7 — Reflective Decision OS proposal: Meta / Metacognition / Concept / Philosophy / Decision Proof + Assumption Ledger + Concept Graph + Philosophy Constitution + Decision Contract + Decision Court + Reflective Loop)**: Reviewed and **REJECTED as new protocol** under v3.1 Intake Checklist. **3rd consecutive REJECT** (v5 Living Architecture Twin → v6 Zero-Human Ops Gate → v7 Reflective Decision OS) — Intake Checklist regulatory force confirmed durable. magi 3-0 REJECT_AS_NEW_PROTOCOL (Logos 88 / Pathos 92 / Sophia 75, weighted confidence 85) + omen 13-of-13 AP=H failure modes (TOP-3 RPN: FM-V7-7 AI self-attestation 630 / FM-V7-8 Philosophy Goodhart 432 / FM-V7-6 Assumption ⊥ Insight Ledger 405). Item-by-item Checklist scores: Item 1 FAIL (~85% absorbable — magi Logos/Pathos/Sophia + accord L0/L1 + spark OST + lore knowledge graph + omen pre-mortem + G15 Constitution + Insight Ledger cover the substantive surface), Item 2 HARD FAIL (proposal adds +42 proof fields / +1 ledger / +1 graph / +1 constitution / +1 contract / +1 court / +1 ontology — simultaneously breaches every CEILING), Item 3 FAIL (~15% true-new), Item 4 PARTIAL, Item 5 HARD FAIL (Solo/SMB cannot operate 42 fields + 9-role court), Item 6 MISSING, Item 7 → decision (a) extend existing SKILL.md, Item 8 HARD FAIL (Decision Court ⊥ magi multi / Constitution ⊥ G15 / Assumption Ledger ⊥ Insight Ledger / Concept Graph ⊥ lore KG / Reflective Loop ⊥ lore decay+harvest — all naming collisions). v6 auto-reject rule **literally triggered** (ledger/guardrail/protocol all at CEILING; proposal adds 4 ledger/contract artifacts vs ceiling=5). User emphasized "this is the core of this system" — Sophia perspective acknowledges the genuine signal (human "違和感" / mismatch IS the final bottleneck not covered by current 6 axes), but the proposed mechanism is ~85% rebrand of existing infrastructure. Folded in narrowly: `magi` Pre-Decision Framing Check Always rule (problem level + alternative framing + implicit assumption gate) + `spark` ≥2 alternative framings Always rule + `lore` `concept_consistency_audit` capability on existing Architecture sub-graph with polysemy preservation + `harvest` `prediction_vs_actual_check` capability using existing Insight Ledger `decision_refs` + Insight Ledger schema `category: market_insight | product_decision | friction` extension (absorbs Assumption Ledger intent) + `omen` pre-merge advisory premortem surfacing (existing capability documented) + 1 new anti-pattern row in PROOF_CARRYING.md. **Zero** new protocols / guardrails / ledgers / contracts / constitutions / Proof fields added. Cumulative load held flat at v5 baseline (proof_field ~30 / ledger 4 / guardrail 15 / protocol 4). **Authoring discipline confirmed**: Intake Checklist functioned as designed for the 3rd consecutive iteration; user-emphasis ("core") did not override structural threshold rules — Cumulative Adoption Fatigue (omen v6 FM-10 RPN 810) prevention now has 3 rejection data points and constitutes precedent. Next proposal that adds another guardrail / contract / ledger / constitution / protocol remains auto-rejected.

**v6 audit trail (Round 6 — Security / Tuning / Environment / Configuration Proof + Zero-Human Ops Gate proposal)**: Reviewed and **REJECTED as new protocol** under v3.1 Intake Checklist. magi 3-0 REJECT_AS_NEW_PROTOCOL (weighted confidence 88) + omen 9-of-12 AP=H failure modes (TOP-3 RPN: FM-10 acceptance-precedent-collapse 810 / FM-5 Ops KG dual-SoT 640 / FM-12 G11 ops-clock-rate collapse 576). Item-by-item Checklist scores: Item 1 FAIL (≥80% absorbable by existing sentinel/vigil/cloak/oath/clause/bolt/tuner/siege/beacon/scaffold/gear/mend/lore), Item 2 FAIL (current proof_field ~30, ledger 4 ALREADY AT CEILING, guardrail 15 AT CEILING, protocol 4 AT CEILING — proposal would add +40 proof obligations / +1 contract), Item 3 FAIL (true-novelty estimated 10-15% — Executable Threat Model + Environment Contract YAML + supply-chain provenance fields are the only net-new portion), Item 4 PARTIAL, Item 5 FAIL (Solo/SMB incompatible), Item 6 MISSING, Item 7 → decision (a) extend existing SKILL.md, Item 8 FAIL (Ops Knowledge Graph collides with lore Architecture sub-graph). Folded in narrowly: `attest.supply_chain_provenance` (advisory, capability-gated) + `sentinel.executable_threat_model_handoff` (STRIDE/LINDDUN YAML) + `gear.environment_drift` (advisory, never blocks merge) + `bolt` continuous-tuning bounds (absorbed dial) + Phase 5 beacon hookup + `lore` Architecture sub-graph ops-node/edge extension (NOT a separate KG) + 3 new anti-pattern rows (Ops KG centralization / Zero-Human Ops Gate regime drift / No-Manual-Production-Mutation absolutism). Zero new protocols, zero new guardrails, zero new contracts/ledgers added. Cumulative load held flat. Baseline thresholds unchanged for v7. **Authoring discipline confirmed**: the Intake Checklist functioned as designed (second consecutive REJECT after v5), preserving precedent against Cumulative Adoption Fatigue (omen v6 FM-10 RPN 810).

---

## References

- AAOS (Autonomous Acceptance OS) original proposal — 5-layer architecture: spec graph → oracle generator → adversarial explorers → Proof-Carrying PR + Acceptance Gate → runtime oracle + auto-rollback
- AWS formal-methods practice for S3 — formal spec + model checking for correctness at scale
- Pact — consumer-driven contract testing pattern
- Property-based testing (Hypothesis / fast-check / PropEr) — properties over examples
- OpenAI Computer-Using Agent + Anthropic Computer Use — adversarial UI exploration substrate
- Argo Rollouts / Flagger — SLO-based progressive delivery with auto-rollback (runtime oracle precedent)
- Magi verdict on AAOS proposal — 3-0 GO-WITH-CONDITIONS, 12 conditions, 5 premise-collapse scenarios
- Omen pre-mortem on AAOS proposal — 32 failure modes, 6 S≥9 Must-Act risks (correlated LLM failure, evidence-completeness illusion, reviewer atrophy, repair storm, spec self-bug, Goodhart inevitability)
- Magi verdict on Code+Design Proof proposal (v2 source) — 3-0 GO-WITH-CONDITIONS (weighted confidence 67.8), 7 conditions C1-C7, orthogonal complement to AAOS
- Omen pre-mortem on Code+Design Proof (v2 source) — 31 new failure modes (4 concepts: A Differential Implementation, B Component State Matrix, C Design Compiler, D Design-Code Contract), 0 fully absorbed by G1-G3, 7 new guardrails proposed G4-G10
- Figma Code Connect (2024) + Figma MCP Server (2025) — Design-Code mapping prerequisites for Design Proof adoption
- Style Dictionary / Tokens Studio — design token SoT (`muse` skill integration)
- Chromatic / Storybook 9 — VRT + Storybook Test integration (`vitrine` skill integration)
- axe-core / Pa11y — WCAG 2.2 AA verification (`canon` skill integration)
- XState — state machine DSL for interactive component states (`weave` skill integration)
- DO-178C N-version programming — regulated-industry precedent for Dual-Implementation Oracle
- AWS S3 parallel-run (legacy compatibility verification) — production precedent for Dual-Implementation in money-domain
- Combinatorial test theory (pairwise / orthogonal-array) — Matrix Sampling Policy basis (`matrix` skill integration)
- Magi verdict on Growth+Brand Acceptance OS proposal (v3 cross-cutting source) — 3-0 GO-WITH-HEAVY-CONDITIONS (weighted confidence 54.7), 12 conditions C1-C12, Phased Adoption (Step 1-4), Org Tier (Solo / SMB / Enterprise) — drove the 3-tier restructure and cross-cutting G11/G14/G15 introduction
- Omen pre-mortem on Growth+Brand Acceptance OS (v3 cross-cutting source) — 25 new failure modes, 7 S≥9 Critical (AI Self-Whitewash FM-F1 RPN=729 / Homogenization FM-E4 / Beige Output FM-G1 / Constitution Mummification FM-G2 / Stop Owner FM-H3 / Privacy Regulation Brittleness FM-X4 / Regulated Auto-Violation FM-E6) — drove G11/G14/G15 cross-cutting placement and `GROWTH_BRAND_PROOF.md` separation
- `_common/GROWTH_BRAND_PROOF.md` — companion protocol for Layer C (Market + Research + Brand axes, lifecycle gates, Insight Ledger, Incrementality Gate, Brand Compiler 3-layer, Growth-Brand Contract). Adopted by Enterprise Tier orgs after Tier A+B foundation is stable
