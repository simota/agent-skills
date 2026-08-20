# Growth-Acceptance Blueprint — the `layer=c` preset of `acceptance`

> `/nexus growth-acceptance` ≡ **`/nexus acceptance layer=c`** — the lifecycle-layer preset of the acceptance merge-adjudication engine. `growth-acceptance` is a **named alias kept for discoverability**; merge-time adjudication (Phases 0-6, Layer A/B, G1-G10, joint verdict) is owned by `reference/acceptance-recipe.md` and is **not** re-derived here — Phase 1 below delegates to it wholly at Tier B. This file owns only what the layer adds: the pre-design insight contract, ship-time market/brand/regulatory setup, the post-launch measurement loop with auto-halt, and G11-G15.

Recipe contract for `nexus growth-acceptance` — orchestrates the **lifecycle gates** (pre-design → ship-time → post-launch) defined by `_common/GROWTH_BRAND_PROOF.md` (Layer C: Market + Research + Brand axes). Use when an Enterprise-tier organization wants AI-generated content / campaigns / brand-touching artifacts to be machine-adjudicated across their entire lifecycle, not only at merge.

**Prerequisites**:
- `_common/PROOF_CARRYING.md` v3 (mandatory — Tier A Foundation + Tier B Production Pipeline + cross-cutting G11/G14/G15)
- `_common/GROWTH_BRAND_PROOF.md` (mandatory — Layer C protocol)
- `nexus/reference/acceptance-recipe.md` (Phase 1 delegates here for merge-time gates)

**Distinguishes from / integrates with**:
- `acceptance` — Code + Design merge-time gate (Tier B); `growth-acceptance` includes it as Phase 1 (full delegation, shared v3 protocol foundation) and extends to pre-design (Phase 0) + ship-time (Phase 2) + post-launch (Phase 3).
- Every other distinction `acceptance` draws (`feature`, `apex`, `summit`, `judge`) applies here unchanged — see `reference/acceptance-recipe.md` § Distinguishes from. The Layer-C-specific chaining on top: `apex` authors → growth-acceptance gates the lifecycle; `summit` decides → growth-acceptance gates execution; `kaizen` produces → growth-acceptance gates brand-touching surfaces; and `feature` is the recommended downgrade when Phase 0 detects Solo / SMB or sub-Step-2 adoption.

---

## When to Invoke

Trigger `nexus growth-acceptance` when **all** apply:
- Org Tier is Enterprise (50+ people with Research / Brand / Growth-analytics specialists)
- Step 2+ of Phased Adoption is in place (Insight Ledger operational + Research Lead role staffed)
- The change is brand-touching content / campaign / customer-facing message (not internal infra / pure backend / dev tooling)
- The organization has committed to lifecycle-gating (this is a workflow choice, not a tactic)

Do **not** invoke when:
- Org Tier is Solo / SMB → use `acceptance` (Tier B) only; Step 1 Measurement Loop optional opt-in
- Pure backend / infrastructure / data pipeline change → use `acceptance` Tier B
- Regulated industry where Layer C autonomy is legally restricted → use `acceptance` Tier B + manual Layer C review per G14
- User wants exploration / brainstorming, not lifecycle gating → use `flux` / `magi` / `omen`
- Layer C Step adoption is below Step 3 → use `acceptance` Tier B + manual Market / Brand review

---

## Phase Contract

### Phase 0 — Pre-Design (Research + Insight + Contract Draft)

**Goal**: No content authoring begins until evidence + Contract are in place.

**Agents** (sequential):

1. **Nexus[classify]** — internal: detect `org_tier`, `step_adoption_level`, `change_category` (content / campaign / brand-touch), `regulatory_jurisdiction`, `tier` (S/A/B/C), `ui_dimension` (none / partial / full)
2. **`insight` (proposed skill) or `field`** — query Insight Ledger for relevant evidence; if no evidence available for the proposed segment, REJECT (block design)
3. **`field`** — if Step 2+ and evidence is stale or missing, queue fresh research
4. **`scribe[unified]` + `spark`** — draft Growth-Brand Contract (Tier 0 / 1 / 2 per scope)
5. **`magi` (optional)** — high-stakes content: arbitrate Strategic-level Constitution alignment

