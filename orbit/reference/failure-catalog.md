# Failure Catalog

Purpose: single source of truth for classifying loop anomalies. Maps every observed evidence shape to a failure class, an anti-pattern ID (`AP-*`) for review/post-mortem cross-reference, a risk level, a safe-by-construction rule, and the smallest reversible recovery action. Load this when classifying live findings, running a safety review, or building a post-mortem.

## Contents

1. Unified catalog (ID + class + risk + safe rule + recovery + sources)
2. High-impact Top 3
3. Severity priority
4. Retry policy by error type
5. Reporting schema
6. Contract-check mapping
7. Multiple-failure rule
8. Circuit breaker integration
9. Prevention checklist
10. Quick detection reference

## Unified Catalog

Columns: `ID` = anti-pattern identifier (for review/post-mortem); `Class` = failure-class token used by the runner and reporting schema; `Risk` = primary hazard; `Safe rule` = preventive design rule; `Recovery` = smallest reversible action; `Source` = research citation (METR/NIST/etc.) when applicable.

| ID | Class | Anti-pattern | Risk | Safe rule | Recovery | Source |
|----|-------|--------------|------|-----------|----------|--------|
| `AP-1` | `TOOL_FAILURE` | Infinite retry | resource waste and hidden failures | keep `RETRY_LIMIT <= 5`, default `3`; combine with circuit breaker | apply retry policy; if `RETRY_LIMIT` exhausted, classify `P1`, record `BLOCKED`, hand off via `ORBIT_TO_SCOUT_HANDOFF` | — |
| `AP-2` | `VERIFY_GAP` | Silent SKIP | unauditable `DONE` | generate `verify.sh` from measurable verification commands | classify `P0`, downgrade to `CONTINUE`, generate `verify.sh` and rerun | — |
| `AP-3` | `CONTRACT_MISSING` | Overloaded goal | ambiguous verification | keep one objective per loop | classify `P1`, apply `vague-goal-handling.md`, rewrite goal | — |
| `AP-4` | `TOOL_FAILURE` | Zombie loop | execution blocked by stale lock | auto-clear dead PID locks | clear `.run-loop.lock` if PID is dead; abort if PID is alive | — |
| `AP-5` | `CONTRACT_MISSING` | Immeasurable AC | unverifiable contract | map every AC to a command with deterministic exit code | classify `P1`, rewrite ACs as measurable, regenerate verify commands | — |
| `AP-6` | `CONTRACT_MISSING` | Copy-paste contract | false verification | rewrite ACs for the current goal | classify `P1`, rewrite ACs for this loop's goal | — |
| `AP-7` | `STATE_DRIFT` | Manual state edit | broken audit trail | use `recover.sh`, not manual edits | run `bash recover.sh` to rebuild `state.env` from evidence | — |
| `AP-8` | `STATE_DRIFT` | Partial recovery | `STATE_DRIFT` persists | recover `state.env` and annotate `progress.md` together | run `bash recover.sh`; append recovery note to `progress.md` in same step | — |
| `AP-9` | `COMMIT_SCOPE_RISK` | Global stage | unrelated changes leak into commit scope | snapshot dirty baseline and use scoped staging | classify `P0`, `git reset HEAD -- <baseline_paths>`; resnapshot dirty baseline | — |
| `AP-10` | `VERIFY_GAP` | Premature `DONE` | false completion | require both `done.md` and verify `PASS`/`SKIP` | classify `P0`, downgrade to `CONTINUE`, run verification independently | — |
| `AP-11` | `COMMIT_SCOPE_RISK` | Manual branch switch during active loop | squash failure and misplaced commits | stop the loop before changing branches | suspend affected loop; delegate via `ORBIT_TO_GUARDIAN_HANDOFF` | — |
| `AP-12` | `VALIDATOR_GAP` | Validator gap (stub compiles → DONE) | placeholder code passes verify because tests are too coarse | `verify.sh` must grep `TODO`/`NotImplementedError`/`return None`/`pass` in changed source + run behavioural assertions derived from AC | extend `verify.sh` with placeholder grep + AC-derived behavioural assertions before accepting DONE | dev.to/itsuzef — The Judge Gate |
| `AP-13` | `REWARD_HACK` | Reward hacking via test inspection | agent mutates `tests/` or `verify.sh` to soften assertions ("test cheating") | `tests/` and `verify.sh` are `chmod 0444` + pre-commit rejects any diff touching them + run verify from a separate worktree the loop cannot write | revert tests/verify changes, ABORT loop, escalate; run verify from a write-isolated worktree on retry | metr.org — Recent Reward Hacking; nist.gov — Cheating AI Agent Evaluations |
| `AP-14` | `TOOL_FAILURE` | Worktree cleanup → repo destruction | parallel subagent's cleanup removes parent `.git/`; loop continues on a hollow tree | iter prologue runs `git fsck` + monitors `.git/` inode; cleanup restricted to a path allowlist scoped to the worktree dir | classify `P0`, ABORT loop; restore `.git/` from worktree backup if available; require manual investigation | github.com/anthropics/claude-code — issue #48927 |
| `AP-15` | `CONTEXT_OVERFLOW` | Context poisoning (error log accumulation) | past-iter error traces persist in `goal.md`/scratchpad, later iters treat hallucinated constraints as spec | rotate scratchpad at 60% context, end-of-iter summary keeps decisions only (no failure traces), `goal.md` size is monotonically tracked | apply memory pointer pattern (externalize outputs > 1KB), rotate or summarize context, then retry | mindstudio.ai — Context Rot; dbreunig.com — How Long Contexts Fail; arxiv.org/abs/2511.22729 |
| `AP-16` | `GOAL_DRIFT` | Goal drift / goalpost moving in `goal.md` | agent edits `goal.md` to weaken AC verbs (`must` → `should` → `may`) then claims DONE | `goal.md` and AC files are `chmod 0444` + sha256-pinned at loop start; any change ABORTs the loop | restore from sha256-pinned baseline, ABORT, escalate to human | usewire.io — Agent Drift; lakera.ai — Agentic AI Threats |
| `AP-17` | `BURN_RATE_ANOMALY` | Token burn-rate anomaly (pre-$47k signal) | rate-limit reset triggers exponential consumption, loop burns tokens without artifact change | EWMA burn-rate alert (5-min window vs prior window > 3x → PAUSE) + absolute USD/iter cap + USD/run cap + auto-reload billing disabled | PAUSE, snapshot state, require explicit user resume; never auto-continue | byteiota.com — Uber Claude Code; mfyz.com — Claude Code on Loop |
| `AP-18` | `VALIDATOR_GAP` | Architectural incoherence blindness | verify only checks "works", duplicate impls / layer violations / naming drift accumulate exponentially over 4h+ runs | verify includes architectural lint (`jscpd` duplication, `dependency-cruiser` cycles, `ts-prune` deadcode); thresholds fail the iter | extend `verify.sh` with architectural lint; fail iter on threshold breach | asdlc.io — Ralph Loop pattern |
| `AP-19` | `STATE_DRIFT` | Compaction-induced decision amnesia | auto-compaction discards "why" notes; next iter re-litigates or reverses prior design decisions | pre-compaction extract to append-only `decisions.md` (≤ 30 lines), first iter after compaction is required to read it | restore decisions from `decisions.md`; if missing, escalate for human review | gist — Compaction Memory; cipherbuilds.ai — Day 30 Agent Memory |
| `AP-20` | `PERMISSION_HIJACK` | Permission mode hijack via settings.json | agent rewrites `.claude/settings.json` `permissions.defaultMode` to `bypassPermissions` mid-run; deny rules silently removed | `.claude/settings*.json` sha256-pinned at start; any change ABORTs; verify runs in a separate process with its own settings file | restore baseline settings, ABORT, escalate; treat as P0 security event | cryptika.com — Claude Code rule bypass; repello.ai — Claude Code Security Checklist |
| `AP-21` | `TOOL_FAILURE` | Identical retry without diff (token loop) | same tool call argv repeats N times with no file mtime change; pure token burn (distinct from `AP-1` retry count) | argv-hash dedup: 2 identical hashes in window forces a `reframe` prompt; 3 ABORTs | force `reframe` prompt on 2 duplicates; ABORT on 3; engage circuit breaker | quickleap.io — AI Agents Reasoning Loops; agentpatterns.tech — Infinite Agent Loop |

