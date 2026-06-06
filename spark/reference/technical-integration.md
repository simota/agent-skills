# Spark Technical Integration Patterns Reference

Purpose: define how Spark hands proposals to Sherpa or Builder and how technical constraints should appear in the proposal.

## Contents
- Direct Builder handoff
- DDD guidance
- API integration requirements
- Sherpa feedback loop
- Scope adjustment rules
- Handoff checklists

## Direct Builder Handoff

### `## SPARK_TO_BUILDER_HANDOFF`

Use direct Builder handoff when:
- the feature is simple and independent
- the risk is low and the requirements are clear
- an existing implementation pattern already exists
- the estimate is hours-level

Prefer Sherpa when:
- the work is multi-step
- dependencies or uncertainty are material
- the estimate is `1 day or more`

### Direct handoff packet

Required fields:
- `Feature`
- `Proposal Doc`
- `Bypass Sherpa`
- `Technical Specification`
  - `Core Requirement`
  - `User Story`
  - `Domain Model Requirements`

Checklist before direct Builder handoff:
- feature is simple (`< 4 hours estimate`)
- existing patterns can be followed
- no external dependency is unresolved
- risk is low
- technical requirements are explicit

## DDD Guidance

### `## DDD Pattern Recommendation`

Choose the lightest appropriate pattern:

| Scenario | Pattern | Rationale |
| --- | --- | --- |
| uniquely identified concept | `Entity` | identity persists across state changes |
| value-only concept | `Value Object` | immutable and comparable by value |
| consistency boundary | `Aggregate Root` | transaction boundary and invariants |
| business logic outside a single entity | `Domain Service` | spans multiple aggregates |
| external interaction | `Infrastructure Service` | API, DB, messaging, or I/O concerns |

### Entity template

```markdown
### Entity: [EntityName]
- Identity
- Properties
- State Transitions
- Invariants
- Methods Expected
```

### Value Object template

```markdown
### Value Object: [VOName]
- Purpose
- Properties
- Creation Validation
- Equality
- Use Cases
```

Keep the expected signature when relevant:

```typescript
static create(raw: RawInput): Result<[VOName], ValidationError>
```

### Aggregate Root template

```markdown
### Aggregate Root: [AggregateName]
- Root Entity
- Child Entities
- Aggregate Invariants
- Transaction Boundary
```

## API Integration Requirements

### `## API Integration Requirements`

Required fields:
- `External API`
- `Purpose`
- `Connection Requirements`
- `Retry Strategy`
- `Rate Limiting`
- `Error Handling`
- `Data Validation`
- `Fallback Strategy`

Keep these default retry rules unless the target API requires something stricter:

| Error type | Retry? | Strategy | Max attempts |
| --- | --- | --- | --- |
| `5xx` | Yes | exponential backoff | `3` |
| `429` | Yes | honor `Retry-After` | `3` |
| `4xx` | No | fail immediately | `1` |
| timeout | Yes | exponential backoff | `3` |
| connection refused | Yes | linear backoff | `2` |

Backoff defaults:

```yaml
initial_delay: 1s
max_delay: 30s
multiplier: 2
jitter: 0.1
```

Circuit-breaker defaults:

```yaml
failure_threshold: 5
reset_timeout: 60s
half_open_requests: 3
```

## Sherpa Feedback Loop

### `## SHERPA_TO_SPARK_FEEDBACK`

Use when breakdown exposes feasibility, scope, dependency, risk, or resource concerns.

Required fields:
- `Feature`
- `Proposal Doc`
- `Feedback Type`
- `Breakdown Attempt Summary`
  - `Total Steps Identified`
  - `Estimated Total Time`
  - `High Risk Steps` (`0-1 acceptable`)
- `Feasibility Concerns`

### `## SPARK_ITERATION_ON_SHERPA_FEEDBACK`

Required fields:
- `Original Proposal`
- `Sherpa Feedback`
- `Iteration`
- `Accepted Adjustments`
- `Revised Scope`

## Scope Adjustment

### `## SCOPE_ADJUSTMENT`

Required fields:
- `Original Feature`
- `Adjustment Reason`
- `Impact Analysis`
- `Adjustment Options`

Preferred adjustments:

| Concern type | Impact | Preferred adjustment |
| --- | --- | --- |
| technically impossible | Critical | remove the feature or replace the approach |
| effort exceeds budget | High | phase split or MVP reduction |
| external dependency blocks progress | High | mock, async follow-up, or phased release |
| quality risk | Medium | add tests or staged release |
| performance concern | Medium | add limits or optimization requirements |

## Integration Workflow

Flow:
- Spark drafts the proposal
- send to `Sherpa` if complexity or uncertainty is material
- send directly to `Builder` only for simple, low-risk work
- if Sherpa pushes back, iterate the proposal before build

## Handoff Checklists

Before Sherpa handoff:
- user story is clear
- acceptance criteria are testable
- DDD hints are suggested, not over-specified
- API requirements are listed when relevant
- priority is explicit

After Sherpa feedback:
- review every concern
- choose the adjustment path
- update the proposal document
- communicate scope changes
- resubmit if needed
