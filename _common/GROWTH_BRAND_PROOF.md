# Growth & Brand Acceptance Protocol (Layer C)

Companion protocol to `_common/PROOF_CARRYING.md` (Tier A Foundation + Tier B Production Pipeline). This file specifies **Tier C — Market-Brand Acceptance**: the lifecycle gates that constrain AI-generated marketing campaigns, customer research outputs, and brand-touching content.

**Prerequisites**:
- `_common/PROOF_CARRYING.md` v3 (mandatory — Tier A + Tier B foundation, cross-cutting G11/G14/G15)
- `_common/MULTI_ENGINE_RECIPE.md` (cross-engine fan-out)
- `_common/HANDOFF.md` (handoff schema)

**Audience**: Skills participating in pre-design / ship-time / post-launch lifecycle gates.
- **Research axis (R)**: `field`, `voice`, `trace`, `plea`, `tome`
- **Brand axis (B)**: `vision`, `crest`, `prose`, `clause`, `oath`, `muse` (token discipline carry-over from Tier B)
- **Market axis (M)**: `pulse`, `experiment`, `funnel`, `bazaar`, `compete`, `ledger` (FinOps), `harvest`, `cloak`, `vigil` (brand safety)
- **Orchestration**: `nexus[growth-acceptance]`

**Inspired by**: AAOS (v1) → Code+Design Proof (v2) → Growth+Brand Acceptance OS (v3 source). All three round verdicts (Magi GO-WITH-CONDITIONS at confidence 65 / 67.8 / 54.7 respectively) inform this document.

---

## Why Layer C is Separated from PROOF_CARRYING.md

Three structural reasons:

1. **Solo / SMB compatibility** — Tier A+B can be operated by a 1-5 person team. Tier C requires Research / Brand / Growth-analytics specialists (10+ people). Embedding Tier C in PROOF_CARRYING.md would break Solo adoption.
2. **Timing axis differs** — Tier A+B are merge-time gates. Tier C is pre-design + ship-time + post-launch lifecycle gates. Mixing temporal models confuses the contract.
3. **Adoption is staged, not all-or-nothing** — Per magi C8, Layer C adopts in 4 steps: Step 1 (Measurement Loop) → Step 2 (Research + Insight Ledger) → Step 3 (Market + Incrementality) → Step 4 (Brand Compiler blocking). Separation enables each step's adoption decision to be independent.

**Cross-cutting guardrails G11 / G14 / G15 live in PROOF_CARRYING.md v3** because they apply equally to Tier A/B knowledge bases (specs, design tokens) and Tier C knowledge bases (insight ledger, brand constitution). This file references them but does not redefine them.

---

## Org Tier Adoption Policy

| Org Tier | Org Size | Layer C Adoption | Rationale |
|----------|----------|-------------------|-----------|
| **Solo** | 1-5 people | None (skip entire file) | Cannot staff Research / Brand / Growth-analytics specialists; v2 baseline sufficient |
| **SMB** | 5-50 people | Step 1 only (Measurement Loop optional opt-in) | v2 baseline + post-launch measurement loop is the only realistic Layer C subset |
| **Enterprise** | 50+ with Research / Brand / Growth specialists | Step 1-4 phased (mandatory ordering) | Full Layer C achievable with sufficient organizational maturity |

**Mandatory rule** (per magi C8): Never adopt Step N+1 before Step N is stable for ≥3 months. Skipping Steps risks adopting blocking gates without the supporting infrastructure (Insight Ledger before Research process, Brand Compiler before Constitution maturity).

**Cross-Tier Ordering Note (v9 fold-in, partial absorption of Bootstrap Roadmap v9 proposal)**: Layer C Step 1-4 adoption presupposes Tier A (Code Acceptance) + Tier B (Design Acceptance via atelier when `ui_dimension != none`) are already operational in the org. Cross-tier sequence: Tier A merge-time → Tier B merge-time → Layer C Step 1 post-launch measurement → Layer C Step 2-4 advancing per the Mandatory rule above. Organizations attempting Layer C Step 1 before Tier A+B foundation produces post-launch measurement loops that cannot ground in pre-merge evidence — the loop becomes anecdotal rather than evidence-chained. This is the full-stack ordering observation Bootstrap Roadmap Phase 1-5 (v9 proposal) correctly identified; it is documented here as a cross-tier annotation rather than as a new framework artifact. Phase 6 (Proof of Proof / Gate Governance) from v9 is explicitly excluded per v8 FM-V8-4 (recursive-meta infinite regress) rejection.

---

## Phased Adoption: Step 1-4

