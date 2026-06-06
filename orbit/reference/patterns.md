# Orbit Patterns

Purpose: load this when multi-loop coordination, dirty-baseline protection, or handoff structure matters. These are reusable operating patterns, not script templates.

## Contents

1. Contract-first stabilization
2. Evidence-gated done
3. Dirty-baseline safe commit
4. Resume drift recovery
5. Parallel-loop conflict detection
6. Sequential-loop handoff
7. Loop-of-loops isolation
8. Dirty-baseline edge cases
9. Pre-flight health gate
10. Ralph two-mode switching (plan / build)
11. Worktree-per-iteration isolation
12. Independent critic gate
13. Prompt cache breakpoint layout

## 1. Contract-First Stabilization

Use when loop behavior is unstable or non-deterministic.

1. Validate artifact presence and schema.
2. Validate footer semantics.
3. Validate resume consistency.
4. Only then propose implementation fixes.

## 2. Evidence-Gated DONE

Use when `DONE` is claimed.

- Require acceptance checklist mapping.
- Require verification commands and outcomes.
- Require rollback note for the latest mutation.
- If any are missing, recommend `CONTINUE`.

## 3. Dirty-Baseline Safe Commit

Use when the worktree was dirty before loop start.

1. Snapshot baseline dirty paths.
2. Build candidate paths from current delta.
3. Exclude baseline paths.
4. Stage and commit candidate paths only.

## 4. Resume Drift Recovery

Use when `state.env` and the progress timeline disagree.

1. Parse the latest iteration record from `progress.md`.
2. Compare it with `NEXT_ITERATION` and `LAST_STATUS`.
3. Reconstruct state from the evidence source.
4. Annotate the recovery decision and reason.

## 5. Parallel Loop Commit Scope Conflict Detection

Use when multiple active loops may touch overlapping paths.

```bash
# 1. Enumerate active loops (collect loop dirs with LAST_STATUS=CONTINUE)
active_loops=$(find . -name "state.env" -exec grep -l "LAST_STATUS=CONTINUE" {} \; | xargs dirname)

# 2. Extract candidate paths per loop (changes excluding baseline delta)
for loop_dir in $active_loops; do
  git diff --name-only | sort | comm -23 - "${loop_dir}/dirty-start-paths.txt" \
    > "${loop_dir}/.candidate-paths.tmp"
done

# 3. Detect overlapping paths -> report CROSS_LOOP_CONFLICT
cat */.candidate-paths.tmp | sort | uniq -d > .conflict-paths.tmp
if [[ -s .conflict-paths.tmp ]]; then
  echo "CROSS_LOOP_CONFLICT: $(cat .conflict-paths.tmp)"
fi
```

On `CROSS_LOOP_CONFLICT`:
1. Suspend the affected loop and keep `LAST_STATUS=CONTINUE`.
2. Delegate commit-order arbitration via `ORBIT_TO_GUARDIAN_HANDOFF`.
3. Skip commit processing until the conflict is resolved.

## 6. Sequential Loop Handoff Implementation Guide

### Append checklist to predecessor `done.md`

```markdown
## Handoff Checklist (for successor loop)
- [ ] Criterion 1: <verified by: command>
- [ ] Criterion 2: <verified by: command>
- [ ] Artifacts produced: <file list>
- [ ] Known limitations: <list>
```

### Link prerequisites in successor `goal.md`

```markdown
## Prerequisites (from predecessor loop)
- Loop: <predecessor loop dir>
- Done file: <path/to/done.md>
- Verified criteria:
  - [ ] Criterion 1: `<verification command>`
  - [ ] Criterion 2: `<verification command>`

> Orbit MUST validate each prerequisite independently before proceeding.
```

Rules:
- Always inspect prerequisites during successor-loop intake.
- Existence of predecessor `done.md` alone is insufficient.
- If any prerequisite is unverified, classify `CONTRACT_MISSING`.

## 7. Loop-of-Loops Isolation Rule

