# Module Boundary Evaluation

Load for a module split/merge, cross-context API, or language-specific boundary review. Bind compiler/toolchain and dependency claims to the target repository via `_common/builder/reference/implementation-policy.md` § Language and Toolchain Grounding; do not select a framework or change a language version from a cheatsheet.

## Boundary Evidence

For each pair, record public surface, import direction, domain-type translation, infrastructure-type leaks, persistence owner, and commit co-change. Keep file/line and manifest evidence with the finding. Count co-change over the same declared window (normally 180 days), deduplicate a module within each commit, and state the denominator; identical names do not prove identical domain semantics.

| Signal | Review criterion / next action |
|--------|--------------------------------|
| Public surface | Healthy target: fewer than 10 public types/functions exposed to the other module; 10+ imports is a chatty-boundary signal. |
| Directionality | Prefer one direction. A module-level cycle invokes `reference/circular-dependency-remediation.md`. |
| Translation / purity | Across distinct domains, translate types; external provider objects, raw DB rows and HTTP types must not silently become another context's domain model. Insert an ACL at the integration boundary, not a second domain model everywhere. |
| Data ownership | Identify one persistence owner. Two contexts mutating the same tables require an ownership/synchronization decision. |
| Co-change | Below 30% is the healthy target. Above 60% **plus shared vocabulary** is a merge candidate, not an automatic merge. |
| Concentration | More than 20% of total package imports is a God-module review signal; corroborate with responsibilities and churn. |
| Shared kernel | Symmetric 15+ cross-module imports may justify a small frozen kernel. Do not move business logic into a growing `common` bucket. |
| Entity/behavior leakage | Check feature envy, raw entities reused with different meanings, anemic public records whose decisions live in neighbors, and `any`/generic type tunneling. |

These criteria select an investigation; they do not authorize a code or architecture change. Atlas proposes; the appropriate implementer executes the approved plan.

## Split / Merge / Harden

| Evidence | Proposal |
|----------|----------|
| High co-change and one vocabulary | Merge the over-split context. |
| Shared table, divergent domain logic | Separate ownership with an explicit synchronization/event contract. |
| External/legacy model leaking inward | Translate at an adapter, facade, repository implementation, or event boundary; choose the actual leaking seam. |
| Same team, low coordination cost | A thinner boundary may be sufficient. |
| Different teams, repeated coordination failures | Harden the versioned public contract. |

## Language-Specific Evidence

Use installed, repository-configured analyzers; adding a plugin or dependency is not implied. Verify command options with the installed tool's help and the matching official documentation.

| Target | Evidence to collect |
|--------|---------------------|
| Rust | `Cargo.toml` workspace/features and `cargo tree --workspace`; `cargo tree --duplicates` locates multiple dependency versions, **not cycles**. Distinguish crate dependency constraints from cycles between modules inside one crate. Check public re-exports, trait bounds and API compatibility against the declared MSRV/features. |
| Kotlin/JVM / KMP | Gradle project/source-set graph, exported `api` versus implementation dependencies, JVM/public ABI and `expect`/`actual` contracts. Use configured dependency/API validation tasks; never assume a graph/health plugin is installed. A language/toolchain or concurrency-default change requires target-version evidence and an ADR when it changes a boundary. |
| Swift | `Package.swift`, target/product edges, `swift package show-dependencies --format dot` and `swift package dump-package`. For a public API change, use `swift package diagnose-api-breaking-changes <baseline-revision>` where the installed SDK/target supports it. Check visibility, concurrency isolation and deployment targets in the actual build settings; do not infer them from the newest language release. |

Visibility syntax, library shopping lists, fixed compile-time/LOC quotas, and blanket SemVer mappings are not boundary evidence. Use compiler/API diagnostics and the project's compatibility policy instead.

## Report

Include: scope and toolchain; module count; each boundary pair with surface/direction/translation/purity/owner/co-change evidence; prioritized smells; the chosen merge/split/ACL/contract proposal and rejected alternative; migration order, effort and risk; implementation handoff; and a fitness function with a baseline and target. Do not manufacture co-change or coupling values when only import text was inspected.

Canonical command references (checked 2026-09-17):
- https://doc.rust-lang.org/cargo/commands/cargo-tree.html — graph scope, feature interpretation and duplicate versions.
- https://docs.swift.org/latest/documentation/packagemanagerdocs/packagediagnoseapibreakingchange/ — baseline comparison and target/toolchain support.
