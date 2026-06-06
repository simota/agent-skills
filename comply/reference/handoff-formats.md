# Comply Handoff Formats

## Inbound Handoffs

### SENTINEL_TO_COMPLY_HANDOFF

```yaml
SENTINEL_TO_COMPLY_HANDOFF:
  from: Sentinel
  findings:
    - id: "[finding ID]"
      type: "[vulnerability | misconfiguration | secret_exposure]"
      severity: "[critical | high | medium | low]"
      location: "[file:line or resource]"
      description: "[what was found]"
  request: "Map findings to regulatory requirements and assess compliance impact"
```

### CLOAK_TO_COMPLY_HANDOFF

```yaml
CLOAK_TO_COMPLY_HANDOFF:
  from: Cloak
  privacy_controls:
    - control: "[control name]"
      status: "[implemented | partial | missing]"
      data_types: ["PII", "ePHI", "cardholder_data"]
      regulations: ["GDPR", "CCPA", "HIPAA"]
  request: "Integrate privacy control status into broader compliance framework assessment"
```

### CANON_TO_COMPLY_HANDOFF

```yaml
CANON_TO_COMPLY_HANDOFF:
  from: Canon
  standards_context:
    - standard: "[OWASP | WCAG | ISO 25010]"
      findings: "[relevant technical standard findings]"
  request: "Interpret technical standard findings in regulatory compliance context"
```

### ATLAS_TO_COMPLY_HANDOFF

```yaml
ATLAS_TO_COMPLY_HANDOFF:
  from: Atlas
  architecture:
    components: ["[component list]"]
    data_flows: ["[data flow descriptions]"]
    trust_boundaries: ["[boundary descriptions]"]
  request: "Assess architecture against regulatory requirements and identify control gaps"
```

---

## Outbound Handoffs

### COMPLY_TO_BUILDER_HANDOFF

```yaml
COMPLY_TO_BUILDER_HANDOFF:
  from: Comply
  framework: "[SOC2 | PCI-DSS | HIPAA | ISO 27001]"
  requirement: "[specific requirement reference]"
  implementation_pattern:
    type: "[audit_logging | access_control | encryption | data_retention]"
    description: "[what to implement]"
    acceptance_criteria:
      - "[criterion 1]"
      - "[criterion 2]"
  priority: "[critical | high | medium | low]"
  evidence_needed: "[what auditor expects to verify]"
```

### COMPLY_TO_BEACON_HANDOFF

```yaml
COMPLY_TO_BEACON_HANDOFF:
  from: Comply
  monitoring_requirements:
    - control_id: "[regulatory control reference]"
      metric: "[what to monitor]"
      threshold: "[alert threshold]"
      frequency: "[check frequency]"
      alert_severity: "[critical | warning | info]"
  dashboard_requirements:
    - panel: "[compliance posture | control health | evidence freshness]"
      data_source: "[where to query]"
```

### COMPLY_TO_SCRIBE_HANDOFF

```yaml
COMPLY_TO_SCRIBE_HANDOFF:
  from: Comply
  document_type: "[policy | procedure | evidence_package | compliance_matrix]"
  framework: "[SOC2 | PCI-DSS | HIPAA | ISO 27001]"
  content:
    title: "[document title]"
    sections: ["[section list]"]
    control_references: ["[control IDs]"]
  audience: "[auditor | management | engineering]"
```

### COMPLY_TO_GEAR_HANDOFF

```yaml
COMPLY_TO_GEAR_HANDOFF:
  from: Comply
  ci_cd_gates:
    - gate_name: "[compliance gate name]"
      policy_file: "[OPA/Rego policy path]"
      enforcement: "[block | warn]"
      frameworks: ["SOC2", "PCI-DSS"]
      requirements: ["[specific requirement references]"]
  integration_point: "[pre-commit | pre-merge | pre-deploy | post-deploy]"
```
