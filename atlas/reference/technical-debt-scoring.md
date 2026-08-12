# Technical Debt Scoring

## Severity Matrix

| Impact | Effort: Low | Effort: Medium | Effort: High |
|--------|------------|----------------|-------------|
| High | P0: Fix now | P1: Next sprint | P2: Plan |
| Medium | P1: Next sprint | P2: Plan | P3: Backlog |
| Low | P2: Plan | P3: Backlog | P4: Accept |

## Debt Categories

| Category | Examples | Typical Impact |
|----------|----------|----------------|
| **Design Debt** | God classes, tight coupling, missing abstractions | High - affects changeability |
| **Code Debt** | Duplicated code, complex functions, poor naming | Medium - affects readability |
| **Architecture Debt** | Coupling, missing abstractions, layer violations | High - affects scalability |
| **Test Debt** | Missing tests, flaky tests, low coverage | High - affects reliability |
| **Documentation Debt** | Missing docs, outdated docs, unclear APIs | Medium - affects onboarding |
| **Infrastructure Debt** | Outdated dependencies, manual deployments | Medium - affects operations |
| **Dependency Debt** | Outdated packages, CVEs | Medium - affects security |

## Quantification

- Story points estimate for remediation
- Impact score (1-5) on development velocity
- Risk score (1-5) for production incidents

---

## Priority Scoring Matrix

```markdown
## Technical Debt Item: [Name]

### Impact Score (1-5)
- Code touchpoints: [how many files/functions affected]
- Developer friction: [how often developers encounter this]
- Bug correlation: [how many bugs related to this area]
- **Impact Score**: [1-5]

### Fix Cost Score (1-5)
- Estimated effort: [hours/days]
- Risk of regression: [low/medium/high]
- Dependencies: [what else needs to change]
- **Cost Score**: [1-5]

### Priority = Impact × (6 - Cost)

| Debt Item | Impact | Cost | Priority |
|-----------|--------|------|----------|
| God class UserService | 5 | 3 | 15 |
| Missing API validation | 4 | 2 | 16 |
| Duplicated auth logic | 3 | 2 | 12 |
| Outdated React version | 4 | 4 | 8 |
```

## Debt Inventory Template

```markdown
# Technical Debt Inventory

## Summary
- Total items: [count]
- High priority: [count]
- Estimated total effort: [days/weeks]

## High Priority (Address this quarter)

### TD-001: UserService God Class
- **Category**: Design Debt
- **Location**: `src/services/UserService.ts` (2,500 lines)
- **Impact**: 5 - Core service, touched by 80% of features
- **Cost**: 3 - Moderate effort, well-tested
- **Priority**: 15
- **Proposed Fix**: Split into UserAuthService, UserProfileService, UserPreferencesService
- **Dependencies**: None
- **Owner**: [assignee]

### TD-002: Missing Input Validation
- **Category**: Code Debt
- ...

## Medium Priority (Address this half)

### TD-003: ...

## Low Priority (Backlog)

### TD-004: ...
```

## Repayment Plan Template

```markdown
# Technical Debt Repayment Plan: Q1 2025

## Budget
- Allocated time: 20% of sprint capacity
- Estimated capacity: 40 story points

## Goals
1. Reduce high-priority debt items by 50%
2. Improve test coverage from 60% to 75%
3. Eliminate all circular dependencies

## Sprint Allocation

### Sprint 1
- [ ] TD-001: UserService split (Phase 1) - 8 points
- [ ] TD-005: Add missing API tests - 5 points

### Sprint 2
- [ ] TD-001: UserService split (Phase 2) - 8 points
- [ ] TD-002: Input validation - 5 points

### Sprint 3
- [ ] TD-001: UserService split (Phase 3) - 5 points
- [ ] TD-003: Fix circular deps - 8 points

## Success Metrics
- [ ] No God classes > 500 lines
- [ ] Zero circular dependencies
- [ ] All API endpoints validated
- [ ] Test coverage > 75%
```

## ROI Calculation Guide

```markdown
## ROI Analysis: [Debt Item]

### Current Cost (per month)
- Bug fixes in this area: [hours] × [hourly rate] = $[amount]
- Extra development time: [hours] × [hourly rate] = $[amount]
- Onboarding overhead: [hours] × [hourly rate] = $[amount]
- **Total monthly cost**: $[amount]

### Fix Cost (one-time)
- Development effort: [hours] × [hourly rate] = $[amount]
- Testing effort: [hours] × [hourly rate] = $[amount]
- Review/deployment: [hours] × [hourly rate] = $[amount]
- **Total fix cost**: $[amount]

### ROI Calculation
- Break-even point: [fix cost] / [monthly savings] = [months]
- 12-month ROI: ([monthly savings × 12] - [fix cost]) / [fix cost] × 100 = [%]

### Recommendation
[Fix / Defer / Accept]
- Rationale: [explanation]
```


## Core Contract Long Form (SKILL.md excerpt)

