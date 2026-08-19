# Control Mapping Reference

## Framework-to-Code Mapping Patterns

### Mapping Process

1. **Identify requirement** -> specific framework section (e.g., PCI-DSS Req 3.4)
2. **Locate implementation** -> code, config, infrastructure, or process
3. **Assess status** -> Implemented / Partial / Missing / N/A
4. **Document evidence** -> file:line, config path, screenshot, or policy reference
5. **Assign owner** -> team or individual responsible for control operation

### Common Code-Level Controls

| Regulatory Requirement | Code Pattern | Where to Check |
|-----------------------|--------------|----------------|
| Encryption at rest | AES-256, KMS integration, DB encryption config | DB config, storage config, KMS policies |
| Encryption in transit | TLS 1.2+, certificate pinning | Server config, HTTP client config, load balancer |
| Access control | RBAC/ABAC middleware, permission checks | Auth middleware, route guards, API interceptors |
| Audit logging | Structured audit events, immutable log store | Logger config, audit middleware, event handlers |
| Input validation | Schema validation, sanitization | Request validators, form handlers, API schemas |
| Session management | Token expiry, secure cookie flags | Auth config, session middleware |
| Password policy | Complexity requirements, bcrypt/argon2 hashing | Auth service, user model, password validator |
| MFA | TOTP, WebAuthn, SMS (deprecated) | Auth flow, login handlers |
| Data retention | TTL policies, cron deletion jobs | DB schemas, cron configs, lifecycle policies |
| Backup/recovery | Automated backups, tested restore procedures | Backup scripts, DR runbooks |

---

## Cross-Framework Control Alignment

Many controls satisfy multiple frameworks simultaneously:

| Control Area | SOC2 | PCI-DSS v4.0 | HIPAA | ISO 27001:2022 |
|-------------|------|-------------|-------|----------------|
| Access control | CC6.1-6.3 | Req 7, 8 | §164.312(a) | A.5.15, A.8.5 |
| Encryption at rest | CC6.7 | Req 3.4-3.5 | §164.312(a)(2)(iv) | A.8.24 |
| Encryption in transit | CC6.7 | Req 4.1 | §164.312(e)(1) | A.8.24 |
| Audit logging | CC7.2 | Req 10 | §164.312(b) | A.8.15, A.8.16 |
| Change management | CC8.1 | Req 6.5 | §164.308(a)(5)(ii)(C) | A.8.25, A.8.32 |
| Vulnerability management | CC7.1 | Req 6.3, 11 | §164.308(a)(1)(ii)(B) | A.8.8 |
| Incident response | CC7.3-7.5 | Req 12.10 | §164.308(a)(6) | A.5.24-5.28 |
| Risk assessment | CC3.1-3.4 | Req 12.2 | §164.308(a)(1)(ii)(A) | A.5.1, Clause 6 |
| Security awareness | CC1.4 | Req 12.6 | §164.308(a)(5) | A.6.3 |
| Data classification | CC6.7 | Req 3.2 | §164.308(a)(1)(ii)(A) | A.5.12, A.5.13 |

### Efficiency Tip
When implementing controls that span multiple frameworks, prioritize the strictest requirement. For example:
- **MFA**: PCI-DSS v4.0 Req 8.3.6 requires MFA for all CDE access (strictest) -> satisfies SOC2 CC6.1 and ISO 27001 A.8.5
- **Log retention**: PCI-DSS Req 10.7 requires 12 months (3 months immediately available) -> typically satisfies SOC2 and ISO 27001

---

## Control Assessment Template

```markdown
## Control Assessment: [Control ID]

**Framework:** [SOC2 CC6.1 / PCI-DSS Req 3.4 / etc.]
**Requirement:** [Description of what the control requires]
**Status:** [Implemented | Partial | Missing | N/A]

### Evidence
- **Location:** [file:line / config path / infrastructure component]
- **Description:** [What was observed]
- **Last verified:** [YYYY-MM-DD]

### Gaps (if Partial or Missing)
- [ ] Gap 1: [description]
- [ ] Gap 2: [description]

### Remediation
- **Priority:** [Critical | High | Medium | Low]
- **Owner:** [team/individual]
- **Implementation pattern:** [reference to code pattern]
- **Target date:** [YYYY-MM-DD]

### Cross-framework coverage
- Also satisfies: [list other framework requirements]
```

---

## Scoping Guidance

### Questions to Determine Scope

1. **What data do you handle?** (cardholder data, ePHI, PII, confidential business data)
2. **Where does it flow?** (ingestion -> processing -> storage -> sharing -> deletion)
3. **Who has access?** (users, admins, third parties, automated systems)
4. **What infrastructure?** (cloud provider, regions, services, network topology)
5. **What third parties?** (subprocessors, SaaS vendors, payment processors)

### Scope Reduction Strategies

| Strategy | Applicable to | How |
|----------|--------------|-----|
| Tokenization | PCI-DSS | Replace PAN with tokens; CDE scope limited to tokenization service |
| Segmentation | PCI-DSS, SOC2 | Network isolation of in-scope systems from general environment |
| Third-party delegation | PCI-DSS | Use payment processor's hosted payment page (iframe/redirect) |
| Data minimization | All | Don't collect/store data you don't need |
| BAA-eligible services | HIPAA | Use only cloud services covered under BAA |
