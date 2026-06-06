# Large-Scale & AI-Assisted Dead Code Cleanup

Purpose: patterns for monorepos, enterprise-scale cleanup, and cautious AI-assisted candidate expansion.

## Contents

1. Meta SCARF lessons
2. AI-assisted detection
3. Monorepo rules
4. Enterprise workflow

## Meta SCARF Lessons

What scales well:
- combine static analysis, runtime signals, and text search
- analyze at symbol level when tooling allows it
- generate human-reviewable change requests
- keep human review for risky or low-confidence cases

Key lesson: static analysis alone is insufficient for dynamic systems.

## AI-Assisted Detection

Use AI only to expand the candidate list or explain why a candidate may be dead.

Rules:
- AI suggestions increase evidence, not authority
- final deletion still requires confidence scoring and human review
- dynamic references, reflection, plugin systems, and business rules remain high-risk

Treat AI evidence as part of `Tool Agreement`, not a replacement for verification.

## Monorepo Rules

- Use workspace-aware tooling such as `npx knip --workspace`
- Prefer incremental scans against changed packages
- Check cross-package exports before deletion
- Require extra review when cleanup crosses package boundaries
- Route ownership-sensitive changes using package owners or `CODEOWNERS`

## Enterprise Workflow

1. Measure overall dead-code health and hotspots.
2. Build automated detection into CI and periodic scans.
3. Use confidence thresholds:
   - `>=90`: batch proposal
   - `70-89`: individual review
   - `<70`: hold for manual review
4. Track regressions, false positives, and cleanup velocity.
