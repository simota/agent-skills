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
