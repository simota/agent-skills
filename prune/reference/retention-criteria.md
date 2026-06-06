# Retention Criteria — 5-Axis Scoring

Score every audited skill on 5 axes, 0-5 each, sum to a 25-point Retention Score that drives the KEEP / MERGE / SUNSET / DEPRECATE verdict.

## Axes

### 1. Usage (0-5)

Activity in `.agents/PROJECT.md` over the last 90 days.

| Score | Threshold |
|-------|-----------|
| 5 | Weekly use (12+ entries / 90 days) |
| 4 | Bi-weekly (6-11) |
| 3 | Monthly (3-5) |
| 2 | Rare (1-2) |
| 1 | One-off in last 90 days |
| 0 | No activity in 90+ days |

### 2. Overlap (0-5, inverted)

Maximum overlap percentage against any other skill, from the overlap matrix.

| Score | Max overlap |
|-------|-------------|
| 5 | < 10% (unique) |
| 4 | 10-19% (clearly differentiated) |
| 3 | 20-29% (acceptable specialization) |
| 2 | 30-49% (merge candidate, evaluate) |
| 1 | 50-69% (strong merge candidate) |
| 0 | ≥ 70% (likely duplicate, sunset or merge mandatory) |

### 3. Uniqueness (0-5)

Number of CAPABILITIES_SUMMARY entries that are NOT covered by any other single skill.

| Score | Unique capabilities |
|-------|---------------------|
| 5 | 5+ unique capabilities |
| 4 | 3-4 |
| 3 | 2 |
| 2 | 1 |
| 1 | 0 unique, but distinct combination of shared capabilities |
| 0 | All capabilities exist in another single skill |

### 4. Coverage (0-5)

Number of `PROJECT_AFFINITY` rows with H or M relevance, plus Pack membership count.

| Score | Coverage breadth |
|-------|------------------|
| 5 | Member of 3+ Packs and high relevance to 3+ project domains |
| 4 | Member of 2 Packs, 2+ project domains |
| 3 | Member of 1-2 Packs, 1-2 project domains |
| 2 | 1 Pack, 1 domain |
| 1 | No Pack but referenced in CLAUDE.md or `_common/` |
| 0 | No Pack membership, no CLAUDE.md / `_common/` reference |

### 5. Maintenance Cost (0-5, inverted)

SKILL.md size, reference count, journal freshness.

| Score | Cost signal |
|-------|-------------|
| 5 | SKILL.md ≤ 5k tokens, 3-5 references, journal updated < 30 days ago |
| 4 | ≤ 7k tokens, ≤ 7 references, journal < 60 days |
| 3 | ≤ 10k tokens, ≤ 10 references |
| 2 | 10-15k tokens, > 10 references OR stale journal (60-180 days) |
| 1 | > 15k tokens OR > 15 references OR very stale (180-365 days) |
| 0 | Unmaintained: > 15k tokens, > 15 references, journal > 365 days |

## Classification Thresholds

Sum the 5 axes (max 25):

| Retention Score | Verdict | Action |
|----------------|---------|--------|
| 20-25 | **KEEP** | No action; healthy skill |
| 15-19 | **KEEP with improvement** | Handoff to Architect IMPROVE recipe |
| 10-14 | **MERGE candidate** | Apply merge protocol (find canonical owner) |
| 5-9 | **SUNSET candidate** | Apply 3-condition gate (see Core Rule 5) before proposing |
| 0-4 | **DEPRECATE** | Immediate sunset proposal; archive within 30 days |

## 3-Condition Sunset Gate

Before proposing SUNSET, **all three** must hold (from Core Rule 5):

1. **6+ months without activity** in `.agents/PROJECT.md` (not 90 days — 90 days is a Usage signal, not a sunset condition)
2. **Clear alternative exists** — another skill covers the unique capabilities
3. **No project depends on it** — zero mentions in `CLAUDE.md`, `_common/*.md`, or any active Pack profile

If any condition fails, downgrade to DEPRECATE-WATCH (note for future audit, no action).

## Protected Skills

Never propose SUNSET or DEPRECATE for:

- `core` Pack members: `nexus`, `sherpa`, `scout`, `builder`, `radar`, `zen`, `guardian`, `compass`, `architect`, `gauge`
- Skills marked mandatory in `_common/SKILL_PACKS.md`
- Skills referenced in repo CLAUDE.md (count as protected even if usage is low)

Score these normally for audit completeness, but apply KEEP regardless of score.
