# Launch Recipe Registry

The full Recipe table for `launch`. `launch/SKILL.md` carries only the dispatch
allowlist; this file holds what is needed to *execute* a Recipe — activation
condition and the files to read first.

**Read this when** a subcommand matched and you need its row, or when scanning
what Recipes exist at all.

---

| Recipe | Subcommand | Default? | When to Use | Read First |
|--------|-----------|---------|-------------|------------|
| Release Plan | `plan` | ✓ | Release planning and strategy | `reference/strategies.md` |
| Changelog | `changelog` | | CHANGELOG generation and updates | `reference/patterns.md` |
| Release Notes | `notes` | | User-facing release notes | `reference/patterns.md` |
| Rollback Plan | `rollback` | | Rollback planning and runbook | `reference/rollback-anti-patterns.md` |
| Feature Flag | `flag` | | Feature flag management and staged rollout design | `reference/feature-flag-pitfalls.md` |
| Hotfix Release | `hotfix` | | Emergency patch release (shortened CI / hotfix branch / 2h SLA / rollback bundled / backport to main) | `reference/hotfix-workflow.md` |
| Canary Rollout | `canary` | | Staged traffic rollout (1%->10%->50%->100%) with automatic guardrails and abort conditions | `reference/canary-rollout.md` |
| Mobile Release | `mobile` | | iOS / Android store release: TestFlight phased release (1%/10%/50%/100% over 7d), Play staged rollout (5%/20%/50%/100%), store-compliance gate, server-driven flag rollback path | `reference/mobile-release.md` |
| Weekly Report | `weekly` | | Weekly PR aggregation and engineering summary | `reference/engineering-report-templates.md`, `reference/github-pr-collection.md` |
| Monthly Report | `monthly` | | Monthly work report with delivery metrics | `reference/engineering-report-templates.md`, `reference/delivery-metrics.md` |
| Client Report | `client-report` | | Client-facing Markdown/HTML/PDF report with effort ranges and charts | `reference/client-report-templates.md`, `reference/report-pdf-export.md` |
| Sprint Retro | `retro` | | Narrative retrospective grounded in PR and release data | `reference/retrospective-voice.md` |
| DORA Deep-Dive | `dora` | | DORA 5-key metric profile, Reliability, SPACE context, and 7-archetype mapping | `reference/delivery-metrics.md` |
| OKR Linkage | `okr` | | PR-to-Objective evidence and KR narrative for a quarterly window | `reference/okr-linkage.md` |
| PR Flow | `pr-flow` | | Cycle-time percentiles, PR-size risk, contributor distribution, and bot/human split | `reference/pr-flow-analysis.md` |
