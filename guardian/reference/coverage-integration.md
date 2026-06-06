# Test Coverage Integration Reference

Purpose: Correlate changed files with CI coverage, score test quality, and trigger Radar when risk is under-tested.

## Contents

- Supported coverage formats
- Change-to-coverage correlation
- Gap categories
- Radar handoff rules
- Test-score contribution
- AUTORUN rules
- Report templates

## Supported Formats

```yaml
coverage_formats:
  lcov:
    file: "coverage/lcov.info"
  cobertura:
    file: "coverage/cobertura.xml"
  istanbul:
    file: "coverage/coverage-summary.json"
```

## Change-to-Coverage Correlation

Guardian should:
1. list changed files
2. parse file-level coverage
3. compute changed-line coverage
4. identify new or modified code that remains uncovered

Key signal:

```yaml
changed_line_coverage:
  critical_threshold: "< 0.5"
```

## Gap Categories

### Critical Gaps

- auth or security code `< 80%`
- new payment logic `< 90%`
- changed code with `0%` coverage

### High Priority Gaps

- core business logic `< 70%`
- hotspot file `< 60%`
- regression risk `> 5%`

## `GUARDIAN_TO_RADAR_HANDOFF (Coverage)`

Trigger Radar when one of these is true:
- `high_risk_file AND coverage_gap > 0.40`
- `hotspot_file AND coverage < 0.50`
- `critical_file AND no_tests`
- `coverage_regression > 5% AND risk_high`
- `regression_risk > 0.70`

Template:

```markdown
## GUARDIAN_TO_RADAR_HANDOFF (Coverage)

**PR / Branch**: ...
**Reason**: coverage gap on high-risk or hotspot change
**Critical files**:
- `src/auth/...`
- `src/payment/...`

**Requested action**:
- add focused tests
- close changed-line coverage gaps
- report residual risk
```

## Test Score Contribution

Within the Test Score component:
- line coverage: `30%`
- branch coverage: `25%`
- changed-line coverage: `25%`
- test quality: `10%`
- coverage delta: `10%`

Within overall PR quality:
- test score weight: `15%`

## AUTORUN Rules

Auto-execute:
- parse coverage reports
- correlate coverage to changed files
- emit coverage gap report

Pause only when:
- critical coverage gap combines with another blocking condition
- coverage data is inconsistent enough to invalidate risk scoring

## Report Templates

### Coverage Gap Report

```markdown
## Coverage Gap Analysis

### Critical Gaps (Must Fix)
- `src/auth/token.ts` changed-line coverage: 32%

### High Priority Gaps
- `src/core/order.ts` branch coverage: 55%
```

### Coverage Summary

```markdown
## Coverage Integration Report

### PR Coverage Summary
- Overall line coverage: 84%
- Changed-line coverage: 61%

### Test Score Breakdown
- Line: 24/30
- Branch: 18/25
- Changed lines: 12/25
```
