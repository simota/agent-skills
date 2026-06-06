# Design Document Templates (HLD/LLD)

Purpose: Use this file when you need architecture-level or module-level design that stays traceable to requirements and actionable for implementation.

Contents:

- HLD template
- LLD template
- scaling, configuration, and rollback anchors
- design quality checklist

## HLD (High-Level Design) Template

```markdown
# HLD: [Feature Name]

## Document Info
| Field | Value |
|-------|-------|
| Version | v0.1 |
| Status | Draft |
| Audience | Architects, senior developers |
| Related PRD/SRS | [links] |

## Change History
| Date | Version | Author | Change |
|------|---------|--------|--------|

## 1. Overview
- purpose
- scope
- audience
- constraints

## 2. Architecture
### 2.1 System Context
[C4-style or equivalent]

### 2.2 Component Overview
| Component | Responsibility | Interfaces |
|-----------|----------------|------------|
| API | request handling | REST |
| Auth Service | identity checks | internal RPC |

## 3. Component Design
### 3.1 [Component Name]
- responsibilities
- dependencies
- failure handling

## 4. Data Design
### 4.1 Data Model Overview
[entities and ownership]

### 4.2 Database Selection
- primary store
- access pattern
- consistency choice

## 5. Integration Design
### 5.1 External Integrations
| Integration | Purpose | Failure Mode | Mitigation |
|-------------|---------|--------------|------------|

## 6. Security Design
- authn/authz
- secrets
- threat considerations

## 7. Deployment & Operations
### 7.1 Environment Model
- dev / staging / prod

### 7.2 Scaling Strategy
| Layer | Strategy | Trigger |
|-------|----------|---------|
| API | Horizontal | `CPU > 70%` |
| Database | Read replicas | `Connections > 80%` |
| Cache | Cluster mode | `Memory > 80%` |

## 8. Non-Functional Considerations
### 8.1 Performance
- latency target
- throughput target

### 8.2 Reliability
- availability
- failover

### 8.3 Observability
- logs
- metrics
- traces
```

## LLD (Low-Level Design) Template

```markdown
# LLD: [Feature Name]

## Document Info
| Field | Value |
|-------|-------|
| Version | v0.1 |
| Status | Draft |
| Related HLD | `HLD-[name]` |
| Audience | Developers |

## 1. Module Design
### 1.1 [Module Name]
#### Responsibilities
- [responsibility]

#### Interface Definitions
| Method | Input | Output | Errors |
|--------|-------|--------|--------|
| `login()` | `LoginDto` | `AuthResponse` | `AUTH_001`, `AUTH_002` |

#### Method Specifications
- preconditions
- business rules
- side effects

## 2. Data Structures
### 2.1 Database Schema
| Table | Key Columns | Constraints |
|-------|-------------|-------------|
| `users` | `id`, `email`, `status` | `email` unique |

### 2.2 Cache Structure
- key pattern
- invalidation
- `TTL: 86400 seconds (24 hours)`

## 3. Sequence Diagrams
### 3.1 Login Flow
- request
- validation
- auth
- token issue

### 3.2 Token Validation Flow
- request
- token parse
- claims validation

## 4. Error Handling
### 4.1 Error Codes
| Code | Status | Meaning | Recovery |
|------|--------|---------|----------|
| `AUTH_001` | `400` | Invalid email format | Fix email input |
| `AUTH_002` | `401` | Invalid credentials | Retry with correct credentials |
| `AUTH_003` | `403` | Account locked | Wait and retry |
| `AUTH_004` | `401` | Token expired | Re-authenticate |
| `AUTH_005` | `401` | Token invalid | Re-authenticate |

## 5. Configuration
### 5.1 Environment Variables
| Variable | Meaning | Default | Required |
|----------|---------|---------|----------|
| `JWT_SECRET` | JWT signing secret | - | Yes |
| `JWT_EXPIRES_IN` | Token expiry | `24h` | No |
| `BCRYPT_ROUNDS` | Password hash rounds | `12` | No |
| `MAX_LOGIN_ATTEMPTS` | Before lockout | `5` | No |
| `LOCKOUT_DURATION` | Lock duration (min) | `30` | No |

## 6. Testability
- unit-test seam
- integration-test seam
- mocks / fixtures

## 7. Release Considerations
### 7.1 Migration Plan
- forward migration

### 7.2 Rollback Plan
- rollback steps
- backward-compat assumptions
```

## Design Document Quality Checklist

### HLD

- [ ] Audience and scope are explicit
- [ ] Components and interfaces are visible
- [ ] NFRs are measurable
- [ ] Security and deployment sections exist
- [ ] Scaling triggers are explicit

### LLD

- [ ] Traceable to HLD
- [ ] Module and interface contracts are explicit
- [ ] Error handling is documented
- [ ] Configuration is documented
- [ ] Migration and rollback are documented where relevant
