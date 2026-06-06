# Scoring Methodology

**Purpose:** RPN scales, definitions, and action thresholds.
**Read when:** Executing SCORE phase or calibrating risk levels.

---

## RPN (Risk Priority Number)

**Formula:** `RPN = Severity × Occurrence × Detection`

Range: 1 (minimal risk) to 1000 (maximum risk)

---

## Severity Scale (S)

| Score | Level | Definition | Examples |
|-------|-------|------------|----------|
| 10 | Catastrophic | Data loss, security breach, regulatory violation | PII leak, financial data corruption |
| 9 | Hazardous | System-wide outage, irreversible damage | Production DB corruption, complete service down |
| 8 | Very High | Major feature broken, significant data inconsistency | Payment processing failure, auth bypass |
| 7 | High | Key functionality degraded, user-visible errors | Search returns wrong results, slow response |
| 6 | Moderate | Secondary feature broken, workaround exists | Export fails but manual download works |
| 5 | Low-Moderate | Minor functionality affected, minor inconvenience | Formatting errors, non-critical notification delay |
| 4 | Low | Cosmetic issues, barely noticeable | Alignment off by pixels, tooltip missing |
| 3 | Very Low | Noticed only by internal team | Log format inconsistency |
| 2 | Minor | Negligible impact, detected in monitoring | Metric drift, non-critical warning |
| 1 | None | No discernible effect | Dead code path never reached |

---

## Occurrence Scale (O)

| Score | Level | Probability | Rough Frequency |
|-------|-------|-------------|-----------------|
| 10 | Certain | > 50% | Every release |
| 9 | Very High | 30-50% | Every other release |
| 8 | High | 20-30% | Monthly |
| 7 | Moderately High | 10-20% | Quarterly |
| 6 | Moderate | 5-10% | Semi-annually |
| 5 | Low-Moderate | 2-5% | Annually |
| 4 | Low | 1-2% | Every few years |
| 3 | Very Low | 0.1-1% | Rare but documented |
| 2 | Remote | < 0.1% | Almost never seen |
| 1 | Nearly Impossible | < 0.01% | Theoretically possible only |

---

## Detection Scale (D) — Inverted

| Score | Level | Definition | Detection Method |
|-------|-------|------------|-----------------|
| 10 | Undetectable | No known detection mechanism | No tests, no monitoring, no review |
| 9 | Very Remote | Detection almost impossible before impact | Only found in production by user reports |
| 8 | Remote | Unreliable detection | Occasional manual review might catch it |
| 7 | Very Low | Low chance of detection | Detected only by thorough code review |
| 6 | Low | Might be caught by existing processes | Caught by integration tests sometimes |
| 5 | Moderate | Even chance of detection | Caught by CI pipeline ~50% of time |
| 4 | Moderately High | Good detection probability | Caught by unit tests most of the time |
| 3 | High | Almost certain detection pre-deploy | Strong test suite + code review catches it |
| 2 | Very High | Detected before code merge | Pre-commit hooks + linting + type checking |
| 1 | Certain | Impossible to miss | Compile error / build failure |

---

## Action Thresholds

| RPN Range | Risk Level | Required Action |
|-----------|-----------|-----------------|
| **> 200** | Critical | Immediate mitigation required. Release blocker. Escalate to Magi if trade-offs involved. |
| **100-200** | High | Planned mitigation before release. Route to appropriate agent for resolution. |
| **50-99** | Medium | Enhanced monitoring. Address in next sprint. Route to Beacon for observability. |
| **< 50** | Low | Acceptable risk. Document and monitor. No immediate action needed. |

### Special Rules

- **S ≥ 9 regardless of RPN**: Always flag as critical — catastrophic severity cannot be offset by low occurrence
- **D ≥ 8 regardless of RPN**: Always flag for detection improvement — undetectable failures are time bombs
- **Multiple RPNs 100-200**: If ≥ 3 failure modes score HIGH, treat aggregate risk as Critical

---

## Failure Category Taxonomy

| Category | Sub-categories |
|----------|---------------|
| **Technical** | Architecture, Performance, Scalability, Integration, Data Integrity |
| **Operational** | Deployment, Configuration, Monitoring, Recovery, Maintenance |
| **Security** | Authentication, Authorization, Data Protection, Input Validation |
| **Human** | Skills Gap, Process Error, Communication, Knowledge Loss |
| **External** | Vendor, Regulatory, Market, Infrastructure (cloud/network) |
| **Temporal** | Race Conditions, Ordering, Timeout, Clock Skew |
