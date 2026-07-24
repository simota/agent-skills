# PMM Framework Reference

**Purpose:** Phase-by-phase workflow, the grounding discipline, and the advisor Q&A loop.
**Read when:** You need GROUND→POSITION→MESSAGE→GTM→ENABLE detail, the proof-grounding rules, or the `ask` loop.

## Contents
- Grounding (product truth + audience + competitive frame)
- GROUND Phase
- POSITION Phase
- MESSAGE Phase
- GTM Phase
- ENABLE Phase
- Advisor Q&A Loop (`ask`)
- Worked Example

---

## Grounding

PMM's distinctive discipline, inherited from PDM: **a message is the intersection of what the product does (truth) and who it is for (audience), differentiated against rivals (frame).** Missing any side is half a message.

| Input | Source | What it provides | If absent |
|-------|--------|------------------|-----------|
| Product truth | PDM (delivery status), Lens (capability detail), specs/README | What is *actually shipped* — the only thing PMM may message | Ask First: message from stated claims only (cap confidence Medium) or stop |
| Audience | Cast (personas), Field (research/JTBD), Voice (verbatims) | The ICP, their job-to-be-done, their language | Ask First: define a provisional ICP or request Cast/Field |
| Competitive frame | Compete (positioning maps, battle cards, differentiation) | What "different" means relative to alternatives | Offer a Compete handoff before asserting differentiation |
| Market context | Helm (sizing, segments), Voice (resonance) | Where value lands, what segments matter | Proceed; note context is inferred |

**Proof-point rule:** every value claim must name a shipped capability and its evidence (`file:line`, a PDM `Done` row, or a spec'd-and-verified behavior). A claim with no proof point is `Unsubstantiated` — drop it from the message, do not soften it into vapor.

---

## GROUND Phase

Establish the three sides before authoring. Confirm with the user if the product-truth source is entirely absent (Ask First boundary).

```yaml
GROUND_INPUTS:
  product_truth:
    from: ["PDM_TO_PMM_HANDOFF (delivery status)", "Lens capability survey", "specs", "README features"]
    capture: ["shipped features + evidence", "what is NOT yet shipped (exclude from messaging)"]
  audience:
    from: ["CAST_TO_PMM_HANDOFF (personas)", "Field research/JTBD", "Voice verbatims"]
    capture: ["ICP", "job-to-be-done", "pains/gains", "their words"]
  competitive_frame:
    from: ["COMPETE_TO_PMM_HANDOFF", "positioning map", "battle card"]
    capture: ["alternatives", "axes of differentiation", "what rivals claim"]
  goal:
    capture: ["launch? reposition? new-segment entry?", "primary metric the marketing serves"]
```

Detail on sourcing → `reference/positioning.md` and `reference/messaging.md`.

---

## POSITION Phase

The highest-stakes judgment — think step-by-step (Opus 5 P5). Author one positioning statement per target segment.

Method, frameworks, and the positioning-map technique → `reference/positioning.md`.

Output: a positioning statement (target / category / value / differentiator) plus an optional positioning map, each competitively anchored and segment-specific.

---

## MESSAGE Phase

Build the messaging house from the positioning: core narrative → value pillars → benefits → proof points → features. One variant per segment.

Method, proof-point grounding, and per-segment variants → `reference/messaging.md`.

Rule: every value pillar carries ≥1 proof point tied to a shipped capability. Value leads; features are evidence, not the headline.

---

## GTM Phase

Assemble the go-to-market / launch plan. **Marketing launch only — pair the technical release to Launch.**

- **Segmentation & ICP**: which segments, in what order, why.
- **Channel mix**: match channels to where the segment already is (do not assume).
- **Launch tier**: Tier 1 (major, full-court) / Tier 2 (standard) / Tier 3 (light) — justify the choice.
- **T-minus timeline**: asset checklist with owners and handoffs (narrative → Saga, LP → Funnel, copy → Prose, slides → Stage, video → Cue/Director).

Priority scoring is deferred to Rank; KPI/metric definition is deferred to Pulse. Detail → `reference/gtm.md`.

---

## ENABLE Phase

Draft the enablement assets that carry the message to sales/market: one-pager, pitch outline, FAQ, objection handling, internal launch brief. Provide strategy and structure; hand polished narrative to Saga and final copy to Prose. Templates → `reference/output-formats.md`.

---

## Advisor Q&A Loop (`ask`)

PMM-style conversational entry point. Per turn: `CLASSIFY → ANSWER → OFFER`.

```
per turn:
  1. CLASSIFY — map the question to a recipe lens:
       "how do we stand out / position"   → position
       "what do we say / value prop"       → message
       "how do we bring it to market"      → gtm
       "how do we launch / announce"       → launch
       "give me a one-pager / FAQ"         → enable
  2. REUSE   — reuse already-grounded product truth, audience, and competitive frame from earlier turns
  3. ANSWER  — lowest sufficient tier: lead with the value/outcome, then the grounding
  4. GROUND  — proof point (shipped capability + evidence); name the segment; state confidence
  5. OFFER   — one most-likely next step, mapped to a recipe or a handoff
  6. ROUTE   — out-of-scope → name the agent and stop:
       "who are the competitors / battle card?" → Compete
       "write the story / narrative"            → Saga
       "write the final copy"                   → Prose
       "what's actually built?"                 → PDM
       "build the landing page"                 → Funnel
```

Session memory: cache grounded product truth, audience, and competitive frame once per session; re-verify a capability claim if the product may have changed. Never reuse a value claim without its proof point still holding.

---

## Worked Example

A `position` pass on a small product, end to end.

**Goal:** "Position our new audit-log feature for security-conscious SaaS buyers."

**GROUND** —
- Product truth (PDM `Done` rows): `audit/logger.ts:8` immutable append-only log, `audit/export.ts:22` SIEM export (Splunk/Datadog), 90-day retention. NOT shipped: real-time alerting (roadmap only → exclude from message).
- Audience (Cast): "Security-conscious SaaS admin" — JTBD: "prove to my auditor who did what, fast." Pain: manual log stitching before SOC 2.
- Competitive frame (Compete): rivals offer logs but no native SIEM export; export is the wedge.

**POSITION** — segment-specific statement:
> *For* security-conscious SaaS admins preparing for SOC 2, *who* must prove access history to auditors, *our* audit log *is* a compliance-ready activity record *that* exports natively to your SIEM — *unlike* competitors' export-less logs, *we* drop the data straight into Splunk/Datadog. (differentiator grounded in `audit/export.ts:22`)

**MESSAGE** — value pillar "Audit-ready in minutes, not weeks":
- benefit: hand auditors a complete trail on demand
- proof point: immutable append-only log (`audit/logger.ts:8`) + native SIEM export (`audit/export.ts:22`) — **grounded, High confidence**
- excluded: "real-time threat alerts" → `Unsubstantiated` (roadmap, not shipped) — dropped, not softened.

**ENABLE** — one-pager headline leads with the outcome ("Pass your SOC 2 access-review in an afternoon"), supported by the two proof points; offer: hand the narrative to Saga, the LP to Funnel.

The valuable discipline here is the **dropped claim**: "real-time alerting" would have been the flashiest line and it is vapor — PMM refuses it, exactly as PDM refuses to call a roadmap item "Done."
