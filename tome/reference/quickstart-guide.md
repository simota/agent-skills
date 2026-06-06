# Quickstart Guide Reference

Purpose: Author a ≤15-minute path to first success. The quickstart's only job is delivering a single visible win — running output, served page, returned API response — fast enough that the user does not abandon. Every minute beyond 15 multiplies drop-off.

## Scope Boundary

- **tome `quickstart` (this command)**: time-boxed first-success path. Filters prerequisites aggressively, validates success at each checkpoint.
- **tome `learn` (default)**: explanation-oriented learning doc from a diff. Quickstart is action-oriented and minimal-explanation.
- **tome `diff`**: diff-to-teaching transformation. Quickstart is product-onramp, not change-driven.
- **tome `onboard`**: comprehensive new-member material with beginner depth. Quickstart is narrower — one path to one win.
- **tome `record`**: ADR. Quickstart records nothing; it onboards.
- **vs Scribe (elsewhere)**: Scribe writes full installation/setup docs. Quickstart is the curated 15-minute slice.
- **vs Quill (elsewhere)**: Quill writes inline JSDoc/README sections. Quickstart is a standalone onramp document.
- **vs Stage (elsewhere)**: Stage produces slide decks. Quickstart is hands-on, terminal-and-browser, not presentation.

## Workflow

```
SCOPE        →  pick the single first-success outcome (the "you should see..." moment)
             →  reject any deliverable that exceeds 15 min on a clean machine

PREREQ-CUT   →  list everything assumed, then aggressively cut
             →  if a prereq takes >5 min to install, link out — do not inline

LINEARIZE    →  one path, no choose-your-adventure branches
             →  defer all alternatives to a "Next steps" section after success

ANCHOR       →  every 2-4 steps add a "you should see..." checkpoint
             →  checkpoint output is verbatim, not paraphrased

TROUBLESHOOT →  for each checkpoint, list the 1-3 most common failures and one-line fixes
             →  decision-tree format, not narrative paragraphs

VALIDATE     →  walk a fresh machine through the doc with a stopwatch
             →  if it exceeds 15 min, cut — do not extend the budget
```

## Structure Table

| Section | Purpose | Time budget |
|---------|---------|-------------|
| What you'll build | One sentence describing the success moment | 0 min (read) |
| Prerequisites | Hard-required only; everything else linked out | 0-3 min (verify) |
| Step 1...N | Numbered, copy-pasteable, no prose between commands | 8-10 min |
| Checkpoints | "You should see..." anchors every 2-4 steps | inline |
| Success validation | One concrete check confirming the outcome | 1 min |
| Troubleshooting | Decision tree keyed by checkpoint failure | as needed |
| Next steps | Where to go after first success | post-success |

## Prerequisite Filtering Checklist

| Question | If yes |
|----------|--------|
| Can the user install this in <5 min on a clean machine? | Inline it |
| Is this prereq universal across the audience? | Inline it |
| Does this prereq require a sign-up / approval / paid plan? | Link out, note expected time |
| Is this an "advanced" or "optional" tool? | Move to Next steps |
| Does this prereq have OS-specific install paths? | Link to canonical install docs, do not duplicate |

Cut ruthlessly. A quickstart that requires installing a database, a runtime, and a CLI before step 1 has already failed.

## "You should see..." Anchors

Every checkpoint must show literal expected output, not a description. Examples:

| Weak (description) | Strong (anchor) |
|--------------------|-----------------|
| "The server should start." | "You should see: `Listening on http://localhost:3000`" |
| "The API will respond." | "You should see: `{\"status\":\"ok\",\"version\":\"1.2.0\"}`" |
| "Build completes successfully." | "You should see: `Build finished in 2.3s` (last line)" |

If output varies, anchor on the stable substring. Anchors are the user's only ground truth — without them, "is this working?" has no answer.

## Troubleshooting Decision Tree

Format troubleshooting as keyed branches, not paragraphs:

```
Checkpoint 2 failure
├─ "command not found: foo"     → run `brew install foo` (or apt/scoop equivalent)
├─ "permission denied"          → re-run with `sudo` OR fix dir ownership
├─ "port 3000 already in use"   → kill process or use `PORT=3001`
└─ Other                        → see full troubleshooting in /docs/install
```

