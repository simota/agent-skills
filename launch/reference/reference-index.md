# Launch Reference Index

Every `reference/` file `launch` owns, and the condition that makes it worth
reading. `launch/SKILL.md` keeps only the shared-contract rows and a pointer here.

**Read this when** you need a reference and the Recipe registry did not already
name it, or when scanning what this skill can consult at all.

---

| File | Read this when |
|------|----------------|
| `reference/strategies.md` | Versioning, CHANGELOG, release notes, rollback options, hotfix flow, release windows, or command references. |
| `reference/patterns.md` | Multi-agent release orchestration or handoff payload expectations. |
| `reference/release-anti-patterns.md` | Deployment anti-patterns, canary/blue-green cautions, or release cadence guardrails. |
| `reference/feature-flag-pitfalls.md` | Feature flag lifecycle rules, debt controls, or cleanup thresholds. |
| `reference/versioning-pitfalls.md` | SemVer pitfalls, breaking-change detection rules, or CalVer decision support. |
| `reference/rollback-anti-patterns.md` | Rollback design, DB migration safety, recovery sequencing, or rolling back an AI feature (prompt / model revision / index / embeddings / adapter / runtime / tool schema). |
| `reference/hotfix-workflow.md` | `hotfix`: emergency patch playbook, 2h SLA, shortened CI gate, hotfix branch, bundled rollback, and backport-to-main planning. |
| `reference/canary-rollout.md` | `canary`: progressive traffic shifts (1% → 10% → 50% → 100%), guardrail metrics, automatic abort conditions, and observation windows. |
| `reference/mobile-release.md` | `mobile`: TestFlight phased release / Play staged rollout, store-compliance gating, App Review / Play Review lead-time planning, server-driven feature flag rollback path, and hotfix submission flow. |
| `reference/github-pr-collection.md` | Read-only `gh` collection, field/date filters, pagination, aggregation, and rate-limit handling. |
| `reference/github-report-cache.md` | Cache TTL, ETag, invalidation, and rate-limit-aware freshness policy. |
| `reference/github-report-error-handling.md` | Authentication, rate-limit, network, partial-data, and graceful-degradation handling. |
| `reference/engineering-report-templates.md` | Weekly, monthly, individual, release-note, and quality-trend report shapes. |
| `reference/client-report-templates.md` | Client-facing report structure and the bundled HTML/template/style/script toolchain. |
| `reference/report-pdf-export.md` | Markdown/HTML-to-PDF paths, Mermaid handling, validation, and fallbacks. |
| `reference/release-report-writing.md` | Changelog categories, audience split, automation, and release-note quality gates. |
| `reference/delivery-metrics.md` | DORA metrics, Reliability, SPACE complement, percentile bands, and 7 team archetypes. |
| `reference/engineering-metrics-guardrails.md` | Goodhart, vanity-metric, burnout, and AI-period comparison safeguards. |
| `reference/pr-flow-analysis.md` | Cycle-time decomposition, percentiles, Lorenz/Gini, bot ratio, and large-PR risk. |
| `reference/okr-linkage.md` | PR-to-Objective tagging, KR narratives, health scoring, and quarterly aggregation. |
| `reference/effort-estimation.md` | Effort-range baseline and adjustment guidance. |
| `reference/effort-estimation-guardrails.md` | LOC and precision caveats for effort estimates. |
| `reference/reporting-anti-patterns.md` | Actionability, gaming resistance, audience layering, and cadence guardrails. |
| `reference/retrospective-voice.md` | Data-grounded retrospective voice and narrative frameworks. |
| `reference/reporting-handoffs.md` | Structured report payloads for Pulse, Canvas, Zen, Sherpa, and Radar. |
| `reference/autorun-schema.md` | Emitting the AUTORUN `_STEP_COMPLETE` block — Launch-specific Output/Next schema. |
| `_common/OPUS_5_AUTHORING.md` | Sizing the release plan, deciding adaptive thinking depth at rollout staging, or front-loading release type/scope/risk at PLAN. Critical for Launch: P3, P5. |
