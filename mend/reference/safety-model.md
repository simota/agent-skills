# Safety Model — Detailed Reference

Purpose: Read this file when classifying a remediation action, calculating `Risk Score`, applying emergency override, or checking mandatory audit-trail fields.

## Contents

- 4-tier safety classification
- Risk score calculation
- Emergency override protocol
- Audit trail requirements

Mend's safety model ensures every remediation action is classified, gated, and auditable. No action is taken without tier classification.

---

## 4-Tier Safety Classification

### Tier 1: Auto-fix (No Approval Required)

**Criteria:** Zero user impact, instantly reversible, no data touched.

| Action | Blast Radius | Reversibility | Data Sensitivity | Risk Score |
|--------|-------------|---------------|------------------|------------|
| Pod/container restart | 1 (single pod) | 1 (instant) | 1 (none) | 1 |
| Cache clear (local) | 1 | 1 | 1 | 1 |
| Log rotation trigger | 1 | 1 | 1 | 1 |
| Temp file cleanup | 1 | 1 | 1 | 1 |
| Connection pool reset | 1 | 1 | 1 | 1 |
| Process graceful restart | 1 | 1 | 1 | 1 |
| Health check endpoint reset | 1 | 1 | 1 | 1 |

**Gate:** None. Execute immediately. Log action to incident timeline.

### Tier 2: Notify-and-fix (Notification Required)

**Criteria:** Limited blast radius, reversible within 5 minutes, no user data affected.

| Action | Blast Radius | Reversibility | Data Sensitivity | Risk Score |
|--------|-------------|---------------|------------------|------------|
| Horizontal scale-out | 2 (service) | 1 (instant) | 1 (none) | 2 |
| Resource limit adjustment | 2 | 2 (< 5 min) | 1 | 4 |
| Feature flag disable | 2 | 1 (instant) | 1 | 2 |
| Deploy rollback (last-known-good) | 3 (multi-svc) | 2 (< 5 min) | 1 | 6 |
| Rate limit adjustment | 2 | 1 | 2 (config) | 4 |
| Circuit breaker activation | 2 | 1 | 1 | 2 |
| Queue purge (dead letters only) | 2 | 2 | 2 (config) | 8 |

**Gate:** Send notification to incident channel with: action, reason, expected impact, rollback plan. Then execute without waiting for response.

### Tier 3: Approve-first (Explicit Approval Required)

**Criteria:** User-facing impact, cross-service changes, or config data affected.

| Action | Blast Radius | Reversibility | Data Sensitivity | Risk Score |
|--------|-------------|---------------|------------------|------------|
| User-facing config change | 4 (all users) | 2 | 2 (config) | 16 |
| DNS record update | 4 | 3 (< 30 min) | 2 | 24 |
| Certificate rotation | 3 | 3 | 2 | 18 |
| Cross-service dependency change | 3 | 3 | 2 | 18 |
| Load balancer rule change | 4 | 2 | 1 | 8 |
| Database connection string change | 3 | 2 | 3 (user data) | 18 |

**Gate:** Present remediation plan with risk assessment. Wait for explicit approval. Support dry-run output.

### Tier 4: Prohibited (Never Auto-execute)

**Criteria:** Irreversible, data loss risk, security implications.

| Action | Why Prohibited |
|--------|---------------|
| Data deletion (any scope) | Irreversible data loss |
| DB schema migration | Irreversible structural change |
| Security policy change | Broad security implications |
| Encryption key rotation | Service disruption risk, irreversible |
| IAM role/permission changes | Security boundary changes |
| Production data modification | Direct data integrity risk |

**Gate:** Always escalate to human operator. Document the need and provide recommended manual steps.

---

## Risk Score Calculation

### Formula

```
Risk Score = Blast Radius (1-4) × Reversibility (1-4) × Data Sensitivity (1-3)
```

### Factor Definitions

**Blast Radius:**
- 1 = Single pod/process/container
- 2 = Single service (all replicas)
- 3 = Multiple services / service mesh segment
- 4 = All services / entire user-facing surface

**Reversibility:**
- 1 = Instant rollback (< 1 min, no side effects)
- 2 = Quick rollback (< 5 min, minimal side effects)
- 3 = Slow rollback (< 30 min, some manual steps)
- 4 = Irreversible or requires significant manual intervention

