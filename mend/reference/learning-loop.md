# Learning Loop — Pattern Extraction & Registration

Purpose: Read this file after incident resolution or failed remediation when updating the pattern catalog, registering a new pattern, or reviewing negative-pattern lessons.

## Contents

- Pattern extraction workflow
- Pattern quality metrics
- Negative pattern catalog
- Knowledge transfer
- Catalog maintenance schedule

How Mend learns from incidents to expand the remediation pattern catalog over time.

---

## Overview

```
Incident Resolved
  ↓
Triage Postmortem Published
  ↓
Mend Pattern Analysis
  ├── Existing pattern improved (update confidence factors, add variants)
  ├── New pattern candidate identified (draft → review → register)
  └── No actionable pattern (log insight only)
```

---

## Pattern Extraction Workflow

### Step 1: Postmortem Analysis (Multi-Stage Pipeline)

When Triage publishes a postmortem, Mend analyzes using a 4-stage pipeline. Single-pass analysis has 40%+ hallucination rates; staged processing reduces this to negligible levels.

#### Stage Pipeline

| Stage | Purpose | Output |
|-------|---------|--------|
| **1. Summarize** | Extract 5 dimensions from postmortem | Issue summary, root causes, impact, resolution, preventive actions |
| **2. Classify** | Identify explicit technology and category connections | Category tag (INFRA/APP/CONFIG/DEPLOY), affected technologies |
| **3. Analyze** | Produce root cause digest | 3-5 sentence summary capturing root causes and technological roles |
| **4. Synthesize** | Cross-reference with existing patterns | New pattern candidate, existing pattern update, or no actionable pattern |

Each stage processes independently, then results are aggregated ("map-fold" approach). This avoids the "lost in the middle" effect of large-context processing.

#### Extraction Fields

| Element | What to Extract |
|---------|-----------------|
| **Symptoms** | Observable indicators that preceded/accompanied the incident |
| **Root Cause** | Confirmed root cause from postmortem |
| **Fix Applied** | What remediation was actually effective |
| **Timeline** | Detection → diagnosis → fix → verification timing |
| **Time to Remediation** | Duration from detection to successful fix (for MTTR tracking) |
| **What Didn't Work** | Failed remediation attempts (negative patterns) |

#### Quality Controls

| Metric | Target | Action if Exceeded |
|--------|--------|--------------------|
| Hallucination rate | < 5% | Re-run with stricter prompts, increase human review |
| Surface attribution error | < 10% | Flag for manual verification |
| Numerical data accuracy | Verify against source | Never trust auto-extracted impact numbers without confirmation |

#### Human Verification Strategy

| Maturity Phase | Verification Rate | Criteria to Advance |
|----------------|-------------------|---------------------|
| Initial (first 20 extractions) | 100% manual review | All outputs verified correct |
| Growing (21-100 extractions) | 30-50% random sampling | Hallucination rate < 10% for 20 consecutive |
| Mature (100+ extractions) | 10-20% random sampling | Hallucination rate < 5% sustained |

### Step 2: Pattern Candidate Assessment

| Question | Answer → Action |
|----------|-----------------|
| Does this match an existing pattern? | Yes → Update existing pattern (Step 3A) |
| Is the root cause generalizable? | No → Log insight only, don't create pattern |
| Is the fix automatable? | No → Log as manual-only pattern for reference |
| Can symptoms be reliably detected? | No → Log insight, flag for Beacon improvement |
| Is the fix safely reversible? | No → Can only be T3/T4 pattern |

### Step 3A: Update Existing Pattern

When an incident matches an existing pattern:

1. **Adjust confidence factors** — Add new positive/negative signals discovered
2. **Add variant** — If symptoms differ slightly, add as variant of existing pattern
3. **Update remediation steps** — If a better fix was found, update primary steps
4. **Update verification criteria** — Add new checks discovered during verification
5. **Adjust safety tier** — If incident revealed different risk level, reclassify

### Step 3B: Register New Pattern

When a genuinely new pattern is discovered:

1. **Draft pattern** using standard template:

```markdown
### [CATEGORY]-[NNN]: [Title]

| Field | Value |
|-------|-------|
| **Symptoms** | [Observable indicators] |
| **Root Cause** | [Confirmed cause] |
| **Safety Tier** | [T1/T2/T3/T4] |
| **Confidence Factors** | [+/-% signals] |

**Remediation Steps:**
1. [Step] → Expected: [outcome]

**Verification:** [Success criteria]
```

2. **Review criteria** — New patterns must meet:
   - At least 1 confirmed incident as evidence
   - Reproducible symptoms (not one-off)
   - Automatable fix steps (not "call Bob")
   - Clear safety tier classification
   - Defined verification criteria

3. **Registration** — Add to `reference/remediation-patterns.md` in appropriate category

---

## Pattern Quality Metrics

Track pattern effectiveness over time:

| Metric | Target | Measurement |
|--------|--------|-------------|
| **Match accuracy** | ≥ 85% | Correct matches / total matches |
| **Fix success rate** | ≥ 90% | Successful remediations / attempted |
| **False positive rate** | < 10% | Incorrect matches / total matches |
| **MTTR per pattern** | Improving | Mean time from detection to fix, tracked per pattern_id |
| **Rollback rate** | < 15% | Rollbacks / total remediations |
| **Extraction hallucination rate** | < 5% | Incorrect facts in postmortem extraction / total extractions |

### Pattern Health Check

Periodically review patterns for:

| Check | Action |
|-------|--------|
| Pattern unused for > 90 days | Review — still relevant? Archive if not |
| Fix success rate < 70% | Review — update steps or reclassify |
| False positive rate > 20% | Review — tighten symptom matching |
| Safety tier mismatch | Reclassify based on recent incidents |

---

## Negative Pattern Catalog

Track what NOT to do — failed remediation attempts:

| Element | Purpose |
|---------|---------|
| **Anti-pattern** | What was tried and failed |
| **Why it failed** | Root cause of failure |
| **What to do instead** | Correct remediation approach |
| **Source incident** | Which incident taught this lesson |

Negative patterns serve as guardrails: if Mend's pattern matching suggests an action that appears in the negative catalog, it should flag the conflict and escalate.

---

## Knowledge Transfer

### To Triage
- Share pattern catalog updates for runbook refinement
- Report patterns that frequently need manual intervention (Triage should improve diagnosis)

### To Beacon
- Share detection gaps discovered during incidents (symptoms that weren't monitored)
- Recommend new alerts based on pattern symptoms

### To Builder
- Share patterns with high failure rates (may indicate code-level fixes needed)
- Report recurring issues that could be prevented with code changes

### From Triage
- Receive postmortems as primary learning input
- Receive updated runbooks incorporating lessons learned

---

## Catalog Maintenance Schedule

| Frequency | Action |
|-----------|--------|
| After each incident | Analyze for pattern updates/additions |
| Weekly | Review pattern health metrics |
| Monthly | Archive stale patterns, audit negative catalog |
| Quarterly | Full catalog review — accuracy, coverage, tier classification |
