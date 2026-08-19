# Legal Review Handoffs

**Purpose:** Canonical payloads between Canon's legal-document recipes and implementation, privacy, native, prose, and specification owners.

All payloads follow `_common/HANDOFF.md`. Include reviewed finding IDs and verified authorities; do not include unnecessary personal data or confidential document text.

## Inbound

### CLOAK_TO_CANON_LEGAL_REVIEW

```yaml
from: Cloak
to: Canon
context:
  data_collected: ["<category>"]
  processing_purposes: ["<purpose>"]
  third_party_sharing: ["<recipient>"]
  retention_periods: {"<category>": "<period>"}
  consent_mechanisms: [{type: opt-in | opt-out | notice-only, scope: "<processing>"}]
  policy_version: "<version or date>"
ask:
  - Compare implementation facts with the privacy, cookie, and DPA text
  - Return contradictions and proposed wording
```

### NATIVE_TO_CANON_STORE_REVIEW

```yaml
from: Native
to: Canon
context:
  stores: [App_Store, Google_Play]
  jurisdictions: ["<country or region>"]
  features: [third_party_ai, external_purchase, iap, social_login, generated_content]
  draft_disclosures: ["<path or excerpt reference>"]
ask:
  - Review store disclosure coverage and policy alignment
  - Return finding IDs and proposed wording for each affected UI or metadata field
```

### SCRIBE_TO_CANON_LEGAL_REVIEW

```yaml
from: Scribe
to: Canon
context:
  specification_type: PRD | SRS | HLD
  legal_relevant_sections:
    - section: "<name>"
      content_summary: "<summary>"
      concern: "<legal or regulatory concern>"
  service_description: "<service>"
  target_jurisdictions: ["<jurisdiction>"]
ask:
  - Derive the required legal-document inventory and clause checklist
```

## Outbound

### CANON_TO_BUILDER_LEGAL_IMPLEMENTATION

```yaml
from: Canon
to: Builder
context:
  implementation_items:
    - id: "<finding id>"
      type: consent_flow | cookie_banner | age_gate | data_export | deletion_flow | opt_out | license_endpoint
      requirement: "<reviewed requirement>"
      authority: "<verified statute, article, or guideline>"
      priority: High | Medium | Low
      acceptance_criteria: ["<criterion>"]
constraints:
  - "Canon's review is reference information, not legal advice"
```

### CANON_TO_CLOAK_LEGAL_IMPLEMENTATION

```yaml
from: Canon
to: Cloak
context:
  findings: ["<privacy, DPA, cookie, telemetry, or consent finding id>"]
  required_behavior: ["<runtime/privacy behavior>"]
  policy_commitments: ["<clause reference, not raw confidential text>"]
ask:
  - Implement and evidence the privacy behavior promised by the reviewed documents
```

### CANON_TO_NATIVE_STORE_DISCLOSURE

```yaml
from: Canon
to: Native
context:
  findings:
    - id: "<finding id>"
      surface: consent_ui | legal_screen | app_store_metadata | play_console_metadata
      proposed_wording: "<reviewed wording>"
      authority: "<verified store rule or statute>"
ask:
  - Implement the disclosure without weakening provider, data, or choice specificity
```

### CANON_TO_PROSE_LEGAL_REWRITE

```yaml
from: Canon
to: Prose
context:
  document_type: "<ToS, privacy, DPA, EULA, cookie, or disclosure>"
  findings:
    - location: "<clause or field>"
      current_issue: jargon-heavy | ambiguous | verbose | inconsistent
      legal_meaning_to_preserve: "<meaning>"
  target_audience: "<audience>"
ask:
  - Improve readability without changing reviewed legal meaning
```

### CANON_TO_SCRIBE_LEGAL_REQUIREMENTS

```yaml
from: Canon
to: Scribe
context:
  requirements:
    - id: "<requirement id>"
      requirement: "<requirement>"
      authority: "<verified authority>"
      priority: High | Medium | Low
      implementation_scope: "<scope>"
  document_request: {type: PRD | checklist | test_spec, format: "<format>"}
```

## Handoff Hygiene

- Start the originating review with the not-legal-advice disclaimer; carry the boundary into every payload.
- Use finding IDs, authority citations, scope, and acceptance criteria instead of copying entire confidential clauses.
- Route legal opinions, contract negotiation, and enforceability decisions to qualified counsel.
- Route implementation by domain: privacy to Cloak, app UI/metadata to Native, business logic to Builder, readability to Prose, artifacts to Scribe.
