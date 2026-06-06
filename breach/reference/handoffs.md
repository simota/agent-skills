# Handoff Templates

**Purpose:** Handoff templates between Breach and partner agents.
**Read when:** Receiving input from or sending output to partner agents.

---

## Inbound Handoffs

### SENTINEL_TO_BREACH_HANDOFF

```yaml
SENTINEL_TO_BREACH_HANDOFF:
  static_findings:
    - id: "[Finding ID]"
      type: "[hardcoded_secret | sql_injection | xss | etc.]"
      file: "[File path]"
      severity: "[Critical/High/Medium/Low]"
      description: "[What was found]"
  request:
    scope: "[attack_scenario | threat_model | full_assessment]"
    priority_findings: "[Which findings to target first]"
```

### PROBE_TO_BREACH_HANDOFF

```yaml
PROBE_TO_BREACH_HANDOFF:
  dast_findings:
    - id: "[Finding ID]"
      endpoint: "[URL/endpoint]"
      vulnerability: "[Type]"
      severity: "[Critical/High/Medium/Low]"
      exploitable: "[Yes/No/Unknown]"
  request:
    scope: "[exploitation_chain | lateral_movement | control_bypass]"
```

### CANON_TO_BREACH_HANDOFF

```yaml
CANON_TO_BREACH_HANDOFF:
  compliance_gaps:
    - standard: "[OWASP/CIS/NIST]"
      requirement: "[Requirement ID]"
      gap: "[What is missing]"
      risk_level: "[High/Medium/Low]"
  request:
    scope: "[attack_from_gaps | control_validation]"
```

### ORACLE_TO_BREACH_HANDOFF

```yaml
ORACLE_TO_BREACH_HANDOFF:
  ai_system:
    model_type: "[LLM/RAG/Agent/Multi-agent]"
    input_modalities: "[Text/Image/Audio]"
    tools_available: "[List of tools]"
    guardrails: "[Input filters, output validators]"
    architecture_notes: "[Key design decisions]"
  request:
    scope: "[prompt_injection | jailbreak | agentic_risks | full_ai_assessment]"
```

---

## Outbound Handoffs

### BREACH_TO_BUILDER_HANDOFF

```yaml
BREACH_TO_BUILDER_HANDOFF:
  findings:
    - id: "[FIND-XXX]"
      title: "[Vulnerability title]"
      severity: "[Critical/High/Medium/Low]"
      remediation:
        immediate: "[Quick fix specification]"
        long_term: "[Architectural fix specification]"
      affected_files: ["[file1]", "[file2]"]
      test_case: "[How to verify the fix]"
```

### BREACH_TO_SENTINEL_HANDOFF

```yaml
BREACH_TO_SENTINEL_HANDOFF:
  new_detection_rules:
    - pattern: "[Detection pattern]"
      attack_type: "[Attack category]"
      description: "[What to detect]"
      false_positive_guidance: "[How to reduce false positives]"
  attack_signatures:
    - signature: "[Pattern/regex]"
      context: "[Where to apply]"
```

### BREACH_TO_RADAR_HANDOFF

```yaml
BREACH_TO_RADAR_HANDOFF:
  security_regression_tests:
    - test_name: "[Descriptive test name]"
      finding_ref: "[FIND-XXX]"
      test_type: "[unit | integration | e2e]"
      input: "[Attack input]"
      expected_behavior: "[What should happen (blocked/sanitized/rejected)]"
      language: "[JS/Python/Go/etc.]"
```

### BREACH_TO_SCRIBE_HANDOFF

```yaml
BREACH_TO_SCRIBE_HANDOFF:
  report_type: "[threat_model | assessment | purple_team]"
  content:
    executive_summary: "[1-3 sentences]"
    findings_count: { critical: 0, high: 0, medium: 0, low: 0 }
    threat_model: "[Framework used and key threats]"
    findings: "[Full findings list]"
    recommendations: "[Prioritized remediation plan]"
  format: "[PRD appendix | standalone report | checklist]"
```

### BREACH_TO_MEND_HANDOFF

```yaml
BREACH_TO_MEND_HANDOFF:
  runbook_updates:
    - trigger: "[Attack pattern that should trigger response]"
      detection: "[How to detect this attack]"
      response_steps:
        - "[Step 1]"
        - "[Step 2]"
      rollback: "[How to recover if attack succeeds]"
```