**Gate (G11 mandatory)**:
- Insight Ledger consultation is mandatory; thinking-aloud claims are rejected
- Contract Tier 1+ requires `insight_refs` field with valid Ledger IDs
- AI cannot write to Insight Ledger (read-only); proposed-edit queue must clear before design begins

**Engine routing**: Field / Voice / Trace on Codex for data extraction; Insight Lead synthesis on Claude (judgment); Echo[demand] on Claude for customer empathy.

**Output**: Approved Contract + Insight Ledger citation set + Constitution Operational-layer rule citations.

### Phase 1 — Merge-Time (delegates to acceptance recipe Tier B)

**Goal**: Code + Design merge-time gates per existing `acceptance` recipe.

**Delegation**: This phase **fully and wholly** delegates to `nexus acceptance` recipe (`nexus/reference/acceptance-recipe.md`) — its complete Phase 1-6 chain (Spec Diff → Layer A/B Oracle Generation → Layer A/B Adversarial Exploration → Layer A/B/Joint Acceptance Gate → Runtime Oracle Hookup) runs unmodified; growth-acceptance never re-implements or re-derives any part of that adjudication (see `reference/acceptance-recipe.md` § Phase Contract for the full agent-level detail).

**Tier C extensions during Phase 1**:
- Brand Compiler **B.hard layer** runs during Phase 4B alongside Design Compiler — blocks taboo words / legal compliance / Distinctiveness Floor violations
- Brand Compiler **B.pattern layer** runs during Phase 4B — blocks token / structure / format compliance failures

**Gate**: Per acceptance recipe Phase 4C joint verdict. Layer C extensions block merge if B.hard or B.pattern FAIL.

### Phase 2 — Ship-Time (Market Setup + Brand Advisory + Regulatory Check)

**Goal**: Before deploy / launch, verify measurement design + brand advisory + regulatory compliance.

**Agents** (parallel):

1. **`pulse` + `experiment`** — Market Proof: declare `incrementality_proof` measurement method per Decision Tree (Conversion Lift / GeoLift / MMM / Synth); compute statistical power
2. **`ledger` (FinOps)** — CAC / LTV thresholds; budget allocation
3. **`compete`** — cannibalization estimation
4. **`funnel` + `funnel[premium]`** — channel-fit rationale and LP coherence
5. **`vision` + `prose`** — Brand Compiler **B.tone advisory** layer (LLM-as-judge, non-blocking)
6. **`canon[legal]` + `canon[regulatory]` + `cloak` + `vigil`** — G14 Regulatory Envelope Pre-Flight: verify `regulatory_jurisdiction` toggles, brand-safety placement exclusions

**Gate (G14 mandatory)**:
- Regulatory jurisdiction declared; per-jurisdiction toggle (auto-scale / auto-generate / holdout test) verified
- Regulated industries (medical / financial / political / pharmaceutical): auto-scale OFF default, manual approval required
- Statistical power adequate for declared measurement method (MDE check)
- B.tone advisory findings recorded as `unspecifiable_advisory` (non-blocking)

**Pre-Registration sub-gate (the integrity backbone — freeze the plan before the data exists):**

A measurement-backed launch is only honest if the success bar is set **before** the outcome is known; otherwise the +14/+30/+90d gates can be gamed by post-hoc metric selection (HARKing / p-hacking). Before ship, lock an **immutable analysis plan**:
- **Primary metric** (single, pre-declared — the incrementality outcome that decides scale/halt), MDE, decision thresholds (auto-scale / auto-halt cut-offs), analysis window, and the **decision rule itself** (what value triggers scale vs halt). Secondary metrics are explicitly labelled secondary and cannot promote to primary post-launch.
- The plan is **frozen and hash-stamped** into the Contract before ship. Phase 3 evaluates against this frozen plan only.
- **Control-validity check** — `experiment` verifies the incrementality counterfactual is sound BEFORE launch: holdout/geo-control assignment is valid, **SRM (sample-ratio-mismatch) clean**, and test/control contamination bounded. A broken control invalidates the incrementality claim no matter what lift is observed — block ship until the control is sound.

**Output**: Ship-eligible artifact with full Market Proof setup + **frozen pre-registered analysis plan (hash-stamped)** + validated control + Brand Advisory record + Regulatory clearance.

### Phase 3 — Post-Launch (Measurement Loop + Auto-Halt + Learning)

