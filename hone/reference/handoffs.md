# Handoff Templates

**Purpose:** Templates for collaboration handoffs between Hone and other agents.
**Read when:** Hone needs to delegate or receive work from partner agents.

---

## Incoming Handoffs

### From User (Direct Request)

```yaml
HONE_AUDIT_REQUEST:
  target_cli: codex | agy | antigravity | claude-code | all  # default: all
  scope: full | model | trust | features | mcp | rules | agents | instructions | safety | extensions | permissions | commands | hooks
  config_path: "~/.codex/ | ~/.gemini/ | ~/.claude/"  # default: based on target_cli
  focus: ""  # optional specific concern
  depth: quick | standard | deep  # default: standard
```

### From Nexus (Task Context)

```yaml
_AGENT_CONTEXT:
  Role: Hone
  Task: "Audit and optimize Codex CLI configuration"
  Mode: AUTORUN
  Chain: [previous] → Hone → [next]
  Input:
    scope: [audit scope]
    concerns: [specific areas]
  Constraints:
    - [constraint 1]
  Expected_Output:
    - Audit report with proposals
```

### From Hearth (Environment Context)

```yaml
HEARTH_TO_HONE_HANDOFF:
  environment:
    os: [macOS/Linux]
    shell: [zsh/fish/bash]
    codex_version: [version]
    config_path: [path]
  target_cli: [codex | agy | antigravity | claude-code | all]
  context: "Environment setup complete, AI CLI config needs optimization"
  findings: [relevant Hearth findings about CLI tools]
```

---

## Outgoing Handoffs

### To Hearth (Shell Integration)

When Hone discovers that Codex config changes require shell environment updates:

```yaml
HONE_TO_HEARTH_HANDOFF:
  context: "Codex configuration changes may require shell/environment updates"
  findings:
    - type: [shell_alias | env_var | path_update]
      description: "[what needs to change]"
      current: "[current state]"
      proposed: "[desired state]"
  priority: P{0-3}
  action_needed: "[specific Hearth action]"
```

### To Judge (Review Config Verification)

When Hone identifies that Codex review settings need validation:

```yaml
HONE_TO_JUDGE_HANDOFF:
  context: "Codex review configuration has been audited"
  config_changes:
    - setting: "[config key]"
      before: "[old value]"
      after: "[proposed value]"
  verification_needed: "Confirm codex review behavior with proposed settings"
```

### To Arena (Exec Config Verification)

When Hone identifies that Codex exec settings need validation:

```yaml
HONE_TO_ARENA_HANDOFF:
  context: "Codex exec configuration has been audited"
  config_changes:
    - setting: "[config key]"
      before: "[old value]"
      after: "[proposed value]"
  verification_needed: "Confirm codex exec behavior with proposed settings"
```

### To Nexus (Results Return)

```yaml
HONE_TO_NEXUS_HANDOFF:
  summary: "[1-3 line audit summary]"
  proposals:
    p0_count: [n]
    p1_count: [n]
    p2_count: [n]
    p3_count: [n]
  critical_findings: ["[finding 1]", "[finding 2]"]
  next_action: "[recommended follow-up]"
  suggested_agent: "[Agent name if handoff needed]"
```

---

## Handoff Decision Matrix

| Finding type | Handoff to | When |
|-------------|------------|------|
| Shell/env changes needed | Hearth | Config requires PATH, alias, or env var changes |
| Review settings changed | Judge | `codex review` behavior may be affected |
| Exec settings changed | Arena | `codex exec` behavior may be affected |
| Security concern found | Sentinel | Plaintext secrets, permission issues |
| Complex multi-agent task | Nexus | Findings span multiple agent domains |
| No handoff needed | User | All proposals are self-contained |
