# Launch Collaboration Patterns

Purpose: Use this file when the release task spans multiple agents and you need the minimum safe handoff shape or orchestration pattern.

## Contents

1. Collaboration patterns
2. Standard orchestration paths
3. Minimum payload expectations

## 1. Collaboration Patterns

| Pattern | Flow | Use when | Output from Launch |
|---------|------|----------|--------------------|
| `A` | `Plan -> Launch -> Guardian` | release scope and timeline already exist | version, tag, CHANGELOG, branch strategy |
| `B` | `Builder -> Launch -> Gear` | completed features are ready to ship | deployment request, release metadata, flags |
| `C` | `Launch -> Quill` | release docs must be published | CHANGELOG, notes, doc update list |
| `D` | `Launch -> Canvas` | release timeline or rollout needs a diagram | timeline / rollout visualization request |
| `E` | `Launch -> Triage` | post-release incident response needs a playbook | rollback triggers, recovery steps |
| `F` | `Launch <-> Builder` | feature flags require implementation alignment | flag design, rollout stages, cleanup timing |

## 2. Standard Orchestration Paths

### Standard release

`Plan -> Launch -> Guardian -> Gear -> Launch (verify)`

### Hotfix release

`Triage -> Launch -> Guardian -> Gear -> Triage (monitor)`

### Feature release with flags

`Plan -> Launch -> Builder (flag) -> Launch -> Gear -> Launch (rollout)`

### Documentation-heavy release

`Launch -> Quill -> Guardian -> Gear`

## 3. Minimum Payload Expectations

### Input from `Plan`

- release scope
- target date
- release type
- explicit blockers or constraints

### Input from `Builder`

- completed features
- tested status
- flag integration status
- rollout readiness

### Input from `Gear`

- pipeline readiness
- environment readiness
- deploy timing constraints

### Output to `Guardian`

- version
- tag
- branch strategy
- release commit guidance

### Output to `Gear`

- deployment request
- environment
- rollout method
- feature flag stages
- rollback method

### Output to `Triage`

- rollback triggers
- rollback procedure
- incident playbook notes

### Output to `Canvas`

- timeline type
- milestones
- rollout stages

### Output to `Quill`

- CHANGELOG location
- release notes location
- docs update scope
