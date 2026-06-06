# Agent Roster

The complete delegate roster for the `bazaar` LP studio chain, organized by stage. Each entry names the role, the artifact returned to `bazaar`, and the overlap watch-out so `bazaar` does not double-book responsibilities.

`bazaar` itself never writes copy, designs pixels, or ships code. It selects delegates and brokers handoffs.

---

## Stage 1 · DISCOVER

| Agent | Role in chain | Returns | Overlap watch |
|-------|---------------|---------|---------------|
| **researcher** | Market and trend intel for the product category | Top-3 insights, market size signals, sub-segments | Skip if brand+market are mature |
| **compete** | Competitor LP teardown (top 3–5), feature matrix, positioning map | Battle card, differentiation hooks, AI brand visibility | Don't ask compete to write copy — that's prose/funnel |
| **voice** | Existing-customer feedback synthesis (reviews, NPS, support tickets) | Sentiment themes, top pain quotes | Skip if no prior customers (greenfield product) |

Parallel fan-out: yes (3 concurrent). Field is independent. Compete and Voice can both run alongside.

---

## Stage 2 · AUDIENCE

| Agent | Role in chain | Returns | Overlap watch |
|-------|---------------|---------|---------------|
| **cast** | Persona generation (1–3 personas, ICP first) | Persona cards with goals, frictions, jobs-to-be-done | Cast persists personas in registry — reuse across runs |
| **echo** | Cognitive walkthrough of the proposed flow per persona | Confusion points, emotional friction score | Run only when a draft structure or wireframe exists |
| **plea** | Unmet-need surfacing, authentic feature-request voice | 5+ unmet needs ranked by intensity | Don't confuse with voice (real feedback); plea is synthetic advocacy |

Parallel fan-out: Cast first (other agents need persona IDs), then Echo + Plea in parallel.

---

## Stage 3 · STRATEGY

| Agent | Role in chain | Returns | Overlap watch |
|-------|---------------|---------|---------------|
| **pulse** | KPI definition, funnel events, North-Star metric, dashboard spec | KPI tree, event taxonomy, CVR target reference | Pulse owns metrics design end-to-end; growth handles SEO/CRO measurement |
| **magi** | Multi-perspective deliberation for high-stakes strategic calls | Logos/Pathos/Sophia view + recommendation | Use for objection-handling framing, price-anchoring, urgency vs. clarity trade |

Parallel fan-out: Serial (Pulse → Magi). Magi consumes Pulse's KPI tree.

---

## Stage 4 · STRUCTURE & COPY

| Agent | Role in chain | Returns | Overlap watch |
|-------|---------------|---------|---------------|
| **funnel** | LP structure (above-fold, sections, CTA strategy, form design, A/B variant outline) | Wireframe outline + copy direction brief | Funnel is the LP-section specialist; bazaar orchestrates it, not replaces it |
| **prose** | UX writing — headlines, microcopy, error states, button labels | Copy v1 (hero, sub, CTA micro, FAQ, error) | Prose owns voice and tone; funnel owns positioning. Prose also writes TL;DR / citable units per ia-blueprint §4.1 (Growth supplies structural brief, never the words). |
| **saga** | **Two roles** — (1) at STRATEGY: Brand Story arc (Hero/Guide/Problem/Plan/Success/Failure) for the Brand System record; (2) at STRUCTURE: narrative-copy application onto wireframe sections | Strategy: brand_story.md; Structure: section-level narrative passes | Use only when narrative is the right framework (B2B, complex products, heritage brand) |

Parallel fan-out: Funnel first, then Prose ↔ Saga in parallel (or Saga skip for SaaS / magnet).

---

## Stage 5 · DESIGN

| Agent | Role in chain | Returns | Overlap watch |
|-------|---------------|---------|---------------|
| **vision** | Creative direction, mood, archetype, design rationale | `direction.md` with tokens hint, type direction, palette intent | Vision decides, doesn't implement; never skip when brand-touching |
| **muse** | Design tokens (color, type, spacing, radius, motion) — DTCG-aligned | Token JSON + apply plan | Reuse existing system if brand is mature; create only when needed |
| **palette** | Usability and a11y polish (contrast, focus, cognitive load) | A11y baseline + interaction recommendations | Palette also re-walks at Verify stage |
| **frame** | Figma context extraction or Code Connect mapping if Figma source exists | Design context bundle for Artisan | Skip if no Figma source |
| **ink** | Vector icons, illustrations, sprite assets | SVG asset bundle | For icon-heavy LPs only |
| **sketch** | AI image generation (hero, lifestyle, abstract) | Generated images + prompt log | External paid API — Ask First |
| **atelier** *(optional)* | Whole design pipeline delegation when LP is part of a multi-artifact bundle (LP + slide + 1-pager + marketing captures) | Bundled handoff package | Use ONLY when multi-artifact bundling; single-LP direct delegation is faster |

