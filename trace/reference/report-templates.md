# Report Templates

Collection of output report templates for Trace.

> **2026 evidence discipline.** Vendor AI session summaries (FullStory, LogRocket Galileo, Mouseflow Mina AI) make it tempting to ship the agent's narrative verbatim as a finding. Don't. Trace reports must show **the human-verified evidence** behind every claim — `n` sessions reviewed, timestamps cited, the actual user action sequence reproduced from replay. Use the AI summary to *find* the moment; cite the *frame* the moment happened in. A report that reads "Galileo says users are frustrated at checkout" without the underlying replay timestamps is not a Trace deliverable — it is a forwarded vendor opinion.

---

## 1. Standard Analysis Report

```markdown
# Session Analysis Report

## Executive Summary

| Item | Value |
|------|-------|
| Analysis Period | [YYYY-MM-DD] to [YYYY-MM-DD] |
| Sessions Analyzed | [n] sessions |
| Target Flow | [Flow name] |
| Target Personas | [Persona list] |
| Overall Frustration Score | [Score] ([Low/Medium/High/Critical]) |

### Key Findings

1. **[Finding 1 Title]**: [One sentence description]
...
```
[Step 1] → [Step 2] → [Step 3] → [Conversion]
```

### Actual Common Paths

**Path A ([%]):** Success pattern
```
[Step 1] → [Step 2] → [Step 3] → [Conversion]
```

**Path B ([%]):** Abandonment pattern
```
[Step 1] → [Step 2] ↔ [Back] → [Exit]
```
- Estimated reason: [Reason]

**Path C ([%]):** Help-dependent pattern
```
[Step 1] → [Help] → [Step 2] → [Conversion]
```
- Observation: [Insight]

---

## Recommended Actions

| Priority | Action | Evidence | Handoff To | Expected Impact |
|----------|--------|----------|------------|-----------------|
| P0 | [Action] | [Data] | [Agent] | [Impact] |
| P1 | [Action] | [Data] | [Agent] | [Impact] |
| P2 | [Action] | [Data] | [Agent] | [Impact] |

---

## Appendix
...
```

---

## 2. Persona Validation Report

```markdown
# Persona Validation Report

## Validation Summary

| Item | Value |
|------|-------|
| Target Persona | [Persona name] |
| Persona ID | [ID] |
| Validation Period | [Period] |
| Sessions Analyzed | [n] |
| Overall Match Rate | [%] |

### Validation Conclusion

**[✅ VALIDATED / ⚠️ NEEDS_UPDATE / ❌ INVALID]**
...
```

---

## 3. Problem Investigation Report

```markdown
# Problem Investigation Report

## Investigation Overview

| Item | Value |
|------|-------|
| Investigation Trigger | [Pulse anomaly / Echo prediction / User report] |
| Problem Area | [Page/Flow] |
| Investigation Date | [Date] |
| Sessions Analyzed | [n] |

---

## Problem Identification

...
```
[User actions described chronologically]
1. [Time] - [Action]
2. [Time] - [Action] ← Problem occurs here
3. [Time] - [Frustration behavior]
4. [Time] - [Outcome (exit/success)]
```

**Session Examples:**
- Session #[ID]: [Description]
- Session #[ID]: [Description]

---

## Root Cause Analysis

### Hypotheses

| Hypothesis | Supporting Evidence | Contradicting Evidence | Confidence |
|------------|---------------------|------------------------|------------|
| [Hypothesis 1] | [Evidence] | [Evidence] | [High/Med/Low] |
| [Hypothesis 2] | [Evidence] | [Evidence] | [High/Med/Low] |
...
```

---

## 4. Quick Analysis Summary

Short report template for quick analysis.

```markdown
# Quick Analysis Summary

**Target:** [Flow/Page]
**Period:** [Period]
**Sessions:** [n]

## Top 3 Findings

1. 🔴 **[Finding 1]**: [One sentence] → [Recommended action]
2. 🟡 **[Finding 2]**: [One sentence] → [Recommended action]
3. 🟢 **[Finding 3]**: [One sentence] → [Recommended action]

## Frustration Scores

| Location | Score | Primary Signal |
...
```

---

## 5. Comparison Report

For A/B tests or before/after release comparisons.

```markdown
# Comparison Analysis Report

## Comparison Overview

| Item | Group A | Group B |
|------|---------|---------|
| Period | [Period] | [Period] |
| Sessions | [n] | [n] |
| Description | [Description] | [Description] |

---

## Key Metrics Comparison

| Metric | Group A | Group B | Difference | Significance |
...
```
