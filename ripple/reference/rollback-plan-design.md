# Rollback Plan Design Reference

Purpose: Reversibility contract for a proposed change. Forward-compatibility strategy, dual-write window, backfill plan, feature-flag kill-switch, reverse-migration, and abort-criteria. Produces a rollback plan with explicit time-to-rollback (ToR) target and blast-radius-after-rollback estimate.

## Scope Boundary

- **ripple `rollback-plan`**: Reversibility design for a *proposed* change — forward-compat, dual-write, backfill, abort criteria (this document).
- **ripple `blast-radius` (elsewhere)**: Blast radius *before* rollback. Pairs with this recipe (blast-radius informs ToR urgency).
- **ripple `canary-scope` (elsewhere)**: Canary rollout. Auto-abort thresholds from canary trigger the rollback plan defined here.
- **schema `rollback` (elsewhere)**: Reverse-DDL and DB-specific reverse operations. This recipe owns the *plan*; schema owns the *SQL*.
- **Launch (elsewhere)**: Release gating and execution. This recipe supplies the rollback artifact; Launch gates the release on its presence.
- **Triage / Mend (elsewhere)**: Live incident rollback execution. This recipe is pre-change; Triage/Mend is during-incident.

## Workflow

```
CLASSIFY   →  change type: stateless / stateful / schema / contract
           →  reversibility floor: reversible / expand-contract / one-way

DESIGN     →  forward-compat strategy (readers tolerate new + old)
           →  dual-write window (when state is involved)
           →  feature flag + kill-switch (runtime reversal)
           →  reverse-operation plan (schema / event replay / compensating action)

CRITERIA   →  auto-abort signals (SLO, error rate, business KPI)
           →  manual-abort signals (customer reports, security escalation)
           →  abort-window: how long after deploy does the plan cover?

ToR TARGET →  time-to-rollback goal (SEV1 < 5 min, SEV2 < 15 min, SEV3 < 1h)
           →  identify slowest step in rollback chain; optimize

VERIFY     →  rollback-rehearsal plan (non-production)
           →  post-rollback state validation checklist

DOCUMENT   →  reversibility contract attached to PR
           →  rollback runbook linked from Launch release ticket
```

## Change Type × Reversibility

| Change Type | Reversibility | Primary Strategy |
|-------------|---------------|------------------|
| Stateless code (pure logic) | Reversible | Deploy previous image; feature-flag instant off |
| Stateful code (session, queue) | Conditionally reversible | Dual-write + drain window; flag-controlled reader |
| Schema additive (new column, new table) | Reversible | Expand-contract; readers tolerate new + old |
| Schema destructive (drop column, rename) | Expand-contract MUST | 3-step: expand → dual-write → contract |
| Data backfill | Reversible only with audit log | Idempotent backfill + replay capability |
| External API contract (v1→v2) | Versioned | Parallel endpoints; sunset timeline |
| Event schema (Kafka topic) | Expand-contract | New field tolerant consumers, then producer emits, then consumers require |
| One-way (delete PII, destroy keys) | Irreversible | Pre-change approval gate; no rollback possible |

## Expand-Contract Pattern (Essential for Schema Changes)

```
PHASE 1 EXPAND
  │
  ├─ Add new column / new table / new API version
  ├─ Readers tolerate BOTH old and new shapes
  ├─ No writer change yet
  │
  ▼
PHASE 2 DUAL-WRITE
  │
  ├─ Writers write to BOTH old and new
  ├─ Readers may still read from old (safe fallback)
  ├─ Backfill historical data into new shape
  ├─ Verify consistency (old == new)
  │
  ▼
PHASE 3 FLIP READERS
  │
  ├─ Readers read from new (via feature flag)
  ├─ Old remains populated as safety net
  │
  ▼
PHASE 4 CONTRACT
  │
  ├─ Writers stop writing to old
  ├─ Readers only new
  ├─ Schedule old column/table removal (24-72h later)
  │
  ▼
PHASE 5 CLEAN UP
  │
  └─ Drop old column/table after safety window
```

**Rollback at any phase**:
- Phase 1: revert code (no state mutation).
- Phase 2: stop dual-write (old is still authoritative).
- Phase 3: flip feature flag back to old reader.
- Phase 4: re-enable old writer (requires backfill if gap exists).
- Phase 5: point of no return — document in PR.

## Feature Flag + Kill-Switch Contract

Every change with customer-visible impact should have:

| Flag Type | Purpose | Latency to Flip |
|-----------|---------|------------------|
| Full kill-switch | Turn feature off globally | < 30 sec (LaunchDarkly / Statsig fast path) |
| Percentage ramp | Gradual rollout | Minutes (by scheduled config) |
| Tenant allowlist | Beta cohort | Minutes |
| Region toggle | Per-region | Minutes |
| Internal-only | Dogfood | Instant |

**Rule**: if the change cannot be reversed by flipping a flag within the ToR target, it does not have a valid rollback plan. Add the flag before merging.

## Abort Criteria (Auto vs Manual)

### Auto-Abort Signals (from Beacon / Canary gates)

