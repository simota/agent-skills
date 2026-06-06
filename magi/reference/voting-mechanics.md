# Voting Mechanics

Detailed rules for Magi's confidence-weighted voting system, consensus patterns, and escalation protocols.

---

## Vote Structure

Each perspective casts a vote with:

```yaml
Vote:
  perspective: Logos | Pathos | Sophia    # Simple Mode
  engine: Claude | Codex | Gemini        # Engine Mode (alternative key)
  position: APPROVE | REJECT | ABSTAIN
  confidence: 0-100
  rationale: "One-line summary of reasoning"
  conditions: ["Optional conditions for approval"]
  dissent_note: "If outvoted, key concern to record"
```

**Mode-specific keys:** Simple Mode uses `perspective`, Engine Mode uses `engine`. Both share the same `position`, `confidence`, `rationale`, `conditions`, and `dissent_note` fields.

---

## Four Consensus Patterns

### Pattern 1: Unanimous (3-0)

**Definition:** All three perspectives agree on the same position.

```
╔═══════════════════════════════════════╗
║          UNANIMOUS VERDICT            ║
║                                       ║
║  Logos    → APPROVE (confidence: 82)  ║
║  Pathos   → APPROVE (confidence: 78)  ║
║  Sophia   → APPROVE (confidence: 85)  ║
║                                       ║
║  Weighted Confidence: 81.7            ║
║  Action: EXECUTE IMMEDIATELY          ║
╚═══════════════════════════════════════╝
```

**Rules:**
- Proceed with decision immediately
- No further deliberation needed
- Record weighted confidence as decision confidence
- If all approve with conditions, merge all conditions

**Weighted Confidence Calculation:**
```
weighted = (logos_conf + pathos_conf + sophia_conf) / 3
```

---

### Pattern 2: Majority (2-1)

**Definition:** Two perspectives agree, one dissents.

```
╔═══════════════════════════════════════╗
║          MAJORITY VERDICT             ║
║                                       ║
║  Logos    → APPROVE (confidence: 80)  ║
║  Pathos   → REJECT  (confidence: 72)  ║
║  Sophia   → APPROVE (confidence: 68)  ║
║                                       ║
║  Majority Confidence: 74.0            ║
║  Dissent: Pathos (conf: 72)           ║
║  Action: EXECUTE + RECORD DISSENT     ║
╚═══════════════════════════════════════╝
```

**Rules:**
- Proceed with majority decision
- **MUST record dissent** in the Risk Register
- If dissenter's confidence > majority's average confidence → flag as "Strong Dissent"
- If dissenter raises safety/security concerns → mandatory mitigation plan

**Strong Dissent Rule:**
```
IF dissenter.confidence > avg(majority.confidence)
THEN flag "STRONG DISSENT - Review recommended"
```

**Dissent Record Format:**
```yaml
Dissent:
  perspective: [Name]
  position: [APPROVE/REJECT]
  confidence: [Score]
  concern: "Key concern that was overruled"
  mitigation: "How the majority plans to address this concern"
  monitor: "What to watch for that would vindicate the dissenter"
```

---

### Pattern 3: Split (1-1-1)

**Definition:** All three perspectives reach different conclusions (or no two agree).

```
╔═══════════════════════════════════════╗
║           SPLIT VERDICT               ║
║                                       ║
║  Logos    → APPROVE  (confidence: 65) ║
║  Pathos   → REJECT   (confidence: 70) ║
║  Sophia   → ABSTAIN  (confidence: 45) ║
║                                       ║
║  No consensus reached.                ║
║  Action: PRESENT TRADE-OFFS TO USER   ║
╚═══════════════════════════════════════╝
```

**Rules:**
- **Do NOT proceed** without user input
- Present all three perspectives with their rationale
- Offer clear options mapped to each perspective's recommendation
- Include "Hybrid" option if perspectives can be partially reconciled
- Use `AskUserQuestion` tool for user decision

**Split Resolution Template:**
```yaml
questions:
  - question: "三視点で意見が分かれました。どの方針で進めますか？"
    header: "Split Vote"
    options:
      - label: "[Logos recommendation]"
        description: "技術的観点: [rationale] (信頼度: X)"
      - label: "[Pathos recommendation]"
        description: "人間中心的観点: [rationale] (信頼度: X)"
      - label: "[Sophia recommendation]"
        description: "戦略的観点: [rationale] (信頼度: X)"
    multiSelect: false
```

---

### Pattern 4: Unanimous Rejection (0-3)

**Definition:** All three perspectives reject the proposal.

```
╔═══════════════════════════════════════╗
║        UNANIMOUS REJECTION            ║
║                                       ║
║  Logos    → REJECT (confidence: 88)   ║
║  Pathos   → REJECT (confidence: 82)   ║
║  Sophia   → REJECT (confidence: 76)   ║
║                                       ║
║  Weighted Confidence: 82.0            ║
║  Action: BLOCK - State reasons        ║
╚═══════════════════════════════════════╝
```

**Rules:**
- **BLOCK** the proposed action
- Clearly state each perspective's reason for rejection
- Suggest alternative approaches if possible
- Only proceed if user explicitly overrides (with documented risk acceptance)

---

## ABSTAIN Rules

A perspective may abstain when:

1. **Domain irrelevance**: The decision has no bearing on their evaluation axis
2. **Insufficient information**: Cannot form a meaningful opinion (confidence < 30)
3. **Conflict of criteria**: Internal criteria conflict prevents a clear position

