# Feature Flag Pitfalls & Lifecycle Management

Purpose: Use this file when you need feature-flag debt controls, lifecycle rules, cleanup thresholds, or rollout guardrails.

## Contents

1. Feature flag anti-patterns
2. Debt impact
3. Lifecycle model
4. Cleanup strategy
5. Launch enforcement points

## 1. Feature Flag Anti-Patterns

| ID | Anti-pattern | What goes wrong | Guardrail |
|----|--------------|-----------------|-----------|
| `FF-01` | Stale flag | Dead branches and cognitive load accumulate after the flag is no longer useful | Set expiry on creation; clean regularly |
| `FF-02` | Orphaned flag | No owner can decide cleanup or rollout policy | Require an owner on creation |
| `FF-03` | Nested flag | Test paths grow exponentially | Maximum nesting depth: `1` |
| `FF-04` | Weak naming | Purpose and lifecycle are unclear | Use prefixes such as `temp_`, `exp_`, `ops_`, `perm_` |
| `FF-05` | Business logic behind flags | Flag removal becomes a production risk | Use flags for exposure control, not core business logic |
| `FF-06` | Missing ON/OFF tests | One path rots silently | Require both ON and OFF tests |
| `FF-07` | Too many active flags | Debugging and rollout reasoning collapse | Require approval when active flags exceed `50` |
| `FF-08` | No fallback | Flag service failure creates undefined behavior | Define a fallback value for every flag |

## 2. Debt Impact

Feature flag debt primarily harms:

- runtime overhead
- developer productivity
- test complexity
- unexpected behavior and accidental exposure

Operational takeaway:

- do not treat flags as free
- plan cleanup at creation time

## 3. Lifecycle Model

### Default lifecycle

`CREATE -> ROLLOUT -> STABLE -> CLEANUP -> REMOVED`

Required fields by stage:

| Stage | Required fields |
|-------|-----------------|
| `CREATE` | owner, purpose, type, expiry, fallback, cleanup ticket |
| `ROLLOUT` | stages, success criteria, rollback trigger |
| `STABLE` | 100% reached, no harmful side effects, stable metrics |
| `CLEANUP` | code removal PR, updated tests |
| `REMOVED` | code deleted, flag-service entry deleted |

### Type-specific lifespan

| Type | Recommended life | Warning | Forced cleanup |
|------|------------------|---------|----------------|
| `Release Flag` (`temp_`) | `7-30 days` | `14 days` | `60 days` |
| `Experiment Flag` (`exp_`) | `14-60 days` | `30 days` | `90 days` |
| `Ops Flag` (`ops_`) | long-lived allowed | `90 days` review | none |
| `Permission Flag` (`perm_`) | long-lived allowed | `180 days` review | none |

## 4. Cleanup Strategy

Recommended detection methods:

| Method | Precision | Cost |
|--------|-----------|------|
| Manual audit | Low | High |
| Static analysis | High | Medium |
| Usage metrics | High | Low |
| CI age checks | Medium | Low |

Best practices:

- create cleanup tickets with the flag
- include removal in the definition of done
- review flags every sprint
- run periodic cleanup work

## 5. Launch Enforcement Points

- Block flag creation without owner (`FF-02`).
- Block flag creation without fallback (`FF-08`).
- Warn when nesting depth exceeds `1` (`FF-03`).
- Require approval when active flags exceed `50` (`FF-07`).
- Force cleanup for release flags older than `60 days` (`FF-01`).
