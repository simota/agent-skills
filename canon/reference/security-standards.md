# Security Standards Reference

Read for a security-compliance audit. This is a version-selection and evidence map, not a replacement for the selected standard's requirements.

## Select the authority before testing

Record `standard`, `edition`, `requirement_id`, `scope`, `source_url`, and `retrieved_at` for each finding. Use the edition required by the engagement, not whichever edition a model remembers. Pin a release/tag or a supplied standard copy; never combine chapter numbers from different editions. Offline work may use that pinned copy. Without it, mark clause-level compliance **unverified**, not compliant/non-compliant by inference.

| Audit subject | Canonical source | Verify at execution time |
|---|---|---|
| Web application risk classification | https://top10.owasp.org/2025/ | Edition and category; Top 10 classification is not a control-level certification. |
| Application verification | https://github.com/OWASP/ASVS | Selected release, exact requirement text/ID and applicable verification level; do not reuse ASVS 4.x chapter numbers for 5.x. |
| API risk classification | https://owasp.org/API-Security/editions/2023/en/0x11-t10/ | API edition, object/function/property authorization distinctions and endpoint applicability. |
| LLM application risk classification | https://genai.owasp.org/llm-top-10/ | Selected edition and exact IDs; keep LLM application and agentic-application taxonomies distinct. |
| Cybersecurity program | https://www.nist.gov/cyberframework | Framework version, Current/Target Profile and applicable outcomes; audit mechanics: `reference/nist-csf.md`. |
| Enterprise safeguards | https://www.cisecurity.org/controls | Version, safeguard and Implementation Group applicability; do not infer the group solely from organization size. |
| Secure development lifecycle | https://csrc.nist.gov/pubs/sp/800/218/final | Final versus draft publication, adopted revision and applicable practices; a draft is not an adopted obligation. |
| Weakness identifiers | https://cwe.mitre.org/ | Exact CWE definition and fit to observed behavior; annual rank does not determine finding severity. |
| Agent/skill supply chain | `_common/SECURITY.md` | Repository intake, capability and artifact-integrity gates; do not substitute an application Top 10 for the repository trust boundary. |

The OWASP Top 10:2025 mapping and ASVS release entry were verified on 2026-09-17. Other rows are canonical discovery entry points; verify the selected publication at use time. Legal/AI-regulatory applicability belongs in the regulatory/legal references, not in a cached security taxonomy.

## OWASP Top 10:2025

The compact mapping is retained to prevent the former mixed-edition classification failure. Use the canonical source above when selecting another edition.

| ID | Category | Evidence focus for this audit |
|---|---|---|
| A01:2025 | Broken Access Control | Server-side object/function/property and tenant checks; negative authorization tests. For SSRF, constrain schemes/destinations, revalidate redirects/resolution and enforce egress boundaries. |
| A02:2025 | Security Misconfiguration | Actual deployed configuration, exposed administration/debug surfaces, secret handling and effective browser/security policies. |
| A03:2025 | Software Supply Chain Failures | Dependency/build provenance, integrity verification, update/review controls and compromised-component response. |
| A04:2025 | Cryptographic Failures | Data classification, transport/storage protection, key lifecycle and approved primitives/parameters for the target policy. |
| A05:2025 | Injection | Untrusted input to interpreters, parameterization and context-appropriate output handling; demonstrate the reachable path, not a regex match alone. |
| A06:2025 | Insecure Design | Threat/abuse cases and missing controls in the design; distinguish design defects from implementation defects. |
| A07:2025 | Authentication Failures | Authentication/recovery/session lifecycle and abuse resistance; select password/authenticator requirements from the adopted standard. |
| A08:2025 | Software or Data Integrity Failures | Trust and integrity of updates, serialized data and execution inputs; verify before consumption. |
| A09:2025 | Security Logging and Alerting Failures | Relevant events, redaction, tamper resistance, alert delivery and exercised response; log presence alone is insufficient. |
| A10:2025 | Mishandling of Exceptional Conditions | Fail-closed authorization, resource/error boundaries, safe recovery and negative-path tests without sensitive-data exposure. |

## Evidence and crosswalk rules

- Preserve Canon's report/status/owner/retest contract in `SKILL.md` and `reference/compliance-templates.md`. A checklist, dependency scan or secure-looking snippet alone does not establish operating effectiveness.
- Separate the **observed defect**, its **risk category**, and each **normative control**. Cross-framework mappings are many-to-many; verify each cited clause rather than translating IDs mechanically.
- For ASVS, select the required level with the system's assurance target and record exclusions. Evaluate the exact adopted requirement; do not promote an example password length, header, algorithm or framework convention into a universal mandate.
- Capture revision/environment, test or configuration evidence, coverage limits and retest outcome. Distinguish absent evidence from evidence that a control failed.
- Do not execute destructive/exploitative checks outside the authorized scope. Hand implementation and active-testing work to the designated owner with the confirmed finding and constraints; redact secrets and personal data from evidence.