Parallel fan-out: Vision first (direction is upstream). Then Muse + Palette + Frame + Ink in parallel. Sketch serial (paid API).

**Decision**: delegate to Atelier if the LP is part of a 3+ artifact design bundle. Otherwise call Vision/Muse/Palette/Frame directly to avoid double-orchestration overhead.

---

## Stage 6 · BUILD

| Agent | Role in chain | Returns | Overlap watch |
|-------|---------------|---------|---------------|
| **forge** | Rapid prototype (working UI on tokens, no production polish) | Prototype code + Lighthouse prototype score | Prototype-only; Artisan does production |
| **pixel** | Mockup-faithful reproduction from PNG/JPG | Pixel-accurate HTML/CSS + diff verification | Use only when high-fidelity mockup exists |
| **artisan** | Production frontend (React/Vue/Svelte) on tokens | Production code, type-safe, test-ready | Convert forge prototype, don't re-architect |
| **flow** | Animations and motion (CSS/JS), scroll-driven effects | Motion implementation + perf-safe verification | INP budget — coordinate with Bolt |
| **polyglot** | i18n and l10n (string extraction, Intl API, RTL) | Translation keys, runtime locale switching | Skip if single-locale; otherwise must be in scope from Structure. **Polyglot starts AFTER Prose copy v1 is frozen** — earlier starts cause key re-extraction and double-wrapped `t()` calls. |

Parallel fan-out: Forge → Artisan serial. Pixel only if mockup. Flow in parallel with Artisan once structure is stable. Polyglot waits for Prose copy v1 freeze.

---

## Stage 7 · OPTIMIZE

| Agent | Role in chain | Returns | Overlap watch |
|-------|---------------|---------|---------------|
| **growth** | SEO (meta/OGP/JSON-LD/headings), SMO (social share), CRO (CTA/form/exit-intent), GEO (AI citation readiness) | SEO + GEO score, CRO recommendations, structured-data spec | Growth covers four pillars; don't split prematurely |
| **bolt** | Frontend perf — re-render reduction, lazy loading, image optimization, CWV tuning | Lighthouse Perf ≥ 90, LCP/INP/CLS in budget | Coordinate with Flow on motion-driven INP cost |
| **experiment** | A/B variant design (hypothesis, variant spec, sample size, decision criteria) | First variant queued + measurement plan | Experiment designs; growth and bolt implement |

Parallel fan-out: Growth + Bolt in parallel, then Experiment when first variant is being designed.

---

## Stage 8 · VERIFY

| Agent | Role in chain | Returns | Overlap watch |
|-------|---------------|---------|---------------|
| **judge** | Tri-engine code review (Codex + Antigravity + Claude) on production code | P1/P2/P3 findings with grounding | Judge is the gate; don't ship under unresolved P1/P2 |
| **voyager** | E2E tests (happy path + form / CTA flows, visual regression, a11y test) | Test suite + green run | Voyager covers E2E; Radar covers unit/integration if needed |
| **attest** | Spec compliance — BDD scenarios, traceability matrix vs. structure spec | Compliance verdict ≥ 95% AC coverage | Attest is evidence-based; reject hand-waving |
| **sentinel** | Static security scan — secrets, input validation, headers, CVE | Security verdict | Form-driven LPs especially must pass Sentinel |
| **echo** *(re-walk)* | Persona re-walk on shipped code | Friction score delta vs. Audience-stage Echo | Compare against earlier echo to confirm improvement |

Parallel fan-out: yes, all 5 in parallel (fan-out cap = 5).

---

## Stage 9 · LAUNCH

| Agent | Role in chain | Returns | Overlap watch |
|-------|---------------|---------|---------------|
| **launch** | Release plan, versioning, CHANGELOG, rollback plan, feature flag | Release dossier | Launch owns release coordination end-to-end |
| **guardian** | Commit/PR strategy, granularity, naming, branch hygiene | PR ready for review | Don't bypass — even a one-page LP needs a clean PR trail |
| **beacon** | Observability — analytics events wired, dashboard live, alerts armed | Live dashboard + alert rules | Beacon validates Pulse's KPI spec is actually emitting (incl. GEO Mention/Citation/SoV KPIs) |
| **funnel (thank-you pass)** | Thank-you / post-conversion page design — confirmation copy, next-step CTA (related resource / share / referral), upsell where appropriate | Thank-you page mockup + copy | Mandatory for lead-gen / magnet / event recipes; skip only for transactional ecom (use order-confirmation flow instead) |

