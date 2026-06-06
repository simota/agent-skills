# Decision Templates

Output format templates and sample deliberations for Magi's verdict delivery.

---

## Full Deliberation Report Template

```markdown
# MAGI Deliberation Report

## Decision Request
- **Type**: [Architecture / Trade-off / Go-No-Go / Strategy / Priority]
- **Subject**: [Decision subject]
- **Requestor**: [User / Agent name]
- **Urgency**: [Low / Medium / High / Critical]
- **Reversibility**: [Low / Medium / High]

---

## Context Summary
[2-3 sentences describing the decision context, constraints, and what's at stake]

---
...
```

---

## Verdict Presentation (Special Effects)

The verdict presentation changes based on the consensus pattern, using dramatic ASCII art.

### 3-0: Unanimous Approval

```
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║                   M A G I   S Y S T E M                      ║
    ║                                                              ║
    ║           ┌─────────┐  ┌─────────┐  ┌─────────┐             ║
    ║           │  LOGOS  │  │ PATHOS  │  │ SOPHIA  │             ║
    ║           │  ██████ │  │  ██████ │  │  ██████ │             ║
    ║           │ APPROVE │  │ APPROVE │  │ APPROVE │             ║
    ║           └─────────┘  └─────────┘  └─────────┘             ║
    ║                                                              ║
    ║        ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░             ║
    ║        ░  ALL SYSTEMS GREEN — UNANIMOUS APPROVAL ░           ║
    ║        ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░             ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
```

### 2-1: Majority Decision

```
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║                   M A G I   S Y S T E M                      ║
    ║                                                              ║
    ║           ┌─────────┐  ┌─────────┐  ┌─────────┐             ║
    ║           │  LOGOS  │  │ PATHOS  │  │ SOPHIA  │             ║
    ║           │  ██████ │  │  ░░░░░░ │  │  ██████ │             ║
    ║           │ APPROVE │  │ REJECT  │  │ APPROVE │             ║
    ║           └─────────┘  └─────────┘  └─────────┘             ║
    ║                                                              ║
    ║        ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓             ║
    ║        ▓  MAJORITY RULE — 2:1 — DISSENT LOGGED  ▓           ║
    ║        ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓             ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
```

### 1-1-1: Split Decision

```
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║                   M A G I   S Y S T E M                      ║
    ║                                                              ║
    ║           ┌─────────┐  ┌─────────┐  ┌─────────┐             ║
    ║           │  LOGOS  │  │ PATHOS  │  │ SOPHIA  │             ║
    ║           │  ▒▒▒▒▒▒ │  │  ░░░░░░ │  │  ▓▓▓▓▓▓ │             ║
    ║           │ APPROVE │  │ REJECT  │  │ ABSTAIN │             ║
    ║           └─────────┘  └─────────┘  └─────────┘             ║
    ║                                                              ║
    ║        ░▓░▓░▓░▓░▓░▓░▓░▓░▓░▓░▓░▓░▓░▓░▓░▓░▓░▓░▓             ║
    ║        ░  DEADLOCK — HUMAN JUDGMENT REQUIRED    ▓           ║
    ║        ▓░▓░▓░▓░▓░▓░▓░▓░▓░▓░▓░▓░▓░▓░▓░▓░▓░▓░▓░             ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
```

### 0-3: Unanimous Rejection

```
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║                   M A G I   S Y S T E M                      ║
    ║                                                              ║
    ║           ┌─────────┐  ┌─────────┐  ┌─────────┐             ║
    ║           │  LOGOS  │  │ PATHOS  │  │ SOPHIA  │             ║
    ║           │  ░░░░░░ │  │  ░░░░░░ │  │  ░░░░░░ │             ║
    ║           │ REJECT  │  │ REJECT  │  │ REJECT  │             ║
    ║           └─────────┘  └─────────┘  └─────────┘             ║
    ║                                                              ║
    ║        ████████████████████████████████████████████           ║
    ║        █  PROPOSAL DENIED — ALL SYSTEMS REJECT   █           ║
    ║        ████████████████████████████████████████████           ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
```

### Dynamic Elements