### Step 1 — Measurement Loop (SMB+ opt-in, Enterprise mandatory entry)

**Goal**: Establish post-launch measurement of every shipped change. Closes the v2 gap (v2 = merge-time only, no post-ship feedback).

**Components**:
- Beacon registers KPI baselines pre-launch
- Pulse + Experiment collect post-launch metrics at +14d / +30d / +90d
- Harvest aggregates findings into a learning record
- Tome stores findings for future reference

**Skills**: `pulse`, `experiment`, `harvest`, `beacon`, `tome`. No new skill needed.

**Blocking?**: No (advisory loop). Findings inform next iteration; do not block current merge.

**Org requirement**: 1 analytics-literate person + working metrics instrumentation.

### Step 2 — Research Proof + Insight Ledger (Enterprise)

**Goal**: AI-generated content / campaigns must cite evidence from a curated Insight Ledger; no thinking-aloud claims.

**Components**: Research Proof (9 fields, below) + Insight Ledger (datamodel + RBAC + AI-attestation, below).

**Cross-cutting**: **G11 mandatory** — AI is read-only on the Insight Ledger; only Research Lead can merge proposed edits; confidence is deterministic-computed, never hand-set.

**Skills**: `field`, `voice`, `trace`, `plea`, `tome`, + new skill `insight` (proposed, Architect responsibility).

**Blocking?**: Yes — content without Insight Ledger citation is rejected at pre-design Phase.

**Org requirement**: 1+ Research Lead (write authority), 3+ Researchers (queue submitters).

### Step 3 — Market Proof + Incrementality Gate (Enterprise + Growth-analytics specialist)

**Goal**: Campaigns auto-scale or auto-stop based on measured incrementality, not vanity metrics.

**Components**: Market Proof (9 fields, below) + Incrementality Gate (measurement-method Decision Tree, below) + Growth-Brand Contract (Tier 0/1/2 templates, below).

**Cross-cutting**: **G13 mandatory** — every Contract names a Stop_Accountable (1 person); 24h no-response → auto-halt. **G14 mandatory** for regulated industries — auto-scale OFF by default.

**Skills**: `pulse`, `experiment`, `funnel`, `bazaar`, `compete`, `ledger` (FinOps), `accord`, `spark`, `scribe`.

**Blocking?**: Yes — campaigns without Contract are non-shippable; Incrementality Gate auto-halts losers.

**Org requirement**: 1+ Growth-analytics specialist (Incrementality methodology), 1+ Legal sign-off for jurisdiction classification.

### Step 4 — Brand Compiler (Enterprise + Brand Director)

**Goal**: All brand-touching content (LP, ads, UI copy, email, SNS, sales decks, press releases) passes a 3-layer Brand Compiler.

**Components**: Brand Proof (8 fields, below) + Brand Constitution (G15 3-layer lifecycle) + Brand Compiler (B.hard / B.pattern / B.tone, below).

**Cross-cutting**: **G15 mandatory** — Brand Constitution split into Core (10y) / Strategic (3-5y) / Operational (12-18mo). **G12 (Diversity Floor) mandatory** — Compiler rejects "minimum viable safe copy" (homogenization counter-pressure).

**Skills**: `vision` (Compiler orchestration), `crest` (brand strategy), `prose` (voice), `muse` (design tokens crossover from Tier B), `clause` (legal), `oath` (regulatory).

**Blocking?**: B.hard (taboo / legal) + B.pattern (tokens / Code Connect) are blocking. B.tone (LLM-as-judge advisory) is non-blocking + weekly sampling audit.

**Org requirement**: 1+ Brand Director (Constitution write authority), 1+ Creative Director (Operational layer maintenance).

---

## Research Proof — 9 Fields

When any AI-generated content cites customer insight, market trend, or user behavior claim, the following 9 evidence fields are required.

| Field | What | Owner Skill |
|-------|------|-------------|
| `source_proof` | Which data source(s) generated the claim | `field` / `trace` / `voice` |
| `sample_proof` | Who was surveyed; N; segmentation; recruitment method | `field` |
| `bias_proof` | Known sampling biases + selection effects explicitly stated | `field` / `plea` |
| `contradiction_proof` | Counter-evidence considered and either reconciled or noted | `magi` / `flux` |
| `triangulation_proof` | At least 2 independent sources support the claim | `field` + at least 1 other |
| `recency_proof` | Source data age; expiration trigger | `tome` |
| `decision_proof` | Which specific decision this claim supports (not unanchored) | `accord` |
| `confidence_score` | Deterministic-computed (N × variance × age decay × counter-evidence weight); never hand-set per G11 | `insight` (proposed skill) |
| `reproducibility_proof` | Methodology document enabling independent replay | `tome` / `field` |

