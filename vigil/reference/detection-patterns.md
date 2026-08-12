# Detection Patterns Reference

**Purpose:** Detection rule patterns organized by MITRE ATT&CK tactic.
**Read when:** Designing detection rules for specific techniques.

---

## Sigma Rule Structure

```yaml
# Required fields
title: "[Descriptive title]"
id: "[UUID or sequential ID]"
status: "[experimental | test | stable | deprecated]"
description: "[What this rule detects]"
references:
  - "[URL to ATT&CK technique or threat report]"

# Log source
logsource:
  product: "[windows | linux | aws | gcp | azure]"
  category: "[process_creation | network_connection | file_event | etc.]"
  service: "[sysmon | security | etc.]"

# Detection logic
detection:
  selection:
    FieldName|modifier:
      - "value1"
      - "value2"
  filter:
    FieldName: "benign_value"
  condition: "selection and not filter"

# Metadata
falsepositives:
  - "[Known benign scenario]"
level: "[informational | low | medium | high | critical]"
tags:
  - "attack.[tactic]"
  - "attack.[technique_id]"
```

### Sigma Modifiers

| Modifier | Purpose | Example |
|----------|---------|---------|
| `contains` | Substring match | `CommandLine\|contains: '-enc'` |
| `startswith` | Prefix match | `Image\|startswith: 'C:\Temp'` |
| `endswith` | Suffix match | `Image\|endswith: '\powershell.exe'` |
| `re` | Regex match | `CommandLine\|re: '.*[A-Za-z0-9+/]{50,}.*'` |
| `base64` | Base64 decode match | `CommandLine\|base64: 'Invoke-'` |
| `all` | All values must match | `selection\|all:` |

---

## Priority Detection Patterns by ATT&CK Tactic

### Initial Access (TA0001)

**T1190 — Exploit Public-Facing Application**
```yaml
title: Web Shell Detection via Process Creation
logsource:
  product: windows
  category: process_creation
detection:
  selection:
    ParentImage|endswith:
      - '\w3wp.exe'
      - '\httpd.exe'
      - '\nginx.exe'
    Image|endswith:
      - '\cmd.exe'
      - '\powershell.exe'
      - '\bash.exe'
  condition: selection
level: high
tags:
  - attack.initial_access
  - attack.t1190
```

### Execution (TA0002)

**T1059.001 — PowerShell**
```yaml
title: Suspicious PowerShell Download Cradle
logsource:
  product: windows
  category: process_creation
detection:
  selection:
    Image|endswith: '\powershell.exe'
    CommandLine|contains:
      - 'IEX'
      - 'Invoke-Expression'
      - 'Net.WebClient'
      - 'DownloadString'
      - 'DownloadFile'
  condition: selection
level: high
tags:
  - attack.execution
  - attack.t1059.001
```

### Persistence (TA0003)

**T1053.005 — Scheduled Task**
```yaml
title: Suspicious Scheduled Task Creation
logsource:
  product: windows
  service: security
  category: process_creation
detection:
  selection:
    Image|endswith: '\schtasks.exe'
    CommandLine|contains:
      - '/create'
    CommandLine|contains:
      - '\AppData\'
      - '\Temp\'
      - 'powershell'
      - 'cmd /c'
  condition: selection
level: medium
tags:
  - attack.persistence
  - attack.t1053.005
```

### Privilege Escalation (TA0004)

**T1548.002 — UAC Bypass**
```yaml
title: UAC Bypass via Event Viewer
logsource:
  product: windows
  category: process_creation
detection:
  selection:
    ParentImage|endswith: '\eventvwr.exe'
    Image|endswith:
      - '\powershell.exe'
      - '\cmd.exe'
  filter:
    Image|endswith: '\mmc.exe'
  condition: selection and not filter
level: high
tags:
  - attack.privilege_escalation
  - attack.t1548.002
```

### Lateral Movement (TA0008)

**T1021.002 — SMB/Windows Admin Shares**
```yaml
title: Remote Service via Admin Share
logsource:
  product: windows
  service: security
detection:
  selection:
    EventID: 5140
    ShareName|contains:
      - 'ADMIN$'
      - 'C$'
      - 'IPC$'
  filter:
    SubjectUserName|endswith: '$'
  condition: selection and not filter
level: medium
tags:
  - attack.lateral_movement
  - attack.t1021.002
```

### Exfiltration (TA0010)

**T1048 — Exfiltration Over Alternative Protocol**
```yaml
title: Large DNS TXT Query (Potential DNS Tunneling)
logsource:
  product: zeek
  service: dns
detection:
  selection:
    query_type: 'TXT'
    query|re: '.*[a-z0-9]{30,}\..*'
  condition: selection
level: medium
tags:
  - attack.exfiltration
  - attack.t1048
```

