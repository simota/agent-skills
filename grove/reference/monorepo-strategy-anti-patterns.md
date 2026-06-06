# Monorepo Strategy Anti-Patterns

Purpose: Use this reference when deciding between monorepo, polyrepo, or hybrid structure, or when auditing governance and ownership issues in a monorepo.

## Contents

- Monorepo strategy anti-patterns
- Monorepo vs polyrepo decision framework
- Governance scaling
- Ownership patterns
- AI-era considerations
- Grove integration

Monorepo-vs-polyrepo decision mistakes, governance traps, and ownership risks.

## 1. Monorepo Strategy Anti-Patterns

| ID | Anti-Pattern | What Goes Wrong | Typical Signals | Recommended Response |
|---|---|---|---|---|
| **MS-01** | **Google Envy** | A small or medium team copies a hyperscale monorepo strategy. | No platform team exists, yet builds take more than an hour. | Choose a strategy that matches current scale and staffing. |
| **MS-02** | **Premature Split** | Teams split into polyrepos before measurable pain exists. | The only argument is “we may not scale.” | Measure actual bottlenecks first; try partial clone or sparse-checkout before splitting. |
| **MS-03** | **Monolith Confusion** | Teams treat a monorepo as permission for tightly coupled code. | Direct cross-package imports and non-independent deployment. | Keep strict package boundaries, public APIs, and independent buildability. |
| **MS-04** | **Cross-Team Mega Refactor** | A monorepo enables giant cross-team PRs. | One PR changes code owned by many teams and becomes unreviewable. | Refactor one team boundary at a time and separate changes by API contract. |
| **MS-05** | **Governance Vacuum** | A monorepo runs without branch policy, ownership, or automated checks. | Review quality falls and `main` becomes a bottleneck. | Use trunk-based development, CODEOWNERS, and automated quality gates. |
| **MS-06** | **Ownership Ambiguity** | Nobody can say who owns a directory or component. | Review approvals stall and quality standards vary by change author. | Define ownership explicitly and expand autonomy gradually. |
| **MS-07** | **Tool Lock-in** | The repository structure becomes hostage to one monorepo tool. | Migration away from Nx/Turborepo becomes prohibitively costly. | Favor tool-agnostic boundaries and standard package-manager capabilities. |

## 2. Monorepo vs Polyrepo Decision Framework

Ask three questions:
1. Has the team actually reached monorepo limits in size, build time, or coordination cost?
2. Are you solving an organizational problem with unnecessary technical complexity?
3. Is the pain measurable and not fixable with cheaper mitigations?

Decision matrix:

| Team size | Coupling | Default recommendation |
|---|---|---|
| `1-10` | High | Monorepo |
| `1-10` | Low | Monorepo or polyrepo |
| `10-50` | High | Monorepo with strong governance |
| `10-50` | Low | Hybrid |
| `50-200` | High | Monorepo with a platform team |
| `50-200` | Low | Polyrepo with a developer portal |
| `200+` | Any | Dedicated evaluation required |

Important:
- Human and organizational problems are harder than technical ones.
- Psychological safety and cross-team trust are prerequisites for a healthy monorepo.

## 3. Governance Scaling

Monorepo prerequisites:
- automated formatting and linting
- strict branch policy
- CODEOWNERS-based ownership
- consistent dependency management
- collaborative engineering culture

Monorepo scaling risks:
- individual cognitive load rises with repo size
- unrelated commits affect more developers
- history and blame become slower to reason about

Polyrepo prerequisites:
- explicit technology-stack policy
- shared tooling for security and dependency updates
- platform investment in developer experience

Polyrepo scaling risks:
- duplicate code grows
- consistency across repositories gets harder
- observability and governance become fragmented

## 4. Ownership Patterns

| Pattern | Ownership unit | Main risk |
|---|---|---|
| Monorepo | Directory / component | Boundary-crossing changes |
| Polyrepo | Repository | Fragmented dependency management |
| Hybrid | Platform + product mix | Higher tooling and governance cost |

