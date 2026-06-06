# Verification Strategies

Purpose: Read this file when validating incoming remediation input, running the staged verification cascade, deciding rollback, or writing the verification report.

## Contents

- Verification cascade
- Rollback criteria
- Extended monitoring
- Post-verification report

Staged verification ensures remediation success before declaring an incident resolved. Every fix goes through 4 stages.

---

## Verification Cascade

### Stage 0: Input Validation (Pre-Remediation)

**Actor:** Mend (pre-check)
**Purpose:** Verify that incoming telemetry and diagnosis are consistent and not adversarially crafted.

| Check | Pass Criteria | Fail Action |
|-------|--------------|-------------|
| Schema validation | All required handoff fields present, values in plausible ranges | Reject — request re-diagnosis |
| Cross-source corroboration | ≥ 2 independent sources confirm the signal (exception: T1 with trusted health check) | Downgrade to INVESTIGATE mode |
| User-content isolation | Pattern match uses structured fields, not raw user-generated text | Sanitize before proceeding |
| Input anomaly detection | No volume anomalies, contradictions, or suspiciously uniform timing | Hold — flag for human review |

**Duration:** < 5 seconds (automated checks)
**On Fail:** Downgrade autonomy — never auto-remediate on suspicious input. See `reference/adversarial-defense.md` for full protocol.

---

### Stage 1: Health Check (Immediate, +0s)

**Actor:** Mend (self-check)
**Purpose:** Confirm the fix didn't make things worse.

| Check | Pass Criteria | Fail Action |
|-------|--------------|-------------|
| Process/service alive | All target pods/processes running | Rollback immediately |
| No crash loops | Restart count stable (not increasing) | Rollback immediately |
| No new errors in logs | No ERROR/FATAL in last 30s of logs | Investigate — rollback if critical |
| Basic endpoint responsive | HTTP 200 on health endpoint within 2s | Rollback immediately |

**Duration:** < 30 seconds
**On Fail:** Trigger immediate rollback → Escalate to Triage with failure details

---

### Stage 2: Smoke Test (+30 seconds)

**Actor:** Mend → Radar (via `MEND_TO_RADAR_HANDOFF`)
**Purpose:** Verify core functionality works correctly.

| Check | Pass Criteria | Fail Action |
|-------|--------------|-------------|
| Core API endpoints respond | Expected status codes and response shapes | Rollback + escalate |
| Critical user flows complete | Login, core actions succeed | Rollback + escalate |
| No error rate increase | Error rate ≤ pre-incident rate + 5% | Hold — recheck at 60s |
| No latency degradation | P99 latency ≤ pre-incident baseline + 20% | Hold — recheck at 60s |

**Duration:** 30-60 seconds
**On Fail:** Rollback → Escalate to Triage with test results

---

### Stage 3: SLO Check (+5 minutes)

**Actor:** Mend → Beacon (via `MEND_TO_BEACON_HANDOFF`)
**Purpose:** Confirm SLO metrics are recovering toward target.

| Check | Pass Criteria | Fail Action |
|-------|--------------|-------------|
| Error budget burn rate | Decreasing or stable (not increasing) | Extend monitoring (max +10 min) |
| SLO compliance trending | Moving toward target (not away) | Extend monitoring (max +10 min) |
| Affected SLIs improving | SLI values better than incident peak | Hold — investigate if stagnant |
| No new SLO violations | No new violations in other SLOs | Investigate correlation |

**Duration:** 5 minutes observation window
**On Fail:** Extend monitoring to +15 min total → If still failing: escalate

---

### Stage 4: Recovery Confirmed (+10 minutes)

**Actor:** Mend → Beacon (final confirmation)
**Purpose:** Declare incident resolved with confidence.