**ABSTAIN Impact on Voting:**
- ABSTAIN reduces the quorum: only voting perspectives count
- 2 APPROVE + 1 ABSTAIN = Majority (proceed)
- 1 APPROVE + 1 REJECT + 1 ABSTAIN = Split (escalate to user)
- 1 APPROVE + 2 ABSTAIN = Insufficient quorum (re-deliberate with more context)
- 2 REJECT + 1 ABSTAIN = Majority rejection (block)
- 3 ABSTAIN = Insufficient information (cannot decide, request more context)

---

## Confidence-Weighted Override

In special cases, confidence weighting may override simple majority:

### High-Confidence Minority Override

```
IF dissenter.confidence >= 90
AND avg(majority.confidence) < 60
THEN trigger "Confidence Override Review"
```

**Action:** Present both positions to user, highlighting the confidence disparity.
The high-confidence dissenter may be seeing something the uncertain majority is missing.

### Low-Confidence Majority Warning

```
IF avg(all.confidence) < 50
THEN append "LOW CONFIDENCE WARNING" to verdict
```

**Action:** Decision is provisional. Re-deliberate when more information is available.

---

## Escalation Conditions

| Condition | Level | Action |
|-----------|-------|--------|
| Split verdict (1-1-1) | L2 | Present options to user |
| Strong dissent on safety | L3 | Mandatory mitigation plan before proceeding |
| All confidence < 50 | L2 | Request more information, re-deliberate |
| Unanimous rejection | L3 | Block and present alternatives |
| User override of unanimous rejection | L4 | Document risk acceptance, proceed with monitoring |
| Confidence override triggered | L3 | Present to user with highlighted disparity |

---

## Re-Deliberation Protocol

### When to Re-Deliberate

1. New evidence changes a perspective's confidence by >20 points
2. User provides additional context after a split verdict
3. Implementation reveals invalid assumptions
4. External conditions change (timeline, budget, requirements)

### Re-Deliberation Process

```
1. IDENTIFY - Which perspective(s) need to re-evaluate
2. ISOLATE - Re-evaluate affected perspective(s) independently
3. RE-VOTE - Conduct new vote with updated assessments
4. COMPARE - Document what changed from original verdict
5. DELIVER - Present updated verdict with change history
```

### Maximum Re-Deliberation Rule

- **Max 2 re-deliberations** per decision
- After 2 re-deliberations without consensus, escalate to user with full deliberation history
- Exception: New factual evidence always warrants re-deliberation

---

## Deadlock Resolution

If the system cannot reach a decision after re-deliberation:

### Resolution Hierarchy

1. **Reframe**: Break the decision into smaller, more decidable sub-questions
2. **Timebound**: Set a deadline and use the highest-confidence perspective as default
3. **Defer**: Recommend a reversible intermediate step that preserves options
4. **Escalate**: Present full analysis to user as the final arbiter

### Reversibility Principle

When deadlocked, always prefer the more reversible option:

```
IF deadlocked AND option_A.reversible AND NOT option_B.reversible
THEN recommend option_A with monitoring plan
```

---

## 2-Engine Voting

When only one external engine is available (Claude + Codex or Claude + Gemini), the voting system adapts to 2-engine consensus patterns.

### 2-Engine Consensus Patterns

| Pattern | Votes | Action |
|---------|-------|--------|
| **2-0 (Unanimous)** | Both engines agree | Proceed with decision |
| **1-1 (Split)** | Engines disagree | Escalate to user (always) |
| **0-2 (Unanimous Rejection)** | Both engines reject | Block, present alternatives |

### 2-0: Unanimous Agreement

```
╔═══════════════════════════════════════╗
║       2-ENGINE UNANIMOUS              ║
║                                       ║
║  Claude   → APPROVE (confidence: 78)  ║
║  Codex    → APPROVE (confidence: 82)  ║
║                                       ║
║  Weighted Confidence: 80.0            ║
║  Action: EXECUTE                      ║
╚═══════════════════════════════════════╝
```

**Rules:**
- Proceed with decision
- Weighted confidence = average of 2 engine confidences
- Note reduced diversity in risk register

### 1-1: Split Decision

```
╔═══════════════════════════════════════╗
║       2-ENGINE SPLIT                  ║
║                                       ║
║  Claude   → APPROVE (confidence: 72)  ║
║  Gemini   → REJECT  (confidence: 68)  ║
║                                       ║
║  No consensus. Escalate to user.      ║
╚═══════════════════════════════════════╝
```

**Rules:**
- **Always escalate** to user (no majority possible with 2 engines)
- Present both positions with rationale
- Use `AskUserQuestion` tool for resolution
- If confidence gap > 30, highlight the higher-confidence position

### 0-2: Unanimous Rejection

```
╔═══════════════════════════════════════╗
║       2-ENGINE REJECTION              ║
║                                       ║
║  Claude   → REJECT (confidence: 85)   ║
║  Codex    → REJECT (confidence: 79)   ║
║                                       ║
║  Weighted Confidence: 82.0            ║
║  Action: BLOCK                        ║
╚═══════════════════════════════════════╝
```

**Rules:**
- Block proposed action
- Same rules as 3-engine 0-3 rejection
- Suggest alternative approaches

### ABSTAIN in 2-Engine Mode

- 1 vote + 1 ABSTAIN = Insufficient quorum (request more context or fall back to Simple Mode)
- 2 ABSTAIN = Insufficient information (fall back to Simple Mode)

### Weighted Confidence (2-Engine)

```
weighted = (engine_1_conf + engine_2_conf) / 2
```

Same override rules apply:
- High-confidence minority: N/A (only 2 engines, split always escalates)
- Low-confidence warning: if average < 50, append warning
