# Hooks in Loop Engineering — Automation Context

Where Claude Code **hooks** sit inside the **loop engineering** pattern. Hooks are one of the heartbeat/automation primitives a loop is built from — useful framing when a user wants "a hook that runs X on a schedule / at lifecycle points" as part of an autonomous loop. For the loop concept and primitives map see `nexus/reference/loop-engineering-primitives.md` and `orbit/reference/loop-engineering.md`.

> Snapshot date: 2026-06-11. Fast-moving topic; verify feature versions against `code.claude.com/docs` before quoting.

## The loop = parts, hooks are one heartbeat option

A loop engineering setup combines: scheduled execution + isolated workspaces + maker/checker verification + persistent memory. Claude Code offers several ways to drive the **scheduled/automation** part:

| Automation primitive | What it is | When to reach for it |
|----------------------|-----------|----------------------|
| `/loop` | Re-runs a prompt/command on a cron cadence (v2.1.72+) | Whole-session recurring task on a timer |
| `/goal` | Runs until a verifiable condition holds; fresh fast model checks completion each turn | Bounded autonomous run with a stop condition |
| **hooks** (Latch's domain) | Shell/prompt/http/agent commands fired at lifecycle events (PreToolUse, PostToolUse, Stop, SessionStart, …) | Per-event reactions *inside* the loop — gates, logging, context injection, completion enforcement |
| GitHub Actions | Push the loop to CI so it survives the laptop closing | Long-running unattended loops |

Hooks are **not** the timer — they are the per-event glue that makes each loop iteration behave: a `Stop`/`SubagentStop` hook can enforce a quality gate before "done", a `PreToolUse` hook can block reward-hacking edits (e.g. mutating `tests/` mid-loop), a `SessionStart` hook can re-inject the loop's memory/state, and a `Notification` hook can route findings to the triage inbox.

## How this informs Latch hook design

- **Completion enforcement** (`Stop`/`SubagentStop`, recipe `Q*`): in a maker/checker loop, a blocking Stop hook is a deterministic, model-independent complement to `/goal`'s fresh-model checker — exit-2 if verification evidence is absent. Don't trust verify-PASS alone.
- **Loop integrity guards** (`PreToolUse` deny, see `security-guard-hook.md`): unattended loops are exactly where reward-hacking and goal-drift happen. A PreToolUse hook that denies writes to sha256-pinned loop artifacts (`tests/`, `verify.sh`, `goal.md`, `.claude/settings*.json`) hardens a loop against AP-13/AP-16/AP-20 (Orbit failure classes).
- **Memory re-injection** (`SessionStart`, see `sessionstart-hook.md`): "the agent forgets, the repo doesn't" — a SessionStart hook can load `state.env`/`progress.md` so each loop iteration resumes with its persistent memory.
- **Findings routing** (`Notification`, see `notification-hook.md`): surface loop discoveries to a human/triage channel so an unattended loop stays auditable.
- **Cost/governance** (`ConfigChange`, `PreToolUse`): unmonitored loops have escalated cost dramatically (documented runaways). Hooks can audit config changes and flag burn-rate-relevant actions.

## Evaluator & cost guards as hooks (Osmani/HuaShu framing, 2026-06)

The Orange Book (*Loop Engineering: The Anthropic Playbook*, HuaShu IEEE reformatting) names three loop disciplines that hooks can enforce deterministically — a model-independent complement to `/goal`'s fresh-model checker:

- **Evaluator must act, not read** (Rajasekaran, Anthropic): a `Stop`/`SubagentStop` hook can require *execution evidence* (test output pasted, screenshot captured) before allowing "done", and default to assume-broken (exit-2 unless proof is present). The maker praises its own work; the hook is the skeptic that can't be talked out of it.
- **Cap before you ship** (token-blowout guard): a `PreToolUse`/`ConfigChange` hook audits budget-relevant actions so an idle bug can't burn a night's quota — the cap converts open-ended risk into a bounded one.
- **Keep one door open** (cognitive-surrender guard): a `Notification` hook routes uncertain findings to a human/triage inbox rather than auto-merging — the structural pause that keeps a human able to say "no".

Of the five anti-patterns (one per skipped move — see `orbit/reference/loop-engineering.md`), hooks directly harden three: **Nodding** (verification-gate `Stop` hook), **Token blowout** (cap `PreToolUse` hook), and **Tangled** (a `PreToolUse` deny on cross-worktree writes). Scheduling (the **Manual** anti-pattern) is *not* a hook's job — that's `/loop`/Cloud Routines/GHA.

## Boundary

Latch owns the **hook** primitive only. The loop's cadence/contract/recovery belongs to **Orbit**; multi-engine orchestration to **Nexus**. When a request is "build me the whole loop," route the loop design to Orbit/Nexus and supply the hooks they need.

## Caveat

No public verifiable ROI study for loop engineering exists yet — propose hooks for correctness/safety/auditability, not on a promise of efficiency gains.