Parallel fan-out: Serial (Launch → Guardian → Beacon).

---

## Cross-Stage Specialists

These agents may be invoked at any stage based on signal, not stage:

| Agent | When `bazaar` invokes it |
|-------|------------------------|
| **canon** | Compliance audit if WCAG 2.2 AA, OpenAPI for embedded forms, or sector-specific standard (HIPAA, PCI) applies |
| **clause** | If the LP carries Terms / Privacy / Tokushoho text, route to clause before Launch |
| **cloak** | If the LP collects PII (forms, cookies, tracking) — privacy review |
| **canvas** | Journey-map visualization for stakeholder review, ERD-like flow diagrams |
| **morph** | Format conversion if a 1-pager / PDF / Word artifact is part of the brief |
| **scribe** | Spec doc for the LP if the team requires PRD / LLD before Build |
| **omen** | Pre-mortem for high-stakes launches — what could fail in production |
| **siege** | Load test if the LP is expected to absorb a campaign spike |
| **director** | Demo video of the LP for sales enablement / onboarding |
| **navigator** | Quick browser checks during Build (visual sanity, console errors) |

**Fan-out cap discipline**: cross-stage specialists count toward the 5-concurrent cap. If a stage already runs 5 primary delegates (e.g., VERIFY = Judge + Voyager + Attest + Sentinel + Echo) and PII / Tokushoho / a11y compliance requires Cloak + Clause + Canon, sequence those after the primary batch — never run 6–8 concurrently.

---

## Overlap with Adjacent Orchestrators

| Orchestrator | Overlap with `bazaar` | Differentiation |
|--------------|----------------------|------------------|
| `funnel` | Stage 4 (Structure) | Funnel is the LP-section specialist; bazaar is the chain. Bazaar invokes funnel. |
| `atelier` | Stage 5 (Design) | Atelier handles design pipeline for multi-artifact bundles; bazaar for single LP handles design directly. Bazaar invokes atelier on bundle requests. |
| `titan` | Stage 6 (Build) | Titan delivers product-wide build; bazaar scopes to a single LP. If the LP is part of a product release, bazaar escalates to titan or coordinates via nexus. |
| `nexus` | Generic multi-domain | Bazaar is LP-axis only. If the request crosses LP axis (security + data + infra + LP), escalate to nexus with the LP slice as a sub-task. |

`bazaar` ≈ 30% capability overlap with the union of (funnel + atelier + portions of titan). The 70% unique surface is research-to-launch coordination, recipe selection, and quality-gate enforcement specific to landing pages.

---

## Axis Ownership Map

Six quality axes mapped to agent clusters. `bazaar` is the conductor; each axis has a lead and supporting cast. Rubrics live in `craft-standards.md` and `ia-blueprint.md`.

### Design Axis

| Role | Agent | Responsibility |
|------|-------|----------------|
| Lead | **Vision** | Archetype, mood, type direction, palette intent, motion intent → `direction.md` |
| Token authority | **Muse** | DTCG tokens (color/type/space/radius/motion), apply plan, dark mode |
| A11y & feel | **Palette** | Contrast (AA/AAA stretch), focus rings, cognitive load, interaction quality |
| Figma source | **Frame** | Design context extraction, Code Connect mapping |
| Asset (vector) | **Ink** | Icon system, illustrations, sprites |
| Asset (raster / AI) | **Sketch** | Hero, lifestyle, atmospheric imagery (paid API — Ask First) |
| Fidelity QA | **Pixel** | Mockup-to-code visual diff verification |

Pattern: Vision (decide) → Muse (encode) → Palette (humanize) → Frame/Ink/Sketch (asset) → Pixel (verify). `bazaar` scores Design Rubric ≥ 18/24 at DESIGN gate.

### Animation Axis

| Role | Agent | Responsibility |
|------|-------|----------------|
| Lead | **Flow** | Motion implementation (CSS / WAAPI / View Transitions / scroll-driven) |
| Token authority | **Muse** | Motion tokens (duration / easing / stagger) under `motion.*` |
| Direction | **Vision** | Motion story consistent with brand archetype |
| Perf guardrail | **Bolt** | INP budget enforcement (motion contribution ≤ 50ms) |
| A11y | **Palette** | `prefers-reduced-motion` alternative path |

