# Documentation Anti-Patterns and Writing Guidelines

Purpose: Use this file when a draft is weak, vague, bloated, untestable, structurally broken, or exhibits AI-generation artifacts. Covers requirements, design, test, and AI-assisted documentation.

## Requirements Writing (RW)

| ID | Anti-Pattern | Risk | Prevention |
|----|--------------|------|------------|
| `RW-01` | Mistaking length for quality | Long PRDs hide the core ask | Keep PRDs to `2-5 pages`; prioritize hypotheses and metrics |
| `RW-02` | Missing non-goals | Scope creep; AI agents implement what isn't excluded | Make `Non-Goals` mandatory |
| `RW-03` | Vague success criteria | No completion signal | Require KPI, target value, and measurement method |
| `RW-04` | Over-specifying implementation | Removes engineering discretion | PRD = `What` and `Why`; move `How` to design docs |
| `RW-05` | Missing business context | Weak prioritization and poor tradeoffs | Add hypothesis and expected impact |
| `RW-06` | Untestable requirements | No reliable acceptance decision | Add Given-When-Then for every requirement |
| `RW-07` | Vague adjectives | "user-friendly" and "fast" are unmeasurable | Replace with quantitative targets |

PRD quality gates — reject if any are missing:

- Requirement IDs (`REQ-XXX`) and acceptance criteria
- `Non-Goals` section
- Measurable success metrics (KPI + target + method)
- `What`/`Why` focus (no implementation `How`)
- Edge cases and dependencies

## Design Documents

### HLD (HD)

| ID | Anti-Pattern | Risk | Prevention |
|----|--------------|------|------------|
| `HD-01` | Skipping requirements | Design drifts from needs | Enforce `Requirements -> HLD -> LLD` |
| `HD-02` | Over-engineering | Complexity and delay | Design for current requirements plus clear extension points |
| `HD-03` | Ignoring scalability | Late rewrites | Add measurable NFRs early |
| `HD-04` | Undefined relationships | Hidden coupling | Define interfaces and dependency diagrams |
| `HD-05` | Security as afterthought | Expensive late fixes | Include threat modeling |
| `HD-06` | Low document quality | Misinterpretation | Require diagrams, updates, and review |
| `HD-07` | Audience mismatch | Document unusable for decisions | State audience and tune detail level |

### LLD (LD)

| ID | Anti-Pattern | Risk | Prevention |
|----|--------------|------|------------|
| `LD-01` | Ignoring SOLID | God classes and brittle changes | Apply SOLID checks during design |
| `LD-02` | Re-inventing patterns | Inconsistent implementation | Select known patterns and record why |
| `LD-03` | Unclear code shape | Implementers misread intent | Use naming rules, examples, and sequence diagrams |
| `LD-04` | Missing test strategy | Hard-to-test implementations | Add unit, integration, and E2E strategy |
| `LD-05` | Excessive implementation detail | Document becomes stale code shadow | Focus on decisions, contracts, and flows |
| `LD-06` | Breaking from HLD | Architectural drift | Preserve HLD-to-LLD traceability |

Design gates — reject if any are missing:

- Requirements document exists before HLD
- NFR section with measurable targets
- Interface and dependency definitions
- Audience declaration
- HLD reference in LLD (traceability)
- Design review or update path

## Test Documentation (TD)

| ID | Anti-Pattern | Risk | Prevention |
|----|--------------|------|------------|
| `TD-01` | Only one test type | Coverage imbalance | Follow the test pyramid (`70:20:10`) |
| `TD-02` | Wrong test type | Slow and noisy feedback | Define purpose per test layer |
| `TD-03` | Testing wrong functionality | High-value paths under-tested | Prioritize by business impact and change frequency |
| `TD-04` | Testing implementation | Refactors break tests | Test public behavior and observable outcomes |
| `TD-05` | Coverage fetish | High numbers with weak signal | Measure meaningful coverage and mutation quality |
| `TD-06` | Flaky or slow suites | CI distrust | Set execution budgets and fix flakes immediately |
| `TD-07` | Test code as second class | Test debt grows fast | Review and refactor like production code |

