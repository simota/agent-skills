# Funnel Recipe Registry

The full Recipe table for `funnel`. `funnel/SKILL.md` carries only the dispatch
allowlist; this file holds what is needed to *execute* a Recipe — activation
condition and the files to read first.

**Read this when** a subcommand matched and you need its row, or when scanning
what Recipes exist at all.

---

| Recipe | Subcommand | Default? | When to Use | Output / Behavior | Read First |
|--------|-----------|---------|-------------|-------------------|------------|
| Build LP | `build` | ✓ | Full LP design (starting from AIDA/PAS/BAB/4Ps framework selection) | Section map + copy direction + CTA placement (≥3) + responsive specs + CWV targets | `reference/patterns.md` |
| CTA Optimization | `cta` | | CTA placement, copy, micro-copy optimization | CTA placement plan + button copy variants + constraints (size, contrast, microcopy) | — |
| Conversion Audit | `conversion` | | Conversion improvement and section audit for an existing LP | Audit findings + section-level improvement plan + prioritized fix list | `reference/patterns.md` |
| Responsive Design | `responsive` |  | Mobile-first implementation, tap targets, viewport optimization | Responsive section spec + breakpoint plan + tap-target / viewport rules | — |
| Form Optimization | `form` | | Field minimization, progressive disclosure, autofill cooperation, validation, submit friction | Form spec — field-count cost model, single vs multi-step, `autocomplete`/`inputmode` contract, blur-time validation, submit state machine. Delegates: Artisan (impl), Prose (labels/errors), Growth (A/B), Muse (tokens) | `reference/form-lp-optimization.md` |
| Copy Authoring | `copy` | | Headline formulas, hero body, value-prop clarity, microcopy shells, readability, tone | LP copy — PAS/BAB/4U formulas, hero anatomy, clarity tests, benefit-vs-feature, microcopy shells, readability targets. Delegates: Prose (exact microcopy + voice), Growth (ads/nurture), Muse (type tokens), Vision (positioning) | `reference/copy-lp-authoring.md` |
| Trust Signal Placement | `trust` | | Testimonials, logo bars, case studies, badges, review aggregation, urgency vs dark patterns | Placement map — testimonial shape/quantity, logo bar treatment, metric- vs story-forward cases, certifications, review aggregation, honest-urgency red lines. Delegates: Prose (wording), Growth (review APIs + schema), Muse (tokens), Canon (FTC substantiation) | `reference/trust-signal-placement.md` |
| Premium LP Studio | `premium` | | Standard-to-premium full LP pipeline; select `premium|lead-gen|saas|ecom|event|magnet` mode | Nine gated stages + six-axis craft rubric + specialist handoff bundle | `reference/premium-chain-recipes.md`, `reference/premium-quality-gates.md` |
