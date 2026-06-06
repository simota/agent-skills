# Threat Modeling Reference

**Purpose:** Detailed threat modeling methodologies for Breach.
**Read when:** Building or reviewing a threat model for a target system.

> **2026 framing addition.** Classical STRIDE / PASTA still apply, but the highest-impact 2026 threats live at two layers STRIDE was not built for. Add these as a sweep *after* the STRIDE pass before declaring the model complete:
>
> - **Agentic action surface (OWASP ASI 2026)** — when an AI agent takes real actions (file writes, API calls, MCP tools, browser automation), model the goal-hijack / tool-misuse / memory-poisoning / cascading-failure paths from `ai-red-teaming.md`. Anthropic's published `~78.6%` breach rate at 200 prompt-injection attempts against an unprotected GUI agent is the calibration point — assume the agent boundary is porous and the human-in-the-loop is load-bearing.
> - **Supply-chain pipeline (Mini Shai-Hulud family, 2026)** — model the build / publish / OIDC / SLSA-attestation chain as a *first-class* trust boundary. The 2026 in-the-wild worms abuse SLSA L3 attestations from hijacked `pull_request_target` workflows, so a model that trusts the attestation without verifying signer identity + branch lineage is incomplete. See `supply-chain-attack-design.md`.

---

## 1. STRIDE (Default)

Microsoft's threat classification framework. Best for component-level analysis.

### Process

1. **Diagram** — Create a data flow diagram (DFD) of the system
2. **Enumerate** — Walk each component/flow and apply STRIDE categories
3. **Prioritize** — Rate each threat by likelihood × impact
4. **Mitigate** — Map mitigations to each identified threat

### STRIDE Template

```markdown
## Threat Model: [System Name]

### System Overview
[Brief description and architecture diagram reference]

### Data Flow Diagram
[ASCII or reference to Canvas-generated diagram]

### Threats

#### [Component/Flow Name]

| # | Category | Threat | Likelihood | Impact | Risk | Mitigation |
|---|----------|--------|------------|--------|------|------------|
| T-01 | Spoofing | [Description] | H/M/L | H/M/L | [Score] | [Mitigation] |
| T-02 | Tampering | [Description] | H/M/L | H/M/L | [Score] | [Mitigation] |
| T-03 | Repudiation | [Description] | H/M/L | H/M/L | [Score] | [Mitigation] |
| T-04 | Info Disclosure | [Description] | H/M/L | H/M/L | [Score] | [Mitigation] |
| T-05 | Denial of Service | [Description] | H/M/L | H/M/L | [Score] | [Mitigation] |
| T-06 | Elevation | [Description] | H/M/L | H/M/L | [Score] | [Mitigation] |
```

### STRIDE Per-Element Mapping

| Element Type | Most Relevant STRIDE | Why |
|-------------|---------------------|-----|
| External Entity | S, R | Can impersonate or deny actions |
| Process | S, T, R, I, D, E | Full attack surface |
| Data Store | T, I, D | Data integrity and confidentiality |
| Data Flow | T, I, D | In-transit protections |
| Trust Boundary | S, E | Boundary crossing = privilege change |

---

## 2. PASTA (Process for Attack Simulation and Threat Analysis)

Risk-centric, 7-stage methodology. Best for business-aligned assessments.

### Seven Stages

| Stage | Name | Activities | Output |
|-------|------|------------|--------|
| 1 | Define Objectives | Align with business goals, compliance | Security objectives document |
| 2 | Define Technical Scope | Identify components, dependencies, APIs | Technical scope diagram |
| 3 | Application Decomposition | Map data flows, entry points, trust boundaries | DFD with trust boundaries |
| 4 | Threat Analysis | Identify threat agents and TTPs | Threat agent profiles |
| 5 | Vulnerability Analysis | Map known vulnerabilities to components | Vulnerability correlation matrix |
| 6 | Attack Modeling | Build attack trees and scenarios | Attack tree diagrams |
| 7 | Risk & Impact Analysis | Calculate risk scores, prioritize | Risk-ranked findings |

### PASTA Template

