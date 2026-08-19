# Loop Engineering — Concept, Lineage, and Applicability

External context for *why* a loop exists, *who* shaped the pattern, and *when not to build one*. Orbit owns the mechanics (contracts, scripts, recovery); this file owns the framing that decides whether a loop is the right answer at all.

> Snapshot date: 2026-06-29 (refreshed; previously 2026-06-11). Fast-moving topic — term and feature versions can shift within weeks. Verify version numbers against primary docs before quoting.

## Definition

**Loop engineering** = replacing *yourself as the person who prompts the agent* with a system that does the prompting. A loop is a **recursive goal**: define a purpose, let the agent iterate until a verifiable stop condition holds. It is an orchestration pattern that combines four parts:

1. **Scheduled/recurring execution** (the heartbeat)
2. **Isolated workspaces** (parallel agents don't collide)
3. **Verification agents** (a checker separate from the maker)
4. **Persistent memory** (state outside the conversation, on disk)

This is exactly Orbit's territory: 1 → `run-loop.sh` cadence, 2 → `git worktree` isolation, 3 → independent `CRITIC_MODEL` DONE gate, 4 → `state.env` / `progress.md` / `done.md` filesystem-as-memory.

## Lineage (who said what)

| Person | Role | Claim | Confidence |
|--------|------|-------|------------|
| **Peter Steinberger** (@steipete) | OpenClaw steward | "You shouldn't be prompting coding agents anymore. You should be designing loops that prompt your agents." Runs a supervisory multi-agent loop (`claw` supervising multiple Codex instances). OpenClaw's verified architecture maps two loop parts directly: **heartbeat** = periodic main-session turn (default 30 min; `docs.openclaw.ai/gateway/heartbeat`) → part 1; **persistent SQLite state DB** (own PR #78595, 2026-05-13) → part 4. The loop-engineering quote is general, not an OpenClaw-architecture statement. | high |
| **Boris Cherny** (@bcherny) | Creator / head of Claude Code, Anthropic | "I don't prompt Claude anymore. I have loops running that prompt Claude… My job is to write loops." Reported (Fortune, 2026-06-08) to have not written code for ~8 months while supervising tens of thousands of agents. | high |
| **Addy Osmani** | Google engineer | **Named** (not invented) the pattern "loop engineering" in a blog post on 2026-06-07 (reposted to O'Reilly Radar 2026-06-22 with permission — mainstream amplification). Stresses "Verification is still on you." | high |

- Primary sources: addyosmani.com/blog/loop-engineering (reposted oreilly.com/radar/loop-engineering, 2026-06-22), thenewstack.io/loop-engineering, developers.openai.com/codex/subagents, code.claude.com/docs, docs.openclaw.ai.
- Note: X/Twitter source URLs return HTTP 402 (text confirmed via Fortune / Lenny's / Digg secondaries). Steinberger's exact claw→Codex topology mechanics (prompt handoff, stop conditions, cost control) remain undisclosed.

## When NOT to build a loop (applicability limits)

A loop is *not* always the right answer. For one-off tasks, a single well-aimed prompt is faster and cheaper. Skip loops when:

1. **Solo builder on a consumer usage-based plan** — token cost dominates; loop ROI is unproven (no public verifiable case study exists yet — and *PR acceptance rate is not ROI*: AIDev's 7,156-PR analysis, arXiv:2602.08915, finds acceptance is dominated by **task type** — documentation 82.1% vs new features 66.1% — and the authors themselves note acceptance rate ≠ code quality).
2. **The code has no automated verification** — an unattended loop is a loop making mistakes unattended; without a real checker, "done" is a claim, not a proof.
3. **The real constraint is review capacity, not typing speed** — loops lengthen the review queue rather than shortening delivery.

These map to Orbit guardrails already in the SKILL: external termination enforcement, independent `CRITIC_MODEL` DONE gate (never trust verify-PASS alone — see AP-12/AP-18), and `USD_PER_RUN_CAP` / `BURN_RATE_ANOMALY` cost caps.

Confidence on this section: medium (critique synthesized largely from secondary sources, e.g. AlphaSignal 2026-06-08). Treat as directional, not absolute. The stronger claim "loops only pay off when all four of {weekly repetition, automated verification, slack token budget, senior-engineer tooling} hold" was weakly refuted in verification (1-2) — necessary-condition framing is too strict.

## Canonical loop shapes (verified 2026-06-15)

Two well-documented loops anchor the design space — one official, one community:

- **evaluator-optimizer** (Anthropic, *Building Effective Agents* + cookbook): a generator LLM produces, a *separate* evaluator LLM returns PASS or feedback inside the loop; **PASS is the only exit** (`while True: if evaluation == "PASS": return result` — no max-iteration cap by itself), and feedback folds into the next generation's context. This is the maker/checker split as a control loop.
- **Ralph** (Geoffrey Huntley / HumanLayer origin; `snarktank/ralph` reference impl): a bash `while` loop re-piping a static prompt into a fresh agent instance. The load-bearing ideas, all verified:
  - **Fresh context per iteration** — state lives *outside* the conversation: git history + `progress.txt` + `prd.json`, not in-context memory.
  - **Per-iteration cycle is observe → decide → act → verify**: pick the highest-priority `passes:false` story → implement *one* → run typecheck/tests → commit only if green → update `prd.json` / append `progress.txt`.
  - **Loop-until-done via completeness sentinel**: when all stories are `passes:true`, the agent emits `<promise>COMPLETE</promise>` and the loop `grep`s for it to exit. (The original Huntley one-liner had *no* auto-exit — operator stopped it by hand; later variants added Stop-hook / max-iterations / sentinel exits.) **Anthropic shipped an official Stop-hook Ralph plugin** — `anthropics/claude-code` → `plugins/ralph-wiggum/` ("Made by Anthropic / Anthropic Verified"), to the public marketplace on **2025-11-16** (commonly misdated "Dec 2025"); its `hooks/stop-hook.sh` intercepts session exit and re-feeds the same prompt. Two-layer relationship: technique = community (Huntley), packaged plugin = Anthropic-official.
  - **The loop only functions with a real verification gate** (typecheck/tests/green CI). No checker → broken code compounds across iterations. Each story must fit in one context window.

**Drift / "overbaking"** is the signature failure of running too long: bizarre emergent scope creep (the canonical anecdote: a loop adding unrequested post-quantum crypto). Mitigation that practitioners converge on — **bound the loop**: tight spec, iteration/time limit, acceptance tests, and for desired-state loops, **run ONCE on an overnight cron merging small increments** rather than unbounded continuous runs. (Mitigation = practitioner consensus.) **Drift is now partially benchmarked**: SlopCodeBench (arXiv:2603.24755, Anthropic + UW-Madison, 2026-03) measures systematic decay across iterative checkpoints — **structural erosion in 77% of trajectories, verbosity in 75.5%** — accumulating *independently of test-passing* ("code can pass the test suite but become progressively harder to extend"). Caveat: figures vary across paper versions (v1 HTML: 80%/89.8%), and the paper measures spec-evolving self-extension (not a maker/checker loop) — the tie to loop engineering is a reasonable extrapolation, not the paper's own claim. Confidence: medium.

> Refuted in verification — do not repeat: `/loop` "expires after 3 days" (it's **7 days**); Ralph being "cost-efficient at ~$10-12/hr indefinitely"; "frequent context resets/compaction are *essential* to loop reliability" (fresh-context-per-iteration is one valid design, not a universal requirement); ChatGPT iOS 1.2026.160 (2026-06-15) "adding worktree creation / `/goal` to Codex Mobile" (refuted 1-2); the "Peng et al. 55.8% faster vs METR −19% slower" pairing cited as loop-ROI evidence (refuted 1-2); SlopCodeBench "best agent passes only 14.8% of checkpoints / solves no problem end-to-end" (version-confused figures, refuted 1-2); "explicit quality guidance cuts initial degradation ~⅓ but not the degradation *rate*" (refuted 1-2).

## Five anti-patterns — one per skipped move (Osmani/HuaShu, 2026-06)

The Orange Book (HuaShu IEEE reformatting, *Loop Engineering: The Anthropic Playbook*) frames a loop's turn as five moves (discovery, handoff, verification, persistence, scheduling). Each failure mode is exactly one move skipped — and maps onto an Orbit guardrail.

| Anti-pattern | Skipped move | Symptom | Orbit guard |
|--------------|--------------|---------|-------------|
| **Nodding loop** (most common) | Verification | self-approved output; "never said no in hundreds of turns" | independent `CRITIC_MODEL` DONE gate — never trust verify-PASS alone (AP-12/AP-18) |
| **Amnesiac loop** | Persistence | no cumulative progress; restarts from the same place each morning | `state.env`/`progress.md` filesystem-as-memory |
| **Manual loop** | Scheduling | silently stops when attention wanders | `run-loop.sh` cadence / a real cron/event trigger |
| **Blind loop** | Discovery | human still spends the morning picking the work | discovery logic in a *skill*, not a pasted list |
| **Tangled loop** | Handoff | parallel agents edit one dir; merge is unanswerable | `git worktree` isolation, one per task |

These cluster: a loop careless about one check is usually careless about others. Hasty loops install only discovery + handoff (the two that produce *visible* output) and skip the three that produce *safety*.

> **New term (2026-06, not yet established):** "**loopmaxxing**" (Ben Dickson, TechTalks, 2026-06-22) — running an agent through an *infinite* execution cycle on a subjective, non-quantifiable goal ("improve the UX of this login page"), which "strips the system of a concrete exit condition" and "convert[s] cloud infrastructure budgets into large API bills without advancing toward a measurable solution." Framed as the successor to "tokenmaxxing." It is the Manual/Nodding-loop pair with the *exit condition* itself missing. Caveat: single-source coinage so far — not yet in wider AI use (other web hits are unrelated gaming slang).

## Four silent costs (they reinforce each other)

A loop that runs itself is a loop that errs quietly. Four costs accrue with no alarm, and each feeds the next (verification debt → comprehension rot → cognitive surrender → token blowout → more unverified output):

- **Verification debt** — unverified output piling up between "runs" and "right"; guard = an independent evaluator (a different agent from the maker).
- **Comprehension rot** — the gap between code written and code understood; guard = read a representative sample daily and force yourself to explain each change.
- **Cognitive surrender** — "no longer want to bother" deciding; guard = keep the capacity to say "this is wrong" (the loop can execute, it cannot decide).
- **Token blowout** — an idle bug burning a night's quota; guard = hard caps set *before* the first unattended run (`USD_PER_RUN_CAP` / `BURN_RATE_ANOMALY`).

**Operational discipline (three standing practices):** Read a Sample Always · Cap Before You Ship · **Keep One Door Open** (build at least one checkpoint where the loop pauses for a human — the pause keeps a human *able* to say no, even if they rarely do).

**Economics of judgment:** loops make generation abundant (code, plans, PRs near-free) and leave *judgment* as the only scarce resource. A loop is a faithful multiplier — the same loop built by two people yields opposite outcomes, separated by one or two checkpoints. Design it "like someone who intends to stay the engineer, not the one who presses go."

**Enterprise structural lesson (Stripe's Minions, 1,300+ PRs/week — up from ~1,000 in Part 1 — human-reviewed, zero hand-written):** reliability comes from the *quality of the constraints, not the size of the model* — Minions runs on a fork of open-source **Goose** (not Claude Code / Codex, not a stronger model). Its **"Blueprints"** interleave *deterministic* workflow nodes (git / lint / test) with *agentic* nodes (implement task / fix CI), and CI iteration is **deliberately capped** (local lint loop → 1 CI run + autofix → one more local fix → hand to human) on an explicit *diminishing-marginal-returns* rationale. A deterministic orchestrator assembles context *before* the LLM wakes; rule-bound work is kept out of the probabilistic model and behind hard-coded gates. This is the same "bound the loop" discipline above, applied at scale. (Sources dated 2026-02; metrics self-reported, not externally audited.)

## How this informs Orbit decisions

- At `INTAKE`/`CONTRACT`: if the goal matches a "skip a loop" case above, say so and recommend a direct prompt instead of generating a runner. A loop with no automated verification command should fail `ON_GOAL_CONTRACT_WEAK`.
- At `CONTRACT`: the maker/checker split is the load-bearing primitive — it is what makes "I can walk away" true. This is the same idea as Claude Code `/goal` (a fresh fast model decides completion) applied to the stop condition itself.
- At `HANDOFF`/`LEARN`: when no verifiable ROI evidence exists for the loop class, record it as an open risk rather than asserting efficiency gains.