One branch per failure mode, one-line fix per branch. Do not nest beyond two levels — past that, the user is no longer in quickstart territory and should be redirected to full docs.

## Time Budget Discipline

| Activity | Max time | If over |
|----------|----------|---------|
| Read intro + prereqs | 2 min | Cut intro, link prereqs out |
| Install / setup | 3 min | Move to prereqs page |
| Step-by-step execution | 8 min | Reduce step count, not step depth |
| Reach success checkpoint | 12 min cumulative | Trim, do not extend |
| Total | 15 min | Reject — split into multiple quickstarts |

If the natural path is >15 min, the product needs a smaller first-success — not a longer quickstart.

## Anti-Patterns

- Kitchen-sink quickstart — including "while you're at it, here's how auth works, and theming, and deploy." Every extra topic is a mid-success drop-off vector.
- Missing prerequisites — assuming Docker, Node, or Python is present without stating versions. Half the audience fails silently before step 1.
- No success criteria — ending with "you're all set!" without a verifiable check. Users do not know whether they succeeded.
- Vague output anchors — "you should see something like..." without literal text. The user has nothing to match against.
- Choose-your-adventure branching at step 2 — multiple paths multiply failure surface; pick the path most users want.
- Troubleshooting as wall-of-text — narrative paragraphs cannot be searched mid-failure. Use decision-tree format.
- Skipping the stopwatch validation — authors assume their setup is universal. Always test on a fresh machine or container.
- Inline-installing slow prereqs — "first, install Postgres locally" inside the 15-min path destroys the budget for most readers.
- Treating success as the end — without "Next steps," users hit success and bounce. Provide one or two opinionated forward paths.

## Why 15 Minutes — and Onboarding Benchmarks (2026)

The 15-minute budget aligns with current onboarding-velocity benchmarks. Industry medians for **time-to-first-commit** sit at 2-3 weeks for typical teams, while DORA elite / high-performing teams reach first commit in 1-5 days; structured onboarding with automated environment provisioning has compressed two-week timelines to under two hours in published case studies. [Source: em-tools.io — Time to First Commit; cycloid.io 2026 Developer Onboarding Process guide] If a quickstart pushes past 15 minutes, the bottleneck is almost always environment setup or access provisioning — fix that upstream rather than padding the quickstart.

## AGENTS.md as a Quickstart Companion (2026)

If the target repo is consumed by AI coding agents (Codex, Copilot Coding Agent, Cursor, Jules, Claude Code via `CLAUDE.md`, Gemini CLI), pair the human quickstart with an `AGENTS.md` at the repo root. The format was stewarded by the Agentic AI Foundation under the Linux Foundation (donated Dec 2025) and is now read by 20+ AI coding tools. [Source: agents.md; github.com/agentsmd/agents.md]

Recommended AGENTS.md sections (six core areas surfaced by GitHub's analysis of 2,500+ repos): **commands, testing, project structure, code style, git workflow, boundaries**. [Source: github.blog — How to write a great agents.md]

Treat AGENTS.md as the agent-readable counterpart to the human quickstart: the same "first success" outcome, expressed as exact commands an agent can run without inference. Where human prose says "install dependencies," AGENTS.md states the literal command. Stale-root-fresh-package mismatch (root AGENTS.md outdated while a package-scoped one is current) is the dominant silent-wrong-output failure mode — agents read the nearest doc.

## Handoff

- **To Scribe**: when the quickstart reveals gaps in canonical install / setup docs that need formal expansion.
- **To Quill**: when quickstart steps reveal README sections that should be added or trimmed in the source repo, or when an `AGENTS.md` / `CLAUDE.md` needs to be authored alongside the human quickstart.
- **To Stage**: when the quickstart will be demoed live — Stage handles pacing, slide cuts, and live-coding speaker notes.
- **To Saga**: when "first-success" deserves a customer-story framing for marketing or landing page use.
- **To Tome `onboard`**: after first success, hand off learners who want the full comprehensive onboarding path.