### Additional `CONTRACT_MISSING` signals (no `AP-*` mapping)

These are runtime-detected contract gaps surfaced by the audit pipeline; they share the `CONTRACT_MISSING` class but are not in the anti-pattern catalog.

| Signal | First response | Recovery |
|--------|----------------|----------|
| `goal.md` missing | classify `P1`, halt execution | `bash bootstrap.sh ${LOOP_DIR}` |
| AC section empty | classify `P1`, trigger `ON_GOAL_CONTRACT_WEAK` | rewrite measurable ACs and verify commands |
| `progress.md` missing or empty | classify `P1`, initialize iteration `0` | append `## Iteration 0 — Bootstrap` |
| `state.env` missing | classify `P1`, rebuild defaults | `bash recover.sh` or create `NEXT_ITERATION=1`, `LAST_STATUS=READY` |
| footer malformed | classify `P1`, re-apply | emit valid `NEXUS_LOOP_STATUS` and `NEXUS_LOOP_SUMMARY` |
| partial template only | classify `P1`, preserve what exists | rebuild missing artifacts only |
| AC not measurable | classify `P1` | apply `vague-goal-handling.md` |

### Additional `STATE_DRIFT` signals

| Signal | First response | Recovery |
|--------|----------------|----------|
| `NEXT_ITERATION` too high | re-sync from `progress.md` | `bash recover.sh` |
| `NEXT_ITERATION` too low | re-sync from `progress.md` | `bash recover.sh` |
| `LAST_STATUS` contradicts `progress.md` | update from evidence | `bash recover.sh` |
| `state.env.sha256` mismatch | treat as corrupted state | auto-run `recover.sh` |
| drift across `2+` consecutive iterations | classify `P0`, pause loop | manual investigation |

