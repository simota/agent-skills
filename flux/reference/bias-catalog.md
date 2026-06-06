# Bias Catalog

**Purpose:** Comprehensive cognitive bias taxonomy for AUDIT mode.
**Read when:** Executing BIAS_SCAN or DEBIASING phases.

---

## Bias Taxonomy by Category

### Decision-Making Biases

| Bias | Description | Detection Signal | Debiasing Technique |
|------|-------------|-----------------|---------------------|
| **Anchoring** | Over-relying on first information received | Decision tracks closely to initial estimate or first option presented | Independently generate estimates before seeing anchors; use multiple reference points |
| **Confirmation** | Seeking information that confirms existing beliefs | Only supporting evidence cited; disconfirming data absent or dismissed | Assign devil's advocate; require "evidence against" section in every proposal |
| **Sunk Cost** | Continuing because of past investment | "We've already spent X" used to justify further investment | Evaluate only future costs and benefits; ask "would we start this today?" |
| **Status Quo** | Preferring the current state over change | "It's always been this way"; change requires stronger justification than staying | Flip the frame: "if we were starting fresh, would we choose the current approach?" |
| **Framing Effect** | Different conclusions from same data presented differently | Decision changes when phrased as gain vs loss | Present data in multiple frames (gain/loss, absolute/relative, now/future) |

### Group Biases

| Bias | Description | Detection Signal | Debiasing Technique |
|------|-------------|-----------------|---------------------|
| **Groupthink** | Desire for conformity overrides critical evaluation | No dissent recorded; unanimous agreement without debate | Anonymous pre-voting; designated dissenter role; independent scoring |
| **HIPPO** | Highest Paid Person's Opinion dominates | Most senior person speaks first; others align | Reverse seniority speaking order; written submissions before discussion |
| **Bandwagon** | Adopting popular positions | "Everyone else is doing it" justification | Ask "what would we do if nobody else had done this?" |
| **Authority** | Deferring to authority without evaluation | "Expert X says" without examining evidence | Evaluate arguments independent of source; require evidence, not appeals |

### Estimation Biases

| Bias | Description | Detection Signal | Debiasing Technique |
|------|-------------|-----------------|---------------------|
| **Planning Fallacy** | Underestimating time, cost, and risk | Historical estimates consistently exceeded; best-case scenarios assumed | Use reference class forecasting; add 50% buffer; check historical actuals |
| **Optimism** | Overestimating positive outcomes | Risk section is empty or perfunctory; only success scenarios considered | Require pre-mortem analysis (→ Omen); mandate worst-case scenario |
| **Dunning-Kruger** | Confidence-competence mismatch | High confidence claims in unfamiliar domain; no acknowledged unknowns | Calibration questions; require team members to rate confidence with evidence |
| **Availability** | Overweighting recent/vivid events | Last incident dominates risk assessment; decisions swing with news cycle | Use base rates from historical data; time-weight inputs deliberately |

### Evaluation Biases

| Bias | Description | Detection Signal | Debiasing Technique |
|------|-------------|-----------------|---------------------|
| **Survivorship** | Learning only from successes | No failed project analysis; "company X succeeded by doing Y" | Systematically study failures; ask "how many tried this and failed?" |
| **IKEA Effect** | Overvaluing self-built solutions | NIH syndrome; rejecting better external alternatives | Blind evaluation: assess options without revealing origin |
| **Halo Effect** | One positive trait influences overall judgment | "They're great at X, so Y must be good too" | Evaluate each dimension independently with separate criteria |
| **Loss Aversion** | Fearing losses more than valuing equivalent gains | Asymmetric weighting of downsides; avoiding any risk for small potential losses | Quantify both gain and loss in same units; focus on expected value |
| **Endowment** | Overvaluing what we already have | Current solution rated higher simply because it's ours | Pre-commit to evaluation criteria before comparing |
| **Recency** | Overweighting recent events in judgment | Last quarter/sprint dominates evaluation; older data dismissed | Deliberately include multi-period data; weight by relevance, not recency |

---

## Bias Interaction Patterns

Biases rarely occur in isolation. Common compounds:

| Compound | Biases | Effect | Example |
|----------|--------|--------|---------|
| **Escalation Trap** | Sunk Cost + Confirmation + Optimism | Continue failing project, seeking confirming evidence while dismissing warning signs | "We're almost there" repeated for months |
| **Innovation Block** | Status Quo + IKEA Effect + Loss Aversion | Reject better external solution in favor of inferior internal one | Building custom when OSS solution exists |
| **Echo Chamber** | Groupthink + Confirmation + Authority | Team reinforces shared assumptions without external challenge | Unanimous "obvious" decisions that fail |
| **False Precision** | Anchoring + Planning Fallacy + Dunning-Kruger | Confident precise estimates in uncertain domains | "This will take exactly 3 sprints" with no basis |

---

## AUDIT Mode Procedure

### Phase 1: CLASSIFY
1. Identify the decision/plan/proposal to audit
2. Categorize: strategic / technical / resource / people / process
3. Note who is involved, what's at stake, and time pressure

### Phase 2: BIAS_SCAN
1. Walk through each bias category systematically
2. For each bias, check:
   - Is the detection signal present? (evidence)
   - How confident are we? (HIGH/MEDIUM/LOW)
   - How impactful if unaddressed? (HIGH/MEDIUM/LOW)
3. Check for compound patterns
4. Document findings with specific evidence, not speculation

### Phase 3: DEBIASING
1. For each detected bias, select the appropriate debiasing technique
2. Generate a debiased alternative framing
3. If compound pattern detected, address the root bias first
4. Propose process changes to prevent recurrence

### Phase 4: CRYSTALLIZE
1. Produce Bias Audit Report (see template below)
2. Include original decision framing vs debiased framing
3. Recommend next steps (proceed, revise, escalate to Magi)

---

## Bias Audit Report Template

```markdown
# Bias Audit Report: [Decision/Plan Name]

## Context
- **Decision:** [what is being decided]
- **Stakeholders:** [who is involved]
- **Stakes:** [what's at risk]
- **Time pressure:** [HIGH/MEDIUM/LOW]

## Detected Biases

| # | Bias | Evidence | Confidence | Impact | Debiasing |
|---|------|----------|------------|--------|-----------|
| 1 | [name] | [specific evidence] | [H/M/L] | [H/M/L] | [recommendation] |

## Compound Patterns
[If detected, describe the interaction]

## Original vs Debiased Framing

| Aspect | Original | Debiased |
|--------|----------|----------|
| [aspect] | [original framing] | [alternative framing] |

## Verdict
- **Bias severity:** [Critical / Significant / Minor / Clean]
- **Recommendation:** [Proceed / Revise / Escalate to Magi]
- **Process fix:** [suggestions to prevent recurrence]
```

---

## Real-World Bias Failure Cases

Reference cases for severity calibration:

| Case | Primary Bias | Cost | Lesson |
|------|-------------|------|--------|
| AOL-Time Warner merger | Confirmation + Optimism | $99B write-off | "Digital convergence" assumption never challenged |
| Kodak digital camera delay | Status Quo + Endowment | Company bankruptcy | Overvalued film business, undervalued digital disruption |
| Nokia smartphone transition | IKEA Effect + Groupthink | Market dominance lost | "Symbian is good enough" internal echo chamber |
| Healthcare.gov launch | Planning Fallacy + Authority | $1.7B+ | Expert estimates accepted without reference class data |
| Mars Climate Orbiter | Groupthink + Confirmation | $327M | Unit mismatch signals dismissed as instrument error |
