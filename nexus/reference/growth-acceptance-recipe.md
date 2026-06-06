# Growth-Acceptance Recipe — Layer C Lifecycle Gate

Recipe contract for `nexus growth-acceptance` — orchestrates the **lifecycle gates** (pre-design → ship-time → post-launch) defined by `_common/GROWTH_BRAND_PROOF.md` (Layer C: Market + Research + Brand axes). Use when an Enterprise-tier organization wants AI-generated content / campaigns / brand-touching artifacts to be machine-adjudicated across their entire lifecycle, not only at merge.

**Prerequisites**:
- `_common/PROOF_CARRYING.md` v3 (mandatory — Tier A Foundation + Tier B Production Pipeline + cross-cutting G11/G14/G15)
- `_common/GROWTH_BRAND_PROOF.md` (mandatory — Layer C protocol)
- `nexus/reference/acceptance-recipe.md` (Phase 1 delegates here for merge-time gates)

**Distinguishes from**:
- `feature` — implements a change with conventional tests. No Insight Ledger, no Brand Compiler, no Incrementality Gate.
- `acceptance` — Code + Design merge-time gate (Tier B). `growth-acceptance` includes this as Phase 1 and extends to pre-design (Phase 0) + ship-time (Phase 2) + post-launch (Phase 3).
- `apex` — full discovery → ship cycle. `growth-acceptance` assumes the spec graph + Insight Ledger + Brand Constitution exist; focus is on gating, not authoring.
- `summit` — strategic decisions and high-stakes releases (tri-engine). `growth-acceptance` is the lifecycle gate; `summit` is the upstream judgment.
- `kaizen` — single-axis improvement (perf / UX / code-quality / feature-extension). `growth-acceptance` is multi-axis lifecycle gating.

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
- User wants exploration / brainstorming, not lifecycle gating → use `riff` / `magi` / `omen`
- Layer C Step adoption is below Step 3 → use `acceptance` Tier B + manual Market / Brand review

---

## Phase Contract

### Phase 0 — Pre-Design (Research + Insight + Contract Draft)

**Goal**: No content authoring begins until evidence + Contract are in place.

**Agents** (sequential):

1. **Nexus[classify]** — internal: detect `org_tier`, `step_adoption_level`, `change_category` (content / campaign / brand-touch), `regulatory_jurisdiction`, `tier` (S/A/B/C), `ui_dimension` (none / partial / full)
2. **`insight` (proposed skill) or `field`** — query Insight Ledger for relevant evidence; if no evidence available for the proposed segment, REJECT (block design)
3. **`field`** — if Step 2+ and evidence is stale or missing, queue fresh research
4. **`accord` + `spark`** — draft Growth-Brand Contract (Tier 0 / 1 / 2 per scope)
5. **`magi` (optional)** — high-stakes content: arbitrate Strategic-level Constitution alignment

**Gate (G11 mandatory)**:
- Insight Ledger consultation is mandatory; thinking-aloud claims are rejected
- Contract Tier 1+ requires `insight_refs` field with valid Ledger IDs
- AI cannot write to Insight Ledger (read-only); proposed-edit queue must clear before design begins

**Engine routing**: Field / Voice / Trace on Codex for data extraction; Insight Lead synthesis on Claude (judgment); Plea on Claude for customer empathy.

**Output**: Approved Contract + Insight Ledger citation set + Constitution Operational-layer rule citations.

### Phase 1 — Merge-Time (delegates to acceptance recipe Tier B)

**Goal**: Code + Design merge-time gates per existing `acceptance` recipe.

**Delegation**: This phase fully delegates to `nexus acceptance` recipe (`nexus/reference/acceptance-recipe.md`):
- Phase 1 (Spec Diff) → attest
- Phase 2A (Code Oracles) → radar / mint / matrix (qa-scenario) / sentinel / attest / rally[engine-paradigm COMPETE if applicable]
- Phase 2B (Design Oracles) → atelier sub-orchestration: muse / frame / palette / weave / flow / canon / vitrine / prose / matrix
- Phase 3A (Code Adversaries) → vigil / sentinel / siege (concurrency + chaos)
- Phase 3B (Design Adversaries) → atelier: echo / voyager+vector / matrix (qa-scenario)
- Phase 4A (Code Acceptance Gate) → judge[tri-engine] / attest
- Phase 4B (Design Acceptance Gate) → atelier: canon / frame / vision
- Phase 4C (Joint Verdict) → guardian

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
4. **`funnel` + `bazaar`** — channel-fit rationale and LP coherence
5. **`vision` + `prose`** — Brand Compiler **B.tone advisory** layer (LLM-as-judge, non-blocking)
6. **`clause` + `oath` + `cloak` + `vigil`** — G14 Regulatory Envelope Pre-Flight: verify `regulatory_jurisdiction` toggles, brand-safety placement exclusions

