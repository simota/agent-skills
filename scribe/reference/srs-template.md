# SRS (Software Requirements Specification) Template

Purpose: Use this file for technical requirements, interfaces, measurable NFRs, and system behavior that implementation teams must follow.

Contents:

- full SRS template
- canonical performance, security, and reliability examples
- SRS quality checklist

## Template

```markdown
# SRS: [Feature Name]

## Document Info
| Field | Value |
|-------|-------|
| Version | v0.1 |
| Status | Draft |
| Author | [name] |
| Reviewers | [lead roles] |
| Audience | Dev, Architect, QA |
| Related PRD | `PRD-[name]` |

## Change History
| Date | Version | Author | Change |
|------|---------|--------|--------|
| YYYY-MM-DD | v0.1 | [name] | Initial draft |

## 1. Introduction
### 1.1 Purpose
[why this SRS exists]

### 1.2 Scope
[in-scope and out-of-scope technical surface]

### 1.3 Definitions & Abbreviations
- JWT
- RBAC
- p95

### 1.4 References
- PRD
- HLD
- API contracts

## 2. System Overview
### 2.1 System Context
[ASCII, Mermaid, or concise narrative]

### 2.2 System Features
- [feature area]

## 3. Functional Requirements
### 3.1 [Feature Area]
#### `FR-001`: [Requirement title]
- Input: [request or event]
- Processing: [key business rule]
- Output: [response or side effect]
- Error conditions:
  - invalid email -> `AUTH_001`, `400`
  - invalid credentials -> `AUTH_002`, `401`
  - account locked -> `AUTH_003`, `403`
- Acceptance criteria:
  - Given valid credentials
  - When the login API is called
  - Then a token is returned
  - And the token expires in `24 hours`

#### `FR-002`: [Requirement title]
- ...

## 4. Data Requirements
### 4.1 Data Model
| Entity | Fields | Notes |
|--------|--------|-------|
| User | `id`, `email`, `passwordHash`, `status` | [constraints] |

### 4.2 Data Relationships
- User -> Session: `1:N`

### 4.3 Data Validation Rules
- email must be valid format
- password length `8-128`

## 5. Interface Requirements
### 5.1 API Specification
#### `POST /api/v1/auth/login`
Request:
```json
{ "email": "user@example.com", "password": "secret" }
```

Success:
```json
{ "token": "jwt", "expiresAt": "2026-03-07T00:00:00Z" }
```

Failure:
```json
{ "code": "AUTH_002", "message": "Invalid credentials" }
```

### 5.2 External Interfaces
- identity provider
- email service

## 6. Non-Functional Requirements
### 6.1 Performance
| ID | Metric | Target |
|----|--------|--------|
| `NFR-P001` | Login API response time | `p95 < 200ms` |
| `NFR-P002` | Token validation | `p95 < 50ms` |
| `NFR-P003` | Concurrent logins | `100/sec` |

### 6.2 Security
| ID | Requirement | Target |
|----|-------------|--------|
| `NFR-S001` | Password hashing | `bcrypt`, cost `12` |
| `NFR-S002` | Token encryption | `JWT` with `RS256` |
| `NFR-S003` | Rate limiting | `10 req/min per IP` |
| `NFR-S004` | Audit logging | all auth events |

### 6.3 Reliability
| ID | Requirement | Target |
|----|-------------|--------|
| `NFR-R001` | Availability | `99.9%` |
| `NFR-R002` | MTTR | `< 5 min` |
| `NFR-R003` | Data durability | `99.999%` |

### 6.4 Scalability
| ID | Requirement | Target |
|----|-------------|--------|
| `NFR-SC001` | Horizontal scaling | auto-scale at `70% CPU` |
| `NFR-SC002` | Database connections | pool size `20-100` |

### 6.5 Maintainability
| ID | Requirement | Target |
|----|-------------|--------|
| `NFR-M001` | Code coverage | `> 80%` |
| `NFR-M002` | Documentation | all public APIs |
| `NFR-M003` | Logging | structured JSON logs |

## 7. Constraints
### 7.1 Technical Constraints
- `JWT_EXPIRES_IN=24h`
- `BCRYPT_ROUNDS=12`
- `MAX_LOGIN_ATTEMPTS=5`
- `LOCKOUT_DURATION=30`

### 7.2 Business Constraints
- [release or compliance constraint]

### 7.3 Regulatory Constraints
- [privacy, audit, retention]

## 8. Assumptions & Dependencies
### 8.1 Assumptions
- [assumption]

### 8.2 Dependencies
| ID | Dependency | Owner | Status | Used By |
|----|------------|-------|--------|---------|
| `D-001` | User table schema | Schema | Done | `FR-001` |
| `D-002` | JWT signing keys | DevOps | Pending | `FR-001` |

## 9. Traceability Matrix
| PRD Requirement | SRS Requirement | Test Cases | Design |
|-----------------|-----------------|------------|--------|
| `REQ-001` | `FR-001` | `TC-001`, `TC-002` | `HLD-3.1` |

## 10. Appendix
- state diagrams
- sequence diagrams
- glossary
```

## SRS Quality Checklist

- [ ] All functional requirements have IDs (`FR-XXX`)
- [ ] NFRs are measurable
- [ ] Error codes and statuses are explicit
- [ ] Interface contracts include request, success, and failure shapes
- [ ] Constraints and dependencies are recorded
- [ ] Traceability maps back to PRD and forward to tests/design
