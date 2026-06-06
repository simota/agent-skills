# Refactoring Anti-Patterns

Purpose: Use this file before refactoring to avoid process failures, unsafe scope growth, and misleading abstractions.

## Contents
- [Process Anti-Patterns](#process-anti-patterns)
- [Technical Anti-Patterns](#technical-anti-patterns)
- [Cognitive Biases](#cognitive-biases)
- [Pre-Refactor Checklist](#pre-refactor-checklist)

## Process Anti-Patterns

| Anti-pattern | Signals | Risk | Zen response |
|--------------|---------|------|--------------|
| **ANTI-001 Big Bang Refactoring** | Hundreds or thousands of lines changed at once | Unreviewable, regression-prone, hard to debug | Keep refactors inside scope tiers. `Focused = 1-3 files, <=50 lines`. `Module/Project-wide = plan or mechanical split work only`. |
| **ANTI-002 Refactoring Without Tests** | "It already works" used as the reason to skip tests | Silent behavior drift | Tests are required before and after. If coverage is `<80%`, hand off to Radar first. |
| **ANTI-003 Mixing Refactoring with Features** | Cleanup mixed into feature commits or PRs | Root cause becomes unclear | Separate cleanup from feature work. Behavior changes remain `NEVER`. Use Guardian for PR-noise separation. |
| **ANTI-004 Perfectionism Over Progress** | Endless cleanup beyond the task goal | Scope creep and delivery delay | Apply Boy Scout Rule. Do one meaningful refactor per pass and stop at the scope boundary. |
| **ANTI-005 Underestimating Effort** | "Small rename" expands into cross-module impact | Half-finished cleanup, schedule slip | Inspect impact first. Treat public API or export changes as `Ask first`. Make scope visible in the Before/After report. |

## Technical Anti-Patterns

| Anti-pattern | Signals | Risk | Zen response |
|--------------|---------|------|--------------|
| **ANTI-006 Golden Hammer** | Same recipe proposed for every smell | Wrong abstraction, more complexity | Map problem to recipe. Stop if complexity increases. |
| **ANTI-007 Premature Abstraction** | Shared utility extracted too early | Indirection without value | Apply Rule of Three. Two similar spots are not enough. Three repetitions justify evaluation. |
| **ANTI-008 Speculative Generality** | Code kept "for future use" | Dead code and maintenance noise | Prefer YAGNI. Use dead-code detection tools and remove unused paths deliberately. |
| **ANTI-009 Shotgun Refactoring** | One rename or smell fix touches many files | Review burden and regression risk | `Module = 4-10 files, mechanical only`. `Project-wide = 10+ files, plan only`. Split execution into later passes. |
| **ANTI-010 Copy-Paste Refactoring** | Patterns copied from other projects without local fit | Context mismatch and inconsistency | Prefer project-native naming and patterns. Use `consistency-audit.md` before importing external style. |

## Cognitive Biases

| Bias | Failure mode | Countermeasure |
|------|--------------|----------------|
| **Confirmation bias** | Assuming the refactor is correct because it looks cleaner | Compare Before/After metrics and test results |
| **Sunk cost** | Refusing to stop a refactor that is going badly | Revert immediately if complexity or risk increases |
| **Planning fallacy** | Underestimating cleanup effort | Respect scope tiers and phase large work |
| **Law of the instrument** | Reusing favorite patterns regardless of fit | Follow smell-to-recipe mapping instead of habit |

## Pre-Refactor Checklist

- [ ] The goal is explicit.
- [ ] The change fits the current scope tier.
- [ ] Tests can run before and after the change.
- [ ] Coverage is sufficient, or Radar is queued first when coverage is `<80%`.
- [ ] Feature work is not mixed into the cleanup.
- [ ] No public API, export, or dynamic usage risk is being changed without confirmation.
- [ ] Before metrics are recorded.
- [ ] The proposed pattern matches the existing project conventions.

**Source:** [Tembo: Code Refactoring Mistakes](https://www.tembo.io/blog/code-refactoring) · [GeeksforGeeks: Anti-Patterns to Avoid](https://www.geeksforgeeks.org/blogs/types-of-anti-patterns-to-avoid-in-software-development/) · [BairesDev: Software Anti-Patterns](https://www.bairesdev.com/blog/software-anti-patterns/) · [Sahand Saba: 9 Anti-Patterns](https://sahandsaba.com/nine-anti-patterns-every-programmer-should-be-aware-of-with-examples.html)