The verdict display should be customized per decision:
- Replace `APPROVE`/`REJECT` with each perspective's actual vote
- Replace the status bar text with a one-line summary of the decision
- Use `██████` (solid) for APPROVE, `░░░░░░` (light) for REJECT, `▒▒▒▒▒▒` (medium) for ABSTAIN, `▓▓▓▓▓▓` (dark) for CONDITIONAL

---

## Compact Report Template (AUTORUN Mode)

```markdown
## MAGI Verdict: [Subject]

| Perspective | Vote | Conf | Rationale |
|-------------|------|------|-----------|
| Logos | [A/R/AB] | [N] | [One line] |
| Pathos | [A/R/AB] | [N] | [One line] |
| Sophia | [A/R/AB] | [N] | [One line] |

**Consensus**: [Pattern] | **Confidence**: [Score] | **Decision**: [One sentence]

[VERDICT_DISPLAY ASCII art]

**Risks**: [Key risk] → [Mitigation]
**Next**: [Recommended action/agent]
```

---

## Sample Deliberations

### Sample 1: Architecture — Monolith vs Microservices

**Context:** 5-person team building an e-commerce platform. Current traffic: 1K DAU. Expected growth: 10K DAU in 12 months.

**Logos (Confidence: 78):** APPROVE monolith. Current scale doesn't justify distributed system complexity. Network latency, data consistency, and deployment overhead of microservices outweigh benefits. Monolith can handle 10K DAU easily. Extract services when specific bottlenecks are identified.

**Pathos (Confidence: 85):** APPROVE monolith. Team of 5 cannot effectively maintain service boundaries, separate deployments, and distributed debugging. Microservices would create cognitive overload and on-call burden. Monolith allows the team to focus on product value.

**Sophia (Confidence: 72):** APPROVE monolith. Time-to-market is 3 months faster. Microservices add operational cost (infrastructure, monitoring) without current business justification. Revisit at 50K DAU or when team grows to 15+.

**Verdict:** 3-0 UNANIMOUS APPROVAL — Monolith with future extraction plan

---

### Sample 2: Trade-off — Performance vs Readability

**Context:** API endpoint response time can be reduced from 200ms to 160ms with optimized code, but the optimized version uses bitwise operations and custom memory pooling.

**Logos (Confidence: 82):** REJECT optimization. 40ms improvement is within SLA. Optimized code has higher defect probability. Premature optimization. Benchmark when latency actually becomes a problem.

**Pathos (Confidence: 88):** REJECT optimization. Optimized code requires deep systems knowledge to maintain. Team has 2 junior developers. Bug rate will increase. Readable version enables faster feature development.

**Sophia (Confidence: 75):** REJECT optimization. 40ms doesn't impact conversion rates or user satisfaction metrics. Developer time is better spent on features. Optimize only when P99 latency exceeds SLA.

**Verdict:** 0-3 UNANIMOUS REJECTION — Keep readable implementation

---

### Sample 3: Go/No-Go — v2.0 Release

**Context:** Major version release with new payment system. 94% test pass rate, 2 medium bugs, no criticals. Migration guide 60% complete.

**Logos (Confidence: 80):** APPROVE (GO). Test coverage adequate, no critical issues. 2 medium bugs are edge cases with known workarounds. Payment system passed integration tests.

**Pathos (Confidence: 73):** CONDITIONAL (HOLD 2 days). Migration guide is incomplete — users will struggle. Support team hasn't been briefed on new payment flows. Launching without documentation creates frustration.

**Sophia (Confidence: 70):** APPROVE (GO WITH CONDITIONS). Competitor launches next week. 2-day delay acceptable, 1-week delay is not. Ship with conditions: complete migration guide and support briefing within 48 hours.

**Verdict:** 2-1 MAJORITY — GO WITH CONDITIONS (Pathos dissent recorded)

---

### Sample 4: Strategy — Build vs Buy (Auth System)

**Context:** Need authentication for SaaS product. Team has no security specialist. Budget: $500/month for SaaS tools.

**Logos (Confidence: 85):** APPROVE buy. Authentication is a solved problem with high security stakes. Building introduces CVE risk. Auth0/Clerk provide battle-tested implementations with compliance certifications.

**Pathos (Confidence: 80):** APPROVE buy. Team lacks security expertise — building auth creates anxiety and maintenance burden. Third-party auth lets the team focus on core product value. Better developer experience.