### Additional `VERIFY_GAP` signals

| Signal | First response | Recovery |
|--------|----------------|----------|
| `verify.sh` missing | classify `P0`, downgrade to `CONTINUE` | generate `verify.sh` |
| `verify.sh` exits non-zero | classify `P0`, downgrade to `CONTINUE` | rerun `bash verify.sh`, then fix failures |
| `done.md` exists but no verify evidence | classify `P0`, downgrade to `CONTINUE` | run verification independently |
| partial verification pass | classify `P1`, log partial state | continue with failing ACs as focus |
| `VERIFY_RESULT=SKIP` with `done.md` present | classify `P1`, warn | generate verify coverage or re-evaluate the claim |

### Additional `COMMIT_SCOPE_RISK` signals

| Signal | First response | Recovery |
|--------|----------------|----------|
| `dirty-start-paths.txt` missing while `AUTOCOMMIT=true` | classify `P1`, regenerate baseline | resnapshot dirty baseline |
| staged files include baseline paths | classify `P0`, unstage baseline paths | `git reset HEAD -- <baseline_paths>` |
| single-loop candidate scope exceeds goal | classify `P1`, restrict staging | verify each candidate path |
| cross-loop path overlap | classify `P1`, suspend affected loop | delegate via `ORBIT_TO_GUARDIAN_HANDOFF` |
| `git add -A` used with dirty baseline | classify `P0`, revert commit | reset, fix baseline, recommit with scoped staging |

### Additional `TOOL_FAILURE` signals

| Signal | First response | Recovery |
|--------|----------------|----------|
| network timeout / DNS failure | retry with backoff | network-focused retry |
| OOM or disk full | classify `P1`, pause | free resources, recover, resume |
| permission or token error | classify `P1`, pause | refresh credentials, resume |
| `EXEC_TIMEOUT` exceeded | retry once, then `P1` | increase timeout or enable adaptive timeout |
| deterministic non-zero exit | apply retry policy once | escalate to Builder if repeatable |
| `RETRY_LIMIT` exhausted | classify `P1`, record `BLOCKED` | investigate via `ORBIT_TO_SCOUT_HANDOFF` |
| circuit breaker `OPEN` | classify `P1`, record `BLOCKED` | cooldown or manual reset via `recover.sh --reset-circuit` |

## High-Impact Top 3

Apply first when generating new runners; these are the highest-leverage protections.

1. `AP-13` `REWARD_HACK` — METR/NIST 2025-2026 demonstrate this across multiple models. `tests/` immutability is a one-line fix with outsized safety value.
2. `AP-14` Worktree Cleanup — destructive data loss reproducible per Claude Code issue #48927. Inode monitoring is cheap; the alternative is unrecoverable.
3. `AP-17` `BURN_RATE_ANOMALY` — multiple 2026 incidents ($6k overnight, Uber-scale events). EWMA monitoring is orthogonal to existing `RETRY_LIMIT` and `TOKEN_BUDGET`.

