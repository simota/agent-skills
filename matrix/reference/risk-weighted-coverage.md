# Risk-Weighted Coverage Reference

Purpose: Prioritize combinations by Risk Priority Number (RPN = Severity × Occurrence × Detection) and Action Priority (AP) per AIAG-VDA 2019. Integrates FMEA output from omen to produce risk-sorted coverage sets with residual-risk reporting.

## Scope Boundary

- **matrix `risk-cover`**: RPN / Action Priority weighting over combinatorial coverage; FMEA integration (this document).
- **matrix `prioritize` (elsewhere)**: General Critical/High/Medium/Low prioritization without RPN integration.
- **matrix `pairwise` (elsewhere)**: Pure 2-way coverage without risk weighting.
- **omen (elsewhere)**: FMEA / pre-mortem analysis. `risk-cover` *consumes* omen's RPN output.
- **Sentinel / Breach (elsewhere)**: Security RPN specifically for attack surface.
- **rank (elsewhere)**: General ICE/RICE/WSJF prioritization for backlog items, not per-combination test selection.

## Workflow

```
FMEA IN    →  pull RPN scores from omen if available
           →  otherwise derive RPN per axis/combination with team input

SCORE      →  RPN = Severity × Occurrence × Detection
           →  each factor 1-10 (AIAG 4th ed. scale)
           →  cap at RPN = 1000

CLASSIFY   →  Action Priority: H (high) / M (medium) / L (low)
           →  AIAG-VDA 2019 replaces RPN-only thresholds with AP matrix

WEIGHT     →  multiply combinatorial coverage priority by RPN
           →  RPN ≥ 200 or AP=H → mandatory inclusion
           →  RPN 100-199 or AP=M → include if under budget
           →  RPN < 100 or AP=L → include on residual budget

RESIDUAL   →  report uncovered combinations with their RPN
           →  residual-risk score = Σ (RPN × uncovered-flag)
           →  hand off residuals to omen for depth review
```

## RPN Scoring

### Severity (S) 1-10 scale

| Score | Description |
|-------|------------|
| 10 | Catastrophic: loss of life, major regulatory breach, total data loss |
| 9 | Very high: injury risk, legal penalty, production-wide outage |
| 8 | High: SEV1 incident, PII leak, top-tier SLA breach |
| 7 | Significant: SEV2, important-customer impact |
| 6 | Moderate: SEV3, noticeable degradation |
| 5 | Low-moderate: limited customer reports |
| 4 | Low: minor feature issue |
| 3 | Minor: cosmetic, workaround available |
| 2 | Very minor: internal only |
| 1 | None: no customer or internal impact |

### Occurrence (O) 1-10 scale

| Score | Description | Probability |
|-------|------------|-------------|
| 10 | Almost certain | > 1 in 2 |
| 9 | Very high | 1 in 3 |
| 8 | High | 1 in 8 |
| 7 | Moderately high | 1 in 20 |
| 6 | Moderate | 1 in 80 |
| 5 | Low-moderate | 1 in 400 |
| 4 | Low | 1 in 2,000 |
| 3 | Very low | 1 in 15,000 |
| 2 | Remote | 1 in 150,000 |
| 1 | Nearly impossible | < 1 in 1,500,000 |

### Detection (D) 1-10 scale (inverse — 1 is best)

| Score | Description |
|-------|------------|
| 10 | No detection method exists |
| 9 | Very unlikely to detect before release |
| 8 | Remote chance of detection |
| 7 | Very low detection probability |
| 6 | Low (may be caught by smoke tests) |
| 5 | Moderate (regression tests likely to catch) |
| 4 | Moderately high (unit tests catch) |
| 3 | High (multiple test layers) |
| 2 | Very high (CI gates + production canaries) |
| 1 | Certain (100% detection before release) |

### RPN Calculation

```
RPN = S × O × D    (range: 1 - 1000)
```

## Action Priority (AIAG-VDA 2019)

RPN alone can mislead (e.g., S=10, O=2, D=5 → RPN 100 looks moderate but S=10 is critical). AIAG-VDA 2019 replaces pure RPN thresholds with an Action Priority matrix.

### AP Matrix (simplified)

| Severity | Occurrence | Detection | Action Priority |
|----------|-----------|-----------|-----------------|
| 9-10 | any | any | **H** |
| 7-8 | 7-10 | any | **H** |
| 7-8 | 4-6 | 7-10 | **H** |
| 7-8 | 4-6 | 1-6 | **M** |
| 7-8 | 2-3 | any | **M** |
| 7-8 | 1 | any | **L** |
| 4-6 | 7-10 | 7-10 | **H** |
| 4-6 | 7-10 | 1-6 | **M** |
| 4-6 | 4-6 | any | **M** |
| 4-6 | 2-3 | any | **L** |
| 4-6 | 1 | any | **L** |
| 1-3 | any | any | **L** |

Use AP as the primary gate; use RPN as a tie-breaker within each AP bucket.

## Risk-Weighted Coverage Selection

