# Overlap Matrix — Cross-Skill Responsibility Calculation

Method for computing pairwise overlap % used by the Overlap axis (`retention-criteria.md` axis 2) and merge candidate detection.

## Inputs (per skill)

1. **CAPABILITIES_SUMMARY entries** — bulleted capabilities at top of SKILL.md HTML comment.
2. **description** — frontmatter description field (especially "Use when" + "Not for" clauses).
3. **Recipes table** — Recipe entries indicate scope boundary.
4. **Trigger Guidance** — "Use X when" + "Route elsewhere when" sections.

## Calculation

### Step 1: Tokenize capabilities

Normalize each CAPABILITIES_SUMMARY entry to a (verb, object, qualifier) triple:

```
- frontend_perf_optimization: "Frontend (re-render reduction, memoization, lazy loading)"
  → (optimize, frontend-perf, react)

- backend_perf_optimization: "Backend (N+1 fix, indexing, caching, async)"
  → (optimize, backend-perf, db)
```

### Step 2: Pairwise capability matching

For skills A and B, compute:

```
shared_capabilities = |A ∩ B|  (capabilities semantically equivalent in both)
unique_to_A = |A| - shared
unique_to_B = |B| - shared

overlap_pct = shared_capabilities / max(|A|, |B|)
```

Use semantic equivalence, not string match. Examples of equivalents:
- `bug_investigation` ≡ `root_cause_analysis`
- `e2e_test_authoring` ≡ `end_to_end_browser_testing`
- `markdown_format_conversion` ≡ `document_format_export`

### Step 3: Refine with explicit boundaries

Subtract overlap when both skills' descriptions explicitly differentiate via "Not for X (→ <other skill>)" clauses. Each explicit mutual exclusion reduces overlap by 5 percentage points (max 20pp reduction).

Example:
- Bolt + Tuner share "performance optimization" capability (raw overlap 40%).
- Bolt: "Don't use for DB query plan (Tuner)"
- Tuner: "Don't use for app rewrites (Builder)" + "schema (Schema)"
- Mutual exclusion present → −5pp → effective overlap 35%.

## Overlap Bands

| Overlap % | Verdict | Action |
|-----------|---------|--------|
| 0-9% | Unique | Skill axis score 5 |
| 10-19% | Differentiated | Score 4; healthy specialization |
| 20-29% | Acceptable | Score 3; note but no action |
| 30-49% | Review | Score 2; **merge candidate**, investigate canonical owner |
| 50-69% | Strong merge | Score 1; merge proposal mandatory |
| 70%+ | Duplicate | Score 0; sunset or absorb mandatory |

## Output Format

For the audit report, produce a triangular matrix of skills with overlap ≥ 30% only (skip lower bands to keep the matrix readable):

```
              architect  darwin  void   sweep   gauge   prune
architect       —         25%     15%   12%     20%     15%
darwin                    —       18%   8%      18%     25%
void                              —     12%     10%     20%
sweep                                   —       8%      10%
gauge                                            —      10%
prune                                                   —
```

## Cross-Pack vs Same-Pack Overlap

Same-Pack overlap is more concerning than cross-Pack (same Pack = same domain context, so users expect specialization).

Multiply overlap % by 1.2 when both skills share at least one Pack membership. Subtract 0.1 from the axis 2 score for any cross-Pack overlap ≥ 30% (cross-Pack is often justified specialization).

## Always

- Compute pairwise overlap for the full audit scope; never select pairs heuristically.
- Use semantic equivalence, not string match — `e2e_test` and `end_to_end_browser_test` are the same capability.
- Apply Pack-membership multiplier before classification.

## Never

- Propose merge from overlap alone — combine with Usage (axis 1) and Coverage (axis 4) to choose canonical owner.
- Skip the explicit-boundary refinement; mutual-exclusion clauses are intentional design and must reduce raw overlap.
