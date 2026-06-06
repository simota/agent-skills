# Handoff Templates

**Purpose:** Handoff format definitions between Clause and other agents.
**Read when:** Coordinating with another agent.

---

## Inbound Handoffs

### From Comply (COMPLY_TO_CLAUSE_HANDOFF)

Use when regulatory requirements must be reflected into legal documents.

```yaml
COMPLY_TO_CLAUSE_HANDOFF:
  source: Comply
  target: Clause
  context:
    regulatory_framework: "[SOC2 | PCI-DSS | HIPAA | ISO 27001 | ...]"
    requirements:
      - requirement_id: "[ID]"
        description: "[Requirement description]"
        impact_on_legal_docs: "[Impact on ToS / Privacy Policy]"
    target_documents:
      - "[Target document name]"
    priority: "[High | Medium | Low]"
  expected_output: "Proposed reflections into legal documents and a consistency report"
```

### From Cloak (CLOAK_TO_CLAUSE_HANDOFF)

Use when verifying alignment between privacy implementation and policy documents.

```yaml
CLOAK_TO_CLAUSE_HANDOFF:
  source: Cloak
  target: Clause
  context:
    privacy_implementation:
      data_collected: ["[Collected data category]"]
      processing_purposes: ["[Processing purpose]"]
      third_party_sharing: ["[Third-party recipient]"]
      retention_periods: {"[Data category]": "[Period]"}
    consent_mechanisms:
      - type: "[opt-in | opt-out | notice-only]"
        scope: "[Covered data / processing]"
    current_policy_version: "[Version / date]"
  expected_output: "Delta report against the policy document and a proposed fix"
```

### From Scribe (SCRIBE_TO_CLAUSE_HANDOFF)

Use when legal requirements must be extracted from a specification and reviewed.

```yaml
SCRIBE_TO_CLAUSE_HANDOFF:
  source: Scribe
  target: Clause
  context:
    specification_type: "[PRD | SRS | HLD]"
    legal_relevant_sections:
      - section: "[Section name]"
        content_summary: "[Summary]"
        legal_concern: "[Legal concern]"
    service_description: "[Service overview]"
    target_jurisdictions: ["[Jurisdiction]"]
  expected_output: "Legal-document requirements list and a checklist"
```

---

## Outbound Handoffs

### To Builder (CLAUSE_TO_BUILDER_HANDOFF)

Use when the review surfaces items that need implementation.

```yaml
CLAUSE_TO_BUILDER_HANDOFF:
  source: Clause
  target: Builder
  context:
    implementation_items:
      - id: "[IMPL-01]"
        type: "[consent_flow | cookie_banner | age_gate | data_export | deletion_flow | opt_out]"
        requirement: "[Legal requirement]"
        reference_finding: "[Finding ID in the review report]"
        reference_law: "[Referenced statute]"
        priority: "[High | Medium | Low]"
        acceptance_criteria:
          - "[Criterion 1]"
          - "[Criterion 2]"
    technical_constraints:
      - "[Constraint]"
  expected_output: "Implementation code and verification result"
```

### To Prose (CLAUSE_TO_PROSE_HANDOFF)

Use when the legal text needs plain-language or UX-writing improvements.

```yaml
CLAUSE_TO_PROSE_HANDOFF:
  source: Clause
  target: Prose
  context:
    document_type: "[Terms of Service | Privacy Policy | ...]"
    readability_issues:
      - location: "[Location in the document]"
        current_text: "[Current wording]"
        issue: "[Issue: jargon-heavy / ambiguous / verbose / ...]"
        target_audience: "[Target reader]"
    tone_requirements:
      formality: "[formal | semi-formal | casual]"
      language_level: "[expert | general | all-ages]"
    constraints:
      - "Maintain legal accuracy"
      - "[Other constraint]"
  expected_output: "Proposed plain-language wording"
```

### To Scribe (CLAUSE_TO_SCRIBE_HANDOFF)

Use when legal requirements should be organized into a specification document.

```yaml
CLAUSE_TO_SCRIBE_HANDOFF:
  source: Clause
  target: Scribe
  context:
    legal_requirements:
      - id: "[REQ-01]"
        requirement: "[Legal requirement]"
        source_law: "[Source statute]"
        priority: "[High | Medium | Low]"
        implementation_scope: "[Impact scope]"
    document_request:
      type: "[PRD | checklist | test_spec]"
      format: "[Preferred output format]"
  expected_output: "Specification document reflecting the legal requirements"
```