Additional pitfalls:

- Manual execution as default
- Bug fixes without regression tests
- Dogmatic TDD where it hurts discovery
- Hard-coded test data instead of factories

Test quality metrics:

| Metric | Target |
|--------|--------|
| `PDWT` (defects found by written tests) | `>= 70%` |
| `PTVB` (tests validating business logic) | `>= 60%` |
| `PTD` (tests with documented intent) | `>= 80%` |

Test gates — reject if any are missing:

- Explicit test type and scope
- Positive, negative, and boundary cases
- Expected result per case
- Traceability to requirement IDs

## AI-Assisted Documentation (AD)

| ID | Anti-Pattern | Risk | Prevention |
|----|--------------|------|------------|
| `AD-01` | Context overload | Redundant output, poor focus, high token cost | Load only structured minimum context |
| `AD-02` | Skipping human review | Missed tacit knowledge and bad assumptions | AI output is draft; human reviews before progression |
| `AD-03` | Curse of instructions | Quality degrades when rules exceed `~200` | Keep prompts focused; `300+` lines is a warning sign |
| `AD-04` | Generic filler | Docs lack project specificity | Require project-specific examples and constraints |
| `AD-05` | Template monoculture | Wrong structure for the reader | Choose template by document type and audience |
| `AD-06` | No specification before implementation | Hidden assumptions, hard maintenance | Follow `Specify -> Plan -> Tasks -> Implement` |
| `AD-07` | No feedback loop | Same failures repeat | Run INSCRIBE and update patterns |
| `AD-08` | READMEtitis | Cliché-filled, formal but empty prose | Reject GitHub-README-style filler; demand actionable content |
| `AD-09` | Version drift | LLM generates outdated API patterns | Verify technical details against current docs |
| `AD-10` | One-shot docs | Generated once, never updated | Require update ownership and decay tracking |
| `AD-11` | Confident hallucination | AI fabricates APIs or specs with certainty | Cross-check generated references against real sources |

Context strategy:

| Rule | Guidance |
|------|----------|
| Load only what is needed | Keep active context below `30%` of budget |
| Prioritize hierarchy | main contract -> template -> one targeted anti-pattern ref |
| Separate draft from approval | AI drafts; humans approve |

## Writing Examples

### Requirement (Good)

```markdown
**REQ-001**: User can log in with an email address.
- Input: Email (RFC 5322), password (8-128 chars)
- Success: JWT token, status 200
- Failure: `AUTH_001`, status 401
- Rate limit: 5 req/min per IP
```

### Requirement (Bad)

```markdown
Enable user login
```

Fails: no input/output contract, no constraints, not testable.

### Acceptance Criteria (Good)

```markdown
**AC-001**: Successful login
Given a valid email and password
When the login API is called
Then a JWT token is returned
And the token expires in 24 hours
```

### Acceptance Criteria (Bad)

```markdown
Login should work
```

Fails: no preconditions, no action, no observable result.

### Checklist Item (Good)

```markdown
- [ ] **IMPL-001**: Add `login()` to `UserService`
  - Input: `LoginDto` (`email`, `password`)
  - Output: `AuthResponse` (`token`, `expiresAt`)
  - Exception: `InvalidCredentialsException`
  - Reference: `REQ-001`
```

### Checklist Item (Bad)

```markdown
- [ ] Implement login feature
```

Fails: no deliverable, no I/O contract, no traceability.

## Quick Rules

- One testable sentence over a long paragraph.
- `What` and `Why` in PRD; `How` in design docs.
- Every requirement maps to acceptance criteria, design, and tests.
- If a sentence cannot be verified, rewrite it.
- PMI: `39%` of project failure ties to weak requirements or design.
- Missing design review can increase downstream cost by `10-100x`.