- **Technical Debt Ratio (TDR)**: Quantify debt via SQALE or equivalent (remediation cost / development cost). TDR thresholds: < 5% healthy, 5–10% significant (prioritized remediation needed), > 10% critical (immediate action). Allocate ≥ 15% of development time to debt reduction for projects above 5% TDR. Prioritize by Cost of Delay: security vulnerabilities > performance degradation > code smell. Industry benchmark (CISQ 2022): organizations with unmanaged debt spend ~40% more on maintenance and deliver features 25-50% slower; accumulated software TD in the US reached ~$1.52 trillion. Deloitte 2026 Global Technology Leadership Study: technical debt accounts for 21–40% of IT spending. Use these figures to frame debt severity for stakeholders. [Source: Deloitte Insights — The hidden drag, quantified: Technical debt's penalty on value and growth (2026)](https://www.deloitte.com/us/en/insights/topics/technology-management/technical-debt-impact.html)

- **ADR quality bar**: Every ADR must include context (forces at play), decision (active voice), status, and consequences (positive and negative). Reference ISO/IEC/IEEE 42010:2022 for formal architecture descriptions (replaces 2011 edition; uses "entity of interest" and "architecture description framework" terminology). Prefer MADR 4.0.0 template for tradeoff-explicit records (considered options + pros/cons with unified consequences section). Schedule post-decision review at 1 month to compare predictions with actual outcomes; update status to Confirmed, Superseded, or Deprecated.

- **ADR narrative is mandatory; YAML header is optional (v5 fold-in)**: Every ADR MUST retain the human-readable narrative — context, forces, considered options, decision rationale, consequences. The narrative is the **primary artifact** and must be preserved verbatim through any tooling. An optional `constraints + affected + tests` YAML header MAY be added at the top of the ADR file for CI integration (fitness function wiring), but the YAML is a derived projection and must never replace the narrative. Rationale: Magi v5 review of the "Executable ADR" proposal (omen FM-EA-1, RPN 729) concluded that YAML-only ADRs lose the "why" within 5 years and produce "a bare enumeration of constraints" with no organizational memory. Pattern reference: `reference/adr-rfc-templates.md` plus a machine-readable header example when CI fitness wiring is desired.

- **Architecture fitness functions**: Recommend automated fitness functions — CI-integrated tests that objectively assess architectural characteristics (coupling thresholds, complexity limits, layer violation rules). Use targets from `reference/architecture-health-metrics.md` as concrete thresholds. Fitness functions are guardrails that enable guided, incremental architecture evolution; without them, architectural drift goes undetected until it causes cascading failures. Every non-deprecated ADR should map to at least one fitness function — this is the operationalization step that connects decisions to enforcement. Recommend language-appropriate tooling: ArchUnit (Java/Kotlin), dependency-cruiser (JS/TS), NetArchTest (.NET), go-arch-lint (Go), or custom AST-based tests. For cross-language declarative enforcement, SonarQube Architecture as Code (GA 2025; Java, JS/TS — Python, C# planned) stores architecture rules alongside code and verifies violations during CI/CD analysis.

- **Default to Modular Monolith** for new systems and as the target for microservices retreat. The 2026 industry retrospective is clear: Amazon Prime Video reported 90% cost reduction by collapsing microservices to a monolith; CNCF's 2025 satisfaction survey showed microservices satisfaction drop 19pp YoY. Enforce module boundaries with `Spring Modulith`, `ArchUnit`, `dependency-cruiser`, or equivalent fitness functions — strict boundaries inside a single deployable beat distributed messes. Reserve true microservices for cases that justify it on independent scale, language, or compliance grounds. [Source: dev.to/x4nent — Modular Monolith 2026 Complete Guide; byteiota.com — Modular Monolith 42]

- **Recommend Vertical Slice Architecture** as the default feature-organisation pattern; reserve Hexagonal / Clean / Onion for stable cross-feature boundaries. Layer-per-folder (`controllers/`, `services/`, `repositories/`, `dto/`) is the canonical over-engineering pattern that AI codegen amplifies — a single feature edit hits 6 files, and the agent context window has to span all of them. A vertical slice (`features/cancel-subscription/`) is independently testable, AI-friendly, and avoids the 15-layer abstraction cliff. [Source: jimmybogard.com/vertical-slice-architecture; milanjovanovic.tech/blog/vertical-slice-architecture]

- **Edge-first hybrid topology is the 2026 default deployment shape** for new web systems: edge (Cloudflare Workers / Deno Deploy / Vercel Edge) for auth, redirect, rate-limit, and short-lived RPC; containers for CRUD and long-lived business logic; serverless for batch and async fan-out. ~78% of teams now run hybrid topologies; ADRs should explicitly justify single-tier choices (pure-container or pure-edge) against the hybrid default. Edge state via Durable Objects / Deno KV / Workers KV is mature enough to colocate. [Source: byteiota.com — Edge Computing 2026; digitalapplied.com — Edge Computing Cloudflare Workers Guide]

- **Track Comprehension Debt alongside Technical Debt.** Comprehension Debt is the gap between code volume the team produces (now amplified by AI codegen) and code volume the team genuinely understands. Symptoms: review approvals without questions, fixes that re-introduce removed code, "we already shipped this" surprise. Add a `comprehension_debt` axis to TDR reports (HIGH / MEDIUM / LOW based on AI authorship % and review depth signals). Remediation is not refactoring — it is documentation, ADR backfill, and judge-level review. [Source: oreilly.com/radar — Comprehension Debt: The Hidden Cost of AI-Generated Code]
