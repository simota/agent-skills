# Code Evolution Tracing

Reference for Lens's `evolution` recipe. Track file lifespan, author concentration (bus factor), abstraction churn, conceptual drift, and module growth/decay trajectories via git history.

> Complements `hotspot` (current state) by surfacing the trajectory and ownership patterns that brought a module to its present condition.

---

## 1. Metrics

### File lifespan
```bash
# First commit
git log --diff-filter=A --follow --format=%aI -- <file> | tail -1
# Last commit
git log -1 --format=%aI -- <file>
# Lifespan = last - first
```

### Author concentration (Bus factor)
```bash
git log --format='%an' -- <file> | sort | uniq -c | sort -rn
```
- Bus factor 1: only one author has touched it → critical knowledge concentration
- Bus factor 5+: distributed knowledge → resilient
- 80% rule: how many authors account for 80% of changes?

### Abstraction churn vs feature growth
```bash
# Recent commits with classification
git log --since="6 months ago" --format='%s' -- <file>
# Categorize by message keywords:
#   refactor / cleanup / restructure → abstraction churn
#   add / implement / new / feat     → feature growth
#   fix / bug / hotfix               → bug-fix
```
- All refactor / cleanup → design exploration phase or instability
- All feature additions → growth phase
- All bug-fix → quality issues

### Conceptual drift
Compare a module's responsibility at two timepoints:
- Function/class names then vs now
- Imports then vs now
- File path/location changes (`git log --follow --name-status`)

If responsibility has fundamentally changed → conceptual drift detected → comment may be stale, name may mislead.

### Growth/decay trajectory
```bash
# LOC over time per month for 12 months
for m in 1 2 3 4 5 6 7 8 9 10 11 12; do
  date=$(date -d "$m months ago" '+%Y-%m-%d' 2>/dev/null || date -v-${m}m '+%Y-%m-%d')
  loc=$(git -P show "$(git rev-list -1 --before="$date" HEAD)":./<file> 2>/dev/null | wc -l)
  echo "$date $loc"
done
```

Patterns:
- Steady growth → active development
- Plateau → mature, stable
- Decay (LOC decreasing) → cleanup or feature removal
- Spike then decay → temporary expansion then refactor

---

## 2. Pattern Library

### Long-stable file (lifespan > 2y, low churn)
- **Healthy**: well-established core (e.g., date utility, constants)
- **Risk**: dead-on-arrival; verify still used (cross-check with `dependency` recipe)

### Recently-touched file (lifespan > 1y, recent burst)
- **Healthy**: active feature growth
- **Risk**: late-stage refactor that could destabilize

### Frequently-renamed file (`git log --follow --name-status` shows renames)
- Scope shifted: original purpose may not match current name
- Consider documenting purpose history

### Knowledge silo (bus factor 1, lifespan > 1y)
- Single author owns critical knowledge
- Action: pair-programming session, documentation push (handoff to Scribe)

### Conceptual drift detected (responsibility changed mid-life)
- Likely outdated docstrings, misleading file names
- Action: audit + rename / re-document (handoff to Quill / Builder)

---

## 3. Output Format

```yaml
file: src/services/UserService.ts
lifespan: 4y 3mo (created 2022-01-15, last 2026-04-25)
total_commits: 124
bus_factor: 2 (Alice 65%, Bob 28%, others 7%)

evolution_classification:
  pattern: long_stable_active
  confidence: HIGH

abstraction_breakdown_6mo:
  refactor: 12 commits (25%)
  feature: 22 commits (47%)
  bug_fix: 13 commits (28%)
  classification: balanced (healthy)

loc_trajectory_12mo: [421, 438, 445, 452, 460, 478, 489, 502, 510, 538, 587, 612]
trajectory_pattern: steady_growth (mean +16 LOC/month)

conceptual_drift:
  detected: yes
  evidence:
    - "Original purpose (2022): UserService = CRUD only"
    - "Current state (2026): adds auth, session, notifications"
  recommendation: "Split into UserCRUD + AuthService + NotificationService"

risk_indicators:
  - bus_factor_2  # OK but not great
  - conceptual_drift  # mismatched naming
  - active_growth + bug_fix_28%  # bug rate consistent with active growth
```

---

## 4. Cross-Recipe Synergies

| Combine with | Insight |
|---|---|
| `dependency` | High fan-in + bus factor 1 = critical risk |
| `hotspot` | Hot file + conceptual drift = refactor + rename combined |
| `responsibility` | Conceptual drift confirms responsibility-name mismatch |

---

## 5. Common Pitfalls

| Pitfall | Avoidance |
|---|---|
| Counting merge commits in author tally | `--no-merges` flag |
| Treating amended commits as separate | Idempotent count where possible |
| Author email changes (Alice@old vs Alice@new) | Use `.mailmap` or merge by name |
| Ignoring file renames in lifespan calc | `--follow` flag |
| Bot commits (Dependabot, Renovate) inflate counts | Exclude bot author patterns |
| Squash-merge hides real author count | Cross-reference PR data via `gh pr` if needed |
| Treating all "refactor" commits equally | Some are tiny renames; weight by lines changed |

---

## 6. Decision Walkthrough Template

```
File: ____
Time scope: ____ months / "lifetime"

Lifespan: ____
Bus factor: ____ (top 3 authors: ____)

Evolution classification: long_stable / steady_growth / recent_burst / decay / mixed

Abstraction breakdown (% of recent commits):
  refactor: ___%
  feature:  ___%
  bug_fix:  ___%
Healthy mix: 20-40% each

Conceptual drift detected: Y/N
  If yes: recommended rename/split: ____

Risk indicators:
  □ Bus factor ≤ 2
  □ Bug-fix > 40% of recent commits
  □ Conceptual drift
  □ Frequent file renames
  □ Late-stage cleanup burst
  □ Decay during active product

Recommendations:
  □ Pair programming / knowledge-share session
  □ Hand off to Scribe for documentation
  □ Hand off to Quill for rename / docstring update
  □ Hand off to Atlas for split decision
```

---

## 7. References
- Adam Tornhill: "Software Design X-Rays" (2018)
- Bus Factor (Wikipedia, software engineering)
- Microsoft Research: "Don't Touch My Code" (code stability vs author concentration)
- `git log --follow`, `git blame`, `git shortlog -sn` documentation