| Operation | Meta-loop allowed? | Reason |
|-----------|--------------------|--------|
| Consume inner `_STEP_COMPLETE` | Yes | designed communication channel |
| Read inner `state.env` | Read-only only | status check |
| Write inner `state.env` | No | induces `STATE_DRIFT` |
| Append to inner `progress.md` | No | contaminates evidence |
| Delete or move inner `done.md` | No | destroys evidence |
| Force-terminate inner loop | Guardian approval required | impact must be assessed |
| Classify inner failures independently | Yes | prevents contamination of outer state |

Principle: the meta-loop observes inner loops; it does not intervene in their state.

## 8. Dirty Baseline Edge Cases

| Case | Problem | Mitigation |
|------|---------|------------|
| Partial path match | baseline prefix matches loop artifact path | exact-line `comm -23` already helps; verify dirty subdirectories manually |
| Same file modified by parallel loops | conflict may slip through | use Pattern 5 and delegate to Guardian |
| Gitignored tracked files | `git check-ignore` does not hide tracked files | maintain an explicit exclusion list |
| Symlink or submodule | path reporting may be confusing | record the symlink path itself; use `--ignore-submodules=all` when needed |

## 9. Pre-flight Health Gate

Pre-flight checks before the main loop:
1. disk space `>= 100MB`
2. no active `.run-loop.lock` or auto-clear stale lock
3. no git rebase in progress when `AUTOCOMMIT=true`
4. rotate `runner.log` above `MAX_LOG_SIZE`
5. validate `state.env.sha256`

Iteration health checks:
1. disk space `>= 50MB`
2. git rebase status still safe for auto-commit
3. log rotation check

## 10. Ralph Two-Mode Switching (plan / build)

Use when generating a Ralph-style runner (see `ralph-loop-pattern.md` for full design rules).

```bash
# Mode dispatcher in run-loop.sh
mode_file="${LOOP_DIR}/.ralph-mode"
[[ -f "$mode_file" ]] || echo "plan" > "$mode_file"
current_mode=$(cat "$mode_file")

case "$current_mode" in
  plan)  prompt_file="PROMPT_plan.md" ;;
  build) prompt_file="PROMPT_build.md" ;;
esac

cat "$prompt_file" | $EXEC_CMD

# Mode switch after iteration
fix_plan_items=$(grep -c '^- \[ \]' fix_plan.md 2>/dev/null || echo 0)
case "$current_mode" in
  plan)
    [[ $fix_plan_items -ge 1 ]] && echo "build" > "$mode_file"
    ;;
  build)
    if [[ $fix_plan_items -eq 0 ]] || \
       grep -q "CONVERGENCE_STALL\|OSCILLATION_LOOP" "${LOOP_DIR}/state.env"; then
      echo "plan" > "$mode_file"
      # Archive disposable plan on re-entry
      cp fix_plan.md "IMPLEMENTATION_PLAN_archive_$(date -u +%Y%m%dT%H%M%SZ).md"
    fi
    ;;
esac
```

Rules:
- `PROMPT_plan.md` may write `fix_plan.md`, `IMPLEMENTATION_PLAN.md`; must not touch source or tests.
- `PROMPT_build.md` may write source, tests, `progress.md`; must not touch spec, plan, AGENTS.md.
- Mode flips on empty plan, convergence stall, or oscillation; never on a single failed iter.

## 11. Worktree-per-Iteration Isolation

Use when `WORKTREE_ISOLATION=true` (default for Ralph-style runners; recommended for any unattended loop).

```bash
# Per-iteration worktree
iter_id="iter-$(date -u +%Y%m%dT%H%M%SZ)-$$"
worktree_dir="${LOOP_DIR}/.worktrees/${iter_id}"
branch_name="orbit/${LOOP_NAME}/${iter_id}"

git worktree add -b "$branch_name" "$worktree_dir" HEAD

# Run iteration inside the worktree
( cd "$worktree_dir" && $EXEC_CMD < "$prompt_file" )
iter_status=$?

# Verify still runs against the worktree
( cd "$worktree_dir" && ./verify.sh )
verify_status=$?

if [[ $iter_status -eq 0 && $verify_status -eq 0 ]]; then
  # Squash-merge worktree branch into iteration branch
  git -C "$worktree_dir" log --oneline HEAD^..HEAD
  git merge --squash "$branch_name"
  git commit -m "iter: ${iter_id}"
  git worktree remove "$worktree_dir"
  git branch -D "$branch_name"
else
  # Preserve for forensic inspection
  echo "FAILED_WORKTREE=$worktree_dir" >> "${LOOP_DIR}/runner.log"
fi
```

