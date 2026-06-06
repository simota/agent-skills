# Vague Goal Handling

Purpose: load this when `goal.md` is weak, vague, or missing. It converts ambiguous requests into measurable loop contracts with the minimum necessary clarification.

## Contents

1. Goal-quality matrix
2. Pattern dictionary
3. Three-hypothesis protocol
4. AC-strengthening templates
5. Non-ask-first rule

## Goal Quality Assessment Matrix

| Grade | Signal | Action |
|-------|--------|--------|
| Strong | objective is specific, ACs are measurable, verify command exists | proceed |
| Weak | objective exists but ACs are incomplete or subjective | strengthen ACs, then proceed |
| Vague | generic verbs such as "improve", "fix", or "refactor" without measurable outcome | apply the Three-Hypothesis Protocol |
| Missing | no `goal.md` or empty placeholder | classify `CONTRACT_MISSING` and request goal input |

## Vague Goal Pattern Dictionary

### "improve X" / "make X better"

| Hypothesis | AC template | Verify command |
|------------|-------------|----------------|
| performance issue | response time < N ms at P95 | `k6 run load-test.js --summary-trend 'http_req_duration:p(95)<N'` |
| quality issue | all checks pass | `npm run lint && npm test` |
| readability issue | complexity or duplication reduced | `npx jscpd --threshold 5 src/X/` |

### "fix tests" / "fix CI"

| Hypothesis | AC template | Verify command |
|------------|-------------|----------------|
| named tests fail | named failing tests pass | `npm test -- --testPathPattern='<failing>'` |
| environment issue | clean-environment run passes | `npm ci && npm test` |
| flaky test | same test passes 5 consecutive runs | `for i in {1..5}; do npm test || exit 1; done` |

### "refactor X"

| Hypothesis | AC template | Verify command |
|------------|-------------|----------------|
| split a large module | X split into `<= N` files, each `< 200` lines | `wc -l src/X/*.ts` |
| remove duplication | duplication score `< 5%` | `npx jscpd src/X/` |
| simplify interface | public API reduced to `<= N` exports | `grep -c '^export' src/X/index.ts` |

### "clean up X"

| Hypothesis | AC template | Verify command |
|------------|-------------|----------------|
| remove dead code | no unused exports | `npx ts-prune src/X/` |
| formatting/lint issue | zero lint errors | `npx eslint src/X/ --max-warnings 0` |
| dependency cleanup | no unused dependencies | `npx depcheck` |

### "make it faster" / "optimize"

| Hypothesis | AC template | Verify command |
|------------|-------------|----------------|
| bundle-size issue | bundle `< N KB` | `npm run build && du -sh dist/` |
| runtime performance issue | benchmark `< N ms` | `npm run bench` |
| startup-time issue | cold start `< N s` | `time node dist/index.js --dry-run` |

## Three-Hypothesis Protocol

When goal quality is `Vague`:

1. infer context first
2. generate 3 likely hypotheses from the dictionary
3. rank them by evidence
4. propose the top hypothesis as default and list alternatives
5. if the user confirms, or no response is needed, proceed with the top hypothesis
6. if the user chooses an alternative, rewrite the contract accordingly

Use this pattern for the proposal:

```text
Goal "<goal>" detected as Vague.
Proposed contract:
  Objective: <top hypothesis>
  AC: <measurable outcome>
  Verify: <command>
Alternatives:
  H2: <alternative 2>
  H3: <alternative 3>
```

## AC Strengthening Templates

| Vague AC | Measurable AC | Verify command |
|----------|---------------|----------------|
| "Code is clean" | zero lint and type errors | `npm run lint && tsc --noEmit` |
| "Tests pass" | all suites exit `0`, coverage `>= N%` | `npm test -- --coverage --coverageThreshold='{"global":{"lines":N}}'` |
| "Performance is good" | P95 latency `< N ms` under `M` users | `k6 run --vus M --duration 30s load-test.js` |
| "No regressions" | all existing tests pass and no new lint warnings | `npm test && npm run lint -- --max-warnings 0` |
| "UI looks correct" | visual diff `< 0.1%` | `npx playwright test --project=visual` |
| "Works on mobile" | Lighthouse mobile score `>= 90` | `npx lighthouse --preset=desktop --output=json URL` |
| "Handles errors" | all error paths return expected status | `npm run test:error-paths` |
| "Is accessible" | zero axe-core violations | `npx playwright test --project=a11y` |

## Non-Ask-First Rule

Before asking the user to clarify a vague goal, exhaust inference from at least `3` sources:

| Source | Use it for |
|--------|------------|
| `git log --oneline -20` | recent scope and intent |
| `package.json` scripts | candidate verify commands |
| CI config | failing checks and command shape |
| `runner.log` | previous failure modes |
| `progress.md` | prior attempts |
| direct test output | precise failing scope |

Rules:
- If `>= 2` sources support the same hypothesis, proceed without asking.
- If inferred scope is large (`> 10` files or `> 3` ACs) or irreversible, confirm before continuing.
