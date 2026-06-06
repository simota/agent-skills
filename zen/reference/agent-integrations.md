# Zen Agent Integrations

Purpose: Use this file when Zen collaborates with Radar, Canvas, Judge, Guardian, AUTORUN, or Nexus.

## Contents
- [Radar Integration](#radar-integration)
- [Canvas Integration](#canvas-integration)
- [Judge Integration](#judge-integration)
- [Guardian Integration](#guardian-integration)
- [AUTORUN Flow](#autorun-flow)

## Radar Integration

Coordinate with Radar whenever verification or coverage work exceeds Zen's boundary.

### Request Radar before refactoring

- Coverage is unknown or below threshold
- Existing tests might not protect the refactor
- Dead-code removal could affect hidden test dependencies

```markdown
### Radar Test Verification Request (Pre-Refactoring)

**Target**: [file/function]

**Checks Needed**:
- [ ] Current coverage percentage
- [ ] Existing tests covering this code
- [ ] Missing edge cases
- [ ] All tests currently passing

**Coverage Requirements**:
- Minimum before refactoring: 80%
- If below 80%: add tests first, then refactor
```

### Request Radar after refactoring

```markdown
### Radar Test Verification Request (Post-Refactoring)

**Refactored**: [file/function]

**Verification Needed**:
- [ ] All existing tests still pass
- [ ] Coverage maintained or improved
- [ ] No new failures introduced
- [ ] Edge cases still covered

**Expected Results**:
- Tests: all passing
- Coverage: >= previous coverage
```

### Report Radar results back

```markdown
### Test Verification Results

**Pre-Refactoring**:
- Coverage: [X%]
- Tests: [N passing, M failing]

**Post-Refactoring**:
- Coverage: [Y%]
- Tests: [N passing, M failing]

**Conclusion**: [Safe to merge / Needs follow-up]
```

## Canvas Integration

Use Canvas only when a diagram materially improves understanding.

### Typical requests

- **Dependency graph**: before/after dependencies for large cleanup
- **Class structure diagram**: extracted responsibilities from a large class
- **Impact map**: files changed, tests affected, untouched areas

Keep Canvas requests minimal:

```markdown
### Canvas Integration: [Dependency Graph / Class Extraction / Refactoring Impact]

**Target**: [file/module]
**Need**: [before/after view or impact map]
**Focus**: [dependencies / classes / changed files]
```

## Judge Integration

Judge invokes Zen during PDCA-style quality loops.

- Zen usually runs in the `DO` phase after Builder fixes bugs.
- Zen should refactor only what the latest `CHECK` phase identified.
- Judge owns the iteration budget and the stop/go decision.
- Zen must report measurable improvement, not only narrative cleanup.

## Guardian Integration

### Pattern H: PR Noise Separation

Use when a PR mixes feature work with cleanup:

1. Guardian identifies cleanup noise.
2. Guardian sends `GUARDIAN_TO_ZEN_HANDOFF`.
3. Zen extracts the cleanup into an isolated refactor.
4. Zen returns `ZEN_TO_GUARDIAN_HANDOFF` with commit guidance.

### Pattern I: Tech Debt Hotspot Refactoring

Use when Guardian flags changed files with debt hotspots:

1. Guardian sends `GUARDIAN_TO_ZEN_HANDOFF`.
2. Zen performs targeted, behavior-preserving cleanup.
3. Zen routes verification to Radar if needed.
4. Guardian uses the result for PR strategy.

## AUTORUN Flow

```
_AGENT_CONTEXT
  -> Parse input handoff
  -> Measure current state
  -> Apply one meaningful refactor
  -> Prepare follow-up handoffs
  -> Emit _STEP_COMPLETE
```

### Common AUTORUN input tokens

- `JUDGE_TO_ZEN`
- `ATLAS_TO_ZEN`
- `BUILDER_TO_ZEN`
- `GUARDIAN_TO_ZEN_HANDOFF`

### Common AUTORUN output tokens

- `ZEN_TO_RADAR`
- `ZEN_TO_JUDGE`
- `ZEN_TO_CANVAS`
- `ZEN_TO_QUILL`
- `ZEN_TO_GUARDIAN_HANDOFF`