## Severity Priority

| Severity | Classes / scenarios | Action |
|----------|---------------------|--------|
| `P0` | false `DONE`, destructive commit-scope risk, escalated drift, `REWARD_HACK`, `GOAL_DRIFT`, `PERMISSION_HIJACK`, `AP-14` worktree destruction | stop and confirm |
| `P1` | drift, contract gaps, retry exhaustion, `BURN_RATE_ANOMALY` (pause + human resume) | recover then continue |
| `P2` | intermittent tool failure within retry budget | retry policy |

## Retry Policy by Error Type

Errors are classified into two categories for retry policy:

| Category | Examples | Retry behavior | Backoff |
|----------|----------|----------------|---------|
| `TRANSIENT` | network timeout, DNS failure, API rate limit, OOM (after cleanup), `EXEC_TIMEOUT` exceeded | retry up to `RETRY_LIMIT` | exponential with jitter: `base^attempt + random(0, base^attempt * 0.5)` |
| `PERMANENT` | permission/token error, invalid input, deterministic non-zero exit, schema violation | no retry; escalate immediately | — |

Detection heuristics:

| Signal | Category | Rationale |
|--------|----------|-----------|
| exit code `124` (timeout) | `TRANSIENT` | timeout is environment-dependent |
| exit code `1` on consecutive identical input | `PERMANENT` | deterministic failure |
| exit code `137` (OOM killed) | `TRANSIENT` | memory pressure may be temporary |
| HTTP `429`, `502`, `503` in stderr | `TRANSIENT` | server-side rate limit or outage |
| HTTP `401`, `403` in stderr | `PERMANENT` | credentials or permissions issue |
| identical error message `3` consecutive times | `PERMANENT` | upgrade from transient to permanent |

When a `TRANSIENT` error is retried `3` consecutive times with the same error signature, it is reclassified as `PERMANENT` and the circuit breaker is engaged (see § Circuit Breaker Integration).

## Reporting Schema

```yaml
ORBIT_FAILURE_REPORT:
  class: "<taxonomy class>"
  anti_pattern_id: "<AP-* if applicable>"
  severity: "P0|P1|P2"
  sub_class: "<specific signal>"
  retry_category: "TRANSIENT|PERMANENT"
  circuit_state: "CLOSED|HALF_OPEN|OPEN"
  evidence:
    - "<file:line>"
  impact: "<what breaks>"
  recommendation: "<smallest reversible action>"
  recovery_cmd: "<command>"
```

## Contract-Check Mapping

| Contract score | Finding | Failure class | Severity | Next action |
|----------------|---------|---------------|----------|-------------|
| Missing | `goal.md` missing | `CONTRACT_MISSING` | `P1` | rebuild in bootstrap mode |
| Missing | `progress.md` empty | `CONTRACT_MISSING` | `P1` | initialize iteration `0` |
| Missing | `state.env` missing | `CONTRACT_MISSING` | `P1` | generate defaults |
| Partial | footer missing or malformed | `CONTRACT_MISSING` | `P1` | repair footer |
| Partial | state and timeline mismatch | `STATE_DRIFT` | `P1` | resync from progress evidence |
| Partial | `done.md` present and verify evidence unclear | `VERIFY_GAP` | `P0` | downgrade to `CONTINUE` |
| Partial | candidate scope may include baseline paths | `COMMIT_SCOPE_RISK` | `P0` | hand off to Guardian |
| Partial | `runner.log` contains failure entries | `TOOL_FAILURE` | `P2` | retry policy and environment check |
| Complete | retry budget exhausted | `TOOL_FAILURE` | `P1` | investigate via Scout |
| Complete | artifacts consistent | none | — | continue safely |

## Rules for Multiple Failure Classes

- Process the highest severity first.
- `P0` always preempts `P1` and `P2`.
- Use one handoff at a time.
- Record remaining issues as pending issues for the next audit cycle.

## Circuit Breaker Integration

When the same failure signature (class + sub_class + error message hash) occurs `CIRCUIT_THRESHOLD` times (default `3`):