Conway-aligned guidance:
- Product autonomy tends to favor polyrepos.
- Strong platform teams favor monorepos.
- Repository strategy that fights org structure creates friction.

Healthy ownership indicators:
- stable review cycle time
- reliable dependency-update cadence
- manageable cross-team coordination overhead
- clear responsibility boundaries

## 5. AI-Era Considerations

Potential monorepo benefit:
- AI assistants get more consistent cross-stack context.

Potential polyrepo benefit:
- each repository boundary is clearer and smaller.

Do not decide repo strategy based on AI tooling alone. Treat it as a secondary factor after scale, coupling, and governance.

### 2026 Tooling Snapshot

By 2026 monorepos are **mainstream** — published industry surveys put adoption at `~63%` for organisations with `50+` developers. The 2026 tool selection has converged on three options:

| Tool | 2026 fit | Notes |
|------|----------|-------|
| **pnpm workspaces + Turborepo** | JavaScript / TypeScript monorepos that need fast task orchestration with minimal setup | Turborepo is a task runner with intelligent caching on top of an npm / pnpm / yarn workspace; Turborepo wins on simplicity. pnpm workspaces give stricter dependency hygiene than npm / yarn. |
| **Nx** | JS/TS monorepos at scale needing affected-detection, project-graph awareness, generators, and a deeper integrated ecosystem | Nx builds a full project graph mapping which packages depend on which; "affected" commands stay precise as the repo grows. Nx wins on scale. |
| **Bazel** | Multi-language (`Go`, `Java`, `Python`, `C++` etc.) and very large repos (typically `1000+` engineers) demanding hermetic, remote-executable builds | High setup cost; reserve for cases where the multi-language + remote execution combination is the binding constraint. |

Heuristic: start with **pnpm + Turborepo** for new JS/TS monorepos in 2026; migrate to **Nx** only after measuring that the project-graph + affected-detection investment is justified by repo size or shared-library coordination cost; reach for **Bazel** only when multi-language hermetic builds are the requirement.

### AI Agent Context Files (CLAUDE.md / AGENTS.md / GEMINI.md)

In 2026, every monorepo serving AI coding agents (Claude Code, Cursor, Copilot, Codex CLI, Antigravity / Gemini CLI) needs **per-package agent context files** in addition to the root project constitution:

- The repo root carries `CLAUDE.md` / `AGENTS.md` (the project constitution) — testing conventions, file-layout rules, non-negotiable policies. See `scribe/reference/adr-writing.md` for the constitution-vs-ADR separation.
- Each package or app under `apps/` / `packages/` MAY carry its own scoped `AGENTS.md` with package-specific conventions (the agent reads the nearest one to the file it is editing).
- DTCG design tokens, OpenAPI specs, and other machine-readable artefacts ship as first-class files so AI agents do not hallucinate brand values, schema fields, or token names. See `quill/reference/readme-templates.md` for the `llms.txt` companion pattern.
- Anti-pattern: leaving the root constitution stale while updating individual package READMEs — agents read the *nearest* relevant doc, so contradiction between the two paths produces silently wrong output.

## 6. Grove Integration

Use this reference in Grove as follows:
1. Detect whether the repository is mono, poly, or hybrid.
2. Screen `MS-01` through `MS-07`.
3. Choose strategy recommendations from the decision matrix.
4. Report governance and ownership health explicitly.

Quality gates:
- hyperscale imitation requires scale-fit evidence
- no measured pain means no split recommendation
- tight package coupling requires stronger boundary enforcement
- giant cross-team PRs require staged refactor planning
- missing CODEOWNERS requires ownership definition

**Source:** [Buildkite: Monorepo vs. Polyrepo](https://buildkite.com/resources/blog/monorepo-polyrepo-choosing/) · [CrashBytes: Code Ownership Patterns](https://crashbytes.com/blog/code-ownership-patterns-polyrepo-vs-monorepo-architectures) · [CircleCI: Monorepo Dev Practices](https://circleci.com/blog/monorepo-dev-practices/) · [DEV.to: Notes on the Monorepo Pattern](https://dev.to/david_whitney/notes-on-the-monorepo-pattern-5egc)
