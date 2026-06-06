# SRM (Sample Ratio Mismatch) Detection Reference

Purpose: Detect, diagnose, and triage Sample Ratio Mismatch — a population-level bias that silently invalidates A/B tests. SRM is the single most dangerous experiment failure mode: the test looks fine, statistical significance arrives, but the conclusion is wrong because treatment and control populations are not comparable.

## Scope Boundary

- **experiment `srm`**: SRM detection and root-cause analysis (this document).
- **experiment `ab` (elsewhere)**: Includes SRM monitoring as part of standard design.
- **experiment `analyze` (elsewhere)**: Full result analysis — SRM is the first check.
- **Pulse (elsewhere)**: Metric definitions; SRM diagnosis uses Pulse-defined segments.

## What SRM Is

Traffic assignment targets, say, 50/50. Actual observed split: 50.3 / 49.7. Is this random variation, or a bug?

SRM = the observed ratio deviates from target beyond what random chance explains, detected via chi-squared goodness-of-fit test.

### Prevalence

Per Fabijan et al. (Microsoft, KDD 2019, *"Diagnosing Sample Ratio Mismatch in Online Controlled Experiments: A Taxonomy and Rules of Thumb for Practitioners"*), **approximately 6% of all online controlled experiments at Microsoft exhibit an SRM** across experience built from 25+ products in four software companies. This is not a rare-edge case — it is roughly 1 in 16 experiments. Treat SRM monitoring as standard infrastructure, not as a one-off check on suspicious results.

### Why it matters

If assignment is biased, the two populations are no longer exchangeable. The ATE (Average Treatment Effect) estimate is biased by whatever factor correlates with the assignment bug. Classic example: treatment bucket over-sampled iOS users → observed +5% conversion isn't from the feature, it's because iOS users convert higher anyway.

**SRM detection does not tell you the direction of the bias — only that the test is invalid.** You cannot "correct for" SRM after the fact; you must fix and re-run.

## Detection

### Chi-squared goodness-of-fit test

```
χ² = Σ (observed_i - expected_i)² / expected_i
```

With k-1 degrees of freedom (k = number of variants).

### Threshold

Industry standard: **p < 0.001** (not 0.05).

