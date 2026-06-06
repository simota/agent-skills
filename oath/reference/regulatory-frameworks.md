# Regulatory Frameworks Reference

## SOC2 Trust Service Criteria

### Overview
SOC2 reports are issued by CPA firms under AICPA standards. Type I evaluates control design at a point in time; Type II evaluates operating effectiveness over a period (typically 6-12 months).
Current authoritative version: **2017 Trust Service Criteria with 2022 Revised Points of Focus** + **2018 Description Criteria with 2022 Revised Implementation Guidance** — no newer revision as of 2025.
Sources: [AICPA SOC 2 overview](https://us.aicpa.org/interestareas/frc/assuranceadvisoryservices/aicpasoc2report.html) | [AICPA-CIMA SOC resources](https://www.aicpa-cima.com/resources/landing/system-and-organization-controls-soc-suite-of-services)

### Trust Service Criteria (TSC)

| Category | ID Range | Key Controls |
|----------|----------|--------------|
| **Security** (Common Criteria) | CC1-CC9 | CC6.1 Logical/physical access, CC6.3 Access removal, CC7.2 Monitoring, CC8.1 Change management |
| **Availability** | A1.1-A1.3 | Capacity planning, disaster recovery, backup/restore |
| **Processing Integrity** | PI1.1-PI1.5 | Data completeness, accuracy, timeliness |
| **Confidentiality** | C1.1-C1.2 | Data classification, confidential data protection |
| **Privacy** | P1-P8 | Notice, choice, collection, use, access, disclosure, quality, monitoring |

### Key Controls for Engineering Teams

| Control | Description | Implementation Pattern |
|---------|-------------|----------------------|
| CC6.1 | Logical access security | RBAC/ABAC, MFA, SSO integration |
| CC6.2 | Access provisioning/deprovisioning | Automated onboarding/offboarding, access reviews |
| CC6.3 | Access removal on termination | Automated deprovisioning triggers |
| CC7.1 | Configuration management | Infrastructure as Code, drift detection |
| CC7.2 | System monitoring | SIEM, anomaly detection, alerting |
| CC8.1 | Change management | PR reviews, CI/CD gates, rollback procedures |
| CC9.1 | Risk mitigation | Risk register, control testing |

---

## PCI-DSS v4.0.1

**Active version since January 2025. PCI-DSS v4.0 retired December 31 2024; v3.2.1 retired March 31 2024 — assessments against either retired version are audit failures.**
Source: [PCI SSC Document Library](https://www.pcisecuritystandards.org/document_library/) | [PCI DSS v4.0.1 blog](https://blog.pcisecuritystandards.org/just-published-pci-dss-v4-0-1)

### 12 Requirements

| Goal | Req | Description | Technical Focus |
|------|-----|-------------|-----------------|
| Build/Maintain Secure Network | 1 | Install and maintain network security controls | Firewalls, NSCs, microsegmentation |
| | 2 | Apply secure configurations | CIS benchmarks, hardening guides |
| Protect Account Data | 3 | Protect stored account data | Encryption at rest (AES-256), tokenization, truncation, hashing |
| | 4 | Protect data in transit | TLS 1.2+, certificate management |
| Maintain Vuln Mgmt | 5 | Protect from malicious software | Anti-malware, endpoint detection |
| | 6 | Develop and maintain secure systems | SDLC, code review, SAST/DAST, WAF |
| Access Control | 7 | Restrict access by business need | Least privilege, RBAC |
| | 8 | Identify users and authenticate | MFA, password policies, service account management |
| | 9 | Restrict physical access | Physical security (less relevant for cloud-native) |
| Monitor/Test | 10 | Log and monitor all access | Centralized logging, NTP sync, log integrity, 12-month retention |
| | 11 | Test security regularly | Vulnerability scans, penetration tests, IDS/IPS, change detection |
| InfoSec Policy | 12 | Support information security with policies | Security awareness, incident response, risk assessment |

### PCI-DSS v4.0.1 Key Changes from v4.0 (June 2024 limited revision)
- Clarified critical-vulnerability patch timeline (30 days applies only to critical vulnerabilities, reverting to v3.2.1 language)
- Added Applicability Notes for payment page script management (Req 6.4.3)
- Clarified MFA exemption: non-administrative CDE access authenticated with phishing-resistant factors is exempt from Req 8.3.6
- Removed sample Customized Approach templates from Appendix E (moved to PCI SSC website)
- No new or deleted requirements from v4.0

### All 51 Future-Dated Requirements Now Mandatory (since March 31 2025)
Key mandates enforced:
- **Req 6.4.3**: Payment page scripts — authorized inventory + integrity check required
- **Req 11.6.1**: Change-detection mechanism for payment page HTTP headers and scripts
- **Req 8.3.6**: Minimum 12-character passwords for all CDE user accounts
- **Req 8.4.2**: MFA for all CDE access including third-party remote access
- **Req 12.3.1**: Targeted Risk Analysis (TRA) for flexible-frequency requirements

### Key Changes from v3.2.1 (for historical context only — do not assess against v3.2.1)
- Customized approach allowed as alternative to defined approach
- Enhanced authentication requirements (Req 8.3.6: MFA for all CDE access)
- Targeted risk analysis for flexible implementation
- New e-commerce and phishing protections (Req 6.4.3: script integrity)
- Roles and responsibilities explicitly defined per requirement

### Cardholder Data Environment (CDE) Scoping
- **CDE systems**: Directly store, process, or transmit cardholder data
- **Connected-to systems**: Connect to CDE but don't handle CHD directly
- **Out of scope**: Segmented, no connectivity to CDE
- **Scope reduction**: Tokenization, P2PE, network segmentation

---

## HIPAA

### Safeguard Categories

| Category | Key Rules | Technical Controls |
|----------|-----------|-------------------|
| **Administrative** (§164.308) | Risk analysis, workforce training, contingency planning, BAA management | Risk assessment tools, training records, DR plans |
| **Physical** (§164.310) | Facility access, workstation security, device controls | Physical access logs, device encryption, media disposal |
| **Technical** (§164.312) | Access control, audit controls, integrity controls, transmission security | Unique user IDs, emergency access, auto-logoff, encryption |
| **Breach Notification** (§164.400-414) | Individual notice (60 days), HHS notice, media notice (500+) | Breach detection, notification workflows |

### Technical Safeguard Details (§164.312)

| Standard | Implementation | Required/Addressable |
|----------|----------------|---------------------|
| Access control (a)(1) | Unique user IDs, emergency access, auto-logoff, encryption | Required |
| Audit controls (b) | Record and examine system activity | Required |
| Integrity (c)(1) | Mechanisms to authenticate ePHI | Required |
| Authentication (d) | Verify person seeking access to ePHI | Required |
| Transmission security (e)(1) | Integrity controls, encryption for ePHI in transit | Required |

### HIPAA Security Rule NPRM — Proposed Changes (2025-2026)
NPRM published January 6 2025 in the Federal Register. Comment period closed March 7 2025 (~5,000 comments received). Finalization tracked on OCR's regulatory agenda targeting May 2026; exact date not confirmed. The Trump administration has not withdrawn the NPRM. Factor proposed changes into readiness assessments now.

Key proposed changes:
- Eliminate required/addressable distinction — all safeguards become mandatory
- Mandate encryption at rest and in transit for all ePHI (no exceptions)
- Business associates must report security incidents to covered entities within 24 hours
- Mandatory technology asset inventory and network map (annual update)
- Vulnerability scanning every 6 months; penetration testing annually
- Anticipated compliance window: 60-day effective date + 180-day compliance period after final rule (~Q4 2026 if finalized May 2026)

Sources: [Federal Register NPRM (2025-01-06)](https://www.federalregister.gov/documents/2025/01/06/2024-30983/hipaa-security-rule-to-strengthen-the-cybersecurity-of-electronic-protected-health-information) | [HHS HIPAA Security Rule NPRM](https://www.hhs.gov/hipaa/for-professionals/security/hipaa-security-rule-nprm/index.html) | [Alston & Bird: Still on Track (Nov 2025)](https://www.alston.com/en/insights/publications/2025/11/hipaa-security-rule-overhaul)

### Business Associate Agreement (BAA)
- Required when sharing ePHI with third parties
- Must specify permitted uses, safeguards, breach reporting
- Cloud providers (AWS, GCP, Azure) offer BAA-eligible services
- Not all cloud services are BAA-eligible (verify per service)

---

## ISO 27001:2022

**ISO 27001:2013 certificates expired October 31 2025 — assessments against the 2013 version are audit failures.**
Sources: [ISO/IEC 27001:2022](https://www.iso.org/standard/27001) | [ISO/IEC 27002:2022 (controls guidance)](https://www.iso.org/standard/75652.html)

### Annex A Control Themes (93 controls)

| Theme | Count | Key Controls |
|-------|-------|--------------|
| **Organizational** (A.5) | 37 | A.5.1 InfoSec policies, A.5.9 Asset inventory, A.5.15 Access control, A.5.23 Cloud security, A.5.36 Compliance |
| **People** (A.6) | 8 | A.6.1 Screening, A.6.3 Awareness/training, A.6.5 Responsibilities after termination |
| **Physical** (A.7) | 14 | A.7.1 Physical perimeters, A.7.9 Off-premises security, A.7.14 Secure disposal |
| **Technological** (A.8) | 34 | A.8.1 User endpoint devices, A.8.5 Secure auth, A.8.9 Config management, A.8.12 DLP, A.8.24 Cryptography, A.8.25 SDLC, A.8.28 Secure coding |

### ISO 27001:2022 Key Changes from 2013
- Reduced from 114 to 93 controls (merged/reorganized)
- New controls: Threat intelligence (A.5.7), Cloud security (A.5.23), ICT readiness for business continuity (A.5.30), Data masking (A.8.11), DLP (A.8.12), Monitoring (A.8.16), Web filtering (A.8.23), Secure coding (A.8.28)
- 4 themes replace 14 domains

### Statement of Applicability (SoA)
- Lists all 93 Annex A controls
- States applicability (applicable/not applicable) with justification
- Links each control to risk treatment plan
- Evidence of implementation for applicable controls

---

## NIST Cybersecurity Framework (CSF) 2.0

Released February 26 2024 — first major revision in 10 years.
Source: [NIST CSF 2.0 Final](https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf) | [NIST announcement](https://www.nist.gov/news-events/news/2024/02/nist-releases-version-20-landmark-cybersecurity-framework)

### Six Core Functions (added Govern in 2.0)

| Function | Abbrev | Description |
|----------|--------|-------------|
| **Govern** (NEW) | GV | Cybersecurity risk governance — strategy, policy, roles, supply chain risk management |
| **Identify** | ID | Understand assets, risks, and organizational context |
| **Protect** | PR | Safeguards to limit or contain cybersecurity events |
| **Detect** | DE | Identify cybersecurity events |
| **Respond** | RS | Actions regarding detected cybersecurity events |
| **Recover** | RC | Restore capabilities impaired by cybersecurity events |

### Key Changes from CSF 1.1
- Govern function added (center of the framework wheel) — treats cybersecurity governance as enterprise risk management concern for senior leadership
- Expanded scope beyond critical infrastructure to all organizations
- Supply chain risk management (SCRM) elevated with dedicated Govern category (GV.SC)
- Tiers include separate descriptions for Cybersecurity Risk Governance (Govern) and Cybersecurity Risk Management (other 5 functions)
- CSF 2.0 profiles and implementation examples available at [nist.gov/cyberframework](https://www.nist.gov/cyberframework)

---

## NIST SP 800-171 Rev. 3 (2024)

Finalized May 14 2024. Governs protection of Controlled Unclassified Information (CUI) in nonfederal systems. Required for US federal contractors under DFARS 252.204-7012.
Source: [NIST SP 800-171r3 Final](https://csrc.nist.gov/pubs/sp/800/171/r3/final) | [NIST SP 800-171Ar3 (Assessment)](https://csrc.nist.gov/pubs/sp/800/171/a/r3/final)

### Key Changes from Rev. 2
- Aligned to NIST SP 800-53 Rev. 5 control structure
- Organization-Defined Parameters (ODP) introduced for tailoring requirements
- 17 security requirement families (consistent with SP 800-53r5)
- New tailoring criteria reduce redundancy
- SP 800-171r2 withdrawn; do not assess against it
