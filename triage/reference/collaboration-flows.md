# Triage Collaboration Flows Reference

Detailed collaboration patterns and flow diagrams for incident response.

Purpose: Read this when Triage must choose or explain the exact handoff flow for standard, critical, security, rollback, postmortem, or multi-service incidents.

Contents:
- `Pattern A: Standard Incident Flow (SEV3/SEV4)`: Scout → Builder → Radar baseline path
- `Pattern B: Critical Incident Flow (SEV1/SEV2)`: urgent path with Lens evidence capture
- `Pattern C: Security Incident`: Sentinel-led incident routing
- `Pattern D: Postmortem Flow`: evidence collection and postmortem closure
- `Pattern E: Rollback Coordination`: Gear rollback and Radar stability verification
- `Pattern F: Multi-Service Incident`: parallel per-service investigation routing

## Pattern A: Standard Incident Flow (SEV3/SEV4)

```
Incident Detected
       ↓
┌─────────────────────────────────────────────┐
│ Triage: Classify & Assess                   │
│ - Severity: SEV3/SEV4                       │
│ - Impact scope identified                   │
│ - Initial mitigation (if quick fix)         │
└──────────────────┬──────────────────────────┘
                   ↓
         TRIAGE_TO_SCOUT_HANDOFF
                   ↓
┌─────────────────────────────────────────────┐
│ Scout: Root Cause Analysis                  │
│ - Investigate symptoms                      │
│ - Identify root cause                       │
│ - Recommend fix location                    │
└──────────────────┬──────────────────────────┘
                   ↓
         SCOUT_TO_BUILDER_HANDOFF
                   ↓
┌─────────────────────────────────────────────┐
│ Builder: Implement Fix                      │
│ - Apply fix                                 │
│ - Deploy to production                      │
└──────────────────┬──────────────────────────┘
                   ↓
         BUILDER_TO_RADAR_HANDOFF
                   ↓
┌─────────────────────────────────────────────┐
│ Radar: Verify Fix                           │
│ - Run regression tests                      │
│ - Confirm no new issues                     │
└──────────────────┬──────────────────────────┘
                   ↓
         RADAR_TO_TRIAGE_HANDOFF
                   ↓
  Triage: Close Incident + Postmortem
```

---

## Pattern B: Critical Incident Flow (SEV1/SEV2)

```
SEV1/SEV2 Detected
       ↓
┌─────────────────────────────────────────────┐
│ Triage: Immediate Response                  │
│ - Severity confirmed: SEV1/SEV2             │
│ - Stakeholders notified                     │
│ - Status page updated                       │
└──────────────────┬──────────────────────────┘
                   ↓
    ┌──────────────┴──────────────┐
    ↓                             ↓
TRIAGE_TO_SCOUT         TRIAGE_TO_LENS
(Root cause)            (Evidence capture)
    ↓                             ↓
Scout investigates      Lens captures state
    ↓                             ↓
    └──────────────┬──────────────┘
                   ↓
         SCOUT_TO_BUILDER_HANDOFF (urgent)
                   ↓
  Builder: Hotfix → Deploy → Verify
                   ↓
  Triage: Extended verification (30 min)
                   ↓
  Triage: Close + Mandatory postmortem (24h)
```

---

## Pattern C: Security Incident

```
Security Issue Detected
       ↓
┌─────────────────────────────────────────────┐
│ Triage: Security Classification             │
│ - Assess breach scope                       │
│ - Activate security protocol                │
└──────────────────┬──────────────────────────┘
                   ↓
         TRIAGE_TO_SENTINEL_HANDOFF
                   ↓
┌─────────────────────────────────────────────┐
│ Sentinel: Security Analysis                 │
│ - Assess vulnerability                      │
│ - Determine exposure                        │
│ - Recommend remediation                     │
└──────────────────┬──────────────────────────┘
                   ↓
    Scout assists with technical RCA
                   ↓
    Builder implements security fix
                   ↓
    Sentinel verifies fix effectiveness
                   ↓
  Triage: Security postmortem + disclosure plan
```

---

## Pattern D: Postmortem Flow

```
Incident Resolved
       ↓
┌─────────────────────────────────────────────┐
│ Triage: Gather Postmortem Data              │
│ - Timeline from all agents                  │
│ - Evidence from Lens                        │
│ - Root cause from Scout                     │
└──────────────────┬──────────────────────────┘
                   ↓
┌─────────────────────────────────────────────┐
│ Triage: Write Postmortem                    │
│ - 5 Whys analysis                           │
│ - Action items with owners                  │
│ - Lessons learned                           │
└──────────────────┬──────────────────────────┘
                   ↓
  Update PROJECT.md and triage.md
```

---

## Pattern E: Rollback Coordination

```
Fix Failed or Regression Detected
       ↓
┌─────────────────────────────────────────────┐
│ Triage: Rollback Decision                   │
│ - Trigger: ON_ROLLBACK_DECISION             │
│ - User confirms rollback                    │
└──────────────────┬──────────────────────────┘
                   ↓
         TRIAGE_TO_GEAR_HANDOFF
                   ↓
┌─────────────────────────────────────────────┐
│ Gear: Execute Rollback                      │
│ - Identify rollback target                  │
│ - Execute deployment rollback               │
│ - Verify rollback success                   │
└──────────────────┬──────────────────────────┘
                   ↓
         GEAR_TO_RADAR_HANDOFF
                   ↓
  Radar: Verify system stability
                   ↓
  Triage: Continue investigation
```

---

## Pattern F: Multi-Service Incident

```
Multiple Services Affected
       ↓
┌─────────────────────────────────────────────┐
│ Triage: Coordinate Multi-Service Response   │
│ - Identify all affected services            │
│ - Prioritize by impact                      │
│ - Assign investigation per service          │
└──────────────────┬──────────────────────────┘
                   ↓
    ┌──────────────┼──────────────┐
    ↓              ↓              ↓
Scout (Svc A)  Scout (Svc B)  Scout (Svc C)
    ↓              ↓              ↓
    └──────────────┼──────────────┘
                   ↓
  Triage: Aggregate findings
                   ↓
  Builder: Coordinated fixes
                   ↓
  Radar: Cross-service verification
```
