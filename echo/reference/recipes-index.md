# Echo Recipe Registry

The full Recipe table for `echo`. `echo/SKILL.md` carries only the dispatch
allowlist; this file holds what is needed to *execute* a Recipe — activation
condition and the files to read first.

**Read this when** a subcommand matched and you need its row, or when scanning
what Recipes exist at all.

---

| Recipe | Subcommand | Default? | When to Use | Read First |
|--------|-----------|---------|-------------|------------|
| Walkthrough | `walkthrough` | ✓ | Persona cognitive walkthrough, emotion scoring | `reference/process-workflows.md`, `reference/ux-frameworks.md` |
| Confusion Points | `confusion` | | Identify confusion points, cognitive load, mental model gaps | `reference/ux-frameworks.md`, `reference/output-templates.md` |
| Emotion Map | `emotion` | | Emotion map, detailed friction score analysis | `reference/ux-frameworks.md`, `reference/output-templates.md` |
| Persona Switch | `persona` | | Multi-persona comparison, cross-persona analysis | `reference/analysis-frameworks.md`, `reference/cognitive-persona-model.md` |
| Heuristic Evaluation | `heuristic` | | Nielsen 10 / domain-specific heuristic expert review with severity scoring and evaluator-panel reconciliation | `reference/heuristic-evaluation.md` |
| SUS Scoring | `sus` | | System Usability Scale authoring, scoring, and benchmark comparison with percentile / grade / adjective mapping | `reference/sus-scoring.md` |
| Think-Aloud | `aloud` | | Concurrent / retrospective think-aloud session moderation, prompt discipline, transcript coding, and finding extraction | `reference/think-aloud-protocol.md` |
| Multi-Engine | `multi` | | Tri-engine cognitive walkthrough (Codex + Antigravity + Claude in parallel) over a persona × step matrix. Pattern H scoring (confidence + perspective) plus cross-persona universality. Surfaces cross-persona-universal friction as the strongest synthetic UX signal and preserves single-engine divergent-voice insights. | `reference/tri-engine-walkthrough.md`, `_common/SUBAGENT.md`, `_common/MULTI_ENGINE_RECIPE.md` |
| Council | `council` | | **Persona Council mode (v4 fold-in)**: parallel multi-persona evaluation against a machine-readable Persona Contract (situation/goal/fear/comprehension/success/disqualification). Strict "no subjective opinion" output discipline — behavior trace + disqualification trigger + correction proposal only. Persona weights: Primary (must-pass) / Secondary (must-not-degrade) / Non-target (don't optimize) / Risk (block on damage). Required for `nexus growth-acceptance` Phase 0 persona evaluation. Cost-capped per Org Tier (Solo: skip, SMB: max 3 personas, Enterprise: max 9). | (inline below) + `reference/cognitive-persona-model.md` |
| Synthetic Demand | `demand` | | Feature request, unmet need, challenge, roleplay, JTBD, 5 Whys, Opportunity Tree, or multi-engine demand; select `request|need|challenge|roleplay|jtbd|5whys|opportunity|multi` mode | `reference/demand-subcommand-behavior.md`, matching `reference/demand-*.md` |
