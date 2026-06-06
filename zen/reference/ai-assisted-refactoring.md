# AI-Assisted Refactoring (2025-2026)

Purpose: Use this file when Zen runs Multi-Engine or any AI-assisted refactoring workflow. It keeps the safety guardrails explicit.

## Contents
- [Current Snapshot](#current-snapshot)
- [Strengths and Limits](#strengths-and-limits)
- [Hallucination Watchlist](#hallucination-watchlist)
- [Zen Guardrails](#zen-guardrails)
- [Enterprise Workflow](#enterprise-workflow)
- [Target Metrics](#target-metrics)

## Current Snapshot

These figures are directional reference points, not hard gates:

- Review time often improves by `40-60%` when teams use AI refactoring tools well.
- Smaller changes perform better; `<=200 LOC` is the preferred atomic size.
- Structured test protocols materially reduce post-deploy issues.
- High-impact legacy targets tend to produce the best ROI.
- **GitHub Copilot Code Review** (agentic architecture overhaul March 2026): gathers full repository context before commenting — not just the diff. Reached 60M reviews by March 2026 (10× growth since April 2025 launch); surfaces actionable feedback in 71% of reviews (~5.1 comments/review). Starting June 1 2026, each review consumes GitHub Actions minutes / AI Credits on private repos. [Source: [GitHub Docs — About Copilot code review](https://docs.github.com/en/copilot/concepts/agents/code-review); [GitHub Changelog 2026-04-27](https://github.blog/changelog/2026-04-27-github-copilot-code-review-will-start-consuming-github-actions-minutes-on-june-1-2026/)]
- **Cursor vs Copilot (2026)**: Copilot scores higher on SWE-bench (56% vs 51.7%) but Cursor completes complex refactoring tasks ~30% faster (avg 62.95s vs 89.91s). Cursor's multi-agent Composer runs up to 8 parallel agents via git worktrees. [Source: [tech-insider.org](https://tech-insider.org/github-copilot-vs-cursor-2026-2/)]
- **Sourcery for Python**: version 1.43.0 (January 2026). Recommended 2026 Python quality setup: Ruff (local linting/formatting) + Sourcery (AI-assisted PR review). [Source: [sourcery.ai](https://www.sourcery.ai/)]

## Strengths and Limits

### Reliable AI strengths

| Capability | Typical confidence |
|------------|--------------------|
| Variable and symbol renaming across files | High |
| Function extraction and structural cleanup | Medium-high |
| Dead-code removal | High |
| Style unification | High |
| Type tightening such as `any` reduction | Medium |
| Documentation scaffolding | Medium |

### Persistent weak spots

- Domain-specific business logic
- Architecture-level tradeoffs
- Legacy constraints that live outside the code
- Context-specific risk balancing
- High-level refactors that depend on product intent rather than structure

## Hallucination Watchlist

Check these explicitly after any AI-generated proposal:

| Risk | Typical symptoms |
|------|------------------|
| **Incorrect imports** | Non-existent modules, wrong API versions, broken moved symbols |
| **Edge-case mishandling** | Added or removed null checks, boundary-condition drift |
| **Overzealous optimization** | Behavior changed in the name of cleanliness or performance |
| **Behavioral modification** | Tests pass but domain semantics or error handling changed |
| **Context loss** | Historical comments removed or legacy constraints ignored |

AI-authored CVEs are accelerating: 35 newly disclosed in March 2026, up from 6 in January and 15 in February (Vibe Security Radar tracking; 27 of the 35 March CVEs traced to Claude Code by commit signature) [Source: Infosecurity Magazine — "Security Researchers Sound the Alarm on Vulnerabilities in AI-Generated Code" (2026-03-26), https://www.infosecurity-magazine.com/news/ai-generated-code-vulnerabilities/].

## Zen Guardrails

### Multi-Engine mitigation

1. Run `3` independent proposals.
2. Use the `Compete` merge strategy.
3. Score on `readability`, `consistency`, and `change volume`.
4. Keep a human review gate before adoption.

### Additional safety rules

- Keep each AI-assisted change to `<=200 LOC`.
- Run static analysis in the verification path.
- Compare Before/After metrics, not just prose claims.
- Prepare rollback support for risky migrations, including feature-flag fallback when appropriate.
- Keep AI changes structural. Humans decide domain-logic changes.
- Start from non-critical utilities before higher-risk modules.
- Run the relevant local test suite before merge.

## Enterprise Workflow

| Phase | Purpose |
|------|---------|
| **1. Code Health Assessment** | Capture baseline metrics |
| **2. Strategic Prioritization** | Overlay risk and change frequency |
| **3. Tool Selection** | Match tool choice to scope and compliance needs |
| **4. Atomic Transformation** | Keep `1 PR = 1 change`, ideally `<=200 LOC` |
| **5. Automated Quality Gates** | Apply CI/static-analysis checks |
| **6. Continuous Measurement** | Track improvement over time, not just one PR |

## Target Metrics

| Metric | Target |
|--------|--------|
| Cyclomatic complexity reduction | `15-25%` |
| Duplicate-code reduction | Measurable decrease |
| Review time reduction | `40-60%` |
| Post-refactor bug rate | No worse than non-refactored code |
| LOC per change | `<=200` |

**Source:** [Augment Code: AI Code Refactoring](https://www.augmentcode.com/tools/ai-code-refactoring-tools-tactics-and-best-practices) · [IBM: AI Code Refactoring](https://www.ibm.com/think/topics/ai-code-refactoring) · [DX: Enterprise AI Refactoring](https://getdx.com/blog/enterprise-ai-refactoring-best-practices/) · [Qodo: Evolution of Code Refactoring Tools](https://www.qodo.ai/blog/evolution-code-refactoring-tools-ai-efficiency/) · [Second Talent: 5 AI Tools for Code Refactoring 2026](https://www.secondtalent.com/resources/ai-tools-for-code-refactoring-and-optimization/) · [GitHub Docs: About Copilot code review](https://docs.github.com/en/copilot/concepts/agents/code-review) · [GitHub Changelog: Copilot code review billing (2026-04-27)](https://github.blog/changelog/2026-04-27-github-copilot-code-review-will-start-consuming-github-actions-minutes-on-june-1-2026/) · [tech-insider.org: Copilot vs Cursor 2026 benchmarks](https://tech-insider.org/github-copilot-vs-cursor-2026-2/) · [Sourcery AI](https://www.sourcery.ai/)