**Semantic-non-emptiness** (G3 carry-over from Tier A): empty fields without a documented exclusion reason are rejected, not "no findings".

---

## Brand Proof — 8 Fields

When any brand-touching content (LP / ad / UI copy / email / SNS / sales / press) is generated, the following 8 evidence fields are required.

| Field | What | Owner Skill | Blocking Layer |
|-------|------|-------------|----------------|
| `tone_proof` | Matches Brand Voice & Tone guide | `prose` | B.tone (advisory) |
| `message_proof` | Value proposition aligns with Positioning | `vision` / `crest` | B.tone (advisory) |
| `distinctiveness_proof` | Embedding distance from competitor recent creatives + own past 90d > G12 threshold | `compete` | B.hard (G12 blocking) |
| `asset_proof` | Distinctive assets (logo, color, type, shape) used per Constitution | `muse` / `vision` | B.pattern (blocking) |
| `memory_proof` | Cognitive associations match intended Category Entry Points | `vision` / `crest` | B.tone (advisory) |
| `trust_proof` | No exaggeration / no false claims / no banned coercive language (per `clause` + `oath`) | `clause` / `oath` | B.hard (blocking) |
| `consistency_proof` | Does not contradict prior brand statements (G15 lifecycle check) | `vision` / `tome` | B.tone (advisory) |
| `brand_lift_proof` | Post-launch awareness / recall / favorability / intent unchanged-or-improved | `pulse` / `experiment` | Post-launch measurement (G13 auto-halt if degraded) |

---

## Market Proof — 9 Fields

When any campaign / ad / channel-allocation decision is made, the following 9 evidence fields are required.

| Field | What | Owner Skill | Blocking Layer |
|-------|------|-------------|----------------|
| `target_proof` | Audience segment defined and addressable in chosen channel | `accord` / `spark` | Ship-time (blocking) |
| `offer_proof` | Value proposition tested or evidenced by Insight Ledger | `spark` / `insight` | Ship-time (blocking) |
| `channel_proof` | Channel-fit rationale based on user behavior data | `funnel` / `compete` | Ship-time (blocking) |
| `funnel_proof` | Funnel stage targeted (awareness / consideration / conversion / retention) named explicitly | `funnel` / `pulse` | Ship-time (blocking) |
| `incrementality_proof` | Measurement method declared per Decision Tree (CL / GeoLift / MMM / Synth); statistical-power-adequate | `experiment` | Post-launch (G13 blocking) |
| `cac_ltv_proof` | Expected CAC < threshold AND LTV / CAC > 3 (or org-specific threshold) | `ledger` (FinOps) / `pulse` | Ship-time (blocking) |
| `cannibalization_proof` | Existing-campaign cannibalization estimated (not just incremental) | `compete` / `experiment` | Post-launch (advisory) |
| `brand_safety_proof` | Brand-safety risk reviewed; placement / context exclusions configured | `clause` / `cloak` / `vigil` | Ship-time (B.hard blocking) |
| `learning_proof` | What we learn if this fails — pre-registered hypothesis | `tome` / `spark` | Post-launch (mandatory) |

**Note**: `incrementality_proof` measurement method follows the Decision Tree below — Privacy regulation aware.

---

## Insight Ledger — Structure and Discipline

The Insight Ledger is the single source of truth for customer insights AI must cite when generating content (Step 2).

### Data Schema (per Logos L-3 + omen FM-F1 mitigation)

```yaml
insight_id: <uuid>
category: market_insight | product_decision | friction | metric_definition  # v7 fold-in: product_decision absorbs "Assumption Ledger" intent (Round 7); v8 fold-in: metric_definition absorbs "Data Reality / Semantic Metrics Layer" intent (Round 8) — anchors pulse.semantic_metric_schema to existing ledger without creating a parallel Metrics Ledger; bot/dupe/exclusion fields per pulse contract
claim: "<one-sentence customer truth>"
evidence_refs:
  - source: <interview / replay / survey / support-ticket / etc>
    n: <sample size>
    date: <YYYY-MM-DD>
    detail: <pointer to raw data>
counter_evidence_refs:
  - source: <...>
    n: <...>
    date: <...>
    detail: "<contradicting observation>"
confidence:
  value: <0-100, deterministic-computed only>
  method: <bayesian-update | weighted-average | etc>
  formula_version: <semver>
valid_from: <YYYY-MM-DD>
valid_until: <YYYY-MM-DD>  # auto-expires
expiration_trigger:
  - calendar: <YYYY-MM-DD>
  - event: <e.g. "competitor X launches Y">
  - count: <N new contradicting observations triggers re-eval>
provenance:
  authored_by: <human-name | ai-proposal>
  attestation: <pending | verified-by-<human> | disputed>
  merged_at: <YYYY-MM-DD>
  merged_by: <research-lead-name>
segment: [<segment-id>, ...]  # which customer cohorts this applies to
contradicts: [<other-insight-id>, ...]  # known incompatibility
decision_refs: [<decision-id>, ...]  # which past decisions cited this
```