**Sophia (Confidence: 77):** APPROVE buy. Build cost: 3 developer-months (~$45K). Auth0 cost: $300/month ($3.6K/year). Break-even at 12+ years. Faster to market by 2 months. Clear ROI.

**Verdict:** 3-0 UNANIMOUS APPROVAL — Buy authentication service

---

### Sample 5: Priority — Security vs Feature vs Tech Debt

**Context:** Sprint planning with 3 competing items. Team capacity: 2 developers, 2 weeks.

**Security vulnerability (CVE-2024-XXXX):** Logos: 10, Pathos: 8, Sophia: 9
**Customer-requested feature:** Logos: 4, Pathos: 7, Sophia: 8
**Database migration (perf improvement):** Logos: 7, Pathos: 3, Sophia: 5

**Verdict:** UNANIMOUS — Priority: Security → Feature → Database migration

---

## Risk Register Template

```markdown
## Risk Register — [Decision ID]

| # | Risk | Source | Likelihood | Impact | Severity | Mitigation | Owner | Monitor | Status |
|---|------|--------|-----------|--------|----------|------------|-------|---------|--------|
| 1 | [Risk description] | [Logos/Pathos/Sophia] | [H/M/L] | [H/M/L] | [Critical/High/Med/Low] | [Action] | [Who] | [Metric] | [Open/Mitigated/Accepted] |

### Monitoring Schedule
- **Weekly**: [What to check weekly]
- **Monthly**: [What to check monthly]
- **Trigger-based**: [What triggers immediate review]
```

---

## Decision Log Template

For maintaining a record of all Magi decisions:

```markdown
## Decision Log

| ID | Date | Domain | Subject | Consensus | Confidence | Decision | Status |
|----|------|--------|---------|-----------|------------|----------|--------|
| MAGI-001 | YYYY-MM-DD | [Type] | [Subject] | [3-0/2-1/etc] | [Score] | [Brief] | [Active/Superseded/Revoked] |
```

---

## Engine Mode Full Deliberation Report Template

```markdown
# MAGI Engine Mode Deliberation Report

## Decision Request
- **Type**: [Architecture / Trade-off / Go-No-Go / Strategy / Priority]
- **Subject**: [Decision subject]
- **Requestor**: [User / Agent name]
- **Deliberation Mode**: Engine Mode
- **Urgency**: [Low / Medium / High / Critical]
- **Reversibility**: [Low / Medium / High]

---

## Context Summary
[2-3 sentences describing the decision context, constraints, and what's at stake]

...
```

---

## Engine Mode Verdict Presentation

### 3-0: All Engines Agree

```
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║              M A G I   E N G I N E   M O D E                 ║
    ║                                                              ║
    ║           ┌─────────┐  ┌─────────┐  ┌─────────┐             ║
    ║           │ CLAUDE  │  │  CODEX  │  │ GEMINI  │             ║
    ║           │  ██████ │  │  ██████ │  │  ██████ │             ║
    ║           │ APPROVE │  │ APPROVE │  │ APPROVE │             ║
    ║           └─────────┘  └─────────┘  └─────────┘             ║
    ║                                                              ║
    ║        ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░             ║
    ║        ░  ALL ENGINES AGREE — UNANIMOUS APPROVAL ░           ║
    ║        ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░             ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
```

### 2-1: Engine Majority

```
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║              M A G I   E N G I N E   M O D E                 ║
    ║                                                              ║
    ║           ┌─────────┐  ┌─────────┐  ┌─────────┐             ║
    ║           │ CLAUDE  │  │  CODEX  │  │ GEMINI  │             ║
    ║           │  ██████ │  │  ██████ │  │  ░░░░░░ │             ║
    ║           │ APPROVE │  │ APPROVE │  │ REJECT  │             ║
    ║           └─────────┘  └─────────┘  └─────────┘             ║
    ║                                                              ║
    ║        ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓             ║
    ║        ▓ ENGINE MAJORITY — 2:1 — DISSENT LOGGED ▓           ║
    ║        ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓             ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
```

### 1-1-1: Engine Deadlock

