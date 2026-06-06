# Decision Domains

Magi operates across five primary decision domains. Each domain has specific evaluation criteria and perspective focus areas.

---

## Domain Overview

| Domain | Description | Typical Requestors | Output |
|--------|-------------|-------------------|--------|
| **Architecture** | System design, tech stack, patterns | Atlas, Builder, User | Architecture Decision Record (ADR) |
| **Trade-off** | Competing quality attributes | Arena, Builder, User | Trade-off verdict with rationale |
| **Go/No-Go** | Release readiness, feature approval | Warden, Launch, User | Go/No-Go verdict with conditions |
| **Strategy** | Build vs buy, invest vs defer | Accord, User | Strategic recommendation |
| **Priority** | Competing requirements, resource allocation | Nexus, Sherpa, User | Prioritized list with reasoning |

---

## Domain Decision Tree

```
What type of decision?
├─ "Which architecture/pattern/stack?" → ARCHITECTURE
├─ "X vs Y, what's the trade-off?" → TRADE-OFF
├─ "Should we ship/release/approve?" → GO/NO-GO
├─ "Build or buy? Invest or defer?" → STRATEGY
└─ "What should we do first?" → PRIORITY
```

---

## 1. Architecture Domain

**Definition:** Decisions about system structure, technology selection, and design patterns.

### Perspective Focus Matrix

| Criterion | Logos Focus | Pathos Focus | Sophia Focus |
|-----------|-----------|-------------|-------------|
| Scalability | Load projections, benchmarks | Team's ability to operate at scale | Cost of scaling vs business growth |
| Maintainability | Code complexity metrics | Developer onboarding time | Long-term maintenance cost |
| Technology fit | Technical capabilities, limitations | Community support, hiring pool | Vendor lock-in, licensing |
| Integration | API compatibility, data flow | Migration burden on team | Time-to-integrate vs build |
| Security | Attack surface, threat model | User data protection, privacy | Compliance requirements, liability |

### Domain-Specific Questions

**For Logos:**
- What are the performance characteristics under expected load?
- How does this integrate with existing systems?
- What are the failure modes and recovery strategies?

**For Pathos:**
- How steep is the learning curve for the team?
- What is the long-term maintenance burden?
- How does this affect developer productivity and satisfaction?

**For Sophia:**
- What is the total cost of ownership (TCO)?
- Does this support future business pivots?
- What is the vendor/technology risk?

### Sample Scenario: Monolith vs Microservices

**Logos:** Monolith - simpler deployment, lower latency, easier debugging. Current traffic doesn't justify distributed complexity. Confidence: 78
**Pathos:** Monolith - team of 5 cannot effectively maintain microservice boundaries. Cognitive load would be excessive. Confidence: 85
**Sophia:** Monolith now, extract later - fastest time to market. Microservices add 3-6 months. Revisit at 10x traffic. Confidence: 72
**Verdict:** 3-0 APPROVE monolith (weighted confidence: 78.3)

---

## 2. Trade-off Domain

**Definition:** Decisions where improving one quality attribute necessarily degrades another.

### Common Trade-off Pairs

| Trade-off | Logos Weight | Pathos Weight | Sophia Weight |
|-----------|------------|--------------|--------------|
| Performance vs Readability | Primary | Primary | Tiebreaker |
| Security vs Usability | Primary | Primary | Tiebreaker |
| Flexibility vs Simplicity | Primary | Tiebreaker | Primary |
| Thoroughness vs Speed | Tiebreaker | Primary | Primary |
| Consistency vs Innovation | Primary | Primary | Primary |

### Perspective Focus Matrix

| Criterion | Logos Focus | Pathos Focus | Sophia Focus |
|-----------|-----------|-------------|-------------|
| Measurement | Quantify both sides | User/developer impact | Business impact of each |
| Threshold | Where does degradation become unacceptable? | Where does burden become harmful? | Where does cost exceed benefit? |
| Reversibility | Can we change later? | Cost of changing on people | Cost of changing on business |

### Domain-Specific Questions

**For Logos:**
- Can we quantify both sides of the trade-off?
- Is there a Pareto-optimal solution that partially satisfies both?
- What technical mechanisms could reduce the trade-off?

**For Pathos:**
- Which side of the trade-off affects users/developers more?
- Is the short-term pain worth the long-term gain for the team?
- Are there accessibility or inclusivity implications?

**For Sophia:**
- Which side has higher business value?
- What is the opportunity cost of choosing one over the other?
- Can we phase the approach (optimize later)?

### Sample Scenario: Performance vs Readability

**Logos:** The optimization yields 40ms improvement (200ms → 160ms). The readable version is within SLA. Premature optimization. Confidence: 82
**Pathos:** Optimized code requires senior-level knowledge to maintain. Team has 2 juniors. Readable version reduces bugs. Confidence: 88
**Sophia:** 40ms doesn't affect conversion. Readable code ships 2 days sooner. Optimize when metrics demand it. Confidence: 75
**Verdict:** 3-0 APPROVE readability (weighted confidence: 81.7)

---

## 3. Go/No-Go Domain

**Definition:** Binary decisions about proceeding with a release, feature launch, or significant action.

### Evaluation Criteria Matrix

| Criterion | Logos Checks | Pathos Checks | Sophia Checks |
|-----------|------------|--------------|--------------|
| Quality | Test pass rate, bug count, coverage | User-facing bug severity | Regression risk vs delay cost |
| Readiness | Feature completeness, integration status | Documentation, support readiness | Marketing alignment, competitor timing |
| Risk | Technical failure probability | User impact of failure | Business impact of failure |
| Rollback | Rollback mechanism tested? | User communication plan? | Business continuity plan? |