**Goal**: Continuous measurement after launch; auto-scale on win, auto-halt on loss, brand erosion → emergency review.

**Schedule** (scheduled gates, not merge-time):
- **+14 days** — initial lift check (early-signal)
- **+30 days** — incrementality confirmed; CAC / LTV trend; cannibalization check
- **+90 days** — Brand Lift / brand search query trend / Distinctive Asset audit; full Learning record

**Agents** (per scheduled gate):

1. **`pulse` + `experiment`** — collect post-launch metrics per Incrementality method
2. **`compete`** — cannibalization analysis (cross-campaign impact)
3. **`ledger`** — CAC / LTV trend update
4. **`beacon`** — Brand Lift monitoring (if Brand Lift Proof was set up)
5. **`mend`** — if Stop_Condition triggered: G13 auto-halt sequence
6. **`launch[weekly]`** — aggregate findings into Learning record
7. **`tome`** — update Insight Ledger with validated findings (queue for Research Lead merge per G11)

**Gate (G13 mandatory)**:
- **Evaluate against the frozen pre-registered plan only** — read the primary metric, MDE, and thresholds from the Phase 2 Pre-Registration sub-gate's hash-stamped plan; they are not re-chosen now. Any proposed post-launch change to metric/threshold/window is a **flagged deviation** requiring explicit Stop_Accountable + Research Lead sign-off (recorded with reason) — never a silent re-baseline.
- Stop_Condition trigger fires → Stop_Accountable notified immediately
- 24h no-response → auto-halt (default deny)
- Brand Director has unilateral veto on Brand-related stops (Growth Lead cannot override)
- Auto-scale eligibility requires: positive incrementality **on the pre-registered primary metric with a valid control (SRM clean)** + Brand Lift not degraded + CAC < threshold + no cannibalization > X%

**Output**: Per-checkpoint Learning record + Auto-scale decision (or Auto-halt + post-mortem) + Insight Ledger proposed-edit queue entry.

### Phase 4 — Continuous Cross-Cutting Audits (background, not per-change)

These run on schedule, not per-change, but affect every Layer C operation. Audit content and mechanics are defined in `_common/GROWTH_BRAND_PROOF.md` (§ Cross-cutting Application of G11/G14/G15 and the Ledger/Constitution audit sections); cadence below is this recipe's own schedule:

- **Quarterly Constitution Health Audit (G15)**
- **Quarterly Goodhart Audit (G6 carry-over from Tier B)**
- **Quarterly Regulatory Horizon Scan (G14)**
- **Quarterly Distinctive Asset Audit (G12)** — Brand Voice Distinctiveness Index; competitor Colour Stealing detection
- **Monthly Insight Ledger Audit (G11)**
- **Monthly Override Audit (G14 + G15 + Hot-Fix Fast-Path)**
- **Weekly B.tone Sampling Audit (G7 carry-over)**

---

## Chain Template (AUTORUN)

```
Phase 0 (Pre-Design, sequential):
  Nexus[classify org_tier + step_adoption + change_category + regulatory_jurisdiction + tier + ui_dimension]
  → if org_tier=Solo: abort with `acceptance` recommendation
  → if org_tier=SMB AND step_adoption < 2: abort with `acceptance` + Step 1 Measurement Loop recommendation
  → insight[query Ledger for evidence] (read-only per G11)
  → if evidence stale/missing AND Step ≥ 2: field[queue fresh research, block design]
  → scribe[unified] + spark[draft Growth-Brand Contract Tier 0/1/2]
  → if change_category=brand_critical: magi[Constitution alignment]

Phase 1 (Merge-Time, delegates to acceptance recipe):
  nexus acceptance (full chain with Tier B Layer A + Layer B + B.hard/B.pattern extensions)

Phase 2 (Ship-Time, parallel):
  ‖ pulse + experiment[Market Proof setup + Incrementality Decision Tree]
  ‖ ledger[CAC/LTV thresholds]
  ‖ compete[cannibalization estimation]
  ‖ funnel + funnel[premium: channel-fit + LP coherence]
  ‖ vision + prose[B.tone advisory, non-blocking]
  ‖ canon[legal] + canon[regulatory] + cloak + vigil[G14 Regulatory Pre-Flight]
  ‖ experiment[pre-register + control-validity/SRM check, per § Pre-Registration sub-gate]
  → Gate: regulatory toggle verified + statistical power adequate + analysis plan frozen + control valid
  → if FAIL: block ship; route to remediation

Phase 3 (Post-Launch, scheduled):
  +14d:
    ‖ pulse + experiment[initial lift]
    ‖ beacon[early Brand Lift]
  +30d:
    ‖ experiment[incrementality confirmed]
    ‖ ledger[CAC/LTV trend]
    ‖ compete[cannibalization]
  +90d:
    ‖ beacon[Brand Lift]
    ‖ compete[Distinctive Asset audit]
    ‖ launch[Learning record]
    ‖ tome[Insight Ledger proposed-edit queue]
  Per-checkpoint Gate (G13) — evaluated against the frozen plan; rules in § Phase 3:
    Stop_Condition fires → notify Stop_Accountable → 24h no-response → mend[auto-halt]

Phase 4 (Cross-Cutting Audits, background):
  Quarterly: G15 Constitution Health / G6 Goodhart / G14 Horizon Scan / G12 Distinctive Asset
  Monthly: G11 Insight Ledger / Override Audit
  Weekly: B.tone Sampling
```

