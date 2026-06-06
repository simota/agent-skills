# Handoff Templates

**Purpose:** Handoff templates between Vigil and partner agents.
**Read when:** Receiving input from or sending output to partner agents.

---

## Inbound Handoffs

### BREACH_TO_VIGIL_HANDOFF

```yaml
BREACH_TO_VIGIL_HANDOFF:
  attack_findings:
    - id: "[FIND-XXX]"
      technique: "[ATT&CK T-ID]"
      attack_path: "[Step-by-step exploitation]"
      detection_gap: "[What should have been caught]"
  purple_team_scenario:
    red_actions:
      - step: "[Red team action]"
        technique: "[T-ID]"
        expected_detection: "[What blue should see]"
  request:
    scope: "[detection_rule | coverage_mapping | purple_team_blue]"
```

### SENTINEL_TO_VIGIL_HANDOFF

```yaml
SENTINEL_TO_VIGIL_HANDOFF:
  static_findings:
    - type: "[Finding type]"
      severity: "[Critical/High/Medium/Low]"
      pattern: "[Code pattern detected]"
  request:
    scope: "[runtime_detection | monitoring_rule]"
    priority: "[Which findings need runtime detection]"
```

### TRIAGE_TO_VIGIL_HANDOFF

```yaml
TRIAGE_TO_VIGIL_HANDOFF:
  incident_pattern:
    type: "[Incident type]"
    root_cause: "[RCA summary]"
    detection_gap: "[How the incident could have been detected earlier]"
  request:
    scope: "[detection_rule | hunting_hypothesis]"
```

---

## Outbound Handoffs

### VIGIL_TO_SENTINEL_HANDOFF

```yaml
VIGIL_TO_SENTINEL_HANDOFF:
  detection_signatures:
    - pattern: "[Detection pattern for static scanning]"
      technique: "[ATT&CK T-ID]"
      description: "[What to detect in source code]"
      false_positive_guidance: "[Known benign patterns]"
```

### VIGIL_TO_RADAR_HANDOFF

```yaml
VIGIL_TO_RADAR_HANDOFF:
  detection_regression_tests:
    - test_name: "[Detection rule regression test]"
      rule_ref: "[DET-XXX]"
      test_type: "[true_positive | false_positive]"
      input_data: "[Sample log data]"
      expected: "[match | no_match]"
```

### VIGIL_TO_GEAR_HANDOFF

```yaml
VIGIL_TO_GEAR_HANDOFF:
  pipeline_config:
    type: "detection-as-code"
    ci_platform: "[github_actions | gitlab_ci | jenkins]"
    steps:
      - name: "lint"
        tool: "sigma-cli check"
      - name: "test"
        tool: "sigma-cli test"
      - name: "convert"
        tool: "sigma convert --target [siem]"
    repo_structure: "[Reference to detection-as-code.md repo layout]"
```

### VIGIL_TO_SCRIBE_HANDOFF

```yaml
VIGIL_TO_SCRIBE_HANDOFF:
  report_type: "[coverage_report | hunting_report | detection_maturity]"
  content:
    coverage_summary:
      total_techniques: "[X]"
      covered: "[Y]"
      coverage_rate: "[Z%]"
    priority_gaps: "[Top uncovered techniques]"
    rules_created: "[Count and list]"
    hunting_results: "[Hypotheses tested and outcomes]"
  format: "[standalone report | appendix to security doc]"
```

### VIGIL_TO_MEND_HANDOFF

```yaml
VIGIL_TO_MEND_HANDOFF:
  detection_triggered_runbooks:
    - trigger_rule: "[DET-XXX]"
      technique: "[ATT&CK T-ID]"
      auto_response:
        - "[Isolation step]"
        - "[Evidence collection step]"
        - "[Notification step]"
      escalation: "[When to escalate to Triage]"
```
