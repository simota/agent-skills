# Orbit Script Processing Flow

Purpose: load this when debugging loop behavior or explaining how the generated scripts interact. It summarizes lifecycle flow without repeating the full templates.

## Contents

1. Overall lifecycle
2. Recovery flow
3. Verification structure
4. Inter-script relationships
5. Key design points

## Overall Lifecycle

| Stage | Main actions | Key guardrails |
|-------|--------------|----------------|
| Bootstrap | create loop directory, `goal.md`, `progress.md`, `state.env`, optional `verify.sh`, always `run-loop.sh` and `notify.sh` | do not overwrite existing `goal.md` or `progress.md` |
| Pre-flight | disk `>= 100MB`, lock liveness, git health, log rotation, checksum validation | abort on `[PREFLIGHT:FAIL]` unless an explicit bypass exists |
| Branch setup | record `ORIGIN_BRANCH`, prepare `ITER_BRANCH`, stash and restore dirt when needed | only when `BRANCH_ISOLATION=true` and `AUTOCOMMIT=true` |
| Main loop | health check, executor run, verification, scoped auto-commit, `DONE` gate, state write, notify | bounded retry, dual `DONE` gate, atomic `state.env` writes |
| Post-loop squash | move from iteration branch to summary branch and squash if configured | only when `STATUS=DONE`, `BRANCH_ISOLATION=true`, `SQUASH_ON_DONE=true` |
| Footer | emit `NEXUS_LOOP_STATUS` and `NEXUS_LOOP_SUMMARY` | non-`DONE` states collapse to footer `CONTINUE` |

## Recovery Flow (`recover.sh`)

1. read latest iteration from `progress.md`
2. infer recovered status from recent progress evidence
3. rebuild `state.env` atomically
4. append a recovery note to `progress.md`

Source-of-truth order:
1. `progress.md`
2. `runner.log`
3. existing `state.env`

## Verification Check Structure (`verify.sh`)

1. initialize `PASS=0`, `FAIL=0`
2. run each acceptance check through `run_check`
3. print pass/fail lines
4. exit `1` if any check fails, else exit `0`

Effect on `DONE`:
- `PASS` allows `done.md` to promote the loop to `DONE`
- `FAIL` forces `CONTINUE`
- no `verify.sh` means `SKIP`, which is tolerated but weaker evidence

## Inter-Script Relationships

| Producer | Consumer | Contract |
|----------|----------|----------|
| `bootstrap.sh` | `goal.md`, `progress.md`, `state.env`, optional `verify.sh`, `run-loop.sh`, `notify.sh` | bootstrap initializes the loop contract |
| `run-loop.sh` | reads `state.env`, `goal.md`, optional `verify.sh`, optional `notify.sh`, optional `done.md` | main execution loop |
| `run-loop.sh` | writes `progress.md`, `runner.log`, `state.env`, `state.env.sha256`, `.run-loop.lock`, optional `.iter-timings.log` | resumable execution state |
| `run-loop.sh` | creates `loop/iter-{name}` and `loop/summary-{name}` | branch isolation and final squash |
| `recover.sh` | reads `progress.md` and rewrites `state.env` | evidence-based recovery |
| `notify.sh` | reads commit metadata and writes notification logs/audio | non-fatal notification hook |

## Key Design Points

- `DONE` is a dual gate: `done.md` plus verify `PASS` or `SKIP`
- retry is bounded by `RETRY_LIMIT`
- timeouts are enforced by `portable_timeout`
- dirty baseline is captured and excluded from scoped auto-commit
- `state.env` is written atomically and protected by checksum
- the runner traps shutdown signals and writes resumable state
- only `READY`, `CONTINUE`, and `DONE` are valid footer statuses
- pre-flight uses `100MB`; iteration health uses `50MB`
- adaptive timeout uses median of the last `5` executions times `2`, bounded to `[EXEC_TIMEOUT, EXEC_TIMEOUT x 3]`

For exact script bodies, use `script-templates.md`.