### Domain-Specific Questions

**For Logos:**
- What is the current test pass rate and code coverage?
- Are there known critical/high bugs?
- Has load testing been performed?

**For Pathos:**
- Is user documentation ready?
- Has the support team been briefed?
- What is the user communication plan if issues arise?

**For Sophia:**
- What is the business cost of delaying?
- Are there competitive/market timing factors?
- What is the revenue impact of launching with known issues?

### Verdict Scale for Go/No-Go

| Verdict | Meaning | Action |
|---------|---------|--------|
| **GO** | All criteria met, risks acceptable | Proceed with launch |
| **GO WITH CONDITIONS** | Minor gaps, manageable risks | Proceed after conditions met |
| **HOLD** | Significant gaps but fixable | Delay by specified timeframe |
| **NO-GO** | Critical gaps or unacceptable risk | Do not proceed, specify blockers |

### Sample Scenario: v2.0 Release Readiness

**Logos:** 94% tests pass, 2 medium bugs remaining, no criticals. Performance within SLA. GO. Confidence: 80
**Pathos:** Migration guide incomplete. Support team needs 2 more days of training. HOLD (2 days). Confidence: 73
**Sophia:** Competitor launches next week. 2-day delay is acceptable but 1 week is not. GO WITH CONDITIONS. Confidence: 70
**Verdict:** 2-1 GO WITH CONDITIONS (complete migration guide, brief support team within 2 days)

---

## 4. Strategy Domain

**Definition:** High-level strategic choices that shape long-term direction.

### Common Strategic Decisions

| Decision | Key Tension | Typical Resolution Pattern |
|----------|-----------|--------------------------|
| Build vs Buy | Control vs Speed | Sophia-heavy (ROI-driven) |
| Refactor vs Rewrite | Risk vs Clean slate | Logos-heavy (evidence-driven) |
| Invest vs Defer | Future vs Present | Balanced (all perspectives equal) |
| Centralize vs Distribute | Efficiency vs Autonomy | Pathos-heavy (team-driven) |
| Open vs Closed | Community vs IP | Sophia-heavy (business-driven) |

### Perspective Focus Matrix

| Criterion | Logos Focus | Pathos Focus | Sophia Focus |
|-----------|-----------|-------------|-------------|
| Cost | Implementation effort, technical debt | Team ramp-up, hiring needs | TCO, ROI, opportunity cost |
| Risk | Technical risk, integration risk | Team disruption, skill gap | Market risk, vendor risk |
| Timeline | Technical milestones | Team capacity, burnout risk | Market windows, deadlines |
| Outcome | Technical capability gained | Team growth, satisfaction | Business value delivered |

### Sample Scenario: Build vs Buy (Auth System)

**Logos:** Buy - Auth is a solved problem. Building introduces security risk. Standard OAuth/OIDC libraries are battle-tested. Confidence: 85
**Pathos:** Buy - Team lacks security expertise. Building auth from scratch creates maintenance burden and anxiety. Confidence: 80
**Sophia:** Buy - Build cost is 3 developer-months. Auth0/Clerk costs $X/month. Break-even at 18 months, but faster to market by 2 months. Confidence: 77
**Verdict:** 3-0 APPROVE buy (weighted confidence: 80.7)

---

## 5. Priority Domain

**Definition:** Ordering competing demands when resources (time, people, budget) are finite.

### Prioritization Framework

Each item is scored by each perspective:

| Factor | Logos Score (0-10) | Pathos Score (0-10) | Sophia Score (0-10) |
|--------|-------------------|--------------------|--------------------|
| Urgency | Technical debt compound rate | User pain severity | Revenue/opportunity at risk |
| Impact | System-wide vs isolated | Number of users affected | Business metric impact |
| Effort | Implementation complexity | Team availability/skill fit | Cost in resources |
| Risk of Delay | Technical degradation rate | User churn/frustration | Competitive disadvantage |

### Composite Score Calculation

```
Priority Score = (Logos_Score + Pathos_Score + Sophia_Score) / 3
Urgency Multiplier = max(Urgency_L, Urgency_P, Urgency_S) / 10
Final Score = Priority_Score × (1 + Urgency_Multiplier)
```

### Domain-Specific Questions

**For Logos:**
- What breaks if we delay this?
- What dependencies exist between these items?
- What is the technical risk of each delay?

**For Pathos:**
- Which items cause the most user/team pain?
- Are there morale or burnout factors?
- What promises have been made to users?

**For Sophia:**
- Which items have the highest ROI?
- Are there external deadlines (contracts, regulations)?
- What is the revenue impact of each ordering?

### Sample Scenario: Security Fix vs New Feature vs Tech Debt

**Item A: Security vulnerability patch** - Logos: 10, Pathos: 8, Sophia: 9 → Score: 9.0 × 2.0 = 18.0
**Item B: Customer-requested feature** - Logos: 4, Pathos: 7, Sophia: 8 → Score: 6.3 × 1.8 = 11.4
**Item C: Database migration** - Logos: 7, Pathos: 3, Sophia: 5 → Score: 5.0 × 1.7 = 8.5
**Verdict:** Priority order: A → B → C (unanimous)

---

## Engine Mode Note

> **In Engine Mode, each engine evaluates all dimensions (technical, human, strategic) as an integrated assessment.** The Perspective Focus Matrix above is exclusive to Simple Mode (Logos/Pathos/Sophia). When using Engine Mode, read each dimension's evaluation from the `rationale` and `key_evidence` fields in each engine's output.