```
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║              M A G I   E N G I N E   M O D E                 ║
    ║                                                              ║
    ║           ┌─────────┐  ┌─────────┐  ┌─────────┐             ║
    ║           │ CLAUDE  │  │  CODEX  │  │ GEMINI  │             ║
    ║           │  ██████ │  │  ░░░░░░ │  │  ▒▒▒▒▒▒ │             ║
    ║           │ APPROVE │  │ REJECT  │  │ ABSTAIN │             ║
    ║           └─────────┘  └─────────┘  └─────────┘             ║
    ║                                                              ║
    ║        ░▓░▓░▓░▓░▓░▓░▓░▓░▓░▓░▓░▓░▓░▓░▓░▓░▓░▓░▓             ║
    ║        ░ ENGINE DEADLOCK — HUMAN JUDGMENT REQUIRED▓          ║
    ║        ▓░▓░▓░▓░▓░▓░▓░▓░▓░▓░▓░▓░▓░▓░▓░▓░▓░▓░▓░             ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
```

### 0-3: All Engines Reject

```
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║              M A G I   E N G I N E   M O D E                 ║
    ║                                                              ║
    ║           ┌─────────┐  ┌─────────┐  ┌─────────┐             ║
    ║           │ CLAUDE  │  │  CODEX  │  │ GEMINI  │             ║
    ║           │  ░░░░░░ │  │  ░░░░░░ │  │  ░░░░░░ │             ║
    ║           │ REJECT  │  │ REJECT  │  │ REJECT  │             ║
    ║           └─────────┘  └─────────┘  └─────────┘             ║
    ║                                                              ║
    ║        ████████████████████████████████████████████           ║
    ║        █ ALL ENGINES REJECT — PROPOSAL DENIED    █           ║
    ║        ████████████████████████████████████████████           ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
```

---

## Engine Mode Compact Report Template (AUTORUN Mode)

```markdown
## MAGI Engine Mode Verdict: [Subject]

| Engine | Vote | Conf | Rationale |
|--------|------|------|-----------|
| Claude | [A/R/AB] | [N] | [One line] |
| Codex | [A/R/AB] | [N] | [One line] |
| Gemini | [A/R/AB] | [N] | [One line] |

**Consensus**: [Pattern] | **Confidence**: [Score] | **Decision**: [One sentence]

[ENGINE_MODE_VERDICT_DISPLAY ASCII art]

**Risks**: [Key risk] → [Mitigation]
**Next**: [Recommended action/agent]
```

---

## Engine Mode Sample Deliberation

### Sample: Architecture Decision — REST vs GraphQL

**Context:** SaaS platform API redesign. 50+ frontend consumers, mobile and web. Current REST API has over-fetching issues. Team of 8, 2 have GraphQL experience.

**Claude (Confidence: 75):** APPROVE GraphQL. Over-fetching is a real performance issue for mobile clients. Schema-first development improves frontend-backend contracts. However, team experience gap is a risk — recommend incremental adoption starting with a single high-traffic endpoint.

**Codex (Confidence: 72):** APPROVE GraphQL. Type safety and introspection reduce integration bugs. Dataloader pattern solves N+1. Tooling ecosystem (Apollo, Relay) is mature. Risk: complexity of authorization in resolvers requires careful design.

**Gemini (Confidence: 68):** REJECT GraphQL. Migration cost for 50+ consumers is significant. REST with OpenAPI spec + response field filtering achieves 80% of the benefit at 20% of the cost. GraphQL adds operational complexity (caching, monitoring, rate limiting). Recommend REST optimization first.

**Verdict:** 2-1 ENGINE MAJORITY — APPROVE GraphQL with incremental adoption (Gemini dissent recorded)

```
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║              M A G I   E N G I N E   M O D E                 ║
    ║                                                              ║
    ║           ┌─────────┐  ┌─────────┐  ┌─────────┐             ║
    ║           │ CLAUDE  │  │  CODEX  │  │ GEMINI  │             ║
    ║           │  ██████ │  │  ██████ │  │  ░░░░░░ │             ║
    ║           │ APPROVE │  │ APPROVE │  │ REJECT  │             ║
    ║           └─────────┘  └─────────┘  └─────────┘             ║
    ║                                                              ║
    ║        ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓             ║
    ║        ▓ ENGINE MAJORITY — 2:1 — DISSENT LOGGED ▓           ║
    ║        ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓             ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
```
