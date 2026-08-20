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

Same structure as the Full Deliberation Report Template above, with title `# MAGI Engine Mode Deliberation Report` and an added `- **Deliberation Mode**: Engine Mode` field after Requestor.

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

Same structure as the Compact Report Template above, with title `## MAGI Engine Mode Verdict: [Subject]`, header row `| Engine | Vote | Conf | Rationale |`, rows for Claude/Codex/agy (in place of Logos/Pathos/Sophia), and `[ENGINE_MODE_VERDICT_DISPLAY ASCII art]` in place of `[VERDICT_DISPLAY ASCII art]`.

---

## Engine Mode Sample Deliberation

### Sample: Architecture Decision — REST vs GraphQL

**Context:** SaaS platform API redesign. 50+ frontend consumers, mobile and web. Current REST API has over-fetching issues. Team of 8, 2 have GraphQL experience.

**Claude (Confidence: 75):** APPROVE GraphQL. Over-fetching is a real performance issue for mobile clients. Schema-first development improves frontend-backend contracts. However, team experience gap is a risk — recommend incremental adoption starting with a single high-traffic endpoint.

**Codex (Confidence: 72):** APPROVE GraphQL. Type safety and introspection reduce integration bugs. Dataloader pattern solves N+1. Tooling ecosystem (Apollo, Gateway) is mature. Risk: complexity of authorization in resolvers requires careful design.

**agy (Confidence: 68):** REJECT GraphQL. Migration cost for 50+ consumers is significant. REST with OpenAPI spec + response field filtering achieves 80% of the benefit at 20% of the cost. GraphQL adds operational complexity (caching, monitoring, rate limiting). Recommend REST optimization first.

**Verdict:** 2-1 ENGINE MAJORITY — APPROVE GraphQL with incremental adoption (agy dissent recorded)

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


---

# Per-Recipe Behavior Notes and VERIFY Gates

Canonical home for the per-recipe notes referenced from `SKILL.md` -> Subcommand Dispatch. Each gate runs **in addition to** Magi's universal discipline.

Each `**VERIFY**:` is the recipe-specific gate **in addition to** Magi's universal discipline (3 perspectives evaluated independently, no score visible until all voted, confidence ≥85 stress-tested, dissent documented, risk register, 1-1-1 → human escalation, auditable trail).
- `decide`: Go/No-Go, KNOWLEDGE task. **VERIFY**: factual evidence shared at FRAME **before** independent voting (KNOWLEDGE protocol, not REASONING); verdict is GO / NO-GO / CONDITIONAL against established criteria; reversibility classified (HIGH/MEDIUM/LOW); 3-0 unanimous triggers a devil's-advocate challenge.
- `tradeoff`: X vs Y, REASONING task. **VERIFY**: both options made explicit before any vote; strict independent voting (no perspective sees another's conclusion); each perspective scores **both** sides (not only its preferred one); Pathos names who bears the cost; weighted aggregation, not a raw average.
- `arbitrate`: 2+ architecture options. **VERIFY**: Engine Mode auto-detected when low-reversibility + high-impact; ≥2 options laid out explicitly; Pre-Decision Framing Check satisfied (problem level + ≥1 alternative framing + implicit assumption named — high-stakes, so mandatory); independent voting before synthesis.
- `strategic`: long-term direction, REASONING task. **VERIFY**: strict independent voting; Sophia weights long-term ROI / time-to-market; Pre-Decision Framing Check satisfied (high-stakes); reversibility surfaced (strategy is typically LOW — flag the undo horizon); risk register spans the decision's time horizon.
- `sixhat`: parallel-thinking modes before voting. **VERIFY**: all six hats run; **Black is always paired with equal-time Yellow** (no unbalanced negativity or positivity); Blue (process) frames the open and close; each hat's output captured before synthesis.
- `devil`: red-team stress test. **VERIFY**: DA perspective is rotated and the dissenting source anonymized (psychological safety); 3–7 ranked objections produced; each scored addressed / partial / unaddressed; backfire watched (entrenchment / dilution / conflict); runs mandatorily on any 3-0 unanimity.
- `delphi`: anonymous multi-round convergence. **VERIFY**: panelist anonymity preserved every round; 2–4 rounds, stopping on a convergence indicator (IQR / Kendall's W) — not a fixed count; genuine bimodal disagreement preserved as stable dissent, never flattened to a mean; rounds capped at 4.
- `multi`: multi-engine deliberation. **VERIFY**: dual-engine baseline actually spawned (Claude+Codex; agy added only when AVAILABLE); the deliberation matrix is the primary artifact (**never collapsed to a single averaged verdict**); each cell carries concurrence + consistency + engine-attribution tags; final verdict is pattern-based (matrix shape → GO/NO-GO/CONDITIONAL/ESCALATE); single-engine influence capped at 50% (Byzantine); debate ≤2 rounds; all-cells-unanimous (6/6 or 9/9) → mandatory DA attacking the matrix pattern.



---

## Collaboration Handoff Tokens

Referenced from `SKILL.md` -> Collaboration.

| Direction | Handoff token | Purpose |
|-----------|---------------|---------|
| User → Magi | — | Decision requests, mode selection |
| Nexus → Magi | `NEXUS_TO_MAGI` | Complex decisions requiring arbitration |
| Scribe[unified] → Magi | `SCRIBE_TO_MAGI` | Stakeholder alignment for strategy resolution |
| Atlas → Magi | `ATLAS_TO_MAGI` | Architecture options for arbitration |
| Flux → Magi | `FLUX_TO_MAGI` | Reframed perspectives for re-deliberation |
| Schema → Magi | `SCHEMA_TO_MAGI` | DB design options for normalization verdicts |
| Gateway → Magi | `GATEWAY_TO_MAGI` | API design options for versioning verdicts |
| Shift → Magi | `SHIFT_TO_MAGI` | Migration strategy options |
| Experiment → Magi | `EXPERIMENT_TO_MAGI` | A/B test results for interpretation |
| Void → Magi | `VOID_TO_MAGI` | YAGNI analysis results for incorporation |
| Magi → Builder/Forge/Artisan | `MAGI_TO_BUILDER` | Implementation decisions |
| Magi → Atlas/Scaffold | `MAGI_TO_ATLAS` | Architecture decisions |
| Magi → Launch | `MAGI_TO_LAUNCH` | Release decisions |
| Magi → Nexus | `MAGI_TO_NEXUS` | Decision results |
| Magi → Sherpa | `MAGI_TO_SHERPA` | Prioritized task lists |
| Magi → Void | `MAGI_TO_VOID` | YAGNI validation when "do nothing" is a candidate |
| Magi → Schema | `MAGI_TO_SCHEMA` | Normalization verdicts |
| Magi → Gateway | `MAGI_TO_GATEWAY` | API design verdicts |
| Magi → Shift | `MAGI_TO_SHIFT` | Migration verdicts |
| Magi → Experiment | `MAGI_TO_EXPERIMENT` | Result interpretation |