Guarantees:
- Iteration cannot mutate the parent worktree's `.git/`, `tests/`, or `verify.sh` if they are sha256-pinned in the parent.
- Rollback is `git worktree remove` — no `git reset --hard`, no risk of `.git/` corruption (AP-14).
- Parallel loops share the same `.git/` safely via worktree isolation rather than separate clones.

## 12. Independent Critic Gate

Use as part of the `VERIFY` phase before the DONE Evidence Gate.

```bash
# Run primary iteration with PRIMARY_MODEL
primary_output=$(cat "$prompt_file" | claude --model "$PRIMARY_MODEL")

# Independent critic with different model + different system prompt
critic_prompt=$(cat <<EOF
You are an independent code reviewer. The agent below claims iteration $iter_id
is complete. Your job is to find reasons it is NOT complete.

ITERATION OUTPUT:
$primary_output

CHECK FOR:
1. Placeholders, stubs, NotImplementedError, return None, pass (AP-12)
2. Tests modified to soften assertions (AP-13)
3. Goal/AC files modified (AP-16)
4. Architectural drift, duplicates, dead code (AP-18)

Output a single line: APPROVE | REJECT: <one-line reason>
EOF
)
critic_verdict=$(echo "$critic_prompt" | claude --model "$CRITIC_MODEL" --system "Be skeptical. Default to REJECT when in doubt.")

if [[ "$critic_verdict" =~ ^APPROVE ]]; then
  # Advance to DONE Evidence Gate
  ./verify.sh && [[ -f done.md ]] && echo "DONE"
else
  # Critic rejection downgrades to CONTINUE; record reason
  echo "CRITIC_REJECT: $critic_verdict" >> progress.md
  echo "CONTINUE"
fi
```

Rules:
- `CRITIC_MODEL` must differ from `PRIMARY_MODEL` (e.g. `haiku` reviewing `opus` output).
- Critic system prompt is skeptical by default; the agent does not control it.
- Critic rejection blocks DONE but does not abort the loop; it forces another iteration with the rejection reason injected into `progress.md`.

## 13. Prompt Cache Breakpoint Layout

Use when generating any runner prompt. Aim for `PROMPT_CACHE_BREAKPOINTS=4` placed at stable boundaries; the goal is `>= 85%` cache hit on the static prefix.

Layout (top-to-bottom, breakpoints after each labelled block):

```
[BLOCK 1: system instructions] ← cache_control breakpoint 1 (most stable)
[BLOCK 2: tool schemas / MCP defs] ← cache_control breakpoint 2
[BLOCK 3: goal.md + AC + 9xx rules] ← cache_control breakpoint 3
[BLOCK 4: recent progress.md tail (last N iters)] ← cache_control breakpoint 4
[BLOCK 5: current iteration directive] ← uncached (changes every iter)
```

Rules:
- Breakpoints 1 and 2 should not change for the entire loop run.
- Breakpoint 3 changes only when `goal.md` legitimately evolves; `GOAL_IMMUTABLE=true` keeps this stable.
- Breakpoint 4 contains the *tail* of `progress.md` (last 5-10 iters), not the full history; older iters live on disk for the agent to read on demand.
- Block 5 is the only variable section — typically a 1-3 line directive like `Current iteration: pick the top item from fix_plan.md and implement.`

Verification:
- After 3+ iterations, total cache_read_input_tokens / (cache_read + uncached_input) should be `>= 0.85`. Below `0.5` indicates a breakpoint is on an unstable block.
