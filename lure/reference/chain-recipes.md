# Chain Recipes

LP-type-aware recipes that compose the existing agent roster into a contracted, stage-gated pipeline. Each recipe is a minimum viable stage subset for a specific LP class — not a budget slider.

---

## Recipe Selection Decision Tree

```
Brief intake
├── Highest-stakes new product / primary acquisition surface?
│   └── premium (full 9-stage chain)
├── B2B form-driven conversion (demo, contact, qualified lead)?
│   └── lead-gen
├── Free trial / freemium signup with onboarding downstream?
│   └── saas
├── Single product or limited collection page in an existing brand?
│   └── ecom
├── Time-boxed campaign (webinar, launch event, conference)?
│   └── event
├── Whitepaper / ebook / template / checklist download?
│   └── magnet
└── Existing LP, single concern (perf / SEO / a11y / copy)?
    └── Route out (not lure) — call bolt / growth / palette / prose directly
```

Choose ONE recipe. Recipe choice is locked at the RECIPE phase and logged to `.agents/lure/{project}.json`.

---

## Recipe 1: `premium` — Premium Custom LP (default)

**Use when**: New product launch, primary acquisition surface, top 1–3 LPs by revenue contribution, brand-defining page, or any request where the user says "best/highest-quality LP".

**Stage Coverage**: all 9 stages, no skips.

| Stage | Primary Delegates | Parallel Tracks | Time Hint |
|-------|------------------|-----------------|-----------|
| DISCOVER | Researcher, Compete, Voice | yes (3 parallel) | M |
| AUDIENCE | Cast, Echo, Plea | yes (Cast first, then Echo+Plea parallel) | M |
| STRATEGY | Pulse, Magi | serial (Pulse → Magi) | S |
| STRUCTURE | Funnel, Prose, Saga | serial (Funnel → Prose ↔ Saga) | M |
| DESIGN | Vision → Muse → Palette → Frame → Ink/Sketch | mixed (or delegate whole bundle to Atelier) | L |
| BUILD | Forge → Pixel → Artisan → Flow → Polyglot | serial with Polyglot parallelizable | L |
| OPTIMIZE | Growth, Bolt, Experiment | yes (Growth + Bolt parallel, then Experiment) | M |
| VERIFY | Judge, Voyager, Attest, Sentinel, Echo | yes (all 5 parallel, cap at 5) | M |
| LAUNCH | Launch, Guardian, Beacon | serial (Launch → Guardian → Beacon) | S |

**Skip rules**: none. If a stage is genuinely irrelevant (e.g., monolingual LP → no Polyglot), the delegate is skipped *within* the stage, but the stage gate still runs.

**Quality bar**: Lighthouse all ≥ 90, CWV all Green, WCAG 2.2 AA, GEO ≥ 90, Judge no P1/P2, first A/B variant queued.

---

## Recipe 2: `lead-gen` — Lead-Gen LP

**Use when**: B2B demo request, contact form, qualified lead capture, sales-assisted funnel.

**Stage Coverage**: all 9, with Discover compressed.

| Stage | Adjustments vs `premium` |
|-------|--------------------------|
| DISCOVER | Compete only (skip Researcher unless new market); Voice if existing customers |
| AUDIENCE | Cast (single ICP persona) + Plea; skip Echo unless complex form |
| STRATEGY | Pulse heavy (funnel events, MQL → SQL → CW), Magi for objection-handling decision |
| STRUCTURE | Funnel + Prose; Saga only if testimonial-driven |
| DESIGN | Direct delegation (Vision → Muse → Palette → Frame); skip Atelier for single-page |
| BUILD | Forge → Artisan → Flow; skip Pixel unless mockup-driven, skip Polyglot if EN-only |
| OPTIMIZE | Growth (heavy on form-field reduction CRO), Bolt, Experiment (variant on form length) |
| VERIFY | Judge, Voyager (form submission flow), Attest, Sentinel (form input validation), Echo (re-walk) |
| LAUNCH | Launch + Guardian + Beacon (lead-event tracking) |

**Skip rules**: Researcher skip when product/market is established. Pixel skip when no high-fidelity mockup exists.

**Conversion focus**: form completion rate, qualified lead %, time-to-MQL.

---

## Recipe 3: `saas` — SaaS Signup LP

**Use when**: Free trial / freemium signup with product-led downstream onboarding.

**Stage Coverage**: 9 stages, Optimize stage extended.

| Stage | Adjustments vs `premium` |
|-------|--------------------------|
| DISCOVER | Compete (feature matrix), Voice (churn reasons); Researcher light |
| AUDIENCE | Cast (ICP + power-user persona), Echo (pricing-page cognitive walkthrough), Plea |
| STRATEGY | Pulse (activation events, North-Star = WAU/PMF metric), Magi (free vs trial vs freemium) |
| STRUCTURE | Funnel (above-fold = product screenshot + signup CTA), Prose (feature copy) |
| DESIGN | Vision → Muse → Frame (design system reuse); avoid bespoke unless brand-defining |
| BUILD | Forge → Artisan → Flow (signup interaction); Polyglot if multi-region |
| OPTIMIZE | Growth (SEO for category terms, GEO for AI search), Bolt (sub-2s LCP), Experiment (3+ variants) |
| VERIFY | Judge, Voyager (signup happy-path + edge cases), Attest, Sentinel (auth flow), Echo |
| LAUNCH | Launch + Guardian + Beacon (signup event + activation event) |

**Skip rules**: Saga skip (SaaS LPs rarely benefit from narrative arc — feature + proof + CTA dominates).

