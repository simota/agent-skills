# Meta-Prompting & Self-Improvement Patterns

Purpose: load this when improving Sigil itself, not during ordinary skill generation. It captures optional self-improvement techniques for ATTUNE, validation, and future evolution.

## Contents

1. Prompt optimization
2. Self-correction patterns
3. Context engineering
4. Automatic rule generation
5. Feedback loop design
6. Incremental roadmap

## Prompt Optimization

### DSPy-Style Optimization

Use a closed loop:

```text
prompt -> run -> evaluate -> refine prompt -> run again
```

Potential Sigil uses:
- improve `description` routing quality
- compare template variants
- refine discovery heuristics from outcomes

### TextGrad-Style Optimization

Treat review feedback as a natural-language gradient:

```text
initial prompt -> output -> critique -> updated prompt
```

Use this only when repeated critique clearly improves results.

## Self-Correction Patterns

### Mistake Ledger

Track recurring failures in a structured log:

```markdown
## Mistake Ledger

| Date | Failure Pattern | Cause | Fix | Prevention Rule |
|------|-----------------|-------|-----|-----------------|
| YYYY-MM | missing tests | VERIFY skipped | add test check | F-test-required |
```

Use it to avoid repeating the same generation defects.

### Reflection Loop

```text
Generate -> Self-Review -> Identify Issues -> Regenerate
```

Options:

| Variant | Cost | Use |
|---------|------|-----|
| Self-Refine | low | default internal review |
| Cross-Model | medium | only when another reviewer is available |
| Multi-Agent | high | use for high-stakes quality loops |

### Constitutional Guardrails

Keep a compact rule set for self-review:

1. Skills MUST mirror project conventions.
2. Skills MUST NOT introduce security risk.
3. Skills SHOULD stay easy to load and selective to read.

## Context Engineering

### Spec-First Pattern

```text
spec -> local rules -> generation -> review -> feedback
```

Use this when the skill itself is complex or safety-sensitive.

### Context Budget

| Context window | Suggested allocation |
|----------------|----------------------|
| `~200K` tokens | rules `5-10K`, code `150-180K`, output `10-40K` |
| `~1M` tokens | rules `10-20K`, code `800-900K`, output `80-100K` |

If a generated skill requires too much inline context, split or externalize detail into `reference/`.

## Automatic Rule Generation

Useful source flows:

1. existing code -> convention extraction -> skill or `CLAUDE.md`
2. CI failures -> recurring failure pattern -> preventive skill
3. PR review comments -> repeated feedback -> new project rule

## Feedback Loop Design

Three levels:

1. structural quality -> automatic validation
2. semantic quality -> self-review or external review
3. practical quality -> ATTUNE over time

Map these back to Sigil:
- structural quality -> `validation-rules.md`
- semantic quality -> recraft / review loop
- practical quality -> `skill-effectiveness.md`

## Incremental Roadmap

1. Add Mistake Ledger to the journal.
2. Run Self-Refine inside `VERIFY` for weak drafts.
3. Track weak `description` activation and propose rewrites.
4. Measure context cost and recommend skill splitting when needed.