```
Step 1  Enumerate combinations (optionally from `pairwise` or `cover`).
Step 2  Assign S, O, D per combination (derive or pull from omen).
Step 3  Compute RPN and AP per combination.
Step 4  Sort by (AP desc, RPN desc).
Step 5  Selection rule:
        AP = H        → mandatory include
        AP = M        → include if under budget
        AP = L        → include on residual budget
Step 6  For pairwise 2-way covering subset, ensure every (P_i, P_j) pair
        is still covered at least once AFTER risk weighting.
        If risk weighting drops a pair, re-insert the cheapest covering case.
Step 7  Report residual risk: Σ RPN of uncovered combinations.
```

## Residual Risk Reporting

Every selection inevitably leaves some combinations uncovered (by budget or pairwise reduction). Report what remains uncovered and why.

```markdown
### Residual Risk Report

| Uncovered Combination | S | O | D | RPN | AP | Reason Uncovered |
|----------------------|---|---|---|-----|----|----|
| (browser=IE11, locale=JA, payment=wire) | 6 | 3 | 8 | 144 | M | pairwise reduction |
| (region=APAC, plan=free, feature=SSO) | 4 | 7 | 4 | 112 | M | budget |
| ... | ... | ... | ... | ... | ... | ... |

**Total residual RPN**: 412
**Residual AP counts**: H=0, M=5, L=12
**Recommendation**: 
  - H residual count must be 0 (mandatory rule). If > 0, request budget increase.
  - M residual count ≤ 5 (acceptable with sign-off).
  - L residual count: advisory only.
```

Hand off to omen for depth review on any AP=H uncovered or RPN ≥ 200 uncovered.

## FMEA Integration with omen

When omen has already produced an FMEA:

1. Ingest omen's FMEA table (failure mode, cause, S, O, D, RPN).
2. Map each failure mode to combinatorial axes: "this failure is triggered by parameter combination {X, Y, Z}".
3. Inherit RPN / AP for that combination.
4. Any axis combination not covered in omen's FMEA defaults to team-estimated S/O/D (flag as "estimated, not FMEA-backed").

Output table must indicate source:

```
Source: [FMEA (omen-20250410-FMEA-03) | Estimated (team)]
```

## Security-Specific RPN (hand off to Sentinel / Breach)

For attack-surface combinations, use CVSS-based scoring instead of generic S/O/D:

| Factor | Mapping |
|--------|---------|
| Severity | CVSS Base Score (0-10) |
| Occurrence | Attack Vector × Attack Complexity (simplified: 10 = network + low complexity; 1 = physical + high complexity) |
| Detection | Log/WAF/IDS coverage (inverse; 1 = monitored, 10 = dark) |

## Output Template

```markdown
## Risk-Weighted Coverage Plan

### Risk Inputs
- **Source**: [FMEA / Estimated / Hybrid]
- **omen reference**: [ID if applicable]
- **Team reviewers**: [names]

### Scoring Summary
| AP Bucket | Count | Total RPN |
|-----------|-------|-----------|
| H | [n] | [sum] |
| M | [n] | [sum] |
| L | [n] | [sum] |

### Selected Test Cases (AP desc, RPN desc)
| TC | Combination | S | O | D | RPN | AP | Source |
|----|-------------|---|---|---|-----|----|----|
| T-1 | (P1=a, P2=x, P3=1) | 9 | 5 | 7 | 315 | H | FMEA-03 |
| T-2 | ... | ... | ... | ... | ... | ... | ... |

### Pairwise Coverage After Weighting
- **Pairs covered**: [%]
- **Pairs dropped by weighting and re-inserted**: [count]
- **Final test count**: [N]

### Residual Risk
| Uncovered | S | O | D | RPN | AP | Reason |
|-----------|---|---|---|-----|----|----|
| ... | ... | ... | ... | ... | ... | ... |

- **Total residual RPN**: [sum]
- **H residual**: [count] (must be 0)
- **M residual**: [count]
- **L residual**: [count]

### Handoff
- **Next agents**: Radar (unit), Voyager (E2E), Siege (load), Sentinel/Probe (security), omen (depth review on residual)
```

## Common Pitfalls

| Pitfall | Fix |
|---------|-----|
| Using RPN thresholds alone | Use AP matrix (AIAG-VDA 2019) |
| Everything is "high RPN" | Calibrate O and D using real incident data |
| No residual report | Always report uncovered combinations + their RPN |
| Dropping H-AP pairs by mistake | Re-insert covering case for every dropped pair |
| Single-person scoring | RPN is team-estimated; single scores are noisy |
| Ignoring FMEA input | Pull omen FMEA when available; do not re-estimate |

## Deliverable Contract

When `risk-cover` completes, emit:

- **Risk input source** (FMEA reference or estimated).
- **S/O/D scores per combination** with rationale.
- **RPN and AP per combination**.
- **Selected test set** (AP desc, RPN desc).
- **Pairwise coverage preservation check** after weighting.
- **Residual risk report** (uncovered combinations + their RPN / AP).
- **Budget check** (H residual must be 0).
- **Handoff**: Radar / Voyager / Siege / Sentinel / Probe / omen.

## References

- AIAG-VDA FMEA Handbook (2019) — Action Priority matrix
- AIAG FMEA 4th Edition — RPN scoring scales (S/O/D 1-10)
- NIST SP 800-30 — Risk Management Framework (risk likelihood × impact)
- CVSS v3.1 / v4.0 — Common Vulnerability Scoring System (security RPN)
- IEC 60812 — FMEA procedure
- ISO 31000 — Risk management principles
