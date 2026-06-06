# Fishbone (Ishikawa) 6M Reference

Purpose: Apply Kaoru Ishikawa's cause-and-effect (fishbone) diagram with the 6M framework — Machine, Method, Material, Measurement, Mother-nature, Manpower. Best when multiple contributing factors interact to produce a failure. Unlike 5 Whys (linear), fishbone is categorical and multi-branched.

## Scope Boundary

- **scout `fishbone`**: Multi-factor categorical RCA (this document).
- **scout `5whys` (elsewhere)**: Linear single-chain RCA.
- **scout `timeline` (elsewhere)**: Temporal sequence reconstruction.
- **omen (elsewhere)**: Pre-failure fishbone (prevention) — scout's fishbone is post-failure.
- **Triage (elsewhere)**: Incident response embedding fishbone.

## Diagram

```
                              ┌─── Machine ──────┐    ┌─── Method ───────┐
                              │  • aging disk    │    │  • no idempotency │
                              │  • CPU spike     │    │  • missing retry  │
                              └────┐             │    │                   │
                                   │             │    │                   │
  PROBLEM ◀────────────────────────────────────────────── [Effect]
                                   │             │    │                   │
                              ┌────┘             │    │                   │
                              │  • corrupt input │    │  • noisy alerts   │
                              │  • schema drift  │    │  • slow dashboard │
                              └─── Material ─────┘    └─── Measurement ──┘
                              ┌─── Mother-nature ─┐   ┌─── Manpower ─────┐
                              │  • cloud outage   │   │  • no training   │
                              │  • DNS provider   │   │  • on-call thin  │
                              └───────────────────┘   └──────────────────┘
```

## The 6M Categories

| Category | Scope | Typical causes |
|----------|-------|----------------|
| **Machine** | Hardware, infra, platforms | aging hardware, CPU/mem/disk saturation, cloud provider region issues |
| **Method** | Process, procedure, code | missing idempotency, wrong retry, missing validation, undocumented procedure |
| **Material** | Input data, dependencies | corrupt data, schema drift, bad library version, untrusted third-party |
| **Measurement** | Observability, alerts, monitoring | missing metric, noisy alerts, slow dashboard, wrong threshold |
| **Mother-nature** | External / environmental | cloud outage, DNS provider, regulatory change, time-of-day load |
| **Manpower** | People, skill, org | insufficient training, on-call thin, knowledge in single head, hand-off gap |

### Variants

- **8M (Manufacturing)**: add Measurement-tool, Management
- **5M+E (Quality)**: drop Measurement, add Environment (like Mother-nature)
- **4P (Services)**: People, Process, Policy, Procedure
- **6M is the software-ops standard.**

## When Fishbone Beats 5 Whys

| Scenario | Choose |
|----------|--------|
| Single causal chain | 5 Whys |
| Multiple interacting factors | Fishbone |
| Novel / unclear failure | Fishbone (to map the space) |
| Known recurring failure | 5 Whys (drill to systemic) |
| Pre-mortem (brainstorm before failure) | Fishbone — via omen |
| Post-mortem with clear sequence | 5 Whys + Timeline |

Sometimes both: fishbone maps the factor space, then 5 Whys drills the most-weighted branch.

## Workflow

```
EFFECT      →  state the problem factually at the head of the fish
            →  1 sentence, no cause hints

BRAINSTORM  →  for each M, list possible causes
            →  don't filter; quantity now, quality next

DRILL       →  for each listed cause, ask 1-2 whys if applicable
            →  mark sub-branches on the bone

WEIGHT      →  per cause, score probability + impact (e.g., 1-5)
            →  mark top 3-5 causes for follow-up

EVIDENCE    →  for each weighted cause, collect evidence
            →  promote to "confirmed" / "ruled out" / "uncertain"

CONVERGE    →  identify primary cause + contributing factors
            →  often primary × contributing = compound failure

RECOMMEND   →  fix primary cause
            →  address 1-2 contributors if high weight
            →  detection upgrade at each weighted branch

HANDOFF     →  Builder: implement fixes
            →  Triage: feed into post-mortem
            →  Lore: pattern storage if recurring
```

## Output Template

```markdown
## Fishbone Analysis: [Incident / Bug]

### Effect
[factual problem statement, 1 sentence]

### Fishbone (by 6M)

**Machine**
- [cause 1] (probability × impact = score)
  - sub-cause
- [cause 2] (score)

**Method**
- [cause 1] (score)
- [cause 2] (score)

**Material**
- [cause 1] (score)

**Measurement**
- [cause 1] (score)

**Mother-nature**
- [cause 1] (score)

**Manpower**
- [cause 1] (score)

### Top Weighted Causes
| Rank | Category | Cause | Score | Evidence | Verdict |
|------|----------|-------|-------|----------|---------|
| 1 | Method | [...] | [N] | [...] | confirmed |
| 2 | Measurement | [...] | [N] | [...] | contributing |
| 3 | Machine | [...] | [N] | [...] | ruled out |

### Primary Cause + Contributors
- **Primary**: [category × cause]
- **Contributing**: [category × cause]
- **Compound story**: [how they interacted]

### Recommendations
- **Fix primary**: [change]
- **Fix contributing**: [change]
- **Detection upgrade per weighted branch**: [alert / test / check]

### Handoffs
- Builder: implementation
- Triage: post-mortem section
- Lore: pattern capture if recurring
- Mend: detection upgrade
```

## Anti-Patterns

| Anti-pattern | Fix |
|--------------|-----|
| Listing every possible cause, never weighting | Weight by probability × impact; focus top 3-5 |
| Using only Method/Manpower branches | Force yourself through all 6M; others surface blind spots |
| Brainstorming with answer in mind | Delay convergence; complete all 6 branches first |
| No evidence collection | Each weighted cause needs "confirmed / ruled out" verdict |
| Blaming Manpower without process view | If Manpower is the cause, ask: why does process depend on heroism? |
| Fishbone without follow-through fix | RCA is useless without preventive action |
| Post-hoc rationalization of primary cause | State weighting before investigation, revise after evidence |

## References

- Kaoru Ishikawa — *Guide to Quality Control* (1968, origin of fishbone)
- Kaoru Ishikawa — *What Is Total Quality Control?* (1985)
- ASQ — Cause-and-Effect Diagram standard (Quality Council)
- Juran — *Quality Handbook* (related to Ishikawa methods)
- Peter Scholtes — *The Team Handbook* (facilitation patterns)
- Google SRE Workbook — structured RCA chapter
- AWS Well-Architected — Reliability Pillar (failure-mode analysis)
- Lean Enterprise Institute — A3 problem solving (integrates fishbone + 5 Whys)