Pattern: Vision sets motion story → Muse tokenizes → Flow implements → Palette validates reduced-motion → Bolt enforces INP budget. `bazaar` scores Motion Rubric ≥ 15/20 at DESIGN gate.

### Branding Axis

| Role | Agent | Responsibility |
|------|-------|----------------|
| Lead (visual) | **Vision** | Archetype, visual identity, mood, design direction |
| Lead (narrative) | **Saga** | Brand story arc (customer-as-hero, problem, plan, success/failure) |
| Lead (positioning) | **Compete** | Category, differentiator, against-whom, positioning map |
| Voice execution | **Prose** | Voice & tone realization in copy across all surfaces |
| Strategy arbitration | **Magi** | Tone-spectrum trade-offs (clarity vs urgency, formal vs casual) |

Pattern: Vision + Saga + Compete jointly author the Brand System record at STRATEGY → Prose carries voice into copy → Vision validates visual coherence → `bazaar` runs Three-Channel Coherence Audit (visual / voice / experience) at VERIFY. Score Brand Rubric ≥ 14/20.

### Marketing Axis

| Role | Agent | Responsibility |
|------|-------|----------------|
| Lead (structure) | **Funnel** | LP structure, CTA strategy, form design, messaging hierarchy (Big Idea → Headline → Sub → Proof) |
| Lead (KPI) | **Pulse** | CVR target, funnel events, North-Star, dashboard spec |
| Lead (acquisition) | **Growth** | SEO/SMO/CRO/GEO four-pillar optimization |
| Variant design | **Experiment** | A/B hypothesis, variant spec, sample size, decision criteria |
| Strategic arbitration | **Magi** | Pricing, urgency, primary objection framing |
| Voice & evidence | **Voice** | Customer feedback themes → copy proof points |

Pattern: Pulse + Magi set CVR target → Funnel structures + Growth optimizes acquisition → Experiment designs first variant → Voice + Saga supply proof. `bazaar` enforces CVR target met, messaging hierarchy clean, variant queued, analytics live.

### SEO Axis

| Role | Agent | Responsibility |
|------|-------|----------------|
| Lead | **Growth** | Technical SEO + content SEO + GEO + SMO four pillars |
| Perf coupling | **Bolt** | Core Web Vitals (LCP/INP/CLS all Green), image / font / JS budgets |
| Schema authority | **Growth** | `Organization`, `WebSite`, `WebPage`, schema choice per LP type (Product / Event / SoftwareApplication / FAQPage etc.) |
| Heading craft | **Funnel + Prose** | H1/H2/H3 tree that serves SEO + Brand voice + a11y simultaneously |
| Multi-locale | **Polyglot** | hreflang, locale routing, schema per locale |

Pattern: Growth audits + applies → Bolt enforces perf → Funnel + Prose author heading tree → Polyglot localizes. `bazaar` enforces Technical SEO checklist 100%, Lighthouse SEO ≥ 95, GEO Rubric ≥ 15/20.

### IA Axis

| Role | Agent | Responsibility |
|------|-------|----------------|
| Lead | **Funnel** | Visual hierarchy, scan-pattern choice (F/Z/Layer-cake/Centered/Card-grid), section sequence, content chunking |
| Heading craft | **Prose** | H tree as meaningful claims (not labels), microcopy IA |
| Cognitive validation | **Echo** | Persona walk through scan pattern; emotional friction score |
| Journey viz | **Canvas** | Journey map, emotion-score chart, scroll-arc diagram |
| Navigation design | **Funnel + Palette** | Sticky CTA, anchor TOC, mobile bottom-bar |

Pattern: Funnel designs structure → Prose writes headings as claims → Echo walks through with persona → Canvas visualizes journey → `bazaar` scores IA Rubric ≥ 15/20 at STRUCTURE gate.

### Axis Coordination

`bazaar` runs a coherence audit at each major gate:

- **STRATEGY exit**: Brand System record locked, CVR target locked. Brand precedes tokens.
- **STRUCTURE exit**: IA rubric ≥ 15/20. Headings serve all 4 readers (human / Google / LLM / screen reader).
- **DESIGN exit**: Design + Motion + Brand rubrics all pass. Motion story matches archetype.
- **OPTIMIZE exit**: SEO + GEO + Marketing axes all pass. Perf + motion + a11y stayed coherent.
- **VERIFY exit**: Three-Channel Brand Coherence Audit (visual / voice / experience) passes. No axis regressed since DESIGN.
