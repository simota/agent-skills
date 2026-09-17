# Dependency Cleanup

Load for package-removal proposals. Apply `reference/cleanup-protocol.md` and the SKILL's confidence/confirmation gates; tools produce candidates, not authorization.

## Implicit Consumers

| Candidate | Evidence needed before removal |
|---|---|
| Build / PostCSS / Babel plugin | Tool configuration, presets, generated build scripts |
| `@types/*` | Type discovery, `types`/`typeRoots`, public declarations and supported TS targets; no blanket ignore |
| Peer dependency | Published package/host contract and consumer installation matrix |
| CLI | Package scripts, CI tasks, hooks, docs and local workflows |
| Polyfill | Runtime/global initialization and supported browser/platform matrix |
| Dev server | Development/test workflows, not production graph alone |

For all packages inspect source, scripts, config, CI and docs. An analyzer's production-only mode cannot prove a development dependency unused. Resolve actual tool syntax through `reference/language-patterns.md`; do not run autofix, overwrite requirements, tidy a manifest or enable warning-only CI during detection.

## Execution Handoff

Provide Builder the manifest/lockfile snapshot and approved ≥90-confidence candidates, one package or one category per reversible change. After implementation require install, build, tests and relevant dev-server startup; inspect lockfile diffs for unrelated/transitive removals. Report failed or unavailable checks, never hide them. Use the project's security audit and refresh its SBOM during major cleanup cycles; vulnerability remediation is a separately scoped security task.

Report each Package, Type (production/development/peer), Size, Last Used/evidence, Recommendation and verification result. Missing measurements remain unknown. Reclaimed install size and shipped-bundle impact are different measurements.