---

## YARA Rule Structure

```yara
rule [RuleName] : [tags]
{
    meta:
        author = "[Author]"
        description = "[What this rule detects]"
        reference = "[URL]"
        date = "[YYYY-MM-DD]"
        severity = "[high | medium | low]"

    strings:
        $s1 = "[string pattern]" ascii wide
        $s2 = { [hex pattern] }
        $r1 = /[regex pattern]/

    condition:
        uint16(0) == 0x5A4D and    // PE file
        filesize < 5MB and
        (2 of ($s*) or $r1)
}
```

### Authoring Engine: YARA-X is the 2026 Default

Default new YARA rules against **YARA-X 1.0.0+** (Rust rewrite, stable since 2025-06, ~`99%` rule compatibility with classic YARA). Classic YARA 4.x is in **maintenance mode** — only critical bug fixes land there; all new features ship to YARA-X exclusively. Practical implications when authoring:

- Heavy rules (large regex, deep loops) run measurably faster on YARA-X — the same rule that took seconds on YARA 4 finishes in milliseconds.
- Memory-safety is no longer a foot-gun; the Rust core eliminates the parser-side memory bugs that historically plagued YARA in long-running scanners.
- The parser and scanner are decoupled — easier to embed in DaC pipelines and to extend with custom modules.
- VirusTotal's Livehunt / Retrohunt pipelines have run at billions-of-files scale on YARA-X since 2025, so production readiness is no longer a question.

Migration rule: if the rule does not use one of the rare `~1%` of features YARA-X does not yet support, port it to YARA-X first and keep the original as a compatibility fallback only.

---

## Coverage Mapping Template

```markdown
## ATT&CK Coverage Map: [System Name]

| Tactic | Technique | T-ID | Detection Rule | Confidence | Status |
|--------|-----------|------|----------------|------------|--------|
| Initial Access | Exploit Public-Facing App | T1190 | DET-001 | High | Active |
| Execution | PowerShell | T1059.001 | DET-002 | High | Active |
| Persistence | Scheduled Task | T1053.005 | — | — | **GAP** |
| Priv Escalation | UAC Bypass | T1548.002 | DET-004 | Medium | Testing |

### Coverage Summary
- Total applicable techniques: [X]
- Techniques with active detection: [Y]
- Coverage rate: [Y/X = Z%]
- Priority gaps: [List top 5 uncovered techniques]
```

---

## Workflow Phase Templates

Full per-phase templates for the `ASSESS → DESIGN → BUILD → TEST → DEPLOY → HUNT` pipeline (SKILL.md `## Workflow` table). Read the relevant subsection when executing that phase.

### ASSESS (Coverage Analysis)

Map current detection coverage against MITRE ATT&CK and identify gaps.

```yaml
COVERAGE_ASSESSMENT:
  scope: "[Endpoint / Network / Cloud / AI]"
  framework: "MITRE ATT&CK [version]"
  current_detections:
    - rule_id: "[Existing rule ID]"
      technique: "[ATT&CK technique ID]"
      confidence: "[High/Medium/Low]"
  gaps:
    - technique: "[Uncovered technique ID]"
      tactic: "[Tactic name]"
      priority: "[Critical/High/Medium/Low]"
      rationale: "[Why this gap matters for this system]"
  coverage_score: "[X/Y techniques covered (Z%)]"
```

### DESIGN (Detection Rule Design)

Design detection rules for identified gaps or specific threats.

```yaml
DETECTION_RULE:
  id: "DET-001"
  name: "[Descriptive rule name]"
  technique: "[ATT&CK technique T-ID]"
  tactic: "[Tactic name]"
  description: "[What this rule detects and why]"
  log_source:
    product: "[sysmon / windows / linux / cloud]"
    service: "[service name]"
    category: "[process_creation / network / file / etc.]"
  detection_logic: "[Sigma/YARA/KQL rule body]"
  false_positive_sources:
    - "[Known benign scenario 1]"
    - "[Known benign scenario 2]"
  tuning_parameters:
    - parameter: "[threshold / exclusion list / time window]"
      default: "[value]"
      guidance: "[When to adjust]"
  severity: "[Critical / High / Medium / Low / Informational]"
  response_action: "[What SOC should do when triggered]"
```

### BUILD (Rule Implementation)

Write the actual detection rule in the selected format.

**Sigma v2.0+ example:**
```yaml
title: Suspicious PowerShell Encoded Command
id: det-001
status: experimental
description: Detects PowerShell execution with encoded commands
references:
  - https://attack.mitre.org/techniques/T1059/001/
logsource:
  product: windows
  category: process_creation
detection:
  selection:
    CommandLine|contains:
      - '-enc'
      - '-EncodedCommand'
    Image|endswith: '\powershell.exe'
  condition: selection
falsepositives:
  - Legitimate admin scripts using encoded commands
level: high
tags:
  - attack.execution
  - attack.t1059.001
```

