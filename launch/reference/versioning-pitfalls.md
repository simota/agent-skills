# Versioning Pitfalls & Breaking Change Management

Purpose: Use this file when you need SemVer failure modes, breaking-change checks, strategy selection, or pre-release guardrails.

## Contents

1. SemVer pitfalls
2. Breaking-change detection
3. Strategy mismatch
4. Dependency versioning pitfalls
5. Launch enforcement points

## 1. SemVer Pitfalls

| ID | Pitfall | What goes wrong | Guardrail |
|----|---------|-----------------|-----------|
| `VP-01` | Breaking changes in `MINOR` or `PATCH` | Downstream users treat the release as safe and break | Check for breaking changes explicitly |
| `VP-02` | Underestimating impact | Small local impact still causes downstream breakage | Require explicit breaking-change definition |
| `VP-03` | Staying on `0.x.y` too long | Users see permanent instability | Recommend `1.0.0` after `6 months` of practical use |
| `VP-04` | Fear of major bumps | Teams accumulate workarounds instead of shipping clean breaks | Use MAJOR releases deliberately when needed |
| `VP-05` | Overloading the version number | Version alone cannot explain impact | Pair versioning with clear CHANGELOG notes |
| `VP-06` | Forcing strict SemVer into CD | Versioning becomes noisy and low-signal | Consider `CalVer` or automated numbering |
| `VP-07` | Endless pre-release labels | Users stop trusting `alpha`, `beta`, `rc` | Put a time limit on pre-release stages |

## 2. Breaking-Change Detection

Three classes matter:

| Class | Detectability | Example |
|-------|---------------|---------|
| Syntactic | High | removed API, changed parameter, changed return type |
| Behavioral | Medium | same API, different runtime behavior |
| Semantic | Low | contract meaning changed, performance expectation changed |

Breaking-change checklist:

- removed or renamed public API
- new required parameter
- return type change
- changed default value
- changed error type or error condition
- same input now yields different behavior
- changed runtime requirement
- changed config format
- incompatible database schema change

## 3. Strategy Mismatch

| Project type | Good fit | Poor fit |
|--------------|----------|---------|
| OSS library | SemVer | CalVer |
| SaaS / CD | CalVer or automated numbering | strict SemVer everywhere |
| Mobile app | SemVer + build number | CalVer only |
| Internal tool | CalVer | SemVer only |
| API | URI/API version + SemVer | SemVer alone |

Pre-release rules:

- `alpha` / `beta` longer than `1 month` -> recommend stabilize or stop
- `rc` longer than `2 weeks` -> recommend ship or reset scope

## 4. Dependency Versioning Pitfalls

Common mistakes:

- overly wide ranges (`>=1.0.0`)
- full pinning without regular updates
- not committing lock files
- ignoring transitive dependency breakage

Default guidance:

- prefer caret or project-standard compatible ranges
- commit lock files
- automate dependency review
- update breaking dependencies manually

## 5. Launch Enforcement Points

- If a `MINOR` or `PATCH` release includes breaking changes, recommend `MAJOR` (`VP-01`).
- If a project stays on `0.x.y` for more than `6 months`, recommend a `1.0.0` plan (`VP-03`).
- If a pre-release phase exceeds `1 month`, recommend stabilization or cancellation (`VP-07`).
- If SemVer creates friction in CD-heavy environments, present `CalVer` as an explicit alternative (`VP-06`).
