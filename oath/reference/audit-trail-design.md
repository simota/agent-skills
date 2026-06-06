# Audit Trail Design Reference

## Core Principles

1. **Immutability**: Audit logs must be append-only; no modification or deletion
2. **Completeness**: Every security-relevant action must be logged
3. **Integrity**: Tamper detection mechanisms must be in place
4. **Availability**: Logs must be accessible for the required retention period
5. **Timeliness**: Events must be logged at or near real-time (NTP sync required)

---

## Audit Event Schema

```typescript
interface AuditEvent {
  // Identity
  eventId: string;          // UUID v7 (time-ordered)
  timestamp: string;        // ISO 8601 with timezone

  // Actor
  actorId: string;          // User ID or system identity
  actorType: 'user' | 'service' | 'system' | 'admin';
  actorIp?: string;         // Source IP (if applicable)
  sessionId?: string;       // Session identifier

  // Action
  action: string;           // Verb: 'create' | 'read' | 'update' | 'delete' | 'login' | 'logout' | 'export' | 'grant' | 'revoke'
  resource: string;         // Target resource type
  resourceId: string;       // Target resource identifier

  // Context
  outcome: 'success' | 'failure' | 'denied';
  reason?: string;          // Failure/denial reason
  metadata?: Record<string, unknown>; // Additional context (no PII/secrets)

  // Integrity
  previousHash?: string;    // Hash chain for tamper detection
  eventHash: string;        // SHA-256 of event payload
}
```

---

## Framework-Specific Logging Requirements

| Framework | What to Log | Retention | Integrity |
|-----------|-------------|-----------|-----------|
| **SOC2** (CC7.2) | Security events, access changes, system modifications | Per policy (typically 1 year) | Monitoring and alerting |
| **PCI-DSS** (Req 10) | All access to CHD, admin actions, invalid access attempts, auth events | 12 months (3 months immediately available) | Log integrity monitoring (Req 10.3.4) |
| **HIPAA** (§164.312(b)) | All ePHI access, modifications, disclosures | 6 years minimum | Protection from alteration |
| **ISO 27001** (A.8.15) | User activities, exceptions, faults, information security events | Per risk assessment | Log protection (A.8.15) |

### PCI-DSS Req 10 Specifics

Must log:
- All individual user access to cardholder data (10.2.1)
- All actions by admin/root (10.2.2)
- Access to all audit trails (10.2.3)
- Invalid logical access attempts (10.2.4)
- Use of identification and authentication mechanisms (10.2.5)
- Initialization, stopping, or pausing of audit logs (10.2.6)
- Creation and deletion of system-level objects (10.2.7)

---

## Implementation Patterns

### Append-Only Log Store

```
Application -> Audit Middleware -> Message Queue -> Immutable Store
                                                     |
                                                     v
                                              Integrity Verifier
                                                     |
                                                     v
                                              SIEM / Analytics
```

**Recommended stores:**
- AWS CloudTrail + S3 (Object Lock) + CloudWatch
- Azure Monitor + Immutable Blob Storage
- GCP Cloud Audit Logs + Cloud Storage (retention lock)
- Self-hosted: Append-only PostgreSQL (BEFORE DELETE trigger blocks deletion) + external backup

### Hash Chain Pattern

```
Event[n].hash = SHA-256(Event[n].payload + Event[n-1].hash)
```

- Genesis event uses a known seed
- Periodic hash checkpoints stored in separate system
- Verification: replay chain from genesis, compare intermediate hashes
- Break in chain indicates tampering

### Log Integrity Monitoring

| Check | Frequency | Action on Failure |
|-------|-----------|-------------------|
| Hash chain verification | Hourly | Alert + investigation |
| Log volume anomaly | Real-time | Alert if volume drops >50% or spikes >300% |
| Gap detection | Hourly | Alert if time gaps >5 minutes between events |
| Cross-system reconciliation | Daily | Compare event counts across systems |

---

## Evidence Collection for Auditors

| Evidence Type | Description | Format |
|--------------|-------------|--------|
| Log samples | Representative audit log entries | JSON/structured text |
| Retention proof | Configuration showing retention period | Config file screenshot |
| Integrity proof | Hash chain verification report | Automated report |
| Access proof | Who can access/modify audit logs | IAM policy export |
| Alerting proof | Alert configuration for log tampering | Alert rule screenshot |
| NTP proof | Time synchronization configuration | NTP config + drift reports |

---

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|-------------|---------|-----|
| Logging PII/secrets in audit trail | Privacy/security violation | Log resource IDs only, never values |
| Mutable log store | Tamper risk, audit failure | Use append-only storage with Object Lock |
| No NTP sync | Unreliable timestamps | Configure NTP on all systems |
| Application-managed log deletion | Logs can be tampered with | Separate log management from application |
| Logging to local filesystem only | Loss risk, no centralization | Ship to centralized immutable store |
| No log access controls | Anyone can read/modify logs | Restrict log access to security team |