**Gate (G14 mandatory)**:
- Regulatory jurisdiction declared; per-jurisdiction toggle (auto-scale / auto-generate / holdout test) verified
- Regulated industries (medical / financial / political / pharmaceutical): auto-scale OFF default, manual approval required
- Statistical power adequate for declared measurement method (MDE check)
- B.tone advisory findings recorded as `unspecifiable_advisory` (non-blocking)

**Output**: Ship-eligible artifact with full Market Proof setup + Brand Advisory record + Regulatory clearance.

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
6. **`harvest`** — aggregate findings into Learning record
7. **`tome`** — update Insight Ledger with validated findings (queue for Research Lead merge per G11)

**Gate (G13 mandatory)**:
- Stop_Condition trigger fires → Stop_Accountable notified immediately
- 24h no-response → auto-halt (default deny)
- Brand Director has unilateral veto on Brand-related stops (Growth Lead cannot override)
- Auto-scale eligibility requires: positive incrementality + Brand Lift not degraded + CAC < threshold + no cannibalization > X%

**Output**: Per-checkpoint Learning record + Auto-scale decision (or Auto-halt + post-mortem) + Insight Ledger proposed-edit queue entry.

### Phase 4 — Continuous Cross-Cutting Audits (background, not per-change)

These run on schedule, not per-change, but affect every Layer C operation:

- **Quarterly Constitution Health Audit (G15)** — % of Operational entries refreshed in past 6mo; Stale ratio
- **Quarterly Goodhart Audit (G6 carry-over from Tier B)** — coverage metrics vs second-axis indicators
- **Quarterly Regulatory Horizon Scan (G14)** — Legal + DataEng publish upcoming changes
- **Quarterly Distinctive Asset Audit (G12)** — Brand Voice Distinctiveness Index; competitor Colour Stealing detection
- **Monthly Insight Ledger Audit (G11)** — AI-proposal acceptance rate, category minimum N coverage, stale ratio
- **Monthly Override Audit (G14 + G15 + Hot-Fix Fast-Path)** — Emergency Overrides per quarter; > 5 triggers process review
- **Weekly B.tone Sampling Audit (G7 carry-over)** — Brand Director reviews sampled B.tone advisory findings

---

## Chain Template (AUTORUN)

