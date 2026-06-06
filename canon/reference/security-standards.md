# Security Standards Reference

## OWASP Top 10:2025 (supersedes 2021)

[Source: https://owasp.org/Top10/2025/]

The OWASP Top 10:2025 restructured significantly from 2021: Security Misconfiguration rose #5→#2; SSRF absorbed into A01 Broken Access Control; A03 expanded to Software Supply Chain Failures (entire supply chain scope); A07 renamed Authentication Failures; A09 renamed Security Logging and Alerting Failures; new A10 Mishandling of Exceptional Conditions. Dataset doubled to 500k+ apps from 40+ orgs. **Always assess against 2025 categories** — the 2021 category names below are superseded.

### Overview
The OWASP Top 10 represents the most critical security risks to web applications (2025 edition).

| ID | Category (2025) | Risk Level |
|----|-----------------|------------|
| A01:2025 | Broken Access Control (incl. SSRF) | Critical |
| A02:2025 | Security Misconfiguration | Critical |
| A03:2025 | Software Supply Chain Failures | Critical |
| A04:2025 | Insecure Design | High |
| A05:2025 | Cryptographic Failures | High |
| A06:2025 | Vulnerable and Outdated Components | High |
| A07:2025 | Authentication Failures | High |
| A08:2025 | Software and Data Integrity Failures | High |
| A09:2025 | Security Logging and Alerting Failures | Medium |
| A10:2025 | Mishandling of Exceptional Conditions | High |

### A01:2025 - Broken Access Control (incl. SSRF)

**Requirement:** Ensure access control policies enforce that users cannot act outside their intended permissions.

**Compliance Checklist:**
- [ ] Deny by default for all resources
- [ ] Implement access control mechanisms once, reuse throughout application
- [ ] Log access control failures, alert on repeated failures
- [ ] Rate limit API and controller access
- [ ] Disable web server directory listing
- [ ] Invalidate JWT tokens on server after logout

**Detection Patterns:**
```regex
# Missing authorization check
@(Get|Post|Put|Delete|Patch).*\n(?!.*@(Authorize|RequirePermission))

# Direct object reference without validation
findById\(req\.(params|query|body)\.\w+\)
```

**Non-Compliant Example:**
```typescript
// Missing authorization - any user can access any order
app.get('/orders/:id', async (req, res) => {
  const order = await Order.findById(req.params.id);
  res.json(order);
});
```

**Compliant Example:**
```typescript
// Authorization check ensures user owns the order
app.get('/orders/:id', async (req, res) => {
  const order = await Order.findById(req.params.id);
  if (order.userId !== req.user.id) {
    return res.status(403).json({ error: 'Forbidden' });
  }
  res.json(order);
});
```

### A05:2025 - Cryptographic Failures

**Requirement:** Protect sensitive data at rest and in transit using appropriate cryptographic mechanisms.

**Compliance Checklist:**
- [ ] Classify data processed, stored, or transmitted
- [ ] Encrypt all sensitive data at rest
- [ ] Encrypt all data in transit with TLS 1.2+
- [ ] Disable caching for sensitive data responses
- [ ] Use strong adaptive hashing (bcrypt, Argon2) for passwords
- [ ] Use authenticated encryption (e.g., AES-GCM)

**Deprecated Algorithms (Never Use):**
- MD5, SHA1 for security purposes
- DES, 3DES
- RC4
- TLS 1.0, TLS 1.1

**Recommended Algorithms:**
| Purpose | Algorithm |
|---------|-----------|
| Password hashing | Argon2id, bcrypt (cost 12+), PBKDF2 |
| Symmetric encryption | AES-256-GCM |
| Asymmetric encryption | RSA-2048+, ECDSA P-256+ |
| Hashing | SHA-256, SHA-3 |
| TLS | TLS 1.3 (preferred), TLS 1.2 |

### A03:2025 - Software Supply Chain Failures (incl. Injection)

**Requirement:** Prevent injection by validating, sanitizing, and parameterizing all user input.

**Injection Types:**
| Type | Vector | Prevention |
|------|--------|------------|
| SQL | Database queries | Parameterized queries, ORM |
| NoSQL | MongoDB, etc. | Input validation, schema enforcement |
| Command | Shell execution | Avoid exec(), use execFile() |
| LDAP | Directory queries | Input escaping, parameterization |
| XSS | HTML output | Output encoding, CSP |

**Detection Patterns:**
```regex
# SQL injection risk
(query|execute)\s*\(\s*['"`].*\$\{.*\}
(query|execute)\s*\(\s*['"`].*\+\s*\w+

# Command injection risk
exec\s*\(\s*['"`].*\$\{
spawn\s*\(.*\+

# NoSQL injection risk
\{\s*\$\w+\s*:.*req\.(body|query|params)
```

**Non-Compliant:**
```typescript
// SQL injection vulnerability
const user = await db.query(`SELECT * FROM users WHERE id = ${req.params.id}`);
```

**Compliant:**
```typescript
// Parameterized query
const user = await db.query('SELECT * FROM users WHERE id = ?', [req.params.id]);
```

### A04:2025 - Insecure Design

**Requirement:** Use secure design patterns and threat modeling from the start.

**Secure Design Principles:**
1. Defense in Depth - Multiple security layers
2. Least Privilege - Minimum necessary permissions
3. Fail Secure - Deny access on error
4. Separation of Concerns - Isolate security-critical code
5. Trust Boundaries - Validate at all boundaries

**Design Review Checklist:**
- [ ] Threat model created for critical flows
- [ ] Security requirements defined
- [ ] Abuse cases documented
- [ ] Rate limiting for resource-intensive operations
- [ ] Business logic abuse prevention

### A02:2025 - Security Misconfiguration

**Requirement:** Secure configuration across all application components.

**Checklist:**
- [ ] Remove or disable unnecessary features
- [ ] Change default credentials
- [ ] Disable directory listing
- [ ] Configure security headers
- [ ] Remove debug/development features in production
- [ ] Update error handling to not leak information

**Required Security Headers:**
```
Content-Security-Policy: default-src 'self'
Strict-Transport-Security: max-age=31536000; includeSubDomains
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: camera=(), microphone=(), geolocation=()
```

### A06:2025 - Vulnerable and Outdated Components

**Requirement:** Maintain inventory of components and update vulnerable dependencies.

**Compliance Activities:**
- [ ] Remove unused dependencies
- [ ] Inventory all components and versions
- [ ] Monitor CVE databases for vulnerabilities
- [ ] Use only components from official sources
- [ ] Have a plan for monitoring and updating

**Detection Commands:**
```bash
# npm/yarn
npm audit
yarn audit

# Python
pip-audit
safety check

# Ruby
bundle audit

# Java
mvn dependency-check:check
```

### A07:2025 - Authentication Failures

**Requirement:** Implement robust authentication mechanisms.

**Checklist:**
- [ ] Multi-factor authentication available
- [ ] Prevent weak passwords
- [ ] Limit failed login attempts (rate limiting)
- [ ] Use secure session management
- [ ] Secure credential recovery process

**Password Requirements:**
- Minimum 8 characters
- Check against breached password lists
- No character composition requirements (NIST 800-63B)
- Rate limit authentication attempts

### A08:2025 - Software and Data Integrity Failures

**Requirement:** Ensure integrity of software and data.

**Checklist:**
- [ ] Verify digital signatures of updates
- [ ] Use integrity checks (SRI) for CDN resources
- [ ] Secure CI/CD pipeline
- [ ] Review code and configuration changes
- [ ] Validate serialized data

### A09:2025 - Security Logging and Alerting Failures

**Requirement:** Log security events and monitor for anomalies.

**Events to Log:**
- Authentication successes and failures
- Authorization failures
- Input validation failures
- Application errors
- Configuration changes
- High-value transactions

**Log Requirements:**
- Timestamp (UTC)
- Event type
- User identifier
- Source IP
- Success/failure status
- Relevant resource identifiers

### A10:2025 - Mishandling of Exceptional Conditions

**Requirement:** Ensure exceptions, errors, and unexpected states are handled appropriately without leaking information or creating exploitable conditions.

**Prevention Measures:**
- [ ] Do not expose stack traces or internal details in production error responses
- [ ] Log exceptions server-side; return generic messages to clients
- [ ] Handle all exception paths explicitly (no bare `except`/`catch` blocks)
- [ ] Validate assumptions at system boundaries; fail securely on unexpected input
- [ ] Test for error-injection scenarios in security testing

> **Note (SSRF):** SSRF is now absorbed into A01:2025 Broken Access Control. Apply allowlist permitted URLs/hosts, disable HTTP redirects, validate URL schemes, block private IP ranges, and use network segmentation as part of A01 remediations.

---

## OWASP ASVS 5.0 (supersedes 4.x)

[Source: https://owasp.org/www-project-application-security-verification-standard/ — released May 2025 at Global AppSec EU Barcelona]

ASVS 5.0 is a major release expanding from 286 requirements (14 chapters, v4.0.3) to ~350 requirements across 17 chapters. Key additions: dedicated chapters for Web Frontend Security and Self-Contained Tokens; cryptography guidelines updated for post-quantum considerations; password rules aligned with NIST SP 800-63B.

### Verification Levels

| Level | Target | Use Case |
|-------|--------|----------|
| L1 | Low assurance | All software |
| L2 | Standard | Most applications |
| L3 | High assurance | Critical applications |

### Key Requirements by Category

#### V1: Architecture, Design, and Threat Modeling
- V1.1: Secure SDLC requirements
- V1.2: Authentication architecture
- V1.3: Session management architecture
- V1.4: Access control architecture
- V1.5: Input/output architecture

#### V2: Authentication
- V2.1: Password security
- V2.2: General authenticator security
- V2.3: Authenticator lifecycle
- V2.4: Credential storage
- V2.5: Credential recovery

#### V3: Session Management
- V3.1: Session management fundamentals
- V3.2: Session binding
- V3.3: Session termination
- V3.4: Cookie-based session management
- V3.5: Token-based session management

#### V4: Access Control
- V4.1: General access control design
- V4.2: Operation level access control
- V4.3: Other access control considerations

#### V5: Validation, Sanitization, and Encoding
- V5.1: Input validation
- V5.2: Sanitization and sandboxing
- V5.3: Output encoding
- V5.4: Memory safety
- V5.5: Deserialization prevention

---

## NIST Cybersecurity Framework

### Core Functions

| Function | Description |
|----------|-------------|
| **Identify** | Understand risk to systems, assets, data |
| **Protect** | Implement appropriate safeguards |
| **Detect** | Identify security events |
| **Respond** | Take action on detected events |
| **Recover** | Restore capabilities after incidents |

### Key Categories

#### Identify (ID)
- Asset Management (ID.AM)
- Business Environment (ID.BE)
- Governance (ID.GV)
- Risk Assessment (ID.RA)
- Risk Management Strategy (ID.RM)

#### Protect (PR)
- Access Control (PR.AC)
- Awareness and Training (PR.AT)
- Data Security (PR.DS)
- Information Protection (PR.IP)
- Maintenance (PR.MA)
- Protective Technology (PR.PT)

#### Detect (DE)
- Anomalies and Events (DE.AE)
- Security Continuous Monitoring (DE.CM)
- Detection Processes (DE.DP)

#### Respond (RS)
- Response Planning (RS.RP)
- Communications (RS.CO)
- Analysis (RS.AN)
- Mitigation (RS.MI)
- Improvements (RS.IM)

#### Recover (RC)
- Recovery Planning (RC.RP)
- Improvements (RC.IM)
- Communications (RC.CO)

---

## CIS Controls v8

### Implementation Groups

| Group | Organization Size | Controls |
|-------|------------------|----------|
| IG1 | Small/basic | 56 safeguards |
| IG2 | Medium/enhanced | 130 safeguards |
| IG3 | Large/advanced | 153 safeguards |

### Top 10 Controls (IG1 Essentials)

1. **Inventory and Control of Enterprise Assets**
2. **Inventory and Control of Software Assets**
3. **Data Protection**
4. **Secure Configuration of Enterprise Assets and Software**
5. **Account Management**
6. **Access Control Management**
7. **Continuous Vulnerability Management**
8. **Audit Log Management**
9. **Email and Web Browser Protections**
10. **Malware Defenses**

---

## OWASP API Security Top 10:2023

[Source: https://owasp.org/API-Security/editions/2023/en/0x11-t10/]

The second edition (supersedes 2019). Authorization remains the dominant API risk with 3 of the top 5 items related to access control.

| ID | Category | Risk Level |
|----|----------|------------|
| API1:2023 | Broken Object Level Authorization | Critical |
| API2:2023 | Broken Authentication | Critical |
| API3:2023 | Broken Object Property Level Authorization | High |
| API4:2023 | Unrestricted Resource Consumption | High |
| API5:2023 | Broken Function Level Authorization | High |
| API6:2023 | Unrestricted Access to Sensitive Business Flows | High |
| API7:2023 | Server Side Request Forgery | High |
| API8:2023 | Security Misconfiguration | Medium |
| API9:2023 | Improper Inventory Management | Medium |
| API10:2023 | Unsafe Consumption of APIs | Medium |

---

## OWASP Top 10 for LLM Applications 2025

[Source: https://genai.owasp.org/resource/owasp-top-10-for-llm-applications-2025/]

Updated late 2024 to reflect real-world incidents, agentic AI, and RAG-specific threats. New entries include LLM09 (Vector and Embedding Weaknesses targeting RAG/vector databases) and LLM10 (System Prompt Leakage). Use alongside OWASP Top 10 for Agentic Applications (2026) when assessing LLM-backed systems.

---

## CWE Top 25 Most Dangerous Software Weaknesses (2025)

[Source: https://cwe.mitre.org/top25/archive/2025/2025_cwe_top25.html] [2024 list: https://cwe.mitre.org/top25/archive/2024/2024_cwe_top25.html]

Published annually by MITRE/CISA. Top 3 in 2024: Cross-Site Scripting (CWE-79), Out-of-Bounds Write (CWE-787), SQL Injection (CWE-89). The 2025 edition is available at the above URL. Use CWE citations in violation findings for interoperability with CVE/NVD tooling.

---

## NIST SSDF v1.1 / v1.2 (Draft)

[Source: https://csrc.nist.gov/pubs/sp/800/218/final] [v1.2 draft: https://csrc.nist.gov/pubs/sp/800/218/r1/ipd]

NIST SP 800-218 v1.1 defines four practice areas: Prepare the Organization (PO), Protect the Software (PS), Produce Well-Secured Software (PW), Respond to Vulnerabilities (RV). SP 800-218A augments v1.1 with AI/generative model development practices. SSDF v1.2 is in public comment (December 2025 draft). Reference SSDF when assessing CI/CD pipeline security, dependency management, and vulnerability response processes.

---

## Quick Reference: Security Standards Mapping

| Requirement | OWASP Top 10:2025 | ASVS 5.0 | NIST CSF | CIS |
|-------------|-------------------|----------|----------|-----|
| Access control (incl. SSRF) | A01:2025 | V4 | PR.AC | 5, 6 |
| Security misconfiguration | A02:2025 | V14 | PR.IP | 4 |
| Supply chain / dependencies | A03:2025, A06:2025 | V14.2 | ID.AM | 2 |
| Secure design | A04:2025 | V1 | ID.RA | - |
| Encryption | A05:2025 | V6, V9 | PR.DS | 3 |
| Authentication | A07:2025 | V2, V3 | PR.AC | 5 |
| Integrity | A08:2025 | V10 | PR.DS | - |
| Logging | A09:2025 | V7 | DE.CM | 8 |
| Error handling | A10:2025 | V7 | - | - |
