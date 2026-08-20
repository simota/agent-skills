# Magi Recipe Registry

The full Recipe table for `magi`. `magi/SKILL.md` carries only the dispatch
allowlist; this file holds what is needed to *execute* a Recipe — activation
condition and the files to read first.

**Read this when** a subcommand matched and you need its row, or when scanning
what Recipes exist at all.

---

| Recipe | Subcommand | Default? | When to Use | Read First |
|--------|-----------|---------|-------------|------------|
| Go/No-Go Decision | `decide` | ✓ | Final adoption verdict (release readiness, feature approval, quality gate). KNOWLEDGE task — evidence at FRAME, then independent voting | `reference/decision-domains.md` |
| Tradeoff Analysis | `tradeoff` | | X vs Y comparison. Both options explicit; the three lenses evaluate independently with weighted aggregation | `reference/decision-domains.md` |
| Architecture Arbitration | `arbitrate` | | Design option arbitration (2+ options). Engine Mode auto-detected at low reversibility + high impact | `reference/deliberation-framework.md` |
| Strategic Direction | `strategic` | | Long-term strategy and roadmap. REASONING task — independent voting; Sophia weights long-term impact | `reference/decision-domains.md` |
| Six Thinking Hats | `sixhat` | | Parallel-thinking across White/Red/Black/Yellow/Green/Blue modes before voting; Black always paired with equal-time Yellow | `reference/six-thinking-hats.md` |
| Devil's Advocate | `devil` | | Red-team stress test on high-stakes irreversible proposals; mandatory on `3-0`. Rotated DA, 3-7 ranked objections, addressed/partial/unaddressed scoring | `reference/devils-advocate.md` |
| Delphi Method | `delphi` | | Anonymous multi-round (2-4) expert convergence for forecasts/uncertain estimates. Bimodal kept as stable disagreement, not flattened | `reference/delphi-method.md` |
| Advisory | `advisor` | | Founder family (`office-hours`, `triage`, `pitch`) or named-expert family (`expert`, `conclave`, `critique`, `roster`) | `reference/office-hours-format.md`, `reference/ethics-and-safety.md` |
| Multi-Engine | `multi` | | Multi-engine deliberation — 6-cell dual baseline, 9-cell tri when agy AVAILABLE. Pattern-based verdict preserving cross-viewpoint trade-offs; engine influence capped at 50%; all-cells-unanimous triggers mandatory DA | `reference/tri-engine-deliberate.md`, `_common/MULTI_ENGINE_RECIPE.md` |
| Strategy Simulation | `simulate` |  | Run baseline / optimistic / pessimistic business scenarios | `reference/strategy-simulation/simulation-patterns.md`, `reference/strategy-simulation/scenario-planning-pitfalls.md`, `reference/strategy-simulation/financial-modeling-pitfalls.md` |
