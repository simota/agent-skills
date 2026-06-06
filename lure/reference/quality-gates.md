# Quality Gates

Per-stage exit criteria for the `lure` LP studio chain. A stage that fails its gate either repairs in place (≤1 retry) or escalates back to the user.

Gates are not negotiable. Recipe selection determines which stages run, but every stage that runs must clear its gate.

---

## Gate Mechanics

| Outcome | Action |
|---------|--------|
| **PASS** | Advance to next stage |
| **FAIL_REPAIR** | Re-dispatch the same delegate(s) with corrective handoff; max 1 retry |
| **FAIL_ESCALATE** | Stop chain, persist state, ask user for direction |
| **CONDITIONAL_PASS** | Pass with an explicit follow-up logged; downstream stage receives the open item as a constraint |

Gate evaluation is owned by `lure` (not the delegate). `lure` reads the delegate's output, checks against the gate's measurable criteria, and chooses outcome.

### Oscillation Guard

If the same criterion flips PASS↔FAIL across 2 retries (same axis or cross-axis), `lure` skips the standard 1-retry rule and escalates immediately to Magi for trade-off arbitration. Examples:

- DESIGN AA contrast PASS → repair for Visual Hierarchy → contrast FAIL again → escalate (don't loop)
- OPTIMIZE Motion ≥15/20 → Bolt INP repair → Motion drops to 14/20 → escalate (Bolt vs Flow ping-pong)
- GEO 14/20 → Growth adds TL;DR → Brand voice variance ≥1.5 → escalate (Growth vs Prose conflict)

### Trade-off Ping-Pong Detector

When repairing axis A causes axis B to regress in the same stage, do NOT use the 1-retry budget. Route to Magi for Logos/Pathos/Sophia arbitration. Common ping-pongs (see also "Axis Trade-off Discipline" below):

- Motion richness vs INP budget (Flow ↔ Bolt)
- Hero asset richness vs LCP (Sketch/Ink ↔ Bolt)
- SEO keyword density vs Brand voice (Growth ↔ Prose)
- Detail-craft completeness vs release date (Vision/Palette ↔ Launch)

---

## Stage 1 · DISCOVER Gate

**Criteria**:
- 3+ market insights with citations (Researcher) — *skip if recipe = saas/ecom/event/magnet with existing brand*
- Top 3 competitor LPs teardown with feature matrix + 2+ differentiation hooks (Compete)
- Sentiment themes + top-5 pain quotes (Voice) — *skip if no existing customers*

**Repair triggers**:
- Generic insights ("the market is growing") — re-dispatch with sharper brief
- Competitor teardown missing CTA / above-fold analysis — re-dispatch
- Pain quotes are summarized, not verbatim — re-dispatch for quotes

**Escalate when**:
- Researcher cannot find category data → ask user for category framing
- Compete cannot identify direct competitors → ask user to name them

---

## Stage 2 · AUDIENCE Gate

**Criteria**:
- 1–3 personas, each with: name, role, goals, frictions, jobs-to-be-done, channel, decision driver (Cast)
- Journey map covering Awareness → Consideration → Decision → Post-purchase (canvas-rendered or text-form)
- 5+ unmet needs ranked by intensity (Plea)
- **Echo baseline mandatory**: if a draft structure/wireframe exists, Echo cognitive walkthrough produces emotional friction score (target ≤ Medium). If none exists, Echo runs on Funnel's preliminary section-list spec at minimum — never skip entirely, otherwise VERIFY-stage re-walk has no baseline to compare against and design regressions become undetectable.

**Repair triggers**:
- Personas are too generic ("decision maker, 30–50") — re-dispatch Cast with named ICP attributes
- Journey map skips a stage — re-dispatch
- Unmet needs duplicate published feature list — re-dispatch Plea with "feature gaps" reframing

**Escalate when**:
- Cast cannot anchor on a primary persona without a stakeholder decision → ask user

---

## Stage 3 · STRATEGY Gate

**Criteria**:
- CVR target locked (Median / Top Quartile / Top Decile + chosen target + traffic-source qualifier), calibrated against `conversion-playbook.md` industry baseline; `recipe_alignment_check` PASS
- KPI tree: primary (CVR) + 3–5 secondary metrics (Pulse)
- Funnel event taxonomy: page_view → engagement → CTA_click → form_start → form_submit → success (Pulse)
- North-Star metric named and consistent with KPI tree
- **GEO measurement plan**: Mention Rate ≥15% target, Citation Rate baseline+30%, Share-of-Voice tracked (Pulse + Growth alignment)
- Strategic deliberation logged (Magi) for: primary persona, primary objection, urgency framing
- **Brand System triple lock** (machine-checkable): all three of `vision_archetype_locked`, `saga_story_locked`, `compete_positioning_locked` are `true` in the project state. Saga's Strategy-stage output is the brand story arc (Hero/Guide/Problem/Plan/Success/Failure); a separate narrative-copy pass happens at STRUCTURE.
- **Above-the-fold asset weight budget** declared: hero image ≤200KB / hero video ≤2MB / total font ≤100KB. Hero asset lead-time risk surfaced (lead-time ≤ remaining stage budget).

**Repair triggers**:
- CVR target not industry-anchored — re-dispatch Pulse with playbook reference
- Event taxonomy missing form fields or success event — re-dispatch
- Magi verdict is "no decision" — re-dispatch with sharper question

**Escalate when**:
- User has not approved CVR target → ask once before Structure stage
- Strategic deliberation reveals two-promise drift → escalate to enforce one-promise rule

---

## Stage 4 · STRUCTURE Gate

**Criteria**:
- **Primary scan pattern locked** (F / Z / Layer-cake / Centered axis / Card grid) per `ia-blueprint.md §1.2`
- **Navigation pattern decided** (no-nav / utility bar / sticky CTA / anchor TOC / mobile bottom bar / exit-intent) per `ia-blueprint.md §1.6`
- Wireframe outline: hero + 5–7 sections (Funnel)
- **Above-fold component set explicit**: headline + sub-headline + hero CTA + (optional secondary CTA) + hero asset + (optional trust strip) — each present-or-absent decision logged
- Copy v1 covering: headline, sub-headline, hero CTA, 3–5 benefits, 1+ objection handling, social proof block, FAQ (3–5 Q), final CTA (Funnel + Prose)
- Reading level appropriate to persona (FK 6–9 for consumer, 8–11 for B2B) (Prose)
- Saga arc (when invoked): narrative copy applied — before/after frame + customer hero arc on at least 1 testimonial; this is distinct from the Strategy-stage Brand Story arc
- **Form consent microcopy drafted** (if form-driven LP): consent/unsubscribe/GDPR notice copy below form fields
- **Thank-you / post-conversion page** sketched for lead-gen / magnet / event recipes

**Repair triggers**:
- Hero copy fails the 5-second test (cannot answer "what / for whom / why now" in 5s) — re-dispatch Funnel + Prose
- Objection handling absent or generic — re-dispatch Prose with persona objection list from Audience stage
- Social proof block is placeholder ("[insert logos]") — re-dispatch with specific proof types (logos / numbers / quotes / case studies)

**Escalate when**:
- Brand has no usable social proof yet → ask user to choose "trust mechanic" (founder authority / industry endorsement / press / open-source signals)

---

## Stage 5 · DESIGN Gate

**Criteria**:
- Vision direction approved (`direction.md` or equivalent) with: archetype, mood, type direction, palette intent
- Tokens frozen (Muse) — color, type scale, spacing scale, radius, motion duration baseline
- WCAG 2.2 AA contrast ratios verified — 4.5:1 text, 3:1 UI (Palette)
- Hero assets locked (Ink or Sketch or Haul) — production-ready, license-cleared
- If Figma source exists: Frame extraction complete, Code Connect mapping if needed

**Repair triggers**:
- AA contrast fails for any text — re-dispatch Muse to adjust palette
- Hero asset is placeholder — re-dispatch Sketch/Ink
- Tokens contradict Vision direction (e.g., dark archetype with high-saturation accent) — re-dispatch Muse

**Escalate when**:
- Vision direction is missing and user brief is ambiguous → route to Vision first, then resume
- Hero asset requires paid API spend > approved budget → ask user

---

## Stage 6 · BUILD Gate

**Criteria**:
- Working prototype on tokens, no hardcoded values (Forge → Artisan)
- Production code passes type-check, lint, build (Artisan)
- Lighthouse Perf ≥ 80 on prototype (not yet 90 — that's Optimize stage)
- Motion implementation respects `prefers-reduced-motion` (Flow)
- i18n string extraction complete if Polyglot in scope — no hardcoded user-facing strings

**Repair triggers**:
- Hardcoded color / spacing values found — re-dispatch Artisan with token reference
- Type errors — re-dispatch Artisan
- Motion breaks INP budget on test devices — coordinate Flow + Bolt

**Escalate when**:
- Build framework choice was not specified and lure cannot infer (no existing codebase) → ask user (React / Vue / Svelte / static)

---

## Stage 7 · OPTIMIZE Gate

**Criteria**:
- Lighthouse Mobile: Perf ≥ 90, Accessibility ≥ 95, Best Practices ≥ 95, SEO ≥ 95
- Core Web Vitals: LCP ≤ 2.5s, INP ≤ 200ms, CLS ≤ 0.1 — all Green; also TTFB ≤ 800ms (p75), FCP ≤ 1.8s
- **GEO rubric ≥ 15/20** (Growth) — JSON-LD, structured data, AI-search friendly headings, per-platform tactics. The `/20` rubric is the canonical scale; `≥90` notation is deprecated.
- First A/B variant designed with hypothesis, sample size (≥1000 conversions/variant, 95% significance, ≥14 days), decision criteria (Experiment)
- Form CRO completed (if form-driven LP): field count justified by lead-quality filter rationale, label clarity, error state copy, segment-aware CTA where traffic permits
- **Schema-content consistency check**: AI engines verify schema fields match visible page content (e.g., `Offer.price` matches displayed price)

**Repair triggers**:
- Perf below 90 — re-dispatch Bolt with specific budget breach (LCP / INP / CLS)
- SEO/GEO below 90 — re-dispatch Growth with missing-element list
- Variant lacks measurable decision criteria — re-dispatch Experiment

**Escalate when**:
- Perf budget cannot be met with current asset weight (e.g., hero video) → ask user about asset reduction
- A/B test infrastructure missing → ask user about variant deployment strategy

---

## Stage 8 · VERIFY Gate

**Criteria**:
- Judge: zero unresolved P1 or P2 findings (P3 acceptable with explicit ack)
- Voyager: E2E suite green covering happy path + form submit + CTA click + error states + visual regression baseline
- Attest: spec compliance ≥ 95% AC coverage against Structure-stage wireframe + copy spec
- Sentinel: zero high-severity findings (form input validation, headers, secrets scan, dependency CVE)
- Echo re-walk: friction score ≤ Low (improved from Audience-stage baseline)
- WCAG 2.2 AA: full audit pass (contrast, focus visible, keyboard reachable, ARIA roles, image alt text)

**Repair triggers**:
- Any P1/P2 — re-dispatch Builder/Artisan with Judge findings
- E2E flake — re-run; if reproducible, re-dispatch Voyager to stabilize
- Attest coverage gap — re-dispatch Artisan to fix or update spec
- Sentinel high finding — re-dispatch Sentinel with fix applied

**Escalate when**:
- Judge finds an intent misalignment (built feature ≠ briefed feature) → escalate to user
- Echo re-walk friction worsened vs. Audience stage → escalate; design regression

---

## Stage 9 · LAUNCH Gate

**Criteria**:
- Release plan: version, rollout strategy (full / staged / canary), rollback plan, feature flag if applicable (Launch)
- PR ready: clean commits, conventional-commit messages, no agent names in commit/PR text (Guardian)
- Analytics events live and emitting: at least page_view + CTA_click + form_submit verified in dashboard (Beacon)
- Alert rules armed: 5xx spike, form-submit drop, CWV regression
- First A/B variant queued or "control only" decision documented
- Privacy / Terms / consent banner in place if PII collected (Cloak / Clause checked)

**Repair triggers**:
- Analytics not firing — re-dispatch Beacon
- Rollback plan missing — re-dispatch Launch
- PR fails Guardian classification (e.g., commit contains agent name) — re-dispatch Guardian

**Escalate when**:
- Rollback strategy requires infrastructure access lure cannot grant → ask user
- Legal review (Clause) flags unresolved compliance item → escalate

---

## Cross-Stage Continuous Checks

These run continuously, not at a single gate:

| Check | Frequency | Owner | Threshold |
|-------|-----------|-------|-----------|
| One-promise discipline | Every stage | `lure` | Brief carries one primary value prop. Two-promise drift = stop and ask. |
| Token discipline | Build, Optimize, Verify | `lure` | No hardcoded user-facing values in production code |
| Brand alignment | Design, Build, Optimize | `lure` | Production rendering matches Vision direction.md and Brand System record |
| Persona alignment | Structure, Design, Verify | `lure` | Copy, design, and tested flow reference the same primary persona |
| Performance budget | Build, Optimize | `lure` + Bolt | LCP ≤ 2.5s, INP ≤ 200ms, CLS ≤ 0.1 throughout |
| A11y baseline | Design, Build, Verify | `lure` + Palette | WCAG 2.2 AA never regresses |

---

## 6-Axis Rubric Gate

Composite gate enforced at the DESIGN exit (Design / Animation / Branding rubrics) and the OPTIMIZE exit (Marketing / SEO / IA / GEO). All thresholds must clear before VERIFY.

| Axis | Rubric | Threshold | Owner | Source |
|------|--------|-----------|-------|--------|
| **Design** | Visual Hierarchy Rubric (9 criteria × 3 points; Hero-Contract Legibility added) | ≥ 20/27 | Vision + Muse + Palette + `lure` (or Atelier — rubric still enforced) | `craft-standards.md` § Design Discipline |
| **Animation** | Motion Quality Rubric (5 criteria × 4 points) — INP ≤50ms is hard ceiling, NOT a rubric criterion | ≥ 15/20 | Flow + Muse + Bolt | `craft-standards.md` § Animation Discipline |
| **Branding** | Brand Quality Rubric (6 criteria × 4 points; Trust-Signal Density added) | ≥ 17/24 | Vision + Saga + Compete + Prose | `craft-standards.md` § Branding Discipline |
| **Marketing** | CVR target + messaging hierarchy + variant queued | CVR target met (industry-calibrated, recipe-aligned, traffic-source qualified); first A/B variant designed; analytics events live | Funnel + Pulse + Growth + Experiment + Magi | `conversion-playbook.md` |
| **SEO (Technical)** | Technical SEO Audit Checklist (extended set) | 100% checked | Growth + Bolt + Polyglot | `ia-blueprint.md` § 2 |
| **SEO (Content)** | Intent alignment + keyword discipline + E-E-A-T signals + Author entity | Intent matched (incl. Answer-Engine intent if applicable); primary keyword aligned across title/H1/first paragraph; ≥ 2 E-E-A-T signals visible; Author entity with sameAs to authoritative profiles | Growth + Prose | `ia-blueprint.md` § 3 |
| **GEO** | GEO Quality Rubric (5 criteria × 4 points) on /20 scale only | ≥ 15/20 | Growth | `ia-blueprint.md` § 4 |
| **IA** | IA Quality Rubric (5 criteria × 4 points) | ≥ 15/20 | Funnel + Canvas + Echo + Prose | `ia-blueprint.md` § 1 |

### Axis Repair Workflow

When an axis fails:

1. `lure` flags the failing criterion with score and gap.
2. Re-dispatch the owning agent(s) with a focused repair bundle.
3. Re-score the rubric.
4. If still failing after one retry → escalate to user with a written choice (accept conditional pass / extend scope / cut feature).

### Axis Trade-off Discipline

Conflicts between axes are managed, not silenced:

| Conflict | Default resolution |
|----------|--------------------|
| SEO keyword vs. Brand voice | Brand voice wins; weave keyword naturally elsewhere |
| Motion richness vs. INP budget | INP budget wins; Flow trims motion to ≤ 50ms contribution |
| Hero asset richness vs. LCP | LCP wins; compress, lazy-load below fold, swap to AVIF/WebP |
| Detail-craft completeness vs. release date | Detail craft wins for premium recipe; escalate for time-boxed event recipe |
| Calm-UI clarity vs. urgency framing | Calm-UI wins when trust-driven persona, urgency wins when transactional persona; Magi arbitrates |

---

## Gate Reporting Format

After each stage, `lure` emits a stage report in this shape and persists to `.agents/lure/{project}.json`:

```yaml
STAGE_REPORT:
  Stage: STRUCTURE
  Outcome: PASS | FAIL_REPAIR | FAIL_ESCALATE | CONDITIONAL_PASS
  Delegates: [Funnel, Prose, Saga]
  Artifacts: [wireframe-v1.md, copy-v1.md, saga-arc.md]
  Gate_Checks:
    - check: hero answers what/for-whom/why-now in 5s
      result: PASS
    - check: objection handling present and specific
      result: FAIL_REPAIR
      action: re-dispatched Prose with persona objection list
  Open_Items: []
  Next_Stage: DESIGN
```