---

## Failure Escalation

| Failure | Trigger | Escalation |
|---------|---------|------------|
| Org Tier Solo invoking growth-acceptance | Phase 0 | Abort; recommend `acceptance` (Tier B only) |
| Step adoption < 2 | Phase 0 | Abort; recommend Step 1 Measurement Loop first |
| Insight Ledger missing evidence for segment | Phase 0 | Block design; queue field; resume when evidence is in Ledger |
| AI attempted to write to Insight Ledger | Phase 0 | Block; G11 violation; require Research Lead merge |
| Constitution Operational layer stale | Phase 1 B.pattern | Block merge; G15 forcing function; require Constitution refresh |
| Distinctiveness Score < threshold (G12) | Phase 1 B.hard | Block merge; require creative iteration |
| Statistical power inadequate for measurement | Phase 2 | Block ship; require N increase or method change per Decision Tree |
| No frozen pre-registered analysis plan before ship | Phase 2 | Block ship; freeze the plan per the § Pre-Registration sub-gate before launch |
| Control invalid (SRM mismatch / contamination / broken holdout) | Phase 2 | Block ship; incrementality counterfactual unsound — fix assignment before launch |
| Post-launch metric/threshold change without sign-off | Phase 3 | Reject silent re-baseline; flagged deviation requires Stop_Accountable + Research Lead sign-off |
| Auto-scale fired on a secondary metric (not pre-registered primary) | Phase 3 | Block; HARKing/p-hacking guard — decision binds to the frozen primary metric only |
| Regulatory jurisdiction not declared | Phase 2 | Block ship; G14 violation; require Legal sign-off |
| Regulated industry + auto-scale ON | Phase 2 | Block ship; G14 enforcement; manual approval required |
| Stop_Accountable unfilled in Contract | Phase 0 / Phase 2 | Block; G13 enforcement; require Contract owner assignment |
| Stop_Condition triggered, 24h no-response | Phase 3 | Auto-halt; default-deny per G13 |
| Brand Director invokes unilateral veto on Brand-related stop | Phase 3 | Halt; Growth Lead cannot override; veto recorded with reason |
| Auto-scale eligibility partial (incrementality+ but cannibalization > X%) | Phase 3 | Hold; require manual review |

4 further rows (Insight Ledger AI-proposal rubber-stamping, Brand Voice Distinctiveness Index degradation, Emergency Override-count review, Constitution staleness lockout) are the Phase 4 audit-triggered failure modes — detection detail in `_common/GROWTH_BRAND_PROOF.md`; escalation actions are as the pattern above (flag / block / process review).

---

## Cost & Scale Profile

| Org Tier | Step Adoption | Phase 0 wall-time | Phase 1 (delegated) | Phase 2 wall-time | Phase 3 wall-time (cumulative across +14d/+30d/+90d) | Total agents | Cost vs `feature` |
|----------|---------------|-------------------|---------------------|-------------------|------------------------|--------------|-------------------|
| Solo | n/a | — | — | — | — | — | (use acceptance) |
| SMB | Step 1 only | — | per acceptance | — | 3-5 (post-launch only) | + 3-5 | 1.1-1.3× |
| Enterprise | Step 1+2 | 30min-2h | per acceptance | — | 5-8 | + 8-12 | 2-3× |
| Enterprise | Step 1+2+3 | 1-3h | per acceptance | 30min-2h | 8-12 | + 14-20 | 3-5× |
| Enterprise | Step 1+2+3+4 (full) | 2-5h | per acceptance + B.hard/B.pattern | 1-3h (+ B.tone) | 10-15 | + 18-25 | 5-8× |