**Sigma v2.0+ correlation types** — `event_count` (threshold on count), `value_count` (threshold on distinct field values), `temporal` (multiple rules co-occur within a timespan, any order), `temporal_ordered` (rules occur in a specific sequence within a timespan). Choose the type that matches the attack narrative; most brute-force-then-lateral chains need `temporal_ordered`, not just `event_count`.

```yaml
title: Brute Force Login Followed by Lateral Movement
name: brute_force_lateral
type: event_count
rules:
  - failed_login_rule
group-by:
  - SourceIP
timespan: 10m
condition:
  gte: 10
action: correlation
```

**Sigma Filter example (centralized FP exclusion, v2.1+):**
```yaml
title: Exclude IT Admin Encoded PowerShell
logsource:
  product: windows
  category: process_creation
filter:
  selection:
    User|contains:
      - 'svc_deploy'
      - 'admin_scripts'
    ParentImage|endswith: '\sccm.exe'
  condition: not selection
```

Use `pySigma` + `sigma-cli` for rule validation, conversion, and pipeline integration (legacy `sigmac` is deprecated).

### TEST (Validation)

Validate rules against sample data before deployment.

| Test Type | Purpose | Method |
|-----------|---------|--------|
| Syntax validation | Rule parses correctly | sigma-cli check (pySigma), YARA compile |
| True positive test | Rule fires on attack data | Replay known-bad logs |
| False positive test | Rule does not fire on benign data | Replay production sample |
| Performance test | Rule executes within time limits | Benchmark against log volume |
| Regression test | Existing rules still work | Automated test suite |

### DEPLOY (Detection-as-Code)

Design the CI/CD pipeline for detection rule management.

```
Git repo (detection rules)
  │
  ├─ PR created → Lint + syntax validation
  ├─ PR approved → True/false positive testing
  ├─ Merge to main → Deploy to staging SIEM
  └─ Release tag → Deploy to production SIEM
```

Pipeline templates → `detection-as-code.md`.

### HUNT (Threat Hunting)

Design hypothesis-driven threat hunting campaigns.

```yaml
HUNTING_HYPOTHESIS:
  id: "HUNT-001"
  hypothesis: "[Testable statement about potential threat activity]"
  technique_ref: "[ATT&CK technique T-ID]"
  rationale: "[Why this hypothesis is worth investigating]"
  data_sources:
    - "[Log source 1]"
    - "[Log source 2]"
  investigation_queries:
    - "[Query 1 with description]"
    - "[Query 2 with description]"
  success_criteria: "[What constitutes a confirmed finding]"
  outcome: "CONFIRMED | INCONCLUSIVE | NEGATIVE"
  detection_gap_found: "[Yes/No — if Yes, create new detection rule]"
```


## INTERACTION_TRIGGERS Question Templates (SKILL.md excerpt)

### DETECTION_SCOPE

```yaml
questions:
  - question: "What is the target detection domain?"
    header: "Domain"
    options:
      - label: "Endpoint (Recommended)"
        description: "Process execution, file operations, registry changes, network connections"
      - label: "Network"
        description: "Network traffic analysis, DNS queries, HTTP requests, lateral movement"
      - label: "Cloud / Container"
        description: "Cloud API calls, IAM events, container runtime, Kubernetes audit logs"
      - label: "AI/LLM system"
        description: "Prompt injection attempts, guardrail bypass, abnormal token usage, data exfiltration"
    multiSelect: true
```

### RULE_FORMAT

```yaml
questions:
  - question: "Which detection rule format should be used?"
    header: "Format"
    options:
      - label: "Sigma (Recommended)"
        description: "Platform-agnostic YAML rules, convertible to any SIEM query language"
      - label: "YARA"
        description: "File and memory pattern matching for malware detection and classification"
      - label: "Platform-specific (KQL/SPL/Lucene)"
        description: "Native query language for a specific SIEM platform"
    multiSelect: false
```

### COVERAGE_PRIORITY

```yaml
questions:
  - question: "Which MITRE ATT&CK tactic should be prioritized for detection coverage?"
    header: "Priority"
    options:
      - label: "Initial Access + Execution (Recommended)"
        description: "Catch attacks early: exploit attempts, phishing, command execution"
      - label: "Persistence + Privilege Escalation"
        description: "Detect attacker footholds: scheduled tasks, valid accounts, elevation"
      - label: "Lateral Movement + Exfiltration"
        description: "Detect spread and theft: remote services, data staging, C2 channels"
      - label: "Defense Evasion"
        description: "Detect stealth: log tampering, obfuscation, indicator removal"
    multiSelect: true
```