```
Phase 0 (Pre-Design, sequential):
  Nexus[classify org_tier + step_adoption + change_category + regulatory_jurisdiction + tier + ui_dimension]
  → if org_tier=Solo: abort with `acceptance` recommendation
  → if org_tier=SMB AND step_adoption < 2: abort with `acceptance` + Step 1 Measurement Loop recommendation
  → insight[query Ledger for evidence] (read-only per G11)
  → if evidence stale/missing AND Step ≥ 2: field[queue fresh research, block design]
  → accord + spark[draft Growth-Brand Contract Tier 0/1/2]
  → if change_category=brand_critical: magi[Constitution alignment]

Phase 1 (Merge-Time, delegates to acceptance recipe):
  nexus acceptance (full chain with Tier B Layer A + Layer B + B.hard/B.pattern extensions)

Phase 2 (Ship-Time, parallel):
  ‖ pulse + experiment[Market Proof setup + Incrementality Decision Tree]
  ‖ ledger[CAC/LTV thresholds]
  ‖ compete[cannibalization estimation]
  ‖ funnel + bazaar[channel-fit + LP coherence]
  ‖ vision + prose[B.tone advisory, non-blocking]
  ‖ clause + oath + cloak + vigil[G14 Regulatory Pre-Flight]
  → Gate: regulatory toggle verified + statistical power adequate
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
    ‖ harvest[Learning record]
    ‖ tome[Insight Ledger proposed-edit queue]
  Per-checkpoint Gate (G13):
    Stop_Condition trigger fires → notify Stop_Accountable
    24h no-response → mend[auto-halt]
    Auto-scale: incrementality+ AND Brand Lift not degraded AND CAC<threshold AND no cannibalization

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
| Regulatory jurisdiction not declared | Phase 2 | Block ship; G14 violation; require Legal sign-off |
| Regulated industry + auto-scale ON | Phase 2 | Block ship; G14 enforcement; manual approval required |
| Stop_Accountable unfilled in Contract | Phase 0 / Phase 2 | Block; G13 enforcement; require Contract owner assignment |
| Stop_Condition triggered, 24h no-response | Phase 3 | Auto-halt; default-deny per G13 |
| Brand Director invokes unilateral veto on Brand-related stop | Phase 3 | Halt; Growth Lead cannot override; veto recorded with reason |
| Auto-scale eligibility partial (incrementality+ but cannibalization > X%) | Phase 3 | Hold; require manual review |
| Insight Ledger AI-proposal acceptance rate > 80% | Monthly audit | Flag rubber-stamping; Research Lead audit triggered |
| Brand Voice Distinctiveness Index < baseline -1σ | Quarterly audit | Compiler threshold tightening; investigate homogenization |
| Override count > 5 / quarter | Monthly audit | Process review; check Emergency Override commonality |
| Constitution Operational layer not refreshed > 18mo | Quarterly audit | Compiler refuses new content (G15 forcing function); Renewal Committee mandatory |

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

## Anti-Patterns Specific to Growth-Acceptance Recipe

| Anti-Pattern | Counter-Rule |
|--------------|--------------|
| Invoking growth-acceptance on Solo org | Phase 0 aborts; recommends `acceptance` |
| Invoking growth-acceptance below Step 2 adoption | Phase 0 aborts; recommends progressive Step adoption |
| Phase 1 inline orchestration instead of delegating to acceptance | Delegate to acceptance recipe; avoid duplication |
| Phase 0 evidence queue cleared by AI alone | G11 violation; Research Lead merge required |
| Phase 2 auto-scale enabled without Decision Tree compliance | Block; require explicit method declaration |
| Phase 3 Auto-halt blocked by Growth Lead override | G13 enforcement; Brand Director veto authority preserved |
| Skipping Phase 4 cross-cutting audits | Long-term drift; mandatory schedule |
| Treating Phase 3 as one-shot post-launch check | Phase 3 has 3 scheduled gates (+14/+30/+90); each is mandatory |
| Bypassing Compiler via CEO/executive direct content | Acknowledged structural residual (Magi-arbitrated, not technical); requires culture commitment |

---

## Integration with Existing Recipes

- **`acceptance`** — Phase 1 fully delegates to acceptance recipe. Both recipes share the v3 protocol foundation.
- **`apex`** — Phase 6 (Ship) of apex can chain into growth-acceptance for Enterprise org deliverables. Apex authors the change; growth-acceptance gates its lifecycle.
- **`summit`** — Strategic-decision deliverables resulting in brand-touching content flow through growth-acceptance. Summit decides strategy; growth-acceptance gates execution.
- **`kaizen`** — Improvements to brand-touching surfaces should chain kaizen → growth-acceptance (kaizen produces; growth-acceptance gates the lifecycle).
- **`feature`** — recommended downgrade when growth-acceptance Phase 0 detects Solo / SMB or sub-Step-2 adoption.

---

## References

- `_common/PROOF_CARRYING.md` v3 — Tier A Foundation + Tier B Production Pipeline + cross-cutting G11/G14/G15
- `_common/GROWTH_BRAND_PROOF.md` — Layer C protocol (Market + Research + Brand axes), Insight Ledger, Incrementality Gate, Brand Compiler 3-layer, Growth-Brand Contract, Phased Adoption Step 1-4
- `nexus/reference/acceptance-recipe.md` — Phase 1 (merge-time) delegated chain
- `nexus/reference/apex-recipe.md` — discovery → ship cycle; Phase 6 can chain into growth-acceptance
- `nexus/reference/summit-recipe.md` — strategic decisions; can author Layer C content for growth-acceptance gating

**Layer C skill references** (see also each skill's Reference Map):
- **Research axis**: `field` (core), `voice` (sentiment), `trace` (replay), `plea` (synthetic demand), `tome` (knowledge), `insight` (proposed Insight Ledger skill, Architect responsibility)
- **Brand axis**: `vision` (Compiler orchestration + direction), `crest` (brand strategy), `prose` (voice/tone), `clause` (legal), `oath` (regulatory), `muse` (token discipline carry-over)
- **Market axis**: `pulse` (KPI), `experiment` (A/B + Incrementality), `funnel` (LP), `bazaar` (LP studio), `compete` (cannibalization + Distinctiveness), `ledger` (FinOps), `harvest` (PR data), `cloak` (privacy), `vigil` (brand safety)
- **Auto-action**: `mend` (auto-halt + remediation), `beacon` (Brand Lift monitoring)
