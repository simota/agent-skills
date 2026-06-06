# Documentation Architecture Anti-Patterns

Purpose: Use this reference when auditing `docs/`, preventing doc rot, or aligning repository documentation with code and operations.

## Contents

- Documentation anti-pattern catalog
- Documentation decay model
- Docs-as-code rules
- Audience-oriented structure
- Cross-repository consistency
- Grove integration

Documentation organization failures, docs-as-code traps, and drift prevention.

## 1. Documentation Architecture Anti-Patterns

| ID | Anti-Pattern | What Goes Wrong | Typical Signals | Recommended Response |
|---|---|---|---|---|
| **DA-01** | **Doc Drift** | Documentation does not keep up with code changes. | Deprecated APIs are still documented; removed fields or stale code samples remain. | Keep docs in the same repo, require docs updates in PRs, and review docs during change approval. |
| **DA-02** | **Single-Owner Fossil** | One person implicitly owns all documentation. | When that person leaves, documentation stops evolving. | Use shared ownership and CODEOWNERS-based review paths. |
| **DA-03** | **Audience Blindness** | One generic document tries to serve every reader. | Backend, frontend, and operations teams all find the docs incomplete. | Split docs by audience and job-to-be-done. |
| **DA-04** | **Intent Amnesia** | Docs explain what exists but not why it exists. | No ADRs, repeated historical debates, old design mistakes reappear. | Add ADRs and explicit invariants for critical decisions. |
| **DA-05** | **Wiki Graveyard** | Docs are scattered across wikis and drift away from code. | No version history, weak searchability, pages untouched for years. | Consolidate canonical docs into `docs/` under version control. |
| **DA-06** | **Text-Only Complex Systems** | Complex systems are explained without diagrams. | Teams disagree on retries, idempotency rules, or service boundaries. | Require sequence, architecture, or data-flow diagrams where the system is non-trivial. |
| **DA-07** | **Post-Implementation Docs** | Documentation is treated as aftercare instead of part of delivery. | PRs modify behavior without doc changes; intent is unclear in review. | Add doc checks to the PR workflow and CI. |

## 2. Documentation Decay Model

| Stage | Description | Typical age / signal | Response |
|---|---|---|---|
| Fresh | Code and docs are aligned. | Updated together | Keep as-is |
| Stale | Small inconsistencies exist. | `1-3 months` behind | Update in the next change touching the area |
| Misleading | Docs contradict implementation. | `3-6 months` behind | Treat as a correctness issue and fix urgently |
| Fossil | Nobody trusts or updates the docs. | Old, unused, confusing | Archive or replace |

Detection checklist:
- Compare doc update timestamps with related source changes.
- Run broken-link checks.
- Validate code snippets where practical.
- Review diagrams and deprecated references quarterly.

## 3. Docs-as-Code Rules

Core rule:
- Documentation is a product component. Apply version control, review, and validation discipline.

Recommended practices:
- Keep canonical docs in `docs/`, not only in a wiki.
- Use Git-backed review and rollback for document changes.
- Add CI warnings for code changes with no matching docs updates.
- Organize docs along user journeys, then by depth.
- Optimize for searchability and incident-time retrieval.

## 4. Audience-Oriented Structure

Use explicit doc layers:

```text
docs/
  architecture/
    adr/
    diagrams/
    invariants/
  operations/
    runbooks/
    alerts/
    deployment/
  guides/
    getting-started/
    contributing/
    troubleshooting/
  api/
    openapi/
    examples/
```

State critical invariants explicitly, for example:
- a service dependency that must never exist
- an idempotency guarantee
- a cascade deadline for destructive actions

## 5. Cross-Repository Consistency

In multi-repository environments, document debt often appears as terminology drift and style drift.

Recommended controls:
- share a documentation style guide
- maintain a glossary for domain terms
- use a review checklist for terminology and diagrams
- run a quarterly cross-repository consistency audit

## 6. Grove Integration

Use this reference in Grove as follows:
1. Screen `DA-01` through `DA-07` during `SCAN`.
2. Combine documentation findings with `AP-005` and `AP-006`.
3. Fold the result into the Doc Completeness score.
4. Route doc-structure remediation to Scribe when needed.

Quality gates:
- code changed without docs: warn on the PR
- one person owns all docs: recommend shared ownership
- no ADR directory: propose one
- wiki-only canonical docs: propose migration into `docs/`
- distributed system with no diagrams: require diagram creation
- implementation PR with no docs consideration: apply the checklist

**Source:** [DeepDocs: Technical Documentation Best Practices](https://deepdocs.dev/technical-documentation-best-practices/) · [Qodo: Code Documentation Best Practices](https://www.qodo.ai/blog/code-documentation-best-practices-2026/) · [42 Coffee Cups: Technical Documentation Best Practices 2025](https://www.42coffeecups.com/blog/technical-documentation-best-practices)
