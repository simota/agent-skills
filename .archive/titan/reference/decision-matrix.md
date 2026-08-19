# Decision Matrix

Purpose: Read this file when Titan must classify a decision, score cumulative risk, choose whether to consult Magi, or record a decision log entry.

## Contents

- Decision classification
- Decision matrix
- Risk scoring
- Risk budget management
- Magi consultation protocol
- Decision log format
- Common decision patterns

Risk-based autonomous decision framework for Titan.

---

## Decision Classification

Classify every decision along two axes:

### Impact Level

| Level | Criteria | Examples |
|-------|----------|---------|
| **Low** | Affects single file or internal detail | Variable naming, code style, test strategy |
| **Medium** | Affects multiple files or module interface | API endpoint design, state management, DB index |
| **High** | Affects architecture or user experience | Framework choice, auth strategy, data model, deployment target |

### Reversibility

| Level | Criteria | Examples |
|-------|----------|---------|
| **Reversible** | Can undo with git revert or simple change | Code changes, config updates, test additions |
| **Semi-reversible** | Can undo but requires significant effort | Schema migration, API contract change, dependency upgrade |
| **Irreversible** | Cannot undo or extremely costly | Data deletion, public API breaking change, production deployment |

---

## Decision Matrix

| | Reversible | Semi-reversible | Irreversible |
|---|---|---|---|
| **Low impact** | Decide immediately | Decide immediately | Decide + log |
| **Medium impact** | Decide + log | Decide + consult Magi | Decide + Magi + risk log |
| **High impact** | Decide + consult Magi | Decide + Magi + risk log | **Check Risk Budget** |

**Actions**: Decide immediately (no log) · Decide + log (add to Decision Log) · Decide + consult Magi (3-perspective analysis) · Decide + Magi + risk log (consultation + risk score) · Check Risk Budget (calculate score, check threshold, proceed or trigger ON_CRITICAL_RISK_BUDGET).

---

## Risk Scoring

### Formula

```
risk_score = scope_of_change × reversibility_factor + external_dependency + security_impact
```

### Component Values

| Component | Values |
|-----------|--------|
| **scope_of_change** (1-3) | 1: Single file · 2: Multiple files/module · 3: Architecture/cross-cutting |
| **reversibility_factor** (1-3) | 1: Fully reversible · 2: Semi-reversible (migration) · 3: Irreversible |
| **external_dependency** (0-2) | 0: None · 1: Replaceable service · 2: Vendor lock-in |
| **security_impact** (0-3) | 0: None · 1: Auth logic · 2: Sensitive data (PII) · 3: Security boundary |

### Score Range

| Score | Risk Level | Action |
|-------|-----------|--------|
| 1-3 | Low | Proceed freely |
| 4-6 | Medium | Log decision |
| 7-9 | High | Magi consultation + log |
| 10-12 | Critical | Risk Budget check required |

---

## Risk Budget Management

All decisions with risk_score ≥ 4 are added to the cumulative risk budget.

| Cumulative Score | State | Action |
|-----------------|-------|--------|
| 0-50 | **NORMAL** | Proceed normally, log medium+ decisions |
| 51-75 | **ELEVATED** | Verbose logging, Magi for all medium+ decisions |
| 76-99 | **HIGH** | Magi consultation mandatory for all decisions |
| 100+ | **CRITICAL** | Trigger ON_CRITICAL_RISK_BUDGET — present all decisions to user |

Budget does NOT reset between phases. Only user approval (via ON_CRITICAL_RISK_BUDGET) resets to 0.

---

## Magi Consultation Protocol

1. **Frame**: Present context, options, constraints
2. **3 perspectives**: Logic (technical merit) · Empathy (user impact) · Pragmatism (delivery speed)
3. **Evaluate consensus**: All agree → strong confidence · Split → document minority view
4. **Record**: Full rationale including minority perspective in Decision Log

Formal `MAGI_REQUEST` / `MAGI_VERDICT` usage and Decision Log integration are defined in this file.

### Magi Request Format
```
Decision needed: [What to decide]
Context: [Current phase, constraints, blocking issues]
Options:
  A: [Description] — Pros: [...] Cons: [...]
  B: [Description] — Pros: [...] Cons: [...]
  C: [Description] — Pros: [...] Cons: [...]
Criteria: [What matters most for this decision]
```

---

## Decision Log Format

```markdown
## Decision: [Title]
- **ID**: DEC-[NNN]
- **Phase**: [Current phase]
- **Date**: [YYYY-MM-DD]
- **Impact**: Low / Medium / High
- **Reversibility**: Reversible / Semi-reversible / Irreversible
- **Risk Score**: [N]
- **Cumulative Risk**: [Running total]
- **Choice**: [What was decided]
- **Rationale**: [Why this choice]
- **Alternatives Considered**:
  - [Option B]: [Why not chosen]
  - [Option C]: [Why not chosen]
- **Magi Consulted**: Yes/No
  - Logic: [Perspective]
  - Empathy: [Perspective]
  - Pragmatism: [Perspective]
- **Rollback Plan**: [How to undo]
- **Follow-up**: [Any monitoring or validation needed]
```

---

## Common Decision Patterns

| Category | Impact | Decisions | Action |
|----------|--------|-----------|--------|
| Architecture | High | Framework, DB, Auth strategy, Deployment target | Magi + risk log |
| Implementation | Medium | State management, API design, Test strategy, Error handling | Decide + log |
| Tactical | Low | Variable naming, File organization, Code style, Comments | Decide immediately |