Rationale: type-I error is low-cost here (investigate a potential SRM, don't ship). Type-II error is catastrophic (ship on bad data). Microsoft Azure team (Fabijan et al.) advocates the 0.001 threshold.

### When to check

- On every experiment, every day.
- Not just at conclusion — catch it early.
- Ideally automated, daily SRM scan across all live tests.

### Example

| Variant | Expected | Observed | Chi-sq contribution |
|---------|----------|----------|---------------------|
| Control | 50000 | 50312 | 1.95 |
| Treatment | 50000 | 49688 | 1.95 |

χ² = 3.90, df = 1, p = 0.048 → not significant at 0.001 threshold. Pass.

| Variant | Expected | Observed |
|---------|----------|----------|
| Control | 50000 | 51047 |
| Treatment | 50000 | 48953 |

χ² = 43.88, df = 1, p ≈ 3.5e-11 → SRM. Investigate.

## Root Cause Diagnosis

SRM is a symptom. Diagnose systematically via segment decomposition.

### Common root causes

| Cause | Mechanism | Signal |
|-------|-----------|--------|
| Bot / crawler traffic | Bots randomly buckets differently | Check by user-agent; exclude bots pre-analysis |
| Pre-experiment filter | Filter applied after assignment, asymmetric | Check filter sequence in pipeline |
| Redirect loop | Treatment has extra redirect that drops some users | Check treatment-specific perf metrics |
| Browser incompatibility | Treatment fails on older browsers | Device / browser segment analysis |
| Cache / CDN inconsistency | Stale variant served to returning users | Check new vs returning user SRM |
| Session vs user mismatch | Randomization at one level, analysis at another | Check assignment-ID vs user-ID |
| Logging loss | One variant loses events at higher rate | Cross-check with server-side logs |
| Bucket hash collision | Hash function maps IDs non-uniformly | Inspect hash function distribution |
| Late arrivals | Users assigned after treatment cutoff | Check time-range of assignments |
| Feature flag default | When flag evaluation fails, defaults to control | Check default-return rate |

### Segment decomposition

Split SRM by segments; find the segment that explains the deviation.

| Segment dimension | Test per-segment |
|-------------------|------------------|
| Device type | iOS / Android / Web desktop / Web mobile |
| Browser | Chrome / Safari / Firefox / Edge / others |
| Region | Country / continent |
| Traffic source | Organic / paid / direct / email |
| New vs returning | First-session vs returning users |
| Tenure | Days since signup (cohort) |
| Plan | Free / Pro / Enterprise |
| Time of day | Hour buckets |

The segment where SRM is strongest → likely root cause locus.

### Example diagnosis

```
Global SRM: chi² = 45, p = 2e-11

Segment decomposition:
| Segment   | control | treatment | chi² |
|-----------|---------|-----------|------|
| iOS       | 15200   | 14800     | 5.3  |
| Android   | 19500   | 19400     | 0.26 |
| Desktop   | 16000   | 15800     | 1.25 |
| Safari iOS| 8200    | 7300      | 52   | ← strong SRM
```

Safari iOS treatment drops ~11% users. Hypothesis: treatment uses a JS API unsupported in older Safari iOS, triggering silent failure before assignment logs. Fix: polyfill, re-run.

## Workflow

```
DETECT     →  daily chi² on top-level traffic split
           →  alert at p < 0.001

INVESTIGATE→  segment decomposition (device / browser / region / source / etc.)
           →  identify segment with strongest chi² contribution

HYPOTHESIZE→  map segment to mechanism (from root cause table)
           →  check infrastructure logs for bucket-time discrepancies

FIX        →  patch the assignment bug
           →  DO NOT attempt post-hoc correction
           →  archive the contaminated data

RE-RUN     →  fresh experiment, new time window
           →  monitor SRM from day 1
           →  require SRM-free period before trusting results

DOCUMENT   →  post-mortem in experiment journal
           →  update assignment pipeline tests
           →  add regression check for this root cause
```

## Preventive Design

- **Early monitoring**: chi² alert on day 1, day 3, day 7, and daily thereafter.
- **Shared assignment bot filter**: exclude known bots uniformly before assignment.
- **Server-side assignment**: prefer over client-side (avoids browser-level bias).
- **Sticky assignment**: hash user-ID, not session-ID.
- **Flag default check**: instrument flag-default rate per variant.
- **Pipeline contract test**: CI test that a synthetic traffic load produces no SRM.
- **A/A test**: before a real A/B, run A/A (no treatment) and verify no SRM — catches pipeline bugs.
- **Non-inferiority SRM threshold**: stricter than 0.001 (0.0001) on mission-critical tests.

## Output Template

```markdown
## SRM Diagnosis: [Experiment]

### Top-Level Check
- **Expected ratio**: [e.g., 50/50]
- **Observed**: control = [N], treatment = [N]
- **Chi²**: [value], df = [k-1], p = [value]
- **Verdict**: PASS / SRM DETECTED

### Segment Decomposition (if SRM)
| Segment | Control | Treatment | Chi² | p |
|---------|---------|-----------|------|---|
| [...] | [...] | [...] | [...] | [...] |

### Root Cause Hypothesis
- **Likely cause**: [from table]
- **Evidence**: [logs, segment signals, mechanism]

### Fix
- **Change**: [what to patch]
- **Verification plan**: [A/A re-run / SRM alert / pipeline test]

### Decision
- [ ] Discard current data
- [ ] Fix and re-run from fresh start
- [ ] Update pipeline regression tests

### Handoffs
- Builder: implement fix
- Pulse: update metric / segment definitions if needed
- Radar: pipeline contract test
- Experiment Lead: formal post-mortem
```

## Anti-Patterns

| Anti-pattern | Fix |
|--------------|-----|
| Using p < 0.05 threshold | Use p < 0.001 — SRM investigation cost is cheap |
| Ignoring SRM and "correcting" with re-weighting | Invalid — use fresh data, fix root cause |
| Only checking SRM at conclusion | Check daily from day 1 |
| Global check only, no segment decomposition | Without segments, can't find root cause |
| Shipping despite SRM because "effect is large" | Effect may be 100% artifact; do not ship |
| Not logging assignment in the pipeline | Can't reconstruct SRM if assignment events missing |
| Blaming randomness for small deviations | Chi² quantifies — don't eyeball |

## Deliverable Contract

When `srm` completes, emit:

- **Top-level chi² result** with p < 0.001 decision.
- **Segment decomposition** if SRM detected.
- **Root cause hypothesis** with evidence.
- **Fix + re-run plan**.
- **Preventive design upgrades** (alerts, tests, A/A).
- **Handoffs**: Builder, Pulse, Radar, Experiment Lead.

## References

- Fabijan, Gupchup, Gupta, Omhover, Vermeer, Young — *Diagnosing Sample Ratio Mismatch in Online Controlled Experiments* (Microsoft, KDD 2019)
- Kohavi, Tang, Xu — *Trustworthy Online Controlled Experiments* (2020, the SRM canon)
- Microsoft ExP — Sample Ratio Mismatch troubleshooting guide
- Airbnb — "Experimentation Platform" blog posts on SRM at scale
- Booking.com — Themis experimentation framework (SRM auto-detection)
- LinkedIn — XLNT platform SRM alerts
- Spotify Confidence — SRM in practice
- Exp-Platform community — SRM war stories