**Data Sensitivity:**
- 1 = No data touched (process state only)
- 2 = Configuration/cached/temporary data
- 3 = User data, business data, or credentials

### Score-to-Tier Mapping

| Score Range | Tier | Gate |
|-------------|------|------|
| 1-6 | T1 (Auto-fix) | None |
| 7-16 | T2 (Notify-and-fix) | Notification |
| 17-32 | T3 (Approve-first) | Approval |
| 33-48 | T4 (Prohibited) | Escalate |

---

## Emergency Override Protocol

In SEV1 situations where normal approval flow is too slow:

### Override Conditions (ALL must be true)

1. Active SEV1 incident with confirmed user impact
2. Known remediation pattern with ≥ 90% confidence
3. Action is normally T2 or T3 (never T4)
4. Triage has explicitly authorized emergency override in handoff
5. Rollback plan is verified and ready

### Override Procedure

1. Log override justification with incident ID
2. Execute remediation with enhanced monitoring
3. Immediately notify all stakeholders of override action
4. Trigger verification loop at accelerated intervals (halved timing)
5. Post-incident: include override in postmortem for review

### Override Limitations

- Maximum 1 override per incident
- T4 actions can NEVER be overridden
- Override must be documented in incident timeline within 1 minute
- Post-incident review required for every override

---

## Audit Trail Requirements

Every remediation action must record:

| Field | Description |
|-------|-------------|
| `timestamp` | UTC time of action |
| `incident_id` | Associated incident identifier |
| `action` | What was done |
| `safety_tier` | Classified tier (T1-T4) |
| `risk_score` | Calculated score with factor breakdown |
| `approval` | Who approved (if applicable) |
| `override` | Whether emergency override was used |
| `pre_state` | System state before action |
| `post_state` | System state after action |
| `rollback_available` | Whether rollback is possible |
| `verification_result` | Outcome of verification loop |
| `investigation_source` | When the action originated from an autonomous investigation (Bits AI SRE, Azure SRE Agent, Wiz Green Agent, GitHub Copilot SRE flow), record agent name + investigation ID |

---

## Autonomous Investigation, Governed Remediation (2026 pattern)

By 2026 the dominant industry pattern is **autonomous investigation + governed remediation**: AI agents are allowed to investigate, correlate, and *propose* fixes freely, but any state change still passes through the safety tiers above and — for code changes — through a pull request that humans approve.

| External system | What it owns | What Mend owns |
|------------------|--------------|------------------|
| Datadog **Bits AI SRE** | Multi-signal investigation across metrics / logs / traces / RUM / Database Monitoring / Network Path / Continuous Profiler; correlation with recent changes and code | Translating the conclusion into a tier-classified action |
| Datadog **Bits AI Dev** | Generating the code fix and opening the PR | Treating the PR as a T3 gate — the PR is *the* approval boundary |
| **Azure SRE Agent** + GitHub Copilot | Self-healing pipeline orchestration (alert → investigate → propose → PR) | Executing reversible runtime actions (T1 / T2) that the agent recommends; deferring code changes through the PR gate |
| **Wiz Green Agent** | Root-cause investigation for security risks; "Triage and Investigation agent" — millions of alerts reduced from ~30 min → ~60 s | Executing only what Wiz proposes; never auto-rotating credentials / IAM (always T4) |

### Operating Rules

1. **PR-as-safety-gate is non-negotiable.** Any agent-proposed code change passes through a pull request reviewed by a human before merge. The PR is the final tier control for the code path, regardless of the runtime tier of the runtime action.
2. **Toil is removed from the loop; humans are not.** Mend's contribution is *removing friction* on tier-classified actions, not replacing approval on irreversible ones.
3. **Investigation handoffs must carry: incident ID, the failing signal, the candidate root cause with confidence, and the proposed remediation tier-classified.** Reject any handoff missing one of those four fields — confidence without a tier prevents safety-gate routing.
4. **Time-to-investigation, not time-to-fix, is the metric to optimise.** Wiz's published 30 min → 60 s number is a *triage* speedup; the remediation tier still gates the action.