**Note**: Phase 1 cost varies per acceptance recipe Tier (Tier-S full UI 9-15×, Tier-A full UI 5-8×, etc.). Total cost = Phase 1 cost + Tier C overhead from above.

**Confirm with user before launching Step 3 or Step 4** — costs and organizational requirements rise sharply. **Strongly confirm before Step 4** — Brand Compiler blocking changes the brand-team workflow.

---

## Output Report — **Lifecycle Dossier** (named)

Extends the engine's **Acceptance Dossier** (`reference/acceptance-recipe.md`) rather than replacing it — the merge-time sections come from there unchanged. Layer C adds:

- **Insight Ledger** — each pre-design insight with its evidence and the contract clause it produced
- **Market / Research / Brand axis verdicts** — G11-G15 disposition per `_common/GROWTH_BRAND_PROOF.md`
- **Ship-time setup record** — market, brand-compiler, and regulatory checks with their outcomes
- **Post-launch measurement state** — the metric contract, current readings, auto-halt status, and the next scheduled checkpoint (+14/+30/+90d)
- **Learning entry** — what the launch taught, written back for the next cycle

## Confirm / Safety Gate

Inherits the engine's gates unchanged (`reference/acceptance-recipe.md`) — **Confirm before launch when `tier == S`**, plus standard **Ask First** tiers. Layer C adds one of its own: **Ask First before any ship-time action that touches an external surface** (market listing, brand asset publication, regulatory filing), since those are outward-facing and not reversible by a revert.

## Resume

**Schedule-resume** — Layer C's post-launch phase is a cadence, not a continuous run: state persists between the +14 / +30 / +90d checkpoints and each wake-up resumes from the recorded metric contract and prior readings. Merge-time phases use the engine's checkpoint-resume.

## Failure Modes Prevented

| Anti-Pattern | Counter-Rule |
|--------------|--------------|
| Phase 1 inline orchestration instead of delegating to acceptance | Delegate to acceptance recipe; avoid duplication |
| Phase 2 auto-scale enabled without Decision Tree compliance | Block; require explicit method declaration |
| Picking the winning metric after results are in (HARKing / p-hacking) | Phase 2 Pre-Registration sub-gate; Phase 3 binds to the frozen plan |
| Claiming incrementality on an invalid control (SRM / contaminated holdout) | Phase 2 Pre-Registration control-validity check blocks ship |
| Phase 3 Auto-halt blocked by Growth Lead override | G13 enforcement; Brand Director veto authority preserved |
| Skipping Phase 4 cross-cutting audits | Long-term drift; mandatory schedule |
| Treating Phase 3 as one-shot post-launch check | Phase 3 has 3 scheduled gates (+14/+30/+90); each is mandatory |

4 further anti-patterns (Solo-org adoption, sub-Step-2 adoption, AI write authority on the Insight Ledger, CEO/executive Compiler bypass) are Layer C anti-patterns owned by `_common/GROWTH_BRAND_PROOF.md` § Anti-Patterns Specific to Layer C — not re-derived here.

---

## References

- `_common/PROOF_CARRYING.md` v3 — Tier A Foundation + Tier B Production Pipeline + cross-cutting G11/G14/G15
- `_common/GROWTH_BRAND_PROOF.md` — Layer C protocol (Market + Research + Brand axes), Insight Ledger, Incrementality Gate, Brand Compiler 3-layer, Growth-Brand Contract, Phased Adoption Step 1-4
- `nexus/reference/acceptance-recipe.md` — Phase 1 (merge-time) delegated chain
- `nexus/reference/apex-recipe.md` — discovery → ship cycle; Phase 6 can chain into growth-acceptance
- `nexus/reference/summit-recipe.md` — strategic decisions; can author Layer C content for growth-acceptance gating

Layer C's per-axis skill roster (Research / Brand / Market / Auto-action) is not re-listed here — every skill already appears against its owning phase in § Phase Contract above.