| Check | Pass Criteria | Fail Action |
|-------|--------------|-------------|
| SLO within acceptable range | SLO compliance ≥ target - 1% | Continue monitoring |
| Error rate normalized | Error rate within normal operating range | Continue monitoring |
| No regression signals | No new alerts or anomalies | Continue monitoring |
| System stable | All metrics stable for 5+ min | Mark RESOLVED |

**Duration:** 5 minutes final observation
**On Pass:** Mark incident as RESOLVED → Generate remediation report
**On Fail:** Escalate to Triage for extended investigation

---

## Verification Flow Diagram

```
Remediation Applied
  │
  ├─[Stage 1: Health Check, +0s]─── FAIL ──→ Rollback → Escalate
  │    │ PASS
  │    ↓
  ├─[Stage 2: Smoke Test, +30s]──── FAIL ──→ Rollback → Escalate
  │    │ PASS
  │    ↓
  ├─[Stage 3: SLO Check, +5min]──── FAIL ──→ Extend (+10min)
  │    │ PASS                                    │ Still FAIL
  │    ↓                                         ↓
  ├─[Stage 4: Confirmed, +10min]── FAIL ──→ Escalate to Triage
  │    │ PASS
  │    ↓
  └─ RESOLVED ✓
```

---

## Rollback Criteria

### Automatic Rollback Triggers

Rollback is triggered immediately (no human approval needed) when:

| Trigger | Threshold | Stage |
|---------|-----------|-------|
| Service crash | Any target service crashes post-fix | Stage 1 |
| Error rate spike | Error rate > pre-incident rate × 1.5 | Stage 1-2 |
| Health check timeout | No response within 10s | Stage 1 |
| New error types | Error types not present pre-remediation | Stage 2 |
| Latency blow-up | P99 > pre-incident × 2 | Stage 2 |

### Conditional Rollback (Requires Evaluation)

| Trigger | Threshold | Action |
|---------|-----------|--------|
| SLO not improving | No improvement after extended monitoring | Evaluate — rollback if stagnant |
| Partial recovery | Some metrics improved, others not | Investigate correlation |
| Resource spike | CPU/Memory > pre-incident + 50% | Evaluate — may be expected during recovery |

### Rollback Execution

1. Record current (failed) state for postmortem
2. Execute rollback steps in reverse order of applied changes
3. Verify rollback success (system returns to pre-remediation state)
4. If rollback fails: escalate immediately to Triage + Gear
5. Document rollback in incident timeline

---

## Extended Monitoring

When Stage 3 fails but doesn't trigger rollback:

| Window | Check Interval | Decision Point |
|--------|---------------|----------------|
| +5 to +10 min | Every 60s | If improving: continue to Stage 4 |
| +10 to +15 min | Every 60s | If stagnant: escalate |
| > +15 min | N/A | Force decision: rollback or escalate |

### Extended Monitoring Criteria

- **Improving:** At least 1 SLI metric improved per interval → Continue
- **Stagnant:** No SLI improvement for 2 consecutive intervals → Escalate
- **Degrading:** Any SLI metric worsening → Rollback

---

## Post-Verification Report

After verification completes (regardless of outcome):

```markdown
## Verification Report

**Incident:** [incident_id]
**Remediation:** [pattern_id / runbook_title]
**Final Status:** RESOLVED / ROLLBACK / ESCALATED

### Stage Results
| Stage | Result | Duration | Details |
|-------|--------|----------|---------|
| Health Check | PASS | 15s | All services healthy |
| Smoke Test | PASS | 45s | Core endpoints OK |
| SLO Check | PASS | 5m | Error budget burn rate decreasing |
| Recovery | PASS | 10m | SLO within target |

### SLO Impact Summary
| SLO | Pre-Incident | During Incident | Post-Remediation |
|-----|-------------|-----------------|------------------|
| Availability | 99.95% | 98.2% | 99.93% |
| Latency P99 | 200ms | 2500ms | 210ms |

### Error Budget Impact
- Budget consumed: [X%]
- Remaining budget: [Y%]
- Projected monthly impact: [Z%]
```
