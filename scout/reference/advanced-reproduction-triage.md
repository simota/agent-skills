# Advanced Reproduction & Triage

**Purpose:** Advanced reproduction methods and formal severity / priority scoring.
**Read when:** Reproduction is difficult, failures are flaky, or business prioritization needs formal scoring.

## Contents

- Time-travel debugging
- Flaky-test strategy
- severity vs priority
- `RICE` / `ICE`
- Assess-phase template

## Time-Travel Debugging

Use for heisenbugs, race conditions, or failures that disappear under observation.

| Tool | Target | Overhead | Strength |
|------|--------|----------|----------|
| `rr` | Linux, C/C++/Rust | `~1.2x` | reverse execution, watchpoints |
| Replay.io | browser, JS/TS | `~3%` | deterministic browser replay |
| Pernosco | rr-based Linux analysis | cloud | collaborative analysis |

### `rr` Flow

```bash
rr record ./program
rr replay
(rr) reverse-continue
(rr) reverse-step
(rr) watch -l var
```

### Replay.io Flow

1. record the failing run
2. upload the session
3. inspect with DevTools without local reproduction

## Flaky-Test Strategy

Common causes:

- shared test state
- fixed `sleep`
- random data
- current-time dependency
- unmanaged external dependencies
- race conditions

Management sequence:

`Detect -> Quarantine -> Root Cause -> Fix -> Monitor`

## Severity Vs Priority

| Concept | Meaning | Evaluate By |
|--------|---------|-------------|
| Severity | how bad the bug is technically | data loss, feature failure, workaround availability |
| Priority | how soon to fix it | business impact, user count, SLA |

Extended severity classes:

| Level | Meaning | SLA Guide |
|------|---------|-----------|
| `Blocker` | cannot continue using or testing the software | immediate |
| `Critical` | major function fully unusable | `within 4 hours` |
| `Major` | important function impaired, workaround exists | `within 24 hours` |
| `Minor` | limited user impact | next sprint |
| `Trivial` | no functional impact | backlog |

## `RICE` And `ICE`

### `RICE`

`RICE Score = (Reach × Impact × Confidence) / Effort`

| Factor | Scale |
|--------|-------|
| Reach | absolute count |
| Impact | `3`, `2`, `1`, `0.5`, `0.25` |
| Confidence | `100%`, `80%`, `50%` |
| Effort | estimated person-months |

### `ICE`

`ICE Score = Impact × Confidence × Ease`

| Factor | Scale |
|--------|-------|
| Impact | `1-10` |
| Confidence | `1-10` |
| Ease | `1-10` |

### Selection Rule

| Situation | Prefer |
|-----------|--------|
| data-rich prioritization | `RICE` |
| fast rough prioritization | `ICE` |
| user-count sensitivity matters | `RICE` |
| fix-cost comparison matters | `RICE` |

## Assess-Phase Template

```markdown
## Impact Assessment

### Severity: [Blocker|Critical|Major|Minor|Trivial]
### Priority: [P0|P1|P2|P3]

### Quantitative Impact
- Affected users: ___
- Affected transactions/day: ___
- Estimated revenue impact: ___
- SLA breach risk: [Yes/No]

### RICE Score
- Reach: ___
- Impact: ___
- Confidence: ___
- Effort: ___
- Score: ___

### Workaround
- Available: [Yes/No]
- Description: ___
```
