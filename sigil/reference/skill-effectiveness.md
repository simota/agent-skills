# Skill Effectiveness Tracking (ATTUNE)

Purpose: load this after `VERIFY` to record quality signals, calibrate discovery safely, and persist reusable skill-generation patterns.

## Contents

1. Observe
2. Measure
3. Adapt
4. Persist
5. Evolution feedback

## ATTUNE Loop

```text
OBSERVE -> MEASURE -> ADAPT -> PERSIST
```

Use ATTUNE after every completed batch. Do not skip it for large or high-impact runs.

## OBSERVE

Record the batch:

```yaml
Batch: [project-name]-[date]
Project_Type: [web-app | api | cli | library | monorepo | full-stack]
Tech_Stack: [framework/language]
Skills_Generated: [count]
Quality_Scores:
  - name: [skill-name]
    type: [Micro | Full]
    score: [0-12]
    dimensions: [Format/Relevance/Completeness/Actionability]
    category: [workflow | convention | pattern | integration]
Existing_Skills_Found: [count]
Style_Profile_Applied: [yes | no]
Evolution_Opportunities: [count]
```

### Usage Signals

| Signal | Detection | Interpretation |
|--------|-----------|----------------|
| Skill file unchanged | file modification time | low usage or already sufficient |
| Skill file manually modified | diff against generated version | user adaptation; learn from it |
| Skill referenced in `CLAUDE.md` | content search | adoption signal |
| New files match the skill pattern | directory scan | behavior is being followed |
| Skill deleted | missing from directory | likely low value; investigate |
| Sync drift appears | directory comparison | one copy evolved, one copy stale |

## MEASURE

Track:

- average quality score
- pass rate at `9+`
- recraft rate
- dominant skill category
- strongest and weakest rubric dimensions

### Cross-Project Calibration Table

| Project type | Likely high-value skills | Likely low-value skills |
|--------------|--------------------------|-------------------------|
| Next.js App Router | `new-page`, `new-component`, `data-fetching` | overly generic `env-setup` |
| Express / Fastify | `new-route`, `new-middleware`, `error-handling` | obvious `naming-rules` |
| Go stdlib | `new-handler`, `testing-pattern` | trivial middleware helpers |
| FastAPI | `new-router`, `crud-pattern` | trivial schemas |
| Monorepo | `deploy-flow`, `pr-template` | package skills with unclear scope |

## ADAPT

### Priority Weight Calibration

Base ranking:

```text
Priority = Frequency × Complexity × Risk × Onboarding
```

Rules:
1. Require `3+` data points before adjusting weights.
2. Limit each adjustment to `±0.3` per batch.
3. Decay adjustments `10%` per month toward defaults.
4. Explicit user priority overrides calibration.

### Rationale for Calibration Constants

The three numerical guardrails (3-point minimum, ±0.3 per-batch cap, 10%/month decay) are deliberately conservative. They derive from the following constraints — when these change, revisit the constants and journal the update.

| Constant | Origin | Why this value |
|----------|--------|----------------|
| `3+` data points minimum | Standard small-sample statistical guard | One or two batches can be project-idiosyncratic; three is the smallest sample where a directional signal is more likely than noise. Higher minima (e.g., 5+) slow adaptation too much for project-local skills. |
| `±0.3` per-batch cap | Bounded gradient analogue | Caps single-batch influence so a single anomalous project cannot flip the ranking. Aligned with reinforcement-learning trust-region intuition (limit step size relative to the parameter's natural scale of ~1.0). |
| `10%/month` decay | Exponential half-life ≈ 6.6 months | Forces weights to re-earn their position over a quarter+; prevents stale calibration from a long-past stack (e.g., abandoned framework) keeping outsized influence. Half-life chosen so a quarterly review cycle naturally revalidates active learnings. |
| `< 50%` activation flag | Anthropic skill-creator guidance | Per Anthropic skill-creator 2.0 (60/40 train/test split), descriptions with held-out activation under 50% are typically misclassified — flag for description refinement rather than weight change. See [`reference/official-skill-guide.md`](official-skill-guide.md) for the train/test methodology. |

**Self-modification guard**: ATTUNE **cannot** modify these constants or its own pass thresholds (`9+/12`, `6-8`, `0-5`). Doing so would be reward hacking — the calibration system rewriting its own evaluator. If the constants appear to be wrong, surface that as an `EVOLUTION_SIGNAL` to Lore and let a human review the change. See [`reference/meta-prompting-self-improvement.md`](meta-prompting-self-improvement.md) for the immutable-evaluator rule.

**Cross-reference**: when a reusable pattern emerges (`reusable: true` in ATTUNE output), forward to Lore for baseline propagation across projects. Lore maintains the cross-project performance baselines that justify per-project deviations from defaults.

### Template Calibration

Track which template shape scores better in each context:

| Context | Usually stronger |
|---------|------------------|
| Next.js + Tailwind | conditional CSS branches |
| API projects | inline validation patterns |
| Monorepos | package-scoped skills |
| strict TypeScript | fully typed templates |

## PERSIST

Write ATTUNE output to `.agents/sigil.md`:

```markdown
## YYYY-MM-DD - ATTUNE: [Project Type]

**Batch size**: N skills
**Avg quality**: X.X/12
**Key insight**: [description]
**Calibration adjustment**: [weight: old -> new]
**Apply when**: [future scenario]
**reusable**: true

<!-- EVOLUTION_SIGNAL
type: PATTERN
source: Sigil
date: YYYY-MM-DD
summary: [skill generation insight]
affects: [Sigil, relevant agents]
priority: MEDIUM
reusable: true
-->
```

### Quick ATTUNE

Use this for batches with fewer than `3` skills:

```markdown
## Quick ATTUNE

**Skills**: [count]
**Avg quality**: [score]/12
**Note**: [brief observation]
**Action**: No weight change
```

Do not change ranking weights from a single small batch.

## Evolution Feedback

ATTUNE affects evolution decisions:

| Signal | Meaning |
|--------|---------|
| Quality improving | current generation strategy is working |
| Quality degrading | re-check `SCAN` accuracy and convention detection |
| A category stays weak | catalog or template gap exists |
| Users keep editing skills | learn from the edits and update templates |
| Skills keep getting deleted | ranking or scope is wrong |

When a pattern is reusable beyond one project:

1. Record it with `reusable: true`.
2. Emit `EVOLUTION_SIGNAL`.
3. Inform `Lore` for propagation.
4. Update local discovery heuristics and, if needed, `skill-catalog.md`.