### Editorial Rules (G11 mandatory)

1. **AI cannot mutate** — only propose edits to a queue
2. **Research Lead merges** — single human role with merge authority
3. **2-person sign-off required for claim deletion** — counter_evidence can be added by anyone (append-only)
4. **AI-generated proposals carry `provenance: ai-proposal, attestation: pending`** — cannot be cited until human verification
5. **AI-proposal acceptance rate must be < 80%** — higher rate signals rubber-stamping; trigger Research Lead audit
6. **AI cannot cite AI-generated insights for AI-generated content** — circular reference detection in CI

### Survivor Bias Mitigation (omen FM-F5)

Mandatory categories (per G15 monthly minimum N):
- **Customer insights** (people who bought): minimum N per quarter
- **Lost-customer insights** (people who tried and didn't buy): minimum N per quarter
- **Non-customer insights** (target segment who hasn't tried): minimum N per quarter

Failure to meet category minimum auto-flags the segment as "insufficient evidence" — content for that segment cannot pass Research Proof.

### Stale Insight Handling

- `valid_until` reached → `status: stale` auto-applied
- Stale insights cannot be cited in new content (Gate blocks)
- Stale insight referenced by active content → escalation: refresh or remove citation
- Quarterly Ledger Health Audit reports stale-ratio, AI-proposal acceptance rate, category minimums

---

## Friction Ledger — Insight Ledger Child Ledger (v4 minimum adoption)

Friction Ledger is **not a new protocol file**. It is an **independent child ledger of Insight Ledger** that captures UI-operation-grained friction signals at second-level granularity. Per Magi v4 C4 + Omen v4 Top-10 recommendation: physical separation is required because update cadence differs (Insight Ledger = weekly/monthly, Friction Ledger = real-time/seconds), but logical lineage is preserved (Friction Ledger entries can be promoted to Insight Ledger claims after pattern accumulation).

### Why a child ledger, not a new top-level Ledger

The original proposal (Persona+Journey+Product, v4 source) treated Friction Ledger as standalone. Magi/Omen v4 review rejected that for two reasons:
1. **Contract/Ledger proliferation** triggers Authoring Principles checklist failure (`PROOF_CARRYING.md` Proposal Intake Checklist § Item 3 Novelty Ratio)
2. **G11 KB Write Authority Separation** can be inherited from Insight Ledger rather than re-declared

### Schema

```yaml
friction_id: <uuid>
parent_insight_id: <uuid | null>  # link to Insight Ledger if promoted
persona_ref: <persona-id from echo Persona Contract>
surface:
  screen_id: <screen identifier>
  component_id: <component identifier within screen>
  operation: <click | tap | scroll | input | wait | navigate>
observation:
  duration_seconds: <numeric, time spent before action>
  text_misread: <quoted text that caused confusion>
  error_signature: <normalized error class if error encountered>
  anxiety_signal: <hesitation | backtrack | help-open | abandon>
  affected_metric: <CTR | conversion | retention | NPS | etc>
  metric_delta: <observed change>
captured_at: <ISO 8601>
captured_by:
  role: <trace | voice | echo>  # G11 — only these 3 can write
  agent_session: <session identifier>
  evidence_ref: <pointer to session replay / sentiment record / persona walkthrough log>
status: <active | promoted-to-insight | resolved | stale>
expiration:
  valid_until: <ISO 8601>  # default: 1 quarter from captured_at
  promotion_trigger: <N similar entries → propose Insight Ledger claim>
```

### G11 KB Write Authority Separation Application

Friction Ledger inherits G11 unchanged:
- **Write authority limited to 3 skills**: `trace` (session replay extraction), `voice` (sentiment-source pointers), `echo` (persona walkthrough observations)
- **AI cannot directly mutate** Friction Ledger entries; the 3 writer skills queue proposed entries, only their respective human leads (UX Field / Product Field / CX Lead) merge
- **Promotion to Insight Ledger requires Research Lead human merge** (Insight Ledger G11 enforcement)
- **Deterministic-computed fields**: `duration_seconds`, `metric_delta`, `valid_until` are auto-derived (never hand-set per G11 confidence rule)

### Promotion Path to Insight Ledger

```
Friction Ledger entry × N (similar pattern)
  ↓ promotion_trigger fires
Pattern Aggregator (field / tome)
  ↓ generates draft Insight Ledger claim
Research Lead human merge (G11 enforced)
  ↓ approved
Insight Ledger entry created with evidence_refs[] = [friction_id × N]
```

This preserves the audit chain: every Insight Ledger claim derived from friction can be traced back to raw observation entries.

### Survivor Bias Mitigation (carried over from Insight Ledger)

Friction Ledger MUST track minimum N per persona category (per Insight Ledger Survivor Bias rule):
- Customer (current users) friction
- Lost-customer (churned within 90d) friction
- Non-customer (abandoned signup / failed activation) friction

Failure to meet category minimum auto-flags the persona segment as "insufficient friction evidence" — content/UI changes for that segment cannot pass Phase 0 Research Proof.

### When to Use Friction Ledger vs Insight Ledger Directly

| Signal type | Target Ledger | Rationale |
|-------------|--------------|-----------|
| Single observation, second-scale, persona-specific UI moment | **Friction Ledger** | Raw signal; not yet a generalizable claim |
| Pattern from N observations (N ≥ 5) generalizing to a customer truth | **Insight Ledger** (promoted from Friction) | Generalized claim with multi-source evidence |
| Customer interview quote | **Insight Ledger** | Already a synthesized signal, not UI-operation granularity |
| Session replay annotation | **Friction Ledger** | UI-operation granularity |
| Sentiment aggregation across channels | **Insight Ledger** | Cross-channel synthesis level |

### Adoption Tier

- **Solo**: skip Friction Ledger entirely (no UX research staff)
- **SMB**: optional, only if Step 1 Measurement Loop is operational
- **Enterprise**: recommended at Step 2+ adoption (when Insight Ledger is operational)

### Anti-Patterns Specific to Friction Ledger

| Anti-Pattern | Counter-Rule |
|--------------|--------------|
| Treating Friction Ledger entries as Insight Ledger claims without promotion | Promotion requires pattern of N ≥ 5 entries + Research Lead merge |
| AI agents writing directly to Friction Ledger (bypassing 3 writer skills) | G11 enforcement — only trace/voice/echo can write |
| Indefinite retention without expiration | `valid_until` mandatory; default 1 quarter; stale entries auto-flagged |
| Customer-only friction data (omitting lost-customer / non-customer) | Survivor Bias mitigation — mandatory 3 category minimums |
| Manual hand-setting of `duration_seconds` or `metric_delta` | G11 deterministic-only — must be auto-derived from telemetry |

---

## Incrementality Gate — Measurement Method Decision Tree

`incrementality_proof` (Market Proof field) must declare its measurement method. The choice depends on Org Tier, budget, jurisdiction, and event type.

| Method | Privacy-resilient | Min Budget | Min Wait | Cross-device | Best For |
|--------|:----------------:|------------|----------|:------------:|----------|
| **Conversion Lift (Meta/Google)** | × | $30K+ | 2-4 weeks | △ | Large B2C, single platform |
| **GeoLift (Geo-experiment)** | ✅ | $5K+ | 4-8 weeks | ✅ | Geo-divisible business, regional rollouts |
| **Synthetic Control (Causal Impact)** | ✅ | $1K+ | 4-12 weeks | ✅ | Treatment of single market vs control markets |
| **MMM (Robyn / Meridian / Recast)** | ✅ | $5K+ historical | 8-12 weeks setup, weekly updates | ✅ | Cross-channel allocation, long-term |
| **Clean Room (Meta AA / GADH)** | △ (privacy-via-aggregation) | $10K+ | 2-4 weeks | △ | Multi-platform attribution |
| **Holdout (user-level)** | × (Privacy-affected) | $1K+ | 2-4 weeks | × | Small-scale, logged-in users only |

### Decision Rules

1. **Regulated industry** (medical / financial / political / pharmaceutical) → auto-scale OFF by G14; manual approval required; only `Brand Lift` advisory permitted
2. **iOS-heavy audience** (>40% iOS user base) → user-level holdout invalid; mandatory GeoLift or MMM
3. **Cross-device journey** (e.g., search-on-mobile → purchase-on-desktop) → user-level holdout invalid; GeoLift / Synth / MMM only
4. **Budget < $5K** → Conversion Lift insufficient power; use Synthetic Control or stop
5. **Time-sensitive** (decision needed < 2 weeks) → only Conversion Lift or Holdout; MMM/GeoLift too slow
6. **Multi-channel allocation** → MMM required; single-channel methods insufficient

### Statistical Power Requirements

Before ship: compute MDE (Minimum Detectable Effect). If observed effect range < MDE × 0.5, the test cannot reach significance — increase N or change method. **Reject auto-scale on power-inadequate experiments**.

---

## Brand Compiler — 3-Layer Architecture

Per magi C11 + Logos L-4, Brand Compiler operates in 3 distinct layers with different blocking semantics:

### B.hard — Deterministic Hard Blocks

Rule-based, deterministic, blocking. No LLM judgment.

| Rule Type | Example | Tooling |
|-----------|---------|---------|
| Taboo words | "革命的" / 過剰使用、競合商標誤用 | Banned-word list (per `prose`) |
| Legal compliance | 薬機法 / 景表法 / 金商法 / 公職選挙法 / GDPR / DMA violations | `clause` + `oath` validators |
| Distinctive asset misuse | Competitor logo / unauthorized celebrity / wrong brand color | `muse` + `vision` AST check |
| Diversity Floor (G12) | Cosine sim > 0.85 to past 90d own creatives OR top-10 competitor recent creatives | Embedding model + threshold |

B.hard is the same architectural layer as Tier B G9 (4-layer detection): deterministic, fast, no LLM in the path. Failure → CI block.

### B.pattern — Deterministic Pattern Compliance

Token / structure / format compliance. Deterministic, blocking.

| Rule Type | Example | Tooling |
|-----------|---------|---------|
| Token compliance | All colors / fonts / spacing in token allow-list (carry-over from Tier B `token_proof`) | `muse` |
| Logo placement | Position / size / clearspace per Constitution | `vision` AST check |
| Type ramp | Font size / weight / line-height per Constitution | `muse` |
| Microcopy structure | CTA format / error-message structure / length budget per channel | `prose` |

### B.tone — LLM-as-Judge Advisory

Voice / tone / distinctiveness / brand consistency. LLM judgment, non-blocking, sampling audit.

| Aspect | Method | Frequency |
|--------|--------|-----------|
| Voice/Tone match | LLM-as-judge against Constitution voice guide | Every content |
| Distinctiveness narrative | LLM compares to competitor positioning | Sampled (10% of content) |
| Memory association | LLM evaluates Category Entry Point alignment | Sampled (5% of content) |
| Brand consistency vs prior statements | LLM cross-checks past 12mo statements | Sampled (5% of content) |

B.tone is **advisory only** — failure does not block merge / ship. Instead:
1. Findings recorded as `unspecifiable_advisory` in evidence package
2. Weekly sampling audit aggregates B.tone findings for human Brand Director review
3. Trend of declining B.tone scores triggers Constitution review (G15)

**G7 Unmeasurable-Quality Audit applies**: Tier-S brand-critical content requires human designer/copywriter sign-off (≥10 min recorded) even on B.tone PASS.

---

## Growth-Brand Contract — Tier 0 / 1 / 2 Templates

Per Logos L-5, Contract templates are tier-sized to avoid bureaucratic theater.

### Tier 0 — Light (small experiment < $5K, < 1 week)

4 fields:
1. **Hypothesis** — what do we expect to happen, why
2. **Variant** — concrete change / creative
3. **Success_metric** — single metric, threshold
4. **Stop_condition** — when to halt, who decides (G13 Stop_Accountable required)

### Tier 1 — Medium (campaign, < $50K, < 4 weeks)

7 fields (Tier 0 + 3):
5. **Insight_refs** — Insight Ledger entries supporting the hypothesis (per Step 2 mandatory citation)
6. **Channel** — distribution channel + rationale
7. **Brand_constraint** — relevant Constitution Operational-layer rule citations

### Tier 2 — Major (launch / rebrand / $50K+, 4+ weeks)

11 fields (Tier 1 + 4):
8. **Target_segment** — full segment definition with N estimate
9. **Offer** — full value proposition
10. **Experiment_design** — Incrementality method (per Decision Tree), MDE, expected duration
11. **Learning_objective** — what we learn whether we win or lose; pre-registered

**Mandatory across all tiers**:
- `regulatory_jurisdiction` (per G14)
- `stop_accountable` (per G13)
- `creator_role` (Marketing / PdM / Growth / Brand)

**Contract bypass blocking**: No content without an active Contract can be shipped (G14 + G13 enforcement).

---

## Lifecycle Phase Map

Layer C operates across 4 timing phases, distinct from Tier B's merge-time-only model:

| Phase | When | Gates | Outcome |
|-------|------|-------|---------|
| **Phase 0: Pre-Design** | Before any content creation | Research Proof + Insight Ledger consultation + Contract draft | Block design if Insight evidence is insufficient |
| **Phase 1: Merge-Time** | At PR merge | Code Proof + Design Proof (Tier B) + Brand Proof B.hard/B.pattern | Block merge if Tier B fails (delegates to PROOF_CARRYING.md acceptance recipe) |
| **Phase 2: Ship-Time** | Before deploy/launch | Market Proof setup + Brand Proof B.tone advisory + G14 regulatory check | Block ship if measurement design invalid OR regulatory check fails |
| **Phase 3: Post-Launch** | +14d / +30d / +90d after ship | Incrementality measurement + Brand Lift + CAC-LTV + Cannibalization check (G13 auto-halt eligible) | Auto-scale on win / Auto-halt on loss / Brand erosion → emergency review |

**Phase 3 is the v3 innovation** — Tier A/B have no post-launch loop. Without Phase 3, "ship and forget" failures accumulate.

---

## Cross-cutting Application of G11 / G14 / G15 in Layer C

| Guardrail | Layer C Specific Application |
|-----------|------------------------------|
| **G11 KB Write Authority Separation** | Insight Ledger: AI read-only, Research Lead merge. Brand Constitution: AI cannot edit; only 2-person human sign-off. Confidence scores are deterministic-computed, never AI-set. |
| **G14 Regulatory Envelope Pre-Flight** | Every Contract declares `regulatory_jurisdiction`. Medical / financial / political / pharmaceutical default: auto-scale OFF, B.tone LLM-judge disabled (only deterministic B.hard/B.pattern). Quarterly Horizon Scan tracks regulatory changes. |
| **G15 Constitution Lifecycle Discipline** | Brand Constitution split: Core (10y mission) / Strategic (3-5y positioning) / Operational (12-18mo tone rules, banned words). Operational auto-expires; Compiler refuses new content if Operational is stale. Emergency Override: 48h fast-path, normal-Gate follow-up within 7 days. |

---

## Layer C Specific Guardrails (G12 / G13)

These are unique to Layer C (not cross-cutting). Documented here, not in PROOF_CARRYING.md.

### G12. Diversity & Distinctiveness Floor

**Problem**: Lift-maximization drives all creatives toward known-effective short-term psychological triggers (FOMO, scarcity, authority). Industry-wide convergence; long-term brand differentiation collapses (omen FM-E4 RPN=720, FM-G1 RPN=648).

**Rule**:
1. **Distinctiveness Score** per creative = mean embedding distance from (own past 90d creatives ∪ top-10 competitor recent creatives)
2. **Reject any creative with Distinctiveness < threshold** even if predicted-lift is high (Compiler B.hard layer)
3. **Boldness Floor (B.tone advisory)** — copy too-bland (lexical entropy below baseline -1σ) flagged as "minimum viable safe"
4. **Monthly "Brand Voice Distinctiveness Index"** — published; baseline -1σ triggers Compiler threshold tightening
5. **Annual "intentional outlier budget"** — 5-10% of spend reserved for low-lift / high-distinctiveness experiments

**Anti-pattern**: "Trust humans to add variety" — humans inherit Compiler's risk aversion via incentives.

### G13. Stop Authority Pre-Designation

**Problem**: Stop triggers fire but no single accountable individual exists to act. Growth and Brand teams each assume the other will halt. 48-72h pass; brand erosion accumulates (omen FM-H3 RPN=648, FM-E5 RPN=504).

**Rule**:
1. **Every Contract names Stop_Accountable (1 person)** — Contract creation blocked if unfilled
2. **Stop trigger fires → notify Stop_Accountable immediately** — 24h no-response → auto-halt (default deny)
3. **Brand Director has unilateral veto on Brand-related stop** — Growth Lead cannot override
4. **Workload cap** — Stop_Accountable cannot own > N concurrent active Contracts (avoid bottleneck)
5. **Chaos drill quarterly** — simulate stop trigger, verify auto-halt mechanism end-to-end

**Anti-pattern**: "Committee-based stop decision" — historically slowest at exactly the wrong moment.

---

## Inherent Residual Risks (cannot be fully designed away)

Per omen FM-G4 / FM-H1 / FM-X3, three failure modes are **structural** — guardrails reduce but cannot eliminate. These require organizational culture commitment, not technical control:

| Residual | Nature | Organizational Response Required |
|----------|--------|----------------------------------|
| **Compiler Bypass via CEO Twitter / executive statements / sales verbal** | Top-down content cannot be CI-gated | Executive personal commitment to Compiler review; sales training; PR/IR brand checklists |
| **Skunkworks bypass** ("emergency test" via personal accounts) | Regulation-strict regimes invite shadow channels | Monthly "tell us what you bypassed" amnesty + post-hoc Contract creation; root-cause analysis when bypass repeats |
| **Emergency Override commonality** | Initial design = "quarterly 1-2 events" → actual = monthly 5-10 | Quarterly override audit; >5 in a quarter triggers process review; override decay (each use raises next override's bar) |

These are explicitly **out of scope for Tier C technical guardrails**. They are Magi-arbitrated organizational issues.

---

## Cost & Scale Profile

| Org Tier | Step | Typical Wall-Time (per change) | Cost vs v2 baseline |
|----------|------|---------------------------|---------------------|
| Solo | None | n/a | 1× (v2 only) |
| SMB | Step 1 only | +15-30 min (post-launch measurement loop) | 1.1-1.3× |
| Enterprise | Step 1+2 | +1-3 days (Research Proof + Ledger consultation) | 2-3× |
| Enterprise | Step 1+2+3 | +1-2 weeks (full Market Proof + Incrementality setup) | 3-5× |
| Enterprise | Step 1+2+3+4 (full Layer C) | +2-4 weeks (Brand Compiler integration) | 5-8× |

**Step adoption ordering is mandatory** — skipping Steps risks adopting blocking gates without supporting infrastructure.

---

## Anti-Patterns Specific to Layer C

| Anti-Pattern | Why It Fails | Counter-Rule |
|--------------|--------------|--------------|
| Adopting full Layer C in Solo org | No staff to operate; gates become formal theater | Org Tier policy; Solo skips entire file |
| Skipping Step 1 → directly to Step 4 | Brand Compiler blocks merges; no Insight evidence; no Measurement Loop to learn from blocks | Phased Adoption mandatory ordering |
| AI write authority on Insight Ledger | Confirmation bias accrues (omen FM-F1) | G11 — AI read-only, human merge |
| Lift-maximization without Distinctiveness Floor | Homogenization (omen FM-E4) | G12 — Distinctiveness Floor + Boldness Floor |
| Stop Owner unspecified in Contract | 48-72h delay, brand erosion (omen FM-H3) | G13 — Stop_Accountable mandatory field, 24h auto-halt |
| Auto-scale enabled in regulated industries | 薬機 / 景表 / 金商法 violations | G14 — per-jurisdiction toggle, regulated default OFF |
| Constitution edits by single editor without lifecycle | Mummification (omen FM-G2) | G15 — Core/Strategic/Operational layers, 2-person sign-off |
| Confidence score hand-set by AI | Goodhart (omen FM-F2) | G11 — deterministic-computed, never hand-set |
| Customer-only Insights (no lost / non-customer) | Survivor bias (omen FM-F5) | Insight Ledger mandatory 3 categories with minimum N |
| "Approve all" on diff floods | Same anti-pattern as Tier B G5 | G5 carry-over from Tier B |
| Compiler PASS celebrated as "brand approved" | False confidence (omen FM-G1 / G7) | G7 Unmeasurable-Quality Audit + "rule coverage verified" wording only |
| Bypass via CEO Twitter / sales verbal | Structural — guardrails cannot block | Executive culture commitment (Magi-arbitrated, not technical) |
| Indefinite Operational Constitution without refresh | Mummification | G15 — Compiler refuses new content when Operational is stale (forcing function) |

---

## References

- `_common/PROOF_CARRYING.md` v3 — Tier A Foundation + Tier B Production Pipeline + cross-cutting G11/G14/G15
- `nexus/reference/growth-acceptance-recipe.md` — chain template orchestrating Layer C across Phase 0-3
- AAOS (v1) / Code+Design Proof (v2) / Growth+Brand Acceptance OS (v3 source) — design lineage
- Magi verdict on v3 source: 3-0 GO-WITH-HEAVY-CONDITIONS, weighted confidence 54.7, 12 conditions (C1-C12), Phased Adoption mandatory, Org Tier mandatory
- Omen pre-mortem on v3 source: 25 new failure modes, 7 S≥9 Critical, 5 new guardrails proposed (G11-G15; G11/G14/G15 cross-cutting, G12/G13 Layer C specific)
- Ehrenberg-Bass Institute — Distinctive Brand Assets / Mental Availability theory (G12 conceptual basis)
- Meta Conversion Lift / Google Brand Lift / GeoLift / Causal Impact / Robyn / Meridian — Incrementality measurement method abstraction
- AWS S3 parallel-run / DO-178C N-version programming — Tier B Dual-Implementation precedent (carry-over)