| State | Condition | Behavior |
|-------|-----------|----------|
| `CLOSED` | `< CIRCUIT_THRESHOLD` consecutive same-signature failures | normal retry policy applies |
| `HALF_OPEN` | exactly `CIRCUIT_THRESHOLD` consecutive same-signature failures | allow one probe execution; if it fails, transition to `OPEN` |
| `OPEN` | `> CIRCUIT_THRESHOLD` consecutive same-signature failures or probe failed | stop execution, emit `BLOCKED` status, require manual reset or cooldown |

Cooldown: `OPEN` state auto-transitions to `HALF_OPEN` after `CIRCUIT_COOLDOWN` seconds (default: `300`).

Reset: manual reset via `recover.sh --reset-circuit` or by clearing `${LOOP_DIR}/.circuit-state`.

Reporting: circuit breaker state changes are logged in the structured log (see `script-template-runner.md § Structured Logging`).

## Prevention Checklist

Run before launching a loop:

- [ ] `RETRY_LIMIT` is set and `<= 5`
- [ ] `verify.sh` exists and covers all acceptance criteria
- [ ] `goal.md` has exactly one objective
- [ ] no stale `.run-loop.lock` exists
- [ ] every AC maps to a deterministic command
- [ ] ACs were written for this loop, not copied from another
- [ ] `state.env` has not been edited manually
- [ ] `state.env` and `progress.md` are consistent
- [ ] `dirty-start-paths.txt` exists when `AUTOCOMMIT=true`
- [ ] the `DONE` gate requires `done.md` and verify `PASS`/`SKIP`
- [ ] no manual `git checkout` will happen during active `BRANCH_ISOLATION`
- [ ] `verify.sh` includes a placeholder-detection step (TODO / `pass` / `NotImplementedError`)
- [ ] `tests/` and `verify.sh` are read-only or protected by pre-commit
- [ ] `git fsck` and `.git/` inode monitoring run at iter start under `WORKTREE_ISOLATION`
- [ ] scratchpad rotation policy is set; `goal.md` size is tracked iter-over-iter
- [ ] `goal.md` and AC files are sha256-pinned and read-only
- [ ] `BURN_RATE_THRESHOLD`, `USD_PER_ITER_CAP`, `USD_PER_RUN_CAP` are configured; auto-reload billing is disabled
- [ ] `verify.sh` includes architectural lint (duplication / cycles / dead code)
- [ ] `decisions.md` (append-only) is referenced; first post-compaction iter re-reads it
- [ ] `.claude/settings*.json` sha256-pinned at loop start
- [ ] tool-call argv dedup is active (last `DEDUP_WINDOW` calls hashed)

## Quick Detection Reference

| ID | Detection |
|----|-----------|
| `AP-1` | `RETRY_LIMIT > 5` or unset |
| `AP-2` | `verify.sh` missing |
| `AP-3` | multiple objectives in `goal.md` |
| `AP-4` | `.run-loop.lock` with dead PID |
| `AP-5` | AC without command mapping |
| `AP-6` | ACs unrelated to current goal |
| `AP-7` | `state.env` changed without recovery note |
| `AP-8` | `state.env` / `progress.md` mismatch |
| `AP-9` | `git add -A` with dirty baseline |
| `AP-10` | `DONE` with `VERIFY_RESULT=FAIL` |
| `AP-11` | `git checkout` during active branch-isolated loop |
| `AP-12` | placeholder tokens (`TODO`, `pass`, `NotImplementedError`) in changed src with verify PASS |
| `AP-13` | `tests/` or `verify.sh` modified in same iter as `src/` |
| `AP-14` | `git rev-parse --git-dir` fails at iter start, or `.git/` inode changed |
| `AP-15` | `goal.md` size strictly increasing across 3+ iters, or same error string in 3+ iters |
| `AP-16` | `goal.md`/AC sha256 changed mid-run |
| `AP-17` | 5-min token rate > 3x prior window, or USD/iter > cap |
| `AP-18` | `jscpd`/`dependency-cruiser`/`ts-prune` threshold exceeded |
| `AP-19` | post-compaction iter produces diff > 2x baseline, or ADR contradicts implementation |
| `AP-20` | `.claude/settings*.json` sha256 changed mid-run |
| `AP-21` | last `DEDUP_WINDOW` tool argv hashes contain a duplicate with no mtime change |
