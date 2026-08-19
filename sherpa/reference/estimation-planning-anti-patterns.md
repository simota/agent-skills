# Estimation & Planning Anti-Patterns
Purpose: Use this file when estimates, capacity plans, or sprint-level planning quality look distorted.
## Contents
- `EP-01` to `EP-07`
- `PP-01` to `PP-07`
- calibration and capacity rules
- execution pitfalls
- retrospective completion trap
## Estimation Anti-Patterns
| ID | Anti-pattern | Core issue | Preferred fix |
| --- | --- | --- | --- |
| `EP-01` | Solo Estimation | one person decides the estimate | estimate with the whole team |
| `EP-02` | Anchoring Bias | the first number dominates | reveal estimates simultaneously |
| `EP-03` | Time-Point Confusion | points are treated as hours | keep points relative, not time-based |
| `EP-04` | Velocity Obsession | velocity becomes a performance score | use velocity only for forecasting |
| `EP-05` | Safety Padding | personal buffer hides real uncertainty | use a separate team buffer of `15-20%` |
| `EP-06` | Estimation as Commitment | estimate becomes a promise | treat estimate as shared understanding |
| `EP-07` | Refinement Skip | vague backlog item is estimated anyway | refine before estimating |
## Planning Anti-Patterns
| ID | Anti-pattern | Core issue | Preferred fix |
| --- | --- | --- | --- |
| `PP-01` | Overcommitment Pressure | too much work is pushed into the plan | commit at about `80-85%` capacity |
| `PP-02` | Missing Sprint Goal | work is a random list, not a coherent goal | define one measurable goal |
| `PP-03` | Capacity Blindness | holidays, meetings, and interruptions are ignored | calculate available time honestly |
| `PP-04` | Last-Minute Items | unrefined work appears during planning | admit only prepared items |
| `PP-05` | Multi-Sprint Waterfall | detailed plans go too far ahead | use rolling-wave planning |
| `PP-06` | Plan Over Goal | the plan matters more than the outcome | adapt the plan to protect the goal |
| `PP-07` | Tech Debt Avoidance | only features are planned | reserve up to `20%` for debt reduction when needed |
## Execution Pitfalls
| Pitfall | Why it hurts | Countermeasure |
| --- | --- | --- |
| Cherry-Picking | easy tasks win, goal-critical work slips | prioritize by goal and critical path |
| Gold-Plating | scope expands during execution | enforce Definition of Done |
| Side-Gigs | invisible work bypasses the board | make all work visible |
| Hardening Sprint | quality is postponed | build quality into normal work |
| Variable Sprint Length | timebox is stretched | adjust scope, not the sprint |
| Everything's a Bug | normal work abuses the emergency lane | define bug severity clearly |
## Retrospective Completion Trap
- common completion rate is roughly `33%`
- root causes:
  - the action never enters the backlog
  - no owner exists
  - no follow-up happens
---
## Planning Context and Sources (SKILL.md excerpt)
- **Output Spec-Kit-compatible Atomic Steps** when the user invokes `spec` or `speckit`. The GitHub Spec-Kit (`/speckit.specify` / `/speckit.plan` / `/speckit.tasks` / `/speckit.implement`) is the executable-spec standard supported by Claude Code, Cursor, Copilot and 29+ other tools. Match the file layout (`spec/`, `plan/`, `tasks/`) and the Constitution → Specify → Plan → Tasks → Implement phase contract so downstream tooling (Builder, Forge, Artisan) can consume the steps without translation. [Source: github.com/github/spec-kit]
- **Keep atomic steps small to counteract AI-era PR bloat.** The DORA 2025 report found that AI-assisted teams produced PRs 51% larger on average, pushing median PR review time up 441% and allowing 31% more PRs to merge without any review — and bugs per developer rose 54% year-over-year. Keeping each Atomic Step to a single, committable concern directly counters this trend. [Source: dora.dev/research/2025/dora-report/](https://dora.dev/research/2025/dora-report/)
- **Leverage AI-native planning tools for epic intake.** Linear Agent (launched March 2026) and ClickUp Brain can draft issue hierarchies from a description. Use these as raw input into Sherpa's MAP phase — validate, time-box, and apply INVEST before passing steps to implementors. Do not treat AI-generated task lists as final without Sherpa's granularity and acceptance-criteria checks. [Sources: linear.app/changelog/2026-03-24-introducing-linear-agent](https://linear.app/changelog/2026-03-24-introducing-linear-agent), [linear.app/docs/agents-in-linear](https://linear.app/docs/agents-in-linear)]
- **Match planning horizon to velocity — prefer just-in-time over long roadmaps when output is high.** When agentic implementation raises throughput, a multi-month roadmap can go stale within weeks — the plan decays faster than it executes. For high-velocity epics, decompose just-in-time: plan the next executable increment in detail, prototype and ship it to real users, then re-plan from feedback rather than pre-committing the whole arc. Keep long-horizon items as a coarse intent backlog (not detailed Atomic Steps) until they reach the front of the queue. Low-velocity or high-coordination work still warrants longer-horizon planning — calibrate to the actual decay rate, not a fixed cadence. [Source: claude.com/blog/running-an-ai-native-engineering-org]
