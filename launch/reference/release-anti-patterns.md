# Release & Deployment Anti-Patterns

Purpose: Use this file when you need release-process failure modes, canary and blue-green cautions, or cadence and timing guardrails.

## Contents

1. Deployment anti-patterns
2. Communication and decision anti-patterns
3. Canary and blue-green pitfalls
4. Release cadence pitfalls
5. Launch enforcement points

## 1. Deployment Anti-Patterns

| ID | Anti-pattern | What goes wrong | Guardrail |
|----|--------------|-----------------|-----------|
| `RL-01` | Big bang deploy | Too much change ships at once; root cause isolation becomes slow | Prefer small, frequent releases and staged exposure |
| `RL-02` | Deploying straight to production | Unverified behavior reaches users | Require staging verification |
| `RL-03` | Manual deployment | Human error and poor reproducibility | Prefer pipeline-driven deployment |
| `RL-04` | No rollback plan | Recovery becomes slow and unsafe | Block release without rollback |
| `RL-05` | Immediate release to all users | Failures affect everyone at once | Use canary, dark launch, or staged rollout |
| `RL-06` | Monolithic pipeline | One failed path blocks the whole delivery train | Split by service or component where possible |
| `RL-07` | Friday release | Recovery coverage is usually weaker | Prefer Tuesday to Thursday |
| `RL-08` | Procedure-only deployment | Human-run playbooks drift | Keep deployment logic in code or pipelines |

## 2. Communication And Decision Anti-Patterns

| ID | Anti-pattern | What goes wrong | Guardrail |
|----|--------------|-----------------|-----------|
| `RL-09` | Silent release | Stakeholders cannot detect regressions quickly | Notify release stakeholders |
| `RL-10` | Skipping Go/No-Go | Blockers stay hidden | Require explicit Go/No-Go review |
| `RL-11` | Writing CHANGELOG after release | Missing or inaccurate notes | Generate CHANGELOG before release |
| `RL-12` | Skipping postmortem | The same failure repeats | Run postmortem within `48 hours` after a significant failure |

## 3. Canary And Blue-Green Pitfalls

### Canary pitfalls

- Canary traffic below `1%` is usually too small to detect meaningful issues.
- Use at least `5%` traffic for signal.
- Keep the canary live for at least `24 hours`.
- Define success metrics before rollout.
- Avoid bundling incompatible DB changes with canary traffic shifts.

### Blue-Green pitfalls

- Shared state can break rollback assumptions.
- Both environments can double cost if not managed.
- Warm-up gaps can create false negatives or latency spikes.
- Switch only after health checks pass.

## 4. Release Cadence Pitfalls

| Pitfall | What goes wrong | Guardrail |
|---------|-----------------|-----------|
| Releasing too rarely | Change batches become too large and risky | Release at least weekly where feasible |
| Releasing too often without gates | Quality drops | Keep quality gates intact |
| Treating schedule as absolute | Unready work ships | Schedule is a target, quality is the gate |
| Always releasing at the same hot spot | Load and coordination risk concentrate | Use flexible release windows |

## 5. Launch Enforcement Points

Apply these during `Review` and `Evaluate`:

- Block if rollback plan is missing (`RL-04`).
- Block if staging verification is skipped (`RL-02`).
- Warn on Friday afternoon release windows (`RL-07`).
- Warn if CHANGELOG is missing (`RL-11`).
- Require explicit Go/No-Go review (`RL-10`).