**Conversion focus**: signup CVR + activation rate downstream (not just signup).

---

## Recipe 4: `ecom` — E-commerce Product LP

**Use when**: Single product, limited collection, DTC product launch.

**Stage Coverage**: 8 stages (skip Discover if brand is established).

| Stage | Adjustments vs `premium` |
|-------|--------------------------|
| DISCOVER | Skip if existing brand; run Compete only if competitive category |
| AUDIENCE | Cast (purchase-intent persona), Plea (unmet need = differentiation), Echo (cart-abandonment walk) |
| STRATEGY | Pulse (AOV, CVR, return rate), Magi (price-anchoring decision) |
| STRUCTURE | Funnel (hero image + benefit + trust + reviews + FAQ + sticky CTA), Prose (product copy) |
| DESIGN | Vision → Muse → Frame; Ink/Sketch heavy (product photography, lifestyle assets) |
| BUILD | Forge → Pixel (photo fidelity) → Artisan → Flow (image gallery, variant selector); Polyglot for multi-region |
| OPTIMIZE | Growth (product-schema JSON-LD, GEO for shopping AI), Bolt (image perf budget), Experiment (variant on price display, urgency) |
| VERIFY | Judge, Voyager (add-to-cart + checkout entry flow), Attest, Sentinel, Echo |
| LAUNCH | Launch + Guardian + Beacon (add-to-cart, purchase event) |

**Skip rules**: Saga skip unless storytelling-driven brand (e.g., heritage / craft). Researcher skip for established brand.

**Conversion focus**: add-to-cart CVR, checkout entry CVR, AOV.

---

## Recipe 5: `event` — Event / Campaign LP

**Use when**: Webinar registration, product launch event, conference, time-boxed campaign.

**Stage Coverage**: 8 stages — Discover skipped (event context = brief), Audience compressed, Verify lightweight.

| Stage | Adjustments vs `premium` |
|-------|--------------------------|
| DISCOVER | Skip (event context is the brief) |
| AUDIENCE | Cast (attendee persona); skip Echo unless complex form |
| STRATEGY | Pulse (registration → attendance → conversion), Magi for date/urgency framing |
| STRUCTURE | Funnel (above-fold = date + speakers + register CTA), Prose, Saga (speaker authority + agenda narrative) |
| DESIGN | Reuse brand tokens (Muse + Frame); minimal Vision unless brand-defining event |
| BUILD | Forge → Artisan → Flow (countdown, scarcity); skip Polyglot if single-region |
| OPTIMIZE | Growth (event schema, social share OGP), Bolt; skip Experiment if single-shot |
| VERIFY | Judge, Voyager (registration flow), Sentinel (form), Echo light |
| LAUNCH | Launch + Guardian + Beacon (registration + reminder funnel) |

**Skip rules**: Discover skip (event scope = brief). Experiment skip for single-shot campaigns.

**Conversion focus**: registration CVR + attendance rate.

---

## Recipe 6: `magnet` — Lead Magnet LP

**Use when**: Whitepaper / ebook / template / checklist / free-resource download.

**Stage Coverage**: 8 stages — Discover skipped (magnet context = brief), Audience compressed, design lightweight.

| Stage | Adjustments vs `premium` |
|-------|--------------------------|
| DISCOVER | Skip (magnet context is the brief) |
| AUDIENCE | Cast (download-intent persona); skip Echo, Plea |
| STRATEGY | Pulse (download → email engagement → MQL); skip Magi unless strategic positioning |
| STRUCTURE | Funnel (above-fold = title + cover + email form), Prose; skip Saga |
| DESIGN | Reuse brand tokens (Muse only); minimal Vision; Ink/Sketch for cover image only |
| BUILD | Forge → Artisan; skip Pixel, Flow (motion), Polyglot |
| OPTIMIZE | Growth (organic + GEO citation pickup), Bolt; skip Experiment for first launch |
| VERIFY | Judge, Voyager (form submission + email confirmation), Sentinel (email validation) |
| LAUNCH | Launch + Beacon (download event + email-engagement tracking) |

**Skip rules**: Most aggressive skip set. Magnet LPs win on copy clarity + low friction, not on production polish.

**Conversion focus**: download CVR (20–30% baseline), follow-up email open rate.

---

## Time and Quality Trade-offs

| Recipe | Approx. Pipeline Depth | Quality Ceiling |
|--------|------------------------|-----------------|
| `premium` | Deepest (all 9 stages, full fan-out) | Highest — top-of-funnel brand-defining LP |
| `lead-gen` | Deep (9 stages, compressed Discover) | High — B2B sales conversion |
| `saas` | Deep (9 stages, extended Optimize) | High — product-led growth |
| `ecom` | Medium-deep (8 stages, skip Discover often) | High — DTC product CVR |
| `event` | Medium (8 stages, Discover skipped) | Medium-high — time-boxed campaign |
| `magnet` | Shallow (8 stages, Discover skipped + aggressive compression) | Medium — friction-minimized download |

Recipe is not "budget tier" — it is "LP-type-appropriate depth." A `magnet` recipe done well is higher quality than a `premium` recipe applied to a lead-magnet brief.

---

## Recipe Switching

A recipe is locked at RECIPE phase. If mid-pipeline the brief turns out to be a different LP class:

1. Stop current stage.
2. Snapshot state to `.agents/lure/{project}.json`.
3. Ask user to confirm recipe switch.
4. Resume from the latest equivalent stage in the new recipe (don't restart).