```markdown
## PASTA Threat Model: [System Name]

### Stage 1: Business Objectives
- Primary business function: [___]
- Regulatory requirements: [___]
- Risk tolerance: [High/Medium/Low]

### Stage 2: Technical Scope
- Components in scope: [___]
- External dependencies: [___]
- Data classification: [___]

### Stage 3: Decomposition
[DFD with trust boundaries]

### Stage 4: Threat Agents
| Agent | Motivation | Capability | Likelihood |
|-------|-----------|------------|------------|
| [External attacker] | [Financial] | [High] | [Medium] |
| [Insider] | [Disgruntlement] | [Medium] | [Low] |

### Stage 5: Vulnerability Correlation
| Component | Known Vulnerabilities | CVE/CWE | Exploitability |
|-----------|----------------------|---------|----------------|
| [___] | [___] | [___] | [___] |

### Stage 6: Attack Scenarios
[Attack trees or kill chain diagrams]

### Stage 7: Risk Ranking
| Finding | Likelihood | Impact | Risk Score | Priority |
|---------|-----------|--------|------------|----------|
| [___] | [___] | [___] | [___] | [___] |
```

---

## 3. MITRE ATT&CK Mapping

Map adversary behaviors to established technique taxonomy.

### Key Matrices

| Matrix | Use Case | Techniques |
|--------|----------|------------|
| Enterprise ATT&CK | Traditional IT/cloud | 14 tactics, 200+ techniques |
| Mobile ATT&CK | Mobile applications | 14 tactics, 100+ techniques |
| ICS ATT&CK | Industrial control | 12 tactics, 80+ techniques |
| ATLAS | AI/ML systems | AI-specific adversary techniques |

### ATT&CK Mapping Template

```markdown
## ATT&CK Map: [System Name]

### Relevant Techniques

| Tactic | Technique ID | Technique Name | Applicability | Test Priority |
|--------|-------------|----------------|---------------|---------------|
| Initial Access | T1190 | Exploit Public-Facing Application | [H/M/L] | [H/M/L] |
| Execution | T1059 | Command and Scripting Interpreter | [H/M/L] | [H/M/L] |
| Persistence | T1078 | Valid Accounts | [H/M/L] | [H/M/L] |
| Privilege Escalation | T1068 | Exploitation for Privilege Escalation | [H/M/L] | [H/M/L] |
| Defense Evasion | T1027 | Obfuscated Files or Information | [H/M/L] | [H/M/L] |
| Credential Access | T1110 | Brute Force | [H/M/L] | [H/M/L] |
| Lateral Movement | T1021 | Remote Services | [H/M/L] | [H/M/L] |
| Exfiltration | T1041 | Exfiltration Over C2 Channel | [H/M/L] | [H/M/L] |
```

---

## 4. Attack Trees

Goal-oriented decomposition. Best for analyzing specific attack objectives.

### Structure

```
[Root Goal: What the attacker wants to achieve]
├── [Sub-goal 1: Attack path A]
│   ├── [Leaf: Specific technique]  [Cost: L] [Difficulty: M]
│   └── [Leaf: Specific technique]  [Cost: M] [Difficulty: H]
├── [Sub-goal 2: Attack path B]
│   ├── [AND node: Requires both]
│   │   ├── [Leaf: Prerequisite 1]
│   │   └── [Leaf: Prerequisite 2]
│   └── [Leaf: Alternative technique]
└── [Sub-goal 3: Attack path C]
    └── [Leaf: Specific technique]  [Cost: H] [Difficulty: L]
```

### Annotations

| Attribute | Values | Purpose |
|-----------|--------|---------|
| Cost | Low / Medium / High | Attacker resource investment |
| Difficulty | Low / Medium / High | Technical skill required |
| Detection | Low / Medium / High | Likelihood of being caught |
| Impact | Low / Medium / High | Damage if successful |

---

## Framework Selection Guide

| Criteria | STRIDE | PASTA | ATT&CK | Attack Trees |
|----------|--------|-------|--------|--------------|
| Best for | Component-level threats | Business-aligned risk | Adversary emulation | Specific attack goals |
| Complexity | Low-Medium | High | Medium | Low |
| Output | Threat catalog | Risk-ranked findings | Technique coverage map | Goal decomposition |
| When to use | Default for most systems | Regulated/enterprise | Known adversary TTPs | Focused attack analysis |
