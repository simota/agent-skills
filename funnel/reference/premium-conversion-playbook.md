# Premium Conversion Decisions

Read during STRATEGY/STRUCTURE when selecting a conversion target and LP copy framework. Funnel/Prose/Growth own the craft; this reference sets handoff decisions, not canned page copy.

## CVR target contract

- Define numerator, denominator, attribution window, event identity and deduplication before choosing a target. A recovery-clicker conversion rate is not a cart-abandoner recovery rate; a pricing next-step click is not a purchase.
- Prefer the client's measured baseline with cohort, traffic source (`warm|cold|mixed`), period, sample size and uncertainty. Do not pool cold and warm traffic or unmatched LP objectives.
- External median/quartile/decile inputs require an actual source/date, comparable event definition and matching traffic/recipe. Otherwise return `unavailable`, not an invented industry value. No default `median × 1.5` uplift.
- Lock the justified target in `PREMIUM_LP_STAGE_BUNDLE.CVR_Target`; preserve baseline/target provenance. A target is a hypothesis, not a promised outcome. Experiment owns testing; Pulse owns the measurement definition; Growth implements the tracking/CRO handoff.
- Carry the target and instrumentation through STRUCTURE → BUILD → OPTIMIZE → LAUNCH. Validate after authorized release against the same denominator; report insufficient data rather than inferred improvement.

## Recipe-specific framework defaults

Choose one coherent framework; a logged strategy decision may override the default. `premium` requires the recipe's strategy arbitration, not an invented universal conversion table.

| Recipe | Default |
|---|---|
| `premium` | Strategy/Magi arbitration; no preset |
| `lead-gen` | PAS |
| `saas` free trial | JTBD-first |
| `saas` demo request | PAS or StoryBrand SB7; resolve against the brief |
| `ecom` | AIDA with substantiated proof |
| `event` | 4Ps |
| `magnet` | 4Ps with low-friction action |

Framework definitions, generic CTA examples and industry page outlines need not be cached here. Existing focused references own copy, form and trust mechanics.

## Repair routing

| Evidence | Next action |
|---|---|
| Two unrelated promises across hero/body | Stop progression; return to UNDERSTAND and lock one promise. A second promise needs a separately scoped LP. |
| Hero-Contract Legibility ≤1/3 | Return to STRUCTURE; make the promised outcome and action legible. |
| Trust-Signal Density ≤1/4 | Address substantiated proof in the brand/trust gate, not fabricated testimonials or badges. |
| CTA clicks without completed forms | Inspect event integrity and form friction before changing the promise. |
| Conversion rises but lead quality/refunds/churn worsen | Preserve guardrails; tighten qualification and truthful expectations rather than celebrating raw CVR. |
| Mobile breakage, inaccessible controls or deceptive urgency | Repair through the responsible implementation/accessibility owner; conversion never waives a blocking quality gate. |

Use `reference/premium-craft-standards.md` and `reference/premium-quality-gates.md` for the authoritative rubrics and exit rules; do not retune thresholds here.