| Signal | Threshold | Action |
|--------|-----------|--------|
| Error rate (5xx) | > 1% over 5 min OR > baseline × 3 | Auto-rollback |
| Latency P95 | > target × 1.5 over 10 min | Auto-rollback |
| Latency P99 | > target × 2 over 5 min | Auto-rollback |
| Business KPI | conversion drop ≥ 20% over 15 min | Pause + investigate |
| SLO burn | > 2x monthly budget in 1 hour | Auto-rollback |
| Audit-log anomaly | unexpected access pattern | Pause + Sentinel |

### Manual-Abort Signals

| Signal | Action |
|--------|--------|
| Customer report via support (≥3 distinct reports in 30 min) | Page on-call + abort |
| Security concern (Sentinel / Probe finding) | Immediate abort |
| Data inconsistency (dual-write divergence > 0.1%) | Abort dual-write phase |
| On-call judgment (gut check) | Abort with justification |

## ToR (Time-to-Rollback) Target

| SEV Tier | ToR Target | Rationale |
|----------|-----------|-----------|
| SEV1 | < 5 min | Customer impact compounding rapidly |
| SEV2 | < 15 min | Significant but scoped impact |
| SEV3 | < 60 min | Limited impact, prefer thoughtful rollback |
| SEV4 | Next business day | Non-urgent, schedule rollback |

Identify the slowest step in the rollback chain. If a rollback requires data replay taking 30 min but SEV1 ToR is 5 min, rollback plan is **invalid** — redesign (e.g., rely on feature flag instead of schema revert).

## Rollback Plan Template

```markdown
## Rollback Plan: [Change Name]

### Change Classification
- **Type**: [stateless / stateful / schema-additive / schema-destructive / backfill / contract / one-way]
- **Reversibility**: [reversible / conditionally / expand-contract / irreversible]
- **Expected SEV on failure**: [SEV1 / SEV2 / SEV3 / SEV4]
- **ToR target**: [time-to-rollback goal]

### Forward-Compatibility
- [ ] Readers tolerate both old and new shapes
- [ ] Writers can be selectively enabled/disabled
- [ ] No breaking change to downstream consumers in the rollback window

### Rollback Mechanism
- **Primary**: [feature flag name / deploy rollback / DB reverse migration / event replay]
- **Flag name**: [if applicable]
- **Deploy rollback command**: [CLI / one-liner]
- **Reverse migration path**: [handoff to schema `rollback`]

### Dual-Write Plan (if stateful)
- **Start timestamp**: [deploy time]
- **End timestamp**: [N hours / days after flip]
- **Consistency check**: [SQL / streaming diff]
- **Divergence threshold for abort**: [% / count]

### Abort Criteria
- **Auto-abort signals**: [list with thresholds]
- **Manual-abort signals**: [list]
- **Abort-window**: [e.g., 72h after deploy]

### Rollback Runbook (ordered steps)
1. [First step, including who executes]
2. [Second step]
3. [Verification step]
4. [Communication step — status page, customer comms]

### Post-Rollback Verification
- [ ] SLOs recovered
- [ ] Data consistency verified
- [ ] Customer reports cleared
- [ ] Error budget no longer burning
- [ ] Team post-mortem scheduled

### Blast Radius After Rollback (estimate)
- [What damage persists even after rollback — e.g., lost events, missed emails]
- [Recovery plan for residual damage]

### Rehearsal Status
- [ ] Rehearsed in staging
- [ ] Rehearsed in preview environment
- [ ] Chaos-engineering rollback drill (siege handoff)

### Handoffs
- [ ] Launch (release gating)
- [ ] schema `rollback` (reverse DDL)
- [ ] Beacon (rollback alerts + SLO guard)
- [ ] Triage (on-call brief if SEV1/2)
- [ ] Mend (runbook registration for automated remediation)
```

## Irreversible Change Gate

If classification is **one-way** (irreversible), enforce:

1. **Approval gate**: sign-off from owner of affected data/system + security/compliance lead.
2. **Pre-change backup**: full snapshot of affected state, retention ≥ 90 days.
3. **Customer communication**: if customer-visible, pre-announce per contract SLA.
4. **Defer if possible**: prefer expand-contract or versioned parallel surface over destructive one-way change.

No irreversible change ships without a documented rollback-not-possible rationale accepted by leadership.

## Deliverable Contract

When `rollback-plan` completes, emit:

- **Change classification** and **reversibility floor**.
- **Forward-compatibility plan** (reader/writer tolerance).
- **Feature flag + kill-switch contract** (name, flip latency).
- **Expand-contract phase map** (if schema / stateful).
- **Auto-abort + manual-abort criteria** with thresholds.
- **ToR target** per SEV tier.
- **Rollback runbook** (ordered, named owners, verification steps).
- **Post-rollback blast-radius estimate** (residual damage).
- **Rehearsal status**.
- **Handoffs**: Launch, schema `rollback`, Beacon, Triage, Mend.

## References

- Martin Fowler — "Branch By Abstraction" and "Expand and Contract" patterns
- GitHub Engineering — "Online migrations at scale"
- Stripe — "Online migrations at scale" (dual-write + backfill)
- Google SRE Workbook — "Managing Incidents" (ToR targets)
- LaunchDarkly / Statsig — Feature flag rollback patterns
- Database Reliability Engineering (Charity Majors et al.)
